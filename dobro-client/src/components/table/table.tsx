import { Card } from "../card";
import styles from "./table.module.css";

type TableProps = {
  drawCard: () => void;
  stackTop: number;
  lastPlayedCards: string[];
  reversed: boolean;
};

export function Table({ drawCard, stackTop, lastPlayedCards, reversed }: TableProps) {
  return (
    <div className={styles.tableTop}>
      <Card onClick={drawCard} isDisabled={false} name="+1" isSelected={false} />
      <div className={styles.cardsInTableTop}>
        <Card className={styles.tableTopCenterCard} isDisabled={false} name={stackTop.toString()} isSelected={false} />
        <div className={styles.tableTopPlayedCard}>
          {lastPlayedCards.map((card) => {
            return <Card isDisabled={true} name={card} isSelected={false} />;
          })}
        </div>
      </div>
      {}
      <Card isDisabled={false} name={reversed ? "directionRight" : "directionLeft"} isSelected={false} />
    </div>
  );
}
