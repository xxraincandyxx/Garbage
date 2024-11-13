import tkinter as tk
from tkinter import ttk


class LanguageSwitcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Switcher Demo")

        # Dictionary to store text in different languages
        self.languages = {
            "en": {"welcome": "Welcome!", "button": "Switch to Spanish", "message": "Hello World"},
            "es": {"welcome": "¡Bienvenidos!", "button": "Cambiar a Inglés", "message": "Hola Mundo"},
        }

        self.current_lang = "en"

        # Create labels and button
        self.welcome_label = ttk.Label(root, text=self.languages[self.current_lang]["welcome"], font=("Arial", 14))
        self.welcome_label.pack(pady=20)

        self.message_label = ttk.Label(root, text=self.languages[self.current_lang]["message"])
        self.message_label.pack(pady=10)

        self.switch_button = ttk.Button(
            root, text=self.languages[self.current_lang]["button"], command=self.switch_language
        )
        self.switch_button.pack(pady=10)

    def switch_language(self):
        # Toggle between languages
        self.current_lang = "es" if self.current_lang == "en" else "en"

        # Update text for all widgets
        self.welcome_label.config(text=self.languages[self.current_lang]["welcome"])
        self.message_label.config(text=self.languages[self.current_lang]["message"])
        self.switch_button.config(text=self.languages[self.current_lang]["button"])


if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageSwitcher(root)
    root.geometry("300x200")
    root.mainloop()
