# Changelog

## 0.4.1 — 2026-07-17

- Added `create_manual_handoff.py` to produce a complete manual-provider kit with source images, detailed copy-paste prompts, official Krea/Dreamina/Vidu links, exact settings, and expected MP4 filenames.
- Added `provider_runner.py --handoff` and made manual provider planning create the handoff kit automatically.
- Requires direct user-visible links to every returned MP4; a video hidden inside a ZIP no longer counts as delivered.
- Blocks local crossfade/interpolation from being executed as production output unless `--allow-diagnostic` is explicitly supplied.
- Prevents large frames/atlas/runtime packages from being generated before the real provider MP4 returns.
- Added the `MANUAL_PROVIDER_REQUIRED` state and Krea manual provider route.

## 0.4.0 — 2026-07-17

- Added a beginner-first provider question and automatic capability-based routing.
- Uses the user's existing subscription or preferred provider first when it can satisfy the clip.
- Probes Krea MCP first when no provider is preferred, without assuming that every model is available or free.
- Added routing references for Dreamina, Vidu, MiniMax Hailuo, PixVerse, fal, Wan 2.1 FLF2V, and LTX.
- Added an explicit paid-approval policy and diagnostic-versus-production generation states.
- Added strong endpoint alignment, transformation-type, and real provider-video validation rules.
- Removed the intended-usage-category question from the user workflow.
- Added a deterministic no-spend provider router and repository tests for the beginner default.

## 0.3.0 — 2026-07-17

- Rebuilt the root README as a full product and integration guide.
- Added Arabic README.
- Added an actual generated demo in GIF and MP4 formats.
- Added start, middle, end, and sprite-atlas media produced by the motion processor.
- Added architecture and output-format diagrams.
- Added repository verification script and GitHub Actions workflow.
- Added contribution and security guidance.

## 0.2.0 — 2026-07-17

- Made the skill provider-agnostic and independent from Sukun.
- Added Higgsfield, generic shell, manual, and HTTP provider contracts.
- Added scrub video, frame sequence, sprite atlas, poster, and runtime metadata processing.
- Added runtime references for iOS, Android, Flutter, React Native, and Web.
- Added time, countdown, count, scroll, drag, sensor, state, audio, network, and custom progress drivers.
