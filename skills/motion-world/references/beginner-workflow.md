# Beginner workflow

Motion World should feel like one request, not a media-engineering course.

## What the user does

1. Describes the visual change and where it will be used.
2. Answers one provider question if no existing provider is known.
3. Approves the generated endpoint images.
4. Approves a paid generation only when required.
5. Receives the integrated package.

## What the skill does automatically

- inspects the target repository and assets;
- infers aspect ratio, resolution, safe area, driver, and runtime mode;
- generates compatible endpoint/checkpoint images;
- retries image alignment before spending video credits;
- probes connected provider tools and account capabilities;
- selects the strongest eligible provider route;
- creates draft motion, validates it, and retries when needed;
- packages scrub video, frames, atlas, or posters only when useful;
- generates platform code;
- verifies direct state restoration and reduced motion;
- creates a data-driven report from actual files and metadata.

## Minimal conversation

Recommended opening:

> I found the target platform and motion source. Do you already have a subscription, credits, or a preferred AI-video service? Name it, or say “none — choose the best for me.” I will ask before any paid generation.

After the answer, do not present a provider comparison table unless the selected route fails. State the recommendation in one sentence and continue.

## Default technical decisions

- **Mode:** Auto / Balanced.
- **Endpoint creation:** edit or condition from the approved start frame.
- **Draft:** cheapest eligible model/profile that preserves required capabilities.
- **Final:** highest practical native resolution for the target, not an enlarged preview.
- **Text/UI:** native, never baked into generated artwork.
- **Audio:** disabled for app scrub assets unless explicitly required.
- **Offline:** runtime output is local after packaging.
- **Reduced Motion:** checkpoint posters or sparse crossfades.
- **Paid action:** ask immediately before spending when the user has not pre-approved it.

## Do not ask beginners

Do not ask them to choose:

- codec, pixel format, CRF, GOP, B-frames, or faststart;
- frame sampling rate or atlas dimensions;
- provider API versus CLI versus MCP when the skill can detect it;
- start/end versus multi-keyframe terminology when the desired visual change makes it clear;
- runtime renderer when platform and motion length determine it;
- intended usage category.

## When to interrupt

Ask only when:

- a paid generation requires approval;
- the user has two connected providers with materially different creative outcomes and no clear best choice;
- the endpoint images are visually plausible but the desired transformation is ambiguous;
- the target platform or progress source cannot be inferred;
- the provider requires a manual sign-in or upload step.

## Definition of done

The task is complete only when:

- a real provider video is present, or the result is explicitly marked diagnostic;
- endpoint fidelity and temporal stability pass;
- production metadata matches the actual files;
- the target-specific package excludes unused duplicate media;
- integration code is generated and syntactically checked;
- opening at an arbitrary progress value shows the corresponding state;
- the report distinguishes generated, validated, diagnostic, and blocked stages.
