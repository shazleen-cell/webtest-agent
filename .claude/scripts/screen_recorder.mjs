// Records the page of a Chrome started with --remote-debugging-port, through the DevTools screencast.
// Started and stopped by browser_recorder.py; not meant to be run by hand.
// Usage: node screen_recorder.mjs <port> <out-dir> [--phone | --tablet | --size=WxH]
// --phone: also turns on iPhone 14 emulation (390x844, DPR 3, mobile, touch, iPhone user agent) through
// DevTools; --tablet: iPad emulation (768x1024, DPR 2, mobile, touch, iPad user agent); --size=WxH: a desktop
// page area of W x H pixels. The emulation lasts as long as this connection, so it stays on for the whole test
// and ends with the recording.
// Writes <out-dir>/frames/NNNNN.jpg while recording, <out-dir>/READY once the screencast runs, and
// <out-dir>/frames.json ([{file, t}], t in seconds) when it stops. It stops when <out-dir>/STOP appears,
// on SIGTERM/SIGINT, or when Chrome closes. Needs Node 22 or newer (built-in WebSocket).
import fs from "node:fs";
import path from "node:path";

const [port, out, ...flags] = process.argv.slice(2);
if (!port || !out) { console.error("usage: node screen_recorder.mjs <port> <out-dir> [--phone | --tablet | --size=WxH]"); process.exit(2); }
const DEVICES = {
  "--phone": { width: 390, height: 844, dpr: 3, platform: "iPhone",
    ua: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" },
  "--tablet": { width: 768, height: 1024, dpr: 2, platform: "iPad",
    ua: "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" },
};
const DEVICE = DEVICES[flags.find((f) => DEVICES[f])];
// --size=WxH: a desktop page area of W x H (no mobile mode, touch or user agent change), for tests that set a
// window size. The recorder's Chrome window cannot be resized once wdio-mcp is attached, so the page area is set
// through DevTools instead, like the phone view.
const SIZE = (() => {
  const f = flags.find((x) => x.startsWith("--size="));
  if (!f) return null;
  const m = /^--size=(\d{3,4})x(\d{3,4})$/.exec(f);
  if (!m) { console.error(`bad ${f}: use --size=WIDTHxHEIGHT, for example --size=1280x800`); process.exit(2); }
  return { width: Number(m[1]), height: Number(m[2]) };
})();
if (DEVICE && SIZE) { console.error("use --phone, --tablet or --size, not two of them"); process.exit(2); }
if (typeof WebSocket !== "function") { console.error("Node 22 or newer is needed (no built-in WebSocket)"); process.exit(2); }
fs.mkdirSync(path.join(out, "frames"), { recursive: true });

const frames = [];
let ws, id = 0, done = false;

async function pageTarget() {
  for (let i = 0; i < 75; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      const page = list.find((t) => t.type === "page");
      if (page) return page;
    } catch {}
    await new Promise((r) => setTimeout(r, 200));
  }
  throw new Error(`no page in Chrome on port ${port}`);
}

const send = (method, params = {}) => ws.send(JSON.stringify({ id: ++id, method, params }));

function finish(why) {
  if (done) return;
  done = true;
  try { send("Page.stopScreencast"); } catch {}
  fs.writeFileSync(path.join(out, "frames.json"), JSON.stringify(frames));
  console.log(`recorder stopped (${why}): ${frames.length} frames`);
  setTimeout(() => process.exit(0), 200);
}

const target = await pageTarget();
ws = new WebSocket(target.webSocketDebuggerUrl);
ws.onopen = () => {
  send("Page.enable");
  if (DEVICE) {
    // No setEmitTouchEventsForMouse: it turns WebDriver's mouse clicks into touches and the clicks then hang.
    const { width, height, dpr, ua, platform } = DEVICE;
    send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: dpr, mobile: true,
      screenWidth: width, screenHeight: height, screenOrientation: { type: "portraitPrimary", angle: 0 } });
    send("Emulation.setUserAgentOverride", { userAgent: ua, platform });
    send("Emulation.setTouchEmulationEnabled", { enabled: true, maxTouchPoints: 5 });
  }
  if (SIZE) {
    // deviceScaleFactor 0 keeps the screen's own pixel ratio; mobile false keeps the desktop layout rules.
    send("Emulation.setDeviceMetricsOverride", { width: SIZE.width, height: SIZE.height, deviceScaleFactor: 0,
      mobile: false, screenWidth: SIZE.width, screenHeight: SIZE.height });
  }
  send("Page.startScreencast", { format: "jpeg", quality: 80, maxWidth: 1440, maxHeight: 900, everyNthFrame: 1 });
  fs.writeFileSync(path.join(out, "READY"), "");
};
ws.onmessage = (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.method !== "Page.screencastFrame" || done) return;
  const { data, metadata, sessionId } = msg.params;
  const file = `${String(frames.length).padStart(5, "0")}.jpg`;
  fs.writeFileSync(path.join(out, "frames", file), Buffer.from(data, "base64"));
  frames.push({ file, t: metadata.timestamp });
  send("Page.screencastFrameAck", { sessionId });
};
ws.onclose = () => finish("Chrome closed");
ws.onerror = () => finish("connection error");
process.on("SIGINT", () => finish("SIGINT"));
process.on("SIGTERM", () => finish("SIGTERM"));
setInterval(() => { if (fs.existsSync(path.join(out, "STOP"))) finish("stop requested"); }, 200);
