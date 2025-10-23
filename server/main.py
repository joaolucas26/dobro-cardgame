import asyncio
import websockets
import json
import http
from typing import Optional, Tuple, Union


from game.player import Player
from game.game import Game
from game.card import Joker
from game.rules import MIN_PLAYERS, MAX_PLAYERS, NOT_YOUR_TURN_EVENT_LIST
from utils.payloads import (
    create_room_update_payload,
    create_game_status_payload,
    create_error_payload,
)
from utils.player_names_generator import generate_player_name


class RoomManager:
    """Manages the state and logic of a single game room."""

    def __init__(self):
        self.clients = []  # List of {'websocket': ws, 'player': player_obj}
        self.game: Union[Game, None] = None

    @property
    def connected_clients(self):
        return [c for c in self.clients if c["websocket"] is not None]

    @property
    def disconnected_clients(self):
        return [c for c in self.clients if c["websocket"] is None]

    async def handle_connection(self, websocket):
        """Handles a new client connection, either as a new player or a reconnection."""
        if len(self.connected_clients) >= MAX_PLAYERS and not self.disconnected_clients:
            payload = create_error_payload(
                "Jogo já esta cheio! Tente novamente mais tarde."
            )
            await self.send(websocket, payload)
            await websocket.close()
            return None

        if self.game and self.disconnected_clients:
            player = self._reconnect_player(websocket)
            await self.broadcast_game_state()
            return player

        if self.game:
            payload = create_error_payload(
                "Jogo já iniciou! Tente novamente mais tarde!"
            )
            await self.send(websocket, payload)
            await websocket.close()
            return None

        player = self._add_new_player(websocket)
        await self.broadcast_room_update()
        return player

    def _reconnect_player(self, websocket):
        client_to_reconnect = self.disconnected_clients[0]
        client_to_reconnect["websocket"] = websocket
        player = client_to_reconnect["player"]

        if not self.disconnected_clients:
            self.game.is_paused = False
        return player

    def _add_new_player(self, websocket):
        player = Player(generate_player_name())
        print(f"player {player.name} conectado")
        self.clients.append({"websocket": websocket, "player": player})
        return player

    async def handle_disconnection(self, websocket):
        """Handles a client disconnection."""
        client = self.find_client_by_ws(websocket)
        if not client:
            print("Disconnected client not found.")
            return

        print("player", client["player"].name, "disconnected")
        
        # Set websocket to None to mark as disconnected
        client["websocket"] = None

        if self.game:
            # If all players disconnect, end the game
            if not self.connected_clients:
                self.reset_game()
            else:
                self.game.is_paused = True
                await self.broadcast_game_state()
        else:
            # If not in a game, just remove the client entirely
            self.clients.remove(client)
            await self.broadcast_room_update()

    def find_client_by_ws(self, websocket):
        for client in self.clients:
            if client["websocket"] == websocket:
                return client
        return None

    async def set_player_ready(self, player):
        if self.game:
            raise Exception("Jogo já iniciou!")

        player.is_ready = True

        if len(self.clients) >= MIN_PLAYERS and all(
            c["player"].is_ready for c in self.clients
        ):
            players = [c["player"] for c in self.clients]
            self.game = Game(players)
            await self.broadcast_game_state()
        else:
            await self.broadcast_room_update()

    def is_player_turn(self, player):
        return self.game and self.game.current_player == player

    def reset_game(self):
        self.game = None
        self.clients = []

    async def send(self, websocket, payload):
        """Sends a JSON payload to a single websocket."""
        try:
            await websocket.send(json.dumps(payload))
        except websockets.exceptions.ConnectionClosed:
            # Handle case where client disconnects before message can be sent
            pass

    async def broadcast_room_update(self):
        """Broadcasts the current state of the pre-game room to each player."""
        tasks = []
        for client in self.connected_clients:
            payload = create_room_update_payload(self.clients, client["player"])
            tasks.append(self.send(client["websocket"], payload))
        await asyncio.gather(*tasks)

    async def broadcast_game_state(self):
        """Broadcasts the current, personalized state of the game to each player."""
        tasks = []
        for client in self.connected_clients:
            payload = create_game_status_payload(
                self.game, self.clients, client["player"]
            )
            if payload:
                tasks.append(self.send(client["websocket"], payload))
        await asyncio.gather(*tasks)


class MessageHandler:
    """Parses messages and calls the appropriate GameManager method."""

    def __init__(self, game_manager: RoomManager, player: Player, websocket):
        self.manager = game_manager
        self.player = player
        self.websocket = websocket

    async def handle_message(self, raw_message):
        try:
            message = json.loads(raw_message)
            message_type = message.get("type")

            if not message_type:
                raise ValueError("Message type is missing")

            # Game state validation
            if self.manager.game and self.manager.game.is_paused:
                raise Exception("Jogo pausado. Espere por uma nova conexão")
            if not self.manager.game and message_type != "player_ready":
                raise Exception("Você precisa estar pronto antes de começar a jogar!")
            if (
                self.manager.game
                and not self.manager.is_player_turn(self.player)
                and message_type in NOT_YOUR_TURN_EVENT_LIST
            ):
                raise Exception("Não é seu turno!")

            # Route to the correct method
            handler_method = getattr(
                self, f"_handle_{message_type.lower()}", self._handle_unknown
            )
            await handler_method(message)

        except json.JSONDecodeError:
            payload = create_error_payload("Invalid JSON format")
            await self.manager.send(self.websocket, payload)
        except Exception as e:
            payload = create_error_payload(str(e))
            await self.manager.send(self.websocket, payload)

    async def _handle_unknown(self, message):
        raise ValueError(f"Unknown message type: {message.get('type')}")

    async def _handle_player_ready(self, message):
        await self.manager.set_player_ready(self.player)

    async def _handle_play_card(self, message):
        list_card_index = message["cards_index"]
        cards_played = [self.player.hand[index] for index in list_card_index]
        if len(cards_played) > 2:
            raise Exception("Não é possivel jogar mais do que 2 cartas simultâneas!")

        card_value = message.get("card_value")
        for card in cards_played:
            if isinstance(card, Joker):
                card.value = card_value

        self.manager.game.play_card(*cards_played)

        if self.manager.game.is_game_over:
            self.manager.reset_game()
            await self.manager.broadcast_room_update()
        else:
            await self.manager.broadcast_game_state()

    async def _handle_draw_card(self, message):
        self.manager.game.draw_card(self.player)
        await self.manager.broadcast_game_state()

    async def _handle_end_turn(self, message):
        self.manager.game.end_turn()
        await self.manager.broadcast_game_state()

    async def _handle_punish(self, message):
        player_index = message["player_index"]
        target_player = self.manager.clients[player_index]["player"]
        self.manager.game.punish_player(target_player, self.player)
        await self.manager.broadcast_game_state()


GAME_MANAGER = RoomManager()


async def health_check(
    path: str, request_headers: websockets.Headers
) -> Optional[Tuple[http.HTTPStatus, websockets.Headers, bytes]]:
    if path == "/health":
        return http.HTTPStatus.OK, [], b"OK\n"


async def main_handler(websocket):
    """The main entry point for all websocket connections."""
    player = await GAME_MANAGER.handle_connection(websocket)
    if not player:
        return

    message_handler = MessageHandler(GAME_MANAGER, player, websocket)

    try:
        async for message in websocket:
            await message_handler.handle_message(message)
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected.")
    finally:
        await GAME_MANAGER.handle_disconnection(websocket)


async def main():
    async with websockets.serve(
        main_handler, "0.0.0.0", 8765, process_request=health_check
    ):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())