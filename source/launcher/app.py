"""
Main application entry point.

App only handles:
  - Window / grid setup
  - Wiring UI widgets together
  - High-level callbacks that delegate to core modules
"""

import os
import sys

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
    if BASE_PATH not in sys.path:
        sys.path.insert(0, BASE_PATH)
else:
    # Running from source, go up one level from 'launcher/'
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if BASE_PATH not in sys.path:
        sys.path.insert(0, BASE_PATH)

import json
from atexit import register
from sys import excepthook
from traceback import format_exception
from tkinter import PhotoImage

from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkOptionMenu, CTkCheckBox, CTkEntry
from os import getcwd
from tkinter import font as tkfont

from launcher_core import StatsManager, GameRunner
from launcher_ui import VersionsFrame, ModsFrame
from launcher_ui.dialogs import RemoveSelectedFiles, DeleteSelectedFilesPopup, CreateNewCategory
from launcher_utils.file_utils import list_subfolders, import_files_dialog
from launcher_utils.format_utils import format_playtime, truncate_label

class App(CTk):
    def __init__(self):
        super().__init__()

        # --- Paths ---
        self.program_path   = BASE_PATH
        self.icon_ico_path  = os.path.join(self.program_path, "system", "images", "icon_main_app.ico")
        self.icon_png_path  = os.path.join(self.program_path, "system", "images", "icon_add_app.png")
        self.icon_png       = PhotoImage(file=self.icon_png_path)
        
        self.versions_path  = os.path.join(self.program_path, "versions")
        self.mods_path      = os.path.join(self.program_path, "mods")
        self.setting_path   = os.path.join(self.program_path, "system", "settings.json")
        self.stats_path     = os.path.join(self.program_path, "system", "stats.json")
        self.bepinex_path   = os.path.join(self.program_path, "BepinEx")
        self.tas_path       = os.path.join(self.program_path, "TAS")
        self.tas_exe_path   = os.path.join(self.tas_path, "TAS.Studio", "TAS.Studio.exe")
        self.temp_perm_path = os.path.join(self.program_path, "system", "temp")

        # --- Settings ---
        with open(self.setting_path, "r") as f:
            self.settings = json.load(f)
        self.colors = self.settings["colors"]

        # --- Stats ---
        self.stats_mgr = StatsManager(self.stats_path)
        try:
            self.stats_mgr.validate_and_load()
        except Exception:
            print("--- Something went wrong while validating stats. Stopping. ---")
            exit()

        # Expose stats dict directly for backward-compat with existing widget code
        self.stats = self.stats_mgr.stats

        # --- Game runner ---
        self.game_runner = GameRunner(self)

        # --- Lifecycle hooks ---
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        register(self.cleanup)
        excepthook = self.handle_crash   # noqa: F841 (intentional reassignment)

        # --- Window ---
        self.title("Smol Ame Launcher")
        self.geometry("900x640")
        self.minsize(700, 500)
        self.resizable(True, True)
        self.iconbitmap(self.icon_ico_path)
        self.configure(fg_color=self.colors["application_fg"])

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Data ---
        self.sorted_folders: list[dict] = []
        self.selected_folder: str = ""
        self.username: str = ""
        self.refresh_folders(False)

        # ---Cleanup ---
        self.cleanup()

        # --- Build UI ---
        self._build_options_frame()
        self._build_username_frame()
        self._build_versions_frame()
        self._build_description_frame()
        self._build_mods_frame()
        self._build_play_frame()

        # Trigger initial folder view
        self.scrollable_button_frame.switch_folders(self.selected_folder)

        # Re-fit text whenever the window is resized
        self.bind("<Configure>", lambda e: self.update_description(
            self.scrollable_button_frame.selected_version_name,
            self.selected_folder,
        ))

    # ==================================================================
    # UI construction helpers
    # ==================================================================

    def _build_options_frame(self):
        self.options_frame = CTkFrame(
            self,
            fg_color=self.colors["options_frame"],
            border_width=4,
            border_color=self.colors["options_frame_border"],
            corner_radius=16,
        )
        self.options_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=3)
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_columnconfigure(2, weight=2)
        self.options_frame.grid_columnconfigure(3, weight=2)

        self.delete_categories_button = CTkButton(
            self.options_frame,
            text="Remove categories",
            command=lambda: DeleteSelectedFilesPopup(self),
            fg_color=self.colors["button_on"],
            hover_color=self.colors["button_hover"],
        )
        self.delete_categories_button.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ew")

        self.create_categories_button = CTkButton(
            self.options_frame,
            text="Add category",
            command=lambda: CreateNewCategory(self),
            fg_color=self.colors["button_on"],
            hover_color=self.colors["button_hover"],
        )
        self.create_categories_button.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="ew")

        self.import_files_button = CTkButton(
            self.options_frame,
            text="Import files to selected category",
            command=self.import_files,
            fg_color=self.colors["button_on"],
            hover_color=self.colors["button_hover"],
        )
        self.import_files_button.grid(row=0, column=2, padx=(10, 0), pady=10, sticky="ew")

        self.remove_files_button = CTkButton(
            self.options_frame,
            text="Remove files from selected category",
            command=lambda: RemoveSelectedFiles(self),
            fg_color=self.colors["button_on"],
            hover_color=self.colors["button_hover"],
        )
        self.remove_files_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    def _build_username_frame(self):
        self.username_frame = CTkFrame(
            self,
            fg_color=self.colors["username_frame"],
            border_width=4,
            border_color=self.colors["username_frame_border"],
            corner_radius=16,
        )
        self.username_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=3)
        self.username_frame.grid_columnconfigure(0, weight=0)
        self.username_frame.grid_columnconfigure(1, weight=1)
        self.username_frame.grid_columnconfigure(2, weight=0)

        self.user_label = CTkLabel(self.username_frame, text="Username:", font=("Arial", 16))
        self.user_label.grid(row=0, column=0, padx=(20, 10), pady=10)

        self.user_entry = CTkEntry(self.username_frame, placeholder_text="Enter name...")
        self.user_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.user_save_btn = CTkButton(
            self.username_frame,
            text="Save",
            width=100,
            command=self.set_username,
            fg_color=self.colors["button_on"],
            hover_color=self.colors["button_hover"],
        )
        self.user_save_btn.grid(row=0, column=2, padx=(10, 20), pady=10)

    def _build_versions_frame(self):
        self.versions_frame = CTkFrame(
            self,
            fg_color=self.colors["version_frame"],
            border_width=4,
            border_color=self.colors["version_frame_border"],
            corner_radius=16,
        )
        self.versions_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.versions_frame.grid_columnconfigure(0, weight=1)
        self.versions_frame.grid_rowconfigure(1, weight=0)
        self.versions_frame.grid_rowconfigure(2, weight=1)

        # Category dropdown
        combo = [f["name"] for f in self.sorted_folders]
        self.selected_folder = combo[0] if combo else ""

        self.menu_box = CTkOptionMenu(
            self.versions_frame,
            values=combo,
            command=self.change_folder,
            fg_color=self.colors["menu"],
            button_color=self.colors["menu_button"],
            button_hover_color=self.colors["menu_button_hover"],
            dropdown_fg_color=self.colors["dropdown"],
            dropdown_hover_color=self.colors["dropdown_hover"],
        )
        if combo:
            self.menu_box.set(combo[0])
        else:
            self.menu_box.configure(state="disabled")
        self.menu_box.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")

        # Scrollable version list
        self.scrollable_button_frame = VersionsFrame(self.versions_frame, self)
        self.scrollable_button_frame.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="nsew")

        # TAS checkbox
        self.tas_frame = CTkFrame(
            self.versions_frame,
            fg_color=self.colors["tas_frame"],
            border_width=4,
            border_color=self.colors["tas_frame_border"],
            corner_radius=12,
            height=42,
            width=80,
        )
        self.tas_frame.grid_propagate(False)
        self.tas_frame.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="")
        self.tas_frame.grid_rowconfigure(0, weight=1)
        self.tas_frame.grid_columnconfigure(0, weight=1)

        self.tas_checkbox = CTkCheckBox(
            self.tas_frame, text="TAS", width=1, height=1,
            border_width=2, onvalue=True, offvalue=False,
        )
        self.tas_checkbox.grid(row=0, column=0, pady=0, sticky="")

    def _build_description_frame(self):
        self.description_frame = CTkFrame(
            self,
            fg_color=self.colors["description_frame"],
            border_width=4,
            border_color=self.colors["description_frame_border"],
            corner_radius=16,
        )
        self.description_frame.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="nsew")

        # Grid-based layout so everything scales with the frame
        self.description_frame.grid_columnconfigure(0, weight=1)
        self.description_frame.grid_rowconfigure(0, weight=2)
        self.description_frame.grid_rowconfigure(1, weight=1)
        self.description_frame.grid_rowconfigure(2, weight=1)
        self.description_frame.grid_rowconfigure(3, weight=1)
        self.description_frame.grid_rowconfigure(4, weight=1)
        self.description_frame.grid_rowconfigure(5, weight=1)

        self.folder_tile = CTkLabel(
            self.description_frame,
            text=self.selected_folder,
            text_color=self.colors["folder_title_color"],
        )
        self.folder_tile.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="nsew")
        self.folder_tile.configure(font=("Ariel", 64))

        self.version_title = CTkLabel(
            self.description_frame, text="",
            text_color=self.colors["version_title_color"],
        )
        self.version_title.grid(row=1, column=0, padx=10, sticky="nsew")
        self.version_title.configure(font=("Ariel", 42))

        self.last_played_tittle = CTkLabel(
            self.description_frame,
            text="Last played: Not played",
            text_color=self.colors["last_played_text_color"],
        )
        self.last_played_tittle.grid(row=2, column=0, padx=30, pady=(10, 0), sticky="sw")
        self.last_played_tittle.configure(font=("Ariel", 32))

        self.time_played_tittle = CTkLabel(
            self.description_frame,
            text="Time played: Not played",
            text_color=self.colors["time_played_text_color"],
        )
        self.time_played_tittle.grid(row=3, column=0, padx=30, sticky="w")
        self.time_played_tittle.configure(font=("Ariel", 32))

        self.total_play_time_tittle = CTkLabel(
            self.description_frame,
            text="Total play time: 0s",
            text_color=self.colors["time_played_text_color"],
        )
        self.total_play_time_tittle.grid(row=4, column=0, padx=30, sticky="w")
        self.total_play_time_tittle.configure(font=("Ariel", 32))

        self.program_version_title = CTkLabel(
            self.description_frame,
            text=f"v{self.settings['version']}",
            text_color=self.colors["program_version_color"],
        )
        self.program_version_title.grid(row=5, column=0, padx=(0, 14), pady=(0, 10), sticky="se")
        self.program_version_title.configure(font=("Ariel", 24))

    def _build_mods_frame(self):
        self.mods_frame = CTkFrame(
            self,
            fg_color=self.colors["mods_frame"],
            border_width=4,
            border_color=self.colors["mods_frame_border"],
            corner_radius=16,
        )

        self.mods_frame.grid(row=2, column=2, padx=(0, 10), pady=10, sticky="nsew")

        self.mods_frame.grid_columnconfigure(0, weight=1)
        self.mods_frame.grid_rowconfigure(0, weight=0)
        self.mods_frame.grid_rowconfigure(1, weight=1)

        self.mods_title = CTkLabel(
            self.mods_frame,
            text="Mods",
            text_color=self.colors["folder_title_color"],
        )
        self.mods_title.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="nsew")
        self.mods_title.configure(font=("Ariel", 18))

        # Define your mods list (or pull from self.settings)
        initial_mods = []
        if os.path.exists(self.mods_path):
            initial_mods = [
                os.path.splitext(f)[0] # This grabs "mod_name" instead of "mod_name.zip"
                for f in os.listdir(self.mods_path) 
                if os.path.isfile(os.path.join(self.mods_path, f)) and f.lower().endswith(".zip")
            ]

        self.scrollable_mods = ModsFrame(self.mods_frame, self, initial_mods)
        self.scrollable_mods.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.import_mods_button = CTkButton(
            self.mods_frame,
            text="Import Mods",
            command=self.import_mods,
            fg_color=self.colors["button_on"],
            hover_color=self.colors["button_hover"],
        )
        self.import_mods_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def _build_play_frame(self):
        self.play_frame = CTkFrame(
            self,
            fg_color=self.colors["play_frame"],
            border_width=4,
            border_color=self.colors["play_frame_border"],
            corner_radius=16,
            height=42
        )
        self.play_frame.grid_propagate(False)
        self.play_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew", columnspan=3)
        
        self.play_frame.grid_columnconfigure(0, weight=1)
        self.play_frame.grid_columnconfigure(1, weight=2)
        self.play_frame.grid_columnconfigure(2, weight=2)

        self.button_refresh = CTkButton(
            self.play_frame,
            text="Refresh",
            command=lambda: self.refresh_folders(True),
            fg_color=self.colors["button_on"],
            hover_color=self.colors["button_hover"],
            height=24
        )

        self.button_refresh.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.button_play = CTkButton(
            self.play_frame,
            text="Play",
            command=self.start_game,
            fg_color=self.colors["button_on"],
            hover_color=self.colors["button_hover"],
            height=24
        )

        self.button_play.grid(row=0, column=1, columnspan=2, padx=(0, 10), pady=(10, 5), sticky="ew")

    # ==================================================================
    # UI update / description callbacks
    # ==================================================================

    def update_description(self, tn: str, fn: str, reset: bool = False):
        # Measure available width dynamically; fall back to 648 before frame is drawn
        frame_w = self.description_frame.winfo_width()
        max_px = (frame_w - 40) if frame_w > 100 else 648
        fts, vts = 64, 48

        f = tkfont.Font(family="Ariel", size=fts)
        fw = f.measure(fn)
        while fw > max_px:
            fts -= 1
            f.configure(size=fts)
            fw = f.measure(fn)

        f.configure(size=vts)
        fw = f.measure(tn)
        while fw > max_px:
            vts -= 1
            f.configure(size=vts)
            fw = f.measure(tn)

        self.version_title.configure(text=f"- {tn} -", font=("Ariel", vts))
        self.folder_tile.configure(text=f"- {fn} -", font=("Ariel", fts))

        if tn != "Select version":
            self.last_played_tittle.configure(
                text=f"Last played: {self.stats_mgr.version_last_played(tn)}"
            )
            self.time_played_tittle.configure(
                text=f"Time played: {format_playtime(self.stats_mgr.version_time_played(tn))}"
            )

        if reset:
            self.last_played_tittle.configure(text="Last played: ")
            self.time_played_tittle.configure(text="Time played: ")

        self.total_play_time_tittle.configure(
            text=f"Total play time: {format_playtime(self.stats_mgr.total_play_time)}"
        )

    def change_folder(self, choice: str):
        self.selected_folder = choice
        self.menu_box.set(truncate_label(choice))
        self.scrollable_button_frame.switch_folders(self.selected_folder)

    def refresh_folders(self, refresh: bool):
        self.sorted_folders = list_subfolders(self.versions_path)
        

        if os.path.exists(self.mods_path):
            # os.path.splitext(f)[0] grabs the filename without the extension
            mod_files = [
                os.path.splitext(f)[0] 
                for f in os.listdir(self.mods_path) 
                if os.path.isfile(os.path.join(self.mods_path, f))
            ]
        else:
            mod_files = []
        
        if refresh:
            combo = [f["name"] for f in self.sorted_folders]
            self.selected_folder = combo[0] if combo else ""
            self.menu_box.configure(values=combo)
            self.menu_box.set(self.selected_folder)

            self.scrollable_button_frame.remove_version_buttons()
            self.scrollable_button_frame.folders = self.sorted_folders
            self.scrollable_button_frame.create_version_buttons()
            
            if hasattr(self, "scrollable_mods"):
                self.scrollable_mods.render_mods(mod_files)
            
            self.change_folder(self.selected_folder)

        print("Folders refreshed: " + str(self.sorted_folders))

    def enable_buttons(self, enable: bool = True):
        state = "normal" if enable else "disabled"

        for widget in (
            self.button_play, self.button_refresh, self.menu_box,
            self.tas_checkbox, self.delete_categories_button,
            self.create_categories_button, self.import_files_button,
            self.remove_files_button,
        ):
            widget.configure(state=state)

        for folder in self.scrollable_button_frame.version_buttons:
            for btn in folder["buttons"]:
                btn.configure(state=state)

    # ==================================================================
    # Game / stats callbacks
    # ==================================================================

    def start_game(self):
        self.game_runner.start()

    def add_play_time(self, version_name: str, seconds_played: float):
        self.stats_mgr.record_session(version_name, seconds_played)
        self.update_time_played(
            version_name,
            self.stats_mgr.version_time_played(version_name),
            self.stats_mgr.total_play_time,
        )

    def update_last_played(self, name: str):
        self.stats_mgr.record_last_played(name)
        self.update_description(
            self.scrollable_button_frame.selected_version_name,
            self.selected_folder,
        )
        from threading import Thread
        Thread(target=self.stats_mgr.save, daemon=True).start()

    def update_time_played(self, name: str, time_played: float, total_played: float):
        # stats_mgr already updated internally; just refresh description + save
        self.update_description(
            self.scrollable_button_frame.selected_version_name,
            self.selected_folder,
        )
        from threading import Thread
        Thread(target=self.stats_mgr.save, daemon=True).start()

    def save_stats(self):
        self.stats_mgr.save()

    # ==================================================================
    # File management
    # ==================================================================

    def import_files(self):
        path_folder = os.path.join(self.versions_path, self.selected_folder) 
        copied = import_files_dialog(path_folder)
        if copied:
            self.refresh_folders(True)

    def import_mods(self):
        path_folder = self.mods_path
        copied = import_files_dialog(path_folder)
        if copied:
            self.refresh_folders(True)

    def set_username(self):
        username = self.user_entry.get().strip()
        self.username = username

    # ==================================================================
    # Lifecycle
    # ==================================================================

    def on_closing(self):
        print("Window closed by user (X or ALT+F4)")
        # Just stop the UI and exit; atexit.register will handle the rest automatically
        self.quit() # Stops mainloop
        self.destroy() # Destroys widgets

    def cleanup(self):
        # Check if cleanup was already done to avoid double-runs
        if hasattr(self, "_cleaned") and self._cleaned:
            return
        self._cleaned = True
        
        from launcher_utils.file_utils import clear_folder
        print("Running cleanup...")

        # Ensure we don't crash during cleanup if objects aren't fully initialized
        if hasattr(self, "game_runner"):
            self.game_runner.terminate_game()

        if hasattr(self, "temp_perm_path") and os.path.exists(self.temp_perm_path):
            print("Cleaning temporary folder...")
            clear_folder(self.temp_perm_path)

        if hasattr(self, "stats_mgr"):
            print("Saving stats...")
            try:
                self.stats_mgr.save()
            except Exception as e:
                print(f"Error saving stats: {e}")

        print("Cleanup complete.")

    def handle_crash(self, exc_type, exc_value, exc_traceback):
        print("Script crashed!")
        print("".join(format_exception(exc_type, exc_value, exc_traceback)))
        self.cleanup()


if __name__ == "__main__":
    app = App()
    app.mainloop()