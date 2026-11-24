// Grava o vídeo: abre cenas.html no Edge, tira uma foto de cada quadro e envia ao FFmpeg com a narração.
// Antes: servidor na raiz do projeto (python -m http.server 5180) e narração gerada (python video/narrar.py).
// Uso: node video/gravar.mjs            -> video/saida/linha900.mp4
//      node video/gravar.mjs 10 14      -> só o trecho de 10s a 14s (teste rápido)
import puppeteer from "puppeteer-core";
import { spawn } from "node:child_process";
import { existsSync, mkdirSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const FPS = 30;
const URL = process.env.VIDEO_URL || "http://localhost:5180/video/cenas.html";

function acharFFmpeg() {
  const base = path.join(process.env.LOCALAPPDATA || "", "Microsoft", "WinGet", "Packages");
  if (existsSync(base)) for (const d of readdirSync(base).filter(n => n.startsWith("Gyan.FFmpeg"))) {
    for (const sub of readdirSync(path.join(base, d))) {
      const p = path.join(base, d, sub, "bin", "ffmpeg.exe");
      if (existsSync(p)) return p;
    }
  }
  return "ffmpeg";
}
const NAVEGADORES = [
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
];

const [ini, fim] = process.argv.slice(2).map(Number);
const browser = await puppeteer.launch({
  executablePath: NAVEGADORES.find(existsSync), headless: true,
  args: ["--hide-scrollbars", "--force-color-profile=srgb", "--disable-gpu-vsync"]
});
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
await page.goto(URL, { waitUntil: "networkidle0" });
const total = await page.evaluate(async () => { await window.pronto; return window.DURACAO; });
const t0 = Number.isFinite(ini) ? ini : 0, t1 = Number.isFinite(fim) ? fim : total;
const n = Math.round((t1 - t0) * FPS);

mkdirSync(path.join(AQUI, "saida"), { recursive: true });
const saida = path.join(AQUI, "saida", Number.isFinite(ini) ? `trecho-${t0}-${t1}.mp4` : "linha900.mp4");
const ff = spawn(acharFFmpeg(), [
  "-y", "-v", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
  "-ss", String(t0), "-t", String(t1 - t0), "-i", path.join(AQUI, "audio", "narracao.mp3"),
  "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
  "-r", String(FPS), "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", saida
], { stdio: ["pipe", "inherit", "inherit"] });

const stage = await page.$("#stage");
const inicio = Date.now();
for (let i = 0; i < n; i++) {
  const t = t0 + i / FPS;
  await page.evaluate((t) => window.seek(t), t);
  const buf = await stage.screenshot({ type: "jpeg", quality: 93 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
  if (i % 60 === 0) process.stdout.write(`quadro ${i}/${n} (${t.toFixed(1)}s)\n`);
}
ff.stdin.end();
await new Promise((r, j) => ff.on("close", c => c === 0 ? r() : j(new Error("FFmpeg falhou: " + c))));
await browser.close();
console.log(`Pronto: ${saida} (${n} quadros em ${((Date.now() - inicio) / 1000).toFixed(0)}s)`);
