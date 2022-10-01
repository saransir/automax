import re
import base64
import logging
import pymongo
import random
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from struct import pack
from bs4 import BeautifulSoup
from pyrogram.errors import UserNotParticipant
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
import os
import PTN
import requests
import json
from imdb import IMDb
from info import DATABASE_URI, DATABASE_NAME, COLLECTION_NAME, USE_CAPTION_FILTER, AUTH_CHANNEL, API_KEY
from pm_filter import advantage_spell_chok
DATABASE_URI_2=os.environ.get('DATABASE_URI_2', DATABASE_URI)
DATABASE_NAME_2=os.environ.get('DATABASE_NAME_2', DATABASE_NAME)
COLLECTION_NAME_2="Posters"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
instance = Instance.from_db(db)

IClient = AsyncIOMotorClient(DATABASE_URI_2)
imdbdb=client[DATABASE_NAME_2]
imdb=Instance.from_db(imdbdb)
imdbb = IMDb()
myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]
RAT = ["🦋", "🌸", "🦄", "🎈", "🥀", "🌻", "🍭", "🍿", "🪁", "🗼",]

PHOTO = [
    "https://telegra.ph/file/9075ca7cbad944afaa823.jpg",
    "https://telegra.ph/file/9688c892ad2f2cf5c3f68.jpg",
    "https://telegra.ph/file/51683050f583af4c81013.jpg",
]

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        collection_name = COLLECTION_NAME

@imdb.register
class Poster(Document):
    imdb_id = fields.StrField(attribute='_id')
    title = fields.StrField()
    poster = fields.StrField()
    year= fields.IntField(allow_none=True)

    class Meta:
        collection_name = COLLECTION_NAME_2

async def add_filter(text, reply_text):
    mycol = mydb[str(2)]
    
    data = {
        'text':str(text),
        'reply':str(reply_text),
    }

    try:
        mycol.update_one({'text': str(text)},  {"$set": data}, upsert=True)
    except:
        logger.exception('Some error occured!', exc_info=True)
async def find_filter(name):
    mycol = mydb[str(2)]
    qu = (name.strip()).lower()
    query = mycol.find( {"text":qu})
    try:
        for file in query:
            reply_text = file['reply']
        return reply_text
    except:
        return None
async def get_filters(message):
    mycol = mydb[str(2)]
    texts = "filters 👇        "
    query = mycol.find()
    count = mycol.count()
    try:
        for file in query:
            text = file['text']
            keywords = " ×  `{}`\n".format(text)
            texts += keywords
    except:
        logger.exception('error at filters find', exc_info=True)
    await message.reply_text(
        f" '`{texts}`' \n total= {count}",
        quote=True,
        parse_mode="md"
    )
async def delete_filter(message, text):
    mycol = mydb[str(2)]
    
    myquery = {'text':text }
    query = mycol.count_documents(myquery)
    count = mycol.count()
    if query == 1:
        mycol.delete_one(myquery)
        await message.reply_text(
            f"'`{text}`'  deleted✌️ total= {count}",
            quote=True,
            parse_mode="md"
        )
    else:
        await message.reply_text("Couldn't find that filter!", quote=True)

async def spell(message):
    titl = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|malayalam|English|english|Malayalam|Hindi|hindi|Telugu|telugu|1080p|720p|HEVC|Esub|Kannada|kannada|tamil|Tamil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|with\ssubtitle(s)?)", "", message.text, flags=re.IGNORECASE) # plis contribute some common words 
    title = titl.strip()
    if len(title) <= 2:
        ki = await message.reply("** I couldn't find any movie in that name**.")
        await asyncio.sleep(8)
        await ki.delete()
        await message.delete()
        return
    fn = titl.replace(" ", "_")[0:30]
    btn = []
    user = message.from_user.id if message.from_user else 0
    movies = await get_post(title, bulk=True)
    if not movies:
        return await advantage_spell_chok(message)
    oam = f"{random.choice(RAT)}"
    for movie in movies:
        title = movie.get('title')[:25]
        year = movie.get('year')
        if not year:
            year = oam
        btn.append(
            [InlineKeyboardButton(text=f"{title} {oam} {year}",callback_data=f"spo#se#{user}#{movie.movieID}")]
        )
    if len(btn) > 9: 
        btn = btn[:9]
    btn.append([InlineKeyboardButton(text=f"🔖 ᴄʟᴏꜱᴇ", callback_data=f'spo#se#{user}#close_spellcheck'), InlineKeyboardButton(text=f"🔖 ᴩᴍ ",url=f"http://t.me/On_air_Filter_bot?start=saran=={fn}")])
    poster=None
    if API_KEY:
        poster=await get_poster(title)
    if poster:
        try:
            await message.reply_photo(photo=poster, caption="        𝐃𝐢𝐝 𝐲𝐨𝐮 𝐦𝐞𝐚𝐧 𝐚𝐧𝐲 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐬𝐞.  ? 👇", quote=True, reply_markup=InlineKeyboardMarkup(btn))
        except:
            await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=" 𝐃𝐢𝐝 𝐲𝐨𝐮 𝐦𝐞𝐚𝐧 𝐚𝐧𝐲 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐬𝐞 ?👇👇", quote=True, reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption="    𝐃𝐢𝐝 𝐲𝐨𝐮 𝐦𝐞𝐚𝐧 𝐚𝐧𝐲 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐬𝐞   ?👇", quote=True, reply_markup=InlineKeyboardMarkup(btn))

async def save_poster(imdb_id, title, year, url):
    try:
        data = Poster(
            imdb_id=imdb_id,
            title=title,
            year=int(year),
            poster=url
        )
    except ValidationError:
        logger.exception('Error occurred while saving poster in database')
    else:
        try:
            await data.commit()
        except DuplicateKeyError:
            logger.warning("already saved in database")
        else:
            logger.info("Poster is saved in database")

async def save_file(media):
    """Save file in database"""

    # TODO: Find better way to get same file_id for same media to avoid duplicates
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\-|\.|\@|\#|\+)", " ", str(media.file_name))

    try:
        file = Media(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None,
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in database')
    else:
        try:
            await file.commit()
        except DuplicateKeyError:
            logger.warning(media.file_name + " is already saved in database")
        else:
            logger.info(file_id + " is saved in database")
            
async def get_search_results(query, file_type=None, max_results=10, offset=0):
    """For given query return (results, next_offset)"""

    query = query.strip()
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')

    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []

    if USE_CAPTION_FILTER:
        filter = {'$or': [{'file_name': regex}, {'caption': regex}]}
    else:
        filter = {'file_name': regex}

    if file_type:
        filter['file_type'] = file_type

    total_results = await Media.count_documents(filter)
    next_offset = offset + max_results

    if next_offset > total_results:
        next_offset = ''

    cursor = Media.find(filter)
    # Sort by recent
    cursor.sort('$natural', -1)
    # Slice files according to offset and max results
    cursor.skip(offset).limit(max_results)
    # Get list of files
    files = await cursor.to_list(length=max_results)

    return files, next_offset


async def get_filter_results(query):
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []
    filter = {'file_name': regex}
    total_results = await Media.count_documents(filter)
    if int(total_results) > 150:
        total_results = 150
    cursor = Media.find(filter)
    cursor.sort('$natural', -1)
    files = await cursor.to_list(length=int(total_results))
    return files

async def get_file_details(query):
    filter = {'file_id': query}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    return filedetails


async def is_subscribed(bot, query):
    try:
        user = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
    except UserNotParticipant:
        pass
    except Exception as e:
        logger.exception(e)
    else:
        if not user.status == 'kicked':
            return True

    return False

async def get_poster(movie):
    extract = PTN.parse(movie)
    try:
        title=extract["title"]
    except KeyError:
        title=movie
    try:
        year=extract["year"]
        year=int(year)
    except KeyError:
        year=None
    if year:
        filter = {'$and': [{'title': str(title).lower().strip()}, {'year': int(year)}]}
    else:
        filter = {'title': str(title).lower().strip()}
    cursor = Poster.find(filter)
    is_in_db = await cursor.to_list(length=1)
    poster=None
    if is_in_db:
        for nyav in is_in_db:
            poster=nyav.poster
    else:
        if year:
            url=f'https://www.omdbapi.com/?s={title}&y={year}&apikey={API_KEY}'
        else:
            url=f'https://www.omdbapi.com/?s={title}&apikey={API_KEY}'
        try:
            n = requests.get(url)
            a = json.loads(n.text)
            if a["Response"] == 'True':
                y = a.get("Search")[0]
                v=y.get("Title").lower().strip()
                poster = y.get("Poster")
                year=y.get("Year")[:4]
                id=y.get("imdbID")
                await get_all(a.get("Search"))
        except Exception as e:
            logger.exception(e)
            pass
    return poster

async def get_post(query, bulk=False, id=False, file=None):
    if not id:
        # https://t.me/GetTGLink/4183
        query = (query.strip()).lower()
        title = query
        year = re.findall(r'[1-2]\d{3}$', query, re.IGNORECASE)
        if year:
            year = list_to_str(year[:1])
            title = (query.replace(year, "")).strip()
        elif file is not None:
            year = re.findall(r'[1-2]\d{3}', file, re.IGNORECASE)
            if year:
                year = list_to_str(year[:1]) 
        else:
            year = None
        movieid = imdbb.search_movie(title.lower(), results=10)
        if not movieid:
            return None
        if year:
            filtered=list(filter(lambda k: str(k.get('year')) == str(year), movieid))
            if not filtered:
                filtered = movieid
        else:
            filtered = movieid
        movieid=list(filter(lambda k: k.get('kind') in ['movie', 'tv series'], filtered))
        if not movieid:
            movieid = filtered
        if bulk:
            return movieid
        movieid = movieid[0].movieID
    else:
        movieid = int(query)
    movie = imdbb.get_movie(movieid)
    if movie.get("original air date"):
        date = movie["original air date"]
    elif movie.get("year"):
        date = movie.get("year")
    else:
        date = "N/A"
    
    return {
        'title': movie.get('title'),
        'votes': movie.get('votes'),
        "aka": list_to_str(movie.get("akas")),
        "seasons": movie.get("number of seasons"),
        "box_office": movie.get('box office'),
        'localized_title': movie.get('localized title'),
        'kind': movie.get("kind"),
        "imdb_id": f"tt{movie.get('imdbID')}",
        "cast": list_to_str(movie.get("cast")),
        "runtime": list_to_str(movie.get("runtimes")),
        "countries": list_to_str(movie.get("countries")),
        "certificates": list_to_str(movie.get("certificates")),
        "languages": list_to_str(movie.get("languages")),
        'release_date': date,
        'year': movie.get('year'),
        'genres': list_to_str(movie.get("genres")),
        'poster': movie.get('full-size cover url'),
        'rating': str(movie.get("rating")),
        'url':f'https://www.imdb.com/title/tt{movieid}'
    }
async def get_all(list):
    for y in list:
        v=y.get("Title").lower().strip()
        poster = y.get("Poster")
        year=y.get("Year")[:4]
        id=y.get("imdbID")
        await save_poster(id, v, year, poster)

async def search_gagala(text):
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.100 Safari/537.36'
        }
    text = text.replace(" ", '+')
    url = f'https://www.google.com/search?q={text}'
    response = requests.get(url, headers=usr_agent)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all( 'h3' )
    return [title.getText() for title in titles]

def list_to_str(k):
    if not k:
        return "N/A"
    elif len(k) == 1:
        return str(k[0])
    else:
        return "#".join(f'{elem}, ' for elem in k)

def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return base64.urlsafe_b64encode(r).decode().rstrip("=")


def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")


def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref

