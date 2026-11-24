/* Efeitos visuais: enxame de agentes, título animado, cursor fantasma e faixas de certificações. */
(() => {
  "use strict";
  const RB = window.RB, { $, $$, esc, reduced } = RB;
  const mobile = matchMedia("(max-width: 640px)").matches;

  /* ---------- Dados das certificações (carregados uma vez) ---------- */
  let _certs;
  RB.loadCerts = () => _certs || (_certs = fetch("/assets/certificacoes.json").then(r => r.json()));

  /* ---------- 1. Enxame de agentes (canvas) ---------- */
  const cv = $("#agentes");
  if (cv && !reduced) {
    const ctx = cv.getContext("2d");
    const DPR = Math.min(devicePixelRatio || 1, 1.5);
    const CORES = ["#4f8cff", "#7c5cff", "#a78bfa", "#22d3ee", "#34d399", "#ff9a3c", "#f472b6"];
    const ROTULOS = ["AZ-900", "SC-900", "AI-901", "DP-900", "PL-900", "AB-900", "AZ-104", "SC-200", "PL-300", "AI-103"];
    let W = 0, H = 0, agents = [], mouse = { x: -9999, y: -9999, on: false };
    const N = mobile ? 26 : 64;
    function resize() {
      W = innerWidth; H = innerHeight;
      cv.width = W * DPR; cv.height = H * DPR; cv.style.width = W + "px"; cv.style.height = H + "px";
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    }
    function make(i) {
      const a = Math.random() * Math.PI * 2, sp = .6 + Math.random() * .8;
      return { x: Math.random() * W, y: Math.random() * H, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp,
        c: CORES[i % CORES.length], r: 1.6 + Math.random() * 1.6, trail: [],
        label: i < (mobile ? 4 : 10) ? ROTULOS[i % ROTULOS.length] : null };
    }
    resize(); agents = Array.from({ length: N }, (_, i) => make(i));
    // Forte no topo, discreto atrás do conteúdo
    const fade = () => { cv.style.opacity = scrollY < innerHeight * .6 ? ".85" : ".28"; };
    cv.style.transition = "opacity .8s ease"; fade();
    addEventListener("scroll", fade, { passive: true });
    addEventListener("resize", resize);
    addEventListener("pointermove", (e) => { mouse.x = e.clientX; mouse.y = e.clientY; mouse.on = true; }, { passive: true });
    addEventListener("pointerleave", () => { mouse.on = false; });

    const MAXV = 1.6, VIEW = 70, SEP = 22, LINK = mobile ? 80 : 110;
    let running = true, last = 0;
    document.addEventListener("visibilitychange", () => { running = !document.hidden; if (running) requestAnimationFrame(tick); });
    function tick(t) {
      if (!running) return;
      if (t - last < 16) { requestAnimationFrame(tick); return; }
      last = t;
      ctx.clearRect(0, 0, W, H);
      // regras de enxame (alinhamento, coesão, separação) + atração pelo mouse
      for (const a of agents) {
        let ax = 0, ay = 0, cx = 0, cy = 0, sx = 0, sy = 0, n = 0;
        for (const b of agents) {
          if (a === b) continue;
          const dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy);
          if (d < VIEW) { ax += b.vx; ay += b.vy; cx += b.x; cy += b.y; n++; if (d < SEP) { sx -= dx / (d || 1); sy -= dy / (d || 1); } }
        }
        if (n) { a.vx += (ax / n - a.vx) * .03 + (cx / n - a.x) * .0006; a.vy += (ay / n - a.vy) * .03 + (cy / n - a.y) * .0006; }
        a.vx += sx * .05; a.vy += sy * .05;
        if (mouse.on) { const dx = mouse.x - a.x, dy = mouse.y - a.y, d = Math.hypot(dx, dy); if (d < 260) { a.vx += dx / d * .05; a.vy += dy / d * .05; } }
        a.vx += (Math.random() - .5) * .06; a.vy += (Math.random() - .5) * .06;
        const v = Math.hypot(a.vx, a.vy); if (v > MAXV) { a.vx = a.vx / v * MAXV; a.vy = a.vy / v * MAXV; }
        a.x += a.vx; a.y += a.vy;
        if (a.x < -20) a.x = W + 20; if (a.x > W + 20) a.x = -20; if (a.y < -20) a.y = H + 20; if (a.y > H + 20) a.y = -20;
        a.trail.push(a.x, a.y); if (a.trail.length > 16) a.trail.splice(0, 2);
      }
      // ligações entre agentes próximos (a "conversa")
      ctx.lineWidth = 1;
      for (let i = 0; i < agents.length; i++) for (let j = i + 1; j < agents.length; j++) {
        const a = agents[i], b = agents[j], d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < LINK) { ctx.strokeStyle = `rgba(140,170,255,${(1 - d / LINK) * .22})`; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
      }
      // rastros, corpos e rótulos
      for (const a of agents) {
        const tr = a.trail;
        for (let k = 2; k < tr.length; k += 2) {
          ctx.strokeStyle = a.c; ctx.globalAlpha = (k / tr.length) * .5; ctx.lineWidth = a.r * (k / tr.length);
          ctx.beginPath(); ctx.moveTo(tr[k - 2], tr[k - 1]); ctx.lineTo(tr[k], tr[k + 1]); ctx.stroke();
        }
        ctx.globalAlpha = 1;
        ctx.fillStyle = a.c; ctx.shadowColor = a.c; ctx.shadowBlur = 10;
        ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2); ctx.fill(); ctx.shadowBlur = 0;
        if (a.label) {
          ctx.font = "600 10px Inter, sans-serif"; const w = ctx.measureText(a.label).width + 10;
          ctx.globalAlpha = .55; ctx.fillStyle = "rgba(10,12,28,.85)"; ctx.strokeStyle = a.c; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.roundRect(a.x + 6, a.y - 18, w, 15, 7); ctx.fill(); ctx.stroke();
          ctx.fillStyle = "#e8ecff"; ctx.fillText(a.label, a.x + 11, a.y - 7); ctx.globalAlpha = 1;
        }
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  /* ---------- 2. Título com palavras surgindo ---------- */
  $$("[data-kinetic]").forEach(h => {
    let i = 0;
    const wrap = (node) => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(p => {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            const s = document.createElement("span"); s.className = "kw"; s.textContent = p; s.style.setProperty("--i", i++); frag.appendChild(s);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) wrap(n);
      });
    };
    wrap(h);
    requestAnimationFrame(() => h.classList.add("go"));
  });

  /* ---------- 3. Cursor fantasma que "clica" no guia ---------- */
  const gc = $("#ghostCursor"), alvo = $("#ctaGuia");
  if (gc && alvo && !reduced && !sessionStorage.getItem("rb_cursor")) {
    sessionStorage.setItem("rb_cursor", "1");
    setTimeout(() => {
      const r = alvo.getBoundingClientRect();
      if (r.top > innerHeight || r.bottom < 0) return;
      const x0 = innerWidth * .82, y0 = innerHeight * .95;
      const x1 = r.left + r.width * .62, y1 = r.top + r.height * .55;
      gc.style.setProperty("--x0", x0 + "px"); gc.style.setProperty("--y0", y0 + "px");
      gc.style.setProperty("--x1", x1 + "px"); gc.style.setProperty("--y1", y1 + "px");
      gc.classList.add("run");
      setTimeout(() => { alvo.classList.add("clicked"); setTimeout(() => alvo.classList.remove("clicked"), 900); }, 1500);
      setTimeout(() => gc.classList.remove("run"), 3200);
    }, 1900);
  }

  /* ---------- 4. Faixas inclinadas com as certificações ---------- */
  const ra = $("#ribbonA"), rb = $("#ribbonB");
  if (ra) RB.loadCerts().then(d => {
    const cs = d.certificacoes;
    const item = (c) => `<a href="/certificacoes/${c.id}/" class="rb-item t-${c.trilha}"><i></i><b>${esc(c.codigo)}</b><span>${esc(c.nomePt)}</span></a>`;
    const a = cs.map(item).join("");
    ra.innerHTML = a + a;
    if (rb) { const b = [...cs].reverse().map(c => `<span class="rb-out">${esc(c.codigo)}</span>`).join(""); rb.innerHTML = b + b; }
    ra.style.setProperty("--dur", (cs.length * 3.2) + "s");
  });
})();
