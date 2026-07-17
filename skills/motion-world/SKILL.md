---
name: motion-world
description: >
  Create controllable motion for any application from generated or supplied images. Use
  ChatGPT image generation, Codex image_gen, local artwork, or another image provider; send
  the approved frames to Higgsfield or any compatible video provider; post-process the video
  into a seekable scrub master, frame sequence, sprite atlas, posters, and native/web runtime
  packages. Drive the result by elapsed time, countdown, counter, scroll, drag, sensor, state
  machine, audio, network progress, or any normalized 0...1 value. Supports SwiftUI, Android
  Compose, Flutter, React Native, and Web. Sukun is only an optional example profile.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill
---

# motion-world

Build a reusable motion package, not a one-off video.

## Core contract

```text
source value -> ProgressDriver -> normalized progress 0...1 -> MotionRuntime -> visual frame
```

The media pipeline is separate:

```text
brief -> still images -> image-to-video provider -> normalized motion assets -> runtime package
```

A project may use one or more output modes:

1. **Scrub video** — short-GOP MP4/WebM whose current time follows progress.
2. **Frame sequence** — exact random-access frames for native apps and deterministic state.
3. **Sprite atlas** — compact short animation for UI components.
4. **Layered assets** — native interpolation when the artwork can be separated into layers.
5. **Playback video** — ordinary autoplay/loop when direct scrubbing is unnecessary.

Do not force one mode onto every platform.

## Step 0 — inspect before asking

Inspect supplied assets, repository, target platforms, current state source, memory limits, offline
needs, accessibility settings, and expected outputs. Do not ask for facts already present.

## Step 1 — collect only missing decisions

Capture:

- What changes visually from 0% to 100%.
- Target platforms.
- Driver: time, countdown, count, scroll, drag, sensor, state, audio, network, or custom.
- Image source: ChatGPT image generation, Codex CLI, local files, or external provider.
- Video provider: Higgsfield, generic CLI, generic HTTP API, or manual upload/download.
- Output mode per platform.
- Aspect ratios and safe areas.
- Offline requirement and package-size budget.
- Reduced-motion fallback.

Defaults:

- One normalized progress contract.
- ChatGPT/Codex for stills when available.
- Higgsfield adapter for image-to-video when installed; generic adapter otherwise.
- 9:16 for mobile, 16:9 for desktop, generated natively rather than blind crop when budget allows.
- Text stays native/HTML and is never baked into images.
- Local runtime files and no network dependency after packaging.

## Step 2 — create the project contract

Create `motion-project.json` using `references/motion-project.schema.json`.

It must define:

- project metadata and canvas profiles;
- ordered scenes or clips;
- image provider and video provider configuration;
- start/end/reference images;
- visual style preamble reused verbatim;
- motion prompts;
- processing outputs;
- progress driver;
- runtime adapters;
- reduced-motion behavior;
- licensing and provenance.

Validate:

```bash
python3 skills/motion-world/scripts/validate_project.py motion-project.json
```

## Step 3 — image production

Use the provider selected by the user.

### ChatGPT image generation

When running inside ChatGPT and image generation is available, call the image tool directly and
save each approved image into `assets/source-images/`. Generate images one at a time or in a small
cohesive batch. Do not claim an image was generated if the tool did not return it.

### Codex image generation

Use `references/providers/image/codex-image-gen.md`.

### Local/manual images

Copy approved images into the project and record dimensions, alpha, checksum, and license.

### Rules

- Reuse the exact style preamble across related images.
- Generate native compositions for materially different aspect ratios.
- Preserve camera, subject identity, lighting, palette, and geometry.
- No embedded text, UI, logos, captions, or watermarks unless the user explicitly needs them.
- Review all images before spending video credits.

## Step 4 — video generation through an adapter

Read `references/provider-contract.md`.

Supported adapter types:

- `higgsfield_cli`
- `generic_shell`
- `generic_http`
- `manual`

Run a plan first:

```bash
python3 skills/motion-world/scripts/provider_runner.py motion-project.json --plan
```

Then execute only after credentials, model support, cost, and prompt are confirmed:

```bash
python3 skills/motion-world/scripts/provider_runner.py motion-project.json --execute
```

For Higgsfield, inspect the selected model schema before generation. Do not assume every model
accepts end-image, resolution, duration, or sound flags. The adapter emits a command plan and can
run the CLI when installed.

### Seam rule for multiple clips

When chaining clips, extract the **actual last rendered frame** of clip A and use it as the next
clip's start image. For a connector, use actual rendered boundary frames as start and end images.
Never use the original still as a substitute for a rendered boundary frame.

## Step 5 — turn provider video into app motion

Use `scripts/prepare_motion.py`.

```bash
python3 skills/motion-world/scripts/prepare_motion.py \
  --input provider-output.mp4 \
  --out build/motion \
  --profiles scrub,frames,atlas \
  --fps 30 \
  --frame-count 180
```

Outputs:

- `scrub/master.mp4`: constant-frame-rate H.264, short GOP, no audio by default.
- `scrub/master.webm`: optional web output when requested.
- `frames/frame_0000.webp...`: evenly sampled frames with deterministic progress mapping.
- `atlas/atlas_*.png` and `atlas.json`: sprite sheets.
- `posters/start.webp`, `middle.webp`, `end.webp`.
- `motion-runtime.json`: duration, frame count, dimensions, checksums, and progress mapping.

### Choosing the right output

- Long cinematic camera movement: scrub video.
- Exact timer/counter states: frames or layered native assets.
- Short icon/component animation: sprite atlas.
- Low-memory fallback: sparse checkpoints plus crossfade.
- Accessibility reduced motion: start/middle/end stills or major checkpoints.

## Step 6 — attach a progress driver

Every runtime receives a value in `0...1`.

Built-in drivers:

- elapsed time;
- countdown;
- count/goal;
- scroll distance;
- drag/pan gesture;
- sensor value;
- state-machine segment;
- audio amplitude/time;
- download/upload/network progress;
- custom closure/callback.

Formulas and edge handling are in `references/progress-drivers.md`.

The runtime must support random access. Opening at 73% must render the 73% state without replaying
from zero.

## Step 7 — generate platform adapters

Generate the selected adapter folders first:

```bash
python3 skills/motion-world/scripts/install_runtime_adapters.py motion-project.json
```

Use the templates in `references/runtimes/`:

- SwiftUI
- Android Compose
- Flutter
- React Native
- Web

Each adapter must expose:

```text
setProgress(value: 0...1)
setActive(active)
setReducedMotion(enabled)
```

It must coalesce seeks, clamp invalid values, and avoid duplicate timers.

## Step 8 — quality gates

### Visual

- same subject identity, camera, palette, and lighting;
- no visible seam pop;
- no unintended morphing or text artifacts;
- first and last frames match the intended endpoints;
- portrait output is intentionally composed.

### Runtime

- direct access at 0%, 25%, 50%, 75%, and 100%;
- no blank frame on first display;
- no stacked seeks during fast scroll/drag;
- background/foreground recovery;
- offline playback after packaging;
- reduced-motion output remains understandable.

### Processing

- constant frame rate;
- verified dimensions, duration, codec, pixel format, and keyframe interval;
- checksums recorded;
- package size measured, not guessed.

## Step 9 — deliver

For repository work, implement the files. For a standalone request, return a complete skill folder
or ZIP.

Report:

- image source and generated/approved inputs;
- video provider, model, prompts, and job outputs;
- generated runtime profiles;
- platform adapters;
- validation commands and results;
- package sizes;
- credentials, provider credits, or platform limitations that remain.

## Optional examples

Examples live under `references/examples/`. They are never required by the core skill.

- `generic-growth.motion-project.json`
- `sukun-oasis.motion-project.json`
