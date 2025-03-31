import os
from dotenv import load_dotenv
load_dotenv()

from .database import Database


db = Database(os.getenv("DB"))


async def is_admin(chat_id):
    ids = await db.get_all_chat_id()
    admin_ids = []
    for id in ids:
        admin_ids.append(id['chat_id'])

    if chat_id in admin_ids:
        return True
    return False

