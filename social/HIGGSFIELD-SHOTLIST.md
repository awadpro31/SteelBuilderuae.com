# Higgsfield shot list — AI-animated reels from real site photos

**Method:** image-to-video. Each shot starts from one of Steel Builder's own site photos (`start_image`),
so every frame shows real work: the structure, crane and site stay as photographed and only the camera and
light move. Do **not** use text-to-video to invent projects, buildings or scale that don't exist. Clients
check, and the footage is presented as your work.

**Model:** Kling v3.0, `mode: pro`, `sound: off`, 9:16, 5 s. **8.75 credits per shot** (Higgsfield quote,
8 Oct 2026). The 12 shots below cost **105 credits**. For hero shots, Veo 3.1 (8 s, 32 credits) costs more but looks better.
Music and titles get added afterwards in our own pipeline (`_build/reels.py`), with the same logo watermark,
title style and end card as the rest of the kit.

Shared prompt suffix (append to every prompt):
> photorealistic documentary footage, keep every steel member, column and beam exactly as in the image, no new
> structures, no text, no logos, natural UAE daylight, subtle heat haze, stable horizon, 24fps cinematic

| # | Start image | Prompt (camera + motion) | Use in |
|---|---|---|---|
| 01 | `source/2.jpg` portal perspective | slow dolly forward down the line of portal frames, low angle, sand dust drifting | Hero reel opener |
| 02 | `source/1.jpg` crane + rafters | slow upward tilt from the column bases to the crane boom against blue sky | Hero reel |
| 03 | `source/3.jpg` crew at connection | gentle orbit around the scaffold tower, workers subtly moving tools at the rafter connection | "Every bolt" reel |
| 04 | `source/4.jpg` purlins + manlift | slow lateral slide right revealing the galvanized purlins catching sunlight | "Purlins" reel |
| 05 | `source/5.jpg` frames + manlift crew | slow pull-back widening from the manlift crew to the whole frame row | Hero reel closer |
| 06 | `../p-sunset.jpg` frames at sunset | very slow push-in, golden sunset light flaring between the steel frames | Brand reel |
| 07 | `../p-crane-lift.jpg` primary beam lift | slow rise following the beam as the crane lifts it, chain gently swaying | "The Lift" B-roll |
| 08 | `../p-erect-boom.jpg` main frame install | parallax drift left, boom in foreground, frame in background | B-roll |
| 09 | `../p-frame-square.jpg` roof structure | top-down slow rotation over the roof grid | Transition shot |
| 10 | `../p-site-wide.jpg` wide site | slow aerial-feel rise revealing the full site footprint | Opener / about |
| 11 | `../p-crane-columns.jpg` column install | slow push toward the column base plate, dust settling | Civil-works reel |
| 12 | `../p-yard.jpg` truck at workshop | slow dolly past the loaded truck leaving the Musaffah workshop | "Workshop to site" reel |

## Reels these shots feed
1. **Hero brand film (30 s):** 10 → 01 → 02 → 03 → 05 → 06 → end card
2. **From workshop to site (20 s):** 12 → 07 → 08 → 11 → end card
3. **Golden hour (15 s):** 06 → 09 → 01 → end card
4. Every shot also works as a 5 s loop for Stories.

## To run
1. Add at least 105 credits to the Higgsfield account (it showed 0 credits on the free plan on 8 Oct 2026).
2. Ask Claude to "run the Higgsfield shot list". The photos get uploaded, the 12 shots are generated as one batch and the reels are cut.
