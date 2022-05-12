import importlib
import time
import re
from sys import argv
from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (BadRequest, ChatMigrated, NetworkError, TelegramError, TimedOut, Unauthorized)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Filters, MessageHandler

from GPSiteInfoBot import (
    CERT_PATH,
    LOGGER,
    IGNORE_PENDING_REQUESTS,
    OWNER_ID,
    TOKEN,
    dispatcher,
    StartTime,
    SUPPORT_CHAT,
    pbot,
    PORT,
    telethn,
    URL,
    WEBHOOK,
    updater)


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


Bot_Photo = "https://telegra.ph/file/c06d92681208824918821.jpg"

def start(update, context):
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
                        [[InlineKeyboardButton(text="Back", callback_data="help_back")]],
                    ),
                )
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
            update.effective_message.reply_photo(
                Bot_Photo,
                PM_START_TEXT.format(
                    escape_markdown(first_name), escape_markdown(context.bot.first_name),
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="✅ Add me in your group",
                                url="t.me/{}?startgroup=true".format(
                                    context.bot.username,
                                ),
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="☯️ Cloud Group",
                                url="https://t.me/+WKZqyWNHpLViMmI1",
                            ),
                            InlineKeyboardButton(
                                text="✳ Find More",
                                url="https://github.com/AL-Noman21",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="🕎 Atrocious Bot Owner",
                                url="https://t.me/smexynos7870",
                            ),
                        ],
                    ],
                ),
            )
    else:
        update.effective_message.reply_photo(
            Bot_Photo,
            GROUP_START_TEXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML)


PM_START_TEXT = """
Hello {}, I'm {}
I can mirror all your links to Google drive. But in pm or unauthorized group you can use all telegram upload tools. If you want to upload in Google Drive you need to join Atrocious Cloud Drive.
For commands and help press /help .
"""

GROUP_START_TEXT = """
Hello, I'm Atrocious Mirror Bot.
I can mirror all your links to Google drive. But in pm or unauthorized group you can use all telegram upload tools. If you want to upload in Google Drive you need to join Atrocious Cloud Drive.
For help and commands press /help .
"""

buttons = [[InlineKeyboardButton(text="☸ Cloud Drive Group", url="https://t.me/+WKZqyWNHpLViMmI1"),],

          [InlineKeyboardButton(text="✅ Add me in your group", url="t.me/Atrocious_Mirror_Bot?startgroup=true",)],]


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendMessage(f"@{SUPPORT_CHAT}", "I am now online!")
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to SUPPORT_CHAT, go support chat group and add bot in admin")
        except BadRequest as e:
            LOGGER.warning(e.message)


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

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()

if __name__ == "__main__":
    LOGGER.info("Starting Pyrogram")
    pbot.start()
    LOGGER.info("Starting Telethon")
    telethn.start(bot_token=TOKEN)
    main()
