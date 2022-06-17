#on air movies program
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, ADMINS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
import random
import asyncio
from info import IMDB_TEMPLATE
from pyrogram.errors import UserNotParticipant, UserIsBlocked
from utils import get_filter_results, get_file_details, is_subscribed, get_poster, get_post, search_gagala
BUTTONS = {}
BOT = {}
SPELL_CHECK = {}
CHAA = "-1001534114432"
RAT = ["🦋", "🫐", "🎡", "🎈", "🥀", "🌻", "🍭", "🍿", "🪁", "🗼",]

PHOTO = [
    "https://telegra.ph/file/9075ca7cbad944afaa823.jpg",
    "https://telegra.ph/file/9688c892ad2f2cf5c3f68.jpg",
    "https://telegra.ph/file/51683050f583af4c81013.jpg",
]

@Client.on_callback_query(filters.regex(r"^spo"))
async def advantage_spoll_choker(bot, query):
    _, s, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("Don't click others Requested files🎬", show_alert=True)
    message = query.message.reply_to_message
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
        movie = movies[(int(movie_))]
        files = await get_filter_results(movie)
    if s  == "se":
        movi = movie_[2:]
        imdb = await get_post(query=movi, id=True)
        tt = imdb.get('title')
        mov = tt.replace(":", "")
        year = imdb.get('year') if movie.get else "None"
        movie = f"{mov} {year}"
        btn.append(
            [InlineKeyboardButton(text="🎪 ɪɴꜰᴏ ",callback_data=f"imdb#tt{movi}")]
            )
        fils = await get_filter_results(movie)
        if fils:
            for file in fils:
                file_id = file.file_id
                sz = get_size(file.file_size)
                fn = file.file_name[0:22]
                filename = f"{fn}{oam}{sz[0:3]} {sz[-2:]}{oam}"  
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"saran#{file_id}")]
                    )
        files = await get_filter_results(mov)
    x = movie.split()
    hari = "+".join(x)
    sesna = "_".join(x)
    a1 = await query.message.edit_text(f"🕵‍♂ᴄʜᴇᴄᴋɪɴɢ..🎬‎**#{sesna}**")
    btn.append(
        [InlineKeyboardButton(text="🕵️𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼",callback_data=f"myree#{sesna}")]
        )
    if files:
        for file in files:
            file_id = file.file_id
            sz = get_size(file.file_size)
            fn = file.file_name[0:22]
            filename = f"{fn}{oam}{sz[0:3]} {sz[-2:]}{oam}"  
            btn.append(
                [InlineKeyboardButton(text=f"{filename}",callback_data=f"saran#{file_id}")]
                )
    else:
        cha = int(CHAA)
        buttons = []
        buttons.append(
            [InlineKeyboardButton(text=f"ɢᴏᴏɢʟᴇ 🍿", url=f"https://google.com/search?q={hari}"),InlineKeyboardButton(text=f"ɪᴍᴅʙ 🍿", url=f"https://www.imdb.com/find?q={hari}")]
        )
        buttons.append(
            [InlineKeyboardButton(text="ʀᴇᴩᴏʀᴛ ᴛᴏ ᴀᴅᴍɪɴ 🤵",callback_data=f"report_{hari}")]
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await bot.send_message(chat_id=cha,text=f"{movie}", disable_web_page_preview=True)
        a = await a1.edit_text(f"{message.from_user.mention}, <spoiler>𝑻𝒉𝒊𝒔 𝑴𝒐𝒗𝒊𝒆 𝑵𝒐𝒕 𝑭𝒐𝒖𝒏𝒅 𝑰𝒏 𝑫𝒂𝒕𝒂𝑩𝒂𝒔𝒆💾</spoiler>\n ᴘᴏssɪʙʟᴇ ᴄᴀᴜsᴇs : 👇\n\n🔺 <b>ɴᴏᴛ ʀᴇʟᴇᴀsᴇᴅ ʏᴇᴛ </b> \n🔺 ɴᴏᴛ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ ꜱᴏ ʀᴇᴩᴏʀᴛ ᴛᴏ ᴀᴅᴍɪɴ👇\n\n 𝙲𝚕𝚒𝚌𝚔 & 𝙲𝚑𝚎𝚌𝚔 𝚝𝚑𝚎 𝚜𝚙𝚎𝚕𝚕𝚒𝚗𝚐 👇", reply_markup=reply_markup, parse_mode="html")
        await asyncio.sleep(25)
        await a.delete()
        await message.delete()
        return 
    if not btn:
        return

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
            [InlineKeyboardButton("💡close💡", callback_data="close")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(movie)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {movie} ‌‌‌‌‎</b> \n\n <b>🌀ꜰᴏʀ- {message.from_user.mention} \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))

        else:
            await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {movie} ‌‌‌‌‎</b> \n\n <b>🌀ꜰᴏʀ- {message.from_user.mention} \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
        return await query.message.delete()

    data = BUTTONS[keyword]
    buttons = data['buttons'][0].copy()

    buttons.append(
        [InlineKeyboardButton(text=f"🎪 Pages 1/{data['total']}🎪",callback_data="pages"),InlineKeyboardButton(text="⇏ɴᴇxᴛ⇏",callback_data=f"next_0_{keyword}")]
    )
    poster=None
    if API_KEY:
        poster=await get_poster(movie)
    if poster:
        await message.reply_photo(photo=poster, caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {movie} ‌‌‌‌‎</b> \n\n <b>🌀ꜰᴏʀ- {message.from_user.mention} \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
        await query.message.delete()
    else:
        await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {movie} ‌‌‌‌‎</b> \n\n <b>🌀ꜰᴏʀ- {message.from_user.mention} \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
        await query.message.delete()

async def filter(client, msg, files):
        btn = []
        search = msg
        message = msg.message.reply_to_message  
        # files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"{random.choice(RAT)}[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"saran#{file_id}")]
                    )
        else:
            k = await query.message.edit('This Movie Not Found In DataBase')
            await asyncio.sleep(10)
            await k.delete()
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton("🎪 channel 🎪", url="https://t.me/joinchat/4-Quex2FaFhjMDM1")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n  <b>🌀 ᴄʜᴀɴɴᴇʟ : [ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n <b>🌀 ᴄʜᴀɴɴᴇʟ : [ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="⇏ɴᴇxᴛ⇏",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🎪 Pages 1/{data['total']}🎪",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(movie)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n <b>🌀 ᴄʜᴀɴɴᴇʟ :[ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n <b>🌀 ᴄʜᴀɴɴᴇʟ :[ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & ~filters.edited & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & ~filters.edited & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^@|^#|^Vikram|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if len(message.text) <= 2:
        kk = await message.reply_text(f"{message.from_user.mention},ɪɴᴄʟᴜᴅᴇ ʏᴇᴀʀ ᴏғ ᴛʜᴇ ᴍᴏᴠɪᴇ. \n\n 𝚜𝚎𝚗𝚝👉 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ & yᴇᴀʀ")
        await asyncio.sleep(10)
        await kk.delete()
        await message.delete()
    elif 2 < len(message.text) <= 6:
        return await spell(message)
    elif 6 < len(message.text) < 45:    
        btn = []
        searc = message.text
        search = searc.strip()
        x = search.split()
        hari = "+".join(x)
        sesna = "_".join(x)
        imdb = await get_post(search)
        if imdb:
            btn.append(
                [InlineKeyboardButton(text="🎪 ɪɴꜰᴏ ",callback_data=f"imdb#{imdb['imdb_id']}"),InlineKeyboardButton(text="🕵️ 𝙿𝙼",callback_data=f"myree#{sesna}")]
            )
            caption = IMDB_TEMPLATE.format(
                query = imdb['title'],
                title = imdb['title'],
                votes = imdb['votes'],
                aka = imdb["aka"],
                seasons = imdb["seasons"],
                box_office = imdb['box_office'],
                localized_title = imdb['localized_title'],
                kind = imdb['kind'],
                imdb_id = imdb["imdb_id"],
                cast = imdb["cast"],
                runtime = imdb["runtime"],
                countries = imdb["countries"],
                certificates = imdb["certificates"],
                languages = imdb["languages"],
                release_date = imdb['release_date'],
                year = imdb['year'],
                genres = imdb['genres'],
                poster = imdb['poster'],
                rating = imdb['rating'],
                url = imdb['url'],
                **locals()
            )
        else:
            caption = f"**<b>🎬↳ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : ‌‌‌‌‎</b>** ‌‌‌‌‎<b>{search}‌‌‌‌‎</b>\n**‌‌‌‌╚\[𝚐𝚛𝚙 1](https://t.me/+PBGW_EV3ldY5YjJl)↮[𝚐𝚛𝚙 2](https://t.me/+eDjzTT2Ua6kwMTI1)**"
        oam = f"{random.choice(RAT)}"
        oamm = f"{random.choice(RAT)}"
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                sz = get_size(file.file_size)
                fn = file.file_name[0:22].strip()
                filename = f"{fn}{oam}{sz[0:3]} {sz[-2:]}{oamm}"
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
                [InlineKeyboardButton("💡close💡", callback_data="close")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
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
            await message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=caption, reply_markup=InlineKeyboardMarkup(buttons))

    else:
        await message.delete()

def get_size(size):
    """Get size in readable format"""

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

async def spell(message):
    titl = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)", "", message.text, flags=re.IGNORECASE) # plis contribute some common words 
    title = titl.strip()
    btn = []
    user = message.from_user.id if message.from_user else 0
    movies = await get_post(title, bulk=True)
    if not movies:
        return await advantage_spell_chok(message)
    oam = f"{random.choice(RAT)}"
    for movie in movies:
        title = movie.get('title')[:25]
        id = movie.get('imdb_id')
        year = movie.get('year') if movie.get else "None"
        btn.append(
            [InlineKeyboardButton(text=f"{title} {oam} {year}",callback_data=f"spo#se#{user}#{id}")]
        )
    if len(btn) > 10: 
        btn = btn[:10]
    btn.append([InlineKeyboardButton(text="🔺 Close 🔺", callback_data=f'spo#se#{user}#close_spellcheck')])
    await message.reply('𝐃𝐢𝐝 𝐲𝐨𝐮 𝐦𝐞𝐚𝐧 𝐚𝐧𝐲 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐬𝐞 ? 👇', reply_markup=InlineKeyboardMarkup(btn)) 

async def advantage_spell_chok(message):
    query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)", "", message.text, flags=re.IGNORECASE) # plis contribute some common words 
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(message.text)
    gs_parsed = []
    if not g_s:
        k = await message.reply("**I couldn't find any movie in that name**.")
        await asyncio.sleep(8)
        await k.delete()
        await message.delete()
        return
    # regex = re.compile(r".*(imdbb|wikipedia).*", re.IGNORECASE) # look for imdb / wiki results
    # gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)', '', i, flags=re.IGNORECASE) for i in g_s]
    if not gs_parsed:
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
        k = await message.reply("I couldn't find anything related to that. Check your spelling")
        await asyncio.sleep(8)
        await k.delete()
        return
    SPELL_CHECK[message.message_id] = movielist
    btn = [[
                InlineKeyboardButton(
                    text=movie.strip(),
                    callback_data=f"spo#sa#{user}#{k}",
                )
            ] for k, movie in enumerate(movielist)]
    if len(btn) > 6: 
        btn = btn[:6]
    btn.append([InlineKeyboardButton(text="🔺 Close 🔺", callback_data=f'spo#sa#{user}#close_spellcheck')])
    kdm = await message.reply("ɪ ᴄᴏᴜʟᴅɴ'ᴛ ғɪɴᴅ ᴀɴʏᴛʜɪɴɢ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ᴛʜᴀᴛ \n 𝐃𝐢𝐝 𝐲𝐨𝐮 𝐦𝐞𝐚𝐧 𝐚𝐧𝐲 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐬𝐞 ?👇", reply_markup=InlineKeyboardMarkup(btn))


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
            for files in filedetails:
                title = files.file_name[0:-4]
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
                        InlineKeyboardButton('ᴍᴀɪɴ ɢʀᴏᴜᴘ', url='https://t.me/+PBGW_EV3ldY5YjJl'),
                        InlineKeyboardButton('sᴇᴀʀᴄʜ ғɪʟᴇ', switch_inline_query_current_chat='')
                    ]
                    ]

            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"http://t.me/On_air_Filter_bot?start=subinps_-_-_-_{file_id}")
                return
            elif (clicked == typed):
                try:  
                    await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f"<code>" + title + "</code>""\n\n <b>[𝙼𝚘𝚟𝚒𝚎/sᴇʀɪᴇs ʀᴇϙᴜᴇsᴛɪɴɢ 𝚐𝚛𝚘𝚞𝚙](https://t.me/+eDjzTT2Ua6kwMTI1)</b>",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                except UserIsBlocked:
                    await query.answer(url=f"http://t.me/On_air_Filter_bot?start=subinps_-_-_-_{file_id}")
                else:
                    await query.answer("ᴄʜᴇcᴋ ᴩᴍ 👀 \n\n file🎬 has 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈✔️ sent to your pm",show_alert=True)
            else:
                await query.answer(url=f"http://t.me/On_air_Filter_bot?start=subinps_-_-_-_{file_id}")           
    
    elif query.data.startswith("myree"):
            ident, file_name = query.data.split("#")
            await query.answer(url=f"http://t.me/On_air_Filter_bot?start=saran=={file_name}")

    elif (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("⭕️ You are using this for one of my old message, please send the request again ⭕️.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ⇍", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"🎪 Pages {int(index)+2}/{data['total']}🎪", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="🕵️𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼",callback_data=f"myree#")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ⇍", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"🎪{int(index)+2}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="🕵️𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼",callback_data=f"myree#")]
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
                buttons.append(
                    [InlineKeyboardButton(text="🕵️𝚂𝙴𝙰𝚁𝙲𝙷 𝙸𝙽 𝙿𝙼",callback_data=f"myree#")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
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
        elif query.data == "about":
            await query.answer("🤖 ɴᴀᴍᴇ: ᴀᴜᴛᴏ ғɪʟᴛᴇʀ v2.7\n🎪ᴄʀᴇᴀᴛᴏʀ: sᴀʀᴀɴ\n📚ʟᴀɴɢᴜᴀɢᴇ: ᴘʏᴛʜᴏɴ3\n🌀 ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄɪᴏ 1.13.0",show_alert=True)
        elif query.data == "close":
            await query.message.delete()
            try:
                await message.delete()
            except KeyError:
                await query.answer(" your query message is deleted 🌩️",show_alert=True)
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
                        InlineKeyboardButton('🎪 ɢʀᴏᴜᴘ', url='https://t.me/+PBGW_EV3ldY5YjJl'),
                        InlineKeyboardButton(' 🔍 sᴇᴀʀᴄʜ ғɪʟᴇ', switch_inline_query_current_chat='')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f"<b>©[ᵒⁿᵃⁱʳᵐᵒᵛⁱᵉˢ](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n 🎬 file name 👉  </b>""<code>" + title + "</code>""\n\n[𝙼𝚘𝚟𝚒𝚎 ʀᴇϙᴜᴇsᴛɪɴɢ 𝚐𝚛𝚘𝚞𝚙](https://t.me/+eDjzTT2Ua6kwMTI1)",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    ) 


        elif query.data == "pages":
            await query.answer()

    else:
        await query.answer("😊  Bro. search your own file, Don't click others Requested files🎬",show_alert=True)
