import type { GameState } from "../types";
import { useState } from "react";
import { Hand } from "./hand";
import { PlayerAction } from "./player-action";
import { JokerNumbers } from "./joker-number";

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
  const selectedCardsNames = selectedCardsIndexes.map((index) => {
    return gameState.hand[index];
  });

  const isJokerSelected = selectedCardsNames.includes("Joker");
  return (
    <>
      <pre>{JSON.stringify(gameState, null, 2)}</pre>

      {isJokerSelected && <JokerNumbers onSelect={setSelectedJokerNumber} selectedNumber={selectedJokerNumber} />}

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
      />

      <PlayerAction
        selectedCardsIndexes={selectedCardsIndexes}
        endTurn={endTurn}
        drawCard={drawCard}
        handSize={gameState.hand.length}
        isCurrent={gameState.is_current}
        play={() => {
          const cardValue = selectedCardsNames.find((card) => card != "Joker");
          playCard(selectedCardsIndexes[0], selectedCardsIndexes[1], Number(cardValue));
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
