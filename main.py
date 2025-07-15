import asyncio
import aiogram
from aiogram.types import FSInputFile, InputFileUnion, InputMediaVideo
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from aiogram import types
from yandex_music import Client
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

def timestamp():
    return int(time.time() * 1000)

@dp.message(Command("search"))
async def music_cmd(message = types.Message):
    textmess = message.text[5:]
    search_result = client.search(textmess)
    wereArtist = 0
    type_ = search_result.best.type
    if type_ == "artist":
        artist_id = search_result.best.result.id
        music_needed = client.artists_tracks(artist_id, 0, 1)
        music_name = music_needed.tracks
        music_title = music_name[0]['title']
        wereArtist = 1
    try:
        if(wereArtist):
            first = client.search(music_title)['best']['result']
            name = music_title + ', ' + search_result.best.result.name
        else:
            first = search_result['best']['result']
            name = search_result.best.result.title + ', ' + search_result.best.result.artists[0]['name']
        print(message.chat.id, message.from_user.id, message.text)
        name = name + ".mp3"
        file = FSInputFile(name)
        first.download(name)
        await message.reply_audio(file)
        os.remove(name)
    except:
        await message.reply("что-то пошло не так")

@dp.message()
async def notcmd(message = types.Message):
    if str(message.text).upper().startswith("ПЕСНЯ") or str(message.text).upper().startswith("НАЙТИ"):     
        textmess = message.text[5:]
        search_result = client.search(textmess)
        wereArtist = 0
        type_ = search_result.best.type
        if type_ == "artist":
            artist_id = search_result.best.result.id
            music_needed = client.artists_tracks(artist_id, 0, 1)
            music_name = music_needed.tracks
            music_title = music_name[0]['title']
            wereArtist = 1
        try:
            if(wereArtist):
                first = client.search(music_title)['best']['result']
                name = music_title + ', ' + search_result.best.result.name
            else:
                first = search_result['best']['result']
                name = search_result.best.result.title + ', ' + search_result.best.result.artists[0]['name']
            print(message.chat.id, message.from_user.id, message.text)
            name = name + ".mp3"
            file = FSInputFile(name)
            first.download(name)
            await message.reply_audio(file)
            os.remove(name)
        except:
            await message.reply("что-то пошло не так")
    elif str(message.text).upper().startswith("ЮТ"):
        try:
            textmess = message.text[2:]
            await message.reply("начинаю")
            name = str(timestamp()) + ".mp4"
            real_full_name = str(Path.cwd()) + '\\' + name
            params = { 
                'outtmpl' : real_full_name,
                'merge_output_format': 'mp4'
            }
            yt_dlp.YoutubeDL(params).download([textmess])
            file = FSInputFile(name)
            await bot.send_video(str(message.chat.id), file)
        except:
            await message.reply("что-то пошло не так")
        finally:
            os.remove(name)
    elif str(message.text).upper().startswith("МУЗ"):
        try:
            textmess = message.text[2:]
            await message.reply("начинаю")
            name = str(timestamp()) + ".mp3 "
            real_full_name = str(Path.cwd()) + '\\' + name
            params = { 
                'outtmpl' : real_full_name,
                'merge_output_format': 'mp3',
            }
            yt_dlp.YoutubeDL(params).download([textmess])
            file = FSInputFile(name)
            await bot.send_video(str(message.chat.id), file)
        except:
            await message.reply("что-то пошло не так")
        finally:
            os.remove(name)
            


async def main():
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
