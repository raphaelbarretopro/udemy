/* Quiz "Qual certificação escolher?" — cobre as certificações Microsoft e os simulados AWS. */
(() => {
  "use strict";
  const body = document.getElementById("quizBody");
  if (!body) return;
  const { $, esc, couponActive, courseUrl, couponChip, simFor, simSoon, track, byId } = window.RB;

  /* Áreas → foco → [certificação do papel, certificação avançada]. Fundamentals da área em "fund". */
  const AREAS = {
    azure: { t: "Infraestrutura e nuvem Azure", ic: "☁️", fund: "AZ-900", focos: [
      ["admin", "Administrar recursos do Azure", "AZ-104", "AZ-305"],
      ["redes", "Redes e conectividade", "AZ-700", "AZ-305"],
      ["arq", "Arquitetar soluções", "AZ-104", "AZ-305"],
      ["win", "Windows Server e ambiente híbrido", "AZ-802", "AZ-104"],
      ["avd", "Desktops virtuais (AVD)", "AZ-104", "AZ-140"],
      ["sap", "SAP no Azure", "AZ-104", "AZ-120"]] },
    dev: { t: "Desenvolvimento e DevOps", ic: "🧩", fund: "AZ-900", focos: [
      ["apps", "Desenvolver aplicações na nuvem", "AI-200", "AZ-401"],
      ["devops", "CI/CD, pipelines e DevOps", "AI-200", "AZ-401"],
      ["cosmos", "Apps com Cosmos DB", "AI-200", "DP-420"]] },
    ia: { t: "IA, agentes e machine learning", ic: "🤖", fund: "AI-901", focos: [
      ["agentes", "Criar apps e agentes com código", "AI-103", "AI-500"],
      ["mlops", "Colocar modelos em produção (MLOps)", "AI-300", "AI-500"],
      ["lowcode", "Criar agentes sem código (Copilot Studio)", "AB-620", "AB-100"]] },
    dados: { t: "Dados e analytics", ic: "📊", fund: "DP-900", focos: [
      ["bi", "Relatórios e dashboards (Power BI)", "PL-300", "DP-600"],
      ["fabric", "Engenharia de dados no Fabric", "DP-700", "DP-600"],
      ["databricks", "Engenharia de dados no Databricks", "DP-750", "DP-700"],
      ["dba", "Administrar bancos SQL", "DP-300", "DP-800"],
      ["sqlia", "IA dentro do banco de dados", "DP-300", "DP-800"]] },
    seguranca: { t: "Segurança e identidade", ic: "🛡️", fund: "SC-900", focos: [
      ["soc", "Detectar e responder a ameaças (SOC)", "SC-200", "SC-100"],
      ["id", "Identidade e acesso", "SC-300", "SC-100"],
      ["dados", "Proteção de dados e conformidade", "SC-401", "SC-100"],
      ["cloud", "Segurança de nuvem e de IA", "SC-500", "SC-100"]] },
    m365: { t: "Microsoft 365, Teams e dispositivos", ic: "💼", fund: "AB-900", focos: [
      ["admin", "Administrar o Microsoft 365 e o Copilot", "AB-650", "AB-650"],
      ["disp", "Dispositivos e Intune", "MD-102", "AB-650"],
      ["teams", "Administrar o Teams", "MS-700", "MS-721"],
      ["voz", "Telefonia e salas Teams", "MS-700", "MS-721"]] },
    power: { t: "Power Platform e low-code", ic: "⚡", fund: "PL-900", focos: [
      ["apps", "Criar apps e automações", "AB-410", "AB-100"],
      ["agentes", "Criar agentes no Copilot Studio", "AB-620", "AB-100"],
      ["code", "Estender com código (pro-dev)", "AB-400", "AB-100"]] },
    dynamics: { t: "Dynamics 365 (ERP e CRM)", ic: "🏢", fund: "PL-900", focos: [
      ["bc", "Business Central (funcional)", "MB-800", "MB-820"],
      ["bcdev", "Business Central (desenvolvimento)", "MB-820", "MB-820"],
      ["fin", "Finanças", "MB-310", "AB-100"],
      ["scm", "Cadeia de suprimentos", "AB-330", "AB-100"],
      ["fodev", "Desenvolvimento X++ (Finance & Operations)", "MB-500", "AB-100"],
      ["vendas", "Vendas com IA", "AB-210", "AB-100"],
      ["atend", "Atendimento ao cliente", "MB-230", "AB-250"],
      ["cc", "Contact Center com IA", "AB-250", "AB-100"]] },
    negocios: { t: "IA para negócios (não técnico)", ic: "🚀", fund: "AB-730", focos: [
      ["uso", "Usar IA para produzir mais no trabalho", "AB-730", "AB-731"],
      ["lider", "Liderar a adoção de IA na empresa", "AB-731", "AB-100"],
      ["arq", "Desenhar soluções de negócio com IA", "AB-731", "AB-100"]] },
    aws: { t: "Nuvem AWS", ic: "🟧", fund: "CLF-C02", focos: [
      ["cloud", "Arquitetura e infraestrutura", "CLF-C02", "SAA-C03"],
      ["ia", "IA e machine learning", "AIF-C01", "SAA-C03"]] }
  };
  if (window.SITE.mostrarAWS === false) delete AREAS.aws;
  const NIVEIS = [
    ["inicio", "🌱", "Estou começando nessa área"],
    ["pratica", "🛠️", "Já trabalho com isso (1 a 3 anos)"],
    ["senior", "🚀", "Sou experiente e quero o nível avançado"]
  ];

  let CERTS = {};
  const AWS = {
    "CLF-C02": { nomePt: "AWS Cloud Practitioner", nivel: "Foundational", resumo: "A porta de entrada da AWS: serviços, segurança, preços e suporte." },
    "AIF-C01": { nomePt: "AWS AI Practitioner", nivel: "Foundational", resumo: "IA generativa e machine learning na AWS, sem exigir programação." },
    "SAA-C03": { nomePt: "AWS Solutions Architect – Associate", nivel: "Associate", resumo: "Arquitetar soluções resilientes, seguras e com bom custo na AWS." }
  };
  const info = (code) => CERTS[code] || AWS[code] || { nomePt: code, nivel: "", resumo: "" };
  const isAws = (code) => !!AWS[code];
  const pageUrl = (code) => isAws(code) ? `/#${code.toLowerCase()}` : `/certificacoes/${code.toLowerCase()}/`;

  const answers = {};
  let step = 0;
  const steps = () => [
    { k: "area", t: "Qual área mais combina com você?", o: Object.entries(AREAS).map(([k, a]) => [k, a.ic, a.t]) },
    { k: "nivel", t: "Qual é a sua experiência nessa área?", o: NIVEIS },
    { k: "foco", t: "E qual é o seu foco?", o: answers.area ? AREAS[answers.area].focos.map(([k, l]) => [k, "›", l]) : [] }
  ];

  function recommend() {
    const a = AREAS[answers.area];
    const f = a.focos.find(x => x[0] === answers.foco) || a.focos[0];
    const [, , papel, avancado] = f;
    let rec;
    if (answers.nivel === "inicio") rec = a.fund;
    else if (answers.nivel === "senior") rec = avancado;
    else rec = papel;
    // Expert com pré-requisito: quem está "na prática" faz primeiro o papel
    const path = [...new Set([a.fund, papel, avancado])];
    const alt = rec === papel ? (avancado !== papel ? avancado : a.fund) : papel;
    return { rec, path, alt };
  }

  function chipPath(path, rec) {
    return path.map((c, i) => `${i ? '<span class="flow flow-sm" aria-hidden="true"><i></i><i></i></span>' : ""}<a class="pchip ${c === rec ? "on" : ""}" href="${pageUrl(c)}"><b>${esc(c)}</b> ${esc(info(c).nomePt)}</a>`).join("");
  }

  function actionFor(code) {
    const s = simFor(code);
    if (s) {
      return `<a class="btn btn-primary" href="${esc(courseUrl(s, s.cursos[0]))}" target="_blank" rel="noopener" data-go="${esc(s.id)}" data-curso="quiz">Treinar ${esc(code)} na Udemy ↗</a>
        ${couponActive(s) ? `<div style="flex:1;min-width:220px">${couponChip(s)}</div>` : ""}`;
    }
    const label = simSoon(code) ? `🔔 Avise-me no lançamento do simulado ${esc(code)}` : `🔔 Quero o simulado ${esc(code)}`;
    return `<a class="btn btn-primary" href="#alerta" data-notify="${esc(code)}">${label}</a>`;
  }

  function render() {
    const list = steps();
    const bar = document.getElementById("quizBar");
    if (bar) bar.style.width = (Math.min(step, list.length) / list.length * 100) + "%";
    if (step >= list.length) return renderResult();
    const q = list[step];
    body.innerHTML = `<div class="q-anim">
      <p class="q-title">${step + 1}/${list.length} · ${esc(q.t)}</p>
      <div class="opts ${q.o.length > 6 ? "opts-3" : ""}">${q.o.map(([v, ic, l]) => `<button type="button" class="opt" data-k="${q.k}" data-v="${v}"><span class="ic">${ic}</span>${esc(l)}</button>`).join("")}</div>
      ${step ? `<p style="margin-top:14px"><button type="button" class="link-btn" data-back>← Voltar</button></p>` : ""}
    </div>`;
  }

  function renderResult() {
    const { rec, path, alt } = recommend();
    const c = info(rec);
    track("quiz_resultado", { exame: rec });
    const aviso = c.status === "aposentando" ? `<p class="why">⚠️ Atenção: este exame se aposenta em ${c.aposenta.split("-").reverse().join("/")}.</p>`
      : c.status === "beta" ? `<p class="why">🧪 Exame em beta: o conteúdo ainda pode mudar.</p>` : "";
    const badges = [c.nivel && `<span class="lvl lvl-${String(c.nivel).toLowerCase()}">${esc(c.nivel)}</span>`,
      c.minutos && `<span class="tag">⏱ ${c.minutos} min</span>`, c.ptbr && `<span class="tag">🇧🇷 Prova em português</span>`].filter(Boolean).join("");
    body.innerHTML = `<div class="result q-anim">
      <p class="q-title">Sua recomendação</p>
      <div class="rec">${c.selo ? `<img class="selo-rec" src="${esc(c.selo)}" alt="Selo oficial" width="84" height="84">` : ""}<span class="code grad">${esc(rec)}</span><div><b>${esc(c.nomePt)}</b><div class="tags" style="margin:6px 0">${badges}</div><p class="why">${esc(c.resumo)}</p></div></div>
      ${aviso}
      <div class="row">${actionFor(rec)}<a class="btn btn-ghost" href="${pageUrl(rec)}">Ver o guia completo</a></div>
      <div><p class="why" style="margin-bottom:8px">Sua rota nesta área:</p><div class="qpath">${chipPath(path, rec)}</div></div>
      ${alt && alt !== rec ? `<p class="why">Também combina com você: <a href="${pageUrl(alt)}" style="text-decoration:underline">${esc(alt)} · ${esc(info(alt).nomePt)}</a></p>` : ""}
      <p><button type="button" class="link-btn" data-restart>Refazer o quiz</button></p>
    </div>`;
  }

  body.addEventListener("click", (e) => {
    const o = e.target.closest(".opt");
    if (o) {
      answers[o.dataset.k] = o.dataset.v;
      if (o.dataset.k === "area") delete answers.foco;
      step++; render();
      const top = body.getBoundingClientRect().top;
      if (top < 60) body.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    if (e.target.closest("[data-back]")) { step = Math.max(0, step - 1); render(); return; }
    if (e.target.closest("[data-restart]")) { step = 0; Object.keys(answers).forEach(k => delete answers[k]); render(); }
  });

  fetch("/assets/certificacoes.json").then(r => r.json()).then(d => {
    d.certificacoes.forEach(c => { CERTS[c.codigo] = c; });
    render();
  }).catch(() => { body.innerHTML = '<p class="muted">Não foi possível carregar o quiz. <a href="/certificacoes/">Veja todas as certificações</a>.</p>'; });
})();
