/* Linha do tempo do vídeo "Linha 900". Tudo é calculado a partir do tempo t (segundos),
   então cada quadro é determinístico: window.seek(t) desenha exatamente aquele instante.
   Abra cenas.html#play para assistir com áudio no navegador. */
(() => {
  "use strict";
  const T = window.TEMPOS;
  const F = Object.fromEntries(T.falas.map(f => [f.id, { i: f.inicio, d: f.dur, e: f.inicio + f.dur }]));
  const TOTAL = T.total;
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => [...document.querySelectorAll(s)];

  /* ---------- utilidades ---------- */
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const lin = (t, a, b) => clamp((t - a) / (b - a));
  const eOut = (p) => 1 - Math.pow(1 - p, 3);
  const eInOut = (p) => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
  const eBack = (p) => { const c = 1.7; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); };
  const P = (t, a, b, ease = eOut) => ease(lin(t, a, b));
  const hash = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  const css = (el, o) => { for (const k in o) el.style[k] = o[k]; };

  /* ---------- cenas e seus intervalos ---------- */
  const CENAS = [
    ["gancho", 0, F.prompt.i],
    ["prompt", F.prompt.i, F.linha.i],
    ["mapa", F.linha.i, F.az900.i],
    ["selos", F.az900.i, F.prova.i],
    ["prova", F.prova.i, F.gratis.i],
    ["final", F.gratis.i, TOTAL + 1]
  ];
  const cenaAlpha = (t, a, b) => (a === 0 ? 1 : P(t, a, a + .28)) * (1 - P(t, b - .22, b, eInOut));

  /* ---------- palavras animadas ---------- */
  function splitWords(root) {
    const walk = (node, inGrad) => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(p => {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            const s = document.createElement("span"); s.className = "kw" + (inGrad ? " grad" : ""); s.textContent = p; frag.appendChild(s);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) {
          const g = n.classList.contains("grad");
          if (g) { n.classList.remove("grad"); }
          walk(n, inGrad || g);
        }
      });
    };
    walk(root, false);
    root._kw = [...root.querySelectorAll(".kw")];
  }
  $$("[data-kin]").forEach(splitWords);
  function kin(el, t, t0, t1) {
    const w = el._kw, n = w.length;
    w.forEach((s, i) => {
      const st = t0 + (t1 - t0) * (i / Math.max(1, n));
      const p = P(t, st, st + .38);
      s.style.opacity = p;
      s.style.transform = `translateY(${(1 - p) * 46}px) rotateX(${(1 - p) * -55}deg)`;
      s.style.filter = p < 1 ? `blur(${(1 - p) * 12}px)` : "none";
    });
  }

  /* ---------- fundo: grade de pontos + agentes ---------- */
  const cv = $("#fx"), ctx = cv.getContext("2d");
  const CORES = ["#4f8cff", "#7c5cff", "#a78bfa", "#22d3ee", "#34d399", "#ff9a3c", "#f472b6"];
  const ROT = ["AZ-900", "AI-901", "DP-900", "SC-900", "PL-900", "AB-900"];
  const AG = Array.from({ length: 34 }, (_, i) => ({
    x: hash(i) * 1080, y: 200 + hash(i + 50) * 1550, ax: 120 + hash(i + 9) * 260, ay: 90 + hash(i + 19) * 240,
    w1: .18 + hash(i + 3) * .35, w2: .14 + hash(i + 7) * .3, p1: hash(i + 11) * 6.28, p2: hash(i + 13) * 6.28,
    c: CORES[i % CORES.length], r: 3 + hash(i + 17) * 3, label: i < 6 ? ROT[i] : null
  }));
  const posAg = (a, t) => [a.x + Math.sin(a.w1 * t + a.p1) * a.ax, a.y + Math.cos(a.w2 * t + a.p2) * a.ay];
  function drawFx(t, glitch) {
    ctx.clearRect(0, 0, 1080, 1920);
    // grade de pontos
    ctx.fillStyle = "rgba(255,255,255,.09)";
    for (let y = 30; y < 1920; y += 60) for (let x = 30; x < 1080; x += 60) ctx.fillRect(x, y, 3, 3);
    // agentes
    const ps = AG.map(a => posAg(a, t));
    ctx.lineWidth = 1.5;
    for (let i = 0; i < ps.length; i++) for (let j = i + 1; j < ps.length; j++) {
      const d = Math.hypot(ps[i][0] - ps[j][0], ps[i][1] - ps[j][1]);
      if (d < 210) { ctx.strokeStyle = `rgba(140,170,255,${(1 - d / 210) * .3})`; ctx.beginPath(); ctx.moveTo(...ps[i]); ctx.lineTo(...ps[j]); ctx.stroke(); }
    }
    AG.forEach((a, i) => {
      for (let k = 8; k >= 1; k--) {
        const [x, y] = posAg(a, t - k * .06);
        ctx.globalAlpha = (1 - k / 9) * .35; ctx.fillStyle = a.c;
        ctx.beginPath(); ctx.arc(x, y, a.r * (1 - k / 12), 0, 6.283); ctx.fill();
      }
      ctx.globalAlpha = .9; ctx.shadowColor = a.c; ctx.shadowBlur = 18; ctx.fillStyle = a.c;
      ctx.beginPath(); ctx.arc(ps[i][0], ps[i][1], a.r, 0, 6.283); ctx.fill(); ctx.shadowBlur = 0;
      if (a.label) {
        ctx.font = "700 22px Inter"; const w = ctx.measureText(a.label).width + 22;
        ctx.globalAlpha = .55; ctx.fillStyle = "rgba(10,12,28,.9)"; ctx.strokeStyle = a.c; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.roundRect(ps[i][0] + 12, ps[i][1] - 40, w, 32, 16); ctx.fill(); ctx.stroke();
        ctx.fillStyle = "#e8ecff"; ctx.fillText(a.label, ps[i][0] + 23, ps[i][1] - 17); ctx.lineWidth = 1.5;
      }
      ctx.globalAlpha = 1;
    });
    // faixas de glitch nas transições
    if (glitch > 0) {
      const seed = Math.floor(t * 30);
      for (let k = 0; k < 7; k++) {
        const y = hash(seed + k) * 1920, h = 8 + hash(seed + k + 40) * 70;
        ctx.fillStyle = k % 2 ? `rgba(79,140,255,${.35 * glitch})` : `rgba(255,61,110,${.3 * glitch})`;
        ctx.fillRect(0, y, 1080, h);
      }
    }
  }

  /* ---------- mapa: nós e linhas ---------- */
  const NOS = [
    ["AZ-900", "Nuvem · Azure"], ["AI-901", "Inteligência Artificial"], ["DP-900", "Dados"],
    ["SC-900", "Segurança"], ["PL-900", "Power Platform"], ["AB-900", "Microsoft 365 Copilot"]
  ];
  const SELO = "../site/assets/selos/microsoft-certified-fundamentals-badge.svg";
  const ROWS = [790, 1010, 1230];
  const mnodes = $("#mnodes"), svg = $("#msvg"), NS = "http://www.w3.org/2000/svg";
  svg.innerHTML = `<defs><marker id="ah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="16" markerHeight="16" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L10,5 L0,10 Z" fill="#5cb3ee"/></marker>
    <filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>`;
  const LIG = NOS.map(([c, n], k) => {
    const esq = k % 2 === 0, yc = ROWS[Math.floor(k / 2)];
    const el = document.createElement("div");
    el.className = "mnode"; el.style.left = (esq ? 90 : 590) + "px"; el.style.top = (yc - 85) + "px";
    el.innerHTML = `<img src="${SELO}" alt=""><div><b>${c}</b><span>${n}</span></div>`;
    mnodes.appendChild(el);
    const x = esq ? 496 : 584, r = 16;
    const d = `M540,620 V${yc - r} Q540,${yc} ${esq ? 540 - r : 540 + r},${yc} H${x}`;
    const base = document.createElementNS(NS, "path");
    base.setAttribute("d", d); base.setAttribute("fill", "none"); base.setAttribute("stroke", "rgba(64,160,220,.85)");
    base.setAttribute("stroke-width", "4"); base.setAttribute("marker-end", "url(#ah)");
    const pulse = document.createElementNS(NS, "path");
    pulse.setAttribute("d", d); pulse.setAttribute("fill", "none"); pulse.setAttribute("stroke", "#eaf6ff");
    pulse.setAttribute("stroke-width", "8"); pulse.setAttribute("stroke-linecap", "round"); pulse.setAttribute("filter", "url(#gl)");
    svg.append(base, pulse);
    return { el, base, pulse, len: 0 };
  });
  const medir = () => LIG.forEach(l => { l.len = l.base.getTotalLength(); });

  /* ---------- selos: cartões ---------- */
  const IDS = ["az900", "ai901", "dp900", "sc900", "pl900", "ab900"];
  const SIM = { az900: true, ai901: true, sc900: true };
  const scards = $("#scards"), sdots = $("#sdots");
  const CARDS = NOS.map(([c, n], k) => {
    const el = document.createElement("div");
    el.className = "scard";
    el.innerHTML = `<img src="${SELO}" alt=""><div class="code grad">${c}</div><div class="topic">${n}</div>
      <div class="tags"><span>🇧🇷 Prova em português</span><span>Não expira</span>${SIM[IDS[k]] ? '<span class="on">✓ Simulado na Udemy</span>' : '<span class="soon">Simulado em breve</span>'}</div>`;
    scards.appendChild(el);
    const d = document.createElement("span"); d.textContent = c; sdots.appendChild(d);
    return { el, dot: d };
  });

  /* ---------- legendas ---------- */
  const LEG = {
    gancho: "Você ainda *NÃO* tem uma certificação Microsoft?",
    atencao: "Então presta *atenção.*",
    prompt: "Se você quer começar em nuvem, IA ou segurança, existe um *caminho certo.*",
    linha: "A *Linha 900:* seis certificações Fundamentals, a porta de entrada da Microsoft.",
    az900: "*AZ-900*, nuvem.", ai901: "*AI-901*, inteligência artificial.", dp900: "*DP-900*, dados.",
    sc900: "*SC-900*, segurança.", pl900: "*PL-900*, Power Platform.", ab900: "E *AB-900*, Copilot.",
    prova: "Mais de *600 questões* no estilo real da prova, com a explicação de cada alternativa.",
    gratis: "E o simulado da *AI-901* está *GRÁTIS*, por tempo limitado.",
    aqui: "Sua próxima certificação Microsoft começa *aqui.*",
    bio: "*Link na bio.*"
  };
  const capEl = $("#cap");
  const LEGW = Object.fromEntries(Object.entries(LEG).map(([k, s]) => {
    const words = []; let hi = false;
    s.split(" ").forEach(w => {
      const starts = w.startsWith("*"), ends = /\*[.,?!:]*$/.test(w);
      const on = hi || starts; words.push({ w: w.replace(/\*/g, ""), hi: on });
      if (starts && !ends) hi = true; if (ends) hi = false;
    });
    return [k, words];
  }));
  let capKey = "", capN = -1;
  function legenda(t) {
    let cur = null;
    T.falas.forEach((f, i) => { const next = T.falas[i + 1]; if (t >= f.inicio - .05 && t < (next ? next.inicio - .05 : TOTAL + 1)) cur = f; });
    if (!cur) { capEl.innerHTML = ""; capKey = ""; return; }
    const ws = LEGW[cur.id];
    const n = Math.ceil(clamp((t - cur.inicio) / (cur.dur * .92)) * ws.length);
    if (cur.id === capKey && n === capN) return;
    capKey = cur.id; capN = n;
    capEl.innerHTML = ws.slice(0, Math.max(1, n)).map(o => `<span class="${o.hi ? "hi" : ""}">${o.w}</span>`).join(" ");
  }

  /* ---------- quadro ---------- */
  const sc = Object.fromEntries(CENAS.map(([id]) => [id, $("#sc-" + id)]));
  const PTXT = "Quero começar em nuvem, IA ou segurança. Por onde eu começo?";
  const ptext = $("#ptext"), caret = $("#caret");
  const opts = $$(".opt");

  function seek(t) {
    // fundo
    css($("#b1"), { left: (-300 + Math.sin(t * .12) * 140) + "px", top: (-250 + Math.cos(t * .1) * 160) + "px" });
    css($("#b2"), { left: (420 + Math.cos(t * .09) * 160) + "px", top: (700 + Math.sin(t * .11) * 220) + "px" });
    css($("#b3"), { left: (-150 + Math.sin(t * .08 + 2) * 180) + "px", top: (1250 + Math.cos(t * .1) * 140) + "px" });
    // brilho/glitch na troca de cena
    let gl = 0;
    CENAS.slice(1).forEach(([, a]) => { gl = Math.max(gl, 1 - Math.abs(t - a) / .18); });
    gl = clamp(gl);
    drawFx(t, gl);
    $("#flash").style.opacity = gl * .5;
    $("#brand").style.opacity = P(t, .2, .8) * (1 - P(t, F.aqui.i - .3, F.aqui.i));

    CENAS.forEach(([id, a, b]) => { const al = cenaAlpha(t, a, b); sc[id].style.opacity = al; sc[id].style.visibility = al > 0.001 ? "visible" : "hidden"; });

    /* 1. gancho */
    const g = F.gancho, tNao = g.i + .72;
    kin($("#g1"), t, g.i + .05, g.i + .45);
    const pn = P(t, tNao, tNao + .28, eBack);
    const jit = t < tNao + .55 ? 1 : .25;
    const s = Math.floor(t * 24);
    const nao = $("#nao");
    nao.style.opacity = lin(t, tNao, tNao + .06);
    nao.style.transform = `scale(${1.7 - .7 * pn})`;
    const dx = (hash(s) - .5) * 26 * jit, dy = (hash(s + 3) - .5) * 10 * jit;
    css(nao.querySelector(".r"), { transform: `translate(${-8 - dx}px,${dy}px)`, opacity: .85 });
    css(nao.querySelector(".c"), { transform: `translate(${8 + dx}px,${-dy}px)`, opacity: .85 });
    css(nao.querySelector(".m"), { transform: `translate(${dx * .3}px,0)` });
    kin($("#g2"), t, tNao + .3, g.e - .1);
    const at = F.atencao;
    const g3 = $("#g3");
    g3.style.opacity = P(t, at.i - .05, at.i + .25);
    g3.style.transform = `translateY(${(1 - P(t, at.i - .05, at.i + .35)) * 50}px)`;
    $("#mark i").style.width = P(t, at.i + .5, at.i + .9, eInOut) * 100 + "%";

    /* 2. prompt */
    const pr = F.prompt;
    kin($("#ptitle"), t, pr.i + .05, pr.i + .4);
    const pb = P(t, pr.i + .1, pr.i + .65);
    css($("#pbox"), { opacity: pb, transform: `translateY(${(1 - pb) * 120}px) scale(${.94 + .06 * pb})` });
    const nch = Math.round(clamp((t - (pr.i + .55)) / (pr.d * .72)) * PTXT.length);
    ptext.textContent = PTXT.slice(0, nch);
    caret.style.opacity = (Math.floor(t * 2.4) % 2 === 0 || nch < PTXT.length) ? 1 : 0;
    $$("#pchips span").forEach((c, k) => {
      const st = pr.i + pr.d * [.3, .5, .68][k];
      const p = P(t, st, st + .35, eBack);
      css(c, { opacity: lin(t, st, st + .15), transform: `scale(${.4 + .6 * p})`,
        background: t > st ? "linear-gradient(135deg,rgba(79,140,255,.35),rgba(124,92,255,.3))" : "", borderColor: t > st ? "rgba(157,188,255,.7)" : "" });
    });
    const po = P(t, pr.i + pr.d * .82, pr.i + pr.d * .82 + .4, eBack);
    css($("#pout"), { opacity: lin(t, pr.i + pr.d * .82, pr.i + pr.d * .82 + .15), transform: `translateY(${(1 - po) * 40}px) scale(${.85 + .15 * po})` });

    /* 3. mapa */
    const li = F.linha;
    const mt = P(t, li.i + .05, li.i + .45);
    css($("#mtitle"), { opacity: mt, transform: `translateY(${(1 - mt) * 40}px)` });
    const hb = P(t, li.i + .3, li.i + .7, eBack);
    css($("#hub"), { opacity: lin(t, li.i + .3, li.i + .45), transform: `scale(${.5 + .5 * hb})` });
    if (!LIG[0].len) medir();
    LIG.forEach((l, k) => {
      const st = li.i + .85 + k * .38;
      const draw = P(t, st, st + .45, eInOut);
      l.base.style.strokeDasharray = `${l.len}`; l.base.style.strokeDashoffset = `${l.len * (1 - draw)}`;
      l.base.style.opacity = draw > 0 ? 1 : 0;
      const np = P(t, st + .35, st + .7, eBack);
      css(l.el, { opacity: lin(t, st + .35, st + .5), transform: `translateX(${(k % 2 ? 1 : -1) * (1 - np) * 80}px) scale(${.8 + .2 * np})` });
      // pulso correndo do centro até a ponta da seta
      const seg = 90, per = 1.5, ph = ((t - st - .5 + k * .23) % per + per) % per / per;
      const on = t > st + .5;
      l.pulse.style.strokeDasharray = `${seg} ${l.len + seg}`;
      l.pulse.style.strokeDashoffset = `${seg - (l.len + seg) * ph}`;
      l.pulse.style.opacity = on ? 1 : 0;
    });
    const ms = P(t, li.i + 3.4, li.i + 3.9);
    css($("#msub"), { opacity: ms, transform: `translateY(${(1 - ms) * 30}px)` });

    /* 4. selos */
    CARDS.forEach((c, k) => {
      const f = F[IDS[k]], nxt = k < 5 ? F[IDS[k + 1]].i : F.prova.i;
      const pin = P(t, f.i - .12, f.i + .38, eOut), pout = P(t, nxt - .2, nxt + .18, eInOut);
      const x = (1 - pin) * 560 - pout * 560, ry = (1 - pin) * -65 + pout * 65;
      const flt = Math.sin(t * 2.2) * 8;
      css(c.el, { opacity: Math.min(lin(t, f.i - .12, f.i + .1), 1 - lin(t, nxt - .05, nxt + .18)), transform: `perspective(1600px) translateX(${x}px) translateY(${flt}px) rotateY(${ry}deg) scale(${.86 + .14 * pin})` });
      c.el.querySelector("img").style.transform = `rotate(${Math.sin(t * 1.6 + k) * 4}deg) scale(${1 + Math.sin(t * 3) * .02})`;
      const act = t >= f.i - .12 && t < nxt - .05;
      css(c.dot, { color: act ? "#fff" : "", borderColor: act ? "rgba(110,231,183,.8)" : "", background: act ? "rgba(52,211,153,.25)" : (t >= nxt ? "rgba(255,255,255,.1)" : ""), transform: act ? "scale(1.12)" : "scale(1)" });
    });

    /* 5. prova */
    const pv = F.prova;
    kin($("#qtitle"), t, pv.i + .05, pv.i + .45);
    const qc = P(t, pv.i + .15, pv.i + .6);
    css($("#qcard"), { opacity: qc, transform: `translateY(${(1 - qc) * 90}px)` });
    const tOk = pv.i + pv.d * .42;
    opts.forEach((o, k) => {
      const p = P(t, pv.i + .45 + k * .12, pv.i + .75 + k * .12);
      o.classList.toggle("ok", k === 2 && t > tOk);
      css(o, { opacity: p * (t > tOk && k !== 2 ? .4 : 1), transform: `translateX(${(1 - p) * 60}px) scale(${k === 2 && t > tOk ? 1 + .04 * (1 - P(t, tOk, tOk + .4)) : 1})` });
    });
    o2(opts[2].querySelector(".chk"), P(t, tOk, tOk + .3, eBack));
    const qe = P(t, pv.i + pv.d * .58, pv.i + pv.d * .58 + .4);
    css($("#qexp"), { opacity: qe, transform: `translateY(${(1 - qe) * 30}px)` });
    const sa = P(t, pv.i + pv.d * .25, pv.i + pv.d * .25 + .4);
    css($("#stats"), { opacity: sa, transform: `translateY(${(1 - sa) * 40}px)` });
    $("#nq").textContent = Math.round(628 * P(t, pv.i + pv.d * .25, pv.i + pv.d * .25 + 1.3, eOut)) + "+";

    /* 6. final */
    const gr = F.gratis, aq = F.aqui, bi = F.bio;
    const fi = P(t, gr.i + .05, gr.i + .5, eBack), fo = P(t, aq.i - .35, aq.i, eInOut);
    css($("#free"), { opacity: lin(t, gr.i, gr.i + .15) * (1 - fo), transform: `scale(${(.7 + .3 * fi) * (1 - .25 * fo)}) translateY(${-fo * 200}px) rotate(${(1 - fi) * -6}deg)` });
    const gp = 1 + Math.max(0, Math.sin((t - gr.i) * 5)) * .05 * P(t, gr.i + .8, gr.i + 1);
    $("#free .g").style.transform = `scale(${gp})`;
    const rb = P(t, gr.i + .9, gr.i + 1.3, eBack);
    $("#free .rib").style.transform = `rotate(-4deg) translateX(${(1 - rb) * -110}%)`;
    const av = P(t, aq.i - .1, aq.i + .4, eBack);
    css($("#avatar"), { opacity: lin(t, aq.i - .1, aq.i + .05), transform: `scale(${.4 + .6 * av})` });
    $("#avatar").style.setProperty("--a", (t * 140) + "deg");
    kin($("#fh"), t, aq.i, aq.e - .3);
    const bb = P(t, bi.i - .25, bi.i + .2, eBack);
    const beat = t > bi.i + .9 ? 1 + Math.max(0, Math.sin((t - bi.i) * 6)) * .04 : 1;
    css($("#fbio"), { opacity: lin(t, bi.i - .25, bi.i - .1), transform: `scale(${(.5 + .5 * bb) * beat})` });
    $("#furl").style.opacity = P(t, bi.i, bi.i + .4);
    // cursor que entra e clica no botão
    const cm = P(t, bi.i + .05, bi.i + .75, eInOut);
    const cx = 900 + (600 - 900) * cm, cy = 1720 + (1255 - 1720) * cm;
    const press = t > bi.i + .78 && t < bi.i + .95 ? .85 : 1;
    css($("#cursor"), { opacity: lin(t, bi.i, bi.i + .15), transform: `translate(${cx}px,${cy}px) scale(${press})` });
    const rp = lin(t, bi.i + .8, bi.i + 1.4);
    css($("#ring"), { opacity: rp > 0 && rp < 1 ? 1 - rp : 0, transform: `translate(${600 - 30}px,${1240 - 30}px) scale(${1 + rp * 4})` });

    legenda(t);
  }
  function o2(el, p) { css(el, { opacity: p, transform: `scale(${.3 + .7 * p})`, display: "inline-block" }); }

  window.seek = seek;
  window.DURACAO = TOTAL;
  window.pronto = Promise.all([document.fonts.ready, ...[...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; }))]).then(() => { medir(); seek(0); return true; });

  /* ---------- prévia com áudio: cenas.html#play ---------- */
  if (location.hash === "#play") {
    document.body.classList.add("preview");
    const fit = () => document.body.style.setProperty("--s", Math.min(innerHeight / 1920, innerWidth / 1080) * .96);
    fit(); addEventListener("resize", fit);
    const aud = $("#aud");
    const loop = () => { seek(aud.currentTime); requestAnimationFrame(loop); };
    window.pronto.then(loop);
    document.body.addEventListener("click", () => { aud.paused ? aud.play() : aud.pause(); });
  }
})();
