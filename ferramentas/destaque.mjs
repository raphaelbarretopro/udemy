// Gera capas de destaque do Instagram (1080 x 1920) a partir de ferramentas/destaque.html.
// Uso: node ferramentas/destaque.mjs                → materiais/destaque-linha900.png
//      node ferramentas/destaque.mjs "AZ|900" "#2f8cff" "#7c5cff" destaque-az900.png
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
const [texto = "LINHA|900", c1 = "#2f8cff", c2 = "#ff9a3c", nome = "destaque-linha900.png"] = process.argv.slice(2);
const saida = path.join(RAIZ, "materiais");
mkdirSync(saida, { recursive: true });

const browser = await puppeteer.launch({ executablePath: NAVEGADORES.find(existsSync), headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
const url = pathToFileURL(path.join(AQUI, "destaque.html")).href + "?" + new URLSearchParams({ t: texto, c1, c2 });
await page.goto(url, { waitUntil: "networkidle0" });
await page.waitForSelector("body[data-pronto]");
const destino = path.join(saida, nome);
await (await page.$("#capa")).screenshot({ path: destino, type: "png" });
console.log("ok", destino);
await browser.close();
