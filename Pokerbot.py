from aiogram import Bot, Dispatcher
from aiogram.types import Message, game
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.utils import executor
import asyncio

token = "6114813877:AAFlSKg8Tcm2d4WplE_vUeSiOJdFokiQ4gg"
bot = Bot(token)
dp = Dispatcher(bot)

buttons = [
    InlineKeyboardButton(text='Fold', callback_game="no_bet"),
    InlineKeyboardButton(text="Minimum", callback_game="min_bet"),
    InlineKeyboardButton(text="All-in", callback_game="max_bet")
]
keyboard = [buttons]
reply_markup = InlineKeyboardMarkup(keyboard)

users = set()


@dp.message_handler(commands=["start"])
async def start_game(message: Message):
    # создаем новую игру
    game = Game()

    # отправляем сообщение с инструкциями
    await message.answer("Начинаем игру! Отправьте /join, чтобы присоединиться к игре.")

@dp.message_handler(commands=["join"])
async def join_game(message: Message):
    # добавляем игрока в игру
    game.add_player(message.from_user.id)

    # отправляем сообщение с подтверждением
    await message.answer("Вы присоединились к игре!")

    # проверяем, есть ли достаточное количество игроков, чтобы начать игру
    if game.can_start():
        # начинаем игру
        game.start()

        # отправляем сообщение со стартовыми картами
        for player_id, cards in game.players.items():
            await bot.send_message(player_id, f"Ваши карты: {cards}")


class Game:
    def __init__(self):
        self.players = {}
        self.deck = []
        self.dealer_cards = []
        self.state = "waiting_for_players"

    def add_player(self, player_id):
        self.players[player_id] = []

    def can_start(self):
        return len(self.players) >= 2 and self.state == "waiting_for_players"

    def start(self):
        self.state = "in_progress"

        # создаем колоду и перемешиваем ее
        self.deck = create_deck()

        # сдаем карты игрокам
        for player_id in self.players:
            self.players[player_id] = [draw_card(self.deck), draw_card(self.deck)]

        # сдаем карты дилеру
        self.dealer_cards = [draw_card(self.deck), draw_card(self.deck)]

    def get_scores(self):
        scores = {}

        for player_id, cards in self.players.items():
            scores[player_id] = calculate_score(cards)

        return scores

    def get_winner(self):
        scores = self.get_scores()

        winner = max(scores, key=scores.get)

        return winner

    def end(self):
        self.state = "finished"

        winner = self.get_winner()

        for player_id in self.players:
            if player_id == winner:
                message = "Вы победили! Поздравляем!"
            else:
                message = f"Победил игрок {winner}!"

            bot.send_message(player_id, message)


import random

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


def create_deck():
    deck = []

    for suit in SUITS:
        for rank in RANKS:
            deck.append(rank + suit)

    random.shuffle(deck)

    return deck


def draw_card(deck):
    return deck.pop()


def calculate_score(cards):
    score = 0
    has_ace = False

    for card in cards:
        rank = card[:-1]

        if rank in ["J", "Q", "K"]:
            score += 10
        elif rank == "A":
            score += 11
            has_ace = True
        else:
            score += int(rank)

    if score > 21 and has_ace:
        score -= 10

    return score


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
