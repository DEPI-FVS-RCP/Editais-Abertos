#!/bin/bash
# =============================================================
#  atualizar.sh — Atualiza data.json com editais FAPEAM + CNPq
#  e publica automaticamente no GitHub Pages (git commit + push)
#  Projeto: Editais Abertos Unificados — FVS-RCP / DEPI
# =============================================================
# Uso manual:
#   bash scripts/atualizar.sh
#
# Agendamento automático via crontab (a cada 10 dias, às 08h00):
#   crontab -e
#   Adicione a linha abaixo (ajuste o caminho):
#
#   0 8 */10 * * /bin/bash "/caminho/para/Editais-Abertos-Unificados-main/scripts/atualizar.sh" >> "/caminho/para/logs/unificado.log" 2>&1
#
#   Exemplo real:
#   0 8 */10 * * /bin/bash "/Users/walterolivasegundo/Downloads/Editais-Abertos-Unificados-main/scripts/atualizar.sh" >> "/Users/walterolivasegundo/Downloads/logs/unificado.log" 2>&1
#
#   Para verificar o cron ativo:   crontab -l
#   Para remover:                  crontab -e  (apague a linha)
#
# Requisito para o push automático funcionar sem pedir senha:
#   Rode "git push" manualmente UMA VEZ neste diretório, autenticando
#   normalmente (usuário + Personal Access Token, ou SSH). O macOS
#   guarda a credencial no Keychain e o cron reaproveita silenciosamente.
# =============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$(cd "$PROJECT_DIR/.." && pwd)/logs"

echo "====================================="
echo " Editais Unificados — atualizar.sh"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "====================================="

# Cria pasta de logs se não existir
mkdir -p "$LOG_DIR"

# Verifica Python3
if ! command -v python3 &>/dev/null; then
  echo "ERRO: python3 não encontrado. Instale com: brew install python3"
  exit 1
fi

# Instala dependências se necessário
echo "Verificando dependências Python..."
python3 -m pip install --quiet --upgrade requests beautifulsoup4 lxml

# Executa o scraper unificado
echo "Executando scraper..."
cd "$PROJECT_DIR"
python3 scripts/scrape_all.py

echo ""
echo "data.json atualizado em: $PROJECT_DIR"

# -------------------------------------------------------------
# Publicação automática (git commit + push)
# -------------------------------------------------------------
if [ -d "$PROJECT_DIR/.git" ]; then
  echo "Verificando alterações para publicar no GitHub..."
  cd "$PROJECT_DIR"

  if ! git diff --quiet -- data.json || ! git diff --cached --quiet -- data.json; then
    git add data.json
    git commit -q -m "Atualização automática de editais — $(date '+%Y-%m-%d %H:%M')"

    if git push origin main 2>>"$LOG_DIR/unificado.log"; then
      echo "Publicado no GitHub com sucesso."
    else
      echo "AVISO: 'git push' falhou (provável falta de credencial salva)."
      echo "Rode 'git push' manualmente uma vez nesta pasta para salvar a credencial no Keychain."
    fi
  else
    echo "Nenhuma mudança em data.json — nada para publicar (editais continuam os mesmos)."
  fi
else
  echo "AVISO: pasta não é um repositório git — publicação automática pulada."
  echo "Rode 'git init' / 'git remote add origin ...' nesta pasta para habilitar."
fi

echo "====================================="
