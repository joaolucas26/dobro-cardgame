import { Button } from "../button";
import { Card } from "../card";
import styles from "./opponents.module.css";

type OpponentsProps = {
  name: string;
  handSize: number;
  stackSize: number;
  score: number;
  isCurrent: boolean;
  isPunished: boolean;
  OnSelect: (playerIndex?: number) => void;
};

export function Opponents({ name, handSize, stackSize, score, isCurrent, isPunished, OnSelect }: OpponentsProps) {
  const containerClasses = `${styles.opponent} ${isCurrent ? styles.current : ""}`;

  return (
    <div className={styles.container}>
      <div className={containerClasses}>
        <div className={styles.punishbutton}>
          <Button onClick={() => OnSelect()}>{`Punir ${name}`}</Button>
        </div>
        <div className={styles.opponentContainer}>
          {Array.from({ length: handSize }).map((_, index) => (
            <Card key={index} isDisabled={true} name="" isSelected={false} className={styles.smallCard} />
          ))}
        </div>
        <div className={styles.info}>
          <Card isDisabled={true} name={String(stackSize)} isSelected={false} className={styles.smallCard} />
          <Card isDisabled={true} name={String(score)} isSelected={false} className={styles.smallCard} />
          {isPunished && <Card isDisabled={true} name="Punish" isSelected={false} className={styles.smallCard} />}
        </div>
      </div>
    </div>
  );
}
