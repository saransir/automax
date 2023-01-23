import logging
from pyrogram import Client, emoji, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
import re
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
    nd = []
    buttons = [[InlineKeyboardButton("ɢʀᴏᴜᴩ", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]
    nd.append(
        InlineQueryResultArticle(
            title="request on group 🎪",
            thumb_url="https://telegra.ph/file/d651c3858b99538bdb311.jpg",
            description="ask movie/series in group",
            input_message_content=InputTextMessageContent(
                message_text="**request on group**🎪 👇",
                disable_web_page_preview=True),
                reply_markup=InlineKeyboardMarkup(buttons)))
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    elif '++' in query.query:       
        me, string = query.query.split('++', maxsplit=1)
        vie = string.strip()
        if len(vie) <= 2:
            return
        movies = await get_post(vie, bulk=True)
        # imdbcap = f"**{movie}**\n\n**╔‎/yᴇᴀʀ: {imdb['year']}**\n**╠|ʀᴀᴛɪɴɢ‌‌‌‌‎: {imdb['rating']}/10‌‌‌‌**\n**╚\ɢᴇɴʀᴇ: #{imdb['genres']}**\n\n__ʀᴜɴᴛɪᴍᴇ: {imdb['runtime']}ᴍɪɴ__\n __ʟᴀɴɢᴜᴀɢᴇꜱ: #{imdb['languages']}__\n 💡__ʀᴇʟᴇᴀꜱᴇ ᴅᴀᴛᴇ: {imdb['release_date']}__\n\n**🍿ʙʏ⇛[𝙾ɴ𝙰ɪʀ_𝚏ɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)**"
        if not movies:
            await query.answer(results=[],
                               cache_time=0,
                               switch_pm_text='No imdb Results',
                               switch_pm_parameter="okay")
            return
        for movie in movies:
            titl = movie.get('title').strip()
            year = movie.get('year')
            title = f"{titl} {year}"
            mid = movie.movieID
            imdb = await get_post(mid, id=True)
            poster=None
            if imdb:
               imdbcap = f"**{titl}**\n\n**╔‎/yᴇᴀʀ: {year}**\n**╠|ʀᴀᴛɪɴɢ‌‌‌‌‎: {imdb['rating']}/10‌‌‌‌**\n**╚\ɢᴇɴʀᴇ: #{imdb['genres']}**\n\n__ʀᴜɴᴛɪᴍᴇ: {imdb['runtime']}ᴍɪɴ__\n __ʟᴀɴɢᴜᴀɢᴇꜱ: #{imdb['languages']}__\n💡__ʀᴇʟᴇᴀꜱᴇ ᴅᴀᴛᴇ: {imdb['release_date']}__\n\n **🍿ʙʏ⇛[𝙾ɴ𝙰ɪʀ_𝚏ɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)**"
               poster = imdb['poster']
               imdbdis = f"ʀᴀᴛɪɴɢ‌‌‌‌‎: {imdb['rating']}/10‌‌‌  ɢᴇɴʀᴇ: #{imdb['genres']} \n ʀᴜɴᴛɪᴍᴇ: {imdb['runtime']}ᴍɪɴ"
               buttons = [[InlineKeyboardButton("ɢʀᴏᴜᴩ 1", url="https://t.me/+PBGW_EV3ldY5YjJl"), InlineKeyboardButton("🎪 ɪɴꜰᴏ ", callback_data=f"imdb#{imdb['imdb_id']}"), InlineKeyboardButton("ɢʀᴏᴜᴩ 2", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]
               if not poster:
                   poster = "https://telegra.ph/file/9075ca7cbad944afaa823.jpg"
            else:
               imdbcap = f"**{titl} 🍿 {year}**"
               imdbdis = "None"
               buttons = [[InlineKeyboardButton("ɢʀᴏᴜᴩ 1", url="https://t.me/+PBGW_EV3ldY5YjJl"), InlineKeyboardButton("ɢʀᴏᴜᴩ 2", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]
               poster = "https://telegra.ph/file/9075ca7cbad944afaa823.jpg"
            results.append(
                InlineQueryResultPhoto(
                    photo_url=poster,
                    thumb_url=poster,
                    title=f"{titl} 🍿 {year}",
                    description=imdbdis,
                    caption=imdbcap,
                    reply_markup=InlineKeyboardMarkup(buttons)))
        try:
            await query.answer(results=results,
                           is_personal = True,                         
                           cache_time=0,
                           switch_pm_text='ʀᴇꜱᴜʟᴛꜱ 👇',
                           switch_pm_parameter="start")                         
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))
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
        at=file.file_name
        f_caption=file.caption
        if at == "None":
            at=f_caption[0:40]
        title=re.sub(r"(#|\@|\~|\©|\[|\]|\_|\.)", " ", at, flags=re.IGNORECASE)
        size=file.file_size        
        results.append(
            InlineQueryResultCachedDocument(
                title=title,
                file_id=file.file_id,
                caption=f"<u><b>#𝙵𝙸𝙻𝙴_𝙽𝙰𝙼𝙴⇛{title}</b></u>\n\n <b>🍿ʙʏ⇛[𝙾ɴ𝙰ɪʀ_𝚏ɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>\n\n<b>♡ ㅤ   ❍ㅤ     ⎙      ⌲\nˡᶦᵏᵉ  ᶜᵒᵐᵐᵉⁿᵗ   ˢᵃᵛᵉ   ˢʰᵃʳᵉ</b>",
                description=f'🍿 {file.file_type} Size: {get_size(file.file_size)}',
                reply_markup=reply_markup))
    if results:
        switch_pm_text = f"results"
        if string:
            switch_pm_text += f" for {string}"
        try:
            await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))
    else:
        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'
        try:
            await query.answer(results=nd,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))

def get_reply_markup(query):
    buttons = [[InlineKeyboardButton("ɢʀᴏᴜᴩ 1", url="https://t.me/+PBGW_EV3ldY5YjJl"), InlineKeyboardButton("ɢʀᴏᴜᴩ 2", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]
    """buttons += [
        [
            InlineKeyboardButton('🔍 𝚂𝙴𝙰𝚁𝙲𝙷 ꜰɪʟᴇ 🔎', switch_inline_query_current_chat=query)
        ]
        ]"""
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
