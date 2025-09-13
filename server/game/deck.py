import random

from game.card import NumberCard
import game.rules as rules


class Deck:
    def __init__(self):
        self.cards = []
        self._create_deck()
        self.shuffle()

    def _create_deck(self):
        numbered_cards = rules.NUMBERED_CARDS
        special_cards = rules.SPECIAL_CARDS

        for value, qtd in numbered_cards:
            for _ in range(qtd):
                self.cards.append(NumberCard(value))

        for cardtype, qtd in special_cards:
            for _ in range(qtd):
                self.cards.append(cardtype())

    def draw(self):
        return self.cards.pop(0)

    def shuffle(self):
        random.shuffle(self.cards)

    def extend(self, list_of_cards):
        self.cards.extend(list_of_cards)
