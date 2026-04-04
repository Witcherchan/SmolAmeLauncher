"""
Scrollable frame that renders mods checklists.
"""

from customtkinter import CTkScrollableFrame, CTkCheckBox, BooleanVar

class ModsFrame(CTkScrollableFrame):
    def __init__(self, master, app, mod_names: list[str]):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.app = app
        
        # This dictionary will store { "Mod Name": BooleanVar }
        self.mod_vars = {}
        self.checkboxes = []

        self.configure(fg_color=self.app.colors["scrollable_frame"])

        # Render the checkboxes immediately
        self.render_mods(mod_names)

    def render_mods(self, mod_names: list[str]):
        """Clear and rebuild the list of checkboxes."""
        # 1. Clear existing (if any)
        for cb in self.checkboxes:
            cb.destroy()
        self.checkboxes.clear()
        self.mod_vars.clear()

        # 2. Build new checkboxes
        for i, name in enumerate(mod_names):
            var = BooleanVar(value=False)
            self.mod_vars[name] = var
            
            cb = CTkCheckBox(
                self, 
                text=name,
                text_color=self.app.colors["folder_title_color"], 
                variable=var,
                hover_color=self.app.colors["button_hover"],
                fg_color=self.app.colors["button_on"],
                border_color=self.app.colors["play_frame_border"]
            )
            cb.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="we")
            self.checkboxes.append(cb)