"""
Dialog for removing one or more mods.
"""

from os.path import join
from os import remove

from .base_checklist_dialog import BaseChecklistDialog

class DeleteSelectedModsPopup(BaseChecklistDialog):
    def __init__(self, parent):
        items = parent.mod_files

        super().__init__(
            parent=parent,
            title="Remove Mods",
            heading="Choose Mods to remove",
            items=items,
            frame_color_key="remove_categories",
            frame_border_color_key="remove_categories_border",
            text_color_key="remove_categories_text_color",
        )

    def confirm(self):
        selected = self.get_selected()
        existing_count = len(self.parent.mod_files)

        if not selected:
            self.label.configure(text="No categories selected!")
            return

        for name in selected:
            mod_path = join(self.parent.mods_path, f"{name}.zip")
            remove(mod_path)
            print("Removing: " + mod_path)

        self.parent.refresh_folders(True)
        self.destroy()