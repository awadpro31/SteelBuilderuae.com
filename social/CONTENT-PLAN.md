# Steel Builder — Instagram & TikTok Content Kit

Everything in this folder is ready to post. Logo watermark is on every asset.
Brand facts used are taken only from steelbuilderuae.com (founded Kuwait 2012, UAE 2019,
+81,000 m² of project area, Musaffah workshop, 6 services, contact details).

```
profile/                      profile picture (1080×1080, circle-safe)
feed/                         6 single posts (1080×1350, 4:5)
carousel-project-spotlight/   6-slide carousel (1080×1350)
reels/                        5 reels (1080×1920, 30 fps, H.264, loudness −16 LUFS)
reels/covers/                 5 reel / TikTok covers (title kept inside the 4:5 grid crop)
stories/                      4 stories (1080×1920)
highlight-covers/             5 story-highlight covers
_build/                       source media, fonts and the scripts that render everything
```

Re-render after editing text: `cd social/_build && python3 posts.py && python3 reels.py`
(needs Python 3 + Pillow with libraqm, and ffmpeg).

---

## 1. Profile setup

**Name field (IG):** `Steel Builder | ستيل بيلدر — Steel Structures UAE`
(the name field is searchable — keep "Steel Structures UAE" in it)

**Instagram bio (≤150 chars)**
```
Steel structures · Fabrication · Erection 🇦🇪
Warehouses · Farms · Villas — since 2012
نبني القوة بدقة | Musaffah, Abu Dhabi
👇 Quote on WhatsApp
```
Link: `https://wa.me/971502332844` (or steelbuilderuae.com — WhatsApp converts better for B2B quotes in the Gulf)
Category: *Construction Company* · Contact buttons: Call + WhatsApp + Email `info@steelbuilderuae.com`

**TikTok bio (≤80 chars)**
```
Steel structures UAE 🏗️ نبني القوة بدقة
WhatsApp +971 50 233 2844
```
Switch TikTok to a **Business account** (category: Construction) to unlock the website link and analytics.

**Highlights (in order):** Projects · On Site · Services · About · Contact → covers in `highlight-covers/`.

---

## 2. Two-week launch calendar

Post the **carousel + Reel 01 first** — they establish who you are. Reels go to both IG and TikTok;
stills are Instagram-only (TikTok photo mode is optional for the carousel).

| Day | Instagram | TikTok | Story |
|---|---|---|---|
| 1 Sun | Reel 01 — From Sand to Steel | Reel 01 | Story 01 + share the reel |
| 2 Mon | Carousel — Project Spotlight | — | Story 04 (quote) |
| 3 Tue | Feed 01 — Strength, built precisely | Reel 02 | — |
| 4 Wed | Reel 02 — The Lift | — | Story 02 |
| 5 Thu | Feed 04 — Numbers | Reel 03 | — |
| 6 Sat | Reel 03 — Precision at height | — | Story 03 |
| 8 Mon | Feed 06 — Services | Reel 04 | Story 04 |
| 9 Tue | Reel 04 — Ground works | — | — |
| 10 Wed | Feed 02 — Every bolt by hand | Reel 05 | Story 01 |
| 12 Fri (after Jummah) | Reel 05 — Frame by frame | — | — |
| 13 Sat | Feed 03 — Frame by frame | — | Story 04 |
| 14 Sun | Feed 05 — The difference is in the detail | — | — |

**Grid order tip:** Instagram shows newest first; the plan above leaves Feed 05 / 03 / 02 on the top row
with the carousel cover beneath — a clean, consistent dark-bottom grid.

**Timing (judgement, not measured data — confirm with your own Insights after 2 weeks):** B2B decision-makers
in the UAE scroll early morning and evening — try 7:30–9:00 and 19:00–21:30 GST, Sunday–Thursday.

---

## 3. Captions (copy-paste)

Every caption ends with the same CTA block:
```
📞 WhatsApp: +971 50 233 2844
✉️ info@steelbuilderuae.com
📍 Musaffah, Abu Dhabi
```

### Reel 01 — From Sand to Steel
**On-screen cover:** FROM SAND TO STEEL.
```
From sand to steel. 🏗️
Ground works, excavation, compaction — then the steel goes up, frame by frame.
One team from workshop to site.

من الرمل إلى الهيكل المعدني.
حفر وتسوية ودك، ثم تركيب الهيكل — إطار تلو الإطار.
فريق واحد من الورشة إلى الموقع.

Planning a warehouse or industrial facility? Send us your drawings for a quote.
```

### Reel 02 — The Lift
```
One lift. Zero guesswork. ⛓️
Every rafter is rigged, lifted and bolted to the drawing — with a clear lifting plan before the crane moves.

رفعة واحدة — بلا تخمين.
كل جمالون يُرفع ويُثبَّت حسب الرسم، وبخطة رفع واضحة قبل أن تتحرك الرافعة.
```

### Reel 03 — Precision at height
```
The difference is in the detail.
Connections that fit first time, because the work in our workshop matches the drawing.

الفرق في التفاصيل.
وصلات تركب من أول مرة — لأن التصنيع في ورشتنا مطابق للرسم.
```

### Reel 04 — Ground works
```
Strong steel needs strong ground.
Before a single column stands: excavation, levels and compaction — done in-house.

الهيكل القوي يبدأ من أرض قوية.
قبل تركيب أول عمود: حفر ومناسيب ودك — بفريقنا.
```

### Reel 05 — Frame by frame (photos)
```
Frame by frame. Columns set, rafters lifted, purlins locked in.
Swipe through the build. 👆

إطار تلو الإطار — أعمدة، جمالونات، مدادات.
```
*Add a trending sound in-app — this reel ships silent on purpose (see §5).*

### Carousel — Project Spotlight
```
Project spotlight: from sand to steel. 🏗️
01 Columns set, rafters fly
02 Every bolt, by hand
03 Purlins locked in
04 Frame by frame

Save this post if you're planning a steel building. 🔖

مشروع من أعمالنا: من الرمل إلى الهيكل المعدني.
احفظ المنشور إذا كنت تخطط لمبنى معدني.
```

### Feed 01 — Strength, built precisely
```
Strength, built precisely.
Steel structures for warehouses, farms, villas and industrial facilities across the UAE.

نبني القوة بدقة.
هياكل معدنية للمستودعات والمزارع والفلل والمنشآت الصناعية في الإمارات.
```

### Feed 02 — Every bolt, by hand
```
Every bolt. By hand.
Our erection crew works to the drawing, at height, with safety first.

كل وصلة تُنفَّذ بإتقان — على ارتفاع، والسلامة أولاً.
```

### Feed 03 — Frame by frame
```
Frame by frame, the building takes shape.
إطار تلو الإطار… والمبنى يأخذ شكله.
```

### Feed 04 — In numbers
```
Founded in Kuwait in 2012. In the UAE since 2019. +81,000 m² of project area delivered and under way.

تأسسنا في الكويت عام 2012، وفي الإمارات منذ 2019 — وأكثر من 81,000 م² من المشاريع.
```

### Feed 05 — The difference is in the detail
```
Precision · Quality · Safety · Reliability · On time.
The difference is in the detail.

الدقة · الجودة · السلامة · الموثوقية · التسليم في الموعد.
الفرق في التفاصيل.
```

### Feed 06 — Services
```
Six services. One team.
01 Workshop fabrication  02 Steel structures  03 On-site erection
04 Sandwich panels  05 Metal cladding  06 Civil works

ست خدمات — فريق واحد. من التصنيع في الورشة حتى التسليم.
```

---

## 4. Hashtags

Use **5–8 per post** on Instagram (more no longer helps) and **3–5 on TikTok**. Rotate sets.

- **Core (always):** `#SteelBuilder #SteelStructure #UAEConstruction #AbuDhabi #هياكل_معدنية`
- **Set A – erection reels:** `#SteelErection #Ironworkers #ConstructionLife #Crane`
- **Set B – B2B / clients:** `#WarehouseConstruction #IndustrialConstruction #PEB #Musaffah`
- **Set C – Arabic reach:** `#مقاولات #الإمارات #أبوظبي #بناء #ورشة_حدادة`
- **TikTok:** `#construction #steelstructure #uae #satisfying #fyp`

---

## 5. Platform notes (read before posting)

1. **Music:** reels 01–04 carry the real site sound (crane, machinery) at a normalised level — authentic and
   safe. For more reach, add a trending sound **inside the IG/TikTok editor** and keep the original at ~20 %.
   Never bake commercial music into the file: business accounts are restricted to the commercial sound
   library and copyrighted tracks get muted.
2. **Covers:** upload the matching file from `reels/covers/` as the cover. Titles sit inside the 4:5 crop so
   they survive the profile grid.
3. **Safe zones:** all text sits above the bottom 420 px and away from the right-hand buttons, so captions and
   UI never cover the headline. The logo sits top-left under the status bar.
4. **Instagram "Trial reels":** post Reel 02 and 03 as trial reels first (shown to non-followers); share to
   followers if they beat your average after 48 h.
5. **Pin** Reel 01, the carousel and Feed 06 (services) to the top of the IG grid; pin Reel 01 on TikTok.
6. **Reply to every comment within the first hour** — and move price questions to WhatsApp.
7. **Collaborations:** if the main contractor or client agrees, post Reel 01 as a *Collab* post so it
   appears on both profiles.

---

## 6. Capture list for next site visit (to keep the pipeline full)

Shoot vertical, 4K if the phone allows, 10–15 s per clip, hold still for 3 s at start and end:
- Drone or roof-level timelapse of a full day of erection (best-performing format in this category)
- Workshop: cutting, welding sparks, drilling, part marking
- A truck leaving the Musaffah workshop → arriving on site (same day)
- Before/after from the **same spot**: empty plot → frames → cladded building
- 20-second face-to-camera from the site engineer: "3 mistakes clients make when ordering a steel warehouse"
- Finished project walk-through with the sandwich panels on
