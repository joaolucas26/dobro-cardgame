from game.deck import Deck
from game.card import Card, Joker, PassTurn, Reverse, NumberCard


def test_create_deck():
    deck = Deck()
    assert len([card for card in deck.cards if isinstance(card, Joker)]) == 3
    assert len([card for card in deck.cards if isinstance(card, PassTurn)]) == 2
    assert len([card for card in deck.cards if isinstance(card, Reverse)]) == 2

    numbered_cards = [card for card in deck.cards if isinstance(card, NumberCard)]

    assert len([card for card in numbered_cards if card.value == 2]) == 5
    assert len([card for card in numbered_cards if card.value == 3]) == 6
    assert len([card for card in numbered_cards if card.value == 4]) == 6
    assert len([card for card in numbered_cards if card.value == 5]) == 6
    assert len([card for card in numbered_cards if card.value == 6]) == 6
    assert len([card for card in numbered_cards if card.value == 7]) == 5
    assert len([card for card in numbered_cards if card.value == 8]) == 4
    assert len([card for card in numbered_cards if card.value == 9]) == 3
    assert len([card for card in numbered_cards if card.value == 10]) == 3
    assert len([card for card in numbered_cards if card.value == 11]) == 3
    assert len([card for card in numbered_cards if card.value == 12]) == 3


def test_extend():
    deck = Deck()
    initial_length = len(deck.cards)
    card1 = Card("Test1")
    card2 = Card("Test2")
    deck.extend([card1, card2])

    assert len(deck.cards) == initial_length + 2
    assert deck.cards[-2] == card1
    assert deck.cards[-1] == card2


def test_draw():
    deck = Deck()
    initial_length = len(deck.cards)
    top_card = deck.cards[0]
    card = deck.draw()
    assert len(deck.cards) == initial_length - 1
    assert isinstance(card, Card)
    assert card == top_card
