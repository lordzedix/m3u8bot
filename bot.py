from pyrogram import Client, filters
import os
import asyncio
from traceback import print_exc
from subprocess import PIPE, STDOUT
from time import time

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']

app = Client('mkv', api_id, api_hash, bot_token=bot_token)

@app.on_message(filters.command('start'))
async def start(_, message):
    await message.reply(f'''Kullanım: `/convert m3u8_link||dosya_ismi`
Admin: [Click to go.](https://t.me/lordzedix)
''')

@app.on_message(filters.command(['convert', 'cevir']))
async def convert(client, message):
    try:
        args = message.text.split(' ', 1)[1]
        link = args.split('||')[0].replace(' ', '')
        filename = args.split('||')[1].replace(' ', '')
    except:
        print_exc()
        return await message.reply(f'''Kullanım: `/convert m3u8_link||dosya_ismi`
Admin : [Click to go.](https://t.me/lordzedix)
''')
    _info = await message.reply('Lütfen bekleyin...')
    
    proc = await asyncio.create_subprocess_shell(
        f'ffmpeg -i {link} -c copy -vf scale=-1:720 -bsf:a aac_adtstoasc {filename}.mp4',
        stdout=PIPE,
        stderr=PIPE
    )
    await _info.edit("Dosya mp4'e çevriliyor...")
    out, err = await proc.communicate()
    await _info.edit('Dosya başarıyla çevrildi.')
    print('\n\n\n', out, err, sep='\n')
    try: 
        await _info.edit('Thumbnail ekleniyor...')
        proc2 = await asyncio.create_subprocess_shell(
            f'ffmpeg -i {filename}.mp4 -ss 00:03:00.000 -vframes 5 {filename}.jpg',
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

        await _info.edit("Dosya Telegram'a yükleniyor...")
        def progress(current, total):
            print(message.from_user.first_name, ' -> ', current, '/', total, sep='')
        await client.send_video(message.chat.id, f'{filename}.mp4', duration=int(float(duration.decode())), thumb=f'{filename}.jpg', file_name=f'{filename}.mp4', progress=progress)
        os.remove(f'{filename}.mp4')
        os.remove(f'{IMG_20211110_010456_911.png}')
    except:
        print_exc()
        return await _info.edit('`Bir hata oluştu.`')


app.run()
