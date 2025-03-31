import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
from telegram import Bot
from tg_bot import Database
from log_config import get_logger

logger = get_logger(__name__)


class AsyncDatabase(Database):
    async def get_all_chat_id(self):
        return await super().get_all_chat_id()

db = AsyncDatabase(os.getenv("DB"))
bot = Bot(token=os.getenv("BOT_TOKEN"))

async def send_message_to_telegram(data, req_type):
    logger.info("Send_message_to_telegram Start--->(UI)")
    admin_ids = await db.get_all_chat_id()

    message_template = (
        "\U0001F4E9 *Новое сообщение!*\n\n"
        "👤 *Имя:* {name}\n"
        "📧 *Email:* {email}\n"
        "📞 *Телефон:* {phone}\n"
    )

    if req_type == "contact":
        message = message_template.format(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone")
        ) + f"✉️ *Сообщение:* {data.get('message')}\n"
    else:
        message = message_template.format(
            name=data.get("full_name"),
            email=data.get("email"),
            phone=data.get("phone")
        ) + f"💼 *Тип услуги:* {data.get('service')}\n"

    for admin in admin_ids:
        try:
            await bot.send_message(chat_id=admin['chat_id'], text=message, parse_mode="Markdown")
            logger.info(f"SEND {admin['chat_id']} Message sent--->(UI)")

        except Exception as e:
            await db.delete_user(admin['chat_id'])
            logger.exception(f"ERROR! {admin['chat_id']} Message not sent--->(UI)")
            logger.exception(f"DELETED! {admin['chat_id']} Admin deleted--->(UI)")

    logger.info("Send_message_to_telegram End--->(UI)")
