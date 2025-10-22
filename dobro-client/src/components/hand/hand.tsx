import { Card } from "../card";
import styles from "./hand.module.css";
import { JokerWheel } from "../joker-wheel/joker-wheel";
import { PlayerAction } from "../player-action/player-action";
import { Button } from "../button";

type HandProps = {
  isPunished: boolean;
  playerScore: number;
  playerStack: number;
  playerName: string;
  cards: string[];
  selectedCardsIndexes: number[];
  onSelectCard: (index: number, isSelected: boolean) => void;
  setSelectedJokerNumber: (number?: number) => void;
  selectedJokerNumber?: number;
  endTurn: () => void;
  isCurrent: boolean;
  playCard: (card1: number, card2?: number, value?: number) => void;
  setSelectedCardsIndexes: (indexes: number[]) => void;
};

const SPECIAL_CARDS_NAMES = ["Reverse", "PassTurn"];
const MAX_SELECTED_CARDS = 2;

export function Hand({
  isPunished,
  playerScore,
  playerStack,
  playerName,
  cards,
  selectedCardsIndexes,
  onSelectCard,
  setSelectedJokerNumber,
  selectedJokerNumber,
  isCurrent,
  endTurn,
  playCard,
  setSelectedCardsIndexes,
}: HandProps) {
  const selectedCardsNames = selectedCardsIndexes.map((index) => {
    return cards[index];
  });

  const isSomeSpecialCardSelected = selectedCardsNames.some((cardName) => SPECIAL_CARDS_NAMES.includes(cardName));
  const isSomeCardSelected = selectedCardsIndexes.length > 0;
  const isMaxCardSelected = selectedCardsIndexes.length >= MAX_SELECTED_CARDS;
  const isJokerSelected = selectedCardsNames.includes("Joker");
  const containerClasses = `${styles.container} ${isCurrent ? styles.current : ""}`;

  return (
    <>
      {isJokerSelected && <JokerWheel onSelect={setSelectedJokerNumber} selectedNumber={selectedJokerNumber} />}
      <div className={containerClasses}>
        <Button disabled={false}>{playerName}</Button>
        <div className={styles.hand}>
          <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", width: "6rem", gap: "0.5rem" }}>
            <Card isDisabled={true} isSelected={false} name={playerStack.toString()} className={styles.smallCard} />
            <Card isDisabled={true} isSelected={false} name={playerScore.toString()} className={styles.smallCard} />
            {isPunished && <Card isDisabled={true} isSelected={false} name="Punish" className={styles.smallCard} />}
          </div>
          {cards.map((card, index) => {
            const isSpecial = SPECIAL_CARDS_NAMES.includes(card);
            const isSelected = selectedCardsIndexes.includes(index);
            return (
              <Card
                key={index}
                isSelected={isSelected}
                name={card}
                isDisabled={isMaxCardSelected || (isSpecial && isSomeCardSelected) || isSomeSpecialCardSelected}
                onClick={() => {
                  onSelectCard(index, isSelected);
                }}
              />
            );
          })}
        </div>
        <div>
          <PlayerAction
            selectedCardsIndexes={selectedCardsIndexes}
            endTurn={endTurn}
            isCurrent={isCurrent}
            play={() => {
              playCard(selectedCardsIndexes[0], selectedCardsIndexes[1], selectedJokerNumber);
              setSelectedCardsIndexes([]);
            }}
          />
        </div>
      </div>
    </>
  );
}
