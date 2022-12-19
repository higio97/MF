import asyncio

from pyrogram import Client
from pyrogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
)
from pyrogram.errors import (
    FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
)
from plugins import Database

async def broadcast_handler(client: Client, msg: Message):
    if msg.reply_to_message != None:
        anu = msg.reply_to_message
        anu = await anu.copy(msg.chat.id, reply_to_message_id=anu.id)
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Ya', 'Ya_Confirm'), InlineKeyboardButton('Tidak', 'Tidak_Confirm')]
        ])
        await anu.reply('Apakah Kamu Akan Mengirimkan Pesan Broadcast ?', True, reply_markup=markup)
    else:
        await msg.reply('Harap Reply Sebuah Pesan', True)

async def broadcast_ya(client: Client, query: CallbackQuery):
    msg = query.message
    db = Database(msg.from_user.id)
    if not msg.reply_to_message:
        await query.answer('Pesan Tidak Ditemukan', True)
        await query.message.delete()
        return
    message = msg.reply_to_message
    user_ids = db.get_pelanggan().id_pelanggan
    
    berhasil = 0
    dihapus = 0
    blokir = 0
    gagal = 0
    await msg.edit('Broadcast Sedang Berlangsung, Tunggu Sebentar', reply_markup = None)
    for user_id in user_ids:
        try:
            await message.copy(user_id)
            berhasil += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await message.copy(user_id)
            berhasil += 1
        except UserIsBlocked:
            blokir += 1
        except PeerIdInvalid:
            gagal += 1
        except InputUserDeactivated:
            dihapus += 1
            await db.hapus_pelanggan(user_id)
    text = f"""<b>Broadcast Selesai</b>
    
Jumlah pengguna: {str(len(user_ids))}
Berhasil Terkirim: {str(berhasil)}
Pengguna Diblokir: {str(blokir)}
Akun Yang Dihapus: {str(dihapus)} (<i>Telah Dihapus Dari Database</i>)
Gagal Terkirim: {str(gagal)}"""

    await msg.reply(text)
    await msg.delete()
    await message.delete()

async def close_cbb(client: Client, query: CallbackQuery):
    try:
        await query.message.reply_to_message.delete()
    except:
        pass
    try:
        await query.message.delete()
    except:
        pass
