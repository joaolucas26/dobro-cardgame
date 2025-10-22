import type { ReactElement } from "react";
import styles from "./card.module.css";
import { SlActionRedo, SlReload } from "react-icons/sl";
import { BsArrowClockwise, BsArrowCounterclockwise } from "react-icons/bs";
import { TbJoker } from "react-icons/tb";
import { FaExclamation } from "react-icons/fa";

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
  directionRight: <BsArrowClockwise />,
  directionLeft: <BsArrowCounterclockwise />,
  Punish: <FaExclamation />,
};

export function Card({ isSelected, onClick, name, isDisabled, className }: CardProps) {
  return (
    <button disabled={!isSelected && isDisabled} onClick={onClick} className={`${styles.card} ${className}`} data-selected={isSelected}>
      {cardNameMap[name] || name}
    </button>
  );
}
