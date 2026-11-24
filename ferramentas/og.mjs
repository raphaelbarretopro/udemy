// Gera as imagens de prévia (1200x630) que aparecem quando alguém compartilha
// uma página no WhatsApp, LinkedIn, Facebook etc.
// Uso (depois de python ferramentas/gerar.py):  node ferramentas/og.mjs
// Saída: site/assets/og/<id>.jpg e site/assets/og/certificacoes.jpg
// Usa o puppeteer-core já instalado em video/ (cd video && npm install).
import { createRequire } from "node:module";
import { existsSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const RAIZ = path.resolve(AQUI, "..");
const SITE = path.join(RAIZ, "site");
const require = createRequire(path.join(RAIZ, "video", "package.json"));
const puppeteer = require("puppeteer-core");

const NAVEGADORES = [
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
];
const arq = (web) => pathToFileURL(path.join(SITE, web)).href;

const dados = JSON.parse(readFileSync(path.join(SITE, "assets", "certificacoes.json"), "utf8"));
const saida = path.join(SITE, "assets", "og");
mkdirSync(saida, { recursive: true });

const so = process.argv[2]; // opcional: gerar só um id (ex.: az-104)
const browser = await puppeteer.launch({ executablePath: NAVEGADORES.find(existsSync), headless: true, args: ["--allow-file-access-from-files"] });
const page = await browser.newPage();
await page.setViewport({ width: 1200, height: 630, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(AQUI, "og.html")).href, { waitUntil: "networkidle0" });
const foto = arq("assets/raphael.webp");

async function foto_(nome, d) {
  await page.evaluate((d) => window.render(d), d);
  await (await page.$("#card")).screenshot({ path: path.join(saida, nome), type: "jpeg", quality: 86 });
  console.log("ok", nome);
}

if (!so) {
  const selos = [...new Set(dados.certificacoes.map(c => c.selo))].slice(0, 6).map(arq);
  await foto_("certificacoes.jpg", { tipo: "catalogo", total: dados.certificacoes.length, atualizado: dados.atualizado, selos, foto });
}
for (const c of dados.certificacoes) {
  if (so && c.id !== so) continue;
  await foto_(`${c.id}.jpg`, {
    codigo: c.codigo, nomePt: c.nomePt, nivel: c.nivel, trilha: dados.trilhas[c.trilha].nome,
    selo: arq(c.selo), foto
  });
}
await browser.close();
