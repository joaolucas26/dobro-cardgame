import { Button } from "./button";

type PlayerActionProps = {
  selectedCardsIndexes: number[];
  isCurrent: boolean;
  endTurn: () => void;
  play: () => void;
};

const MIN_SELECTED_CARDS = 1;

export function PlayerAction({ selectedCardsIndexes, isCurrent, endTurn, play }: PlayerActionProps) {
  return (
    <div>
      <Button disabled={selectedCardsIndexes.length < MIN_SELECTED_CARDS || !isCurrent} onClick={play}>
        Jogar
      </Button>
      <Button onClick={endTurn} disabled={!isCurrent}>
        Encerrar Turno
      </Button>
    </div>
  );
}
