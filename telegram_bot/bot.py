import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import CommandStart

from config import BOT_TOKEN

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

VIDEO_ID = "BAACAgIAAxkBAAMNaYI2gJJKqexCGUP0H9Vo8zmqhhkAAi6aAAJPVRFIsZ_kPLsHfsc4BA"

VIDEOS = {
    "g_create": VIDEO_ID,
    "g_deposit": VIDEO_ID,
    "g_trade": VIDEO_ID,
    "g_withdraw": VIDEO_ID,
}

user_lang = {}

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # ─── KEYBOARDS ───────────────────────────

    lang_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
        ]
    ])

    main_menu_ru = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Гайды", callback_data="guide")],
        [InlineKeyboardButton(text="🌐 Наши ресурсы", callback_data="resources")],
        [InlineKeyboardButton(text="🌍 Сменить язык", callback_data="change_lang")],
    ])

    main_menu_en = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Guides", callback_data="guide")],
        [InlineKeyboardButton(text="🌐 Our resources", callback_data="resources")],
        [InlineKeyboardButton(text="🌍 Change language", callback_data="change_lang")],
    ])

    guide_menu_ru = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧾 Создание аккаунта", callback_data="g_create")],
        [InlineKeyboardButton(text="💳 Пополнение счёта", callback_data="g_deposit")],
        [InlineKeyboardButton(text="📈 Первый трейд", callback_data="g_trade")],
        [InlineKeyboardButton(text="💸 Вывод средств", callback_data="g_withdraw")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_main")],
    ])

    guide_menu_en = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧾 Create an account", callback_data="g_create")],
        [InlineKeyboardButton(text="💳 Fund your account", callback_data="g_deposit")],
        [InlineKeyboardButton(text="📈 First trade", callback_data="g_trade")],
        [InlineKeyboardButton(text="💸 Withdraw funds", callback_data="g_withdraw")],
        [InlineKeyboardButton(text="⬅️ Back to menu", callback_data="back_main")],
    ])

    back_to_guides = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back / Назад", callback_data="guide")]
    ])

    back_to_main = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back / Назад", callback_data="back_main")]
    ])

    # ─────────────────────────────────────────
    # HANDLERS
    # ─────────────────────────────────────────

    @dp.message(CommandStart())
    async def start_cmd(message: Message):
        await message.answer(
            "Добро пожаловать в официальный Preddy Guide Bot 👋\n\n"
            "Здесь собраны пошаговые видео-гайды и полезные ресурсы,\n"
            "которые помогут тебе быстро разобраться и начать работу.\n\n"
            "Пожалуйста, выбери язык гайда 👇\n\n"
            "— — — — — — — — — —\n\n"
            "Welcome to the official Preddy Guide Bot 👋\n\n"
            "Here you’ll find step-by-step video guides and useful resources\n"
            "to help you get started quickly and with confidence.\n\n"
            "Please choose your guide language 👇",
            reply_markup=lang_kb
        )

    @dp.callback_query(F.data.startswith("lang_"))
    async def set_language(callback: CallbackQuery):
        lang = callback.data.split("_")[1]
        user_lang[callback.from_user.id] = lang

        if lang == "ru":
            await callback.message.edit_text(
                "Добро пожаловать в гайд-бот Preddy 👋\n\n"
                "Здесь ты можешь:\n"
                "• посмотреть пошаговые видео-гайды\n"
                "• разобраться в основах торговли\n"
                "• найти все официальные ресурсы в одном месте\n\n"
                "Выбери нужный раздел ниже 👇",
                reply_markup=main_menu_ru
            )
        else:
            await callback.message.edit_text(
                "Welcome to the Preddy guide bot 👋\n\n"
                "Here you can:\n"
                "• watch step-by-step video guides\n"
                "• understand the basics of trading\n"
                "• find all official resources in one place\n\n"
                "Choose a section below 👇",
                reply_markup=main_menu_en
            )

    @dp.callback_query(F.data == "change_lang")
    async def change_language(callback: CallbackQuery):
        await callback.message.answer(
            "Выбери язык гайда\nChoose guide language",
            reply_markup=lang_kb
        )

    @dp.callback_query(F.data == "guide")
    async def open_guides(callback: CallbackQuery):
        lang = user_lang.get(callback.from_user.id, "en")

        await callback.message.answer(
            (
                "📘 Твой стартовый путь в Preddy\n\n"
                "Эти короткие видео-гайды помогут тебе шаг за шагом\n"
                "разобраться в платформе, понять основы торговли\n"
                "и уверенно сделать первые действия.\n\n"
                "Начни с первого гайда и двигайся дальше 👇"
            )
            if lang == "ru"
            else
            (
                "📘 Your starting path with Preddy\n\n"
                "These short video guides will help you step by step\n"
                "understand the platform, learn the basics of trading,\n"
                "and confidently make your first moves.\n\n"
                "Start with the first guide and move forward 👇"
            ),
            reply_markup=guide_menu_ru if lang == "ru" else guide_menu_en
        )

    @dp.callback_query(F.data.startswith("g_"))
    async def send_video(callback: CallbackQuery):
        lang = user_lang.get(callback.from_user.id, "en")

        await callback.message.answer_video(
            video=VIDEOS[callback.data],
            caption=(
                "🎥 Видео-гайд\n\n"
                "Следуй инструкции и возвращайся к списку гайдов,\n"
                "когда будешь готов продолжить 👇"
            )
            if lang == "ru"
            else
            (
                "🎥 Video guide\n\n"
                "Follow the instructions and return to the guide list\n"
                "when you’re ready to continue 👇"
            ),
            reply_markup=back_to_guides
        )

    @dp.callback_query(F.data == "resources")
    async def open_resources(callback: CallbackQuery):
        lang = user_lang.get(callback.from_user.id, "en")

        await callback.message.answer(
            (
                "🌐 Официальные ресурсы Preddy\n\n"
                "Будь в курсе всех обновлений, новостей и анонсов Preddy.\n"
                "Здесь собраны только официальные каналы и платформы,\n"
                "чтобы ты не пропустил важную информацию 👇\n\n"
                "📣 Telegram — — —\n"
                "🐦 X (Twitter) — — —\n"
                "🎥 YouTube — — —\n"
                "🌍 Website — — —"
            )
            if lang == "ru"
            else
            (
                "🌐 Official Preddy resources\n\n"
                "Stay up to date with all Preddy news, updates, and announcements.\n"
                "Here you’ll find only official channels and platforms\n"
                "so you never miss important information 👇\n\n"
                "📣 Telegram — — —\n"
                "🐦 X (Twitter) — — —\n"
                "🎥 YouTube — — —\n"
                "🌍 Website — — —"
            ),
            reply_markup=back_to_main
        )

    @dp.callback_query(F.data == "back_main")
    async def back_main(callback: CallbackQuery):
        lang = user_lang.get(callback.from_user.id, "en")

        await callback.message.answer(
            "Выбери нужный раздел 👇" if lang == "ru" else "Choose a section 👇",
            reply_markup=main_menu_ru if lang == "ru" else main_menu_en
        )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
