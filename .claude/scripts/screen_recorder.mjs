// Records the page of a Chrome started with --remote-debugging-port, through the DevTools screencast.
// Started and stopped by browser_recorder.py; not meant to be run by hand.
// Usage: node screen_recorder.mjs <port> <out-dir>
// Writes <out-dir>/frames/NNNNN.jpg while recording, <out-dir>/READY once the screencast runs, and
// <out-dir>/frames.json ([{file, t}], t in seconds) when it stops. It stops when <out-dir>/STOP appears,
// on SIGTERM/SIGINT, or when Chrome closes. Needs Node 22 or newer (built-in WebSocket).
import fs from "node:fs";
import path from "node:path";

const [port, out] = process.argv.slice(2);
if (!port || !out) { console.error("usage: node screen_recorder.mjs <port> <out-dir>"); process.exit(2); }
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
