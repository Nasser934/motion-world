# Test report — Motion World 0.3.0

Verified on 2026-07-17.

## Repository checks

- Python syntax and bytecode compilation for all scripts.
- JSON parsing and semantic validation for the generic and Sukun example manifests.
- JavaScript syntax check for the web runtime.
- Swift parse check when `swiftc` is available.
- Provider command planning for Higgsfield CLI.
- Runtime-adapter installation paths for iOS, Android, Flutter, React Native, and Web.
- Required README media and sections.
- Local links and image references in both README files.

## End-to-end media test

The README demo was rendered at 1280×720 and processed through the included motion processor.

Passed outputs:

- H.264 MP4 demo with `yuv420p` and faststart.
- Animated GIF preview.
- Scrub MP4 with constant frame rate, short GOP, no B-frames, and no audio.
- 24 zero-based WebP frames beginning with `frame_0000.webp`.
- PNG sprite atlas and JSON frame map.
- Start, middle, and end WebP posters.
- Runtime metadata with media probe data and SHA-256 hashes.

## Commands

```bash
./scripts/verify.sh

python3 scripts/render_readme_demo.py --out docs/media

python3 skills/motion-world/scripts/prepare_motion.py \
  --input docs/media/motion-world-demo.mp4 \
  --out docs/media/demo-package \
  --profiles scrub,frames,atlas,posters \
  --fps 30 \
  --frame-count 24 \
  --frame-width 240 \
  --atlas-columns 6 \
  --atlas-max-frames 24
```

## External-provider boundary

A paid Higgsfield generation was not executed because it requires the user's authenticated account and credits. The adapter command plan, output parsing, result URL lookup, download path, and provider-response persistence were validated locally.
