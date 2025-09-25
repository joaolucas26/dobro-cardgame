import type { GameState } from "../../types";
import { useState } from "react";
import { Hand } from "../hand";
import { Table } from "../table";
import { Logs } from "../logs";
import { Opponents } from "../opponents";

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
      <div style={{ display: "flex", flexDirection: "row", gap: "4rem" }}>
        {gameState.players.map((p, index) => {
          return (
            <Opponents
              key={index}
              handSize={p.hand_size}
              isCurrent={p.is_current}
              name={p.name}
              isPunished={p.is_punished}
              score={p.score}
              stackSize={p.stack_size}
              OnSelect={() => punishPlayer(index)}
            />
          );
        })}
      </div>
      {/* <pre>{JSON.stringify(gameState, null, 2)}</pre>? */}
      <Table
        currentRound={gameState.game.current_round}
        stackSize={gameState.game.stack_cards.length}
        drawCard={drawCard}
        stackTop={gameState.game.stack_top}
        lastPlayedCards={gameState.game.last_played_cards}
        reversed={gameState.game.is_reversed}
      />
      <Hand
        isPunished={gameState.is_punished}
        playerScore={gameState.score}
        playerStack={gameState.stack_size}
        playerName={gameState.name}
        cards={gameState.hand}
        endTurn={endTurn}
        playCard={playCard}
        setSelectedCardsIndexes={setSelectedCardsIndexes}
        isCurrent={gameState.is_current}
        selectedCardsIndexes={selectedCardsIndexes}
        selectedJokerNumber={selectedJokerNumber}
        setSelectedJokerNumber={setSelectedJokerNumber}
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
      <Logs logs={gameState.game.logging} />
    </>
  );
}
