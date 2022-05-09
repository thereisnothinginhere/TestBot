# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.

import json
import os


def get_user_list(config, key):
    with open('{}/GPSiteInfoBot/{}'.format(os.getcwd(), config),
              'r') as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    #Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 2076846
    API_HASH = "a7c38b63155953f8c529718a3ac0003a"
    TOKEN = "5223488987:AAElKjdePVrpuRtUbU0K31cFNG_jU2ndJzs"
    OWNER_ID = 1063430421
    OWNER_USERNAME = "smexynos7870"
    SUPPORT_CHAT = "AtrociousBotSupport"
    JOIN_LOGGER = -1001157029074
    EVENT_LOGS = -1001648580903

    #RECOMMENDED
    SQLALCHEMY_DATABASE_URI = "postgres://fiybstodajfijm:17052b4a6e1c723dd6d300a0ec324961b03becb561f62fa90cf8d16f8354c9e6@ec2-54-173-77-184.compute-1.amazonaws.com:5432/dbiq9077nq8qkg"
    LOAD = []
    NO_LOAD = ['rss', 'cleaner', 'connection', 'math']
    WEBHOOK = False
    INFOPIC = True
    URL = None
 

    #OPTIONAL
    AUTHORIZED_CHATS = ""
    ##List of id's -  (not usernames) for users which have sudo access to the bot.
    SUDO_USERS = get_user_list('elevated_users.json', 'sudos')
    ##List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = get_user_list('elevated_users.json', 'devs')
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    SUPPORT_USERS = get_user_list('elevated_users.json', 'supports')
    #List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGER_USERS = get_user_list('elevated_users.json', 'tigers')
    WHITELIST_USERS = get_user_list('elevated_users.json', 'whitelists')
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  #Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    WORKERS = 8  # Number of subthreads to use. Set as number of threads your processor uses
    BAN_STICKER = ''  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = 'awoo'  # Get your API key from https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = 'awoo'  # Get your API key from https://timezonedb.com/api
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None
    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
