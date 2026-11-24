# raphaelbarreto.com.br: simulados + guia de certificações Microsoft

Site estático (HTML + CSS + JS). A pasta `site/` é o que vai para o ar.

## Estrutura
| Página | Endereço | O que é |
|---|---|---|
| Início (link da bio) | `/` | Oferta da semana, simulados Microsoft e AWS, quiz, alerta de cupom, depoimentos |
| Guia de certificações | `/certificacoes/` | As 50 certificações Microsoft ativas (nov/2026) com filtros, busca, quiz, rotas, níveis e checklist |
| Página de cada certificação | `/certificacoes/az-104/` etc. | O que é, resumo do exame, para quem é, o que cai na prova (pesos oficiais), como se preparar, rota, links oficiais e caixa do simulado/cupom |

Atalhos curtos para stories: `/az-104`, `/sc-200`, `/pl-300`… (todas as 50) levam à página da certificação.
`/clf-c02`, `/aif-c01`, `/saa-c03`, `/cupons`, `/quiz` levam à home. `/microsoft` leva ao guia.
Todos mantêm os `utm_` para a medição. O guia também aceita filtro pela URL: `/certificacoes/?trilha=seguranca` ou `?nivel=Expert`.

## Antes de publicar
1. Abra `site/assets/dados.js` e:
   - coloque `modoDemo: false`;
   - preencha `codigo`, `validade` (AAAA-MM-DD) e `preco` dos cupons de cada simulado;
   - preencha `instagram`, `linkedin` e, se quiser, `foto` (ex.: `assets/raphael.jpg`, quadrada).
2. O formulário "Quero receber os cupons" grava no Supabase (tabela `inscritos`), usando a mesma
   configuração de `SOCIAL` em `dados.js`. Veja "Alerta de cupons" abaixo. A planilha do
   `apps-script/Codigo.gs` (`formEndpoint`) só é usada se o Supabase não estiver configurado.
3. (Opcional) Preencha `ga4` e/ou `metaPixel` para medir cliques e cadastros.

## Ajustes rápidos em `site/assets/dados.js`
- `foto`: sua foto (hoje `/assets/raphael.webp`; o original está em `originais/`).
- `mostrarAWS`: `false` esconde tudo da AWS (seção, quiz, depoimentos). `true` mostra de novo.
- `DEPOIMENTOS` e `NUMEROS_UDEMY`: textos e números reais que passam na faixa de avaliações.
- Os selos oficiais ficam em `site/assets/selos/` (baixados do Microsoft Learn) e são ligados a cada
  certificação automaticamente pelo `ferramentas/gerar.py`.

## Dia a dia
- **Trocar cupom:** edite só `dados.js` (código + validade). Home, guia, páginas de certificação e quiz
  usam o mesmo cupom automaticamente.
- **Oferta da semana:** mude `ofertaDaSemana` para o id do simulado (ex.: `"az-900"`).
- **Lançou um simulado novo:** em `dados.js`, troque `status: "em-breve"` por `"disponivel"` (ou crie um
  item novo com `id` igual ao código em minúsculas, ex.: `"az-104"`), preencha `cupom` e `cursos`.
  A página `/certificacoes/az-104/` passa a mostrar o simulado sozinha e o selo aparece no catálogo.
  Antes de lançar, veja no Supabase quem pediu aquele código ("Alerta de cupons" abaixo) e avise.

## Atualizar as certificações (quando a Microsoft mudar algo)
Os textos ficam em `ferramentas/conteudo_pt.py` e os dados oficiais (pesos, duração, idioma) em
`ferramentas/base_learn.json`. Depois de editar, gere as páginas de novo:
```
python ferramentas/gerar.py
```
Isso recria `site/certificacoes/`, os atalhos, `site/assets/certificacoes.json` (usado pelo quiz) e o `sitemap.xml`.

## Publicar com o domínio (grátis)
**Cloudflare Pages** ou **Netlify**: arraste a pasta `site/` em "Deploy manual", depois em
"Custom domains" adicione `raphaelbarreto.com.br` e `www` e siga as instruções de DNS que aparecem
(no Registro.br, troque os servidores DNS ou crie os registros indicados).
Depois, cadastre `https://raphaelbarreto.com.br/sitemap.xml` no Google Search Console.

## Testar no computador
```
python -m http.server 5173 --directory site
```
e abra http://localhost:5173

## Vídeo da Linha 900 (Reels)
Arquivos em `video/`. O vídeo final fica em `video/saida/linha900.mp4` (1080×1920, 30 fps, com narração).

| Arquivo | Para que serve |
|---|---|
| `roteiro.json` | texto de cada fala, voz (`pt-BR-MacerioMultilingualNeural`) e velocidade |
| `narrar.py` | gera a narração no Azure e a linha do tempo de cada fala |
| `cenas.html` + `cenas.js` | as animações (abra `cenas.html#play` para ver com áudio) |
| `gravar.mjs` | grava os quadros no Edge e monta o MP4 com o FFmpeg |
| `voz.py` | lista vozes e gera áudios avulsos |

Para refazer depois de mudar o roteiro ou as cenas:
```
python video/narrar.py
python -m http.server 5180
node video/gravar.mjs
```
(o segundo comando fica rodando em outra janela enquanto o terceiro grava).
A chave do Azure fica em `.env.local` (fora do GitHub). Para trocar a chave: `video/gravar-chave.ps1`.

## Stories na foto do site
Ao tocar na sua foto (topo da página e seção "Sobre"), abre um story em tela cheia, como no Instagram,
mas sem ligação com ele. O anel colorido pulsa enquanto houver story não visto e fica cinza depois que o
visitante viu todos (fica guardado no navegador dele).

**Publicar um story novo:**
1. Coloque o arquivo em `site/stories/`: vídeo `.mp4` vertical (1080×1920) ou imagem `.jpg`/`.png`/`.webp`.
   Para vídeos grandes, reduza o tamanho antes:
   ```
   ffmpeg -i original.mp4 -c:v libx264 -crf 27 -preset slow -pix_fmt yuv420p -c:a aac -b:a 112k -movflags +faststart site/stories/novo.mp4
   ```
2. Em `site/assets/dados.js`, na lista `window.STORIES`, adicione um item **no topo** (o mais novo primeiro):
   ```js
   { id: "dicas-sc900", tipo: "video", arquivo: "/stories/novo.mp4", capa: "/stories/novo-capa.jpg",
     data: "2026-12-01T19:00", botao: { texto: "Simulado SC-900", simulado: "sc-900" } },
   ```
   - `tipo: "imagem"` aceita `segundos: 6` (tempo na tela).
   - `ate: "2026-12-24"` faz o story sumir sozinho nessa data.
   - `botao` pode abrir um simulado com o cupom ativo (`simulado: "ai-901"`) ou um endereço (`link: "/certificacoes/az-900/"`).
3. Envie para o GitHub: o site é publicado sozinho.

Gestos no story: tocar à direita avança, à esquerda volta, segurar pausa, arrastar para baixo fecha.
No computador: setas, espaço (pausa) e Esc (fecha).

## Curtidas, comentários e compartilhamentos

Cada página de certificação tem uma barra no estilo do Instagram: ♡ curtir, 💬 comentar, 🔁 recomendar no LinkedIn, ↗ compartilhar e 🔖 salvar em "Minhas metas".

- **Compartilhar, recomendar e salvar** funcionam sem configuração. Os links levam `utm_source=<canal>` para você ver de onde veio cada visita no Analytics.
- **Curtidas e comentários** usam o Supabase (gratuito). Até configurar, esses dois botões ficam escondidos.

### Ativar o Supabase (uma vez)
1. Crie uma conta em https://supabase.com e um projeto novo (região São Paulo).
2. Abra **SQL Editor → New query**, cole o conteúdo de `supabase/social.sql` e clique em **Run**.
3. Em **Project Settings → API**, copie a **Project URL** e a chave **publishable** (ou **anon**). Não use a chave *secret* / *service_role*.
4. Cole as duas em `site/assets/dados.js`, em `window.SOCIAL`, e publique.

A chave publishable é pública de propósito: pelas regras do `social.sql`, ela só permite curtir, comentar e compartilhar.

### Moderar comentários
Os comentários chegam como pendentes. No Supabase, abra **Table Editor → comentarios**:
- marque **aprovado** para publicar;
- escreva na coluna **resposta** para responder (aparece com o selo "Instrutor");
- apague a linha para remover.

### Ver os números
No Supabase, abra **SQL Editor** e rode `select * from resumo;`. Aparece, por certificação: curtidas, **salvos em Minhas metas**, comentários aprovados e pendentes, e compartilhamentos (LinkedIn, WhatsApp e outros). A lista vem ordenada pelas mais salvas, um bom termômetro para escolher o próximo simulado. Esse resumo só você vê; o site não tem acesso a ele.

### Alerta de cupons (inscritos)
Quem preenche "Quero receber os cupons" vai para **Table Editor → inscritos**: nome, contato, tipo
(`email` ou `whatsapp`), provas de interesse, origem e data do aceite. O mesmo e-mail ou WhatsApp não
duplica: as provas novas são somadas ao cadastro. O site só consegue inscrever; ninguém lê a lista por ele.

    select * from inscritos_por_prova;                      -- quantos querem cada prova
    select nome, contato, tipo from inscritos
    where 'SC-900' = any(interesses) and not descadastrado; -- lista para avisar sobre a SC-900

Para exportar, use **Export → CSV** no resultado. Se alguém pedir para sair, marque `descadastrado = true`.

### Manter o projeto ativo
O plano gratuito pausa o projeto depois de 7 dias sem uso. A tarefa `.github/workflows/supabase-ativo.yml` consulta o banco duas vezes por semana para evitar isso.

### Imagens de prévia
Quando alguém compartilha uma página, aparece a imagem de `site/assets/og/<código>.jpg`. Para gerar de novo, depois de `python ferramentas/gerar.py`:

    node ferramentas/og.mjs          # todas
    node ferramentas/og.mjs az-104   # só uma
