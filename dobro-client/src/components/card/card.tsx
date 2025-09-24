import type { ReactElement } from "react";
import styles from "./card.module.css";
import { SlReload } from "react-icons/sl";
import { SlActionRedo } from "react-icons/sl";
import { TbJoker } from "react-icons/tb";

type CardProps = {
  isSelected: boolean;
  onClick?: () => void;
  name: string;
  isDisabled: boolean;
  className?: string;
};

const cardNameMap: Record<string, string | ReactElement> = {
  Joker: <TbJoker />,
  PassTurn: <SlActionRedo />,
  Reverse: <SlReload />,
};

export function Card({ isSelected, onClick, name, isDisabled, className }: CardProps) {
  return (
    <button disabled={!isSelected && isDisabled} onClick={onClick} className={`${styles.card} ${className}`} data-selected={isSelected}>
      {cardNameMap[name] || name}
    </button>
  );
}
