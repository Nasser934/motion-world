# Higgsfield CLI adapter

The adapter follows the same safety rule as scroll-world: inspect the model schema before batching.

Typical plan:

```bash
higgsfield workspace list
higgsfield model get <model>
higgsfield generate create <model> \
  --prompt "$(cat prompts/scene-01-motion.txt)" \
  --start-image assets/source-images/scene-01.png \
  --aspect_ratio 9:16 \
  --duration 8 \
  --wait --json
```

Do not blindly add `--end-image`, `--resolution`, `--sound`, or other flags. The chosen model may not
support them. The runner prints a command plan; inspect it before execution.

For a chain, use actual rendered boundary frames. Extract with:

```bash
ffmpeg -sseof -0.05 -i clip-a.mp4 -frames:v 1 boundary-a-last.png
ffmpeg -i clip-b.mp4 -frames:v 1 boundary-b-first.png
```
