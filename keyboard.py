from aiogram.types import \
    KeyboardButton, \
    ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, \
    InlineKeyboardButton, \
    InlineKeyboardMarkup

a1 = KeyboardButton("Найти собеседника ")
a2 = KeyboardButton("Привет!")
i1 = InlineKeyboardButton("👍")
i2 = InlineKeyboardButton("👎")

inlinekeyboard =  InlineKeyboardMarkup()
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(a1).add(a2)
inlinekeyboard.insert(i1).insert(i2)
