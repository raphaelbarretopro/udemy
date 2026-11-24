# -*- coding: utf-8 -*-
"""
Gera as páginas de certificações Microsoft a partir de:
  ferramentas/conteudo_pt.py  (textos em português)
  ferramentas/base_learn.json (dados oficiais do Microsoft Learn: pesos, duração, idiomas)

Saída (dentro de site/):
  assets/certificacoes.json          dados usados pelo quiz e pelo catálogo
  certificacoes/index.html           guia com todas as certificações
  certificacoes/<codigo>/index.html  página de cada certificação
  <codigo>/index.html                atalho curto (raphaelbarreto.com.br/az-104)
  sitemap.xml

Uso:  python ferramentas/gerar.py
"""
import json, os, re, sys
from html import escape as e
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RAIZ, "site")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conteudo_pt import C, TRILHAS
from conteudo_extra import EXTRA

BASE = json.load(open(os.path.join(RAIZ, "ferramentas", "base_learn.json"), encoding="utf-8"))
DOMINIO = "https://raphaelbarreto.com.br"
ATUALIZADO = "novembro de 2026"
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
MESES_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
NIVEIS = ["Fundamentals", "Associate", "Expert", "Specialty", "Business"]
NIVEL_INFO = {
    "Fundamentals": ("Fundamentos", "Porta de entrada. Vocabulário, conceitos e casos de uso de um produto. Não exige experiência e não expira."),
    "Associate": ("Associado", "Ligada a uma função do dia a dia: administrar, desenvolver, analisar, implementar. Exige prática."),
    "Expert": ("Especialista", "Arquitetura e decisões de nível sênior. Normalmente exige uma certificação Associate antes."),
    "Specialty": ("Especialidade", "Foco em uma carga de trabalho específica, como SAP, Azure Virtual Desktop ou Cosmos DB."),
    "Business": ("Negócios", "Para profissionais de negócio e líderes: valor, adoção e uso responsável da IA. Não é técnica."),
}
ORDEM_NIVEL = {n: i for i, n in enumerate(NIVEIS)}

def data_br(iso):
    y, m, d = map(int, iso.split("-"))
    return f"{d:02d}/{m:02d}/{y}"

def data_en_br(txt):
    if not txt: return None
    m = re.match(r"([A-Za-z]+) (\d+), (\d{4})", txt)
    return f"{int(m.group(2))} de {MESES[MESES_EN.index(m.group(1))]} de {m.group(3)}" if m else None

def ponto_medio(peso):
    a, b = re.findall(r"\d+", peso)[:2]
    return (int(a) + int(b)) / 2

# ---------------------------------------------------------------- dados combinados
CERTS = []
for cod, c in C.items():
    b = BASE[cod]
    CERTS.append(dict(
        codigo=cod, id=cod.lower(), nomePt=c["nome_pt"], nome=b["nome"], trilha=c["trilha"], nivel=c["nivel"],
        status=c["status"], aposenta=c["aposenta"], resumo=c["resumo"], publico=c["publico"], prereq=c["prereq"],
        antes=c["antes"], depois=c["depois"], minutos=b["minutos"], ptbr=b["ptbr"],
        guiaAtualizado=data_en_br(b["guia_atualizado"]),
        dominios=[dict(nome=n, peso=p, topicos=t) for (n, t), p in zip(c["dominios"], b["pesos"])],
        learn=f"https://learn.microsoft.com/pt-br/credentials/certifications/{b['slug']}/",
        exame=f"https://learn.microsoft.com/pt-br/credentials/certifications/exams/{cod.lower()}/",
        guia=f"https://learn.microsoft.com/pt-br/credentials/certifications/resources/study-guides/{cod.lower()}",
        selo=b["selo"],
    ))
ANO = ATUALIZADO.split()[-1]

# Simulados já lançados e perfis do autor, lidos de site/assets/dados.js
_DADOS = open(os.path.join(SITE, "assets", "dados.js"), encoding="utf-8").read()
COM_SIMULADO = {m.group(1).upper() for m in re.finditer(r'id: "([a-z]{2}-\d{3})", trilha: "microsoft".*?status: "([a-z-]+)"', _DADOS, re.S) if m.group(2) == "disponivel"}
PERFIS = [u for u in re.findall(r'^\s*(?:instagram|linkedin|youtube|udemyPerfil): "(https?://[^"]+)"', _DADOS, re.M)]
PESSOA = {"@type": "Person", "@id": f"{DOMINIO}/#raphael", "name": "Raphael Barreto", "url": f"{DOMINIO}/",
          "image": f"{DOMINIO}/assets/raphael.webp", "jobTitle": "Microsoft Certified Educator"}
if PERFIS: PESSOA["sameAs"] = PERFIS
SITE_LD = {"@type": "WebSite", "@id": f"{DOMINIO}/#site", "name": "Raphael Barreto · Simulados Microsoft", "url": f"{DOMINIO}/",
           "inLanguage": "pt-BR", "publisher": {"@id": f"{DOMINIO}/#raphael"}}

def ld_script(*nos):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": list(nos)}, ensure_ascii=False) + "</script>"

ORDEM_TRILHA = list(TRILHAS)
CERTS.sort(key=lambda c: (ORDEM_TRILHA.index(c["trilha"]), ORDEM_NIVEL[c["nivel"]], c["codigo"]))
POR = {c["codigo"]: c for c in CERTS}

# ---------------------------------------------------------------- partes comuns
def head(titulo, desc, url, extra="", imagem="/assets/og/certificacoes.jpg"):
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(titulo)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="author" content="Raphael Barreto">
  <meta name="theme-color" content="#07080f">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{e(titulo)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{DOMINIO}{url}">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:image" content="{DOMINIO}{imagem}">
  <meta property="og:image:secure_url" content="{DOMINIO}{imagem}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:alt" content="{e(titulo)}">
  <meta property="og:site_name" content="Raphael Barreto · Simulados Microsoft">
  <meta name="twitter:image" content="{DOMINIO}{imagem}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{DOMINIO}{url}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/style.css">
  <link rel="stylesheet" href="/assets/guia.css">
  <link rel="stylesheet" href="/assets/efeitos.css">
  <link rel="stylesheet" href="/assets/social.css">
  {extra}
</head>
<body>
  <div class="bg" aria-hidden="true"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="grid"></div><canvas id="agentes"></canvas><div class="spot"></div></div>
  <div class="demo-bar" id="demoBar" hidden>Modo demonstração · os cupons exibidos são exemplos</div>
  <header class="topbar">
    <a class="brand" href="/" aria-label="Início"><span class="brand-mark">RB</span><span class="brand-name">Raphael Barreto</span></a>
    <nav class="topnav" aria-label="Seções">
      <a href="/">Simulados</a>
      <a href="/certificacoes/" class="nav-hot">Certificações <span class="nav-badge">50</span></a>
      <a href="/certificacoes/#quiz">Qual fazer?</a>
    </nav>
    <a class="btn btn-sm btn-glow" href="#alerta">Receber cupons</a>
  </header>
"""

def lead_form(titulo, texto, codigo=None, opcoes=False):
    oculto = f'<input type="hidden" name="interesses" value="{e(codigo)}">' if codigo else ""
    seletor = ""
    if opcoes:
        ops = "".join(f'<option value="{c["codigo"]}">{c["codigo"]} · {e(c["nomePt"])}</option>' for c in CERTS)
        seletor = f'<label>Qual certificação você quer fazer?<select name="interesses"><option value="">Escolha uma certificação</option>{ops}</select></label>'
    return f"""
  <section class="section" id="alerta">
    <div class="lead-box glass reveal">
      <div class="lead-copy">
        <span class="eyebrow">Alerta de cupom</span>
        <h2>{titulo}</h2>
        <p>{texto}</p>
        <ul class="ticks"><li>Cupom de estreia para quem está na lista</li><li>Aviso no dia do lançamento</li><li>Sem spam. Sai quando quiser.</li></ul>
      </div>
      <form class="lead-form" data-lead novalidate>
        <label>Seu nome<input name="nome" autocomplete="given-name" required placeholder="Como posso te chamar?"></label>
        <label>WhatsApp ou e-mail<input name="contato" required placeholder="(21) 99999-9999 ou voce@email.com"></label>
        {seletor}{oculto}
        <label class="consent"><input type="checkbox" name="consent" required><span>Aceito receber cupons e novidades de Raphael Barreto.</span></label>
        <input type="text" name="site" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <button class="btn btn-primary btn-block" type="submit">Quero ser avisado</button>
        <p class="form-msg" role="status"></p>
      </form>
    </div>
  </section>"""

def rodape(scripts):
    s = "\n".join(f'  <script src="/assets/{x}"></script>' for x in ["dados.js", "comum.js", "efeitos.js"] + scripts)
    return f"""
  <footer class="footer">
    <div class="social" id="social"></div>
    <p>Conteúdo independente baseado no Microsoft Learn, atualizado em {ATUALIZADO}. Não afiliado à Microsoft.<br>Os selos exibidos são os selos oficiais das certificações e pertencem à Microsoft Corporation.<br>Nomes de exames, datas, idiomas e preços podem mudar: confirme no Microsoft Learn antes de agendar.</p>
    <p>© <span id="ano"></span> Raphael Barreto</p>
  </footer>
  <div class="dock" id="dock"><a class="btn btn-primary btn-block" href="/certificacoes/#quiz">🎯 Descobrir minha certificação</a></div>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>
{s}
</body>
</html>
"""

def badge_nivel(n): return f'<span class="lvl lvl-{n.lower()}">{n}</span>'

def badge_status(c):
    if c["status"] == "aposentando": return f'<span class="tag warn">Aposenta em {data_br(c["aposenta"])}</span>'
    if c["status"] == "beta": return '<span class="tag soon">Beta</span>'
    return ""

def chip_pt(c):
    if c["ptbr"] is True: return '<span class="tag">🇧🇷 Prova em português</span>'
    if c["ptbr"] is False: return '<span class="tag muted-tag">Prova em inglês</span>'
    return ""

def card_cert(c):
    t = TRILHAS[c["trilha"]][0]
    dur = f'{c["minutos"]} min' if c["minutos"] else ""
    busca = " ".join([c["codigo"], c["nomePt"], c["nome"], t, c["nivel"], c["resumo"]]).lower()
    return f"""<div class="ccard-box"><a class="ccard {'aws' if False else ''}" href="/certificacoes/{c['id']}/" data-cert="{c['id']}" data-trilha="{c['trilha']}" data-nivel="{c['nivel']}" data-pt="{'1' if c['ptbr'] else '0'}" data-busca="{e(busca)}">
  <div class="ccard-top"><img class="selo-sm" src="{c['selo']}" alt="" loading="lazy" width="44" height="44"><span class="ccode">{c['codigo']}</span>{badge_nivel(c['nivel'])}</div>
  <h3>{e(c['nomePt'])}</h3>
  <p class="cname">{e(c['nome'])}</p>
  <div class="tags">{badge_status(c)}{'<span class="tag">⏱ ' + dur + '</span>' if dur else ''}{'<span class="tag">🇧🇷 PT-BR</span>' if c['ptbr'] else ''}<span class="sim-slot"></span></div>
</a><div class="ig ig-card" data-social="{c['id']}" data-nome="{e(c['nomePt'])}"></div></div>"""

def link_cert(cod):
    c = POR.get(cod)
    if not c: return f"<span>{e(cod)}</span>"
    return f'<a class="pchip" data-node="{c["codigo"]}" href="/certificacoes/{c["id"]}/"><b>{c["codigo"]}</b> {e(c["nomePt"])}</a>'

# ---------------------------------------------------------------- rotas por trilha
ROTAS = [
    ("azure", ["AZ-900"], ["AZ-104", "AZ-802"], ["AZ-305", "AZ-700", "AZ-140", "AZ-120"], "Operação e arquitetura de nuvem no Azure. Depois da AZ-104, escolha entre arquitetura, redes ou especialidades."),
    ("dev", ["AZ-900", "AI-901"], ["AI-200", "AZ-104"], ["AZ-401", "AZ-400"], "Desenvolvimento na nuvem e entrega contínua. A AZ-400 se aposenta em 01/02/2027; a AZ-401 está em beta."),
    ("ia", ["AI-901"], ["AI-103", "AI-300"], ["AI-500"], "Apps generativos, agentes, MLOps e sistemas multiagente."),
    ("dados", ["DP-900"], ["PL-300", "DP-300", "DP-700", "DP-750", "DP-420"], ["DP-600", "DP-800"], "Power BI, bancos de dados, Fabric, Databricks, Cosmos DB e IA no SQL."),
    ("seguranca", ["SC-900"], ["SC-200", "SC-300", "SC-401", "SC-500"], ["SC-100"], "Operações de segurança, identidade, proteção de dados e nuvem."),
    ("m365", ["AB-900"], ["MD-102", "MS-700", "AB-650"], ["MS-721", "MS-102"], "Dispositivos, Teams, Copilot e administração do locatário. A MS-102 se aposenta em 30/11/2026."),
    ("power", ["PL-900"], ["AB-410", "AB-620"], ["AB-400", "AB-100"], "Apps, automação, agentes no Copilot Studio e extensões com código."),
    ("dynamics", ["MB-800", "MB-230", "AB-210", "MB-310", "AB-330"], ["MB-820", "AB-250", "MB-500"], ["AB-100"], "ERP e CRM: comece pelo módulo com que você trabalha. A AB-100 aceita qualquer uma dessas Associate como pré-requisito."),
    ("negocios", ["AB-730"], ["AB-731"], ["AB-100"], "Uso, liderança e arquitetura de IA em negócios."),
]
# Conexões extras que não vêm de "antes/depois" (mesma plataforma ou pré-requisito oficial da AB-100)
LIGACOES_EXTRAS = {"dynamics": ["MB-310>MB-500", "AB-330>MB-500", "AB-210>AB-250", "MB-820>AB-100", "AB-250>AB-100", "MB-500>AB-100"]}

def arestas(tk, cols):
    """Liga cada certificação às da coluna seguinte quando uma é pré-requisito ou próximo passo da outra."""
    ed = []
    for i in range(len(cols) - 1):
        for b in cols[i + 1]:
            for a in cols[i]:
                if a in POR and b in POR and (b in POR[a]["depois"] or a in POR[b]["antes"]):
                    ed.append(f"{a}>{b}")
    for x in LIGACOES_EXTRAS.get(tk, []):
        if x not in ed: ed.append(x)
    return ";".join(ed)

ESCOLHA = [
    ("Começar em nuvem Microsoft", ["AZ-900"]), ("Começar em IA", ["AI-901"]), ("Começar em dados", ["DP-900"]),
    ("Começar em segurança", ["SC-900"]), ("Começar em Power Platform", ["PL-900"]), ("Começar em Microsoft 365 e Copilot", ["AB-900"]),
    ("Administrar o Azure", ["AZ-104"]), ("Arquitetar soluções no Azure", ["AZ-305"]), ("Desenvolver na nuvem com IA", ["AI-200"]),
    ("DevOps e entrega contínua", ["AZ-401", "AZ-400"]), ("Criar apps e agentes de IA", ["AI-103"]), ("Colocar modelos em produção (MLOps)", ["AI-300"]),
    ("Relatórios e dashboards", ["PL-300"]), ("Engenharia de dados", ["DP-700", "DP-750"]), ("Banco de dados SQL", ["DP-300", "DP-800"]),
    ("Operações de segurança (SOC)", ["SC-200"]), ("Identidade e acesso", ["SC-300"]), ("Proteção de dados e conformidade", ["SC-401"]),
    ("Segurança de nuvem e IA", ["SC-500"]), ("Dispositivos e Intune", ["MD-102"]), ("Microsoft Teams", ["MS-700", "MS-721"]),
    ("Agentes no Copilot Studio", ["AB-620"]), ("ERP Business Central", ["MB-800", "MB-820"]), ("CRM e vendas com IA", ["AB-210", "MB-230", "AB-250"]),
    ("Usar IA no trabalho (não técnico)", ["AB-730"]), ("Liderar a adoção de IA", ["AB-731"]),
]

# ---------------------------------------------------------------- página guia
def pagina_guia():
    total = len(CERTS)
    pt = sum(1 for c in CERTS if c["ptbr"])
    grupos = ""
    for tk, (tn, ic) in TRILHAS.items():
        cs = [c for c in CERTS if c["trilha"] == tk]
        grupos += f"""
    <div class="cgroup" data-grupo="{tk}">
      <h3 class="cgroup-title"><span>{ic}</span> {e(tn)} <small>{len(cs)}</small></h3>
      <div class="cgrid">{''.join(card_cert(c) for c in cs)}</div>
    </div>"""
    chips_t = "".join(f'<button type="button" class="fchip" data-f="trilha" data-v="{k}">{v[1]} {e(v[0])}</button>' for k, v in TRILHAS.items())
    chips_n = "".join(f'<button type="button" class="fchip" data-f="nivel" data-v="{n}">{n}</button>' for n in NIVEIS)
    aposent = [c for c in CERTS if c["status"] == "aposentando"]
    betas = [c for c in CERTS if c["status"] == "beta"]
    alertas = "".join(f'<li><a href="/certificacoes/{c["id"]}/"><b>{c["codigo"]}</b> {e(c["nomePt"])}</a> se aposenta em <b>{data_br(c["aposenta"])}</b>.</li>' for c in sorted(aposent, key=lambda c: c["aposenta"]))
    alertas += "".join(f'<li><a href="/certificacoes/{c["id"]}/"><b>{c["codigo"]}</b> {e(c["nomePt"])}</a> está em <b>beta</b>.</li>' for c in betas)
    rotas = ""
    for tk, ini, meio, fim, nota in ROTAS:
        tn, ic = TRILHAS[tk]
        col = lambda xs: "".join(link_cert(x) for x in xs)
        rotas += f"""
      <div class="route reveal">
        <h3><span>{ic}</span> {e(tn)}</h3>
        <div class="route-steps graph" data-graph data-edges="{arestas(tk, [ini, meio, fim])}">
          <div class="rstep gcol"><small>Começo</small>{col(ini)}</div>
          <div class="rstep gcol"><small>Depois</small>{col(meio)}</div>
          <div class="rstep gcol"><small>Avançado</small>{col(fim)}</div>
        </div>
        <p class="muted small">{e(nota)}</p>
      </div>"""
    escolha = "".join(f'<tr><td>{e(o)}</td><td>{" ".join(link_cert(x) for x in xs)}</td></tr>' for o, xs in ESCOLHA)
    SELO_NIVEL = {n: next(c["selo"] for c in CERTS if c["nivel"] == n) for n in NIVEIS}
    niveis = "".join(f'<div class="lvlcard glass reveal"><img class="selo-md" src="{SELO_NIVEL[n]}" alt="Selo {n}" loading="lazy" width="96" height="96">{badge_nivel(n)}<h3>{NIVEL_INFO[n][0]}</h3><p>{NIVEL_INFO[n][1]}</p><small class="muted">{sum(1 for c in CERTS if c["nivel"]==n)} certificações</small></div>' for n in NIVEIS)
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Certificações Microsoft",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{DOMINIO}/certificacoes/{c['id']}/", "name": f"{c['codigo']} {c['nome']}"} for i, c in enumerate(CERTS)]}
    ld["@id"] = f"{DOMINIO}/certificacoes/#lista"; del ld["@context"]
    bc = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": DOMINIO + "/"},
        {"@type": "ListItem", "position": 2, "name": "Certificações", "item": DOMINIO + "/certificacoes/"}]}
    html = head(f"Certificações Microsoft {ANO}: as {total} explicadas em português",
                f"Guia com as {total} certificações Microsoft ativas: Azure, IA, dados, segurança, Microsoft 365, Power Platform e Dynamics 365. Rotas, níveis, pesos da prova e quiz para escolher a sua.",
                "/certificacoes/", ld_script(PESSOA, SITE_LD, ld, bc))
    html += f"""
  <main id="topo">
    <section class="hero hero-guide">
      <nav class="crumbs reveal" aria-label="Você está em"><a href="/">Início</a><span>/</span><b>Certificações</b></nav>
      <span class="eyebrow reveal">Atualizado em {ATUALIZADO}</span>
      <h1 class="reveal">Todas as certificações <span class="grad">Microsoft</span></h1>
      <p class="lead reveal">As {total} certificações ativas no Microsoft Learn, organizadas por trilha e nível. Clique em qualquer uma para ver o que cai na prova, para quem é e por onde começar.</p>
      <div class="cta-row reveal">
        <a class="btn btn-primary magnetic" href="#quiz">Descobrir a certificação certa para mim →</a>
        <a class="btn btn-ghost" href="#catalogo">Ver todas</a>
      </div>
      <dl class="stats reveal">
        <div><dt>{total}</dt><dd>certificações</dd></div>
        <div><dt>{len(TRILHAS)}</dt><dd>trilhas</dd></div>
        <div><dt>{pt}</dt><dd>prova em PT-BR</dd></div>
        <div><dt><span id="nSim">0</span></dt><dd>com simulado</dd></div>
      </dl>
    </section>

    <section class="section" id="avisos">
      <div class="notice glass reveal">
        <div><span class="eyebrow">Fique de olho</span><h2>Mudanças no calendário</h2></div>
        <ul>{alertas}<li>A <b>AI-900</b> foi substituída pela <a href="/certificacoes/ai-901/"><b>AI-901</b></a>, e o exame do Power Platform Developer agora é a <a href="/certificacoes/ab-400/"><b>AB-400</b></a>.</li></ul>
      </div>
    </section>

    <section class="section" id="vitrine">
      <div class="guide-feature solo reveal">
        <div class="gf-vitrine">
          <header class="section-head"><span class="eyebrow ms">Vitrine</span><h2>Escolha pela trilha</h2><p>Toque em um selo para ver o resumo da certificação.</p></header>
          <div data-vitrine></div>
        </div>
      </div>
    </section>

    <section class="section" id="catalogo">
      <header class="section-head reveal">
        <span class="eyebrow ms">Catálogo</span>
        <h2>Encontre sua certificação</h2>
        <p>Filtre por trilha, nível ou idioma, ou busque pelo código ou nome.</p>
      </header>
      <div class="filters glass reveal">
        <label class="search"><span aria-hidden="true">🔎</span><input id="busca" type="search" placeholder="Busque: AZ-104, Power BI, segurança, Copilot…" autocomplete="off"></label>
        <div class="frow"><span class="flabel">Trilha</span><div class="fchips">{chips_t}</div></div>
        <div class="frow"><span class="flabel">Nível</span><div class="fchips">{chips_n}</div></div>
        <div class="frow toggles">
          <label class="tgl"><input type="checkbox" id="soPt"><span></span>Prova em português</label>
          <label class="tgl"><input type="checkbox" id="soSim"><span></span>Com simulado na Udemy</label>
          <label class="tgl" id="tglMetas" hidden><input type="checkbox" id="soMetas"><span></span><em id="nMetas" style="font-style:normal">Minhas metas</em></label>
          <button type="button" class="link-btn" id="limpar">Limpar filtros</button>
          <span class="count" id="contagem" aria-live="polite">{total} certificações</span>
        </div>
      </div>
      <div id="grupos">{grupos}</div>
      <p class="empty" id="vazio" hidden>Nenhuma certificação com esses filtros. <button type="button" class="link-btn" data-limpar>Limpar filtros</button></p>
    </section>

    <section class="section" id="quiz">
      <div class="quiz glass reveal">
        <div class="quiz-head">
          <span class="eyebrow">Menos de 1 minuto</span>
          <h2>Qual certificação escolher?</h2>
          <p class="muted">Responda 3 perguntas e receba a recomendação e a rota completa entre as {total} certificações Microsoft.</p>
          <div class="progress" aria-hidden="true"><i id="quizBar"></i></div>
        </div>
        <div id="quizBody" aria-live="polite"></div>
      </div>
    </section>

    <section class="section" id="escolher">
      <header class="section-head reveal"><span class="eyebrow">Atalho</span><h2>Qual certificação para cada objetivo</h2></header>
      <div class="table-wrap glass reveal"><table class="tbl"><thead><tr><th>Seu objetivo</th><th>Considere</th></tr></thead><tbody>{escolha}</tbody></table></div>
    </section>

    <section class="section" id="rotas">
      <header class="section-head reveal"><span class="eyebrow">Caminhos</span><h2>Rotas de certificação</h2><p>Do primeiro exame ao nível avançado em cada área.</p></header>
      <div class="routes">{rotas}</div>
    </section>

    <section class="section" id="niveis">
      <header class="section-head reveal"><span class="eyebrow">Entenda</span><h2>Fundamentals, Associate, Expert, Specialty e Business</h2></header>
      <div class="lvlgrid">{niveis}</div>
    </section>

    <section class="section" id="agendar">
      <div class="two glass reveal">
        <div>
          <span class="eyebrow">Antes de pagar</span>
          <h2>Checklist para agendar a prova</h2>
          <p class="muted">O preço varia por país e aparece na página do exame no Microsoft Learn. A inscrição é feita pelo botão “Agendar exame” da própria página, normalmente pela Pearson VUE.</p>
        </div>
        <ul class="checklist">
          <li><b>Código exato</b> Confirme o nome da certificação e o código do exame.</li>
          <li><b>Situação</b> Veja se o exame está ativo, em beta ou perto de se aposentar.</li>
          <li><b>Preço</b> Confira o valor para o Brasil na página do exame.</li>
          <li><b>Idioma</b> Verifique se a prova é oferecida em português.</li>
          <li><b>Formato</b> Escolha entre prova online ou em centro de testes.</li>
          <li><b>Documento</b> Seu nome no perfil do Microsoft Learn deve ser igual ao do documento.</li>
          <li><b>Treino</b> Faça simulados até passar com folga dos 700 pontos.</li>
        </ul>
      </div>
    </section>
{lead_form('Quer um simulado de outra certificação? <span class="grad">Me conta.</span>', 'Os próximos simulados serão lançados de acordo com a procura. Escolha a certificação e receba o cupom de estreia quando ela chegar à Udemy.', opcoes=True)}
  </main>"""
    html += rodape(["vitrine.js", "quiz.js", "guia.js", "grafo.js", "social.js"])
    return html

# ---------------------------------------------------------------- página de cada certificação
def preparo(c):
    n = c["nivel"]
    dicas = {
        "Fundamentals": "Foque em vocabulário, categorias de serviço, casos de uso e no “quando usar o quê”. A prova cobra entendimento, não configuração.",
        "Associate": "Combine teoria com prática: crie uma conta gratuita ou use os laboratórios do Microsoft Learn e execute as tarefas de cada domínio.",
        "Expert": "Espere cenários longos e decisões de arquitetura com trade-offs. Revise requisitos de custo, segurança e disponibilidade em cada escolha.",
        "Specialty": "A prova é profunda em uma única carga de trabalho. Pratique implantações reais e conheça bem os limites e as integrações do produto.",
        "Business": "Pense como gestor: valor de negócio, adoção, governança e uso responsável. Use os recursos de IA no seu trabalho enquanto estuda.",
    }
    return dicas[n]

def secoes_extra(c):
    """Seções escritas à mão (conteudo_extra.py) para as certificações mais buscadas.
    Devolve (html, [(âncora, título do índice)])."""
    x = EXTRA.get(c["codigo"])
    if not x: return "", []
    cod = c["codigo"]
    def linka(txt):  # transforma códigos de outras certificações em links
        t = e(txt)
        return re.sub(r"\b([A-Z]{2}-\d{3})\b", lambda m: f'<a href="/certificacoes/{m.group(1).lower()}/">{m.group(1)}</a>' if m.group(1) in POR and m.group(1) != cod else m.group(1), t)
    linhas = "".join(f"<tr><th>Semana {i}<small>{e(t)}</small></th><td>{linka(o)}</td><td>{linka(p)}</td></tr>" for i, (t, o, p) in enumerate(x["semanas"], 1))
    conf = "".join(f"<div class=\"conf\"><b>{e(t)}</b><p>{linka(d)}</p></div>" for t, d in x["confusoes"])
    outro, tit, pars = x["compara"]
    comp = "".join(f"<p>{linka(p)}</p>" for p in pars)
    html = f"""
        <section id="plano" class="block reveal">
          <h2>Plano de estudo da {cod} em {len(x['semanas'])} semanas</h2>
          <p class="muted">Ritmo pensado para cerca de 1 hora por dia. Se você já trabalha com o assunto, junte semanas; se está começando do zero, estique.</p>
          <div class="table-wrap"><table class="tbl plano"><thead><tr><th>Semana</th><th>O que estudar</th><th>Como praticar</th></tr></thead><tbody>{linhas}</tbody></table></div>
        </section>
        <section id="confunde" class="block reveal">
          <h2>O que mais confunde na prova {cod}</h2>
          <div class="confs">{conf}</div>
          <p class="dica-prova"><b>Dica para o dia da prova:</b> {linka(x['dica'])}</p>
        </section>
        <section id="vale" class="block reveal">
          <h2>A {cod} vale a pena?</h2>
          <p>{linka(x['vale'])}</p>
        </section>
        <section id="compara" class="block reveal">
          <h2>{linka(tit)}</h2>
          {comp}
        </section>"""
    toc = [("plano", "Plano de estudo"), ("confunde", "O que mais confunde"), ("vale", "Vale a pena?"), ("compara", f"{cod} x {outro}")]
    return html, toc

def faq_cert(c):
    """Perguntas frequentes geradas com os dados reais de cada exame.
    Devolve [(pergunta, resposta_html, resposta_texto)] — o texto vai para o JSON-LD."""
    cod, nome = c["codigo"], c["nome"]
    nomes = lambda xs: ", ".join(f"{x} ({POR[x]['nomePt']})" for x in xs if x in POR)
    links = lambda xs: ", ".join(f'<a href="/certificacoes/{x.lower()}/">{x}</a> ({e(POR[x]["nomePt"])})' for x in xs if x in POR)
    itens = []
    def add(p, html, txt): itens.append((p, html, txt))

    # 1. Idioma
    if c["ptbr"]:
        t = f"Sim. A prova {cod} pode ser feita em português do Brasil, no centro de provas ou online, com supervisão remota."
    elif c["ptbr"] is False:
        t = f"Não. Hoje a prova {cod} é oferecida só em inglês (e em alguns outros idiomas, sem português). Quem não tem inglês fluente pode pedir tempo extra de 30 minutos ao agendar."
    else:
        t = f"Confirme na página oficial do exame {cod}, no Microsoft Learn, quais idiomas estão disponíveis no momento."
    add(f"A prova {cod} tem em português?", e(t), t)

    # 2. Duração e nota
    if c["minutos"]:
        t = f"A prova {cod} dura {c['minutos']} minutos e a nota mínima para passar é 700, numa escala de 1 a 1000."
    else:
        t = f"A nota mínima para passar na {cod} é 700, numa escala de 1 a 1000. A duração aparece na página oficial do exame no Microsoft Learn."
    add(f"Quanto tempo dura a prova {cod} e qual a nota para passar?", e(t), t)

    # 3. Pré-requisito
    if c["prereq"]:
        req = c["prereq"].rstrip(".")
        t = f"Sim. Para receber a certificação {nome}, é preciso {req[0].lower() + req[1:]}."
        h = e(t)
    elif c["antes"]:
        t = f"Não há pré-requisito obrigatório para a {cod}. Mesmo assim, ajuda ter feito antes {nomes(c['antes'])}."
        h = f"Não há pré-requisito obrigatório para a {cod}. Mesmo assim, ajuda ter feito antes {links(c['antes'])}."
    else:
        t = f"Não. A {cod} não tem pré-requisito e é um ponto de partida: dá para fazer sem nenhuma certificação anterior."
        h = e(t)
    add(f"Precisa de pré-requisito para a {cod}?", h, t)

    # 4. Validade
    if c["nivel"] == "Fundamentals":
        t = f"Não. As certificações Fundamentals, como a {cod}, não expiram."
    elif c["nivel"] == "Business":
        t = f"Confirme no Microsoft Learn as regras de validade da {nome}; as certificações de negócio seguem regras próprias."
    else:
        t = f"Sim, vale por um ano. A renovação é gratuita, feita online no Microsoft Learn nos seis meses antes do vencimento, sem precisar refazer a prova {cod}."
    add(f"A certificação {cod} expira?", e(t), t)

    # 5. O que mais cai
    if c["dominios"]:
        ord_ = sorted(c["dominios"], key=lambda d: -ponto_medio(d["peso"]))
        topo = [d for d in ord_ if ponto_medio(d["peso"]) == ponto_medio(ord_[0]["peso"])]
        if len(topo) == 1:
            t = f"O assunto com mais peso na {cod} é “{topo[0]['nome']}”, com {topo[0]['peso']} das questões. Ao todo, a prova cobre {len(c['dominios'])} áreas."
        else:
            t = f"As áreas com mais peso na {cod} são " + " e ".join(f"“{d['nome']}” ({d['peso']})" for d in topo) + f". Ao todo, a prova cobre {len(c['dominios'])} áreas."
        add(f"O que mais cai na prova {cod}?", e(t), t)

    # 6. Próximo passo
    if c["depois"]:
        ini = "o caminho mais comum é" if len(c["depois"]) == 1 else "os caminhos mais comuns são"
        t = f"Depois da {cod}, {ini} {nomes(c['depois'])}."
        h = f"Depois da {cod}, {ini} {links(c['depois'])}."
    else:
        t = f"A {cod} está no topo desta trilha. O próximo passo costuma ser uma certificação de outra área que complemente o seu trabalho."
        h = e(t)
    add(f"Qual certificação fazer depois da {cod}?", h, t)

    # 7. Simulado
    if cod in COM_SIMULADO:
        t = f"Sim. O simulado da {cod} na Udemy tem questões no estilo da prova real, com a explicação de cada alternativa em português, e costuma ter cupom de desconto nesta página."
    else:
        t = f"Ainda não há simulado da {cod} nesta página. Entre na lista no fim da página para receber o aviso e o cupom de estreia quando ele for lançado."
    add(f"Tem simulado da {cod} em português?", e(t), t)

    # 8. Aposentadoria / beta
    if c["status"] == "aposentando" and c["aposenta"]:
        t = f"Sim. A Microsoft vai aposentar a {cod} em {data_br(c['aposenta'])}. Quem já tem a certificação continua com ela até a data de validade."
        h = e(t)
        if c["depois"]:
            t += f" Para quem ainda vai estudar, vale olhar {nomes(c['depois'])}."
            h += f" Para quem ainda vai estudar, vale olhar {links(c['depois'])}."
        add(f"A {cod} vai ser aposentada?", h, t)
    elif c["status"] == "beta":
        t = f"Sim. A {cod} está em beta: o conteúdo ainda pode mudar e o resultado sai algumas semanas depois da prova, não na hora."
        add(f"A prova {cod} está em beta?", e(t), t)
    return itens

def pagina_cert(c):
    tn, ic = TRILHAS[c["trilha"]]
    dur = f'{c["minutos"]} minutos' if c["minutos"] else "Confirme na página do exame"
    idioma = "Disponível em português (Brasil)" if c["ptbr"] else ("Somente em inglês" if c["ptbr"] is False else "Confirme na página do exame")
    validade = {"Fundamentals": "Não expira"}.get(c["nivel"], "Renovação anual gratuita, online, no Microsoft Learn" if c["nivel"] != "Business" else "Confirme no Microsoft Learn")
    alerta = ""
    if c["status"] == "aposentando":
        alerta = f'<div class="alert reveal">⚠️ Esta certificação e o exame se aposentam em <b>{data_br(c["aposenta"])}</b>. Depois dessa data, não será possível obtê-la. {"Veja as alternativas em “Onde ela se encaixa”." if c["depois"] else ""}</div>'
    elif c["status"] == "beta":
        alerta = '<div class="alert info reveal">🧪 Exame em <b>beta</b>: o conteúdo ainda pode mudar e o resultado sai algumas semanas depois da prova.</div>'
    linhas = [("Selo", f'<img class="selo-sm" src="{c["selo"]}" alt="" width="44" height="44"> {e(c["nome"])}'), ("Certificação", e(c["nome"])), ("Código do exame", c["codigo"]), ("Nível", badge_nivel(c["nivel"])), ("Trilha", f"{ic} {e(tn)}"),
              ("Duração", dur), ("Nota mínima", "700 de 1000"), ("Idioma", idioma), ("Pré-requisito", e(c["prereq"]) if c["prereq"] else "Nenhum"),
              ("Validade", validade)]
    if c["guiaAtualizado"]: linhas.append(("Conteúdo da prova", f"Versão de {c['guiaAtualizado']}"))
    tabela = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in linhas)
    doms = ""
    for i, d in enumerate(c["dominios"], 1):
        tops = "".join(f"<li>{e(t)}</li>" for t in d["topicos"])
        doms += f"""
        <div class="dom reveal">
          <div class="dom-head"><span class="dom-n">{i:02d}</span><h3>{e(d['nome'])}</h3><span class="dom-w">{d['peso']}</span></div>
          <div class="bar"><i style="--w:{ponto_medio(d['peso'])}%"></i></div>
          {f'<ul class="dom-tops">{tops}</ul>' if tops else ''}
        </div>"""
    antes = "".join(link_cert(x) for x in c["antes"]) or '<span class="muted small">Ponto de partida, sem etapa anterior</span>'
    depois = "".join(link_cert(x) for x in c["depois"]) or '<span class="muted small">Topo desta trilha</span>'
    rel = [x for x in CERTS if x["trilha"] == c["trilha"] and x["codigo"] != c["codigo"]][:6]
    relacionadas = "".join(card_cert(x) for x in rel)
    toc = [("oque", "O que é"), ("resumo", "Resumo do exame"), ("publico", "Para quem é"), ("conteudo", "O que cai na prova"),
           ("preparar", "Como se preparar"), ("rota", "Onde ela se encaixa"), ("faq", "Perguntas frequentes"), ("links", "Links oficiais"), ("comentarios", "Comentários")]
    extra_html, extra_toc = secoes_extra(c)
    if extra_toc:
        i = [a for a, _ in toc].index("preparar") + 1
        toc = toc[:i] + extra_toc + toc[i:]
    tocs = "".join(f'<a href="#{a}">{b}</a>' for a, b in toc)
    curto = c['nome'].replace('Microsoft Certified: ', '').replace('Microsoft 365 Certified: ', '')
    url = f"{DOMINIO}/certificacoes/{c['id']}/"
    if c["codigo"] in COM_SIMULADO:
        titulo = f"{c['codigo']} {curto}: simulado e guia em português"
        if len(titulo) > 62: titulo = f"{c['codigo']}: simulado e guia em português ({ANO})"
        desc = f"Simulado da {c['codigo']} com explicação de cada alternativa e cupom na Udemy, mais o que cai na prova, pesos oficiais, duração e idioma."
    else:
        titulo = f"{c['codigo']} {curto}: o que cai na prova"
        if len(titulo) > 62: titulo = f"{c['codigo']}: guia da prova em português ({ANO})"
        desc = f"Guia da {c['codigo']} ({c['nomePt']}) em português: o que cai na prova com os pesos oficiais, duração, idioma, pré-requisitos e por onde começar a estudar."
    cred = {"@type": "EducationalOccupationalCredential", "@id": url + "#credencial", "name": c["nome"], "alternateName": c["codigo"],
            "credentialCategory": "certification", "educationalLevel": c["nivel"],
            "competencyRequired": [d["nome"] for d in c["dominios"]], "recognizedBy": {"@type": "Organization", "name": "Microsoft"}, "url": c["learn"]}
    art = {"@type": "Article", "@id": url + "#guia", "headline": titulo, "description": desc, "inLanguage": "pt-BR",
           "dateModified": date.today().isoformat(), "author": {"@id": f"{DOMINIO}/#raphael"}, "publisher": {"@id": f"{DOMINIO}/#raphael"},
           "isPartOf": {"@id": f"{DOMINIO}/#site"}, "image": f"{DOMINIO}/assets/og/{c['id']}.jpg", "about": {"@id": url + "#credencial"},
           "mainEntityOfPage": url}
    perguntas = faq_cert(c)
    faq_ld = {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": txt}} for p, _, txt in perguntas]}
    faq_html = "".join(f'<details class="faq-item"><summary>{e(p)}</summary><p>{h}</p></details>' for p, h, _ in perguntas)
    bc = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": DOMINIO + "/"},
        {"@type": "ListItem", "position": 2, "name": "Certificações", "item": DOMINIO + "/certificacoes/"},
        {"@type": "ListItem", "position": 3, "name": c["codigo"], "item": f"{DOMINIO}/certificacoes/{c['id']}/"}]}
    html = head(titulo, desc, f"/certificacoes/{c['id']}/",
                ld_script(PESSOA, SITE_LD, art, cred, bc, faq_ld),
                imagem=f"/assets/og/{c['id']}.jpg")
    html += f"""
  <main id="topo" data-cert="{c['id']}" class="cert-page t-{c['trilha']}">
    <section class="cert-hero">
      <nav class="crumbs reveal" aria-label="Você está em"><a href="/">Início</a><span>/</span><a href="/certificacoes/">Certificações</a><span>/</span><b>{c['codigo']}</b></nav>
      <div class="cert-hero-grid">
        <div>
          <div class="tags reveal">{badge_nivel(c['nivel'])}<span class="tag">{ic} {e(tn)}</span>{badge_status(c)}{chip_pt(c)}</div>
          <div class="cert-id reveal"><figure class="selo-hero"><img src="{c['selo']}" alt="Selo oficial {e(c['nome'])}" width="150" height="150"><figcaption>Selo oficial</figcaption></figure><div class="code-xl" aria-hidden="true">{c['codigo']}</div></div>
          <h1 class="reveal"><span class="sr-only">{c['codigo']}: </span>{e(c['nomePt'])}</h1>
          <p class="cname reveal">{e(c['nome'])}</p>
          <p class="lead reveal">{e(c['resumo'])}</p>
          <div class="ig reveal" data-social></div>
          {alerta}
        </div>
        <aside class="sim-box glass reveal" id="simBox" aria-live="polite"></aside>
      </div>
    </section>

    <div class="cert-layout">
      <nav class="toc" aria-label="Neste guia"><span class="eyebrow">Neste guia</span>{tocs}</nav>
      <article class="cert-body">
        <section id="oque" class="block reveal">
          <h2>O que é a {c['codigo']}</h2>
          <p>A <b>{e(c['nome'])}</b> é uma certificação de nível <b>{c['nivel']}</b> da trilha <b>{e(tn)}</b>. {e(c['resumo'])}</p>
        </section>
        <section id="resumo" class="block reveal">
          <h2>Resumo do exame</h2>
          <div class="table-wrap"><table class="tbl kv">{tabela}</table></div>
        </section>
        <section id="publico" class="block reveal">
          <h2>Para quem é</h2>
          <p>{e(c['publico'])}</p>
        </section>
        <section id="conteudo" class="block">
          <h2 class="reveal">O que cai na prova</h2>
          <p class="muted reveal">Áreas de conhecimento e pesos oficiais do guia de estudo da Microsoft{(' (versão de ' + c['guiaAtualizado'] + ')') if c['guiaAtualizado'] else ''}. Quanto maior o peso, mais questões.</p>
          <div class="doms">{doms}</div>
        </section>
        <section id="preparar" class="block reveal">
          <h2>Como se preparar</h2>
          <p>{preparo(c)}</p>
          <ol class="steps">
            <li><b>Leia o guia de estudo</b><span>Ele lista cada habilidade cobrada. Use a seção acima como mapa.</span></li>
            <li><b>Faça a trilha do Microsoft Learn</b><span>Os módulos gratuitos cobrem todo o conteúdo oficial.</span></li>
            <li><b>Treine com simulados</b><span>Questões no formato real mostram onde você ainda erra.</span></li>
            <li><b>Agende quando passar com folga</b><span>Mire em 800+ nos simulados antes de marcar a prova.</span></li>
          </ol>
        </section>
{extra_html}
        <section id="rota" class="block reveal">
          <h2>Onde ela se encaixa</h2>
          <div class="path graph" data-graph data-edges="{';'.join([f'{a}>{c["codigo"]}' for a in c['antes']] + [f'{c["codigo"]}>{b}' for b in c['depois']])}">
            <div class="pcol gcol"><small>Antes</small>{antes}</div>
            <div class="pcol gcol now"><small>Você está aqui</small><span class="pchip on" data-node="{c['codigo']}"><b>{c['codigo']}</b> {e(c['nomePt'])}</span></div>
            <div class="pcol gcol"><small>Próximo passo</small>{depois}</div>
          </div>
        </section>
        <section id="faq" class="block reveal">
          <h2>Perguntas frequentes sobre a {c['codigo']}</h2>
          <div class="faq">{faq_html}</div>
        </section>
        <section id="links" class="block reveal">
          <h2>Links oficiais</h2>
          <div class="links">
            <a class="olink" href="{c['learn']}" target="_blank" rel="noopener"><b>Página da certificação</b><span>Microsoft Learn ↗</span></a>
            <a class="olink" href="{c['guia']}" target="_blank" rel="noopener"><b>Guia de estudo {c['codigo']}</b><span>Habilidades medidas ↗</span></a>
            <a class="olink" href="{c['exame']}" target="_blank" rel="noopener"><b>Agendar o exame</b><span>Preço e datas ↗</span></a>
          </div>
          <p class="muted small">Guia independente, atualizado em {ATUALIZADO}. Datas, idiomas, preços e regras podem mudar: confirme no Microsoft Learn antes de se inscrever.</p>
        </section>
        <section id="comentarios" class="block" data-comentarios hidden></section>
      </article>
    </div>

    <section class="section" id="relacionadas">
      <header class="section-head reveal"><span class="eyebrow">Mesma trilha</span><h2>Outras certificações de {e(tn)}</h2></header>
      <div class="cgrid">{relacionadas}</div>
      <p style="margin-top:20px"><a class="btn btn-ghost" href="/certificacoes/">Ver todas as {len(CERTS)} certificações</a></p>
    </section>
{lead_form(f'Receba o cupom do simulado <span class="grad">{c["codigo"]}</span>.', f'Entre na lista para receber cupons e o aviso de lançamento do simulado {c["codigo"]} na Udemy.', codigo=c['codigo'])}
  </main>"""
    html += rodape(["cert.js", "grafo.js", "social.js"])
    return html

# ---------------------------------------------------------------- escrita
def grava(rel, conteudo):
    p = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(conteudo)

def atalho(destino):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Redirecionando…</title><link rel="canonical" href="{DOMINIO}{destino}">
<script>location.replace("{destino}" + location.search + location.hash);</script>
<meta http-equiv="refresh" content="0;url={destino}"></head><body><a href="{destino}">Continuar</a></body></html>
"""

if __name__ == "__main__":
    dados = dict(atualizado=ATUALIZADO, trilhas={k: dict(nome=v[0], icone=v[1]) for k, v in TRILHAS.items()},
                 certificacoes=[{k: c[k] for k in ("codigo", "id", "nomePt", "nome", "trilha", "nivel", "status", "aposenta", "resumo", "minutos", "ptbr", "antes", "depois", "selo")} for c in CERTS])
    grava("assets/certificacoes.json", json.dumps(dados, ensure_ascii=False, separators=(",", ":")))
    grava("certificacoes/index.html", pagina_guia())
    for c in CERTS:
        grava(f"certificacoes/{c['id']}/index.html", pagina_cert(c))
        grava(f"{c['id']}/index.html", atalho(f"/certificacoes/{c['id']}/"))
    hoje = date.today().isoformat()
    urls = ["/", "/certificacoes/"] + [f"/certificacoes/{c['id']}/" for c in CERTS]
    grava("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{DOMINIO}{u}</loc><lastmod>{hoje}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    grava("robots.txt", "# raphaelbarreto.com.br\nUser-agent: *\nAllow: /\n\n# Parâmetros que só mudam a visão da mesma página\n"
          f"Disallow: /*?metas=\nDisallow: /*?diag=\n\nSitemap: {DOMINIO}/sitemap.xml\n")
    print(f"OK: {len(CERTS)} páginas de certificação + guia + sitemap geradas em site/")
