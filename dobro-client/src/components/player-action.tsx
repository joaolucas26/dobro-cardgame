import { Button } from "./button";

type PlayerActionProps = {
  selectedCardsIndexes: number[];
  handSize: number;
  isCurrent: boolean;
  drawCard: () => void;
  endTurn: () => void;
  play: () => void;
};

const MIN_SELECTED_CARDS = 1;
const MAX_HAND_SIZE = 6;

export function PlayerAction({ selectedCardsIndexes, handSize, isCurrent, drawCard, endTurn, play }: PlayerActionProps) {
  return (
    <div>
      <Button disabled={selectedCardsIndexes.length < MIN_SELECTED_CARDS || !isCurrent} onClick={play}>
        Jogar
      </Button>
      <Button onClick={drawCard} disabled={handSize >= MAX_HAND_SIZE}>
        Pescar
      </Button>
      <Button onClick={endTurn} disabled={!isCurrent}>
        Encerrar Turno
      </Button>
    </div>
  );
}
