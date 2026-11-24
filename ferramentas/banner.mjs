// Gera o banner (capa) do LinkedIn, 1584 x 396, a partir de ferramentas/banner.html.
// Uso: node ferramentas/banner.mjs   →   materiais/linkedin-banner.png
// Usa o puppeteer-core já instalado em video/ (cd video && npm install).
import { createRequire } from "node:module";
import { existsSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const RAIZ = path.resolve(AQUI, "..");
const require = createRequire(path.join(RAIZ, "video", "package.json"));
const puppeteer = require("puppeteer-core");

const NAVEGADORES = [
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
];
const saida = path.join(RAIZ, "materiais");
mkdirSync(saida, { recursive: true });

const browser = await puppeteer.launch({ executablePath: NAVEGADORES.find(existsSync), headless: true, args: ["--allow-file-access-from-files"] });
const page = await browser.newPage();
await page.setViewport({ width: 1584, height: 396, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(AQUI, "banner.html")).href, { waitUntil: "networkidle0" });
await page.evaluate(() => document.fonts.ready);
const destino = path.join(saida, "linkedin-banner.png");
await (await page.$("#banner")).screenshot({ path: destino, type: "png" });
console.log("ok", destino);
await browser.close();
