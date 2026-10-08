"""Screenshots for itch.io (1280 x 800), with Chrome in headless mode.

Writes a temporary _shot.html next to index.html that sets a fixed state (seed 9001; Grove, eight Mistel, by day,
with reconnaissance, late May 1944, Dragon's Lair flown) before the study loads, then deletes it.
Needs the local server on port 8963 (preview "dragons-lair", or python -m http.server 8963).
Run from the repository root:  python itch/make-shots.py
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "http://localhost:8963/_shot.html"

SHOTS = [
    ("screenshot-1-start.png", "read", ""),
    ("screenshot-2-chapter.png", "read", "#/ch/2"),
    ("screenshot-3-decision.png", "play", "#/ch/5"),
    ("screenshot-4-file.png", "read", "#/file/b3"),
    ("screenshot-5-strike.png", "play", "#/strike"),
    ("screenshot-6-accounting.png", "play", "#/result"),
    ("screenshot-7-fleet.png", "read", "#/ch/7"),
    ("screenshot-8-prisoners.png", "read", "#/ch/9"),
]

DRIVER = """
<script>
(function () {
  var m = new URLSearchParams(location.search).get("m");
  var st = { mode: m, seed: 9001, reached: 10,
    choices: m === "play" ? { base: "grove", count: "8", method: "day", recon: "recon", when: "may", drachen: "attack" } : {} };
  try { localStorage.setItem("dragonslair_state", JSON.stringify(st)); } catch (e) {}
})();
</script>
"""


def main():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    shot = ROOT / "_shot.html"
    shot.write_text(html.replace("<head>", "<head>" + DRIVER, 1), encoding="utf-8")
    try:
        for name, mode, hashpart in SHOTS:
            out = ROOT / "itch" / name
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1280,800",
                            "--virtual-time-budget=8000", f"--screenshot={out}", f"{BASE}?m={mode}{hashpart}"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(name, out.stat().st_size // 1024, "KB")
    finally:
        shot.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
