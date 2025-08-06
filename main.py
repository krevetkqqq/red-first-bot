import asyncio
from typing import Optional
import aiogram
from aiogram.types import FSInputFile
from dotenv import load_dotenv
import os
from aiogram import types, F
from yandex_music import Client, Search
import yt_dlp
import time
from pathlib import Path

load_dotenv()
token = os.getenv('token')
token_music = os.getenv('token_music')
client = Client(token_music).init()
bot = aiogram.Bot(token)
dp = aiogram.Dispatcher()
router = aiogram.Router()

global_search_result: Optional[Search] = None

def timestamp():
    return int(time.time() * 1000)

@dp.message(F.text.lower().startswith("песня"))
async def song(message):
    global global_search_result
    # if str(message.text).upper().startswith("ПЕСНЯ") or str(message.text).upper().startswith("НАЙТИ") or str(message.text).upper().startswith("АЛЬБОМ"):    
    if True:
        newtext = str(message.text).split()
        textmess = ' '.join(newtext[1:]) if len(newtext) > 1 else ""
        search_result = client.search(textmess)
        wereArtist = 0
        wereAlbum = 0
        type_ = search_result.best.type
        if type_ == "artist":
            artist_id = search_result.best.result.id
            music_needed = client.artists_tracks(artist_id, 0, 1)
            music_name = music_needed.tracks
            music_title = music_name[0]['title']
            wereArtist = 1
        if type_ == "album":
            wereAlbum = 1
        if True:
            if(wereArtist):
                first = client.search(music_title)['best']['result']
                name = music_title + ', ' + search_result.best.result.name
            elif(wereAlbum):
                # first = search_result["tracks"]["results"][0]
                # name = search_result["tracks"]["results"][0]["title"] + ',' + search_result["tracks"]["results"][0]["artists"][0]["name"]
                for index, track in enumerate(search_result["tracks"]["results"]):
                    await message.reply(str(index) + ", "+ track["artists"][0]["name"] + ", " + track["title"])
                global_search_result = search_result
                return
            else:
                first = search_result['best']['result']
                name = search_result.best.result.title + ', ' + search_result.best.result.artists[0]['name']
            print(message.chat.id, timestamp(), message.text)
            name = name + ".mp3"
            name = name.replace("/"," или ")
            char_to_replace = "\\:?\"<>|*"
            for i in char_to_replace:
                name = name.replace(i,"")
            first.download(name)
            file = FSInputFile(name)
            await message.reply_audio(file)
            os.remove(name)
        # except:
        #     await message.reply("что-то пошло не так")

@dp.message(F.text.lower().startswith("альбом"))
async def album(message):
    await song(message)

@dp.message(F.text.lower().startswith("ют"))
async def YT(message):
        try:
            textmess = message.text[2:]
            await message.reply("начинаю")
            name = str(timestamp()) + ".mp4"
            real_full_name = str(Path.cwd()) + '\\' + name
            params = { 
                'outtmpl' : real_full_name,
                'merge_output_format': 'mp4',
                'cookies_from_browser':'firefox'
            }
            yt_dlp.YoutubeDL(params).download([textmess])
            file = FSInputFile(name)
            await bot.send_video(str(message.chat.id), file)
        except:
            await message.reply("что-то пошло не так")
        finally:
            os.remove(name)

@dp.message()
async def TryParseNum(message):
        if True:
            id = int(message.text)
            first = global_search_result["tracks"]["results"][id]
            name = global_search_result["tracks"]["results"][id]["title"] + ', ' + global_search_result["tracks"]["results"][id]["artists"][0]["name"]
            name = name + ".mp3"
            file = FSInputFile(name)
            first.download(name)
            await message.reply_audio(file)
            os.remove(name)
        # except:
        #     await message.reply("что-то пошло не так")


    
async def main():
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
