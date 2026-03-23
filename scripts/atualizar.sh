#!/bin/bash
# =============================================================
#  atualizar.sh — Atualiza data.json com editais FAPEAM + CNPq
#  Projeto: Editais Abertos Unificados — FVS-RCP / DEPI
# =============================================================
# Uso manual:
#   bash scripts/atualizar.sh
#
# Agendamento automático via crontab (a cada 20 dias, às 08h00):
#   crontab -e
#   Adicione a linha abaixo (ajuste o caminho):
#
#   0 8 */20 * * /bin/bash "/caminho/para/Editais-Abertos-Unificados-main/scripts/atualizar.sh" >> "/caminho/para/logs/unificado.log" 2>&1
#
#   Exemplo real:
#   0 8 */20 * * /bin/bash "/Users/walterolivasegundo/Downloads/Editais-Abertos-Unificados-main/scripts/atualizar.sh" >> "/Users/walterolivasegundo/Downloads/logs/unificado.log" 2>&1
#
#   Para verificar o cron ativo:   crontab -l
#   Para remover:                  crontab -e  (apague a linha)
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
echo "Concluído! data.json atualizado em: $PROJECT_DIR"
echo "Faça commit do novo data.json e publique no GitHub Pages."
echo "====================================="
