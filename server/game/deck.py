import random
from typing import List

from game.card import NumberCard, Card
import game.rules as rules


class Deck:
    def __init__(self, num_players: int):
        self.cards = []
        self.num_players = num_players
        self._create_deck()
        self.shuffle()

    def _create_deck(self):
        numbered_cards = rules.NUMBERED_CARDS
        special_cards = rules.SPECIAL_CARDS

        for value, qtd in numbered_cards:
            for _ in range(qtd):
                self.cards.append(NumberCard(value))

        if self.num_players == 2:
            special_cards = rules.SPECIAL_CARDS_2_PLAYERS
            self.cards = random.sample(
                self.cards,
                len(self.cards) - rules.QTD_CARDS_TO_REMOVE_TWO_PLAYERS,
            )

        for cardtype, qtd in special_cards:
            for _ in range(qtd):
                self.cards.append(cardtype())

    def draw(self):
        return self.cards.pop(0)

    def shuffle(self):
        random.shuffle(self.cards)

    def extend(self, list_of_cards: List[Card]):
        self.cards.extend(list_of_cards)
