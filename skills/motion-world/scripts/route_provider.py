#!/usr/bin/env python3
"""Recommend a Motion World video-provider route.

This script is deterministic and does not spend credits. The agent should probe
connected tools/accounts first, then pass the available provider IDs here.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_catalog(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("providers"), list):
        raise ValueError("provider catalog must contain a providers array")
    return data


def capability_ok(value: Any, required: bool) -> tuple[bool, bool]:
    """Return (eligible, probe_needed)."""
    if not required:
        return True, False
    if value is True:
        return True, False
    if value in ("probe", "model-dependent"):
        return True, True
    return False, False


def score_provider(
    provider: dict[str, Any],
    *,
    available: set[str],
    preferred: str | None,
    mode: str,
    first_last: bool,
    multi_keyframe: bool,
    allow_paid: str,
    advanced: bool,
) -> tuple[float, list[str]] | None:
    reasons: list[str] = []
    pid = provider["id"]
    access = set(provider.get("access", []))

    if provider.get("advancedOnly") and not advanced:
        return None
    if pid == "preferred_user_provider" and not preferred:
        return None
    if mode != "either" and mode not in access:
        return None
    if provider.get("diagnosticOnly"):
        return None

    caps = provider.get("capabilities", {})
    ok, probe = capability_ok(caps.get("firstLastFrame"), first_last)
    if not ok:
        return None
    if probe:
        reasons.append("first/last-frame support must be confirmed for the selected model")

    ok, probe = capability_ok(caps.get("multiKeyframe"), multi_keyframe)
    if not ok:
        return None
    if probe:
        reasons.append("multi-keyframe support must be confirmed for the selected model")

    free_access = provider.get("freeAccess")
    if allow_paid == "never" and free_access in {"paid", "separate-api-balance"}:
        return None

    score = float(provider.get("priority", 0))
    score += float(provider.get("beginnerScore", 0)) * 2
    score += float(provider.get("qualityScore", 0))

    if pid in available:
        score += 100
        reasons.append("already connected, subscribed, or funded")
    elif pid == "krea_mcp":
        score += 15
        reasons.append("default first probe when no preferred service is available")
    elif access == {"manual"} or "manual" in access:
        score += 5

    if preferred and pid == preferred:
        score += 250
        reasons.append("explicit user preference")

    if provider.get("probeRequired"):
        reasons.append("availability, model capability, and balance must be probed before execution")
    if free_access == "daily-credits":
        reasons.append("may use daily free credits")
    elif free_access == "trial-daily-bonus":
        reasons.append("may use trial or daily bonus credits")
    elif free_access == "paid":
        reasons.append("requires approval before paid generation")

    return score, reasons


def main() -> int:
    here = Path(__file__).resolve().parent
    default_catalog = here.parent / "references" / "provider-catalog.json"

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=default_catalog)
    parser.add_argument("--available", default="", help="Comma-separated connected/subscribed provider IDs")
    parser.add_argument("--preferred", default=None)
    parser.add_argument("--mode", choices=["agent", "api", "cli", "manual", "local", "either"], default="either")
    parser.add_argument("--first-last", action="store_true")
    parser.add_argument("--multi-keyframe", action="store_true")
    parser.add_argument("--allow-paid", choices=["never", "ask", "yes"], default="ask")
    parser.add_argument("--advanced", action="store_true", help="Allow advanced local providers")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    catalog = load_catalog(args.catalog)
    available = {item.strip() for item in args.available.split(",") if item.strip()}

    ranked: list[dict[str, Any]] = []
    for provider in catalog["providers"]:
        result = score_provider(
            provider,
            available=available,
            preferred=args.preferred,
            mode=args.mode,
            first_last=args.first_last,
            multi_keyframe=args.multi_keyframe,
            allow_paid=args.allow_paid,
            advanced=args.advanced,
        )
        if result is None:
            continue
        score, reasons = result
        ranked.append(
            {
                "id": provider["id"],
                "label": provider["label"],
                "score": round(score, 2),
                "reasons": reasons,
                "probeRequired": bool(provider.get("probeRequired")),
                "automation": provider.get("automation"),
                "freeAccess": provider.get("freeAccess"),
            }
        )

    ranked.sort(key=lambda item: (-item["score"], item["id"]))
    ranked = ranked[: max(args.top, 1)]
    payload = {
        "recommended": ranked[0] if ranked else None,
        "alternatives": ranked[1:],
        "paidPolicy": args.allow_paid,
        "executionRule": "Probe the recommended provider and model before generation; ask only before a paid action or when no eligible route is available.",
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if not ranked:
            print("No eligible provider route found.")
            return 2
        print(f"Recommended: {ranked[0]['label']} ({ranked[0]['id']})")
        for reason in ranked[0]["reasons"]:
            print(f"- {reason}")
        if len(ranked) > 1:
            print("Alternatives:")
            for item in ranked[1:]:
                print(f"- {item['label']} ({item['id']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
