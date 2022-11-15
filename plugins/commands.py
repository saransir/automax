import os
import re
import logging
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest, CallbackQuery, ForceReply
from info import START_MSG, CHANNELS, ADMINS, AUTH_CHANNEL, AUTH_GROUPS, CUSTOM_FILE_CAPTION, API_KEY
from utils import Media, get_file_details, get_poster, unpack_new_file_id, get_post, add_filter, get_filters, delete_filter
from info import TUTORIAL
from info import IMDB_TEMPLATE, IMDB_TEMPLATEE
from plugins.pm_filter import spell
from pyrogram.errors import UserNotParticipant
logger = logging.getLogger(__name__)
from asyncio.exceptions import TimeoutError
MYRE = ["CAADBQAD2AMAAvjDaFSsTHfTpJDaShYE", "CAADBQADDQMAAtC6kVRSm-hyq9LjMRYE", "CAADBQADowEAAsuvXSk7LlkDJBYrnRYE", "CAADBQADAQcAAljMOFdOolwetNErQxYE", "CAADBQADeAMAArLJgFRXeMmuvdTQchYE", "CAADBQADsAMAAgYG8VSFaQgU6X596BYE", "CAADBQAD6AMAAi8MwVS1_PRa7JTUWxYE", "CAADBQADOgIAAnRfsFRgDjrWSQK3kxYE", "CAADBQADRAQAAlaVaVSKDdtGH1UJKhYE", ]
HI = ["CAADAgADVBYAAtB7QUn8uVjZ80ZWKBYE", "CAADAgADjhUAAiVNwUmPFk1-69E28xYE", "CAADAgADbBkAArFrGEl6sWLRwfR3mhYE", "CAADAgADqBYAAsaGIEonqRtNuY60VRYE", "CAADAgADKRUAAiLQKEqf0KMMiyjVPBYE", "CAADAgADhxUAAj0PUEnem2b91sejvxYE", "CAADAgADCh0AAsGoIEkIjTf-YvDReBYE", "CAADAgADmxcAAgN6kEkVW672usFGgxYE", "CAADAgADoAADlp-MDmce7YYzVgABVRYE", "CAADAgADsQADwZxgDIoe_kMAAUM8AhYE", "CAADAgADuAAD9wLID0YLnLTiTgs4FgQ", "CAADAgAD0wIAAvPjvguBRPfRdizrsRYE", "CAADAgADbwADwZxgDMsOfYvA3U1WFgQ", "CAADAgAD_gADMNSdERxr3cDCcFZUFgQ", "CAADAgADbgUAAj-VzAqGOtldiLy3NRYE", ]
PHOT = [
    "https://telegra.ph/file/9075ca7cbad944afaa823.jpg",
    "https://telegra.ph/file/9688c892ad2f2cf5c3f68.jpg",
    "https://telegra.ph/file/51683050f583af4c81013.jpg",
]
LN = "https://t.me/+PBGW_EV3ldY5YjJl"

@Client.on_message(filters.regex('Livegram') & filters.private)
async def dfhhg(bot, message):
    return await message.delete()
   
@Client.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(bot, cmd):
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/start seren"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=cmd.from_user.id,
                        text="Sorry mowna 💋,You are Banned to use me.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return await cmd.delete()
            except UserNotParticipant:
                ident, file_id = cmd.text.split("_-_-_-_")
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="__Join My group 💒 to use this Bot__",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(" 👉 ᴊᴏɪɴ ɢʀᴏᴜᴩ 💒 ", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton(" 🖐️ 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽 🔄", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return await cmd.delete()
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Something went Wrong.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return await cmd.delete()
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
            await cmd.reply_chat_action("upload_document")
            await asyncio.sleep(.5)
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                at = files.file_name[0:-4]
                size=files.file_size
                title = re.sub(r"(#|\@|\~|\©|\[|\]|\_|\.)", " ", at, flags=re.IGNORECASE)
                buttons = [[InlineKeyboardButton("ɢʀᴏᴜᴩ 1", url="https://t.me/+PBGW_EV3ldY5YjJl"), InlineKeyboardButton("ɢʀᴏᴜᴩ 2", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]
                await cmd.delete()
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption=f"<b><u>#𝙵𝙸𝙻𝙴_𝙽𝙰𝙼𝙴⇛{title}</u></b>\n\n <i>ʙʏ⇛[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</i>",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    elif len(cmd.command) > 1 and cmd.command[1] == 'join':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="** Join My  group👇 to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("👉 Join group 🎪", url=invite_link.invite_link)
                    ]
                ]
            )
        )
        await cmd.delete()
    elif len(cmd.command) > 1 and cmd.command[1] == 'okay' or usr_cmdall1.startswith("/start saran"):
        user = cmd.from_user.id if cmd.from_user else 0
        while True:
            try:
                nx = await bot.ask(text="__ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴍᴏᴠɪᴇ\sᴇʀɪᴇs ɴᴀᴍᴇ ᴡɪᴛʜᴏᴜᴛ sᴘᴇʟʟɪɴɢ ᴍɪsᴛᴀᴋᴇ__", chat_id=cmd.from_user.id, filters=filters.text, timeout=30, reply_markup=ForceReply(placeholder="ᵗʸᵖᵉ...."))
            except TimeoutError:
                await cmd.reply("**ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ** __ᴏꜰ 30 ꜱᴇᴄᴏɴᴅꜱ \n\n try again♻️ or request on group👇__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎪 group 🎪", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]))
                return await cmd.delete()
            if not nx.reply_to_message or user != nx.from_user.id:
                await cmd.reply("__ᴛʜɪs ɪs ᴀɴ ɪɴᴠᴀʟɪᴅ ᴍᴇssᴀɢᴇ ᴛʀʏ ᴀɢᴀɪɴ__ ♻️")
                await asyncio.sleep(.8)
                continue
            else:
                await cmd.delete()
                await nx.reply_to_message.delete()
                break
        if nx.text.startswith("/"):
            await nx.delete()
            return
        else:
            await nx.forward("@S1a2r3a4n")
            return await spell(nx)
        """await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**request on group🎪**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🎪 group 🎪", url="https://t.me/+eDjzTT2Ua6kwMTI1")
                    ]
                ]
            )
        )"""
    elif usr_cmdall1.startswith("/start imx"):
        ident, file_name = cmd.text.split("==")
        await cmd.reply_chat_action("typing")
        await asyncio.sleep(1)
        x = file_name.split("_")
        hari = " ".join(x)
        await cmd.reply_text(
            "**തായേ👇 കാണുന്ന 🔍 𝗦𝗲𝗮𝗿𝗰𝗵 𝗙𝗶𝗹𝗲 എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്തു 🎬 സിനിമ ഫയൽ തിരഞ്ഞെടുക്കുക** \n\n **👇Click on the 🔍𝗦𝗲𝗮𝗿𝗰𝗵 𝗙𝗶𝗹𝗲 button and Select the movie file**",
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
        await cmd.delete()
    else:
        await cmd.reply_sticker(sticker=f"{random.choice(HI)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="start",callback_data="start")]]))
        await cmd.delete()
        
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

@Client.on_message(filters.command('add') & filters.private & filters.user(ADMINS))
async def addfilter(bot, message):
    reply = message.reply_to_message
    r, txt = message.text.split(None, 1)
    text = txt.lower()
    if reply:
        try:
            reply_text = message.reply_to_message.text
        except:
            reply_text = "𝑻𝒉𝒊𝒔 𝑴𝒐𝒗𝒊𝒆 𝑵𝒐𝒕 ʀᴇʟᴇᴀsᴇᴅ ᴏɴ ᴏᴛᴛ"         
    else:
        reply_text = "Tʜᴇᴀᴛʀɪᴄᴀʟ Pʀɪɴᴛ ɪꜱ Nᴏᴛ Aᴠᴀɪʟᴀʙʟᴇ Hᴇʀᴇ.Sᴛᴀy Tᴜɴᴇᴅ Fᴏʀ Tʜᴇ 'Oᴛᴛ' Rᴇʟᴇᴀꜱᴇ..!"

    await add_filter(text, reply_text)

    await message.reply_text(
        f"Filter for  `{text}`  added",
        quote=True,
        parse_mode="md"
    )
@Client.on_message(filters.command('dl') & filters.private & filters.user(ADMINS))
async def adekfilter(bot, message):
    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>Mention the filtername which you wanna delete!</i>\n\n"
            "<code>/dele filtername</code>\n\n",
            quote=True
        )
        return

    query = text.lower()

    await delete_filter(message, query)
@Client.on_message(filters.command('filters') & filters.private & filters.user(ADMINS))
async def adxfiltxr(bot, message):
    await get_filters(message)

@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def totalv(bot, message):
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


@Client.on_message(filters.command('del') & filters.private & filters.user(ADMINS))
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
    file_name = re.sub(r"(_|\-|\.|\@|\#|\+)", " ", str(media.file_name))
    result = await Media.collection.delete_one({
        'file_name': file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await message.delete()
        aa = await msg.edit('File is successfully deleted from database')
        await reply.delete()
        await asyncio.sleep(1)
        await aa.delete()
    else:
        result = await Media.collection.delete_one({
            'file_name': media.file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
        })
        if result.deleted_count:
            await message.delete()
            aa = await msg.edit('File is successfully deleted from database')
            await reply.delete()
            await asyncio.sleep(1)
            await aa.delete()
        else:
            await message.delete()
            await reply.delete()
            await msg.edit('File not found in database')

@Client.on_message(filters.command('search_f') & filters.private)
async def bot_link(bot, message):
    buttons = [
        [
            InlineKeyboardButton('🔍 🅂ᴇᴀʀᴄʜ 🄵ɪʟᴇ 💼', switch_inline_query_current_chat='')
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
    a = await message.reply(text=f"🧞‍♂️ ɴᴀᴍᴇ : ғɪʟᴛᴇʀ -x- v2.7 \n\n🎪 ᴄʀᴇᴀᴛᴏʀ : [sᴀʀᴀɴ](https://t.me/+aZIoNNlskWk4ODg1)\n\n📚 ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ3\n\n🌀 ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄɪᴏ 1.13.0\n\n🥀 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ : [ᴄʟɪᴄᴋ ᴍᴇ](https://t.me/nokiyirunnoippokitum)", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    await asyncio.sleep(4) # program error 
    await a.delete()
    await message.reply_sticker(sticker=f"{random.choice(MYRE)}", reply_markup=InlineKeyboardMarkup(buttons))
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
    await asyncio.sleep(2)
    await message.reply(text=f"<b>If you want all the new and old movies and web series, click on the link below 👇\n\n\n https://t.me/+eDjzTT2Ua6kwMTI1 https://t.me/+eDjzTT2Ua6kwMTI1 </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
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

@Client.on_message(filters.command('st_a_rt') & filters.private)
async def texddtx(bot, message):
    await message.reply_sticker(sticker=f"{random.choice(HI)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🎪 start 🎪",callback_data="start")]]))
    return await message.delete()  
@Client.on_message(filters.command('malalm_new') & filters.private)
async def textx(bot, message):
    buttons = [
        [
            InlineKeyboardButton('🔍 sᴇᴀʀᴄʜ 🍿', switch_inline_query_current_chat='2022 malayalam')
        ]
        ]
    await message.reply_chat_action("typing")
    await asyncio.sleep(1)
    await bot.send_message(chat_id=message.from_user.id, text="<b>ഏറ്റവും പുതിയതായി ബോട്ടിൽ add ചെയ്ത മലയാളം സിനിമകൾക്കായ് തായേ👇 കാണുന്ന 🔍 𝗦𝗲𝗮𝗿𝗰𝗵 എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്ത ശേഷം അനുയോജ്യമായ file select ചെയ്യുക 😇</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

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
    await message.reply(f"https://telegram.dog/On_air_Filter_bot?start=seren_-_-_-_{file_id}")

@Client.on_message(filters.command(['pmfilter', 'imdb']) & filters.private)
async def imdb_searh(bot, message):
    user = message.from_user.id if message.from_user else 0
    while True:
        try:
            nx = await bot.ask(text="__ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴍᴏᴠɪᴇ\sᴇʀɪᴇs ɴᴀᴍᴇ ᴡɪᴛʜᴏᴜᴛ sᴘᴇʟʟɪɴɢ ᴍɪsᴛᴀᴋᴇ__", chat_id=message.from_user.id, filters=filters.text, timeout=30, reply_markup=ForceReply(placeholder="ᵗʸᵖᵉ...."))
        except TimeoutError:
            await message.reply("**ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 30 ꜱᴇᴄᴏɴᴅꜱ \n\n try again♻️ or request on group👇**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎪 group 🎪", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]))
            return await message.delete()
        if not nx.reply_to_message or user != nx.from_user.id:
            await message.reply("__ᴛʜɪs ɪs ᴀɴ ɪɴᴠᴀʟɪᴅ ᴍᴇssᴀɢᴇ ᴛʀʏ ᴀɢᴀɪɴ__ ♻️")
            await asyncio.sleep(.8)
            continue
        else:
            await message.delete()
            await nx.reply_to_message.delete()
            break
    if nx.text.startswith("/"):
        await nx.delete()
        return
    else:
        return await spell(nx)
       
"""@Client.on_message(filters.regex('Name📃') & filters.private)
async def helmogth(bot, message):
    await asyncio.sleep(20)
    await message.delete()"""
@Client.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot, quer_y: CallbackQuery):
    i, movi = quer_y.data.split('#')
    movie = movi[2:]
    imdb = await get_post(query=movie, id=True)
    # message = quer_y.message.reply_to_message or quer_y.message
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
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url'],
            **locals()
        )
    else:
        await quer_y.answer("No Results🤷🏻‍♂️")
        return
    if len(caption) > 197: 
        cap = caption[:196] + "..."
    await quer_y.answer(cap, show_alert=True)
    
