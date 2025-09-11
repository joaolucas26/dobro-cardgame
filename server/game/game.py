from server.game.deck import Deck
from server.game.player import Player
from server.game.card import Card, Joker, PassTurn, Reverse, NumberCard
import server.rules.rules as rules


from typing import List, Optional


class Game:
    def __init__(self, players: List[Player], deck: Deck):
        self.players = players
        self.current_player = self.players[0]
        self.stack: List[Card] = []
        self.deck = deck
        self.current_round = 1
        self.max_hand_size = rules.MAX_HAND[len(self.players)]
        self.stack_top = 0

        self._start_round()

    def _start_round(self):
        self.deck.shuffle()
        for _ in range(self.max_hand_size):
            for player in self.players:
                player.add_card(self.deck.draw())

    def play_card(self, card: Card, card2: Optional[Card] = None):
        if card not in self.current_player.hand:
            return
        if card2 not in self.current_player.hand and card2 != None:
            return

        if isinstance(card, Joker) or isinstance(card2, Joker):
            # implementar
            return

        if isinstance(card, Reverse):
            if card2:
                return
            self.players.reverse()

        if isinstance(card, PassTurn):
            if card2:
                return
            pass

        if isinstance(card, NumberCard):
            value = card.value
            if card2:
                if not isinstance(card, NumberCard):
                    return

                if card.value != card2.value:
                    return

                value = card.value + card2.value

            if value < self.stack_top:
                return
            if value == self.stack_top:
                self.stack_top *= 2
            else:
                self.stack_top = value

        self.current_player.played_turn = True
        self.current_player.remove_card(card)
        self.stack.append(card)

        if self.current_player.hand:
            self.end_turn()
        else:
            self._end_round()

    def end_turn(self):
        if not self.current_player.played_turn:
            self._draw_stack()

        if not self.deck.cards:
            self._end_round()
            return

        current_player_hand_size = len(self.current_player.hand)

        for _ in range(self.max_hand_size - current_player_hand_size):
            if not self.deck.cards:
                break
            self.current_player.add_card(self.deck.draw())

        current_player_index = self.players.index(self.current_player)
        new_index = current_player_index + 1
        if new_index >= len(self.players):
            new_index = 0
        self.current_player.played_turn = False
        self.current_player = self.players[new_index]

    def _end_round(self):
        if self.current_round == rules.MAX_ROUND:
            self._end_game()
            return

        self.current_round += 1
        self.deck.extend(self.stack)
        self.stack = []

        self._calculate_player_score()
        for player in self.players:
            self.deck.extend(player.hand)
            self.deck.extend(player.stack)
            player.hand = []
            player.stack = []

        self.current_player = min(self.players, key=lambda player: player.score)
        self.stack_top = 0
        self._start_round()

    def _calculate_player_score(self):
        sorted_players_by_stack = sorted(
            self.players, key=lambda player: len(player.stack), reverse=True
        )
        for index, player in enumerate(sorted_players_by_stack):
            player.score += index + 1

    def _draw_stack(self):
        self.current_player.stack.extend(self.stack)
        self.stack = []

    def _draw(self):
        drawn_card = self.deck.draw()
        self.current_player.hand.append(drawn_card)

    def _end_game(self):
        return
