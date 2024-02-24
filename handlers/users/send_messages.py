from aiogram import types
from aiogram.types import Message

from data.config import ADMINS
from keyboards.default.back_menu import back_menu_keyboard
from keyboards.inline.menu_keyboard import menu
from keyboards.inline.messages_for_users import yes_or_no
from loader import dp, db, bot
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext, filters

from states.for_users import SendMessage


@dp.message_handler(Command('send_message'), user_id=ADMINS)
async def create_sending_message(message: Message):
    text = "Yubormoqchi bo'lgan narsangizni kiriting"
    await message.answer(text=text)
    await SendMessage.message.set()


@dp.message_handler(Command('send_message'))
async def create_sending_message(message: Message):
    await message.answer(text="Sizda xabar yuborish uchun ruxsat yo'q!")


@dp.message_handler(state=SendMessage.message, user_id=ADMINS)
async def get_message(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(
        {
            'message': text,
        }
    )
    text = "Xabar jo'natilsinmi?"
    await message.answer(text=text, reply_markup=yes_or_no)


@dp.callback_query_handler(text=['yes', 'no'], state=SendMessage.message, user_id=ADMINS)
async def send_message(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("message")
    if call.data == "yes":
        users = await db.select_all_users()
        for user in users:
            await bot.send_message(chat_id=user['telegram_id'], text=message, reply_markup=back_menu_keyboard)
        await call.message.answer(text="Xabar jo'natildi", reply_markup=back_menu_keyboard)
    else:
        text = "Amaliyot bekor qilindi"
        await call.message.answer(text=text, reply_markup=back_menu_keyboard)
    await state.finish()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
