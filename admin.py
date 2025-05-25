from aiogram import Router, F
from aiogram.types import Message
from database.db import get_all_users

router = Router()

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id != 555786443:  # Замените на ваш Telegram ID
        return
    users = await get_all_users()
    await message.answer(f"👥 Всего пользователей: {len(users)}")