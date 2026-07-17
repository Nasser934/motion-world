#!/usr/bin/env python3
from __future__ import annotations
import argparse, subprocess
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('input')
ap.add_argument('output')
ap.add_argument('--which',choices=['first','last'],default='last')
args=ap.parse_args()
cmd=['ffmpeg','-y']
if args.which=='last': cmd += ['-sseof','-0.05']
cmd += ['-i',args.input,'-frames:v','1',args.output]
subprocess.run(cmd,check=True)
print(Path(args.output).resolve())
