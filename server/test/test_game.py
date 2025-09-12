import pytest
from server.game.game import Game
from server.game.player import Player
from server.game.deck import Deck
from server.game.card import Card, NumberCard, Reverse, PassTurn, Joker


def test_game_initialization():
    players = [Player("player1"), Player("player2")]
    deck = Deck()
    game = Game(players, deck)

    assert game.players == players
    assert game.current_player == players[0]
    assert game.stack == []
    assert game.deck == deck
    assert game.current_round == 1
    assert game.max_hand_size == 6
    assert game.stack_top == 0

    for player in players:
        assert len(player.hand) == game.max_hand_size


def test_play_card_reverse():
    p1 = Player("player1")
    p2 = Player("player2")
    p3 = Player("player3")
    players = [p1, p2, p3]
    reverse_player = [p3, p2, p1]
    deck = Deck()
    game = Game(players, deck)

    reverse_card = Reverse()
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(reverse_card)
    game.play_card(reverse_card)

    assert game.players == reverse_player
    assert game.current_player == p3


def test_play_card_passturn():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    passturn_card = PassTurn()
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(passturn_card)
    game.play_card(passturn_card)

    assert game.current_player == p2


def test_play_card_joker():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    joker_card = Joker()
    joker_card.value = 5

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)

    game.play_card(joker_card)
    assert game.stack_top == 5
    assert game.stack[0] == joker_card
    assert joker_card.value == None


def test_play_card_joker_same_value_stack_top():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)
    game.stack_top = 5

    joker_card = Joker()
    joker_card.value = 5

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)

    game.play_card(joker_card)
    assert game.stack_top == 10
    assert joker_card.value == None


def test_end_round_no_cards_in_hand():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    p1.stack = [NumberCard(3), NumberCard(4)]
    p2.stack = [NumberCard(5)]

    for card in game.current_player.hand[:]:
        game.current_player.remove_card(card)
    new_card = NumberCard(5)
    game.current_player.add_card(new_card)
    game.play_card(new_card)

    assert game.current_round == 2
    assert game.stack == []
    assert p1.score == 1
    assert p2.score == 2
    assert len(p1.hand) == 6
    assert len(p2.hand) == 6


def test_end_round_no_cards_in_deck():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()

    p1.stack = [NumberCard(3), NumberCard(4)]
    p2.stack = [NumberCard(5)]

    game = Game(players, deck)
    game.deck.cards = []

    game.current_player.played_turn = True
    game.end_turn()

    assert game.current_round == 2
    assert game.stack == []
    assert p1.stack == []
    assert p2.stack == []


def test_end_game_max_rounds():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)
    game.current_round = 3

    p1.stack = [NumberCard(3), NumberCard(4)]
    p2.stack = [NumberCard(5)]

    game.stack = [NumberCard(6), NumberCard(7), NumberCard(8)]
    game.deck.cards = []

    for card in game.current_player.hand[:]:
        game.current_player.remove_card(card)

    new_card = NumberCard(5)
    game.current_player.add_card(new_card)

    game.play_card(new_card)

    assert game.is_game_over == True
    assert game.current_round == 3
    assert p1.score == 1
    assert p2.score == 2


def test_play_card_two_joker_same_value():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    joker_card = Joker()
    joker_card.value = 5
    joker_card2 = Joker()
    joker_card2.value = 5

    player_hand_before_play = game.current_player.hand.copy()

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)
    game.current_player.add_card(joker_card2)

    game.play_card(joker_card, joker_card2)
    assert game.stack_top == 10
    assert game.stack[0] == joker_card
    assert game.stack[1] == joker_card2
    assert joker_card.value == None
    assert joker_card2.value == None
    assert len(p1.hand) == 6
    assert len(p2.hand) == 6
    assert player_hand_before_play != game.current_player.hand


def test_play_card_when_card_not_in_hand():
    """
    Testa se a carta jogada não está na mão do jogador atual.
    Testa se a segunda carta jogadacurrent_round não está na mão do jogador atual mesmo que a primeira esteja.
    """
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)
    card = Card("carta1")

    with pytest.raises(Exception, match="Card not in hand"):
        game.play_card(card)
    assert game.current_player == p1

    with pytest.raises(Exception, match="Second Card not in hand"):
        game.play_card(game.current_player.hand[0], card)
    assert game.current_player == p1


def test_play_card_joker_no_value():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)
    joker_card = Joker()

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)

    with pytest.raises(Exception, match="Joker must have a value when played"):
        game.play_card(joker_card)

    assert game.current_player == p1


def test_play_card_second_card_joker_no_value():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)
    joker_card = Joker()
    joker_card.value = 5
    joker_card2 = Joker()

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)
    game.current_player.add_card(joker_card2)

    with pytest.raises(Exception, match="Joker must have a value when played"):
        game.play_card(joker_card, joker_card2)
    assert game.current_player == p1


def test_play_card_numberedcard_second_card_invalid():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    number_card = NumberCard(5)
    second_card = PassTurn()

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card)
    game.current_player.add_card(second_card)

    with pytest.raises(Exception, match="Second card must be NumberCard or Joker"):
        game.play_card(number_card, second_card)
    assert game.current_player == p1


def test_play_card_second_card_reverse():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    reverse_card = Reverse()
    second_card = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(reverse_card)
    game.current_player.add_card(second_card)

    with pytest.raises(Exception, match="Cannot play second card with Reverse"):
        game.play_card(reverse_card, second_card)
    assert game.current_player == p1


def test_play_card_second_card_passturn():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    passturn_card = PassTurn()
    second_card = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(passturn_card)
    game.current_player.add_card(second_card)

    with pytest.raises(Exception, match="Cannot play second card with PassTurn"):
        game.play_card(passturn_card, second_card)
    assert game.current_player == p1


def test_play_card_numbercard():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    number_card = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card)
    game.play_card(number_card)
    assert game.stack_top == 5


def test_play_card_numbercard_double_the_stack_value():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    game.stack_top = 5
    number_card = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card)
    game.play_card(number_card)
    assert game.stack_top == 10


def test_play_card_numbercard_less_than_top_stack():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    game.stack_top = 10
    number_card = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card)
    with pytest.raises(
        Exception, match="Card value must be greater than or equal to stack top"
    ):
        game.play_card(number_card)
    assert game.stack_top == 10


def test_play_card_same_card():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    reverse_card = Reverse()

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(reverse_card)
    game.current_player.add_card(reverse_card)

    with pytest.raises(Exception, match="Cannot play the same card twice"):
        game.play_card(reverse_card, reverse_card)
    assert game.current_player == p1


def test_play_card_two_different_numbercards_equal_values():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)

    number_card1 = NumberCard(5)
    number_card2 = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card1)
    game.current_player.add_card(number_card2)
    game.play_card(number_card1, number_card2)
    assert game.stack_top == 10


def test_play_card_two_numbercards_different_different_values():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)
    game.stack_top = 2

    number_card1 = NumberCard(5)
    number_card2 = NumberCard(3)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card1)
    game.current_player.add_card(number_card2)
    with pytest.raises(
        Exception, match="Both cards must have the same value when played together"
    ):

        game.play_card(number_card1, number_card2)
    assert game.stack_top == 2
    assert game.current_player == p1


def test_draw_card_when_played():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)
    top_card = game.deck.cards[0]

    passturn_card = PassTurn()
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(passturn_card)
    game.play_card(passturn_card)

    assert len(p1.hand) == 6
    assert game.stack[-1] == passturn_card
    assert p1.hand[-1] == top_card
    assert passturn_card not in game.current_player.hand
    assert game.current_player == p2

    card1 = NumberCard(2)
    card2 = NumberCard(2)
    game.deck.cards = [NumberCard(1)]
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(card1)
    game.current_player.add_card(card2)
    game.play_card(card1, card2)
    assert len(p2.hand) == 5
    assert game.current_player == p1


def test_draw_stack():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    deck = Deck()
    game = Game(players, deck)
    game.stack = [NumberCard(3), NumberCard(4), NumberCard(5)]
    game.end_turn()

    assert all(
        [
            card
            for card in p1.stack
            if card in [NumberCard(3), NumberCard(4), NumberCard(5)]
        ]
    )
    assert game.stack == []
    assert game.current_player == p2
    assert len(p1.hand) == 6
    assert len(p2.hand) == 6
