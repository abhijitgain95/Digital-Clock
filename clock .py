"""A small interactive digital clock built with Tkinter."""

import tkinter as tk
from datetime import datetime
from typing import Callable


class DigitalClock:
    """Display the current time with a few simple viewing options."""

    THEMES = (
        {
            "background": "#111827",
            "foreground": "#F9FAFB",
            "muted": "#9CA3AF",
            "accent": "#38BDF8",
            "button": "#1F2937",
        },
        {
            "background": "#F3F4F6",
            "foreground": "#111827",
            "muted": "#6B7280",
            "accent": "#0284C7",
            "button": "#E5E7EB",
        },
    )

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.use_24_hour = True
        self.show_seconds = True
        self.theme_index = 0
        self.widgets: list[tuple[tk.Widget, str]] = []

        root.title("Digital Clock")
        root.geometry("560x320")
        root.minsize(420, 260)

        self.container = tk.Frame(root, padx=32, pady=26)
        self.container.pack(fill="both", expand=True)

        self.heading = self._label(
            self.container, "DIGITAL CLOCK", font=("Segoe UI", 11, "bold")
        )
        self.heading.pack(pady=(0, 20))

        self.time_label = self._label(
            self.container,
            "",
            font=("Segoe UI", 58, "bold"),
        )
        self.time_label.pack(pady=(0, 4))

        self.date_label = self._label(
            self.container, "", font=("Segoe UI", 14)
        )
        self.date_label.pack(pady=(0, 24))

        self.controls = tk.Frame(self.container)
        self.controls.pack()
        self.format_button = self._add_button("Use 12-hour", self.toggle_format)
        self.seconds_button = self._add_button("Hide seconds", self.toggle_seconds)
        self._add_button("Change theme", self.toggle_theme)

        self.apply_theme()
        self.update_clock()

    def _label(
        self, parent: tk.Widget, text: str, font: tuple[str, int, str] | tuple[str, int]
    ) -> tk.Label:
        label = tk.Label(parent, text=text, font=font)
        self.widgets.append((label, "foreground"))
        return label

    def _add_button(self, text: str, command: Callable[[], None]) -> tk.Button:
        button = tk.Button(
            self.controls,
            text=text,
            command=command,
            relief="flat",
            padx=12,
            pady=9,
            cursor="hand2",
        )
        button.pack(side="left", padx=5)
        self.widgets.append((button, "button"))
        return button

    def apply_theme(self) -> None:
        theme = self.THEMES[self.theme_index]
        self.root.configure(bg=theme["background"])
        self.container.configure(bg=theme["background"])
        self.controls.configure(bg=theme["background"])

        for widget, color_role in self.widgets:
            widget.configure(
                bg=theme["button"] if color_role == "button" else theme["background"],
                fg=theme["accent"] if widget is self.heading else theme["foreground"],
            )
            if isinstance(widget, tk.Button):
                widget.configure(
                    activebackground=theme["accent"],
                    activeforeground=theme["foreground"],
                )

        self.date_label.configure(fg=theme["muted"])

    def toggle_format(self) -> None:
        self.use_24_hour = not self.use_24_hour
        self.format_button.configure(
            text="Use 12-hour" if self.use_24_hour else "Use 24-hour"
        )

    def toggle_seconds(self) -> None:
        self.show_seconds = not self.show_seconds
        self.seconds_button.configure(
            text="Hide seconds" if self.show_seconds else "Show seconds"
        )

    def toggle_theme(self) -> None:
        self.theme_index = 1 - self.theme_index
        self.apply_theme()

    def update_clock(self) -> None:
        now = datetime.now()
        time_format = "%H:%M:%S" if self.show_seconds else "%H:%M"
        if not self.use_24_hour:
            time_format = "%I:%M:%S %p" if self.show_seconds else "%I:%M %p"

        self.time_label.configure(text=now.strftime(time_format))
        self.date_label.configure(text=now.strftime("%A, %B %d, %Y"))
        self.root.after(250, self.update_clock)


def main() -> None:
    root = tk.Tk()
    DigitalClock(root)
    root.mainloop()


if __name__ == "__main__":
    main()