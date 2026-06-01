#!/usr/bin/env python3
"""Generate TTS audio with Xiaomi MiMo V2.5 TTS.

Requires MIMO_API_KEY in the environment.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError


API_URL = "https://api.xiaomimimo.com/v1/chat/completions"


DEFAULT_STYLE = (
    "用适合小说口播的沉稳叙事男声来读。语速中等略慢，咬字清楚，"
    "前半段压住情绪，关键反转前稍作停顿，结尾保留悬念感。"
)


def prepare_segments(input_path: Path, out_dir: Path, series: str, target_chars: int) -> Path:
    script_path = Path(__file__).with_name("prepare_tts_segments.py")
    csv_path = out_dir / f"{series}_segments.csv"
    subprocess.run(
        [
            sys.executable,
            str(script_path),
            str(input_path),
            "--series",
            series,
            "--target-chars",
            str(target_chars),
            "--out",
            str(csv_path),
        ],
        check=True,
    )
    return csv_path


def call_mimo(api_key: str, text: str, style: str, voice: str, model: str, audio_format: str) -> bytes:
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": style},
            {"role": "assistant", "content": text},
        ],
        "audio": {
            "format": audio_format,
            "voice": voice,
        },
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        API_URL,
        data=data,
        headers={
            "api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"MiMo API HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"MiMo API request failed: {exc}") from exc

    result = json.loads(body)
    try:
        audio_data = result["choices"][0]["message"]["audio"]["data"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"MiMo API response did not contain audio data: {body[:1000]}") from exc
    return base64.b64decode(audio_data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate audio files using Xiaomi MiMo V2.5 TTS.")
    parser.add_argument("input", help="Path to a TTS-only script markdown/text file.")
    parser.add_argument("--out-dir", required=True, help="Directory for generated audio.")
    parser.add_argument("--series", default="series", help="Series slug for output filenames.")
    parser.add_argument("--voice", default="白桦", help="MiMo preset voice, e.g. 苏打, 白桦, 冰糖, 茉莉.")
    parser.add_argument("--model", default="mimo-v2.5-tts", help="MiMo TTS model ID.")
    parser.add_argument("--format", default="wav", choices=["wav", "mp3", "pcm16"], help="Audio format.")
    parser.add_argument("--style", default=DEFAULT_STYLE, help="Natural-language style/director prompt.")
    parser.add_argument("--target-chars", type=int, default=420, help="Target characters per audio segment.")
    parser.add_argument("--api-key-env", default="MIMO_API_KEY", help="Environment variable containing API key.")
    args = parser.parse_args()

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        raise SystemExit(f"Missing API key. Set {args.api_key_env} first.")

    input_path = Path(args.input)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = prepare_segments(input_path, out_dir, args.series, args.target_chars)

    generated: list[Path] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = Path(row["filename"]).with_suffix(f".{args.format}").name
            out_path = out_dir / filename
            text = row["text"].replace("\r\n", "\n").strip()
            audio = call_mimo(api_key, text, args.style, args.voice, args.model, args.format)
            out_path.write_bytes(audio)
            generated.append(out_path)
            print(f"wrote={out_path}")

    print(f"segments_csv={csv_path}")
    print(f"files={len(generated)}")


if __name__ == "__main__":
    main()
