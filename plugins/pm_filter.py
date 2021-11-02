#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
import random
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster
BUTTONS = {}
BOT = {}

RAT = ["🎪", "🇲🇰", "🌀", "🍿", "🎬", ]
RATING = ["5.1/10 🤺ɪᴍᴅʙ", "6.2/10 🤺ɪᴍᴅʙ", "7.3/10 🤺ɪᴍᴅʙ", "8.4/10 🤺ɪᴍᴅʙ", "7.5/10 🤺ɪᴍᴅʙ", ]
GENRES = ["ғᴜɴ🍿 ғᴀᴄᴛ",
         "ᴛʜʀɪʟʟᴇʀ🍿",
         "ᴅʀᴀᴍᴀ🍿 ᴄᴏᴍᴇᴅʏ",
         "ғᴀᴍɪʟʏ🍿 ᴅʀᴀᴍᴀ",
         "ᴀᴅᴠᴇɴᴛᴜʀᴇ🍿",
         "ғɪʟᴍ ɴᴏɪʀ🍿",
         "ᴅᴏᴄᴜᴍᴇɴᴛᴀʀʏ🍿"]

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry mowne 💋, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Join My group🎪 to use this Bot 😉**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🎪 Join GROUP 🌀", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        rat = f"**{random.choice(RATING)}**[{get_size(file.file_size)}]** {file.file_name}**"
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = rat
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await client.send_photo(chat_id=message.from_user.id, photo='https://telegra.ph/file/69152843f167e3977e59d.jpg')
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
                [InlineKeyboardButton(text="🎪 Pages 1/1 🎪",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n  <b>🌀 ᴄʜᴀɴɴᴇʟ : [ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n <b>🌀 ᴄʜᴀɴɴᴇʟ : [ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="⇛⇛next⇛⇛",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🎪 Pages 1/{data['total']}🎪",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n <b>🌀 ᴄʜᴀɴɴᴇʟ :[ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : {search} ‌‌‌‌‎</b> \n\n <b>🌀 ᴄʜᴀɴɴᴇʟ :[ᴏɴᴀɪʀᴍᴏᴠɪᴇs](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []

        search = message.text
        result_txt = f"**<b>🎬 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ : ‌‌‌‌‎</b>** ‌‌‌‌‎<b> {search}‌‌‌‌‎</b>\n\n**‌‌‌‌‎🦚ʀᴀᴛɪɴɢ‌‌‌‌‎ :** {random.choice(RATING)}\n**🎭ɢᴇɴʀᴇ :** {random.choice(GENRES)}\n\n**⚡️ᴘᴏᴡᴇʀᴇᴅ ʙʏ:[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)\n**©[🎪 ᴛᴇʟᴇ ɢʀᴀᴍᴀᴍ 🎪](https://t.me/joinchat/q4xMr02fvA9jNzQ1) **"

        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"🎪-[{get_size(file.file_size)}]-🥀-{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
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
                [InlineKeyboardButton(text="🎪 Pages 1/1 🎪",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=result_txt, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(result_txt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="⇛⇛next⇛⇛",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🎪 Pages 1/{data['total']}🎪",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=result_txt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(result_txt, reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

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
                    [InlineKeyboardButton("⇚⇚back⇚⇚", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🎪 Pages {int(index)+2}/{data['total']}🎪", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇚⇚back⇚⇚", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("⇛⇛next⇛⇛", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🎪 Pages {int(index)+2}/{data['total']}🎪", callback_data="pages")]
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
                    [InlineKeyboardButton("⇛⇛next⇛⇛", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🎪 Pages {int(index)}/{data['total']}🎪", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇚⇚back⇚⇚ ", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("⇛⇛next⇛⇛", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🎪 Pages {int(index)}/{data['total']}🎪", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('🎪 group ⭕️', url='https://t.me/joinchat/q4xMr02fvA9jNzQ1'),
                    InlineKeyboardButton('on air ', url=f'{TUTORIAL}')
                ]
                ]
            await query.message.edit(text=f"<b>Developer⭕️ : <a href='https://github.com/subinps'>SUBIN</a>\nLanguage : <code>Python3</code>\nLibrary : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio</a>\nSource Code : <a href='https://t.me/joinchat/q4xMr02fvA9jNzQ1'>Click here</a>\nUpdate Channel⭕️ : <a href='https://t.me/bhddhhddnjd'>on air</a> </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)



        elif query.data.startswith("subinps"):
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
                        InlineKeyboardButton('🎪 group 🎪', url='https://t.me/joinchat/q4xMr02fvA9jNzQ1')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption="<b>©[ᵒⁿᵃⁱʳᵐᵒᵛⁱᵉˢ](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n 🎬 file name 👉</b>""<code>" + title + "</code>""\n\n [𝙼𝚘𝚟𝚒𝚎 ʀᴇϙᴜᴇsᴛɪɴɢ 𝚐𝚛𝚘𝚞𝚙](https://t.me/joinchat/q4xMr02fvA9jNzQ1)",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("⭕️ ഗ്രൂപ്പിൽ ജോയിൻ ചെയ്തതിനു ശേഷം ക്ലിക്ക് ചെയ്യൂ 😉⭕️",show_alert=True)
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
                        InlineKeyboardButton('🎪 group 🎪', url=f'https://t.me/joinchat/q4xMr02fvA9jNzQ1')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f"<b>©[ᵒⁿᵃⁱʳᵐᵒᵛⁱᵉˢ](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n 🎬 file name 👉  </b>""<code>" + title + "</code>""\n\n[𝙼𝚘𝚟𝚒𝚎 ʀᴇϙᴜᴇsᴛɪɴɢ 𝚐𝚛𝚘𝚞𝚙](https://t.me/joinchat/q4xMr02fvA9jNzQ1)",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    ) 


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("⭕️ യെടാ മോനാ ഇത് നിനക്ക് ഉള്ളതല്ല 🙃 ⭕️",show_alert=True)
