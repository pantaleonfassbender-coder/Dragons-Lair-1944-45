"""Download the plates from Wikimedia Commons into tools/plates_src/ and record their metadata.
Run from the repository root:  python tools/fetch-plates.py"""
import json, urllib.request, urllib.parse
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "plates_src"
UA = {"User-Agent": "dragons-lair-study/1.0 (pantaleonfassbender@gmail.com)"}
FILES = {
    "lambholm1": "File:Target Dossier for Lamb-Holm, Orkney, Scotland - DPLA - 38b945587612b0a58b8761354d0c156c (page 1).jpg",
    "lambholm2": "File:Target Dossier for Lamb-Holm, Orkney, Scotland - DPLA - 38b945587612b0a58b8761354d0c156c (page 2).jpg",
    "lambholm3": "File:Target Dossier for Lamb-Holm, Orkney, Scotland - DPLA - 38b945587612b0a58b8761354d0c156c (page 3).jpg",
    "scapasw1": "File:Target Dossier for Scapa Flow SW, Orkney, Scotland - DPLA - b8d8aa3675753153e8eed763560d7794 (page 1).jpg",
    "scapasw2": "File:Target Dossier for Scapa Flow SW, Orkney, Scotland - DPLA - b8d8aa3675753153e8eed763560d7794 (page 2).jpg",
    "scapasw3": "File:Target Dossier for Scapa Flow SW, Orkney, Scotland - DPLA - b8d8aa3675753153e8eed763560d7794 (page 3).jpg",
    "chart35": "File:Admiralty Chart No 35 Scapa Flow Northern Part, Published 1944.jpg",
    "boom": "File:Royal Navy Vessels Maintain the Boom Defence at Scapa Flow, Scotland, May 1943 A16572.jpg",
    "wasp": "File:USS Wichita (CA-45) and USS Wasp (CV-7) in Scapa Flow in April 1942.jpg",
    "royaloak": "File:HMS Royal Oak (08).jpg",
    "chapel": "File:The Italian Chapel, Orkney (Exterior) (2926632589).jpg",
    "barrier": "File:Churchill Barrier 4 South Ronaldsay.jpg",
    "blockship": "File:Blockship at Churchill Barrier No 4 - geograph.org.uk - 1331240.jpg",
}
meta = {}
SRC.mkdir(parents=True, exist_ok=True)
for key, title in FILES.items():
    q = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "format": "json"})
    d = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA)))
    page = next(iter(d["query"]["pages"].values()))
    ii = page["imageinfo"][0]; m = ii["extmetadata"]
    get = lambda k: m.get(k, {}).get("value", "")
    meta[key] = {"title": title, "url": ii["descriptionurl"], "file": ii["url"], "w": ii["width"], "h": ii["height"],
                 "license": get("LicenseShortName"), "artist": get("Artist"), "credit": get("Credit"), "date": get("DateTimeOriginal"), "desc": get("ImageDescription")[:500]}
    out = SRC / (key + "." + ii["url"].split("?")[0].rsplit(".", 1)[1].lower())
    if not out.exists():
        out.write_bytes(urllib.request.urlopen(urllib.request.Request(ii["url"], headers=UA)).read())
    print(key, ii["width"], ii["height"], meta[key]["license"])
(SRC / "meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
