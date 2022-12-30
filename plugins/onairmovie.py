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

INMAL = """താങ്കൾ ആവശ്യപ്പെട്ട ഫയൽ എനിക്ക് കണ്ടെത്താനായില്ല 😕
താഴെ പറയുന്ന കാര്യങ്ങളിൽ ശ്രദ്ധിക്കുക...

=> കറക്റ്റ് സ്പെല്ലിംഗിൽ ചോദിക്കുക.

=> ഒ.ടി.ടി പ്ലാറ്റ്ഫോമുകളിൽ റിലീസ് ആകാത്ത സിനിമകൾ ചോദിക്കരുത്.

=> കഴിവതും [സിനിമയുടെ പേര്, വർഷം] ഈ രീതിയിൽ ചോദിക്കുക.

=> ഗൂഗിളിൽ സെർച്ച് ചെയ്യാനായി താഴെ കാണുന്ന ബട്ടൺ ഉപയോഗിക്കാം 😌"""

INTAM = """நீங்கள் கோரிய கோப்பை என்னால் கண்டுபிடிக்க முடியவில்லை 😕
பின்வருவனவற்றை செய்ய முயற்சிக்கவும்...

=> சரியான எழுத்துப்பிழையுடன் கோரிக்கை

=> OTT இயங்குதளங்களில் வெளியிடப்படாத திரைப்படங்களைக் கேட்க வேண்டாம்

=> [MovieName, year] இந்த வடிவமைப்பில் கேட்க முயற்சிக்கவும்.

=> Google இல் தேட கீழே உள்ள பொத்தானைப் பயன்படுத்தவும் 😌"""

INHIN = """मुझे आपके द्वारा अनुरोधित फ़ाइल नहीं मिली 😕
निम्नलिखित करने का प्रयास करें...

=> सही वर्तनी के साथ अनुरोध

=> उन फिल्मों के बारे में न पूछें जो ओटीटी प्लेटफॉर्म पर रिलीज नहीं हुई हैं

=> इस प्रारूप में [MovieName, year] में पूछने का प्रयास करें।

=> Google पर खोजने के लिए नीचे दिए गए बटन का प्रयोग करें 😌"""

INENG = """I couldn't find the file you requested 😕
Try to do the following...

=> Request with correct spelling

=> Don't ask movies that are not released in OTT platforms

=> Try to ask in [MovieName, year] this format.

=> Use the button below to search on Google 😌"""
