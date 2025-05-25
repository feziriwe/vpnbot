import aiosqlite
from datetime import datetime, timedelta
from services.outline_api import create_key, delete_key

DB_PATH = "vpn_bot.db"

async def create_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, trial_used INTEGER)")
        await db.execute("CREATE TABLE IF NOT EXISTS keys (user_id INTEGER, key_id TEXT, url TEXT, expires_at TEXT)")
        await db.commit()

async def add_user(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, trial_used) VALUES (?, 0)", (user_id,))
        await db.commit()

async def has_trial(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT trial_used FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return row and row[0] == 1

async def add_trial(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET trial_used = 1 WHERE user_id = ?", (user_id,))
        await db.commit()

async def create_access_key(user_id, days):
    url, key_id = create_key()
    expires_at = (datetime.utcnow() + timedelta(days=days)).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO keys (user_id, key_id, url, expires_at) VALUES (?, ?, ?, ?)",
                         (user_id, key_id, url, expires_at))
        await db.commit()
    return url

async def get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM users")
        return await cursor.fetchall()

async def get_expired_keys():
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT key_id FROM keys WHERE expires_at <= ?", (now,))
        return await cursor.fetchall()

async def delete_expired_keys():
    expired = await get_expired_keys()
    async with aiosqlite.connect(DB_PATH) as db:
        for (key_id,) in expired:
            delete_key(key_id)
            await db.execute("DELETE FROM keys WHERE key_id = ?", (key_id,))
        await db.commit()