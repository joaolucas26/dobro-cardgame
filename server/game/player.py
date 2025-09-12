from server.game.card import Card


class Player:
    def __init__(self, name):
        self.name: str = name
        self.hand: list[Card] = []
        self.stack: list[Card] = []
        self.score = 0
        self.played_turn: bool = False

    def add_card(self, card: Card):
        self.hand.append(card)

    def remove_card(self, card: Card):
        self.hand.remove(card)
