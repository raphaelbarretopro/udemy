/* Funções compartilhadas por todas as páginas: medição, cupons, formulário, efeitos. */
(() => {
  "use strict";
  const S = window.SITE;
  /* AWS escondida: tira simulados e depoimentos AWS de todas as páginas */
  if (S.mostrarAWS === false) {
    window.SIMULADOS = (window.SIMULADOS || []).filter(s => s.trilha !== "aws");
    window.DEPOIMENTOS = (window.DEPOIMENTOS || []).filter(d => d.trilha !== "aws");
  }
  const LIST = window.SIMULADOS || [];
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = (v) => String(v ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fine = matchMedia("(hover:hover) and (pointer:fine)").matches;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const params = new URLSearchParams(location.search);
  const fmt = (n) => Number(n).toLocaleString("pt-BR");

  /* ---------- Medição (GA4 / Meta Pixel opcionais) ---------- */
  if (S.ga4) {
    const s = document.createElement("script");
    s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(S.ga4);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date()); gtag("config", S.ga4);
  }
  if (S.metaPixel) {
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments) }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s) }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    fbq("init", S.metaPixel); fbq("track", "PageView");
  }
  const track = (name, data = {}) => {
    try { window.gtag && gtag("event", name, data); } catch (e) {}
    try { window.fbq && fbq("trackCustom", name, data); } catch (e) {}
  };

  /* ---------- Cupons ---------- */
  if (S.modoDemo) {
    const bar = $("#demoBar"); if (bar) bar.hidden = false;
    const fim = new Date(Date.now() + 3 * 864e5 + 5 * 36e5).toISOString().slice(0, 10);
    LIST.forEach(s => { if (s.cupom && !s.cupom.codigo) { s.cupom.codigo = "EXEMPLO-" + s.codigo.replace("-", ""); s.cupom.validade = fim; } });
  }
  const byId = Object.fromEntries(LIST.map(s => [s.id, s]));
  /* validade: "AAAA-MM-DD" (vale até 23:59 do dia) ou data e hora exatas, ex.: "2026-11-28T21:21:00-03:00" */
  const deadline = (s) => {
    const v = s.cupom && s.cupom.validade; if (!v) return null;
    return new Date(v.includes("T") ? v : v + "T23:59:59");
  };
  const couponActive = (s) => !!(s && s.cupom && s.cupom.codigo && (!deadline(s) || deadline(s) > new Date()));
  const courseUrl = (s, c) => {
    // Se o curso tiver "cupom" próprio (mesmo vazio), ele vale; senão usa o cupom do simulado
    const code = (c && "cupom" in c) ? c.cupom : (couponActive(s) ? s.cupom.codigo : "");
    return code ? `${c.url}?couponCode=${encodeURIComponent(code)}` : c.url;
  };
  const totalQ = (s) => s.cursos.reduce((a, c) => a + (c.questoes || 0), 0);
  const daysLeft = (s) => {
    const d = deadline(s); if (!d) return "";
    const ms = d - new Date(); if (ms <= 0) return "";
    const days = Math.floor(ms / 864e5);
    return days >= 1 ? `Cupom válido por mais ${days} dia${days > 1 ? "s" : ""}` : "Cupom termina hoje";
  };
  const couponChip = (s) => `
    <button class="coupon" type="button" data-copy="${esc(s.cupom.codigo)}" data-exam="${esc(s.id)}" aria-label="Copiar cupom ${esc(s.cupom.codigo)}">
      <span>${esc(s.cupom.codigo)}</span><span class="copy">Copiar</span>
    </button>`;
  /* Simulado disponível na Udemy para um código de certificação? */
  const simFor = (id) => { const s = byId[String(id).toLowerCase()]; return s && s.status === "disponivel" ? s : null; };
  const simSoon = (id) => { const s = byId[String(id).toLowerCase()]; return s && s.status === "em-breve" ? s : null; };

  /* ---------- Toast e cópia ---------- */
  const toast = (msg) => {
    const t = $("#toast"); if (!t) return;
    t.textContent = msg; t.classList.add("show");
    clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove("show"), 2600);
  };
  async function copy(text) {
    try { await navigator.clipboard.writeText(text); return true; }
    catch (e) {
      const ta = document.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select(); const ok = document.execCommand("copy"); ta.remove(); return ok;
    }
  }
  document.addEventListener("click", async (e) => {
    const c = e.target.closest("[data-copy]");
    if (c) {
      const ok = await copy(c.dataset.copy);
      $$(`[data-copy="${CSS.escape(c.dataset.copy)}"]`).forEach(el => { el.classList.add("copied"); $(".copy", el).textContent = "Copiado ✓"; });
      setTimeout(() => $$(".coupon.copied").forEach(el => { el.classList.remove("copied"); $(".copy", el).textContent = "Copiar"; }), 2500);
      toast(ok ? `Cupom ${c.dataset.copy} copiado! Ele também já vai aplicado no link.` : `Cupom: ${c.dataset.copy}`);
      track("copiar_cupom", { exame: c.dataset.exam });
      return;
    }
    const go = e.target.closest("[data-go]");
    if (go) track("abrir_udemy", { exame: go.dataset.go, curso: go.dataset.curso });
    const n = e.target.closest("[data-notify]");
    if (n) { e.preventDefault(); notifyFor(n.dataset.notify); }
  });

  /* ---------- Formulário de captação (qualquer form[data-lead]) ---------- */
  function notifyFor(code) {
    const C = String(code).toUpperCase();
    const form = $("form[data-lead]"); if (!form) { location.href = `/certificacoes/${String(code).toLowerCase()}/#alerta`; return; }
    const cb = $(`input[name="interesses"][value="${CSS.escape(C)}"]`, form);
    if (cb && cb.type === "checkbox") cb.checked = true;
    const sel = $('select[name="interesses"]', form); if (sel) sel.value = C;
    $("#alerta").scrollIntoView({ behavior: reduced ? "auto" : "smooth" });
    setTimeout(() => $('[name="nome"]', form).focus({ preventScroll: true }), 700);
    track("avise_me", { exame: C });
  }
  $$("form[data-lead]").forEach(f => f.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = $(".form-msg", f);
    if (f.site && f.site.value) return; // robô
    const nome = f.nome.value.trim(), contato = f.contato.value.trim();
    const email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contato);
    const fone = contato.replace(/\D/g, "").length >= 10;
    f.nome.classList.toggle("err", !nome);
    f.contato.classList.toggle("err", !(email || fone));
    msg.className = "form-msg bad";
    if (!nome || !(email || fone)) { msg.textContent = "Preencha seu nome e um WhatsApp (com DDD) ou e-mail válido."; return; }
    if (!f.consent.checked) { msg.textContent = "Marque a autorização para receber os cupons."; return; }
    const interesses = $$('[name="interesses"]', f).filter(i => (i.type === "checkbox" ? i.checked : i.value)).map(i => i.value).join(", ");
    const data = new URLSearchParams({
      nome, contato, tipo: email ? "email" : "whatsapp", interesses,
      origem: params.get("utm_source") || document.referrer || "direto",
      campanha: params.get("utm_campaign") || "", pagina: location.pathname + location.hash,
      data: new Date().toISOString()
    });
    const btn = $("button[type=submit]", f), label = btn.textContent;
    btn.disabled = true; btn.textContent = "Enviando…";
    const SB = window.SOCIAL || {};
    try {
      if (SB.supabaseUrl && SB.chavePublica) {
        /* Grava no Supabase (tabela "inscritos", via função "inscrever") */
        let disp = localStorage.getItem("rb_disp");
        if (!/^[0-9a-f-]{36}$/i.test(disp || "") && crypto.randomUUID) { disp = crypto.randomUUID(); localStorage.setItem("rb_disp", disp); }
        const r = await fetch(`${SB.supabaseUrl.replace(/\/$/, "")}/rest/v1/rpc/inscrever`, {
          method: "POST",
          headers: { apikey: SB.chavePublica, "Content-Type": "application/json" },
          body: JSON.stringify({
            p_nome: nome, p_contato: contato, p_tipo: email ? "email" : "whatsapp", p_interesses: interesses,
            p_origem: data.get("origem"), p_campanha: data.get("campanha"), p_pagina: data.get("pagina"),
            p_dispositivo: /^[0-9a-f-]{36}$/i.test(disp || "") ? disp : null
          })
        });
        if (!r.ok) throw new Error(await r.text());
      }
      else if (S.formEndpoint) await fetch(S.formEndpoint, { method: "POST", mode: "no-cors", body: data });
      else if (!S.modoDemo) throw new Error("sem endpoint");
      msg.className = "form-msg ok";
      msg.textContent = `Pronto, ${nome.split(" ")[0]}! Você vai receber os próximos cupons antes de todo mundo.`;
      f.reset(); track("lead", { interesses });
      try { window.fbq && fbq("track", "Lead"); } catch (e2) {}
    } catch (err) {
      msg.textContent = "Não foi possível enviar agora. Tente novamente em instantes.";
    } finally { btn.disabled = false; btn.textContent = label; }
  }));

  /* ---------- Rodapé ---------- */
  const ano = $("#ano"); if (ano) ano.textContent = new Date().getFullYear();
  const ICONS = {
    instagram: '<path d="M12 7.3A4.7 4.7 0 1 0 16.7 12 4.7 4.7 0 0 0 12 7.3Zm0 7.7a3 3 0 1 1 3-3 3 3 0 0 1-3 3Zm6-7.9a1.1 1.1 0 1 1-1.1-1.1A1.1 1.1 0 0 1 18 7.1ZM21.9 8.2a5.4 5.4 0 0 0-1.5-3.9 5.5 5.5 0 0 0-3.9-1.5c-1.5-.1-6-.1-7.6 0a5.5 5.5 0 0 0-3.9 1.5 5.5 5.5 0 0 0-1.5 3.9c-.1 1.5-.1 6 0 7.6a5.4 5.4 0 0 0 1.5 3.9 5.5 5.5 0 0 0 3.9 1.5c1.5.1 6 .1 7.6 0a5.4 5.4 0 0 0 3.9-1.5 5.5 5.5 0 0 0 1.5-3.9c.1-1.6.1-6.1 0-7.6Zm-2 9.3a3 3 0 0 1-1.7 1.7c-1.2.5-4 .4-5.2.4s-4.1.1-5.2-.4a3 3 0 0 1-1.7-1.7c-.5-1.2-.4-4-.4-5.2s-.1-4.1.4-5.2a3 3 0 0 1 1.7-1.7c1.2-.5 4-.4 5.2-.4s4.1-.1 5.2.4a3 3 0 0 1 1.7 1.7c.5 1.2.4 4 .4 5.2s.1 4.1-.4 5.2Z"/>',
    linkedin: '<path d="M6.9 21H2.6V8.9h4.3ZM4.8 7.1a2.5 2.5 0 1 1 2.5-2.5 2.5 2.5 0 0 1-2.5 2.5ZM21.4 21h-4.3v-5.9c0-1.4 0-3.2-2-3.2s-2.2 1.5-2.2 3.1v6H8.6V8.9h4.1v1.7h.1a4.5 4.5 0 0 1 4-2.2c4.3 0 5.1 2.8 5.1 6.5Z"/>',
    udemy: '<path d="M12 2 3.5 6.9V10L12 5.1l8.5 4.9V6.9ZM5.3 11.5v4.3c0 3.5 3 6.2 6.7 6.2s6.7-2.7 6.7-6.2v-4.3h-3v4.2a3.7 3.7 0 0 1-7.4 0v-4.2Z"/>'
  };
  const social = $("#social");
  if (social) social.innerHTML = [["instagram", S.instagram, "Instagram"], ["linkedin", S.linkedin, "LinkedIn"], ["udemy", S.udemyPerfil, "Udemy"]]
    .filter(([, u]) => u).map(([k, u, l]) => `<a href="${esc(u)}" target="_blank" rel="noopener" aria-label="${l}"><svg viewBox="0 0 24 24" aria-hidden="true">${ICONS[k]}</svg></a>`).join("");

  /* ---------- Efeitos ---------- */
  const io = new IntersectionObserver((ents) => ents.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
  }), { threshold: .08, rootMargin: "0px 0px -40px 0px" });
  const observeReveal = (root = document) => $$(".reveal:not(.in)", root).forEach((el, i) => { el.style.transitionDelay = (i % 3) * 70 + "ms"; io.observe(el); });

  function attachTilt(root = document) {
    if (!fine || reduced) return;
    $$("[data-tilt]:not([data-tilt-on])", root).forEach(c => {
      c.dataset.tiltOn = "1";
      c.addEventListener("pointermove", (e) => {
        const r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        c.style.setProperty("--x", x * 100 + "%"); c.style.setProperty("--y", y * 100 + "%");
        c.style.transform = `perspective(900px) rotateX(${(.5 - y) * 7}deg) rotateY(${(x - .5) * 7}deg) translateY(-4px)`;
      });
      c.addEventListener("pointerleave", () => { c.style.transform = ""; });
    });
    $$(".ccard:not([data-glow])", root).forEach(c => {
      c.dataset.glow = "1";
      c.addEventListener("pointermove", (e) => {
        const r = c.getBoundingClientRect();
        c.style.setProperty("--x", (e.clientX - r.left) + "px"); c.style.setProperty("--y", (e.clientY - r.top) + "px");
      });
    });
  }
  if (fine && !reduced) {
    const bg = $(".bg");
    addEventListener("pointermove", (e) => { bg.style.setProperty("--mx", e.clientX + "px"); bg.style.setProperty("--my", e.clientY + "px"); }, { passive: true });
    $$(".magnetic").forEach(b => {
      b.addEventListener("pointermove", (e) => {
        const r = b.getBoundingClientRect();
        b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * .15}px,${(e.clientY - r.top - r.height / 2) * .25}px)`;
      });
      b.addEventListener("pointerleave", () => { b.style.transform = ""; });
    });
  }

  // Barra fixa no celular: aparece depois do topo, some no formulário
  const dock = $("#dock"), topo = $(".hero") || $(".cert-hero");
  if (dock && topo) {
    let heroOut = false, formIn = false;
    const upd = () => dock.classList.toggle("show", heroOut && !formIn);
    new IntersectionObserver(([en]) => { heroOut = !en.isIntersecting; upd(); }).observe(topo);
    const al = $("#alerta"); if (al) new IntersectionObserver(([en]) => { formIn = en.isIntersecting; upd(); }, { threshold: .1 }).observe(al);
  }

  window.RB = { $, $$, esc, fmt, track, toast, byId, couponActive, courseUrl, couponChip, totalQ, daysLeft, deadline, simFor, simSoon, notifyFor, observeReveal, attachTilt, reduced, params };
  // Inicializa depois que os scripts específicos da página rodarem
  addEventListener("DOMContentLoaded", () => { observeReveal(); attachTilt(); });
  if (document.readyState !== "loading") setTimeout(() => { observeReveal(); attachTilt(); });
})();
