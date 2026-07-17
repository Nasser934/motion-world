---
name: motion-world
description: >
  Create strong progress-controlled motion for any application from generated or supplied images.
  Ask one beginner-friendly question about the user's existing video subscriptions or preferred
  provider, then route automatically to a suitable connected, free-credit, paid, manual, or local
  provider. Krea MCP is the first probe when no provider is preferred, but it is used only when an
  available model satisfies the clip. Generate aligned endpoint or checkpoint images, validate the
  real provider video, then package it as scrub video, frame sequence, sprite atlas, posters, and
  native/web runtime integrations driven by time, countdown, counter, scroll, drag, sensor, state,
  audio, network progress, or any normalized 0...1 value. Supports SwiftUI, Android Compose,
  Flutter, React Native, and Web. Sukun is only an optional example.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill
---

# motion-world

Build reusable application motion, not a one-off autoplay video.

```text
brief
→ compatible start/end/checkpoint images
→ suitable real video provider
→ validated provider video
→ target-specific motion assets
→ progress driver 0...1
→ exact visual state
```

## Non-negotiable rules

1. The user's application state is the source of truth. The animation never owns business timing.
2. Ask only for missing decisions. Do not ask technical questions that can be inferred.
3. Do not ask the user to classify the intended usage. Keep provenance and terms checks internal;
   surface them only when they create a concrete blocker.
4. Ask before any paid generation unless the user already approved a spending policy.
5. A local crossfade/interpolation is diagnostic only. Never call it a provider result or production
   motion.
6. Do not say “generated successfully” until a real provider video was received and validated.
7. Generate end/checkpoint frames from the approved start frame whenever possible. Do not create
   unrelated images and pretend they are one evolving scene.
8. Text, labels, UI, and captions stay native. Do not bake them into generated scene artwork.
9. Package only the runtime media needed by each target. Avoid shipping video, frames, and atlases
   together without a reason.
10. Opening at any progress value must show the corresponding state without replaying from zero.

## Core runtime contract

```text
source value → ProgressDriver → clamped progress 0...1 → MotionRuntime → visual frame
```

Built-in drivers:

- elapsed time;
- countdown;
- completed count / target;
- scroll distance;
- drag or pan distance;
- sensor value;
- state-machine segment;
- audio playback or amplitude;
- upload, download, or network progress;
- custom callback.

Read `references/progress-drivers.md` for formulas and edge handling.

# Beginner-first workflow

The default mode is **Auto / Balanced**. The user should not need to understand APIs, MCP, CLI,
codecs, frame rates, GOP size, atlas layout, or provider model catalogs.

## Step 0 — inspect before asking

Inspect the conversation, target repository, supplied assets, target platform, current state source,
aspect ratio, safe areas, memory limits, offline needs, accessibility settings, and expected output.
Do not ask for facts already present.

## Step 1 — ask one provider question

Ask only when no existing provider preference or account is known:

> Do you already have a subscription, credits, or a preferred AI-video service? Name it, or say
> “none — choose the best for me.” I will ask before any paid generation.

This is a grouped question. Do not follow it with a catalog of technical choices.

If the user names a provider, use it first only when it can satisfy the clip. If it cannot, explain
that in one sentence and route to the next suitable option.

Read:

- `references/beginner-workflow.md`
- `references/provider-routing.md`
- `references/provider-catalog.json`

For a deterministic recommendation after probing available tools/accounts:

```bash
python3 skills/motion-world/scripts/route_provider.py \
  --available krea_mcp,vidu_api \
  --first-last \
  --allow-paid ask \
  --json
```

## Step 2 — derive the motion specification

Infer and record:

- what must visually change from 0% to 100%;
- transformation type: `scene_evolution`, `world_transition`, `multi_checkpoint`, `loop`,
  `camera_flight`, `character_action`, or custom;
- target platforms and canvases;
- progress driver;
- required endpoint/checkpoint count;
- camera behavior: locked, parallax, pan, orbit, zoom, or deliberate transition;
- duration and native output resolution;
- runtime mode per platform;
- reduced-motion fallback;
- package-size and memory budget.

Do not ask the beginner to choose output codecs or renderers. Infer them from the target.

## Step 3 — create `motion-project.json`

Use `references/motion-project.schema.json`.

The project contract records:

- project/canvas metadata;
- provider policy and selected provider;
- ordered clips;
- approved endpoint/checkpoint images;
- prompts and model settings;
- processing profiles;
- progress driver;
- runtime targets;
- reduced-motion behavior;
- provenance and actual generation state.

Validate:

```bash
python3 skills/motion-world/scripts/validate_project.py motion-project.json
```

# Strong image production

A strong video starts with compatible images. Provider quality cannot repair incompatible endpoints.

## Scene evolution

Examples: empty island to oasis, seed to tree, empty room to furnished room.

1. Generate the start frame.
2. Approve composition, anchors, safe areas, and permanent background geometry.
3. Create the end frame by editing or conditioning on the approved start frame.
4. Lock camera, horizon, lighting direction, focal length, and permanent objects.
5. Generate aligned intermediate checkpoints when the middle states have meaning.

Reject the pair when the end frame changes the camera, horizon, subject bounds, lighting direction,
or permanent background without the brief requiring it.

## World transition

Examples: castle to cyberpunk city, desert to outer space.

Geometry may deliberately transform. Do not describe this as camera-locked growth. Use prompts and
providers optimized for controlled transformation.

## Multi-checkpoint evolution

Use aligned 0%, 25%, 50%, 75%, and 100% frames when intermediate stages matter. Prefer genuine
multi-frame/keyframe generation instead of a two-image morph.

## Image rules

- Reuse one exact style preamble across related frames.
- Generate native compositions for materially different aspect ratios.
- Preserve subject identity, palette, lighting, camera, and anchors when required.
- No text, UI, logos, captions, or watermarks unless explicitly part of the artwork.
- Review and approve images before spending video credits.
- Save approved inputs under `assets/source-images/` with dimensions and checksums.

# Provider routing

Use the user's existing provider first when suitable. Otherwise:

1. Probe **Krea MCP** first when connected. It is a gateway, not a guarantee; select only an actually
   available model that supports the required start/end/checkpoint inputs.
2. If no automatic free/connected route is suitable, use the easiest strong manual route:
   Dreamina/Seedance or Vidu Web.
3. Before paid automatic generation, request approval once and then use the strongest eligible route,
   commonly Vidu API, MiniMax Hailuo-02, PixVerse API, Higgsfield, or fal API.
4. Use Wan 2.1 FLF2V or LTX locally only when a suitable GPU environment already exists.
5. Keep local diagnostic interpolation as a separate, clearly labeled preview path.

Provider availability, model access, credits, and pricing change. Probe them at execution time. Never
hard-code a claim that a provider or model is free.

## Provider capability gate

Before selection, confirm internally:

- first image only versus first + last versus multiple keyframes;
- portrait/landscape support and native resolution;
- duration;
- camera lock or camera motion;
- reference-image support;
- current model availability and account balance;
- automatic execution versus one-step manual upload;
- output download and watermark status.

Reject a provider route that cannot meet required capabilities, even if it is popular.

## Provider states

Record one of these states during the workflow:

- `PROVIDER_DISCOVERY`
- `PROVIDER_AUTH_REQUIRED`
- `PROVIDER_FREE_BALANCE_AVAILABLE`
- `PROVIDER_PAID_APPROVAL_REQUIRED`
- `PROVIDER_MODEL_UNAVAILABLE`
- `PROVIDER_VIDEO_RECEIVED`
- `PROVIDER_VIDEO_REJECTED`
- `DIAGNOSTIC_PREVIEW_ONLY`
- `PRODUCTION_ASSETS_GENERATED`
- `INTEGRATION_VERIFIED`

# Video generation

Generate a low-cost draft first when credits allow. A draft must preserve the same required input
capabilities as the final render; do not test a first/last-frame clip with a first-frame-only model.

Before execution:

1. Probe authentication and available tools.
2. Inspect the selected model schema.
3. Confirm the input images and prompt.
4. Estimate cost when available.
5. Ask immediately before a paid action when approval is required.

After execution, save:

- raw provider response;
- provider/model identifiers;
- task ID;
- returned source video;
- actual cost/credits when available;
- actual duration, resolution, codec, and checksum.

For multiple clips, use the actual last rendered frame of clip A as the start frame of clip B. Never
substitute the original still for a rendered boundary frame.

# Provider-video validation

Do not package the first returned file blindly.

Validate:

- real provider output exists and opens;
- duration, dimensions, orientation, codec, and frame rate are plausible;
- rendered first and last frames correspond to the approved endpoints;
- no black or blank frames;
- no unintended cuts;
- no severe camera drift for a locked scene;
- no unwanted object duplication, disappearance, melting, text, or watermark;
- temporal motion is continuous;
- portrait output is intentionally composed, not a blind crop.

Reject and retry when a material failure is visible. Do not hide a failed provider result behind a
local crossfade.

# Turn provider video into application motion

Use `scripts/prepare_motion.py` only after the provider video passes validation.

```bash
python3 skills/motion-world/scripts/prepare_motion.py \
  --input provider-output.mp4 \
  --out build/motion \
  --profiles scrub,frames,atlas,posters \
  --fps 30 \
  --frame-count 180
```

Available outputs:

1. **Scrub video** — short-GOP MP4/WebM whose current time follows progress.
2. **Frame sequence** — exact random-access frames for native state restoration.
3. **Sprite atlas** — packed frames for short UI motion.
4. **Layered assets** — native interpolation for artwork that can be decomposed.
5. **Playback video** — ordinary autoplay/loop when direct scrubbing is unnecessary.
6. **Posters/checkpoints** — reduced-motion, loading, and failure fallback.

## Choose output automatically

- Long cinematic web/scroll movement: scrub video.
- Exact timer/counter states: frame sequence or layered native assets.
- Short icon/component animation: sprite atlas.
- Low-memory target: sparse checkpoints or scrub video, based on measured cost.
- Reduced Motion: static checkpoints or sparse crossfades.

Create target-specific distributions. Do not duplicate frames under both `build/frames` and the final
app bundle, and do not include unused atlases in a frame-sequence target.

Metadata must distinguish:

- source duration/FPS/frame count;
- scrub-video FPS;
- sampled sequence frame count and effective sampling rate;
- atlas dimensions and decoded texture cost;
- checksums and actual paths.

# Runtime adapters

Generate selected target folders:

```bash
python3 skills/motion-world/scripts/install_runtime_adapters.py motion-project.json
```

Supported targets:

- SwiftUI / iOS;
- Jetpack Compose / Android;
- Flutter;
- React Native;
- Web.

Every adapter exposes the equivalent of:

```text
setProgress(value: 0...1)
setActive(active)
setReducedMotion(enabled)
```

It must:

- clamp invalid values;
- coalesce seeks;
- avoid duplicate business timers;
- restore the correct arbitrary state;
- recover from foreground/background changes;
- remain usable offline after packaging;
- preload/cache nearby frames rather than decoding the same file repeatedly on the main thread.

# Quality gates

## Visual

- compatible endpoint/checkpoint geometry;
- correct transformation type;
- stable identity, palette, lighting, and camera where required;
- no visible seam pop, unintended morphing, or text artifacts;
- first and last provider frames match the intended endpoints.

## Runtime

- direct access at 0%, 25%, 50%, 75%, and 100%;
- no blank first display;
- no stacked seeks during fast scroll/drag;
- state restoration after relaunch/backgrounding;
- reduced-motion path;
- measured package and decoded-memory sizes.

## Truthfulness

- reports and infographics are generated from real metadata, not AI-drawn fake code or invented
  frame counts;
- diagnostic previews are labeled diagnostic;
- blocked provider execution is reported as blocked;
- production-ready is used only after provider validation and integration checks.

# Deliver

For repository work, implement files and run validation. For standalone work, return a complete ZIP.

The final report should be simple for the user and precise internally. Include:

- approved source images;
- selected provider/model and why it was eligible;
- actual provider status and output;
- validation result;
- generated target packages;
- integration files;
- package sizes and performance notes;
- remaining blocker, if any.

Do not dump the full provider catalog on a beginner. Show the selected route, the result, and only the
next action they must perform.

# Optional examples

Examples live under `references/examples/` and are never required by the core skill.

- `generic-growth.motion-project.json`
- `sukun-oasis.motion-project.json`
