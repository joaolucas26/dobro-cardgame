import asyncio
import json


from global_variables import GLOBAL


async def _send_to_all(message):
    await asyncio.gather(
        *[
            client["websocket"].send(json.dumps(message(client["player"])))
            for client in GLOBAL["clients"]
            if client["websocket"] != None
        ]
    )


async def _send_message_to_player(message, player):
    for client in GLOBAL["clients"]:
        if client["player"] == player:
            await client["websocket"].send(json.dumps(message))
            break


async def send_update_room():
    await _send_to_all(
        lambda p: {
            "type": "update_room",
            "players": [
                {
                    "is_me": client["player"] == p,
                    "name": client["player"].name,
                    "is_ready": client["player"].is_ready,
                }
                for client in GLOBAL["clients"]
            ],
        }
    )


async def send_update_game_status():
    game_data = {
        "current_player": GLOBAL["game"].current_player.name,
        "deck_size": len(GLOBAL["game"].deck.cards),
        "stack_top": GLOBAL["game"].stack_top,
        "stack": [card.name for card in GLOBAL["game"].stack],
        "is_reversed": GLOBAL["game"].is_reversed,
        "current_round": GLOBAL["game"].current_round,
        "is_game_over": GLOBAL["game"].is_game_over,
        "logging": GLOBAL["game"].logs,
        "is_paused": GLOBAL["game"].is_paused,
    }

    players_data = [
        {
            "name": client["player"].name,
            "hand_size": len(client["player"].hand),
            "stack_size": len(client["player"].stack),
            "stack": [card.name for card in client["player"].stack],
            "score": client["player"].score,
            "is_current": client["player"] == GLOBAL["game"].current_player,
            "is_punished": client["player"].is_punished,
            "has_drew_card": client["player"].has_drew_card,
            "is_ready": client["player"].is_ready,
        }
        for client in GLOBAL["clients"]
    ]

    await _send_to_all(
        lambda p: {
            "type": "update_game",
            "name": p.name,
            "hand": [card.name for card in p.hand],
            "stack_size": len(p.stack),
            "score": p.score,
            "stack": [card.name for card in p.stack],
            "is_current": p == GLOBAL["game"].current_player,
            "is_punished": p.is_punished,
            "has_drew_card": p.has_drew_card,
            "players": [
                player_data
                for player_data in players_data
                if player_data["name"] != p.name
            ],
            "game": game_data,
        }
    )


async def send_error_message(e, player):
    message = {"type": "error", "message": e}
    await _send_message_to_player(message, player)
