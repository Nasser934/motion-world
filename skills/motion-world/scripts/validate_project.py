#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def fail(msg: str) -> None:
    raise ValueError(msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    args = ap.parse_args()
    path = Path(args.project)
    data = json.loads(path.read_text(encoding="utf-8"))

    if data.get("schemaVersion") != "0.2":
        fail("schemaVersion must be 0.2")
    if not data.get("project", {}).get("id"):
        fail("project.id is required")
    if not data.get("clips"):
        fail("at least one clip is required")
    if not data.get("runtimes"):
        fail("at least one runtime is required")
    if not data.get("processing", {}).get("profiles"):
        fail("processing.profiles is required")

    provider_type = data.get("videoProvider", {}).get("type")
    allowed_providers = {
        "auto_router",
        "higgsfield_cli",
        "krea_mcp",
        "krea_manual",
        "dreamina_manual",
        "vidu_manual",
        "vidu_api",
        "minimax_api",
        "pixverse_api",
        "fal_api",
        "wan21_flf2v_local",
        "ltx_local",
        "local_diagnostic",
        "generic_shell",
        "generic_http",
        "manual",
    }
    if provider_type not in allowed_providers:
        fail(f"unsupported video provider: {provider_type}")

    policy = data.get("providerPolicy", {})
    paid_policy = policy.get("paidPolicy", "ask")
    if paid_policy not in {"never", "ask", "yes"}:
        fail("providerPolicy.paidPolicy must be never, ask, or yes")

    allowed_states = {
        None,
        "PROVIDER_DISCOVERY",
        "PROVIDER_AUTH_REQUIRED",
        "PROVIDER_FREE_BALANCE_AVAILABLE",
        "PROVIDER_PAID_APPROVAL_REQUIRED",
        "PROVIDER_MODEL_UNAVAILABLE",
        "MANUAL_PROVIDER_REQUIRED",
        "PROVIDER_VIDEO_RECEIVED",
        "PROVIDER_VIDEO_REJECTED",
        "DIAGNOSTIC_PREVIEW_ONLY",
        "PRODUCTION_ASSETS_GENERATED",
        "INTEGRATION_VERIFIED",
    }
    state = data.get("generationState")
    if state not in allowed_states:
        fail(f"unsupported generationState: {state}")

    canvas_ids = {c.get("id") for c in data.get("canvases", [])}
    clip_ids = set()
    for i, clip in enumerate(data["clips"]):
        cid = clip.get("id")
        if not cid:
            fail(f"clips[{i}].id is required")
        if cid in clip_ids:
            fail(f"duplicate clip id: {cid}")
        clip_ids.add(cid)
        if clip.get("canvas") and clip["canvas"] not in canvas_ids:
            fail(f'clip {cid} references unknown canvas {clip["canvas"]}')
        if not clip.get("promptFile"):
            fail(f"clip {cid} promptFile is required")
        if not clip.get("output"):
            fail(f"clip {cid} output is required")
        if clip.get("durationSeconds", 1) <= 0:
            fail(f"clip {cid} durationSeconds must be > 0")

    allowed_profiles = {"scrub", "frames", "atlas", "playback", "posters"}
    unknown = set(data["processing"]["profiles"]) - allowed_profiles
    if unknown:
        fail(f"unknown processing profiles: {sorted(unknown)}")

    allowed_drivers = {
        "elapsed_time",
        "countdown",
        "count",
        "scroll",
        "drag",
        "sensor",
        "state_machine",
        "audio",
        "network",
        "custom",
    }
    driver = data.get("driver", {}).get("type")
    if driver not in allowed_drivers:
        fail(f"unsupported driver: {driver}")

    print(
        f'OK: {path} ({len(clip_ids)} clip(s), {len(data["runtimes"])} runtime(s), '
        f'provider={provider_type}, state={state or "unspecified"})'
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
