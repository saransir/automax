import os
import logging
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import START_MSG, CHANNELS, ADMINS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
from utils import Media, get_file_details
from info import TUTORIAL
from pyrogram.errors import UserNotParticipant
logger = logging.getLogger(__name__)

MYRE = ["CAADBQAD2AMAAvjDaFSsTHfTpJDaShYE", "CAADBQADDQMAAtC6kVRSm-hyq9LjMRYE", "CAADBQADowEAAsuvXSk7LlkDJBYrnRYE", "CAADBQADAQcAAljMOFdOolwetNErQxYE", "CAADBQADeAMAArLJgFRXeMmuvdTQchYE", "CAADBQADsAMAAgYG8VSFaQgU6X596BYE", "CAADBQAD6AMAAi8MwVS1_PRa7JTUWxYE", "CAADBQADOgIAAnRfsFRgDjrWSQK3kxYE", "CAADBQADRAQAAlaVaVSKDdtGH1UJKhYE", ]
PHOT = [
    "https://telegra.ph/file/9075ca7cbad944afaa823.jpg",
    "https://telegra.ph/file/9688c892ad2f2cf5c3f68.jpg",
    "https://telegra.ph/file/51683050f583af4c81013.jpg",
]

@Client.on_message(filters.command("start"))
async def start(bot, cmd):
    usr_cmdall1 = cmd.text
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
                    text="**⭕️ Join My group to use this Bot ⭕️",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🌀 Join group 🌀", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton("🔄 Try Again 🔄", callback_data=f"checksub#{file_id}")
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
                        InlineKeyboardButton('🎪 ɢʀᴏᴜᴘ', url='https://t.me/+aZIoNNlskWk4ODg1'),
                        InlineKeyboardButton(' 🔍 sᴇᴀʀᴄʜ ғɪʟᴇ', switch_inline_query_current_chat='')
                    ]
                    ]
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption="<b>©[ᵒⁿᵃⁱʳᵐᵒᵛⁱᵉˢ](https://t.me/joinchat/4-Quex2FaFhjMDM1)\n 🎬file name 👉 </b>""<code>" + title + "</code>""\n\n<b>[𝙼𝚘𝚟𝚒𝚎 ʀᴇϙᴜᴇsᴛɪɴɢ 𝚐𝚛𝚘𝚞𝚙](https://t.me/+aZIoNNlskWk4ODg1)</b>",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    elif len(cmd.command) > 1 and cmd.command[1] == '⭕️subscribe⭕️':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="** Join My 🎪 group to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🎪 Join group 🎪", url=invite_link.invite_link)
                    ]
                ]
            )
        )
    elif usr_cmdall1.startswith("/start saran"):
        await cmd.reply_text(f"set")
    else:
        await cmd.reply_text(
            START_MSG,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🌀 ᴄʜᴀɴɴᴇʟ 🌀", url="https://t.me/joinchat/4-Quex2FaFhjMDM1"), 
                        InlineKeyboardButton("🎪 ɢʀᴏᴜᴘ  🎪", url="https://t.me/+aZIoNNlskWk4ODg1")
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
        await msg.edit(f'⭕️ Saved files: {total}')
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
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
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
@Client.on_message(filters.command(['search', 'help']))
async def bot_link(bot, message):
    buttons = [
        [
            InlineKeyboardButton('🔍 sᴇᴀʀᴄʜ ғɪʟᴇ 💼', switch_inline_query_current_chat='')
        ]
        ]
    await bot.send_message(chat_id=message.from_user.id, text="<b>തായേ👇 കാണുന്ന 🔍𝗦𝗲𝗮𝗿𝗰𝗵 𝗙𝗶𝗹𝗲 എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്തു 🎬സിനിമയുടെ പേര്  ടൈപ്പ് ചെയ്യുക</b> \n\n <b>👇Click on the 🔍𝗦𝗲𝗮𝗿𝗰𝗵 𝗙𝗶𝗹𝗲 button and type the name of the movie‌‌</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
@Client.on_message(filters.command('about'))
async def bot_info(bot, message):
    buttons = [
        [
            InlineKeyboardButton("🎪 ɢʀᴏᴜᴘ  🎪", url="https://t.me/+aZIoNNlskWk4ODg1")
        ]
        ]
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
            InlineKeyboardButton('🍿 ɢʀᴏᴜᴘ  🍿', url='https://t.me/+aZIoNNlskWk4ODg1')
        ]
        ]
    await message.reply(text=f"<b>പുതിയതും പഴയതും ആയ എല്ലാ 🎬 സിനിമകളും നിങ്ങൾക് ഈ ഗ്രൂപ്പിൽ ചോദിക്കാം , താല്പര്യം ഉള്ളവർ താഴെ👇 ഉള്ള ലിങ്കിൽ കേറി പോരുക\n\n\n https://t.me/+aZIoNNlskWk4ODg1 https://t.me/+aZIoNNlskWk4ODg1 https://t.me/+aZIoNNlskWk4ODg1 </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
@Client.on_message(filters.regex('https') & filters.group)
async def hellto(bot, message):
    await message.delete()
@Client.on_message(filters.regex('movie') & filters.group & filters.chat(AUTH_CHANNEL))
async def helmo(bot, message):
    buttons = [
        [
            InlineKeyboardButton('🔍 ꜱᴇᴀʀᴄʜ ʙᴏᴛ ', url='https://t.me/On_air_Filter_bot'),
            InlineKeyboardButton(' 🔍 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ', url='https://www.google.com/')
        ]
        ]
    mo = await message.reply(text=f"𝗦𝗲𝗻𝘁 𝗠𝗼𝘃𝗶𝗲 𝗡𝗮𝗺𝗲 & 𝘆𝗲𝗮𝗿 𝗼𝗻𝗹𝘆 \n മൂവിയുടെ പേര് & വർഷം മാത്രം മതി \n ᴇxᴀᴍᴘʟᴇ :👇\n\n ᴛᴇɴᴇᴛ ✅ \n ᴛᴇɴᴇᴛ 2021 ✅ \n ᴛᴇɴᴇᴛ ᴍᴏᴠɪᴇ ❌ \n\n▫️ɪғ ʏᴏᴜ sᴛɪʟʟ ᴅᴏ ɴᴏᴛ ғɪɴᴅ ᴛʜᴇ 😪 ᴍᴏᴠɪᴇ sᴇᴀʀᴄʜ ᴛʜᴇ ʙᴏᴛ👇\n▪️ɪғ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ᴋɴᴏᴡ ᴛʜᴇ ᴍᴏᴠɪᴇ ᴄᴜʀʀᴇᴄᴛ sᴘᴇʟʟɪɴɢ ᴄʟɪᴄᴋ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ 👇", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    await asyncio.sleep(15) # error 
    await mo.delete()
    await message.delete()
@Client.on_message(filters.command('mlm_new'))
async def textx(bot, message):
    buttons = [
        [
            InlineKeyboardButton('🔍 sᴇᴀʀᴄʜ 🍿', switch_inline_query_current_chat='2022 malayalam')
        ]
        ]
    await bot.send_message(chat_id=message.from_user.id, text="<b>ഏറ്റവും പുതിയതായി ബോട്ടിൽ add ചെയ്ത മലയാളം സിനിമകൾക്കായ് തായേ👇 കാണുന്ന 🔍 𝗦𝗲𝗮𝗿𝗰𝗵 എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്ത ശേഷം അനുയോജ്യമായ file select ചെയ്യുക 😇</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
@Client.on_message(filters.regex('Livegram'))
async def dfhhg(bot, message):
    await message.reply(f"𝙷𝙸 🙌🏻 **{message.from_user.mention}**\n <code> മുകളിൽ കാണുന്ന -𝘀𝗲𝗮𝗿𝗰𝗵 𝗳𝗶𝗹𝗲- എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്തു സിനിമയുടെ പേര്  ടൈപ്പ് ചെയ്താൽ  സിനിമ ഫയൽ ലഭികും</code> \n\n <b>⚠️ Note: search ചെയ്യുബോൾ Correct Spelling ആയിരിക്കണം. Correct Spelling അറിയാൻ ഗൂഗിളിൽ നോക്കി  ടൈപ്പ് ചെയ്യുക</b>")
    await message.delete()
