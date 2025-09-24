import { useGame } from "./hooks/use-game";
import { useEffect } from "react";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Toast } from "./components/toast";
import { Game } from "./components/game/game";
import { WaitingRoom } from "./components/waiting-room";

export function App() {
  const { roomState, gameState, errorState, ready, playCard, drawCard, endTurn, punishPlayer } = useGame();

  useEffect(() => {
    if (errorState) {
      toast.error(errorState.message);
    }
  }, [errorState]);

  function renderContent() {
    if (gameState) {
      return <Game drawCard={drawCard} endTurn={endTurn} gameState={gameState} playCard={playCard} punishPlayer={punishPlayer} />;
    }

    if (roomState) {
      return <WaitingRoom roomState={roomState} ready={ready} />;
    }

    return <div>Esperando conexão....</div>;
  }

  return (
    <>
      {renderContent()}
      <Toast />
    </>
  );
}
