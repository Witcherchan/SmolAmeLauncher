"""
Scrollable frame that renders per-category version buttons.
"""

from customtkinter import CTkScrollableFrame, CTkButton
from threading import Thread

class VersionsFrame(CTkScrollableFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.app = app
        self.folders = app.sorted_folders
        self.version_buttons: list[dict] = []
        self.configure(fg_color=self.app.colors["scrollable_frame"])

        self.selected_version = -1
        self.selected_version_name = "None"

        self.create_version_buttons()

    # ------------------------------------------------------------------
    # Button creation / removal
    # ------------------------------------------------------------------

    def create_version_buttons(self):
        """Build one CTkButton per version, grouped by folder."""
        stats_mgr = self.app.stats_mgr

        # Refresh stats from disk
        stats_mgr.validate_and_load()

        for folder in self.folders:
            folder_buttons = []

            for v, version in enumerate(folder["versions"]):
                btn = CTkButton(self, text=version)
                btn.configure(
                    command=lambda refer=btn: self.select_button(refer),
                    hover_color=self.app.colors["button_hover"],
                )
                btn.grid(row=v, column=0, padx=10, pady=(10, 0), sticky="we")

                self.switch_folders(self.app.selected_folder)

                stats_mgr.ensure_version_entry(version)
                folder_buttons.append(btn)

            self.version_buttons.append(
                {"name": folder["name"], "buttons": folder_buttons}
            )

        print("VERSION BUTTONS NEW: " + str(self.version_buttons))

        thread = Thread(target=stats_mgr.save, daemon=True)
        thread.start()

    def remove_version_buttons(self):
        """Destroy all existing version buttons."""
        for folder in self.version_buttons:
            for btn in folder["buttons"]:
                btn.destroy()
        self.version_buttons = []

    # ------------------------------------------------------------------
    # Folder / selection management
    # ------------------------------------------------------------------

    def switch_folders(self, selected_folder: str):
        """Show only the buttons that belong to selected_folder."""
        self.selected_version = -1
        self.selected_version_name = "Select version"

        for folder in self.version_buttons:
            if folder["name"] == selected_folder:
                for b, btn in enumerate(folder["buttons"]):
                    btn.configure(
                        state="normal", fg_color=self.app.colors["button_on"]
                    )
                    btn.grid(row=b, column=0, padx=10, pady=(10, 0), sticky="we")
            else:
                for btn in folder["buttons"]:
                    btn.configure(state="disabled")
                    btn.grid_forget()

        if hasattr(self.app, "description_frame"):
            self.app.update_description(
                self.selected_version_name, self.app.selected_folder, reset=True
            )

    def select_button(self, refer: CTkButton):
        """Handle a version button click."""
        if refer.cget("state") != "normal":
            return

        for folder in self.version_buttons:
            if folder["name"] == self.app.selected_folder:
                button_id = refer.grid_info()["row"]

                # Deselect previous
                if self.selected_version >= 0:
                    folder["buttons"][self.selected_version].configure(
                        fg_color=self.app.colors["button_on"]
                    )

                # Select new
                folder["buttons"][button_id].configure(
                    fg_color=self.app.colors["button_selected"]
                )
                self.selected_version = button_id
                self.selected_version_name = refer.cget("text")

                self.app.update_description(
                    self.selected_version_name, self.app.selected_folder
                )
                print(
                    "Selected version: "
                    + str(folder["buttons"][button_id].cget("text"))
                )
                break