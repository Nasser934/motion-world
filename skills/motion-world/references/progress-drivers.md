# Progress drivers

All drivers output a clamped number from 0 to 1.

## Time elapsed

```text
progress = clamp((now - startTime) / (endTime - startTime), 0, 1)
```

## Countdown

```text
progress = clamp(1 - remaining / total, 0, 1)
```

## Count toward goal

```text
progress = clamp((current - minimum) / (goal - minimum), 0, 1)
```

## Scroll

```text
progress = clamp((scrollOffset - startOffset) / scrollDistance, 0, 1)
```

## Drag or pan

```text
progress = clamp((translation - minimumTranslation) / range, 0, 1)
```

## Sensor or metric

Normalize a known safe input range. Apply smoothing only to presentation; do not change the stored
business value.

## State machine

Map each state to a segment, then interpolate local progress inside the segment:

```text
global = segmentStart + localProgress * segmentLength
```

## Rules

- Guard zero and invalid ranges.
- Clamp NaN and infinity.
- Restore from domain state after relaunch.
- Do not create a second business timer inside the renderer.
- Pause ambient work when inactive, but preserve progress identity.
- Support direct random access.
