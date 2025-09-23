type JokerNumbersProps = {
  selectedNumber?: number;
  onSelect: (number?: number) => void;
};

const LIST_JOKER_NUMBER = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
export function JokerNumbers({ selectedNumber, onSelect }: JokerNumbersProps) {
  return (
    <div>
      {LIST_JOKER_NUMBER.map((number) => {
        return (
          <button
            onClick={() => {
              if (selectedNumber == number) {
                onSelect();
              } else {
                onSelect(number);
              }
            }}
            disabled={Boolean(selectedNumber && selectedNumber != number)}
          >
            {number}
          </button>
        );
      })}
    </div>
  );
}
