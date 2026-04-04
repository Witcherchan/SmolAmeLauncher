"""
Dialog for removing one or more version categories (folders).
"""

from shutil import rmtree
from os.path import join

from .base_checklist_dialog import BaseChecklistDialog


class DeleteSelectedFilesPopup(BaseChecklistDialog):
    def __init__(self, parent):
        items = [folder["name"] for folder in parent.sorted_folders]

        super().__init__(
            parent=parent,
            title="Remove category",
            heading="Choose categories to remove",
            items=items,
            frame_color_key="remove_categories",
            frame_border_color_key="remove_categories_border",
            text_color_key="remove_categories_text_color",
        )

    def confirm(self):
        selected = self.get_selected()
        existing_count = len(self.parent.sorted_folders)

        if not selected:
            self.label.configure(text="No categories selected!")
            return

        if len(selected) >= existing_count:
            self.label.configure(
                text="At least one category has to exist!", font=("Arial", 17)
            )
            return

        for name in selected:
            folder_path = join(self.parent.versions_path, name)
            rmtree(folder_path)
            print("Removing: " + folder_path)

        self.parent.refresh_folders(True)
        self.destroy()
