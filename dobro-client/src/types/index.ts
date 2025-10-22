export type RoomState = {
  type: string;
  players: {
    is_me: boolean;
    name: string;
    is_ready: Boolean;
  }[];
};

export type ErrorState = {
  type: string;
  message: string;
};

export type GameState = {
  type: string;
  name: string;
  hand: string[];
  score: number;
  is_current: boolean;
  stack_size: number;
  stack_cards: string[];
  is_punished: boolean;
  has_drew_card: boolean;

  players: {
    id: number;
    name: string;
    hand_size: number;
    stack_size: number;
    score: number;
    is_current: boolean;
    is_punished: boolean;
    has_drew_card: boolean;
    is_ready: boolean;
  }[];
  game: {
    current_player: string;
    deck_size: number;
    stack_top: number;
    stack_cards: string[];
    is_reversed: boolean;
    current_round: number;
    is_game_over: boolean;
    logging: string[];
    is_paused: boolean;
    last_played_cards: string[];
  };
};
