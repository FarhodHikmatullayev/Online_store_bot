from aiogram.dispatcher.filters.state import State, StatesGroup

class Product(StatesGroup):
    name = State()
    category = State()
    photo = State()
    price = State()
    description = State()