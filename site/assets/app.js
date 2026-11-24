/* Página inicial (link na bio): oferta, simulados, depoimentos e contadores. */
(() => {
  "use strict";
  const S = window.SITE, LIST = window.SIMULADOS, REVIEWS = window.DEPOIMENTOS || [];
  const { $, $$, esc, fmt, couponActive, courseUrl, couponChip, totalQ, daysLeft, deadline, byId, track, toast, reduced, params } = window.RB;

  /* ---------------- Cards ---------------- */
  function card(s) {
    const isAws = s.trilha === "aws";
    const guia = isAws ? "" : `<a class="guide-link" href="/certificacoes/${esc(s.id)}/">Ver o guia da ${esc(s.codigo)} →</a>`;
    const barra = isAws ? "" : `<div class="ig ig-card" data-social="${esc(s.id)}" data-nome="${esc(s.nome)}"></div>`;
    if (s.status !== "disponivel") {
      return `<article class="card soon ${isAws ? "aws" : ""} reveal" id="${esc(s.id)}" data-tilt>
        <div class="card-top"><span class="code">${esc(s.codigo)}</span><span class="tag soon">Em breve na Udemy</span></div>
        <div><h3>${esc(s.nome)}</h3><p class="desc">${esc(s.resumo)}</p></div>
        <div class="tags"><span class="tag">${esc(s.nivel)}</span></div>
        ${guia}
        <div class="vols"><a class="vol main" href="#alerta" data-notify="${esc(s.codigo)}">🔔 Avise-me no lançamento <small>cupom de estreia</small></a></div>
        ${barra}
      </article>`;
    }
    const active = couponActive(s);
    const tags = [
      s.maisVendido ? `<span class="tag hot">🔥 Mais vendido</span>` : "",
      s.novo ? `<span class="tag new">Novo</span>` : "",
      `<span class="tag">${esc(s.nivel)}</span>`,
      s.cursos.length > 1 ? `<span class="tag">${s.cursos.length} cursos</span>` : ""
    ].join("");
    const rating = s.nota && s.avaliacoes ? `<span>⭐ <b>${s.nota.toFixed(1).replace(".", ",")}</b> (${s.avaliacoes})</span>` : "";
    const price = active && s.cupom.preco ? `<div class="price"><s>${esc(S.precoOriginal)}</s><strong>${esc(s.cupom.preco)}</strong></div>` : "";
    const vols = s.cursos.map((c, i) => `
      <a class="vol ${i === 0 ? "main" : ""}" href="${esc(courseUrl(s, c))}" target="_blank" rel="noopener" data-go="${esc(s.id)}" data-curso="${esc(c.rotulo)}">
        <span>${esc(c.rotulo)}</span><small>${fmt(c.questoes)} questões ↗</small>
      </a>`).join("");
    return `<article class="card ${isAws ? "aws" : ""} reveal" id="${esc(s.id)}" data-tilt>
      <div class="card-top"><span class="code">${esc(s.codigo)}</span></div>
      <div><h3>${esc(s.nome)}</h3><p class="desc">${esc(s.resumo)}</p></div>
      <div class="tags">${tags}</div>
      <div class="meta"><span><b>${fmt(totalQ(s))}</b> questões</span>${rating}</div>
      ${price}
      ${active ? couponChip(s) + `<span class="expiry ok">${esc(daysLeft(s))}</span>` + (s.cupom.nota ? `<span class="coupon-note">${esc(s.cupom.nota)}</span>` : "") : ""}
      ${guia}
      <div class="vols">${vols}</div>
      ${barra}
    </article>`;
  }
  ["microsoft", "aws"].forEach(t => {
    const el = $("#cards-" + t); if (el) el.innerHTML = LIST.filter(s => s.trilha === t).map(card).join("");
  });

  /* ---------------- Oferta da semana ---------------- */
  (function offer() {
    const s = byId[S.ofertaDaSemana] || LIST.find(couponActive);
    const box = $("#offer");
    if (!box) return;
    if (!s || s.status !== "disponivel") { $("#cupons").remove(); return; }
    const active = couponActive(s);
    const main = s.cursos[0];
    const gratis = active && /gr[aá]tis/i.test(s.cupom.preco || "");
    box.innerHTML = `
      <div>
        <span class="badge-hot"><i></i>${gratis ? "Grátis por tempo limitado" : active ? "Oferta da semana" : "Destaque"}</span>
        <div style="margin-top:18px" class="code-big">${esc(s.codigo)}</div>
        <h2>${esc(s.nome)}</h2>
        <p style="color:var(--ink2)">${fmt(totalQ(s))} questões com explicação de cada alternativa${s.nota && s.avaliacoes ? ` · ⭐ ${s.nota.toFixed(1).replace(".", ",")} com ${s.avaliacoes} avaliações` : ""}.</p>
        ${active && s.cupom.preco ? `<div class="price"><s>${esc(S.precoOriginal)}</s><strong>${esc(s.cupom.preco)}</strong></div>` : ""}
      </div>
      <div class="offer-side">
        ${active && deadline(s) ? `<div class="countdown" id="cd" aria-label="Tempo restante do cupom">
          <div><b data-u="d">0</b><small>dias</small></div><div><b data-u="h">0</b><small>horas</small></div>
          <div><b data-u="m">0</b><small>min</small></div><div><b data-u="s">0</b><small>seg</small></div></div>` : ""}
        ${active ? couponChip(s) : ""}
        ${active && s.cupom.nota ? `<p class="coupon-note" style="margin:-4px 0 12px;text-align:center">${esc(s.cupom.nota)}</p>` : ""}
        <a class="btn btn-primary btn-block magnetic" href="${esc(courseUrl(s, main))}" target="_blank" rel="noopener" data-go="${esc(s.id)}" data-curso="oferta">
          ${gratis ? "Garantir grátis na Udemy" : active ? "Garantir com desconto na Udemy" : "Ver na Udemy"} ↗</a>
        <p class="small">${active ? "O cupom já vai aplicado no link." : "Entre na lista e receba o próximo cupom."}</p>
      </div>`;
    const cd = $("#cd");
    if (cd) {
      const end = deadline(s);
      const tick = () => {
        const ms = Math.max(0, end - new Date());
        const u = { d: Math.floor(ms / 864e5), h: Math.floor(ms / 36e5) % 24, m: Math.floor(ms / 6e4) % 60, s: Math.floor(ms / 1e3) % 60 };
        $$("[data-u]", cd).forEach(b => b.textContent = String(u[b.dataset.u]).padStart(2, "0"));
        if (ms <= 0) { clearInterval(timer); location.reload(); }
      };
      tick(); const timer = setInterval(tick, 1000);
    }
  })();

  /* ---------------- Marquee ---------------- */
  const mq = LIST.map(s => `<span><i class="dot ${s.trilha === "aws" ? "aws" : "ms"}"></i><b>${esc(s.codigo)}</b> ${esc(s.nome)}</span>`).join("");
  const mqEl = $("#marquee"); if (mqEl) mqEl.innerHTML = mq + mq;

  /* ---------------- Interesses do formulário ---------------- */
  const pills = $("#interesses");
  if (pills) pills.innerHTML = LIST.map(s =>
    `<label class="pill ${s.trilha === "aws" ? "aws" : ""}"><input type="checkbox" name="interesses" value="${esc(s.codigo)}"><span>${esc(s.codigo)}</span></label>`).join("")
    + `<a class="pill more" href="/certificacoes/#alerta"><span>Outra certificação →</span></a>`;

  /* ---------------- Depoimentos ---------------- */
  const rv = $("#reviews");
  if (rv) {
    const NUM = window.NUMEROS_UDEMY || [];
    const review = (r) => `<article class="review">
      <div class="stars" aria-label="${r.nota} de 5 estrelas">${"★".repeat(Math.round(r.nota))}</div>
      <blockquote>“${esc(r.texto)}”</blockquote>
      <footer><span class="ini">${esc(r.nome.split(/[\s.]+/).filter(Boolean).map(p => p[0]).slice(0, 2).join(""))}</span>
        <div>${esc(r.nome)}<small>Aluno · ${esc(r.exame)}${r.data ? " · " + esc(r.data) : ""}</small></div></footer></article>`;
    const numero = (n) => `<article class="review num"><b>${esc(n.grande)}</b><span>${esc(n.texto)}</span><small>${esc(n.pequeno)}</small></article>`;
    // Linha 1: depoimentos; linha 2: depoimentos em outra ordem intercalados com números reais
    const l1 = REVIEWS.map(review);
    const rev2 = [...REVIEWS].reverse();
    const l2 = []; rev2.forEach((r, i) => { l2.push(review(r)); if (NUM[i]) l2.push(numero(NUM[i])); });
    NUM.slice(rev2.length).forEach(n => l2.push(numero(n)));
    const fill = (arr) => { let out = [...arr]; while (out.length < 8) out = out.concat(arr); return out.join(""); };
    rv.innerHTML = `<div class="rv-row"><div class="rv-track">${fill(l1)}${fill(l1)}</div></div>
      <div class="rv-row rev"><div class="rv-track">${fill(l2)}${fill(l2)}</div></div>
      <p class="rv-note">Todas as avaliações escritas com 4★ ou mais dos simulados Microsoft na Udemy, com o nome abreviado.</p>`;
    if (!REVIEWS.length) $("#depoimentos").remove();
  }

  /* ---------------- Sobre ---------------- */
  if (S.foto) ["#avatar", "#avatar2"].forEach(id => { const el = $(id); if (el) el.innerHTML = `<img src="${esc(S.foto)}" alt="Foto de ${esc(S.nome)}">`; });
  const up = $("#udemyProfile"); if (up) up.href = S.udemyPerfil;

  /* ---------------- Contadores ---------------- */
  S.stats.questoes = LIST.filter(s => s.status === "disponivel").reduce((a, s) => a + totalQ(s), 0);
  if (S.mostrarAWS !== false) { const aws = $("#aws"); if (aws) aws.hidden = false; }
  const counted = new IntersectionObserver((ents) => ents.forEach(en => {
    if (!en.isIntersecting) return;
    const el = en.target, end = S.stats[el.dataset.count] || 0, t0 = performance.now(), dur = reduced ? 0 : 1600;
    const f = (t) => { const p = dur ? Math.min(1, (t - t0) / dur) : 1; el.textContent = fmt(Math.round(end * (1 - Math.pow(1 - p, 4)))); if (p < 1) requestAnimationFrame(f); };
    requestAnimationFrame(f); counted.unobserve(el);
  }), { threshold: .5 });
  $$("[data-count]").forEach(el => counted.observe(el));
  const dock = $("#dock a"); if (dock && !$("#cupons")) dock.setAttribute("href", "#microsoft");

  /* ---------------- Rotas (/clf-c02, /cupons, /obrigado...) ---------------- */
  function focusCard(id) {
    const el = document.getElementById(id); if (!el) return;
    el.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
    el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash");
  }
  window.RB.focusCard = focusCard;
  function route() {
    const h = (params.get("ver") || location.hash.slice(1) || "").toLowerCase();
    if (!h) return;
    if (byId[h]) { track("rota_exame", { exame: h }); setTimeout(() => focusCard(h), 350); }
    else if (h === "obrigado") toast("Você está na lista! Fique de olho nos próximos cupons. 🎉");
    else if (document.getElementById(h)) setTimeout(() => document.getElementById(h).scrollIntoView({ behavior: "smooth" }), 200);
  }
  route();
  addEventListener("hashchange", () => { const h = location.hash.slice(1); if (byId[h]) focusCard(h); });
})();
