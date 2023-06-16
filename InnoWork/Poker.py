import random
import asyncio
import logging
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton


# создаем класс состояний для машины состояний
from aiogram.utils import executor


class UserState(StatesGroup):
    WAITING_FOR_START = State()  # ожидание начала игры
    IN_PROGRESS = State()  # игра в процессе
    SHOWDOWN = State()  # раскрытие карт


# создаем объекты бота и диспетчера
bot = Bot(token="")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


# функция для начала игры
async def start_poker_game(message: types.Message, state: FSMContext):
    # создаем массив с картами, который перемешиваем
    deck = [i+1 for i in range(52)]
    random.shuffle(deck)
    await state.update_data(deck=deck)  # сохраняем состояние массива карт в машине состояний
    await UserState.IN_PROGRESS.set()  # переводим машину состояний в игровой режим

    # сообщение пользователю о начале игры и отображение кнопок
    buttons = [
        [InlineKeyboardButton("Сменить карты", callback_data="change_cards")],
        [InlineKeyboardButton("Раскрыть карты", callback_data="showdown")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await message.answer("Добро пожаловать в покер! Ваша рука:", reply_markup=keyboard)


# функция для смены карт в игре
async def change_cards(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    deck = data.get("deck")  # получаем текущий массив карт из машины состояний

    # выбираем случайные карты для смены
    new_cards = random.sample(deck, 3)
    updated_deck = [c if c not in new_cards else random.randint(1, 52) for c in deck]
    await state.update_data(deck=updated_deck)  # сохраняем обновленный массив карт в машине состояний

    # формируем сообщение с новыми картами и обновленной клавиатурой
    buttons = [
        [InlineKeyboardButton("Сменить карты", callback_data="change_cards")],
        [InlineKeyboardButton("Раскрыть карты", callback_data="showdown")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    message_text = "Вот ваши новые карты:"
    for card in new_cards:
        message_text += f"\n{card}"
    message_text += "\nЕсли желаете, вы можете сменить до 2 карт. Нажмите 'Сменить карты', чтобы сделать это."
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboard)


# функция для раскрытия карт в игре
async def showdown(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    deck = data.get("deck")  # получаем текущий массив карт из машины состояний

    # формируем сообщение с картами и результатом игры
    message_text = "Ваша рука:"
    for card in deck:
        message_text += f"\n{card}"
    message_text += "\n\nРезультат игры: ничья"  # здесь будет логика выявления победителя

    await bot.send_message(callback_query.from_user.id, message_text)


# обрабатываем нажатия на кнопки
@dp.callback_query_handler(lambda c: c.data == 'change_cards', state=UserState.IN_PROGRESS)
async def process_callback_change_cards(callback_query: types.CallbackQuery, state: FSMContext):
    await change_cards(callback_query, state)


@dp.callback_query_handler(lambda c: c.data == 'showdown', state=UserState.IN_PROGRESS)
async def process_callback_showdown(callback_query: types.CallbackQuery, state: FSMContext):
    await showdown(callback_query, state)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)