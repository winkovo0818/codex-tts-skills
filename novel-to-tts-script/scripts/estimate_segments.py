#!/usr/bin/env python3
"""Estimate Chinese TTS speaking time and rough short-video segment counts."""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path


def count_cjk_and_words(text: str) -> int:
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    latin_words = re.findall(r"[A-Za-z0-9]+", text)
    return len(cjk) + len(latin_words)


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate TTS segmentation for novel chapters.")
    parser.add_argument("input", help="Path to a UTF-8 text file.")
    parser.add_argument("--target-seconds", type=int, default=90, help="Target seconds per episode.")
    parser.add_argument("--cpm", type=int, default=280, help="Estimated Chinese characters per minute.")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    units = count_cjk_and_words(text)
    minutes = units / args.cpm if args.cpm else 0
    target_units = args.cpm * args.target_seconds / 60
    segments = max(1, math.ceil(units / target_units)) if target_units else 1
    avg_units = math.ceil(units / segments)
    avg_seconds = avg_units / args.cpm * 60 if args.cpm else 0

    print(f"estimated_units={units}")
    print(f"estimated_minutes={minutes:.1f}")
    print(f"target_seconds={args.target_seconds}")
    print(f"suggested_segments={segments}")
    print(f"average_units_per_segment={avg_units}")
    print(f"average_seconds_per_segment={avg_seconds:.0f}")
    print("note=Use this only for sizing; final cuts should follow story beats.")


if __name__ == "__main__":
    main()
