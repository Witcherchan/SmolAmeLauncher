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
        # Base paths
        self.local = LOCAL_PATH
        self.program = BASE_PATH

        # Folders
        self.system = join(self.program, "system")
        self.mods = join(self.program, "mods")
        self.tas = join(self.program, "tas")
        self.versions = join(self.program, "versions")
        self.bepinex = join(self.program, "BepinEx")

        self.images = join(self.system, "images")
        self.temp_perm = join(self.system, "temp")

        # Files
        self.icon_ico = join(self.images, "icon_main_app.ico")
        self.icon_png = join(self.images, "icon_add_app.png")

        self.settings = join(self.system, "settings.json")

        self.stats = join(self.local, "stats.json")

        self.tas_exe = join(self.tas, "TAS.Studio", "TAS.Studio.exe")

        print(f"Creating dictionary for compatibility")

        self.paths = {
            "local": self.local,
            "program": self.program,
            "system": self.system,
            "mods": self.mods,
            "tas": self.tas,
            "versions": self.versions,
            "bepinex": self.bepinex,
            "images": self.images,
            "temp_perm": self.temp_perm,
            "icon_ico": self.icon_ico,
            "icon_png": self.icon_png,
            "settings": self.settings,
            "stats": self.stats,
            "tas_exe": self.tas_exe,
        }

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