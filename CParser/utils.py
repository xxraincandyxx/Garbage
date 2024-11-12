import os
import re
import logging
import tkinter as tk
from tkinter import filedialog
from typing import Optional


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
