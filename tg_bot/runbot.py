import os
from dotenv import load_dotenv
load_dotenv()

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler, \
    CallbackQueryHandler
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, BotCommand, ReplyKeyboardRemove
from .register import is_admin
from .message import add_admin, text_handler
from .btns import ADD_ADMIN_BTN, SHOW_ADMIN_BTN, REQUEST_BTN
from .database import Database
from .admins import delete_admin

db = Database(os.getenv("DB"))
ADD_ADMIN = range(1)

async def start_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="info", description="Информация о боте")
    ]
    await context.bot.set_my_commands(commands=commands)
    user_id = update.effective_user.id
    if await is_admin(user_id):
        buttons = [
            [
                KeyboardButton(text=ADD_ADMIN_BTN),
                KeyboardButton(text=SHOW_ADMIN_BTN)
            ],
        ]
        await update.message.reply_text(
            text=f"✅ <b>{update.message.from_user.full_name}</b>, у вас есть права администратора! 🔹",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True,
            ),
            parse_mode='HTML'
        )

        return ConversationHandler.END
    else:
        buttons = [
            [
                KeyboardButton(text=REQUEST_BTN)
            ]
        ]
        await update.message.reply_text(
            text="⚠️ Вы не администратор! Чтобы получить права администратора, вы можете отправить запрос.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True,
            ),
            parse_mode='HTML'
        )

        return ConversationHandler.END


async def info_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=(
        "<b>Silk Road Multilingual</b>\n\n"
        "🔹 В этом боте администраторы могут просматривать сообщения, отправленные пользователями. /start"
    ), parse_mode="HTML")

    return ConversationHandler.END


def main_bot():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    print(f'Ushbu tokenda bot ishga tushdi {os.getenv("BOT_TOKEN")}')

    register_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)],
        states={
            ADD_ADMIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_admin)],
        },
        fallbacks=[
            CommandHandler("start", start_handler),
            CommandHandler("info", info_handler)
        ]
    )

    app.add_handler(register_conv_handler)
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("info", info_handler))

    # CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(delete_admin, pattern='^del_'))

    app.run_polling()
