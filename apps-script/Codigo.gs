/**
 * Recebe os cadastros do formulário "Alerta de cupom" e grava numa Planilha Google.
 *
 * Como instalar (5 minutos):
 * 1. Crie uma planilha nova no Google Sheets (ex.: "Leads simulados").
 * 2. Menu Extensões → Apps Script. Apague o conteúdo e cole este arquivo.
 * 3. Clique em Implantar → Nova implantação → tipo "App da Web".
 *      Executar como: Eu  ·  Quem pode acessar: Qualquer pessoa
 * 4. Autorize, copie a URL que termina em /exec e cole em
 *    site/assets/dados.js → formEndpoint: "https://script.google.com/macros/s/.../exec"
 */
const CAMPOS = ["data", "nome", "contato", "tipo", "interesses", "origem", "campanha", "pagina"];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const aba = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    if (aba.getLastRow() === 0) aba.appendRow(CAMPOS);
    const p = (e && e.parameter) || {};
    // Evita fórmulas injetadas na planilha
    const limpa = (v) => String(v || "").slice(0, 300).replace(/^[=+\-@]/, "'$&");
    aba.appendRow(CAMPOS.map((c) => limpa(p[c])));
    return ContentService.createTextOutput("ok");
  } finally {
    lock.releaseLock();
  }
}
