# Reyimation website - kaise use karna hai

## Naya project add karna (3 step)
1. `projects/` me naya folder banao (naam chhota, bina space: `nova-brand-film`).
   Ya `projects/_TEMPLATE` ko copy karke rename kar do.
2. Folder me daalo:
   - `video.mp4`  (apni original video, kuch bhi size)
   - `thumb.jpg`  (optional - nahi daaloge to video se auto ban jayega)
   - `info.json`  (optional - nahi daaloge to auto ban jayega, phir edit kar lena)
3. **UPDATE-SITE.bat** (Windows) ya **update-site.command** (Mac) double-click karo.
   Bas. `index.html` / `allwork.html` refresh karo - project aa gaya.

## info.json ke fields
| field | matlab |
|---|---|
| title | project ka naam |
| category | `Video Editing`, `Motion Graphics`, `3D Animation`, `Brand Film`, `Music Video`, `Color Grading` (filter buttons yahi hain) |
| subtitle | card ke neeche choti line |
| description | home page ke bade card ka text (khali chhod sakte ho) |
| tags | home page ke tags, jaise `["Premiere Pro","4K"]` |
| year | khali chhodo to nahi dikhega |
| featured | `true` = home page par sabse bada card |
| order | chhota number = pehle (featured ke baad) |
| link | video nahi hai to click par ye link khulega (YouTube etc.) |
| hide | `true` = website se chhupa do, folder rehne do |

Home page par pehle 3 projects dikhte hain (1 bada + 2 chhote), allwork par sab.

## Zaroori cheezein
- **Python 3** (python.org se install, "Add to PATH" tick karna)
- **ffmpeg** (video compress + auto thumbnail ke liye). Nahi hai to bhi chalega,
  bas video compress nahi hogi aur thumb.jpg khud daalna padega.
  Windows: `winget install ffmpeg`  |  Mac: `brew install ffmpeg`

## Kya kahan hai
```
index.html, allwork.html      pages
update.py                     magic script (folders scan -> data/projects-data.js)
assets/js/projects.js         cards banane wala code (demo cards wapas chahiye to SHOW_PLACEHOLDERS = true)
data/projects-data.js         AUTO-GENERATED, edit mat karna
projects/<naam>/              har project ka folder
   video.mp4  (original)      video-web.mp4 (auto, website yahi chalati hai)
   thumb.jpg  info.json
```
Website hosting par daalte waqt original `video.mp4` upload mat karo - sirf `video-web.mp4`, `thumb.jpg` kaafi hain.
