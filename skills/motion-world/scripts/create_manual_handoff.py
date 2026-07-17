#!/usr/bin/env python3
"""Create a complete beginner-friendly manual video-provider handoff kit.

The kit contains the exact source images, copy-paste prompt, official provider
links, settings, expected return filename, and machine-readable manifest.
It intentionally does not generate frames, atlases, or a fake production video.
"""
from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path
from typing import Any

PROVIDERS: dict[str, dict[str, Any]] = {
    "krea": {
        "label": "Krea",
        "url": "https://www.krea.ai/features/ai-video-generator",
        "steps_ar": [
            "سجّل الدخول وافتح Video ثم Image to Video.",
            "اختر نموذجًا يظهر أنه يدعم First frame + Last frame.",
            "ارفع صورة البداية ثم صورة النهاية بالترتيب.",
            "الصق ملف الـPrompt كاملًا.",
            "اختر 9:16، والدقة 1080p إن توفرت، وأوقف الصوت.",
            "اجعل الكاميرا Locked/None والحركة Low أو Medium-Low.",
        ],
        "steps_en": [
            "Sign in and open Video → Image to Video.",
            "Choose a model that visibly supports first and last frames.",
            "Upload the start image, then the end image.",
            "Paste the complete prompt file.",
            "Choose 9:16, 1080p when available, and disable audio.",
            "Use locked/no camera motion and low or medium-low motion strength.",
        ],
    },
    "dreamina": {
        "label": "Dreamina / Seedance",
        "url": "https://dreamina.capcut.com/resource/first-last-frame",
        "secondaryUrl": "https://dreamina.capcut.com/create/frames-to-video",
        "steps_ar": [
            "سجّل الدخول وافتح AI Video أو Frames to Video.",
            "اختر First & Last Frame أو Multi-frames عند وجود مراحل متعددة.",
            "ارفع البداية ثم النهاية/المراحل بالترتيب.",
            "الصق الـPrompt كاملًا.",
            "اختر 9:16، والمدة المطلوبة أو أقرب مدة، و1080p، ومن دون صوت.",
        ],
        "steps_en": [
            "Sign in and open AI Video or Frames to Video.",
            "Choose First & Last Frame, or Multi-frames for multiple checkpoints.",
            "Upload the start and end/checkpoint images in timeline order.",
            "Paste the complete prompt.",
            "Choose 9:16, the requested or nearest duration, 1080p, and no audio.",
        ],
    },
    "vidu": {
        "label": "Vidu",
        "url": "https://www.vidu.com/ai-video-generator",
        "secondaryUrl": "https://www.vidu.com/",
        "steps_ar": [
            "سجّل الدخول وافتح Image to Video ثم First & Last Frames.",
            "ارفع صورة البداية ثم صورة النهاية.",
            "الصق الـPrompt كاملًا.",
            "اختر 9:16 و1080p والمدة المطلوبة أو أقرب خيار.",
            "استخدم حركة منخفضة وكاميرا ثابتة، ثم نزّل MP4.",
        ],
        "steps_en": [
            "Sign in and open Image to Video → First & Last Frames.",
            "Upload the start image, then the end image.",
            "Paste the complete prompt.",
            "Choose 9:16, 1080p, and the requested or nearest duration.",
            "Use low motion and a locked camera, then download MP4.",
        ],
    },
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_required(root: Path, relative: str | None, destination: Path, label: str) -> str | None:
    if not relative:
        return None
    source = (root / relative).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"{label} not found: {source}")
    shutil.copy2(source, destination)
    return destination.name


def provider_sections(language: str, selected: list[str]) -> str:
    sections: list[str] = []
    for index, provider_id in enumerate(selected, start=1):
        provider = PROVIDERS[provider_id]
        if language == "ar":
            lines = [f"## الخيار {index}: {provider['label']}", "", f"الرابط الرسمي: {provider['url']}"]
            if provider.get("secondaryUrl"):
                lines.append(f"رابط بديل مباشر: {provider['secondaryUrl']}")
            lines += [""] + [f"{n}. {step}" for n, step in enumerate(provider["steps_ar"], start=1)]
        else:
            lines = [f"## Option {index}: {provider['label']}", "", f"Official link: {provider['url']}"]
            if provider.get("secondaryUrl"):
                lines.append(f"Secondary direct link: {provider['secondaryUrl']}")
            lines += [""] + [f"{n}. {step}" for n, step in enumerate(provider["steps_en"], start=1)]
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


def create_clip_kit(project: dict[str, Any], project_root: Path, clip: dict[str, Any], output_root: Path, providers: list[str]) -> dict[str, Any]:
    clip_id = clip["id"]
    clip_dir = output_root / clip_id
    clip_dir.mkdir(parents=True, exist_ok=True)

    start_name = copy_required(project_root, clip.get("startImage"), clip_dir / "01-start-frame.png", "start image")
    end_name = copy_required(project_root, clip.get("endImage"), clip_dir / "02-end-frame.png", "end image")

    prompt_source = (project_root / clip["promptFile"]).resolve()
    if not prompt_source.is_file():
        raise FileNotFoundError(f"prompt not found: {prompt_source}")
    prompt_text = prompt_source.read_text(encoding="utf-8").strip() + "\n"
    prompt_name = "03-copy-paste-prompt.txt"
    (clip_dir / prompt_name).write_text(prompt_text, encoding="utf-8")

    refs: list[str] = []
    for idx, relative in enumerate(clip.get("referenceImages", []), start=1):
        ext = Path(relative).suffix or ".png"
        dest = clip_dir / f"reference-{idx:02d}{ext}"
        copied = copy_required(project_root, relative, dest, f"reference image {idx}")
        if copied:
            refs.append(copied)

    duration = clip.get("durationSeconds", 5)
    aspect = clip.get("aspectRatio") or "match the supplied images"
    canvas = next((c for c in project.get("canvases", []) if c.get("id") == clip.get("canvas")), {})
    resolution = f"{canvas.get('width')}x{canvas.get('height')}" if canvas.get("width") and canvas.get("height") else "native portrait/landscape resolution"
    return_name = f"{clip_id}-PROVIDER-FINAL.mp4"

    ar = f"""# حزمة إنشاء الفيديو يدويًا — {clip_id}

هذه الحزمة هي الخطوة الصحيحة عندما لا تستطيع Motion World تنفيذ مزود الفيديو تلقائيًا.
لا توجد داخلها نتيجة مزود وهمية، ولا Frames أو Atlas قبل رجوع الفيديو الحقيقي.

## الملفات

- `{start_name}` — First/Start frame.
- `{end_name}` — Last/End frame.
- `{prompt_name}` — انسخ النص كاملًا في خانة Prompt.
{('- صور مرجعية: ' + ', '.join(f'`{r}`' for r in refs)) if refs else ''}

## الإعدادات المطلوبة

- المقاس: `{aspect}`
- الدقة المستهدفة: `{resolution}` أو أعلى دقة أصلية متاحة.
- المدة: `{duration}` ثوانٍ أو أقرب خيار متاح.
- الكاميرا: ثابتة ما لم يطلب الـPrompt غير ذلك.
- الصوت: متوقف ما لم يطلب المشروع صوتًا.
- اسم الملف بعد التنزيل: `{return_name}`

{provider_sections('ar', providers)}

## بعد إنشاء الفيديو

1. نزّل النتيجة بصيغة MP4.
2. أعد تسميتها إلى `{return_name}`.
3. ارفعها للمحادثة أو ضعها في المسار المحدد داخل المشروع.
4. على Motion World التحقق من الفيديو الحقيقي أولًا، ثم إنشاء Scrub/Frames/Posters وحزمة المنصة المطلوبة.

لا تقبل نتيجة فيها Crossfade، إطار أسود، حركة كاميرا غير مطلوبة، تشوه، عناصر مكررة، نص، أو علامة مائية.
"""
    en = f"""# Manual video-provider handoff — {clip_id}

Use this kit when Motion World cannot execute a connected video provider automatically.
It intentionally contains no fake provider result and no frames/atlases before the real video returns.

## Files

- `{start_name}` — first/start frame.
- `{end_name}` — last/end frame.
- `{prompt_name}` — paste the complete text into the provider prompt field.
{('- Reference images: ' + ', '.join(f'`{r}`' for r in refs)) if refs else ''}

## Required settings

- Aspect ratio: `{aspect}`
- Target resolution: `{resolution}` or the highest available native resolution.
- Duration: `{duration}` seconds or the nearest available option.
- Camera: locked unless the prompt explicitly requests movement.
- Audio: disabled unless required by the project.
- Download filename: `{return_name}`

{provider_sections('en', providers)}

## After generation

1. Download the result as MP4.
2. Rename it to `{return_name}`.
3. Upload it to the conversation or place it at the declared project path.
4. Motion World must validate the real video before creating scrub/frames/posters and the target runtime package.

Reject crossfades, black frames, unintended camera motion, deformation, duplication, text, or watermarks.
"""
    (clip_dir / "README_AR.md").write_text(ar, encoding="utf-8")
    (clip_dir / "README.md").write_text(en, encoding="utf-8")

    manifest = {
        "clipId": clip_id,
        "status": "MANUAL_PROVIDER_REQUIRED",
        "startFrame": start_name,
        "endFrame": end_name,
        "referenceImages": refs,
        "prompt": prompt_name,
        "expectedReturnFile": return_name,
        "expectedProjectOutput": clip["output"],
        "providers": [{"id": p, "label": PROVIDERS[p]["label"], "url": PROVIDERS[p]["url"]} for p in providers],
        "settings": {
            "aspectRatio": aspect,
            "durationSeconds": duration,
            "targetResolution": resolution,
            "camera": "locked unless explicitly requested",
            "audio": False,
        },
    }
    (clip_dir / "manual-handoff.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def zip_directory(source: Path, destination: Path) -> None:
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source.parent))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--providers", default="krea,dreamina,vidu")
    parser.add_argument("--no-zip", action="store_true")
    args = parser.parse_args()

    project_path = args.project.resolve()
    root = project_path.parent
    project = read_json(project_path)
    providers = [item.strip().lower() for item in args.providers.split(",") if item.strip()]
    unknown = [p for p in providers if p not in PROVIDERS]
    if unknown:
        raise ValueError(f"unknown provider IDs: {unknown}; choose from {sorted(PROVIDERS)}")

    output = (args.out or (root / "manual-provider-kit")).resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    manifests = [create_clip_kit(project, root, clip, output, providers) for clip in project["clips"]]
    summary = {
        "status": "MANUAL_PROVIDER_REQUIRED",
        "project": project.get("project", {}).get("id"),
        "clips": manifests,
        "nextAction": "Generate the real MP4 using one of the official links, then return the expected filename.",
    }
    (output / "handoff-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    zip_path = output.with_suffix(".zip")
    if not args.no_zip:
        zip_directory(output, zip_path)

    print(json.dumps({
        "status": "MANUAL_PROVIDER_REQUIRED",
        "directory": str(output),
        "zip": None if args.no_zip else str(zip_path),
        "clips": [m["clipId"] for m in manifests],
        "instruction": "Give the user direct links to the ZIP, every start/end image, the prompt file, and the official provider pages. Do not build production frames or atlases yet.",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
