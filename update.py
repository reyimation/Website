#!/usr/bin/env python3
"""
Reyimation site updater.

projects/ ke andar har project ka apna folder hota hai. Is script ko chalao
(UPDATE-SITE.bat / update-site.command double-click) aur ye:
  1. har folder me video + thumbnail dhoondhta hai
  2. info.json nahi hai to bana deta hai
  3. thumbnail nahi hai to video se bana deta hai (ffmpeg chahiye)
  4. video ka light web version (video-web.mp4) bana deta hai (ffmpeg chahiye)
  5. data/projects-data.js likh deta hai -> website isi se cards banati hai
"""
import json, shutil, subprocess, sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
PROJECTS = ROOT / "projects"
OUT = ROOT / "data" / "projects-data.js"
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
FFMPEG = shutil.which("ffmpeg")


def run(cmd):
    return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)


def find_source_video(folder):
    vids = [p for p in sorted(folder.iterdir())
            if p.suffix.lower() in VIDEO_EXT and not p.stem.lower().endswith("-web")]
    for p in vids:
        if p.stem.lower() == "video":
            return p
    return vids[0] if vids else None


def find_thumb(folder):
    imgs = [p for p in sorted(folder.iterdir()) if p.suffix.lower() in IMAGE_EXT]
    for p in imgs:
        if p.stem.lower() == "thumb":
            return p
    return imgs[0] if imgs else None


def make_web_video(src, dst):
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return True
    if not FFMPEG:
        return False
    print(f"   video compress ho raha hai (thoda time lagega): {src.name}")
    r = run([FFMPEG, "-y", "-i", str(src),
             "-vf", "scale='min(1920,iw)':-2",
             "-c:v", "libx264", "-crf", "24", "-preset", "medium", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(dst)])
    if r.returncode != 0:
        print("   ! compress fail:", r.stderr[-300:])
        if dst.exists():
            dst.unlink()
        return False
    return True


def make_thumb(video, dst):
    if not FFMPEG:
        return False
    for t in ("5", "0"):  # 5 sec ka frame; video chhoti ho to pehla frame
        r = run([FFMPEG, "-y", "-ss", t, "-i", str(video), "-frames:v", "1",
                 "-vf", "scale='min(1280,iw)':-2", "-q:v", "3", str(dst)])
        if r.returncode == 0 and dst.exists():
            return True
    return False


def web(path):
    return "/".join(quote(part) for part in path.relative_to(ROOT).parts)


def load_info(folder):
    f = folder / "info.json"
    if not f.exists():
        info = {
            "title": folder.name.replace("-", " ").replace("_", " ").title(),
            "category": "Video Editing",
            "subtitle": "",
            "description": "",
            "tags": [],
            "year": str(date.today().year),
            "featured": False,
            "order": 10,
        }
        f.write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
        print("   info.json bana diya - title/category wagairah edit kar lena")
        return info
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"   ! info.json me galti ({e}) - ye project skip kiya")
        return None


def main():
    PROJECTS.mkdir(exist_ok=True)
    if not FFMPEG:
        print("NOTE: ffmpeg nahi mila. Video compress / auto-thumbnail nahi hoga.\n"
              "      (Thumbnail khud thumb.jpg naam se folder me daal do.)\n")
    items = []
    for folder in sorted(PROJECTS.iterdir()):
        if not folder.is_dir() or folder.name.startswith(("_", ".")):
            continue
        print(f"-> {folder.name}")
        info = load_info(folder)
        if info is None or info.get("hide"):
            continue

        src = find_source_video(folder)
        web_video = folder / "video-web.mp4"
        video = None
        if src:
            video = web_video if make_web_video(src, web_video) else src
        elif web_video.exists():
            video = web_video

        thumb = find_thumb(folder)
        if thumb is None and video is not None:
            t = folder / "thumb.jpg"
            thumb = t if make_thumb(video, t) else None
        if video is None and thumb is None:
            print("   ! na video mili na thumbnail - skip")
            continue

        items.append({
            "slug": folder.name,
            "title": info.get("title", folder.name),
            "category": info.get("category", "Video Editing"),
            "subtitle": info.get("subtitle", ""),
            "description": info.get("description", ""),
            "tags": info.get("tags", []),
            "year": str(info.get("year", "") or ""),
            "featured": bool(info.get("featured", False)),
            "order": info.get("order", 10),
            "link": info.get("link", ""),
            "video": web(video) if video else "",
            "thumb": web(thumb) if thumb else "",
        })

    items.sort(key=lambda p: (not p["featured"], p["order"], p["title"].lower()))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("/* AUTO-GENERATED by update.py - isse edit mat karo */\n"
                   "window.PROJECTS = " + json.dumps(items, indent=2, ensure_ascii=False) + ";\n",
                   encoding="utf-8")
    print(f"\nDone. {len(items)} project(s) website par. index.html / allwork.html refresh karo.")


if __name__ == "__main__":
    sys.exit(main())
