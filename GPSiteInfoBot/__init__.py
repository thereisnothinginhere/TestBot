import logging
import os
import sys
import time
import spamwatch
import threading
import telegram.ext as tg

from telegram.ext import CallbackContext
from telethon import TelegramClient

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

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(int(x) for x in os.environ.get("SUPPORT_USERS", "").split())
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(int(x) for x in os.environ.get("WHITELIST_USERS", "").split())
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGER_USERS = set(int(x) for x in os.environ.get("TIGER_USERS", "").split())
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        AUTHORIZED_CHATS = set(int(x) for x in os.environ.get("AUTHORIZED_CHATS", "").split())
    except ValueError:
        raise Exception(
            "Your authorized chat list does not contain valid integers.")

    ALLOW_CHATS = "True"
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    API_HASH = os.environ.get("API_HASH", None)
    API_ID = os.environ.get("API_ID", None)
    CERT_PATH = os.environ.get("CERT_PATH")
    DB_URI = os.environ.get("DATABASE_URL")
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    INFOPIC = bool(os.environ.get("INFOPIC", False))
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    PORT = int(os.environ.get("PORT", 5000))
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
    URL = os.environ.get("URL", "")  # Does not contain token
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    WORKERS = int(os.environ.get("WORKERS", 8))
    sw = "T5WnpMhoKlC0PfWntW56c6t0YnkYQCZLDlRLKnQPAh9iRcrc2ijyDJMjQvknijJJ"

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

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGER_USERS = set(int(x) for x in Config.TIGER_USERS or [])
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")


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


telethn = TelegramClient("TelethonBot", API_ID, API_HASH)
updater = tg.Updater(TOKEN, workers=8, use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher

SUDO_USERS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

AUTHORIZED_CHATS = list(AUTHORIZED_CHATS)
SUDO_USERS = list(SUDO_USERS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)
TIGER_USERS = list(TIGER_USERS)

# Load at end to ensure all prev variables have been set
from GPSiteInfoBot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler)

# make sure the regex handler can take extra kwargs
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
