/* Dragon's Lair, 1944–45 — the strike model.
   Takes the decisions of the playable study and the figures in data/model.json and runs the attack on
   Scapa Flow: which heavy ships were there (from the Home Fleet's war diary), what reaches the anchorage,
   what is hit, what it costs. Every probability is either the file's own or an assumption named in model.json. */
"use strict";

const DL = (function () {
  let D = null;

  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function dist(a, b) {
    const r = x => x * Math.PI / 180;
    const h = Math.sin(r(b.lat - a.lat) / 2) ** 2 + Math.cos(r(a.lat)) * Math.cos(r(b.lat)) * Math.sin(r(b.lon - a.lon) / 2) ** 2;
    return 2 * 6371 * Math.asin(Math.sqrt(h));
  }

  const win = id => D.windows.find(w => w.id === id);
  const base = id => D.bases.find(b => b.id === id);

  /* One strike against the anchorage. c: the player's choices; w: the window; b: the base. */
  function strike(c, w, b, rnd, L) {
    const A = D.assumptions;
    const s = { window: w.id, date: w.date, base: b.name, present: [], launched: 0, intercepted: 0, lostNav: 0, flak: 0, released: 0, hits: [], sunk: [], damaged: [], pilotsLost: 0, flown: false };
    const wanted = +c.count || 8;
    const ready = Math.min(wanted, w.available);
    for (let i = 0; i < ready; i++) if (rnd() < A.serviceable) s.launched++;
    s.present = w.ships.filter(x => rnd() < x.p);
    if (w.year === 1945 && rnd() >= w.weather) {
      L(`${w.date}: the weather over the North Sea and the Orkneys allows no low flight on the days before the Reichsmarschall's decision. The combinations stay at ${b.name}.`);
      return s;
    }
    if (w.year === 1944 && rnd() >= w.weather) L("The first planned days bring low cloud over the Orkneys; the staff waits for a clear day.");
    s.flown = true;

    // reconnaissance
    let fresh = false;
    if (c.recon === "recon") {
      fresh = rnd() < A.reconSuccess;
      L(fresh ? "A reconnaissance aircraft brings back photographs of the anchorage; the ships' positions are marked for the crews, as the file demands."
        : "The reconnaissance flight brings back no usable photographs. The crews fly with the old target dossiers of 1939–41.");
    } else L("No reconnaissance flight, so as not to warn the defence. The crews fly with the target dossiers of 1939–41.");

    const capital = s.present.slice().sort((a, b2) => (a.type === b2.type ? 0 : a.type === "BB" ? -1 : 1));
    L(`${s.launched} of ${ready} combinations take off from ${b.name}, ${Math.round(dist(b, D.target))} km from Scapa Flow. In the anchorage that day (war diary): ${capital.length ? capital.map(x => x.name + (x.type === "CV" ? " (carrier)" : "")).join(", ") : "no battleship and no fleet carrier"}.`);

    // allocate two per heavy ship, the file's rule; any surplus to the battleships
    const aim = [];
    for (let i = 0; i < s.launched; i++) aim.push(capital.length ? capital[Math.floor(i / 2) % capital.length] : null);

    const intercept = (w.year === 1945 ? A.interceptFeb : c.method === "dawn" ? A.interceptDawn : A.interceptDay) + (c.base === "sola" && w.year === 1944 ? A.solaAlert : 0);
    const find = w.year === 1945 ? A.findWinter : c.method === "dawn" ? A.findDawn : A.findSchwan;
    const ident = fresh ? A.identifyFresh : A.identifyOld;
    const ret = w.year === 1945 ? A.returnTirstrup : c.base === "sola" ? A.returnSola : A.returnGrove;
    const state = new Map();
    for (const t of aim) {
      if (rnd() < intercept) { s.intercepted++; if (rnd() < 0.5) s.pilotsLost++; continue; }
      if (rnd() >= find) { s.lostNav++; if (rnd() >= ret) s.pilotsLost++; continue; }
      if (!t || rnd() >= ident) { s.released++; if (rnd() >= ret) s.pilotsLost++; continue; }   // released at something else, or nothing
      if (rnd() < A.flakLoss) { s.flak++; if (rnd() < 0.5) s.pilotsLost++; continue; }
      s.released++;
      if (rnd() < A.hit && state.get(t.name) !== "sunk") {
        s.hits.push(t.name);
        const sinks = rnd() < (t.type === "BB" ? A.sinkBB : A.sinkCV);
        state.set(t.name, sinks ? "sunk" : state.get(t.name) || "damaged");
      }
      if (rnd() >= ret) s.pilotsLost++;
    }
    for (const [name, st] of state) (st === "sunk" ? s.sunk : s.damaged).push(name);
    L(`${s.intercepted} combinations are caught by fighters on the way in, ${s.lostNav} do not find the anchorage, ${s.flak} fall to the anti-aircraft fire; ${s.released} are released.`);
    L(s.hits.length ? `Hits: ${s.hits.length}. ${s.sunk.length ? "Sunk: " + s.sunk.join(", ") + ". " : ""}${s.damaged.length ? "Damaged: " + s.damaged.join(", ") + "." : ""}` : "No heavy ship is hit.");
    L(`${s.pilotsLost} fighter pilot${s.pilotsLost === 1 ? "" : "s"} do not come back.`);
    return s;
  }

  function run(c, seed) {
    const R = mulberry32(seed >>> 0), rnd = () => R();
    const out = { choices: c, log: [], s44: null, s45: null };
    const L = (msg, part) => out.log.push({ msg, part });
    const L44 = m => L(m, 1944), L45 = m => L(m, 1945);
    if (c.when === "hold") L44("The Mistel are held back for the Allied landing, against the file's advice. Scapa Flow is not attacked in 1944.");
    else out.s44 = strike(c, win(c.when || "june"), base(c.base || "grove"), rnd, L44);
    if (c.drachen === "attack") out.s45 = strike(c, win("feb45"), base("tirstrup"), rnd, L45);
    else L45("February 1945: Dragon's Lair is postponed and then not carried out, as the war diary records.");
    return out;
  }

  function monteCarlo(c, n, seed0) {
    const rows = [];
    for (let i = 0; i < n; i++) {
      const r = run(c, (seed0 || 1) + i);
      const sum = k => (r.s44 ? r.s44[k] : 0) + (r.s45 ? r.s45[k] : 0);
      const cnt = k => (r.s44 ? r.s44[k].length : 0) + (r.s45 ? r.s45[k].length : 0);
      rows.push({ hits: cnt("hits"), sunk: cnt("sunk"), damaged: cnt("damaged"), pilots: sum("pilotsLost"), launched: sum("launched"),
        flown: (r.s44 && r.s44.flown ? 1 : 0) + (r.s45 && r.s45.flown ? 1 : 0), present: r.s44 ? r.s44.present.length : 0 });
    }
    const q = (k, f) => { const s = rows.map(x => x[k]).sort((a, b) => a - b); return s[Math.floor(f * (s.length - 1))]; };
    const share = fn => rows.filter(fn).length / n;
    return { n, hits: { p10: q("hits", 0.1), med: q("hits", 0.5), p90: q("hits", 0.9) }, sunk: { p10: q("sunk", 0.1), med: q("sunk", 0.5), p90: q("sunk", 0.9) },
      pilots: q("pilots", 0.5), noHit: share(x => x.hits === 0), anySunk: share(x => x.sunk > 0), flown: share(x => x.flown > 0), present: q("present", 0.5) };
  }

  return { setData: d => { D = d; }, run, monteCarlo, dist, win, base };
})();

if (typeof module !== "undefined") module.exports = DL;
