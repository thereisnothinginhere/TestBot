import logging
import os
import sys
import time
import threading
import telegram.ext as tg

from pyrogram import Client
from telegram.ext import CallbackContext
from telethon import TelegramClient

AS_DOC_USERS = set()
AS_MEDIA_USERS = set()
DRIVES_IDS = []
DRIVES_NAMES = []
INDEX_URLS = []
Interval = []
download_dict = {}
download_dict_lock = threading.Lock()
status_reply_dict = {}
status_reply_dict_lock = threading.Lock()
StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)


    try:
        AUTHORIZED_CHATS = set(int(x) for x in os.environ.get("AUTHORIZED_CHATS", "").split())
    except ValueError:
        raise Exception(
            "Your authorized chat list does not contain valid integers.")

    ALLOW_CHATS = "True"
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", True)
    API_HASH = os.environ.get("API_HASH", None)
    API_ID = os.environ.get("API_ID", None)
    CERT_PATH = os.environ.get("CERT_PATH")
    DB_URI = os.environ.get("DATABASE_URL")
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    PORT = int(os.environ.get("PORT", 5000))
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
    URL = os.environ.get("URL", "")  # Does not contain token
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    WORKERS = int(os.environ.get("WORKERS", 8))


    # Clone Bot
    AS_DOCUMENT = False
    AUTO_DELETE_MESSAGE_DURATION = -1
    BUTTON_FOUR_NAME = os.environ.get("BUTTON_FOUR_NAME")
    BUTTON_FOUR_URL = os.environ.get("BUTTON_FOUR_URL")
    BUTTON_FIVE_NAME = os.environ.get("BUTTON_FIVE_NAME")
    BUTTON_FIVE_URL = os.environ.get("BUTTON_FIVE_URL")
    BUTTON_SIX_NAME = os.environ.get("BUTTON_SIX_NAME")
    BUTTON_SIX_URL = os.environ.get("BUTTON_SIX_URL")
    CLONE_LIMIT = os.environ.get("CLONE_LIMIT", None)
    CRYPT = os.environ.get("CRYPT", None)
    CUSTOM_FILENAME = None
    DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "usr/src/app/downloads")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    DOWNLOAD_STATUS_UPDATE_INTERVAL = os.environ.get("DOWNLOAD_STATUS_UPDATE_INTERVAL")
    EQUAL_SPLITS = bool(os.environ.get("EQUAL_SPLITS", False))
    INDEX_URLS = os.environ.get("INDEX_URL", None)
    INDEX_URL = os.environ.get("INDEX_URL", None)
    IS_TEAM_DRIVE = bool(os.environ.get("IS_TEAM_DRIVE", False))
    parent_id = os.environ.get("GDRIVE_FOLDER_ID")
    PHPSESSID = os.environ.get("PHPSESSID", None)
    RSS_CHAT_ID = os.environ.get("RSS_CHAT_ID")
    rss_session = os.environ.get("USER_STRING_SESSION, api_id=int(TELEGRAM_API), api_hash=TELEGRAM_HASH", None)
    SHORTENER = os.environ.get("SHORTENER")
    SHORTENER_API = os.environ.get("SHORTENER_API")
    STATUS_LIMIT = os.environ.get("STATUS_LIMIT", "3")
    STOP_DUPLICATE = bool(os.environ.get("STOP_DUPLICATE", False))
    TG_SPLIT_SIZE = os.environ.get("TG_SPLIT_SIZE", 2097151000)
    UPTOBOX_TOKEN = os.environ.get("UPTOBOX_TOKEN", None)
    USE_SERVICE_ACCOUNTS = False
    VIEW_LINK = bool(os.environ.get("VIEW_LINK", False))
    PROCESS_MAX_TIMEOUT = 3600
    TG_MAX_FILE_SIZE = 2097152000

    try:
        BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")
else:
    from GPSiteInfoBot.config import Development as Config

    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    OWNER_USERNAME = Config.OWNER_USERNAME

 
    ALLOW_EXCL = Config.ALLOW_EXCL
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    AUTHORIZED_CHATS = Config.AUTHORIZED_CHATS
    CERT_PATH = Config.CERT_PATH
    DEL_CMDS = Config.DEL_CMDS
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    PORT = Config.PORT
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    URL = Config.URL
    WORKERS = Config.WORKERS
    WEBHOOK = Config.WEBHOOK  
    AUTHORIZED_CHATS = list(AUTHORIZED_CHATS)

DRIVES_NAMES.append("Main")
DRIVES_IDS.append(parent_id)
if os.path.exists("drive_folder"):
    with open("drive_folder", "r+") as f:
        lines = f.readlines()
        for line in lines:
            try:
                temp = line.strip().split()
                DRIVES_IDS.append(temp[1])
                DRIVES_NAMES.append(temp[0].replace("_", " "))
            except:
                pass
            try:
                INDEX_URLS.append(temp[2])
            except IndexError as e:
                INDEX_URLS.append(None)


pbot = Client("PyrogramBot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
telethn = TelegramClient("TelethonBot", API_ID, API_HASH)
updater = tg.Updater(TOKEN, workers=8, use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher

