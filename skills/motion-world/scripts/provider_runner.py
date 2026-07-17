#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, shlex, subprocess, sys, urllib.request
from pathlib import Path


def q(value):
    return shlex.quote(str(value))


def higgsfield_command(provider, clip, root: Path):
    model = clip.get('model') or provider.get('model')
    if not model: raise ValueError(f'clip {clip.get("id")} has no model')
    parts = ['higgsfield', 'generate', 'create', model]
    parts += ['--prompt', f'"$(cat {q(root / clip["promptFile"])})"']
    if clip.get('startImage'): parts += ['--start-image', q(root / clip['startImage'])]
    if clip.get('endImage'): parts += ['--end-image', q(root / clip['endImage'])]
    for ref in clip.get('referenceImages', []): parts += ['--image', q(root / ref)]
    if clip.get('canvas'):
        # Canvas id is not necessarily an aspect ratio. Prefer explicit provider config when supplied.
        ratio = clip.get('aspectRatio') or provider.get('config', {}).get('aspectRatio')
        if ratio: parts += ['--aspect_ratio', q(ratio)]
    if clip.get('durationSeconds'): parts += ['--duration', str(clip['durationSeconds'])]
    parts += ['--wait', '--json']
    return ' '.join(parts)


def shell_command(provider, clip, root: Path):
    template = provider.get('commandTemplate')
    if not template: raise ValueError('generic_shell requires commandTemplate')
    vals = {
      'prompt_file': str(root / clip['promptFile']),
      'start_image': str(root / clip['startImage']) if clip.get('startImage') else '',
      'end_image': str(root / clip['endImage']) if clip.get('endImage') else '',
      'output': str(root / clip['output']),
      'duration': clip.get('durationSeconds', ''),
      'model': clip.get('model') or provider.get('model', ''),
      'aspect_ratio': clip.get('aspectRatio', provider.get('config', {}).get('aspectRatio', '')),
    }
    return template.format(**vals)




def find_result_url(value):
    if isinstance(value, dict):
        for key in ("result_url", "resultUrl", "download_url", "downloadUrl", "url"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.startswith(("http://", "https://")):
                return candidate
        for child in value.values():
            found = find_result_url(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_result_url(child)
            if found:
                return found
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('project')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--plan', action='store_true')
    g.add_argument('--execute', action='store_true')
    args = ap.parse_args()
    project_path = Path(args.project).resolve()
    root = project_path.parent
    data = json.loads(project_path.read_text(encoding='utf-8'))
    provider = data['videoProvider']
    ptype = provider['type']

    commands = []
    for clip in data['clips']:
        if ptype == 'higgsfield_cli':
            command = higgsfield_command(provider, clip, root)
        elif ptype == 'generic_shell':
            command = shell_command(provider, clip, root)
        elif ptype in ('manual', 'generic_http'):
            command = None
        else:
            raise ValueError(f'unsupported video provider type: {ptype}')
        commands.append((clip, command))

    print(f'Provider: {ptype}')
    if ptype == 'higgsfield_cli':
        print('Preflight: higgsfield workspace list')
        for model in sorted({(c.get('model') or provider.get('model')) for c,_ in commands}):
            print(f'Preflight: higgsfield model get {model}')
    for clip, command in commands:
        print(f'\n[{clip["id"]}] -> {root / clip["output"]}')
        if command:
            print(command)
        elif ptype == 'manual':
            print(f'Upload {clip.get("startImage")} / {clip.get("endImage")} using prompt {clip["promptFile"]}; save result at {clip["output"]}')
        else:
            print('generic_http requires explicit endpoint/auth/upload/poll/download mapping; create a provider-specific shell wrapper or use manual mode.')

    if args.execute:
        if ptype not in ('higgsfield_cli','generic_shell'):
            raise ValueError(f'--execute is not supported for {ptype} without an explicit wrapper')
        for clip, command in commands:
            out = root / clip['output']
            out.parent.mkdir(parents=True, exist_ok=True)
            print(f'Executing {clip["id"]}...', flush=True)
            if ptype == 'higgsfield_cli':
                completed = subprocess.run(command, shell=True, cwd=root, check=True, text=True, capture_output=True)
                job_json = out.with_suffix(out.suffix + '.provider.json')
                job_json.write_text(completed.stdout, encoding='utf-8')
                try:
                    payload = json.loads(completed.stdout)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f'Higgsfield returned non-JSON output; saved at {job_json}') from exc
                result_url = find_result_url(payload)
                if not result_url:
                    raise RuntimeError(f'No result URL found in Higgsfield output; inspect {job_json}')
                print(f'Downloading result -> {out}', flush=True)
                urllib.request.urlretrieve(result_url, out)
            else:
                subprocess.run(command, shell=True, cwd=root, check=True)
                if not out.exists():
                    raise RuntimeError(f'generic_shell completed but output is missing: {out}')
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(1)
