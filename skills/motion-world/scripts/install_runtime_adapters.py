#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIMES = HERE.parent / 'references' / 'runtimes'
MAP = {
    'ios_swiftui': ['ios/MotionProgress.swift', 'ios/FrameSequenceView.swift'],
    'android_compose': ['android/MotionProgress.kt', 'android/FrameSequence.kt'],
    'flutter': ['flutter/motion_progress.dart', 'flutter/frame_sequence.dart'],
    'react_native': ['react-native/motionProgress.ts', 'react-native/frameSequence.ts'],
    'web': ['web/motion-runtime.js'],
}

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('project')
    ap.add_argument('--force', action='store_true')
    args=ap.parse_args()
    project=Path(args.project).resolve()
    root=project.parent
    data=json.loads(project.read_text(encoding='utf-8'))
    for runtime in data['runtimes']:
        platform=runtime['platform']
        out=root/runtime.get('outputDirectory', f'runtime/{platform}')
        out.mkdir(parents=True, exist_ok=True)
        for rel in MAP[platform]:
            src=RUNTIMES/rel
            dst=out/src.name
            if dst.exists() and not args.force:
                print(f'SKIP {dst} (use --force to replace)')
                continue
            shutil.copy2(src,dst)
            print(f'COPY {src.name} -> {dst}')
        (out/'MOTION_WORLD_INTEGRATION.txt').write_text(
            'Pass normalized progress 0...1 from the host application. Do not create a duplicate business timer inside the renderer.\n',
            encoding='utf-8'
        )
    return 0

if __name__=='__main__':
    raise SystemExit(main())
