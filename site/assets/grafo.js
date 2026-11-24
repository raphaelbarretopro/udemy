/* Linhas de ligação entre certificações (rotas e "Onde ela se encaixa").
   Cada [data-graph] tem colunas .gcol com nós [data-node] e data-edges="A>B;A>C;...".
   Desenha linhas em ângulo com seta e um pulso de luz que percorre a linha até a ponta. */
(() => {
  "use strict";
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const NS = "http://www.w3.org/2000/svg";
  let uid = 0;

  function el(tag, attrs) { const n = document.createElementNS(NS, tag); for (const k in attrs) n.setAttribute(k, attrs[k]); return n; }

  // Caminho em "L" com cantos arredondados: sai para a direita, desce/sobe no meio, entra no alvo
  function elbowH(sx, sy, mx, tx, ty, r = 10) {
    if (Math.abs(ty - sy) < 1.5) return `M${sx},${sy} H${tx}`;
    const d = ty > sy ? 1 : -1;
    r = Math.min(r, Math.abs(ty - sy) / 2, mx - sx, tx - mx);
    return `M${sx},${sy} H${mx - r} Q${mx},${sy} ${mx},${sy + d * r} V${ty - d * r} Q${mx},${ty} ${mx + r},${ty} H${tx}`;
  }
  // Versão empilhada (celular): sai pela esquerda, desce pela calha e entra no alvo pela esquerda
  function elbowV(sx, sy, gx, tx, ty, r = 9) {
    const d = ty > sy ? 1 : -1;
    r = Math.min(r, Math.abs(ty - sy) / 2, sx - gx, tx - gx);
    return `M${sx},${sy} H${gx + r} Q${gx},${sy} ${gx},${sy + d * r} V${ty - d * r} Q${gx},${ty} ${gx + r},${ty} H${tx}`;
  }

  function draw(g) {
    const edges = (g.dataset.edges || "").split(";").filter(Boolean).map(x => x.split(">"));
    (g._anims || []).forEach(a => a.cancel()); g._anims = [];
    g.querySelector(":scope > svg.gsvg")?.remove();
    if (!edges.length) return;
    const box = g.getBoundingClientRect();
    if (!box.width) return;
    const cols = [...g.querySelectorAll(":scope > .gcol")];
    const nodes = {};
    cols.forEach((c, ci) => c.querySelectorAll("[data-node]").forEach(n => { nodes[n.dataset.node] = { el: n, col: ci, r: n.getBoundingClientRect() }; }));
    const horizontal = cols.length > 1 && cols[1].getBoundingClientRect().left > cols[0].getBoundingClientRect().right - 2;
    const colR = cols.map(c => c.getBoundingClientRect());

    const id = "gh" + (++uid);
    const svg = el("svg", { class: "gsvg", width: box.width, height: box.height, viewBox: `0 0 ${box.width} ${box.height}`, "aria-hidden": "true" });
    const defs = el("defs", {});
    const mk = el("marker", { id: id + "a", viewBox: "0 0 10 10", refX: "8.5", refY: "5", markerWidth: "7", markerHeight: "7", orient: "auto-start-reverse", markerUnits: "userSpaceOnUse" });
    mk.appendChild(el("path", { d: "M0,0 L10,5 L0,10 Z", class: "garrow" }));
    const glow = el("filter", { id: id + "g", x: "-50%", y: "-50%", width: "200%", height: "200%" });
    glow.appendChild(el("feGaussianBlur", { stdDeviation: "2.2", result: "b" }));
    const merge = el("feMerge", {}); merge.appendChild(el("feMergeNode", { in: "b" })); merge.appendChild(el("feMergeNode", { in: "SourceGraphic" })); glow.appendChild(merge);
    defs.append(mk, glow); svg.appendChild(defs);

    // calhas diferentes por origem no modo empilhado
    const fontes = [...new Set(edges.map(e => e[0]))];
    edges.forEach(([a, b], i) => {
      const A = nodes[a], B = nodes[b];
      if (!A || !B) return;
      const ra = A.r, rb = B.r;
      let d;
      if (horizontal) {
        const sx = ra.right - box.left, sy = ra.top + ra.height / 2 - box.top;
        const tx = rb.left - box.left - 2, ty = rb.top + rb.height / 2 - box.top;
        const gapL = colR[A.col].right - box.left, gapR = colR[B.col].left - box.left;
        const mx = gapL + (gapR - gapL) * .5;
        d = elbowH(sx, sy, mx, tx, ty);
      } else {
        const k = fontes.indexOf(a);
        const gx = 6 + (k % 4) * 5;
        const sx = ra.left - box.left, sy = ra.top + ra.height / 2 - box.top;
        const tx = rb.left - box.left - 2, ty = rb.top + rb.height / 2 - box.top;
        d = elbowV(sx, sy, gx, tx, ty);
      }
      const base = el("path", { d, class: "gline", "marker-end": `url(#${id}a)` });
      svg.appendChild(base);
      if (reduced) return;
      const len = base.getTotalLength();
      const seg = Math.min(46, len * .35);
      const pulse = el("path", { d, class: "gpulse", filter: `url(#${id}g)`, "stroke-dasharray": `${seg} ${len + seg}`, "stroke-dashoffset": seg });
      const end = base.getPointAtLength(len);
      const tip = el("circle", { cx: end.x, cy: end.y, r: 4.5, class: "gtip", filter: `url(#${id}g)` });
      svg.append(pulse, tip);
      const dur = Math.max(1300, len * 7), delay = (i * 420) % 2400;
      const opt = { duration: dur, delay, iterations: Infinity, easing: "cubic-bezier(.45,0,.55,1)" };
      g._anims.push(pulse.animate([{ strokeDashoffset: seg }, { strokeDashoffset: -len }], opt));
      g._anims.push(tip.animate([{ opacity: 0, transform: "scale(.4)" }, { opacity: 0, transform: "scale(.4)", offset: .86 }, { opacity: 1, transform: "scale(1.3)", offset: .95 }, { opacity: 0, transform: "scale(.6)" }], opt));
      tip.style.transformOrigin = `${end.x}px ${end.y}px`; tip.style.transformBox = "view-box";
    });
    g.prepend(svg);
  }

  const graphs = [...document.querySelectorAll("[data-graph]")];
  if (!graphs.length) return;
  let raf;
  const redrawAll = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => graphs.forEach(draw)); };
  const ro = new ResizeObserver(redrawAll);
  graphs.forEach(g => {
    ro.observe(g);
    // acelera o pulso ao passar o mouse
    const host = g.closest(".route, .block") || g;
    host.addEventListener("pointerenter", () => (g._anims || []).forEach(a => a.playbackRate = 2.2));
    host.addEventListener("pointerleave", () => (g._anims || []).forEach(a => a.playbackRate = 1));
  });
  document.fonts && document.fonts.ready.then(redrawAll);
  addEventListener("load", redrawAll);
  // redesenha quando as animações de entrada terminam
  setTimeout(redrawAll, 1200);
})();
