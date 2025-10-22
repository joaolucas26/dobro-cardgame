from typing import List, Tuple, Dict
from game.card import Card, PassTurn, Reverse, Joker

NUMBERED_CARDS: List[Tuple[int, int]] = [
    (2, 5),
    (3, 6),
    (4, 6),
    (5, 6),
    (6, 6),
    (7, 5),
    (8, 4),
    (9, 3),
    (10, 3),
    (11, 3),
    (12, 3),
]

SPECIAL_CARDS: List[Tuple[Card, int]] = [
    (Joker, 3),
    (PassTurn, 2),
    (Reverse, 2),
]

SPECIAL_CARDS_2_PLAYERS: List[Tuple[Card, int]] = [
    (Joker, 3),
    (PassTurn, 2),
]

MAX_HAND: Dict[int, int] = {
    2: 6,
    3: 6,
    4: 6,
    5: 6,
    6: 5,
}

QTD_CARDS_TO_REMOVE_TWO_PLAYERS = 10
MAX_ROUND: int = 3
MIN_PLAYERS: int = 2
MAX_PLAYERS: int = 6

NOT_YOUR_TURN_EVENT_LIST = ["play_card", "end_turn"]
