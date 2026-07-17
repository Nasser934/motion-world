export const clampProgress = (value: number): number =>
  Number.isFinite(value) ? Math.min(1, Math.max(0, value)) : 0;

export const elapsedProgress = (nowMs: number, startMs: number, endMs: number): number => {
  const duration = endMs - startMs;
  if (duration <= 0) return nowMs >= endMs ? 1 : 0;
  return clampProgress((nowMs - startMs) / duration);
};

export const countdownProgress = (remaining: number, total: number): number => {
  if (total <= 0) return remaining <= 0 ? 1 : 0;
  return clampProgress(1 - remaining / total);
};

export const countProgress = (current: number, goal: number, minimum = 0): number => {
  const range = goal - minimum;
  if (range <= 0) return current >= goal ? 1 : 0;
  return clampProgress((current - minimum) / range);
};
