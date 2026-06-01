# TTS Production QA

## Before Generation

- Spoken text contains no markdown headings, table pipes, visual notes, or editor-only comments.
- Each segment starts and ends at a natural breath or beat.
- Names, rare words, numbers, dates, and English letters have obvious pronunciation.
- Voice style matches genre and target audience.
- File names are stable and sort correctly.

## After Generation

- Listen to the first 10 seconds and every suspense reveal.
- Check for wrong names, swallowed numbers, awkward pauses, robotic emotion, clipping, and background noise.
- Rerender only the smallest failed segment.
- Normalize loudness across all segments before editing.
- Keep the final audio archive with text source and provider/settings notes.

## Publishing Safety

- Use licensed platform voices or voices the user has authorization to clone.
- Avoid celebrity, streamer, or actor voice imitation without permission.
- Add AI/TTS labels when platform rules require them.
- Keep proof of story rights and voice authorization for commercial accounts.
