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
2. Instale o formulário na planilha: siga as instruções no topo de `apps-script/Codigo.gs`
   e cole a URL `/exec` em `formEndpoint`. Todos os formulários do site gravam na mesma planilha;
   a coluna `interesses` diz qual certificação a pessoa quer.
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
  Antes de lançar, filtre a planilha por aquele código e avise quem pediu.

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
