# Contributing to Motion World

Thanks for improving Motion World. Keep changes focused, tested, and provider-agnostic.

## Good contribution areas

- Video provider adapters.
- Image provider instructions.
- Native runtime adapters.
- Progress-driver edge cases.
- Media-size and decode-performance improvements.
- Accessibility and Reduced Motion behavior.
- Cross-platform tests.

## Before opening a pull request

```bash
python3 -m pip install Pillow jsonschema
./scripts/verify.sh
```

For runtime changes, include:

- Target platform and minimum OS/runtime version.
- Output mode used: scrub video, frames, atlas, posters, or layers.
- A test for progress values `0`, `0.25`, `0.5`, `0.75`, and `1`.
- Reduced Motion behavior.
- Package-size and performance notes when media handling changes.

For provider adapters, include:

- Authentication method without secrets.
- Upload and polling flow.
- Supported start/end/reference image inputs.
- Model capability checks.
- Result download logic.
- A `--plan` or dry-run path that does not spend credits.

Do not commit API keys, access tokens, signed URLs, private media, or provider responses containing credentials.
