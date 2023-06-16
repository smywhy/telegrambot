from telegram import ReplyKeyboardMarkup, Bot, ReplyMarkup, Update
from aiogram.dispatcher import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from credits_meme import bot_token
from PIL import Image, ImageFont, ImageDraw
import datetime
import random

bot = Bot(token=bot_token)
updater = Updater(token=bot_token)
dispatcher = updater.dispatcher

FIRST = 0
SIX = 6
SEVENS = 7
EIGHTS = 8
NINES = 9
TEN = 10

user = ''

font_size = ''
coord_x = ''
coord_y = ''
color = ''
colors = {
    'Белый':(255,255,255),
    'Красный':(255,0,0),
    'Зелёный':(0,255,0),
    'Синий':(0,0,255),
    'Чёрный':(0,0,0)
}

# 1) Имя
# 2) Фамилия
# 3) Возраст
# 4) ПОЛ
# 5) фото

def start(update, context):
    update.message.reply_text('Скинь своё фото для мема')
    return FIRST

def get_photo(update, context):
    photo_file = update.message.document.get_file()
    photo_file.download(str(update.message.from_user['id']) + '.png')
    update.message.reply_text('Фотка получена, давай теперь размер шрифта')
    return SIX

def get_font_size(update, context):
    global font_size
    font_size = update.message.text
    update.message.reply_text('Введи координату расположения по оси X')
    return SEVENS

def get_coord_x(update, context):
    global coord_x
    coord_x = update.message.text
    update.message.reply_text('Теперь по оси Y')
    return EIGHTS

def get_coord_y(update, context):
    global coord_y
    coord_y = update.message.text
    reply_keyboard = [['Чёрный', 'Белый', 'Красный','Синий','Зелёный']]
    update.message.reply_text('Выбери цвет текста из предложенных', reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return NINES

def get_color(update, context):
    global color
    color = update.message.text
    update.message.reply_text('Цвет выбрали, теперь напиши текст для мема')
    return TEN

def get_text(update, context):
    text = update.message.text
    img = Image.open(str(update.message.from_user['id']) + '.png')
    rgb_img = img.convert('RGB')
    title_font = ImageFont.truetype('arial.ttf', int(font_size))
    meme = ImageDraw.Draw(rgb_img)
    meme.text((int(coord_x), int(coord_y)), text, colors[color], font=title_font)
    name = str(update.message.from_user['id']) + '_meme.png'
    rgb_img.save(name)
    sending_img = open(name, 'rb')
    context.bot.send_document(update.effective_chat.id, sending_img)

    return ConversationHandler.END


start_handler = CommandHandler('start', start)
get_photo_handler = MessageHandler(Filters.document.category('image'), get_photo)
get_font_size_handler = MessageHandler(Filters.text,get_font_size)
get_coord_x_handler = MessageHandler(Filters.text,get_coord_x)
get_coord_y_handler = MessageHandler(Filters.text,get_coord_y)
get_text_handler = MessageHandler(Filters.text, get_text)
get_color_handler = MessageHandler(Filters.text,get_color)

conv_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        FIRST: [get_photo_handler],
        SIX: [get_font_size_handler],
        SEVENS: [get_coord_x_handler],
        EIGHTS:[get_coord_y_handler],
        NINES:[get_color_handler],
        TEN:[get_text_handler],

    }, fallbacks=[]
)

dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()