import styles from "./button.module.css";

type ButtonProps = {
  disabled?: boolean;
  onClick?: () => void;
};

export function Button({ disabled, onClick, children }: React.PropsWithChildren<ButtonProps>) {
  return (
    <button disabled={disabled} onClick={onClick} className={styles.button}>
      {children}
    </button>
  );
}
