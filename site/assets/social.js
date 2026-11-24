/* =====================================================================
   INTERAÇÕES no estilo Instagram: curtir, comentar, recomendar no LinkedIn,
   compartilhar e salvar em "Minhas metas".
   - Compartilhar e salvar funcionam sempre (não precisam de servidor).
   - Curtidas e comentários usam o Supabase configurado em window.SOCIAL
     (dados.js). Sem configuração, esses dois botões ficam escondidos.
   ===================================================================== */
(() => {
  "use strict";
  const { $, $$, esc, toast, track } = window.RB;
  const CFG = window.SOCIAL || {};
  const ON = !!(CFG.supabaseUrl && CFG.chavePublica);
  const S = window.SITE || {};

  /* ---------- armazenamento local ---------- */
  const ler = (k, d) => { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch (e) { return d; } };
  const gravar = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const uuid = () => (crypto.randomUUID ? crypto.randomUUID() :
    "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c => (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)));
  let DISP = ler("rb_disp", null); if (!DISP) { DISP = uuid(); gravar("rb_disp", DISP); }
  const curtidas = new Set(ler("rb_curtidas", []));
  const metas = new Set(ler("rb_metas", []));

  /* ---------- servidor ---------- */
  async function rpc(fn, body) {
    const r = await fetch(`${CFG.supabaseUrl.replace(/\/$/, "")}/rest/v1/rpc/${fn}`, {
      method: "POST", headers: { apikey: CFG.chavePublica, "Content-Type": "application/json" }, body: JSON.stringify(body || {})
    });
    const t = await r.text();
    if (!r.ok) { let m = t; try { m = JSON.parse(t).message || t; } catch (e) {} throw new Error(m); }
    return t ? JSON.parse(t) : null;
  }

  /* ---------- números no formato do Instagram: 1,1 mil ---------- */
  const NF = new Intl.NumberFormat("pt-BR", { notation: "compact", maximumFractionDigits: 1 });
  const num = (n) => n > 0 ? NF.format(n) : "";
  const CONT = {};
  const cont = (id) => CONT[id] || (CONT[id] = { curtidas: 0, comentarios: 0, reposts: 0, compart: 0 });

  /* ---------- ícones ---------- */
  const svg = (p, extra = "") => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" ${extra}>${p}</svg>`;
  const I = {
    heart: svg('<path d="M12 20.6s-7.6-4.5-9.4-9.3C1.3 7.9 3.5 4.4 7 4.4c2 0 3.7 1.1 5 3 1.3-1.9 3-3 5-3 3.5 0 5.7 3.5 4.4 6.9-1.8 4.8-9.4 9.3-9.4 9.3z"/>'),
    com: svg('<path d="M20.7 16.6a9 9 0 1 0-3.5 3.6l4.3 1.3z"/>'),
    rep: svg('<path d="M17 2.8l3.5 3.5L17 9.8"/><path d="M3.5 11.6v-1.3a4 4 0 0 1 4-4h13"/><path d="M7 21.2l-3.5-3.5L7 14.2"/><path d="M20.5 12.4v1.3a4 4 0 0 1-4 4h-13"/>'),
    plane: svg('<path d="M21.5 2.5L10.2 13.8"/><path d="M21.5 2.5l-6.6 19-4.7-7.7-7.7-4.7z"/>'),
    save: svg('<path d="M19 21l-7-5.2L5 21V4.6A1.6 1.6 0 0 1 6.6 3h10.8A1.6 1.6 0 0 1 19 4.6z"/>'),
    x: svg('<path d="M18 6L6 18M6 6l12 12"/>'),
    link: svg('<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>'),
    mail: svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5L12 13l8.5-6.5"/>'),
    mais: svg('<circle cx="5" cy="12" r="1.3"/><circle cx="12" cy="12" r="1.3"/><circle cx="19" cy="12" r="1.3"/>')
  };

  /* =====================================================================
     BARRAS: na página da certificação e nos cards de simulado da página inicial.
     Cada barra é um elemento [data-social]. Na página da certificação ele vem
     vazio (os dados saem da própria página); nos cards vem com o id do exame.
     ===================================================================== */
  const DOMINIO = "https://raphaelbarreto.com.br";
  const main = $("main.cert-page[data-cert]");
  const ID = main ? main.dataset.cert : null;  // página da certificação (se for)
  const SELOS = {};
  if (window.RB.loadCerts) window.RB.loadCerts().then(d => d.certificacoes.forEach(c => { SELOS[c.id] = c.selo; })).catch(() => {});

  function ctxDe(el) {
    const id = el.dataset.social || ID;
    const naPagina = id === ID && !!main;
    return {
      id, code: id.toUpperCase(), naPagina,
      nome: el.dataset.nome || (naPagina ? ($(".cert-hero h1") || {}).textContent || "" : ""),
      url: `${DOMINIO}/certificacoes/${id}/`,
      selo: () => (naPagina && ($(".selo-hero img") || {}).src) || SELOS[id] || ""
    };
  }
  const linkCom = (x, canal) => `${x.url}?utm_source=${canal}&utm_medium=social&utm_campaign=compartilhar`;
  const texto = (x) => `${x.code}${x.nome ? ` (${x.nome})` : ""}: guia em português com o que cai na prova, rota de estudo e simulado.`;

  const BARRAS = [];
  function pintar() {
    BARRAS.forEach(({ el, x }) => {
      const c = cont(x.id);
      $$("[data-n]", el).forEach(n => { n.textContent = num(c[n.dataset.n]); });
      const lk = $(".ig-like", el), sv = $(".ig-save", el), on = curtidas.has(x.id);
      lk.classList.toggle("on", on); lk.setAttribute("aria-pressed", on); lk.setAttribute("aria-label", on ? `Descurtir ${x.code}` : `Curtir ${x.code}`);
      sv.classList.toggle("on", metas.has(x.id)); sv.setAttribute("aria-pressed", metas.has(x.id));
    });
    const tot = $(".cm-total"); if (tot && ID) { const c = cont(ID); tot.textContent = c.comentarios ? `(${num(c.comentarios)})` : ""; }
  }

  function montarBarra(el) {
    const x = ctxDe(el);
    el.innerHTML = `
      <div class="ig-row" role="group" aria-label="Interações ${esc(x.code)}">
        <button class="ig-b ig-like" type="button" ${ON ? "" : "hidden"}>${I.heart}<span class="ig-n" data-n="curtidas"></span></button>
        <a class="ig-b ig-com" href="${x.naPagina ? "#comentarios" : `/certificacoes/${esc(x.id)}/#comentarios`}" aria-label="Comentários ${esc(x.code)}" ${ON ? "" : "hidden"}>${I.com}<span class="ig-n" data-n="comentarios"></span></a>
        <button class="ig-b ig-rep" type="button" aria-label="Recomendar ${esc(x.code)} no LinkedIn" data-dica="Recomendar no LinkedIn">${I.rep}<span class="ig-n" data-n="reposts"></span></button>
        <button class="ig-b ig-share" type="button" aria-label="Compartilhar ${esc(x.code)}" data-dica="Compartilhar">${I.plane}<span class="ig-n" data-n="compart"></span></button>
        <span class="ig-sp"></span>
        <button class="ig-b ig-save" type="button" aria-label="Salvar ${esc(x.code)} em Minhas metas" data-dica="Salvar em Minhas metas">${I.save}</button>
      </div>`;
    $(".ig-like", el).addEventListener("click", () => alternarCurtida(x));
    $(".ig-rep", el).addEventListener("click", () => compartilhar(x, "linkedin"));
    $(".ig-share", el).addEventListener("click", (e) => abrirFolha(x, e.currentTarget));
    $(".ig-save", el).addEventListener("click", () => alternarMeta(x));
    BARRAS.push({ el, x });
  }

  const estourar = (sel, id) => BARRAS.filter(b => b.x.id === id).forEach(({ el }) => {
    const b = $(sel, el); b.classList.remove("pop"); void b.offsetWidth; b.classList.add("pop");
  });

  const enviando = new Set();
  async function alternarCurtida(x, forcarCurtir) {
    const id = x.id;
    if (!ON || enviando.has(id)) return;
    if (forcarCurtir && curtidas.has(id)) return;
    const quer = forcarCurtir ? true : !curtidas.has(id);
    const c = cont(id), antes = c.curtidas, primeira = !ler("rb_ja_curtiu", false);
    quer ? curtidas.add(id) : curtidas.delete(id);
    c.curtidas = Math.max(0, antes + (quer ? 1 : -1));
    gravar("rb_curtidas", [...curtidas]); pintar();
    if (quer) {
      estourar(".ig-like", id);
      if (primeira) { gravar("rb_ja_curtiu", true); setTimeout(() => toast(`❤️ Curtido! Quer cupons e o aviso de lançamento da ${x.code}? Entre na lista no fim da página.`), 500); }
      track("curtir", { exame: x.code });
    }
    enviando.add(id);
    try { c.curtidas = await rpc("curtir", { p_cert: id, p_dispositivo: DISP, p_curtir: quer }); }
    catch (e) {
      quer ? curtidas.delete(id) : curtidas.add(id); c.curtidas = antes; gravar("rb_curtidas", [...curtidas]);
      toast("Não foi possível registrar agora. Tente de novo em instantes.");
    }
    enviando.delete(id); pintar(); pintarCards();
  }

  /* Toque duplo no selo = curtir, com o coração grande do Instagram */
  function curtirNoSelo() {
    const fig = $(".selo-hero"); if (!fig || !ON || !ID) return;
    const x = ctxDe($("[data-social]") || main);
    fig.classList.add("dbl-like");
    const coracao = document.createElement("span"); coracao.className = "big-heart"; coracao.innerHTML = I.heart; fig.appendChild(coracao);
    fig.addEventListener("dblclick", (e) => {
      e.preventDefault();
      coracao.classList.remove("go"); void coracao.offsetWidth; coracao.classList.add("go");
      alternarCurtida(x, true);
    });
    fig.title = "Toque duas vezes para curtir";
  }

  function alternarMeta(x) {
    const add = !metas.has(x.id);
    add ? metas.add(x.id) : metas.delete(x.id); gravar("rb_metas", [...metas]); pintar(); pintarCards();
    if (add) estourar(".ig-save", x.id);
    if (ON) rpc("salvar", { p_cert: x.id, p_dispositivo: DISP, p_salvar: add }).catch(() => {});
    toast(add ? `🔖 ${x.code} salva em Minhas metas. Ative o filtro “Minhas metas” no catálogo para ver todas.` : `${x.code} removida de Minhas metas.`);
    track(add ? "salvar_meta" : "remover_meta", { exame: x.code });
  }

  /* ---------- compartilhar ---------- */
  const CANAIS = [
    { id: "whatsapp", nome: "WhatsApp", cor: "#25d366", ic: '<b class="glyph">' + I.com + "</b>", url: (x, u) => `https://wa.me/?text=${encodeURIComponent(texto(x) + " " + u)}` },
    { id: "linkedin", nome: "LinkedIn", cor: "#0a66c2", ic: '<b class="glyph txt">in</b>', url: (x, u) => `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(u)}` },
    { id: "telegram", nome: "Telegram", cor: "#229ed9", ic: '<b class="glyph">' + I.plane + "</b>", url: (x, u) => `https://t.me/share/url?url=${encodeURIComponent(u)}&text=${encodeURIComponent(texto(x))}` },
    { id: "x", nome: "X", cor: "#111", ic: '<b class="glyph txt">𝕏</b>', url: (x, u) => `https://twitter.com/intent/tweet?text=${encodeURIComponent(texto(x))}&url=${encodeURIComponent(u)}` },
    { id: "facebook", nome: "Facebook", cor: "#1877f2", ic: '<b class="glyph txt">f</b>', url: (x, u) => `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(u)}` },
    { id: "email", nome: "E-mail", cor: "#6b7280", ic: '<b class="glyph">' + I.mail + "</b>", url: (x, u) => `mailto:?subject=${encodeURIComponent("Guia da certificação " + x.code)}&body=${encodeURIComponent(texto(x) + "\n\n" + u)}` }
  ];

  function registrar(x, canal) {
    const c = cont(x.id);
    canal === "linkedin" ? c.reposts++ : c.compart++;
    pintar();
    track("compartilhar", { exame: x.code, canal });
    if (ON) rpc("compartilhar", { p_cert: x.id, p_canal: canal, p_dispositivo: DISP }).catch(() => {});
  }

  function compartilhar(x, canal) {
    const u = CANAIS.find(k => k.id === canal).url(x, linkCom(x, canal));
    if (canal === "email") location.href = u;
    else window.open(u, "_blank", "noopener,width=640,height=640");
    registrar(x, canal);
    fecharFolha();
  }

  let folha, atual, origem;
  function abrirFolha(x, botao) {
    atual = x; origem = botao;
    if (!folha) {
      folha = document.createElement("div");
      folha.className = "sh"; folha.hidden = true;
      folha.setAttribute("role", "dialog"); folha.setAttribute("aria-modal", "true");
      document.body.appendChild(folha);
      folha.addEventListener("click", async (e) => {
        if (e.target === folha || e.target.closest(".sh-x")) return fecharFolha();
        const b = e.target.closest("[data-canal]"); if (!b) return;
        const canal = b.dataset.canal, x = atual;
        if (canal === "link") {
          const u = linkCom(x, "link");
          try { await navigator.clipboard.writeText(u); } catch (er) { const i = $("input", folha); i.value = u; i.select(); document.execCommand("copy"); }
          b.textContent = "Copiado ✓"; setTimeout(() => { b.textContent = "Copiar"; }, 2000);
          toast("Link copiado! Cole no Instagram, no grupo de estudos ou onde quiser.");
          registrar(x, "link");
        } else if (canal === "nativo") {
          try { await navigator.share({ title: `Guia da certificação ${x.code}`, text: texto(x), url: linkCom(x, "nativo") }); registrar(x, "nativo"); fecharFolha(); } catch (er) {}
        } else compartilhar(x, canal);
      });
      document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !folha.hidden) fecharFolha(); });
    }
    const selo = x.selo();
    folha.setAttribute("aria-label", `Compartilhar ${x.code}`);
    folha.innerHTML = `
      <div class="sh-card">
        <span class="sh-grab" aria-hidden="true"></span>
        <header class="sh-head">
          ${selo ? `<img src="${esc(selo)}" alt="" width="44" height="44">` : ""}
          <div><b>Compartilhar ${esc(x.code)}</b><span>${esc(x.nome)}</span></div>
          <button class="sh-x" type="button" aria-label="Fechar">${I.x}</button>
        </header>
        <div class="sh-grid">
          ${CANAIS.map(k => `<button type="button" class="sh-op" data-canal="${k.id}"><span class="sh-ic" style="--c:${k.cor}">${k.ic}</span>${k.nome}</button>`).join("")}
          ${navigator.share ? `<button type="button" class="sh-op" data-canal="nativo"><span class="sh-ic" style="--c:#334155"><b class="glyph">${I.mais}</b></span>Mais opções</button>` : ""}
        </div>
        <div class="sh-link"><span class="sh-lic">${I.link}</span><input type="text" readonly value="${esc(x.url)}" aria-label="Link da página"><button type="button" class="btn btn-sm btn-primary" data-canal="link">Copiar</button></div>
      </div>`;
    folha.classList.remove("open");
    folha.hidden = false; document.documentElement.classList.add("sh-lock");
    requestAnimationFrame(() => requestAnimationFrame(() => folha.classList.add("open")));
    $(".sh-op", folha).focus({ preventScroll: true });
  }
  function fecharFolha() {
    if (!folha || folha.hidden) return;
    folha.classList.remove("open"); document.documentElement.classList.remove("sh-lock");
    setTimeout(() => { folha.hidden = true; }, 250);
    if (origem) origem.focus({ preventScroll: true });
  }

  /* ---------- comentários ---------- */
  const secao = $("[data-comentarios]");
  const CODE = ID ? ID.toUpperCase() : "";
  const meus = () => ler("rb_meus_comentarios", []).filter(x => x.cert === ID);
  const RTF = new Intl.RelativeTimeFormat("pt-BR", { numeric: "auto" });
  function quando(iso) {
    const s = (new Date(iso) - Date.now()) / 1000, a = Math.abs(s);
    if (a < 60) return "agora";
    if (a < 3600) return RTF.format(Math.round(s / 60), "minute");
    if (a < 86400) return RTF.format(Math.round(s / 3600), "hour");
    if (a < 86400 * 30) return RTF.format(Math.round(s / 86400), "day");
    return new Date(iso).toLocaleDateString("pt-BR", { day: "2-digit", month: "short", year: "numeric" });
  }
  const tom = (n) => [...n].reduce((h, ch) => (h * 31 + ch.charCodeAt(0)) % 360, 7);
  const avatar = (n) => `<span class="cm-av" style="--h:${tom(n)}" aria-hidden="true">${esc(n.trim().charAt(0).toUpperCase())}</span>`;
  function item(c, pendente) {
    return `<li class="cm${pendente ? " pend" : ""}">
      ${avatar(c.nome)}
      <div class="cm-c">
        <p class="cm-h"><b>${esc(c.nome)}</b><time datetime="${esc(c.criado)}">${quando(c.criado)}</time></p>
        <p class="cm-t">${esc(c.texto)}</p>
        ${pendente ? '<span class="cm-pend">⏳ Aguardando aprovação. Só você vê por enquanto.</span>' : ""}
        ${c.resposta ? `<div class="cm-rep">${S.foto ? `<img class="cm-av" src="${esc(S.foto)}" alt="">` : avatar("R")}<div><p class="cm-h"><b>Raphael Barreto</b><span class="cm-inst">Instrutor</span></p><p class="cm-t">${esc(c.resposta)}</p></div></div>` : ""}
      </div></li>`;
  }

  let aprovados = [];
  function listar() {
    const ids = new Set(aprovados.map(c => c.id));
    const pend = meus().filter(m => !ids.has(m.id));
    const ul = $(".cm-list", secao);
    ul.innerHTML = aprovados.map(c => item(c, false)).join("") + pend.map(c => item(c, true)).join("") ||
      `<li class="cm-vazio">Seja a primeira pessoa a comentar sobre a ${esc(CODE)}. Já fez a prova? Está estudando? Conte aqui.</li>`;
    // limpa da memória local os que já foram aprovados
    const resto = ler("rb_meus_comentarios", []).filter(m => !(m.cert === ID && ids.has(m.id)));
    gravar("rb_meus_comentarios", resto);
  }

  function montarComentarios() {
    secao.hidden = false;
    const nomeSalvo = ler("rb_nome", "");
    secao.innerHTML = `
      <h2>Comentários <span class="cm-total muted"></span></h2>
      <p class="muted">Já fez a ${esc(CODE)} ou está estudando? Deixe uma dica, conte como foi a prova ou tire uma dúvida.</p>
      <ul class="cm-list" aria-live="polite"><li class="cm-vazio">Carregando comentários…</li></ul>
      <form class="cm-form" novalidate>
        ${avatar(nomeSalvo || "?")}
        <div class="cm-fields">
          <input name="nome" type="text" maxlength="40" required placeholder="Seu nome" autocomplete="given-name" value="${esc(nomeSalvo)}" aria-label="Seu nome">
          <textarea name="texto" maxlength="600" rows="3" required placeholder="Escreva um comentário…" aria-label="Comentário"></textarea>
          <input name="site" class="cm-hp" type="text" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="cm-foot">
            <small class="muted">Os comentários aparecem depois de aprovados. Guardamos só o nome e o texto que você enviar.</small>
            <span class="cm-cont">0/600</span>
            <button class="btn btn-primary btn-sm" type="submit">Publicar</button>
          </div>
        </div>
      </form>`;
    const f = $(".cm-form", secao), ta = f.texto, ini = $(".cm-av", f);
    ta.addEventListener("input", () => { $(".cm-cont", f).textContent = `${ta.value.length}/600`; });
    f.nome.addEventListener("input", () => { ini.textContent = (f.nome.value.trim().charAt(0) || "?").toUpperCase(); ini.style.setProperty("--h", tom(f.nome.value || "?")); });
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (f.site.value) return; // robô
      const nome = f.nome.value.trim(), texto = ta.value.trim();
      if (nome.length < 2) { toast("Escreva seu nome (pelo menos 2 letras)."); return f.nome.focus(); }
      if (texto.length < 2) { toast("Escreva o seu comentário."); return ta.focus(); }
      const bt = $("button[type=submit]", f); bt.disabled = true; bt.textContent = "Enviando…";
      try {
        const id = await rpc("comentar", { p_cert: ID, p_nome: nome, p_texto: texto, p_dispositivo: DISP });
        gravar("rb_nome", nome);
        gravar("rb_meus_comentarios", [...ler("rb_meus_comentarios", []), { id, cert: ID, nome, texto, criado: new Date().toISOString() }]);
        ta.value = ""; $(".cm-cont", f).textContent = "0/600";
        listar();
        toast("💬 Comentário enviado! Ele aparece para todos depois da aprovação.");
        track("comentar", { exame: CODE });
      } catch (er) {
        toast(/limite/.test(er.message) ? "Você comentou várias vezes seguidas. Tente de novo em alguns minutos." : "Não foi possível enviar agora. Tente de novo em instantes.");
      }
      bt.disabled = false; bt.textContent = "Publicar";
    });
    rpc("comentarios_de", { p_cert: ID }).then(l => { aprovados = l || []; listar(); })
      .catch(() => { $(".cm-list", secao).innerHTML = '<li class="cm-vazio">Não foi possível carregar os comentários agora.</li>'; });
  }

  /* =====================================================================
     CARDS (catálogo e relacionadas): contadores pequenos e marca de meta
     ===================================================================== */
  function pintarCards() {
    $$(".ccard[data-cert]").forEach(a => {
      if (a.closest(".ccard-box")) return; // card já tem a barra completa
      const id = a.dataset.cert, c = CONT[id];
      a.classList.toggle("is-meta", metas.has(id));
      let m = $(".ig-mini", a);
      const partes = [];
      if (c && c.curtidas) partes.push(`<span>${I.heart}${num(c.curtidas)}</span>`);
      if (c && c.comentarios) partes.push(`<span>${I.com}${num(c.comentarios)}</span>`);
      if (metas.has(id)) partes.push(`<span class="mt" title="Em Minhas metas">${I.save}</span>`);
      if (!partes.length) { if (m) m.remove(); return; }
      if (!m) { m = document.createElement("span"); m.className = "ig-mini"; ($(".tags", a) || a).appendChild(m); }
      m.innerHTML = partes.join("");
    });
  }

  /* ---------- início ---------- */
  function iniciarBarras(root = document) {
    $$("[data-social]", root).forEach(el => { if (!el.dataset.pronta && (el.dataset.social || ID)) { el.dataset.pronta = "1"; montarBarra(el); } });
    pintar();
  }
  iniciarBarras();
  curtirNoSelo();
  if (secao && ID && ON) montarComentarios();
  pintarCards();
  if (ON) rpc("contagens").then(l => {
    (l || []).forEach(r => { CONT[r.cert] = { curtidas: +r.curtidas, comentarios: +r.comentarios, reposts: +r.reposts, compart: +r.compart }; });
    pintar(); pintarCards();
  }).catch(() => {});

  window.RB.metas = () => [...metas];
  window.RB.iniciarBarras = iniciarBarras;
})();
