from typing import List, Optional
from datetime import datetime
import random


from game.deck import Deck
from game.player import Player
from game.card import Card, Joker, PassTurn, Reverse, NumberCard
import game.rules as rules


class Game:
    def __init__(self, players: List[Player]):
        self.players = players
        self.current_player = self.players[0]
        self.stack: List[Card] = []
        self.deck = []
        self.current_round = 1
        self.max_hand_size = rules.MAX_HAND[len(self.players)]
        self.stack_top = 0
        self.is_game_over = False
        self.is_reversed = False
        self.logs = []
        self.is_paused = False

        self._start_round()

    def _start_round(self):
        new_deck = Deck(len(self.players))
        self.deck = new_deck
        self.deck.shuffle()
        for _ in range(self.max_hand_size):
            for player in self.players:
                player.add_card(self.deck.draw())

    def play_card(self, card: Card, card2: Optional[Card] = None):
        if card == card2:
            raise Exception("Cannot play the same card twice")

        if card not in self.current_player.hand:
            raise Exception("Card not in hand")

        if card2 not in self.current_player.hand and card2 != None:
            raise Exception("Second Card not in hand")

        if isinstance(card, Joker):
            if card.value is None:
                raise Exception("Joker must have a value when played")

        if isinstance(card2, Joker):
            if card2.value is None:
                raise Exception("Joker must have a value when played")

        if isinstance(card, Reverse):
            if card2:
                raise Exception("Cannot play second card with Reverse")
            self.players.reverse()
            self.is_reversed = not self.is_reversed

        if isinstance(card, PassTurn):
            if card2:
                raise Exception("Cannot play second card with PassTurn")
            pass

        if isinstance(card, NumberCard) or isinstance(card, Joker):
            if card2:
                if not isinstance(card2, NumberCard) and not isinstance(card2, Joker):
                    raise Exception("Second card must be NumberCard or Joker")

            value = card.value
            if card2:
                if card.value != card2.value:
                    raise Exception(
                        "Both cards must have the same value when played together"
                    )

                value = card.value + card2.value

            if value < self.stack_top:
                raise Exception("Card value must be greater than or equal to stack top")
            if value == self.stack_top:
                self.stack_top *= 2
            else:
                self.stack_top = value

        if card2:
            self._logging(
                f"Player {self.current_player.name} played card {card.name} and {card2.name}",
            )

        else:
            self._logging(
                f"Player {self.current_player.name} played card {card.name}",
            )

        if isinstance(card, Joker):
            card.value = None

        if isinstance(card2, Joker):
            card2.value = None

        self.current_player.played_turn = True
        self.current_player.remove_card(card)
        self.stack.insert(0, card)

        if card2:
            self.current_player.remove_card(card2)
            self.stack.insert(0, card2)

        if self.current_player.hand:
            self.end_turn()
        else:
            self._end_round()

    def end_turn(self):
        self._logging(f"Player {self.current_player.name} Ended Turn")

        if not self.current_player.played_turn:
            self._draw_stack()

        current_player_hand_size = len(self.current_player.hand)

        for _ in range(self.max_hand_size - current_player_hand_size):
            if not self.deck.cards:
                break
            self.current_player.add_card(self.deck.draw())

        if self.current_player.played_turn:
            current_player_index = self.players.index(self.current_player)
            new_index = current_player_index + 1
            if new_index >= len(self.players):
                new_index = 0
            self.current_player.played_turn = False
            self.current_player = self.players[new_index]

    def _end_round(self):
        self._calculate_player_score()
        self._logging(f"Round {self.current_round} Ended")

        if self.current_round == rules.MAX_ROUND:
            self._end_game()
            return

        self.current_round += 1
        self.deck.extend(self.stack)
        self.stack = []

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
        self.stack_top = 0

    def _end_game(self):
        winner = max(self.players, key=lambda player: player.score)
        print(f"Game over! The winner is {winner.name} with a score of {winner.score}")
        self.is_game_over = True

    def _logging(self, message):
        log_time = datetime.now()
        message = f"{log_time.hour}:{log_time.minute} - {message}"
        self.logs.insert(0, message)
