# OrcaSlicer Studio UI — Manual de Design System & Template de Tema (`TEMA.md`)

Este documento é o guia definitivo e o **template reutilizável de arquitetura visual e técnica** desenvolvido para os plugins nativos do **OrcaSlicer 2.5.1+** (como *Orca Gear Studio* e *Orca Vase Studio*). 

Use este arquivo como ponto de partida para qualquer novo plugin sem precisar reconstruir o design, os estilos, o sistema de temas, os controles de UI ou a ponte IPC do zero.

---

## Sumário

1. [Visão Geral & Filosofia de Design](#1-visão-geral--filosofia-de-design)
2. [Tokens de Design & Variáveis CSS (`Dark` e `Light`)](#2-tokens-de-design--variáveis-css-dark-e-light)
3. [Arquitetura Híbrida: Aba Completa (`page`) vs Dock Lateral (`dock`)](#3-arquitetura-híbrida-aba-completa-page-vs-dock-lateral-dock)
4. [Catálogo de Componentes de UI (CSS + HTML)](#4-catálogo-de-componentes-de-ui-css--html)
   - [Header Bar & Printer Status Pill](#41-header-bar--printer-status-pill)
   - [Cards de Configuração & Badges](#42-cards-de-configuração--badges)
   - [Sliders Paramétricos com Valor Duplo (`factor × | mm`)](#43-sliders-paramétricos-com-valor-duplo-factor---mm)
   - [Segmented Mode Switchers](#44-segmented-mode-switchers)
   - [Pills Rápidos & Chips de Filtro](#45-pills-rápidos--chips-de-filtro)
   - [Toggle Switch Animado](#46-toggle-switch-animado)
   - [Custom Select](#47-custom-select)
   - [Grade de Presets com Miniaturas e Ações](#48-grade-de-presets-com-miniaturas-e-ações)
   - [Viewport 3D, Toolbars Flutuantes (Glassmorphism) & HUD](#49-viewport-3d-toolbars-flutuantes-glassmorphism--hud)
   - [Painel Inferior de Transporte / Micro-Controle](#410-painel-inferior-de-transporte--micro-controle)
   - [Barra de Ações (Hero Button "Enviar para a Mesa" + Exportadores)](#411-barra-de-ações-hero-button-enviar-para-a-mesa--exportadores)
   - [Toast Notifications & Alertas Pulsantes](#412-toast-notifications--alertas-pulsantes)
5. [Protocolo de Comunicação IPC (JavaScript ↔ Python)](#5-protocolo-de-comunicação-ipc-javascript--python)
6. [Template HTML5 Completo (Starter Template Pronto para Copiar)](#6-template-html5-completo-starter-template-pronto-para-copiar)
7. [Regras de Ouro e Boas Práticas do OrcaSlicer](#7-regras-de-ouro-e-boas-práticas-do-orcaslicer)

---

## 1. Visão Geral & Filosofia de Design

Os plugins modernos do OrcaSlicer rodam em um ambiente embutido **WebView2** (Windows) ou **WebKit** (macOS). Para garantir máxima performance, conformidade com a auditoria de segurança do OrcaSlicer e publicação fluida no OrcaCloud, o tema adota os seguintes princípios:

- **100% Offline (Zero CDN):** Nenhum script, folha de estilo ou fonte web externa (`Google Fonts`, `FontAwesome`, `cdnjs`). Isso evita prompts de segurança de rede (`network permission`) no fatiador e permite execução totalmente sem internet.
- **Glassmorphism & Cyberpunk Slicer Aesthetic:** Superfícies escuras com leve translucidez (`backdrop-filter: blur(8px)`), contraste refinado, bordas sutis e tipografia monospace para valores numéricos e cotas de engenharia.
- **Suporte Nativo a Dark & Light Theme:** Alternância dinâmica de variáveis CSS controlada por `data-theme="dark"` ou `data-theme="light"`.
- **Feedback Tátil em 60 FPS:** Sliders com polegar destacado, botões com transições ativas (`transform: translateY(1px)`), indicadores pulsantes em alertas e toasts flutuantes não-bloqueantes.

---

## 2. Tokens de Design & Variáveis CSS (`Dark` e `Light`)

As variáveis abaixo devem ser declaradas no topo da folha de estilos:

```css
:root,
[data-theme="dark"] {
  /* Fundos & Superfícies */
  --bg-app: #15171b;
  --bg-panel: #1d2026;
  --bg-card: #242830;
  --bg-card-hover: #2b303a;
  --bg-input: #16181d;
  --bg-viewport-top: #222731;
  --bg-viewport-bot: #111318;
  --bg-hud: rgba(23, 26, 33, 0.88);

  /* Bordas */
  --border-subtle: #313641;
  --border-strong: #434b5a;

  /* Tipografia */
  --text-main: #eef2f7;
  --text-muted: #9aa4b4;
  --text-dim: #6d7788;
  --font-sans: var(--orca-font, "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif);
  --font-mono: "Cascadia Code", Consolas, "SFMono-Regular", monospace;

  /* Cores de Destaque Primárias (Orca Teal) */
  --orca-accent: #00a896;
  --orca-accent-hover: #00bfa5;
  --orca-accent-soft: rgba(0, 191, 165, 0.15);
  --orca-accent-border: rgba(0, 191, 165, 0.48);

  /* Cores Secundárias (Azul Engenharia / Componente Secundário) */
  --secondary-accent: #4f9cf9;
  --secondary-soft: rgba(79, 156, 249, 0.15);

  /* Status & Diagnósticos */
  --status-ok: #00c853;
  --status-warn: #ffb300;
  --status-crit: #ff5252;

  /* Efeitos e Geometria */
  --shadow-soft: 0 8px 24px rgba(0, 0, 0, 0.36);
  --radius-sm: 6px;
  --radius-md: 9px;
  --radius-lg: 12px;
}

[data-theme="light"] {
  --bg-app: #edf1f6;
  --bg-panel: #ffffff;
  --bg-card: #f5f7fb;
  --bg-card-hover: #eaeff6;
  --bg-input: #ffffff;
  --bg-viewport-top: #dce3ec;
  --bg-viewport-bot: #c6d0dc;
  --bg-hud: rgba(255, 255, 255, 0.91);

  --border-subtle: #d4dce5;
  --border-strong: #b6c2cf;

  --text-main: #1b222c;
  --text-muted: #525e6f;
  --text-dim: #798596;

  --orca-accent: #00897b;
  --orca-accent-hover: #00796b;
  --orca-accent-soft: rgba(0, 137, 123, 0.12);
  --orca-accent-border: rgba(0, 137, 123, 0.45);

  --secondary-accent: #2563eb;
  --secondary-soft: rgba(37, 99, 235, 0.12);

  --status-ok: #169c46;
  --status-warn: #d47f00;
  --status-crit: #d93025;

  --shadow-soft: 0 8px 24px rgba(15, 25, 40, 0.10);
}
```

---

## 3. Arquitetura Híbrida: Aba Completa (`page`) vs Dock Lateral (`dock`)

O mesmo código HTML/CSS atende perfeitamente a **dois modos operacionais do OrcaSlicer**:

1. **Modo Página Cheia (`mode="page"`):**
   - Usado em `PagesPluginCapabilityBase` (aba dedicada superior).
   - Layout de 3 colunas em grid CSS:
     - **Coluna Esquerda (344px):** Parâmetros primários e presets.
     - **Coluna Central (1fr flexível):** Viewport 3D com canvas WebGL2, micro-simulação ou loupe.
     - **Coluna Direita (356px):** Configurações secundárias, diagnóstico CAD e footer com botão de exportar/enviar para a mesa.
2. **Modo Painel Acoplado (`mode="dock"`):**
   - Ativado simplesmente aplicando o atributo `data-mode="dock"` na tag `<body>`.
   - Converte a grid em uma pilha vertical com abas superiores compactas (`dock-tabs`), recolhe o viewport para a parte superior e oculta elementos secundários redundantes.

```css
/* Layout Padrão: 3 Colunas Studio */
.studio-workspace {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 344px minmax(380px, 1fr) 356px;
  overflow: hidden;
}

/* Modo Dock Compacto */
body[data-mode="dock"] .studio-workspace {
  display: flex;
  flex-direction: column;
}

body[data-mode="dock"] .dock-tabs {
  display: flex;
}

body[data-mode="dock"] .viewport-col {
  order: -1;
  height: 280px;
  flex-shrink: 0;
  border-bottom: 1px solid var(--border-subtle);
}
```

---

## 4. Catálogo de Componentes de UI (CSS + HTML)

### 4.1 Header Bar & Printer Status Pill

Barra de cabeçalho com logo estilizado, input de nome do modelo, indicador da impressora ativa e botões de ação rápida (Reset, Randomize, Tema Dark/Light).

```html
<header class="studio-header">
  <div class="brand-group">
    <div class="brand-logo">
      <!-- Ícone SVG inline 16x16 -->
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
      </svg>
    </div>
    <div class="brand-name-row">
      <span class="brand-title">Orca Studio Plugin</span>
      <input type="text" id="model-name-input" class="model-name-input" value="Modelo_Parametrico_01" />
    </div>
    <div class="printer-pill" id="printer-pill" title="Perfil ativo do fatiador">
      <span class="printer-dot"></span>
      <span id="printer-label">Bambu Lab X1 Carbon (0.4 nozzle)</span>
    </div>
  </div>
  <div class="header-actions">
    <button class="btn btn-icon" id="btn-theme-toggle" title="Alternar Tema Claro/Escuro">🌓</button>
    <button class="btn btn-icon" id="btn-randomize" title="Gerar Variação Aleatória">🎲</button>
    <button class="btn" id="btn-reset">↺ Reset</button>
  </div>
</header>
```

```css
.studio-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 6px 12px;
  background: var(--bg-panel);
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.brand-group {
  display: flex;
  align-items: center;
  gap: 9px;
  min-width: 0;
}

.brand-logo {
  width: 26px;
  height: 26px;
  border-radius: 7px;
  background: linear-gradient(135deg, var(--orca-accent-hover) 0%, var(--orca-accent) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 191, 165, 0.30);
}

.brand-title {
  font-weight: 700;
  font-size: 13.5px;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

.model-name-input {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 3px 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-main);
  width: 175px;
  transition: border-color 0.15s;
}
.model-name-input:focus {
  outline: none;
  border-color: var(--orca-accent);
}

.printer-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 9px;
  border-radius: 99px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  color: var(--text-muted);
  font-size: 11px;
  white-space: nowrap;
  max-width: 320px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.printer-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--orca-accent-hover);
  box-shadow: 0 0 6px var(--orca-accent);
  flex-shrink: 0;
}
```

---

### 4.2 Cards de Configuração & Badges

Estrutura padrão de agrupamento de parâmetros:

```html
<section class="studio-card">
  <div class="card-head">
    <div class="card-title">
      <span>⚙️ Geometria Principal</span>
    </div>
    <span class="card-badge" id="badge-geom">24 dentes</span>
  </div>
  <!-- Conteúdo de controles aqui -->
</section>
```

```css
.studio-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 9px 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.card-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 5px;
}

.card-badge {
  font-size: 10px;
  font-weight: 700;
  font-family: var(--font-mono);
  padding: 2px 7px;
  border-radius: 99px;
  background: var(--orca-accent-soft);
  color: var(--orca-accent-hover);
  white-space: nowrap;
}
```

---

### 4.3 Sliders Paramétricos com Valor Duplo (`factor × | mm`)

O padrão de ouro para modelagem paramétrica no fatiador: uma barra deslizante contínua acompanhada de um input numérico direto e um badge que calcula automaticamente a conversão para milímetros em tempo real.

```html
<div class="ctrl-row">
  <div class="ctrl-top">
    <span class="ctrl-label">Módulo / Altura do Dente</span>
    <div class="ctrl-val-wrap">
      <span class="dual-mm-badge" id="badge-module-mm">2.00 mm</span>
      <input type="number" id="num-module" class="ctrl-num" step="0.1" min="0.5" max="8.0" value="2.0" />
      <span class="ctrl-unit">mod</span>
    </div>
  </div>
  <input type="range" id="range-module" class="orca-slider" step="0.1" min="0.5" max="8.0" value="2.0" />
</div>
```

```css
.ctrl-row {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.ctrl-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.ctrl-label {
  font-size: 11.1px;
  color: var(--text-muted);
  font-weight: 500;
  white-space: nowrap;
}

.ctrl-val-wrap {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.dual-mm-badge {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 4px;
  background: var(--orca-accent-soft);
  color: var(--orca-accent-hover);
  border: 1px solid var(--orca-accent-border);
  white-space: nowrap;
}

.ctrl-num {
  width: 56px;
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 2px 5px;
  text-align: right;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-main);
}
.ctrl-num:focus {
  outline: none;
  border-color: var(--orca-accent);
}

.ctrl-unit {
  font-size: 10px;
  color: var(--text-dim);
  min-width: 18px;
}

/* Slider Customizado */
input[type="range"].orca-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 5px;
  border-radius: 99px;
  background: var(--border-strong);
  outline: none;
  cursor: pointer;
}

input[type="range"].orca-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: var(--orca-accent-hover);
  border: 2px solid #ffffff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.4);
  cursor: grab;
  transition: transform 0.1s;
}

input[type="range"].orca-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}
```

---

### 4.4 Segmented Mode Switchers

Para alternar entre modos exclusivos (ex.: Spur / Helicoidal / Herringbone, ou Tipos de Furo):

```html
<div class="seg-group" role="tablist">
  <button class="seg-btn active" data-val="spur">Reta (Spur)</button>
  <button class="seg-btn" data-val="helical">Helicoidal</button>
  <button class="seg-btn" data-val="herringbone">Espinha (Herringbone)</button>
</div>
```

```css
.seg-group {
  display: flex;
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 2px;
  gap: 2px;
}

.seg-btn {
  flex: 1;
  padding: 5px 6px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  font-size: 10.8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.14s;
  white-space: nowrap;
}

.seg-btn:hover {
  color: var(--text-main);
}

.seg-btn.active {
  background: var(--orca-accent);
  color: #ffffff;
}
```

---

### 4.5 Pills Rápidos & Chips de Filtro

Seletores compactos horizontais:

```html
<div class="pill-row">
  <button class="quick-pill active">Todos</button>
  <button class="quick-pill">Mecânicos</button>
  <button class="quick-pill">Brinquedos</button>
  <button class="quick-pill">Robótica</button>
</div>
```

```css
.pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.quick-pill {
  flex: 1;
  min-width: 0;
  padding: 3px 6px;
  font-size: 10.5px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-input);
  color: var(--text-muted);
  cursor: pointer;
  text-align: center;
  transition: all 0.12s;
  white-space: nowrap;
}

.quick-pill:hover {
  border-color: var(--border-strong);
  color: var(--text-main);
}

.quick-pill.active {
  background: var(--orca-accent);
  border-color: var(--orca-accent);
  color: #ffffff;
}
```

---

### 4.6 Toggle Switch Animado

Chaves tipo iOS/macOS para ligar/desligar opções (ex.: "Auto-Configurar Slicer", "Alívio de Peso"):

```html
<div class="switch-row">
  <span class="ctrl-label">Auto-ajustar Parâmetros de Fatiamento</span>
  <label class="toggle-switch">
    <input type="checkbox" id="toggle-slicer-sync" checked />
    <span class="toggle-track"></span>
  </label>
</div>
```

```css
.switch-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 34px;
  height: 18px;
  flex-shrink: 0;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-track {
  position: absolute;
  inset: 0;
  background: var(--border-strong);
  border-radius: 99px;
  cursor: pointer;
  transition: background 0.18s;
}

.toggle-track::before {
  content: "";
  position: absolute;
  width: 14px;
  height: 14px;
  left: 2px;
  top: 2px;
  border-radius: 50%;
  background: #ffffff;
  transition: transform 0.18s;
}

.toggle-switch input:checked + .toggle-track {
  background: var(--orca-accent);
}

.toggle-switch input:checked + .toggle-track::before {
  transform: translateX(16px);
}
```

---

### 4.7 Custom Select

Menus suspensos customizados combinando com a paleta do fatiador:

```html
<select class="studio-select" id="select-bore-type">
  <option value="none">Sólido (Sem Furo)</option>
  <option value="round" selected>Cilíndrico Padrão (Round)</option>
  <option value="d_shaft">Eixo D (D-Shaft com Trava)</option>
  <option value="hex">Sextavado (Hex Nut / M4)</option>
</select>
```

```css
.studio-select {
  width: 100%;
  background: var(--bg-input);
  color: var(--text-main);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 5px 8px;
  font-size: 11.3px;
  font-weight: 600;
  cursor: pointer;
}
.studio-select:focus {
  outline: none;
  border-color: var(--orca-accent);
}
```

---

### 4.8 Grade de Presets com Miniaturas e Ações

Exibição em duas colunas com miniatura SVG vetorial embutida e botão rápido de exclusão:

```html
<div class="presets-grid" id="presets-grid">
  <div class="preset-card active">
    <div class="preset-thumb">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="var(--orca-accent)"><circle cx="12" cy="12" r="8"/></svg>
    </div>
    <div class="preset-meta">
      <div class="preset-name">Redução Standard 2:1</div>
      <div class="preset-sub">Helicoidal 45° • Módulo 1.5</div>
    </div>
    <button class="preset-del-btn" title="Excluir Preset">×</button>
  </div>
</div>
```

```css
.presets-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 5px;
  max-height: 180px;
  overflow-y: auto;
  padding-right: 2px;
}

.preset-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 6px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel);
  cursor: pointer;
  transition: border-color 0.14s, background 0.14s;
  text-align: left;
}
.preset-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-strong);
}
.preset-card.active {
  border-color: var(--orca-accent-hover);
  background: var(--orca-accent-soft);
}

.preset-thumb {
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preset-meta {
  min-width: 0;
  flex: 1;
}

.preset-name {
  font-size: 10.8px;
  font-weight: 600;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.preset-sub {
  font-size: 9.6px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.preset-del-btn {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: none;
  background: rgba(255, 82, 82, 0.16);
  color: var(--status-crit);
  font-size: 11px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.preset-del-btn:hover {
  background: var(--status-crit);
  color: #ffffff;
}
```

---

### 4.9 Viewport 3D, Toolbars Flutuantes (Glassmorphism) & HUD

O palco 3D possui degradê radial sutil e elementos flutuantes transparentes com efeito *frosted glass*:

```html
<div class="viewport-col">
  <div class="vp-stage-3d">
    <canvas id="gl-canvas"></canvas>

    <!-- Toolbar Flutuante Superior Esquerda -->
    <div class="vp-toolbar-left vp-glass">
      <button class="vp-chip active" id="chip-shading">Sólido</button>
      <button class="vp-chip" id="chip-wireframe">Wireframe</button>
      <button class="vp-chip" id="chip-xray">Raio-X</button>
    </div>

    <!-- HUD Flutuante Superior Direita -->
    <div class="vp-hud-right vp-glass">
      <div class="hud-title-row">
        <span>Diagnóstico CAD</span>
        <span class="hud-status-pill ok">OK (Imprimível)</span>
      </div>
      <div class="hud-grid">
        <div class="hud-metric">
          <span class="hud-metric-k">Distância de Centros</span>
          <span class="hud-metric-v">45.00 mm</span>
        </div>
        <div class="hud-metric">
          <span class="hud-metric-k">Folga no Flanco (Backlash)</span>
          <span class="hud-metric-v">0.18 mm</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

```css
.vp-stage-3d {
  position: relative;
  flex: 1;
  min-height: 200px;
  background: radial-gradient(circle at 50% 35%, var(--bg-viewport-top) 0%, var(--bg-viewport-bot) 100%);
  overflow: hidden;
}

#gl-canvas {
  width: 100%;
  height: 100%;
  display: block;
  touch-action: none;
  cursor: grab;
}
#gl-canvas:active {
  cursor: grabbing;
}

.vp-glass {
  background: var(--bg-hud);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-soft);
}

.vp-toolbar-left {
  position: absolute;
  top: 9px;
  left: 9px;
  display: flex;
  gap: 4px;
  padding: 4px;
  z-index: 10;
}

.vp-chip {
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-muted);
  font-size: 10.8px;
  font-weight: 600;
  cursor: pointer;
}
.vp-chip:hover {
  color: var(--text-main);
}
.vp-chip.active {
  background: var(--orca-accent);
  color: #ffffff;
}

.vp-hud-right {
  position: absolute;
  top: 9px;
  right: 9px;
  width: 220px;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  z-index: 10;
}

.hud-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
}

.hud-status-pill {
  padding: 1px 7px;
  border-radius: 99px;
  font-size: 9.8px;
  font-weight: 700;
}
.hud-status-pill.ok {
  background: rgba(0, 200, 83, 0.18);
  color: var(--status-ok);
}
.hud-status-pill.warn {
  background: rgba(255, 179, 0, 0.20);
  color: var(--status-warn);
}
.hud-status-pill.crit {
  background: rgba(255, 82, 82, 0.22);
  color: var(--status-crit);
}

.hud-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px 8px;
}

.hud-metric-k {
  font-size: 9.5px;
  color: var(--text-dim);
}
.hud-metric-v {
  font-family: var(--font-mono);
  font-size: 10.8px;
  font-weight: 600;
  color: var(--text-main);
}
```

---

### 4.10 Painel Inferior de Transporte / Micro-Controle

Barra dedicada a animação, controle de RPM ou passos incrementais:

```html
<div class="sim-transport-bar">
  <div class="sim-row">
    <button class="btn btn-soft" id="btn-sim-play">▶ Play</button>
    <div class="sim-flex-slider">
      <span class="sim-tag">Giro:</span>
      <input type="range" id="sim-speed-slider" class="orca-slider" min="1.0" max="10.0" step="0.5" value="1.0" />
      <span class="sim-mono" id="sim-speed-val">1.0 RPM</span>
    </div>
  </div>
</div>
```

```css
.sim-transport-bar {
  background: var(--bg-panel);
  border-top: 1px solid var(--border-subtle);
  border-bottom: 1px solid var(--border-subtle);
  padding: 6px 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  flex-shrink: 0;
}

.sim-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.sim-flex-slider {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 140px;
}

.sim-tag {
  font-size: 10.5px;
  font-weight: 700;
  color: var(--text-muted);
}

.sim-mono {
  font-family: var(--font-mono);
  font-size: 10.8px;
  font-weight: 700;
  color: var(--orca-accent-hover);
  min-width: 55px;
  text-align: right;
}
```

---

### 4.11 Barra de Ações (Hero Button "Enviar para a Mesa" + Exportadores)

Rodapé fixo que acomoda a ação principal com gradiente chamativo e os botões auxiliares para baixar arquivos em disco:

```html
<footer class="action-footer">
  <button class="btn-hero" id="btn-send-to-plater">
    <span>🚀 Enviar Direto para a Mesa (Plater)</span>
  </button>
  <div class="export-btn-row">
    <button class="btn" id="btn-export-stl">💾 Exportar STL</button>
    <button class="btn" id="btn-export-3mf">📦 Projeto 3MF</button>
  </div>
</footer>
```

```css
.action-footer {
  padding: 9px 10px;
  background: var(--bg-panel);
  border-top: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;
}

.btn-hero {
  width: 100%;
  padding: 10px 14px;
  font-size: 12.8px;
  font-weight: 700;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--orca-accent-hover) 0%, var(--orca-accent) 100%);
  color: #ffffff;
  border: none;
  box-shadow: 0 4px 14px rgba(0, 191, 165, 0.32);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: filter 0.15s, transform 0.08s;
}
.btn-hero:hover:not(:disabled) {
  filter: brightness(1.08);
}
.btn-hero:active:not(:disabled) {
  transform: translateY(1px);
}
.btn-hero:disabled {
  opacity: 0.55;
  cursor: wait;
}

.export-btn-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}
```

---

### 4.12 Toast Notifications & Alertas Pulsantes

Para dar feedback imediato de ações concluídas ou erros de validação:

```html
<div class="toast-banner" id="toast-banner">Peças adicionadas à mesa com sucesso!</div>
```

```css
.toast-banner {
  position: fixed;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%) translateY(20px);
  opacity: 0;
  pointer-events: none;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  background: var(--bg-card);
  border: 1px solid var(--orca-accent);
  color: var(--text-main);
  font-size: 12px;
  font-weight: 600;
  box-shadow: var(--shadow-soft);
  transition: opacity 0.2s, transform 0.2s;
  z-index: 999;
  max-width: 90vw;
}
.toast-banner.visible {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
.toast-banner.error {
  border-color: var(--status-crit);
  color: var(--status-crit);
}

/* Alerta Pulsante de Colisão ou Travamento */
.jam-alert-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 2px 8px;
  border-radius: 99px;
  background: rgba(255, 42, 42, 0.22);
  border: 1px solid var(--status-crit);
  color: #ff6b6b;
  font-size: 10px;
  font-weight: 800;
  animation: jamPulse 0.9s infinite alternate;
}

@keyframes jamPulse {
  from { transform: scale(1.0); box-shadow: 0 0 0 rgba(255, 82, 82, 0); }
  to   { transform: scale(1.02); box-shadow: 0 0 10px rgba(255, 82, 82, 0.45); }
}
```

---

## 5. Protocolo de Comunicação IPC (JavaScript ↔ Python)

A camada de interface comunica-se com o Python através de um manipulador universal resiliente.

```javascript
// Utilitário universal para envio ao Python host
function sendToHost(payload) {
  const jsonStr = typeof payload === "string" ? payload : JSON.stringify(payload);
  if (window.chrome && window.chrome.webview && typeof window.chrome.webview.postMessage === "function") {
    // Windows WebView2 oficial
    window.chrome.webview.postMessage(jsonStr);
  } else if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.orca) {
    // macOS WebKit
    window.webkit.messageHandlers.orca.postMessage(jsonStr);
  } else {
    // Fallback de desenvolvimento local no navegador
    console.log("[IPC -> Host]:", payload);
  }
}

// Receptor universal chamado pelo Python host
window.onHostMessage = function(data) {
  const msg = typeof data === "string" ? JSON.parse(data) : data;
  switch (msg.type) {
    case "init_state":
      applyInitialState(msg.params, msg.builtin_presets);
      break;
    case "analysis_result":
      updateDiagnosticsHUD(msg.report);
      break;
    case "action_result":
      if (msg.ok) {
        showToast(msg.message || "Operação realizada com sucesso!");
      } else {
        showToast(msg.message || "Falha na operação", true);
      }
      break;
  }
};

// Ao carregar o DOM, avisa o Python imediatamente
window.addEventListener("DOMContentLoaded", () => {
  sendToHost({ type: "ready", mode: document.body.dataset.mode || "page" });
});
```

---

## 6. Template HTML5 Completo (Starter Template Pronto para Copiar)

Copie e cole este esqueleto para inicializar qualquer novo plugin:

```html
<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>OrcaSlicer Plugin Starter</title>
<style>
/* ==========================================================================
   1. TOKENS DE DESIGN
   ========================================================================== */
:root, [data-theme="dark"] {
  --bg-app: #15171b;
  --bg-panel: #1d2026;
  --bg-card: #242830;
  --bg-card-hover: #2b303a;
  --bg-input: #16181d;
  --bg-viewport-top: #222731;
  --bg-viewport-bot: #111318;
  --bg-hud: rgba(23, 26, 33, 0.88);
  --border-subtle: #313641;
  --border-strong: #434b5a;
  --text-main: #eef2f7;
  --text-muted: #9aa4b4;
  --text-dim: #6d7788;
  --orca-accent: #00a896;
  --orca-accent-hover: #00bfa5;
  --orca-accent-soft: rgba(0, 191, 165, 0.15);
  --orca-accent-border: rgba(0, 191, 165, 0.48);
  --status-ok: #00c853;
  --status-warn: #ffb300;
  --status-crit: #ff5252;
  --shadow-soft: 0 8px 24px rgba(0, 0, 0, 0.36);
  --radius-sm: 6px;
  --radius-md: 9px;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: "Cascadia Code", Consolas, monospace;
}

[data-theme="light"] {
  --bg-app: #edf1f6;
  --bg-panel: #ffffff;
  --bg-card: #f5f7fb;
  --bg-card-hover: #eaeff6;
  --bg-input: #ffffff;
  --bg-viewport-top: #dce3ec;
  --bg-viewport-bot: #c6d0dc;
  --bg-hud: rgba(255, 255, 255, 0.91);
  --border-subtle: #d4dce5;
  --border-strong: #b6c2cf;
  --text-main: #1b222c;
  --text-muted: #525e6f;
  --text-dim: #798596;
  --orca-accent: #00897b;
  --orca-accent-hover: #00796b;
  --orca-accent-soft: rgba(0, 137, 123, 0.12);
  --orca-accent-border: rgba(0, 137, 123, 0.45);
  --status-ok: #169c46;
  --status-warn: #d47f00;
  --status-crit: #d93025;
  --shadow-soft: 0 8px 24px rgba(15, 25, 40, 0.10);
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  width: 100%; height: 100%; overflow: hidden;
  background: var(--bg-app); color: var(--text-main);
  font-family: var(--font-sans); font-size: 12px; user-select: none;
}
button, input, select { font-family: inherit; font-size: inherit; color: inherit; }

/* ==========================================================================
   2. ESTRUTURA GERAL & GRID
   ========================================================================== */
.studio-shell { display: flex; flex-direction: column; width: 100%; height: 100%; }
.studio-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 6px 12px; background: var(--bg-panel); border-bottom: 1px solid var(--border-subtle);
}
.brand-group { display: flex; align-items: center; gap: 8px; }
.brand-logo {
  width: 26px; height: 26px; border-radius: 6px;
  background: linear-gradient(135deg, var(--orca-accent-hover), var(--orca-accent));
  display: flex; align-items: center; justify-content: center; color: #fff; font-weight: bold;
}
.brand-title { font-weight: 700; font-size: 13px; }

.studio-workspace {
  flex: 1; min-height: 0; display: grid;
  grid-template-columns: 340px 1fr 340px; overflow: hidden;
}
.col-panel { display: flex; flex-direction: column; background: var(--bg-panel); min-height: 0; }
.col-left { border-right: 1px solid var(--border-subtle); }
.col-right { border-left: 1px solid var(--border-subtle); }
.col-scroll { flex: 1; overflow-y: auto; padding: 10px; display: flex; flex-direction: column; gap: 10px; }

/* Palco Central 3D */
.viewport-col { display: flex; flex-direction: column; background: var(--bg-app); position: relative; }
.vp-stage-3d {
  flex: 1; position: relative;
  background: radial-gradient(circle at 50% 35%, var(--bg-viewport-top) 0%, var(--bg-viewport-bot) 100%);
}
#gl-canvas { width: 100%; height: 100%; display: block; }

/* Componentes */
.studio-card {
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md); padding: 10px; display: flex; flex-direction: column; gap: 8px;
}
.card-head { display: flex; justify-content: space-between; align-items: center; font-weight: 700; font-size: 11px; }
.card-badge {
  font-family: var(--font-mono); font-size: 10px; padding: 1px 6px;
  border-radius: 99px; background: var(--orca-accent-soft); color: var(--orca-accent-hover);
}

.ctrl-row { display: flex; flex-direction: column; gap: 4px; }
.ctrl-top { display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); }
.ctrl-num {
  width: 55px; background: var(--bg-input); border: 1px solid var(--border-subtle);
  border-radius: 4px; padding: 2px 4px; text-align: right; color: var(--text-main); font-family: var(--font-mono);
}
input[type="range"].orca-slider {
  -webkit-appearance: none; width: 100%; height: 5px; border-radius: 99px;
  background: var(--border-strong); outline: none; cursor: pointer;
}
input[type="range"].orca-slider::-webkit-slider-thumb {
  -webkit-appearance: none; width: 13px; height: 13px; border-radius: 50%;
  background: var(--orca-accent-hover); border: 2px solid #fff; cursor: grab;
}

/* Footer de Ações */
.action-footer {
  padding: 10px; background: var(--bg-panel); border-top: 1px solid var(--border-subtle);
  display: flex; flex-direction: column; gap: 6px;
}
.btn-hero {
  padding: 10px; border-radius: var(--radius-md); border: none; font-weight: 700; cursor: pointer;
  background: linear-gradient(135deg, var(--orca-accent-hover), var(--orca-accent)); color: #fff;
  box-shadow: 0 4px 12px rgba(0, 191, 165, 0.3);
}
.btn-hero:hover { filter: brightness(1.08); }
.btn-secondary {
  padding: 6px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);
  background: var(--bg-card); color: var(--text-main); font-weight: 600; cursor: pointer;
}

/* Toast */
.toast-banner {
  position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%) translateY(20px);
  opacity: 0; pointer-events: none; padding: 8px 16px; border-radius: var(--radius-md);
  background: var(--bg-card); border: 1px solid var(--orca-accent); color: var(--text-main);
  box-shadow: var(--shadow-soft); transition: all 0.2s; z-index: 1000;
}
.toast-banner.visible { opacity: 1; transform: translateX(-50%) translateY(0); }
</style>
</head>
<body>
<div class="studio-shell">
  <!-- Top Header -->
  <header class="studio-header">
    <div class="brand-group">
      <div class="brand-logo">★</div>
      <span class="brand-title">Meu Plugin OrcaSlicer</span>
    </div>
    <div>
      <button class="btn-secondary" id="btn-theme-toggle">🌓 Tema</button>
    </div>
  </header>

  <!-- Workspace -->
  <main class="studio-workspace">
    <!-- Coluna 1: Parâmetros -->
    <aside class="col-panel col-left">
      <div class="col-scroll">
        <section class="studio-card">
          <div class="card-head">
            <span>Dimensões</span>
            <span class="card-badge">mm</span>
          </div>
          <div class="ctrl-row">
            <div class="ctrl-top">
              <span>Diâmetro Base</span>
              <input type="number" id="num-dia" class="ctrl-num" value="50" />
            </div>
            <input type="range" id="range-dia" class="orca-slider" min="10" max="150" value="50" />
          </div>
        </section>
      </div>
    </aside>

    <!-- Coluna 2: Palco 3D -->
    <section class="viewport-col">
      <div class="vp-stage-3d">
        <canvas id="gl-canvas"></canvas>
      </div>
    </section>

    <!-- Coluna 3: Opções & Ação -->
    <aside class="col-panel col-right">
      <div class="col-scroll">
        <section class="studio-card">
          <div class="card-head"><span>Resumo CAD</span></div>
          <p style="color:var(--text-muted);font-size:11px;">Status: Pronto para fatiar.</p>
        </section>
      </div>
      <footer class="action-footer">
        <button class="btn-hero" id="btn-send">🚀 Enviar para a Mesa (Plater)</button>
        <button class="btn-secondary" id="btn-export">💾 Exportar STL</button>
      </footer>
    </aside>
  </main>
</div>

<div class="toast-banner" id="toast-banner">Notificação</div>

<script>
// IPC Universal com o OrcaSlicer Host
function sendToHost(payload) {
  const jsonStr = typeof payload === "string" ? payload : JSON.stringify(payload);
  if (window.chrome && window.chrome.webview) {
    window.chrome.webview.postMessage(jsonStr);
  } else if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.orca) {
    window.webkit.messageHandlers.orca.postMessage(jsonStr);
  } else {
    console.log("[IPC Debug]:", payload);
  }
}

function showToast(text) {
  const toast = document.getElementById("toast-banner");
  toast.textContent = text;
  toast.classList.add("visible");
  setTimeout(() => toast.classList.remove("visible"), 3200);
}

// Alternar Tema
document.getElementById("btn-theme-toggle").addEventListener("click", () => {
  const root = document.documentElement;
  const current = root.getAttribute("data-theme") || "dark";
  root.setAttribute("data-theme", current === "dark" ? "light" : "dark");
});

// Sincronizar Sliders e Inputs Numéricos
const rDia = document.getElementById("range-dia");
const nDia = document.getElementById("num-dia");
rDia.addEventListener("input", (e) => { nDia.value = e.target.value; });
nDia.addEventListener("input", (e) => { rDia.value = e.target.value; });

// Ações
document.getElementById("btn-send").addEventListener("click", () => {
  showToast("Enviando modelo para o fatiador...");
  sendToHost({ type: "send_to_plater", diameter: parseFloat(nDia.value) });
});

window.addEventListener("DOMContentLoaded", () => {
  sendToHost({ type: "ready", mode: "page" });
});
</script>
</body>
</html>
```

---

## 7. Regras de Ouro e Boas Práticas do OrcaSlicer

Ao criar novos plugins baseados neste template, siga à risca estas regras de engenharia:

1. **Injeção de Arquivos na Mesa (`Plater`) na Main UI Thread:**
   - **No Windows:** Use Win32 in-process `WM_COPYDATA` (`dwData = 1`, payload `"orca-slicer.exe";"C:\\caminho\\arquivo.stl"` sem ponto e vírgula no final). Nunca chame `subprocess.Popen("orca-slicer.exe", ...)` pois isso abre uma nova janela ou trava a instância ativa.
   - **No macOS:** Despache via Cocoa GCD na thread principal (`_dispatch_main_q`) usando `[NSApp.delegate application:NSApp openFiles:@[path]]`.
   - **Atenção:** Ambas as operações devem ocorrer na **Main UI Thread** do `on_message` para manter compatibilidade com o modelo STA COM do `WebView2`.
2. **Sanitização de Nomes de Arquivo:**
   - O `PluginAuditManager` do OrcaSlicer bloqueia qualquer acesso a caminhos que contenham trechos como `secret`, `cert` ou `conf` (case-insensitive). Certifique-se de que sua função de gerar nomes de STL substitua essas palavras.
3. **Publicação no OrcaCloud (GitHub OIDC):**
   - No workflow `.github/workflows/publish-orcacloud.yml`, os arquivos `.py` enviados devem obrigatoriamente ter o sufixo universal `_any.py` (ex.: `meu_plugin_any.py`), e os wheels devem terminar em `-py3-none-any.whl`.
4. **Preservação de `.install_state.json`:**
   - Durante a compilação e cópia para `%APPDATA%\OrcaSlicer\orca_plugins\<plugin_name>\`, preserve estritamente o arquivo `.install_state.json` criado pelo próprio OrcaSlicer, garantindo que o checkbox de ativação continue marcado.

---
*Documento gerado como base padrão de engenharia para o ecossistema de plugins do OrcaSlicer.*
