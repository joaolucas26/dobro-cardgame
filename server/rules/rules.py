from typing import List, Tuple, Dict
from server.game.card import Card, PassTurn, Reverse, Joker

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
    (Joker, 0),
    (PassTurn, 2),
    (Reverse, 2),
]

MAX_HAND: Dict[int, int] = {
    2: 6,
    3: 6,
    4: 6,
    5: 6,
    6: 5,
}

MAX_ROUND: int = 3
