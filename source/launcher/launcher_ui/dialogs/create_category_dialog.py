"""
Dialog for creating a new version category (folder).
"""

from os import mkdir
from os.path import join

from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkEntry, CTkButton


class CreateNewCategory(CTkToplevel):

    MAX_NAME_LENGTH = 20

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # --- Window setup ---
        self.title("Create category")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.after(
            1,
            self.geometry(
                f"500x200+{self.parent.winfo_x()+200}+{self.parent.winfo_y()+225}"
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
            fg_color=self.parent.colors["create_category"],
            border_width=4,
            border_color=self.parent.colors["create_category_border"],
            corner_radius=16,
        )
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # --- Widgets ---
        self.label = CTkLabel(
            self.frame,
            text="Type the name of the new category",
            text_color=self.parent.colors["create_category_text_color"],
            font=("Arial", 18),
        )
        self.label.grid(
            row=0, column=0, padx=10, pady=(10, 0), columnspan=2, sticky="nsew"
        )

        self.text_typer = CTkEntry(
            self.frame,
            placeholder_text="For example: Speedrun",
            font=("Arial", 28),
        )
        self.text_typer.grid(
            row=2, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )

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

    def confirm(self):
        category_name = self.text_typer.get()

        if not category_name.strip():
            self.label.configure(text="Category name can not be empty!")
            return

        for folder in self.parent.sorted_folders:
            if category_name == folder["name"]:
                self.label.configure(text="This category already exists!")
                return

        if len(category_name) > self.MAX_NAME_LENGTH:
            self.label.configure(
                text=f"Name too long! Max {self.MAX_NAME_LENGTH} characters!"
            )
            return

        mkdir(join(self.parent.versions_path, category_name))
        print("Created category:", category_name)
        self.parent.refresh_folders(True)
        self.destroy()
