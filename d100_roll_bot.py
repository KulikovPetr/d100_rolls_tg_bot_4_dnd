from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# загружаем токен бота
with open('token.txt','r') as f:
    BOT_TOKEN = f.readline()


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут d100-криты-Бот!\nНапиши мне число, и я отвечу на него значением крита!')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне число от 1 до 100, и я отвечу на него значением крита!'
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_d100_crit(message: Message):
    await message.answer('boop')


if __name__ == '__main__':
    dp.run_polling(bot)