#!/usr/bin/env python3
"""Build per-test evidence from one result JSON.

Usage: python3 test_evidence.py <RUN>/results/<TC ID>.json

Expects raw step screenshots in <RUN>/<TC ID>/ named stepNN.png or stepNN.jpg
(NN = two-digit step number). Produces in the same folder:
  stepNN.png            every step as PNG (JPGs are converted and removed)
  stepNN_FAIL.png       failed steps, with red border and red banner (step text + reason)
  <TC ID>_replay.gif    all steps in order, 1.5 s per frame, step number + PASSED/FAILED on each
  <TC ID>_replay.mp4    the same frames as a video that can be paused and scrubbed (needs ffmpeg)
  <TC ID>_steps.pdf     one page per step: screenshot, step text, expected, answer, saw, result
and rewrites each step's "screenshot" in the JSON to the final relative path (<TC ID>/stepNN[_FAIL].png).
Needs Pillow: pip3 install --user pillow
The MP4 needs ffmpeg: either on PATH or from pip3 install --user imageio-ffmpeg. Without it the MP4 is
skipped with a note, and the GIF and PDF are still made.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap

from PIL import Image, ImageDraw, ImageFont

FONT_FILES = ["/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"]
RED = (220, 38, 38)
GREEN = (22, 163, 74)
GREY = (100, 116, 139)
FRAME_MS = 1500
GIF_WIDTH = 960


def font(size):
    for f in FONT_FILES:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default(size=size)


def wrap(draw, text, fnt, width_px):
    """Wrap text to fit width_px using the font's real width."""
    avg = max(draw.textlength("abcdefghij", font=fnt) / 10, 1)
    lines = []
    for para in str(text).split("\n"):
        lines += textwrap.wrap(para, max(int(width_px / avg), 10)) or [""]
    return lines


def step_status(step):
    return "PASSED" if step.get("ok", True) else "FAILED"


def find_raw(folder, n):
    for name in (f"step{n:02d}.png", f"step{n:02d}.jpg", f"step{n:02d}.jpeg",
                 f"step{n:02d}_FAIL.png"):
        p = os.path.join(folder, name)
        if os.path.exists(p):
            return p
    return None


def mark_failed(img, step, reason):
    """Red banner (step text + reason) added above the screenshot, and a red border around it all.
    The banner sits above the screenshot so it never hides the page content."""
    shot = img.convert("RGB")
    w, h = shot.size
    border = max(8, w // 120)
    f_big, f_small = font(max(18, w // 55)), font(max(15, w // 70))
    pad = border + 12
    probe = ImageDraw.Draw(shot)
    wrapped = []
    for text, fnt in ((f"FAILED - Step {step['n']}: {step.get('text', '')}", f_big),
                      (f"Reason: {reason}", f_small)):
        for ln in wrap(probe, text, fnt, w - 2 * pad):
            wrapped.append((ln, fnt))
    line_h = [fnt.getbbox("Ag")[3] + 8 for _, fnt in wrapped]
    banner_h = border + sum(line_h) + 24
    out = Image.new("RGB", (w, h + banner_h), RED)
    out.paste(shot, (0, banner_h))
    d = ImageDraw.Draw(out)
    y = border + 12
    for (ln, fnt), lh in zip(wrapped, line_h):
        d.text((pad, y), ln, fill="white", font=fnt)
        y += lh
    for i in range(border):
        d.rectangle([i, i, w - 1 - i, out.height - 1 - i], outline=RED)
    return out


def gif_frame(img, tc_id, step, total):
    img = img.convert("RGB")
    scale = GIF_WIDTH / img.width
    img = img.resize((GIF_WIDTH, int(img.height * scale)))
    status = step_status(step)
    colour = GREEN if status == "PASSED" else RED
    bar_f, txt_f = font(24), font(17)
    d0 = ImageDraw.Draw(img)
    text_lines = wrap(d0, step.get("text", ""), txt_f, GIF_WIDTH - 24)[:2]
    bar_h = 40 + 24 * len(text_lines) + 8
    frame = Image.new("RGB", (GIF_WIDTH, img.height + bar_h), "white")
    frame.paste(img, (0, bar_h))
    d = ImageDraw.Draw(frame)
    d.rectangle([0, 0, GIF_WIDTH, bar_h], fill=colour)
    d.text((12, 8), f"{tc_id}   Step {step['n']}/{total}   {status}", fill="white", font=bar_f)
    y = 42
    for ln in text_lines:
        d.text((12, y), ln, fill="white", font=txt_f)
        y += 24
    if status == "FAILED":
        for i in range(6):
            d.rectangle([i, i, GIF_WIDTH - 1 - i, frame.height - 1 - i], outline=RED)
    return frame


def ffmpeg_exe():
    """ffmpeg on PATH, else the binary bundled with imageio-ffmpeg, else None."""
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def write_mp4(frames, path):
    """Write the replay frames as an H.264 MP4, FRAME_MS per frame. Returns None or an error note.
    Frames can differ in height, so each is padded with white at the bottom to the tallest one
    (H.264 also needs even width and height)."""
    exe = ffmpeg_exe()
    if not exe:
        return "ffmpeg not found (pip3 install --user imageio-ffmpeg)"
    w = max(f.width for f in frames)
    h = max(f.height for f in frames)
    w, h = w + w % 2, h + h % 2
    with tempfile.TemporaryDirectory() as tmp:
        for i, fr in enumerate(frames):
            canvas = Image.new("RGB", (w, h), "white")
            canvas.paste(fr, (0, 0))
            canvas.save(os.path.join(tmp, f"f{i:04d}.png"))
        cmd = [exe, "-y", "-loglevel", "error", "-framerate", f"1000/{FRAME_MS}",
               "-i", os.path.join(tmp, "f%04d.png"), "-c:v", "libx264", "-tune", "stillimage",
               "-pix_fmt", "yuv420p", "-r", "10", "-g", str(FRAME_MS // 100), "-movflags", "+faststart", path]
        res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        if os.path.exists(path):
            os.remove(path)
        return "ffmpeg failed: " + (res.stderr.strip().splitlines() or ["unknown error"])[-1]
    return None


def pdf_page(img, tc, step, total):
    page_w = 1654  # A4 landscape-ish at ~150 dpi
    margin = 50
    img = img.convert("RGB")
    shot_w = page_w - 2 * margin
    max_shot_h = 900
    scale = min(shot_w / img.width, max_shot_h / img.height)  # shrink to fit, never crop
    shot = img.resize((int(img.width * scale), int(img.height * scale)))
    h_f, b_f = font(30), font(22)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    status = step_status(step)
    rows = [("Step", step.get("text", "")),
            ("Expected", step.get("expected") or "-"),
            ("Answer", step.get("answer") or "-"),
            ("What I saw", step.get("saw") or "-"),
            ("Result", status)]
    body = []
    for label, val in rows:
        for i, ln in enumerate(wrap(probe, val, b_f, shot_w - 200)):
            body.append((label if i == 0 else "", ln, label == "Result"))
    text_h = 60 + 32 * len(body) + 30
    page = Image.new("RGB", (page_w, margin + text_h + shot.height + margin), "white")
    d = ImageDraw.Draw(page)
    colour = GREEN if status == "PASSED" else RED
    d.text((margin, margin), f"{tc['id']} - {tc.get('title', '')}   (step {step['n']} of {total})",
           fill="black", font=h_f)
    y = margin + 50
    for label, ln, is_result in body:
        d.text((margin, y), label, fill=GREY, font=b_f)
        d.text((margin + 200, y), ln, fill=colour if is_result else "black", font=b_f)
        y += 32
    y += 20
    page.paste(shot, (margin, y))
    d.rectangle([margin - 2, y - 2, margin + shot.width + 1, y + shot.height + 1],
                outline=colour, width=4 if status == "FAILED" else 1)
    return page


def main(json_path):
    with open(json_path, encoding="utf-8") as f:
        tc = json.load(f)
    run_dir = os.path.dirname(os.path.dirname(os.path.abspath(json_path)))
    tc_id = tc["id"]
    folder = os.path.join(run_dir, tc_id)
    os.makedirs(folder, exist_ok=True)
    steps = sorted(tc.get("steps", []), key=lambda s: s["n"])
    total = len(steps)
    frames, pages, missing = [], [], []

    for step in steps:
        n = step["n"]
        raw = find_raw(folder, n)
        if not raw:
            missing.append(n)
            step["screenshot"] = None
            continue
        img = Image.open(raw).convert("RGB")
        failed = step_status(step) == "FAILED"
        final = os.path.join(folder, f"step{n:02d}{'_FAIL' if failed else ''}.png")
        if failed and not raw.endswith("_FAIL.png"):
            reason = step.get("saw") or tc.get("reason") or "Answer did not match the expected answer"
            img = mark_failed(img, step, reason)
        img.save(final)
        if os.path.abspath(raw) != os.path.abspath(final):
            os.remove(raw)
        step["screenshot"] = f"{tc_id}/{os.path.basename(final)}"
        frames.append(gif_frame(img, tc_id, step, total))
        pages.append(pdf_page(img, tc, step, total))

    if frames:
        pal = [fr.convert("P", palette=Image.ADAPTIVE, colors=255) for fr in frames]
        pal[0].save(os.path.join(folder, f"{tc_id}_replay.gif"), save_all=True,
                    append_images=pal[1:], duration=FRAME_MS, loop=0, optimize=True)
        pages[0].save(os.path.join(folder, f"{tc_id}_steps.pdf"), save_all=True,
                      append_images=pages[1:], resolution=150)
        tc["replay_gif"] = f"{tc_id}/{tc_id}_replay.gif"
        tc["steps_pdf"] = f"{tc_id}/{tc_id}_steps.pdf"
        mp4_note = write_mp4(frames, os.path.join(folder, f"{tc_id}_replay.mp4"))
        if mp4_note:
            tc.pop("replay_mp4", None)
        else:
            tc["replay_mp4"] = f"{tc_id}/{tc_id}_replay.mp4"
    tc["evidence_folder"] = f"{tc_id}/"
    tc["steps"] = steps
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tc, f, ensure_ascii=False, indent=2)
    made = ("gif+mp4+pdf" if tc.get("replay_mp4") else "gif+pdf") + " written" if frames else "gif+pdf skipped"
    print(f"{tc_id}: {len(frames)} frames, {made}"
          + (f", mp4 skipped: {mp4_note}" if frames and mp4_note else "")
          + (f", missing screenshots for steps {missing}" if missing else ""))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
