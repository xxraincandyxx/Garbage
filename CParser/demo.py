import os
import re
import logging
import tkinter as tk
from dataclasses import dataclass
from tkinter import filedialog, scrolledtext
from typing import Optional, Union, Dict, List, Tuple, Any


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log", "w", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def load_cfile(filepath: str, verbose: bool = False) -> str:
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return ""
    with open(filepath, "r") as file:
        src_code = file.read()
        if not verbose:
            return re.sub(r"\s+", " ", src_code)
        return src_code


def tk_load_cfile(tk_inputs) -> None:
    fp = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
    if not os.path.exists(fp):
        raise FileNotFoundError(f"File {fp} is not found.")
    try:
        with open(fp, "r") as file:
            src_code = file.read()
            tk_inputs.delete("1.0", tk.END)
            tk_inputs.insert(tk.END, src_code)
    except Exception as e:
        logger.error(f"Failed to load file: {e}")


def shrink_code(code: str) -> str:
    return re.sub(r"\s+", " ", code)


class btNode:
    # deprecated
    def __init__(
        self,
        fct_name: str,
        condition: Optional[str] = None,
        return_val: bool = False,
    ) -> None:
        self.fct_name = fct_name
        self.condition = condition
        self.return_val = return_val
        self.left = None
        self.right = None

    def insert_left(self, fct_name, condition, return_val):
        self.left = btNode(fct_name, condition, return_val)
        return self.left

    def insert_right(self, fct_name, condition, return_val):
        self.right = btNode(fct_name, condition, return_val)
        return self.right


@dataclass
class Cache:
    fct_name: str
    fct_content: str
    type_name: str
    fct_args: Dict[str, str]


@dataclass
class Cache:
    fct_name: str
    fct_content: str
    type_name: str
    fct_args: Dict[str, str]


@dataclass
class DOCS_EN:
    _SWITCHER_: str = "切换到中文"
    _WHILE_: str = "While"
    _END_WHILE_: str = ""
    _IF_: str = "If"
    _ELSE_: str = "Else"
    _RETURN_: str = "Return"
    _FUNCTION_: str = "Function"
    _ARGUMENT_: str = "Argument"
    _VARIABLE_: str = "Variable"
    _AND_: str = "And"
    _AND_NOT_: str = "And Not"
    _TYPE_: str = "Type"
    _LOAD_FILE_: str = "Load File"
    _PARSE_CODE_: str = "Parse Code"
    _FUNCTION_NAME_: str = "Function Name"
    _FUNCTION_ARGS_: str = "Function Arguments"
    _FUNCTION_ARGS_TYPE_: str = "Function Arguments Type"
    _FUNCTION_ARGS_VALUE_: str = "Function Arguments Value"
    _FUNCTION_ARGS_VALUE_TYPE_: str = "Function Arguments Value Type"
    _FUNCTION_STATES_: str = "Function States"
    _FUNCTION_REFS_: str = "Function Reference"
    _ARGUMENT_RELAS_: str = "Arguments Relations"
    _NONE_: str = "None"


@dataclass
class DOCS_CN:
    _SWITCHER_: str = "Switch to English"
    _WHILE_: str = "当"
    _END_WHILE_: str = "时"
    _IF_: str = "如果"
    _ELSE_: str = "否则"
    _RETURN_: str = "返回"
    _FUNCTION_: str = "函数"
    _ARGUMENT_: str = "参数"
    _VARIABLE_: str = "变量"
    _AND_: str = "并且"
    _AND_NOT_: str = "并且不"
    _TYPE_: str = "类型"
    _LOAD_FILE_: str = "读取文件"
    _PARSE_CODE_: str = "分析代码"
    _FUNCTION_NAME_: str = "函数名"
    _FUNCTION_ARGS_: str = "函数参数"
    _FUNCTION_ARGS_TYPE_: str = "函数参数类型"
    _FUNCTION_ARGS_VALUE_: str = "函数参数值"
    _FUNCTION_ARGS_VALUE_TYPE_: str = "函数参数值类型"
    _FUNCTION_STATES_: str = "函数信息"
    _FUNCTION_REFS_: str = "函数调用"
    _ARGUMENT_RELAS_: str = "参数调用"
    _NONE_: str = "无"


class FunctionStateCache:
    def __init__(self):
        """Base Cache to store the state of the function

        fct_namme (str): function name
        fct_content (str): function content
        type_name (str): type of the function
        fct_args (Dict[str, Tuple[int, str]]): arguments of the function
            containing (arg_name, (arg_value, arg_type))
        conditions (List[List, List]): conditions needed to trigger the function
        """

        self.caches: Dict[str, Cache] = {}

    def __len__(self) -> int:
        return len(self.cache)

    def __getitem__(self, key: str) -> Cache:
        return self.caches[key] if key in self.caches else None

    def __iter__(self):
        return iter(self.caches.values())

    def update(
        self,
        fct_name: str,
        fct_content: Optional[str] = None,
        type_name: Optional[str] = None,
        fct_args: Optional[Dict[str, str]] = None,
    ) -> None:
        if fct_name in self.caches:
            cache: Cache = self.caches[fct_name]
            cache.fct_content = fct_content if fct_content is not None else cache.fct_content
            cache.type_name = type_name if type_name is not None else cache.type_name
            if fct_args is not None:
                cache.fct_args.update(fct_args)
        else:
            self.caches.update(
                {
                    fct_name: Cache(
                        fct_name,
                        fct_content,
                        type_name,
                        fct_args,
                    )
                }
            )

    def _output_(self) -> None:
        for cache in self.caches.values():
            print(f"Function Name: {getattr(cache, 'fct_name', None)}")
            print(f"Return Type: {getattr(cache, 'type_name', None)}")
            print(f"Arguments: {getattr(cache, 'fct_args', None)}")
            print(f"Conditions: {getattr(cache, 'conditions', None)}")
            print(f"Content: {getattr(cache, 'fct_content', None)}")
            print()


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


class Core:
    def __init__(
        self,
        DOCS: Union[DOCS_CN, DOCS_EN],
        src_code: Optional[Any] = None,
        tk_inputs: Optional[Any] = None,
        tk_outputs: Optional[Any] = None,
        output_fct_cache: Optional[Any] = None,
        output_walkthroughs: Optional[Any] = None,
        output_relatives: Optional[Any] = None,
    ) -> None:
        self.DOCS = DOCS
        self.src_code = tk_inputs.get("1.0", tk.END) if src_code is None else src_code
        logger.debug(f"src_code: {self.src_code}")
        if self.src_code is None or self.src_code == "" or self.src_code == "\n":
            logger.error(f"`code` got None ({self.src_code}).")
            raise ValueError(f"`code` got None ({self.src_code}).")
        self.output_fct_cache = output_fct_cache.get()
        self.output_walkthroughs = output_walkthroughs.get()
        self.output_relatives = output_relatives.get()
        self.tk_outputs = tk_outputs
        self.pwd = os.getcwd()

        # process
        self.caches = FunctionStateCache()
        self.parser = CodeParser(self.src_code, self.caches)

        self._output_()

    def _output_(self) -> None:
        self.tk_outputs.configure(state="normal")
        self.tk_outputs.delete("1.0", tk.END)

        outputs = self._preprocessing_before_output()
        outputs = "\n".join(outputs)

        # TODO
        self.tk_outputs.insert(tk.END, outputs)

        self.tk_outputs.configure(state="disable")

    def _format_fct_statements(self) -> List[str]:
        fct_state_caches = self.parser.fct_cache
        fct_state_lst = []
        for cache in fct_state_caches:
            args = (
                ", ".join([f"{dtype} {var}" for var, dtype in cache.fct_args.items()])
                if cache.fct_args is not None
                else f"{self.DOCS._NONE_}"
            )
            args_format = (
                ", ".join([f"{var} ({dtype})" for var, dtype in cache.fct_args.items()])
                if cache.fct_args is not None
                else f"{self.DOCS._NONE_}"
            )
            fct_state_lst.append(
                f"{cache.type_name} {cache.fct_name}({args if args != "" else f"{self.DOCS._NONE_}"}): {self.DOCS._FUNCTION_NAME_}: "
                f"{cache.fct_name}, {self.DOCS._ARGUMENT_}: {args_format if args_format != "" else f"{self.DOCS._NONE_}"}"
            )
        if fct_state_lst == []:
            fct_state_lst.append(f"{self.DOCS._NONE_}")
        return fct_state_lst

    def _preprocessing_before_output(self) -> List[str]:
        walkthroughs = self.parser.merged_walkthrough_lst
        conditions = self.parser.merged_conditions_lst
        relatives = self.parser.relatives_lst

        outputs = []
        outputs.append(f"{self.DOCS._FUNCTION_STATES_}: ")
        fct_state_lst = self._format_fct_statements()
        outputs.extend(fct_state_lst)
        outputs.append("")

        outputs.append(f"{self.DOCS._FUNCTION_REFS_}: ")
        for cond, call_path in zip(conditions, walkthroughs):
            if cond == "":
                outputs.append(call_path)
                continue

            cond = self._format_cond(cond)
            outputs.append(f"{self.DOCS._WHILE_} {cond} {self.DOCS._END_WHILE_}: {call_path}")
        outputs.append("")

        outputs.append(f"{self.DOCS._ARGUMENT_RELAS_}: ")
        if relatives == []:
            outputs.append(f"{self.DOCS._NONE_}")
        else:
            for rela in relatives:
                outputs.append(f"{rela}")
        return outputs

    def _format_cond(self, cond: str) -> str:
        cond_lst: List[str] = cond.split(" and ")
        for idx in range(len(cond_lst)):
            if "not" in cond_lst[idx]:
                logger.debug(f"prev cond batch: {cond_lst[idx]}")
                cond_lst[idx] = cond_lst[idx].replace("not ", "")
                if "<" in cond_lst[idx] or "<=" in cond_lst[idx]:
                    cond_lst[idx] = cond_lst[idx].replace("<", ">=").replace("<=", ">")
                    logger.debug(f"post cond batch: {cond_lst[idx]}")
                    continue
                if ">" in cond_lst[idx] or ">=" in cond_lst[idx]:
                    cond_lst[idx] = cond_lst[idx].replace(">", "<=").replace(">=", "<")
                    logger.debug(f"post cond batch: {cond_lst[idx]}")
                    continue
                if "==" in cond_lst[idx]:
                    cond_lst[idx] = cond_lst[idx].replace("==", "!=")
                else:
                    cond_lst[idx] = cond_lst[idx].replace("!=", "==")
                logger.debug(f"post cond batch: {cond_lst[idx]}")
        return f" {self.DOCS._AND_} ".join(cond_lst)


class GUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Petit Tool")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        # default language
        self.docs = DOCS_EN

        # input box
        self.inputs = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=80, height=20, font=("Arial", 12))
        self.inputs.grid(row=0, column=0, columnspan=4, padx=10, pady=5)

        # NOTE: output config deprecated, all set to True as default
        # output config check box
        self.output_fct_cache = tk.BooleanVar(value=True)
        self.output_walkthroughs = tk.BooleanVar(value=True)
        self.output_relatives = tk.BooleanVar(value=True)
        # tk.Checkbutton(frame, text="Output Function States", variable=output_fct_cache).grid(
        #     row=1, column=2, padx=5, pady=5
        # )
        # tk.Checkbutton(frame, text="Output Function Reference", variable=output_walkthroughs).grid(
        #     row=1, column=3, padx=5, pady=5
        # )
        # tk.Checkbutton(frame, text="Output Argument Relations", variable=output_relatives).grid(
        #     row=1, column=4, padx=5, pady=5
        # )

        # output box
        self.outputs = scrolledtext.ScrolledText(
            self.frame, wrap=tk.WORD, width=80, height=15, font=("Arial", 12), state="disabled"
        )
        self.outputs.grid(row=3, column=0, columnspan=4, padx=10, pady=5)

        # file loading button
        self.load_button = tk.Button(self.frame, text=self.docs._LOAD_FILE_, command=lambda: tk_load_cfile(self.inputs))
        self.load_button.grid(row=1, column=0)

        self.parse_button = tk.Button(
            self.frame,
            text="Parse Code",
            command=lambda: Core(
                DOCS=self.docs,
                src_code=None,
                tk_inputs=self.inputs,
                tk_outputs=self.outputs,
                output_fct_cache=self.output_fct_cache,
                output_relatives=self.output_relatives,
                output_walkthroughs=self.output_walkthroughs,
            ),
        )
        self.parse_button.grid(row=1, column=1)

        self.switch_button = tk.Button(self.frame, text=self.docs._SWITCHER_, command=self.switcher)
        self.switch_button.grid(row=1, column=3, pady=10)

        self.root.mainloop()

    def switcher(self) -> None:
        self.docs = DOCS_CN if self.docs == DOCS_EN else DOCS_EN

        # renew UI text
        self.load_button.config(text=self.docs._LOAD_FILE_)
        self.parse_button.config(text=self.docs._PARSE_CODE_)
        self.switch_button.config(text=self.docs._SWITCHER_)


if __name__ == "__main__":
    GUI()
