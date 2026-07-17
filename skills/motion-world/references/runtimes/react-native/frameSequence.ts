import { clampProgress } from './motionProgress';

export const frameIndex = (
  progress: number,
  frameCount: number,
  reducedMotion = false,
): number => {
  const count = Math.max(1, Math.floor(frameCount));
  let p = clampProgress(progress);
  if (reducedMotion) p = p < 0.25 ? 0 : p < 0.75 ? 0.5 : 1;
  return Math.min(count - 1, Math.max(0, Math.round(p * (count - 1))));
};

export const frameFileName = (
  progress: number,
  frameCount: number,
  reducedMotion = false,
): string => `frame_${String(frameIndex(progress, frameCount, reducedMotion)).padStart(4, '0')}.webp`;
