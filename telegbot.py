import logging
from aiogram.types import Message
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.utils.exceptions import RetryAfter

logger = logging.getLogger(__name__)

bot = Bot(token='6217757600:AAF-7GlvaahttkdTbm2BCrUCN3IWusFAH2E')

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
c1 = InlineKeyboardButton('games')
d1 = InlineKeyboardButton
inline_buttons = [b1, b2, b3, b4, b5, b6, b7, b8, b9]
# filling the field with buttons
inline_kb_full = InlineKeyboardMarkup(row_width=3).add(b1, b2, b3)
inline_kb_full.add(b4, b5, b6)
inline_kb_full.add(b7, b8, b9)

all_users = set()
my_win_tictac = 0


# Обработка команды старт
@dp.message_handler(commands=["start"])
async def process(message: types.Message):
    username = message.from_user.username
    await message.answer(f'Привет @{username}👋🏻\n\nЕсли хочешь поиграть в игры, жмакай сюда 👉🏻 — /games\n'
                         f'Количество пользователей онлайн 👨‍👩‍👧‍👦 — /online\n'
                         f'Посмотреть свой профиль ✉️ — /my\n'
                         f'Наши планы на будущее — /soon\n\n'
                         f'Если у вас есть идеи 💡,то можете предлагать мне их здесь — @smywhy\n\n'
                         f'Хотите, чтобы это реализовывалось быстрее ⏭, то закидывайте донатик по номеру +79827001917')


@dp.message_handler(commands=['soon'])
async def process4(message: types.Message):
    await message.answer(f'\n1. Добавим другие многопользовательские игры🎯🎲🎰 \n'
                         f'2. Добавим валюту 💸,что позволит делать ставки в играх\n'
                         f'3. Добавим ввод и вывод выигранных средств📲\n\n'
                         f'Удачных вам игр на нашем проекте')


@dp.message_handler(commands=['games'])
async def process2(message: types.Message):
    await message.answer(f'На выбор у нас есть только две игры 😰 \n👉🏻 /tictactoe \n👉🏻 /seabattle')


@dp.message_handler(commands=['my'])
async def process3(message: types.Message):
    await message.answer(f'Привет, да это твой профиль! \nЗдесь ты можешь увидеть твои достижения, а именно победы')


@dp.message_handler(commands=['tictactoe'])
async def process_command_1(message: types.Message):
    renew_field()
    global user1id, user1name, mid, cid, msg
    user1name = message.from_user.first_name
    user1id = message.from_user.id
    cid = message.chat.id
    msg = await message.answer(f"Первый игрок1️1️⃣: {user1name} ❌\nВторой игрок: ... ⭕️",
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
        winss = my_win_tictac + 1
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


# name getter
@dp.message_handler(commands=['id'])
async def get_user_name(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup()
    await message.answer(f"name: {message.from_user.first_name}", reply_markup=keyboard_markup)


if __name__ == '__main__':
    executor.start_polling(dp)
