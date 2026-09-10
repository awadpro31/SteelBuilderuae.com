# Steel Builder — Website

Steel Builder Metal Industry L.L.C · Musaffah, Abu Dhabi, UAE
Live site: https://awadpro31.github.io/SteelBuilderuae.com/

## How this repo is laid out

Every file sits at the **root of the repository** — there is no `assets` folder.
`index.html` looks for the pictures and videos as neighbours, in the same place.

```
index.html            the website
logo.png              logo (header, hero, footer)
favicon.png           browser tab icon
hero.mp4              background film at the top
hero-poster.jpg       first frame of hero.mp4
film.mp4              full-screen showreel in the middle
film-poster.jpg       first frame of film.mp4
p-portal.jpg          warehouse frame  — About + KIZAD
p-sunset.jpg          portal frames at sunset — gallery + CTA
p-crane-lift.jpg      primary beam lift
p-erect-boom.jpg      main frame installation
p-frame-square.jpg    roof structure
p-site-wide.jpg       wide site view
p-crane-columns.jpg   column installation
p-yard.jpg            transport truck at the workshop
.nojekyll             tells GitHub Pages not to run Jekyll
```

**Do not move these into a folder.** If you do, the pictures stop loading.

## Replacing a picture

Upload the new file with **exactly the same name** — or use the admin panel,
which handles it for you.

## GitHub Pages

Settings → Pages → Deploy from a branch → `main` → `/ (root)`

## Admin panel

Lock icon at the bottom of the page.

```
Email    : ahmed.k@steelbuilderuae.com
Password : Steel@2844
```

Edit → **حفظ** (Save) → **تصدير الموقع** (Export) → upload the exported
`index.html` to the repo, replacing the old one. Changes are not live for
visitors until you upload it.

> The login is a convenience lock, not real security — the check runs in the
> visitor's browser and can be read from the page source.

## Contact details on the site

- Phone / WhatsApp: +971 50 233 2844
- Email: info@steelbuilderuae.com
- Instagram: @steel_builderr
- Musaffah, Abu Dhabi, UAE — 24.353325, 54.513988
- Monday – Saturday, 08:00 – 18:00

Facebook and LinkedIn icons are in the footer, not yet linked.
