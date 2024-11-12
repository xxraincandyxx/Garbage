import logging
import tkinter as tk
from tkinter import scrolledtext

from utils import tk_load_cfile
from kernel import Core


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log", "w", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def main():
    root = tk.Tk()
    root.title("Petit Tool")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    # input box
    inputs = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20, font=("Arial", 12))
    inputs.grid(row=0, column=0, columnspan=4, padx=10, pady=5)

    # NOTE: output config deprecated, all set to True as default
    # output config check box
    output_fct_cache = tk.BooleanVar(value=True)
    output_walkthroughs = tk.BooleanVar(value=True)
    output_relatives = tk.BooleanVar(value=True)
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
    outputs = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=15, font=("Arial", 12), state="disabled")
    outputs.grid(row=3, column=0, columnspan=4, padx=10, pady=5)

    # file loading button
    load_button = tk.Button(frame, text="Load File", command=lambda: tk_load_cfile(inputs))
    load_button.grid(row=1, column=0)

    parse_button = tk.Button(
        frame,
        text="Parse Code",
        command=lambda: Core(
            src_code=None,
            tk_inputs=inputs,
            tk_outputs=outputs,
            output_fct_cache=output_fct_cache,
            output_relatives=output_relatives,
            output_walkthroughs=output_walkthroughs,
        ),
    )
    parse_button.grid(row=1, column=1)

    root.mainloop()


if __name__ == "__main__":
    main()
