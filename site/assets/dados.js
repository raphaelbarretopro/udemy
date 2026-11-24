/* =====================================================================
   DADOS DO SITE — é só este arquivo que você precisa editar no dia a dia.
   ---------------------------------------------------------------------
   • Para trocar um cupom: altere "codigo" e "validade" (AAAA-MM-DD).
   • Cupom vazio ("") = o botão abre a Udemy sem cupom.
   • Para lançar PL-900 / DP-900 / AB-900: mude status para "disponivel"
     e preencha a lista "cursos" com o link da Udemy.
   ===================================================================== */

window.SITE = {
  /* true = mostra cupons de EXEMPLO para visualizar o layout.
     Coloque false antes de publicar com os cupons reais. */
  modoDemo: false,

  nome: "Raphael Barreto",
  udemyPerfil: "https://www.udemy.com/user/raphael-barreto-de-oliveira-2/",

  /* Deixe "" para esconder o ícone */
  instagram: "",   // ex.: "https://instagram.com/seuperfil"
  linkedin: "",    // ex.: "https://linkedin.com/in/seuperfil"
  foto: "/assets/raphael.webp",  // quadrada. Vazio = monograma RB

  /* false = esconde tudo da AWS (seção, quiz, faixa, depoimentos). true = mostra de novo. */
  mostrarAWS: false,

  /* URL do Google Apps Script que grava os contatos na planilha
     (veja apps-script/Codigo.gs e o LEIA-ME). */
  formEndpoint: "",

  /* Opcional: medição */
  ga4: "",         // ex.: "G-XXXXXXX"
  metaPixel: "",   // ex.: "123456789012345"

  /* Simulado em destaque na "Oferta da semana" (id de um item abaixo) */
  ofertaDaSemana: "ai-901",

  precoOriginal: "R$ 79,90",

  /* "questoes" é calculado sozinho a partir dos simulados visíveis */
  stats: { alunos: 360, avaliacoes: 58, certificacoes: 50 }
};

window.SIMULADOS = [
  /* ------------------------- MICROSOFT · LINHA 900 ------------------------- */
  {
    id: "az-900", trilha: "microsoft", codigo: "AZ-900",
    nome: "Azure Fundamentals",
    resumo: "Conceitos de nuvem, serviços do Azure, governança e custos.",
    nivel: "Iniciante", status: "disponivel",
    /* Cupom GRATUITO segmentado criado em 23/11/2026: 100 resgates, termina 24/12/2026 16:30 PST (21:30 de Brasília).
       "nota" aparece embaixo do cupom. */
    cupom: { codigo: "AZ-900-GRATIS", validade: "2026-12-24T21:30:00-03:00", preco: "Grátis",
             nota: "Limitado a 100 resgates: quando acabarem, a Udemy mostra o preço normal." },
    cursos: [
      { rotulo: "Simulado AZ-900", questoes: 142,
        url: "https://www.udemy.com/course/simulado-az-900-preparatorio-para-o-exame-de-certificacao/" }
    ]
  },
  {
    id: "sc-900", trilha: "microsoft", codigo: "SC-900",
    nome: "Security, Compliance & Identity",
    resumo: "Zero Trust, Microsoft Entra, Defender e Purview.",
    nivel: "Iniciante", status: "disponivel", maisVendido: true,
    nota: 4.8, avaliacoes: 45, alunos: 352,
    /* Cupom "melhor preço" criado em 23/11/2026, termina 28/11/2026 16:21 PST (21:21 de Brasília) */
    cupom: { codigo: "SIMULADO-SC-900", validade: "2026-11-28T21:21:00-03:00", preco: "R$ 24,90" },
    cursos: [
      { rotulo: "Simulado SC-900 · 6 testes", questoes: 249,
        url: "https://www.udemy.com/course/simulado-sc-900-preparatorio-para-o-exame-de-certificacao/" },
      /* cupom: "" = este curso ainda não tem cupom próprio (cada curso da Udemy precisa do seu) */
      { rotulo: "SC-900 BÔNUS", questoes: 109, cupom: "",
        url: "https://www.udemy.com/course/simulado-sc-900-preparatorio-para-o-exame-bonus/" }
    ]
  },
  {
    id: "ai-901", trilha: "microsoft", codigo: "AI-901",
    nome: "Azure AI Fundamentals",
    resumo: "IA no Azure com Microsoft Foundry, alinhado ao novo guia do exame.",
    nivel: "Iniciante", status: "disponivel", novo: true,
    /* Cupom GRATUITO com o código padrão da Udemy (criado em 23/11/2026).
       Validade não informada: preencha "validade" para ligar a contagem regressiva.
       Cupom pago anterior (até 28/11): SIMULADO-AI-901 */
    cupom: { codigo: "87C4F93DA6FAB1E2E769", validade: "", preco: "Grátis",
             nota: "Cupom gratuito com vagas limitadas: quando acabarem, a Udemy mostra o preço normal." },
    cursos: [
      { rotulo: "Simulados AI-901", questoes: 128,
        url: "https://www.udemy.com/course/simulados-ai-901-microsoft-azure-ai-fundamentals-2026-y/" }
    ]
  },
  {
    id: "pl-900", trilha: "microsoft", codigo: "PL-900",
    nome: "Power Platform Fundamentals",
    resumo: "Power Apps, Power Automate, Power BI e Copilot Studio.",
    nivel: "Iniciante", status: "em-breve", cursos: []
  },
  {
    id: "dp-900", trilha: "microsoft", codigo: "DP-900",
    nome: "Azure Data Fundamentals",
    resumo: "Dados relacionais, não relacionais e análise no Azure.",
    nivel: "Iniciante", status: "em-breve", cursos: []
  },
  {
    id: "ab-900", trilha: "microsoft", codigo: "AB-900",
    nome: "Microsoft 365 Copilot & Agents",
    resumo: "Administração do Microsoft 365 Copilot e de agentes.",
    nivel: "Iniciante", status: "em-breve", cursos: []
  },

  /* ---------------------------------- AWS ---------------------------------- */
  {
    id: "clf-c02", trilha: "aws", codigo: "CLF-C02",
    nome: "Cloud Practitioner",
    resumo: "A porta de entrada da AWS: serviços, segurança, preços e suporte.",
    nivel: "Iniciante", status: "disponivel",
    nota: 5.0, avaliacoes: 3,
    cupom: { codigo: "", validade: "", preco: "R$ 24,90" },
    cursos: [
      { rotulo: "Simulado CLF-C02", questoes: 360,
        url: "https://www.udemy.com/course/simulado-aws-cloud-pratitioner-clf-c02/" },
      { rotulo: "CLF-C02 BÔNUS", questoes: 339,
        url: "https://www.udemy.com/course/simulado-aws-cloud-pratitioner-clf-c02-bonus/" }
    ]
  },
  {
    id: "aif-c01", trilha: "aws", codigo: "AIF-C01",
    nome: "AI Practitioner",
    resumo: "IA/ML na AWS: serviços prontos, Bedrock, SageMaker e IA responsável.",
    nivel: "Iniciante", status: "disponivel",
    nota: 5.0, avaliacoes: 1,
    cupom: { codigo: "", validade: "", preco: "R$ 24,90" },
    cursos: [
      { rotulo: "Simulado AIF-C01", questoes: 318,
        url: "https://www.udemy.com/course/simulado-aws-certified-ai-practitioner-aif-c01/" }
    ]
  },
  {
    id: "saa-c03", trilha: "aws", codigo: "SAA-C03",
    nome: "Solutions Architect – Associate",
    resumo: "Trilha em 3 volumes para arquitetar soluções resilientes e seguras.",
    nivel: "Intermediário", status: "disponivel",
    cupom: { codigo: "", validade: "", preco: "R$ 24,90" },
    cursos: [
      { rotulo: "Volume 1", questoes: 360,
        url: "https://www.udemy.com/course/simulado-aws-certified-solutions-architect-associate-saa-c/" },
      { rotulo: "Volume 2", questoes: 360,
        url: "https://www.udemy.com/course/simulado-aws-certified-solutions-architect-associate-saa-c-l/" },
      { rotulo: "Volume 3", questoes: 278,
        url: "https://www.udemy.com/course/simulado-aws-certified-solutions-architect-associate-saa-c-i/" }
    ]
  }
];

/* Avaliações reais de alunos na Udemy (todas as avaliações escritas com 4★ ou mais;
   nome abreviado por privacidade). "trilha: aws" some quando mostrarAWS = false. */
window.DEPOIMENTOS = [
  { nome: "Victor H.", exame: "SC-900", nota: 5, data: "10/2026",
    texto: "Fui aprovado hoje na SC-900 com 809 pontos. Esses simulados ajudaram muito. Só com o simulado do Microsoft Learn seria complicado ter base do meu nível de preparo real." },
  { nome: "Anne K.", exame: "SC-900", nota: 5, data: "10/2026",
    texto: "Esse simulado foi essencial para minha aprovação! Muitas perguntas parecidas e a implantação da IA nas perguntas para explicação está perfeito." },
  { nome: "J. Brandão", exame: "SC-900 BÔNUS", nota: 5, data: "05/2025",
    texto: "Estes simulados foram muito importantes para a aprovação no exame." },
  { nome: "Rodrigo L.", exame: "SC-900 BÔNUS", nota: 5, data: "04/2025",
    texto: "Excelentes simulados, condizem com as questões das provas." },
  { nome: "Carlos S.", exame: "SC-900 BÔNUS", nota: 5, data: "04/2025",
    texto: "Excelente simulado!" },
  { nome: "Fabricio C.", exame: "CLF-C02", nota: 5, trilha: "aws", data: "11/2025",
    texto: "Questões com grau de dificuldade semelhante às do exame de certificação AWS. Recomendo!" },
  { nome: "Fabricio C.", exame: "CLF-C02 BÔNUS", nota: 5, trilha: "aws", data: "11/2025",
    texto: "Material espetacular para estudos referentes a esta certificação." }
];

/* Números reais da Udemy exibidos entre os depoimentos */
window.NUMEROS_UDEMY = [
  { grande: "4,8★", texto: "nota média do simulado SC-900", pequeno: "45 avaliações na Udemy" },
  { grande: "352", texto: "alunos no simulado SC-900", pequeno: "o mais vendido" },
  { grande: "4,9★", texto: "nota do SC-900 BÔNUS", pequeno: "6 avaliações" },
  { grande: "809", texto: "pontos na prova oficial", pequeno: "aluno aprovado na SC-900" }
];

/* =====================================================================
   STORIES (abrem ao tocar na sua foto, no topo da página)
   ---------------------------------------------------------------------
   Para publicar um story novo:
   1. Coloque o arquivo em site/stories/ (vídeo .mp4 vertical 1080x1920 ou imagem .jpg/.png/.webp).
   2. Adicione um item NO TOPO da lista abaixo (o mais novo primeiro).
   Campos:
     id        nome único (use letras, números e hífen)
     tipo      "video" ou "imagem"
     arquivo   caminho do arquivo
     capa      (opcional, vídeos) imagem mostrada enquanto o vídeo carrega
     data      data e hora da publicação, ex.: "2026-11-23T20:00"
     segundos  (opcional, imagens) quanto tempo a imagem fica na tela. Padrão: 6
     ate       (opcional) data em que o story some sozinho, ex.: "2026-12-24"
     botao     (opcional) botão de link na parte de baixo:
                 { texto: "…", simulado: "ai-901" }  -> abre o simulado com o cupom ativo
                 { texto: "…", link: "/certificacoes/az-900/" } -> abre um endereço
   Os stories já vistos ficam marcados no navegador do visitante: quando ele viu todos,
   o anel da foto fica cinza (como no Instagram). Um story novo faz o anel colorir de novo.
   ===================================================================== */
window.STORIES = [
  {
    id: "linha900-reels",
    tipo: "video",
    arquivo: "/stories/linha900.mp4",
    capa: "/stories/linha900-capa.jpg",
    data: "2026-11-23T23:15",
    botao: { texto: "Simulado AI-901 grátis", simulado: "ai-901" }
  }
];
