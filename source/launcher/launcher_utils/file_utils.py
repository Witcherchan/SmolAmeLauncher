"""
Utility functions for file and folder operations.
"""

from os import listdir, remove, mkdir
from os.path import isfile, isdir, join
from shutil import copy, copytree, rmtree
from zipfile import ZipFile
from tkinter import filedialog, messagebox as mb


def list_zip_versions(folder_path: str) -> list[str]:
    """Return list of .zip filenames (without extension) in a folder."""
    versions = []
    for name in listdir(folder_path):
        if name.endswith(".zip"):
            versions.append(name.removesuffix(".zip"))
    return versions


def list_subfolders(base_path: str) -> list[dict]:
    """
    Scan base_path and return sorted_folders structure:
    [{"name": str, "versions": [str, ...]}, ...]
    """
    folders = []
    for f_name in listdir(base_path):
        f_path = join(base_path, f_name)
        if isdir(f_path):
            versions = list_zip_versions(f_path)
            folders.append({"name": f_name, "versions": versions})
    return folders


def clear_folder(target: str, on_error=None):
    """
    Delete all files and subfolders inside target directory.
    Calls on_error(file_path) if deletion fails.
    """
    for f in listdir(target):
        file_path = join(target, f)
        try:
            if isfile(file_path):
                remove(file_path)
                print("Removed file: " + file_path)
            elif isdir(file_path):
                rmtree(file_path)
                print("Removed folder: " + file_path)
        except Exception:
            print(f'Unable to clear: "{file_path}"')
            if on_error:
                on_error(file_path)
            return
    print("--------------------")
    print("Done clearing folder: " + target)


def extract_zip(zip_path: str, dest_path: str) -> bool:
    """Extract a zip file to dest_path. Returns True on success."""
    try:
        zp = ZipFile(zip_path)
        zp.extractall(dest_path)
        zp.close()
        return True
    except Exception:
        return False


def copy_directory_contents(src: str, dest: str, on_error=None) -> bool:
    """
    Copy all files and subdirectories from src into dest.
    Returns True on success, False on failure.
    """
    try:
        for file_name in listdir(src):
            file_path = join(src, file_name)
            if isdir(file_path):
                dest_dir = join(dest, file_name) 
                print(f'Copying folder: "{file_path}" to: "{dest_dir}"')
                copytree(file_path, dest_dir, dirs_exist_ok=True)
            else:
                print(f'Copying file: "{file_path}" to: "{dest}"')
                copy(file_path, dest)
        return True
    except Exception:
        if on_error:
            on_error(file_path)
        return False


def find_exe(folder: str, exclude: list[str] = None) -> str | None:
    """
    Find the first .exe in folder that is not in the exclude list.
    Returns full path or None.
    """
    if exclude is None:
        exclude = ["UnityCrashHandler64.exe"]
    for name in listdir(folder):
        full = join(folder, name)
        if isfile(full) and name.endswith(".exe") and name not in exclude:
            return full
    return None


def import_files_dialog(dest_folder: str) -> list[str]:
    """
    Open a file dialog for selecting .zip files, copy them to dest_folder.
    Returns list of copied file paths.
    """
    files = filedialog.askopenfilenames(
        title="Select files",
        filetypes=[("All files", "*.zip")]
    )
    if not files:
        print("No files selected")
        return []

    copied = []
    for file in files:
        try:
            copy(file, dest_folder)
            print(f"Copied {file} to {dest_folder}")
            copied.append(file)
        except Exception:
            pass
    return copied
