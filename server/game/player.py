from game.card import Card
import random


class Player:
    def __init__(self, name):
        self.name: str = name
        self.hand: list[Card] = []
        self.stack: list[Card] = []
        self.score = 0
        self.played_turn: bool = False
        self.is_ready: bool = False
        self.is_punished: bool = False
        self.has_drew_card = False
        self.ended_turn = False

    def add_card(self, card: Card):
        self.hand.append(card)

    def remove_card(self, card: Card):
        self.hand.remove(card)

    def reset_for_new_round(self):
        self.hand = []
        self.stack = []
        self.played_turn = False
        self.is_ready = False
        self.is_punished = False
        self.has_drew_card = False
        self.ended_turn = False
