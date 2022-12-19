import config
import re

from pyrogram import Client, types, enums
from plugins import Database, Helper

async def send_with_pic_handler(client: Client, msg: types.Message, key: str, hastag: list):
    db = Database(msg.from_user.id)
    helper = Helper(client, msg)
    user = db.get_data_pelanggan()
    if msg.text or msg.photo or msg.video or msg.voice:
        menfess = user.menfess
        all_menfess = user.all_menfess
        dm = user.dm
        if menfess >= config.batas_kirim:
            if user.status == 'member' or user.status == 'talent':
                if dm >= config.biaya_kirim:
                    dm = user.dm - config.biaya_kirim
                else:
                    return await msg.reply(f'🙅🏻‍♀️ Post Gagal Terkirim. Kamu Hari Ini Telah Mengirim Pesan Sebanyak {menfess}/{config.batas_kirim} Kali. Serta Diamond Mu Kurang Untuk Mengirim Pesan Diluar Batas Harian., Kamu Dapat Mengirim Pesan Kembali Pada Hari Besok.\n\n Waktu Reset Jam 1 Pagi', quote=True)

        if key == hastag[0]:
            picture = config.pic_girl
        elif key == hastag[1]:
            picture = config.pic_boy
        
        link = await get_link()
        caption = msg.text or msg.caption
        entities = msg.entities or msg.caption_entities

        kirim = await client.send_photo(config.channel_1, picture, caption, caption_entities=entities)
        await helper.send_to_channel_log(type="log_channel", link=link + str(kirim.id))
        await db.update_menfess(cdm, menfess, all_menfess)
        await msg.reply(f"Pesan Telah Berhasil Terkirim. Hari Ini Kamu Telah Mengirim Pesan Sebanyak {menfess + 1}/{config.batas_kirim} . Kamu Dapat Mengirim Pesan Sebanyak {config.batas_kirim} Kali Dalam Sehari\n\nWaktu Reset Setiap Jam 1 Pagi\n<a href='{link + str(kirim.id)}'>Check Pesan Kamu</a>")
    else:
        await msg.reply('Media Yang Didukung Photo, Video Dan Voice')

async def send_menfess_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    db = Database(msg.from_user.id)
    db_user = db.get_data_pelanggan()
    db_bot = db.get_data_bot(client.id_bot).kirimchannel
    if msg.text or msg.photo or msg.video or msg.voice:
        if msg.photo and not db_bot.photo:
            if db_user.status == 'member' or db_user.status == 'talent':
                return await msg.reply('Tidak bisa mengirim photo, karena sedang dinonaktifkan oleh admin', True)
        elif msg.video and not db_bot.video:
            if db_user.status == 'member' or db_user.status == 'talent':
                return await msg.reply('Tidak bisa mengirim video, karena sedang dinonaktifkan oleh admin', True)
        elif msg.voice and not db_bot.voice:
            if db_user.status == 'member' or db_user.status == 'talent':
                return await msg.reply('Tidak bisa mengirim voice, karena sedang dinonaktifkan oleh admin', True)

        menfess = db_user.menfess
        all_menfess = db_user.all_menfess
        dm = db_user.dm
        if menfess >= config.batas_kirim:
            if db_user.status == 'member' or db_user.status == 'talent':
                if dm >= config.biaya_kirim:
                    dm = db_user.dm - config.biaya_kirim
                else:
                    return await msg.reply(f'🙅🏻‍♀️ Post Gagal Terkirim. Kamu Hari Ini Telah Mengirim Ke Pesan Sebanyak {menfess}/{config.batas_kirim} Kali. Serta Diamond Mu Kurang Untuk Mengirim Pesan Diluar Batas Harian., Kamu Dapat Mengirim Pesan Kembali Pada Hari Besok.\n\nWaktu Reset Jam 1 Pagi', quote=True)

        link = await get_link()
        kirim = await client.copy_message(config.channel_1, msg.from_user.id, msg.id)
        await helper.send_to_channel_log(type="log_channel", link=link + str(kirim.id))
        await db.update_menfess(dm, menfess, all_menfess)
        await msg.reply(f"Pesan Telah Berhasil Terkirim. Hari Ini Kamu Telah Mengirim Pesan Sebanyak {menfess + 1}/{config.batas_kirim} . Kamu Dapat Mengirim Pesan Sebanyak {config.batas_kirim} Kali Dalam Sehari\n\nWaktu Reset Setiap Jam 1 Pagi\n<a href='{link + str(kirim.id)}'>Check Pesan Kamu</a>")
    else:
        await msg.reply('media yang didukung photo, video dan voice')

async def get_link():
    anu = str(config.channel_1).split('-100')[1]
    return f"https://t.me/c/{anu}/"

async def transfer_dm_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]tf_dm(\s|\n)*$", msg.text or msg.caption):
        err = "<i>Perintah Salah /tf_dm [jmlh_dm]</i>" if msg.reply_to_message else "<i>Perintah Salah /tf_dm [id_user] [jmlh_dm]</i>"
        return await msg.reply(err, True)
    helper = Helper(client, msg)
    if re.search(r"^[\/]tf_dm\s(\d+)(\s(\d+))?", msg.text or msg.caption):
        x = re.search(r"^[\/]tf_dm\s(\d+)(\s(\d+))$", msg.text or msg.caption)
        if x:
            target = x.group(1)
            dm = x.group(3)
        y = re.search(r"^[\/]tf_dm\s(\d+)$", msg.text or msg.caption)
        if y:
            if msg.reply_to_message:
                if msg.reply_to_message.from_user.is_bot == True:
                    return await msg.reply('🤖Bot Tidak Dapat Ditranfer dm', True)
                elif msg.reply_to_message.sender_chat:
                    return await msg.reply('Channel Tidak Dapat Ditranfer dm', True)
                else:
                    target = msg.reply_to_message.from_user.id
                    dm = y.group(1)
            else:
                return await msg.reply('sambil mereply sebuah pesan', True)
        
        if msg.from_user.id == int(target):
            return await msg.reply('<i>Tidak Dapat Transfer Diamond Untuk Diri Sendiri</i>', True)

        user_db = Database(msg.from_user.id)
        anu = user_db.get_data_pelanggan()
        my_dm = anu.dm
        if my_dm >= int(dm):
            db_target = Database(int(target))
            if await db_target.cek_user_didatabase():
                target_db = db_target.get_data_pelanggan()
                ditransfer = my_dm - int(dm)
                diterima = target_db.dm + int(dm)
                nama = "Admin" if anu.status == 'owner' or anu.status == 'admin' else msg.from_user.first_name
                nama = await helper.escapeHTML(nama)
                try:
                    await client.send_message(target, f"Diamond Berhasil Ditambahkan Senilai {dm} Diamond, Cek /status\n└Oleh <a href='tg://user?id={msg.from_user.id}'>{nama}</a>")
                    await user_db.transfer_dm(ditransfer, diterima, target_db.dm_full, int(target))
                    await msg.reply(f'<i>Berhasil Transfer Diamond Sebesar {dm} Diamond 💎</i>', True)
                except Exception as e:
                    return await msg.reply_text(
                        text=f"❌<i>Terjadi Kesalahan, Sepertinya User Memblokir Bot</i>\n\n{e}", quote=True,
                        parse_mode=enums.ParseMode.HTML
                    )
            else:
                return await msg.reply_text(
                    text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            return await msg.reply(f'<i>Diamond Kamu ({my_dm}) Tidak Dapat Transfer Diamond.</i>', True)
