import config

from pyrogram import Client, types, enums
from plugins import Helper, Database

async def start_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    first = msg.from_user.first_name
    last = msg.from_user.last_name
    fullname = first if not last else first + ' ' + last
    username = '@AlterFWBBot' if not msg.from_user.username else '@' + msg.from_user.username
    mention = msg.from_user.mention
    await msg.reply_text(
        text = config.start_msg.format(
            id = msg.from_user.id,
            mention = mention,
            username = username,
            first_name = await helper.escapeHTML(first),
            last_name = await helper.escapeHTML(last),
            fullname = await helper.escapeHTML(fullname),
            ),
        disable_web_page_preview = True,
        quote = True
    )

async def status_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    db = Database(msg.from_user.id).get_data_pelanggan()
    pesan = '<b>🏷Info User</b>\n'
    pesan += f'├ID : <code>{db.id}</code>\n'
    pesan += f'├Nama : {db.mention}\n'
    pesan += f'└Status : {db.status}\n\n'
    pesan += '<b>📝Lainnya</b>\n'
    pesan += f'├Coin : {helper.formatrupiah(db.coin)}💰\n'
    pesan += f'├MenFess : {db.menfess}/{config.batas_kirim}\n'
    pesan += f'├Semua MenFess : {db.all_menfess}\n'
    pesan += f'└Bergabung : {db.sign_up}'
    await msg.reply(pesan, True, enums.ParseMode.HTML)

async def statistik_handler(client: Helper, id_bot: int):
    db = Database(client.user_id)
    bot = db.get_data_bot(id_bot)
    pesan = "<b>📊 STATISTIK BOT\n\n"
    pesan += f"▪️Pelanggan: {db.get_pelanggan().total_pelanggan}\n"
    pesan += f"▪️Admin: {len(bot.admin)}\n"
    pesan += f"▪️Talent: {len(bot.talent)}\n"
    pesan += f"▪️Daddy sugar: {len(bot.daddy_sugar)}\n"
    pesan += f"▪️Moans girl: {len(bot.moansgirl)}\n"
    pesan += f"▪️Moans boy: {len(bot.moansboy)}\n"
    pesan += f"▪️Girlfriend rent: {len(bot.gfrent)}\n"
    pesan += f"▪️Boyfriend rent: {len(bot.bfrent)}\n"
    pesan += f"▪️Banned: {len(bot.ban)}\n\n"
    pesan += f"🔰Status bot: {'AKTIF' if bot.bot_status else 'TIDAK AKTIF'}</b>"
    await client.message.reply_text(pesan, True, enums.ParseMode.HTML)

async def list_admin_handler(helper: Helper, id_bot: int):
    db = Database(helper.user_id).get_data_bot(id_bot)
    pesan = "<b>Owner bot</b>\n"
    pesan += "• ID: " + str(config.id_admin) + " | <a href='tg://user?id=" + str(config.id_admin) + "'>Owner bot</a>\n\n"
    if len(db.admin) > 0:
        pesan += "<b>Daftar Admin bot</b>\n"
        ind = 1
        for i in db.admin:
            pesan += "• ID: " + str(i) + " | <a href='tg://user?id=" + str(i) + "'>Admin " + str(ind) + "</a>\n"
            ind += 1
    await helper.message.reply_text(pesan, True, enums.ParseMode.HTML)

async def list_ban_handler(helper: Helper, id_bot: int):
    db = Database(helper.user_id).get_data_bot(id_bot)
    if len(db.ban) == 0:
        return await helper.message.reply_text('<i>Tidak Ada User Dibanned Saat Ini</i>', True, enums.ParseMode.HTML)
    else:
        pesan = "<b>Daftar Banned</b>\n"
        ind = 1
        for i in db.ban:
            pesan += "• ID: " + str(i) + " | <a href='tg://openmessage?user_id=" + str(i) + "'>( " + str(ind) + " )</a>\n"
            ind += 1
    await helper.message.reply_text(pesan, True, enums.ParseMode.HTML)

async def gagal_kirim_handler(client: Client, msg: types.Message):
    anu = Helper(client, msg)
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    fullname = first_name if not last_name else first_name + ' ' + last_name
    username = '@AlterFWBBot' if not msg.from_user.username else '@' + msg.from_user.username
    mention = msg.from_user.mention
    return await msg.reply(config.gagalkirim_msg.format(
        id = msg.from_user.id,
        mention = mention,
        username = username,
        first_name = await anu.escapeHTML(first_name),
        last_name = await anu.escapeHTML(last_name),
        fullname = await anu.escapeHTML(fullname)
    ), True, enums.ParseMode.HTML, disable_web_page_preview=True)

async def help_handler(client, msg):
    db = Database(msg.from_user.id)
    member = db.get_data_pelanggan()
    pesan = "Supported Commands\n"
    pesan += '/status — Melihat Status\n'
    pesan += '/talent — Melihat Talent\n'
    if member.status == 'admin':
        pesan += '\nHanya Admin\n'
        pesan += '/tf_dm — Transfer Diamond\n'
        pesan += '/settings — Melihat Settingan Bot\n'
        pesan += '/list_admin — Melihat List Admin\n'
        pesan += '/list_ban — Melihat List Banned\n\n'
        pesan += 'Perintah Banned\n'
        pesan += '/ban — Ban User\n'
        pesan += '/unban — Unban User\n'
    if member.status == 'owner':
        pesan += '\n=====OWNER COMMAND=====\n'
        pesan += '/tf_dm — Transfer Diamond\n'
        pesan += '/settings — Melihat Settingan Bot\n'
        pesan += '/list_admin — Melihat List Admin\n'
        pesan += '/list_ban — Melihat List Banned\n'
        pesan += '/stats — Melihat Statistik Bot\n'
        pesan += '/bot — setbot (on|off)\n'
        pesan += '\n=====FITUR TALENT=====\n'
        pesan += '/addtalent — Menambahkan Talent Baru\n'
        pesan += '/addsugar — Menambahkan Talent Daddy Sugar\n'
        pesan += '/addgirl — Menambahkan Talent Moans Girl\n'
        pesan += '/addboy — Menambahkan Talent Moans Boy\n'
        pesan += '/addgf — Menambahkan Talent Girlfriend Rent\n'
        pesan += '/addbf — Menambahkan Talent Boyfriend Rent\n'
        pesan += '/hapus — Menghapus Talent\n'
        pesan += '\n=====BROADCAST OWNER=====\n'
        pesan += '/broadcast — mengirim Pesan Broadcast Kesemua User\n'
        pesan += '/admin — Menambahkan Admin Baru\n'
        pesan += '/unadmin — Menghapus Admin\n'
        pesan += '/list_ban — Melihat List Banned\n'
        pesan += '\n=====BANNED COMMAND=====\n'
        pesan += '/ban — Ban User\n'
        pesan += '/unban — Unban User\n'
    await msg.reply(pesan, True)
