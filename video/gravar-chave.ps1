# Grava a chave do Azure Speech em .env.local (na raiz do projeto) e confere se deu certo.
# A chave digitada fica oculta na tela e não é exibida em nenhum momento.
$raiz = Split-Path -Parent $PSScriptRoot
$arquivo = Join-Path $raiz ".env.local"

# Entrada visível: a colagem em campo oculto pode cortar caracteres em alguns terminais
$chave = (Read-Host "Cole a CHAVE 1 do Azure e tecle Enter").Trim()
Clear-Host

if ($chave.Length -ne 84 -and $chave.Length -ne 32) {
    Write-Host "A chave colada tem $($chave.Length) caracteres. As chaves do Azure Speech tem 84 (ou 32, nas mais antigas). Copie de novo pelo icone de copiar do portal e rode outra vez." -ForegroundColor Red
    exit 1
}
if ($chave.Length -lt 20) {
    Write-Host "Nada foi colado (ou a chave esta incompleta: $($chave.Length) caracteres). Copie a chave de novo no portal e rode outra vez." -ForegroundColor Red
    exit 1
}

$regiao = Read-Host "Regiao do recurso (tecle Enter para usar brazilsouth)"
if (-not $regiao.Trim()) { $regiao = "brazilsouth" }

$conteudo = @(
    "# Chave do Azure AI Speech (fica fora do GitHub, veja .gitignore)",
    "AZURE_SPEECH_KEY=$chave",
    "AZURE_SPEECH_REGION=$($regiao.Trim())"
)
[IO.File]::WriteAllLines($arquivo, $conteudo, (New-Object System.Text.UTF8Encoding $false))

# Conferência: relê o arquivo
$lida = ((Get-Content $arquivo | Where-Object { $_ -like "AZURE_SPEECH_KEY=*" }) -split "=", 2)[1]
if ($lida -eq $chave) {
    Write-Host "OK: chave gravada em .env.local ($($lida.Length) caracteres), regiao $($regiao.Trim())." -ForegroundColor Green
} else {
    Write-Host "Algo deu errado ao gravar o arquivo. Feche o Bloco de Notas se estiver aberto e rode de novo." -ForegroundColor Red
}
