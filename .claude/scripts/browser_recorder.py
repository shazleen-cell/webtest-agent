#!/usr/bin/env python3
"""Start Chrome with a screen recorder for one test, and stop it again.

Usage:
  browser_recorder.py start <RUN> <TC ID>   opens Chrome (1440x900, new empty profile) with a debugging port and
                                           starts the recorder; prints "port: <N>". The website-tester then
                                           attaches wdio-mcp to that port (start_session with attach: true).
  browser_recorder.py stop <RUN> <TC ID>    stops the recorder, writes <RUN>/<TC ID>/<TC ID>_screen.mp4 and
                                           closes Chrome. Run it after close_session.

Exit code 2 from start means recording is not available here (no Chrome, Node older than 22, or Chrome did not
start); the reason is printed, nothing is left running, and the test runs with a normal wdio-mcp session instead.
The video shows the page as it changed, with pauses longer than MAX_PAUSE seconds shortened to MAX_PAUSE, so the
time the agent spends thinking between steps does not make it long. It ends CUT_AFTER seconds after the last step
screenshot (stepNN file) was saved, so closing the session is not in it. It records one tab only.
Needs ffmpeg (on PATH, or pip3 install --user imageio-ffmpeg) to build the video.
"""
import json
import re
import os
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_evidence import ffmpeg_exe  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RECORDER = os.path.join(HERE, "screen_recorder.mjs")
MAX_PAUSE = 1.0     # seconds; longer pauses between frames are shortened to this
LAST_FRAME = 1.5    # seconds the last frame stays on screen
CUT_AFTER = 0.0     # seconds of recording kept after the last step screenshot was saved (it is saved after it is taken)
CHROME_PATHS = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium"]


def paths(run, tc):
    work = os.path.join(run, tc, ".recorder")
    return work, os.path.join(work, "state.json"), os.path.join(run, tc, f"{tc}_screen.mp4")


def find_chrome():
    if os.environ.get("CHROME_PATH") and os.path.exists(os.environ["CHROME_PATH"]):
        return os.environ["CHROME_PATH"]
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if shutil.which(name):
            return shutil.which(name)
    return None


def node_ok():
    node = shutil.which("node")
    if not node:
        return None
    r = subprocess.run([node, "-e", "process.exit(typeof WebSocket === 'function' ? 0 : 1)"], capture_output=True)
    return node if r.returncode == 0 else None


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for(check, seconds):
    end = time.time() + seconds
    while time.time() < end:
        if check():
            return True
        time.sleep(0.2)
    return False


def chrome_up(port):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1).read()
        return True
    except Exception:
        return False


def kill(pid, wait=5):
    if not pid:
        return
    try:
        os.killpg(pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return
    if not wait_for(lambda: not alive(pid), wait):
        try:
            os.killpg(pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    # A finished child stays as a zombie until it is reaped.
    try:
        done, _ = os.waitpid(pid, os.WNOHANG)
        return done == 0
    except ChildProcessError:
        return True


def unavailable(reason):
    print(f"recording not available: {reason}")
    sys.exit(2)


def start(run, tc):
    work, state_path, _ = paths(run, tc)
    if os.path.exists(state_path):
        stop(run, tc, build=False)  # a leftover from an earlier attempt
    chrome = find_chrome()
    if not chrome:
        unavailable("Google Chrome not found (set CHROME_PATH)")
    node = node_ok()
    if not node:
        unavailable("Node 22 or newer not found (the recorder needs its built-in WebSocket)")
    os.makedirs(work, exist_ok=True)
    profile = tempfile.mkdtemp(prefix="webtest-chrome-")
    port = free_port()
    log = open(os.path.join(work, "chrome.log"), "w")
    cp = subprocess.Popen([chrome, f"--remote-debugging-port={port}", f"--user-data-dir={profile}",
                           "--no-first-run", "--no-default-browser-check", "--disable-search-engine-choice-screen",
                           "--window-size=1440,900", "about:blank"],
                          stdout=log, stderr=log, start_new_session=True)
    state = {"port": port, "chrome_pid": cp.pid, "profile": profile, "recorder_pid": None}
    json.dump(state, open(state_path, "w"))
    if not wait_for(lambda: chrome_up(port), 20):
        stop(run, tc, build=False)
        unavailable("Chrome did not open its debugging port")
    rlog = open(os.path.join(work, "recorder.log"), "w")
    rp = subprocess.Popen([node, RECORDER, str(port), work], stdout=rlog, stderr=rlog, start_new_session=True)
    state["recorder_pid"] = rp.pid
    json.dump(state, open(state_path, "w"))
    if not wait_for(lambda: os.path.exists(os.path.join(work, "READY")), 15):
        stop(run, tc, build=False)
        unavailable("the recorder did not start (see .recorder/recorder.log)")
    print(f"port: {port}")


def step_times(folder):
    """{step number: when its screenshot file was saved}. The website-tester copies each stepNN file right after
    taking the screenshot, so this is when the step finished. Read before test_evidence.py rewrites the files."""
    times = {}
    for f in os.listdir(folder):
        m = re.match(r"step(\d+)(_FAIL)?\.(png|jpe?g)$", f, re.I)
        if m:
            times[int(m.group(1))] = os.path.getmtime(os.path.join(folder, f))
    return times


def last_step_time(folder):
    """When the last step screenshot was saved (file time), or None. Frames after it come from closing the
    session (for example the page going back from phone to desktop size) and are not part of the test."""
    times = step_times(folder)
    return max(times.values()) if times else None


def video_time(frames, starts, durations, t):
    """Real time t -> seconds into the video (which has blank frames dropped and long pauses shortened)."""
    i = -1
    for k, f in enumerate(frames):
        if f["t"] <= t:
            i = k
        else:
            break
    if i < 0:
        return 0.0
    return starts[i] + min(max(t - frames[i]["t"], 0.0), durations[i])


def build_video(work, out):
    """Frames -> MP4. Returns a short note."""
    fj = os.path.join(work, "frames.json")
    frames = json.load(open(fj)) if os.path.exists(fj) else []
    end = last_step_time(os.path.dirname(work))
    if end is not None:
        kept = [f for f in frames if f["t"] <= end + CUT_AFTER]
        frames = kept or frames[:1]
    if not frames:
        return "no frames recorded"
    exe = ffmpeg_exe()
    if not exe:
        return "ffmpeg not found (pip3 install --user imageio-ffmpeg)"
    from PIL import Image, ImageStat
    # Drop the empty page shown before the test opens its Start URL (one flat colour).
    while len(frames) > 1:
        with Image.open(os.path.join(work, "frames", frames[0]["file"])) as im:
            if max(ImageStat.Stat(im.convert("L")).stddev) > 2:
                break
        frames = frames[1:]
    w = h = 0
    for f in frames:
        with Image.open(os.path.join(work, "frames", f["file"])) as im:
            w, h = max(w, im.width), max(h, im.height)
    w, h = w + w % 2, h + h % 2
    total = 0.0
    starts, durations = [], []
    lst = os.path.join(work, "frames.txt")
    with open(lst, "w") as o:
        for a, b in zip(frames, frames[1:] + [None]):
            d = min(b["t"] - a["t"], MAX_PAUSE) if b else LAST_FRAME
            d = max(d, 0.04)
            starts.append(total)
            durations.append(d)
            total += d
            o.write(f"file 'frames/{a['file']}'\nduration {d:.3f}\n")
        o.write(f"file 'frames/{frames[-1]['file']}'\n")  # the concat format needs the last file twice
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
          f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=white,format=yuv420p")
    r = subprocess.run([exe, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf", vf,
                        "-c:v", "libx264", "-crf", "23", "-r", "25", "-movflags", "+faststart", out],
                       capture_output=True, text=True, cwd=work)
    if r.returncode != 0:
        if os.path.exists(out):
            os.remove(out)
        return "ffmpeg failed: " + (r.stderr.strip().splitlines() or ["unknown error"])[-1]
    # Where each step is in the video: it starts where the previous step's screenshot was saved, and ends at
    # its own. The report uses this for its "Watch step N" buttons.
    ends = {n: round(video_time(frames, starts, durations, t), 2)
            for n, t in sorted(step_times(os.path.dirname(work)).items())}
    steps, prev = {}, 0.0
    for n in sorted(ends):
        steps[str(n)] = {"start": min(prev, ends[n]), "end": ends[n]}  # a screenshot taken late can be out of order
        prev = ends[n]
    with open(os.path.splitext(out)[0] + ".json", "w") as f:
        json.dump({"duration": round(total, 2), "steps": steps}, f, indent=2)
    return f"{len(frames)} frames, {total:.1f} s"


def stop(run, tc, build=True):
    work, state_path, out = paths(run, tc)
    if not os.path.exists(state_path):
        print("no recording to stop")
        return
    state = json.load(open(state_path))
    rpid = state.get("recorder_pid")
    if rpid:
        open(os.path.join(work, "STOP"), "w").close()
        if not wait_for(lambda: os.path.exists(os.path.join(work, "frames.json")), 10):
            kill(rpid)
        wait_for(lambda: not alive(rpid), 3)
    note = build_video(work, out) if build else None
    kill(state.get("chrome_pid"))
    shutil.rmtree(state.get("profile") or "", ignore_errors=True)
    shutil.rmtree(work, ignore_errors=True)
    if build:
        print(f"screen video: {out} ({note})" if os.path.exists(out) else f"screen video skipped: {note}")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ("start", "stop"):
        sys.exit(__doc__)
    cmd, run_dir, tc_id = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3]
    start(run_dir, tc_id) if cmd == "start" else stop(run_dir, tc_id)
