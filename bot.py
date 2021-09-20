from pyrogram import Client, filters
import os
import asyncio
from traceback import print_exc
from subprocess import PIPE
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
    filename = f'{message.from_user.id}_{time()}.mp4'
    proc = await asyncio.create_subprocess_shell(
        f'ffmpeg -i {link} -c copy -bsf:a aac_adtstoasc {filename}',
        stdout=PIPE,
        stderr=PIPE
    )
    await _info.edit('bekle mp4 çeviriyom')
    out, err = await proc.communicate()
    await _info.edit('çevirdik')
    print('\n\n\n', out, err, sep='\n')
    if proc.returncode != 0:
        await _info.edit('yüklüyom telegrama')
        async def progress(current, total):
            await _info.edit(f'yüklüyom telegrama\n{current}/{total}')
        await client.send_video(message.chat.id, filename, progress=progress)
    else:
        return await _info.edit('sıçtı knk')

    
