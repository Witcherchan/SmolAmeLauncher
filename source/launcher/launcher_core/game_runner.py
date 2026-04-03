"""
Handles launching, monitoring, and cleaning up the game process.
"""

from subprocess import Popen, TimeoutExpired
from threading import Thread
from time import time
from os.path import join
from tkinter import messagebox as mb

from launcher_utils.file_utils import extract_zip, copy_directory_contents, find_exe, clear_folder


class GameRunner:
    """
    Encapsulates all game-launch logic:
      - zip extraction
      - optional TAS file injection
      - .exe discovery and launch
      - polling for game exit
      - cleanup
    """

    def __init__(self, app):
        # `app` is the main App instance; we store a reference to reach
        # paths, stats, UI callbacks, etc.
        self.app = app
        self.game_process: Popen | None = None
        self.tas_process: Popen | None = None
        self.game_start_time: float = 0.0

    # ------------------------------------------------------------------
    # Public entry points
    # ------------------------------------------------------------------

    def start(self):
        """Launch the game in a background thread."""
        thread = Thread(target=self._run, daemon=True)
        thread.start()

    def terminate_game(self):
        """Forcefully stop the game process if running."""
        if self.game_process and self.game_process.poll() is None:
            print("Terminating running game...")
            self.game_process.terminate()
            try:
                self.game_process.wait(timeout=5)
            except TimeoutExpired:
                print("Force killing game...")
                self.game_process.kill()
            self._on_game_closed()
            self.game_process = None

    def terminate_tas(self):
        """Forcefully stop the TAS process if running."""
        if self.tas_process and self.tas_process.poll() is None:
            print("Terminating running TAS...")
            self.tas_process.terminate()
            try:
                self.tas_process.wait(timeout=3)
            except TimeoutExpired:
                print("Force killing TAS...")
                self.tas_process.kill()
            self.tas_process = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _run(self):
        """Full launch sequence (runs on a background thread)."""
        app = self.app
        scf = app.scrollable_button_frame

        if scf.selected_version == -1:
            mb.showinfo("Info", "Please select game version first!")
            return

        app.enable_buttons(False)
        app.button_play.configure(text="Loading...")

        # Locate the selected version in version_buttons
        version_entry = self._find_version_entry(scf)
        if version_entry is None:
            mb.showerror("Error", "ERROR: Couldn't find right folder!")
            self._reset_ui()
            return

        version_name, zip_path = version_entry

        # --- Extract ZIP ---
        app.button_play.configure(text="Extracting files...")
        if not extract_zip(zip_path, app.temp_perm_path):
            mb.showerror(
                "Error",
                f"ERROR: Couldn't open ZIP: {zip_path}\n\n"
                "Did you change the name of the ZIP or remove it after opening the app?",
            )
            self._reset_ui()
            return

        print("Extracted to:", app.temp_perm_path)

        # --- Optional TAS injection ---
        if app.tas_checkbox.get():
            if not self._inject_tas(zip_path):
                self._reset_ui()
                return

        # --- Find .exe ---
        app.button_play.configure(text="Finding '.exe' file...")
        exe_path = find_exe(app.temp_perm_path)
        if exe_path is None:
            mb.showerror(
                "Error",
                f"ERROR: No valid .exe found in: {zip_path}!\n\n"
                "Are you sure that the game's .exe file is located directly in the selected ZIP file?",
            )
            self._reset_ui()
            return

        # --- Mark last played & launch ---
        app.update_last_played(version_name)
        print("Running:", exe_path)
        self.game_start_time = time()
        app.button_play.configure(text="Running...")
        self.game_process = Popen([exe_path])
        app.iconify()

        # Begin polling loop (on the main thread via after())
        app.after(1000, self._poll_game_closed)

    def _find_version_entry(self, scf) -> tuple[str, str] | None:
        """Return (version_name, zip_path) for the currently selected version."""
        app = self.app
        for folder in scf.version_buttons:
            if folder["name"] == app.selected_folder:
                version_name = folder["buttons"][scf.selected_version].cget("text")
                zip_path = (
                    f"{app.versions_path}{app.selected_folder}\\{version_name}.zip"
                )
                return version_name, zip_path
        return None

    def _inject_tas(self, zip_path: str) -> bool:
        """Copy TAS files into temp folder and launch TAS.exe. Returns success."""
        app = self.app
        app.button_play.configure(text="Copying TAS files...")

        success = copy_directory_contents(
            app.tas_path,
            app.temp_perm_path,
            on_error=lambda p: mb.showerror(
                "Error", f"ERROR: Couldn't copy TAS files: {zip_path}"
            ),
        )
        if not success:
            return False

        app.button_play.configure(text="Running TAS...")
        tas_exe = app.temp_perm_path + app.tas_exe_path
        try:
            self.tas_process = Popen([tas_exe])
        except Exception:
            mb.showerror("Error", f"ERROR: Couldn't find TAS exe file: {tas_exe}")
            return False

        return True

    def _poll_game_closed(self):
        """Called repeatedly via app.after() until the game process exits."""
        if self.game_process.poll() is None:
            self.app.after(1000, self._poll_game_closed)
            return
        self._on_game_closed()

    def _on_game_closed(self):
        """Handle everything that happens after the game exits."""
        app = self.app
        sbf = app.scrollable_button_frame
        elapsed = time() - self.game_start_time

        # Identify the version that was played
        version_name = self._resolve_playing_version(sbf)
        if version_name:
            app.add_play_time(version_name, elapsed)
        else:
            print("Couldn't find the played version in stats.")

        # Stop TAS if still running
        self.terminate_tas()

        # Wipe temp folder
        clear_folder(app.temp_perm_path)

        # Restore UI
        self._reset_ui()
        app.deiconify()
        app.lift()

    def _resolve_playing_version(self, sbf) -> str | None:
        """Return the version name that was playing, or None."""
        app = self.app
        for folder in app.sorted_folders:
            if folder["name"] == app.selected_folder:
                for version in folder["versions"]:
                    if version == sbf.selected_version_name:
                        return version
        return None

    def _reset_ui(self):
        app = self.app
        app.enable_buttons(True)
        app.button_play.configure(text="Play")
