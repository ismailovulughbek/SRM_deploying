import os
from dotenv import load_dotenv
load_dotenv()

from .database import Database
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

db = Database(os.getenv("DB"))

async def get_admins(update, context):
    user = update.message.from_user
    data = await db.get_users()
    if data:
        for admin in data:
            del_btn = [
                [
                    InlineKeyboardButton(
                        text='🗑️ DELETE',
                        callback_data=f"del_{admin['chat_id']}",
                    )
                ]
            ]
            reply_markup = InlineKeyboardMarkup(del_btn)
            text = (
                "📩 <b>ADMIN!</b>\n\n"
                f"👤 <b>Ф.И.О:</b> {admin['full_name']}\n"
                f"📝 <b>username:</b> {admin['username']}\n\n"
                f"ID <b>CHAT ID:</b> {admin['chat_id']}"
            )

            await update.message.reply_text(
                text=text,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
#
    else:
        await update.message.reply_text(text="ADMINS not found")


async def delete_admin(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    data_sp = str(query.data).split('_')
    print(data_sp)

    if user.id != int(data_sp[1]):
        await db.delete_user(int(data_sp[1]))
        await query.edit_message_text(
            text="✅ Успешно удалено!",
            reply_markup=None
        )
    elif user.id == int(data_sp[1]):
        await query.edit_message_text(
            text="⚠️ Вы не можете удалить себя!",
            reply_markup=None
        )



