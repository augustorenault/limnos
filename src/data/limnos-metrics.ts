/**
 * Métricas da home: média linear desde 01/01/1991.
 * Os totais abaixo correspondem a 30 anos de operação; o valor atual
 * cresce continuamente à mesma taxa média.
 */
export const LIMNOS_METRICS_START_MS = new Date('1991-01-01T00:00:00-03:00').getTime();

const THIRTY_YEARS_SEC = 30 * 365.25 * 24 * 60 * 60;

export const LIMNOS_METRICS_TOTALS_30Y = {
  clientes: 1_000,
  amostras: 1_200_000,
  analises: 4_500_000,
} as const;

export const LIMNOS_METRICS_RATES_PER_SEC = {
  clientes: LIMNOS_METRICS_TOTALS_30Y.clientes / THIRTY_YEARS_SEC,
  amostras: LIMNOS_METRICS_TOTALS_30Y.amostras / THIRTY_YEARS_SEC,
  analises: LIMNOS_METRICS_TOTALS_30Y.analises / THIRTY_YEARS_SEC,
} as const;

export type LiveMetrics = {
  clientes: number;
  amostras: number;
  analises: number;
};

export function getLiveMetrics(at = Date.now()): LiveMetrics {
  const elapsedSec = Math.max(0, (at - LIMNOS_METRICS_START_MS) / 1000);
  return {
    clientes: Math.floor(LIMNOS_METRICS_RATES_PER_SEC.clientes * elapsedSec),
    amostras: Math.floor(LIMNOS_METRICS_RATES_PER_SEC.amostras * elapsedSec),
    analises: Math.floor(LIMNOS_METRICS_RATES_PER_SEC.analises * elapsedSec),
  };
}

/** Duração alvo da animação do numscroller por métrica (ms). */
export const METRICS_SCROLL_TARGET_MS = {
  clientes: 1_200,
  amostras: 2_000,
  analises: 2_500,
} as const;

/** Configura data-delay / data-increment para a duração alvo no numscroller. */
export function getMetricsScrollerConfig(max: number, targetMs = 2500, steps = 100) {
  const increment = Math.max(1, Math.floor(max / steps));
  const delay = Math.max(1, Math.ceil((targetMs * increment) / 1000));
  return { increment, delay };
}

export function formatMetric(n: number): string {
  return n.toLocaleString('pt-BR');
}
