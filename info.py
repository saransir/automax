import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ['ADMINS'].split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ['CHANNELS'].split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]
FILTER_GROUPS = [int(admin) for admin in environ.get("FILTER_GROUPS", "").split()]
TUTORIAL = "https://t.me/joinchat/q4xMr02fvA9jNzQ1"
# MongoDB information
DATABASE_URI = environ['DATABASE_URI']
DATABASE_NAME = environ['DATABASE_NAME']
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', -1001529899497))

# Messages
default_start_msg = """
**Hi, I'm Media Search Bot or ypu can call me as Auto-Filter Bot**
Here you can search files in Inline mode as well as PM, Use the below buttons to search files or send me the name of file to search.
"""
START_MSG = environ.get('START_MSG', default_start_msg)
IMDB_TEMPLATE = "<b><a href={url}>{title}</a>🤺ɪᴍᴅʙ</b>\n\n <b>‌‌‌‌╔‎/yᴇᴀʀ: {year}\n ╠|ʀᴀᴛɪɴɢ‌‌‌‌‎: {rating}/10‌‌‌‌ \n ╚\ɢᴇɴʀᴇ: #{genres}</b> \n\n     <b>[𝚐𝚛𝚙 1](https://t.me/+PBGW_EV3ldY5YjJl)↮[𝚐𝚛𝚙 2](https://t.me/+eDjzTT2Ua6kwMTI1)</b>"
IMDB_TEMPLATEE = "🎬𝙽𝙰𝙼𝙴: {title} {year}\n 🤵‍♂️𝙳𝙸𝚁𝙴𝙲𝚃𝙾𝚁: #{director}\n 📝𝚆𝚁𝙸𝚃𝙴𝚁: #{writer}\n 👥ᴄᴀꜱᴛ: #{cast}"

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
