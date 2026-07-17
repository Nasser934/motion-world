# Provider routing — beginner-first, quality-first

Updated: 2026-07-17.

The user should not need to understand model catalogs, APIs, codecs, frame extraction, or runtime packaging. Motion World asks one compact provider question, probes the environment, chooses a suitable route, and only interrupts before a paid action, sign-in/manual upload, or when no route can satisfy the clip.

## The only provider question

Ask only when the answer is not already known:

> Do you already have a subscription, credits, or a preferred AI-video service? Name it, or say “none — choose the best for me.” I will ask before any paid generation.

Do not ask the user to classify the intended usage.

## Routing order

1. Use the user's existing provider first when it supports the required inputs, ratio, duration, and output quality.
2. If there is no preference, probe Krea MCP first. Krea is a gateway, not a guarantee; use only an actually available eligible model.
3. If no connected automatic route is suitable, immediately create a manual-provider kit containing Krea Web, Dreamina/Seedance, and Vidu instructions.
4. If the user approves a paid automatic route, prefer the strongest eligible route such as Vidu API, MiniMax Hailuo-02, PixVerse, Higgsfield, or fal.
5. Use Wan 2.1 FLF2V or LTX locally only when a suitable GPU environment already exists.
6. A local interpolation/crossfade is diagnostic only and must never be presented as provider-generated or production-ready.

## Capability gate

Derive internally:

- first frame only, first + last, or multiple keyframes;
- portrait/landscape/square and safe area;
- duration and native resolution;
- locked camera versus deliberate camera travel;
- consistency and reference requirements;
- audio requirement;
- automatic versus one-step manual execution;
- account connection, balance, and model availability;
- direct MP4 download and watermark status.

Reject any route that cannot satisfy required capabilities.

## Beginner behavior

Default to Auto / Balanced:

- infer technical settings from the target;
- create low-cost drafts before expensive finals when possible;
- show one recommended route, not a long catalog;
- keep alternatives hidden unless needed;
- provide one-click or copy-paste manual steps;
- resume automatically when the MP4 is uploaded;
- never ask the user to invent a prompt or locate a hidden video;
- never package frames/atlas before a real provider MP4 returns.

## Manual-provider handoff

When automatic execution is unavailable, run:

```bash
python3 skills/motion-world/scripts/provider_runner.py motion-project.json --handoff
```

The generated kit must include:

- start/end/checkpoint images;
- a complete provider-ready prompt;
- Arabic and English instructions;
- official Krea, Dreamina, and Vidu links;
- upload order and exact settings;
- the expected returned MP4 filename;
- `manual-handoff.json`.

The user response must directly link the kit ZIP, every input image, the prompt file, and official provider pages. Then stop until the real MP4 returns.

Never respond only with “send me the video.”

## Direct video delivery

Whenever any MP4 exists:

- directly link the MP4;
- identify it as provider output or diagnostic;
- state its exact path, dimensions, duration, and size;
- keep the full ZIP secondary.

A video buried in a ZIP does not count as delivered.

## Quality routing by clip type

### Scene evolution

Examples: empty island to oasis, seed to tree, empty room to furnished room.

- Generate the end frame by editing/conditioning on the approved start frame.
- Lock camera, horizon, anchor bounds, light direction, and permanent background.
- Prefer first/last-frame providers.

### World transition

Examples: castle to cyberpunk city, desert to outer space.

- The scene intentionally transforms.
- Do not describe it as camera-locked growth.
- Select a provider with strong transformation adherence.

### Multi-checkpoint evolution

Examples: 0%, 25%, 50%, 75%, 100%.

- Generate aligned checkpoints.
- Prefer Vidu multi-frame, Dreamina multi-frame, PixVerse multi-keyframe, or LTX local.
- Do not rely on a two-image morph when middle states matter.

## Strong-output pipeline

1. Inspect the target and derive the motion contract.
2. Generate the start frame.
3. Generate end/checkpoint frames from the approved start frame.
4. Run image alignment and regenerate failed endpoints.
5. Route to a provider.
6. If automatic execution is unavailable, generate the manual kit and stop.
7. Generate a draft and directly expose the MP4.
8. Compare provider first/last frames to approved endpoints.
9. Reject cuts, black frames, watermark, text, severe morphing, and camera drift.
10. Produce the final render after draft approval.
11. Package only the runtime format needed by each target.
12. Verify random access at 0%, 25%, 50%, 75%, and 100%.

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

Never say “motion generated successfully” unless a real provider video was received, directly linked, and validated.

## Official references

Availability and pricing change; probe them at execution time:

- Krea video: https://www.krea.ai/features/ai-video-generator
- Krea MCP: https://www.krea.ai/mcp
- Dreamina first/last frame: https://dreamina.capcut.com/resource/first-last-frame
- Dreamina frames to video: https://dreamina.capcut.com/create/frames-to-video
- Vidu video: https://www.vidu.com/ai-video-generator
- Vidu Start/End API: https://platform.vidu.com/docs/start-end-to-video
- MiniMax video API: https://platform.minimax.io/docs/guides/video-generation
- Wan 2.1 FLF2V: https://github.com/Wan-Video/Wan2.1
- LTX official repository: https://github.com/Lightricks/LTX-Video
