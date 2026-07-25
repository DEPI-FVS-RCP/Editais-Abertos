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
- **Repositório:** https://github.com/DEPI-FVS-RCP/Editais-Abertos

---

## Estrutura de arquivos

```
Editais-Abertos-Unificados-main/
├── index.html              — Painel HTML principal (FAPEAM + CNPq em seções separadas)
├── data.json               — Base unificada (atualizada pelo scraper)
├── .nojekyll               — Necessário para GitHub Pages servir arquivos corretamente
├── .gitignore               — Ignora .DS_Store
├── logo.png                — Logomarca FVS-RCP
├── logo_depi.png            — Logomarca DEPI
├── CLAUDE.md                — Este arquivo (histórico e documentação)
└── scripts/
    ├── scrape_all.py       — Scraper Python unificado (FAPEAM + CNPq)
    ├── atualizar.sh        — Shell script para execução local + commit/push automático + instruções de cron
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

## Agentes de trabalho

O projeto define três agentes com responsabilidades separadas para manter a qualidade visual sem
comprometer a lógica existente. **Fluxo obrigatório:**
`UI_VISUAL_INSTITUCIONAL` propõe → `UI_COMPONENTES_CARDS` refina → `CORE_LOGIC_QA` valida → só então aplicar.

---

### Agente UI_VISUAL_INSTITUCIONAL

**Escopo:** ajustes visuais globais do painel — tudo que envolve identidade institucional e estrutura
geral da página, exceto os cards de editais.

**Responsabilidades:**
- Cabeçalho institucional (`<header>`, logos, título `<h1>`, subtítulo `.t2`)
- Equilíbrio visual entre `logo.png` (FVS-RCP), `logo_depi.png` (DEPI), título e chips de fonte
- Paleta de cores harmônica com a identidade FVS-RCP/DEPI (azuis institucionais, contraste acessível)
- Rodapé institucional (links de fonte, dividers, texto de atualização, `.footer-copy`)
- Marca d'água CARAVELA (SVG, opacidade, posicionamento)
- Responsividade geral da página (breakpoints de layout global)
- Tipografia base (família, tamanho, peso)

**Restrições:**
- Não alterar IDs ou classes usados pelo JavaScript (`$('filtro')`, `$('err')`, `$('total')` etc.)
- Não tocar nos cards (`.card`, `.cards`, `.pill`) — esses são escopo de UI_COMPONENTES_CARDS
- Não alterar `data.json`, `scripts/` ou qualquer lógica JS
- Não adicionar bibliotecas, frameworks ou dependências externas
- Mudanças devem ser cirúrgicas e acompanhadas de justificativa no CLAUDE.md

**Arquivo de atuação:** `index.html` (CSS e HTML do cabeçalho e rodapé)

---

### Agente UI_COMPONENTES_CARDS

**Escopo:** componentes de card e área de listagem — tudo que envolve a apresentação dos editais
individuais e os controles de filtragem.

**Responsabilidades:**
- Cards de editais: layout interno, sombra, borda, hover, tamanho mínimo
- Grid `.cards`: colunas (3 no desktop), `gap`, alinhamento vertical dos cards
- Breakpoints do grid: tablet (`max-width: 1100px` → 2 col.), mobile (`max-width: 680px` → 1 col.)
- Pills de fonte (`FAPEAM` / `CNPq`), área e tipo: cores, forma, tamanho, espaçamento
- Destaque visual do prazo (campo `date`): cor, peso, posição dentro do card
- Separação visual entre a seção FAPEAM e a seção CNPq (título de seção, divider, cor de fundo)
- Filtros de texto, fonte, área e tipo: layout, espaçamento, estilo dos `<select>` e `<input>`
- Botões "Copiar tudo" e "Limpar filtros": aparência visual (cor, borda, hover) — sem alterar eventos JS
- Contadores `#total`, `#totalFapeam`, `#totalCnpq`: posicionamento e tipografia — sem alterar JS

**Restrições:**
- Não alterar `id` de nenhum elemento (ex.: `cardsFapeam`, `cardsCnpq`, `filtro`, `total` etc.)
- Não alterar eventos JavaScript (`onclick`, `oninput`, `onchange`)
- Não alterar a estrutura HTML dos cards gerados pelo JS (apenas o CSS que os estiliza)
- Não alterar `data.json`, `scripts/` ou lógica de renderização
- Não adicionar bibliotecas externas

**Arquivo de atuação:** `index.html` (CSS das classes `.card`, `.cards`, `.pill`, filtros, botões)

---

### Agente CORE_LOGIC_QA

**Escopo:** validação funcional completa do painel antes de qualquer mudança ser aplicada definitivamente.
Não propõe alterações visuais — apenas aprova ou rejeita com lista de problemas encontrados.

**Checklist de validação obrigatório:**

| # | Item | Critério de aprovação |
|---|------|-----------------------|
| 1 | Leitura do `data.json` | Fetch retorna 200; `items` é array não vazio; `updated_at` exibido |
| 2 | Renderização dos cards | Todos os itens de `data.json` geram um card; título, URL e prazo visíveis |
| 3 | Separação FAPEAM / CNPq | Cards aparecem na seção correta conforme `source_system` |
| 4 | Filtro por texto | `<input id="filtro">` filtra por título em tempo real |
| 5 | Filtro por fonte | `<select id="filtroFonte">` exibe só FAPEAM ou só CNPq conforme seleção |
| 6 | Filtro por área | `<select id="filtroArea">` filtra corretamente; opções populadas do JSON |
| 7 | Filtro por tipo | `<select id="filtroTipo">` filtra corretamente; opções populadas do JSON |
| 8 | Botão "Copiar tudo" | Copia lista de URLs/títulos para o clipboard sem erro JS |
| 9 | Botão "Limpar filtros" | Redefine todos os filtros e reexibe todos os cards |
| 10 | Contadores | `#total`, `#totalFapeam`, `#totalCnpq` refletem contagem atual após filtros |
| 11 | Console sem erros | DevTools → Console: zero erros JS após carregamento e interação |
| 12 | GitHub Pages | Página carrega via `https://` sem dependências externas quebradas |
| 13 | Responsividade | Layout correto em 320 px, 768 px e 1280 px (simulação DevTools) |
| 14 | IDs preservados | Nenhum ID usado pelo JS foi renomeado ou removido nas mudanças propostas |

**Fluxo de resposta:**
- **APROVADO:** lista o que foi verificado e libera a aplicação das mudanças.
- **REPROVADO:** lista os itens com falha e retorna o controle para o agente responsável corrigir.

**Restrições:**
- Não edita `index.html`, `data.json` ou `scripts/`
- Não propõe mudanças visuais
- Não aprova mudanças que alterem IDs usados pelo JavaScript

---

## Tabela de responsabilidades por arquivo

| Arquivo | Quem altera | Quando |
|---------|-------------|--------|
| `index.html` | UI_VISUAL_INSTITUCIONAL, UI_COMPONENTES_CARDS | Após aprovação de CORE_LOGIC_QA |
| `data.json` | Somente o scraper (`scrape_all.py`) | Nunca manualmente sem autorização explícita |
| `scripts/scrape_all.py` | Manutenção de coleta | Fora do escopo dos agentes UI/QA |
| `scripts/atualizar.sh` | Manutenção de coleta e publicação | Fora do escopo dos agentes UI/QA |
| `scripts/seed_*.json` | Manutenção manual de fallback | Fora do escopo dos agentes UI/QA |
| `CLAUDE.md` | Todos os agentes | Ao final de cada sessão, registrar o que foi feito |

---

## Histórico de alterações

### 2026-07-25 — Publicação automática real: conexão git + atualizar.sh com push + desativação da tarefa Claude (Cowork)

**Contexto:**
Após o redesign visual (registrado abaixo), o usuário reportou que o site publicado estava exibindo
editais da FAPEAM já encerrados. Investigação revelou que o `data.json` estava parado desde 23/03/2026
(mais de 4 meses), pois a tarefa agendada criada na sessão anterior ainda não havia rodado (primeira
execução programada para 5 dias depois). O usuário pediu atualização "sozinha" via busca ativa nos
dois sites.

**Diagnóstico técnico (bloqueio duplo confirmado por teste direto):**
1. **Rede:** `curl` a partir do ambiente sandboxed do Claude retornou `403 blocked-by-allowlist` tanto
   para `fapeam.am.gov.br` quanto para `gov.br/cnpq` — bloqueio de proxy de saída do próprio ambiente,
   não contornável.
2. **Credenciais git:** `github.com` respondeu normalmente (200), mas `git push` a partir do sandbox
   falhou com `could not read Username for 'https://github.com'` — o ambiente sandboxed é um contêiner
   Linux isolado, sem acesso ao Keychain/credenciais do Mac do usuário, e por política o Claude não
   pode digitar/armazenar tokens ou senhas em nome do usuário.

**Conclusão:** a automação "100% Claude na nuvem" (tarefa agendada anterior) não é viável para este
projeto — esbarra em dois bloqueios estruturais do ambiente (rede + isolamento de credenciais), não
em erro de configuração. A arquitetura correta é rodar a atualização **localmente, no Mac do usuário**,
via `cron` nativo — que já não tem nenhum dos dois bloqueios.

**Ações realizadas:**
1. Descoberto que o usuário já havia publicado o painel redesenhado via **upload manual pela interface
   web do GitHub** (sem git local), no repositório `https://github.com/DEPI-FVS-RCP/Editais-Abertos`.
   Confirmado por diff direto (`git show origin/main:index.html` vs arquivo local) que `index.html` e
   `data.json` remotos já eram **idênticos** aos locais — nenhuma perda de trabalho.
2. Pasta local conectada ao repositório real: `git init` + `git remote add origin` + `git fetch` +
   `git reset --hard origin/main` (alinhamento seguro, pois conteúdo já era idêntico) + `git config
   user.name/user.email`.
3. Adicionados e commitados localmente (aguardando primeiro `git push` manual do usuário):
   `.gitignore` (ignora `.DS_Store`) e `.nojekyll` (ausente no repositório remoto até então —
   necessário para o GitHub Pages servir corretamente).
4. `scripts/atualizar.sh` estendido: ao final da execução do scraper, se houver mudanças em
   `data.json`, faz `git add` + `git commit` + `git push origin main` automaticamente; se o push
   falhar por falta de credencial salva, registra aviso no log em vez de quebrar o script
   (`set -e` mantido para o scraper, mas o bloco git usa `if`, que não aciona `errexit`). Comentário
   de cabeçalho do script atualizado explicando o pré-requisito de autenticar o `git push` uma vez
   manualmente para o macOS salvar a credencial no Keychain (reaproveitada silenciosamente pelo cron).
   Cron de exemplo no cabeçalho do script atualizado de `*/20` para `*/10` dias, alinhado ao pedido
   do usuário.
5. Tarefa agendada `editais-abertos-atualizacao` (criada na sessão anterior) **desativada**
   (`enabled:false`), com descrição atualizada explicando o motivo, para não gerar falsa sensação de
   automação funcionando em segundo plano.
6. **Correção de um problema colateral desta própria sessão:** o `git reset --hard origin/main` do
   passo 2, executado antes de conferir `CLAUDE.md`, sobrescreveu este arquivo com uma versão mais
   antiga e mais curta presente no repositório remoto (upload manual anterior não incluiu as últimas
   atualizações de documentação). O conteúdo completo foi restaurado a partir do contexto da conversa
   (a versão íntegra havia sido lida no início da sessão) — nenhuma perda definitiva de histórico.

**Pendências / próximos passos do usuário:**
- Rodar `git push origin main` manualmente **uma vez** nesta pasta (autenticando com usuário +
  Personal Access Token do GitHub, ou SSH) para: (a) publicar os commits de `.gitignore`/`.nojekyll`
  já preparados; (b) salvar a credencial no Keychain do macOS para uso silencioso pelo `cron`.
- Adicionar a linha de `crontab` (fornecida na resposta ao usuário) no Terminal do próprio Mac, para
  rodar `scripts/atualizar.sh` a cada 10 dias — isso resolve na origem tanto a busca ativa (rede sem
  bloqueio no Mac) quanto a publicação (credencial já salva no Keychain).
- Rodar `bash scripts/atualizar.sh` manualmente pelo menos uma vez para corrigir imediatamente os
  editais desatualizados exibidos no site (o `data.json` atual ainda reflete 23/03/2026).

**Impacto no sistema:** Nenhuma lógica de renderização, filtros ou dados foi alterada nesta sessão.
Mudanças restritas a infraestrutura de publicação (`scripts/atualizar.sh`, conexão git, tarefa
agendada) e à correção do próprio `CLAUDE.md`.

**Arquivos afetados:** `scripts/atualizar.sh`, `.gitignore` (novo), `.nojekyll` (adicionado ao git),
`CLAUDE.md` (este registro + restauração de conteúdo).

---

### 2026-07-25 — Redesign Apple-like institucional + automação de atualização (Cowork)

**Contexto:**
Solicitado profissionalizar o painel no mesmo molde visual dos projetos "Controle de Acordos de
Cooperação Técnica / FAROL DEPI-FVS-RCP" e "SISTEMA_OTTO_PAIC" (estilo "Apple-like"), e configurar
atualização automática dos dados a cada 10 dias.

**Referência de estilo usada:** projeto "Controle de Acordos de Cooperação Técnica, Convênios e
Termos de Colaboração (FAROL DEPI/FVS-RCP)" — leitura do `:root` de design tokens e componentes
(topbar em card, KPIs, cards com sombra dupla suave, tipografia `-apple-system/SF Pro`).

**Agentes executados:** UI_VISUAL_INSTITUCIONAL → UI_COMPONENTES_CARDS → CORE_LOGIC_QA

**Alterações aplicadas em `index.html` (CSS + reestruturação do wrapper do cabeçalho, IDs e JS 100% preservados):**

| Elemento | Mudança | Agente |
|----------|---------|--------|
| `:root` | Tokens redesenhados: `--font-family-base` (-apple-system/SF Pro), `--radius-card/panel/btn`, `--shadow-card` (sombra dupla suave, no molde FAROL), `--shadow-card-hover`, `--focus-ring` (verde institucional), `--brand`/`--brand-dark`/`--brand-tint` substituindo o antigo `--brand:#5f7f73` | UI_VISUAL |
| `body` | `font-family` migrado para pilha Apple-like; adicionada textura SVG institucional de fundo (opacity .04), no mesmo espírito do FAROL | UI_VISUAL |
| `<header>` | Convertido de barra colorida fixa para `.topbar` — card branco flutuante, `border-radius`, `box-shadow:var(--shadow-card)`, `position:sticky` com respiro (`top:12px`) | UI_VISUAL |
| `.chip` | De "pill translúcido sobre fundo verde" para pill com `--brand-tint`/`--brand-dark` sobre fundo branco (mesma pegada dos badges do FAROL) — **IDs `chipUpdated`, `chipTotal`, `chipFapeam`, `chipCnpq` inalterados** | UI_VISUAL |
| `.panel` | `border-radius:16px`, `box-shadow:var(--shadow-card)` substituindo borda simples | UI_VISUAL |
| `.btn`, `input`, `select` | Raio e paleta ajustados ao token system; `select` ganhou seta customizada (SVG) e `appearance:none`, igual ao padrão `.select` do FAROL; foco com `--focus-ring` verde (antes `outline` azul/verde genérico) | UI_CARDS |
| `.card` (editais) | `box-shadow:var(--shadow-card)`/`--shadow-card-hover`, `border-radius:14px`, tipografia com `letter-spacing` mais fechado (`-0.005em` a `-0.015em`), no padrão tipográfico Apple-like | UI_CARDS |
| `.pill`, `.pill.system` | Cores migradas para os novos tokens (`--pill`, `--brand-tint`) | UI_CARDS |
| `.site-footer` | Apenas ajuste de `letter-spacing` e `z-index` para respeitar a nova textura de fundo — assinatura CARAVELA inalterada | UI_VISUAL |

**CORE_LOGIC_QA — Resultado: APROVADO**
- IDs: diff automatizado entre HTML antigo e novo → **0 diferenças** (todos os 19 IDs usados pelo JS preservados)
- Bloco `<script>`: diff byte a byte entre antigo e novo → **idêntico**, nenhuma linha de JS tocada
- Teste funcional automatizado (Playwright headless, servidor local): filtro por texto/fonte, botão "Limpar filtros", contadores (`chipTotal`, `chipFapeam`, `chipCnpq`) — todos responderam corretamente (21 → 2 → 21 editais)
- Console do navegador: **zero erros** em 3 breakpoints (1280px desktop, 900px tablet, 375px mobile)
- Grid responsivo (3/2/1 colunas) validado visualmente nos 3 breakpoints via screenshot
- `data.json` e `scripts/` intocados

**Automação de atualização (novidade desta sessão, revisada na sessão seguinte — ver entrada acima):**
Criada tarefa agendada `editais-abertos-atualizacao` (cron `0 8 */10 * *`), posteriormente
**desativada** por inviabilidade técnica (bloqueio de rede + credenciais do ambiente Claude — ver
registro de 2026-07-25 acima). Substituída por automação local via `cron` no Mac do usuário.

**Impacto no sistema:** Nenhuma lógica de dados, filtros ou renderização foi alterada — mudança
puramente visual (CSS + wrapper do cabeçalho).

**Arquivos afetados:** `index.html` (CSS e reestruturação do `<header>`→`.topbar`), `CLAUDE.md` (este registro).

---

### 2026-05-24 — Acabamento premium institucional — ciclo 2 (Claude Code)

**Agentes executados:** UI_VISUAL_INSTITUCIONAL → UI_COMPONENTES_CARDS → CORE_LOGIC_QA

**Alterações aplicadas em `index.html` (somente CSS):**

| Elemento | Propriedade | Antes | Depois | Agente |
|----------|-------------|-------|--------|--------|
| `.t1` header | `font-size` | *(herdado)* | `15px` explícito | UI_VISUAL |
| `.t1` header | `line-height` | *(herdado)* | `1.2` | UI_VISUAL |
| `.titleblock` | `border-left` | *(ausente)* | `1px solid rgba(255,255,255,.28)` | UI_VISUAL |
| `.titleblock` | `padding-left` | *(ausente)* | `18px` | UI_VISUAL |
| `.panel h1` | `font-size` | `22px` | `20px` | UI_VISUAL |
| `.panel h1` | `font-weight` | *(herdado)* | `700` explícito | UI_VISUAL |
| `.panel p` | `line-height` | `1.4` | `1.6` | UI_VISUAL |
| `.btn` | `transition` | *(ausente)* | `background .18s` | UI_CARDS |
| `.btn:hover` | `background` | *(ausente)* | `#256054` | UI_CARDS |
| `.btn.secondary:hover` | `background` | *(ausente)* | `#dce8e4` | UI_CARDS |
| `input, select` | `transition` | *(ausente)* | `border-color/outline .15s` | UI_CARDS |
| `input:focus, select:focus` | `outline` | *(padrão browser)* | `2px solid var(--brand)` | UI_CARDS |
| `.legendBox` | `border-left` | *(ausente)* | `3px solid var(--brand)` | UI_VISUAL |
| `.legendBox` | `border-radius` | `14px` | `12px` | UI_VISUAL |
| `.section` | `margin-top` | `20px` | `28px` | UI_CARDS |
| `.sectionHead` | `margin-bottom` | `10px` | `12px` | UI_CARDS |
| `.sectionHead` | `padding-bottom` | `8px` | `10px` | UI_CARDS |
| `.sectionHead h2` | `border-left` | *(ausente)* | `3px solid var(--brand)` | UI_CARDS |
| `.sectionHead h2` | `padding-left` | *(ausente)* | `10px` | UI_CARDS |
| `.num` | `background` | `var(--pill)` | `var(--brand)` | UI_CARDS |
| `.num` | `color` | `var(--ink)` | `#fff` | UI_CARDS |
| `.num` | `font-size` | *(herdado)* | `12px` | UI_CARDS |
| `.num` | `width/height` | `28px` | `26px` | UI_CARDS |

**CORE_LOGIC_QA — Resultado:** APROVADO — CSS puro, nenhum ID ou JS alterado.

---

### 2026-05-24 — Acabamento premium institucional — fase visual (Claude Code)

**Agentes executados:** UI_VISUAL_INSTITUCIONAL → UI_COMPONENTES_CARDS → CORE_LOGIC_QA

**Alterações aplicadas em `index.html` (somente CSS + 1 atributo inline no footer):**

| Elemento | Propriedade | Antes | Depois | Agente |
|----------|-------------|-------|--------|--------|
| `.titleblock .t2` | `opacity` | `.95` | `.80` | UI_VISUAL |
| `.chip` | `background` | `rgba(255,255,255,.18)` | `rgba(255,255,255,.22)` | UI_VISUAL |
| `.chip` | `border` | `rgba(255,255,255,.25)` | `rgba(255,255,255,.32)` | UI_VISUAL |
| `.chip` | `padding` | `8px 10px` | `8px 12px` | UI_VISUAL |
| `.panel` | `padding` | `18px` | `22px 24px` | UI_VISUAL |
| `.panel` (mobile) | `padding` | *(ausente)* | `16px 14px` via `@media(max-width:680px)` | UI_VISUAL |
| `.card` | `padding` | `14px` | `16px 18px` | UI_CARDS |
| `.card` | `box-shadow` | `0 1px 0 rgba(0,0,0,.02)` | `0 2px 8px rgba(0,0,0,.06)` | UI_CARDS |
| `.card` | `border-left` | `4px solid var(--line)` | `4px solid rgba(95,127,115,.28)` | UI_CARDS |
| `.card:hover` | `box-shadow` | `0 10px 22px rgba(28,54,47,.08)` | `0 8px 24px rgba(28,54,47,.13)` | UI_CARDS |
| `.card h3` | `font-size` | `17px` | `15px` | UI_CARDS |
| `.card h3` | `line-height` | `1.35` | `1.40` | UI_CARDS |
| `.link` | `word-break` | `break-all` | removido | UI_CARDS |
| `.link` | `overflow-wrap` | *(ausente)* | `break-word` | UI_CARDS |
| `.link` | `font-size` | *(herdado)* | `12px` explícito | UI_CARDS |
| `.card-date` | `font-size` | `12px` | `13px` | UI_CARDS |
| `.card-date` | `font-weight` | *(normal)* | `600` | UI_CARDS |
| `.card-date` | `color` | `var(--muted)` | `#1a5c47` | UI_CARDS |
| `.card-date` | `margin-bottom` | `6px` | `8px` | UI_CARDS |
| `.footer-copy` | `opacity` | `.70` | `.78` | UI_VISUAL |
| CARAVELA container | `opacity` | `.34` | `.22` | UI_VISUAL |

**CORE_LOGIC_QA — Resultado:** APROVADO
- Nenhum `id` alterado ou removido
- Nenhum evento JS alterado
- Nenhuma estrutura HTML alterada
- `data.json` intocado
- `scripts/` intocado
- Mudanças restritas ao bloco `<style>` e 1 atributo `opacity` inline no footer

---


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

# 2. Execute o script (busca ativa + publica automaticamente no GitHub, se houver mudanças)
bash scripts/atualizar.sh
```

---

## Como agendar atualização automática a cada 10 dias (macOS)

```bash
# Abra o editor de cron
crontab -e

# Adicione esta linha (ajuste o caminho completo):
0 8 */10 * * /bin/bash "/Users/walterolivasegundo/Downloads/Editais-Abertos-Unificados-main/scripts/atualizar.sh" >> "/Users/walterolivasegundo/Downloads/logs/unificado.log" 2>&1
```

Isso executa o script às **08h00** a cada 10 dias, fazendo busca ativa nos dois sites e publicando
automaticamente no GitHub (branch `main`) se houver mudanças em `data.json`.

**Pré-requisito único:** rodar `git push` manualmente uma vez nesta pasta (autenticando com usuário +
Personal Access Token do GitHub, ou SSH) para o macOS salvar a credencial no Keychain — o cron
reaproveita essa credencial silenciosamente nas execuções seguintes.

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
- **O ambiente Claude (Cowork) não consegue rodar o scraper nem publicar sozinho** — bloqueio de
  rede (proxy de saída não permite `fapeam.am.gov.br`/`gov.br`) e isolamento de credenciais (sandbox
  não tem acesso ao Keychain do Mac). A automação real roda via `cron` local, não via tarefa
  agendada do Claude.

---

## Publicação no GitHub Pages

1. Repositório: `https://github.com/DEPI-FVS-RCP/Editais-Abertos` (branch `main`).
2. Faça commit de todos os arquivos (incluindo o `data.json` gerado) — `scripts/atualizar.sh` já
   faz isso automaticamente após cada scraping bem-sucedido, desde que o `git push` já tenha sido
   autenticado manualmente uma vez (ver seção de agendamento acima).
3. No GitHub, em Settings → Pages → Source: branch `main`, pasta `/root`.
4. O painel está disponível em `https://depi-fvs-rcp.github.io/Editais-Abertos/`.

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
