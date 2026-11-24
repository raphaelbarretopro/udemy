/* Vitrine 3D: as certificações "penduradas" lado a lado. Ao tocar, a escolhida vem para a frente
   e abre um painel com o resumo. Use <div data-vitrine></div> em qualquer página. */
(() => {
  "use strict";
  const RB = window.RB, { $, $$, esc, simFor, simSoon, couponActive, courseUrl, track } = RB;
  const roots = $$("[data-vitrine]");
  if (!roots.length) return;
  const loader = RB.loadCerts ? RB.loadCerts() : fetch("/assets/certificacoes.json").then(r => r.json());

  loader.then(d => {
    const CS = d.certificacoes, TR = d.trilhas;
    const ABAS = [["inicio", "🌱", "Para começar"], ...Object.entries(TR).map(([k, t]) => [k, t.icone, t.nome])];
    const lista = (aba) => aba === "inicio" ? CS.filter(c => c.nivel === "Fundamentals") : CS.filter(c => c.trilha === aba);

    roots.forEach(root => {
      root.classList.add("vitrine");
      root.innerHTML = `
        <div class="vit-tabs" role="tablist">${ABAS.map(([k, ic, n], i) => `<button type="button" role="tab" class="vit-tab ${i ? "" : "on"}" data-aba="${k}" aria-selected="${!i}">${ic} ${esc(n)}</button>`).join("")}</div>
        <div class="vit-stage">
          <div class="vit-rod" aria-hidden="true"></div>
          <div class="vit-rack" role="listbox" aria-label="Certificações"></div>
        </div>
        <div class="vit-panel" aria-live="polite"></div>`;
      const rack = $(".vit-rack", root), panel = $(".vit-panel", root);

      function badge(c, i, n) {
        const off = i - (n - 1) / 2;
        return `<button type="button" class="vit-item lv-${c.nivel.toLowerCase()} t-${c.trilha}" role="option" data-id="${c.id}" style="--i:${i};--off:${off}">
          <span class="vit-hook" aria-hidden="true"></span>
          <span class="vit-badge">
            <span class="vb-shine" aria-hidden="true"></span>
            <img class="vb-selo" src="${esc(c.selo)}" alt="" loading="lazy" width="96" height="96" draggable="false">
            <small>${esc(c.nivel)}</small>
            <b>${esc(c.codigo)}</b>
            <em>${esc(c.nomePt)}</em>
            ${simFor(c.id) ? '<span class="vb-sim">Simulado</span>' : ""}
          </span>
        </button>`;
      }
      function show(aba) {
        const cs = lista(aba);
        rack.classList.remove("in"); void rack.offsetWidth;
        rack.innerHTML = cs.map((c, i) => badge(c, i, cs.length)).join("");
        rack.style.setProperty("--n", cs.length);
        rack.classList.add("in");
        select(cs[0].id, false);
      }
      function select(id, user = true) {
        const c = CS.find(x => x.id === id); if (!c) return;
        $$(".vit-item", rack).forEach(b => { const on = b.dataset.id === id; b.classList.toggle("sel", on); b.setAttribute("aria-selected", on); });
        rack.classList.add("has-sel");
        const s = simFor(id), soon = simSoon(id);
        const cta = s
          ? `<a class="btn btn-primary" href="${esc(courseUrl(s, s.cursos[0]))}" target="_blank" rel="noopener" data-go="${esc(s.id)}" data-curso="vitrine">Simulado${couponActive(s) ? " com cupom" : ""} ↗</a>`
          : `<a class="btn btn-ghost" href="/certificacoes/${c.id}/#alerta">🔔 ${soon ? "Avise-me no lançamento" : "Quero este simulado"}</a>`;
        const st = c.status === "aposentando" ? `<span class="tag warn">Aposenta em ${c.aposenta.split("-").reverse().join("/")}</span>` : c.status === "beta" ? `<span class="tag soon">Beta</span>` : "";
        panel.innerHTML = `<div class="vp-in">
          <div class="vp-head"><img class="vp-selo" src="${esc(c.selo)}" alt="Selo oficial ${esc(c.codigo)}" width="72" height="72"><span class="vp-code grad">${esc(c.codigo)}</span><div class="tags"><span class="lvl lvl-${c.nivel.toLowerCase()}">${esc(c.nivel)}</span>${st}${c.minutos ? `<span class="tag">⏱ ${c.minutos} min</span>` : ""}${c.ptbr ? '<span class="tag">🇧🇷 PT-BR</span>' : ""}</div></div>
          <h3>${esc(c.nomePt)}</h3>
          <p>${esc(c.resumo)}</p>
          <div class="row"><a class="btn btn-primary" href="/certificacoes/${c.id}/">Ver o guia da ${esc(c.codigo)} →</a>${cta}</div>
        </div>`;
        if (user) track("vitrine_escolha", { exame: c.codigo });
      }
      root.addEventListener("click", (e) => {
        const t = e.target.closest(".vit-tab");
        if (t) {
          $$(".vit-tab", root).forEach(b => { b.classList.toggle("on", b === t); b.setAttribute("aria-selected", b === t); });
          show(t.dataset.aba); return;
        }
        const it = e.target.closest(".vit-item");
        if (it) { select(it.dataset.id); it.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" }); }
      });
      // Arrastar com o mouse no desktop
      let down = false, sx = 0, sl = 0;
      rack.addEventListener("pointerdown", (e) => { if (e.pointerType !== "mouse") return; down = true; sx = e.clientX; sl = rack.scrollLeft; });
      addEventListener("pointerup", () => { down = false; });
      rack.addEventListener("pointermove", (e) => { if (down) rack.scrollLeft = sl - (e.clientX - sx); });
      show("inicio");
    });
  });
})();
