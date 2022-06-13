import os
import re
import logging
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest, CallbackQuery
from info import START_MSG, CHANNELS, ADMINS, AUTH_CHANNEL, AUTH_GROUPS, CUSTOM_FILE_CAPTION, API_KEY
from utils import Media, get_file_details, get_poster, unpack_new_file_id, get_post
from info import TUTORIAL
from info import IMDB_TEMPLATE, IMDB_TEMPLATEE
from pyrogram.errors import UserNotParticipant
logger = logging.getLogger(__name__)

MYRE = ["CAADBQAD2AMAAvjDaFSsTHfTpJDaShYE", "CAADBQADDQMAAtC6kVRSm-hyq9LjMRYE", "CAADBQADowEAAsuvXSk7LlkDJBYrnRYE", "CAADBQADAQcAAljMOFdOolwetNErQxYE", "CAADBQADeAMAArLJgFRXeMmuvdTQchYE", "CAADBQADsAMAAgYG8VSFaQgU6X596BYE", "CAADBQAD6AMAAi8MwVS1_PRa7JTUWxYE", "CAADBQADOgIAAnRfsFRgDjrWSQK3kxYE", "CAADBQADRAQAAlaVaVSKDdtGH1UJKhYE", ]
PHOT = [
    "https://telegra.ph/file/9075ca7cbad944afaa823.jpg",
    "https://telegra.ph/file/9688c892ad2f2cf5c3f68.jpg",
    "https://telegra.ph/file/51683050f583af4c81013.jpg",
]
LN = "https://t.me/+PBGW_EV3ldY5YjJl"

@Client.on_message(filters.command("start"))
async def start(bot, cmd):
    usr_cmdall1 = cmd.text
    await cmd.delete()
    if usr_cmdall1.startswith("/start subinps"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=cmd.from_user.id,
                        text="Sorry  mowna 💋, You are Banned to use me.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                ident, file_id = cmd.text.split("_-_-_-_")
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="**Join My group to use this Bot**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(" ᴊᴏɪɴ ɢʀᴏᴜᴩ 🎪 ", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton(" 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽 🔄", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Something went Wrong.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
            await cmd.reply_chat_action("upload_document")
            await asyncio.sleep(.5)
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
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('ᴍᴀɪɴ ɢʀᴏᴜᴘ', url=f'{LN}'),
                        InlineKeyboardButton('sᴇᴀʀᴄʜ ғɪʟᴇ', switch_inline_query_current_chat='')
                    ]
                    ]
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption="<b>🎬ꜰɪʟᴇ ɴᴀᴍᴇ⇛</b>""<code>" + title + "</code>""\n\n<b>[ᴍᴏᴠɪᴇ/sᴇʀɪᴇs ʀᴇϙᴜᴇsᴛɪɴɢ 𝚐𝚛𝚘𝚞𝚙](https://t.me/+eDjzTT2Ua6kwMTI1)</b>",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    elif len(cmd.command) > 1 and cmd.command[1] == 'join':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="** Join My  group🎪 to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🎪 Join group 🎪", url=invite_link.invite_link)
                    ]
                ]
            )
        )
    elif len(cmd.command) > 1 and cmd.command[1] == 'okay':
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**request on group🎪**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🎪 group 🎪", url="https://t.me/+eDjzTT2Ua6kwMTI1")
                    ]
                ]
            )
        )
    elif usr_cmdall1.startswith("/start saran"):
        ident, file_name = cmd.text.split("==")
        await cmd.reply_chat_action("typing")
        await asyncio.sleep(1)
        x = file_name.split("_")
        hari = " ".join(x)
        await cmd.reply_text(
            "**തായേ👇 കാണുന്ന 🔍𝗦𝗲𝗮𝗿𝗰𝗵 𝗙𝗶𝗹𝗲 എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്തു 🎬 സിനിമ ഫയൽ തിരഞ്ഞെടുക്കുക** \n\n **👇Click on the 🔍𝗦𝗲𝗮𝗿𝗰𝗵 𝗙𝗶𝗹𝗲 button and Select the movie file**",
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('🔍 sᴇᴀʀᴄʜ ғɪʟᴇ 💼', switch_inline_query_current_chat=f'{hari}')
                    ]
                ]
            )
        )
    else:
        await cmd.reply_text(
            START_MSG.format(cmd.from_user.first_name),
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴀʙᴏᴜᴛ 💡",callback_data="about"),
                        InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ 🍿", url="https://t.me/joinchat/4-Quex2FaFhjMDM1")   
                    ],
                    [
                        InlineKeyboardButton("ɢʀᴏᴜᴩ 1 🎪", url=f"{LN}"),
                        InlineKeyboardButton("ɢʀᴏᴜᴩ 2 🎪", url="https://t.me/+eDjzTT2Ua6kwMTI1")   
                    ],
                    [
                        InlineKeyboardButton("🔎 𝚂𝙴𝙰𝚁𝙲𝙷 𝙵𝙸𝙻𝙴 🔍", switch_inline_query_current_chat='')
                    ],
                    [
                        InlineKeyboardButton('🔍 ɢᴏ ɪɴʟɪɴᴇ 🔎', switch_inline_query='')
                    ]
                ]
            )
        )

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def total(bot, message):
    """Show total files in database"""
    msg = await message.reply("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f' Saved files: {total}')
    except Exception as e:
        logger.exception('Failed to check total files')
        await msg.edit(f'Error: {e}')


@Client.on_message(filters.command('logger') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))


@Client.on_message(filters.command('del') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /del which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        await msg.edit('File not found in database')
@Client.on_message(filters.command('rul'))
async def bot_indo(bot, message):
    buttons = [
        [
            InlineKeyboardButton('⚠️ group rules ⚠️', url='https://t.me/movie_requesting_group_rules/4')
        ]
        ] 
    await message.reply(text=f"<b>click the 👇 button to read group rules </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
@Client.on_message(filters.command(['search', 'help']) & filters.private)
async def bot_link(bot, message):
    buttons = [
        [
            InlineKeyboardButton('🔍 sᴇᴀʀᴄʜ ғɪʟᴇ 💼', switch_inline_query_current_chat='')
        ]
        ]
    await message.reply_chat_action("typing")
    await asyncio.sleep(1)
    await bot.send_message(chat_id=message.from_user.id, text="<b>തായേ👇 കാണുന്ന 🔍𝗦𝗲𝗮𝗿𝗰𝗵 𝗙𝗶𝗹𝗲 എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്തു 🎬സിനിമയുടെ പേര്  ടൈപ്പ് ചെയ്യുക</b> \n\n <b>👇Click on the 🔍𝗦𝗲𝗮𝗿𝗰𝗵 𝗙𝗶𝗹𝗲 button and type the name of the movie‌‌</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
@Client.on_message(filters.command('about') & filters.private)
async def bot_info(bot, message):
    buttons = [
        [
            InlineKeyboardButton("🎪 ɢʀᴏᴜᴘ  🎪", url="https://t.me/+eDjzTT2Ua6kwMTI1")
        ]
        ]
    await message.reply_chat_action("typing")
    await asyncio.sleep(1)
    a = await message.reply(text=f"🧞‍♂️ ɴᴀᴍᴇ : ᴀᴜᴛᴏ ғɪʟᴛᴇʀ v2.7 \n\n🎪 ᴄʀᴇᴀᴛᴏʀ : [sᴀʀᴀɴ](https://t.me/+aZIoNNlskWk4ODg1)\n\n📚 ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ3\n\n🌀 ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄɪᴏ 1.13.0\n\n🥀 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ : [ᴄʟɪᴄᴋ ᴍᴇ](https://t.me/nokiyirunnoippokitum)", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    await asyncio.sleep(4) # program error 
    await a.delete()
    await bot.send_sticker(chat_id=message.from_user.id, sticker=f"{random.choice(MYRE)}")
@Client.on_message(filters.command('source'))
async def bot_srern(bot, message):
    await bot.send_sticker(chat_id=message.from_user.id, sticker=f"{random.choice(MYRE)}")
@Client.on_message(filters.command('group'))
async def bot_kunna(bot, message):
    buttons = [
        [
            InlineKeyboardButton('🍿 ɢʀᴏᴜᴘ  🍿', url='https://t.me/+eDjzTT2Ua6kwMTI1')
        ]
        ]
    await message.reply_chat_action("typing")
    await asyncio.sleep(1)
    await message.reply(text=f"<b>പുതിയതും പഴയതും ആയ എല്ലാ 🎬 സിനിമകളും നിങ്ങൾക് ഈ ഗ്രൂപ്പിൽ ചോദിക്കാം , താല്പര്യം ഉള്ളവർ താഴെ👇 ഉള്ള ലിങ്കിൽ കേറി പോരുക\n\n\n https://t.me/+eDjzTT2Ua6kwMTI1 https://t.me/+eDjzTT2Ua6kwMTI1 </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
@Client.on_message(filters.regex('https') & filters.group & filters.chat(AUTH_GROUPS) & ~filters.user(ADMINS))
async def hellto(bot, message):
    await message.delete()
@Client.on_chat_join_request(filters.chat(AUTH_GROUPS))
async def autoapprove(bot, message: ChatJoinRequest):
    chat=message.chat # Chat
    user=message.from_user # User
    await asyncio.sleep(2)
    await bot.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    cg = await bot.send_message(chat_id=chat.id, text=f"ʜɪ {user.mention} \n 💐 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {chat.title}")
    await asyncio.sleep(16) 
    await cg.delete()
@Client.on_message(filters.new_chat_members & filters.chat(AUTH_GROUPS))
async def auto_welcoime(bot, message):
    chat=message.chat
    user=message.from_user
    cg = await bot.send_message(chat_id=chat.id, text=f"ʜɪ {user.mention} \n 💐 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {chat.title}")
    await asyncio.sleep(16) 
    await cg.delete()
@Client.on_message(filters.forwarded & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) & ~filters.user(ADMINS))
async def delfor(bot,message):
    await message.delete()
@Client.on_message(filters.regex('movie') & filters.group & filters.incoming & ~filters.user(ADMINS))
async def helmo(bot, message):
    buttons = [
        [
            InlineKeyboardButton(text="🔍 ꜱᴇᴀʀᴄʜ ʙᴏᴛ",callback_data=f"myree#"),
            InlineKeyboardButton(' 🔍 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ', url='https://www.google.com/')
        ]
        ]
    mo = await message.reply(text=f"𝗦𝗲𝗻𝘁 𝗠𝗼𝘃𝗶𝗲 𝗡𝗮𝗺𝗲 & 𝘆𝗲𝗮𝗿 𝗼𝗻𝗹𝘆 \n മൂവിയുടെ പേര് & വർഷം മാത്രം മതി \n ᴇxᴀᴍᴘʟᴇ :👇\n\n ᴛᴇɴᴇᴛ ✅ \n ᴛᴇɴᴇᴛ 2021 ✅ \n ᴛᴇɴᴇᴛ ᴍᴏᴠɪᴇ ❌ \n\n▫️ɪғ ʏᴏᴜ sᴛɪʟʟ ᴅᴏ ɴᴏᴛ ғɪɴᴅ ᴛʜᴇ 😪 ᴍᴏᴠɪᴇ sᴇᴀʀᴄʜ ᴛʜᴇ ʙᴏᴛ👇\n▪️ɪғ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ᴋɴᴏᴡ ᴛʜᴇ ᴍᴏᴠɪᴇ ᴄᴜʀʀᴇᴄᴛ sᴘᴇʟʟɪɴɢ ᴄʟɪᴄᴋ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ 👇", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    await asyncio.sleep(15) # error 
    await mo.delete()
    await message.delete()
@Client.on_message(filters.command('mlm_new') & filters.private)
async def textx(bot, message):
    buttons = [
        [
            InlineKeyboardButton('🔍 sᴇᴀʀᴄʜ 🍿', switch_inline_query_current_chat='2022 malayalam')
        ]
        ]
    await message.reply_chat_action("typing")
    await asyncio.sleep(1)
    await bot.send_message(chat_id=message.from_user.id, text="<b>ഏറ്റവും പുതിയതായി ബോട്ടിൽ add ചെയ്ത മലയാളം സിനിമകൾക്കായ് തായേ👇 കാണുന്ന 🔍 𝗦𝗲𝗮𝗿𝗰𝗵 എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്ത ശേഷം അനുയോജ്യമായ file select ചെയ്യുക 😇</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
@Client.on_message(filters.regex('Livegram') & filters.private)
async def dfhhg(bot, message):
    await message.delete()
    await asyncio.sleep(1)
    await message.reply(f"<code> മുകളിൽ കാണുന്ന -𝘀𝗲𝗮𝗿𝗰𝗵 𝗳𝗶𝗹𝗲- എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്തു സിനിമയുടെ പേര്  ടൈപ്പ് ചെയ്താൽ  സിനിമ ഫയൽ ലഭികും</code> \n\n <b>⚠️ Note: search ചെയ്യുബോൾ Correct Spelling ആയിരിക്കണം. Correct Spelling അറിയാൻ ഗൂഗിളിൽ നോക്കി  ടൈപ്പ് ചെയ്യുക</b>")
@Client.on_message(filters.command('idd'))
async def texthx(bot, message):
    status_message = await message.reply_text(
        "`Fetching user info...`"
    )
    await status_message.edit(
        "`Processing user info...`"
    )
    
    from_user = message.reply_to_message.from_user
    
    if from_user is None:
        return await status_message.edit("no valid user_id / message specified")
    message_out_str = ""
    message_out_str += f"<b>➲First Name:</b> {message.reply_to_message.from_user.first_name}\n"
    last_name = from_user.last_name or "<b>None</b>"
    message_out_str += f"<b>➲Last Name:</b> {last_name}\n"
    message_out_str += f"<b>➲Telegram ID:</b> <code>{from_user.id}</code>\n"
    username = from_user.username or "<b>None</b>"
    dc_id = from_user.dc_id or "[User Doesn't Have A Valid DP]"
    message_out_str += f"<b>➲Data Centre:</b> <code>{dc_id}</code>\n"
    message_out_str += f"<b>➲User Name:</b> @{username}\n"
    message_out_str += f"<b>➲User 𝖫𝗂𝗇𝗄:</b> <a href='tg://user?id={from_user.id}'><b>Click Here</b></a>\n"
    await status_message.edit(f"{message_out_str}")

@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('my group ', url=f'https://t.me/+eDjzTT2Ua6kwMTI1')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>Hello Friends, \nMy admin has told me to leave from group so i go! If you wanna add me again contact my support group.</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"left the chat `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')
  
@Client.on_message(filters.command('f_link') & filters.user(ADMINS))
async def gen_link_s(bot, message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply('Reply to a message to get a shareable link.')
    file_type = replied.media
    if file_type not in ["video", 'audio', 'document']:
        return await message.reply("Reply to a supported media")
    file_id, ref = unpack_new_file_id((getattr(replied, file_type)).file_id)
    await message.reply(f"https://telegram.dog/On_air_Filter_bot?start=subinps_-_-_-_{file_id}")

@Client.on_message(filters.command('imdb') & filters.private)
async def imdb_searh(bot, message):
    if ' ' in message.text:
        r, title = message.text.split(None, 1)
        movies = await get_post(title, bulk=True)
        if not movies:
            return await message.reply("No results Found")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await message.reply('Here is what i.found on IMDb', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('Give me a movie / series Name')

@Client.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot, quer_y: CallbackQuery):
    i, movi = quer_y.data.split('#')
    movie = movi[-7:]
    try:
        typed = quer_y.message.reply_to_message.from_user.id
    except:
        typed = quer_y.from_user.id
        pass
    imdb = await get_post(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{imdb.get('title')}",
                    switch_inline_query_current_chat=f"{imdb.get('title')}"
                )
            ]
        ]
    message = quer_y.message.reply_to_message or quer_y.message
    if imdb:
        caption = IMDB_TEMPLATEE.format(
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
        caption = "No Results🤷🏻‍♂️"
    await quer_y.answer(caption, show_alert=True)
