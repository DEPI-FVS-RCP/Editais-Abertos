# CLAUDE.md — Registro e Histórico do Projeto
## Editais Abertos Unificados (FAPEAM + CNPq) — FVS-RCP / DEPI

---

## Sobre o projeto

Painel público (HTML estático + JSON) que exibe em uma única página os editais abertos
da **FAPEAM** e as chamadas abertas do **CNPq**, para divulgação em grupos externos
(WhatsApp, e-mail etc.).
Mantido pela **Diretoria de Ensino, Pesquisa e Inovação (DEPI)** da **FVS-RCP**.

- **Fontes:** https://www.fapeam.am.gov.br/editais/?aba=editais-abertos
             https://www.gov.br/cnpq/pt-br/chamadas/abertas-para-submissao
- **Formato:** `index.html` (front-end) + `data.json` (dados) + `scripts/` (automação)
- **Publicação:** GitHub Pages (branch `main`, pasta `/root`)

---

## Estrutura de arquivos

```
Editais-Abertos-Unificados-main/
├── index.html              — Painel HTML principal (FAPEAM + CNPq em seções separadas)
├── data.json               — Base unificada (atualizada pelo scraper)
├── .nojekyll               — Necessário para GitHub Pages servir arquivos corretamente
├── logo.png                — Logomarca FVS-RCP
├── logo_depi.png           — Logomarca DEPI
├── CLAUDE.md               — Este arquivo (histórico e documentação)
└── scripts/
    ├── scrape_all.py       — Scraper Python unificado (FAPEAM + CNPq)
    ├── atualizar.sh        — Shell script para execução local + instruções de cron
    ├── seed_fapeam.json    — Fallback manual de URLs para FAPEAM
    └── seed_cnpq.json      — Fallback manual de {title, url} para CNPq
```

---

## Esquema do data.json

```json
{
  "updated_at": "YYYY-MM-DD",
  "sources": {
    "FAPEAM": {"name": "FAPEAM — Editais Abertos", "url": "..."},
    "CNPq":   {"name": "CNPq — Chamadas Abertas para Submissão", "url": "..."}
  },
  "items": [
    {
      "source_system": "FAPEAM ou CNPq",
      "title": "...",
      "url": "...",
      "area": "...",
      "type": "...",
      "date": "YYYY-MM-DD ou vazio"
    }
  ]
}
```

---

## Histórico de alterações

### 2026-03-23 — Revisão e correção do projeto unificado (Claude Code)

**Contexto:**
Revisão completa do projeto unificado, comparando com os dois projetos originais
(Editais-Abertos-FAPEAM e Editais-Abertos-CNPq), para corrigir bugs e melhorar robustez.

**Bugs corrigidos em `index.html`:**
- `SOURCES` do JSON era carregado mas nunca utilizado → agora popula links clicáveis no rodapé
  (`footFonteFapeam` e `footFonteCnpq`), como nos projetos originais.
- Opções dos filtros (`<option>`) não tinham `value=""` explícito e usavam `escapeHtml()` no texto
  → mismatch silencioso quando `area` ou `tipo` contivesse caracteres especiais HTML. Corrigido
  com `value="${escapeAttr(v)}"` em todos os selects.
- `$('err').style.display = 'none'` era chamado após `render()` → movido para antes.
- Estilos `.footer-divider` e `.footer-copy` ausentes (presentes nos originais) → adicionados.
- Dividers e link de fonte no rodapé HTML ausentes → adicionados.

**Melhorias em `scrape_all.py`:**
- Adicionado fallback de seed manual para FAPEAM (`seed_fapeam.json`): se o scraping da lista
  falhar, usa URLs do seed antes de desistir.
- Adicionado fallback de seed manual para CNPq (`seed_cnpq.json`): mesmo comportamento.
- Extração de título da FAPEAM melhorada: tenta H1 → og:title → `<title>`, igualando o
  comportamento do scraper original (`scrape_fapeam.py`).
- Adicionados prints de progresso durante scraping (OK / FALHOU / AVISO por item).
- Separação clara entre utilitários, seeds, scraper CNPq e scraper FAPEAM para facilitar
  manutenção futura.

**Melhorias em `atualizar.sh`:**
- Adicionado `set -euo pipefail` para abortar em erros inesperados.
- Adicionada criação automática da pasta `../logs/`.
- Adicionadas instruções completas de agendamento via `crontab` (ciclo de 20 dias, às 08h00).
- `lxml` incluído no `pip install` para parsing HTML mais robusto.

**Arquivos criados:**
- `scripts/seed_fapeam.json` — stub vazio `{ "urls": [] }` para fallback manual FAPEAM.
- `scripts/seed_cnpq.json`   — stub vazio `{ "items": [] }` para fallback manual CNPq.

---

### 2026-03-23 — Ajuste de linguagem nos textos de identificação do painel (Claude Code)

#### Alterações realizadas
- `<title>`: `"Editais Abertos — FAPEAM + CNPq"` → `"Editais Abertos — FAPEAM, CNPq"`
- `.t2` (subtítulo do cabeçalho): `"Painel público de links — Editais Abertos (FAPEAM + CNPq)"` → `"Painel público de links — Editais Abertos FAPEAM, CNPq"` (parênteses e `+` removidos)
- `<h1>`: `"Editais Abertos — FAPEAM + CNPq"` → `"Editais Abertos — FAPEAM, CNPq"`

#### Justificativa técnica
O operador `+` possui conotação matemática/técnica e os parênteses criam hierarquia visual desnecessária.
A vírgula é a forma gramaticalmente correta para enumerar fontes de dados em texto corrido,
tornando o painel mais legível para o público-alvo (divulgação externa via WhatsApp e e-mail).

#### Impacto no sistema
Puramente cosmético — nenhuma lógica de dados, filtros, scraper ou JSON foi alterada.
O `data.json` não contém esses textos, portanto não requer atualização.

#### Arquivos afetados
- `index.html` — 3 ocorrências alteradas (linhas `<title>`, `.t2`, `<h1>`)

#### Recomendações futuras
- Revisar se o cabeçalho do `CLAUDE.md` (`## Editais Abertos Unificados (FAPEAM + CNPq)`) deve ser harmonizado com a nova grafia adotada no painel.
- Caso novas fontes de dados sejam incorporadas ao painel, manter o padrão de enumeração por vírgula nos textos visíveis ao usuário.

---

### 2026-03-23 — Melhorias visuais no rodapé e grid de cards (Claude Code)

#### Alterações realizadas

**Assinatura CARAVELA no rodapé (`index.html`):**
- Inserido bloco inicial com emoji `⛵ CARAVELA` antes de `</footer>` (primeira versão).
- Inserido bloco SVG da caravela separado (segunda versão intermediária).
- Ambos os blocos anteriores substituídos por versão final unificada: SVG inline da caravela
  (traçado branco, 42×42 px) com texto `CARAVELA` centralizado abaixo, alinhado à direita,
  `opacity: .16`, sem emoji, sem cor de destaque — apenas branco discreto sobre o fundo do rodapé.

**Grid de cards (`index.html`, CSS inline):**
- Classe `.cards`: `grid-template-columns` alterada de `repeat(2, 1fr)` para `repeat(3, 1fr)`;
  `gap` ajustado de `12px` para `18px`.
- Breakpoint tablet adicionado: `@media (max-width: 1100px)` → 2 colunas.
- Breakpoint mobile mantido e ajustado: `@media (max-width: 680px)` → 1 coluna
  (anterior era `max-width: 760px`).

#### Justificativa técnica
- A assinatura CARAVELA identifica a autoria/ferramenta do painel de forma discreta, sem
  interferir na leitura do conteúdo. O SVG inline elimina dependência de fontes de ícones
  externas e o emoji colorido (⛵) foi removido por ser inconsistente entre sistemas operacionais.
- A grid de 3 colunas aproveita melhor o espaço horizontal em monitores desktop modernos
  (largura típica ≥ 1280 px), reduzindo a rolagem vertical e melhorando a escaneabilidade
  dos editais. Os breakpoints responsivos preservam a usabilidade em telas menores.

#### Impacto no sistema
- Puramente visual — nenhuma lógica de dados, JavaScript, scraper ou `data.json` foi alterada.
- A grid de 3 colunas pode exigir revisão do tamanho mínimo dos cards caso títulos muito longos
  causem overflow em resoluções intermediárias (1100–1280 px).

#### Arquivos afetados
- `index.html` — CSS inline (`.cards` e breakpoints) e bloco HTML do rodapé (`</footer>`).

#### Recomendações futuras
- Avaliar migrar o CSS inline para um arquivo `styles.css` externo, facilitando manutenção
  e separação de responsabilidades.
- Testar a grid de 3 colunas com volume alto de cards (> 30 itens) para verificar se o gap
  de 18 px mantém boa legibilidade.
- Considerar adicionar breakpoint intermediário em `max-width: 900px` → 2 colunas compactas,
  caso monitores de 10–12 polegadas sejam comuns entre o público-alvo.

---

## Como atualizar os dados manualmente

```bash
# 1. Entre na pasta do projeto
cd "caminho/para/Editais-Abertos-Unificados-main"

# 2. Execute o script
bash scripts/atualizar.sh
```

---

## Como agendar atualização automática a cada 20 dias (macOS)

```bash
# Abra o editor de cron
crontab -e

# Adicione esta linha (ajuste o caminho completo):
0 8 */20 * * /bin/bash "/Users/walterolivasegundo/Downloads/Editais-Abertos-Unificados-main/scripts/atualizar.sh" >> "/Users/walterolivasegundo/Downloads/logs/unificado.log" 2>&1
```

Isso executa o script às **08h00** nos dias **1, 21, 41...** de cada mês (ciclo ~20 dias).

---

## Como usar o fallback manual (seed)

Se o scraping falhar (site fora do ar ou mudança de layout):

**FAPEAM** — edite `scripts/seed_fapeam.json`:
```json
{
  "urls": [
    "https://www.fapeam.am.gov.br/editais/edital-n-o-001...",
    "https://www.fapeam.am.gov.br/editais/edital-n-o-002..."
  ]
}
```

**CNPq** — edite `scripts/seed_cnpq.json`:
```json
{
  "items": [
    {"title": "Chamada ...", "url": "https://www.gov.br/cnpq/..."},
    {"title": "Chamada ...", "url": "https://www.gov.br/cnpq/..."}
  ]
}
```

Depois execute `bash scripts/atualizar.sh` normalmente.

---

## Observações técnicas

- O scraper FAPEAM tenta raspar a lista de editais. Se não encontrar URLs (site com JS dinâmico),
  usa `seed_fapeam.json`. Cada URL é acessada individualmente para extrair título, prazo e tipo.
- O scraper CNPq busca links dentro de `<h2>` da página de chamadas. Se não encontrar itens,
  usa `seed_cnpq.json`. O prazo é extraído por regex de range de datas nas páginas de detalhe.
- O campo `date` (prazo) pode ficar vazio se o site não exibir datas estruturadas.
- A área dos editais é classificada como "Geral" por padrão; para categorização fina,
  edite o `data.json` manualmente.

---

## Publicação no GitHub Pages

1. Faça commit de todos os arquivos (incluindo o `data.json` gerado).
2. No GitHub, vá em Settings → Pages → Source: branch `main`, pasta `/root`.
3. O painel estará disponível em `https://<usuario>.github.io/<repo>/`.

---

## Contato / Manutenção

**FVS-RCP — DEPI**
Diretoria de Ensino, Pesquisa e Inovação
Av. Torquato Tapajós, 4.010 — Manaus/AM

---

## Atualização — 2026-03-23

### Alterações realizadas

Iterações sucessivas de refinamento da assinatura/marca d'água "CARAVELA" exibida no canto inferior direito do painel (`index.html`). As alterações desta sessão foram exclusivamente visuais, sem tocar em qualquer lógica de dados, JavaScript, grid ou layout do painel.

**Ciclo de substituições do bloco SVG:**
1. Bloco com classes CSS dedicadas (`.marca-caravela`, `.caravela-svg`, `.texto-caravela`) substituído por bloco com estilos inline, SVG 56×56 minimalista (casco curvo, duas velas, bandeira).
2. SVG 56×56 substituído por SVG 74×74 (viewBox 140×140) com casco poligonal, proa/popa curvos, cruz templária simples e bandeira.
3. SVG 74×74 substituído por SVG 92×92 (viewBox 180×180) com casco realista, vela latina, vela traseira, cordame, verga inclinada, linha de água e cruz templária estilizada com quadrado externo.

**Ajustes finos sobre o SVG 92×92 final:**
- Cruz templária reposicionada para o centro geométrico da vela esquerda (coordenadas M72/M66/M78).
- Segunda cruz templária adicionada na vela direita (coordenadas M112/M106/M118).
- Ambas as cruzes reduzidas e centralizadas em iteração posterior.
- Ambas as cruzes removidas definitivamente por decisão estética.
- `margin-top` do texto "CARAVELA" ajustado de `2px` → `-6px` → `-10px` para aproximar a legenda do desenho.
- CSS das classes órfãs (`.marca-caravela`, `.caravela-svg`, `.texto-caravela`) removido quando o bloco migrou para estilos inline.

**Estado final da assinatura:**
- Container: `position:fixed; right:34px; bottom:26px; opacity:.34; z-index:0`
- SVG: `width="92" height="92" viewBox="0 0 180 180"`, stroke branco, `stroke-width="2.8"`
- Elementos SVG: casco com proa/popa, linhas internas, mastro, bandeira, verga inclinada, vela latina, vela traseira, cordame, linha de água — sem cruzes
- Texto: `font-size:10px; letter-spacing:2.8px; font-weight:600; opacity:.96; margin-top:-10px`

### Justificativa técnica

A assinatura CARAVELA identifica a autoria/ferramenta do painel de forma discreta. As iterações buscaram equilibrar visibilidade (opacidade e stroke legíveis) com elegância (sem poluição visual). A remoção das cruzes templárias foi decisão estética final — o desenho do barco já é suficientemente identificável sem elementos adicionais dentro das velas.

### Impacto no sistema

Puramente visual. Nenhuma lógica de dados, filtros, scraper, `data.json` ou JavaScript foi alterada. O posicionamento `fixed` garante que a marca d'água flutue sobre o conteúdo sem interferir no scroll ou no layout do rodapé institucional.

### Arquivos afetados

- `index.html` — bloco HTML/SVG da assinatura CARAVELA e CSS inline associado

### Recomendações futuras

- Avaliar migrar o bloco inline para uma classe CSS reutilizável em arquivo `styles.css` externo, facilitando futuros ajustes de opacidade ou tamanho sem editar o HTML diretamente.
- Testar a legibilidade da assinatura em monitores com fundo claro (modo de alto contraste / acessibilidade) — o stroke branco pode se perder se o footer mudar de cor.
- Considerar versão SVG exportada como arquivo externo (`caravela.svg`) e referenciada via `<img>`, eliminando o SVG inline do HTML.

---

## Atualização — 2026-03-23

### Alterações realizadas

Nenhuma alteração de código nesta sessão. Sessão de esclarecimento técnico sobre o escopo de arquivos do projeto:

- Confirmado que alterações exclusivamente visuais (marca d'água, layout, CSS) requerem apenas edição de `index.html`.
- Confirmado que `data.json`, `scripts/scrape_all.py`, `scripts/atualizar.sh`, `scripts/seed_fapeam.json`, `scripts/seed_cnpq.json`, `.nojekyll`, `logo.png` e `logo_depi.png` **não precisam ser alterados** para mudanças visuais.

### Justificativa técnica

O projeto segue separação clara de responsabilidades:
- **`index.html`** — apresentação visual (front-end)
- **`data.json`** — dados dos editais (gerado pelo scraper)
- **`scripts/`** — automação de coleta de dados (back-end)

Alterações visuais são contidas no front-end e não propagam efeitos para a camada de dados ou automação.

### Impacto no sistema

Nenhum. Sessão informativa sem modificações de arquivos do projeto.

### Arquivos afetados

Nenhum arquivo modificado nesta sessão.

### Recomendações futuras

- Documentar explicitamente no início do `CLAUDE.md` a tabela de responsabilidades por arquivo (visual → `index.html`; dados → `data.json`; coleta → `scripts/`), como referência rápida para futuras sessões de manutenção.

---

## Atualização — 2026-03-23

### Alterações realizadas

Correção do posicionamento da assinatura CARAVELA no rodapé do painel (`index.html`):

- `position:fixed` → `position:absolute` no bloco inline da assinatura CARAVELA (SVG + texto).
- `position:relative` adicionado à regra CSS `.site-footer`.

### Justificativa técnica

`position:fixed` ancora o elemento em relação à **janela do navegador** (_viewport_), fazendo com que ele acompanhe o scroll da página. A correção usa `position:absolute`, que ancora o elemento em relação ao seu ancestral posicionado mais próximo. Para isso funcionar corretamente, o `<footer>` (`.site-footer`) precisou receber `position:relative`, tornando-se o contexto de posicionamento do elemento filho.

### Impacto no sistema

- A assinatura CARAVELA agora fica estática no canto inferior direito do rodapé, independentemente da posição de rolagem da página.
- Nenhuma lógica de dados, filtros, scraper, `data.json` ou JavaScript foi alterada.
- O layout e demais elementos visuais do painel permanecem inalterados.

### Arquivos afetados

- `index.html` — duas alterações cirúrgicas:
  - Regra CSS `.site-footer`: adicionado `position:relative`.
  - Bloco inline da assinatura CARAVELA: `position:fixed` substituído por `position:absolute`.

### Recomendações futuras

- Ao adicionar novos elementos posicionados absolutamente dentro do rodapé, verificar que `.site-footer` mantém `position:relative` para evitar regressão do mesmo bug.
- Avaliar migrar o bloco inline da assinatura para uma classe CSS dedicada em arquivo `styles.css` externo, centralizando o gerenciamento de posicionamento e facilitando futuras manutenções.
