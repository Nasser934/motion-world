---
name: motion-world
description: >
  Create strong progress-controlled motion for any application from generated or supplied images.
  Ask one beginner-friendly question about existing video subscriptions or preferred providers, then
  route automatically to a suitable connected, free-credit, paid, manual, or local provider. Krea
  MCP is the first probe when no provider is preferred, but only an available model with the required
  capabilities may be used. When automatic generation is unavailable, create a complete manual
  provider kit with direct official links, source images, a detailed copy-paste prompt, exact settings,
  and the expected return filename. Never hide a video inside a ZIP or build a large production package
  from a local crossfade. Validate the real provider video, then package it as scrub video, frames,
  atlas, posters, and native/web runtime integrations driven by any normalized 0...1 value.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill
---

# motion-world

Build reusable application motion, not an unexplained autoplay video or a folder of hidden assets.

```text
brief
→ compatible start/end/checkpoint images
→ real provider video or complete manual handoff
→ provider-video validation
→ target-specific motion assets
→ progress driver 0...1
→ exact visual state
```

# Non-negotiable rules

1. The host application state is the source of truth. The animation does not own business timing.
2. Ask only for missing decisions. Do not ask technical questions that can be inferred.
3. Do not ask the user to classify the intended usage.
4. Ask before any paid generation unless the user already approved a spending policy.
5. A local crossfade/interpolation is diagnostic only. Never call it a provider result or production motion.
6. Do not say “generated successfully” until a real provider video was received and validated.
7. Generate end/checkpoint frames from the approved start frame whenever possible.
8. Keep text, labels, captions, and UI native instead of baking them into scene artwork.
9. Package only the media needed by each runtime target.
10. Opening at any progress value must show the corresponding state without replaying from zero.
11. If a video exists, provide a direct user-visible link and its exact path. Never make the user search a ZIP.
12. If generation must be manual, create and link a complete manual-provider kit immediately. Never merely say “send me a video.”
13. Do not generate frames, atlases, or a large integration ZIP before the real provider video returns, unless the user explicitly requested a diagnostic prototype.

# Core runtime contract

```text
source value → ProgressDriver → clamp 0...1 → MotionRuntime → exact visual state
```

Supported drivers:

- elapsed time;
- countdown;
- completed count / target;
- scroll position;
- drag distance;
- sensor value;
- state-machine segment;
- audio playback/amplitude;
- upload/download/network progress;
- custom normalized value.

Read `references/progress-drivers.md` for formulas and edge handling.

# Beginner-first workflow

The default mode is **Auto / Balanced**. The user should not need to understand APIs, MCP, CLI,
codecs, frame rates, GOP size, atlas layout, or provider model catalogs.

## Step 0 — inspect before asking

Inspect the conversation, target repository, supplied assets, platform, progress source, aspect ratio,
safe areas, memory limits, offline needs, accessibility requirements, and expected output. Do not ask
for facts already present.

## Step 1 — ask one provider question

Ask only when no provider preference/account is already known:

> Do you already have a subscription, credits, or a preferred AI-video service? Name it, or say
> “none — choose the best for me.” I will ask before any paid generation.

Do not follow this with a catalog of technical options.

Read:

- `references/beginner-workflow.md`
- `references/provider-routing.md`
- `references/provider-catalog.json`

Use the no-spend router after probing available tools/accounts:

```bash
python3 skills/motion-world/scripts/route_provider.py \
  --available krea_mcp,vidu_api \
  --first-last \
  --allow-paid ask \
  --json
```

## Step 2 — derive the motion specification

Infer internally:

- the visual change from 0% to 100%;
- transformation type: `scene_evolution`, `world_transition`, `multi_checkpoint`, `loop`,
  `camera_flight`, `character_action`, or custom;
- canvases and target platforms;
- progress driver;
- endpoint/checkpoint count;
- camera behavior;
- duration and native output resolution;
- runtime mode per target;
- reduced-motion fallback;
- package-size and memory budget.

Do not ask a beginner to choose codecs, renderers, or frame counts.

## Step 3 — create and validate `motion-project.json`

Use `references/motion-project.schema.json` and record:

- project/canvas metadata;
- provider policy and state;
- clips and approved images;
- prompts and settings;
- processing profiles;
- progress driver;
- runtime targets;
- reduced-motion behavior;
- provenance.

```bash
python3 skills/motion-world/scripts/validate_project.py motion-project.json
```

# Strong image production

Provider quality cannot repair incompatible endpoint images.

## Scene evolution

Examples: seed to tree, empty island to oasis, empty room to furnished room.

1. Generate the start frame.
2. Approve camera, anchors, safe areas, and permanent geometry.
3. Create the end frame by editing or conditioning on the approved start frame.
4. Lock horizon, camera, focal length, lighting direction, and permanent objects.
5. Add aligned intermediate checkpoints when middle states matter.

Reject an endpoint pair when camera, horizon, subject bounds, light direction, or permanent background
changes without the brief requiring it.

## World transition

Examples: castle to cyberpunk city, desert to outer space.

Geometry may deliberately transform. Do not describe this as camera-locked growth. Use a controlled
transition prompt and an eligible provider.

## Multi-checkpoint evolution

Use aligned 0%, 25%, 50%, 75%, and 100% frames when intermediate states carry meaning. Prefer genuine
multi-frame/keyframe generation instead of a two-image morph.

## Image rules

- Reuse one exact style preamble across related frames.
- Generate native compositions for materially different aspect ratios.
- Preserve identity, palette, light, camera, and anchors where required.
- No text, UI, captions, logos, or watermarks.
- Review images before spending video credits.
- Store approved images under `assets/source-images/` with dimensions and checksums.

# Provider routing

Use a suitable provider the user already has first. Otherwise:

1. Probe Krea MCP when connected; select only a model that actually supports the required inputs.
2. If no connected automatic route works, create a manual kit for Krea Web, Dreamina/Seedance, and Vidu.
3. Before paid automatic generation, ask once and then use the strongest eligible route, commonly
   Vidu API, MiniMax Hailuo-02, PixVerse, Higgsfield, or fal.
4. Use Wan 2.1 FLF2V or LTX locally only when a suitable GPU environment already exists.
5. Keep diagnostic interpolation separate and explicitly labeled.

Provider availability, pricing, credits, and model capabilities change. Probe them at execution time.
Never hard-code a promise that a provider or model is free.

## Capability gate

Confirm internally:

- first frame only versus first + last versus multiple checkpoints;
- portrait/landscape support and native resolution;
- duration;
- locked camera versus deliberate camera motion;
- reference-image support;
- authentication, account balance, and model availability;
- automatic execution versus one-step manual upload;
- downloadable MP4 and watermark status.

Reject an ineligible route even if it is popular.

## Provider states

- `PROVIDER_DISCOVERY`
- `PROVIDER_AUTH_REQUIRED`
- `PROVIDER_FREE_BALANCE_AVAILABLE`
- `PROVIDER_PAID_APPROVAL_REQUIRED`
- `PROVIDER_MODEL_UNAVAILABLE`
- `MANUAL_PROVIDER_REQUIRED`
- `PROVIDER_VIDEO_RECEIVED`
- `PROVIDER_VIDEO_REJECTED`
- `DIAGNOSTIC_PREVIEW_ONLY`
- `PRODUCTION_ASSETS_GENERATED`
- `INTEGRATION_VERIFIED`

# Automatic provider path

Before execution:

1. Probe authentication and available models.
2. Inspect the selected model schema.
3. Confirm required image inputs and prompt.
4. Estimate cost when available.
5. Ask immediately before spending if approval is required.

After execution, save and expose:

- real returned MP4;
- a direct user-visible link to the MP4;
- provider/model/task identifiers;
- raw provider response;
- cost/credits when available;
- duration, resolution, codec, and checksum.

The final user message must state where the video is and link it directly. Do not only link a ZIP.

# Manual provider path

When no connected automatic provider can execute, do not ask the user to create an unspecified video.
Run:

```bash
python3 skills/motion-world/scripts/provider_runner.py motion-project.json --handoff
```

or:

```bash
python3 skills/motion-world/scripts/create_manual_handoff.py motion-project.json
```

This must create `manual-provider-kit/` and `manual-provider-kit.zip` containing, for every clip:

- `01-start-frame.png`;
- `02-end-frame.png` when required;
- reference/checkpoint images;
- `03-copy-paste-prompt.txt` with the complete detailed prompt;
- `README_AR.md` and `README.md`;
- direct official provider links;
- exact upload order and settings;
- target aspect ratio, duration, resolution, camera, motion, and audio settings;
- exact expected return filename;
- machine-readable `manual-handoff.json`.

The response to the user must directly link:

1. the manual kit ZIP;
2. each start/end/checkpoint image;
3. the prompt text file;
4. the official provider pages;
5. any diagnostic preview separately, clearly labeled.

Then stop. Do not build production frames, atlases, runtime copies, or a large final ZIP until the real
provider MP4 is returned.

After the user uploads the MP4, place it at the declared clip output path, validate it, and resume the
pipeline automatically. Do not make the user repeat the brief.

# Diagnostic preview path

A local crossfade/interpolation may be useful only for testing layout or the progress contract.

- It requires explicit approval or `--allow-diagnostic`.
- Label it `DIAGNOSTIC_PREVIEW_ONLY`.
- Return the MP4 directly.
- Keep it lightweight.
- Do not generate 180 frames, atlases, or a production integration bundle from it by default.
- Do not imply it came from Krea, Higgsfield, Dreamina, Vidu, or another provider.

# Provider-video validation

Do not package the first returned file blindly. Validate:

- the real file exists, opens, and is linked to the user;
- duration, orientation, resolution, codec, and frame rate are plausible;
- first and last rendered frames match approved endpoints;
- no black/blank frames;
- no unintended cuts or crossfade when organic motion was requested;
- no severe camera drift in a locked scene;
- no duplication, disappearance, melting, text, or watermark;
- continuous temporal motion;
- portrait output is intentionally composed rather than blindly cropped.

Reject and retry material failures. Never conceal a failed provider result behind a local crossfade.

# Turn the real video into application motion

Only after validation:

```bash
python3 skills/motion-world/scripts/prepare_motion.py \
  --input provider-output.mp4 \
  --out build/motion \
  --profiles scrub,frames,atlas,posters \
  --fps 30 \
  --frame-count 180
```

Available outputs:

1. scrub video;
2. frame sequence;
3. sprite atlas;
4. layered native assets;
5. ordinary playback video;
6. posters/checkpoints.

## Choose output automatically

- Long cinematic web/scroll scene: scrub video.
- Exact timer/counter state: frames or layered assets.
- Short component motion: atlas.
- Low-memory target: measured scrub or sparse checkpoints.
- Reduced Motion: static checkpoints or sparse crossfades.

Create target-specific distributions. Do not duplicate frames in `build/` and the final app bundle, and
do not include unused atlases.

Metadata must distinguish source FPS/frame count, scrub FPS, sampled sequence count/effective rate,
atlas dimensions/decoded cost, paths, and checksums.

# Runtime adapters

```bash
python3 skills/motion-world/scripts/install_runtime_adapters.py motion-project.json
```

Supported targets:

- SwiftUI / iOS;
- Jetpack Compose / Android;
- Flutter;
- React Native;
- Web.

Each adapter must expose the equivalent of:

```text
setProgress(value: 0...1)
setActive(active)
setReducedMotion(enabled)
```

It must clamp values, coalesce seeks, avoid duplicate business timers, restore arbitrary state,
recover after foreground/background transitions, work offline after packaging, and cache/preload
nearby frames rather than decoding the same files repeatedly on the main thread.

# Quality gates

## Visual

- compatible endpoint/checkpoint geometry;
- correct transformation type;
- stable identity, palette, lighting, and camera where required;
- no seam pop, accidental morph, duplicate object, or text artifact;
- provider first/last frames match intended endpoints.

## Runtime

- direct access at 0%, 25%, 50%, 75%, and 100%;
- no blank first display;
- no stacked seeks;
- state restoration after relaunch/backgrounding;
- reduced-motion path;
- measured package and decoded-memory sizes.

## Truthfulness and delivery

- reports/infographics come from actual metadata, not AI-drawn fake code or invented counts;
- diagnostic previews are labeled and directly linked;
- blocked provider execution is reported as blocked;
- production-ready is used only after provider validation and integration checks;
- every returned video is linked directly and named in the report;
- every manual workflow contains a detailed prompt and official provider links.

# Deliver

For repository work, implement files and run validation. For standalone work, return a complete,
target-specific ZIP only after the real provider video exists.

The final report must be simple for the user and precise internally. Include:

- approved images and direct links;
- selected provider/model or manual handoff status;
- direct link to the real or diagnostic video;
- validation result;
- target packages and integration files;
- package sizes and performance notes;
- one remaining next action, if any.

Do not dump the full provider catalog on a beginner. Show the selected route and only the next action.

# Optional examples

- `references/examples/generic-growth.motion-project.json`
- `references/examples/sukun-oasis.motion-project.json`
