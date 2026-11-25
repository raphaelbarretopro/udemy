# Paleta oficial · raphaelbarreto.com.br

Vale para o site, as artes do Instagram, YouTube e LinkedIn, as capas de destaque e o banner.
Fechada em 25/11/2026. As cores da marca vêm de `site/assets/style.css` (`:root`) e as das trilhas de `site/assets/guia.css` (`.t-*`).

## Marca e fundo

| Uso | Hex | Variável no site |
| --- | --- | --- |
| Fundo principal | `#07080F` | `--bg` |
| Fundo 2 (cartões) | `#0D1020` | `--bg2` |
| Texto | `#EEF1FF` | `--ink` |
| Texto 2 (apoio) | `#A9B0CC` | `--ink2` |
| Texto 3 (legendas) | `#6F7695` | `--ink3` |
| Azul Microsoft (cor principal) | `#4F8CFF` | `--ms` |
| Violeta (par do azul nos degradês) | `#7C5CFF` | `--ms2` |
| Laranja (destaque quente) | `#FF9A3C` | `--aws` |
| Coral | `#FF5F6D` | `--aws2` |

Degradê da marca: `#4F8CFF → #7C5CFF` (botões) e `#7AA6FF → #B58CFF → #FFB070` (palavras em destaque nos títulos).

## Apoio (estados)

| Uso | Hex |
| --- | --- |
| Sucesso, preço, "disponível" | `#34D399` |
| Destaque, metas salvas, estrela | `#FBBF24` |
| Urgência ("por tempo limitado") | `#FF5F6D` |
| Curtida | `#FF3040` |

## Uma cor por certificação (linha 900)

A mesma cor aparece no guia do site (trilha), na capa de destaque e nas artes de cada prova.

| Certificação | Trilha | Cor | Hex |
| --- | --- | --- | --- |
| AZ-900 | Azure | Azul Microsoft | `#4F8CFF` |
| SC-900 | Segurança | Verde | `#34D399` |
| AI-901 | IA | Violeta | `#A78BFA` |
| DP-900 | Dados | Ciano | `#22D3EE` |
| PL-900 | Power Platform | Magenta | `#D946EF` |
| AB-900 | Microsoft 365 | Rosa | `#F472B6` |
| Linha 900 (geral) | — | Azul com toque de laranja | `#4F8CFF` + `#FF9A3C` |

Outras trilhas do site: Desenvolvimento `#38BDF8`, Dynamics 365 `#60A5FA`, Negócios `#FF9A3C`.

## Níveis (etiquetas do catálogo)

| Nível | Hex |
| --- | --- |
| Fundamentals | `#6EE7B7` |
| Associate | `#93C5FD` |
| Expert | `#FCD34D` |
| Specialty | `#F0ABFC` |
| Business | `#FDBA74` |

## Fontes

| Uso | Fonte |
| --- | --- |
| Títulos e números | Space Grotesk (500 a 700) |
| Texto | Inter (400 a 700) |
| Capas de destaque do Instagram | Lilita One |

## Regras rápidas

- Fundo sempre escuro (`#07080F`); texto branco; a cor da certificação só na palavra-chave ou no brilho.
- Sem logotipos da Microsoft nas artes (o site é independente); use só as siglas dos exames.
- Geradores que já seguem a paleta: `ferramentas/destaque.mjs` (capas de destaque), `ferramentas/banner.mjs` (banner do LinkedIn) e `ferramentas/og.mjs` (imagens de compartilhamento).

Comandos das capas de destaque:

```
node ferramentas/destaque.mjs "AZ-900" "#4f8cff" "#38bdf8" destaque-az900.png
node ferramentas/destaque.mjs "SC-900" "#34d399" "#6ee7b7" destaque-sc900.png
node ferramentas/destaque.mjs "AI-901" "#a78bfa" "#c4b5fd" destaque-ai901.png
node ferramentas/destaque.mjs "DP-900" "#22d3ee" "#67e8f9" destaque-dp900.png
node ferramentas/destaque.mjs "PL-900" "#d946ef" "#f0abfc" destaque-pl900.png
node ferramentas/destaque.mjs "AB-900" "#f472b6" "#f9a8d4" destaque-ab900.png
node ferramentas/destaque.mjs "LINHA|900" "#4f8cff" "#ff9a3c" destaque-linha900.png
```
