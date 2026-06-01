# Codex TTS Skills

This repository contains two Codex skills for turning Chinese web-novel chapters into generated TTS audio.

The workflow is intentionally audio-only:

```text
novel chapter
  -> novel-to-tts-script
  -> episode-based TTS narration scripts
  -> tts-script-to-audio
  -> generated audio files
```

These skills do not create videos, find background footage, design captions, or produce shot lists. They are meant for creators who already handle video editing separately and only want Codex to manage the narration/TTS pipeline.

## Skills

### `novel-to-tts-script`

Converts a novel chapter into clean, short-video-ready narration text.

Use it when you have a chapter, outline, or scene and want Codex to:

- split the chapter into episodes;
- rewrite literary prose into spoken narration;
- decide per-episode TTS tone, rhythm, pause, and emotion direction;
- create strong openings and cliffhangers;
- keep each episode suitable for TTS;
- output only text that can later be turned into audio.

It should not output video ideas, B-roll suggestions, background footage categories, or editing instructions unless explicitly asked.

Example prompt:

```text
Use $novel-to-tts-script to convert this first chapter into TTS narration episodes.
Only output the episode title and spoken narration text.
```

### `tts-script-to-audio`

Converts episode narration scripts into generated audio files.

Use it after `novel-to-tts-script` when you want Codex to:

- extract only the spoken text;
- extract per-episode TTS director prompts and pass them to providers such as MiMo;
- preserve episode structure;
- split long narration into manageable audio segments;
- generate stable filenames;
- produce local WAV files with Windows TTS when no external provider is configured;
- generate MiMo V2.5 TTS audio when `MIMO_API_KEY` is configured;
- prepare provider-ready payloads when using an API TTS provider.

Example prompt:

```text
Use $tts-script-to-audio to turn these episode narration scripts into WAV audio files.
```

## Installation

Clone this repository and copy the skill folders into your Codex skills directory.

On Windows:

```powershell
git clone https://github.com/winkovo0818/codex-tts-skills.git
Copy-Item -Recurse .\codex-tts-skills\novel-to-tts-script $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\codex-tts-skills\tts-script-to-audio $env:USERPROFILE\.codex\skills\
```

Expected final layout:

```text
%USERPROFILE%\.codex\skills\novel-to-tts-script\SKILL.md
%USERPROFILE%\.codex\skills\tts-script-to-audio\SKILL.md
```

Restart Codex or start a new thread after installing so the skills can be discovered.

## Xiaomi MiMo TTS Generation

`tts-script-to-audio` includes a Xiaomi MiMo V2.5 TTS helper:

```text
tts-script-to-audio/scripts/synthesize_mimo_tts.py
```

It follows MiMo's chat-style TTS pattern:

- style/director prompt goes in the `user` message;
- exact narration text goes in the `assistant` message;
- preset voices include Chinese voices such as `苏打`, `白桦`, `冰糖`, and `茉莉`.

Example:

```powershell
$env:MIMO_API_KEY="your_api_key"
python .\tts-script-to-audio\scripts\synthesize_mimo_tts.py .\chapter01_tts.md `
  --out-dir .\audio `
  --series guozu2002 `
  --voice 白桦 `
  --format wav `
  --style "用沉稳、有压迫感的男声进行小说口播。语速中等略慢，关键反转前停顿，结尾保留悬念。"
```

## Local Windows Audio Generation

`tts-script-to-audio` includes a Windows TTS helper:

```text
tts-script-to-audio/scripts/synthesize_windows_tts.ps1
```

It can generate `.wav` files from a TTS-only script using installed Windows voices.

Example:

```powershell
powershell -ExecutionPolicy Bypass -File .\tts-script-to-audio\scripts\synthesize_windows_tts.ps1 `
  -InputPath .\chapter01_tts.md `
  -OutDir .\audio `
  -Series guozu2002 `
  -VoiceName "Microsoft Huihui Desktop" `
  -Rate -1
```

The script internally creates segment filenames like:

```text
guozu2002_e01_p01.wav
guozu2002_e02_p01.wav
guozu2002_e03_p01.wav
```

## Notes

- Windows TTS voices vary by machine. If a voice name fails, list installed voices or choose another available Chinese voice.
- Local Windows TTS is useful for testing the pipeline, but production quality may be better with a dedicated provider such as Volcengine, MiniMax, Fish Audio, Azure, or another TTS API.
- Do not clone or imitate a real person's voice without authorization.
- Add AI/TTS labels when your publishing platform requires them.

## Repository Contents

```text
novel-to-tts-script/
  SKILL.md
  agents/openai.yaml
  references/checklist.md
  scripts/estimate_segments.py

tts-script-to-audio/
  SKILL.md
  agents/openai.yaml
  references/tts-qa.md
  scripts/prepare_tts_segments.py
  scripts/synthesize_mimo_tts.py
  scripts/synthesize_windows_tts.ps1
```
