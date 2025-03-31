import aiosqlite

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    async def connect(self):
        if self.conn is None:
            self.conn = await aiosqlite.connect(self.db_name)
            await self.conn.execute('PRAGMA foreign_keys = ON;')
            self.conn.row_factory = aiosqlite.Row

    # USER==============================================================

    async def create_user(self, full_name, username, chat_id):
        await self.connect()
        async with self.conn.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO admins (full_name, username, chat_id)
                VALUES (?,?,?) 
            """, (full_name, username, chat_id))
            await self.conn.commit()

    async def get_users(self):
        await self.connect()
        async with self.conn.cursor() as cursor:
            await cursor.execute("""SELECT * FROM admins""")

            return await dict_fetchall(cursor)

    async def get_user_by_chat_id(self, chat_id):
        await self.connect()
        async with self.conn.cursor() as cursor:
            await cursor.execute("""SELECT * FROM admins WHERE chat_id = ?""", (chat_id,))

            return await dict_fetchone(cursor)

    async def get_all_chat_id(self):
        await self.connect()
        async with self.conn.cursor() as cursor:
            await cursor.execute("""SELECT chat_id FROM admins""")

            return await dict_fetchall(cursor)


    async def get_users_count(self):
        await self.connect()
        async with self.conn.cursor() as cursor:
            await cursor.execute("""SELECT COUNT(*) FROM admins""")

            return await dict_fetchone(cursor)

    async def delete_user(self, chat_id: int):
        await self.connect()
        async with self.conn.cursor() as cursor:
            await cursor.execute("DELETE FROM admins WHERE chat_id = ?", (chat_id,))
            await self.conn.commit()

    # USER END =========================================================================

    async def close(self):
        if self.conn:
            await self.conn.close()


async def dict_fetchone(cursor):
    row = await cursor.fetchone()
    desc = cursor.description

    if row is None:
        return False
    columns = [col[0] for col in desc]

    return dict(zip(columns, row))


async def dict_fetchall(cursor):
    desc = cursor.description
    fetchall = await cursor.fetchall()
    columns = [col[0] for col in desc]
    return [
        dict(zip(columns, row))
        for row in fetchall
    ]
