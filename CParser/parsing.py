import os
import re
import logging
from typing import Dict, List, Tuple

from utils import load_cfile, shrink_code
from cache_utils import FunctionStateCache, Cache


logger = logging.getLogger(__name__)


class CodeParser:
    def __init__(
        self,
        src_code: str,
        fct_cache: FunctionStateCache,
    ) -> None:
        self.src_code = src_code
        self.fct_cache = fct_cache

        self.walkthrough_lst = []
        self.conditions_lst = []
        self.relatives_lst = []

        self.patterns = {
            # if": r"\bif\s*\(.*?\)\s*{.*?}",
            "if": r"if\s*\([^)]*\)\s*{[^{}]*(?:{[^{}]*}[^{}]*)*}",
            "else": r"\belse\s*{.*?}",
            "assign_fct": r"(?:(?:int|float|double|char|void|long|short|unsigned|signed)\s+)?(\w+)\s*=\s*(\w+)\s*\(",
            "call_fct": r"(\w+)\s*\((.*?)\)",
            "statement": r"\b\w+\s+.*?;",
        }

        self.variable_pattern = re.compile(r"\b(int|float|double|char)\s+(\w+)\s*=\s*([^;]+);")
        self.function_pattern = re.compile(r"\b(\w+)\s+(\w+)\s*\((.*?)\)\s*{")
        self.argument_pattern = re.compile(r"\b(\w+)\s+(\w+)(?:\s*,\s*)?")
        self.call_fct_pattern = re.compile(r"\b(\w+)\s*\([^)]*\)")
        self.condition_pattern = re.compile(r"if\s*\(([^)]*)\)")
        self.return_pattern = re.compile(r"return ([^\n;]+);")

        # Group Number | Capture content
        #            1 | if block
        #            2 | else block
        #            3 | assign function statement
        #            4 | -- assigned variable by function
        #            5 | -- assigning function name
        #            6 | call function statement
        #            7 | -- called function name
        #            8 | -- called function arguments
        #            9 | statement -- return
        self.combined_pattern = re.compile(
            f"({self.patterns['if']})|({self.patterns['else']})|({self.patterns['assign_fct']})"
            f"|({self.patterns['call_fct']})|({self.patterns['statement']})",
            re.DOTALL,
        )

        self.control_keywords = {"if", "while", "for", "switch"}

        # deprecated
        # self.contents_pattern = re.compile(r"\b\w+\s+\w+\s*\([^)]*\)\s*{([^{}]*(?:{[^{}]*}[^{}]*)*)}")
        # self.contents_pattern = re.compile(r'(?s)(?<=\{)(.*?)(?=\}(?:\s*\n*[^\}]|$))')
        # self.split_ie_pattern = re.compile(
        #     r"(if\s*\([^)]*\)\s*{[^{}]*(?:{[^{}]*}[^{}]*)*}\s*else\s*{[^{}]*(?:{[^{}]*}[^{}]*)*})"
        # )
        # self.ie_block_pattern = re.compile(
        #     r"if\s*\(([^)]*)\)\s*({[^{}]*(?:{[^{}]*}[^{}]*)*})\s*else\s*({[^{}]*(?:{[^{}]*}[^{}]*)*})"
        # )

        contents_lst = self._extract_all_function_bodies(src_code)
        for idx, match in enumerate(self.function_pattern.finditer(src_code)):
            return_type, name, args = match.groups()
            content = contents_lst[idx]
            re.findall(self.argument_pattern, args)
            args = re.findall(self.argument_pattern, args)
            fct_args = self._extract_args(args)
            logger.debug(
                f"\nFunction Name: {name} \nReturn Type: {return_type} \n"
                f"Arguments: {fct_args} \nContent: \n{content}\n"
            )
            self.fct_cache.update(
                fct_name=name,
                fct_content=content,
                type_name=return_type,
                fct_args=fct_args,
            )

        self._inner_parse()
        logger.debug(f"INNER PARSING OUTPUT:")
        logger.debug(f"walkthrough list: {self.walkthrough_lst}")
        logger.debug(f"conditions  list: {self.conditions_lst}")
        logger.debug(f"relatives   list: {self.relatives_lst}")

        self.merged_walkthrough_lst = []
        self.merged_conditions_lst = []

        self._merge_original_res()
        logger.debug("######################## REAL ANSWER BELOW ########################")
        logger.debug(f"walkthrough list: {self.merged_walkthrough_lst}")
        logger.debug(f"conditions  list: {self.merged_conditions_lst}")
        logger.debug(f"relatives   list: {self.relatives_lst}")

        # TODO

    def _inner_parse(self) -> None:
        main_cache: Cache = self.fct_cache["main"]
        if not main_cache:
            raise RuntimeError("`main` function not found.")

        def dps(fct_path: str, content: str, conditions: str) -> None:
            for match in self.combined_pattern.finditer(content):
                # logger.debug(f"DEBUG MATCH: {match}")

                if match.group(1):  # if block
                    if_block = match.group(1)
                    logger.debug(f"if block: {if_block.strip()}")
                    if_block = shrink_code(str(if_block))
                    condition = self.condition_pattern.search(if_block)
                    condition = condition.group(1) if condition else None
                    if_body = self.extract_if_block(if_block)
                    logger.debug(f"if body: {if_body}")
                    dps(fct_path, if_body, f"{conditions} and {condition}")
                    continue

                if match.group(2):  # else block
                    else_block = match.group(2)
                    logger.debug(f"else block: {else_block.strip()}")
                    else_block = shrink_code(str(else_block))
                    condition = self.condition_pattern.search(if_block) if if_block is not None else None
                    condition = condition.group(1) if condition else None
                    else_body = self.extract_else_block(else_block)
                    logger.debug(f"else body: {else_body}")
                    dps(fct_path, else_body, f"{conditions} and not {condition}")
                    continue

                if match.group(3):  # assign function, occupies 3 groups
                    assign_block = match.group(3)
                    logger.debug(f"assign func: {assign_block.strip()}")
                    assign_match = re.findall(self.patterns["assign_fct"], assign_block)
                    if assign_match:
                        val, func_name = assign_match[0]
                        logger.debug(f"assign function: {val} from {func_name}")
                        cur_fct_name = fct_path.split(" -> ")[-1]
                        self.relatives_lst.append(f"<{cur_fct_name}(), {val}> = <{func_name}(), return value>")

                        # call function
                        call_fct_cache = self.fct_cache[func_name]
                        if call_fct_cache is None:
                            logger.warning(f"Failed to find function state `{func_name}`.")
                        else:
                            dps(fct_path + " -> " + func_name, call_fct_cache.fct_content, conditions)
                        continue

                if match.group(6):  # call function, occupies 3 groups
                    call_block = match.group(6)
                    logger.debug(f"call func: {call_block.strip()}")
                    call_match = re.findall(self.patterns["call_fct"], call_block)
                    if call_match:
                        call_fct_name, var = call_match[0]
                        logger.debug(f"call function: {call_fct_name}")

                        call_fct_cache = self.fct_cache[call_fct_name]
                        if call_fct_cache is None:
                            logger.warning(f"Failed to find function state `{call_fct_name}`.")
                        else:
                            # fast replace
                            if call_fct_cache.fct_args != {}:
                                arg = list(call_fct_cache.fct_args.keys())[0]
                                logger.debug(f"args: var - {var}  arg - {arg}")
                                self._fast_replace(call_fct_cache.fct_name, var, arg)
                                logger.debug(f"replaced content preview: {call_fct_cache.fct_content}")

                            dps(fct_path + " -> " + call_fct_name, call_fct_cache.fct_content, conditions)
                        continue

                # return value or none
                if match.group(9):
                    norm_block = match.group(9)
                    logger.debug(f"statement: {norm_block.strip()}")
                    return_match = re.search(self.return_pattern, norm_block)
                    if not return_match:
                        continue
                    return_value = return_match.group(1)
                    logger.debug(f"return: {return_value}\n")

                    # append result
                    self.walkthrough_lst.append(fct_path.split(" -> "))
                    self.conditions_lst.append(conditions)
                    return
                else:
                    logger.warning(f"Failed to classify code: {match}")

            # end for function content
            self.walkthrough_lst.append(fct_path.split(" -> "))
            self.conditions_lst.append(conditions)
            return

        dps("main", main_cache.fct_content, "")

    def output_caches(self) -> None:
        self.fct_cache._output_()

    def _merge_original_res(self) -> None:  # TODO
        self.merged_conditions_lst = list(set(self.conditions_lst))
        for cond in self.merged_conditions_lst:
            fct_name_set = set([])
            fct_name_lst = []
            for idx, fct_path_lst in enumerate(self.walkthrough_lst):
                if not self.conditions_lst[idx] in cond:
                    continue
                for fn in fct_path_lst:
                    if fn in fct_name_set:
                        continue
                    fct_name_lst.append(fn)
                    fct_name_set.add(fn)
            self.merged_walkthrough_lst.append(" -> ".join(fct_name_lst))

        for idx in range(len(self.merged_conditions_lst)):
            if self.merged_conditions_lst[idx].startswith(" and "):
                self.merged_conditions_lst[idx] = self.merged_conditions_lst[idx].replace(" and ", "", 1)

    # deprecated
    def _split_code(self, code):
        match = self.split_ie_pattern.search(code)
        if match:
            if_else_block = match.group(1)
            start, end = match.span()
            before_block = code[:start].strip()
            after_block = code[end:].strip()
            return {
                "before": before_block,
                "if_else": if_else_block,
                "after": after_block,
            }
        return None

    def _extract_all_function_bodies(self, code):
        pattern = r"(?s)(\w+\s*\([^)]*\)\s*{)((?:[^{}]|{(?:[^{}]|{[^{}]*})*})*})"
        matches = re.finditer(pattern, code)
        bodies = []

        for match in matches:
            full_match = match.group(2)
            body = full_match[1:-1].strip()
            bodies.append(body)

        return bodies

    def extract_if_block(self, code):
        # Pattern for if block content
        if_pattern = r"if\s*\([^)]*\)\s*{([^{}]*(?:{[^{}]*}[^{}]*)*)}"
        match = re.search(if_pattern, code)
        return match.group(1).strip() if match else ""

    def extract_else_block(self, code):
        # Pattern for else block content
        else_pattern = r"else\s*{([^{}]*(?:{[^{}]*}[^{}]*)*)}"
        match = re.search(else_pattern, code)
        return match.group(1).strip() if match else ""

    def get_function_calls(self, content: str) -> List[str]:
        return re.findall(self.call_fct_pattern, content)

    def _extract_args(self, args: List[Tuple]) -> Dict:
        args_dict = {}
        for type_name, var in args:
            args_dict[var] = type_name
        return args_dict

    def extract_function_arguments(self, function_call):
        # Pattern to match arguments inside parentheses
        pattern = r"\w+\s*\((.*?)\)"
        match = re.search(pattern, function_call)
        return match.group(1) if match else ""

    def get_argument_list(self, function_call):
        args_string = self.extract_function_arguments(function_call)
        # Handle nested parentheses and commas within strings
        pattern = r',\s*(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$)'
        return [arg.strip() for arg in re.split(pattern, args_string)] if args_string else []

    def _fast_replace(self, fct_name: str, var: str, arg: str) -> None:
        self.fct_cache[fct_name].fct_content = (
            self.fct_cache[fct_name].fct_content.replace(f"({arg}", f"({var}").replace(f"{arg})", f"{var})")
        )
