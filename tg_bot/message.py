import os
from dotenv import load_dotenv
load_dotenv()

import re
from telegram import Update, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import BadRequest, Forbidden
from .btns import ADD_ADMIN_BTN, REQUEST_BTN, SHOW_ADMIN_BTN
from .database import Database
from .admins import get_admins
from .register import is_admin
from log_config import get_logger

logger = get_logger(__name__)

db = Database(os.getenv("DB"))

ADD_ADMIN = range(1)


def get_admin_buttons():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=ADD_ADMIN_BTN), KeyboardButton(text=SHOW_ADMIN_BTN)]],
        resize_keyboard=True,
    )


async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()

    if not re.match(r'^-?\d+$', message):
        await update.message.reply_text("⚠️ Это не Chat ID, так как это не число.", reply_markup=get_admin_buttons())
        return ConversationHandler.END

    chat_id = int(message)

    if await is_admin(chat_id):
        await update.message.reply_text("⚠️ Этому пользователю уже были предоставлены права администратора.",
                                        reply_markup=get_admin_buttons())
        return ConversationHandler.END

    try:
        chat = await context.bot.get_chat(chat_id)
        await db.create_user(chat.full_name, chat.username, chat_id)
        await update.message.reply_text(f"✅ Успешно добавлено!: {chat.full_name}", reply_markup=get_admin_buttons())
        logger.info("(add_admin) ADMIN created--->(UI)")
    except BadRequest:
        error_text = "⚠️ Этот Chat ID неверный или пользователь не запустил бота."
        await update.message.reply_text(text=error_text, reply_markup=get_admin_buttons())

    except Forbidden:
        error_text = "⚠️ Бот не имеет доступа к этому пользователю. Возможно, он его заблокировал."
        await update.message.reply_text(text=error_text, reply_markup=get_admin_buttons())

    except Exception as e:
        error_text = f"❌ Произошла ошибка: {str(e)}"
        await update.message.reply_text(text=error_text, reply_markup=get_admin_buttons())
        logger.exception(f"ERROR! (add_admin) ADMIN dont created --->(UI)")

    return ConversationHandler.END



async def send_admin_request(update, context, user):
    admin_ids = await db.get_all_chat_id()
    text = (
        f"🔹 <b>Запрос к администратору:</b>\n\n"
        f"👤 <b>Имя:</b> - {user.full_name}\n"
        f"📝 <b>username:</b> - {user.username}\n\n"
        f"🆔 <b>ID:</b> - <code>{user.id}</code>"
    )

    for admin in admin_ids:
        try:
            await context.bot.send_message(chat_id=admin['chat_id'], text=text, parse_mode='HTML')
            logger.exception(f" (send_admin_request): {admin['chat_id']} Message sended--->(UI)")
        except Exception as e:
            await db.delete_user(admin['chat_id'])
            logger.exception(f"ERROR! (send_admin_request): {admin['chat_id']} Message not sent--->(UI)")
            logger.exception(f"DELETED! (send_admin_request): {admin['chat_id']} Admin deleted--->(UI)")

    await update.message.reply_text(
        "✅ Ваш запрос отправлен! Если вас добавили в список администраторов, перезапустите бота с помощью команды /start.")




async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message = update.message.text
    db_user = await db.get_user_by_chat_id(user.id)

    if db_user:
        if message == ADD_ADMIN_BTN:
            await update.message.reply_text("Введите chat_id пользователя, который отправил вам запрос:",
                                            reply_markup=ReplyKeyboardRemove())
            return ADD_ADMIN
        elif message == SHOW_ADMIN_BTN:
            await get_admins(update, context)
            return ConversationHandler.END
        else:
            return ConversationHandler.END

    elif message == REQUEST_BTN:
        await send_admin_request(update, context, user)

    else:
        await update.message.reply_text(
            "Если вас добавили в список администраторов, перезапустите бота с помощью команды /start.")
        return ConversationHandler.END
