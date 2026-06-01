#!/usr/bin/env python3
"""Create a CSV sheet of TTS-sized text segments with stable filenames."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


SPLIT_RE = re.compile(r"(?<=[。！？!?；;])\s*|\n+")


EPISODE_HEADING_RE = re.compile(r"^#{1,6}\s*第\s*(\d+|[一二三四五六七八九十百]+)\s*集[：:：\s]*(.*)$", re.M)


def chinese_num_to_int(value: str) -> int:
    if value.isdigit():
        return int(value)
    digits = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    if value == "十":
        return 10
    if "十" in value:
        left, _, right = value.partition("十")
        tens = digits.get(left, 1) if left else 1
        ones = digits.get(right, 0) if right else 0
        return tens * 10 + ones
    return digits.get(value, 1)


def clean_text(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.M)
    text = text.replace("|", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_episodes(text: str) -> list[tuple[int, str, str]]:
    matches = list(EPISODE_HEADING_RE.finditer(text))
    if not matches:
        return [(1, "", text)]

    episodes: list[tuple[int, str, str]] = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        number = chinese_num_to_int(match.group(1))
        title = match.group(2).strip()
        body = text[start:end].strip()
        episodes.append((number, title, body))
    return episodes


def split_sentences(text: str) -> list[str]:
    parts = [p.strip() for p in SPLIT_RE.split(text) if p and p.strip()]
    return parts


def pack_segments(sentences: list[str], target_chars: int, min_chars: int = 80) -> list[str]:
    segments: list[str] = []
    current: list[str] = []
    current_len = 0

    for sentence in sentences:
        sentence_len = len(sentence)
        if current and current_len + sentence_len > target_chars:
            segments.append("\n".join(current))
            current = [sentence]
            current_len = sentence_len
        else:
            current.append(sentence)
            current_len += sentence_len

    if current:
        segments.append("\n".join(current))
    if len(segments) > 1 and len(segments[-1]) < min_chars:
        tail = segments.pop()
        segments[-1] = f"{segments[-1]}\n{tail}"
    return segments


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare TTS segment CSV.")
    parser.add_argument("input", help="Path to a UTF-8 text file.")
    parser.add_argument("--series", default="series", help="Series slug for filenames.")
    parser.add_argument("--episode", type=int, default=1, help="Episode number if no episode headings exist.")
    parser.add_argument("--target-chars", type=int, default=350, help="Target characters per audio file.")
    parser.add_argument("--min-chars", type=int, default=80, help="Merge trailing segments shorter than this.")
    parser.add_argument("--cpm", type=int, default=280, help="Estimated Chinese characters per minute.")
    parser.add_argument("--out", default="tts_segments.csv", help="Output CSV path.")
    args = parser.parse_args()

    raw = Path(args.input).read_text(encoding="utf-8")
    episodes = extract_episodes(raw)

    out_path = Path(args.out)
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["filename", "episode", "episode_title", "part", "estimated_seconds", "text"],
        )
        writer.writeheader()
        total_segments = 0
        for episode_number, episode_title, episode_text in episodes:
            number = episode_number if matches_episode_heading(raw) else args.episode
            cleaned = clean_text(episode_text)
            sentences = split_sentences(cleaned)
            segments = pack_segments(sentences, args.target_chars, args.min_chars)
            for i, text in enumerate(segments, start=1):
                filename = f"{args.series}_e{number:02d}_p{i:02d}.mp3"
                estimated_seconds = round(len(text) / args.cpm * 60)
                writer.writerow(
                    {
                        "filename": filename,
                        "episode": number,
                        "episode_title": episode_title,
                        "part": i,
                        "estimated_seconds": estimated_seconds,
                        "text": text,
                    }
                )
                total_segments += 1

    print(f"wrote={out_path}")
    print(f"segments={total_segments}")


def matches_episode_heading(text: str) -> bool:
    return EPISODE_HEADING_RE.search(text) is not None


if __name__ == "__main__":
    main()
