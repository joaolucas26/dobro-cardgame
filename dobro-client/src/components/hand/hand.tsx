import { useState } from "react";
import { Card } from "../card";
import styles from "./hand.module.css";
import { JokerNumbers } from "../joker-number";

type HandProps = {
  cards: string[];
  selectedCardsIndexes: number[];
  onSelectCard: (index: number, isSelected: boolean) => void;
};

const SPECIAL_CARDS_NAMES = ["Reverse", "PassTurn"];
const MAX_SELECTED_CARDS = 2;

export function Hand({ cards, selectedCardsIndexes, onSelectCard }: HandProps) {
  const selectedCardsNames = selectedCardsIndexes.map((index) => {
    return cards[index];
  });

  const [selectedJokerNumber, setSelectedJokerNumber] = useState<number>();
  const isSomeSpecialCardSelected = selectedCardsNames.some((cardName) => SPECIAL_CARDS_NAMES.includes(cardName));
  const isSomeCardSelected = selectedCardsIndexes.length > 0;
  const isMaxCardSelected = selectedCardsIndexes.length >= MAX_SELECTED_CARDS;
  const isJokerSelected = selectedCardsNames.includes("Joker");

  return (
    <div className={styles.hand}>
      {isJokerSelected && <JokerNumbers onSelect={setSelectedJokerNumber} selectedNumber={selectedJokerNumber} />}
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
  );
}
