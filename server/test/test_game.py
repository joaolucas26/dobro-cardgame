import pytest
from pytest import mark
from game.game import Game
from game.player import Player
from game.deck import Deck
from game.card import Card, NumberCard, Reverse, PassTurn, Joker


@pytest.fixture
def two_player_game():
    p1 = Player("player1")
    p2 = Player("player2")
    players = [p1, p2]
    game = Game(players)
    return game, players


@pytest.fixture
def three_player_game():
    p1 = Player("player1")
    p2 = Player("player2")
    p3 = Player("player3")
    players = [p1, p2, p3]
    game = Game(players)
    return game, players


def test_game_initialization(three_player_game):
    game, players = three_player_game
    assert game.players == players
    assert game.current_player == players[0]
    assert game.stack == []
    assert game.current_round == 1
    assert game.max_hand_size == 6
    assert game.stack_top == 0

    for player in players:
        assert len(player.hand) == game.max_hand_size


def test_play_card_reverse(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
    reverse_player = [p3, p2, p1]

    reverse_card = Reverse()
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(reverse_card)
    game.play_card(reverse_card)
    game.end_turn()

    assert game.players == reverse_player
    assert game.current_player == p3


def test_play_card_passturn(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players

    passturn_card = PassTurn()
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(passturn_card)
    game.play_card(passturn_card)
    game.draw_card(p1)
    game.end_turn()

    assert game.current_player == p2


def test_play_card_joker(three_player_game):
    game, players = three_player_game
    joker_card = Joker()
    joker_card.value = 5

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)

    game.play_card(joker_card)
    assert game.stack_top == 5
    assert game.stack[0] == joker_card
    assert joker_card.value == None


def test_play_card_joker_same_value_stack_top(three_player_game):
    game, players = three_player_game
    game.stack_top = 5

    joker_card = Joker()
    joker_card.value = 5

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)

    game.play_card(joker_card)
    assert game.stack_top == 10
    assert joker_card.value == None


def test_end_round_no_cards_in_hand(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
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


def test_end_game_max_rounds(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
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


def test_play_card_two_joker_same_value(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
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
    assert len(p1.hand) == 4

    assert game.stack_top == 10
    assert game.stack[1] == joker_card
    assert game.stack[0] == joker_card2
    assert joker_card.value == None
    assert joker_card2.value == None
    assert player_hand_before_play != game.current_player.hand


def test_joker_invalid_low_value_error(two_player_game):
    game, players = two_player_game
    joker_card = Joker()
    joker_card.value = 1
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)

    with pytest.raises(
        Exception,
        match="Não é possivel jogar um valor pro joker menor que 2 ou maior que 12!",
    ):
        game.play_card(joker_card)


def test_play_card_when_card_not_in_hand_error(three_player_game):
    """
    Testa se a carta jogada não está na mão do jogador atual.
    Testa se a segunda carta jogadacurrent_round não está na mão do jogador atual mesmo que a primeira esteja.
    """
    game, players = three_player_game
    p1, p2, p3 = players
    card = Card("carta1")

    with pytest.raises(Exception, match="Carta não esta na mão do jogador!"):
        game.play_card(card)
    assert game.current_player == p1

    with pytest.raises(Exception, match="Segunda carta não esta na mão do jogador!"):
        game.play_card(game.current_player.hand[0], card)
    assert game.current_player == p1


def test_player_played_turn_error(three_player_game):
    game, players = three_player_game
    game.current_player.played_turn = True
    with pytest.raises(
        Exception,
        match="Você ja jogou este turno! Pesque cartas e passe para o proximo!",
    ):
        game.play_card(game.current_player.hand[0])


def test_play_card_joker_no_value_error(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
    joker_card = Joker()

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)

    with pytest.raises(Exception, match="Joker deve possuir um valor para ser jogado!"):
        game.play_card(joker_card)

    assert game.current_player == p1


def test_play_card_second_card_joker_no_value_error(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
    joker_card = Joker()
    joker_card.value = 5
    joker_card2 = Joker()

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)
    game.current_player.add_card(joker_card2)

    with pytest.raises(Exception, match="Joker deve possuir um valor para ser jogado!"):
        game.play_card(joker_card, joker_card2)
    assert game.current_player == p1


def test_play_card_numberedcard_second_card_invalid_error(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
    number_card = NumberCard(5)
    second_card = PassTurn()

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card)
    game.current_player.add_card(second_card)

    with pytest.raises(
        Exception, match="A segunda carta deve ser um número ou um Joker!"
    ):
        game.play_card(number_card, second_card)
    assert game.current_player == p1


def test_play_card_second_card_reverse_error(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
    reverse_card = Reverse()
    second_card = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(reverse_card)
    game.current_player.add_card(second_card)

    with pytest.raises(
        Exception, match="Não é possivel jogar uma segunda carta com Reverso"
    ):
        game.play_card(reverse_card, second_card)
    assert game.current_player == p1


def test_play_card_second_card_passturn_error(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
    passturn_card = PassTurn()
    second_card = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(passturn_card)
    game.current_player.add_card(second_card)

    with pytest.raises(
        Exception, match="Não é possivel jogar uma segunda carta com Passe-o-turno"
    ):
        game.play_card(passturn_card, second_card)
    assert game.current_player == p1


def test_play_card_numbercard(three_player_game):
    game, players = three_player_game
    number_card = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card)
    game.play_card(number_card)
    assert game.stack_top == 5


def test_play_card_numbercard_double_the_stack_value(three_player_game):
    game, players = three_player_game
    game.stack_top = 5
    number_card = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card)
    game.play_card(number_card)
    assert game.stack_top == 10


def test_play_card_numbercard_less_than_top_stack_error(three_player_game):
    game, players = three_player_game
    game.stack_top = 10
    number_card = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card)
    with pytest.raises(
        Exception, match="O valor da carta deve ser maior ou igual ao do topo da pilha!"
    ):
        game.play_card(number_card)
    assert game.stack_top == 10


def test_play_card_same_card_error(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
    reverse_card = Reverse()

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(reverse_card)
    game.current_player.add_card(reverse_card)

    with pytest.raises(Exception, match="Não é possivel jogar a mesma carta 2 vezes!"):
        game.play_card(reverse_card, reverse_card)
    assert game.current_player == p1


def test_play_card_two_different_numbercards_equal_values(three_player_game):
    game, players = three_player_game
    number_card1 = NumberCard(5)
    number_card2 = NumberCard(5)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card1)
    game.current_player.add_card(number_card2)
    game.play_card(number_card1, number_card2)
    assert game.stack_top == 10


def test_play_card_two_numbercards_different_different_values(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
    game.stack_top = 2

    number_card1 = NumberCard(5)
    number_card2 = NumberCard(3)

    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(number_card1)
    game.current_player.add_card(number_card2)
    with pytest.raises(Exception, match="Ambas as cartas devem possuir o mesmo valor!"):

        game.play_card(number_card1, number_card2)
    assert game.stack_top == 2
    assert game.current_player == p1


def test_draw_card_when_played(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
    top_card = game.deck.cards[0]

    passturn_card = PassTurn()
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(passturn_card)
    game.play_card(passturn_card)
    game.draw_card(p1)

    assert len(p1.hand) == 6
    assert game.stack[-1] == passturn_card
    assert p1.hand[-1] == top_card
    assert passturn_card not in game.current_player.hand


def test_draw_stack(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
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
    assert game.current_player == p1


def test_punish_player_success(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players
    game.punish_player(p2)

    assert p2.is_punished is True
    assert p1.is_punished is False
    assert p3.is_punished is False


def test_punish_player_self_error(two_player_game):
    game, players = two_player_game
    p1, p2 = players
    with pytest.raises(Exception, match="Não é possivel punir a si mesmo!"):
        game.punish_player(p1)


def test_punish_player_already_punished_error(two_player_game):
    game, players = two_player_game
    p1, p2 = players
    p2.is_punished = True

    with pytest.raises(Exception, match="Jogador já foi punido!"):
        game.punish_player(p2)


def test_punish_player_hand_full_error(two_player_game):
    game, players = two_player_game
    p1, p2 = players
    p2.has_drew_card = True

    with pytest.raises(
        Exception, match="O jogador não pode ser punido. Sua mão esta completa!"
    ):
        game.punish_player(p2)


def test_joker_invalid_high_value_error(two_player_game):
    game, players = two_player_game
    joker_card = Joker()
    joker_card.value = 13
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(joker_card)

    with pytest.raises(
        Exception,
        match="Não é possivel jogar um valor pro joker menor que 2 ou maior que 12!",
    ):
        game.play_card(joker_card)


def test_play_two_cards_sum_less_than_stack_top_error(three_player_game):
    game, players = three_player_game
    game.stack_top = 11
    card1 = NumberCard(5)
    card2 = NumberCard(5)
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.remove_card(game.current_player.hand[0])
    game.current_player.add_card(card1)
    game.current_player.add_card(card2)

    with pytest.raises(
        Exception,
        match="O valor da soma de ambas as cartas deve ser maior ou igual ao do topo da pilha!",
    ):
        game.play_card(card1, card2)


def test_draw_card_from_empty_deck_error(two_player_game):
    game, players = two_player_game
    game.deck.cards = []
    with pytest.raises(
        Exception, match="Deck vazio! Não é possivel pescar. Passe o Turno!"
    ):
        game.draw_card(players[0])


def test_draw_card_with_full_hand_error(two_player_game):
    game, players = two_player_game
    p1 = players[0]
    game.max_hand_size = 2
    p1.hand = [NumberCard(2), NumberCard(3)]

    with pytest.raises(
        Exception,
        match=f"Não é possivel comprar mais do que {game.max_hand_size} cartas",
    ):
        game.draw_card(p1)


def test_draw_card_sets_has_drew_card_flag(two_player_game):
    game, players = two_player_game
    p1 = players[0]
    game.max_hand_size = 3
    p1.hand = [NumberCard(2), NumberCard(3)]
    game.deck.cards.append(NumberCard(4))  # Ensure deck is not empty

    assert p1.has_drew_card is False
    game.draw_card(p1)
    assert len(p1.hand) == 3
    assert p1.has_drew_card is True


def test_end_round_with_punished_player(three_player_game):
    game, players = three_player_game
    p1, p2, p3 = players

    p1.stack = [NumberCard(2), NumberCard(3), NumberCard(4)]
    p2.stack = [NumberCard(5), NumberCard(6)]
    p3.stack = [NumberCard(7)]
    p3.is_punished = True

    # End the round by making the current player's hand empty
    game.current_player.hand = []
    game._end_round()

    assert p1.score == 1
    assert p2.score == 2
    assert p3.score == 2  # 3 (base) - 1 (punish) = 2
