#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, shutil, subprocess, sys
from pathlib import Path


def run(*args):
    subprocess.run([str(a) for a in args], check=True)


def capture(*args):
    return subprocess.check_output([str(a) for a in args], text=True).strip()


def sha256(path: Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()


def probe(path: Path):
    raw = capture('ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,codec_name,pix_fmt','-show_entries','format=duration','-of','json',path)
    return json.loads(raw)


def make_atlases(frames_dir: Path, out_dir: Path, columns: int, max_frames: int):
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError('Pillow is required for atlas output: python3 -m pip install Pillow') from exc
    frames=sorted(frames_dir.glob('frame_*.webp'))
    if not frames: raise RuntimeError('no frames found for atlas')
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest={'atlases':[], 'frames':[]}
    global_index=0
    for atlas_i in range(math.ceil(len(frames)/max_frames)):
        batch=frames[atlas_i*max_frames:(atlas_i+1)*max_frames]
        first=Image.open(batch[0]).convert('RGBA')
        fw,fh=first.size
        rows=math.ceil(len(batch)/columns)
        atlas=Image.new('RGBA',(columns*fw,rows*fh),(0,0,0,0))
        for local_i,path in enumerate(batch):
            im=Image.open(path).convert('RGBA')
            if im.size!=(fw,fh): raise RuntimeError('frame dimensions differ')
            x=(local_i%columns)*fw; y=(local_i//columns)*fh
            atlas.paste(im,(x,y))
            manifest['frames'].append({'index':global_index,'atlas':atlas_i,'x':x,'y':y,'width':fw,'height':fh})
            global_index+=1
        name=f'atlas_{atlas_i:03d}.png'
        atlas.save(out_dir/name,optimize=True)
        manifest['atlases'].append({'index':atlas_i,'file':name,'width':atlas.width,'height':atlas.height})
    (out_dir/'atlas.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--profiles',default='scrub,frames,atlas,posters')
    ap.add_argument('--fps',type=float,default=30)
    ap.add_argument('--frame-count',type=int,default=180)
    ap.add_argument('--gop',type=int,default=4)
    ap.add_argument('--crf',type=int,default=20)
    ap.add_argument('--frame-width',type=int,default=540)
    ap.add_argument('--atlas-columns',type=int,default=10)
    ap.add_argument('--atlas-max-frames',type=int,default=100)
    args=ap.parse_args()
    src=Path(args.input).resolve(); out=Path(args.out).resolve()
    if not src.exists(): raise FileNotFoundError(src)
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'): raise RuntimeError('ffmpeg and ffprobe are required')
    profiles={p.strip() for p in args.profiles.split(',') if p.strip()}
    out.mkdir(parents=True,exist_ok=True)

    metadata={'source':str(src),'sourceSha256':sha256(src),'profiles':sorted(profiles),'fps':args.fps,'frameCount':args.frame_count,'outputs':{}}

    if 'scrub' in profiles or 'playback' in profiles:
        d=out/'scrub'; d.mkdir(exist_ok=True)
        mp4=d/'master.mp4'
        run('ffmpeg','-loglevel','error','-y','-i',src,'-an','-vf',f'fps={args.fps}', '-c:v','libx264','-preset','medium','-crf',args.crf,'-pix_fmt','yuv420p','-g',args.gop,'-keyint_min',args.gop,'-sc_threshold','0','-bf','0','-movflags','+faststart',mp4)
        metadata['outputs']['scrubMp4']={'path':str(mp4.relative_to(out)),'sha256':sha256(mp4)}

    frames_dir=out/'frames'
    if {'frames','atlas'} & profiles:
        frames_dir.mkdir(exist_ok=True)
        # Select evenly spaced frames by scaling timeline to requested count.
        # Sample evenly by deriving a target extraction fps from source duration.
        duration=float(capture('ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',src))
        target_fps=max(0.001,args.frame_count/max(duration,0.001))
        run('ffmpeg','-loglevel','error','-y','-i',src,'-an','-vf',f'fps={target_fps:.8f},scale={args.frame_width}:-2:flags=lanczos','-frames:v',args.frame_count,'-start_number','0','-c:v','libwebp','-quality','82',frames_dir/'frame_%04d.webp')
        frames=sorted(frames_dir.glob('frame_*.webp'))
        metadata['frameCount']=len(frames)
        metadata['outputs']['frames']={'directory':'frames','pattern':'frame_%04d.webp','count':len(frames)}

    if 'atlas' in profiles:
        make_atlases(frames_dir,out/'atlas',args.atlas_columns,args.atlas_max_frames)
        metadata['outputs']['atlas']={'directory':'atlas','manifest':'atlas/atlas.json'}

    if 'posters' in profiles:
        d=out/'posters'; d.mkdir(exist_ok=True)
        duration=float(capture('ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',src))
        for name,t in [('start',0),('middle',duration/2),('end',max(0,duration-0.05))]:
            p=d/f'{name}.webp'
            run('ffmpeg','-loglevel','error','-y','-ss',f'{t:.6f}','-i',src,'-frames:v','1','-c:v','libwebp','-quality','88',p)
            metadata['outputs'][f'poster{name.title()}']={'path':str(p.relative_to(out)),'sha256':sha256(p)}

    metadata['probe']=probe(src)
    (out/'motion-runtime.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    print(f'Created motion package: {out}')
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}',file=sys.stderr); raise SystemExit(1)
