# -*- coding: utf-8 -*-
"""
Gera a narração do vídeo a partir de video/roteiro.json:
  1. cada fala vira um áudio separado (Azure, voz do roteiro)
  2. mede a duração de cada um (ffprobe)
  3. monta a linha do tempo (início de cada fala) em video/audio/tempos.json e tempos.js
  4. junta tudo em video/audio/narracao.mp3

Uso: python video/narrar.py
"""
import json, os, sys, glob, shutil, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voz

AQUI = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(AQUI, "audio")

def ferramenta(nome):
    achado = shutil.which(nome)
    if achado: return achado
    base = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
    achados = glob.glob(os.path.join(base, "Gyan.FFmpeg*", "*", "bin", nome + ".exe"))
    if achados: return achados[0]
    sys.exit(f"{nome} não encontrado. Instale com: winget install --id Gyan.FFmpeg -e --source winget")

FFMPEG, FFPROBE = ferramenta("ffmpeg"), ferramenta("ffprobe")

def duracao(arq):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", arq], capture_output=True, text=True).stdout
    return float(out.strip())

def main():
    r = json.load(open(os.path.join(AQUI, "roteiro.json"), encoding="utf-8"))
    os.makedirs(os.path.join(AUDIO, "falas"), exist_ok=True)
    t = r["inicio"]; linha = []
    for f in r["falas"]:
        arq = os.path.join(AUDIO, "falas", f["id"] + ".mp3")
        ssml = (f'<speak version="1.0" xml:lang="pt-BR" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts">'
                f'<voice name="{r["voz"]}"><lang xml:lang="pt-BR"><prosody rate="{r["ritmo"]}">{f["texto"]}</prosody></lang></voice></speak>')
        bruto = arq.replace(".mp3", ".bruto.mp3")
        voz.sintetizar(ssml, bruto)
        # corta o silêncio do começo e do fim (deixa 60 ms de respiro)
        corte = ("silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.06,"
                 "areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.08,areverse")
        subprocess.run([FFMPEG, "-y", "-v", "error", "-i", bruto, "-af", corte, "-c:a", "libmp3lame", "-b:a", "192k", arq], check=True)
        os.remove(bruto)
        d = duracao(arq)
        linha.append({"id": f["id"], "cena": f["cena"], "inicio": round(t, 3), "dur": round(d, 3)})
        t += d + f["pausa"]
    total = round(t, 3)
    tempos = {"total": total, "falas": linha}
    json.dump(tempos, open(os.path.join(AUDIO, "tempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(AUDIO, "tempos.js"), "w", encoding="utf-8").write("window.TEMPOS = " + json.dumps(tempos, ensure_ascii=False) + ";\n")
    # junta as falas, cada uma no seu instante
    entradas, filtros = [], []
    for i, f in enumerate(linha):
        entradas += ["-i", os.path.join(AUDIO, "falas", f["id"] + ".mp3")]
        ms = int(f["inicio"] * 1000)
        filtros.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(linha))) + f"amix=inputs={len(linha)}:normalize=0,apad=whole_dur={total}[s]"
    subprocess.run([FFMPEG, "-y", "-v", "error", *entradas, "-filter_complex", ";".join(filtros) + ";" + mix,
                    "-map", "[s]", "-ar", "48000", "-c:a", "libmp3lame", "-b:a", "192k", os.path.join(AUDIO, "narracao.mp3")], check=True)
    print(f"Narração pronta: {total:.1f}s")
    for f in linha: print(f'  {f["inicio"]:6.2f}s  {f["dur"]:5.2f}s  {f["cena"]:7} {f["id"]}')

if __name__ == "__main__":
    main()
