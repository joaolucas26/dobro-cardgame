import styles from "./card.module.css";

type CardProps = {
  isSelected: boolean;
  onClick: () => void;
  name: string;
  isDisabled: boolean;
};

const cardNameMap: Record<string, string> = {
  Joker: "J",
  PassTurn: "->",
  Reverse: "<->",
};

export function Card({ isSelected, onClick, name, isDisabled }: CardProps) {
  return (
    <button disabled={!isSelected && isDisabled} onClick={onClick} className={styles.card} data-selected={isSelected}>
      {cardNameMap[name] || name}
    </button>
  );
}
