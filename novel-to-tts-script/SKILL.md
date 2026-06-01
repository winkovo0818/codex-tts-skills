---
name: novel-to-tts-script
description: Convert Chinese web-novel chapters, outlines, or scenes into TTS-ready short-video narration scripts. Use when the user wants to adapt a novel chapter of about 5000 Chinese characters or less into episode cuts, spoken口播稿, hooks, clean TTS text, titles, or cliffhangers for Douyin/TikTok/Kuaishou narration accounts. Do not include video, B-roll, decompression-video, or visual production suggestions unless the user explicitly asks for them.
---

# Novel To TTS Script

## Operating Goal

Turn long-form fiction into TTS narration episodes that can hold retention: strong first sentence, one conflict per clip, spoken-language pacing, clear cliffhanger, and clean text another TTS skill can consume.

Prefer making an immediately usable script package over giving generic advice. If the user supplies only a chapter, infer genre, selling point, and target length. Ask questions only when rights, platform, or desired tone are impossible to infer.

## Default Assumptions

- Target platform: Douyin.
- Chapter length: under 5000 Chinese characters.
- Spoken speed: 280 Chinese characters per minute unless user specifies another voice speed.
- Episode length: 60-120 seconds for testing; 2-4 minutes for deeper followers; never adapt a 5000-character chapter as one undifferentiated clip unless explicitly requested.
- Video output: omit video, B-roll, decompression-video, and visual notes by default. The user may find visuals independently. Include visual guidance only when explicitly requested.
- Style: dramatic but not clickbait beyond the story facts.
- Output language: Chinese unless the user requests otherwise.
- Rights: assume user owns the story when they say it is their own novel. For third-party text, warn that authorization is needed before publishing.

## Workflow

1. Diagnose the chapter.
   - Identify genre, protagonist, antagonist/pressure source, core desire, secret, reversal, and strongest emotional hook.
   - Mark the best opening line candidate. If the original opening is slow, create a sharper cold open based on a later scene.

2. Build an episode map.
   - Cut by tension beats, not equal word count.
   - Each episode should contain: hook, setup, conflict escalation, micro-payoff, cliffhanger.
   - Keep one main information reveal per episode.
   - Preserve continuity by ending with a question, threat, discovery, reversal, or interrupted action.

3. Rewrite into oral TTS script.
   - Convert literary narration into speakable sentences.
   - Shorten long descriptions; keep sensory details only when they carry mood or plot.
   - Favor actions, dialogue, and consequence over exposition.
   - Replace dense names/titles with clear repeated references if the listener may be confused.
   - Use punctuation to guide TTS breathing: short commas, full stops, and paragraph breaks.
   - Decide the voice direction while cutting the script: tone, tempo, pauses, intensity, and emotional arc.

4. Add TTS text package.
   - Title: 3-5 options with conflict, identity, or reversal.
   - Cover text: 6-12 Chinese characters, punchy and readable.
   - TTS direction: per-episode voice type, emotion curve, speed, pauses, and emphasized words. This should be usable as the next skill's provider style prompt.
   - Clean口播稿: no markdown inside spoken text, one breath unit per line.
   - Compliance notes: mark AI/TTS use where platform rules require it; avoid unauthorized voices or copied footage.

5. Add test plan.
   - Suggest 3-5 alternate hooks for the first episode.
   - Recommend what to A/B test: first sentence, cover text, title, voice, or length.
   - Define success signals: 3-second hold, completion, comments asking for follow-up, profile visits, and saves.

## Output Format

Use this format for a full chapter adaptation:

```markdown
**改编判断**
题材：
核心卖点：
目标受众：
建议切分：

**分集地图**
| 集数 | 时长 | 剧情功能 | 开头钩子 | 语气节奏 | 结尾悬念 |
|---|---:|---|---|---|---|

**第1集成片脚本**
标题：
封面字：
TTS导演提示：
口播稿：

**后续分集脚本**
...

**发布测试**
...
```

For quick requests, output only the episode map plus the first complete script.

## Hook Patterns

Use story-specific facts, then sharpen with one of these patterns:

- Death/rebirth: "我死后的第X天，..."
- Betrayal: "成亲当天，...却..."
- Status reversal: "所有人都以为我是X，直到..."
- Forbidden secret: "师父临死前，只让我记住一句话..."
- Countdown: "再过一炷香，我就会..."
- Discovery: "我推开门时，才知道..."
- Public humiliation: "全城都在等我出丑，可他们不知道..."
- Impossible choice: "救他，还是杀他，我只剩三息。"

Do not invent facts that contradict the chapter. If creating a cold open from a later scene, keep it truthful and later resolve it.

## TTS Writing Rules

- Prefer 8-22 Chinese characters per sentence.
- Start paragraphs with concrete action or consequence.
- Use names sparingly; repeat relationship labels where helpful: "我妹妹", "那位太子", "师父".
- Remove web-novel filler such as excessive inner monologue, redundant adjectives, and repeated shock reactions.
- Keep one signature line per episode that could become a comment quote.
- Add pause markers only when useful: `[停顿]`, `[压低声音]`, `[加重]`.
- Avoid emoji and excessive punctuation in scripts intended for TTS.

## TTS Direction Rules

Each episode should include a provider-ready director prompt. Write it in natural Chinese so TTS providers such as MiMo can use it directly.

Include:

- Voice type: male/female, age feel, texture, narration style.
- Tempo: slow, medium, slightly fast, with approximate intent rather than numbers when possible.
- Emotional curve: where to suppress, build, pause, or release.
- Emphasis: 2-4 key words or sentences.
- Ending: whether to drop voice, suspend, hard stop, or leave suspense.

Good example:

```text
TTS导演提示：用沉稳中低音男声讲述，语速中等略慢。前半段像刚醒来一样压低、疑惑；看到日期后明显放慢；读到“二零零二年五月二十九日”时加重并停顿；结尾保留震惊和悬念，不要热血。
```

Bad example:

```text
TTS：男声，正常读。
```

## Do Not Include Unless Asked

- Video suggestions.
- Background素材 categories.
- B-roll prompts.
- Shot lists.
- Scene-by-scene visual directions.
- Editing steps for video.

If the user asks only for TTS content, output only episode metadata and spoken text.

## Useful Script

Use `scripts/estimate_segments.py` when the user provides a chapter as a file or large text and you need quick character counts, rough speaking time, and suggested segment count.

Example:

```bash
python scripts/estimate_segments.py chapter.txt --target-seconds 90 --cpm 280
```

Then adapt by story beats; do not blindly cut at the suggested boundaries.

## References

Read `references/checklist.md` when you need a concise QA checklist before delivering scripts.
