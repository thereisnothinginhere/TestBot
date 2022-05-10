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

    API_ID = 
    API_HASH = ""
    AUTHORIZED_CHATS = ""
    CERT_PATH = None
    TOKEN = ""
    OWNER_ID = 
    OWNER_USERNAME = ""
    PORT = 5000
    SUPPORT_CHAT = ""
    URL = None
    WEBHOOK = False
    WORKERS = 8  # Number of subthreads to use. Set as number of threads your processor uses
    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
