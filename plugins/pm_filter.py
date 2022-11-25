#on airmovie
from pyrogram.errors import UserNotParticipant, UserIsBlocked, FloodWait 
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, ADMINS, START_MSG
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram import Client, filters
import re
import random
import asyncio
from info import IMDB_TEMPLATE
from utils import get_filter_results, get_file_details, is_subscribed, get_poster, get_post, search_gagala, find_filter
BUTTONS = {}
BOT = {}
SPELL_CHECK = {}
CHAA = "-1001534114432"
RAT = ["🦋", "🌸", "🦄", "🎈", "🥀", "🌻", "🍭", "🍿", "🪁", "🗼", "🪗", "🎬", "🪘", "🗽",]

PHOTO = [
    "https://telegra.ph/file/9075ca7cbad944afaa823.jpg",
    "https://telegra.ph/file/9688c892ad2f2cf5c3f68.jpg",
    "https://telegra.ph/file/51683050f583af4c81013.jpg",
]

@Client.on_callback_query(filters.regex(r"^spo"))
async def advantage_spoll_choker(bot, query):
    _, s, user, movie_ = query.data.split('#')
    message = query.message.reply_to_message
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("Don't click others Requested files🎬", show_alert=True)
    if movie_  == "close_spellcheck":
        await message.delete()
        return await query.message.delete()
    btn = []
    oam = f"{random.choice(RAT)}"
    if s  == "sa":
        movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
        if not movies:
            await query.answer("You are clicking on an old button which is expired.", show_alert=True)
            return await query.message.delete()
        ttte = movies[(int(movie_))]
        mov = re.sub(r"(\:|\-|\_|\,|\;|\?|IMDb|Streaming|Online|Netflix|Episode|Season|movies|Movies)", " ", ttte, flags=re.IGNORECASE)
        movie = mov.replace("  ", " ").strip()
        imdb = await get_post(movie)
        if len(movie) > 30:
            await query.message.edit_text(f"𝑻𝒉𝒊𝒔 𝑴𝒐𝒗𝒊𝒆 𝑵𝒐𝒕 𝑭𝒐𝒖𝒏𝒅 𝑰𝒏 𝑫𝒂𝒕𝒂𝑩𝒂𝒔𝒆💾 \n <spoiler>sᴇᴀʀᴄʜ ɪɴ ɢᴏᴏɢʟᴇ ғᴏʀ ᴄᴏʀʀᴇᴄᴛ sᴘᴇʟʟɪɴɢ</spoiler>")
            await asyncio.sleep(10)
            await query.message.delete()
            return await message.delete()       
        x = mov.split()
        sesna = "_".join(x)
        btn.append(
            [InlineKeyboardButton(text="🕵️ 𝙿𝙼",callback_data=f"myree#{sesna}")]
            )
        files = await get_filter_results(movie)
    a1 = await query.message.edit_text(f"{oam} ᴄʜᴇᴄᴋɪɴɢ... {oam}")
    if s  == "se":
        movi = movie_
        imdb = await get_post(query=movi, id=True)
        ttt = imdb.get('title')[0:29]
        movx = re.sub(r"(\:|\-|\,|\_|\.|\#|\;|IMDb|None|Streaming|Online|Netflix|'s|Episode|Season|Movie|movie|movies|Movies)", " ", ttt, flags=re.IGNORECASE).strip()
        mov = movx.replace("  ", " ")
        yea = imdb.get('year')
        movie = f"{mov} {yea}"
        x = mov.split()
        sesna = "_".join(x) # list(set(test_list))
        if yea:
            files = await get_filter_results(movie)
            if files:
                # files += await get_filter_results(mov)
                fies = await get_filter_results(mov)
                files.append(fies.group(1))
                files = list(dict.fromkeys(files)) 
            else:
                files = await get_filter_results(mov)
        else:
            files = await get_filter_results(mov)
        btn.append(
            [InlineKeyboardButton(text="🎪 ɪɴꜰᴏ ",callback_data=f"imdb#tt{movi}"),InlineKeyboardButton(text="🕵️ 𝙿𝙼",callback_data=f"myree#{sesna}")]
            )

    hari = "+".join(x)
    kuttons = []
    if imdb:
        imdbcap = f"**{movie}**\n\n **╔‎/yᴇᴀʀ: {imdb['year']}**\n **╠|ʀᴀᴛɪɴɢ‌‌‌‌‎: {imdb['rating']}/10‌‌‌‌** \n **╚\ɢᴇɴʀᴇ: #{imdb['genres']}**\n\n__ʀᴜɴᴛɪᴍᴇ: {imdb['runtime']}ᴍɪɴ__\n __ʟᴀɴɢᴜᴀɢᴇꜱ: #{imdb['languages']}__\n 💡__ʀᴇʟᴇᴀꜱᴇ ᴅᴀᴛᴇ: {imdb['release_date']}__"
    else:
        imdbcap = f" **{movie}**"     
    cha = int(CHAA)
    if files:
        chat_type = query.message.chat.type
        N = int(23)
        if chat_type == "private":
            N = int(31)
            btn = []
        for file in files:
            file_id = file.file_id
            sz = get_size(file.file_size)
            tt = str(file.file_name[0:35].title().lstrip())
            dcode = re.sub(r"(_|\-|\.|\´|\`|\,|\#|\@|\+)", " ", tt, flags=re.IGNORECASE)
            filename = f"{dcode[0:N]}{oam}{sz[0:3]} {sz[-2:]}{oam}"
            btn.append(
                [InlineKeyboardButton(text=f"{filename}",callback_data=f"saran#{file_id}")]
                )
    else:
        reply_text = await find_filter(mov)
        if reply_text:
            kuttons.append(
                [InlineKeyboardButton(text=f"{oam} 𝙾𝚃𝚃/𝙷𝙳 {oam}", callback_data="ott")]
            )
            if imdb:
                kuttons.append(
                    [InlineKeyboardButton(text=f"{oam} ɪɴꜰᴏ ",callback_data=f"imdb#tt{movi}"), InlineKeyboardButton(text=f"ᴄʟᴏꜱᴇ {oam}",callback_data="close")]
                )
            await a1.edit_text(f"{imdbcap}\n\n <b>❗️<u>{reply_text}</u>❗️</b> \n", reply_markup=InlineKeyboardMarkup(kuttons))
            return
        else:
            kuttons.append(
                [InlineKeyboardButton(text=f"ɢᴏᴏɢʟᴇ 🍿", url=f"https://google.com/search?q={hari}"),InlineKeyboardButton(text=f"ɪᴍᴅʙ 🍿", url=f"https://www.imdb.com/find?q={hari}")]
            )
            chat_type = query.message.chat.type
            if chat_type == "private":
                kuttons.append([InlineKeyboardButton(text="💒 ʀᴇϙᴜᴇsᴛ ᴏɴ ɢʀᴏᴜᴘ 💒",url="https://t.me/+eDjzTT2Ua6kwMTI1")])
            else:
                # await bot.send_message(chat_id=cha,text=f"{movie}", disable_web_page_preview=True)
                kuttons.append(
                    [InlineKeyboardButton(text="ʀᴇᴩᴏʀᴛ ᴛᴏ ᴀᴅᴍɪɴ",callback_data=f"report_{hari}")]
                )
            reply_markup = InlineKeyboardMarkup(kuttons)
            if not message.from_user:
                return await a1.delete()
            a = await a1.edit_text(f"{imdbcap}\n\n <i>𝑻𝒉𝒊𝒔 𝑴𝒐𝒗𝒊𝒆 𝑵𝒐𝒕 𝑭𝒐𝒖𝒏𝒅 𝑰𝒏 𝑫𝒂𝒕𝒂𝑩𝒂𝒔𝒆💾</i>\n\n ᴘᴏssɪʙʟᴇ ᴄᴀᴜsᴇs : 👇\n\n🔺<b>ɴᴏᴛ ʀᴇʟᴇᴀsᴇᴅ ʏᴇᴛ </b>\n🔺 ɴᴏᴛ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ \n\n 𝙲𝚕𝚒𝚌𝚔 & 𝙲𝚑𝚎𝚌𝚔 𝚝𝚑𝚎 𝚜𝚙𝚎𝚕𝚕𝚒𝚗𝚐 👇", reply_markup=reply_markup)
            await asyncio.sleep(35)
            await a.delete()
            await message.delete()
            return 
    if not btn:
        a = await a1.edit_text(f"{message.from_user.mention}, <spoiler>𝑻𝒉𝒊𝒔 𝑴𝒐𝒗𝒊𝒆 𝑵𝒐𝒕 𝑭𝒐𝒖𝒏𝒅 𝑰𝒏 𝑫𝒂𝒕𝒂𝑩𝒂𝒔𝒆💾</spoiler>")
        await asyncio.sleep(5)
        await a.delete()
        await message.delete()
        return
    if not message.message_id:
        return await a1.delete()
    if len(btn) > 6: 
        btns = list(split_list(btn, 6)) 
        keyword = f"{message.chat.id}-{message.message_id}"
        BUTTONS[keyword] = {
            "total" : len(btns),
            "buttons" : btns
        }
    else:
        buttons = btn
        buttons.append(
            [InlineKeyboardButton(" 💒💒  ᴄʜᴀɴɴᴇʟ 💒💒 ", url="https://t.me/+R9zxAI4mCkk0NzVl")]
        )
        await a1.edit_text(f"<b>{imdbcap} ‌‌‌‌‎</b> \n\n<b>{oam}ꜰᴏʀ-{message.from_user.mention} \n⚡️ʙʏ:[𝙾ɴ𝙰ɪʀ_𝚏ɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(buttons))
        return
    data = BUTTONS[keyword]
    buttons = data['buttons'][0].copy()
    buttons.append(
        [InlineKeyboardButton(text=f"🎪 Pages 1/{data['total']}🎪",callback_data="pages"),InlineKeyboardButton(text="⇏ɴᴇxᴛ⇏",callback_data=f"next_0_{keyword}")]
    )
    await a1.edit_text(f"<b>{imdbcap} ‌‌‌‌‎</b> \n\n<b>{oam}ꜰᴏʀ-{message.from_user.mention} \n⚡️ʙʏ:[𝙾ɴ𝙰ɪʀ_𝚏ɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(buttons))
        
@Client.on_message(filters.text & ~filters.edited & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & ~filters.edited & filters.incoming)
async def group(client, message):
    if re.findall("((^/|^!|^@|^#|^[\U0001F600-\U000E007F]).*)", message.text):
        if not ((message.from_user.id == "None") or (message.from_user.id in ADMINS)):
            await message.delete()
        return 
    if len(message.text) <= 2:
        kk = await message.reply_text(f"{message.from_user.mention},ɪɴᴄʟᴜᴅᴇ ʏᴇᴀʀ ᴏғ ᴛʜᴇ ᴍᴏᴠɪᴇ. \n\n 𝚜𝚎𝚗𝚝👉 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ & yᴇᴀʀ")
        await asyncio.sleep(10)
        await kk.delete()
        await message.delete()
    elif 2 < len(message.text) <= 3:
        return await spell(message)
    elif 3 < len(message.text) < 40:    
        btn = []
        search = []
        search = message.text.strip()
        x = search.split()
        hari = "+".join(x)
        sesna = "_".join(x)
        files = await get_filter_results(query=search)
        if files:
            oam = f"{random.choice(RAT)}"
            oamm = f"{random.choice(RAT)}"
            imdb = await get_post(search)
            if imdb:
                btn.append(
                    [InlineKeyboardButton(text="🎪 ɪɴꜰᴏ ",callback_data=f"imdb#{imdb['imdb_id']}"),InlineKeyboardButton(text="🕵️ 𝙿𝙼",callback_data=f"myree#{sesna}")]
                )
                caption = f"**{search}**\n\n **╔‎/yᴇᴀʀ: {imdb['year']}**\n **╠|ʀᴀᴛɪɴɢ‌‌‌‌‎: {imdb['rating']}/10‌‌‌‌**\n **╚\ɢᴇɴʀᴇ: #{imdb['genres']}**\n\n__ʀᴜɴᴛɪᴍᴇ: {imdb['runtime']}ᴍɪɴ__\n__ʟᴀɴɢᴜᴀɢᴇꜱ: #{imdb['languages']}__ \n\n      **‌‌‌‌[𝚐𝚛𝚙 1](https://t.me/+PBGW_EV3ldY5YjJl)↮[𝚐𝚛𝚙 2](https://t.me/+eDjzTT2Ua6kwMTI1)**"
            else:
                caption = f"<b>{search}‌‌‌‌‎</b>\n\n<b>{oam}ꜰᴏʀ-{message.from_user.mention} \n{oamm}ʙʏ:[𝙾ɴ𝙰ɪʀ_𝚏ɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>"         
            for file in files:
                file_id = file.file_id
                sz = get_size(file.file_size)
                tt = file.file_name[0:26].title().lstrip()
                fn = re.sub(r"(_|\-|\.|\#|\@|\+)", " ", tt, flags=re.IGNORECASE)
                dcode = fn[0:23]
                filename = f"{dcode} {oam}{sz[0:3]} {sz[-2:]}{oamm}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"saran#{file_id}")]
                )
        else:
            return await spell(message)
        if not btn:
            return await spell(message)
        if len(btn) > 6: 
            btns = list(split_list(btn, 6)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(" 💒💒  ᴄʜᴀɴɴᴇʟ 💒💒 ", url="https://t.me/+R9zxAI4mCkk0NzVl")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                try:
                    await message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
                except:
                    await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text=f"🎪 Pages 1/{data['total']}🎪",callback_data="pages"),InlineKeyboardButton(text="⇏ɴᴇxᴛ⇏",callback_data=f"next_0_{keyword}")]
        )
        
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            try:
                await message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
            except:
                await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=caption, reply_markup=InlineKeyboardMarkup(buttons))

    else:
        await message.delete()

def get_size(size):
    
    units = ["Bytes", "ᴋʙ", "ᴍʙ", "ɢʙ", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          
        n += 1

async def spell(message):
    titl = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|malayalam|English|english|Malayalam|Hindi|hindi|Telugu|telugu|1080p|720p|HEVC|Esub|Kannada|kannada|tamil|Tamil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|with\ssubtitle(s)?)", "", message.text, flags=re.IGNORECASE).strip() # plis contribute some common words 
    title = titl.strip()
    if len(title) <= 2:
        ki = await message.reply("** I couldn't find any movie in that name**\n\n__ɪɴᴄʟᴜᴅᴇ ʏᴇᴀʀ ᴏғ ᴛʜᴇ ᴍᴏᴠɪᴇ__")
        await asyncio.sleep(7)
        await ki.delete()
        await message.delete()
        return
    fn = titl.replace(" ", "_")[0:30]
    btn = []
    user = message.from_user.id if message.from_user else 0
    try:
        movies = await get_post(titl, bulk=True)
    except:
        return await advantage_spell_chok(message)
    if not movies:
        return await advantage_spell_chok(message)
    oam = f"{random.choice(RAT)}"
    for movie in movies:
        title = movie.get('title')[:27]
        year = movie.get('year')
        if not year:
            year = oam
        btn.append(
            [InlineKeyboardButton(text=f"{oam} {title} {year}",callback_data=f"spo#se#{user}#{movie.movieID}")]
        )
    if len(btn) > 10: 
        btn = btn[:10]
    chat_type = message.chat.type
    if chat_type == "private":
       btn.append([InlineKeyboardButton(text="💒 ʀᴇϙᴜᴇsᴛ ᴏɴ ɢʀᴏᴜᴘ 💒",url="https://t.me/+eDjzTT2Ua6kwMTI1")])
    else:
       btn.append([InlineKeyboardButton(text=f"{oam} ᴄʟᴏꜱᴇ", callback_data=f"close"), InlineKeyboardButton(text=f"{oam} ᴩᴍ ",callback_data="myree#")])
    await message.reply("__𝐃𝐢𝐝 𝐲𝐨𝐮 𝐦𝐞𝐚𝐧 𝐚𝐧𝐲 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐬𝐞__?👇", quote=True, reply_markup=InlineKeyboardMarkup(btn))

async def advantage_spell_chok(message):
    query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)", "", message.text, flags=re.IGNORECASE).strip()
    if len(query) <= 3:
        ko = await message.reply("**ɪɴᴄʟᴜᴅᴇ ʏᴇᴀʀ ᴏғ ᴛʜᴇ ᴍᴏᴠɪᴇ. \n\n 𝚜𝚎𝚗𝚝👉 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ & yᴇᴀʀ**")
        await asyncio.sleep(5)
        await ko.delete()
        await message.delete()
        return
    fn = query.replace(" ", "_")[0:30]
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(message.text)
    files = await get_filter_results(query)
    if files:
        g_s += f"query" 
    gs_parsed = []
    x = fn.split()
    hari = "+".join(x)
    kuttons = []
    kuttons.append(
        [InlineKeyboardButton(text=f"ɢᴏᴏɢʟᴇ 🍿", url=f"https://google.com/search?q={hari}"),InlineKeyboardButton(text=f"ɪᴍᴅʙ 🍿", url=f"https://www.imdb.com/find?q={hari}")]
    )
    chat_type = message.chat.type
    if chat_type == "private":
        kuttons.append([InlineKeyboardButton(text="💒 ʀᴇϙᴜᴇsᴛ ᴏɴ ɢʀᴏᴜᴘ 💒",url="https://t.me/+eDjzTT2Ua6kwMTI1")])
    else:
        kuttons.append(
            [InlineKeyboardButton(text="✉️ ʀᴇᴩᴏʀᴛ ᴛᴏ ᴀᴅᴍɪɴ ✉️",callback_data=f"report_{hari}")]
        )
    reply_arkup = InlineKeyboardMarkup(kuttons)
    if not g_s:
        k = await message.reply("**I couldn't find any movie in that name** \n\n**𝙲𝚕𝚒𝚌𝚔 & 𝙲𝚑𝚎𝚌𝚔 𝚝𝚑𝚎 𝚜𝚙𝚎𝚕𝚕𝚒𝚗𝚐** 👇", reply_markup=reply_arkup)
        await asyncio.sleep(38)
        await k.delete()
        await message.delete()
        return
    # regex = re.compile(r".*(imdbb|wikipedia).*", re.IGNORECASE) # look for imdb / wiki results
    # gs = list(filter(regex.match, g_s))
    # gs_parsed = [re.sub(r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)', '', i, flags=re.IGNORECASE) for i in g_s]
    # if not gs_parsed:
    if g_s:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*", re.IGNORECASE) # match something like Watch Niram | Amazon Prime 
        for mv in g_s:
            match  = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = message.from_user.id if message.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed)) # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_post(mov.strip(), bulk=True) # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist)) # removing duplicates
    if not movielist:
        k = await message.reply("__I couldn't find anything related to that. Check your__ **spelling**\n\n__𝙲𝚕𝚒𝚌𝚔 & 𝙲𝚑𝚎𝚌𝚔 𝚝𝚑𝚎__ **𝚜𝚙𝚎𝚕𝚕𝚒𝚗𝚐** 👇", reply_markup=reply_arkup)
        await asyncio.sleep(40)
        await k.delete()
        await message.delete()
        return
    SPELL_CHECK[message.message_id] = movielist
    btn = [[
                InlineKeyboardButton(
                    text=f"{random.choice(RAT)} {movie.strip()}",
                    callback_data=f"spo#sa#{user}#{k}",
                )
            ] for k, movie in enumerate(movielist)]
    if len(btn) > 9: 
        btn = btn[:9]
    btn.append([InlineKeyboardButton(text="🄲🄻🄾🅂🄴", callback_data="close"), InlineKeyboardButton(text=f"🄶🄾🄾🄶🄻🄴", url=f"https://google.com/search?q={hari}")])
    await message.reply("__𝐃𝐢𝐝 𝐲𝐨𝐮 𝐦𝐞𝐚𝐧 𝐚𝐧𝐲 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐬𝐞__ ?👇👇", quote=True, reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    message = query.message.reply_to_message
    try:
        typed = query.message.reply_to_message.from_user.id
    except:  
        typed = query.from_user.id
        pass
    if query.data.startswith("saran"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            if not filedetails:
                return await query.answer("No such file exist.",show_alert=True)
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"http://t.me/On_air_Filter_bot?start=seren_-_-_-_{file_id}")
                return
            chat_type = query.message.chat.type
            if chat_type == "private":
                await query.answer(url=f"http://t.me/On_air_Filter_bot?start=seren_-_-_-_{file_id}")
                return
            if clicked == typed or clicked in ADMINS:
                for files in filedetails:
                    at = files.file_name[0:-4]
                    title = re.sub(r"(#|\@|\~|\©|\[|\]|\_|\.)", " ", at, flags=re.IGNORECASE)
                    size=files.file_size
                    # f_caption=files.caption  
                    buttons = [[InlineKeyboardButton("ɢʀᴏᴜᴩ 1", url="https://t.me/+PBGW_EV3ldY5YjJl"), InlineKeyboardButton("ɢʀᴏᴜᴩ 2", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]
                try:  
                    await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f"<b>#𝙵𝙸𝙻𝙴_𝙽𝙰𝙼𝙴⇛<u>{title}</u></b>\n\n <b>ʙʏ⇛[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                except UserIsBlocked:
                    await query.answer(url=f"http://t.me/On_air_Filter_bot?start=seren_-_-_-_{file_id}")
                except FloodWait as e:
                    await asyncio.sleep(1)
                else:
                    await query.answer(f"file🎬 has 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 ✔️ sent to your pm \n\n🎬𝙵𝙸𝙻𝙴 𝙽𝙰𝙼𝙴⇛ ~~{title}~~",show_alert=True)        
            else:
                await query.answer(url=f"http://t.me/On_air_Filter_bot?start=seren_-_-_-_{file_id}")
    
    if not ((clicked == typed) or (clicked in ADMINS)):
        return await query.answer(f"🖐️ {query.from_user.first_name} search your own file,\n\n this is >> {query.message.reply_to_message.from_user.first_name} << Requested files🎬",show_alert=True)
    else:    
        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer(" You are using this for one of my old message, please send the request again ",show_alert=True)
                return
            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ⇍", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"🎪 {int(index)+2}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton(text="🕯️ᴄʟᴏꜱᴇ", callback_data="close")]
                )
                """buttons.append(
                    [InlineKeyboardButton(text="🍿𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼🍿",callback_data=f"myree#")]
                )"""

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ⇍", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"🎪{int(index)+2}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton(f"🎪 Pages {int(index)}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{int(index)-1}_{keyword}")]                   
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ⇍", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton(f"🎪{int(index)}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{int(index)-1}_{keyword}")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data.startswith("start"):
            buttons = [
                [
                    InlineKeyboardButton(text="ᴀʙᴏᴜᴛ 💡",callback_data="about"),
                    InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ 🍿", url="https://t.me/+R9zxAI4mCkk0NzVl")   
                ],
                [
                    InlineKeyboardButton("ɢʀᴏᴜᴩ 1 🎪", url="https://t.me/+PBGW_EV3ldY5YjJl"),
                    InlineKeyboardButton("ɢʀᴏᴜᴩ 2 🎪", url="https://t.me/+eDjzTT2Ua6kwMTI1")   
                ]
                ]
                
            a = await query.message.reply_text(
            START_MSG.format(query.from_user.first_name),
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons))
            await query.message.delete()
        elif query.data.startswith("myree"):
            ident, file_name = query.data.split("#")
            await query.answer(url=f"http://t.me/On_air_Filter_bot?start=saran=={file_name}")   
        elif query.data.startswith("report"):
            ident, movie = query.data.split("_")
            x = movie.split("+")
            kdm = " ".join(x)
            cha = int(CHAA)
            try:
                await client.send_message(chat_id=cha,text=f"{kdm}", disable_web_page_preview=True)
            except UserIsBlocked:
                await query.answer(url=f"http://t.me/On_air_Filter_bot?start=saran")
            else:
                await query.answer("𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 Reported to Admins 👮‍♂ \n\n\n ᴛʜᴇ ᴍᴏᴠɪᴇ ᴡɪʟʟ ᴜᴩʟᴏᴀᴅɪɴɢ ꜱᴏᴏɴ..",show_alert=True)
                await message.delete()
                return await query.message.delete()
        elif query.data == "ott":
            buttons = []
            buttons.append(
                [InlineKeyboardButton(" 💒💒  ᴄʜᴀɴɴᴇʟ 💒💒 ", url="https://t.me/+R9zxAI4mCkk0NzVl")]
            )
            await query.edit_message_reply_markup( 
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            await asyncio.sleep(.3)
            await query.answer("Once this movie is releas HDRip/OTT, it will be upload on the👇 💒channel \n\n\n ഈ സിനിമയുടെ HD/OTT ഇറങ്ങിയാൽ ഉടൻ ചുവടെ ഉള്ള 💒ചാനലിൽ അപ്‌ലോഡ് ചെയ്യുന്നതാണ്",show_alert=True)
            return
        elif query.data == "about":
            await query.answer("🤖 ɴᴀᴍᴇ: ғɪʟᴛᴇʀ -x- v2.8\n\n🎪ᴄʀᴇᴀᴛᴏʀ: sᴀʀᴀɴ😁\n\n📚ʟᴀɴɢᴜᴀɢᴇ: ᴘʏᴛʜᴏɴ3\n\n🌀 ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄɪᴏ 1.13.0",show_alert=True)
        elif query.data == "close":
            await query.answer("your query message is deleted 🌩️",show_alert=True)
            await query.message.delete()
            try:
                await message.delete()
            except:
                return
                
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("🎪ഗ്രൂപ്പിൽ join ചെയ്തതിനു ശേഷം ക്ലിക്ക് ചെയ്യൂ \n\n Join My 🎪 group 🎪 to click",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption="{title}",
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('💒 ɢʀᴏᴜᴘ 💒', url='https://t.me/+PBGW_EV3ldY5YjJl')
                    ]
                    ]
                
                await query.answer("Thanks for joining the group",show_alert=True)
                await query.message.delete()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f"<b>©[ᵒⁿᵃⁱʳᵐᵒᵛⁱᵉˢ](https://t.me/+R9zxAI4mCkk0NzVl) \n 🎬 file name 👉  </b>""<code>" + title + "</code>""\n\n[𝙼𝚘𝚟𝚒𝚎 ʀᴇϙᴜᴇsᴛɪɴɢ 𝚐𝚛𝚘𝚞𝚙](https://t.me/+eDjzTT2Ua6kwMTI1)",
                    reply_markup=InlineKeyboardMarkup(buttons)) 
        elif query.data == "pages":
            await query.answer("ɪꜰ ❌️ꜱᴇᴇ ᴛʜᴇ ꜰɪʟᴇ, ʟᴏᴏᴋ ᴀᴛ ɴᴇxᴛ ᴘᴀɢᴇ")

