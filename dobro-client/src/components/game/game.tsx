import type { GameState } from "../../types";
import { useState } from "react";
import { Hand } from "../hand";
import { PlayerAction } from "../player-action";
import { Table } from "../table";
import { Logs } from "../logs";

type GameProps = {
  gameState: GameState;
  endTurn: () => void;
  drawCard: () => void;
  playCard: (card1: number, card2?: number, value?: number) => void;
  punishPlayer: (playerIndex: number) => void;
};

export function Game({ gameState, endTurn, drawCard, playCard, punishPlayer }: GameProps) {
  const [selectedCardsIndexes, setSelectedCardsIndexes] = useState<number[]>([]);
  const [selectedJokerNumber, setSelectedJokerNumber] = useState<number>();
  return (
    <>
      {/* <pre>{JSON.stringify(gameState, null, 2)}</pre>? */}
      <Table drawCard={drawCard} stackTop={gameState.game.stack_top} lastPlayedCards={gameState.game.last_played_cards} reversed={gameState.game.is_reversed} />
      <Hand
        cards={gameState.hand}
        selectedCardsIndexes={selectedCardsIndexes}
        onSelectCard={(index, isSelected) => {
          if (isSelected) {
            setSelectedCardsIndexes((prev) =>
              prev.filter((i) => {
                return i != index;
              })
            );
          } else {
            setSelectedCardsIndexes((prev) => [...prev, index]);
          }
        }}
        selectedJokerNumber={selectedJokerNumber}
        setSelectedJokerNumber={setSelectedJokerNumber}
      />
      <Logs logs={gameState.game.logging} />
      <PlayerAction
        selectedCardsIndexes={selectedCardsIndexes}
        endTurn={endTurn}
        isCurrent={gameState.is_current}
        play={() => {
          playCard(selectedCardsIndexes[0], selectedCardsIndexes[1], selectedJokerNumber);
          setSelectedCardsIndexes([]);
        }}
      />
      <div>
        {gameState.players.map((p, index) => {
          return (
            <button key={index} onClick={() => punishPlayer(index)}>
              Punir {p.name}
            </button>
          );
        })}
      </div>
    </>
  );
}
