export function clampProgress(value) {
  const n = Number(value);
  return Number.isFinite(n) ? Math.min(1, Math.max(0, n)) : 0;
}

export class ScrubVideoRuntime {
  constructor(video, { duration = null, reducedMotion = false } = {}) {
    this.video = video;
    this.duration = duration;
    this.reducedMotion = reducedMotion;
    this.pending = null;
    this.seeking = false;
    video.muted = true;
    video.playsInline = true;
    video.preload = 'auto';
    video.addEventListener('seeked', () => {
      this.seeking = false;
      if (this.pending !== null) {
        const p = this.pending;
        this.pending = null;
        this.setProgress(p);
      }
    });
  }

  setReducedMotion(enabled) { this.reducedMotion = Boolean(enabled); }
  setActive(active) { if (!active) this.video.pause(); }

  setProgress(value) {
    let p = clampProgress(value);
    if (this.reducedMotion) p = p < 0.25 ? 0 : (p < 0.75 ? 0.5 : 1);
    const duration = this.duration || this.video.duration;
    if (!Number.isFinite(duration) || duration <= 0) return;
    if (this.seeking) { this.pending = p; return; }
    this.seeking = true;
    const epsilon = 1 / 120;
    this.video.currentTime = Math.min(Math.max(0, duration * p), Math.max(0, duration - epsilon));
  }
}

export class FrameSequenceRuntime {
  constructor(img, { pattern, frameCount, reducedMotion = false }) {
    this.img = img;
    this.pattern = pattern;
    this.frameCount = Math.max(1, frameCount);
    this.reducedMotion = reducedMotion;
    this.lastIndex = -1;
  }
  setActive(_) {}
  setReducedMotion(enabled) { this.reducedMotion = Boolean(enabled); }
  setProgress(value) {
    let p = clampProgress(value);
    if (this.reducedMotion) p = p < 0.25 ? 0 : (p < 0.75 ? 0.5 : 1);
    const i = Math.min(this.frameCount - 1, Math.round(p * (this.frameCount - 1)));
    if (i === this.lastIndex) return;
    this.lastIndex = i;
    this.img.src = this.pattern.replace('{index}', String(i).padStart(4, '0'));
  }
}

export function scrollDriver({ start = 0, distance = document.documentElement.scrollHeight - innerHeight } = {}) {
  const d = Math.max(1, distance);
  return clampProgress((scrollY - start) / d);
}
