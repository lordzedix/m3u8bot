from pyrogram import Client, filters
import os
import asyncio
from traceback import print_exc
from subprocess import PIPE, STDOUT
from time import time

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']

app = Client('m3u8', api_id, api_hash, bot_token=bot_token)

@app.on_message(filters.command('start'))
async def start(_, message):
    await message.reply('kullanım: `/convert m3u8_link`')

@app.on_message(filters.command(['convert', 'cevir']))
async def convert(client, message):
    try:
        link = message.text.split(' ', 1)[1]
    except:
        print_exc()
        return await message.reply('kullanım: `/convert m3u8_link`')
    _info = await message.reply('bekle')
    filename = f'{message.from_user.id}_{int(time())}'
    proc = await asyncio.create_subprocess_shell(
        f'ffmpeg -i {link} -c copy -bsf:a aac_adtstoasc {filename}.mp4',
        stdout=PIPE,
        stderr=PIPE
    )
    await _info.edit('bekle mp4 çeviriyom')
    out, err = await proc.communicate()
    await _info.edit('çevirdik')
    print('\n\n\n', out, err, sep='\n')
    try: 
        await _info.edit('thumbnail çekiyom')
        proc2 = await asyncio.create_subprocess_shell(
            f'ffmpeg -i {filename}.mp4 -ss 00:00:00.000 -vframes 1 {filename}.jpg',
            stdout=PIPE,
            stderr=PIPE
        )
        await proc2.communicate()
        await _info.edit('duration çekiyom')
        proc3 = await asyncio.create_subprocess_shell(
            f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {filename}.mp4',
            stdout=PIPE,
            stderr=STDOUT
        )
        duration, _ = await proc3.communicate()
        await _info.edit('yüklüyom telegrama')
        def progress(current, total):
            print(message.from_user.first_name, ' -> ', current, '/', total, sep='')
        return await client.send_video(message.chat.id, f'{filename}.mp4', duration=int(str(duration)), thumb=f'{filename}.jpg', progress=progress)
    except:
        print_exc()
        return await _info.edit('sıçtı knk')


app.run()
