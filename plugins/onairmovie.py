from pyrogram import Client, filters
import datetime
import time
import logging
from saran import db
from info import ADMINS
import asyncio
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS) & filters.reply)
async def grp_brodcst(bot, message):
    chats = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    total_chats = await db.total_chat_count()
    done = 0
    failed =0

    success = 0
    async for chat in chats:
        pti, sh = await broadcast_messages(int(chat['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        await sts.edit(f"Broadcast in progress:\n\nTotal Chats {total_chats}\nCompleted: {done} / {total_chats}\nSuccess: {success}\nFailed: {failed}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Chats {total_chats}\nCompleted: {done} / {total_chats}\nSuccess: {success}\nFailed: {failed}")


async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"
