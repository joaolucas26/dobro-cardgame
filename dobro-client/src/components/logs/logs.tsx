import styles from "./logs.module.css";

type LogsProps = {
  logs: string[];
};

export const Logs = ({ logs }: LogsProps) => {
  return (
    <>
      <ul className={styles.logs}>
        {logs.map((log, index) => {
          return <li key={index}>{log}</li>;
        })}
      </ul>
    </>
  );
};
