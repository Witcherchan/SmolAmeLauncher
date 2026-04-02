import json

from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame, CTkButton, CTkOptionMenu, CTk, CTkCheckBox, CTkToplevel, CTkEntry
from os import listdir, getcwd, remove, mkdir
from os.path import isfile, isdir, join
from tempfile import TemporaryDirectory
from datetime import datetime
from subprocess import Popen, TimeoutExpired
from json import load,dump
from tkinter import messagebox as mb
from tkinter import filedialog, simpledialog, PhotoImage, font
from zipfile import ZipFile
from threading import Thread
from time import time
from sys import excepthook
from atexit import register
from traceback import format_exception
from shutil import copy,copytree,rmtree

class DownloadVersions(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Remove files")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.after(1,self.geometry(f"300x400+{self.parent.winfo_x()+300}+{self.parent.winfo_y()+100}")) #Main App: 900x600
        self.buttons = []
        self.wm_iconbitmap()
        self.after(200,lambda: self.iconbitmap(self.parent.icon_ico_path))
        self.configure(fg_color=self.parent.colors["application_fg"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = CTkFrame(self,fg_color=self.parent.colors["remove_files"], border_width=4,
                                                        border_color=self.parent.colors["remove_files_border"], corner_radius=16)
        self.frame.grid(row=0, column=0, sticky="nsew",padx=10,pady=10)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.lable = CTkLabel(self.frame, text="Choose files to remove",text_color=self.parent.colors["remove_files_text_color"],font=("Arial", 18))
        self.lable.grid(row = 0, column = 0, padx = 10, pady = (10,0), columnspan = 2, sticky = "nsew")

        scrollable_checkbox = CTkScrollableFrame(self.frame,fg_color=self.parent.colors["scrollable_frame"])
        scrollable_checkbox.grid(row = 1, column = 0, padx = 10, pady = (10,0), sticky = "nsew", columnspan = 2)
        scrollable_checkbox.grid_columnconfigure(1,weight=1)

        count = 0
        path_folder = self.parent.versions_path + self.parent.selected_folder
        files = listdir(path_folder)
        for file in files:
            file_checkbox = CTkCheckBox(scrollable_checkbox,text="",width=0,
                                        font=("Arial",24),onvalue=file,offvalue="False")
            file_button = CTkButton(scrollable_checkbox,text=file,fg_color=self.parent.colors["button_on"],
                                      hover_color=self.parent.colors["button_on"])
            file_button.grid(row=count,column=1,padx=(0,10),pady=(10,0),sticky="nsew")
            file_checkbox.grid(row=count,column = 0, padx = (10,0), pady = (10,0), sticky = "nsew")
            self.buttons.append(file_checkbox)
            count += 1

        confirm_button = CTkButton(self.frame,text="Confirm",command=self.confirm,fg_color=self.parent.colors["button_on"],
                                   hover_color=self.parent.colors["button_hover"])
        confirm_button.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = "nsew")
        cancel_button = CTkButton(self.frame,text="Cancel",command=self.cancel,fg_color=self.parent.colors["button_on"],
                                   hover_color=self.parent.colors["button_hover"])
        cancel_button.grid(row = 2, column = 0, padx=(10,0), pady=10, sticky="nsew")

class RemoveSelectedFiles(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Remove files")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.after(1,self.geometry(f"300x400+{self.parent.winfo_x()+300}+{self.parent.winfo_y()+100}")) #Main App: 900x600
        self.buttons = []
        self.wm_iconbitmap()
        self.after(200,lambda: self.iconbitmap(self.parent.icon_ico_path))
        self.configure(fg_color=self.parent.colors["application_fg"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = CTkFrame(self,fg_color=self.parent.colors["remove_files"], border_width=4,
                                                        border_color=self.parent.colors["remove_files_border"], corner_radius=16)
        self.frame.grid(row=0, column=0, sticky="nsew",padx=10,pady=10)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.lable = CTkLabel(self.frame, text="Choose files to remove",text_color=self.parent.colors["remove_files_text_color"],font=("Arial", 18))
        self.lable.grid(row = 0, column = 0, padx = 10, pady = (10,0), columnspan = 2, sticky = "nsew")

        scrollable_checkbox = CTkScrollableFrame(self.frame,fg_color=self.parent.colors["scrollable_frame"])
        scrollable_checkbox.grid(row = 1, column = 0, padx = 10, pady = (10,0), sticky = "nsew", columnspan = 2)
        scrollable_checkbox.grid_columnconfigure(1,weight=1)

        count = 0
        path_folder = self.parent.versions_path + self.parent.selected_folder
        files = listdir(path_folder)
        for file in files:
            file_checkbox = CTkCheckBox(scrollable_checkbox,text="",width=0,
                                        font=("Arial",24),onvalue=file,offvalue="False")
            file_button = CTkButton(scrollable_checkbox,text=file,fg_color=self.parent.colors["button_on"],
                                      hover_color=self.parent.colors["button_on"])
            file_button.grid(row=count,column=1,padx=(0,10),pady=(10,0),sticky="nsew")
            file_checkbox.grid(row=count,column = 0, padx = (10,0), pady = (10,0), sticky = "nsew")
            self.buttons.append(file_checkbox)
            count += 1

        confirm_button = CTkButton(self.frame,text="Confirm",command=self.confirm,fg_color=self.parent.colors["button_on"],
                                   hover_color=self.parent.colors["button_hover"])
        confirm_button.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = "nsew")
        cancel_button = CTkButton(self.frame,text="Cancel",command=self.cancel,fg_color=self.parent.colors["button_on"],
                                   hover_color=self.parent.colors["button_hover"])
        cancel_button.grid(row = 2, column = 0, padx=(10,0), pady=10, sticky="nsew")

    def confirm(self):

        count = 0
        for b in self.buttons:
            if b.get() != "False":
                count += 1

        if count == 0:
            self.lable.configure(text="No files selected!")
            return

        for b in self.buttons:
            if b.get() != "False":
                file_path = self.parent.versions_path + self.parent.selected_folder + "\\" + b.get()
                remove(file_path)
                print("Removing: "+file_path)

        self.parent.refresh_folders(True)

        self.destroy()

    def cancel(self):
        self.destroy()

class CreateNewCategory(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Create category")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.after(1,self.geometry(f"500x200+{self.parent.winfo_x()+200}+{self.parent.winfo_y()+225}")) #Main App: 900x600
        self.buttons = []
        self.wm_iconbitmap()
        self.after(200,lambda: self.iconbitmap(self.parent.icon_ico_path))
        self.configure(fg_color=self.parent.colors["application_fg"])

        self.max_name_length = 20

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = CTkFrame(self,fg_color=self.parent.colors["create_category"], border_width=4,
                                                        border_color=self.parent.colors["create_category_border"], corner_radius=16)
        self.frame.grid(row=0, column=0, sticky="nsew",padx=10,pady=10)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.lable = CTkLabel(self.frame, text="Type the name of the new category",text_color=self.parent.colors["create_category_text_color"],font=("Arial", 18))
        self.lable.grid(row = 0, column = 0, padx = 10, pady = (10,0), columnspan = 2, sticky = "nsew")

        self.text_typer = CTkEntry(self.frame,placeholder_text="For example: Speedrun",font=("Arial", 28))
        self.text_typer.grid(row=2,column=0,padx=10,pady=10,sticky="nsew", columnspan = 2)

        confirm_button = CTkButton(self.frame,text="Confirm",command=self.confirm,fg_color=self.parent.colors["button_on"],
                                   hover_color=self.parent.colors["button_hover"])
        confirm_button.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = "nsew")
        cancel_button = CTkButton(self.frame,text="Cancel",command=self.cancel,fg_color=self.parent.colors["button_on"],
                                   hover_color=self.parent.colors["button_hover"])
        cancel_button.grid(row = 2, column = 0, padx=(10,0), pady=10, sticky="nsew")

    def confirm(self):

        category_name = self.text_typer.get()

        if not category_name.strip():
            self.lable.configure(text="Category name can not be empty!")
            return

        for folder in self.parent.sorted_folders:
            if category_name == folder["name"]:
                self.lable.configure(text="This category already exists!")
                return

        if len(category_name) > self.max_name_length:
            self.lable.configure(text=f"Name too long! Max {self.max_name_length} characters!")
            return


        mkdir(self.parent.versions_path + category_name)
        self.parent.refresh_folders(True)
        print("Created category:", category_name)

        self.parent.refresh_folders(True)

        self.destroy()

    def cancel(self):
        self.destroy()

class DeleteSelectedFilesPopup(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Remove category")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.after(1,self.geometry(f"300x400+{self.parent.winfo_x()+300}+{self.parent.winfo_y()+100}")) #Main App: 900x600
        self.buttons = []
        self.wm_iconbitmap()
        self.after(200,lambda: self.iconbitmap(self.parent.icon_ico_path))
        self.configure(fg_color=self.parent.colors["application_fg"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = CTkFrame(self,fg_color=self.parent.colors["remove_categories"], border_width=4,
                                                        border_color=self.parent.colors["remove_categories_border"], corner_radius=16)
        self.frame.grid(row=0, column=0, sticky="nsew",padx=10,pady=10)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.lable = CTkLabel(self.frame, text="Choose categories to remove",text_color=self.parent.colors["remove_categories_text_color"],font=("Arial", 18))
        self.lable.grid(row = 0, column = 0, padx = 10, pady = (10,0), columnspan = 2, sticky = "nsew")

        scrollable_checkbox = CTkScrollableFrame(self.frame,fg_color=self.parent.colors["scrollable_frame"])
        scrollable_checkbox.grid(row = 1, column = 0, padx = 10, pady = (10,0), sticky = "nsew", columnspan = 2)
        scrollable_checkbox.grid_columnconfigure(1,weight=1)

        count = 0
        for folder in self.parent.sorted_folders:
            folder_checkbox = CTkCheckBox(scrollable_checkbox,text="",width=0,
                                        font=("Arial",24),onvalue=folder["name"],offvalue="False")
            folder_button = CTkButton(scrollable_checkbox,text=folder["name"],fg_color=self.parent.colors["button_on"],
                                      hover_color=self.parent.colors["button_on"])
            folder_button.grid(row=count,column=1,padx=(0,10),pady=(10,0),sticky="nsew")
            folder_checkbox.grid(row=count,column = 0, padx = (10,0), pady = (10,0), sticky = "nsew")
            self.buttons.append(folder_checkbox)
            count += 1

        confirm_button = CTkButton(self.frame,text="Confirm",command=self.confirm,fg_color=self.parent.colors["button_on"],
                                   hover_color=self.parent.colors["button_hover"])
        confirm_button.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = "nsew")
        cancel_button = CTkButton(self.frame,text="Cancel",command=self.cancel,fg_color=self.parent.colors["button_on"],
                                   hover_color=self.parent.colors["button_hover"])
        cancel_button.grid(row = 2, column = 0, padx=(10,0), pady=10, sticky="nsew")

    def confirm(self):

        existing_categories_count = len(self.parent.sorted_folders)
        count = 0
        for b in self.buttons:
            if b.get() != "False":
                count += 1

        if count == 0:
            self.lable.configure(text="No categories selected!")
            return

        if count >= existing_categories_count:
            self.lable.configure(text="At least one category has to exist!",font=("Arial", 17))
            return

        for b in self.buttons:
            if b.get() != "False":
                folder_path = self.parent.versions_path + b.get()
                rmtree(folder_path)
                print("Removing: "+folder_path)

        self.parent.refresh_folders(True)

        self.destroy()

    def cancel(self):
        self.destroy()

class VersionsFrame(CTkScrollableFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.app = app
        self.folders = app.sorted_folders
        self.version_buttons = []
        self.configure(fg_color=self.app.colors["scrollable_frame"])

        self.selected_version = -1
        self.selected_version_name = "None"

        self.create_version_buttons()

    def create_version_buttons(self):

        #self.remove_version_buttons()

        self.app.stats = {}
        with open(self.app.stats_path, 'r') as file:
            self.app.stats = load(file)

        for f, folder in enumerate(self.folders):

            vb = []

            for v, version in enumerate(folder["versions"]):
                version_button = CTkButton(self, text=version)
                version_button.configure(command = lambda refer = version_button: self.select_button(refer),hover_color=self.app.colors["button_hover"])
                version_button.grid(row=v, column=0, padx=10, pady=(10, 0), sticky="we")

                self.switch_folders(self.app.selected_folder)

                temp_stats = dict(self.app.stats)
                print("STATS: "+str(temp_stats["version_play_time"]))
                if len(self.app.stats) == 0:
                    nstat = \
                        {
                            "last_played": "Not played",
                            "time_played": 0
                        }

                    self.app.stats["version_play_time"][version] = nstat
                else:
                    exist = False
                    for n, name in enumerate(temp_stats["version_play_time"]):

                        print(str(name)," : ",version)

                        if name == version:
                            print("Broke, because it exists!: " + str(name))
                            exist = True
                            break
                    if not exist:
                        print("Creating new stat cause it does not exist!")
                        nstat = \
                            {
                                "last_played": "Not played",
                                "time_played": 0
                            }
                        self.app.stats["version_play_time"][version] = nstat
                    else:
                        print("It already exists!")

                vb.append(version_button)

            vb2 = {"name": folder["name"], "buttons":vb}
            self.version_buttons.append(vb2)

        print("VERSION BUTTONS NEW: " + str(self.version_buttons))

        thread = Thread(target=self.app.save_stats, daemon=True)
        thread.start()

    def switch_folders(self,selected_folder):
        self.selected_version = -1
        self.selected_version_name = "Select version"

        for f, folder in enumerate(self.version_buttons):
            if folder["name"] == selected_folder:
                for b, button in enumerate(folder["buttons"]):
                    button.configure(state="normal",fg_color = self.app.colors["button_on"])
                    button.grid(row=b, column=0, padx=10, pady=(10, 0), sticky="we")
            else:
                for b, button in enumerate(folder["buttons"]):
                    button.configure(state="disabled")
                    button.grid_forget()

        self.app.update_description(self.selected_version_name,self.app.selected_folder,True)

    def remove_version_buttons(self):
        for f,folder in enumerate(self.version_buttons):
            for b,button in enumerate(folder["buttons"]):
                button.destroy()

        self.version_buttons = []


    def select_button(self, refer):
        if refer.cget("state") == "normal":
            for f,folder in enumerate(self.version_buttons):
                if folder["name"] == self.app.selected_folder:
                    button_id = refer.grid_info()["row"]

                    folder["buttons"][self.selected_version].configure(fg_color = self.app.colors["button_on"]) #ON
                    folder["buttons"][button_id].configure(fg_color = self.app.colors["button_selected"]) #OFF

                    self.selected_version = button_id
                    self.selected_version_name = refer.cget("text")

                    self.app.update_description(self.selected_version_name,self.app.selected_folder)

                    print("Selected version: "+ str(folder["buttons"][button_id].cget("text")))
                    break

class App(CTk):
    def __init__(self):
        super().__init__()

        # Bind window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Register atexit handler
        register(self.cleanup)

        # Register crash handler
        excepthook = self.handle_crash

        self.program_path = getcwd()
        self.icon_ico_path = self.program_path + "\\system\\images\\icon_main_app.ico"
        self.icon_png = PhotoImage(file = self.program_path + "\\system\\images\\icon_add_app.png")
        self.versions_path = self.program_path + "\\versions\\"
        self.setting_path = self.program_path + "\\system\\settings.json"
        self.stats_path = self.program_path + "\\system\\stats.json"
        self.tas_path = self.program_path + "\\TAS"
        self.tas_exe_path = "\\TAS.Studio\\TAS.Studio.exe"
        self.temp_perm_path = self.program_path + "\\system\\temp"

        self.settings = {}
        with open(self.setting_path, 'r') as file:
            self.settings = load(file)

        self.stats = {}
        try:
            self.validate_stats()
        except:
            print("--- Something went wrong while validating stats. Program has been stopped! ---")
            exit()

        # Get the content of the stats.json
        with open(self.stats_path, 'r') as file:
            self.stats = load(file)

        # Check if total_play_time exists!
        if "total_play_time" not in self.stats:
            self.stats["total_play_time"] = 0

        self.colors = self.settings["colors"]

        self.title("Smol Ame Launcher")
        self.geometry("900x640")
        self.resizable(False,False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.iconbitmap(self.icon_ico_path)
        self.configure(fg_color=self.colors["application_fg"])
        self.sorted_folders = []
        self.refresh_folders(False)

        self.options_frame = CTkFrame(self,fg_color=self.colors["options_frame"],border_width=4,
                                                        border_color=self.colors["options_frame_border"],corner_radius=16)
        self.options_frame.grid(row=0,column=0,padx=10, pady=(10,0), sticky="nsew",columnspan = 2)
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_columnconfigure(2, weight=2)
        self.options_frame.grid_columnconfigure(3, weight=2)

        self.username_frame = CTkFrame(self,fg_color=self.colors["username_frame"],border_width=4,
                                                        border_color=self.colors["username_frame_border"],corner_radius=16)
        self.username_frame.grid_columnconfigure(0, weight=1) 
        self.username_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)

        self.username_frame.grid_columnconfigure(0, weight=0) # Label (Fixed width)
        self.username_frame.grid_columnconfigure(1, weight=1) # Entry (Expands)
        self.username_frame.grid_columnconfigure(2, weight=0) # Button (Fixed width)

        # 1. First Column: The Label
        self.user_label = CTkLabel(self.username_frame, text="Username:", font=("Arial", 16))
        self.user_label.grid(row=0, column=0, padx=(20, 10), pady=10)

        # 2. Second Column: The Textbox (Entry)
        self.user_entry = CTkEntry(self.username_frame, placeholder_text="Enter name...")
        self.user_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # 3. Third Column: The Button
        self.user_save_btn = CTkButton(self.username_frame, 
                                       text="Save", 
                                       width=100,
                                       command=self.set_username, # Your function here
                                       fg_color=self.colors["button_on"],
                                       hover_color=self.colors["button_hover"])
        self.user_save_btn.grid(row=0, column=2, padx=(10, 20), pady=10)  

        self.versions_frame = CTkFrame(self,fg_color=self.colors["version_frame"],border_width=4,
                                                        border_color=self.colors["version_frame_border"],corner_radius=16)
        self.versions_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.versions_frame.grid_columnconfigure(0, weight=1)
        self.versions_frame.grid_rowconfigure(1,weight=6)
        self.versions_frame.grid_rowconfigure(2,weight=1)

        self.description_frame = CTkFrame(self,fg_color=self.colors["description_frame"], border_width=4,
                                                        border_color=self.colors["description_frame_border"], corner_radius=16)
        self.description_frame.grid(row=2, column=1, padx=(0,10), pady=10, sticky="nsew")


        self.combo = []
        for i in self.sorted_folders:
            self.combo.append(i["name"])

        if len(self.combo) != 0:
            self.selected_folder = self.combo[0]
        self.menu_box = CTkOptionMenu(self.versions_frame,values=self.combo, command=self.change_folder,
                                                    fg_color=self.colors["menu"],button_color=self.colors["menu_button"],
                                                    button_hover_color=self.colors["menu_button_hover"],
                                                    dropdown_fg_color=self.colors["dropdown"],
                                                    dropdown_hover_color=self.colors["dropdown_hover"])
        if len(self.combo) != 0:
            self.menu_box.set(self.combo[0])
        else:
            self.menu_box.configure(state="disabled")
        self.menu_box.grid(row=0, column=0, padx=20, pady=(20,0), sticky="nsew")

        self.folder_tile = CTkLabel(self.description_frame, text=self.selected_folder,
                                                    text_color=self.colors["folder_title_color"], height = 80)
        self.folder_tile.pack(pady=(20, 0), anchor="center")
        self.folder_tile.configure(font=("Ariel", 64))

        self.version_title = CTkLabel(self.description_frame, text="",
                                                    text_color=self.colors["version_title_color"], height = 55)
        self.version_title.pack(pady=(10, 0), anchor="center")
        self.version_title.configure(font=("Ariel", 42))

        self.last_played_tittle = CTkLabel(self.description_frame, text=f"Last played: Not played",
                                                            text_color=self.colors["last_played_text_color"], )
        self.last_played_tittle.pack(padx=(30,0), pady=(60, 0), anchor="w")
        self.last_played_tittle.configure(font=("Ariel", 32))

        self.time_played_tittle = CTkLabel(self.description_frame, text=f"Time played: Not played",
                                                         text_color=self.colors["time_played_text_color"], )
        self.time_played_tittle.pack(padx=(30, 0), pady=(30, 0), anchor="w")
        self.time_played_tittle.configure(font=("Ariel", 32))

        self.total_play_time_tittle = CTkLabel(self.description_frame, text=f"Total play time: 0s",
                                           text_color=self.colors["time_played_text_color"])
        self.total_play_time_tittle.pack(padx=(30, 0), pady=(90, 0), anchor="w")
        self.total_play_time_tittle.configure(font=("Ariel", 32))

        self.program_version_title = CTkLabel(self.description_frame, text=f"v{self.settings['version']}",
                                                            text_color=self.colors['program_version_color'], )
        self.program_version_title.place(x=530,y=435)
        self.program_version_title.configure(font=("Ariel", 24))

        self.scrollable_button_frame = VersionsFrame(self.versions_frame,self)
        self.scrollable_button_frame.grid(row=2,column=0,padx=20, pady=(10,0), sticky="nsew")

        self.tas_frame = CTkFrame(self.versions_frame,fg_color=self.colors["tas_frame"],border_width=4,
                                                        border_color=self.colors["tas_frame_border"],corner_radius=12,
                                                        height=42,width=80)
        self.tas_frame.grid_propagate(False)
        self.tas_frame.grid(row=3, column=0, padx=10, sticky="")
        self.tas_frame.grid_rowconfigure(0, weight=1)
        self.tas_frame.grid_columnconfigure(0, weight=1)

        self.tas_checkbox = CTkCheckBox(self.tas_frame,text="TAS",width=1,height=1,border_width=2,onvalue=True,offvalue=False)
        self.tas_checkbox.grid(row=0,column=0, pady=0, sticky="")

        self.button_play = CTkButton(self, text="Play", command=self.start_game,fg_color=self.colors["button_on"],hover_color=self.colors["button_hover"])
        self.button_play.grid(row=3, column=1, padx=(0,10), pady=10, sticky="nsew")

        self.button_refresh = CTkButton(self, state="normal", text="Refresh",command=lambda refresh = True: self.refresh_folders(refresh), fg_color=self.colors["button_on"],hover_color=self.colors["button_hover"])
        self.button_refresh.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.scrollable_button_frame.switch_folders(self.selected_folder)

        self.delete_categories_button = CTkButton(self.options_frame, text="Remove categories",
                                                  command=lambda parent=self: DeleteSelectedFilesPopup(parent),
                                                  fg_color=self.colors["button_on"],hover_color=self.colors["button_hover"])
        self.delete_categories_button.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ew")

        self.create_categories_button = CTkButton(self.options_frame, text="Add category",
                                                  command= lambda parent=self: CreateNewCategory(parent),
                                                  fg_color=self.colors["button_on"],hover_color=self.colors["button_hover"])
        self.create_categories_button.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="ew")

        self.import_files_button = CTkButton(self.options_frame, text="Import files to selected category",
                                                  command=self.import_files,
                                                  fg_color=self.colors["button_on"],hover_color=self.colors["button_hover"])
        self.import_files_button.grid(row=0, column=2, padx=(10, 0), pady=10, sticky="ew")

        self.remove_files_button = CTkButton(self.options_frame, text="Remove files from selected category",
                                             command= lambda parent = self: RemoveSelectedFiles(parent),
                                             fg_color=self.colors["button_on"], hover_color=self.colors["button_hover"])
        self.remove_files_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    def validate_stats(self):

        print("--- Started validating stats ---")

        # Check if stats.json exists!
        try:
            # Get the content of the stats.json. If it's invalid or does not exist, override it with empty dictionary
            with open(self.stats_path, 'r') as file:
                self.stats = load(file)
            print("Stats.json is a valid json file! Loaded successfully!")
        except:
            print("Stats.json is not a valid json file or does not exist! Failed to load!")

        # Check if total_play_time exists in the stats and if it is an int or float. If one of those is false, override it with 0
        if "total_play_time" not in self.stats:
            self.stats["total_play_time"] = 0
            print("Total play time didn't exist! Created it!")
        elif not isinstance(self.stats["total_play_time"],(int,float)):
            self.stats["total_play_time"] = 0
            print("Total play time wasn't a float or int! Set it to 0!")
        else:
            print("Total play time is a valid float or int!")

        # Check if version_play_time exists in the stats and if it is an dictionary. If one of those is false, override it with empty dictionary
        if "version_play_time" not in self.stats:
            self.stats["version_play_time"] = {}
            print("Version play time didn't exist! Created it!")
        elif not isinstance(self.stats["version_play_time"],dict):
            self.stats["version_play_time"] = {}
            print("Version play time was not a dicitonary! Cleared and made it a dictionary!")
        else:
            print("Version play time is a valid dictionary!")

        # Save stats (duh)
        self.save_stats()

        print("--- Finished validating stats ---")

    def remove_files(self):

        path_folder = self.versions_path + self.selected_folder
        files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=[(path_folder, "*.zip")]
        )

        if len(files) == 0:
            print("No files selected")
            return

        print(path_folder)
        for file in files:
            try:
                print("Copied "+file+" to "+path_folder)
                copy(file,path_folder)
            except:
                pass
        self.refresh_folders(True)

    def import_files(self):
        files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=[("All files", "*.zip")]
        )

        if len(files) == 0:
            print("No files selected")
            return

        path_folder = self.versions_path + self.selected_folder
        print(path_folder)
        for file in files:
            try:
                print("Copied "+file+" to "+path_folder)
                copy(file,path_folder)
            except:
                pass
        self.refresh_folders(True)


    def update_description(self,tn,fn,reset = False):

        max_folder_width_text_pixels = 648
        max_version_width_text_pixels = 10000
        fts = 64
        vts = 48

        f = font.Font(family="Ariel", size=fts)
        print("Folder height: "+str(f.metrics("linespace")))
        fw = f.measure(fn)
        while fw > max_folder_width_text_pixels:
            fts -= 1
            f.configure(size=fts)
            fw = f.measure(fn)
            print("Folder font too big: "+str(fw))

        f.configure(size=vts)
        print("Version height: " +str(f.metrics("linespace")))
        fw = f.measure(tn)
        while fw > max_folder_width_text_pixels:
            vts -= 1
            f.configure(size=vts)
            fw = f.measure(tn)
            print("Version font too big: " + str(fw))
        print(f.measure(tn))

        self.version_title.configure(text=f"- {tn} -",font=("Ariel",vts))
        self.folder_tile.configure(text=f"- {fn} -",font=("Ariel",fts))
        if tn != "Select version":
            self.last_played_tittle.configure(text=f"Last played: {self.stats['version_play_time'][tn]['last_played']}")
            self.time_played_tittle.configure(text=f"Time played: {self.format_playtime(self.stats['version_play_time'][tn]['time_played'])}")
        if reset:
            self.last_played_tittle.configure(text=f"Last played: ")
            self.time_played_tittle.configure(text=f"Time played: ")

        self.total_play_time_tittle.configure(
            text=f"Total play time: {self.format_playtime(self.stats['total_play_time'])}")

    def change_folder(self,choice):
        self.selected_folder = choice

        nstr = choice[:12]
        if len(choice) > 12:
            nstr += "..."

        self.menu_box.set(nstr)
        self.scrollable_button_frame.switch_folders(self.selected_folder)

    def refresh_folders(self,refresh):

        self.sorted_folders = []
        folders = listdir(self.versions_path)
        print("All folders: "+str(folders))

        #runs throught all folders in "versions" folder
        for i, f_name in enumerate(folders):

            t_folder = {"name": f_name, "versions": []}

            #gets the path to the file
            f_path = self.versions_path + f_name

            #checks if given path is path to the directory (folder)
            if isdir(f_path):

                #gets the path to the file
                versions = listdir(f_path)

                for ii, v_name in enumerate(versions):

                    if str.endswith(v_name, ".zip"):
                        t_folder["versions"].append(str.removesuffix(v_name,".zip"))

                self.sorted_folders.append(t_folder)


        if refresh:

            self.combo = []
            for i in self.sorted_folders:
                self.combo.append(i["name"])
            self.selected_folder = self.combo[0]
            self.menu_box.configure(values=self.combo)
            self.menu_box.set(self.selected_folder)

            self.scrollable_button_frame.remove_version_buttons()
            self.scrollable_button_frame.folders = self.sorted_folders
            self.scrollable_button_frame.create_version_buttons()

            self.change_folder(self.selected_folder)

        print("Folders refreshed: "+str(self.sorted_folders))

    def run_game_code(self):

        scf = self.scrollable_button_frame

        if scf.selected_version == -1:
            mb.showinfo("Info","Please select game version first!")
            return

        # Disable Play button to stop spam

        self.enable_buttons(False)
        self.button_play.configure(text="Loading...")

        found = False

        for f, folder in enumerate(scf.version_buttons):

            if folder["name"] == self.selected_folder:
                found = True

                version_name = scf.version_buttons[f]["buttons"][scf.selected_version].cget("text")
                zpath = f"{self.versions_path}{self.selected_folder}\\{version_name}.zip"

                try:
                    self.button_play.configure(text="Extracting files...")
                    zp = ZipFile(zpath)
                except:
                    mb.showerror("Error", f"ERROR: Couldn't open ZIP: {zpath}\n\nDid you change the name of the ZIP or remove it after opening the app?")
                    self.enable_buttons()
                    self.button_play.configure(text="Play")
                    return

                # Extract to temp perm folder
                zp.extractall(self.temp_perm_path)
                zp.close()

                print("Temp extraction folder:", self.temp_perm_path)

                # Coping TAS files and run TAS

                if self.tas_checkbox.get():
                    self.button_play.configure(text="Copying TAS files...")
                    try:
                        tas_files = listdir(self.tas_path)
                        for file_name in tas_files:
                            file_path = join(self.tas_path,file_name)

                            if isdir(file_path):
                                dest = self.temp_perm_path + "\\" + file_name
                                print("Coping folder: \"", file_path,"\" to: \"",dest)
                                copytree(file_path,dest,dirs_exist_ok=True)
                            else:
                                print("Coping file: \"", file_path, "\" to: \"", self.temp_perm_path)
                                copy(file_path, self.temp_perm_path)
                    except:
                        print("Unable to copy: \"", file_path, "\" to: \"", self.temp_perm_path)
                        mb.showerror("Error",
                                     f"ERROR: Couldn't copy TAS files: {zpath}")
                        self.enable_buttons()
                        self.button_play.configure(text="Play")
                        return

                    self.button_play.configure(text="Running TAS...")
                    tas_exe = self.temp_perm_path + self.tas_exe_path
                    try:
                        self.tas_process = Popen([tas_exe])
                    except:
                        mb.showerror("Error",
                                     f"ERROR: Couldn't find TAS exe file: {tas_exe}")
                        self.enable_buttons()
                        self.button_play.configure(text="Play")
                        return

                # Find EXE
                self.button_play.configure(text="Finding '.exe' file...")
                exe_path = None
                for name in listdir(self.temp_perm_path):
                    full = join(self.temp_perm_path, name)

                    if isfile(full) and name.endswith(".exe") and name != "UnityCrashHandler64.exe":
                        exe_path = full
                        break

                if exe_path is None:
                    mb.showerror("Error", f"ERROR: No valid .exe found: {zpath}!\n\nAre you sure that the game's .exe file is located directly in the selected ZIP file?")
                    self.enable_buttons()
                    self.button_play.configure(text="Play")
                    return

                # Update last played database
                self.update_last_played(version_name)

                # Start the game
                print("Running:", exe_path)
                self.game_start_time = time()
                self.button_play.configure(text="Running...")
                self.game_process = Popen([exe_path])
                self.iconify()

                # Begin checking for game close
                self.after(1000, self._check_game_closed)
                return

        if not found:
            mb.showerror("Error", "ERROR: Couldn't find right folder!")
            self.enable_buttons()
            self.button_play.configure(text="Play")

    def _check_game_closed(self):

        sbf = self.scrollable_button_frame

        # Game still running → check again in 1 sec
        if self.game_process.poll() is None:
            self.after(1000, self._check_game_closed)
            return

        # Game closed
        elapsed = time() - self.game_start_time

        version_name = "None"

        for f,folder in enumerate(self.sorted_folders):
            if folder["name"] == self.selected_folder:
                for v,version in enumerate(folder["versions"]):
                    if version == sbf.selected_version_name:
                        version_name = version

        if version_name != "None":
            self.add_play_time(version_name, elapsed)

        else:
            print("Coun't find the version!")

        if hasattr(self,"tas_process") and self.tas_process:
            if self.tas_process.poll() is None:
                print("Terminating running tas...")
                self.tas_process.terminate()
                try:
                    self.tas_process.wait(timeout=3)
                except TimeoutExpired:
                    print("Force killing tas...")
                    self.tas_process.kill()
                self.tas_process = None

        self.clear_folder(self.temp_perm_path)

        # Re-enable Play button
        self.enable_buttons()
        self.button_play.configure(text="Play")
        self.deiconify()
        self.lift()

    def add_play_time(self, version_name, seconds_played):
        time = self.stats["version_play_time"][version_name]["time_played"]
        ttime = self.stats["total_play_time"]
        # Add play time
        time += seconds_played
        ttime += seconds_played
        time = round(time, 0)
        ttime = round(ttime, 0)

        self.update_time_played(version_name,time,ttime)

    def start_game(self):
        thread = Thread(target=self.run_game_code, daemon=True)
        thread.start()

    def format_playtime(self, seconds):
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0 or hours > 0:  # show minutes if hours exist
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")

        return " ".join(parts)

    def update_last_played(self, name):

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.stats["version_play_time"][name]["last_played"] = date
        self.update_description(self.scrollable_button_frame.selected_version_name,self.selected_folder)

        thread = Thread(target=self.save_stats, daemon=True)
        thread.start()

    def update_time_played(self, name, time_played,total_played):
        self.stats["version_play_time"][name]["time_played"] = time_played
        self.stats["total_play_time"] = total_played
        self.update_description(self.scrollable_button_frame.selected_version_name, self.selected_folder)

        thread = Thread(target=self.save_stats, daemon=True)
        thread.start()

    def save_stats(self):
        with open(self.stats_path, "w") as json_file:
            dump(self.stats, json_file, indent=4)

    def enable_buttons(self,enable=True):

        s = "disabled"
        if enable:
            s = "normal"

        self.button_play.configure(state=s)
        self.button_refresh.configure(state=s)
        self.menu_box.configure(state=s)
        self.tas_checkbox.configure(state=s)
        self.delete_categories_button.configure(state=s)
        self.create_categories_button.configure(state=s)
        self.import_files_button.configure(state=s)
        self.remove_files_button.configure(state=s)

        for f, folder in enumerate(self.scrollable_button_frame.version_buttons):
            for v, versinon in enumerate(folder["buttons"]):
                versinon.configure(state=s)

    def clear_folder(self, target):

        files = listdir(target)

        for f in files:
            try:
                file_path = join(target, f)

                if isfile(file_path):
                    remove(file_path)
                    print("Removed file: " + file_path)
                if isdir(file_path):
                    rmtree(file_path)
                    print("Removed folder: " + file_path)
            except:
                print("Unable to clear: \"", file_path)
                mb.showerror("Error",
                             f"ERROR: Unable to clear: {file_path}")
                self.enable_buttons()
                self.button_play.configure(text="Play")
                return
        print("--------------------")
        print("Done clearing folder: " + target)


    def on_closing(self):
        print("Window closed by user (X or ALT+F4)")
        self.cleanup()
        self.destroy()

    def cleanup(self):
        print("Running cleanup...")

        # Stop game if running
        if hasattr(self, "game_process") and self.game_process:
            if self.game_process.poll() is None:
                print("Terminating running game...")
                self.game_process.terminate()
                try:
                    self.game_process.wait(timeout=5)
                except TimeoutExpired:
                    print("Force killing game...")
                    self.game_process.kill()

                self._check_game_closed()
                self.game_process = None

        # Clear temp perm folder
        if hasattr(self, "temp_perm_path") and self.temp_perm_path:
            print("Cleaning temporary permna folder...")
            self.clear_folder(self.temp_perm_path)

        # Save stats
        if hasattr(self, "stats") and self.stats:
            print("Saving stats...")
            try:
                pass
            except Exception as e:
                print("Error saving stats:", e)

        print("Cleanup complete.")

    def handle_crash(self, exc_type, exc_value, exc_traceback):
        print("Script crashed!")
        print("".join(format_exception(exc_type, exc_value, exc_traceback)))
        self.cleanup()
    
    def set_username(self):
        print("username set")

app = App()
app.mainloop()

