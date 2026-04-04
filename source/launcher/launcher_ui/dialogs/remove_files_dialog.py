"""
Dialog for removing individual version files from the selected category.
"""

from os import remove, listdir
from os.path import join

from .base_checklist_dialog import BaseChecklistDialog


class RemoveSelectedFiles(BaseChecklistDialog):
    def __init__(self, parent):
        folder_path = join(parent.versions_path, parent.selected_folder)
        items = list(listdir(folder_path))

        super().__init__(
            parent=parent,
            title="Remove files",
            heading="Choose files to remove",
            items=items,
            frame_color_key="remove_files",
            frame_border_color_key="remove_files_border",
            text_color_key="remove_files_text_color",
        )

    def confirm(self):
        selected = self.get_selected()

        if not selected:
            self.label.configure(text="No files selected!")
            return

        for file_name in selected:
            file_path = join(self.parent.versions_path, self.parent.selected_folder, file_name)
            remove(file_path)
            print("Removing: " + file_path)

        self.parent.refresh_folders(True)
        self.destroy()
