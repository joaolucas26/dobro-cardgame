import type { RoomState } from "../types";
import { Button } from "./button";

type WaitingRoomProps = {
  roomState: RoomState;
  ready: () => void;
};

export function WaitingRoom(props: WaitingRoomProps) {
  return (
    <div>
      {props.roomState?.players.map((player, index) => {
        return (
          <div key={index}>
            {player.name}
            {player.is_ready ? "✅" : "❌"}
          </div>
        );
      })}

      <Button onClick={props.ready}>PRONTO</Button>
    </div>
  );
}
