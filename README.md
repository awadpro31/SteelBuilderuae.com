# Steel Builder — Website

Company website for **Steel Builder Metal Industry L.L.C**, Musaffah, Abu Dhabi, UAE.

---

## Publish on GitHub Pages

1. Upload **all the files in this folder** to the repository — including the
   `assets` folder and the hidden `.nojekyll` file.
   The files must sit at the **top level of the repo**, not inside another folder.
2. Repo → **Settings** → **Pages**
3. **Source:** Deploy from a branch · **Branch:** `main` · **Folder:** `/ (root)`
4. Save, wait 1–2 minutes, open the link GitHub gives you.

The repository must be **public** (GitHub Pages needs Pro for private repos).

---

## Which file is the website?

| File | What it is |
|---|---|
| `index.html` | **The live site.** Videos, photos and logo are embedded inside the file. Nothing external to break. This is what visitors see. |
| `index-fast.html` | Same site, but loads media from `assets/`. Roughly 25× smaller and faster — use it once you've confirmed `assets/` uploaded correctly. |
| `assets/` | The videos, photos, logo and favicon. |
| `.nojekyll` | Tells GitHub not to process the site with Jekyll. Do not delete. |
| `Steel-Builder-Company-Profile.pdf` | 12-page company profile, print-ready A4. |

### To switch to the fast version later
Rename `index.html` to `index-full.html`, then rename `index-fast.html` to `index.html`.
If photos disappear after switching, the `assets` folder did not upload — switch back.

---

## Admin panel

Scroll to the bottom of the site and click the **lock icon** next to the language button.

```
Email    : ahmed.k@steelbuilderuae.com
Password : Steel@2844
```

**Editing workflow**

1. Log in and make your changes
2. Press **حفظ** (Save)
3. Press **تصدير الموقع** (Export) — downloads a new `index.html`
4. Upload that file to the repo, replacing the old one

Your edits are **not visible to visitors** until you finish steps 3 and 4.

> **Security note:** this login is a convenience lock, not real protection. The
> password check runs in the visitor's browser and can be read from the page
> source. Do not reuse this password anywhere that matters.

---

## Contact details on the site

- Phone / WhatsApp: +971 50 233 2844
- Email: info@steelbuilderuae.com
- Instagram: @steel_builderr
- Location: Musaffah, Abu Dhabi, UAE — 24.353325, 54.513988
- Hours: Monday – Saturday, 08:00 – 18:00

Facebook and LinkedIn icons are in the footer but not yet linked — add the URLs
when you have them.

---

## Features

- Arabic (RTL) by default, English (LTR) toggle, full layout flip
- Night mode and day mode (navy & white)
- Full-screen video hero and full-screen showreel section
- Project gallery with detail pop-ups, plus a six-project data table
- Floating WhatsApp button
- Built-in admin panel
- Tested at 320 / 360 / 390 / 430 / 768 / 1024 / 1440 / 1920 px
- No frameworks, no build step, no database
