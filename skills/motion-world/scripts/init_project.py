#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLE = HERE.parent / 'references' / 'examples' / 'generic-growth.motion-project.json'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('directory')
    ap.add_argument('--preset', default='generic-cinematic')
    args = ap.parse_args()
    root = Path(args.directory)
    root.mkdir(parents=True, exist_ok=True)
    for d in ['assets/source-images', 'prompts', 'provider-output', 'build', 'runtime']:
        (root / d).mkdir(parents=True, exist_ok=True)
    data = json.loads(EXAMPLE.read_text(encoding='utf-8'))
    data['project']['id'] = root.name.replace(' ', '-').lower()
    data['project']['name'] = root.name.replace('-', ' ').title()
    (root / 'motion-project.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (root / 'prompts' / 'growth-motion.txt').write_text(
        'Single continuous cinematic motion, no cuts. Preserve subject identity, camera, lighting, and palette. '
        'Move smoothly from the approved start image toward the approved end state. No text or captions.\n',
        encoding='utf-8'
    )
    print(f'Created {root.resolve()}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
