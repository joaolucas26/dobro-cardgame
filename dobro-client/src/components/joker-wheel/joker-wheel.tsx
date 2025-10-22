import React, { useRef, useEffect, useState } from "react";
import styles from "./joker-wheel.module.css";

// Constantes para configuração da roda
const value = 1.5;
const CANVAS_SIZE = 300 * value;
const CENTER = CANVAS_SIZE / 2;
const OUTER_RADIUS = 112 * value;
const INNER_RADIUS = 55 * value;
const NUM_SEGMENTS = 11; // 11 segmentos para os valores de 2 a 12
const SEGMENT_ANGLE = (Math.PI * 2) / NUM_SEGMENTS;
const START_ANGLE_OFFSET = -SEGMENT_ANGLE / 2;
const WRAP_AROUND_ANGLE = Math.PI * 2 - SEGMENT_ANGLE / 2;

// Cores
const PRIMARY_COLOR = "#5e239d";
const PRIMARY_ACCENT = "#311350";
const CENTER_COLOR = "#deeef1";
const TEXT_COLOR = "#e4e4e4";
const SECONDARY_COLOR = "#0f7173";
const SECONDARY_ACCENT = "#0c5455";

type JokerWheelProps = {
  selectedNumber?: number;
  onSelect: (number?: number) => void;
};

export function JokerWheel({ selectedNumber, onSelect }: JokerWheelProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [activeRegion, setActiveRegion] = useState<number | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      return;
    }

    ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

    // Loop para desenhar cada segmento e o texto correspondente
    for (let i = 0; i < NUM_SEGMENTS; i++) {
      const angle = START_ANGLE_OFFSET + i * SEGMENT_ANGLE;

      // 1. Desenha o fundo do segmento
      if (selectedNumber === i + 2) {
        ctx.fillStyle = i === activeRegion ? SECONDARY_ACCENT : SECONDARY_COLOR;
      } else {
        ctx.fillStyle = i === activeRegion ? PRIMARY_ACCENT : PRIMARY_COLOR;
      }
      ctx.beginPath();
      ctx.moveTo(CENTER, CENTER);
      ctx.arc(CENTER, CENTER, OUTER_RADIUS, angle, angle + SEGMENT_ANGLE, false);
      ctx.lineTo(CENTER, CENTER);
      ctx.fill();

      // Adicionado: Desenha as linhas divisórias
      ctx.strokeStyle = CENTER_COLOR; // Define a cor da linha
      ctx.lineWidth = 2; // Define a espessura da linha
      ctx.stroke(); // Desenha o contorno do segmento

      // 2. Desenha o número no segmento
      // Define as propriedades do texto
      ctx.fillStyle = TEXT_COLOR;
      ctx.font = "bold 28px Montserrat ";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      // Calcula a posição do texto no meio do segmento
      const textAngle = angle + SEGMENT_ANGLE / 2;
      const textRadius = INNER_RADIUS + (OUTER_RADIUS - INNER_RADIUS) / 2; // Ponto médio do raio
      const textX = CENTER + Math.cos(textAngle) * textRadius;
      const textY = CENTER + Math.sin(textAngle) * textRadius;

      // O valor a ser exibido é o índice (0-10) + 2
      const segmentValue = (i + 2).toString();

      // Desenha o texto
      ctx.fillText(segmentValue, textX, textY);
    }

    // 3. Desenha o círculo central para criar o anel
    ctx.fillStyle = CENTER_COLOR;
    ctx.beginPath();
    ctx.arc(CENTER, CENTER, INNER_RADIUS, 0, 2 * Math.PI, false);
    ctx.fill();
  }, [activeRegion]); // Redesenha quando a região ativa muda

  const handleMouseMove = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const mx = event.clientX - rect.left;
    const my = event.clientY - rect.top;

    const mouseAngle = (-Math.atan2(mx - CENTER, my - CENTER) + Math.PI * 2.5) % (Math.PI * 2);
    const mouseRadius = Math.sqrt(Math.pow(mx - CENTER, 2) + Math.pow(my - CENTER, 2));

    let regionFound: number | null = null;

    if (mouseRadius <= OUTER_RADIUS && mouseRadius >= INNER_RADIUS) {
      for (let i = 0; i < NUM_SEGMENTS; i++) {
        const angle = START_ANGLE_OFFSET + i * SEGMENT_ANGLE;
        const isOverSegment = (mouseAngle > angle && mouseAngle < angle + SEGMENT_ANGLE) || (i === 0 && mouseAngle > WRAP_AROUND_ANGLE);

        if (isOverSegment) {
          regionFound = i;
          break;
        }
      }
    }

    if (regionFound !== activeRegion) {
      setActiveRegion(regionFound);
    }
  };

  const handleMouseLeave = () => {
    setActiveRegion(null);
  };

  const handleClick = () => {
    if (activeRegion !== null) {
      const clickedValue = activeRegion + 2;
      if (clickedValue == selectedNumber) {
        onSelect();
      } else {
        onSelect(clickedValue);
      }
    }
  };

  return (
    <canvas
      className={styles.jokerWheel}
      ref={canvasRef}
      width={CANVAS_SIZE}
      height={CANVAS_SIZE}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
      style={{ cursor: "pointer", borderRadius: "50%" }}
    />
  );
}
