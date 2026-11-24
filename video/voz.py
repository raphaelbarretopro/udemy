# -*- coding: utf-8 -*-
"""
Gera narração com as vozes neurais do Azure AI Speech (sem dependências extras).
A chave é lida de .env.local (na raiz do projeto) e nunca é impressa.

Uso:
  python video/voz.py vozes                         -> lista as vozes pt-BR disponíveis
  python video/voz.py falar VOZ "texto" saida.mp3   -> gera um áudio
  python video/voz.py ssml arquivo.xml saida.mp3     -> gera a partir de um SSML pronto
"""
import os, sys, json, urllib.request, html

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def credenciais():
    cfg = {}
    with open(os.path.join(RAIZ, ".env.local"), encoding="utf-8-sig") as f:
        for linha in f:
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                k, v = linha.split("=", 1)
                cfg[k.strip()] = v.strip().strip('"').strip("'")
    chave, regiao = cfg.get("AZURE_SPEECH_KEY", ""), cfg.get("AZURE_SPEECH_REGION", "")
    if not chave or "cole-aqui" in chave or not regiao:
        sys.exit("Preencha AZURE_SPEECH_KEY e AZURE_SPEECH_REGION em .env.local")
    return chave, regiao

def pedido(url, chave, dados=None, cabecalhos=None):
    req = urllib.request.Request(url, data=dados, headers={"Ocp-Apim-Subscription-Key": chave, "User-Agent": "video-raphael", **(cabecalhos or {})})
    try:
        return urllib.request.urlopen(req, timeout=60).read()
    except urllib.error.HTTPError as e:
        sys.exit(f"Erro do Azure: HTTP {e.code} {e.reason}")

def vozes():
    chave, regiao = credenciais()
    lista = json.loads(pedido(f"https://{regiao}.tts.speech.microsoft.com/cognitiveservices/voices/list", chave))
    for v in lista:
        if v.get("Locale") == "pt-BR" or "pt-BR" in v.get("SecondaryLocaleList", []):
            print(f'{v["ShortName"]:42} {v.get("Gender",""):7} {v.get("VoiceType","")}  estilos: {",".join(v.get("StyleList", []))}')

def sintetizar(ssml, saida):
    chave, regiao = credenciais()
    audio = pedido(f"https://{regiao}.tts.speech.microsoft.com/cognitiveservices/v1", chave, ssml.encode("utf-8"),
                   {"Content-Type": "application/ssml+xml", "X-Microsoft-OutputFormat": "audio-48khz-192kbitrate-mono-mp3"})
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    open(saida, "wb").write(audio)
    print(f"OK: {saida} ({len(audio)//1024} KB)")

def falar(voz, texto, saida, ritmo="+0%"):
    ssml = (f'<speak version="1.0" xml:lang="pt-BR" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts">'
            f'<voice name="{voz}"><prosody rate="{ritmo}">{html.escape(texto)}</prosody></voice></speak>')
    sintetizar(ssml, saida)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "vozes": vozes()
    elif cmd == "falar": falar(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "+0%")
    elif cmd == "ssml": sintetizar(open(sys.argv[2], encoding="utf-8").read(), sys.argv[3])
    else: print(__doc__)
