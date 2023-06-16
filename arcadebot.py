from idlelib.window import register_callback
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.utils.exceptions import RetryAfter
import random
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
import requests


logger = logging.getLogger(__name__)
TOKEN = "6185398029:AAFl5O5oX_jErHWSd5cGG0KQCihnKpHj-1w"
bot = Bot(TOKEN)

dp = Dispatcher(bot)

white_square = '⬜'
circle = '⭕'
X = '❌'
# inline buttons
b1 = InlineKeyboardButton(white_square, callback_data='1')
b2 = InlineKeyboardButton(white_square, callback_data='2')
b3 = InlineKeyboardButton(white_square, callback_data='3')
b4 = InlineKeyboardButton(white_square, callback_data='4')
b5 = InlineKeyboardButton(white_square, callback_data='5')
b6 = InlineKeyboardButton(white_square, callback_data='6')
b7 = InlineKeyboardButton(white_square, callback_data='7')
b8 = InlineKeyboardButton(white_square, callback_data='8')
b9 = InlineKeyboardButton(white_square, callback_data='9')
c1 = InlineKeyboardButton(text="games", callback_data='games')
c2 = InlineKeyboardButton(text="memes", callback_data='memes')
c3 = InlineKeyboardButton(text="online", callback_data='online')
c4 = InlineKeyboardButton(text="my", callback_data='my')
c5 = InlineKeyboardButton(text="soon", callback_data='soon')
c6 = InlineKeyboardButton(text="help", callback_data='help')
inline_buttons = [b1, b2, b3, b4, b5, b6, b7, b8, b9]
# filling the field with buttons
inline_kb_full = InlineKeyboardMarkup(row_width=3).add(b1, b2, b3)
inline_kb_full.add(b4, b5, b6)
inline_kb_full.add(b7, b8, b9)
inline_but_full = InlineKeyboardMarkup(row_width=2).add(c1, c2, c3, c4, c5, c6)

all_users = set()


# Обработка команды старт
@dp.message_handler(commands=["start"])
async def process(message: types.Message):
    username = message.from_user.username
    await message.answer(f'Добро пожаловать 👋🏻 на сервер мини-игр @{username}\n'
                         f'Для того, чтобы продолжить пропишите — /command\n\n'
                         f'Если у вас есть идеи 💡,то можете предлагать мне их здесь — @smywhy\n\n'
                         f'Хотите, чтобы ваши идеи реализовывалось быстрее ⏭, то закидывайте донат по номеру — +79827001917')


@dp.message_handler(commands=['command'])
async def process2(message: types.Message):
    await message.answer(f'Хочешь поиграть в игры, жмакай сюда 👉🏻 /games\n'
                         f'Хочешь увидеть парочку мемов, тыкай — /memes\n'
                         f'Количество пользователей онлайн 👨‍👩‍👧‍👦 — /online\n'
                         f'Посмотреть свой профиль ✉️ — /my\n'
                         f'Планы на будущее — /soon\n\n'
                         f'Узнать правила мини-игр ➡️ /help', reply_markup=inline_but_full)


@dp.message_handler(commands=['soon'])
async def process3(message: types.Message):
    await message.answer(f'\n1. Добавим другие многопользовательские игры🎯🎲🎰 \n'
                         f'2. Добавим валюту 💸,что позволит делать ставки в играх\n'
                         f'3. Добавим ввод и вывод выигранных средств📲\n\n'
                         f'Удачных вам игр на нашем проекте')


@dp.message_handler(commands=['help'])
async def process6(message: types.Message):
    await message.answer(f'*TicTacToe* ⬇️', parse_mode="Markdown")
    await message.answer(
        f'Крестики и нолики - каждый игрок поочередно выбирает свободные клетки поля(один всегда крестики, а другой нолики). '
        f'Первый, кто выстроит в ряд 3 своих фигуры по вертикали, горизонтали или большой диагонали, выигрывает!')


@dp.message_handler(commands=['online'])
async def process4(message: types.Message):
    user_id = message.from_user.id
    if user_id not in all_users:
        all_users.add(user_id)
        await message.answer(f'Всего пользователей онлайн: {len(all_users)}')


@dp.message_handler(commands=['games'])
async def process5(message: types.Message):
    await message.answer(f'Выбор игр: \n\n/tictactoe — веселая игра крестики и нолики ❌⭕️\n\n'
                         f'/maths — жми, если давно не решал простые математические задачки 1️⃣2️⃣3️⃣ '
                         f'Возникли вопросы по поводу правил игр, жми сюда — /help')


@dp.callback_query_handler(lambda c: c.data == 'c1', state='*')
async def button_с1(callback: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=callback.id)
    await process5()


@dp.message_handler(commands=['tictactoe'])
async def process_command_1(message: types.Message):
    renew_field()
    global user1id, user1name, mid, cid, msg
    user1name = message.from_user.first_name
    user1id = message.from_user.id
    cid = message.chat.id
    msg = await message.answer(
        f"Приветствую тебя в старой и веселой игре крестики-нолики! ❌⭕️\nЕсть вопросы по поводу правил игры? Жми на — /help\n\n"
        f"Удачной игры!🤪\n\n"
        f"1st player: {user1name} ❌\n2nd player: ... ⭕️",
        reply_markup=inline_kb_full)
    mid = msg.message_id


@dp.callback_query_handler(lambda c: c.data)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = int(callback_query.data)
    global user2name
    user2name = callback_query.from_user.first_name
    if count_white_squares() == 8 and user2name != user1name:
        try:
            await bot.edit_message_text(message_id=mid, chat_id=cid,
                                        text=f"1st player: {user1name}❌\n2nd player: {user2name}⭕️",
                                        reply_markup=inline_kb_full)
        except Exception:
            print('Flood in line 58')
    if callback_query.from_user.id == user1id:
        if count_white_squares() in [9, 7, 5, 3, 1]:
            step = user1_steps(code)
            if step == False:
                await bot.answer_callback_query(callback_query.id, text="You can't change your oponent's sign")
            else:
                try:
                    await bot.edit_message_reply_markup(message_id=mid, chat_id=cid, reply_markup=inline_kb_full)
                except RetryAfter:
                    print('Flood in line 68')
        elif count_white_squares() not in [9, 7, 5, 3, 1]:
            await bot.answer_callback_query(callback_query.id, text="It's not your turn")

    if callback_query.from_user.id != user1id:
        if count_white_squares() not in [9, 7, 5, 3, 1]:
            step = user2_steps(code)
            if step == False:
                await bot.answer_callback_query(callback_query.id, text="You can't change your opponent's sign")
            else:
                try:
                    await bot.edit_message_reply_markup(message_id=mid, chat_id=cid, reply_markup=inline_kb_full)
                except RetryAfter:
                    print('Flood line 81')
        elif count_white_squares() in [9, 7, 5, 3, 1]:
            await bot.answer_callback_query(callback_query.id, text="It's not your turn")
    if count_white_squares() < 5:
        await check_game()


async def check_game():
    # win cases
    if b1.text == b2.text == b3.text != white_square or b1.text == b4.text == b7.text != white_square or \
            b1.text == b5.text == b9.text != white_square or b2.text == b5.text == b8.text != white_square or \
            b3.text == b5.text == b7.text != white_square or b4.text == b5.text == b6.text != white_square or \
            b7.text == b8.text == b9.text != white_square or b3.text == b6.text == b9.text != white_square:
        await end_game('win')
    else:
        if count_white_squares() == 0:
            # tie case
            await end_game('tie')


async def end_game(status):
    if status == 'win':
        winner = get_current_user()
        await announce_winner(winner)
    else:
        await bot.delete_message(chat_id=cid, message_id=mid)
        await bot.send_message(chat_id=cid,
                               text=f'Tie 🤝 \n{b1.text}{b2.text}{b3.text}\n{b4.text}{b5.text}{b6.text}\n{b7.text}{b8.text}{b9.text}')


def get_current_user():
    if count_white_squares() % 2 == 0:
        return user1name
    else:
        return user2name


async def announce_winner(winner):
    await bot.delete_message(chat_id=cid, message_id=mid)
    await bot.send_message(chat_id=cid,
                           text=f'The winner is {winner} 🏆\n{b1.text}{b2.text}{b3.text}\n{b4.text}{b5.text}{b6.text}\n{b7.text}{b8.text}{b9.text}')


def count_white_squares():
    counter = 0
    for btn in inline_buttons:
        if btn.text == white_square:
            counter += 1
    return counter


def renew_field():
    for btn in inline_buttons:
        btn.text = white_square


def user1_steps(x):
    btn = eval('b' + str(x))
    if btn.text == white_square:
        btn.text = X
    else:
        return False


def user2_steps(x):
    btn = eval('b' + str(x))
    if btn.text == white_square:
        btn.text = circle
    else:
        return False


# flood control
def __send_message(text: str, chat_id: int, parse_mode: str = None, update=None, context=None):
    if update:
        try:
            update.message.reply_text(text=text,
                                      parse_mode=parse_mode)
        except Exception:  # ignore users who spam in private chat
            pass
    else:
        logger.error('No update or context to send the message.')


class GameStates(StatesGroup):
    playing = State()


@dp.message_handler(commands=['maths'])
async def game(update: types.Update, state: FSMContext):
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)

    operator = random.choice(['+', '-', '*'])

    if operator == '+':
        answer = num1 + num2

    elif operator == '-':
        answer = num1 - num2

    elif operator == '*':
        answer = num1 * num2

    await state.update_data(answer=answer)
    answer_options = [answer]

    while len(answer_options) < 4:

        new_answer = random.randint(1, 200)

        if new_answer not in answer_options:
            answer_options.append(new_answer)

    random.shuffle(answer_options)
    keyboard = InlineKeyboardMarkup(row_width=2)

    for option in answer_options:
        callback_data = str(option)

        button = InlineKeyboardButton(str(option), callback_data=callback_data)
        keyboard.add(button)

    await bot.send_message(chat_id=update.from_user.id, text=f"{num1} {operator} {num2} = ?", reply_markup=keyboard)
    await GameStates.playing.set()

async def process2maths(update: types.Update, state: FSMContext):
    await game(update, state)
async def answer_handler(update: types.Update, state: FSMContext):
    user_answer = int(update.data)
    data = await state.get_data()
    correct_answer = data['answer']
    if user_answer == correct_answer:

        await bot.delete_message(update.message.chat.id, update.message.message_id)
        await bot.answer_callback_query(callback_query_id=update.id, text="Correct")
        await game(update, state)

    else:

        await bot.answer_callback_query(callback_query_id=update.id, text="Incorrect")
        await state.finish()


async def processmaths(update: types.Update):
    await bot.send_message(chat_id=update.chat.id, text="Welcome to the math game! Press the /maths command to start.")


async def process2maths(update: types.Update, state: FSMContext):
    await game(update, state)


dp.register_message_handler(processmaths, Command("maths"))

dp.register_message_handler(process2maths, Command("play"), state="*")

dp.register_callback_query_handler(answer_handler, state=GameStates.playing)


@dp.message_handler(Text(equals='memes'), state='*')
async def processmem(message: types.Message, state: FSMContext):
    await bot.send_video(message.chat.id, 'https://tenor.com/ru/view/%D1%81%D0%BA%D0%B0%D0%BB%D0%B0-gif-26139573', None,'Text')


@dp.message_handler(commands=['my'])
async def process3(message: types.Message):
    username = message.from_user.username
    user_id = message.from_user.id
    await message.answer(f'Привет, да это твой профиль!\n\n'
                         f'Твой никнейм: {username}\nТвой алиас: @{username}\nТвой id: {user_id}\n\nСкоро здесь появятся твои достижения...')


if __name__ == '__main__':
    executor.start_polling(dp)
