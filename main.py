from server.game.player import Player
from server.game.game import Game
from server.game.deck import Deck

if __name__ == "__main__":

    player1 = Player("p1")
    player2 = Player("p2")
    player3 = Player("p3")

    deck = Deck()

    game = Game(players=[player1, player2, player3], deck=deck)

    def print_cards(cards):
        print([x.name for x in cards])

    print_cards(player1.hand)
    print_cards(player2.hand)
    print_cards(player3.hand)

    game.play_card(player1.hand[0])
    print("player 2 arregou e n jogou nd")
    game.end_turn()

    print("novas moes no round", game.current_round)
    print_cards(player1.hand)
    print_cards(player2.hand)
    print_cards(player3.hand)

    # game.play_card()
