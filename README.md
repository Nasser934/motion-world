<p align="center">
  <img src="docs/media/hero.svg" alt="Motion World — generated images to controllable application motion" width="100%" />
</p>

<p align="center">
  <a href="README_AR.md">العربية</a> ·
  <a href="#60-second-start">60-second start</a> ·
  <a href="#how-the-pipeline-works">Pipeline</a> ·
  <a href="#runtime-integration">Runtime integration</a> ·
  <a href="docs/GUIDE_AR.md">Arabic guide</a> ·
  <a href="docs/PUBLISH_AR.md">Publish to GitHub</a>
</p>

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-0.3.0-7659F4?style=flat-square" />
  <a href="https://github.com/Nasser934/motion-world/actions/workflows/verify.yml"><img alt="Verify" src="https://img.shields.io/github/actions/workflow/status/Nasser934/motion-world/verify.yml?branch=main&style=flat-square&label=verify" /></a>
  <img alt="License" src="https://img.shields.io/badge/license-MIT-63E6BE?style=flat-square" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="FFmpeg" src="https://img.shields.io/badge/FFmpeg-required-007808?style=flat-square&logo=ffmpeg&logoColor=white" />
  <img alt="Platforms" src="https://img.shields.io/badge/runtimes-iOS%20%C2%B7%20Android%20%C2%B7%20Flutter%20%C2%B7%20React%20Native%20%C2%B7%20Web-101827?style=flat-square" />
</p>

# Motion World

**Motion World turns generated or supplied images into motion that your application can control.** It can create images with ChatGPT or Codex, send approved frames to Higgsfield or another video provider, process the returned video into application-friendly assets, and generate runtime adapters for iOS, Android, Flutter, React Native, and the web.

The output is not limited to autoplay video. Your app can control the visual state using elapsed time, a countdown, a count, scroll position, drag distance, a sensor, a state machine, network progress, audio level, or any value normalized to `0...1`.

```text
source value → progress 0...1 → motion runtime → exact visual state
```

---

## See it working

<p align="center">
  <img src="docs/media/motion-world-demo.gif" alt="Motion World progress-controlled demo" width="800" />
</p>

<p align="center">
  <a href="docs/media/motion-world-demo.mp4"><strong>Open the MP4 demo</strong></a>
</p>

The preview above was built with the repository itself:

1. A source video was created.
2. `prepare_motion.py` converted it into a seekable MP4, frame sequence, sprite atlas, and fallback posters.
3. The same normalized progress value selected every state.

<table>
  <tr>
    <th align="center">0%</th>
    <th align="center">50%</th>
    <th align="center">100%</th>
  </tr>
  <tr>
    <td><img src="docs/media/demo-start.webp" alt="Motion at zero percent" /></td>
    <td><img src="docs/media/demo-middle.webp" alt="Motion at fifty percent" /></td>
    <td><img src="docs/media/demo-end.webp" alt="Motion at one hundred percent" /></td>
  </tr>
</table>

The generated sprite atlas is also included at [`docs/media/demo-atlas.png`](docs/media/demo-atlas.png), with its frame map in [`docs/media/demo-package/atlas/atlas.json`](docs/media/demo-package/atlas/atlas.json).

---

## What problem it solves

AI video tools make video files. Application interfaces need **controllable state**.

A normal video answers:

> What should play next?

An application motion runtime answers:

> What should the visual look like at exactly 37%?

That difference matters when motion represents a timer, task completion, onboarding step, fitness goal, prayer session, upload, purchase flow, educational sequence, map route, or scroll section.

Motion World separates the pipeline into five replaceable parts:

| Part | Responsibility | Replaceable? |
|---|---|---:|
| Image provider | Creates start, end, and reference frames | Yes |
| Video provider | Animates the approved frames | Yes |
| Motion processor | Converts video into runtime media | Yes |
| Runtime adapter | Displays the selected state on each platform | Yes |
| Progress driver | Maps application data to `0...1` | Yes |

---

## How the pipeline works

<p align="center">
  <img src="docs/media/architecture.svg" alt="Motion World architecture" width="100%" />
</p>

### 1. Create or supply source images

Use one source for all keyframes in a visual set to reduce style drift.

Supported paths:

- ChatGPT image generation.
- Codex `image_gen`.
- Existing product artwork.
- Local PNG, WebP, JPEG, or HEIF files.
- Any external image provider that can save files locally.

Motion World keeps user-facing text outside artwork. Text remains native SwiftUI, Compose, Flutter, React Native, or HTML.

### 2. Animate with a video provider

The included runner supports:

| Provider type | Status | Use case |
|---|---:|---|
| `higgsfield_cli` | Built in | Automated Higgsfield generation and download |
| `generic_shell` | Built in | Any provider exposed through a CLI or wrapper script |
| `manual` | Built in | Upload images yourself and place the returned file at the declared output path |
| `generic_http` | Contract included | Add an endpoint-specific wrapper for upload, polling, and download |

The skill plans provider commands before spending credits. Higgsfield commands support start images, end images, references, model selection, duration, and aspect ratio when the selected model accepts them.

### 3. Process the returned video

The processor can create:

<p align="center">
  <img src="docs/media/output-matrix.svg" alt="Motion World output formats" width="100%" />
</p>

| Output | What it contains | Best fit |
|---|---|---|
| Scrub video | Constant-frame-rate H.264 MP4, short GOP, no B-frames, faststart | Cinematic web sections and long scenes |
| Frame sequence | Zero-based WebP files such as `frame_0000.webp` | Native random access and exact state restoration |
| Sprite atlas | Packed PNG atlases plus `atlas.json` | Short UI motion with fewer file reads |
| Posters | Start, middle, and end WebP files | Reduced Motion, low-memory fallback, previews |
| Runtime metadata | Probe data, frame count, paths, and SHA-256 hashes | Integration, cache validation, diagnostics |

### 4. Install runtime adapters

The repository includes reference adapters for:

- SwiftUI / iOS.
- Jetpack Compose / Android.
- Flutter.
- React Native.
- Browser JavaScript.

### 5. Connect any progress driver

The runtime only needs one clamped value:

```text
0.0 = first visual state
0.5 = middle visual state
1.0 = final visual state
```

The application remains the source of truth. The animation does not decide when a session, task, or process has completed.

---

## 60-second start

### Requirements

- Python 3.10 or newer.
- `ffmpeg` and `ffprobe` on `PATH`.
- Pillow for sprite atlases.
- Optional: Higgsfield CLI and an authenticated account.
- Optional: Codex CLI for image generation through your ChatGPT subscription.

### Install system dependencies

<details>
<summary><strong>macOS</strong></summary>

```bash
brew install ffmpeg python
python3 -m pip install Pillow
```

</details>

<details>
<summary><strong>Ubuntu / Debian</strong></summary>

```bash
sudo apt update
sudo apt install -y ffmpeg python3 python3-pip
python3 -m pip install --user Pillow
```

</details>

<details>
<summary><strong>Windows</strong></summary>

Install Python 3.10+, install FFmpeg, add its `bin` directory to `PATH`, then run:

```powershell
py -m pip install Pillow
```

Verify:

```powershell
ffmpeg -version
ffprobe -version
py --version
```

</details>

### Install the agent skill

#### Codex and other Skills CLI agents

```bash
npx skills add Nasser934/motion-world -a codex
```

Or select an agent interactively:

```bash
npx skills add Nasser934/motion-world
```

#### Claude Code plugin

```text
/plugin marketplace add Nasser934/motion-world
/plugin install motion-world@motion-world
```

#### Manual install

```bash
git clone https://github.com/Nasser934/motion-world.git
cp -R motion-world/skills/motion-world ~/.codex/skills/
# or
cp -R motion-world/skills/motion-world ~/.claude/skills/
```

### Create a project

```bash
python3 skills/motion-world/scripts/init_project.py my-motion \
  --preset generic-cinematic
```

Generated structure:

```text
my-motion/
├── motion-project.json
├── prompts/
├── input/
├── provider-output/
├── build/
└── runtime/
```

### Validate before generation

```bash
python3 skills/motion-world/scripts/validate_project.py \
  my-motion/motion-project.json
```

### Preview provider commands without spending credits

```bash
python3 skills/motion-world/scripts/provider_runner.py \
  my-motion/motion-project.json \
  --plan
```

### Generate with the configured provider

For supported automated providers:

```bash
python3 skills/motion-world/scripts/provider_runner.py \
  my-motion/motion-project.json \
  --execute
```

For manual mode, upload the declared start/end images and prompt to your chosen platform, then save the result at the output path printed by `--plan`.

### Convert the video into runtime assets

```bash
python3 skills/motion-world/scripts/prepare_motion.py \
  --input my-motion/provider-output/source.mp4 \
  --out my-motion/build \
  --profiles scrub,frames,atlas,posters \
  --fps 30 \
  --frame-count 180
```

### Generate platform integration folders

```bash
python3 skills/motion-world/scripts/install_runtime_adapters.py \
  my-motion/motion-project.json
```

---

## The project contract

Every project is described by `motion-project.json`. The schema is located at:

```text
skills/motion-world/references/motion-project.schema.json
```

Minimal example:

```json
{
  "$schema": "../skills/motion-world/references/motion-project.schema.json",
  "version": "1.0",
  "project": {
    "id": "seed-to-tree",
    "title": "Seed to tree",
    "description": "A growth scene controlled by progress"
  },
  "imageProvider": {
    "type": "codex_image_gen"
  },
  "videoProvider": {
    "type": "higgsfield_cli",
    "model": "seedance_2_0",
    "config": {
      "aspectRatio": "9:16"
    }
  },
  "clips": [
    {
      "id": "growth",
      "promptFile": "prompts/growth.txt",
      "startImage": "input/start.png",
      "endImage": "input/end.png",
      "durationSeconds": 8,
      "output": "provider-output/source.mp4"
    }
  ],
  "processing": {
    "profiles": ["scrub", "frames", "atlas", "posters"]
  },
  "runtimes": ["ios", "android", "flutter", "react-native", "web"]
}
```

Full examples:

- [`generic-growth.motion-project.json`](skills/motion-world/references/examples/generic-growth.motion-project.json)
- [`generic-shell-provider.json`](skills/motion-world/references/examples/generic-shell-provider.json)
- [`sukun-oasis.motion-project.json`](skills/motion-world/references/examples/sukun-oasis.motion-project.json) — an optional example, not a dependency

---

## Image generation workflow

A good image-to-video result begins with compatible keyframes.

### Recommended sequence

1. Write one style preamble.
2. Generate the start frame.
3. Review composition and safe areas.
4. Generate the end frame using the approved start frame as style reference when the provider supports it.
5. Compare camera angle, focal length, subject identity, lighting, horizon, and aspect ratio.
6. Only then send the frames to the video provider.

### Image rules

- Keep the main subject inside the safe area for the target platform.
- Generate portrait and landscape compositions separately when both matter.
- Do not rely on a center crop for important mobile content.
- Keep UI text out of artwork.
- Keep start and end frame geometry compatible.
- Avoid unexplained object additions between keyframes.
- Keep one art source per visual set when possible.

Prompt guidance is in [`image-prompts.md`](skills/motion-world/references/image-prompts.md).

---

## Higgsfield integration

Set the provider type:

```json
{
  "videoProvider": {
    "type": "higgsfield_cli",
    "model": "seedance_2_0",
    "config": {
      "aspectRatio": "9:16"
    }
  }
}
```

Then inspect the plan:

```bash
python3 skills/motion-world/scripts/provider_runner.py \
  motion-project.json \
  --plan
```

The plan prints:

- Authentication preflight.
- Model schema preflight.
- One command per clip.
- Input image paths.
- Output video paths.

Execute only after reviewing cost, duration, aspect ratio, and model support:

```bash
python3 skills/motion-world/scripts/provider_runner.py \
  motion-project.json \
  --execute
```

The runner stores the provider JSON response beside the output video for diagnosis.

Higgsfield-specific notes are in [`higgsfield.md`](skills/motion-world/references/providers/video/higgsfield.md).

---

## Use any other video provider

### Generic CLI wrapper

```json
{
  "videoProvider": {
    "type": "generic_shell",
    "commandTemplate": "my-video-cli --prompt-file {prompt_file} --start {start_image} --end {end_image} --duration {duration} --output {output}"
  }
}
```

Supported placeholders:

| Placeholder | Value |
|---|---|
| `{prompt_file}` | Full prompt file path |
| `{start_image}` | Start image path or empty string |
| `{end_image}` | End image path or empty string |
| `{output}` | Required local output path |
| `{duration}` | Requested duration |
| `{model}` | Clip or provider model |
| `{aspect_ratio}` | Requested aspect ratio |

### Manual provider

Set:

```json
{
  "videoProvider": {
    "type": "manual"
  }
}
```

The plan prints exactly which images, prompt, and output path to use. This works with a browser-only platform that has no CLI or API.

### HTTP provider

`generic_http` defines the contract, but authentication, upload format, polling, and result parsing vary by provider. Add a small shell or Python wrapper and call it through `generic_shell`.

---

## Processing profiles

### Scrub video

Creates a video designed for frequent seeking:

```bash
python3 skills/motion-world/scripts/prepare_motion.py \
  --input source.mp4 \
  --out build \
  --profiles scrub \
  --fps 30 \
  --gop 4 \
  --crf 20
```

Processing choices:

- Constant frame rate.
- H.264.
- `yuv420p`.
- Short fixed GOP.
- No B-frames.
- Scene-cut keyframes disabled.
- Faststart enabled.
- Audio removed from the runtime master.

### Frame sequence

```bash
python3 skills/motion-world/scripts/prepare_motion.py \
  --input source.mp4 \
  --out build \
  --profiles frames \
  --frame-count 180 \
  --frame-width 540
```

Frames use zero-based names:

```text
frame_0000.webp
frame_0001.webp
...
```

### Sprite atlas

```bash
python3 skills/motion-world/scripts/prepare_motion.py \
  --input source.mp4 \
  --out build \
  --profiles frames,atlas \
  --frame-count 60 \
  --atlas-columns 10 \
  --atlas-max-frames 100
```

### Posters

```bash
python3 skills/motion-world/scripts/prepare_motion.py \
  --input source.mp4 \
  --out build \
  --profiles posters
```

Creates:

```text
posters/start.webp
posters/middle.webp
posters/end.webp
```

---

## Progress drivers

| Driver | Formula | Example |
|---|---|---|
| Elapsed time | `(now - start) / (end - start)` | Focus session, prayer period, cooldown |
| Countdown | `1 - remaining / total` | Timer, launch countdown |
| Count | `(current - min) / (goal - min)` | Habit, steps, completed tasks |
| Scroll | `(offset - start) / distance` | Marketing page, product story |
| Drag | `translation / allowedDistance` | Interactive reveal |
| Sensor | Normalized sensor range | Tilt, pressure, rotation |
| State machine | Map states to checkpoints | Onboarding, order lifecycle |
| Network | `bytesSent / totalBytes` | Upload or download |
| Audio | Smoothed amplitude mapping | Voice or music visualizer |
| Custom | Any finite number clamped to `0...1` | Product-specific state |

Rules:

- Clamp invalid values.
- Handle zero duration and zero range.
- Restore directly at any progress value after relaunch.
- Do not require earlier frames to play first.
- Keep completion logic in the application domain layer.
- Reduce or replace motion when the user enables reduced motion.

Detailed formulas and edge cases are in [`progress-drivers.md`](skills/motion-world/references/progress-drivers.md).

---

## Runtime integration

### SwiftUI

```swift
let progress = MotionProgress.elapsed(
    now: Date(),
    start: session.startDate,
    end: session.endDate
)

FrameSequenceView(
    progress: progress,
    frameCount: 180,
    reducedMotion: accessibilityReduceMotion
) { index in
    String(format: "frame_%04d", index)
}
```

Reference files:

- [`MotionProgress.swift`](skills/motion-world/references/runtimes/ios/MotionProgress.swift)
- [`FrameSequenceView.swift`](skills/motion-world/references/runtimes/ios/FrameSequenceView.swift)

### Jetpack Compose

```kotlin
val progress = MotionProgress.elapsed(
    nowMillis = System.currentTimeMillis(),
    startMillis = session.startMillis,
    endMillis = session.endMillis
)

val frameIndex = ((frameCount - 1) * progress)
    .roundToInt()
    .coerceIn(0, frameCount - 1)
```

Reference files are in [`runtimes/android`](skills/motion-world/references/runtimes/android).

### Flutter

```dart
final progress = MotionProgress.elapsed(
  DateTime.now(),
  session.start,
  session.end,
);

final index = (progress * (frameCount - 1)).round();
```

Reference files are in [`runtimes/flutter`](skills/motion-world/references/runtimes/flutter).

### React Native

```ts
const progress = elapsedProgress(
  Date.now(),
  session.startMs,
  session.endMs,
);

const frameIndex = Math.round(progress * (frameCount - 1));
```

Reference files are in [`runtimes/react-native`](skills/motion-world/references/runtimes/react-native).

### Web scrub video

```js
import { ScrubVideoRuntime, scrollDriver } from './motion-runtime.js';

const runtime = new ScrubVideoRuntime(
  document.querySelector('video'),
  { reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches }
);

function update() {
  runtime.setProgress(scrollDriver());
  requestAnimationFrame(update);
}

update();
```

Reference file: [`motion-runtime.js`](skills/motion-world/references/runtimes/web/motion-runtime.js).

---

## Choosing the runtime format

| Situation | Recommended output |
|---|---|
| Long cinematic camera move on a website | Scrub video |
| Native timer that must restore at an exact state | Frame sequence |
| Small badge, icon, or short loop | Sprite atlas |
| Low-memory device | Reduced frame sequence or posters |
| Reduce Motion enabled | Posters or three-state crossfade |
| Simple separable artwork | Native layered interpolation |
| App Store or investor video | Playback MP4 exported from the same source |

A single project can generate multiple formats. Use a different format per target when that improves reliability or size.

---

## Example applications

- A seed grows into a full garden as a habit streak advances.
- A landscape changes during a focus session.
- A product camera move follows page scroll.
- A delivery route moves through order states.
- A character evolves as a user completes lessons.
- A progress scene follows an upload.
- A map animation follows GPS distance.
- A wellness environment responds to breathing or audio.
- An App Store preview uses the same provider output as the product runtime.

Sukun is included only as a sample configuration. Motion World does not depend on Sukun and is not installed inside the Sukun repository.

---

## Repository layout

```text
motion-world/
├── .claude-plugin/
│   └── marketplace.json
├── docs/
│   ├── GUIDE_AR.md
│   └── media/
├── skills/
│   └── motion-world/
│       ├── SKILL.md
│       ├── references/
│       │   ├── examples/
│       │   ├── providers/
│       │   └── runtimes/
│       └── scripts/
├── LICENSE
├── NOTICE
├── README.md
├── README_AR.md
├── TEST_REPORT.md
└── VERSION
```

---

## Validation and test proof

Run project validation:

```bash
python3 skills/motion-world/scripts/validate_project.py \
  path/to/motion-project.json
```

Run basic repository checks:

```bash
python3 -m compileall skills/motion-world/scripts
node --check skills/motion-world/references/runtimes/web/motion-runtime.js
```

The included test report covers:

- Python compilation.
- JSON validation.
- JavaScript syntax.
- Swift parsing when `swiftc` is available.
- Higgsfield command planning.
- Runtime adapter installation.
- End-to-end FFmpeg processing.
- Zero-based frame extraction.
- Sprite atlas creation.
- Poster generation.
- Runtime metadata and hashes.

See [`TEST_REPORT.md`](TEST_REPORT.md).

---

## Production checklist

Before shipping:

### Source media

- [ ] Start and end images use matching composition.
- [ ] Important content stays inside target safe areas.
- [ ] Portrait output was composed for portrait.
- [ ] Text is native, not baked into artwork.
- [ ] Provider terms permit the intended use.

### Processing

- [ ] Runtime video has a short GOP.
- [ ] Frame names start at `0000`.
- [ ] Frame count matches metadata.
- [ ] First and final states were inspected.
- [ ] Package size was measured on the real device.

### Application

- [ ] Progress clamps to `0...1`.
- [ ] Relaunch restores the same visual state.
- [ ] Backgrounding does not create a second timer.
- [ ] Reduced Motion has a usable fallback.
- [ ] Offline behavior was tested.
- [ ] Screen readers receive a meaningful scene label.
- [ ] Decorative frames are hidden from accessibility APIs.

---

## What Motion World is not

- It is not a new video-generation model.
- It does not require Higgsfield.
- It is not limited to scroll pages.
- It does not force WebView code into native applications.
- It does not replace application state management.
- It does not make Apple-controlled shield screens accept arbitrary SwiftUI or JavaScript.
- It does not claim that every AI video will scrub well without processing.

---

## Motion World vs other approaches

| Approach | Best at | Limitation Motion World addresses |
|---|---|---|
| Normal MP4 | Playback | Weak random access and state restoration |
| Lottie | Vector UI animation | Requires vector animation assets, not arbitrary AI video |
| Rive | Interactive vector state machines | Requires authoring inside Rive |
| Sprite sheet | Compact short sequences | Needs extraction, packing, metadata, and runtime mapping |
| Scroll-video page | Cinematic web storytelling | Usually tied to scroll and one web implementation |
| Motion World | Provider-to-runtime pipeline | Adds processing, multi-format output, and cross-platform drivers |

Motion World can coexist with Lottie, Rive, or native layers. It chooses the runtime format per use case instead of treating one format as the answer to every animation.

---

## Troubleshooting

<details>
<summary><strong><code>ffmpeg</code> or <code>ffprobe</code> is not found</strong></summary>

Install FFmpeg and confirm both commands work in the same terminal used to run Python.

```bash
ffmpeg -version
ffprobe -version
```

</details>

<details>
<summary><strong>Atlas generation says Pillow is missing</strong></summary>

```bash
python3 -m pip install Pillow
```

</details>

<details>
<summary><strong>The provider video jumps when scrubbed</strong></summary>

Reprocess it with the scrub profile and a short GOP:

```bash
python3 skills/motion-world/scripts/prepare_motion.py \
  --input source.mp4 \
  --out build \
  --profiles scrub \
  --gop 4
```

For exact native state, use a frame sequence instead of video seeking.

</details>

<details>
<summary><strong>The first displayed frame is wrong</strong></summary>

Check that your runtime uses zero-based frame names beginning with `frame_0000.webp`. The included extractor and runtime use the same convention.

</details>

<details>
<summary><strong>Higgsfield returns JSON but no video is downloaded</strong></summary>

Inspect the saved `*.provider.json` file. The runner searches common result URL keys recursively. A provider response change may require updating `find_result_url`.

</details>

<details>
<summary><strong>The mobile composition is cropped badly</strong></summary>

Generate a separate 9:16 source composition. Do not assume a 16:9 camera move will remain readable after center cropping.

</details>

---

## Security and privacy

- Runtime packages can run fully offline.
- Provider credentials stay in the provider CLI or wrapper environment.
- Do not commit API keys, access tokens, signed URLs, or provider responses containing secrets.
- Review generated media before publishing it.
- Keep private source images outside public repositories unless you have permission to publish them.

---

## Contributing

Useful contributions include:

- Provider adapters.
- Runtime adapters.
- Better asset-size strategies.
- Device performance reports.
- Accessibility improvements.
- Additional project presets.
- Tests for Windows, Linux, macOS, iOS, and Android.

Open an issue with:

1. The target platform.
2. Provider and model.
3. Project manifest with secrets removed.
4. The exact command.
5. Console output.
6. Media metadata from `ffprobe`.

---

## Credits

Motion World builds on production patterns used by scroll-controlled video experiences and was informed by the MIT-licensed [`scroll-world`](https://github.com/oso95/scroll-world) project. Motion World broadens the pattern into a provider-agnostic pipeline for time, count, scroll, gesture, sensor, state, and other application drivers.

See [`NOTICE`](NOTICE) for attribution details.

---

## License

MIT. See [`LICENSE`](LICENSE).

<p align="center">
  <strong>Generate the motion once. Control it from any application state.</strong>
</p>
