def create_room_update_payload(clients, target_player):
    """Creates the payload for a room update for a specific player."""
    return {
        "type": "update_room",
        "players": [
            {
                "is_me": client["player"] == target_player,
                "name": client["player"].name,
                "is_ready": client["player"].is_ready,
            }
            for client in clients
        ],
    }


def create_game_status_payload(game, clients, target_player):
    """Creates the detailed game status payload for a specific player."""
    if not game:
        return None

    game_data = {
        "current_player": game.current_player.name,
        "deck_size": len(game.deck.cards),
        "stack_top": game.stack_top,
        "stack": [card.name for card in game.stack],
        "is_reversed": game.is_reversed,
        "current_round": game.current_round,
        "is_game_over": game.is_game_over,
        "logging": game.logs,
        "is_paused": game.is_paused,
    }

    players_data = [
        {
            "name": client["player"].name,
            "hand_size": len(client["player"].hand),
            "stack_size": len(client["player"].stack),
            "score": client["player"].score,
            "is_current": client["player"] == game.current_player,
            "is_punished": client["player"].is_punished,
            "has_drew_card": client["player"].has_drew_card,
            "is_ready": client["player"].is_ready,
        }
        for client in clients
    ]

    # This specific player's data
    player_specific_data = {
        "name": target_player.name,
        "hand": [card.name for card in target_player.hand],
        "is_current": target_player == game.current_player,
    }

    # Combine all data for the final payload
    return {
        "type": "update_game",
        **player_specific_data,
        "players": [p for p in players_data if p["name"] != target_player.name],
        "game": game_data,
    }


def create_error_payload(message):
    """Creates a generic error payload."""
    return {"type": "error", "message": message}
