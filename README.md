# Dragon's Lair, 1944–45

**A hypothetical campaign study from the Luftwaffe's own file.** On 16 April 1944 the Luftwaffe Operations Staff proposed to send eight Mistel, pilotless Ju 88 bombers steered by a fighter on their backs, against the British Home Fleet in Scapa Flow. In February 1945 the plan came back as Operation *Drachenhöhle* (Dragon's Lair) and was dropped within four days. The study follows the staff's own arithmetic, sets it beside the Home Fleet's war diary, and follows what the file did not count: the men aboard, the Churchill Barriers and the Italian prisoners of war who built them.

Read it as a dossier, or take the staff's seat and decide where the file decides; a model then runs the attack with the file's figures and named assumptions. A sequel to [Iron Hammer, 1945](https://iron-hammer-1945.netlify.app/).

## Sources

- **The file:** NARA, RG 242, microfilm T-321 (Records of Headquarters, German Air Force High Command), roll 10: war diary of the Luftwaffe Operations Staff, annex volume C, item 89 (study, technical annex, naval note and maps, 16 April 1944) and text volume, February 1945. Facsimile, full transcription and translation in `data/file.json`.
- **The interrogation:** CSDIC (WEA) Final Report 30 on Maj. Horst Hans Beeger, January 1946 (NARA, RG 498).
- **The other side:** war diary of the Commander-in-Chief, Home Fleet (ADM 199, transcription by Don Kindell); S. W. Roskill, *The War at Sea* (HMSO, 1954–61); Hansard; Johann Custodis, "Exploiting the Enemy in the Orkneys" (2011), summarised.

## Files

- `index.html`, `app.js`, `model.js`, `style.css`: the study; `legal.html`: legal notice and privacy.
- `data/`: chapters (`study.json`), the file (`file.json`), model figures and assumptions (`model.json`), plates, sources, map.
- `tools/`: scripts that build the facsimiles, plates, map and data from the sources (`make-facsimiles.py`, `fetch-plates.py`, `make-plates.py`, `make-map.py`, `build-file.py`, `build-study.py`).

Local: `python -m http.server` in this folder, then `http://localhost:8000/`. The model also runs in Node: `node -e "const DL=require('./model.js');DL.setData(require('./data/model.json'));console.log(DL.monteCarlo({base:'grove',count:'8',method:'day',recon:'recon',when:'june',drachen:'postpone'},1000,1))"`.

## Licences

Code MIT; transcriptions and translations CC0; editorial matter CC BY 4.0; plates as credited (public domain, and CC BY 2.0 / CC BY-SA 2.0 for three recent photographs). See [LICENSES.md](LICENSES.md).
