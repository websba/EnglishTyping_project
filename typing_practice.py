"""英文打字練習小工具：題目與輸入逐字比對，正確綠底、錯誤粉底。"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class TypingPracticeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("英文打字練習")
        self.geometry("800x500")
        self.minsize(480, 360)

        self._updating = False

        self._build_ui()
        self._bind_events()

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=12)
        root.pack(fill=tk.BOTH, expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(3, weight=1)

        ttk.Label(root, text="題目").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.prompt_text = tk.Text(
            root,
            wrap=tk.WORD,
            height=8,
            font=("Consolas", 12),
            undo=True,
        )
        self.prompt_text.grid(row=1, column=0, sticky="nsew")

        ttk.Label(root, text="輸入").grid(row=2, column=0, sticky="w", pady=(12, 4))
        self.input_text = tk.Text(
            root,
            wrap=tk.WORD,
            height=8,
            font=("Consolas", 12),
            undo=True,
        )
        self.input_text.grid(row=3, column=0, sticky="nsew")
        self.input_text.tag_configure("correct", background="#90EE90")
        self.input_text.tag_configure("wrong", background="#FFB6C1")

        button_row = ttk.Frame(root)
        button_row.grid(row=4, column=0, sticky="w", pady=(12, 0))
        ttk.Button(button_row, text="清空題目", command=self.clear_prompt).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(button_row, text="清空輸入", command=self.clear_input).pack(
            side=tk.LEFT
        )

    def _bind_events(self) -> None:
        for sequence in ("<KeyRelease>", "<<Paste>>", "<<Cut>>"):
            self.input_text.bind(sequence, self._on_input_changed)
            self.prompt_text.bind(sequence, self._on_prompt_changed)

    def _get_text(self, widget: tk.Text) -> str:
        return widget.get("1.0", "end-1c")

    def _on_input_changed(self, _event: tk.Event | None = None) -> None:
        self.refresh_highlight()

    def _on_prompt_changed(self, _event: tk.Event | None = None) -> None:
        self.refresh_highlight()

    def refresh_highlight(self) -> None:
        if self._updating:
            return

        self._updating = True
        try:
            prompt = self._get_text(self.prompt_text)
            typed = self._get_text(self.input_text)

            self.input_text.tag_remove("correct", "1.0", tk.END)
            self.input_text.tag_remove("wrong", "1.0", tk.END)

            for index, char in enumerate(typed):
                start = f"1.0+{index}c"
                end = f"1.0+{index + 1}c"
                if index < len(prompt) and char == prompt[index]:
                    self.input_text.tag_add("correct", start, end)
                else:
                    self.input_text.tag_add("wrong", start, end)
        finally:
            self._updating = False

    def clear_prompt(self) -> None:
        self.prompt_text.delete("1.0", tk.END)
        self.refresh_highlight()

    def clear_input(self) -> None:
        self.input_text.delete("1.0", tk.END)
        self.refresh_highlight()


def main() -> None:
    app = TypingPracticeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
