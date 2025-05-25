from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from database.db import add_user, has_trial, add_trial, create_access_key

router = Router()

# Главная клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔓 Получить триал (7 дней)")],
        [KeyboardButton(text="💳 Купить 7 дней")],
        [KeyboardButton(text="💳 Купить 30 дней")],
        [KeyboardButton(text="💳 Купить 90 дней")],
        [KeyboardButton(text="📞 Поддержка")]
    ],
    resize_keyboard=True
)

SUPPORT_USERNAME = "@your_support_username"  # Замени на свой @username

@router.message(F.text == "/start")
async def start_cmd(message: Message):
    await add_user(message.from_user.id)
    await message.answer("👋 Добро пожаловать! Выберите действие:", reply_markup=main_keyboard)

@router.message(F.text == "🔓 Получить триал (7 дней)")
async def trial_access(message: Message):
    user_id = message.from_user.id
    if await has_trial(user_id):
        await message.answer("❗️Вы уже использовали пробный доступ.")
        return
    key = await create_access_key(user_id, 7)
    await add_trial(user_id)
    await message.answer(
        f"🎁 Ваш пробный ключ:\n<code>{key}</code>\nСрок действия: 7 дней",
        parse_mode="HTML",
    )

@router.message(F.text.in_({"💳 Купить 7 дней", "💳 Купить 30 дней", "💳 Купить 90 дней"}))
async def buy_access(message: Message):
    user_id = message.from_user.id
    days = int(message.text.split()[2])
    key = await create_access_key(user_id, days)
    await message.answer(
        f"✅ Ваш ключ на {days} дней:\n<code>{key}</code>",
        parse_mode="HTML",
    )

@router.message(F.text == "📞 Поддержка")
async def support(message: Message):
    await message.answer("Связь с поддержкой: @fffyt5")

