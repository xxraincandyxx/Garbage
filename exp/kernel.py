import os
import re
import logging
import tkinter as tk
from typing import Optional, List, Any

from parsing import CodeParser
from cache_utils import FunctionStateCache, Cache
from utils import load_cfile


logger = logging.getLogger(__name__)


class Core:
    def __init__(
        self,
        src_code: Optional[Any] = None,
        tk_inputs: Optional[Any] = None,
        tk_outputs: Optional[Any] = None,
        output_fct_cache: Optional[Any] = None,
        output_walkthroughs: Optional[Any] = None,
        output_relatives: Optional[Any] = None,
    ) -> None:
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
                else ""
            )
            args_format = (
                ", ".join([f"{var} ({dtype})" for var, dtype in cache.fct_args.items()])
                if cache.fct_args is not None
                else ""
            )
            fct_state_lst.append(
                f"{cache.type_name} {cache.fct_name}({args}): Function Name: {cache.fct_name}, Arguments: {args_format}"
            )
        if fct_state_lst == []:
            fct_state_lst.append("None")
        return fct_state_lst

    def _preprocessing_before_output(self) -> List[str]:
        walkthroughs = self.parser.merged_walkthrough_lst
        conditions = self.parser.merged_conditions_lst
        relatives = self.parser.relatives_lst

        outputs = []
        outputs.append("Function States: ")
        fct_state_lst = self._format_fct_statements()
        outputs.extend(fct_state_lst)
        outputs.append("")

        outputs.append("Function Reference: ")
        for cond, call_path in zip(conditions, walkthroughs):
            if cond == "":
                outputs.append(call_path)
                continue
            outputs.append(f"When {cond}: {call_path}")
        outputs.append("")

        outputs.append("Arguments Relations: ")
        if relatives == []:
            outputs.append("None")
        else:
            for rela in relatives:
                outputs.append(f"{rela}")
        return outputs
