import os
import sys

from platformdirs import user_data_dir

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
    if BASE_PATH not in sys.path:
        sys.path.insert(0, BASE_PATH)
else:
    # Running from source, go up one level from 'launcher/'
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if BASE_PATH not in sys.path:
        sys.path.insert(0, BASE_PATH)

APPLICATION_NAME = "Smol Ame Launcher"
AUTHOR_NAME = "Witcherchan"
LOCAL_PATH = user_data_dir(APPLICATION_NAME,AUTHOR_NAME)
BASE_APPLICATION_SIZE = (900,640)
MIN_APPLICATION_SIZE = (900,640)
