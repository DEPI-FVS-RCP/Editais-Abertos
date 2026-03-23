#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Atualiza um único data.json com editais abertos da FAPEAM e do CNPq.

Uso:
  python3 scripts/scrape_all.py

Saída:
  data.json na raiz do projeto, pronto para o GitHub Pages.

Fallback manual:
  Se o scraping falhar (site fora do ar ou mudança de layout), edite
  scripts/seed_fapeam.json (lista de URLs) ou scripts/seed_cnpq.json
  (lista de {title, url}) e rode novamente.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0 Safari/537.36"
}

ROOT         = Path(__file__).resolve().parents[1]
OUT_JSON     = ROOT / 'data.json'
SEED_FAPEAM  = Path(__file__).resolve().parent / 'seed_fapeam.json'
SEED_CNPQ    = Path(__file__).resolve().parent / 'seed_cnpq.json'

CNPQ_URL   = 'https://www.gov.br/cnpq/pt-br/chamadas/abertas-para-submissao'
FAPEAM_URL = 'https://www.fapeam.am.gov.br/editais/?aba=editais-abertos'

DATE_RANGE_RE    = re.compile(r'(\d{2}/\d{2}/\d{4})\s*a\s*(\d{2}/\d{2}/\d{4})', re.I)
RE_VIGENCIA_RANGE = re.compile(
    r'(vig[eê]ncia)\s*:\s*(\d{2}/\d{2}/\d{4})\s*(a|à|-|até)\s*(\d{2}/\d{2}/\d{4})',
    flags=re.IGNORECASE
)
RE_ANY_DATE = re.compile(r'\b(\d{2}/\d{2}/\d{4})\b')


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def fetch(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=40)
    r.raise_for_status()
    return r.text


def ddmmyyyy_to_iso(s: str) -> str:
    try:
        return datetime.strptime(s, '%d/%m/%Y').date().isoformat()
    except Exception:
        return ''


def normalize_space(s: str) -> str:
    return ' '.join((s or '').split())


def guess_type(title: str, default='Edital') -> str:
    t = (title or '').lower()
    if 'chamada' in t:
        return 'Chamada Pública'
    if 'programa' in t:
        return 'Programa'
    if 'bolsa' in t:
        return 'Bolsa'
    return default


# ---------------------------------------------------------------------------
# Seeds de fallback
# ---------------------------------------------------------------------------

def load_seed_fapeam() -> list:
    """Retorna lista de URLs do seed_fapeam.json (fallback manual)."""
    if not SEED_FAPEAM.exists():
        return []
    try:
        data = json.loads(SEED_FAPEAM.read_text(encoding='utf-8'))
    except Exception:
        return []
    if isinstance(data, dict) and 'urls' in data:
        return [u for u in data['urls'] if isinstance(u, str) and u.startswith('http')]
    if isinstance(data, list):
        return [u for u in data if isinstance(u, str) and u.startswith('http')]
    return []


def load_seed_cnpq() -> list:
    """Retorna lista de {title, url} do seed_cnpq.json (fallback manual)."""
    if not SEED_CNPQ.exists():
        return []
    try:
        data = json.loads(SEED_CNPQ.read_text(encoding='utf-8'))
    except Exception:
        return []
    if isinstance(data, dict) and 'items' in data:
        return [it for it in data['items'] if it.get('title') and it.get('url')]
    return []


# ---------------------------------------------------------------------------
# CNPq
# ---------------------------------------------------------------------------

def scrape_cnpq() -> list:
    print('CNPq: iniciando scraping...')
    base_items = []
    try:
        html = fetch(CNPQ_URL)
        soup = BeautifulSoup(html, 'html.parser')
        seen = set()
        for h2 in soup.find_all('h2'):
            a = h2.find('a', href=True)
            if not a:
                continue
            title = normalize_space(a.get_text(' ', strip=True))
            if not title:
                continue
            url = urljoin(CNPQ_URL, a['href'].strip())
            if url not in seen:
                seen.add(url)
                base_items.append({'title': title, 'url': url})
        print(f'  CNPq: {len(base_items)} itens encontrados na lista.')
    except Exception as e:
        print(f'  AVISO CNPq: falha ao raspar lista — {e}')

    # Fallback: seed manual
    if not base_items:
        seed = load_seed_cnpq()
        if seed:
            print(f'  CNPq: usando seed_cnpq.json ({len(seed)} itens).')
            base_items = seed
        else:
            print('  AVISO CNPq: sem itens (scraping falhou e seed vazio).')

    items = []
    for it in base_items:
        date = ''
        try:
            detail = fetch(it['url'])
            txt = BeautifulSoup(detail, 'html.parser').get_text('\n', strip=True)
            m = DATE_RANGE_RE.search(txt)
            if m:
                date = ddmmyyyy_to_iso(m.group(2))
        except Exception as e:
            print(f'  AVISO CNPq prazo: {it["url"][:70]} — {e}')
        items.append({
            'source_system': 'CNPq',
            'title': it['title'],
            'url': it['url'],
            'area': 'Geral',
            'type': 'Chamada Pública',
            'date': date,
        })
        print(f'  CNPq OK: {it["title"][:70]}')
    return items


# ---------------------------------------------------------------------------
# FAPEAM
# ---------------------------------------------------------------------------

def extract_vigencia(text: str) -> str:
    if not text:
        return ''
    m = RE_VIGENCIA_RANGE.search(text)
    if m:
        return ddmmyyyy_to_iso(m.group(4))
    dates = RE_ANY_DATE.findall(text)
    if len(dates) >= 2:
        return ddmmyyyy_to_iso(dates[1])
    return ''


def extract_title_fapeam(soup: BeautifulSoup) -> str:
    """Extrai título da página de edital: H1 → og:title → <title>."""
    h1 = soup.find('h1')
    if h1 and h1.get_text(strip=True):
        return normalize_space(h1.get_text(' ', strip=True))
    og = soup.find('meta', property='og:title')
    if og and og.get('content'):
        return normalize_space(og['content'])
    if soup.title and soup.title.get_text(strip=True):
        return normalize_space(soup.title.get_text(strip=True))
    return 'Edital'


def scrape_fapeam() -> list:
    print('FAPEAM: iniciando scraping...')
    unique_urls = []
    try:
        html = fetch(FAPEAM_URL)
        soup = BeautifulSoup(html, 'html.parser')
        seen = set()
        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            if href.startswith('https://www.fapeam.am.gov.br/editais/edital') and href not in seen:
                seen.add(href)
                unique_urls.append(href)
        print(f'  FAPEAM: {len(unique_urls)} URLs encontradas na lista.')
    except Exception as e:
        print(f'  AVISO FAPEAM: falha ao raspar lista — {e}')

    # Fallback: seed manual
    if not unique_urls:
        seed = load_seed_fapeam()
        if seed:
            print(f'  FAPEAM: usando seed_fapeam.json ({len(seed)} URLs).')
            unique_urls = seed
        else:
            print('  AVISO FAPEAM: sem URLs (scraping falhou e seed vazio).')

    items = []
    for url in unique_urls:
        try:
            page = fetch(url)
            psoup = BeautifulSoup(page, 'html.parser')
            title = extract_title_fapeam(psoup)
            date  = extract_vigencia(psoup.get_text(' ', strip=True))
            items.append({
                'source_system': 'FAPEAM',
                'title': title,
                'url': url,
                'area': 'Geral',
                'type': guess_type(title),
                'date': date,
            })
            print(f'  FAPEAM OK: {title[:70]}')
        except Exception as e:
            print(f'  FAPEAM FALHOU: {url[:70]} — {e}')
            items.append({
                'source_system': 'FAPEAM',
                'title': 'Edital (falha ao coletar)',
                'url': url,
                'area': 'Geral',
                'type': 'Edital',
                'date': '',
            })
    return items


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    items = scrape_fapeam() + scrape_cnpq()
    out = {
        'updated_at': datetime.now().date().isoformat(),
        'sources': {
            'FAPEAM': {'name': 'FAPEAM — Editais Abertos', 'url': FAPEAM_URL},
            'CNPq':   {'name': 'CNPq — Chamadas Abertas para Submissão', 'url': CNPQ_URL},
        },
        'items': items,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    fapeam_n = sum(1 for x in items if x['source_system'] == 'FAPEAM')
    cnpq_n   = sum(1 for x in items if x['source_system'] == 'CNPq')
    print(f'\nOK: {OUT_JSON} ({len(items)} itens — FAPEAM: {fapeam_n}, CNPq: {cnpq_n})')


if __name__ == '__main__':
    main()
