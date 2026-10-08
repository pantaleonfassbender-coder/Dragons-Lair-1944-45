/* Dragon's Lair, 1944–45 — a hypothetical campaign study from the Luftwaffe's own file.
   Two ways through the same chapters: read the dossier, or take the staff's seat and decide. */
"use strict";

const D = {};
// Set when the itch.io page exists; the itch build sets window.DL_ITCH instead.
const ITCH_URL = "https://leofassb.itch.io/dragons-lair-194445";
function supportBox() {
  if (window.DL_ITCH) return `<div class="support"><b>This study is free.</b> It took weeks of work in the archives. If you found it useful, please support it with a donation: use the <b>Support</b> / donate button on this itch.io page. Every contribution helps to open the next file.</div>`;
  if (ITCH_URL) return `<div class="support"><b>This study is free.</b> If you found it useful, you can support the work with a donation on its <a href="${ITCH_URL}" target="_blank" rel="noopener">itch.io page</a>.</div>`;
  return "";
}
const KEY = "dragonslair_state";
let S = { mode: null, choices: {}, seed: 1, reached: 1 };

const $ = s => document.querySelector(s);
const view = $("#view");
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const fmt = n => Math.round(n).toLocaleString("en");
const pct = x => Math.round(x * 100) + " %";
const NCH = () => D.study.chapters.length;

function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* storage blocked */ } }
function load() { try { const s = JSON.parse(localStorage.getItem(KEY)); if (s && "choices" in s) S = s; } catch (e) { /* none */ } }

async function boot() {
  const get = f => fetch(f, { cache: "no-cache" }).then(r => r.json());
  [D.study, D.file, D.model, D.plates, D.sources, D.map] = await Promise.all(
    ["data/study.json", "data/file.json", "data/model.json", "data/plates.json", "data/sources.json", "data/map.json"].map(get));
  DL.setData(D.model);
  load();
  window.addEventListener("hashchange", route);
  route();
}

function route() {
  const parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  const [page, arg] = parts;
  document.querySelectorAll("nav a").forEach(a => {
    const t = a.getAttribute("href").replace(/^#\/?/, "").split("/")[0];
    a.classList.toggle("on", t === (page === "strike" || page === "result" ? "ch" : page));
  });
  modebar();
  window.scrollTo(0, 0);
  const pages = { "": start, ch: chapter, strike, result, file, data, plates, reflection, sources };
  (pages[page || ""] || start)(arg);
}

function modebar() {
  const m = S.mode === "play" ? `You are in the staff's seat. <a href="#/">Change</a>`
    : S.mode === "read" ? `You are reading the study. <a href="#/">Take the staff's seat instead</a>` : "";
  $("#modebar").innerHTML = m;
}

/* ------------------------------------------------------------ start */
function start() {
  view.innerHTML = `
  <div class="hero">
    <div>
      <span class="tag">April 1944 – February 1945 · Luftwaffe operations staff · KG 200</span>
      <h1>The Home Fleet at Scapa Flow, from the file that planned to sink it</h1>
      <p class="lede">On 16 April 1944 the Luftwaffe's operations staff proposed to send eight Mistel, pilotless Ju 88 bombers steered by a fighter on their backs, against the British fleet in Scapa Flow. Ten months later the plan came back as Operation Dragon's Lair, and was dropped within four days. The study of 1944 and the war-diary entries of 1945 survive in the captured German records of the US National Archives.</p>
      <p class="readable">This is a hypothetical campaign study built on those papers, a sequel to <a href="https://iron-hammer-1945.netlify.app/" target="_blank" rel="noopener">Iron Hammer, 1945</a>. It follows the staff's own arithmetic, sets it beside the Home Fleet's war diary, which records where every ship lay on every day, and follows what the file did not count: the men aboard, the barriers built after the Royal Oak, and the Italian prisoners who built them. You can read it as a dossier, or take the staff's seat and decide where the file decides. A model then runs the attack with the file's figures and named assumptions.</p>
      <div class="modes">
        <div class="mode"><h3>Read the study</h3><p class="fine">Ten chapters with the file in facsimile and translation, the war diaries of both sides and the other side of the Flow. At each decision point you see what the staff proposed, and the study computes the file's own plan at the end.</p><button class="primary" data-mode="read">Read</button></div>
        <div class="mode play"><h3>Take the staff's seat</h3><p class="fine">The same chapters, but you decide: the airfield, how many, how to come in, whether to photograph the anchorage first, when to strike, and in February 1945 whether to fly Dragon's Lair. The study runs your plan against the ships that were actually there.</p><button class="primary" data-mode="play">Decide</button></div>
      </div>
      ${supportBox()}
      <p class="fine">The study shows the planning of an attack from the side of those who planned it. It does not adopt their view: chapters 7 to 9 and the reflection follow what the file does not count. No swastika is shown; where one appears on a document, it is masked.</p>
    </div>
    <figure class="facs"><img src="assets/file/b3-remains.jpg" alt="Facsimile: 'bleibt Scapa Flow'">
      <figcaption>16 April 1944: "… bleibt Scapa Flow", remains Scapa Flow. <a href="#/file/b3">The page →</a></figcaption></figure>
  </div>`;
  view.querySelectorAll("[data-mode]").forEach(b => b.onclick = () => {
    const mode = b.dataset.mode;
    if (mode !== S.mode || mode === "play") { S.choices = {}; S.seed = Math.floor(Math.random() * 1e9); S.reached = 1; }
    S.mode = mode; save(); location.hash = "#/ch/1";
  });
}

/* ------------------------------------------------------------ chapters */
const strikeOn = () => S.mode === "play" && S.choices.drachen && (S.choices.when !== "hold" || S.choices.drachen === "attack");

function progress(cur) {
  const chs = D.study.chapters;
  const items = chs.map(c => `<a href="#/ch/${c.n}" class="${cur === c.n ? "on" : c.n < S.reached ? "done" : ""}">${c.n}. ${esc(c.title)}</a>`);
  if (strikeOn()) items.splice(6, 0, `<a href="#/strike" class="${cur === "strike" ? "on" : ""}">The strike</a>`);
  items.push(`<a href="#/result" class="${cur === "result" ? "on" : ""}">Accounting</a>`);
  return `<div class="progress">${items.join("")}</div>`;
}

function chapter(arg) {
  if (!S.mode) { S.mode = "read"; save(); modebar(); }
  const n = Math.max(1, Math.min(NCH(), +arg || 1));
  const c = D.study.chapters[n - 1];
  S.reached = Math.max(S.reached || 1, n); save();
  const side = [
    ...(c.facsimiles || []).map(f => `<figure class="facs"><a href="${f.href}"><img src="${f.src}" alt="${esc(f.caption)}" loading="lazy"></a><figcaption>${esc(f.caption)} <a href="${f.href}">Transcription and translation →</a></figcaption></figure>`),
    ...(c.plates || []).map(id => plateFig(id)),
    ...(c.data || []).map(id => `<div class="panel">${PANELS[id] ? PANELS[id]() : ""}</div>`),
  ].join("");
  view.innerHTML = `
    ${progress(n)}
    <div class="chapter">
      <div>
        <span class="tag">Chapter ${n} · ${esc(c.part)} · ${esc(c.date)}</span>
        <h1>${esc(c.title)}</h1>
        <p class="lede">${esc(c.lede)}</p>
        <div class="readable">${c.body.map(p => `<p>${esc(p)}</p>`).join("")}</div>
        ${(c.quotes || []).map(q => `<div class="quote readable"><div class="de">${esc(q.de)}</div>${q.en ? `<div class="en">${esc(q.en)}</div>` : ""}<div class="fine"><a href="${q.cite.href}">${esc(q.cite.label)}</a></div></div>`).join("")}
        ${decisionBox(c)}
        <p class="fine">Sources: ${(c.sources || []).map(id => `<a href="#/sources" title="${esc(D.sources[id].cite)}">${esc(D.sources[id].short)}</a>`).join(" · ")}</p>
        <div class="navrow">${n > 1 ? `<a class="btn" href="#/ch/${n - 1}">← Chapter ${n - 1}</a>` : "<span></span>"}<span id="next"></span></div>
      </div>
      <div class="side">${side}</div>
    </div>`;
  wireDecision(c, n);
}

function decisionBox(c) {
  const d = c.decision;
  if (!d) return "";
  if (S.mode === "play") {
    const cur = S.choices[d.key];
    return `<div class="decision"><span class="tag">Your decision</span><h3>${esc(d.prompt)}</h3>
      <div class="opts">${d.options.map(o => `<button class="opt ${cur === o.value ? "chosen" : ""}" data-v="${o.value}"><b>${esc(o.label)}</b><span>${esc(o.detail)}</span></button>`).join("")}</div>
      <p class="filenote">The file: ${esc(d.fileNote)}</p></div>`;
  }
  return `<div class="decision"><span class="tag">Decision point</span><h3>${esc(d.prompt)}</h3>
    <div class="opts">${d.options.map(o => `<div class="opt ${d.file === o.value ? "chosen" : ""}"><b>${esc(o.label)}${d.file === o.value ? " · the file's answer" : ""}</b><span>${esc(o.detail)}</span></div>`).join("")}</div>
    <p class="filenote">${esc(d.fileNote)}</p></div>`;
}

function wireDecision(c, n) {
  const next = $("#next");
  const nextTarget = () => {
    if (n === 6 && strikeOn()) return ["#/strike", "The strike →"];
    if (n === NCH()) return ["#/result", "The accounting →"];
    return [`#/ch/${n + 1}`, `Chapter ${n + 1} →`];
  };
  const draw = () => {
    const need = S.mode === "play" && c.decision && !S.choices[c.decision.key];
    const [href, label] = nextTarget();
    next.innerHTML = need ? `<span class="fine">Decide to continue.</span>` : `<a class="btn primary" href="${href}">${label}</a>`;
  };
  view.querySelectorAll(".opt[data-v]").forEach(b => b.onclick = () => {
    S.choices[c.decision.key] = b.dataset.v;
    save();
    view.querySelectorAll(".opt[data-v]").forEach(x => x.classList.toggle("chosen", x === b));
    draw(); progressRefresh(n);
  });
  draw();
}
function progressRefresh(n) { const p = view.querySelector(".progress"); if (p) p.outerHTML = progress(n); }

/* ------------------------------------------------------------ the strike (play) */
const FILE_PLAN = { base: "grove", count: "8", method: "day", recon: "recon", when: "june", drachen: "postpone" };

function strikeTable(s) {
  if (!s || !s.flown) return "";
  const rows = s.present.map(x => {
    const st = s.sunk.includes(x.name) ? "sunk" : s.damaged.includes(x.name) ? "damaged" : "—";
    return `<tr><td>${esc(x.name)}</td><td>${x.type === "BB" ? "battleship" : "fleet carrier"}</td><td>${st}</td></tr>`;
  }).join("");
  return `<table><tr><th>Heavy ships in the anchorage (war diary)</th><th>Type</th><th>In this run</th></tr>${rows || `<tr><td colspan="3">None that day</td></tr>`}</table>`;
}

function strike() {
  if (!strikeOn()) { location.hash = "#/ch/6"; return; }
  const r = DL.run(S.choices, S.seed);
  const part = y => r.log.filter(l => l.part === y).map(l => `<p>${esc(l.msg)}</p>`).join("");
  view.innerHTML = `
    ${progress("strike")}
    <span class="tag">In this study only</span>
    <h1>The strike</h1>
    <p class="lede readable">What follows did not happen. It is the model's run of your plan, with the file's figures where it gives them, the ships the Home Fleet's war diary places in the Flow, and named assumptions where neither says.</p>
    <h2>1944</h2><div class="log readable">${part(1944)}</div>${strikeTable(r.s44)}
    <h2>February 1945</h2><div class="log readable">${part(1945)}</div>${strikeTable(r.s45)}
    <div class="navrow"><a class="btn" href="#/ch/6">← Chapter 6</a><a class="btn primary" href="#/ch/7">Chapter 7: the other side →</a></div>`;
}

/* ------------------------------------------------------------ accounting */
function result() {
  const play = S.mode === "play" && S.choices.drachen;
  const c = play ? S.choices : FILE_PLAN;
  const mc = DL.monteCarlo(c, 1000, play ? 9000 : 3000);
  const r = play ? DL.run(c, S.seed) : null;
  const w = DL.win(c.when === "hold" ? "june" : c.when);
  const fileCol = `<div class="col"><span class="tag">What the file expected</span>
      <div class="big">4 heavy ships</div>
      <p class="fine">"No more than at most 2 battleships and 1–2 carriers" in Scapa; one hit destroys a battleship; two Mistel against each: eight. One estimate, no reconnaissance in the file, no losses on the way, no weather.</p></div>`;
  const recordCol = `<div class="col soviet"><span class="tag">What the war diary shows</span>
      <div class="big">${c.when === "hold" ? "—" : `${w.ships.filter(x => x.p >= 0.5).length} heavy ships`}</div>
      <p class="fine">${c.when === "hold" ? "No attack on Scapa Flow in 1944 in your plan." : `Around ${esc(w.date)}: ${w.ships.filter(x => x.p >= 0.5).map(x => esc(x.name)).join(", ")} on most days.`} In late May 1944 there were up to seven battleships and three fleet carriers; in late June, two battleships and one carrier; in February 1945, the Rodney alone. In October 1939 a single attack inside the Flow killed 833 men of the Royal Oak.</p></div>`;
  const modelCol = mcx => `<div class="col model"><span class="tag">What the model gives</span><div class="big">${mcx.hits.med} hit${mcx.hits.med === 1 ? "" : "s"}</div>
      <p class="fine">Median of 1,000 runs; 10 % of runs ${mcx.hits.p10}, 90 % ${mcx.hits.p90}. No heavy ship hit in ${pct(mcx.noHit)} of runs; at least one sunk in ${pct(mcx.anySunk)}. Median fighter pilots lost: ${mcx.pilots}.</p></div>`;
  let body;
  if (play) {
    const thisRun = s => s && s.flown ? `${s.launched} launched, ${s.hits.length} hit${s.hits.length === 1 ? "" : "s"}${s.sunk.length ? `, sunk: ${s.sunk.join(", ")}` : ""}${s.damaged.length ? `, damaged: ${s.damaged.join(", ")}` : ""}; ${s.pilotsLost} pilot${s.pilotsLost === 1 ? "" : "s"} lost` : "no attack";
    body = `<h2>Your plan</h2>
      <div class="cols3">${fileCol}${modelCol(mc)}${recordCol}</div>
      <h2>This run</h2>
      <ul class="readable"><li>1944: ${esc(thisRun(r.s44))}.</li><li>February 1945: ${esc(thisRun(r.s45))}.</li></ul>
      <p class="fine readable">Choices: ${esc(D.model.bases.find(b => b.id === c.base)?.name || "")}, ${c.count} combinations, ${c.method === "dawn" ? "moonlit night to dawn" : "by day at low level"}, ${c.recon === "recon" ? "with" : "without"} reconnaissance, ${c.when === "hold" ? "held for the landing" : esc(DL.win(c.when).label.toLowerCase())}, Dragon's Lair ${c.drachen === "attack" ? "flown" : "postponed"}.</p>`;
  } else {
    body = `<h2>The file's own plan, computed</h2>
      <p class="readable">The plan of 16 April 1944 as the study proposes it: eight Mistel from Grove, by day at very low level, after a reconnaissance flight, once all fifteen are ready about 15 June; Dragon's Lair postponed in February 1945, as it was. Run 1,000 times against the ships the war diary places in the Flow in the second half of June 1944:</p>
      <div class="cols3">${fileCol}${modelCol(mc)}${recordCol}</div>
      <h2>What happened</h2>
      <p class="readable">No Mistel ever attacked Scapa Flow. Whether the study of April 1944 was approved is not in the file; later accounts say the Mistel were sent to France after the landing. In February 1945 Göring put off Dragon's Lair, postponed it and then dropped it, while the fuel went to Eisenhammer. <a href="#/">Take the staff's seat</a> to run your own plan.</p>`;
  }
  view.innerHTML = `
    ${progress("result")}
    <span class="tag">The accounting</span>
    <h1>What the file expected, what the model gives, what the war diary shows</h1>
    ${body}
    <h2>What no column counts</h2>
    <p class="readable">The model counts heavy ships, because that is what the file counts. Each of them was manned by hundreds of men; the Royal Oak lost 833 of hers in one night in 1939. The file does not count them, or the people of Orkney, or the Italian prisoners in the camps on Lamb Holm and Burray at the edge of the Flow, who were still there in June 1944. Nor does it count the German pilots: the model does, and in most runs some do not come back. See the <a href="#/reflection">reflection</a>.</p>
    ${supportBox()}
    <div class="navrow"><a class="btn" href="#/ch/${NCH()}">← Chapter ${NCH()}</a>${S.mode === "play" ? `<button id="again">Plan again</button>` : `<a class="btn primary" href="#/">Take the staff's seat</a>`}</div>`;
  const again = $("#again");
  if (again) again.onclick = () => { S.choices = {}; S.seed = Math.floor(Math.random() * 1e9); S.reached = 1; save(); location.hash = "#/ch/1"; };
}

/* ------------------------------------------------------------ panels */
const PANELS = {
  mistel() {
    return `<h3>The Mistel of 1944, in the file's figures</h3><table>
      <tr><td>Composition</td><td>Ju 88 without crew, with 2 hollow-charge warheads; Bf 109 on top; three engines</td></tr>
      <tr><td>Expected</td><td>15 in all: 2 prototypes for training, 13 more by about 15 June 1944</td></tr>
      <tr><td>Penetration depth</td><td>400–500 km; 750–800 km with a 300-litre tank on the Bf 109; 1,400 km \"not without larger trials\"</td></tr>
      <tr><td>Take-off</td><td>run 1,200 m; runway about 1,400 × 60 m</td></tr>
      <tr><td>Speed</td><td>cruising 380–400 km/h; maximum 450–480 km/h; in the glide 550–600 km/h</td></tr>
      <tr><td>Release</td><td>at 700 m, 2 km from the ship, 20°; scatter 18 × 18 m</td></tr>
      <tr><td>Ground crew</td><td>6 mechanics and 2 armourers per aircraft for a day; a crane with a 7.50 m hook</td></tr>
    </table><p class="fine">All figures from the technical annex of 16 April 1944. <a href="#/file/c1">The annex →</a></p>`;
  },
  probabilities() {
    const A = D.model.assumptions;
    const chain = [["takes off", A.serviceable], ["not caught by fighters", 1 - A.interceptDay], ["finds the anchorage", A.findSchwan], ["finds its ship (fresh photos)", A.identifyFresh], ["survives the flak", 1 - A.flakLoss], ["hits", A.hit]];
    const prod = chain.reduce((p, x) => p * x[1], 1);
    return `<h3>One estimate, or six steps</h3>
      <p class="fine">The file reckons two Mistel per ship. The study counts the steps the file itself describes, by day at low level with fresh photographs:</p>
      <div class="chain">${chain.map(([l, p]) => `<span class="p">${l} ${pct(p)}</span>`).join(" × ")} = <b>${pct(prod)}</b></div>
      <p class="fine">Every one of these figures is an assumption of the study, named on the <a href="#/data">Data</a> page; the file gives none of them.</p>`;
  },
  fleet() {
    const rows = D.model.windows.map(w => `<tr><td><b>${esc(w.date)}</b></td><td>${w.ships.map(x => `${esc(x.name)}${x.type === "CV" ? " (carrier)" : ""} <span class="fine">${pct(x.p)}</span>`).join(", ")}</td></tr>`).join("");
    return `<h3>Heavy ships in Scapa Flow</h3><table><tr><th>Around</th><th>Battleships and fleet carriers, share of days present</th></tr>${rows}</table>
      <p class="fine">${esc(D.model.shipsNote)}</p>`;
  },
  map() { return `<h3>Jump-off airfields and Scapa Flow</h3>${mapSvg()}<p class="fine">Great-circle distances; arc of 775 km round Grove (the file's figure) and 865 km round Tirstrup. Coastline: Natural Earth.</p>`; },
};

function plateFig(id) {
  const p = D.plates.plates.find(x => x.id === id);
  if (!p) return "";
  return `<figure><a href="assets/plates/${p.id}.jpg"><img src="assets/plates/${p.id}_t.jpg" alt="${esc(p.titel)}" loading="lazy"></a><figcaption><b>${esc(p.titel)}.</b> ${esc(p.caption)}</figcaption></figure>`;
}

/* ------------------------------------------------------------ map */
function mapSvg() {
  const M = D.map;
  const P = (lon, lat) => [((lon - M.lon0) * M.cos * M.k).toFixed(1), ((M.lat1 - lat) * M.k).toFixed(1)];
  const arc = (b, km) => {
    const pts = [], R = 6371, d = km / R, la = b.lat * Math.PI / 180, lo = b.lon * Math.PI / 180;
    for (let a = 250; a <= 340; a += 3) {
      const br = a * Math.PI / 180;
      const la2 = Math.asin(Math.sin(la) * Math.cos(d) + Math.cos(la) * Math.sin(d) * Math.cos(br));
      const lo2 = lo + Math.atan2(Math.sin(br) * Math.sin(d) * Math.cos(la), Math.cos(d) - Math.sin(la) * Math.sin(la2));
      pts.push(P(lo2 * 180 / Math.PI, la2 * 180 / Math.PI).join(","));
    }
    return `<polyline points="${pts.join(" ")}" fill="none" stroke="var(--steel)" stroke-width="1.5" stroke-dasharray="5 4"/>`;
  };
  const t = D.model.target, [tx, ty] = P(t.lon, t.lat);
  const lines = D.model.bases.map(b => { const [x, y] = P(b.lon, b.lat); return `<line x1="${x}" y1="${y}" x2="${tx}" y2="${ty}" stroke="var(--ink2)" stroke-width="1" opacity=".6"/><text x="${(+x + +tx) / 2}" y="${(+y + +ty) / 2 - 4}" font-size="12" fill="var(--ink2)">${Math.round(DL.dist(b, t))} km</text>`; }).join("");
  const bases = D.model.bases.map(b => { const [x, y] = P(b.lon, b.lat); return `<g><rect x="${x - 5}" y="${y - 5}" width="10" height="10" fill="var(--steel)"/><text x="${+x + 8}" y="${+y + 16}" font-size="13" fill="var(--ink)">${esc(b.name.split(" (")[0])}</text></g>`; }).join("");
  const grove = D.model.bases.find(b => b.id === "grove"), tir = D.model.bases.find(b => b.id === "tirstrup");
  return `<div class="mapwrap"><svg viewBox="0 0 ${M.w} ${M.h}" role="img" aria-label="Map of the jump-off airfields and Scapa Flow">
    <rect width="${M.w}" height="${M.h}" fill="var(--sea)"/><path d="${M.land}" fill="var(--land)" stroke="var(--ink2)" stroke-width="0.6" fill-rule="evenodd"/>
    ${arc(grove, 775)}${arc(tir, 865)}${lines}${bases}
    <g><circle cx="${tx}" cy="${ty}" r="6" fill="var(--accent)"/><text x="${+tx + 9}" y="${+ty - 8}" font-size="14" fill="var(--ink)">Scapa Flow</text></g></svg></div>`;
}

/* ------------------------------------------------------------ the file */
function file(arg) {
  const pages = D.file.docs.flatMap(d => d.pages.map(p => ({ ...p, doc: d })));
  const cur = pages.find(p => p.id === arg);
  const list = D.file.docs.map(d => `<div><b>${esc(d.title)}</b> <span class="fine">${esc(d.ref)} · ${esc(d.src)}</span><div class="pagelist">${d.pages.map((p, i) => `<a class="btn" href="#/file/${p.id}">${p.date ? esc(p.date) : "page " + (i + 1)}</a>`).join("")}</div></div>`).join("");
  if (!cur) {
    view.innerHTML = `<span class="tag">The file</span><h1>${esc(D.file.title)}</h1>
      <p class="lede readable">Eighteen pages from three documents: the Luftwaffe operations staff's study of April 1944 with its annexes, the war diary of February 1945, and the British interrogation of the officer who was to direct Dragon's Lair. ${esc(D.file.note)}</p>
      <div class="panel readable">${list}</div>
      ${plateFig("rangemap")}
      <p class="fine">Source: ${esc(D.file.source)} <a href="${D.file.url}">NARA catalog →</a></p>`;
    return;
  }
  const i = pages.indexOf(cur);
  view.innerHTML = `<span class="tag">The file · ${esc(cur.doc.short)} · ${cur.date ? esc(cur.date) + " · " : ""}frame ${esc(cur.frame)}</span>
    <h1>${esc(cur.doc.title)}</h1>
    <div class="pagelist">${pages.map(p => `<a class="btn ${p === cur ? "primary" : ""}" href="#/file/${p.id}">${esc(p.id)}</a>`).join("")}</div>
    <div class="pageview">
      <figure class="facs"><a href="assets/file/${cur.id}.jpg"><img src="assets/file/${cur.id}.jpg" alt="Facsimile of page ${esc(cur.id)}"></a><figcaption>${esc(cur.doc.src)}, frame ${esc(cur.frame)}.</figcaption></figure>
      <div><h3>Transcription</h3><pre>${esc(cur.de)}</pre><h3 style="margin-top:1rem">${cur.doc.id === "v" ? "Note" : "Translation"}</h3><div class="en">${esc(cur.en)}</div></div>
    </div>
    <div class="navrow">${i > 0 ? `<a class="btn" href="#/file/${pages[i - 1].id}">← previous page</a>` : "<span></span>"}${i < pages.length - 1 ? `<a class="btn" href="#/file/${pages[i + 1].id}">next page →</a>` : ""}</div>
    <p class="fine">${esc(D.file.note)}</p>`;
}

/* ------------------------------------------------------------ data */
function data() {
  const A = D.model.assumptions, N = D.model.assumptionNotes;
  view.innerHTML = `<span class="tag">Data</span><h1>The figures behind the study</h1>
    <p class="lede readable">Three kinds of number: the file's own, the Home Fleet's war diary, and the study's assumptions. They are marked as such wherever they appear.</p>
    <div class="panel">${PANELS.map()}</div>
    <div class="grid g2"><div class="panel">${PANELS.mistel()}</div><div class="panel">${PANELS.probabilities()}</div></div>
    <div class="panel">${PANELS.fleet()}</div>
    <h2>The airfields</h2>
    <table>${D.model.bases.map(b => `<tr><td><b>${esc(b.name)}</b></td><td class="num">${Math.round(DL.dist(b, D.model.target))} km</td><td class="fine">${esc(b.note)}</td></tr>`).join("")}</table>
    <h2>The strike windows</h2>
    <table>${D.model.windows.map(w => `<tr><td><b>${esc(w.label)}</b></td><td>${w.available} combinations available</td><td class="fine">${esc(w.availableNote)} Weather allows the attack: ${pct(w.weather)} (assumption).</td></tr>`).join("")}</table>
    <p class="fine">${esc(D.model.weatherNote)}</p>
    <h2>The study's assumptions</h2>
    <table><tr><th>Parameter</th><th>Value</th><th>Basis</th></tr>${Object.keys(A).map(k => `<tr><td>${esc(k)}</td><td>${pct(A[k])}</td><td class="fine">${esc(N[k] || "")}</td></tr>`).join("")}</table>
    <p class="fine">The model is in <code>model.js</code>, every number in <code>data/model.json</code>. ${esc(D.map.source)}.</p>`;
}

/* ------------------------------------------------------------ plates, sources, reflection */
function plates() {
  view.innerHTML = `<span class="tag">Plates</span><h1>Scapa Flow, as the planners and the defenders saw it</h1>
    <p class="lede readable">The range map from the file, German target dossiers of 1939–41, an Admiralty chart of 1944, photographs of the Royal Navy and the US Navy, and three recent photographs of the barriers and the chapel.</p>
    <div class="plates">${D.plates.plates.map(p => plateFig(p.id).replace("</figcaption>", ` <span class="fine">${esc(p.source)}</span></figcaption>`)).join("")}</div>
    <p class="fine">${esc(D.plates.credit)}</p>`;
}

function sources() {
  const order = ["t321file", "t321ktb", "csdic", "nhn", "roskill1", "roskill3", "roof", "hansard", "dossiers", "ironhammer", "custodis", "hes", "forsyth"];
  const read = { checked: "checked by the editor at the page images or text", research: "read by a research pass, not yet checked by the editor", referred: "referred to only", lead: "lead, not seen" };
  view.innerHTML = `<span class="tag">Sources, method, limits</span><h1>How this study is made</h1>
    <div class="readable">
      <p><b>The file first.</b> The core is the study of 16 April 1944 with its annexes and the war-diary entries of February 1945, in the captured German records of the US National Archives (microfilm T-321, roll 10), and the British interrogation of Major Beeger. They are given in facsimile, full transcription and translation.</p>
      <p><b>The other side from its own record.</b> Where the British ships lay comes from the war diary of the Commander-in-Chief, Home Fleet, in a modern transcription; the defences and the fleet's movements from Roskill's official history; the barriers and the prisoners from Hansard and from Johann Custodis's study of the files.</p>
      <p><b>Public domain where it is quoted.</b> German official records, British official histories whose Crown copyright has expired, Hansard and US government works are quoted. Modern scholarship and books still in copyright are summarised and cited, not reproduced.</p>
      <p><b>Three kinds of number.</b> The file's own figures, the war diary's, and the study's assumptions, each named on the <a href="#/data">Data</a> page.</p>
      <p><b>Hypothetical.</b> The strike in the playable study did not happen. The model is a way of reading the file's arithmetic against the record, not a forecast of an alternative war.</p>
    </div>
    <h2>Sources</h2>
    ${order.map(id => { const s = D.sources[id]; return `<div class="panel readable"><b>${esc(s.short)}</b><p class="fine">${esc(s.cite)}</p><p class="fine">${esc(s.status)} · <i>${read[s.read]}</i>${s.url ? ` · <a href="${s.url}" target="_blank" rel="noopener">online</a>` : ""}</p></div>`; }).join("")}
    <h2>Open questions</h2>
    <ul class="readable fine">
      <li>Whether the study of April 1944 was approved, and what became of the fifteen Mistel, is not in the file.</li>
      <li>The detailed plans of KG 200 for Dragon's Lair (ships allotted, number of Mistel, airfields) have not been found; the war diary refers to day files that are not on the roll, and Beeger's \"fuller details\" have not been found.</li>
      <li>The British Air Ministry files on the Mistel (The National Archives, AIR 40/1486 \"Mistel: German intentions\", AIR 40/186) and on the defence of Scapa (AIR 16/689) have not been seen.</li>
      <li>The strength of the anti-aircraft defence of Scapa Flow in 1944–45 has not been found in a public-domain source.</li>
      <li>The ship movements are taken from a transcription of the Home Fleet's war diary, not yet checked against the original in ADM 199.</li>
      <li>The RAF attack on Tirstrup said to have happened on 14 February 1945 is known only from later accounts.</li>
    </ul>`;
}

function reflection() {
  view.innerHTML = `<span class="tag">Reflection</span><h1>An estimate, an anchorage, and a causeway</h1>
    <div class="readable">
      <p>This study, like <i>Iron Hammer</i>, puts its reader in the seat of a Luftwaffe staff officer. The reason is again the file: a short paper of April 1944 in which a staff weighs three targets, settles on one in a single line, and builds its whole plan on an estimate of what lies at anchor there.</p>
      <p><b>An estimate.</b> \"No more than at most 2 battleships and 1–2 carriers\": the memo does not say where the figure comes from, and the study asks for reconnaissance only afterwards. The Home Fleet's war diary shows that the estimate was wrong for the weeks in which the file was written, when Scapa held up to seven battleships, and right for the second half of June, when the weapon was due and the carriers had sailed for the Far East. It was right by accident. Ten months later, when the plan came back as Dragon's Lair, the Flow held a single old battleship. The entries of February 1945 read for this study do not say what there was to sink.</p>
      <p><b>Two answers in one file.</b> The study says night flight is impossible; the covering memo, signed the same day, says night is the best chance of surprise. The planners knew how thin their margin was. Their arithmetic of eight Mistel for four ships needed every combination to arrive, find its ship and hit it. The model does nothing cleverer than ask how often each of those things happens.</p>
      <p><b>What the arithmetic did not count.</b> A hit on a battleship meant hundreds of dead: the Royal Oak, sunk inside the Flow in 1939, lost 833 men. The barriers built afterwards to close the eastern entrances were raised in large part by Italian prisoners of war, who struck because they believed the work was forbidden to them, and lived in camps at the edge of the anchorage that the file meant to attack. The file does not mention them, because a staff paper about range and scatter has no place for them. That is the point of reading it next to the record of the other side.</p>
      <p><b>Reasons after the fact.</b> Beeger told his interrogators that bad weather ended Dragon's Lair. The war diary records a postponement in favour of Eisenhammer and a fuel crisis. A later account adds an RAF strike on the airfield and a commander who may have warned the enemy. Each version serves its teller. The study's task is to set them side by side and say what each rests on.</p>
      <p><b>Why play it.</b> The playable part does not reward destruction; it measures plans against the record. Most plans end with one hit or none and several pilots lost. The point is not that the attack would have failed, but to see, decision by decision, what the people who planned it had in front of them, and what they did not look at.</p>
    </div>`;
}

boot();
