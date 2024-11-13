import os
import re
import logging
import tkinter as tk
from typing import Optional, Union, List, Any

from cache_utils import FunctionStateCache
from parsing import CodeParser
from utils import load_cfile
from docs import *


logger = logging.getLogger(__name__)


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
