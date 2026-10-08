"""Builds the single ready-to-publish zip (<30 MB): python3 package.py <out_dir>"""
import os, sys, shutil, subprocess, glob, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SOC = os.path.dirname(HERE)
OUTDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SOC, "zips")
KIT = os.path.join(OUTDIR, "Steel-Builder-Social-Kit")
shutil.rmtree(KIT, ignore_errors=True)
os.makedirs(KIT)

PHONE = "+971 50 233 2844"
CTA = f"\n\n📞 WhatsApp: {PHONE}\n✉️ info@steelbuilderuae.com\n📍 Musaffah, Abu Dhabi"
IGT = "#SteelBuilder #SteelStructure #UAEConstruction #AbuDhabi #هياكل_معدنية"
TT = "#construction #steelstructure #uae #هياكل_معدنية #fyp"

# captions live in CONTENT-PLAN.md; pull each fenced block that follows a "### " heading
plan = open(os.path.join(SOC, "CONTENT-PLAN.md"), encoding="utf-8").read()
blocks = dict(re.findall(r"### ([^\n]+)\n(?:[^\n]*\n)??```\n(.*?)```", plan, re.S))
def cap(h, extra, tiktok=False):
    body = blocks[h].strip()
    return body + CTA + "\n\n" + (TT if tiktok else IGT + " " + extra) + "\n"

def cp(src, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy(os.path.join(SOC, src), dst_dir)

DAYS = [
 ("Day01_Reel_From-Sand-to-Steel", "Reel 01 — From Sand to Steel", "#SteelErection #WarehouseConstruction #Musaffah",
  ["reels/reel-01-from-sand-to-steel.mp4", "reels/covers/reel-01-cover.jpg", "stories/01-live-from-site.jpg"],
  "REEL — upload the video, choose the cover image. Then post the story image and share the reel to your story."),
 ("Day02_Carousel_Project-Spotlight", "Carousel — Project Spotlight", "#WarehouseConstruction #PEB #Musaffah",
  sorted("carousel-project-spotlight/" + f for f in os.listdir(os.path.join(SOC, "carousel-project-spotlight"))),
  "CAROUSEL — select all 6 images in order 01 → 06."),
 ("Day03_Post_Strength-Built-Precisely", "Feed 01 — Strength, built precisely", "#IndustrialConstruction #الإمارات",
  ["feed/01-strength-built-precisely.jpg"], "POST — single image."),
 ("Day04_Reel_The-Lift", "Reel 02 — The Lift", "#SteelErection #Crane #ConstructionLife",
  ["reels/reel-02-the-lift.mp4", "reels/covers/reel-02-cover.jpg", "stories/02-this-week.jpg"],
  "REEL — upload the video, choose the cover image."),
 ("Day05_Post_Numbers", "Feed 04 — In numbers", "#مقاولات #الإمارات", ["feed/04-numbers.jpg"], "POST — single image."),
 ("Day06_Reel_Precision-at-Height", "Reel 03 — Precision at height", "#Ironworkers #SteelErection #مقاولات",
  ["reels/reel-03-precision-at-height.mp4", "reels/covers/reel-03-cover.jpg", "stories/03-precision.jpg"],
  "REEL — upload the video, choose the cover image."),
 ("Day08_Post_Services", "Feed 06 — Services", "#SandwichPanel #Cladding #ورشة_حدادة",
  ["feed/06-services.jpg", "stories/04-request-a-quote.jpg"],
  "POST — single image. STORY: request-a-quote, add a Link sticker → https://wa.me/971502332844"),
 ("Day09_Reel_Ground-Works", "Reel 04 — Ground works", "#CivilWorks #IndustrialConstruction #أبوظبي",
  ["reels/reel-04-ground-works.mp4", "reels/covers/reel-04-cover.jpg"], "REEL — upload the video, choose the cover image."),
 ("Day10_Post_Every-Bolt-by-Hand", "Feed 02 — Every bolt, by hand", "#Ironworkers #ConstructionLife",
  ["feed/02-every-bolt-by-hand.jpg"], "POST — single image."),
 ("Day12_Reel_Frame-by-Frame", "Reel 05 — Frame by frame (photos)", "#PEB #WarehouseConstruction #بناء",
  ["reels/reel-05-frame-by-frame-photos.mp4", "reels/covers/reel-05-cover.jpg"],
  "REEL — SILENT on purpose: add a trending sound in the Instagram / TikTok editor."),
 ("Day13_Post_Frame-by-Frame", "Feed 03 — Frame by frame", "#SteelErection #بناء", ["feed/03-frame-by-frame.jpg"], "POST — single image."),
 ("Day14_Post_The-Detail", "Feed 05 — The difference is in the detail", "#IndustrialConstruction #Musaffah",
  ["feed/05-detail.jpg"], "POST — single image."),
]
POST = os.path.join(KIT, "2_POSTING-PLAN")
for name, head, extra, files, how in DAYS:
    d = os.path.join(POST, name)
    for f in files:
        cp(f, d)
    open(os.path.join(d, "CAPTION.txt"), "w").write(how + "\n\n----- COPY BELOW -----\n\n" + cap(head, extra))
    if "Reel" in name:
        open(os.path.join(d, "CAPTION-TIKTOK.txt"), "w").write(
            "TIKTOK — same video + cover. Pin Reel 01 to your TikTok profile.\n\n----- COPY BELOW -----\n\n"
            + cap(head, extra, tiktok=True))

# ---- profile + highlights
PRO = os.path.join(KIT, "1_PROFILE-AND-HIGHLIGHTS")
cp("profile/profile-picture-1080.jpg", PRO)
LINKS = {
 "01-projects": ("Projects", "No sticker needed."),
 "02-services": ("Services", "Add a Link sticker → https://steelbuilderuae.com"),
 "03-on-site": ("On Site", "Add new site stories here every week."),
 "04-about": ("About", "No sticker needed."),
 "05-whatsapp": ("WhatsApp", "Add a Link sticker → https://wa.me/971502332844  (label it: WhatsApp)"),
 "06-location": ("Location", "Add a Location sticker → search 'Musaffah' (or your workshop's Google listing),\n   or a Link sticker → https://maps.google.com/?q=24.353325,54.513988  (label it: Directions)"),
 "07-call": ("Call", "Instagram link stickers accept web links only (no tel:). Add a Link sticker →\n   https://wa.me/971502332844 labelled 'Call / WhatsApp' — the number is printed on the story."),
 "08-email": ("Email", "Link stickers accept web links only (no mailto:). Add a Link sticker →\n   https://steelbuilderuae.com/#contact labelled 'Send drawings'."),
 "09-website": ("Website", "Add a Link sticker → https://steelbuilderuae.com"),
}
for key, (label, sticker) in LINKS.items():
    d = os.path.join(PRO, "highlights", f"{key}_{label.replace(' ', '-')}")
    cp(f"highlight-covers/{key}.jpg", d)
    os.rename(os.path.join(d, f"{key}.jpg"), os.path.join(d, "COVER.jpg"))
    for f in sorted(glob.glob(os.path.join(SOC, "highlight-stories", key, "*.jpg"))):
        shutil.copy(f, os.path.join(d, "story-" + os.path.basename(f)))
    open(os.path.join(d, "HOW-TO.txt"), "w").write(
        f"HIGHLIGHT NAME: {label}\n\n1. Post each story-*.jpg as a Story (in number order).\n"
        f"2. Sticker: {sticker}\n   Place it in the empty space under the orange arrow.\n"
        f"3. Profile → + New highlight → select these stories → name it \"{label}\" → Edit cover → pick COVER.jpg.\n")

open(os.path.join(PRO, "BIO-AND-SETUP.txt"), "w").write("""PROFILE — @steelbuilderuae

!! FIX FIRST: the current profile picture says "STYLE BUILDER" — that is not your logo.
   Replace it with profile-picture-1080.jpg (STEEL BUILDER logo).

INSTAGRAM
Name:  Steel Builder | ستيل بيلدر — Steel Structures UAE
Bio (copy the 4 lines):
Steel structures · Fabrication · Erection 🇦🇪
Warehouses · Farms · Villas — since 2012
نبني القوة بدقة | Musaffah, Abu Dhabi
👇 Quote on WhatsApp
Links (Edit profile → Links, add both):
  1. https://wa.me/971502332844   title: WhatsApp — Request a quote
  2. https://steelbuilderuae.com  title: Website
Switch to Professional account → Business → Category: Construction Company
Contact options: Phone + WhatsApp +971 50 233 2844, Email info@steelbuilderuae.com,
Address: Musaffah, Abu Dhabi, UAE (this adds a "Directions" button on the profile).

HIGHLIGHTS (create in this order so they show left → right):
Projects · Services · On Site · About · WhatsApp · Location · Call · Email · Website
Each folder in /highlights has the cover, the stories and a HOW-TO.txt.

TIKTOK — same handle @steelbuilderuae
Bio:
Steel structures UAE 🏗️ نبني القوة بدقة
WhatsApp +971 50 233 2844
Switch to Business account → Category: Construction; add website steelbuilderuae.com.

WEBSITE: steelbuilderuae.com still links Instagram as @steel_builderr — update it to @steelbuilderuae.
""")
open(os.path.join(KIT, "START-HERE.txt"), "w").write("""STEEL BUILDER — SOCIAL KIT (Instagram + TikTok)  @steelbuilderuae

STEP 1  1_PROFILE-AND-HIGHLIGHTS
        - Change the profile picture (current one says "STYLE BUILDER" — wrong logo)
        - Paste the bio + links from BIO-AND-SETUP.txt
        - Build the 9 highlights: each folder has COVER.jpg + stories + HOW-TO.txt
STEP 2  2_POSTING-PLAN
        - Post one Day folder per day, in order. CAPTION.txt = Instagram, CAPTION-TIKTOK.txt = TikTok.
Best times (UAE): 07:30–09:00 or 19:00–21:30, Sunday–Thursday.
All media is final size with the logo watermark: posts 1080x1350, stories/reels 1080x1920.
""")

# ---- compress for one <30 MB download
for f in glob.glob(os.path.join(KIT, "**", "*.mp4"), recursive=True):
    tmp, log = f + ".tmp.mp4", os.path.join(OUTDIR, "x264")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-c:v", "libx264", "-preset", "slow", "-b:v", "1500k",
                    "-pass", "1", "-passlogfile", log, "-an", "-f", "mp4", os.devnull], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-c:v", "libx264", "-preset", "slow", "-b:v", "1500k",
                    "-maxrate", "2200k", "-bufsize", "3000k", "-pass", "2", "-passlogfile", log,
                    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, f)
for p in glob.glob(os.path.join(OUTDIR, "x264*")):
    os.remove(p)
for f in glob.glob(os.path.join(KIT, "**", "*.jpg"), recursive=True):
    Image.open(f).save(f, "JPEG", quality=86, optimize=True, progressive=True)

zp = os.path.join(OUTDIR, "Steel-Builder-Social-Kit.zip")
if os.path.exists(zp):
    os.remove(zp)
subprocess.run(["zip", "-qr", "-9", zp, "Steel-Builder-Social-Kit"], cwd=OUTDIR, check=True)
print(zp, os.path.getsize(zp) // 1024 // 1024, "MB")
