from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

# загрузка токена бота из файла
def bot_token_download():
    with open('token.txt','r') as file:
        return(file.readline())

# загрузка д100 провалов из файла
def d100_failure_download():
    with open('d100_txt_DB_lol\d100_failure.txt') as file:
        return(file.readlines())

# загрузка д100 успехов из файла
def d100_success_download():
    with open('d100_txt_DB_lol\d100_success.txt') as file:
        return(file.readlines())


# добавил словарь с состоянием одного пользователя.
users = {}

# сохранение списков д100 успехов и провалов
d100_success_list = d100_success_download()
d100_failure_list = d100_failure_download()

# Создаем объекты бота и диспетчера
bot = Bot(token=bot_token_download())
dp = Dispatcher()

# Создаем объекты кнопок
button_success = KeyboardButton(text='Успех')
button_failure = KeyboardButton(text='Провал')

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard = ReplyKeyboardMarkup(keyboard=[[button_success, button_failure]],resize_keyboard=True)

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут d100-криты-Бот!\nНапиши мне число, и я отвечу на него значением крита! Выбери режим:', reply_markup=keyboard)

    # регистрация пользователя в словаре по id
    if message.from_user.id not in users:
        users[message.from_user.id] = {'d_100_mode': None}



# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Выбери режим, напиши мне число от 1 до 100, и я отвечу на него значением крита!', reply_markup=keyboard
    )

# Этот хэндлер будет срабатывать на сообщение с клавиатуры "Успех"
@dp.message(F.text == 'Успех')
async def process_roll_success_command(message: Message):
    users[message.from_user.id]['d_100_mode'] = 'success'
    await message.answer(
        'О, так ты кританул? Ну-ка, и что у тебя на д100?'
    )

# Этот хэндлер будет срабатывать на сообщение с клавиатуры "Провал"
@dp.message(F.text == 'Провал')
async def process_roll_failure_command(message: Message):
    users[message.from_user.id]['d_100_mode'] = 'failure'
    await message.answer(
        'Единица? Харооооош! И что у тебя на д100, хехе?'
    )


# Этот хэндлер будет срабатывать на числа от 1 до 100, означающие крит.успех.
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def send_d100_crit_success(message: Message):
    if message.from_user.id not in users:
        await message.answer('Сначала зарегестрируйся, нажав /start!')
    else:
        if users[message.from_user.id]['d_100_mode'] == 'success':
            await message.answer(d100_success_list[int(message.text)-1], reply_markup=keyboard)
        elif users[message.from_user.id]['d_100_mode'] == 'failure':
            await message.answer(d100_failure_list[int(message.text)-1], reply_markup=keyboard)
        else:
            await message.answer('Сначала выбери "Успех" или "Провал", а потом уже пиши число', reply_markup=keyboard)

# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_messages(message: Message):
    await message.answer(
            'Пришли число от 1 до 100.'
        )


if __name__ == '__main__':
    dp.run_polling(bot)