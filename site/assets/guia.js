/* Página /certificacoes/: filtros, busca e selos de simulado. */
(() => {
  "use strict";
  const { $, $$, simFor, simSoon, couponActive } = window.RB;
  const cards = $$("#grupos .ccard");
  let nSim = 0;

  // Selos de simulado em cada card
  cards.forEach(a => {
    const id = a.dataset.cert, slot = $(".sim-slot", a);
    const s = simFor(id), soon = simSoon(id);
    if (s) {
      nSim++; a.dataset.sim = "1";
      slot.outerHTML = `<span class="tag new">✓ Simulado na Udemy${couponActive(s) ? " · cupom" : ""}</span>`;
    } else if (soon) {
      slot.outerHTML = `<span class="tag soon">Simulado em breve</span>`;
    } else slot.remove();
  });
  $("#nSim").textContent = nSim;

  const state = { trilha: new Set(), nivel: new Set(), q: "", pt: false, sim: false };
  const norm = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

  function apply() {
    let n = 0;
    const q = norm(state.q.trim());
    cards.forEach(a => {
      const ok = (!state.trilha.size || state.trilha.has(a.dataset.trilha))
        && (!state.nivel.size || state.nivel.has(a.dataset.nivel))
        && (!state.pt || a.dataset.pt === "1")
        && (!state.sim || a.dataset.sim === "1")
        && (!q || norm(a.dataset.busca).includes(q) || norm(a.dataset.busca.replace(/-/g, "")).includes(q.replace(/-/g, "")));
      a.hidden = !ok; if (ok) n++;
    });
    $$(".cgroup").forEach(g => { g.hidden = !$$(".ccard", g).some(a => !a.hidden); });
    $("#contagem").textContent = `${n} certificaç${n === 1 ? "ão" : "ões"}`;
    $("#vazio").hidden = n > 0;
  }
  $$(".fchip").forEach(b => b.addEventListener("click", () => {
    const set = state[b.dataset.f], v = b.dataset.v;
    set.has(v) ? set.delete(v) : set.add(v);
    b.classList.toggle("on", set.has(v)); b.setAttribute("aria-pressed", set.has(v));
    apply();
  }));
  $("#busca").addEventListener("input", (e) => { state.q = e.target.value; apply(); });
  $("#soPt").addEventListener("change", (e) => { state.pt = e.target.checked; apply(); });
  $("#soSim").addEventListener("change", (e) => { state.sim = e.target.checked; apply(); });
  const limpar = () => {
    state.trilha.clear(); state.nivel.clear(); state.q = ""; state.pt = state.sim = false;
    $("#busca").value = ""; $("#soPt").checked = $("#soSim").checked = false;
    $$(".fchip").forEach(b => { b.classList.remove("on"); b.setAttribute("aria-pressed", "false"); });
    apply();
  };
  $("#limpar").addEventListener("click", limpar);
  document.addEventListener("click", (e) => { if (e.target.closest("[data-limpar]")) limpar(); });

  // ?trilha=seguranca abre já filtrado (útil para stories)
  const p = new URLSearchParams(location.search);
  const t = p.get("trilha"); if (t) { const b = $(`.fchip[data-f="trilha"][data-v="${CSS.escape(t)}"]`); if (b) b.click(); }
  const n = p.get("nivel"); if (n) { const b = $(`.fchip[data-f="nivel"][data-v="${CSS.escape(n)}"]`); if (b) b.click(); }
})();
