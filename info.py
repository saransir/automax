import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
SESSIO = "BQAY67damhL3DQAvY_HbCH8Is5GkfQ7pOOCCExyIxLrlHk33tr9xCbvfnrhN4rHZuO317UZuBo8oIV4Jx_yaRgy0N6Zfbiq5VE3ZDEgUR0o6GFpGMcN-JtG-mxRnbhkW-ew7jBE32VdcS4SIEfnfWEp-OAyYw07LiB9uVLwM-bs8oVmW6rnHW243AQgiapqCmctiz65HcU32zpEg0FfMuAqMnzW1iLBtpw_uTO3zl0uUyGAGsiu1o9073gzKDpVYV6JIJUzRvC1NGeKMnyQz4Ev8p3JR4a-TZn5kFP1fz8Q-PEWYzC2-U26qRL4FKsWck0xETkTfBQ4eNmji8gVjaCYgZgqOdgA"
# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ['ADMINS'].split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ['CHANNELS'].split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]
TUTORIAL = "https://t.me/joinchat/q4xMr02fvA9jNzQ1"
# MongoDB information
DATABASE_URI = environ['DATABASE_URI']
DATABASE_NAME = environ['DATABASE_NAME']
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Messages
default_start_msg = """
**Hi, I'm Media Search Bot or ypu can call me as Auto-Filter Bot**
Here you can search files in Inline mode as well as PM, Use the below buttons to search files or send me the name of file to search.
"""
START_MSG = environ.get('START_MSG', default_start_msg)
IMDB_TEMPLATE = "<b>🎬↳ ɴᴀᴍᴇ: <a href={url}>{title}</a>🤺ɪᴍᴅʙ</b>\n\n <b>‌‌‌‌╔‎/yᴇᴀʀ: {year}\n ╠|ʀᴀᴛɪɴɢ‌‌‌‌‎: {rating}/10‌‌‌‌ \n ╚\ɢᴇɴʀᴇ: #{genres}</b> \n\n     <b>[𝚐𝚛𝚙 1](https://t.me/+PBGW_EV3ldY5YjJl)↮[𝚐𝚛𝚙 2](https://t.me/+eDjzTT2Ua6kwMTI1)</b>"

FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "")
OMDB_API_KEY = environ.get("OMDB_API_KEY", "http://www.omdbapi.com/?i=tt3896198&apikey=4f08a979")
if FILE_CAPTION.strip() == "":
    CUSTOM_FILE_CAPTION=None
else:
    CUSTOM_FILE_CAPTION=FILE_CAPTION
if OMDB_API_KEY.strip() == "":
    API_KEY=None
else:
    API_KEY=OMDB_API_KEY
