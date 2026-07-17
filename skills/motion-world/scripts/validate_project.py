#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path


def fail(msg: str) -> None:
    raise ValueError(msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('project')
    args = ap.parse_args()
    path = Path(args.project)
    data = json.loads(path.read_text(encoding='utf-8'))

    if data.get('schemaVersion') != '0.2': fail('schemaVersion must be 0.2')
    if not data.get('project', {}).get('id'): fail('project.id is required')
    if not data.get('clips'): fail('at least one clip is required')
    if not data.get('runtimes'): fail('at least one runtime is required')
    if not data.get('processing', {}).get('profiles'): fail('processing.profiles is required')

    canvas_ids = {c.get('id') for c in data.get('canvases', [])}
    clip_ids = set()
    for i, clip in enumerate(data['clips']):
        cid = clip.get('id')
        if not cid: fail(f'clips[{i}].id is required')
        if cid in clip_ids: fail(f'duplicate clip id: {cid}')
        clip_ids.add(cid)
        if clip.get('canvas') and clip['canvas'] not in canvas_ids:
            fail(f'clip {cid} references unknown canvas {clip["canvas"]}')
        if not clip.get('promptFile'): fail(f'clip {cid} promptFile is required')
        if not clip.get('output'): fail(f'clip {cid} output is required')
        if clip.get('durationSeconds', 1) <= 0: fail(f'clip {cid} durationSeconds must be > 0')

    allowed_profiles = {'scrub','frames','atlas','playback','posters'}
    unknown = set(data['processing']['profiles']) - allowed_profiles
    if unknown: fail(f'unknown processing profiles: {sorted(unknown)}')

    allowed_drivers = {'elapsed_time','countdown','count','scroll','drag','sensor','state_machine','audio','network','custom'}
    driver = data.get('driver', {}).get('type')
    if driver not in allowed_drivers: fail(f'unsupported driver: {driver}')

    print(f'OK: {path} ({len(clip_ids)} clip(s), {len(data["runtimes"])} runtime(s))')
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(1)
