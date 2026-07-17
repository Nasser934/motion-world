# Beginner workflow

Motion World should feel like one request, not a media-engineering course or a ZIP scavenger hunt.

## What the user does

1. Describes the visual change and target application/site.
2. Answers one provider question if no preference/account is known.
3. Approves endpoint/checkpoint images.
4. Approves a paid generation only when required.
5. If no automatic provider is connected, follows one clear manual page and returns one MP4.
6. Receives the final integrated package.

## What the skill does automatically

- inspects the target repository and assets;
- infers aspect ratio, resolution, safe area, driver, and runtime mode;
- generates compatible endpoint/checkpoint images;
- retries image alignment before spending credits;
- probes connected provider tools and account capabilities;
- selects the strongest eligible route;
- generates and directly links the real provider video when automation is available;
- creates a complete manual-provider kit when automation is unavailable;
- validates the real returned video;
- packages only useful scrub video, frames, atlas, or posters;
- generates platform code;
- verifies state restoration and reduced motion;
- creates a report from actual files and metadata.

## Minimal conversation

Recommended opening:

> I found the target platform and motion source. Do you already have a subscription, credits, or a preferred AI-video service? Name it, or say “none — choose the best for me.” I will ask before any paid generation.

After the answer, do not display a provider comparison table unless the selected route fails. State one recommendation and continue.

## Default technical decisions

- **Mode:** Auto / Balanced.
- **Endpoint creation:** edit or condition from the approved start frame.
- **Draft:** cheapest eligible profile preserving required capabilities.
- **Final:** highest practical native target resolution, not an enlarged preview.
- **Text/UI:** native, never baked into generated artwork.
- **Audio:** disabled for application scrub assets unless required.
- **Offline:** runtime output is local after packaging.
- **Reduced Motion:** checkpoint posters or sparse crossfades.
- **Paid action:** ask immediately before spending without prior approval.
- **Manual fallback:** create `manual-provider-kit.zip` immediately.
- **Diagnostic fallback:** one lightweight, directly linked MP4 only after explicit approval.

## Do not ask beginners

Do not ask them to choose:

- codec, pixel format, CRF, GOP, B-frames, or faststart;
- frame sampling rate or atlas dimensions;
- API versus CLI versus MCP when the skill can detect it;
- start/end versus multi-keyframe terminology when the visual goal makes it clear;
- runtime renderer when platform and motion length determine it;
- intended usage category;
- where the video is hidden inside a generated ZIP;
- what prompt or settings to invent for a manual provider.

## Manual fallback contract

If no connected provider can execute, the skill must run:

```bash
python3 skills/motion-world/scripts/provider_runner.py motion-project.json --handoff
```

Then provide direct links to:

1. `manual-provider-kit.zip`;
2. start/end/checkpoint images;
3. the detailed copy-paste prompt;
4. Krea, Dreamina, and Vidu official pages;
5. the expected MP4 filename.

The guide must explain upload order, aspect ratio, duration, resolution, camera, motion strength, audio, download format, and return filename. The skill then stops until the real MP4 returns.

Do not build production frames, atlases, runtime copies, or a large final ZIP from a local crossfade.

## Direct video delivery contract

Whenever a video exists:

- state whether it is real provider output or diagnostic;
- provide a direct user-visible link to the MP4;
- state its exact path, duration, dimensions, and size;
- keep any ZIP as a secondary download, not the only way to find the video.

## When to interrupt

Ask only when:

- paid generation requires approval;
- two connected providers have materially different creative outcomes and no clear best route;
- the desired transformation is genuinely ambiguous;
- target platform or progress source cannot be inferred;
- a provider requires sign-in or one manual upload step.

## Definition of done

The task is complete only when:

- a real provider video is present, or the result is explicitly marked diagnostic;
- every video is directly linked and clearly identified;
- endpoint fidelity and temporal stability pass;
- metadata matches actual files;
- the target package excludes unused duplicate media;
- integration code is generated and checked;
- arbitrary progress opens at the corresponding state;
- the report distinguishes generated, validated, diagnostic, manual-required, and blocked stages.
