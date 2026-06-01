---
name: tts-script-to-audio
description: Convert TTS-ready口播稿 from novel-to-tts-script or other narration scripts into audio files. Use when the user wants to consume episode scripts, extract only spoken text, clean it, split it into audio segments, create filenames, SSML/pause markup, provider-ready payloads, or directly generate WAV/MP3 audio when a local or API TTS provider is available. Do not add video, caption, cover, or visual suggestions.
---

# TTS Script To Audio

## Operating Goal

Convert finished narration scripts into actual TTS audio whenever possible. This skill starts after `novel-to-tts-script`; it should consume that skill's口播稿 sections, ignore titles/cover/video/analysis, and produce audio files directly. If no external provider is configured, use the bundled Windows TTS script to generate WAV files locally.

## Vendor Decision

Choose the simplest production path that fits the user's scale:

- Jianying/CapCut manual flow: use for early testing, low volume, no code, fastest Douyin publishing.
- Xiaomi MiMo V2.5 TTS: use for novel口播 when the user wants controllable emotion, pacing, style, and preset Chinese voices through API.
- Volcengine or other API flow: use for batch production, recurring series, multiple accounts, or automation.
- MiniMax/Fish Audio/ElevenLabs style flow: use when the user prioritizes emotional acting, character voice consistency, or voice cloning with authorized voices.

If the user has `MIMO_API_KEY` configured, prefer Xiaomi MiMo for Chinese novel narration. Otherwise generate WAV files with local Windows TTS first. Use provider-neutral segment files only as an intermediate artifact, not the final deliverable.

## Workflow

1. Intake the script.
   - Identify episodes, speaker count, language, desired mood, target duration, and target platform.
   - Preserve episode titles and order.
   - If the text came from `novel-to-tts-script`, keep its episode structure.
   - Extract only text under `口播稿` or equivalent spoken-script sections.
   - Discard `标题`, `封面字`, `背景视频`, `字幕`, `发布测试`, and analysis blocks unless explicitly requested.

2. Clean for speech.
   - Remove production-only labels from the spoken text unless they are meant to be read.
   - Convert symbols and abbreviations into speakable Chinese.
   - Break long sentences into TTS-friendly lines.
   - Normalize numbers, dates, names, and uncommon terms when pronunciation may be ambiguous.
   - Keep dramatic wording intact; do not flatten style.

3. Add performance markup.
   - Use lightweight tags: `[停顿0.3秒]`, `[压低声音]`, `[加重]`, `[语速稍慢]`, `[冷笑]`.
   - Put tags on separate lines or before the phrase they affect.
   - Avoid dense markup; too many tags make TTS robotic.
   - For SSML-capable providers, optionally map to SSML in a separate block.

4. Segment for generation.
   - Keep each generated audio file short enough to rerender easily: usually 30-90 seconds.
   - Split at punctuation, paragraph boundaries, or emotional turns.
   - Avoid cutting inside names, suspense phrases, or direct quotes.
   - Create stable filenames: `series_s01e01_p01.mp3`, `series_s01e01_p02.mp3`.

5. Produce the package.
   - Generated audio files.
   - Voice settings.
   - Any failed segments and rerender instructions.
   - Audio QA checklist.

## Output Format

For production packages, use:

```markdown
**TTS生成结果**
音色：
输出格式：
生成文件：

**音频质检**
...
```

For a single short script, output the cleaned script, voice direction, and filename only.

## Spoken Copy Rules

- Prefer short lines: 10-25 Chinese characters.
- Put one breath unit per line.
- Change written forms into speech forms:
  - "2026年6月1日" -> "二零二六年六月一日" if pronunciation matters.
  - "3秒" -> "三秒".
  - "AI/TTS" -> "人工智能配音" or "T T S" depending on context.
- Keep suspense pauses before reveals.
- Remove markdown bullets, table pipes, headings, title/cover fields, visual notes, and publish-test notes from the audio text.
- Keep quoted dialogue if it drives emotion, but clarify speaker changes when one voice reads all roles.

## Voice Direction Patterns

Use simple, repeatable voice settings:

- 悬疑复仇：女声/男声中低音，语速0.92-0.98，情绪克制，关键反转前停顿。
- 都市爽文：中性偏有力，语速1.0-1.08，打脸处加重。
- 情感虐文：柔和、稍慢，语速0.88-0.96，少量气声，避免哭腔过满。
- 玄幻仙侠：沉稳、有叙事感，语速0.94-1.0，人名和设定词读清楚。
- 沙雕轻喜：明亮、快一点，语速1.05-1.15，句尾不要过度上扬。

## Provider Notes

- Xiaomi MiMo V2.5 TTS:
  - Use model `mimo-v2.5-tts` for preset voices.
  - Put style/director instructions in the `user` message.
  - Put the exact narration text in the `assistant` message.
  - Use Chinese preset voices such as `苏打`, `白桦`, `冰糖`, or `茉莉`.
  - Use natural-language style prompts for global emotion/pacing, and inline audio tags only when the user wants fine control.
- Jianying/CapCut: deliver clean text chunks and manual steps. Avoid SSML; use visible pause markers sparingly or replace with punctuation.
- Volcengine/API TTS: deliver JSON/CSV-style segment sheet, filenames, voice parameters, and retry notes.
- MiniMax/Fish/ElevenLabs: include style prompts and consistency notes. Use only authorized/cloned voices.
- Always mention that platform-required AI/TTS labels should be applied when publishing.

## Useful Scripts

Use `scripts/synthesize_mimo_tts.py` to generate audio with Xiaomi MiMo when `MIMO_API_KEY` is available.

Example:

```powershell
$env:MIMO_API_KEY="your_api_key"
python scripts/synthesize_mimo_tts.py input.md --out-dir output_audio --series mynovel --voice 白桦 --format wav
```

Use `scripts/synthesize_windows_tts.ps1` to generate WAV audio locally from a TTS-only script when no API provider is configured. It calls `prepare_tts_segments.py` internally.

```powershell
powershell -ExecutionPolicy Bypass -File scripts/synthesize_windows_tts.ps1 -InputPath input.md -OutDir output_audio -Series mynovel -VoiceName "Microsoft Kangkang" -Rate -1
```

Use `scripts/prepare_tts_segments.py` only when the user explicitly asks for text/CSV rather than audio.

## References

Read `references/tts-qa.md` before final delivery when the package includes audio generation instructions.
