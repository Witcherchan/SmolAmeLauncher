"""
Handles creating, validating, and copying paths to the main app.
"""

import sys
from os import makedirs
from source.launcher.launcher_utils.constants import  BASE_PATH, LOCAL_PATH
from os.path import exists, join
from json import dump

class PathsManager:
    """Manages paths on startup."""

    def __init__(self,_parent):
        self.parent = _parent
        self.paths: dict = {}
        self.create_paths()

    def create_paths(self):
        """
        Create paths on startup.
        """
        self.paths = {
            "local": LOCAL_PATH,
            "program": BASE_PATH
        }

        # Folders

        self.paths["system"]    = join(self.paths["program"], "system")
        self.paths["mods"]      = join(self.paths["program"], "mods")
        self.paths["tas"]       = join(self.paths["program"], "tas")
        self.paths["versions"]  = join(self.paths["program"], "versions")
        self.paths["bepinex"]   = join(self.paths["program"], "BepinEx")

        self.paths["images"]    = join(self.paths["system"], "images")
        self.paths["temp_perm"] = join(self.paths["system"], "temp")

        # Files
        self.paths["icon_ico"]  = join(self.paths["images"], "icon_main_app.ico")
        self.paths["icon_png"]  = join(self.paths["images"], "icon_add_app.png")

        self.paths["setting"]  = join(self.paths["system"], "settings.json")

        self.paths["stats"]     = join(self.paths["local"], "stats.json")

        self.paths["tas_exe"]   = join(self.paths["tas"], "TAS.Studio", "TAS.Studio.exe")

        print("--- Finished creating paths ---")

    def validate_paths(self):
        """
        Validate paths on startup.
        Raises SystemExit if important folders/files are missing.
        """

        print("--- Started validating paths ---")

        for _key,_value in self.paths.items():
            if not exists(_value):
                if _key in ("mods","stats","temp_perm"):
                    print(f"{_key} path does not exist. Creating new one! Continuing...")
                    if _key in ("mods","temp_perm"):
                        makedirs(_value)
                    elif _key in ("stats"):
                        with open(_value, "w") as f:
                            dump({}, f, indent=4)
                else:
                    print(f"--- Required {_key} ({_value}) path does not exist. Application has been closed! ---")
                    sys.exit()
            else:
                print(f"{_key} ({_value}) exists. Continuing...")

        print("--- Finished validating paths ---")

    def copy_paths(self):
        """
        Copies paths to the main app
        """

        print("--- Started copying paths ---")

        for _key,_value in self.paths.items():
            _real_key = _key + "_path"
            setattr(self.parent, _real_key, _value)
            print(f"Copied {_value} to {_real_key}")

        print("--- Finished copying paths ---")