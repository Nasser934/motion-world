# Runtime integration

Run:

```bash
python3 skills/motion-world/scripts/install_runtime_adapters.py motion-project.json
```

The script copies platform-neutral progress helpers and the relevant reference runtime into each
configured `outputDirectory`. These are starting points: connect image/video loading to the host
application's resource system and pass progress from the host domain state.

Do not let the copied renderer create a second timer, counter, download task, or state machine.
