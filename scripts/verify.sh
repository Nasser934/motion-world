#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo "[1/7] Python compile"
python3 -m compileall -q skills/motion-world/scripts
echo "[2/7] Provider catalog"
python3 -m json.tool skills/motion-world/references/provider-catalog.json >/dev/null
echo "[3/7] Validate example projects"
python3 skills/motion-world/scripts/validate_project.py skills/motion-world/references/examples/generic-growth.motion-project.json
python3 skills/motion-world/scripts/validate_project.py skills/motion-world/references/examples/sukun-oasis.motion-project.json
echo "[4/7] Beginner provider routing"
python3 skills/motion-world/scripts/route_provider.py --first-last --mode agent --allow-paid ask --json >/tmp/motion-world-provider-route.json
grep -q '"id": "krea_mcp"' /tmp/motion-world-provider-route.json
echo "[5/7] JavaScript syntax"
node --check skills/motion-world/references/runtimes/web/motion-runtime.js
echo "[6/7] Provider planning"
python3 skills/motion-world/scripts/provider_runner.py skills/motion-world/references/examples/generic-growth.motion-project.json --plan >/tmp/motion-world-provider-plan.txt
grep -q "Provider: auto_router" /tmp/motion-world-provider-plan.txt
echo "[7/7] Media and README"
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
