#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[1/9] Python compile"
python3 -m compileall -q skills/motion-world/scripts

echo "[2/9] JSON and provider catalog"
python3 -m json.tool skills/motion-world/references/provider-catalog.json >/dev/null
python3 -m json.tool skills/motion-world/references/motion-project.schema.json >/dev/null

echo "[3/9] Validate example projects"
python3 skills/motion-world/scripts/validate_project.py skills/motion-world/references/examples/generic-growth.motion-project.json
python3 skills/motion-world/scripts/validate_project.py skills/motion-world/references/examples/sukun-oasis.motion-project.json

echo "[4/9] Beginner provider routing"
python3 skills/motion-world/scripts/route_provider.py --first-last --mode agent --allow-paid ask --json >/tmp/motion-world-provider-route.json
grep -q '"id": "krea_mcp"' /tmp/motion-world-provider-route.json

echo "[5/9] Manual-provider handoff"
rm -rf /tmp/motion-world-handoff-test
mkdir -p /tmp/motion-world-handoff-test/assets /tmp/motion-world-handoff-test/prompts
python3 - <<'PY'
import base64, json
from pathlib import Path
root = Path('/tmp/motion-world-handoff-test')
png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Y9Z2xQAAAAASUVORK5CYII=')
(root/'assets/start.png').write_bytes(png)
(root/'assets/end.png').write_bytes(png)
(root/'prompts/motion.txt').write_text('One continuous locked-camera transformation. No text.\n', encoding='utf-8')
project = {
  'schemaVersion': '0.2',
  'project': {'id': 'handoff-test', 'name': 'Handoff Test'},
  'providerPolicy': {'paidPolicy': 'ask'},
  'canvases': [{'id': 'portrait', 'width': 1080, 'height': 1920}],
  'imageProvider': {'type': 'local'},
  'videoProvider': {'type': 'manual'},
  'clips': [{
    'id': 'clip',
    'startImage': 'assets/start.png',
    'endImage': 'assets/end.png',
    'promptFile': 'prompts/motion.txt',
    'canvas': 'portrait',
    'aspectRatio': '9:16',
    'durationSeconds': 8,
    'output': 'provider-output/clip.mp4'
  }],
  'processing': {'profiles': ['scrub', 'frames', 'posters']},
  'driver': {'type': 'custom'},
  'runtimes': [{'platform': 'ios_swiftui', 'mode': 'frames'}]
}
(root/'motion-project.json').write_text(json.dumps(project, indent=2), encoding='utf-8')
PY
python3 skills/motion-world/scripts/provider_runner.py /tmp/motion-world-handoff-test/motion-project.json --plan >/tmp/motion-world-handoff-plan.txt
test -s /tmp/motion-world-handoff-test/manual-provider-kit.zip
test -s /tmp/motion-world-handoff-test/manual-provider-kit/clip/01-start-frame.png
test -s /tmp/motion-world-handoff-test/manual-provider-kit/clip/02-end-frame.png
test -s /tmp/motion-world-handoff-test/manual-provider-kit/clip/03-copy-paste-prompt.txt
grep -q 'https://www.krea.ai/features/ai-video-generator' /tmp/motion-world-handoff-test/manual-provider-kit/clip/README_AR.md
grep -q 'clip-PROVIDER-FINAL.mp4' /tmp/motion-world-handoff-test/manual-provider-kit/clip/README_AR.md

echo "[6/9] Diagnostic production guard"
python3 - <<'PY'
import json
from pathlib import Path
p = Path('/tmp/motion-world-handoff-test/motion-project.json')
data = json.loads(p.read_text())
data['videoProvider'] = {
  'type': 'generic_shell',
  'model': 'local-crossfade-preview',
  'commandTemplate': 'true'
}
p.write_text(json.dumps(data, indent=2))
PY
if python3 skills/motion-world/scripts/provider_runner.py /tmp/motion-world-handoff-test/motion-project.json --execute >/tmp/motion-world-diagnostic.txt 2>&1; then
  echo "ERROR: diagnostic preview was allowed without --allow-diagnostic"
  exit 1
fi
grep -q 'Refusing to create a local crossfade' /tmp/motion-world-diagnostic.txt

echo "[7/9] JavaScript syntax"
node --check skills/motion-world/references/runtimes/web/motion-runtime.js

echo "[8/9] Auto provider planning"
python3 skills/motion-world/scripts/provider_runner.py skills/motion-world/references/examples/generic-growth.motion-project.json --plan >/tmp/motion-world-provider-plan.txt
grep -q "Provider: auto_router" /tmp/motion-world-provider-plan.txt
grep -q -- "--handoff" /tmp/motion-world-provider-plan.txt

echo "[9/9] Media and README"
test -s docs/media/hero.svg
test -s docs/media/architecture.svg
test -s docs/media/output-matrix.svg
test -s docs/media/motion-world-demo.gif
test -s docs/media/motion-world-demo.mp4
test -s docs/media/demo-start.webp
test -s docs/media/demo-middle.webp
test -s docs/media/demo-end.webp
grep -q "## 60-second start" README.md
grep -q "## Runtime integration" README.md
grep -q "## البدء خلال دقيقة" README_AR.md

echo "Motion World repository verification passed."
