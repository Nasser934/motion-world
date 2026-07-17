# Provider routing — beginner-first, quality-first

Updated: 2026-07-17.

The user should not need to understand model catalogs, API schemas, codecs, frame extraction, or runtime packaging. Motion World asks one compact provider question, probes the environment, chooses a suitable route, and only interrupts again before an irreversible paid action or when no route can satisfy the clip.

## The only provider question

Ask this only when the answer is not already known:

> Do you already have a subscription, credits, or a preferred AI-video service? Name it, or say “none — choose the best for me.” I will ask before any paid generation.

Do not ask the user to classify the intended usage. Keep licensing/provenance checks internal and surface them only when they create a concrete blocker.

## Routing order

1. **Use the user's existing provider first** when it supports the required inputs, aspect ratio, duration, and output quality.
2. If there is no preference, **probe Krea MCP first** because it offers a beginner-friendly agent connection. Krea is a gateway, not a guarantee: select only an actually available model that satisfies the clip.
3. If no connected automatic route is suitable, use the easiest strong manual route:
   - Dreamina / Seedance for first/last-frame and multi-frame work.
   - Vidu Web for first/last-frame and multi-frame work when credits are available.
4. If the user approves a paid automatic route:
   - Vidu API for first/last-frame or multi-frame control.
   - MiniMax Hailuo-02 for low-cost automatic first/last-frame generation.
   - PixVerse API when several checkpoints are needed.
   - Higgsfield when the user already has access or prefers it.
   - fal API when a model marketplace or benchmark layer is useful.
5. Use local open models only when an appropriate GPU environment already exists:
   - Wan 2.1 FLF2V for exact first/last-frame generation.
   - LTX for multiple keyframes and advanced control.
6. A local interpolation or crossfade is **diagnostic only**. Never label it as provider-generated or production-ready.

## Capability gate before provider choice

Derive these requirements from the brief; do not ask the user technical questions unless they are truly missing:

- first image only, first + last image, or multiple keyframes;
- portrait, landscape, square, and safe area;
- duration and native resolution;
- camera lock versus deliberate camera travel;
- subject/scene consistency;
- audio requirement;
- automatic versus one-step manual execution;
- connected account, available balance, and model availability.

A provider may be famous and still be wrong for a clip. Reject any route that cannot satisfy required capabilities.

## Beginner behavior

Default to **Auto / Balanced**:

- infer technical settings from the target platform;
- create low-cost drafts before a final expensive render when credits allow;
- present one recommended route, not a long catalog;
- keep alternatives hidden unless the first route is unavailable;
- give one-click or copy-paste instructions for any manual step;
- resume automatically when the returned MP4 is uploaded;
- produce the runtime package and integration without asking the user to choose codecs, GOP size, frame count, or atlas geometry.

## Quality routing by clip type

### Scene evolution

Examples: empty island to oasis, empty room to furnished room, seed to tree.

- Generate the end frame by editing or conditioning on the approved start frame.
- Lock camera, horizon, anchor bounds, lighting direction, and permanent background geometry.
- Prefer first/last-frame providers.

### World transition

Examples: castle to cyberpunk city, desert to outer space.

- The scene is intentionally transformed into another world.
- Do not describe it as camera-locked growth.
- A provider with strong transformation adherence may be selected even when geometry changes.

### Multi-checkpoint evolution

Examples: 0%, 25%, 50%, 75%, 100% growth.

- Generate aligned checkpoints.
- Prefer Vidu multi-frame, Dreamina multi-frame, PixVerse multi-keyframe, or LTX local.
- Do not rely on a two-image morph when the middle states matter semantically.

## Strong-output pipeline

1. Inspect the target app/site and derive the motion contract.
2. Generate the start frame.
3. Generate the end/checkpoint frames from the approved start frame, not as unrelated prompts.
4. Run the image-alignment gate. Regenerate failed endpoints before video generation.
5. Route to a suitable provider.
6. Generate a draft and validate actual provider output.
7. Compare the rendered first and last frames with the approved endpoints.
8. Reject cuts, black frames, watermarks, text artifacts, severe morphing, and camera drift.
9. Produce the final render only after the draft passes.
10. Package only the runtime format needed by each target.
11. Verify direct random access at 0%, 25%, 50%, 75%, and 100%.

## Provider states

Use explicit machine-readable states:

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

Never say “motion generated successfully” unless a real provider video was received and passed validation.

## Current official capability references

Provider availability and pricing change. Probe them at execution time and use official sources:

- Krea pricing and MCP: https://www.krea.ai/pricing and https://www.krea.ai/mcp
- Vidu pricing/API: https://www.vidu.com/pricing and https://platform.vidu.com/docs/pricing
- MiniMax video API: https://platform.minimax.io/docs/guides/video-generation
- Dreamina first/last frame: https://dreamina.capcut.com/resource/first-last-frame
- Wan 2.1 FLF2V: https://github.com/Wan-Video/Wan2.1
- LTX official repository: https://github.com/Lightricks/LTX-Video
