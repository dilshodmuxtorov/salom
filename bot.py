import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
import selectors

API_TOKEN = "8175468014:AAHHXenesmv8On1hEN1MpizpN3PzZdvgG7k"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

# Определение состояний
class Registration(StatesGroup):
    full_name = State()
    birth_date = State()
    phone_number = State()
    gmail = State()
    
@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await message.answer("Привет! Давай зарегистрируем Gmail. Как тебя зовут? (Полное имя)")
    await state.set_state(Registration.full_name)

@dp.message(Registration.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Отлично! Теперь укажи дату рождения (например, 01.01.2000)")
    await state.set_state(Registration.birth_date)

@dp.message(Registration.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Теперь укажи номер телефона (например, +79991234567)")
    await state.set_state(Registration.phone_number)

@dp.message(Registration.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("И наконец, укажи адрес Gmail (например, example@gmail.com)")
    await state.set_state(Registration.gmail)

@dp.message(Registration.gmail)
async def process_gmail(message: Message, state: FSMContext):
    await state.update_data(gmail=message.text)
    user_data = await state.get_data()

    response = (
        "Регистрация завершена! Вот твои данные:\n"
        f"Полное имя: {user_data['full_name']}\n"
        f"Дата рождения: {user_data['birth_date']}\n"
        f"Номер телефона: {user_data['phone_number']}\n"
        f"Gmail: {user_data['gmail']}"
    )
    await message.answer(response)

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
