# Image prompt system

Keep one style preamble byte-for-byte identical across all related images.

## Base structure

```text
[STYLE PREAMBLE]
[PALETTE AND LIGHTING]
[CAMERA AND COMPOSITION]
Subject: [THE EXACT SCENE OR ENDPOINT]
No text, letters, numbers, captions, logos, UI, phone frame, or watermark.
```

## Start/end frame pair

When a video provider supports start and end images, generate a pair that preserves:

- subject identity;
- camera and focal length;
- horizon and anchor;
- palette and lighting direction;
- geometry that should not morph;
- enough visual change to justify motion.

## Native aspect ratios

Generate a new composition for portrait and landscape when important content would be lost by crop.
Do not merely extend a background around a landscape image and call it a portrait render.

## Review before video

Reject stills with:

- changed subject identity;
- inconsistent camera;
- embedded text;
- mismatched perspective;
- missing limbs/parts;
- accidental extra objects;
- poor safe-area placement.
