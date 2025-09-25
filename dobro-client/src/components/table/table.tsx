import { Card } from "../card";
import styles from "./table.module.css";

type TableProps = {
  stackSize: number;
  currentRound: number;
  drawCard: () => void;
  stackTop: number;
  lastPlayedCards: string[];
  reversed: boolean;
};

export function Table({ drawCard, stackTop, lastPlayedCards, reversed, stackSize, currentRound }: TableProps) {
  return (
    <div className={styles.tableTop}>
      <Card isDisabled={true} name={stackSize.toString()} isSelected={false} className={styles.smallCard} />
      <Card onClick={drawCard} isDisabled={false} name="+1" isSelected={false} />
      <div className={styles.cardsInTableTop}>
        <Card className={styles.tableTopCenterCard} isDisabled={false} name={stackTop.toString()} isSelected={false} />
        <div className={styles.tableTopPlayedCard}>
          {lastPlayedCards.map((card) => {
            return <Card isDisabled={true} name={card} isSelected={false} />;
          })}
        </div>
      </div>
      <Card isDisabled={false} name={reversed ? "directionRight" : "directionLeft"} isSelected={false} />
      <Card isDisabled={true} name={currentRound.toString()} isSelected={false} className={styles.smallCard} />
    </div>
  );
}
