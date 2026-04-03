"""
Base class for dialogs that display a scrollable checklist of items
with Confirm / Cancel buttons.

Subclasses only need to implement:
  - build_items()  – populate self.buttons from self.items
  - confirm()      – handle confirmation action
"""

from customtkinter import (
    CTkToplevel, CTkFrame, CTkLabel, CTkScrollableFrame, CTkButton, CTkCheckBox,
)


class BaseChecklistDialog(CTkToplevel):
    """
    Reusable scrollable-checklist dialog.

    Parameters
    ----------
    parent      : the App instance
    title       : window title string
    heading     : label text at the top of the dialog
    items       : list of item labels to render as checkboxes
    geometry    : optional geometry string (default: 300x400 offset by parent pos)
    frame_color_key          : colors dict key for main frame fg_color
    frame_border_color_key   : colors dict key for main frame border_color
    text_color_key           : colors dict key for heading label text_color
    """

    def __init__(
        self,
        parent,
        title: str,
        heading: str,
        items: list[str],
        frame_color_key: str,
        frame_border_color_key: str,
        text_color_key: str,
    ):
        super().__init__(parent)
        self.parent = parent
        self.items = items
        self.buttons: list[CTkCheckBox] = []

        # --- Window setup ---
        self.title(title)
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.after(
            1,
            self.geometry(
                f"300x400+{self.parent.winfo_x()+300}+{self.parent.winfo_y()+100}"
            ),
        )
        self.wm_iconbitmap()
        self.after(200, lambda: self.iconbitmap(self.parent.icon_ico_path))
        self.configure(fg_color=self.parent.colors["application_fg"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Main frame ---
        self.frame = CTkFrame(
            self,
            fg_color=self.parent.colors[frame_color_key],
            border_width=4,
            border_color=self.parent.colors[frame_border_color_key],
            corner_radius=16,
        )
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # --- Heading label ---
        self.label = CTkLabel(
            self.frame,
            text=heading,
            text_color=self.parent.colors[text_color_key],
            font=("Arial", 18),
        )
        self.label.grid(
            row=0, column=0, padx=10, pady=(10, 0), columnspan=2, sticky="nsew"
        )

        # --- Scrollable checklist ---
        scrollable = CTkScrollableFrame(
            self.frame, fg_color=self.parent.colors["scrollable_frame"]
        )
        scrollable.grid(
            row=1, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2
        )
        scrollable.grid_columnconfigure(1, weight=1)

        for idx, item in enumerate(self.items):
            cb = CTkCheckBox(
                scrollable,
                text="",
                width=0,
                font=("Arial", 24),
                onvalue=item,
                offvalue="False",
            )
            btn = CTkButton(
                scrollable,
                text=item,
                fg_color=self.parent.colors["button_on"],
                hover_color=self.parent.colors["button_on"],
            )
            btn.grid(row=idx, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")
            cb.grid(row=idx, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
            self.buttons.append(cb)

        # --- Action buttons ---
        confirm_btn = CTkButton(
            self.frame,
            text="Confirm",
            command=self.confirm,
            fg_color=self.parent.colors["button_on"],
            hover_color=self.parent.colors["button_hover"],
        )
        confirm_btn.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        cancel_btn = CTkButton(
            self.frame,
            text="Cancel",
            command=self.destroy,
            fg_color=self.parent.colors["button_on"],
            hover_color=self.parent.colors["button_hover"],
        )
        cancel_btn.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="nsew")

    def get_selected(self) -> list[str]:
        """Return list of checked item values."""
        return [b.get() for b in self.buttons if b.get() != "False"]

    def confirm(self):
        """Override in subclasses to handle the confirm action."""
        raise NotImplementedError
