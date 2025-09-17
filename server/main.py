import asyncio
import websockets
import json
import random

from game.player import Player
from game.game import Game
from game.card import Joker
from game.rules import MIN_PLAYERS, MAX_PLAYERS, NOT_YOUR_TURN_EVENT_LIST
from utils.payloads import (
    send_update_room,
    send_update_game_status,
    send_error_message,
)
from global_variables import GLOBAL
from utils.player_names_generator import generate_player_name


async def handler(websocket):
    player = None
    connected_clients = [x for x in GLOBAL["clients"] if x["websocket"] != None]
    disconnected_clients = [x for x in GLOBAL["clients"] if x["websocket"] == None]

    if len(connected_clients) >= MAX_PLAYERS:
        response = {
            "type": "error",
            "message": "Jogo já esta cheio! Tente novamente mais tarde.",
        }
        await websocket.send(json.dumps(response))
        await websocket.close()
        return

    if GLOBAL["game"]:
        if disconnected_clients:
            disconnected_clients[0]["websocket"] = websocket
            player = disconnected_clients[0]["player"]
            all_player_reconnected = [
                x for x in GLOBAL["clients"] if x["websocket"] == None
            ] == []

            if all_player_reconnected:
                GLOBAL["game"].is_paused = False

            await send_update_game_status()

        else:
            response = {
                "type": "error",
                "message": "Jogo já iniciou! Tente novamente mais tarde!",
            }
            await websocket.send(json.dumps(response))
            await websocket.close()
            return

    else:
        player = Player(generate_player_name())
        GLOBAL["clients"].append({"websocket": websocket, "player": player})
        for client in GLOBAL["clients"]:
            client["player"].is_ready = False
        await send_update_room()

    try:
        async for message in websocket:
            try:
                message = json.loads(message)
                if message["type"] == "PLAYER_READY":
                    if GLOBAL["game"]:
                        raise Exception("Jogo já iniciou!")

                    elif not player.is_ready:
                        player.is_ready = True
                        if len(GLOBAL["clients"]) >= MIN_PLAYERS:
                            if all(c["player"].is_ready for c in GLOBAL["clients"]):
                                players = [c["player"] for c in GLOBAL["clients"]]
                                GLOBAL["game"] = Game(players)
                                await send_update_game_status()

                    await send_update_room()

                elif GLOBAL["game"] and GLOBAL["game"].is_paused:
                    raise Exception("Jogo pausado. Espere por uma nova conexão")

                elif not GLOBAL["game"] and message["type"] != "PLAYER_READY":
                    raise Exception(
                        "Você precisa estar pronto antes de começar a jogar!"
                    )

                elif GLOBAL["game"] and player != GLOBAL["game"].current_player:
                    if message["type"] in NOT_YOUR_TURN_EVENT_LIST:
                        raise Exception("Não é seu turno!")

                if message["type"] == "PLAY_CARD":
                    list_card_index = message["card_index"]
                    cards_played = [player.hand[index] for index in list_card_index]
                    if len(cards_played) > 2:
                        raise Exception(
                            "Não é possivel jogar mais do que 2 cartas simultâneas!"
                        )

                    card_value = message.get("card_value")
                    for card in cards_played:
                        if isinstance(card, Joker):
                            card.value = card_value

                    GLOBAL["game"].play_card(*cards_played)

                    if GLOBAL["game"].is_game_over:
                        GLOBAL["game"] = None
                        for client in GLOBAL["clients"]:
                            client["player"].is_ready = False
                        await send_update_room()
                    await send_update_game_status()

                if message["type"] == "DRAW_CARD":
                    GLOBAL["game"].draw_card(player)
                    await send_update_game_status()

                if message["type"] == "END_TURN":
                    GLOBAL["game"].end_turn()
                    await send_update_game_status()

                if message["type"] == "PAUSE_GAME":
                    if disconnected_clients:
                        raise Exception(
                            "Não é possivel despausar/despausa o jogo enquanto existe jogadores faltando! Reinicie o jogo ou aguarde reconexão"
                        )
                    GLOBAL["game"].is_paused = not GLOBAL["game"].is_paused
                    await send_update_game_status()

                if message["type"] == "PUNISH":
                    player_index = message["player_index"]
                    target_player = GLOBAL["clients"][player_index]["player"]
                    GLOBAL["game"].punish_player(target_player)
                    await send_update_game_status()

            except Exception as e:
                await send_error_message(str(e), player)

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client {websocket.remote_address} disconnected gracefully.")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Client {websocket.remote_address} disconnected with error: {e}")
    finally:
        disconnected_clients = [
            x for x in GLOBAL["clients"] if x["websocket"] == websocket
        ]
        if GLOBAL["game"]:
            if len(disconnected_clients) == len(GLOBAL["clients"]) - 1:
                GLOBAL["game"] = None
                GLOBAL["clients"] = []
            else:
                disconnected_clients[0]["websocket"] = None
                GLOBAL["game"].is_paused = True
                await send_update_game_status()

        else:
            GLOBAL["clients"].remove(disconnected_clients[0])
            for client in GLOBAL["clients"]:
                client["player"].is_ready = False
                await send_update_room()


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
