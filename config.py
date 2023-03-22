import os

class Config(object):
    API_ID = int(os.environ.get("API_ID", ""))
    API_HASH = os.environ.get("API_HASH", "") 
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    SESSION_STRING = os.environ.get("SESSION_STRING", "") 
    AUTH_CHANNEL = int(os.environ.get("AUTH_CHANNEL", ""))
    OWNER_ID = int(os.environ.get("OWNER_ID", ""))
    DATABASE_URI = os.environ.get("DATABASE_URI", "")
    WELCOME_TEXT = os.environ.get("WELCOME_TEXT", "Hey {name}, your request to join {title} has been approved!")
