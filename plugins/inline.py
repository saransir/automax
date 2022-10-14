import logging
from pyrogram import Client, emoji, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument, InlineQueryResultArticle, InputTextMessageContent

from utils import get_search_results, is_subscribed, get_post
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME


@Client.on_inline_query(filters.user(AUTH_USERS) if AUTH_USERS else None)
async def answer(bot, query):
    """Show search results for given inline query"""

    if AUTH_CHANNEL and not await is_subscribed(bot, query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='join main group 🎪 then use 😉',
                           switch_pm_parameter="join")
        return

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    elif '<' in query.query:
        me, string = query.query.split('<', maxsplit=1)
        movie = string.strip()
        imdb = await get_post(movie)
        if imdb:
            imdbcap = f"**{movie}**\n\n **╔‎/yᴇᴀʀ: {imdb['year']}**\n **╠|ʀᴀᴛɪɴɢ‌‌‌‌‎: {imdb['rating']}/10‌‌‌‌** \n **╚\ɢᴇɴʀᴇ: #{imdb['genres']}**\n\n__ʀᴜɴᴛɪᴍᴇ: {imdb['runtime']}ᴍɪɴ__\n __ʟᴀɴɢᴜᴀɢᴇꜱ: #{imdb['languages']}__\n 💡__ʀᴇʟᴇᴀꜱᴇ ᴅᴀᴛᴇ: {imdb['release_date']}__"
        else:
            imdbcap = f" **{movie}**"
        try:
            results.append(
                InlineQueryResultArticle(
                    title=movie,
                    thumb_url=imdb['poster'],
                    description="click",
                    input_message_content=InputTextMessageContent(
                        message_text=imdbcap,
                        disable_web_page_preview=True
        except:
            pass
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    reply_markup = get_reply_markup(query=string)
    files, next_offset = await get_search_results(string,
                                                  file_type=file_type,
                                                  max_results=10,
                                                  offset=offset)

    for file in files:
        title=file.file_name
        size=file.file_size
        f_caption=file.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption="🍿{title}",
            except Exception as e:
                print(e)
                f_caption=f_caption
        if f_caption is None:
            f_caption = f"{file.file_name}"
        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                file_id=file.file_id,
                caption="<code>" + title + "</code>""\n\n  <b>ᴍᴏᴠɪᴇ/sᴇʀɪᴇs ʀᴇϙᴜᴇsᴛɪɴɢ \n [𝚐𝚛𝚘𝚞𝚙 1](https://t.me/+PBGW_EV3ldY5YjJl)  ↮  [𝚐𝚛𝚘𝚞𝚙 2](https://t.me/+eDjzTT2Ua6kwMTI1)</b>",
                description=f'💒 Size: {get_size(file.file_size)}\n🍿Type: {file.file_type}'))

    if results:
        switch_pm_text = f"𝚁𝙴𝚂𝚄𝙻𝚃𝚂"
        if string:
            switch_pm_text += f" for {string}"

        await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
        return
    else:
        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'

        await query.answer(results=[],
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")
        return

def get_reply_markup(query):
    buttons = [
        [
            InlineKeyboardButton('🔍 𝚂𝙴𝙰𝚁𝙲𝙷 ꜰɪʟᴇ 🔎', switch_inline_query_current_chat=query)
        ]
        ]
    return InlineKeyboardMarkup(buttons)


def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "ᴋʙ", "ᴍʙ", "ɢʙ", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])
