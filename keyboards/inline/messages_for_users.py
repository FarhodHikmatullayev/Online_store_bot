from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

yes_or_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha", callback_data='yes'),
            InlineKeyboardButton(text="Yo'q", callback_data="no")
        ]
    ]
)
