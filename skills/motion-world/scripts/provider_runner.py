#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import urllib.request
from pathlib import Path


def q(value):
    return shlex.quote(str(value))


def higgsfield_command(provider, clip, root: Path):
    model = clip.get("model") or provider.get("model")
    if not model:
        raise ValueError(f'clip {clip.get("id")} has no model')
    parts = ["higgsfield", "generate", "create", model]
    parts += ["--prompt", f'"$(cat {q(root / clip["promptFile"])})"']
    if clip.get("startImage"):
        parts += ["--start-image", q(root / clip["startImage"])]
    if clip.get("endImage"):
        parts += ["--end-image", q(root / clip["endImage"])]
    for ref in clip.get("referenceImages", []):
        parts += ["--image", q(root / ref)]
    ratio = clip.get("aspectRatio") or provider.get("config", {}).get("aspectRatio")
    if ratio:
        parts += ["--aspect_ratio", q(ratio)]
    if clip.get("durationSeconds"):
        parts += ["--duration", str(clip["durationSeconds"])]
    parts += ["--wait", "--json"]
    return " ".join(parts)


def shell_command(provider, clip, root: Path):
    template = provider.get("commandTemplate")
    if not template:
        raise ValueError("generic_shell requires commandTemplate")
    vals = {
        "prompt_file": str(root / clip["promptFile"]),
        "start_image": str(root / clip["startImage"]) if clip.get("startImage") else "",
        "end_image": str(root / clip["endImage"]) if clip.get("endImage") else "",
        "output": str(root / clip["output"]),
        "duration": clip.get("durationSeconds", ""),
        "model": clip.get("model") or provider.get("model", ""),
        "aspect_ratio": clip.get("aspectRatio", provider.get("config", {}).get("aspectRatio", "")),
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


def create_handoff(project_path: Path) -> None:
    script = Path(__file__).resolve().parent / "create_manual_handoff.py"
    subprocess.run(
        [sys.executable, str(script), str(project_path)],
        check=True,
        cwd=project_path.parent,
    )


def is_diagnostic_provider(provider: dict, ptype: str) -> bool:
    if ptype == "local_diagnostic":
        return True
    haystack = " ".join(
        str(value)
        for value in [
            provider.get("model", ""),
            provider.get("commandTemplate", ""),
            provider.get("config", {}).get("purpose", ""),
        ]
    ).lower()
    return any(token in haystack for token in ("crossfade", "diagnostic", "local preview", "local-preview"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--plan", action="store_true")
    g.add_argument("--handoff", action="store_true", help="Create a complete manual-provider kit")
    g.add_argument("--execute", action="store_true")
    ap.add_argument(
        "--allow-diagnostic",
        action="store_true",
        help="Explicitly allow a local crossfade/interpolation preview. It is never production output.",
    )
    args = ap.parse_args()

    project_path = Path(args.project).resolve()
    root = project_path.parent
    data = json.loads(project_path.read_text(encoding="utf-8"))
    provider = data["videoProvider"]
    ptype = provider["type"]

    if args.handoff:
        create_handoff(project_path)
        return 0

    if ptype == "auto_router":
        policy = data.get("providerPolicy", {})
        flags = []
        if any(clip.get("endImage") for clip in data["clips"]):
            flags.append("--first-last")
        if any(len(clip.get("referenceImages", [])) > 1 for clip in data["clips"]):
            flags.append("--multi-keyframe")
        paid = policy.get("paidPolicy", "ask")
        print("Provider: auto_router")
        print("Ask the single provider question, probe connected accounts, then run:")
        print(
            "python3 skills/motion-world/scripts/route_provider.py "
            + " ".join(flags)
            + f" --allow-paid {q(paid)} --json"
        )
        print("If no connected automatic route is available, create the manual kit immediately:")
        print(
            f"python3 skills/motion-world/scripts/provider_runner.py {q(project_path)} --handoff"
        )
        print("Do not generate frames, atlases, or a production package before the real provider MP4 returns.")
        if args.execute:
            raise ValueError("auto_router must resolve to a concrete provider before --execute")
        return 0

    commands = []
    manual_types = {"manual", "krea_manual", "dreamina_manual", "vidu_manual"}
    for clip in data["clips"]:
        if ptype == "higgsfield_cli":
            command = higgsfield_command(provider, clip, root)
        elif ptype == "generic_shell":
            command = shell_command(provider, clip, root)
        elif ptype in manual_types | {
            "generic_http",
            "krea_mcp",
            "vidu_api",
            "minimax_api",
            "pixverse_api",
            "fal_api",
            "wan21_flf2v_local",
            "ltx_local",
            "local_diagnostic",
        }:
            command = None
        else:
            raise ValueError(f"unsupported video provider type: {ptype}")
        commands.append((clip, command))

    print(f"Provider: {ptype}")
    if ptype == "higgsfield_cli":
        print("Preflight: higgsfield workspace list")
        for model in sorted({(c.get("model") or provider.get("model")) for c, _ in commands}):
            print(f"Preflight: higgsfield model get {model}")

    if ptype in manual_types and args.plan:
        print("No automatic provider is connected. Creating a complete manual-provider kit now...")
        create_handoff(project_path)
        print("Give the user direct links to the kit ZIP, start/end images, prompt, and official provider pages.")
        print("Stop here until the real provider MP4 is returned.")
        return 0

    for clip, command in commands:
        print(f'\n[{clip["id"]}] -> {root / clip["output"]}')
        if command:
            print(command)
        elif ptype == "krea_mcp":
            print("Use the connected Krea MCP tool after probing model capability and balance; return and link the real MP4 directly.")
        elif ptype in {"vidu_api", "minimax_api", "pixverse_api", "fal_api", "generic_http"}:
            print("Use the authenticated API/MCP adapter. If unavailable, run --handoff instead of asking for an unexplained video upload.")
        elif ptype in {"wan21_flf2v_local", "ltx_local"}:
            print("Run only after a compatible local GPU environment has been detected and the official workflow is installed.")
        elif ptype == "local_diagnostic":
            print("Diagnostic preview only. Do not package production frames or atlases from this output.")

    if args.execute:
        diagnostic = is_diagnostic_provider(provider, ptype)
        if diagnostic and not args.allow_diagnostic:
            raise ValueError(
                "Refusing to create a local crossfade/interpolation as production output. "
                "Run --handoff for a real provider workflow, or pass --allow-diagnostic explicitly for a lightweight labeled preview."
            )
        if ptype not in ("higgsfield_cli", "generic_shell"):
            raise ValueError(f"--execute is not supported for {ptype} without its authenticated adapter")
        for clip, command in commands:
            out = root / clip["output"]
            out.parent.mkdir(parents=True, exist_ok=True)
            print(f'Executing {clip["id"]}...', flush=True)
            if ptype == "higgsfield_cli":
                completed = subprocess.run(command, shell=True, cwd=root, check=True, text=True, capture_output=True)
                job_json = out.with_suffix(out.suffix + ".provider.json")
                job_json.write_text(completed.stdout, encoding="utf-8")
                try:
                    payload = json.loads(completed.stdout)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"Higgsfield returned non-JSON output; saved at {job_json}") from exc
                result_url = find_result_url(payload)
                if not result_url:
                    raise RuntimeError(f"No result URL found in Higgsfield output; inspect {job_json}")
                print(f"Downloading result -> {out}", flush=True)
                urllib.request.urlretrieve(result_url, out)
            else:
                subprocess.run(command, shell=True, cwd=root, check=True)
                if not out.exists():
                    raise RuntimeError(f"generic_shell completed but output is missing: {out}")
            if diagnostic:
                label = out.with_suffix(out.suffix + ".DIAGNOSTIC_ONLY.txt")
                label.write_text(
                    "This is a local diagnostic preview, not a provider-generated or production-ready video.\n",
                    encoding="utf-8",
                )
                print(f"DIAGNOSTIC_PREVIEW_ONLY -> {out}")
            else:
                print(f"PROVIDER_VIDEO_RECEIVED -> {out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
