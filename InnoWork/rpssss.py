import telebot
from telebot import types
import random

bot = telebot.TeleBot('')

items = types.InlineKeyboardMarkup()
k = types.InlineKeyboardButton(text="Камень", callback_data="Камень")
g = types.InlineKeyboardButton(text="Ножницы", callback_data="Ножницы")
b = types.InlineKeyboardButton(text="Бумага", callback_data="Бумага")
items.add(k, g, b)

ask = types.InlineKeyboardMarkup()
y = types.InlineKeyboardButton(text="Да", callback_data="Да")
n = types.InlineKeyboardButton(text="Нет", callback_data="Нет")
ask.add(y, n)


@bot.message_handler(commands=['RPS'])
def kgb_message(message):
    bot.send_message(message.chat.id,
                     'Приветcтвую тебя в камень-ножницы-бумага - это одна из самых любимых игр детства. '
                     '\nЕсть вопросы по поводу правил игры? Жми на — /help:'
                     '\n\nВыберите один из предметов: Камень Ножницы Бумага ', reply_markup=items)


@bot.callback_query_handler(func=lambda call: call.data in ["Камень", "Ножницы", "Бумага"])
def query_handler(call):
    kgb = random.choice(["Камень", "Ножницы", "Бумага"])

    bot.answer_callback_query(callback_query_id=call.id, text='Ваш ход принят!')
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"Вы выбрали: {call.data}", reply_markup=None)

    win = {"Камень": "Ножницы", "Ножницы": "Бумага", "Бумага": "Камень"}

    if win[call.data] == kgb:
        bot.send_message(call.message.chat.id, f"Поздравляю, вы победили! \nБот выбрал: {kgb}")
    elif call.data == kgb:
        bot.send_message(call.message.chat.id, f"У вас ничья! \nБот выбрал: {kgb}")
    else:
        bot.send_message(call.message.chat.id, f"Вы проиграли, но ничего получиться в следующий раз! \nБот выбрал: {kgb}")

    bot.send_message(call.message.chat.id, "Хочешь попробовать еще? ", reply_markup=ask)


@bot.callback_query_handler(func=lambda call: call.data in ["Да", "Нет"])
def replay(call):
    if call.data == 'Да':
        bot.answer_callback_query(callback_query_id=call.id, text='Новая игра!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите один из предметов: Камень Ножницы Бумага ", reply_markup=items)
    else:
        bot.answer_callback_query(callback_query_id=call.id, text='Игра окончена!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Спасибо за игру.", reply_markup=None)


bot.infinity_polling()