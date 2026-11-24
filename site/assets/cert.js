/* Página de cada certificação: caixa do simulado (com cupom) e selos nos cards relacionados. */
(() => {
  "use strict";
  const { $, $$, esc, fmt, simFor, simSoon, couponActive, courseUrl, couponChip, totalQ, daysLeft, track } = window.RB;
  const S = window.SITE;
  const id = document.querySelector("main[data-cert]").dataset.cert;
  const code = id.toUpperCase();
  const box = $("#simBox");
  const s = simFor(id), soon = simSoon(id);

  if (s) {
    const active = couponActive(s);
    const rating = s.nota && s.avaliacoes ? `<span>⭐ <b>${s.nota.toFixed(1).replace(".", ",")}</b> (${s.avaliacoes} avaliações)</span>` : "";
    box.innerHTML = `
      <span class="badge-hot"><i></i>${active ? "Simulado com cupom" : "Simulado disponível"}</span>
      <h2>Simulado ${esc(code)} na Udemy</h2>
      <div class="meta"><span><b>${fmt(totalQ(s))}</b> questões com explicação</span>${rating}</div>
      ${active && s.cupom.preco ? `<div class="price"><s>${esc(S.precoOriginal)}</s><strong>${esc(s.cupom.preco)}</strong></div>` : ""}
      ${active ? couponChip(s) + `<span class="expiry ok">${esc(daysLeft(s))}</span>` + (s.cupom.nota ? `<span class="coupon-note">${esc(s.cupom.nota)}</span>` : "") : ""}
      <div class="vols">${s.cursos.map((c, i) => `<a class="vol ${i === 0 ? "main" : ""}" href="${esc(courseUrl(s, c))}" target="_blank" rel="noopener" data-go="${esc(s.id)}" data-curso="${esc(c.rotulo)}"><span>${esc(c.rotulo)}</span><small>${fmt(c.questoes)} questões ↗</small></a>`).join("")}</div>`;
  } else {
    box.innerHTML = `
      <span class="badge-hot soft"><i></i>${soon ? "Em breve na Udemy" : "Simulado sob demanda"}</span>
      <h2>${soon ? `Simulado ${esc(code)} chegando` : `Quer um simulado ${esc(code)}?`}</h2>
      <p class="muted">${soon ? "Entre na lista e receba o cupom de estreia no dia do lançamento." : "Os próximos simulados saem de acordo com a procura. Deixe seu contato e eu aviso quando lançar, com cupom de estreia."}</p>
      <a class="btn btn-primary btn-block" href="#alerta" data-notify="${esc(code)}">🔔 ${soon ? "Avise-me no lançamento" : "Quero este simulado"}</a>
      <a class="btn btn-ghost btn-block" href="/">Ver simulados disponíveis</a>`;
  }
  track("ver_certificacao", { exame: code });

  // Selos nos cards relacionados
  $$(".ccard").forEach(a => {
    const slot = $(".sim-slot", a); if (!slot) return;
    const x = simFor(a.dataset.cert);
    if (x) slot.outerHTML = `<span class="tag new">✓ Simulado</span>`;
    else if (simSoon(a.dataset.cert)) slot.outerHTML = `<span class="tag soon">Em breve</span>`;
    else slot.remove();
  });

  // Destaque do item do índice conforme a rolagem
  const links = $$(".toc a");
  const io = new IntersectionObserver((ents) => ents.forEach(en => {
    if (en.isIntersecting) links.forEach(l => l.classList.toggle("on", l.getAttribute("href") === "#" + en.target.id));
  }), { rootMargin: "-30% 0px -60% 0px" });
  $$(".cert-body section[id]").forEach(s => io.observe(s));

  // Barras de peso animadas
  const bars = new IntersectionObserver((ents) => ents.forEach(en => { if (en.isIntersecting) { en.target.classList.add("fill"); bars.unobserve(en.target); } }), { threshold: .4 });
  $$(".bar").forEach(b => bars.observe(b));
})();
