from game.player import Player
from game.card import NumberCard


def test_player_initialization():
    player = Player("player1")
    assert player.name == "player1"
    assert player.hand == []
    assert player.stack == []
    assert player.score == 0
    assert player.played_turn == False


def test_player_add_card():
    player = Player("player1")
    card = NumberCard(2)
    player.add_card(card)
    assert card in player.hand


def test_player_remove_card():
    player = Player("player1")
    card = NumberCard(5)
    player.add_card(card)
    player.remove_card(card)
    assert card not in player.hand
