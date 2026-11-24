/* Stories do site (sem ligação com o Instagram).
   A lista fica em dados.js (window.STORIES). Tocar na foto abre o visualizador. */
(() => {
  "use strict";
  const RB = window.RB, S = window.SITE;
  const { esc, simFor, couponActive, courseUrl, track } = RB;
  const quando = (v) => new Date(v.includes("T") ? v : v + "T23:59:59");
  const agora = new Date();
  const LISTA = (window.STORIES || []).filter(s => s && s.arquivo && (!s.ate || quando(s.ate) > agora));
  if (!LISTA.length) return;
  const SEQ = [...LISTA].reverse();               // assiste do mais antigo para o mais novo, como no Instagram

  /* ---------- vistos (guardados no navegador do visitante) ---------- */
  const CHAVE = "rb_stories_vistos";
  let vistos;
  try { vistos = new Set(JSON.parse(localStorage.getItem(CHAVE) || "[]")); } catch (e) { vistos = new Set(); }
  const marcar = (id) => { vistos.add(id); try { localStorage.setItem(CHAVE, JSON.stringify([...vistos])); } catch (e) {} atualizarAnel(); };
  const todosVistos = () => SEQ.every(s => vistos.has(s.id));

  /* ---------- foto com anel ---------- */
  const alvos = ["#avatar", "#avatar2"].map(s => document.querySelector(s)).filter(Boolean);
  alvos.forEach(el => {
    el.classList.add("has-stories");
    el.setAttribute("role", "button"); el.tabIndex = 0;
    el.setAttribute("aria-label", `Ver stories de ${S.nome}`);
    if (el.id === "avatar") { const tag = document.createElement("span"); tag.className = "story-tag"; tag.textContent = "Story"; el.appendChild(tag); }
    el.addEventListener("click", () => abrir());
    el.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); abrir(); } });
  });
  function atualizarAnel() { alvos.forEach(el => el.classList.toggle("seen", todosVistos())); }
  atualizarAnel();

  /* ---------- visualizador ---------- */
  const ICON = {
    x: '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    som: '<svg viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 8.5a5 5 0 010 7M18.5 6a8.5 8.5 0 010 12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
    mudo: '<svg viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 9l6 6M22 9l-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    pausa: '<svg viewBox="0 0 24 24"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z" fill="currentColor"/></svg>',
    play: '<svg viewBox="0 0 24 24"><path d="M7 4.5v15l12-7.5z" fill="currentColor"/></svg>',
    seta: '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7" stroke="currentColor" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    link: '<svg viewBox="0 0 24 24"><path d="M10 14a4.5 4.5 0 006.4 0l3-3a4.5 4.5 0 00-6.4-6.4l-1.2 1.2M14 10a4.5 4.5 0 00-6.4 0l-3 3a4.5 4.5 0 006.4 6.4l1.2-1.2" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg>'
  };
  let root, frame, bars, media, tap, cta, btnSom, btnPausa, spin, timeEl;
  let idx = 0, aberto = false, pausado = false, mudo = false;
  let video = null, imgInicio = 0, imgDecorrido = 0, imgDur = 6, raf = 0, segurando = false, origem = null;

  function montar() {
    root = document.createElement("div");
    root.className = "sv"; root.setAttribute("role", "dialog"); root.setAttribute("aria-modal", "true"); root.setAttribute("aria-label", `Stories de ${S.nome}`);
    root.innerHTML = `
      <button class="sv-side sv-prev" type="button" aria-label="Story anterior">${ICON.seta}</button>
      <div class="sv-frame">
        <div class="sv-bars">${SEQ.map(() => "<i><b></b></i>").join("")}</div>
        <div class="sv-head">
          <img class="sv-av" src="${esc(S.foto || "/assets/favicon.svg")}" alt="">
          <span class="sv-name">${esc(S.nome)}</span><span class="sv-time"></span>
          <span class="sv-sp"></span>
          <button type="button" class="sv-btn sv-pausa" aria-label="Pausar">${ICON.pausa}</button>
          <button type="button" class="sv-btn sv-som" aria-label="Som">${ICON.som}</button>
          <button type="button" class="sv-btn sv-x" aria-label="Fechar">${ICON.x}</button>
        </div>
        <div class="sv-media"></div>
        <div class="sv-spin" aria-hidden="true"></div>
        <div class="sv-tap" aria-hidden="true"></div>
        <a class="sv-cta" target="_blank" rel="noopener" hidden></a>
      </div>
      <button class="sv-side sv-next" type="button" aria-label="Próximo story">${ICON.seta}</button>`;
    document.body.appendChild(root);
    frame = root.querySelector(".sv-frame"); bars = [...root.querySelectorAll(".sv-bars b")];
    media = root.querySelector(".sv-media"); tap = root.querySelector(".sv-tap"); cta = root.querySelector(".sv-cta");
    btnSom = root.querySelector(".sv-som"); btnPausa = root.querySelector(".sv-pausa"); spin = root.querySelector(".sv-spin"); timeEl = root.querySelector(".sv-time");

    root.querySelector(".sv-x").addEventListener("click", fechar);
    root.querySelector(".sv-prev").addEventListener("click", anterior);
    root.querySelector(".sv-next").addEventListener("click", proximo);
    btnSom.addEventListener("click", () => { mudo = !mudo; if (video) video.muted = mudo; btnSom.innerHTML = mudo ? ICON.mudo : ICON.som; });
    btnPausa.addEventListener("click", () => (pausado ? retomar() : pausar()));
    root.addEventListener("click", (e) => { if (e.target === root) fechar(); });
    cta.addEventListener("click", () => { pausar(); track("story_link", { story: SEQ[idx].id }); });

    // toque: esquerda volta, direita avança, segurar pausa, arrastar para baixo fecha
    let holdT = 0;
    tap.addEventListener("pointerdown", (e) => {
      origem = { x: e.clientX, y: e.clientY, t: Date.now() }; segurando = false;
      tap.setPointerCapture(e.pointerId);
      holdT = setTimeout(() => { segurando = true; pausar(true); }, 200);
    });
    tap.addEventListener("pointermove", (e) => {
      if (!origem) return;
      const dy = e.clientY - origem.y;
      if (dy > 8) { clearTimeout(holdT); frame.style.transform = `translateY(${dy}px) scale(${1 - Math.min(dy, 400) / 2000})`; frame.style.opacity = 1 - Math.min(dy, 400) / 700; }
    });
    const solta = (e) => {
      if (!origem) return;
      clearTimeout(holdT);
      const dy = e.clientY - origem.y, dx = e.clientX - origem.x;
      frame.style.transform = ""; frame.style.opacity = "";
      if (dy > 110) { origem = null; fechar(); return; }
      if (segurando) { retomar(true); }
      else if (Math.abs(dx) > 60) { dx < 0 ? proximo() : anterior(); }
      else { const r = tap.getBoundingClientRect(); (e.clientX - r.left < r.width * .32) ? anterior() : proximo(); }
      origem = null; segurando = false;
    };
    tap.addEventListener("pointerup", solta);
    tap.addEventListener("pointercancel", () => { clearTimeout(holdT); origem = null; frame.style.transform = ""; frame.style.opacity = ""; if (segurando) retomar(true); });
    document.addEventListener("keydown", (e) => {
      if (!aberto) return;
      if (e.key === "Escape") fechar();
      else if (e.key === "ArrowRight") proximo();
      else if (e.key === "ArrowLeft") anterior();
      else if (e.key === " ") { e.preventDefault(); pausado ? retomar() : pausar(); }
    });
    document.addEventListener("visibilitychange", () => { if (aberto && document.hidden) pausar(); });
  }

  function tempoRelativo(d) {
    const min = Math.max(0, Math.round((Date.now() - new Date(d)) / 6e4));
    if (min < 1) return "agora";
    if (min < 60) return `há ${min} min`;
    const h = Math.round(min / 60); if (h < 24) return `há ${h} h`;
    const dd = Math.round(h / 24); return dd < 7 ? `há ${dd} d` : new Date(d).toLocaleDateString("pt-BR", { day: "2-digit", month: "short" });
  }

  function botao(s) {
    const b = s.botao;
    if (!b) { cta.hidden = true; return; }
    let href = b.link || "";
    if (b.simulado) {
      const sim = simFor(b.simulado);
      href = sim ? courseUrl(sim, sim.cursos[0]) : `/certificacoes/${b.simulado}/`;
      if (sim && !couponActive(sim)) href = sim.cursos[0].url;
    }
    if (!href) { cta.hidden = true; return; }
    cta.href = href;
    cta.target = /^https?:/.test(href) ? "_blank" : "_self";
    cta.innerHTML = `${ICON.link}<span>${esc(b.texto || "Saiba mais")}</span>`;
    cta.hidden = false;
  }

  function limpar() {
    cancelAnimationFrame(raf);
    if (video) { video.pause(); video.removeAttribute("src"); video.load(); video = null; }
    media.innerHTML = "";
  }

  function mostrar(i) {
    limpar();
    idx = i; pausado = false; btnPausa.innerHTML = ICON.pausa;
    const s = SEQ[i];
    bars.forEach((b, k) => { b.style.width = k < i ? "100%" : "0%"; });
    timeEl.textContent = s.data ? tempoRelativo(s.data) : "";
    botao(s);
    marcar(s.id);
    track("story_ver", { story: s.id });
    root.querySelector(".sv-prev").style.visibility = i > 0 ? "visible" : "hidden";
    btnSom.style.display = s.tipo === "video" ? "" : "none";
    spin.classList.add("on");
    if (s.tipo === "video") {
      video = document.createElement("video");
      video.playsInline = true; video.setAttribute("playsinline", ""); video.preload = "auto";
      if (s.capa) video.poster = s.capa;
      video.muted = mudo; video.src = s.arquivo;
      video.addEventListener("waiting", () => spin.classList.add("on"));
      video.addEventListener("playing", () => spin.classList.remove("on"));
      video.addEventListener("ended", proximo);
      media.appendChild(video);
      const p = video.play();
      if (p && p.catch) p.catch(() => { mudo = true; video.muted = true; btnSom.innerHTML = ICON.mudo; video.play().catch(() => {}); });
    } else {
      const img = new Image(); img.alt = ""; img.src = s.arquivo;
      imgDur = s.segundos || 6; imgDecorrido = 0;
      img.onload = () => { spin.classList.remove("on"); imgInicio = performance.now(); };
      media.appendChild(img);
    }
    const loop = (t) => {
      let p = 0;
      if (video) p = video.duration ? video.currentTime / video.duration : 0;
      else if (imgInicio) {
        const dec = imgDecorrido + (pausado ? 0 : (t - imgInicio) / 1000);
        p = dec / imgDur;
        if (p >= 1) { proximo(); return; }
      }
      bars[idx].style.width = (Math.min(1, p) * 100) + "%";
      raf = requestAnimationFrame(loop);
    };
    imgInicio = 0;
    raf = requestAnimationFrame(loop);
  }

  function pausar(silencioso) {
    if (pausado) return; pausado = true;
    if (video) video.pause();
    else if (imgInicio) { imgDecorrido += (performance.now() - imgInicio) / 1000; }
    if (!silencioso) btnPausa.innerHTML = ICON.play;
    root.classList.add("paused");
  }
  function retomar() {
    if (!pausado) return; pausado = false;
    if (video) video.play().catch(() => {});
    else if (imgInicio) imgInicio = performance.now();
    btnPausa.innerHTML = ICON.pausa;
    root.classList.remove("paused");
  }
  function proximo() { idx < SEQ.length - 1 ? mostrar(idx + 1) : fechar(); }
  function anterior() {
    if (video && video.currentTime > 2 && idx === 0) { video.currentTime = 0; return; }
    idx > 0 ? mostrar(idx - 1) : mostrar(0);
  }

  let focoAnterior = null;
  function abrir() {
    if (!root) montar();
    focoAnterior = document.activeElement;
    aberto = true;
    root.classList.add("open");
    document.documentElement.classList.add("sv-lock");
    const primeiroNaoVisto = SEQ.findIndex(s => !vistos.has(s.id));
    mostrar(primeiroNaoVisto >= 0 ? primeiroNaoVisto : 0);
    root.querySelector(".sv-x").focus({ preventScroll: true });
    track("story_abrir", {});
  }
  function fechar() {
    if (!aberto) return;
    aberto = false;
    limpar();
    root.classList.remove("open", "paused");
    document.documentElement.classList.remove("sv-lock");
    if (focoAnterior && focoAnterior.focus) focoAnterior.focus({ preventScroll: true });
  }
  window.RB.abrirStories = abrir;
})();
