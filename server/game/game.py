from typing import List, Optional, Tuple
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
        self.last_played_cards = []

        self._start_round()

    def _start_round(self):
        new_deck = Deck(len(self.players))
        self.deck = new_deck
        self.deck.shuffle()
        for _ in range(self.max_hand_size):
            for player in self.players:
                player.add_card(self.deck.draw())

    def _validade_cards(
        self, card: Card, card2: Optional[Card] = None
    ) -> Tuple[bool, Exception | None]:
        if self.current_player.played_turn:
            return False, Exception(
                "Você ja jogou este turno! Pesque cartas e passe para o proximo!"
            )

        if card == card2:
            return False, Exception("Não é possivel jogar a mesma carta 2 vezes!")

        if card not in self.current_player.hand:
            return False, Exception("Carta não esta na mão do jogador!")

        if card2 not in self.current_player.hand and card2 != None:
            return False, Exception("Segunda carta não esta na mão do jogador!")

        if isinstance(card, Joker):
            if card.value is None:
                return False, Exception("Joker deve possuir um valor para ser jogado!")

        if isinstance(card2, Joker):
            if card2.value is None:
                return False, Exception("Joker deve possuir um valor para ser jogado!")

        if isinstance(card, Reverse):
            if card2:
                return False, Exception(
                    "Não é possivel jogar uma segunda carta com Reverso"
                )

        if isinstance(card, PassTurn):
            if card2:
                return False, Exception(
                    "Não é possivel jogar uma segunda carta com Passe-o-turno"
                )

        if isinstance(card, NumberCard) or isinstance(card, Joker):
            if card2:
                if not isinstance(card2, NumberCard) and not isinstance(card2, Joker):
                    return False, Exception(
                        "A segunda carta deve ser um número ou um Joker!"
                    )

                if card2.value < 2 or card2.value > 12:
                    return False, Exception(
                        "Não é possivel jogar um valor pro joker menor que 2 ou maior que 12!"
                    )

                if card.value + card2.value < self.stack_top:
                    return False, Exception(
                        "O valor da soma de ambas as cartas deve ser maior ou igual ao do topo da pilha!"
                    )

                if card.value != card2.value:
                    return False, Exception(
                        "Ambas as cartas devem possuir o mesmo valor!"
                    )

            elif card.value < self.stack_top:
                return False, Exception(
                    "O valor da carta deve ser maior ou igual ao do topo da pilha!"
                )

            if card.value < 2 or card.value > 12:
                return False, Exception(
                    "Não é possivel jogar um valor pro joker menor que 2 ou maior que 12!"
                )
        return True, None

    def play_card(self, card: Card, card2: Optional[Card] = None):
        IS_CARDS_VALID, error = self._validade_cards(card, card2)

        if not IS_CARDS_VALID:
            raise error

        self.current_player.has_drew_card = False
        self.current_player.ended_turn = False

        if isinstance(card, Reverse):
            self.players.reverse()
            self.is_reversed = not self.is_reversed

        if isinstance(card, PassTurn):
            pass

        if isinstance(card, NumberCard) or isinstance(card, Joker):
            value = card.value
            if card2:
                if card.value == card2.value:
                    value = card.value + card2.value
                    self._logging_play_card(card, card2)
            else:
                self._logging_play_card(card)

            if value == self.stack_top:
                self.stack_top *= 2
                self._logging(
                    f"Jogador {self.current_player.name} Dobrou a pilha! Valor atual: {self.stack_top}"
                )
            else:
                self.stack_top = value

            self._clean_joker_values(card, card2)

        self.current_player.played_turn = True
        self.current_player.remove_card(card)
        self.stack.insert(0, card)
        self.last_played_cards = []
        self.last_played_cards.append(card.name)

        if card2:
            self.current_player.remove_card(card2)
            self.stack.insert(0, card2)
            self.last_played_cards.append(card2.name)

        if not self.current_player.hand:
            self._end_round()

    def end_turn(self):
        self.current_player.ended_turn = True
        self._logging(f"Jogador {self.current_player.name} Encerrou o turno")

        if not self.current_player.played_turn:
            self._logging(
                f"Jogador {self.current_player.name} não jogou nenhuma carta e pescou todo a pilha! ({len(self.stack)} cartas)"
            )
            self._draw_stack()
            self.current_player.played_turn = False
            self.current_player.has_drew_card = False
            self.current_player.ended_turn = False

            return

        current_player_index = self.players.index(self.current_player)
        new_index = current_player_index + 1
        if new_index >= len(self.players):
            new_index = 0
        self.current_player = self.players[new_index]
        self.current_player.played_turn = False
        self.current_player.has_drew_card = False
        self.current_player.ended_turn = False

    def draw_card(self, player):
        if not self.deck.cards:
            raise Exception("Deck vazio! Não é possivel pescar. Passe o Turno!")

        if len(player.hand) >= self.max_hand_size:
            raise Exception(
                f"Não é possivel comprar mais do que {self.max_hand_size} cartas"
            )

        player.add_card(self.deck.draw())
        if not self.deck.cards or self.max_hand_size == len(player.hand):
            player.has_drew_card = True
        else:
            player.has_drew_card = False

        self._logging(f"Jogador {player.name} pescou uma carta!")

    def punish_player(self, player_punished, player_accusation):
        if not player_punished.ended_turn:
            raise Exception("O jogador acusado ainda não terminou o turno!")
        if player_punished.has_drew_card:
            raise Exception("O jogador não pode ser punido. Sua mão esta completa!")
        if player_punished == player_accusation:
            raise Exception("Não é possivel punir a si mesmo!")
        if player_punished.is_punished:
            raise Exception("Jogador já foi punido!")

        self._logging(
            f"Jogador Acusado! Jogador {self.current_player.name} puniu {player_punished.name} por não pescar carta!"
        )

        player_punished.is_punished = True
        for player in self.players:
            if player != player_punished:
                player.is_punished = False

    def _end_round(self):
        self._calculate_player_score()
        self._logging(f"Rodada {self.current_round}/{rules.MAX_ROUND} Encerrada!")

        if self.current_round == rules.MAX_ROUND:
            self._end_game()
            return

        self.current_round += 1
        self.stack = []

        for player in self.players:
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
            if player.is_punished:
                player.score -= 1
            player.score += index + 1

    def _draw_stack(self):
        self.current_player.stack.extend(self.stack)
        self.stack = []
        self.last_played_cards = []

        self.stack_top = 0

    def _end_game(self):
        winner = max(self.players, key=lambda player: player.score)
        self._logging(
            f"Fim de Jogo! O vencedor é {winner.name} com Score de {winner.score}"
        )
        self.is_game_over = True

    def _clean_joker_values(self, card, card2: Optional[Card] = None):
        if isinstance(card, Joker):
            card.value = None
        if isinstance(card2, Joker):
            card2.value = None

    def _logging(self, message):
        log_time = datetime.now()
        message = f"{log_time.hour}:{log_time.minute} - {message}"
        self.logs.insert(0, message)

    def _logging_play_card(self, card, card2=None):
        if card2:
            if isinstance(card2, Joker):
                self._logging(
                    f"Jogador {self.current_player.name} Jogou duas cartas {card.name}, valendo {card.value}!",
                )
            else:
                self._logging(
                    f"Jogador {self.current_player.name} Jogou duas cartas {card.name}!",
                )

        else:
            if isinstance(card, Joker):
                self._logging(
                    f"Jogador {self.current_player.name} Jogou uma cartas {card.name}, valendo {card.value}!",
                )
            else:
                self._logging(
                    f"Jogador {self.current_player.name} jogou uma carta {card.name}!",
                )
