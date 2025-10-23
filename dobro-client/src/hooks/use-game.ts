import { useState, useEffect, useRef } from "react";
import type { RoomState, GameState, ErrorState } from "../types";

const SERVER_URL = "wss://dobro.imbroglio.com.br";
const TIMEOUT_LIMIT = 3000;
export function useGame() {
  const [roomState, setRoomState] = useState<RoomState>();
  const [gameState, setGameState] = useState<GameState>();
  const [errorState, setErrorState] = useState<ErrorState>();

  const socketRef = useRef<WebSocket>(null);
  const timeoutRef = useRef<number>(null);

  useEffect(() => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    if (!socketRef.current) {
      socketRef.current = new WebSocket(SERVER_URL);
      socketRef.current.onopen = () => {
        console.log("player connected");
      };
      socketRef.current.onclose = () => {
        console.log("player disconnected");
      };
      socketRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        switch (data.type) {
          case "update_room":
            setRoomState(data);
            break;
          case "update_game":
            setGameState(data);
            break;
          case "error":
            setErrorState(data);
            break;
        }
      };
    }
    return () => {
      timeoutRef.current = setTimeout(() => {
        socketRef.current?.close();
        socketRef.current = null;
      }, TIMEOUT_LIMIT);
    };
  }, []);

  function send(data: any) {
    console.log(data);
    if (!socketRef.current) return;
    socketRef.current.send(JSON.stringify(data));
  }

  function ready() {
    send({
      type: "player_ready",
    });
  }

  function playCard(cardIndex1: number, cardIndex2?: number, cardValue?: number) {
    send({
      type: "play_card",
      cards_index: cardIndex2 ? [cardIndex1, cardIndex2] : [cardIndex1],
      card_value: cardValue,
    });
  }

  function drawCard() {
    send({ type: "draw_card" });
  }

  function endTurn() {
    send({ type: "end_turn" });
  }

  function punishPlayer(playerIndex: number) {
    send({ type: "punish", player_index: playerIndex });
  }

  return {
    roomState,
    gameState,
    errorState,
    ready,
    playCard,
    drawCard,
    endTurn,
    punishPlayer,
  };
}
