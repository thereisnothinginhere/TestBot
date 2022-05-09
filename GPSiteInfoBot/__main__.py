import importlib
import time
import re
from sys import argv
from typing import Optional

from GPSiteInfoBot import (
    ALLOW_EXCL,
    CERT_PATH,
    LOGGER,
    OWNER_ID,
    PORT,
    TOKEN,
    URL,
    WEBHOOK,
    dispatcher,
    StartTime,
    SUPPORT_CHAT,
    pbot,
    telethn,
    updater)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!

from .modules import clone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (BadRequest, ChatMigrated, NetworkError, TelegramError, TimedOut, Unauthorized)

from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler)

from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """
Hello {}, I'm {}. [ ](https://telegra.ph/file/c063ef61885578d9e7c20.jpg)
I can give you Grameenphone all site information of Bagerhat.
"""


HELP_STRINGS = """
Hey there! My name is *{}*.
I'm a Hero For Fun and help admins manage their groups. Have a look at the following for an idea of some of \
the things I can help you with.

*Main* commands available:
 • /help: PM's you this message.
 • /help <module name>: PM's you info about that module.
 • /settings:
   • in PM: will send you your settings for all supported modules.
   • in a group: will redirect you to pm, with all that chat's settings.

{}
And the following:
""".format(
    dispatcher.bot.first_name,
    "" if not ALLOW_EXCL else "All commands can either be used with /")


IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}
GDPR = []


dispatcher.run_async
def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


dispatcher.run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="Back", callback_data="help_back")]]))
            elif args[0].lower() == "markdownhelp":
                IMPORTED["extras"].markdown_help_sender(update)
            elif args[0].lower() == "disasters":
                IMPORTED["disasters"].send_disasters(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            last_name = update.effective_user.last_name
            update.effective_message.reply_text(
                PM_START_TEXT.format(
                    escape_markdown(first_name), escape_markdown(context.bot.first_name)),
                parse_mode=ParseMode.MARKDOWN)


GROUP_START_TEXT = """
Hi ,I am Optimus Prime Bot.
I'm a group management bot.
"""

GROUP_START_BUTTONS = [[InlineKeyboardButton(text="☸ Repository", url="https://github.com/Al-Noman-Pro/GPSiteInfoBot"),],

                      [InlineKeyboardButton(text="✅ Add me in your group", url="t.me/GPSiteInfoBot_Pro_Bot?startgroup=true")],]


def main():

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)


    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)


pbot.start()
main()
