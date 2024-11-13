import logging
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

from utils import tk_load_cfile
from kernel import Core
from docs import *


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log", "w", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


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
