"""Self-contained offline HTML5 + CSS3 + WebGL2 + 2D Tooth-Mesh Loupe Studio UI for Orca Gear Studio.

Generates the interactive 3D & 2D parametric mechanical gear design studio for both:
- `mode="page"`: Wide 3-column engineering studio tab inside OrcaSlicer (`PagesPluginCapabilityBase`)
- `mode="dock"`: Compact tabbed side-docked panel beside OrcaSlicer's 3D Plater (`UiDockPanel`)

Zero external CDN scripts, stylesheets, or web fonts are referenced so WebView2 runs 100% offline
without network permission prompts.
"""

from __future__ import annotations

import copy
import json
from typing import Any

if "DEFAULT_PARAMS" not in globals():
    try:
        from .schema import DEFAULT_PARAMS
    except Exception:
        DEFAULT_PARAMS = None  # type: ignore[assignment]

if "BUILTIN_PRESETS" not in globals():
    try:
        from .presets_catalog import BUILTIN_PRESETS
    except Exception:
        BUILTIN_PRESETS = None  # type: ignore[assignment]

__all__ = ["get_studio_html"]


def _studio_ui_safe_json(payload: dict[str, Any]) -> str:
    """Serialize payload into script-safe JSON (escaping `</` and Unicode line separators)."""
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return (
        raw.replace("</", "<\\/")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


_STUDIO_UI_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="__INITIAL_LANG__" data-theme="__INITIAL_THEME__">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Orca Gear Studio</title>
<style>
:root,
[data-theme="dark"] {
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
  --gear2-accent: #4f9cf9;
  --gear2-soft: rgba(79, 156, 249, 0.15);
  --status-ok: #00c853;
  --status-warn: #ffb300;
  --status-crit: #ff5252;
  --shadow-soft: 0 8px 24px rgba(0, 0, 0, 0.36);
  --radius-sm: 6px;
  --radius-md: 9px;
  --radius-lg: 12px;
  --font-sans: var(--orca-font, "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif);
  --font-mono: "Cascadia Code", Consolas, "SFMono-Regular", monospace;
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
  --gear2-accent: #2563eb;
  --gear2-soft: rgba(37, 99, 235, 0.12);
  --status-ok: #169c46;
  --status-warn: #d47f00;
  --status-crit: #d93025;
  --shadow-soft: 0 8px 24px rgba(15, 25, 40, 0.10);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--bg-app);
  color: var(--text-main);
  font-family: var(--font-sans);
  font-size: 12.2px;
  line-height: 1.38;
  user-select: none;
  -webkit-font-smoothing: antialiased;
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: var(--border-strong);
  border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--orca-accent);
}

button, input, select {
  font-family: inherit;
  font-size: inherit;
  color: inherit;
}

.studio-shell {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

/* Header Bar */
.studio-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 6px 12px;
  background: var(--bg-panel);
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
  z-index: 20;
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
  background: linear-gradient(135deg, #00bfa5 0%, #00796b 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 191, 165, 0.30);
}

.brand-name-row {
  display: flex;
  align-items: center;
  gap: 7px;
}

.brand-title {
  font-weight: 700;
  font-size: 13.5px;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

.gear-name-input {
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
.gear-name-input:focus {
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
  max-width: 340px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.printer-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--orca-accent-hover);
  flex-shrink: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 5px;
  flex-shrink: 0;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 5px 9px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-card);
  color: var(--text-main);
  font-weight: 600;
  font-size: 11.2px;
  cursor: pointer;
  transition: background 0.14s, border-color 0.14s, transform 0.08s;
  white-space: nowrap;
}
.btn:hover:not(:disabled) {
  background: var(--bg-card-hover);
  border-color: var(--border-strong);
}
.btn:active:not(:disabled) {
  transform: translateY(1px);
}
.btn:disabled {
  opacity: 0.42;
  cursor: not-allowed;
}

.btn-icon {
  padding: 5px 7px;
}

.btn-accent {
  background: linear-gradient(135deg, var(--orca-accent) 0%, #00897b 100%);
  border-color: transparent;
  color: #ffffff;
}
.btn-accent:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--orca-accent-hover) 0%, var(--orca-accent) 100%);
  border-color: transparent;
}

.btn-soft {
  background: var(--orca-accent-soft);
  border-color: var(--orca-accent-border);
  color: var(--orca-accent-hover);
}
[data-theme="light"] .btn-soft {
  color: var(--orca-accent);
}
.btn-soft:hover:not(:disabled) {
  background: var(--orca-accent);
  color: #ffffff;
}

/* Main Workspace Grid */
.studio-workspace {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 344px minmax(380px, 1fr) 356px;
  overflow: hidden;
}

.col-panel {
  display: flex;
  flex-direction: column;
  min-height: 0;
  background: var(--bg-panel);
  overflow: hidden;
}
.col-left {
  border-right: 1px solid var(--border-subtle);
}
.col-right {
  border-left: 1px solid var(--border-subtle);
}

.col-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 9px;
  display: flex;
  flex-direction: column;
  gap: 9px;
}

/* Dock Mode Navigation Tabs */
.dock-tabs {
  display: none;
  background: var(--bg-panel);
  border-bottom: 1px solid var(--border-subtle);
  padding: 4px 6px;
  gap: 4px;
  flex-shrink: 0;
}

.dock-tab-btn {
  flex: 1;
  padding: 5px 4px;
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-muted);
  font-size: 10.8px;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  transition: all 0.14s;
}
.dock-tab-btn:hover {
  color: var(--text-main);
  background: var(--bg-card);
}
.dock-tab-btn.active {
  background: var(--orca-accent-soft);
  border-color: var(--orca-accent-border);
  color: var(--orca-accent-hover);
}
[data-theme="light"] .dock-tab-btn.active {
  color: var(--orca-accent);
}

/* Cards & Sections */
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
[data-theme="light"] .card-badge {
  color: var(--orca-accent);
}

/* Quick Pills Row */
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

/* Presets Grid */
.preset-filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.filter-chip {
  padding: 2px 7px;
  font-size: 10.2px;
  font-weight: 600;
  border-radius: 99px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-input);
  color: var(--text-muted);
  cursor: pointer;
}
.filter-chip.active {
  background: var(--orca-accent);
  border-color: var(--orca-accent);
  color: #ffffff;
}

.presets-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 5px;
  max-height: 178px;
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
  width: 32px;
  height: 32px;
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
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.preset-del-btn:hover {
  background: var(--status-crit);
  color: #ffffff;
}

.save-preset-bar {
  display: none;
  gap: 5px;
  align-items: center;
  padding-top: 4px;
  border-top: 1px dashed var(--border-subtle);
}
.save-preset-bar.open {
  display: flex;
}
.save-preset-input {
  flex: 1;
  min-width: 0;
  background: var(--bg-input);
  border: 1px solid var(--orca-accent-border);
  border-radius: var(--radius-sm);
  padding: 4px 7px;
  font-size: 11.2px;
}

/* Segmented Mode Switch */
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
  padding: 5px 5px;
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
.seg-btn.active {
  background: var(--orca-accent);
  color: #ffffff;
}
.seg-btn.active-g2 {
  background: var(--gear2-accent);
  color: #ffffff;
}

/* Slider Controls & Dual Badges */
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
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
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
[data-theme="light"] .dual-mm-badge {
  color: var(--orca-accent);
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
  min-width: 16px;
}

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
  transform: scale(1.15);
}

/* Toggle Switch */
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

.sub-feature-box {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 7px 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* Center Column: 3D Stage + Sim Transport Bar + 2D Tooth-Mesh Loupe */
.viewport-col {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  background: var(--bg-app);
  overflow: hidden;
}

.vp-stage-3d {
  position: relative;
  flex: 1;
  min-height: 180px;
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

.vp-toolbar-left {
  position: absolute;
  top: 9px;
  left: 9px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  max-width: calc(100% - 225px);
  z-index: 10;
}

.vp-glass {
  background: var(--bg-hud);
  backdrop-filter: blur(8px);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-soft);
}

.vp-chip {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-hud);
  color: var(--text-muted);
  font-size: 10.8px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.vp-chip:hover {
  color: var(--text-main);
  border-color: var(--border-strong);
}
.vp-chip.active {
  background: var(--orca-accent);
  border-color: var(--orca-accent);
  color: #ffffff;
}

.vp-cam-bar {
  position: absolute;
  bottom: 9px;
  left: 9px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  z-index: 10;
}

.vp-cut-bar {
  position: absolute;
  bottom: 9px;
  right: 9px;
  width: 248px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 9px;
  z-index: 10;
}

.vp-cut-label {
  font-size: 10.5px;
  font-weight: 600;
  white-space: nowrap;
  color: var(--text-muted);
}

/* 3D Force Vectors & Status HUD */
.vp-hud-right {
  position: absolute;
  top: 9px;
  right: 9px;
  width: 210px;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  z-index: 10;
}

.hud-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
  gap: 4px 7px;
}

.hud-metric {
  display: flex;
  flex-direction: column;
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

.thrust-banner {
  font-size: 10px;
  font-weight: 600;
  padding: 3px 6px;
  border-radius: 4px;
  background: rgba(0, 191, 165, 0.12);
  border-left: 2px solid var(--orca-accent);
  color: var(--text-main);
}
.thrust-banner.axial-active {
  background: rgba(255, 179, 0, 0.14);
  border-left-color: #f59e0b;
}

.heatmap-legend {
  display: none;
  align-items: center;
  gap: 6px;
  font-size: 9.8px;
  padding-top: 4px;
  border-top: 1px solid var(--border-subtle);
  color: var(--text-muted);
}
.heatmap-legend.visible {
  display: flex;
}
.legend-swatch {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  display: inline-block;
}

/* Micro-Simulation Transport & Live Delta_a Bar */
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
  gap: 7px;
  flex-wrap: wrap;
}

.sim-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.sim-flex-slider {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 135px;
}

.sim-tag {
  font-size: 10.3px;
  font-weight: 700;
  color: var(--text-muted);
  white-space: nowrap;
}

.sim-mono {
  font-family: var(--font-mono);
  font-size: 10.8px;
  font-weight: 700;
  color: var(--orca-accent-hover);
  min-width: 52px;
  text-align: right;
  white-space: nowrap;
}
[data-theme="light"] .sim-mono {
  color: var(--orca-accent);
}

.step-btn {
  padding: 2px 5px;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  border-radius: 4px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-card);
  color: var(--text-main);
  cursor: pointer;
}
.step-btn:hover {
  background: var(--bg-card-hover);
  border-color: var(--orca-accent);
}

/* Synchronized 2D Tooth-Mesh Loupe Panel */
.loupe-panel {
  height: 196px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: var(--bg-input);
  position: relative;
  overflow: hidden;
}
.loupe-panel.collapsed {
  height: 28px;
}

.loupe-header {
  height: 28px;
  padding: 0 10px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-shrink: 0;
}

.loupe-title {
  font-size: 10.8px;
  font-weight: 700;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}

.jam-alert-badge {
  display: none;
  align-items: center;
  gap: 5px;
  padding: 2px 8px;
  border-radius: 99px;
  background: rgba(255, 42, 42, 0.22);
  border: 1px solid var(--status-crit);
  color: #ff6b6b;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.3px;
  animation: jamPulse 0.9s infinite alternate;
}
[data-theme="light"] .jam-alert-badge {
  color: #c62828;
  background: rgba(217, 48, 37, 0.15);
}
.jam-alert-badge.visible {
  display: inline-flex;
}

@keyframes jamPulse {
  from { transform: scale(1.0); box-shadow: 0 0 0 rgba(255, 82, 82, 0); }
  to   { transform: scale(1.02); box-shadow: 0 0 10px rgba(255, 82, 82, 0.45); }
}

.loupe-canvas-wrap {
  position: relative;
  flex: 1;
  min-height: 0;
}

#loupe-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

/* Diagnostics Grid in Right Column */
.diag-section-title {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.45px;
  color: var(--orca-accent-hover);
  padding-top: 4px;
  border-top: 1px solid var(--border-subtle);
}
[data-theme="light"] .diag-section-title {
  color: var(--orca-accent);
}

.diag-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 5px 8px;
}

.diag-cell {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 5px;
  padding: 4px 7px;
  display: flex;
  flex-direction: column;
}

.diag-k {
  font-size: 9.6px;
  color: var(--text-dim);
}
.diag-v {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  color: var(--text-main);
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 120px;
  overflow-y: auto;
}

.issue-item {
  font-size: 10.3px;
  padding: 4px 7px;
  border-radius: 4px;
  background: rgba(0, 200, 83, 0.10);
  border-left: 2.5px solid var(--status-ok);
  color: var(--text-main);
}
.issue-item.warn {
  background: rgba(255, 179, 0, 0.13);
  border-left-color: var(--status-warn);
}
.issue-item.critical {
  background: rgba(255, 82, 82, 0.16);
  border-left-color: var(--status-crit);
}

.helper-note {
  font-size: 10.3px;
  color: var(--text-muted);
  background: var(--bg-input);
  border-left: 2px solid var(--orca-accent);
  padding: 5px 7px;
  border-radius: 0 4px 4px 0;
}

/* Sticky Action Footer */
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
  background: linear-gradient(135deg, #00bfa5 0%, #00897b 100%);
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
  filter: brightness(1.07);
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
  grid-template-columns: 1fr 1fr auto;
  gap: 6px;
}

/* Toast Notification */
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
}

.dock-global-footer {
  display: none;
}

/* ============================================================================
   COMPACT SIDE-DOCK MODE (`data-mode="dock"`)
   ============================================================================ */
body[data-mode="dock"] .printer-pill,
body[data-mode="dock"] .brand-title {
  display: none;
}

body[data-mode="dock"] .gear-name-input {
  width: 118px;
}

body[data-mode="dock"] .studio-workspace {
  display: flex;
  flex-direction: column;
}

body[data-mode="dock"] .viewport-col {
  order: -1;
  height: 318px;
  flex-shrink: 0;
  border-bottom: 1px solid var(--border-subtle);
}

body[data-mode="dock"] .vp-stage-3d {
  min-height: 130px;
}

body[data-mode="dock"] .loupe-panel {
  height: 112px;
}
body[data-mode="dock"] .loupe-panel.collapsed {
  height: 26px;
}

body[data-mode="dock"] .vp-hud-right,
body[data-mode="dock"] .vp-cam-bar,
body[data-mode="dock"] .vp-cut-bar {
  display: none;
}

body[data-mode="dock"] .dock-tabs {
  display: flex;
  order: 0;
}

body[data-mode="dock"] .col-left,
body[data-mode="dock"] .col-right {
  border: none;
  flex: 1;
  min-height: 0;
}

body[data-mode="dock"] .col-right .action-footer {
  display: none;
}
body[data-mode="dock"] .dock-global-footer {
  display: flex;
}

body[data-mode="dock"][data-dock-tab="gears"] .col-right,
body[data-mode="dock"][data-dock-tab="gears"] #card-presets,
body[data-mode="dock"][data-dock-tab="gears"] #card-bodies {
  display: none;
}

body[data-mode="dock"][data-dock-tab="bodies"] .col-right,
body[data-mode="dock"][data-dock-tab="bodies"] #card-presets,
body[data-mode="dock"][data-dock-tab="bodies"] #card-transmission,
body[data-mode="dock"][data-dock-tab="bodies"] #card-tooth-profile {
  display: none;
}

body[data-mode="dock"][data-dock-tab="export"] .col-left {
  display: none;
}

body[data-mode="dock"][data-dock-tab="presets"] .col-right,
body[data-mode="dock"][data-dock-tab="presets"] #card-transmission,
body[data-mode="dock"][data-dock-tab="presets"] #card-tooth-profile,
body[data-mode="dock"][data-dock-tab="presets"] #card-bodies {
  display: none;
}
body[data-mode="dock"][data-dock-tab="presets"] .presets-grid {
  max-height: none;
}

@media (max-width: 1020px) {
  .printer-pill {
    display: none;
  }
  .studio-workspace {
    grid-template-columns: 300px minmax(280px, 1fr) 310px;
  }
}
</style>
</head>
<body data-mode="__INITIAL_MODE__" data-dock-tab="gears">
<div class="studio-shell">
  <!-- TOP HEADER -->
  <header class="studio-header">
    <div class="brand-group">
      <div class="brand-logo" title="Orca Gear Studio">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9.5" cy="9.5" r="3.2"/>
          <path d="M9.5 3.5v1.6M9.5 13.9v1.6M3.5 9.5h1.6M13.9 9.5h1.6M5.3 5.3l1.1 1.1M12.6 12.6l1.1 1.1M13.7 5.3l-1.1 1.1M6.4 12.6l-1.1 1.1"/>
          <circle cx="17" cy="16.5" r="2.3"/>
          <path d="M17 12.2v1.1M17 19.7v1.1M12.7 16.5h1.1M20.2 16.5h1.1"/>
        </svg>
      </div>
      <div class="brand-name-row">
        <span class="brand-title">Orca Gear Studio</span>
        <input id="inp-gear-name" class="gear-name-input" type="text" maxlength="80" value="Par Engrenagens" aria-label="Gear Pair Name" />
      </div>
      <div id="printer-pill" class="printer-pill" title="Active OrcaSlicer Printer Profile">
        <span class="printer-dot"></span>
        <span id="printer-pill-text">Generic FDM · 220×220×250 mm · 0.4mm</span>
      </div>
    </div>

    <div class="header-actions">
      <button id="btn-undo" class="btn btn-icon" title="Undo (Ctrl+Z)" disabled>↶</button>
      <button id="btn-redo" class="btn btn-icon" title="Redo (Ctrl+Y)" disabled>↷</button>
      <button id="btn-randomize" class="btn btn-soft">
        <span>🎲</span>
        <span data-i18n="btn_random">Aleatório</span>
      </button>
      <button id="btn-reset" class="btn btn-icon" title="Reset">↺</button>
      <button id="btn-lang" class="btn btn-icon" title="Português / English">PT</button>
      <button id="btn-theme" class="btn btn-icon" title="Dark / Light">☾</button>
    </div>
  </header>

  <!-- DOCK MODE TABS -->
  <nav class="dock-tabs" aria-label="Studio Sections">
    <button class="dock-tab-btn active" data-tab="gears" data-i18n="tab_gears">Engrenamento</button>
    <button class="dock-tab-btn" data-tab="bodies" data-i18n="tab_bodies">Eixos &amp; Cubos</button>
    <button class="dock-tab-btn" data-tab="export" data-i18n="tab_export">Diagnóstico</button>
    <button class="dock-tab-btn" data-tab="presets" data-i18n="tab_presets">Presets</button>
  </nav>

  <!-- MAIN 3-COLUMN WORKSPACE -->
  <main class="studio-workspace">
    <!-- LEFT COLUMN: PRESETS + GEAR TRANSMISSION + DUAL TOOTH HEIGHT + PINION/GEAR BODIES -->
    <section class="col-panel col-left">
      <div class="col-scroll">
        <!-- 1. Mechanical Presets Gallery -->
        <div id="card-presets" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_presets">Presets Mecânicos</span>
            <button id="btn-toggle-save-preset" class="btn btn-soft" style="padding:2px 8px;font-size:10.5px;" data-i18n="btn_save_preset">+ Salvar</button>
          </div>
          <div id="save-preset-bar" class="save-preset-bar">
            <input id="inp-save-preset-name" class="save-preset-input" type="text" maxlength="64" placeholder="Nome do preset..." />
            <button id="btn-confirm-save-preset" class="btn btn-accent" style="padding:4px 8px;" data-i18n="btn_ok">Salvar</button>
          </div>
          <div id="preset-filters" class="preset-filter-row">
            <button class="filter-chip active" data-cat="all" data-i18n="cat_all">Todos</button>
            <button class="filter-chip" data-cat="spur_ind" data-i18n="cat_spur">Retas/Ind</button>
            <button class="filter-chip" data-cat="helical" data-i18n="cat_helical">Helicoidal</button>
            <button class="filter-chip" data-cat="herringbone" data-i18n="cat_herringbone">Espinha V</button>
            <button class="filter-chip" data-cat="robotics_cal" data-i18n="cat_robotics">Robótica/Fit</button>
            <button class="filter-chip" data-cat="user" data-i18n="cat_user">Meus</button>
          </div>
          <div id="presets-grid" class="presets-grid"></div>
        </div>

        <!-- 2. Transmission Type, Helix Angle & Teeth Pair -->
        <div id="card-transmission" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_transmission">Transmissão &amp; Hélice</span>
            <span id="badge-ratio" class="card-badge">1 : 2.00</span>
          </div>

          <div class="seg-group" role="radiogroup" aria-label="Gear Type">
            <button class="seg-btn active" data-gear-type="spur" data-i18n="gt_spur">Reta (Spur)</button>
            <button class="seg-btn" data-gear-type="helical" data-i18n="gt_helical">Helicoidal</button>
            <button class="seg-btn" data-gear-type="herringbone" data-i18n="gt_herringbone">Espinha de Peixe</button>
          </div>

          <!-- Helix Quick Pills (0°, 15°, 30°, 45° — 1-click auto-switches spur -> helical!) -->
          <div style="display:flex;flex-direction:column;gap:5px;">
            <div class="ctrl-top">
              <span class="ctrl-label" data-i18n="lbl_helix_quick">Ângulo de Hélice Rápido</span>
              <span id="badge-eff-helix" class="card-badge">β_eff 0.0°</span>
            </div>
            <div class="pill-row">
              <button class="quick-pill" data-helix-pill="0">0° (Reta)</button>
              <button class="quick-pill" data-helix-pill="15">15°</button>
              <button class="quick-pill" data-helix-pill="30">30°</button>
              <button class="quick-pill" data-helix-pill="45">45° Sem Suporte</button>
            </div>
            <div data-slider="helix_angle_deg"></div>
            <div id="row-helix-hand" class="seg-group">
              <button class="seg-btn active" data-helix-hand="right" data-i18n="hand_right">Mão Destra (G1 R / G2 L)</button>
              <button class="seg-btn" data-helix-hand="left" data-i18n="hand_left">Mão Canhota (G1 L / G2 R)</button>
            </div>
          </div>

          <div style="border-top:1px solid var(--border-subtle);padding-top:6px;display:flex;flex-direction:column;gap:6px;">
            <div data-slider="pinion.teeth"></div>
            <div data-slider="gear.teeth"></div>
            <button id="btn-swap-teeth" class="btn" style="padding:3px 8px;font-size:10.5px;" data-i18n="btn_swap_teeth">⇄ Inverter Pinhão / Coroa (Z1 ↔ Z2)</button>
          </div>

          <div style="border-top:1px solid var(--border-subtle);padding-top:6px;display:flex;flex-direction:column;gap:6px;">
            <div data-slider="module_mm"></div>
            <div class="pill-row">
              <button class="quick-pill" data-mod-pill="1.0">m 1.0</button>
              <button class="quick-pill" data-mod-pill="1.5">m 1.5</button>
              <button class="quick-pill" data-mod-pill="2.0">m 2.0</button>
              <button class="quick-pill" data-mod-pill="2.5">m 2.5</button>
              <button class="quick-pill" data-mod-pill="3.0">m 3.0</button>
            </div>
            <div data-slider="pressure_angle_deg"></div>
            <div data-slider="face_width_mm"></div>
          </div>
        </div>

        <!-- 3. Dual Tooth-Height Badges (Factor x | Real mm) & Profile Shift -->
        <div id="card-tooth-profile" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_tooth_height">Altura do Dente (Fator × | mm)</span>
            <span id="badge-total-tooth-h" class="card-badge">h = 4.50 mm</span>
          </div>

          <div class="pill-row">
            <button class="quick-pill" data-tooth-preset="iso" data-i18n="tp_iso">ISO Padrão 1.00×</button>
            <button class="quick-pill" data-tooth-preset="stub" data-i18n="tp_stub">Stub Robusto 0.75×</button>
            <button class="quick-pill" data-tooth-preset="high" data-i18n="tp_high">Alto Contato 1.20×</button>
          </div>

          <div data-slider="addendum_coeff" data-dual-mm="1"></div>
          <div data-slider="clearance_coeff" data-dual-mm="1"></div>
          <div data-slider="root_fillet_coeff" data-dual-mm="1"></div>
          <div data-slider="tip_chamfer_coeff" data-dual-mm="1"></div>

          <div style="border-top:1px solid var(--border-subtle);padding-top:6px;display:flex;flex-direction:column;gap:6px;">
            <div class="switch-row">
              <span class="ctrl-label" data-i18n="lbl_auto_shift">Auto Correção Anti-Undercut (x)</span>
              <label class="toggle-switch">
                <input id="chk-auto-shift" type="checkbox" checked />
                <span class="toggle-track"></span>
              </label>
            </div>
            <div id="badge-eff-shifts" class="helper-note">x₁ efetivo: +0.00 · x₂ efetivo: +0.00</div>
            <div data-slider="profile_shift_g1"></div>
            <div data-slider="profile_shift_g2"></div>
          </div>
        </div>

        <!-- 4. Independent Shafts, Hubs, Recesses & Lightening for Pinion (G1) and Gear (G2) -->
        <div id="card-bodies" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_bodies">Furos, Cubos &amp; Alívio</span>
          </div>

          <div class="seg-group">
            <button id="btn-body-tab-pinion" class="seg-btn active" data-i18n="body_pinion">⚙ Pinhão G1 (Motriz)</button>
            <button id="btn-body-tab-gear" class="seg-btn" data-i18n="body_gear">⚙ Coroa G2 (Movida)</button>
          </div>

          <!-- PINION G1 BODY PANE -->
          <div id="body-pane-pinion" style="display:flex;flex-direction:column;gap:7px;">
            <div class="ctrl-row">
              <span class="ctrl-label" data-i18n="lbl_bore_type">Tipo de Furo / Eixo (G1)</span>
              <select id="sel-pinion-bore-type" class="studio-select">
                <option value="none" data-i18n="bore_none">Sem Furo (Sólido)</option>
                <option value="round" data-i18n="bore_round">Circular Liso</option>
                <option value="d_shaft" data-i18n="bore_d">Eixo em D (NEMA / Motor)</option>
                <option value="double_d" data-i18n="bore_dd">Duplo D</option>
                <option value="hex" data-i18n="bore_hex">Sextavado (Hex / Porca)</option>
                <option value="keyway" data-i18n="bore_keyway">Rasgo de Chaveta DIN</option>
              </select>
            </div>
            <div id="box-pinion-bore-dims" style="display:flex;flex-direction:column;gap:6px;">
              <div data-slider="pinion.bore_diameter_mm"></div>
              <div data-slider="pinion.bore_clearance_mm"></div>
              <div id="box-pinion-dflat" data-slider="pinion.d_flat_depth_mm"></div>
              <div id="box-pinion-keyway" style="display:none;flex-direction:column;gap:6px;">
                <div data-slider="pinion.keyway_width_mm"></div>
                <div data-slider="pinion.keyway_depth_mm"></div>
              </div>
            </div>

            <!-- Hub G1 -->
            <div class="sub-feature-box">
              <div class="switch-row">
                <span class="ctrl-label" data-i18n="lbl_hub">Cubo Saliente Central (Hub)</span>
                <label class="toggle-switch">
                  <input id="chk-pinion-hub" type="checkbox" />
                  <span class="toggle-track"></span>
                </label>
              </div>
              <div id="box-pinion-hub" style="display:none;flex-direction:column;gap:6px;">
                <div data-slider="pinion.hub_diameter_mm"></div>
                <div data-slider="pinion.hub_height_mm"></div>
              </div>
            </div>

            <!-- Recess G1 -->
            <div class="sub-feature-box">
              <div class="switch-row">
                <span class="ctrl-label" data-i18n="lbl_recess">Alojamento Rolamento / Rebaixo</span>
                <label class="toggle-switch">
                  <input id="chk-pinion-recess" type="checkbox" />
                  <span class="toggle-track"></span>
                </label>
              </div>
              <div id="box-pinion-recess" style="display:none;flex-direction:column;gap:6px;">
                <select id="sel-pinion-recess-side" class="studio-select">
                  <option value="top" data-i18n="side_top">Topo (+Z)</option>
                  <option value="bottom" data-i18n="side_bottom">Base (Z=0)</option>
                  <option value="both" data-i18n="side_both">Ambos os Lados</option>
                </select>
                <div data-slider="pinion.recess_diameter_mm"></div>
                <div data-slider="pinion.recess_depth_mm"></div>
              </div>
            </div>

            <!-- Lightening G1 -->
            <div class="sub-feature-box">
              <span class="ctrl-label" data-i18n="lbl_lightening">Alívio de Massa do Corpo</span>
              <select id="sel-pinion-lightening" class="studio-select">
                <option value="solid" data-i18n="light_solid">Corpo Maciço</option>
                <option value="web_recess" data-i18n="light_web">Alma Rebaixada (Web)</option>
                <option value="lightening_holes" data-i18n="light_holes">Furos Circulares de Alívio</option>
              </select>
              <div id="box-pinion-web" style="display:none;" data-slider="pinion.web_thickness_mm"></div>
              <div id="box-pinion-holes" style="display:none;flex-direction:column;gap:6px;">
                <div data-slider="pinion.lightening_hole_count"></div>
                <div data-slider="pinion.lightening_hole_diameter_mm"></div>
              </div>
            </div>
          </div>

          <!-- DRIVEN GEAR G2 BODY PANE -->
          <div id="body-pane-gear" style="display:none;flex-direction:column;gap:7px;">
            <div class="ctrl-row">
              <span class="ctrl-label" data-i18n="lbl_bore_type_g2">Tipo de Furo / Eixo (G2)</span>
              <select id="sel-gear-bore-type" class="studio-select">
                <option value="none" data-i18n="bore_none">Sem Furo (Sólido)</option>
                <option value="round" data-i18n="bore_round">Circular Liso</option>
                <option value="d_shaft" data-i18n="bore_d">Eixo em D (NEMA / Motor)</option>
                <option value="double_d" data-i18n="bore_dd">Duplo D</option>
                <option value="hex" data-i18n="bore_hex">Sextavado (Hex / Porca)</option>
                <option value="keyway" data-i18n="bore_keyway">Rasgo de Chaveta DIN</option>
              </select>
            </div>
            <div id="box-gear-bore-dims" style="display:flex;flex-direction:column;gap:6px;">
              <div data-slider="gear.bore_diameter_mm"></div>
              <div data-slider="gear.bore_clearance_mm"></div>
              <div id="box-gear-dflat" style="display:none;" data-slider="gear.d_flat_depth_mm"></div>
              <div id="box-gear-keyway" style="display:none;flex-direction:column;gap:6px;">
                <div data-slider="gear.keyway_width_mm"></div>
                <div data-slider="gear.keyway_depth_mm"></div>
              </div>
            </div>

            <!-- Hub G2 -->
            <div class="sub-feature-box">
              <div class="switch-row">
                <span class="ctrl-label" data-i18n="lbl_hub">Cubo Saliente Central (Hub)</span>
                <label class="toggle-switch">
                  <input id="chk-gear-hub" type="checkbox" />
                  <span class="toggle-track"></span>
                </label>
              </div>
              <div id="box-gear-hub" style="display:none;flex-direction:column;gap:6px;">
                <div data-slider="gear.hub_diameter_mm"></div>
                <div data-slider="gear.hub_height_mm"></div>
              </div>
            </div>

            <!-- Recess G2 -->
            <div class="sub-feature-box">
              <div class="switch-row">
                <span class="ctrl-label" data-i18n="lbl_recess">Alojamento Rolamento / Rebaixo</span>
                <label class="toggle-switch">
                  <input id="chk-gear-recess" type="checkbox" />
                  <span class="toggle-track"></span>
                </label>
              </div>
              <div id="box-gear-recess" style="display:none;flex-direction:column;gap:6px;">
                <button id="btn-608-gear" class="btn btn-soft" style="padding:3px 7px;font-size:10px;">🎯 Preset Rolamento 608ZZ (Ø22.2×7mm)</button>
                <select id="sel-gear-recess-side" class="studio-select">
                  <option value="top" data-i18n="side_top">Topo (+Z)</option>
                  <option value="bottom" data-i18n="side_bottom">Base (Z=0)</option>
                  <option value="both" data-i18n="side_both">Ambos os Lados</option>
                </select>
                <div data-slider="gear.recess_diameter_mm"></div>
                <div data-slider="gear.recess_depth_mm"></div>
              </div>
            </div>

            <!-- Lightening G2 -->
            <div class="sub-feature-box">
              <span class="ctrl-label" data-i18n="lbl_lightening">Alívio de Massa do Corpo</span>
              <select id="sel-gear-lightening" class="studio-select">
                <option value="solid" data-i18n="light_solid">Corpo Maciço</option>
                <option value="web_recess" data-i18n="light_web">Alma Rebaixada (Web)</option>
                <option value="lightening_holes" data-i18n="light_holes">Furos Circulares de Alívio</option>
              </select>
              <div id="box-gear-web" style="display:none;" data-slider="gear.web_thickness_mm"></div>
              <div id="box-gear-holes" style="display:flex;flex-direction:column;gap:6px;">
                <div data-slider="gear.lightening_hole_count"></div>
                <div data-slider="gear.lightening_hole_diameter_mm"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CENTER COLUMN: 60 FPS 3D WEBGL2 VIEWPORT + MICRO-SIMULATION BAR + 2D TOOTH-MESH LOUPE -->
    <section class="viewport-col">
      <div class="vp-stage-3d">
        <canvas id="gl-canvas"></canvas>

        <!-- Top-Left View Mode & Shader Overlays -->
        <div class="vp-toolbar-left">
          <button class="vp-chip active" data-vp-view="meshed" data-i18n="vp_meshed">⚙ Par Engrenado</button>
          <button class="vp-chip" data-vp-view="plater" data-i18n="vp_plater">🖨 Mesa de Impressão</button>
          <button class="vp-chip" data-vp-view="fit_kit" data-i18n="vp_fit_kit">🧪 Kit de Teste Rápido</button>
          <button id="btn-vp-heatmap" class="vp-chip" data-i18n="vp_heatmap">🔥 Overhang</button>
          <button id="btn-vp-forces" class="vp-chip active" data-i18n="vp_forces">⚡ Forças 3D</button>
          <button id="btn-vp-wire" class="vp-chip" data-i18n="vp_wire">⌗ Malha</button>
        </div>

        <!-- Top-Right Live Force Vectors & Printability HUD -->
        <aside class="vp-hud-right vp-glass">
          <div class="hud-title-row">
            <span data-i18n="hud_title">Cargas &amp; Malha</span>
            <span id="hud-status-pill" class="hud-status-pill ok">OK</span>
          </div>
          <div class="hud-grid">
            <div class="hud-metric">
              <span class="hud-metric-k" data-i18n="hud_cd">Centros a (mm)</span>
              <span id="hud-cd" class="hud-metric-v">48.00</span>
            </div>
            <div class="hud-metric">
              <span class="hud-metric-k" data-i18n="hud_ft">Tangencial Ft</span>
              <span id="hud-ft" class="hud-metric-v">62.5 N</span>
            </div>
            <div class="hud-metric">
              <span class="hud-metric-k" data-i18n="hud_fr">Radial Fr</span>
              <span id="hud-fr" class="hud-metric-v">22.7 N</span>
            </div>
            <div class="hud-metric">
              <span class="hud-metric-k" data-i18n="hud_fa">Empuxo Axial Fa</span>
              <span id="hud-fa" class="hud-metric-v">0.0 N</span>
            </div>
          </div>
          <div id="hud-thrust-note" class="thrust-banner">Empuxo Axial Nulo (0 N)</div>
          <div id="heatmap-legend" class="heatmap-legend">
            <span><i class="legend-swatch" style="background:#00c853"></i>≤45°</span>
            <span><i class="legend-swatch" style="background:#ffb300"></i>45–55°</span>
            <span><i class="legend-swatch" style="background:#ff3d00"></i>&gt;55°</span>
          </div>
        </aside>

        <!-- Bottom-Left Camera Presets -->
        <div class="vp-cam-bar">
          <button class="vp-chip" data-cam="iso" data-i18n="cam_iso">Perspectiva</button>
          <button class="vp-chip" data-cam="top" data-i18n="cam_top">Topo (Engrenamento)</button>
          <button class="vp-chip" data-cam="front" data-i18n="cam_front">Frontal (Hélice)</button>
          <button class="vp-chip" data-cam="reset" data-i18n="cam_reset">Reset</button>
        </div>

        <!-- Bottom-Right Z Cross-Section Clipping Bar -->
        <div class="vp-cut-bar vp-glass">
          <span id="lbl-cut-axis" class="vp-cut-label" style="cursor:pointer;" title="Toggle Z / Y Cut Plane">✂ Corte Z</span>
          <input id="inp-cross-cut" class="orca-slider" type="range" min="0" max="100" step="1" value="0" />
          <span id="lbl-cross-cut" class="ctrl-num" style="width:40px;text-align:center;">Off</span>
          <button id="btn-cut-half" class="step-btn">50%</button>
        </div>
      </div>

      <!-- DEDICATED MICRO-SIMULATION & LIVE DELTA_A TRANSPORT BAR -->
      <div class="sim-transport-bar">
        <div class="sim-row">
          <div class="sim-group">
            <button id="btn-sim-play" class="btn btn-accent" style="min-width:74px;padding:4px 9px;" title="Play / Pause (Space)">⏸ Pause</button>
            <button id="btn-sim-dir" class="btn" style="padding:4px 8px;" title="Toggle CW / CCW">CW ↻</button>
          </div>

          <div class="sim-flex-slider">
            <span class="sim-tag">RPM</span>
            <input id="inp-sim-rpm" class="orca-slider" type="range" min="1" max="300" step="1" value="24" />
            <span id="lbl-sim-rpm" class="sim-mono" style="min-width:48px;">24 rpm</span>
          </div>

          <div class="sim-flex-slider">
            <span class="sim-tag" data-i18n="sim_scrub">Ângulo θ₁</span>
            <input id="inp-sim-angle" class="orca-slider" type="range" min="0" max="360" step="0.1" value="0" />
            <span id="lbl-sim-angle" class="sim-mono" style="min-width:46px;">0.0°</span>
            <div class="sim-group">
              <button class="step-btn" data-angle-step="-1">-1°</button>
              <button class="step-btn" data-angle-step="-0.2">-0.2°</button>
              <button class="step-btn" data-angle-step="0.2">+0.2°</button>
              <button class="step-btn" data-angle-step="1">+1°</button>
            </div>
          </div>
        </div>

        <div class="sim-row">
          <span class="sim-tag" data-i18n="sim_delta_a">Afaste / Aproxime Eixos (Δa):</span>
          <input id="inp-sim-delta-a" class="orca-slider" style="flex:1;" type="range" min="-1.00" max="2.00" step="0.01" value="0.00" />
          <span id="lbl-sim-delta-a" class="sim-mono" style="min-width:66px;">+0.00 mm</span>
          <button id="btn-sim-delta-reset" class="step-btn" data-i18n="btn_reset_da">Reset 0.00 mm</button>
        </div>
      </div>

      <!-- SYNCHRONIZED HIGH-DPI 2D TOOTH-MESH LOUPE -->
      <div id="loupe-panel" class="loupe-panel">
        <div class="loupe-header">
          <div class="loupe-title">
            <span data-i18n="loupe_title">🔍 Lupa 2D de Engrenamento &amp; Linha de Pressão</span>
            <span id="loupe-jam-badge" class="jam-alert-badge">
              <span>⚠</span>
              <span data-i18n="jam_alert">INTERFERÊNCIA / TRAVAMENTO DETECTADO</span>
            </span>
          </div>
          <div class="sim-group">
            <button class="step-btn" data-loupe-zoom="1.0">1×</button>
            <button class="step-btn" data-loupe-zoom="1.7">1.7×</button>
            <button class="step-btn" data-loupe-zoom="2.6">2.6×</button>
            <button id="btn-loupe-collapse" class="step-btn" title="Expand / Collapse 2D Loupe">▾</button>
          </div>
        </div>
        <div class="loupe-canvas-wrap">
          <canvas id="loupe-canvas" width="640" height="168"></canvas>
        </div>
      </div>
    </section>

    <!-- RIGHT COLUMN: FDM FIT TOLERANCES + FULL DIAGNOSTICS REPORT + ORCASLICER EXPORT -->
    <section class="col-panel col-right">
      <div class="col-scroll">
        <!-- 1. FDM Fit Tolerances & Input Torque -->
        <div id="card-tolerances" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_tolerances">Folgas FDM &amp; Torque Motriz</span>
          </div>
          <div data-slider="backlash_mm"></div>
          <div data-slider="xy_compensation_mm"></div>
          <div data-slider="elephant_foot_chamfer_mm"></div>
          <div data-slider="center_distance_offset_mm"></div>
          <div data-slider="input_torque_nm"></div>
        </div>

        <!-- 2. Comprehensive Engineering & Fit Diagnostics -->
        <div id="card-diagnostics" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_diagnostics">Diagnóstico de Engrenamento</span>
            <span id="diag-status-pill" class="hud-status-pill ok">ÓTIMO</span>
          </div>

          <div class="diag-section-title" data-i18n="diag_sec_contact">Razão de Contato &amp; Envolvente</div>
          <div class="diag-grid">
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_eps_a">Transversal ε_α</span>
              <span id="dv-eps-a" class="diag-v">1.58</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_eps_b">Recobrimento Axial ε_β</span>
              <span id="dv-eps-b" class="diag-v">0.00</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_eps_g">Contato Total ε_γ</span>
              <span id="dv-eps-g" class="diag-v">1.58</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_loa">Linha de Ação</span>
              <span id="dv-loa" class="diag-v">9.35 mm</span>
            </div>
          </div>

          <div class="diag-section-title" data-i18n="diag_sec_fit">Encaixe, Folga &amp; Cinemática</div>
          <div class="diag-grid">
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_cd">Distância Centros a</span>
              <span id="dv-cd" class="diag-v">48.00 mm</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_clr">Folga Mín. Dentes</span>
              <span id="dv-clr" class="diag-v">0.14 mm</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_t2">Torque Saída (G2)</span>
              <span id="dv-t2" class="diag-v">2.00 N·m</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_rpm2">Rotação Saída / Vel.</span>
              <span id="dv-rpm2" class="diag-v">12.0 rpm</span>
            </div>
          </div>

          <div class="diag-section-title" data-i18n="diag_sec_print">Impressão Mecânica FDM</div>
          <div class="diag-grid">
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_ovh">Overhang Hélice</span>
              <span id="dv-ovh" class="diag-v">0.0° (Livre)</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_walls">Paredes Sugeridas</span>
              <span id="dv-walls" class="diag-v">4 loops</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_wgt">Peso / Tempo Est.</span>
              <span id="dv-wgt" class="diag-v">~34 g · 42 min</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_bed">Área na Mesa</span>
              <span id="dv-bed" class="diag-v">112×68 mm</span>
            </div>
          </div>

          <div id="diag-issues-list" class="issues-list"></div>
        </div>

        <!-- 3. Export Target & Mechanical Slicer Auto-Configuration -->
        <div id="card-export-cfg" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_export_pkg">Pacote de Saída &amp; Fatiamento</span>
          </div>

          <div class="ctrl-row">
            <span class="ctrl-label" data-i18n="lbl_export_target">O que enviar / exportar:</span>
            <select id="sel-export-target" class="studio-select">
              <option value="pair_separated" data-i18n="exp_pair">Par Separado (Pronto p/ Imprimir)</option>
              <option value="pinion_only" data-i18n="exp_pinion">Apenas Pinhão (G1)</option>
              <option value="gear_only" data-i18n="exp_gear">Apenas Coroa (G2)</option>
              <option value="fit_test_kit" data-i18n="exp_kit">Kit de Teste Rápido (Setores + Base 2 Pinos + Régua Eixo)</option>
              <option value="full_suite" data-i18n="exp_full">Conjunto Completo (Par + Gabaritos)</option>
            </select>
          </div>

          <div id="export-target-note" class="helper-note" data-i18n="note_exp_pair">
            Posiciona Pinhão (G1) e Coroa (G2) separados com margem segura na mesa, prontos para fatiar sem fusão de dentes.
          </div>

          <div class="switch-row" style="padding-top:3px;">
            <span class="ctrl-label" style="white-space:normal;" data-i18n="lbl_auto_slicer">Auto-Ajustar Fatiamento Mecânico (4–6 paredes maciças + Gyroid)</span>
            <label class="toggle-switch">
              <input id="chk-auto-slicer" type="checkbox" checked />
              <span class="toggle-track"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Wide Mode Sticky Action Footer -->
      <footer class="action-footer">
        <button class="btn-hero" data-action="send_to_plater">
          <span>🚀</span>
          <span data-i18n="btn_send_plater">Enviar para a Mesa do OrcaSlicer</span>
        </button>
        <div class="export-btn-row">
          <button class="btn" data-action="export_3mf">💾 <span data-i18n="btn_exp_3mf">Exportar .3MF</span></button>
          <button class="btn" data-action="export_stl">📐 <span data-i18n="btn_exp_stl">Exportar .STL</span></button>
          <button class="btn btn-icon" data-action="open_folder" title="Abrir Pasta de Exportação">📂</button>
        </div>
      </footer>
    </section>
  </main>

  <!-- Compact Dock Mode Sticky Footer -->
  <footer class="action-footer dock-global-footer">
    <button class="btn-hero" data-action="send_to_plater" style="padding:8px 10px;font-size:12px;">
      <span>🚀</span>
      <span data-i18n="btn_send_plater">Enviar para a Mesa do OrcaSlicer</span>
    </button>
    <div class="export-btn-row">
      <button class="btn" data-action="export_3mf">💾 .3MF</button>
      <button class="btn" data-action="export_stl">📐 .STL</button>
      <button class="btn btn-icon" data-action="open_folder" title="Abrir Pasta">📂</button>
    </div>
  </footer>
</div>

<div id="toast-banner" class="toast-banner" role="status" aria-live="polite"></div>

<script>
(function () {
  "use strict";

  const BOOT_PAYLOAD = __ORCA_GEAR_STUDIO_BOOT_JSON__;
  const DEG2RAD = Math.PI / 180.0;
  const RAD2DEG = 180.0 / Math.PI;
  const TWO_PI = 2.0 * Math.PI;

  // ==========================================================================
  // 1. Canonical Parameter Schema & Normalization (100% Parity with schema.py)
  // ==========================================================================
  const VALID_GEAR_TYPES = ["spur", "helical", "herringbone"];
  const VALID_HELIX_HANDS = ["right", "left"];
  const VALID_BORE_TYPES = ["none", "round", "d_shaft", "double_d", "hex", "keyway"];
  const VALID_RECESS_SIDES = ["top", "bottom", "both"];
  const VALID_LIGHTENING_MODES = ["solid", "web_recess", "lightening_holes"];
  const VALID_SIM_DIRECTIONS = ["cw", "ccw"];
  const VALID_EXPORT_TARGETS = ["pair_separated", "pinion_only", "gear_only", "fit_test_kit", "full_suite"];

  const JS_DEFAULT_PARAMS = {
    schema_version: 1,
    name: "Par Engrenagens",
    gear_type: "spur",
    module_mm: 2.0,
    pressure_angle_deg: 20.0,
    helix_angle_deg: 30.0,
    helix_hand: "right",
    face_width_mm: 12.0,
    addendum_coeff: 1.00,
    clearance_coeff: 0.25,
    root_fillet_coeff: 0.30,
    tip_chamfer_coeff: 0.06,
    auto_profile_shift: true,
    profile_shift_g1: 0.0,
    profile_shift_g2: 0.0,
    backlash_mm: 0.15,
    xy_compensation_mm: 0.02,
    elephant_foot_chamfer_mm: 0.40,
    center_distance_offset_mm: 0.0,
    input_torque_nm: 1.0,
    pinion: {
      teeth: 16,
      bore_type: "d_shaft",
      bore_diameter_mm: 5.0,
      bore_clearance_mm: 0.12,
      d_flat_depth_mm: 0.50,
      keyway_width_mm: 2.0,
      keyway_depth_mm: 1.0,
      hub_enabled: false,
      hub_diameter_mm: 14.0,
      hub_height_mm: 5.0,
      recess_enabled: false,
      recess_side: "top",
      recess_diameter_mm: 16.0,
      recess_depth_mm: 4.0,
      lightening_mode: "solid",
      web_thickness_mm: 4.0,
      lightening_hole_count: 6,
      lightening_hole_diameter_mm: 5.0
    },
    gear: {
      teeth: 32,
      bore_type: "round",
      bore_diameter_mm: 8.0,
      bore_clearance_mm: 0.12,
      d_flat_depth_mm: 0.60,
      keyway_width_mm: 3.0,
      keyway_depth_mm: 1.4,
      hub_enabled: false,
      hub_diameter_mm: 20.0,
      hub_height_mm: 5.0,
      recess_enabled: false,
      recess_side: "top",
      recess_diameter_mm: 22.0,
      recess_depth_mm: 3.5,
      lightening_mode: "lightening_holes",
      web_thickness_mm: 4.0,
      lightening_hole_count: 6,
      lightening_hole_diameter_mm: 8.0
    },
    sim_rpm: 24.0,
    sim_direction: "cw",
    export_target: "pair_separated",
    auto_configure_slicer: true
  };

  function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  function clampFloat(val, defVal, lo, hi) {
    if (typeof val === "boolean" || val === null || val === undefined || val === "") return defVal;
    const f = Number(val);
    if (!Number.isFinite(f)) return defVal;
    return Math.max(lo, Math.min(hi, f));
  }

  function clampInt(val, defVal, lo, hi) {
    if (typeof val === "boolean" || val === null || val === undefined || val === "") return defVal;
    const f = Number(val);
    if (!Number.isFinite(f)) return defVal;
    return Math.max(lo, Math.min(hi, Math.round(f)));
  }

  function toBool(val, defVal) {
    if (typeof val === "boolean") return val;
    if (typeof val === "number") return Number.isFinite(val) ? Boolean(val) : defVal;
    if (typeof val === "string") {
      const s = val.trim().toLowerCase();
      if (s === "true" || s === "1" || s === "yes" || s === "on") return true;
      if (s === "false" || s === "0" || s === "no" || s === "off" || s === "") return false;
    }
    return defVal;
  }

  function toChoice(val, defVal, allowed) {
    if (typeof val === "string") {
      const s = val.trim().toLowerCase();
      if (allowed.indexOf(s) >= 0) return s;
    }
    return defVal;
  }

  function normalizeGearBody(rawBody, template) {
    const base = template || JS_DEFAULT_PARAMS.pinion;
    const src = (rawBody && typeof rawBody === "object") ? rawBody : {};
    return {
      teeth: clampInt(src.teeth, base.teeth, 6, 240),
      bore_type: toChoice(src.bore_type, base.bore_type, VALID_BORE_TYPES),
      bore_diameter_mm: clampFloat(src.bore_diameter_mm, base.bore_diameter_mm, 1.0, 160.0),
      bore_clearance_mm: clampFloat(src.bore_clearance_mm, base.bore_clearance_mm, -0.25, 1.50),
      d_flat_depth_mm: clampFloat(src.d_flat_depth_mm, base.d_flat_depth_mm, 0.05, 25.0),
      keyway_width_mm: clampFloat(src.keyway_width_mm, base.keyway_width_mm, 0.50, 40.0),
      keyway_depth_mm: clampFloat(src.keyway_depth_mm, base.keyway_depth_mm, 0.25, 25.0),
      hub_enabled: toBool(src.hub_enabled, base.hub_enabled),
      hub_diameter_mm: clampFloat(src.hub_diameter_mm, base.hub_diameter_mm, 3.0, 300.0),
      hub_height_mm: clampFloat(src.hub_height_mm, base.hub_height_mm, 0.5, 80.0),
      recess_enabled: toBool(src.recess_enabled, base.recess_enabled),
      recess_side: toChoice(src.recess_side, base.recess_side, VALID_RECESS_SIDES),
      recess_diameter_mm: clampFloat(src.recess_diameter_mm, base.recess_diameter_mm, 3.0, 300.0),
      recess_depth_mm: clampFloat(src.recess_depth_mm, base.recess_depth_mm, 0.5, 60.0),
      lightening_mode: toChoice(src.lightening_mode, base.lightening_mode, VALID_LIGHTENING_MODES),
      web_thickness_mm: clampFloat(src.web_thickness_mm, base.web_thickness_mm, 1.2, 80.0),
      lightening_hole_count: clampInt(src.lightening_hole_count, base.lightening_hole_count, 3, 18),
      lightening_hole_diameter_mm: clampFloat(src.lightening_hole_diameter_mm, base.lightening_hole_diameter_mm, 1.5, 100.0)
    };
  }

  function effectiveHelixAngleDeg(params) {
    if (!params || typeof params !== "object") return 0.0;
    const gt = toChoice(params.gear_type, "spur", VALID_GEAR_TYPES);
    if (gt === "spur") return 0.0;
    return clampFloat(params.helix_angle_deg, 30.0, 0.0, 60.0);
  }

  function normalizeParams(raw) {
    const d = JS_DEFAULT_PARAMS;
    const src = (raw && typeof raw === "object") ? raw : {};
    const rawName = typeof src.name === "string" ? src.name.trim() : "";
    const cleanName = (rawName || d.name).slice(0, 80);

    return {
      schema_version: 1,
      name: cleanName,
      gear_type: toChoice(src.gear_type, d.gear_type, VALID_GEAR_TYPES),
      module_mm: clampFloat(src.module_mm, d.module_mm, 0.5, 10.0),
      pressure_angle_deg: clampFloat(src.pressure_angle_deg, d.pressure_angle_deg, 14.5, 30.0),
      helix_angle_deg: clampFloat(src.helix_angle_deg, d.helix_angle_deg, 0.0, 60.0),
      helix_hand: toChoice(src.helix_hand, d.helix_hand, VALID_HELIX_HANDS),
      face_width_mm: clampFloat(src.face_width_mm, d.face_width_mm, 2.0, 120.0),
      addendum_coeff: clampFloat(src.addendum_coeff, d.addendum_coeff, 0.40, 1.40),
      clearance_coeff: clampFloat(src.clearance_coeff, d.clearance_coeff, 0.10, 0.50),
      root_fillet_coeff: clampFloat(src.root_fillet_coeff, d.root_fillet_coeff, 0.05, 0.45),
      tip_chamfer_coeff: clampFloat(src.tip_chamfer_coeff, d.tip_chamfer_coeff, 0.00, 0.25),
      auto_profile_shift: toBool(src.auto_profile_shift, d.auto_profile_shift),
      profile_shift_g1: clampFloat(src.profile_shift_g1, d.profile_shift_g1, -0.50, 0.80),
      profile_shift_g2: clampFloat(src.profile_shift_g2, d.profile_shift_g2, -0.50, 0.80),
      backlash_mm: clampFloat(src.backlash_mm, d.backlash_mm, 0.00, 1.00),
      xy_compensation_mm: clampFloat(src.xy_compensation_mm, d.xy_compensation_mm, -0.20, 0.30),
      elephant_foot_chamfer_mm: clampFloat(src.elephant_foot_chamfer_mm, d.elephant_foot_chamfer_mm, 0.00, 1.50),
      center_distance_offset_mm: clampFloat(src.center_distance_offset_mm, d.center_distance_offset_mm, -1.50, 3.00),
      input_torque_nm: clampFloat(src.input_torque_nm, d.input_torque_nm, 0.05, 50.0),
      pinion: normalizeGearBody(src.pinion, d.pinion),
      gear: normalizeGearBody(src.gear, d.gear),
      sim_rpm: clampFloat(src.sim_rpm, d.sim_rpm, 1.0, 300.0),
      sim_direction: toChoice(src.sim_direction, d.sim_direction, VALID_SIM_DIRECTIONS),
      export_target: toChoice(src.export_target, d.export_target, VALID_EXPORT_TARGETS),
      auto_configure_slicer: toBool(src.auto_configure_slicer, d.auto_configure_slicer)
    };
  }

  // ==========================================================================
  // 2. ISO 21771 / ISO 53 Involute Math & 2D Contour Parity (involute_math.py)
  // ==========================================================================
  function involuteFn(alphaRad) {
    return Math.tan(alphaRad) - alphaRad;
  }

  function inverseInvoluteFn(invVal) {
    if (!Number.isFinite(invVal) || invVal <= 0.0) return 0.0;
    const maxAlpha = 0.5 * Math.PI - 1e-9;
    let alpha;
    if (invVal < 0.5) {
      const c = Math.cbrt(3.0 * invVal);
      alpha = c / (1.0 + 0.4 * c * c / 3.0);
    } else {
      alpha = Math.min(maxAlpha, 0.5 * Math.PI - 1.0 / (invVal + 0.5 * Math.PI));
    }
    alpha = Math.max(1e-12, Math.min(maxAlpha, alpha));
    for (let i = 0; i < 32; i++) {
      const t = Math.tan(alpha);
      const res = t - alpha - invVal;
      if (Math.abs(res) <= 1e-13) break;
      const t2 = t * t;
      if (t2 <= 1e-30) break;
      const step = res / t2;
      const nextA = alpha - step;
      if (nextA <= 0.0) alpha *= 0.5;
      else if (nextA >= maxAlpha) alpha = 0.5 * (alpha + maxAlpha);
      else alpha = nextA;
      if (Math.abs(step) <= 1e-13) break;
    }
    return alpha;
  }

  function transverseToothThicknessAtRadius(r, rb, psiB) {
    if (r <= 0.0) return 0.0;
    if (r <= rb) return 2.0 * r * psiB;
    const cosA = Math.max(-1.0, Math.min(1.0, rb / r));
    const alphaR = Math.acos(cosA);
    return 2.0 * r * (psiB - involuteFn(alphaR));
  }

  function clampTipRadiusNonPointed(raTarget, rRef, rb, rf, psiB, minTipS) {
    const sTarget = transverseToothThicknessAtRadius(raTarget, rb, psiB);
    if (sTarget > minTipS) return [raTarget, sTarget];
    const rLo = Math.max(rf + 0.05, Math.min(rRef, rb));
    const sLo = transverseToothThicknessAtRadius(rLo, rb, psiB);
    if (sLo <= minTipS) return [rLo, Math.max(1e-4, sLo)];
    let lo = rLo;
    let hi = raTarget;
    for (let i = 0; i < 40; i++) {
      const mid = 0.5 * (lo + hi);
      if (transverseToothThicknessAtRadius(mid, rb, psiB) >= minTipS) lo = mid;
      else hi = mid;
    }
    return [lo, Math.max(1e-4, transverseToothThicknessAtRadius(lo, rb, psiB))];
  }

  function computeGearPairGeometry(params) {
    const p = normalizeParams(params);
    const betaDeg = effectiveHelixAngleDeg(p);
    const betaRad = betaDeg * DEG2RAD;
    const cosBeta = Math.cos(betaRad);

    const mN = p.module_mm;
    const mT = mN / cosBeta;

    const alphaNDeg = p.pressure_angle_deg;
    const alphaNRad = alphaNDeg * DEG2RAD;
    const tanAlphaN = Math.tan(alphaNRad);

    const alphaTRad = Math.atan(tanAlphaN / cosBeta);
    const alphaTDeg = alphaTRad * RAD2DEG;
    const cosAlphaT = Math.cos(alphaTRad);
    const sinAlphaT = Math.sin(alphaTRad);
    const invAlphaT = involuteFn(alphaTRad);

    const z1 = p.pinion.teeth;
    const z2 = p.gear.teeth;
    const zSum = z1 + z2;

    const haCoeff = p.addendum_coeff;
    const cCoeff = p.clearance_coeff;

    const xMin1 = Math.max(0.0, haCoeff - 0.5 * z1 * sinAlphaT * sinAlphaT);
    const xMin2 = Math.max(0.0, haCoeff - 0.5 * z2 * sinAlphaT * sinAlphaT);

    const x1 = p.auto_profile_shift ? Math.max(p.profile_shift_g1, xMin1) : p.profile_shift_g1;
    const x2 = p.auto_profile_shift ? Math.max(p.profile_shift_g2, xMin2) : p.profile_shift_g2;

    const invAlphaTwRaw = invAlphaT + 2.0 * tanAlphaN * (x1 + x2) / zSum;
    const alphaTwRad = inverseInvoluteFn(Math.max(0.0, invAlphaTwRaw));
    const alphaTwDeg = alphaTwRad * RAD2DEG;
    const cosAlphaTw = Math.max(1e-6, Math.cos(alphaTwRad));

    const a0 = 0.5 * mT * zSum * cosAlphaT / cosAlphaTw;
    const a = Math.max(2.0, a0 + p.center_distance_offset_mm);

    const rw1 = a * z1 / zSum;
    const rw2 = a * z2 / zSum;

    const r1 = 0.5 * mT * z1;
    const r2 = 0.5 * mT * z2;
    const rb1 = r1 * cosAlphaT;
    const rb2 = r2 * cosAlphaT;

    const sMinPitch = 0.15 * mT;
    const sMaxPitch = 0.90 * Math.PI * mT;
    let sT1 = mT * (0.5 * Math.PI + 2.0 * x1 * tanAlphaN) - p.backlash_mm / (2.0 * cosBeta) - 2.0 * p.xy_compensation_mm;
    let sT2 = mT * (0.5 * Math.PI + 2.0 * x2 * tanAlphaN) - p.backlash_mm / (2.0 * cosBeta) - 2.0 * p.xy_compensation_mm;
    sT1 = Math.max(sMinPitch, Math.min(sMaxPitch, sT1));
    sT2 = Math.max(sMinPitch, Math.min(sMaxPitch, sT2));

    const psiB1 = sT1 / (2.0 * r1) + invAlphaT;
    const psiB2 = sT2 / (2.0 * r2) + invAlphaT;

    const ded1 = Math.max(0.10 * mN, mN * (haCoeff + cCoeff - x1));
    const ded2 = Math.max(0.10 * mN, mN * (haCoeff + cCoeff - x2));
    const rf1 = Math.max(0.8, r1 - ded1);
    const rf2 = Math.max(0.8, r2 - ded2);

    const ra1Raw = r1 + Math.max(0.10 * mN, mN * (haCoeff + x1));
    const ra2Raw = r2 + Math.max(0.10 * mN, mN * (haCoeff + x2));

    const minTipS = 0.08 * mN;
    const res1 = clampTipRadiusNonPointed(ra1Raw, r1, rb1, rf1, psiB1, minTipS);
    const res2 = clampTipRadiusNonPointed(ra2Raw, r2, rb2, rf2, psiB2, minTipS);
    const ra1 = res1[0], sA1 = res1[1];
    const ra2 = res2[0], sA2 = res2[1];

    const invLockRhs = (z1 * psiB1 + z2 * psiB2 - Math.PI) / zSum;
    const alphaLockRad = inverseInvoluteFn(Math.max(0.0, invLockRhs));
    const aInvLock = (rb1 + rb2) / Math.max(1e-6, Math.cos(alphaLockRad));
    const aBottom = Math.max(ra1 + rf2, ra2 + rf1);
    const minNonJamA = Math.max(aInvLock, aBottom);

    const pinionHand = p.helix_hand;
    const gearHand = pinionHand === "right" ? "left" : "right";
    const meshPhaseG2Rad = Math.PI - (Math.PI / z2);

    return {
      beta_deg: betaDeg,
      beta_rad: betaRad,
      alpha_n_deg: alphaNDeg,
      alpha_t_deg: alphaTDeg,
      alpha_tw_deg: alphaTwDeg,
      m_n: mN,
      m_t: mT,
      x1: x1,
      x2: x2,
      nominal_center_distance_mm: a0,
      center_distance_mm: a,
      min_non_jam_center_distance_mm: minNonJamA,
      ratio: z2 / z1,
      mesh_phase_g2_rad: meshPhaseG2Rad,
      pinion: {
        teeth: z1,
        profile_shift: x1,
        min_profile_shift_no_undercut: xMin1,
        undercut: x1 < xMin1 - 1e-4,
        pitch_radius_mm: r1,
        working_pitch_radius_mm: rw1,
        base_radius_mm: rb1,
        tip_radius_mm: ra1,
        root_radius_mm: rf1,
        addendum_mm: ra1 - r1,
        dedendum_mm: r1 - rf1,
        tooth_height_mm: ra1 - rf1,
        tooth_thickness_pitch_mm: sT1,
        tip_thickness_mm: sA1,
        base_half_angle_rad: psiB1,
        helix_hand: pinionHand,
        face_width_mm: p.face_width_mm
      },
      gear: {
        teeth: z2,
        profile_shift: x2,
        min_profile_shift_no_undercut: xMin2,
        undercut: x2 < xMin2 - 1e-4,
        pitch_radius_mm: r2,
        working_pitch_radius_mm: rw2,
        base_radius_mm: rb2,
        tip_radius_mm: ra2,
        root_radius_mm: rf2,
        addendum_mm: ra2 - r2,
        dedendum_mm: r2 - rf2,
        tooth_height_mm: ra2 - rf2,
        tooth_thickness_pitch_mm: sT2,
        tip_thickness_mm: sA2,
        base_half_angle_rad: psiB2,
        helix_hand: gearHand,
        face_width_mm: p.face_width_mm
      }
    };
  }

  function helixTwistAngleRad(zMm, faceWidthMm, pitchRadiusMm, betaDeg, hand, gearType) {
    if (gearType === "spur" || Math.abs(betaDeg) < 1e-6 || pitchRadiusMm <= 1e-6) return 0.0;
    const sign = hand === "right" ? 1.0 : -1.0;
    const zEff = gearType === "herringbone" ? Math.min(zMm, faceWidthMm - zMm) : zMm;
    return sign * zEff * Math.tan(betaDeg * DEG2RAD) / pitchRadiusMm;
  }

  function buildSingleToothPolarTemplate(p, geom, which, samplesPerFlank, radialInsetMm) {
    const g = which === "gear" ? geom.gear : geom.pinion;
    const zTeeth = g.teeth;
    const mN = geom.m_n;
    const mT = geom.m_t;
    const alphaTRad = geom.alpha_t_deg * DEG2RAD;
    const alphaNRad = geom.alpha_n_deg * DEG2RAD;
    const invAlphaT = involuteFn(alphaTRad);

    const rRef = g.pitch_radius_mm;
    const rb = g.base_radius_mm;
    const raBase = g.tip_radius_mm;
    const rfBase = g.root_radius_mm;
    const sTBase = g.tooth_thickness_pitch_mm;

    const nFlank = Math.max(4, samplesPerFlank | 0);
    const nInv = nFlank - 1;
    const tauHalf = Math.PI / zTeeth;

    let rf = rfBase;
    let raTarget = raBase;
    let sT = sTBase;
    const inset = Math.max(0.0, radialInsetMm || 0.0);
    if (inset > 0.0) {
      const maxSafeInset = Math.min(0.32 * mN, 0.25 * (raBase - rfBase), 0.20 * sTBase);
      const effInset = Math.min(inset, Math.max(0.0, maxSafeInset));
      rf = Math.max(0.5, rfBase - effInset);
      raTarget = Math.max(rf + 0.20 * mN, raBase - effInset);
      sT = Math.max(0.16 * mT, sTBase - 2.0 * effInset / Math.max(0.5, Math.cos(alphaNRad)));
    }

    const psiB = sT / (2.0 * rRef) + invAlphaT;
    const ra = clampTipRadiusNonPointed(raTarget, rRef, rb, rf, psiB, 0.06 * mN)[0];

    const invHalfAngle = function (rVal) {
      if (rVal <= rb) return psiB;
      return psiB - involuteFn(Math.acos(Math.max(-1.0, Math.min(1.0, rb / rVal))));
    };

    const rhoFillet = Math.max(0.02 * mN, Math.min(p.root_fillet_coeff * mN, 0.45 * (ra - rf)));
    let rJoin = Math.max(rb, Math.min(rf + rhoFillet, rf + 0.48 * (ra - rf)));
    rJoin = Math.min(rJoin, ra - 0.08 * (ra - rf));

    const psiJoin = invHalfAngle(rJoin);
    const maxPsiJoin = 0.86 * tauHalf;
    const angleScale = psiJoin > maxPsiJoin ? (maxPsiJoin / psiJoin) : 1.0;
    const scaledPsi = function (rVal) {
      return Math.max(1e-5, invHalfAngle(rVal) * angleScale);
    };

    const psiJoinEff = scaledPsi(rJoin);
    const cTip = Math.max(0.0, Math.min(p.tip_chamfer_coeff * mN, 0.28 * (ra - rJoin)));
    const psiRa = scaledPsi(ra);

    let rChamf, psiTipCorner;
    if (cTip > 1e-5) {
      rChamf = ra - cTip;
      psiTipCorner = Math.max(0.22 * psiRa, psiRa - 0.85 * cTip / Math.max(1.0, ra));
    } else {
      rChamf = rJoin + ((nInv - 1) / Math.max(1, nInv)) * (ra - rJoin);
      psiTipCorner = psiRa;
    }

    const rInvPts = new Float64Array(nInv);
    const psiInvPts = new Float64Array(nInv);
    for (let i = 0; i < nInv; i++) {
      const u = nInv > 1 ? (i / (nInv - 1)) : 0.0;
      const sParam = 0.55 * u * u + 0.45 * u;
      const rv = rJoin + sParam * (rChamf - rJoin);
      rInvPts[i] = rv;
      psiInvPts[i] = scaledPsi(rv);
    }

    const availValley = Math.max(1e-4, tauHalf - psiJoinEff);
    const deltaPsiFil = Math.min(Math.max(rhoFillet / Math.max(1.0, rf), 0.16 * availValley), 0.68 * availValley);
    const psiFilEnd = psiJoinEff + deltaPsiFil;
    const uFil = [0.32, 0.68, 1.0];
    const psiFilUpper = uFil.map(function (u) { return psiJoinEff + u * deltaPsiFil; });
    const rFilUpper = uFil.map(function (u) { return rf + (rJoin - rf) * (1.0 - Math.sin(0.5 * Math.PI * u)); });
    const psiRootMid = 0.5 * (psiFilEnd + tauHalf);

    const phi = [];
    const rad = [];
    phi.push(-psiRootMid); rad.push(rf);
    for (let i = 2; i >= 0; i--) { phi.push(-psiFilUpper[i]); rad.push(rFilUpper[i]); }
    for (let i = 0; i < nInv; i++) { phi.push(-psiInvPts[i]); rad.push(rInvPts[i]); }
    phi.push(-psiTipCorner); rad.push(ra);
    phi.push(0.0); rad.push(ra);
    phi.push(psiTipCorner); rad.push(ra);
    for (let i = nInv - 1; i >= 0; i--) { phi.push(psiInvPts[i]); rad.push(rInvPts[i]); }
    for (let i = 0; i < 3; i++) { phi.push(psiFilUpper[i]); rad.push(rFilUpper[i]); }
    phi.push(psiRootMid); rad.push(rf);
    phi.push(tauHalf); rad.push(rf);

    return { phi: phi, rad: rad, rf: rf, ra: ra };
  }

  function buildGear2DContour(p, geom, which, samplesPerFlank, radialInsetMm) {
    const g = which === "gear" ? geom.gear : geom.pinion;
    const zTeeth = g.teeth;
    const tpl = buildSingleToothPolarTemplate(p, geom, which, samplesPerFlank, radialInsetMm);
    const ptsPerTooth = tpl.phi.length;
    const total = zTeeth * ptsPerTooth;
    const xs = new Float64Array(total);
    const ys = new Float64Array(total);
    let ptr = 0;
    for (let k = 0; k < zTeeth; k++) {
      const baseAng = (TWO_PI * k) / zTeeth;
      for (let j = 0; j < ptsPerTooth; j++) {
        const a = baseAng + tpl.phi[j];
        const r = tpl.rad[j];
        xs[ptr] = r * Math.cos(a);
        ys[ptr] = r * Math.sin(a);
        ptr++;
      }
    }
    return { xs: xs, ys: ys, count: total, ptsPerTooth: ptsPerTooth, rf: tpl.rf, ra: tpl.ra };
  }

  function buildBore2DContour(boreCfg, maxAllowedRadiusMm, radialSamples, extraClearanceMm) {
    const bt = boreCfg ? boreCfg.bore_type : "none";
    if (!boreCfg || bt === "none") return null;
    const m = Math.max(24, radialSamples | 0);
    const maxR = Math.max(0.4, maxAllowedRadiusMm);
    const dEff = boreCfg.bore_diameter_mm + boreCfg.bore_clearance_mm + (extraClearanceMm || 0.0);
    const rNom = Math.max(0.35, Math.min(maxR, 0.5 * dEff));
    const xs = new Float64Array(m);
    const ys = new Float64Array(m);

    for (let i = 0; i < m; i++) {
      const ang = (TWO_PI * i) / m;
      const cosA = Math.cos(ang);
      const sinA = Math.sin(ang);
      let r = rNom;

      if (bt === "d_shaft" || bt === "double_d") {
        const flatDepth = Math.max(0.05 * rNom, Math.min(boreCfg.d_flat_depth_mm, 0.68 * rNom));
        const yFlat = rNom - flatDepth;
        if (bt === "d_shaft") {
          if (sinA > 1e-6) r = Math.min(rNom, yFlat / sinA);
        } else {
          if (Math.abs(sinA) > 1e-6) r = Math.min(rNom, yFlat / Math.abs(sinA));
        }
        xs[i] = r * cosA;
        ys[i] = r * sinA;
      } else if (bt === "hex") {
        const cos30 = Math.cos(Math.PI / 6.0);
        const apothem = Math.min(rNom, maxR * cos30);
        const sec = Math.min(5, Math.floor(ang / (Math.PI / 3.0)));
        const midAng = (sec + 0.5) * (Math.PI / 3.0);
        r = Math.min(maxR, apothem / Math.cos(ang - midAng));
        xs[i] = r * cosA;
        ys[i] = r * sinA;
      } else if (bt === "keyway") {
        const rCirc = Math.min(rNom, 0.90 * maxR);
        const halfW = Math.max(0.15 * rCirc, Math.min(0.5 * boreCfg.keyway_width_mm, 0.62 * rCirc));
        const yCirc = Math.sqrt(Math.max(1e-6, rCirc * rCirc - halfW * halfW));
        const yTop = Math.min(
          Math.sqrt(Math.max(yCirc * yCirc + 1e-5, maxR * maxR - halfW * halfW)),
          rCirc + Math.max(0.15, boreCfg.keyway_depth_mm)
        );
        const t1 = Math.atan2(yCirc, halfW);
        const t2 = Math.atan2(yTop, halfW);
        const t3 = Math.PI - t2;
        const t4 = Math.PI - t1;
        if (ang >= t1 && ang <= t2) {
          xs[i] = halfW;
          ys[i] = Math.min(yTop, Math.max(yCirc, halfW * Math.tan(ang)));
        } else if (ang > t2 && ang < t3) {
          ys[i] = yTop;
          const tA = Math.tan(ang);
          xs[i] = Math.abs(tA) > 1e9 ? 0.0 : Math.max(-halfW, Math.min(halfW, yTop / tA));
        } else if (ang >= t3 && ang <= t4) {
          xs[i] = -halfW;
          ys[i] = Math.min(yTop, Math.max(yCirc, -halfW * Math.tan(ang)));
        } else {
          xs[i] = rCirc * cosA;
          ys[i] = rCirc * sinA;
        }
      } else {
        xs[i] = r * cosA;
        ys[i] = r * sinA;
      }
    }
    return { xs: xs, ys: ys, count: m, rNom: rNom };
  }

  // ==========================================================================
  // 3. Client-Side Engineering Diagnostics & Live 2D Collision / LOA Solver
  // ==========================================================================
  function computeClientAnalysis(p, geom, printer) {
    const betaRad = geom.beta_rad;
    const cosB = Math.cos(betaRad);
    const sinB = Math.sin(betaRad);
    const tanB = Math.tan(betaRad);

    const rb1 = geom.pinion.base_radius_mm;
    const rb2 = geom.gear.base_radius_mm;
    const ra1 = geom.pinion.tip_radius_mm;
    const ra2 = geom.gear.tip_radius_mm;
    const rf1 = geom.pinion.root_radius_mm;
    const rf2 = geom.gear.root_radius_mm;
    const r1 = geom.pinion.pitch_radius_mm;
    const r2 = geom.gear.pitch_radius_mm;
    const a = geom.center_distance_mm;
    const a0 = geom.nominal_center_distance_mm;
    const rw1 = geom.pinion.working_pitch_radius_mm;
    const rw2 = geom.gear.working_pitch_radius_mm;

    const cosAw = Math.max(-0.9999, Math.min(0.9999, (rb1 + rb2) / Math.max(a, 1e-5)));
    const alphaWRad = cosAw >= 0.99985 ? 0.0 : Math.acos(cosAw);
    const sinAw = Math.sin(alphaWRad);
    const tanAw = Math.tan(alphaWRad);

    // Active Line of Action bounds along s (P + s * u_loa)
    const sMinBase = -rw1 * sinAw;
    const sMaxBase = rw2 * sinAw;
    const sEntryTip = rw2 * sinAw - Math.sqrt(Math.max(0.0, ra2 * ra2 - rb2 * rb2));
    const sExitTip = Math.sqrt(Math.max(0.0, ra1 * ra1 - rb1 * rb1)) - rw1 * sinAw;
    const sStart = Math.max(sMinBase, sEntryTip);
    const sEnd = Math.min(sMaxBase, sExitTip);
    const loaLen = Math.max(0.0, sEnd - sStart);

    const pBt = Math.PI * geom.m_t * Math.cos(geom.alpha_t_deg * DEG2RAD);
    const epsAlpha = pBt > 1e-6 ? (loaLen / pBt) : 0.0;
    const effAxialWidth = p.gear_type === "herringbone" ? (0.5 * p.face_width_mm) : p.face_width_mm;
    const epsBeta = p.gear_type === "spur" ? 0.0 : ((effAxialWidth * sinB) / Math.max(1e-6, Math.PI * geom.m_n));
    const epsTotal = epsAlpha + epsBeta;

    // Effective operating backlash & clearances
    const zSum = geom.pinion.teeth + geom.gear.teeth;
    const pTw = TWO_PI * rw1 / geom.pinion.teeth;
    const sW1 = 2.0 * rw1 * Math.max(0.0, geom.pinion.base_half_angle_rad - involuteFn(alphaWRad));
    const sW2 = 2.0 * rw2 * Math.max(0.0, geom.gear.base_half_angle_rad - involuteFn(alphaWRad));
    const effBacklash = (pTw - sW1 - sW2) * cosB;

    const radClr1 = a - (ra2 + rf1);
    const radClr2 = a - (ra1 + rf2);
    const baseInterference = (sEntryTip < sMinBase - 0.03 * geom.m_n) || (sExitTip > sMaxBase + 0.03 * geom.m_n);
    const jammed = (a < geom.min_non_jam_center_distance_mm - 0.004) || (effBacklash < -0.008) || (radClr1 < -0.005) || (radClr2 < -0.005);
    const interference = jammed || baseInterference;
    const minClr = jammed ? 0.0 : Math.max(0.0, Math.min(0.5 * effBacklash, radClr1, radClr2));

    // Kinematics & 3D Forces
    const torque1 = p.input_torque_nm;
    const torque2 = torque1 * geom.ratio;
    const rpm1 = p.sim_rpm;
    const rpm2 = rpm1 / geom.ratio;
    const pitchVel = (TWO_PI * rw1 * rpm1) / 60.0;

    // F_t in Newtons: T1 [N*m] / (r1 [m]) = 1000 * T1 / r1_mm
    const fT = (1000.0 * torque1) / Math.max(1.0, rw1);
    const fR = fT * tanAw;
    const axialBalanced = p.gear_type !== "helical" || geom.beta_deg < 0.1;
    const fA = axialBalanced ? 0.0 : (fT * tanB);

    // Printability
    const ovhDeg = geom.beta_deg;
    const supportsNeeded = ovhDeg > 47.0;
    const sepFootprintX = 2.0 * ra1 + 2.0 * ra2 + 10.0;
    const sepFootprintY = 2.0 * Math.max(ra1, ra2);
    const bedX = Number(printer.bed_x) || 220.0;
    const bedY = Number(printer.bed_y) || 220.0;
    const fitsBed = sepFootprintX <= bedX && sepFootprintY <= bedY;

    const vol1Cm3 = (Math.PI * r1 * r1 * p.face_width_mm) / 1000.0;
    const vol2Cm3 = (Math.PI * r2 * r2 * p.face_width_mm) / 1000.0;
    const totVolCm3 = 0.85 * (vol1Cm3 + vol2Cm3);
    const estWeightG = totVolCm3 * 1.24 * 0.62;
    const estTimeMin = Math.max(8, Math.round(estWeightG * 1.25));
    const lw = Number(printer.line_width_mm) || 0.42;
    const recWalls = Math.max(4, Math.min(6, Math.round((1.8 * geom.m_n) / (2.0 * lw))));

    const issues = [];
    if (jammed) {
      issues.push({
        severity: "critical",
        pt: "TRAVAMENTO MECÂNICO: Distância entre centros Δa muito negativa ou adendo excessivo — dentes colidem!",
        en: "MECHANICAL JAMMING: Center distance Δa too negative or excessive addendum — teeth collide!"
      });
    } else if (interference) {
      issues.push({
        severity: "warn",
        pt: "Interferência de base detectada: ative Auto Correção Anti-Undercut (x) ou aumente o número de dentes.",
        en: "Base-circle interference detected: enable Auto Anti-Undercut Shift (x) or increase tooth count."
      });
    }
    if (geom.pinion.undercut || geom.gear.undercut) {
      issues.push({
        severity: "warn",
        pt: "Adelgaçamento na raiz (Undercut): habilite Auto Correção (x) para reforçar o pé do dente.",
        en: "Root undercut detected: enable Auto Profile Shift (x) to strengthen tooth root."
      });
    }
    if (epsAlpha < 1.15) {
      issues.push({
        severity: "warn",
        pt: "Razão de contato transversal baixa (" + epsAlpha.toFixed(2) + "): aproxime Δa ou aumente o adendo.",
        en: "Low transverse contact ratio (" + epsAlpha.toFixed(2) + "): reduce Δa or increase addendum."
      });
    }
    if (!axialBalanced && fA > 15.0) {
      issues.push({
        severity: "warn",
        pt: "Empuxo axial relevante (" + fA.toFixed(1) + " N): use rolamento axial ou mude para Espinha de Peixe.",
        en: "Significant axial thrust (" + fA.toFixed(1) + " N): use thrust bearing or switch to Herringbone."
      });
    }
    if (supportsNeeded) {
      issues.push({
        severity: "warn",
        pt: "Hélice acima de 47° (" + ovhDeg.toFixed(0) + "°): pode exigir suportes ou camadas finas em FDM.",
        en: "Helix above 47° (" + ovhDeg.toFixed(0) + "°): may require supports or thin layer height in FDM."
      });
    }
    if (!fitsBed) {
      issues.push({
        severity: "critical",
        pt: "Par separado excede a mesa (" + Math.round(bedX) + "×" + Math.round(bedY) + " mm): exporte G1 e G2 individualmente.",
        en: "Separated pair exceeds build plate (" + Math.round(bedX) + "×" + Math.round(bedY) + " mm): export G1/G2 individually."
      });
    }
    if (issues.length === 0) {
      issues.push({
        severity: "ok",
        pt: "Engrenamento livre de interferência com folga saudável para impressão FDM.",
        en: "Interference-free conjugate meshing with healthy FDM printing clearance."
      });
    }

    const status = (jammed || !fitsBed) ? "critical" : (issues.some(function (x) { return x.severity === "warn"; }) ? "warn" : "ok");

    return {
      status: status,
      loa: { alphaWRad: alphaWRad, sStart: sStart, sEnd: sEnd, sMinBase: sMinBase, sMaxBase: sMaxBase, pBt: pBt },
      contact: {
        transverse_ratio: epsAlpha,
        axial_overlap_ratio: epsBeta,
        total_contact_ratio: epsTotal,
        line_of_action_length_mm: loaLen
      },
      fit: {
        effective_backlash_mm: effBacklash,
        radial_clearance_g1_mm: radClr1,
        radial_clearance_g2_mm: radClr2,
        min_tooth_clearance_mm: minClr,
        interference_detected: interference,
        jammed: jammed,
        undercut_g1: geom.pinion.undercut,
        undercut_g2: geom.gear.undercut,
        thin_tip_g1: geom.pinion.tip_thickness_mm < 0.25 * geom.m_n,
        thin_tip_g2: geom.gear.tip_thickness_mm < 0.25 * geom.m_n,
        center_distance_mm: a,
        nominal_center_distance_mm: a0,
        delta_a_mm: p.center_distance_offset_mm
      },
      kinematics: {
        ratio: geom.ratio,
        rpm_g1: rpm1,
        rpm_g2: rpm2,
        pitch_line_velocity_mm_s: pitchVel,
        torque_g1_nm: torque1,
        torque_g2_nm: torque2,
        tangential_force_n: fT,
        radial_force_n: fR,
        axial_force_n: fA,
        axial_thrust_balanced: axialBalanced
      },
      printability: {
        helix_overhang_deg: ovhDeg,
        supports_needed: supportsNeeded,
        fits_bed: fitsBed,
        bed_x_mm: bedX,
        bed_y_mm: bedY,
        pair_footprint_mm: [sepFootprintX, sepFootprintY],
        estimated_volume_cm3: totVolCm3,
        estimated_weight_g: estWeightG,
        estimated_print_time_min: estTimeMin,
        recommended_wall_loops: recWalls
      },
      issues: issues
    };
  }

  // Real-time 2D Meshing Window Collision & Clearance Check at exact current angle theta1
  function checkLive2DMeshCollision(c1, c2, theta1, theta2, a, mN, r1) {
    const cos1 = Math.cos(theta1), sin1 = Math.sin(theta1);
    const cos2 = Math.cos(theta2), sin2 = Math.sin(theta2);
    const xLo = r1 - 3.2 * mN;
    const xHi = r1 + 3.2 * mN;
    const yLim = 3.6 * mN;

    const segs1 = [];
    const n1 = c1.count;
    for (let i = 0; i < n1; i++) {
      const j = (i + 1) % n1;
      const x0 = c1.xs[i] * cos1 - c1.ys[i] * sin1;
      const y0 = c1.xs[i] * sin1 + c1.ys[i] * cos1;
      if (Math.abs(y0) > yLim * 1.4 || x0 < xLo - 2.0 * mN) continue;
      const x1p = c1.xs[j] * cos1 - c1.ys[j] * sin1;
      const y1p = c1.xs[j] * sin1 + c1.ys[j] * cos1;
      if (Math.max(x0, x1p) >= xLo && Math.min(x0, x1p) <= xHi && Math.min(Math.abs(y0), Math.abs(y1p)) <= yLim) {
        segs1.push(x0, y0, x1p, y1p);
      }
    }

    const segs2 = [];
    const n2 = c2.count;
    for (let i = 0; i < n2; i++) {
      const j = (i + 1) % n2;
      const x0 = c2.xs[i] * cos2 - c2.ys[i] * sin2 + a;
      const y0 = c2.xs[i] * sin2 + c2.ys[i] * cos2;
      if (Math.abs(y0) > yLim * 1.4 || x0 > xHi + 2.0 * mN) continue;
      const x1p = c2.xs[j] * cos2 - c2.ys[j] * sin2 + a;
      const y1p = c2.xs[j] * sin2 + c2.ys[j] * cos2;
      if (Math.max(x0, x1p) >= xLo && Math.min(x0, x1p) <= xHi && Math.min(Math.abs(y0), Math.abs(y1p)) <= yLim) {
        segs2.push(x0, y0, x1p, y1p);
      }
    }

    const hitPoints = [];
    let minDistSq = Infinity;
    const cSeg1 = segs1.length >> 2;
    const cSeg2 = segs2.length >> 2;

    for (let i = 0; i < cSeg1; i++) {
      const ax0 = segs1[4 * i], ay0 = segs1[4 * i + 1], ax1 = segs1[4 * i + 2], ay1 = segs1[4 * i + 3];
      const dpx = ax1 - ax0, dpy = ay1 - ay0;
      const lenA2 = Math.max(1e-12, dpx * dpx + dpy * dpy);

      for (let j = 0; j < cSeg2; j++) {
        const bx0 = segs2[4 * j], by0 = segs2[4 * j + 1], bx1 = segs2[4 * j + 2], by1 = segs2[4 * j + 3];
        const dqx = bx1 - bx0, dqy = by1 - by0;
        const denom = dpx * dqy - dpy * dqx;
        if (Math.abs(denom) > 1e-12) {
          const qpx = bx0 - ax0, qpy = by0 - ay0;
          const t = (qpx * dqy - qpy * dqx) / denom;
          const u = (qpx * dpy - qpy * dpx) / denom;
          if (t >= 0.0 && t <= 1.0 && u >= 0.0 && u <= 1.0) {
            minDistSq = 0.0;
            if (hitPoints.length < 24) {
              hitPoints.push([ax0 + t * dpx, ay0 + t * dpy]);
            }
            continue;
          }
        }
        // Point-to-segment distance check
        const lenB2 = Math.max(1e-12, dqx * dqx + dqy * dqy);
        const projB = Math.max(0.0, Math.min(1.0, ((ax0 - bx0) * dqx + (ay0 - by0) * dqy) / lenB2));
        const dxB = ax0 - (bx0 + projB * dqx);
        const dyB = ay0 - (by0 + projB * dqy);
        const d2B = dxB * dxB + dyB * dyB;
        if (d2B < minDistSq) minDistSq = d2B;

        const projA = Math.max(0.0, Math.min(1.0, ((bx0 - ax0) * dpx + (by0 - ay0) * dpy) / lenA2));
        const dxA = bx0 - (ax0 + projA * dpx);
        const dyA = by0 - (ay0 + projA * dpy);
        const d2A = dxA * dxA + dyA * dyA;
        if (d2A < minDistSq) minDistSq = d2A;
      }
    }

    return {
      collided: hitPoints.length > 0,
      minDistMm: Number.isFinite(minDistSq) ? Math.sqrt(minDistSq) : 0.0,
      hitPoints: hitPoints
    };
  }

  // ==========================================================================
  // 4. Translations (PT-BR & EN) & Slider Metadata
  // ==========================================================================
  const I18N = {
    pt: {
      btn_random: "Aleatório",
      tab_gears: "Engrenamento",
      tab_bodies: "Eixos & Cubos",
      tab_export: "Diagnóstico",
      tab_presets: "Presets",
      sec_presets: "Presets Mecânicos",
      btn_save_preset: "+ Salvar",
      btn_ok: "Salvar",
      cat_all: "Todos",
      cat_spur: "Retas/Ind",
      cat_helical: "Helicoidal",
      cat_herringbone: "Espinha V",
      cat_robotics: "Robótica/Fit",
      cat_user: "Meus",
      sec_transmission: "Transmissão & Hélice",
      gt_spur: "Reta (Spur)",
      gt_helical: "Helicoidal",
      gt_herringbone: "Espinha de Peixe",
      lbl_helix_quick: "Ângulo de Hélice Rápido",
      hand_right: "Mão Destra (G1 R / G2 L)",
      hand_left: "Mão Canhota (G1 L / G2 R)",
      btn_swap_teeth: "⇄ Inverter Pinhão / Coroa (Z1 ↔ Z2)",
      sec_tooth_height: "Altura do Dente (Fator × | mm)",
      tp_iso: "ISO Padrão 1.00×",
      tp_stub: "Stub Robusto 0.75×",
      tp_high: "Alto Contato 1.20×",
      lbl_auto_shift: "Auto Correção Anti-Undercut (x)",
      sec_bodies: "Furos, Cubos & Alívio",
      body_pinion: "⚙ Pinhão G1 (Motriz)",
      body_gear: "⚙ Coroa G2 (Movida)",
      lbl_bore_type: "Tipo de Furo / Eixo (G1)",
      lbl_bore_type_g2: "Tipo de Furo / Eixo (G2)",
      bore_none: "Sem Furo (Sólido)",
      bore_round: "Circular Liso",
      bore_d: "Eixo em D (NEMA / Motor)",
      bore_dd: "Duplo D",
      bore_hex: "Sextavado (Hex / Porca)",
      bore_keyway: "Rasgo de Chaveta DIN",
      lbl_hub: "Cubo Saliente Central (Hub)",
      lbl_recess: "Alojamento Rolamento / Rebaixo",
      side_top: "Topo (+Z)",
      side_bottom: "Base (Z=0)",
      side_both: "Ambos os Lados",
      lbl_lightening: "Alívio de Massa do Corpo",
      light_solid: "Corpo Maciço",
      light_web: "Alma Rebaixada (Web)",
      light_holes: "Furos Circulares de Alívio",
      vp_meshed: "⚙ Par Engrenado",
      vp_plater: "🖨 Mesa de Impressão",
      vp_fit_kit: "🧪 Kit de Teste Rápido",
      vp_heatmap: "🔥 Overhang",
      vp_forces: "⚡ Forças 3D",
      vp_wire: "⌗ Malha",
      hud_title: "Cargas & Malha",
      hud_cd: "Centros a (mm)",
      hud_ft: "Tangencial Ft",
      hud_fr: "Radial Fr",
      hud_fa: "Empuxo Axial Fa",
      cam_iso: "Perspectiva",
      cam_top: "Topo (Engrenamento)",
      cam_front: "Frontal (Hélice)",
      cam_reset: "Reset",
      sim_scrub: "Ângulo θ₁",
      sim_delta_a: "Afaste / Aproxime Eixos (Δa):",
      btn_reset_da: "Reset 0.00 mm",
      loupe_title: "🔍 Lupa 2D de Engrenamento & Linha de Pressão",
      jam_alert: "INTERFERÊNCIA / TRAVAMENTO DETECTADO",
      sec_tolerances: "Folgas FDM & Torque Motriz",
      sec_diagnostics: "Diagnóstico de Engrenamento",
      diag_sec_contact: "Razão de Contato & Envolvente",
      dk_eps_a: "Transversal ε_α",
      dk_eps_b: "Recobrimento Axial ε_β",
      dk_eps_g: "Contato Total ε_γ",
      dk_loa: "Linha de Ação",
      diag_sec_fit: "Encaixe, Folga & Cinemática",
      dk_cd: "Distância Centros a",
      dk_clr: "Folga Mín. Dentes",
      dk_t2: "Torque Saída (G2)",
      dk_rpm2: "Rotação Saída / Vel.",
      diag_sec_print: "Impressão Mecânica FDM",
      dk_ovh: "Overhang Hélice",
      dk_walls: "Paredes Sugeridas",
      dk_wgt: "Peso / Tempo Est.",
      dk_bed: "Área na Mesa",
      sec_export_pkg: "Pacote de Saída & Fatiamento",
      lbl_export_target: "O que enviar / exportar:",
      exp_pair: "Par Separado (Pronto p/ Imprimir)",
      exp_pinion: "Apenas Pinhão (G1)",
      exp_gear: "Apenas Coroa (G2)",
      exp_kit: "Kit de Teste Rápido (Setores + Base 2 Pinos + Régua Eixo)",
      exp_full: "Conjunto Completo (Par + Gabaritos)",
      note_exp_pair: "Posiciona Pinhão (G1) e Coroa (G2) separados com margem segura na mesa, prontos para fatiar sem fusão de dentes.",
      note_exp_single: "Exporta individualmente a engrenagem selecionada centralizada na mesa de impressão.",
      note_exp_kit: "Imprime em ~10 min: 2 setores dentados + base gabarito na distância entre centros exata (a) + régua de calibração de eixo!",
      note_exp_full: "Pacote completo na mesa: Par de Engrenagens (G1 + G2) acompanhado da base de teste e régua de furo.",
      lbl_auto_slicer: "Auto-Ajustar Fatiamento Mecânico (4–6 paredes maciças + Gyroid)",
      btn_send_plater: "Enviar para a Mesa do OrcaSlicer",
      btn_exp_3mf: "Exportar .3MF",
      btn_exp_stl: "Exportar .STL",
      status_ok: "ÓTIMO",
      status_warn: "ATENÇÃO",
      status_crit: "CRÍTICO",
      thrust_zero_spur: "Empuxo Axial: 0.0 N (Dentes Retos)",
      thrust_zero_hb: "Empuxo Axial: 0.0 N (Auto-Balanceado V)",
      thrust_helical_fmt: "Empuxo Axial Z: {fa} N (Hélice {b}°)",
      toast_randomized: "Novo par de engrenagens gerado!",
      toast_preset_saved: "Preset mecânico salvo com sucesso!"
    },
    en: {
      btn_random: "Randomize",
      tab_gears: "Meshing",
      tab_bodies: "Shafts & Hubs",
      tab_export: "Diagnostics",
      tab_presets: "Presets",
      sec_presets: "Mechanical Presets",
      btn_save_preset: "+ Save",
      btn_ok: "Save",
      cat_all: "All",
      cat_spur: "Spur/Ind",
      cat_helical: "Helical",
      cat_herringbone: "Herringbone",
      cat_robotics: "Robotics/Fit",
      cat_user: "Saved",
      sec_transmission: "Transmission & Helix",
      gt_spur: "Spur",
      gt_helical: "Helical",
      gt_herringbone: "Herringbone (V)",
      lbl_helix_quick: "Quick Helix Angle",
      hand_right: "Right-Hand (G1 R / G2 L)",
      hand_left: "Left-Hand (G1 L / G2 R)",
      btn_swap_teeth: "⇄ Swap Pinion / Gear (Z1 ↔ Z2)",
      sec_tooth_height: "Tooth Height (Factor × | mm)",
      tp_iso: "ISO Standard 1.00×",
      tp_stub: "Heavy Stub 0.75×",
      tp_high: "High Contact 1.20×",
      lbl_auto_shift: "Auto Anti-Undercut Shift (x)",
      sec_bodies: "Bores, Hubs & Lightening",
      body_pinion: "⚙ Pinion G1 (Driver)",
      body_gear: "⚙ Gear G2 (Driven)",
      lbl_bore_type: "Shaft / Bore Type (G1)",
      lbl_bore_type_g2: "Shaft / Bore Type (G2)",
      bore_none: "No Bore (Solid)",
      bore_round: "Round Shaft",
      bore_d: "D-Shaft (NEMA / Motor)",
      bore_dd: "Double-D Shaft",
      bore_hex: "Hex Bore (Across-Flats)",
      bore_keyway: "DIN Keyway Bore",
      lbl_hub: "Raised Central Hub",
      lbl_recess: "Bearing / Bolt Recess",
      side_top: "Top (+Z)",
      side_bottom: "Bottom (Z=0)",
      side_both: "Both Sides",
      lbl_lightening: "Body Mass Lightening",
      light_solid: "Solid Gear Body",
      light_web: "Recessed Web Pocket",
      light_holes: "Circular Lightening Holes",
      vp_meshed: "⚙ Meshed Pair",
      vp_plater: "🖨 Build Plate",
      vp_fit_kit: "🧪 Quick Fit-Test Kit",
      vp_heatmap: "🔥 Overhang",
      vp_forces: "⚡ 3D Forces",
      vp_wire: "⌗ Wire",
      hud_title: "Loads & Mesh",
      hud_cd: "Center Dist a",
      hud_ft: "Tangential Ft",
      hud_fr: "Radial Fr",
      hud_fa: "Axial Thrust Fa",
      cam_iso: "Perspective",
      cam_top: "Top (Meshing)",
      cam_front: "Front (Helix)",
      cam_reset: "Reset",
      sim_scrub: "Angle θ₁",
      sim_delta_a: "Center-Distance Offset (Δa):",
      btn_reset_da: "Reset 0.00 mm",
      loupe_title: "🔍 2D Tooth-Mesh Loupe & Pressure Line",
      jam_alert: "INTERFERENCE / JAMMING DETECTED",
      sec_tolerances: "FDM Clearances & Input Torque",
      sec_diagnostics: "Meshing & Fit Diagnostics",
      diag_sec_contact: "Contact Ratio & Involute",
      dk_eps_a: "Transverse ε_α",
      dk_eps_b: "Axial Overlap ε_β",
      dk_eps_g: "Total Contact ε_γ",
      dk_loa: "Line of Action",
      diag_sec_fit: "Fit, Clearance & Kinematics",
      dk_cd: "Center Distance a",
      dk_clr: "Min Tooth Clearance",
      dk_t2: "Output Torque (G2)",
      dk_rpm2: "Output Speed",
      diag_sec_print: "Mechanical FDM Printability",
      dk_ovh: "Helix Overhang",
      dk_walls: "Suggested Walls",
      dk_wgt: "Est. Weight / Time",
      dk_bed: "Bed Footprint",
      sec_export_pkg: "Export Package & Slicing",
      lbl_export_target: "Target package:",
      exp_pair: "Separated Pair (Ready to Print)",
      exp_pinion: "Pinion Only (G1)",
      exp_gear: "Driven Gear Only (G2)",
      exp_kit: "Quick Fit-Test Kit (Sectors + 2-Pin Jig + Shaft Gauge)",
      exp_full: "Full Suite (Gear Pair + Calibration Jigs)",
      note_exp_pair: "Places Pinion (G1) and Gear (G2) separated with safe gap on the build plate so teeth never fuse.",
      note_exp_single: "Exports only the selected gear centered on the printer build plate.",
      note_exp_kit: "10-minute calibration print: two 5-tooth sectors + 2-pin center-distance base jig + 4-hole shaft gauge!",
      note_exp_full: "Complete build plate suite: full G1 + G2 gear pair alongside center-distance jig and shaft gauge.",
      lbl_auto_slicer: "Auto-Configure Mechanical Slicing (4–6 solid walls + Gyroid)",
      btn_send_plater: "Send to OrcaSlicer Plater",
      btn_exp_3mf: "Export .3MF",
      btn_exp_stl: "Export .STL",
      status_ok: "OPTIMAL",
      status_warn: "WARNING",
      status_crit: "CRITICAL",
      thrust_zero_spur: "Axial Thrust: 0.0 N (Spur)",
      thrust_zero_hb: "Axial Thrust: 0.0 N (Balanced V)",
      thrust_helical_fmt: "Axial Thrust Z: {fa} N ({b}° Helix)",
      toast_randomized: "Generated printable gear pair!",
      toast_preset_saved: "Mechanical preset saved!"
    }
  };

  const SLIDER_SPECS = [
    { path: "helix_angle_deg", min: 0, max: 60, step: 1, unit: "°", pt: "Ângulo de Hélice (β)", en: "Helix Angle (β)" },
    { path: "pinion.teeth", min: 6, max: 160, step: 1, unit: "Z₁", pt: "Dentes do Pinhão (G1)", en: "Pinion Teeth (G1)" },
    { path: "gear.teeth", min: 6, max: 200, step: 1, unit: "Z₂", pt: "Dentes da Coroa (G2)", en: "Driven Gear Teeth (G2)" },
    { path: "module_mm", min: 0.5, max: 10.0, step: 0.05, unit: "mm", pt: "Módulo Normal (m_n)", en: "Normal Module (m_n)" },
    { path: "pressure_angle_deg", min: 14.5, max: 30.0, step: 0.5, unit: "°", pt: "Ângulo de Pressão (α_n)", en: "Pressure Angle (α_n)" },
    { path: "face_width_mm", min: 2.0, max: 120.0, step: 0.5, unit: "mm", pt: "Largura de Face (b)", en: "Face Width (b)" },

    { path: "addendum_coeff", min: 0.40, max: 1.40, step: 0.02, unit: "×", dualMm: true, pt: "Fator de Adendo (h_a*)", en: "Addendum Coeff (h_a*)" },
    { path: "clearance_coeff", min: 0.10, max: 0.50, step: 0.02, unit: "×", dualMm: true, pt: "Folga de Fundo (c*)", en: "Root Clearance Coeff (c*)" },
    { path: "root_fillet_coeff", min: 0.05, max: 0.45, step: 0.02, unit: "×", dualMm: true, pt: "Raio de Filete Raiz (ρ_f*)", en: "Root Fillet Coeff (ρ_f*)" },
    { path: "tip_chamfer_coeff", min: 0.00, max: 0.25, step: 0.01, unit: "×", dualMm: true, pt: "Quebra de Quina Topo (c_k*)", en: "Tip Chamfer Coeff (c_k*)" },

    { path: "profile_shift_g1", min: -0.50, max: 0.80, step: 0.02, unit: "x₁", pt: "Deslocamento Perfil G1 (x₁)", en: "Profile Shift G1 (x₁)" },
    { path: "profile_shift_g2", min: -0.50, max: 0.80, step: 0.02, unit: "x₂", pt: "Deslocamento Perfil G2 (x₂)", en: "Profile Shift G2 (x₂)" },

    { path: "backlash_mm", min: 0.00, max: 1.00, step: 0.01, unit: "mm", pt: "Backlash / Folga Lateral", en: "Circumferential Backlash" },
    { path: "xy_compensation_mm", min: -0.20, max: 0.30, step: 0.01, unit: "mm", pt: "Compensação Expansão XY", en: "FDM XY Compensation" },
    { path: "elephant_foot_chamfer_mm", min: 0.00, max: 1.50, step: 0.05, unit: "mm", pt: "Chanfro Anti-Pé-de-Elefante", en: "Anti-Elephant-Foot Chamfer" },
    { path: "center_distance_offset_mm", min: -1.50, max: 3.00, step: 0.01, unit: "mm", pt: "Offset Distância Centros (Δa)", en: "Center-Distance Offset (Δa)" },
    { path: "input_torque_nm", min: 0.05, max: 50.0, step: 0.05, unit: "N·m", pt: "Torque no Pinhão (T₁)", en: "Input Torque on G1 (T₁)" },

    { path: "pinion.bore_diameter_mm", min: 1.5, max: 80.0, step: 0.1, unit: "mm", pt: "Diâmetro Nominal Eixo", en: "Nominal Shaft Diameter" },
    { path: "pinion.bore_clearance_mm", min: -0.20, max: 0.80, step: 0.01, unit: "mm", pt: "Folga Diametral Furo", en: "Diametral Bore Clearance" },
    { path: "pinion.d_flat_depth_mm", min: 0.10, max: 8.0, step: 0.05, unit: "mm", pt: "Rebaixo do Chanfro D", en: "D-Flat Depth" },
    { path: "pinion.keyway_width_mm", min: 0.8, max: 20.0, step: 0.1, unit: "mm", pt: "Largura da Chaveta", en: "Keyway Width" },
    { path: "pinion.keyway_depth_mm", min: 0.4, max: 12.0, step: 0.1, unit: "mm", pt: "Profundidade da Chaveta", en: "Keyway Depth" },
    { path: "pinion.hub_diameter_mm", min: 4.0, max: 140.0, step: 0.5, unit: "mm", pt: "Diâmetro do Cubo (G1)", en: "Hub Diameter (G1)" },
    { path: "pinion.hub_height_mm", min: 0.5, max: 50.0, step: 0.5, unit: "mm", pt: "Altura do Cubo (G1)", en: "Hub Height (G1)" },
    { path: "pinion.recess_diameter_mm", min: 4.0, max: 140.0, step: 0.2, unit: "mm", pt: "Diâmetro do Rebaixo (G1)", en: "Recess Diameter (G1)" },
    { path: "pinion.recess_depth_mm", min: 0.5, max: 40.0, step: 0.2, unit: "mm", pt: "Profundidade Rebaixo (G1)", en: "Recess Depth (G1)" },
    { path: "pinion.web_thickness_mm", min: 1.2, max: 40.0, step: 0.2, unit: "mm", pt: "Espessura da Alma (G1)", en: "Web Thickness (G1)" },
    { path: "pinion.lightening_hole_count", min: 3, max: 16, step: 1, unit: "un", pt: "Nº Furos de Alívio (G1)", en: "Lightening Hole Count (G1)" },
    { path: "pinion.lightening_hole_diameter_mm", min: 2.0, max: 60.0, step: 0.5, unit: "mm", pt: "Diâmetro Furos Alívio (G1)", en: "Lightening Hole Ø (G1)" },

    { path: "gear.bore_diameter_mm", min: 1.5, max: 80.0, step: 0.1, unit: "mm", pt: "Diâmetro Nominal Eixo", en: "Nominal Shaft Diameter" },
    { path: "gear.bore_clearance_mm", min: -0.20, max: 0.80, step: 0.01, unit: "mm", pt: "Folga Diametral Furo", en: "Diametral Bore Clearance" },
    { path: "gear.d_flat_depth_mm", min: 0.10, max: 8.0, step: 0.05, unit: "mm", pt: "Rebaixo do Chanfro D", en: "D-Flat Depth" },
    { path: "gear.keyway_width_mm", min: 0.8, max: 20.0, step: 0.1, unit: "mm", pt: "Largura da Chaveta", en: "Keyway Width" },
    { path: "gear.keyway_depth_mm", min: 0.4, max: 12.0, step: 0.1, unit: "mm", pt: "Profundidade da Chaveta", en: "Keyway Depth" },
    { path: "gear.hub_diameter_mm", min: 4.0, max: 160.0, step: 0.5, unit: "mm", pt: "Diâmetro do Cubo (G2)", en: "Hub Diameter (G2)" },
    { path: "gear.hub_height_mm", min: 0.5, max: 50.0, step: 0.5, unit: "mm", pt: "Altura do Cubo (G2)", en: "Hub Height (G2)" },
    { path: "gear.recess_diameter_mm", min: 4.0, max: 160.0, step: 0.2, unit: "mm", pt: "Diâmetro do Rebaixo (G2)", en: "Recess Diameter (G2)" },
    { path: "gear.recess_depth_mm", min: 0.5, max: 40.0, step: 0.2, unit: "mm", pt: "Profundidade Rebaixo (G2)", en: "Recess Depth (G2)" },
    { path: "gear.web_thickness_mm", min: 1.2, max: 40.0, step: 0.2, unit: "mm", pt: "Espessura da Alma (G2)", en: "Web Thickness (G2)" },
    { path: "gear.lightening_hole_count", min: 3, max: 16, step: 1, unit: "un", pt: "Nº Furos de Alívio (G2)", en: "Lightening Hole Count (G2)" },
    { path: "gear.lightening_hole_diameter_mm", min: 2.0, max: 80.0, step: 0.5, unit: "mm", pt: "Diâmetro Furos Alívio (G2)", en: "Lightening Hole Ø (G2)" }
  ];

  // ==========================================================================
  // 5. Application State, Simulation State & Undo/Redo Stack
  // ==========================================================================
  const initCtx = (BOOT_PAYLOAD && BOOT_PAYLOAD.initial_context) ? BOOT_PAYLOAD.initial_context : {};
  const state = {
    mode: BOOT_PAYLOAD.mode === "dock" ? "dock" : "page",
    lang: initCtx.lang === "en" ? "en" : "pt",
    theme: initCtx.theme === "light" ? "light" : "dark",
    printer: Object.assign(
      {
        name: "Generic FDM 220×220",
        bed_x: 220.0,
        bed_y: 220.0,
        max_z: 250.0,
        nozzle_mm: 0.4,
        layer_height_mm: 0.2,
        line_width_mm: 0.42
      },
      initCtx.printer || {}
    ),
    builtinPresets: Array.isArray(initCtx.builtin_presets) && initCtx.builtin_presets.length
      ? initCtx.builtin_presets
      : (Array.isArray(BOOT_PAYLOAD.fallback_presets) ? BOOT_PAYLOAD.fallback_presets : []),
    userPresets: Array.isArray(initCtx.user_presets) ? initCtx.user_presets : [],
    presetFilter: "all",
    activePresetId: "spur_classic_1_2",
    activeBodyTab: "pinion", // "pinion" | "gear"
    vpView: "meshed",        // "meshed" | "plater" | "fit_kit"
    heatmap: false,
    showForces: true,
    wireframe: false,
    crossCutPct: 0,
    crossCutAxis: "z",       // "z" | "y"
    loupeZoom: 1.7,
    loupeCollapsed: false,
    simPlaying: true,
    theta1Rad: 0.0,
    lastFrameMs: 0.0,
    isInteracting: false,
    busyAction: false,
    params: normalizeParams(initCtx.params || BOOT_PAYLOAD.fallback_params || JS_DEFAULT_PARAMS),
    geom: null,
    contourG1: null,
    contourG2: null,
    clientReport: null,
    hostReport: null,
    liveCollision: { collided: false, minDistMm: 0.15, hitPoints: [] },
    undoStack: [],
    redoStack: []
  };

  function tr(key) {
    const dict = I18N[state.lang] || I18N.pt;
    return dict[key] !== undefined ? dict[key] : key;
  }

  function getByPath(obj, path) {
    const parts = path.split(".");
    let cur = obj;
    for (let i = 0; i < parts.length; i++) {
      if (cur == null) return undefined;
      cur = cur[parts[i]];
    }
    return cur;
  }

  function setByPath(obj, path, val) {
    const parts = path.split(".");
    let cur = obj;
    for (let i = 0; i < parts.length - 1; i++) {
      if (cur[parts[i]] == null || typeof cur[parts[i]] !== "object") cur[parts[i]] = {};
      cur = cur[parts[i]];
    }
    cur[parts[parts.length - 1]] = val;
  }

  let dragSnapshot = null;
  function beginUndoGesture() {
    if (!dragSnapshot) dragSnapshot = deepClone(state.params);
  }

  function commitUndoGesture() {
    if (!dragSnapshot) return;
    if (JSON.stringify(dragSnapshot) !== JSON.stringify(state.params)) {
      state.undoStack.push(dragSnapshot);
      if (state.undoStack.length > 50) state.undoStack.shift();
      state.redoStack.length = 0;
      updateUndoButtons();
    }
    dragSnapshot = null;
  }

  function pushUndoSnapshot(beforeParams) {
    state.undoStack.push(deepClone(beforeParams));
    if (state.undoStack.length > 50) state.undoStack.shift();
    state.redoStack.length = 0;
    updateUndoButtons();
  }

  function performUndo() {
    if (!state.undoStack.length) return;
    state.redoStack.push(deepClone(state.params));
    state.params = normalizeParams(state.undoStack.pop());
    state.hostReport = null;
    updateUndoButtons();
    syncControlsFromState();
    rebuildScene(false);
    scheduleHostAnalyze();
  }

  function performRedo() {
    if (!state.redoStack.length) return;
    state.undoStack.push(deepClone(state.params));
    state.params = normalizeParams(state.redoStack.pop());
    state.hostReport = null;
    updateUndoButtons();
    syncControlsFromState();
    rebuildScene(false);
    scheduleHostAnalyze();
  }

  // ==========================================================================
  // 6. OrcaSlicer WebView2 IPC Bridge (`window.orca` / `window.chrome.webview` / `postMessage`)
  // ==========================================================================
  let bridgeReadySent = false;
  let analyzeTimer = null;

  function hasOrcaBridge() {
    if (typeof window === "undefined") return false;
    if (window.orca && typeof window.orca.postMessage === "function") return true;
    if (window.chrome && window.chrome.webview && typeof window.chrome.webview.postMessage === "function") return true;
    return false;
  }

  function sendToHost(payload) {
    if (typeof window === "undefined") return false;
    try {
      if (window.orca && typeof window.orca.postMessage === "function") {
        window.orca.postMessage(payload);
        return true;
      }
      if (window.chrome && window.chrome.webview && typeof window.chrome.webview.postMessage === "function") {
        window.chrome.webview.postMessage(payload);
        return true;
      }
    } catch (err) {
      console.error("Orca WebView2 bridge postMessage error:", err);
    }
    return false;
  }

  function scheduleHostAnalyze() {
    if (analyzeTimer) clearTimeout(analyzeTimer);
    analyzeTimer = setTimeout(function () {
      sendToHost({
        type: "analyze",
        params: deepClone(state.params)
      });
    }, 180);
  }

  function detectHostInjectedTheme() {
    if (typeof window === "undefined" || typeof document === "undefined" || !window.getComputedStyle) return null;
    try {
      const rawBg = String(window.getComputedStyle(document.documentElement).getPropertyValue("--orca-bg") || "").trim();
      if (!rawBg) return null;
      let r = -1, g = -1, b = -1;
      if (rawBg.charAt(0) === "#") {
        const hex = rawBg.slice(1).trim();
        if (hex.length === 3) {
          r = parseInt(hex[0] + hex[0], 16);
          g = parseInt(hex[1] + hex[1], 16);
          b = parseInt(hex[2] + hex[2], 16);
        } else if (hex.length >= 6) {
          r = parseInt(hex.slice(0, 2), 16);
          g = parseInt(hex.slice(2, 4), 16);
          b = parseInt(hex.slice(4, 6), 16);
        }
      } else {
        const m = rawBg.match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/i);
        if (m) {
          r = parseInt(m[1], 10);
          g = parseInt(m[2], 10);
          b = parseInt(m[3], 10);
        }
      }
      if (r >= 0 && g >= 0 && b >= 0 && !isNaN(r) && !isNaN(g) && !isNaN(b)) {
        const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
        return lum > 135 ? "light" : "dark";
      }
    } catch (_) {}
    return null;
  }

  function handleHostMessage(rawData) {
    let msg = rawData;
    if (typeof rawData === "string") {
      try {
        msg = JSON.parse(rawData);
      } catch (_) {
        return;
      }
    }
    if (!msg || typeof msg !== "object" || typeof msg.type !== "string") return;

    if (msg.type === "init_state") {
      if (msg.lang === "en" || msg.lang === "pt") state.lang = msg.lang;
      const injectedTheme = detectHostInjectedTheme();
      if (injectedTheme && !msg.theme_explicit) {
        state.theme = injectedTheme;
      } else if (msg.theme === "light" || msg.theme === "dark") {
        state.theme = msg.theme;
      }
      if (msg.printer && typeof msg.printer === "object") {
        state.printer = Object.assign(state.printer, msg.printer);
      }
      if (Array.isArray(msg.builtin_presets) && msg.builtin_presets.length) {
        state.builtinPresets = msg.builtin_presets;
      }
      if (Array.isArray(msg.user_presets)) {
        state.userPresets = msg.user_presets;
      }
      if (msg.params && typeof msg.params === "object") {
        state.params = normalizeParams(msg.params);
      }
      applyThemeAndLanguage();
      renderPresetsGrid();
      syncControlsFromState();
      rebuildBedGeometry();
      rebuildScene(false);
      fitCameraToScene();
      return;
    }

    if (msg.type === "analysis_result" && msg.report) {
      state.hostReport = msg.report;
      updateDiagnosticsUI();
      return;
    }

    if (msg.type === "params_updated" && msg.params) {
      pushUndoSnapshot(state.params);
      state.params = normalizeParams(msg.params);
      state.hostReport = null;
      syncControlsFromState();
      rebuildScene(false);
      scheduleHostAnalyze();
      showToast(tr("toast_randomized"), false);
      return;
    }

    if (msg.type === "presets_updated" && Array.isArray(msg.user_presets)) {
      state.userPresets = msg.user_presets;
      renderPresetsGrid();
      return;
    }

    if (msg.type === "action_result") {
      setActionButtonsBusy(false);
      if (msg.report) {
        state.hostReport = msg.report;
        updateDiagnosticsUI();
      }
      if (msg.message) {
        showToast(msg.message, !msg.ok);
      }
      return;
    }
  }

  function connectOrcaBridge() {
    if (typeof window === "undefined") return;
    window.addEventListener("message", function (ev) {
      if (ev && ev.data) handleHostMessage(ev.data);
    });
    if (window.chrome && window.chrome.webview && typeof window.chrome.webview.addEventListener === "function") {
      window.chrome.webview.addEventListener("message", function (ev) {
        if (ev && ev.data) handleHostMessage(ev.data);
      });
    }
    const tryBind = function () {
      if (bridgeReadySent) return;
      if (window.orca && typeof window.orca.onMessage === "function") {
        bridgeReadySent = true;
        window.orca.onMessage(handleHostMessage);
        sendToHost({ type: "ready", mode: state.mode });
      } else if (window.chrome && window.chrome.webview && typeof window.chrome.webview.postMessage === "function") {
        bridgeReadySent = true;
        sendToHost({ type: "ready", mode: state.mode });
      }
    };
    tryBind();
    if (!bridgeReadySent) {
      setTimeout(tryBind, 80);
      setTimeout(tryBind, 300);
    }
  }

  // ==========================================================================
  // 7. 3D Mesh Builders (Pinion, Gear, Bores, Hubs, Recesses, Lightening & Fit Kit)
  // ==========================================================================
  function createCollector() {
    return {
      pos: [],
      nrm: [],
      ovh: [],
      idx: [],
      wire: [],
      vCount: 0,
      addV: function (x, y, z, nx, ny, nz, ovhDeg) {
        const id = this.vCount++;
        this.pos.push(x, y, z);
        this.nrm.push(nx, ny, nz);
        this.ovh.push(ovhDeg);
        return id;
      },
      addTri: function (a, b, c) {
        this.idx.push(a, b, c);
      },
      addWire: function (x1, y1, z1, x2, y2, z2) {
        this.wire.push(x1, y1, z1, x2, y2, z2);
      }
    };
  }

  function raySectorDistance(hx, hy, dirX, dirY, halfAngle, outerRadius) {
    const b = 2.0 * (hx * dirX + hy * dirY);
    const c = hx * hx + hy * hy - outerRadius * outerRadius;
    const disc = Math.max(0.0, b * b - 4.0 * c);
    let bestT = 0.5 * (-b + Math.sqrt(disc));
    if (halfAngle < Math.PI - 1e-4) {
      const angles = [halfAngle, -halfAngle];
      for (let k = 0; k < 2; k++) {
        const rx = Math.cos(angles[k]);
        const ry = Math.sin(angles[k]);
        const det = dirX * ry - dirY * rx;
        if (Math.abs(det) > 1e-8) {
          const tRay = (ry * (-hx) - rx * (-hy)) / det;
          const sRay = (dirX * (-hy) - dirY * (-hx)) / det;
          if (tRay > 1e-5 && sRay >= -1e-5 && tRay < bestT) bestT = tRay;
        }
      }
    }
    return Math.max(bestT, 0.1);
  }

  function appendAnnulusCap(col, rInPtsX, rInPtsY, rOut, zVal, facingUp) {
    const n = rInPtsX.length;
    const nz = facingUp ? 1.0 : -1.0;
    const inIds = new Int32Array(n);
    const outIds = new Int32Array(n);
    for (let i = 0; i < n; i++) {
      const ang = (TWO_PI * i) / n;
      inIds[i] = col.addV(rInPtsX[i], rInPtsY[i], zVal, 0, 0, nz, 0.0);
      outIds[i] = col.addV(rOut * Math.cos(ang), rOut * Math.sin(ang), zVal, 0, 0, nz, 0.0);
    }
    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n;
      if (facingUp) {
        col.addTri(inIds[i], outIds[i], outIds[j]);
        col.addTri(inIds[i], outIds[j], inIds[j]);
      } else {
        col.addTri(inIds[i], outIds[j], outIds[i]);
        col.addTri(inIds[i], inIds[j], outIds[j]);
      }
    }
  }

  function appendCircleStepWall(col, radius, z0, z1, segs, outward) {
    if (Math.abs(z1 - z0) < 1e-4) return;
    const r0 = new Int32Array(segs);
    const r1 = new Int32Array(segs);
    const sgn = outward ? 1.0 : -1.0;
    for (let i = 0; i < segs; i++) {
      const a = (TWO_PI * i) / segs;
      const c = Math.cos(a), s = Math.sin(a);
      r0[i] = col.addV(radius * c, radius * s, z0, sgn * c, sgn * s, 0, 0);
      r1[i] = col.addV(radius * c, radius * s, z1, sgn * c, sgn * s, 0, 0);
    }
    const zUp = z1 > z0;
    const flip = outward ? zUp : !zUp;
    for (let i = 0; i < segs; i++) {
      const j = (i + 1) % segs;
      if (flip) {
        col.addTri(r0[i], r0[j], r1[j]);
        col.addTri(r0[i], r1[j], r1[i]);
      } else {
        col.addTri(r0[i], r1[j], r0[j]);
        col.addTri(r0[i], r1[i], r1[j]);
      }
    }
  }

  function appendPerforatedWebAnnulus(col, rIn, rOut, zBot, zTop, holeCount, holeDiam) {
    const nHoles = Math.max(3, Math.min(18, holeCount | 0));
    const midR = 0.5 * (rIn + rOut);
    const radialHalf = 0.5 * (rOut - rIn);
    const maxChordHalf = midR * Math.sin(Math.PI / nHoles) * 0.72;
    const hr = Math.max(0.8, Math.min(0.5 * holeDiam, radialHalf - 0.8, maxChordHalf));
    const holeSegs = 20;
    const halfSector = Math.PI / nHoles;

    for (let k = 0; k < nHoles; k++) {
      const rot = (TWO_PI * k) / nHoles;
      const cosR = Math.cos(rot), sinR = Math.sin(rot);
      const botHole = [], botBnd = [], topHole = [], topBnd = [];
      const tunBot = [], tunTop = [];

      for (let s = 0; s < holeSegs; s++) {
        const aL = (TWO_PI * s) / holeSegs;
        const dx = Math.cos(aL), dy = Math.sin(aL);
        let dBnd = raySectorDistance(midR, 0.0, dx, dy, halfSector, rOut);

        // Intersect ray with inner circle rIn if pointing inward
        const bIn = 2.0 * midR * dx;
        const cIn = midR * midR - rIn * rIn;
        const discIn = bIn * bIn - 4.0 * cIn;
        if (discIn > 0.0) {
          const tIn = 0.5 * (-bIn - Math.sqrt(discIn));
          if (tIn > 1e-4 && tIn < dBnd) dBnd = tIn;
        }
        dBnd = Math.max(hr + 0.15, dBnd);

        const lxH = midR + hr * dx, lyH = hr * dy;
        const lxB = midR + dBnd * dx, lyB = dBnd * dy;
        const wxH = lxH * cosR - lyH * sinR, wyH = lxH * sinR + lyH * cosR;
        const wxB = lxB * cosR - lyB * sinR, wyB = lxB * sinR + lyB * cosR;

        botHole.push(col.addV(wxH, wyH, zBot, 0, 0, -1, 0));
        botBnd.push(col.addV(wxB, wyB, zBot, 0, 0, -1, 0));
        topHole.push(col.addV(wxH, wyH, zTop, 0, 0, 1, 0));
        topBnd.push(col.addV(wxB, wyB, zTop, 0, 0, 1, 0));

        const nx = -(dx * cosR - dy * sinR);
        const ny = -(dx * sinR + dy * cosR);
        tunBot.push(col.addV(wxH, wyH, zBot, nx, ny, 0, 0));
        tunTop.push(col.addV(wxH, wyH, zTop, nx, ny, 0, 0));
      }

      for (let s = 0; s < holeSegs; s++) {
        const j = (s + 1) % holeSegs;
        col.addTri(botHole[s], botBnd[j], botBnd[s]);
        col.addTri(botHole[s], botHole[j], botBnd[j]);
        col.addTri(topHole[s], topBnd[s], topBnd[j]);
        col.addTri(topHole[s], topBnd[j], topHole[j]);
        col.addTri(tunBot[s], tunTop[s], tunTop[j]);
        col.addTri(tunBot[s], tunTop[j], tunBot[j]);
      }
    }
  }

  function buildGear3DMeshData(p, geom, which, fast) {
    const col = createCollector();
    const g = which === "gear" ? geom.gear : geom.pinion;
    const bodyCfg = which === "gear" ? p.gear : p.pinion;
    const b = p.face_width_mm;
    const samplesFlank = fast ? 5 : 8;

    const baseContour = buildGear2DContour(p, geom, which, samplesFlank, 0.0);
    const chamf = Math.max(0.0, Math.min(p.elephant_foot_chamfer_mm, 0.22 * b));
    const chamfContour = chamf > 0.02
      ? buildGear2DContour(p, geom, which, samplesFlank, chamf)
      : baseContour;

    const interiorSlices = p.gear_type === "spur"
      ? 2
      : (fast ? Math.max(12, Math.round(b * 1.3)) : Math.max(22, Math.round(b * 2.2)));

    const zLevels = [];
    const zContours = [];
    if (chamf > 0.02) {
      zLevels.push(0.0);
      zContours.push(chamfContour);
      for (let i = 0; i <= interiorSlices; i++) {
        const t = i / interiorSlices;
        const z = chamf + t * (b - 2.0 * chamf);
        zLevels.push(z);
        zContours.push(baseContour);
      }
      zLevels.push(b);
      zContours.push(chamfContour);
    } else {
      for (let i = 0; i <= interiorSlices; i++) {
        zLevels.push((i / interiorSlices) * b);
        zContours.push(baseContour);
      }
    }

    const nz = zLevels.length;
    const nt = baseContour.count;
    const ringX = new Array(nz);
    const ringY = new Array(nz);

    for (let i = 0; i < nz; i++) {
      const z = zLevels[i];
      const psi = helixTwistAngleRad(z, b, g.pitch_radius_mm, geom.beta_deg, g.helix_hand, p.gear_type);
      const cosP = Math.cos(psi), sinP = Math.sin(psi);
      const src = zContours[i];
      const rx = new Float32Array(nt);
      const ry = new Float32Array(nt);
      for (let j = 0; j < nt; j++) {
        rx[j] = src.xs[j] * cosP - src.ys[j] * sinP;
        ry[j] = src.xs[j] * sinP + src.ys[j] * cosP;
      }
      ringX[i] = rx;
      ringY[i] = ry;
    }

    // Build outer gear tooth wall with exact helical & chamfer normals + overhang
    const wallRingIds = new Array(nz);
    for (let i = 0; i < nz; i++) {
      const ids = new Int32Array(nt);
      const i0 = Math.max(0, i - 1);
      const i1 = Math.min(nz - 1, i + 1);
      const dz = Math.max(1e-5, zLevels[i1] - zLevels[i0]);
      const z = zLevels[i];

      for (let j = 0; j < nt; j++) {
        const jp = (j + nt - 1) % nt;
        const jn = (j + 1) % nt;
        const tx = ringX[i][jn] - ringX[i][jp];
        const ty = ringY[i][jn] - ringY[i][jp];
        const ux = ringX[i1][j] - ringX[i0][j];
        const uy = ringY[i1][j] - ringY[i0][j];

        // Outward normal = T_ring x T_up
        let nx = ty * dz;
        let ny = -tx * dz;
        let nzVal = tx * uy - ty * ux;
        const nLen = Math.hypot(nx, ny, nzVal) || 1.0;
        nx /= nLen; ny /= nLen; nzVal /= nLen;

        let ovhDeg = 0.0;
        if (z > 0.03 && nzVal < -1e-4) {
          ovhDeg = Math.asin(Math.min(1.0, -nzVal)) * RAD2DEG;
        }
        ids[j] = col.addV(ringX[i][j], ringY[i][j], z, nx, ny, nzVal, ovhDeg);
      }
      wallRingIds[i] = ids;
    }

    for (let i = 0; i < nz - 1; i++) {
      const r0 = wallRingIds[i], r1 = wallRingIds[i + 1];
      for (let j = 0; j < nt; j++) {
        const jn = (j + 1) % nt;
        col.addTri(r0[j], r0[jn], r1[jn]);
        col.addTri(r0[j], r1[jn], r1[j]);
      }
    }

    // Sample clean wireframe lines on top, mid, and bottom tooth contours
    const wireSlices = [0, Math.floor(nz * 0.5), nz - 1];
    for (let ws = 0; ws < wireSlices.length; ws++) {
      const si = wireSlices[ws];
      const z = zLevels[si];
      for (let j = 0; j < nt; j++) {
        const jn = (j + 1) % nt;
        col.addWire(ringX[si][j], ringY[si][j], z, ringX[si][jn], ringY[si][jn], z);
      }
    }

    // Rim inner circle inside root radius
    const rSafeRim = Math.max(1.2, chamfContour.rf - Math.max(0.9, 0.45 * geom.m_n));
    const capSegs = 64;

    // Stitch outer tooth contour at z=0 and z=b cleanly inward to circular rim `rSafeRim`
    const stitchContourToCircle = function (rx, ry, rInner, zVal, facingUp) {
      const nzDir = facingUp ? 1.0 : -1.0;
      const outIds = new Int32Array(nt);
      const inIds = new Int32Array(nt);
      for (let j = 0; j < nt; j++) {
        const ang = Math.atan2(ry[j], rx[j]);
        outIds[j] = col.addV(rx[j], ry[j], zVal, 0, 0, nzDir, 0);
        inIds[j] = col.addV(rInner * Math.cos(ang), rInner * Math.sin(ang), zVal, 0, 0, nzDir, 0);
      }
      for (let j = 0; j < nt; j++) {
        const jn = (j + 1) % nt;
        if (facingUp) {
          col.addTri(inIds[j], outIds[j], outIds[jn]);
          col.addTri(inIds[j], outIds[jn], inIds[jn]);
        } else {
          col.addTri(inIds[j], outIds[jn], outIds[j]);
          col.addTri(inIds[j], inIds[jn], outIds[jn]);
        }
      }
    };
    stitchContourToCircle(ringX[0], ringY[0], rSafeRim, 0.0, false);
    stitchContourToCircle(ringX[nz - 1], ringY[nz - 1], rSafeRim, b, true);

    // Bore contour inside safe radius
    const maxBoreR = Math.max(0.6, rSafeRim - 1.0);
    const bore = buildBore2DContour(bodyCfg, maxBoreR, capSegs, 0.0);
    const rBoreOuter = bore
      ? Math.min(rSafeRim - 0.6, Math.max(bore.rNom, 0.5 * bodyCfg.bore_diameter_mm) + (bodyCfg.bore_type === "keyway" ? bodyCfg.keyway_depth_mm : 0.0) + 0.8)
      : 0.0;

    // Determine concentric radial zones from rCoreOut -> rSafeRim
    let zTopInner = b;
    let zBotInner = 0.0;
    let rInnerCore = Math.min(rSafeRim, Math.max(rBoreOuter, 1.2));

    const hasHub = Boolean(bodyCfg.hub_enabled) && (rSafeRim > rBoreOuter + 1.2);
    const hasRecess = Boolean(bodyCfg.recess_enabled) && (rSafeRim > rBoreOuter + 1.2);
    const rHub = hasHub ? Math.max(rInnerCore + 0.6, Math.min(rSafeRim - 0.3, 0.5 * bodyCfg.hub_diameter_mm)) : rInnerCore;
    const rRecess = hasRecess ? Math.max(rInnerCore + 0.6, Math.min(rSafeRim - 0.3, 0.5 * bodyCfg.recess_diameter_mm)) : rInnerCore;

    let zFeatureTop = b;
    let zFeatureBot = 0.0;
    let rFeature = rInnerCore;

    if (hasRecess) {
      rFeature = rRecess;
      const maxDepth = Math.max(0.4, 0.42 * b);
      const dep = Math.min(bodyCfg.recess_depth_mm, maxDepth);
      if (bodyCfg.recess_side === "top" || bodyCfg.recess_side === "both") zFeatureTop = b - dep;
      if (bodyCfg.recess_side === "bottom" || bodyCfg.recess_side === "both") zFeatureBot = dep;
    } else if (hasHub) {
      rFeature = rHub;
      zFeatureTop = b + bodyCfg.hub_height_mm;
    }
    zTopInner = zFeatureTop;
    zBotInner = zFeatureBot;

    // Inner bore tunnel OR solid center disk
    if (bore) {
      const bBot = new Int32Array(capSegs);
      const bTop = new Int32Array(capSegs);
      for (let i = 0; i < capSegs; i++) {
        const ip = (i + capSegs - 1) % capSegs;
        const inx = (i + 1) % capSegs;
        const tx = bore.xs[inx] - bore.xs[ip];
        const ty = bore.ys[inx] - bore.ys[ip];
        const tl = Math.hypot(tx, ty) || 1.0;
        // Bore wall faces inward toward origin: (-ty, tx) for CCW contour
        const nx = -ty / tl, ny = tx / tl;
        bBot[i] = col.addV(bore.xs[i], bore.ys[i], zBotInner, nx, ny, 0, 0);
        bTop[i] = col.addV(bore.xs[i], bore.ys[i], zTopInner, nx, ny, 0, 0);
      }
      for (let i = 0; i < capSegs; i++) {
        const j = (i + 1) % capSegs;
        col.addTri(bBot[i], bTop[i], bTop[j]);
        col.addTri(bBot[i], bTop[j], bBot[j]);
      }
      appendAnnulusCap(col, bore.xs, bore.ys, rFeature, zTopInner, true);
      appendAnnulusCap(col, bore.xs, bore.ys, rFeature, zBotInner, false);
    } else {
      const cTop = col.addV(0, 0, zTopInner, 0, 0, 1, 0);
      const cBot = col.addV(0, 0, zBotInner, 0, 0, -1, 0);
      const rTop = new Int32Array(capSegs);
      const rBot = new Int32Array(capSegs);
      for (let i = 0; i < capSegs; i++) {
        const a = (TWO_PI * i) / capSegs;
        rTop[i] = col.addV(rFeature * Math.cos(a), rFeature * Math.sin(a), zTopInner, 0, 0, 1, 0);
        rBot[i] = col.addV(rFeature * Math.cos(a), rFeature * Math.sin(a), zBotInner, 0, 0, -1, 0);
      }
      for (let i = 0; i < capSegs; i++) {
        const j = (i + 1) % capSegs;
        col.addTri(cTop, rTop[i], rTop[j]);
        col.addTri(cBot, rBot[j], rBot[i]);
      }
    }

    // Vertical step wall at rFeature if Hub or Recess changed Z
    if (Math.abs(zFeatureTop - b) > 1e-4) {
      appendCircleStepWall(col, rFeature, b, zFeatureTop, capSegs, zFeatureTop > b);
    }
    if (Math.abs(zFeatureBot - 0.0) > 1e-4) {
      // Bottom recess ceiling overhang = 90 deg if recessed on bottom
      appendCircleStepWall(col, rFeature, 0.0, zFeatureBot, capSegs, false);
    }

    // Body region between rFeature and rSafeRim: Solid, Web Recess, or Lightening Holes
    const spanRadial = rSafeRim - rFeature;
    const circlePts = function (rad) {
      const xs = new Float64Array(capSegs), ys = new Float64Array(capSegs);
      for (let i = 0; i < capSegs; i++) {
        const a = (TWO_PI * i) / capSegs;
        xs[i] = rad * Math.cos(a);
        ys[i] = rad * Math.sin(a);
      }
      return { xs: xs, ys: ys };
    };

    if (bodyCfg.lightening_mode === "web_recess" && spanRadial > 3.0) {
      const rWebIn = rFeature + 0.8;
      const rWebOut = rSafeRim - 0.8;
      const webH = Math.max(1.2, Math.min(b - 0.8, bodyCfg.web_thickness_mm));
      const zWebBot = 0.5 * (b - webH);
      const zWebTop = b - zWebBot;

      const cFeat = circlePts(rFeature);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rWebIn, b, true);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rWebIn, 0.0, false);

      appendCircleStepWall(col, rWebIn, zWebTop, b, capSegs, true);
      appendCircleStepWall(col, rWebIn, zWebBot, 0.0, capSegs, true);

      const cWebIn = circlePts(rWebIn);
      appendAnnulusCap(col, cWebIn.xs, cWebIn.ys, rWebOut, zWebTop, true);
      appendAnnulusCap(col, cWebIn.xs, cWebIn.ys, rWebOut, zWebBot, false);

      appendCircleStepWall(col, rWebOut, zWebTop, b, capSegs, false);
      appendCircleStepWall(col, rWebOut, zWebBot, 0.0, capSegs, false);

      const cWebOut = circlePts(rWebOut);
      appendAnnulusCap(col, cWebOut.xs, cWebOut.ys, rSafeRim, b, true);
      appendAnnulusCap(col, cWebOut.xs, cWebOut.ys, rSafeRim, 0.0, false);
    } else if (bodyCfg.lightening_mode === "lightening_holes" && spanRadial > 3.6) {
      const rHoleIn = rFeature + 0.6;
      const rHoleOut = rSafeRim - 0.6;
      const cFeat = circlePts(rFeature);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rHoleIn, b, true);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rHoleIn, 0.0, false);

      appendPerforatedWebAnnulus(
        col,
        rHoleIn,
        rHoleOut,
        0.0,
        b,
        bodyCfg.lightening_hole_count,
        bodyCfg.lightening_hole_diameter_mm
      );

      const cHoleOut = circlePts(rHoleOut);
      appendAnnulusCap(col, cHoleOut.xs, cHoleOut.ys, rSafeRim, b, true);
      appendAnnulusCap(col, cHoleOut.xs, cHoleOut.ys, rSafeRim, 0.0, false);
    } else if (spanRadial > 1e-4) {
      const cFeat = circlePts(rFeature);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rSafeRim, b, true);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rSafeRim, 0.0, false);
    }

    return col;
  }

  // Fit-Test Kit 3D Preview Builders (Jig Base + 2 Pins, 5-Tooth Sectors, 4-Hole Bore Gauge)
  function buildFitKitSectorMesh(p, geom, which) {
    const g = which === "gear" ? geom.gear : geom.pinion;
    const zTeeth = g.teeth;
    const bKit = Math.min(p.face_width_mm, 8.0);
    const minRootD = 2.0 * Math.min(geom.pinion.root_radius_mm, geom.gear.root_radius_mm);
    const dPinHole = Math.max(4.0, Math.min(8.0, 0.45 * minRootD));

    if (zTeeth <= 9) {
      const pClone = deepClone(p);
      pClone.face_width_mm = bKit;
      const bObj = which === "gear" ? pClone.gear : pClone.pinion;
      bObj.bore_type = "round";
      bObj.bore_diameter_mm = dPinHole;
      bObj.bore_clearance_mm = 0.0;
      bObj.hub_enabled = false;
      bObj.recess_enabled = false;
      bObj.lightening_mode = "solid";
      return buildGear3DMeshData(pClone, geom, which, true);
    }

    const col = createCollector();
    const tpl = buildSingleToothPolarTemplate(p, geom, which, 6, 0.0);
    const nKeep = Math.min(5, zTeeth);
    const kStart = -Math.floor(nKeep / 2);
    const kEnd = kStart + nKeep - 1;
    const centerBaseAng = which === "gear" ? Math.PI : 0.0;

    const arcPhi = [];
    const arcR = [];
    for (let k = kStart; k <= kEnd; k++) {
      const off = centerBaseAng + (TWO_PI * k) / zTeeth;
      for (let j = 0; j < tpl.phi.length; j++) {
        arcPhi.push(off + tpl.phi[j]);
        arcR.push(tpl.rad[j]);
      }
    }

    const rRingInner = 0.5 * dPinHole;
    const rRingOuter = Math.max(rRingInner + 2.4, Math.min(tpl.rf - 0.5, rRingInner + 4.5));
    const phiFirst = arcPhi[0];
    const phiLast = arcPhi[arcPhi.length - 1];

    // Closed outer loop of sector wedge + hub ring
    const polyBaseX = [];
    const polyBaseY = [];
    const polyIsTeeth = [];
    for (let i = 0; i < arcPhi.length; i++) {
      polyBaseX.push(arcR[i] * Math.cos(arcPhi[i]));
      polyBaseY.push(arcR[i] * Math.sin(arcPhi[i]));
      polyIsTeeth.push(true);
    }
    const backSteps = 28;
    const backSpan = TWO_PI - (phiLast - phiFirst);
    for (let s = 0; s <= backSteps; s++) {
      const ang = phiLast + (s / backSteps) * backSpan;
      polyBaseX.push(rRingOuter * Math.cos(ang));
      polyBaseY.push(rRingOuter * Math.sin(ang));
      polyIsTeeth.push(false);
    }

    const nLoop = polyBaseX.length;
    const nz = p.gear_type === "spur" ? 2 : 14;
    const ringsIds = new Array(nz);
    const ringWX = new Array(nz);
    const ringWY = new Array(nz);

    for (let i = 0; i < nz; i++) {
      const z = (i / (nz - 1)) * bKit;
      const psi = helixTwistAngleRad(z, bKit, g.pitch_radius_mm, geom.beta_deg, g.helix_hand, p.gear_type);
      const cp = Math.cos(psi), sp = Math.sin(psi);
      const wx = new Float32Array(nLoop);
      const wy = new Float32Array(nLoop);
      for (let j = 0; j < nLoop; j++) {
        if (polyIsTeeth[j]) {
          wx[j] = polyBaseX[j] * cp - polyBaseY[j] * sp;
          wy[j] = polyBaseX[j] * sp + polyBaseY[j] * cp;
        } else {
          wx[j] = polyBaseX[j];
          wy[j] = polyBaseY[j];
        }
      }
      ringWX[i] = wx;
      ringWY[i] = wy;
    }

    for (let i = 0; i < nz; i++) {
      const z = (i / (nz - 1)) * bKit;
      const ids = new Int32Array(nLoop);
      for (let j = 0; j < nLoop; j++) {
        const jp = (j + nLoop - 1) % nLoop;
        const jn = (j + 1) % nLoop;
        const tx = ringWX[i][jn] - ringWX[i][jp];
        const ty = ringWY[i][jn] - ringWY[i][jp];
        const tl = Math.hypot(tx, ty) || 1.0;
        ids[j] = col.addV(ringWX[i][j], ringWY[i][j], z, ty / tl, -tx / tl, 0, 0);
      }
      ringsIds[i] = ids;
    }
    for (let i = 0; i < nz - 1; i++) {
      for (let j = 0; j < nLoop; j++) {
        const jn = (j + 1) % nLoop;
        col.addTri(ringsIds[i][j], ringsIds[i][jn], ringsIds[i + 1][jn]);
        col.addTri(ringsIds[i][j], ringsIds[i + 1][jn], ringsIds[i + 1][j]);
      }
    }

    // Inner pin hole tunnel + top/bottom caps
    const holeBot = new Int32Array(nLoop);
    const holeTop = new Int32Array(nLoop);
    const capBotIn = new Int32Array(nLoop), capBotOut = new Int32Array(nLoop);
    const capTopIn = new Int32Array(nLoop), capTopOut = new Int32Array(nLoop);

    for (let j = 0; j < nLoop; j++) {
      const angB = Math.atan2(ringWY[0][j], ringWX[0][j]);
      const angT = Math.atan2(ringWY[nz - 1][j], ringWX[nz - 1][j]);
      const ixB = rRingInner * Math.cos(angB), iyB = rRingInner * Math.sin(angB);
      const ixT = rRingInner * Math.cos(angT), iyT = rRingInner * Math.sin(angT);

      const aHole = (TWO_PI * j) / nLoop;
      const ch = Math.cos(aHole), sh = Math.sin(aHole);
      holeBot[j] = col.addV(rRingInner * ch, rRingInner * sh, 0.0, -ch, -sh, 0, 0);
      holeTop[j] = col.addV(rRingInner * ch, rRingInner * sh, bKit, -ch, -sh, 0, 0);

      capBotIn[j] = col.addV(ixB, iyB, 0.0, 0, 0, -1, 0);
      capBotOut[j] = col.addV(ringWX[0][j], ringWY[0][j], 0.0, 0, 0, -1, 0);
      capTopIn[j] = col.addV(ixT, iyT, bKit, 0, 0, 1, 0);
      capTopOut[j] = col.addV(ringWX[nz - 1][j], ringWY[nz - 1][j], bKit, 0, 0, 1, 0);
    }
    for (let j = 0; j < nLoop; j++) {
      const jn = (j + 1) % nLoop;
      col.addTri(holeBot[j], holeTop[j], holeTop[jn]);
      col.addTri(holeBot[j], holeTop[jn], holeBot[jn]);
      col.addTri(capBotIn[j], capBotOut[jn], capBotOut[j]);
      col.addTri(capBotIn[j], capBotIn[jn], capBotOut[jn]);
      col.addTri(capTopIn[j], capTopOut[j], capTopOut[jn]);
      col.addTri(capTopIn[j], capTopOut[jn], capTopIn[jn]);
    }

    return col;
  }

  function buildFitKitJigAndGaugeMeshes(p, geom) {
    const a = geom.center_distance_mm;
    const minRootD = 2.0 * Math.min(geom.pinion.root_radius_mm, geom.gear.root_radius_mm);
    const dPin = Math.max(4.0, Math.min(8.0, 0.45 * minRootD)) - 0.22;
    const rPin = 0.5 * dPin;
    const bKit = Math.min(p.face_width_mm, 8.0);
    const rPad = Math.max(rPin + 5.5, 9.5);
    const baseH = 3.0;
    const pinTopZ = baseH + bKit + 1.5;

    // 1. 2-Pin Rounded Stadium Jig Base
    const jigCol = createCollector();
    const nArc = 24;
    const stadX = [], stadY = [];
    for (let i = 0; i <= nArc; i++) {
      const ang = -0.5 * Math.PI + (Math.PI * i) / nArc;
      stadX.push(0.5 * a + rPad * Math.cos(ang));
      stadY.push(rPad * Math.sin(ang));
    }
    for (let i = 0; i <= nArc; i++) {
      const ang = 0.5 * Math.PI + (Math.PI * i) / nArc;
      stadX.push(-0.5 * a + rPad * Math.cos(ang));
      stadY.push(rPad * Math.sin(ang));
    }
    const nS = stadX.length;
    const bIds = new Int32Array(nS), tIds = new Int32Array(nS);
    const cBot = jigCol.addV(0, 0, 0, 0, 0, -1, 0);
    const cTop = jigCol.addV(0, 0, baseH, 0, 0, 1, 0);
    const cbRing = new Int32Array(nS), ctRing = new Int32Array(nS);

    for (let i = 0; i < nS; i++) {
      const ip = (i + nS - 1) % nS, inx = (i + 1) % nS;
      const tx = stadX[inx] - stadX[ip], ty = stadY[inx] - stadY[ip];
      const tl = Math.hypot(tx, ty) || 1.0;
      bIds[i] = jigCol.addV(stadX[i], stadY[i], 0, ty / tl, -tx / tl, 0, 0);
      tIds[i] = jigCol.addV(stadX[i], stadY[i], baseH, ty / tl, -tx / tl, 0, 0);
      cbRing[i] = jigCol.addV(stadX[i], stadY[i], 0, 0, 0, -1, 0);
      ctRing[i] = jigCol.addV(stadX[i], stadY[i], baseH, 0, 0, 1, 0);
    }
    for (let i = 0; i < nS; i++) {
      const j = (i + 1) % nS;
      jigCol.addTri(bIds[i], bIds[j], tIds[j]);
      jigCol.addTri(bIds[i], tIds[j], tIds[i]);
      jigCol.addTri(cBot, cbRing[j], cbRing[i]);
      jigCol.addTri(cTop, ctRing[i], ctRing[j]);
    }

    // Add 2 vertical pins at (-a/2, 0) and (+a/2, 0) with 0.6mm top chamfer
    const pinCenters = [-0.5 * a, 0.5 * a];
    const pSegs = 28;
    for (let pk = 0; pk < 2; pk++) {
      const px = pinCenters[pk];
      const r0 = new Int32Array(pSegs), r1 = new Int32Array(pSegs), r2 = new Int32Array(pSegs);
      const capC = jigCol.addV(px, 0, pinTopZ, 0, 0, 1, 0);
      const capR = new Int32Array(pSegs);
      const rChamfTop = Math.max(0.5, rPin - 0.6);
      for (let s = 0; s < pSegs; s++) {
        const ang = (TWO_PI * s) / pSegs;
        const cs = Math.cos(ang), sn = Math.sin(ang);
        r0[s] = jigCol.addV(px + rPin * cs, rPin * sn, baseH, cs, sn, 0, 0);
        r1[s] = jigCol.addV(px + rPin * cs, rPin * sn, pinTopZ - 0.6, cs, sn, 0.3, 0);
        r2[s] = jigCol.addV(px + rChamfTop * cs, rChamfTop * sn, pinTopZ, 0.7 * cs, 0.7 * sn, 0.7, 0);
        capR[s] = jigCol.addV(px + rChamfTop * cs, rChamfTop * sn, pinTopZ, 0, 0, 1, 0);
      }
      for (let s = 0; s < pSegs; s++) {
        const j = (s + 1) % pSegs;
        jigCol.addTri(r0[s], r0[j], r1[j]);
        jigCol.addTri(r0[s], r1[j], r1[s]);
        jigCol.addTri(r1[s], r1[j], r2[j]);
        jigCol.addTri(r1[s], r2[j], r2[s]);
        jigCol.addTri(capC, capR[s], capR[j]);
      }
    }

    // 2. 4-Hole Bore Calibration Strip Gauge with V-Notch Markers
    const gaugeCol = createCollector();
    const bCfg = deepClone(p.pinion);
    if (bCfg.bore_type === "none") bCfg.bore_type = "round";
    const holeD = Math.max(2.0, Math.min(18.0, bCfg.bore_diameter_mm));
    const pitchX = holeD + 6.5;
    const halfW = 2.0 * pitchX + 3.0;
    const halfD = 0.5 * holeD + 4.5;
    const gH = 5.0;
    const deltas = [-0.05, 0.0, 0.05, 0.10];

    for (let k = 0; k < 4; k++) {
      const cx = (k - 1.5) * pitchX;
      const xL = cx - 0.5 * pitchX + (k === 0 ? -1.5 : 0.0);
      const xR = cx + 0.5 * pitchX + (k === 3 ? 1.5 : 0.0);
      const holePoly = buildBore2DContour(bCfg, 0.5 * holeD + 1.8, 32, deltas[k]);
      const hN = holePoly.count;

      const botH = new Int32Array(hN), botB = new Int32Array(hN);
      const topH = new Int32Array(hN), topB = new Int32Array(hN);
      const tunB = new Int32Array(hN), tunT = new Int32Array(hN);

      for (let s = 0; s < hN; s++) {
        const aL = (TWO_PI * s) / hN;
        const dx = Math.cos(aL), dy = Math.sin(aL);
        let tBox = Infinity;
        if (dx > 1e-6) tBox = Math.min(tBox, (xR - cx) / dx);
        if (dx < -1e-6) tBox = Math.min(tBox, (xL - cx) / dx);
        if (dy > 1e-6) tBox = Math.min(tBox, halfD / dy);
        if (dy < -1e-6) {
          // Add subtle V-notch marker(s) on front -Y edge for hole index (k+1)
          let yFront = -halfD;
          const bxTest = cx + (yFront / dy) * dx;
          for (let m = 0; m <= k; m++) {
            const notchX = cx + (m - 0.5 * k) * 1.8;
            const distN = Math.abs(bxTest - notchX);
            if (distN < 0.65) yFront += (0.65 - distN) * 0.9;
          }
          tBox = Math.min(tBox, yFront / dy);
        }

        const hx = cx + holePoly.xs[s], hy = holePoly.ys[s];
        const bx = cx + tBox * dx, by = tBox * dy;
        botH[s] = gaugeCol.addV(hx, hy, 0, 0, 0, -1, 0);
        botB[s] = gaugeCol.addV(bx, by, 0, 0, 0, -1, 0);
        topH[s] = gaugeCol.addV(hx, hy, gH, 0, 0, 1, 0);
        topB[s] = gaugeCol.addV(bx, by, gH, 0, 0, 1, 0);
        tunB[s] = gaugeCol.addV(hx, hy, 0, -dx, -dy, 0, 0);
        tunT[s] = gaugeCol.addV(hx, hy, gH, -dx, -dy, 0, 0);

        // Outer box side walls where ray hits strip exterior
        const sn = (s + 1) % hN;
        const aLn = (TWO_PI * sn) / hN;
        const dxn = Math.cos(aLn), dyn = Math.sin(aLn);
        let tBoxN = Infinity;
        if (dxn > 1e-6) tBoxN = Math.min(tBoxN, (xR - cx) / dxn);
        if (dxn < -1e-6) tBoxN = Math.min(tBoxN, (xL - cx) / dxn);
        if (dyn > 1e-6) tBoxN = Math.min(tBoxN, halfD / dyn);
        if (dyn < -1e-6) {
          let yFrontN = -halfD;
          const bxTestN = cx + (yFrontN / dyn) * dxn;
          for (let m = 0; m <= k; m++) {
            const notchX = cx + (m - 0.5 * k) * 1.8;
            const distN = Math.abs(bxTestN - notchX);
            if (distN < 0.65) yFrontN += (0.65 - distN) * 0.9;
          }
          tBoxN = Math.min(tBoxN, yFrontN / dyn);
        }
        const bxN = cx + tBoxN * dxn, byN = tBoxN * dyn;
        const isExtWall =
          (Math.abs(by - halfD) < 0.05 && Math.abs(byN - halfD) < 0.05) ||
          (by < -halfD + 0.9 && byN < -halfD + 0.9) ||
          (k === 0 && Math.abs(bx - xL) < 0.05 && Math.abs(bxN - xL) < 0.05) ||
          (k === 3 && Math.abs(bx - xR) < 0.05 && Math.abs(bxN - xR) < 0.05);
        if (isExtWall) {
          const etx = bxN - bx, ety = byN - by;
          const etl = Math.hypot(etx, ety) || 1.0;
          const w0 = gaugeCol.addV(bx, by, 0, ety / etl, -etx / etl, 0, 0);
          const w1 = gaugeCol.addV(bxN, byN, 0, ety / etl, -etx / etl, 0, 0);
          const w2 = gaugeCol.addV(bxN, byN, gH, ety / etl, -etx / etl, 0, 0);
          const w3 = gaugeCol.addV(bx, by, gH, ety / etl, -etx / etl, 0, 0);
          gaugeCol.addTri(w0, w1, w2);
          gaugeCol.addTri(w0, w2, w3);
        }
      }

      for (let s = 0; s < hN; s++) {
        const j = (s + 1) % hN;
        gaugeCol.addTri(botH[s], botB[j], botB[s]);
        gaugeCol.addTri(botH[s], botH[j], botB[j]);
        gaugeCol.addTri(topH[s], topB[s], topB[j]);
        gaugeCol.addTri(topH[s], topB[j], topH[j]);
        gaugeCol.addTri(tunB[s], tunT[s], tunT[j]);
        gaugeCol.addTri(tunB[s], tunT[j], tunB[j]);
      }
    }

    return { jig: jigCol, gauge: gaugeCol, rPad: rPad, stripHalfW: halfW, stripHalfD: halfD };
  }

  // ==========================================================================
  // 8. WebGL2 3D Viewport Engine (Rigid-Body Instanced Transforms + 3D Force Vectors)
  // ==========================================================================
  let gl = null;
  let isWebGL2 = false;
  let meshProg = null;
  let lineProg = null;
  let bedBuffer = null;
  let bedVertCount = 0;
  let dynLineBuffer = null;
  const gpuParts = {};

  const camera = {
    yaw: -0.72,
    pitch: 0.56,
    distance: 155.0,
    target: [0.0, 0.0, 6.0]
  };

  function mat4Identity() {
    const m = new Float32Array(16);
    m[0] = 1; m[5] = 1; m[10] = 1; m[15] = 1;
    return m;
  }

  function mat4Multiply(a, b) {
    const out = new Float32Array(16);
    for (let col = 0; col < 4; col++) {
      const b0 = b[col * 4], b1 = b[col * 4 + 1], b2 = b[col * 4 + 2], b3 = b[col * 4 + 3];
      out[col * 4]     = a[0] * b0 + a[4] * b1 + a[8]  * b2 + a[12] * b3;
      out[col * 4 + 1] = a[1] * b0 + a[5] * b1 + a[9]  * b2 + a[13] * b3;
      out[col * 4 + 2] = a[2] * b0 + a[6] * b1 + a[10] * b2 + a[14] * b3;
      out[col * 4 + 3] = a[3] * b0 + a[7] * b1 + a[11] * b2 + a[15] * b3;
    }
    return out;
  }

  function mat4TranslateRotateZ(tx, ty, tz, rotRad) {
    const c = Math.cos(rotRad), s = Math.sin(rotRad);
    const m = mat4Identity();
    m[0] = c;  m[4] = -s; m[12] = tx;
    m[1] = s;  m[5] = c;  m[13] = ty;
    m[14] = tz;
    return m;
  }

  function mat4Perspective(fovyRad, aspect, near, far) {
    const f = 1.0 / Math.tan(0.5 * fovyRad);
    const nf = 1.0 / (near - far);
    const out = new Float32Array(16);
    out[0] = f / Math.max(aspect, 0.05);
    out[5] = f;
    out[10] = (far + near) * nf;
    out[11] = -1.0;
    out[14] = (2.0 * far * near) * nf;
    return out;
  }

  function mat4LookAtZUp(eye, center) {
    let fx = center[0] - eye[0], fy = center[1] - eye[1], fz = center[2] - eye[2];
    const fl = Math.hypot(fx, fy, fz) || 1.0;
    fx /= fl; fy /= fl; fz /= fl;

    let upX = 0.0, upY = 0.0, upZ = 1.0;
    if (Math.abs(fz) > 0.998) { upY = 1.0; upZ = 0.0; }

    let sx = fy * upZ - fz * upY;
    let sy = fz * upX - fx * upZ;
    let sz = fx * upY - fy * upX;
    const sl = Math.hypot(sx, sy, sz) || 1.0;
    sx /= sl; sy /= sl; sz /= sl;

    const ux = sy * fz - sz * fy;
    const uy = sz * fx - sx * fz;
    const uz = sx * fy - sy * fx;

    const out = mat4Identity();
    out[0] = sx;  out[4] = sy;  out[8]  = sz;  out[12] = -(sx * eye[0] + sy * eye[1] + sz * eye[2]);
    out[1] = ux;  out[5] = uy;  out[9]  = uz;  out[13] = -(ux * eye[0] + uy * eye[1] + uz * eye[2]);
    out[2] = -fx; out[6] = -fy; out[10] = -fz; out[14] = (fx * eye[0] + fy * eye[1] + fz * eye[2]);
    return out;
  }

  function compileProgram(glCtx, vsSrc, fsSrc) {
    const vs = glCtx.createShader(glCtx.VERTEX_SHADER);
    glCtx.shaderSource(vs, vsSrc);
    glCtx.compileShader(vs);
    if (!glCtx.getShaderParameter(vs, glCtx.COMPILE_STATUS)) return null;
    const fs = glCtx.createShader(glCtx.FRAGMENT_SHADER);
    glCtx.shaderSource(fs, fsSrc);
    glCtx.compileShader(fs);
    if (!glCtx.getShaderParameter(fs, glCtx.COMPILE_STATUS)) return null;
    const prog = glCtx.createProgram();
    glCtx.attachShader(prog, vs);
    glCtx.attachShader(prog, fs);
    glCtx.linkProgram(prog);
    if (!glCtx.getProgramParameter(prog, glCtx.LINK_STATUS)) return null;
    return prog;
  }

  function initWebGLViewport() {
    const canvas = document.getElementById("gl-canvas");
    if (!canvas || !canvas.getContext) return;

    gl = canvas.getContext("webgl2", { antialias: true, alpha: false, depth: true });
    if (gl) {
      isWebGL2 = true;
    } else {
      gl = canvas.getContext("webgl", { antialias: true, alpha: false, depth: true });
      isWebGL2 = false;
      if (gl) gl.getExtension("OES_element_index_uint");
    }
    if (!gl) return;

    const vsMesh300 = `#version 300 es
      precision highp float;
      in vec3 a_pos;
      in vec3 a_nrm;
      in float a_ovh;
      uniform mat4 u_vp;
      uniform mat4 u_model;
      out vec3 v_pos;
      out vec3 v_nrm;
      out float v_ovh;
      void main() {
        vec4 wp = u_model * vec4(a_pos, 1.0);
        v_pos = wp.xyz;
        v_nrm = mat3(u_model) * a_nrm;
        v_ovh = a_ovh;
        gl_Position = u_vp * wp;
      }
    `;

    const fsMesh300 = `#version 300 es
      precision highp float;
      in vec3 v_pos;
      in vec3 v_nrm;
      in float v_ovh;
      uniform vec3 u_eye;
      uniform vec3 u_albedo;
      uniform float u_roughness;
      uniform float u_metallic;
      uniform float u_heatmap;
      uniform float u_jamPulse;
      uniform float u_clipMode;
      uniform float u_clipVal;
      out vec4 outColor;

      vec3 heatmapColor(float deg) {
        vec3 safeA = vec3(0.04, 0.78, 0.44);
        vec3 safeB = vec3(0.18, 0.86, 0.42);
        vec3 warn  = vec3(1.00, 0.69, 0.02);
        vec3 crit  = vec3(0.98, 0.20, 0.16);
        if (deg <= 45.0) return mix(safeA, safeB, clamp(deg / 45.0, 0.0, 1.0));
        if (deg <= 55.0) return mix(warn, crit, (deg - 45.0) / 10.0);
        return crit;
      }

      void main() {
        if (u_clipMode > 0.5 && u_clipMode < 1.5 && v_pos.z > u_clipVal) discard;
        if (u_clipMode > 1.5 && v_pos.y < u_clipVal) discard;

        vec3 N = normalize(v_nrm);
        bool backFace = !gl_FrontFacing;
        if (backFace) N = -N;

        vec3 V = normalize(u_eye - v_pos);
        vec3 albedo = u_heatmap > 0.5 ? heatmapColor(v_ovh) : u_albedo;
        if (u_jamPulse > 0.01) {
          albedo = mix(albedo, vec3(0.98, 0.20, 0.22), u_jamPulse * 0.42);
        }
        if (backFace && u_clipMode > 0.5) {
          albedo = mix(albedo, vec3(1.0, 0.72, 0.24), 0.55);
        }

        float layerSheen = 0.988 + 0.012 * sin(v_pos.z * 31.4159);
        albedo *= layerSheen;

        vec3 L1 = normalize(vec3(-0.48, -0.62, 0.62));
        vec3 L2 = normalize(vec3(0.66, -0.22, 0.48));
        vec3 L3 = normalize(vec3(0.08, 0.84, 0.36));

        float d1 = max(dot(N, L1), 0.0);
        float d2 = max(dot(N, L2), 0.0);
        float d3 = max(dot(N, L3), 0.0);

        vec3 H1 = normalize(L1 + V);
        float shininess = mix(92.0, 18.0, u_roughness);
        float spec = pow(max(dot(N, H1), 0.0), shininess) * mix(0.28, 0.85, 1.0 - u_roughness);

        float hemi = 0.5 + 0.5 * N.z;
        vec3 ambient = mix(vec3(0.15, 0.17, 0.22), vec3(0.35, 0.38, 0.44), hemi);
        float rim = pow(1.0 - max(dot(N, V), 0.0), 3.0) * 0.22;

        vec3 specTint = mix(vec3(1.0), albedo, u_metallic);
        vec3 col = albedo * (ambient + 0.78 * d1 + 0.32 * d2 + 0.22 * d3)
                 + specTint * spec
                 + vec3(0.55, 0.84, 0.88) * rim;
        outColor = vec4(pow(clamp(col, 0.0, 1.0), vec3(0.93)), 1.0);
      }
    `;

    const vsLine300 = `#version 300 es
      precision highp float;
      in vec3 a_pos;
      uniform mat4 u_mvp;
      void main() { gl_Position = u_mvp * vec4(a_pos, 1.0); }
    `;

    const fsLine300 = `#version 300 es
      precision highp float;
      uniform vec4 u_color;
      out vec4 outColor;
      void main() { outColor = u_color; }
    `;

    const vsMesh100 = `
      precision highp float;
      attribute vec3 a_pos;
      attribute vec3 a_nrm;
      attribute float a_ovh;
      uniform mat4 u_vp;
      uniform mat4 u_model;
      varying vec3 v_pos;
      varying vec3 v_nrm;
      varying float v_ovh;
      void main() {
        vec4 wp = u_model * vec4(a_pos, 1.0);
        v_pos = wp.xyz;
        v_nrm = mat3(u_model) * a_nrm;
        v_ovh = a_ovh;
        gl_Position = u_vp * wp;
      }
    `;

    const fsMesh100 = `
      precision highp float;
      varying vec3 v_pos;
      varying vec3 v_nrm;
      varying float v_ovh;
      uniform vec3 u_eye;
      uniform vec3 u_albedo;
      uniform float u_heatmap;
      uniform float u_jamPulse;
      uniform float u_clipMode;
      uniform float u_clipVal;
      vec3 heatmapColor(float deg) {
        if (deg <= 45.0) return vec3(0.08, 0.80, 0.44);
        if (deg <= 55.0) return vec3(1.00, 0.68, 0.02);
        return vec3(0.98, 0.20, 0.16);
      }
      void main() {
        if (u_clipMode > 0.5 && u_clipMode < 1.5 && v_pos.z > u_clipVal) discard;
        if (u_clipMode > 1.5 && v_pos.y < u_clipVal) discard;
        vec3 N = normalize(v_nrm);
        if (!gl_FrontFacing) N = -N;
        vec3 V = normalize(u_eye - v_pos);
        vec3 alb = u_heatmap > 0.5 ? heatmapColor(v_ovh) : u_albedo;
        if (u_jamPulse > 0.01) alb = mix(alb, vec3(0.98, 0.20, 0.22), u_jamPulse * 0.42);
        vec3 L1 = normalize(vec3(-0.48, -0.62, 0.62));
        float diff = max(dot(N, L1), 0.0);
        vec3 H = normalize(L1 + V);
        float spec = pow(max(dot(N, H), 0.0), 42.0) * 0.38;
        gl_FragColor = vec4(alb * (0.32 + 0.76 * diff) + vec3(spec), 1.0);
      }
    `;

    const vsLine100 = `
      precision highp float;
      attribute vec3 a_pos;
      uniform mat4 u_mvp;
      void main() { gl_Position = u_mvp * vec4(a_pos, 1.0); }
    `;

    const fsLine100 = `
      precision highp float;
      uniform vec4 u_color;
      void main() { gl_FragColor = u_color; }
    `;

    meshProg = compileProgram(gl, isWebGL2 ? vsMesh300 : vsMesh100, isWebGL2 ? fsMesh300 : fsMesh100);
    lineProg = compileProgram(gl, isWebGL2 ? vsLine300 : vsLine100, isWebGL2 ? fsLine300 : fsLine100);
    bedBuffer = gl.createBuffer();
    dynLineBuffer = gl.createBuffer();

    rebuildBedGeometry();
    bindViewportEvents(canvas);
  }

  function ensurePartGPU(key) {
    if (!gpuParts[key] && gl) {
      gpuParts[key] = {
        pos: gl.createBuffer(),
        nrm: gl.createBuffer(),
        ovh: gl.createBuffer(),
        idx: gl.createBuffer(),
        wire: gl.createBuffer(),
        indexCount: 0,
        indexType: 0,
        wireCount: 0
      };
    }
    return gpuParts[key];
  }

  function uploadCollectorToPart(key, col) {
    if (!gl) return;
    const part = ensurePartGPU(key);
    const usage = state.isInteracting ? gl.DYNAMIC_DRAW : gl.STATIC_DRAW;

    const posArr = new Float32Array(col.pos);
    const nrmArr = new Float32Array(col.nrm);
    const ovhArr = new Float32Array(col.ovh);
    const wireArr = new Float32Array(col.wire);

    gl.bindBuffer(gl.ARRAY_BUFFER, part.pos);
    gl.bufferData(gl.ARRAY_BUFFER, posArr, usage);
    gl.bindBuffer(gl.ARRAY_BUFFER, part.nrm);
    gl.bufferData(gl.ARRAY_BUFFER, nrmArr, usage);
    gl.bindBuffer(gl.ARRAY_BUFFER, part.ovh);
    gl.bufferData(gl.ARRAY_BUFFER, ovhArr, usage);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, part.idx);
    if (isWebGL2 || posArr.length / 3 > 65530) {
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint32Array(col.idx), usage);
      part.indexType = gl.UNSIGNED_INT;
    } else {
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(col.idx), usage);
      part.indexType = gl.UNSIGNED_SHORT;
    }
    part.indexCount = col.idx.length;

    gl.bindBuffer(gl.ARRAY_BUFFER, part.wire);
    gl.bufferData(gl.ARRAY_BUFFER, wireArr, usage);
    part.wireCount = wireArr.length / 3;
  }

  function rebuildBedGeometry() {
    if (!gl || !bedBuffer) return;
    const bx = Math.max(80, Number(state.printer.bed_x) || 220);
    const by = Math.max(80, Number(state.printer.bed_y) || 220);
    const hx = 0.5 * bx, hy = 0.5 * by;
    const verts = [];
    const step = 20;
    for (let x = -Math.floor(hx / step) * step; x <= hx + 0.01; x += step) {
      verts.push(x, -hy, -0.06, x, hy, -0.06);
    }
    for (let y = -Math.floor(hy / step) * step; y <= hy + 0.01; y += step) {
      verts.push(-hx, y, -0.06, hx, y, -0.06);
    }
    verts.push(
      -hx, -hy, 0.02, hx, -hy, 0.02,
      hx, -hy, 0.02, hx, hy, 0.02,
      hx, hy, 0.02, -hx, hy, 0.02,
      -hx, hy, 0.02, -hx, -hy, 0.02,
      -18, -hy - 3.5, 0.02, 18, -hy - 3.5, 0.02
    );
    const arr = new Float32Array(verts);
    bedVertCount = arr.length / 3;
    gl.bindBuffer(gl.ARRAY_BUFFER, bedBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, arr, gl.STATIC_DRAW);
  }

  function append3DArrowLines(arr, ox, oy, oz, dx, dy, dz, lengthMm) {
    if (lengthMm < 0.8) return;
    const dl = Math.hypot(dx, dy, dz) || 1.0;
    const ux = dx / dl, uy = dy / dl, uz = dz / dl;
    const ex = ox + ux * lengthMm, ey = oy + uy * lengthMm, ez = oz + uz * lengthMm;
    arr.push(ox, oy, oz, ex, ey, ez);

    // Build two perpendicular wing vectors for crisp 3D arrowhead
    let px = -uy, py = ux, pz = 0.0;
    if (Math.hypot(px, py) < 0.15) { px = 1.0; py = 0.0; pz = 0.0; }
    const pl = Math.hypot(px, py, pz) || 1.0;
    px /= pl; py /= pl; pz /= pl;
    const qx = uy * pz - uz * py, qy = uz * px - ux * pz, qz = ux * py - uy * px;

    const headLen = Math.min(4.8, 0.26 * lengthMm);
    const headRad = 0.45 * headLen;
    const bx = ex - ux * headLen, by = ey - uy * headLen, bz = ez - uz * headLen;
    arr.push(
      ex, ey, ez, bx + px * headRad, by + py * headRad, bz + pz * headRad,
      ex, ey, ez, bx - px * headRad, by - py * headRad, bz - pz * headRad,
      ex, ey, ez, bx + qx * headRad, by + qy * headRad, bz + qz * headRad,
      ex, ey, ez, bx - qx * headRad, by - qy * headRad, bz - qz * headRad
    );
  }

  function drawDynamicLines(vpMat, coords, r, g, b, a) {
    if (!gl || !lineProg || !coords.length) return;
    const arr = new Float32Array(coords);
    gl.useProgram(lineProg);
    gl.uniformMatrix4fv(gl.getUniformLocation(lineProg, "u_mvp"), false, vpMat);
    gl.uniform4f(gl.getUniformLocation(lineProg, "u_color"), r, g, b, a);
    const loc = gl.getAttribLocation(lineProg, "a_pos");
    gl.bindBuffer(gl.ARRAY_BUFFER, dynLineBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, arr, gl.DYNAMIC_DRAW);
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 3, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.LINES, 0, arr.length / 3);
  }

  function drawPartInstance(vpMat, eye, partKey, modelMat, albedo, rough, metal, jamPulse) {
    const part = gpuParts[partKey];
    if (!part || part.indexCount <= 0) return;

    gl.useProgram(meshProg);
    gl.uniformMatrix4fv(gl.getUniformLocation(meshProg, "u_vp"), false, vpMat);
    gl.uniformMatrix4fv(gl.getUniformLocation(meshProg, "u_model"), false, modelMat);
    gl.uniform3fv(gl.getUniformLocation(meshProg, "u_eye"), eye);
    gl.uniform3fv(gl.getUniformLocation(meshProg, "u_albedo"), albedo);
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_roughness"), rough);
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_metallic"), metal);
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_heatmap"), state.heatmap ? 1.0 : 0.0);
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_jamPulse"), jamPulse);

    const maxH = state.params.face_width_mm + Math.max(
      state.params.pinion.hub_enabled ? state.params.pinion.hub_height_mm : 0,
      state.params.gear.hub_enabled ? state.params.gear.hub_height_mm : 0
    ) + 2.0;
    const maxY = Math.max(state.geom.pinion.tip_radius_mm, state.geom.gear.tip_radius_mm) + 15.0;

    let clipMode = 0.0;
    let clipVal = 9999.0;
    if (state.crossCutPct > 0) {
      if (state.crossCutAxis === "z") {
        clipMode = 1.0;
        clipVal = maxH * (1.0 - (state.crossCutPct / 105.0));
      } else {
        clipMode = 2.0;
        clipVal = maxY * (1.0 - 2.0 * (state.crossCutPct / 100.0));
      }
    }
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_clipMode"), clipMode);
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_clipVal"), clipVal);

    const locPos = gl.getAttribLocation(meshProg, "a_pos");
    const locNrm = gl.getAttribLocation(meshProg, "a_nrm");
    const locOvh = gl.getAttribLocation(meshProg, "a_ovh");

    gl.bindBuffer(gl.ARRAY_BUFFER, part.pos);
    gl.enableVertexAttribArray(locPos);
    gl.vertexAttribPointer(locPos, 3, gl.FLOAT, false, 0, 0);

    if (locNrm >= 0) {
      gl.bindBuffer(gl.ARRAY_BUFFER, part.nrm);
      gl.enableVertexAttribArray(locNrm);
      gl.vertexAttribPointer(locNrm, 3, gl.FLOAT, false, 0, 0);
    }
    if (locOvh >= 0) {
      gl.bindBuffer(gl.ARRAY_BUFFER, part.ovh);
      gl.enableVertexAttribArray(locOvh);
      gl.vertexAttribPointer(locOvh, 1, gl.FLOAT, false, 0, 0);
    }

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, part.idx);
    gl.drawElements(gl.TRIANGLES, part.indexCount, part.indexType, 0);

    if (state.wireframe && part.wireCount > 0 && state.crossCutPct === 0) {
      const mvp = mat4Multiply(vpMat, modelMat);
      gl.useProgram(lineProg);
      gl.uniformMatrix4fv(gl.getUniformLocation(lineProg, "u_mvp"), false, mvp);
      gl.uniform4f(gl.getUniformLocation(lineProg, "u_color"), 0.0, 0.0, 0.0, 0.35);
      const locL = gl.getAttribLocation(lineProg, "a_pos");
      gl.bindBuffer(gl.ARRAY_BUFFER, part.wire);
      gl.enableVertexAttribArray(locL);
      gl.vertexAttribPointer(locL, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.LINES, 0, part.wireCount);
    }
  }

  function renderWebGLFrame(nowMs) {
    if (!gl || !meshProg || !lineProg || !state.geom) return;
    const canvas = gl.canvas;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.max(1, Math.floor((canvas.clientWidth || 640) * dpr));
    const h = Math.max(1, Math.floor((canvas.clientHeight || 360) * dpr));
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }

    gl.viewport(0, 0, w, h);
    gl.enable(gl.DEPTH_TEST);
    gl.disable(gl.CULL_FACE);

    if (state.theme === "light") gl.clearColor(0.84, 0.88, 0.93, 1.0);
    else gl.clearColor(0.095, 0.11, 0.135, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    const cosP = Math.cos(camera.pitch);
    const eye = [
      camera.target[0] + camera.distance * cosP * Math.cos(camera.yaw),
      camera.target[1] + camera.distance * cosP * Math.sin(camera.yaw),
      camera.target[2] + camera.distance * Math.sin(camera.pitch)
    ];

    const proj = mat4Perspective(38.0 * DEG2RAD, w / h, 2.0, 2600.0);
    const view = mat4LookAtZUp(eye, camera.target);
    const vp = mat4Multiply(proj, view);

    // 1. Draw Printer Build Plate Grid
    if (bedVertCount > 0) {
      gl.useProgram(lineProg);
      gl.uniformMatrix4fv(gl.getUniformLocation(lineProg, "u_mvp"), false, vp);
      const fits = state.clientReport ? state.clientReport.printability.fits_bed : true;
      if (!fits) gl.uniform4f(gl.getUniformLocation(lineProg, "u_color"), 0.98, 0.26, 0.26, 0.82);
      else if (state.theme === "light") gl.uniform4f(gl.getUniformLocation(lineProg, "u_color"), 0.34, 0.44, 0.54, 0.45);
      else gl.uniform4f(gl.getUniformLocation(lineProg, "u_color"), 0.0, 0.72, 0.62, 0.30);

      const locL = gl.getAttribLocation(lineProg, "a_pos");
      gl.bindBuffer(gl.ARRAY_BUFFER, bedBuffer);
      gl.enableVertexAttribArray(locL);
      gl.vertexAttribPointer(locL, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.LINES, 0, bedVertCount);
    }

    const g = state.geom;
    const p = state.params;
    const a = g.center_distance_mm;
    const ra1 = g.pinion.tip_radius_mm;
    const ra2 = g.gear.tip_radius_mm;
    const theta1 = state.theta1Rad;
    const theta2 = g.mesh_phase_g2_rad - theta1 * (g.pinion.teeth / g.gear.teeth);

    const isJammed = Boolean((state.clientReport && state.clientReport.fit.jammed) || state.liveCollision.collided);
    const jamPulse = isJammed ? (0.45 + 0.55 * Math.abs(Math.sin((nowMs || 0) * 0.007))) : 0.0;

    // Distinct CAD engineering colors: Pinion G1 = Orca Teal (#00bfa5), Gear G2 = Precision Steel Blue (#4f9cf9)
    const colG1 = [0.02, 0.74, 0.64];
    const colG2 = [0.31, 0.61, 0.96];
    const colJig = [0.38, 0.43, 0.50];
    const colGauge = [0.85, 0.62, 0.16];

    if (state.vpView === "meshed") {
      // Center pair bounding box on build plate
      const x1 = -0.5 * (a + ra2 - ra1);
      const x2 = x1 + a;

      // Subtle mechanical judder when jammed & playing
      const judder = (isJammed && state.simPlaying) ? (0.015 * Math.sin((nowMs || 0) * 0.06)) : 0.0;

      const m1 = mat4TranslateRotateZ(x1, 0.0, 0.0, theta1 + judder);
      const m2 = mat4TranslateRotateZ(x2, 0.0, 0.0, theta2 - judder);

      drawPartInstance(vp, eye, "pinion", m1, colG1, 0.28, 0.35, jamPulse);
      drawPartInstance(vp, eye, "gear", m2, colG2, 0.30, 0.42, jamPulse);

      // 3D Force Vector Arrows (Ft, Fr, Fa) at the Pitch Contact Point!
      if (state.showForces && state.clientReport) {
        const kin = state.clientReport.kinematics;
        const px = x1 + g.pinion.working_pitch_radius_mm;
        const py = 0.0;
        const pz = 0.5 * p.face_width_mm;
        const dirSgn = p.sim_direction === "cw" ? -1.0 : 1.0;

        const baseScale = Math.max(10.0, Math.min(34.0, 0.42 * (ra1 + ra2)));
        const ftLen = baseScale;
        const frLen = Math.max(4.0, ftLen * Math.tan(state.clientReport.loa.alphaWRad));

        const ftLines = [];
        append3DArrowLines(ftLines, px, py, pz, 0.0, dirSgn, 0.0, ftLen);
        drawDynamicLines(vp, ftLines, 0.05, 0.92, 0.65, 1.0); // Emerald Ft

        const frLines = [];
        append3DArrowLines(frLines, px, py, pz, 1.0, 0.0, 0.0, frLen);
        drawDynamicLines(vp, frLines, 1.0, 0.72, 0.12, 1.0); // Gold Fr

        if (p.gear_type === "helical" && g.beta_deg > 0.2) {
          const faLen = Math.min(42.0, ftLen * Math.tan(g.beta_rad));
          const handSgn = p.helix_hand === "right" ? 1.0 : -1.0;
          const faLines = [];
          append3DArrowLines(faLines, px, py, pz, 0.0, 0.0, dirSgn * handSgn, faLen);
          drawDynamicLines(vp, faLines, 0.98, 0.32, 0.58, 1.0); // Magenta Axial Thrust Fa!
        } else if (p.gear_type === "herringbone" && g.beta_deg > 0.2) {
          // Balanced opposing V-thrust arrows canceling at mid-plane z = b/2!
          const halfZ = 0.46 * p.face_width_mm;
          const hbLines = [];
          append3DArrowLines(hbLines, px, py + 2.5, p.face_width_mm + 4.0, 0.0, 0.0, -1.0, Math.max(4.5, halfZ * 0.75));
          append3DArrowLines(hbLines, px, py + 2.5, -4.0, 0.0, 0.0, 1.0, Math.max(4.5, halfZ * 0.75));
          drawDynamicLines(vp, hbLines, 0.20, 0.90, 0.48, 0.95); // Balanced green opposing arrows
        }
      }
    } else if (state.vpView === "fit_kit") {
      // Interactive 4-piece Fit-Test Kit mounted on 2-pin jig + Bore Gauge in front!
      const osc = Math.sin(theta1 * 2.0) * (1.25 / Math.max(6, g.pinion.teeth)) * Math.PI;
      const oscG2 = g.mesh_phase_g2_rad - osc * (g.pinion.teeth / g.gear.teeth);
      const jigY = 10.0;
      const gaugeY = -18.0;

      drawPartInstance(vp, eye, "jig_base", mat4TranslateRotateZ(0.0, jigY, 0.0, 0.0), colJig, 0.45, 0.25, 0.0);
      drawPartInstance(vp, eye, "sector_pinion", mat4TranslateRotateZ(-0.5 * a, jigY, 3.05, osc), colG1, 0.28, 0.35, jamPulse);
      drawPartInstance(vp, eye, "sector_gear", mat4TranslateRotateZ(0.5 * a, jigY, 3.05, oscG2), colG2, 0.30, 0.42, jamPulse);
      drawPartInstance(vp, eye, "bore_gauge", mat4TranslateRotateZ(0.0, gaugeY, 0.0, 0.0), colGauge, 0.38, 0.22, 0.0);
    } else {
      // "plater" view: shows exact print-ready separated layout matching `export_target`
      const target = p.export_target;
      const gap = 8.0;
      if (target === "pinion_only") {
        drawPartInstance(vp, eye, "pinion", mat4TranslateRotateZ(0, 0, 0, 0), colG1, 0.28, 0.35, 0);
      } else if (target === "gear_only") {
        drawPartInstance(vp, eye, "gear", mat4TranslateRotateZ(0, 0, 0, 0), colG2, 0.30, 0.42, 0);
      } else if (target === "fit_test_kit") {
        drawPartInstance(vp, eye, "jig_base", mat4TranslateRotateZ(0, 22, 0, 0), colJig, 0.45, 0.25, 0);
        drawPartInstance(vp, eye, "sector_pinion", mat4TranslateRotateZ(-26, -12, 0, 0), colG1, 0.28, 0.35, 0);
        drawPartInstance(vp, eye, "sector_gear", mat4TranslateRotateZ(26, -12, 0, 0), colG2, 0.30, 0.42, 0);
        drawPartInstance(vp, eye, "bore_gauge", mat4TranslateRotateZ(0, -44, 0, 0), colGauge, 0.38, 0.22, 0);
      } else if (target === "full_suite") {
        const totW = 2 * ra1 + gap + 2 * ra2;
        const x1 = -0.5 * totW + ra1;
        const x2 = 0.5 * totW - ra2;
        const yOff = Math.max(ra1, ra2) * 0.45 + 12.0;
        drawPartInstance(vp, eye, "pinion", mat4TranslateRotateZ(x1, yOff, 0, 0), colG1, 0.28, 0.35, 0);
        drawPartInstance(vp, eye, "gear", mat4TranslateRotateZ(x2, yOff, 0, 0), colG2, 0.30, 0.42, 0);
        drawPartInstance(vp, eye, "jig_base", mat4TranslateRotateZ(-28, -yOff - 14, 0, 0), colJig, 0.45, 0.25, 0);
        drawPartInstance(vp, eye, "bore_gauge", mat4TranslateRotateZ(36, -yOff - 14, 0, 0), colGauge, 0.38, 0.22, 0);
      } else {
        // pair_separated
        const totW = 2 * ra1 + gap + 2 * ra2;
        const x1 = -0.5 * totW + ra1;
        const x2 = 0.5 * totW - ra2;
        drawPartInstance(vp, eye, "pinion", mat4TranslateRotateZ(x1, 0, 0, 0), colG1, 0.28, 0.35, 0);
        drawPartInstance(vp, eye, "gear", mat4TranslateRotateZ(x2, 0, 0, 0), colG2, 0.30, 0.42, 0);
      }
    }
  }

  function fitCameraToScene() {
    if (!state.geom) return;
    const ra1 = state.geom.pinion.tip_radius_mm;
    const ra2 = state.geom.gear.tip_radius_mm;
    const a = state.geom.center_distance_mm;
    const b = state.params.face_width_mm;
    const spanXY = Math.max(a + ra1 + ra2, 55.0);
    camera.target = [0.0, 0.0, b * 0.45];
    camera.distance = Math.max(85.0, Math.min(950.0, spanXY * 1.65 + b * 1.2));
    requestRender();
  }

  function bindViewportEvents(canvas) {
    let dragging = false;
    let panMode = false;
    let lastX = 0, lastY = 0;

    canvas.addEventListener("contextmenu", function (e) { e.preventDefault(); });
    canvas.addEventListener("pointerdown", function (e) {
      dragging = true;
      panMode = (e.button === 1 || e.button === 2 || e.shiftKey);
      lastX = e.clientX;
      lastY = e.clientY;
      canvas.setPointerCapture?.(e.pointerId);
    });
    canvas.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      const dx = e.clientX - lastX;
      const dy = e.clientY - lastY;
      lastX = e.clientX;
      lastY = e.clientY;

      if (panMode) {
        const panScale = camera.distance * 0.0014;
        const rx = -Math.sin(camera.yaw), ry = Math.cos(camera.yaw);
        camera.target[0] -= dx * rx * panScale;
        camera.target[1] -= dx * ry * panScale;
        camera.target[2] += dy * panScale;
      } else {
        camera.yaw -= dx * 0.0085;
        camera.pitch = Math.max(-1.48, Math.min(1.48, camera.pitch + dy * 0.0075));
      }
      requestRender();
    });
    const endDrag = function (e) {
      dragging = false;
      canvas.releasePointerCapture?.(e.pointerId);
    };
    canvas.addEventListener("pointerup", endDrag);
    canvas.addEventListener("pointercancel", endDrag);

    canvas.addEventListener("wheel", function (e) {
      e.preventDefault();
      camera.distance = Math.max(35.0, Math.min(1200.0, camera.distance * Math.exp(e.deltaY * 0.0011)));
      requestRender();
    }, { passive: false });

    canvas.addEventListener("dblclick", fitCameraToScene);

    if (typeof ResizeObserver !== "undefined") {
      const ro = new ResizeObserver(function () {
        requestRender();
        draw2DLoupe(performance.now());
      });
      ro.observe(canvas);
    }
  }

  // ==========================================================================
  // 9. Synchronized High-DPI 2D Tooth-Mesh Loupe (`#loupe-canvas`)
  // ==========================================================================
  function draw2DLoupe(nowMs) {
    if (state.loupeCollapsed) return;
    const canvas = document.getElementById("loupe-canvas");
    if (!canvas || !canvas.getContext || !state.geom || !state.contourG1 || !state.contourG2) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const w = canvas.clientWidth || 640;
    const h = canvas.clientHeight || 168;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const cw = Math.max(1, Math.floor(w * dpr));
    const ch = Math.max(1, Math.floor(h * dpr));
    if (canvas.width !== cw || canvas.height !== ch) {
      canvas.width = cw;
      canvas.height = ch;
    }

    const g = state.geom;
    const p = state.params;
    const rep = state.clientReport;
    const a = g.center_distance_mm;
    const rw1 = g.pinion.working_pitch_radius_mm;
    const rw2 = g.gear.working_pitch_radius_mm;
    const rb1 = g.pinion.base_radius_mm;
    const rb2 = g.gear.base_radius_mm;

    const theta1 = state.theta1Rad;
    const theta2 = g.mesh_phase_g2_rad - theta1 * (g.pinion.teeth / g.gear.teeth);

    // Live exact 2D meshing window collision & clearance check
    state.liveCollision = checkLive2DMeshCollision(
      state.contourG1,
      state.contourG2,
      theta1,
      theta2,
      a,
      g.m_n,
      g.pinion.pitch_radius_mm
    );
    const isJammed = Boolean(state.liveCollision.collided || (rep && rep.fit.jammed));
    const jamBadge = document.getElementById("loupe-jam-badge");
    if (jamBadge) jamBadge.classList.toggle("visible", isJammed);

    ctx.save();
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, w, h);

    const isLight = state.theme === "light";
    ctx.fillStyle = isLight ? "#f4f7fb" : "#14171d";
    ctx.fillRect(0, 0, w, h);

    // Coordinate transform centered right on the working Pitch Point P = (rw1, 0)!
    const cxScreen = w * 0.44;
    const cyScreen = h * 0.52;
    const viewWindowMm = Math.max(4.5 * g.m_n, 7.0) / state.loupeZoom;
    const pxPerMm = (h * 0.45) / viewWindowMm;

    const toSX = function (wx) { return cxScreen + (wx - rw1) * pxPerMm; };
    const toSY = function (wy) { return cyScreen - wy * pxPerMm; };

    // Subtle engineering grid in mm around pitch point
    const gridStepMm = g.m_n >= 2.0 ? 2.0 : 1.0;
    ctx.strokeStyle = isLight ? "rgba(60, 80, 110, 0.09)" : "rgba(255, 255, 255, 0.05)";
    ctx.lineWidth = 1;
    const spanXMm = (w / pxPerMm) * 0.65;
    for (let gx = Math.floor((rw1 - spanXMm) / gridStepMm) * gridStepMm; gx <= rw1 + spanXMm; gx += gridStepMm) {
      const sx = toSX(gx);
      ctx.beginPath(); ctx.moveTo(sx, 0); ctx.lineTo(sx, h); ctx.stroke();
    }
    for (let gy = -Math.ceil(viewWindowMm * 1.4 / gridStepMm) * gridStepMm; gy <= viewWindowMm * 1.4; gy += gridStepMm) {
      const sy = toSY(gy);
      ctx.beginPath(); ctx.moveTo(0, sy); ctx.lineTo(w, sy); ctx.stroke();
    }

    // Centerline O1 -> O2
    ctx.save();
    ctx.strokeStyle = isLight ? "rgba(80, 100, 125, 0.25)" : "rgba(255, 255, 255, 0.14)";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, cyScreen);
    ctx.lineTo(w, cyScreen);
    ctx.stroke();
    ctx.restore();

    // Draw Gear 1 (Teal) and Gear 2 (Steel Blue) exact 2D involute contours
    const drawContour = function (c, ox, rotRad, fillCol, strokeCol) {
      const cs = Math.cos(rotRad), sn = Math.sin(rotRad);
      ctx.beginPath();
      for (let i = 0; i < c.count; i++) {
        const wx = ox + c.xs[i] * cs - c.ys[i] * sn;
        const wy = c.xs[i] * sn + c.ys[i] * cs;
        const sx = toSX(wx), sy = toSY(wy);
        if (i === 0) ctx.moveTo(sx, sy);
        else ctx.lineTo(sx, sy);
      }
      ctx.closePath();
      ctx.fillStyle = fillCol;
      ctx.fill();
      ctx.strokeStyle = strokeCol;
      ctx.lineWidth = 1.7;
      ctx.stroke();
    };

    drawContour(
      state.contourG1,
      0.0,
      theta1,
      isJammed ? "rgba(255, 65, 65, 0.22)" : (isLight ? "rgba(0, 150, 136, 0.22)" : "rgba(0, 191, 165, 0.24)"),
      isJammed ? "#ff5252" : (isLight ? "#00796b" : "#00bfa5")
    );

    drawContour(
      state.contourG2,
      a,
      theta2,
      isJammed ? "rgba(255, 90, 65, 0.20)" : (isLight ? "rgba(37, 99, 235, 0.18)" : "rgba(79, 156, 249, 0.22)"),
      isJammed ? "#ff6e40" : (isLight ? "#1d4ed8" : "#4f9cf9")
    );

    // Dashed Working Pitch Circles (rw1, rw2) & Dotted Base Circles (rb1, rb2)
    const drawCircleArc = function (ox, rad, dash, color) {
      ctx.save();
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.1;
      ctx.setLineDash(dash);
      ctx.beginPath();
      ctx.arc(toSX(ox), toSY(0), rad * pxPerMm, 0, TWO_PI);
      ctx.stroke();
      ctx.restore();
    };
    drawCircleArc(0.0, rw1, [5, 4], isLight ? "rgba(0, 137, 123, 0.65)" : "rgba(0, 229, 195, 0.55)");
    drawCircleArc(a, rw2, [5, 4], isLight ? "rgba(37, 99, 235, 0.65)" : "rgba(110, 178, 255, 0.55)");
    drawCircleArc(0.0, rb1, [2, 3], isLight ? "rgba(0, 105, 92, 0.42)" : "rgba(0, 191, 165, 0.35)");
    drawCircleArc(a, rb2, [2, 3], isLight ? "rgba(30, 64, 175, 0.42)" : "rgba(79, 156, 249, 0.35)");

    // Tilted Pressure Line of Action & Live Moving Contact Points!
    if (rep && rep.loa) {
      const loa = rep.loa;
      const dirSign = p.sim_direction === "cw" ? -1.0 : 1.0;
      // Driving line of action unit vector u = (dirSign * sinAw, cosAw) or (-sinAw, -cosAw)
      // Check: when G1 rotates CW (theta1 decreasing, teeth move -Y at pitch point), G1 upper flank pushes -Y on G2:
      // Normal along LOA has tangent direction u = (sinAw, -cosAw) for CW and (sinAw, +cosAw) for CCW!
      const ux = Math.sin(loa.alphaWRad);
      const uy = dirSign * Math.cos(loa.alphaWRad);

      // Extended reference pressure line
      const ext = Math.max(loa.sEnd - loa.sStart, 3.0 * g.m_n) * 0.95;
      ctx.save();
      ctx.strokeStyle = isLight ? "rgba(217, 119, 6, 0.36)" : "rgba(255, 193, 7, 0.30)";
      ctx.setLineDash([3, 3]);
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(toSX(rw1 - ext * ux), toSY(-ext * uy));
      ctx.lineTo(toSX(rw1 + ext * ux), toSY(ext * uy));
      ctx.stroke();
      ctx.restore();

      // Active Contact Segment [sStart, sEnd]
      if (loa.sEnd > loa.sStart + 1e-4) {
        const sx0 = toSX(rw1 + loa.sStart * ux), sy0 = toSY(loa.sStart * uy);
        const sx1 = toSX(rw1 + loa.sEnd * ux), sy1 = toSY(loa.sEnd * uy);

        ctx.strokeStyle = isLight ? "#d97706" : "#ffc107";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(sx0, sy0);
        ctx.lineTo(sx1, sy1);
        ctx.stroke();

        // Entry & Exit limit ticks
        ctx.fillStyle = isLight ? "#d97706" : "#ffd54f";
        ctx.beginPath(); ctx.arc(sx0, sy0, 3.0, 0, TWO_PI); ctx.fill();
        ctx.beginPath(); ctx.arc(sx1, sy1, 3.0, 0, TWO_PI); ctx.fill();

        // Live Moving Contact Dots sliding along the Pressure Line of Action in exact phase!
        const pBt = loa.pBt;
        if (pBt > 1e-4 && !isJammed) {
          // Exact involute contact position along LOA for tooth k:
          // On G1, flank is at theta1 + k*(2*pi/Z1) +/- psiB1. Contact roll distance from T1 = rb1 * rollAngle
          const sBaseRef = -rw1 * Math.sin(loa.alphaWRad);
          const flankPhase = dirSign > 0
            ? (theta1 + g.pinion.base_half_angle_rad)
            : (-theta1 + g.pinion.base_half_angle_rad);
          const sPhase = rb1 * flankPhase + sBaseRef;

          const kMin = Math.floor((loa.sStart - sPhase) / pBt) - 1;
          const kMax = Math.ceil((loa.sEnd - sPhase) / pBt) + 1;
          for (let k = kMin; k <= kMax; k++) {
            const sVal = sPhase + k * pBt;
            if (sVal >= loa.sStart - 0.02 && sVal <= loa.sEnd + 0.02) {
              const cxPt = toSX(rw1 + sVal * ux);
              const cyPt = toSY(sVal * uy);
              ctx.beginPath();
              ctx.arc(cxPt, cyPt, 4.8, 0, TWO_PI);
              ctx.fillStyle = "#00e676";
              ctx.fill();
              ctx.lineWidth = 1.6;
              ctx.strokeStyle = "#ffffff";
              ctx.stroke();
            }
          }
        }
      }
    }

    // Pitch Point Crosshair P
    const pxS = toSX(rw1), pyS = toSY(0.0);
    ctx.strokeStyle = isLight ? "#111827" : "#ffffff";
    ctx.lineWidth = 1.3;
    ctx.beginPath();
    ctx.moveTo(pxS - 5, pyS); ctx.lineTo(pxS + 5, pyS);
    ctx.moveTo(pxS, pyS - 5); ctx.lineTo(pxS, pyS + 5);
    ctx.stroke();

    // Pulsing Red Collision Zone Highlights if Jammed / Overlapping!
    if (isJammed) {
      const pulseR = 7.0 + 4.5 * Math.abs(Math.sin((nowMs || 0) * 0.008));
      const pts = state.liveCollision.hitPoints.length
        ? state.liveCollision.hitPoints
        : [[rw1, 0.0]];
      for (let i = 0; i < pts.length; i++) {
        const hx = toSX(pts[i][0]), hy = toSY(pts[i][1]);
        ctx.beginPath();
        ctx.arc(hx, hy, pulseR, 0, TWO_PI);
        ctx.fillStyle = "rgba(255, 35, 35, 0.34)";
        ctx.fill();
        ctx.beginPath();
        ctx.arc(hx, hy, 3.6, 0, TWO_PI);
        ctx.fillStyle = "#ff1744";
        ctx.fill();
      }
    }

    // Right-Side Live Engineering Readout Card inside 2D Loupe
    if (rep && w >= 360) {
      const boxW = 178;
      const boxH = h - 16;
      const bx = w - boxW - 8;
      const by = 8;
      ctx.fillStyle = isLight ? "rgba(255, 255, 255, 0.88)" : "rgba(22, 25, 32, 0.86)";
      ctx.strokeStyle = isJammed ? "#ff5252" : (isLight ? "#cbd5e1" : "#323846");
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect ? ctx.roundRect(bx, by, boxW, boxH, 6) : ctx.rect(bx, by, boxW, boxH);
      ctx.fill();
      ctx.stroke();

      const lblCol = isLight ? "#64748b" : "#8b96a8";
      const valCol = isLight ? "#0f172a" : "#eef2f7";
      const rows = [
        [state.lang === "en" ? "Ratio" : "Relação", "1 : " + g.ratio.toFixed(2) + " (" + g.pinion.teeth + ":" + g.gear.teeth + ")"],
        [state.lang === "en" ? "Out Speed" : "Saída G2", rep.kinematics.rpm_g2.toFixed(1) + " RPM"],
        [state.lang === "en" ? "Contact ε_γ" : "Contato ε_γ", rep.contact.total_contact_ratio.toFixed(2) + " (εα " + rep.contact.transverse_ratio.toFixed(2) + ")"],
        [state.lang === "en" ? "Clearance" : "Folga Mín.", (isJammed ? "0.000 COLISÃO" : state.liveCollision.minDistMm.toFixed(3) + " mm")]
      ];

      const rowStep = Math.max(22, Math.floor((boxH - 10) / rows.length));
      ctx.font = "600 10px Segoe UI, sans-serif";
      for (let r = 0; r < rows.length; r++) {
        const ry = by + 16 + r * rowStep;
        ctx.fillStyle = lblCol;
        ctx.fillText(rows[r][0], bx + 8, ry);
        ctx.fillStyle = (r === 3 && isJammed) ? "#ff5252" : (r === 3 ? "#00c853" : valCol);
        ctx.font = "700 10.5px Consolas, monospace";
        const tw = ctx.measureText(rows[r][1]).width;
        ctx.fillText(rows[r][1], bx + boxW - tw - 8, ry);
        ctx.font = "600 10px Segoe UI, sans-serif";
      }
    }

    ctx.restore();
  }

  // ==========================================================================
  // 10. Animation Loop (60 FPS Micro-Simulation + Degree Scrubbing)
  // ==========================================================================
  let rafId = 0;

  function updateAngleReadoutsOnly() {
    let deg = ((state.theta1Rad * RAD2DEG) % 360.0 + 360.0) % 360.0;
    if (deg >= 359.95) deg = 0.0;
    const inp = document.getElementById("inp-sim-angle");
    const lbl = document.getElementById("lbl-sim-angle");
    if (inp && document.activeElement !== inp) inp.value = deg.toFixed(1);
    if (lbl) lbl.textContent = deg.toFixed(1) + "°";
  }

  function stepAnimation(nowMs) {
    rafId = 0;
    if (!state.lastFrameMs) state.lastFrameMs = nowMs;
    const dtSec = Math.min(0.08, Math.max(0.0, (nowMs - state.lastFrameMs) / 1000.0));
    state.lastFrameMs = nowMs;

    if (state.simPlaying) {
      const dirSign = state.params.sim_direction === "cw" ? -1.0 : 1.0;
      const omegaRadSec = (state.params.sim_rpm * TWO_PI) / 60.0;
      state.theta1Rad = (state.theta1Rad + dirSign * omegaRadSec * dtSec) % TWO_PI;
      if (state.theta1Rad < 0) state.theta1Rad += TWO_PI;
      updateAngleReadoutsOnly();
    }

    renderWebGLFrame(nowMs);
    draw2DLoupe(nowMs);

    const isJammed = Boolean((state.clientReport && state.clientReport.fit.jammed) || state.liveCollision.collided);
    if (state.simPlaying || isJammed) {
      requestRender();
    }
  }

  function requestRender() {
    if (rafId || typeof requestAnimationFrame === "undefined") return;
    rafId = requestAnimationFrame(stepAnimation);
  }

  // ==========================================================================
  // 11. Scene Rebuild, Dual Badges, Presets & Diagnostics Sync
  // ==========================================================================
  function recomputeKinematicsAndLoupeOnly() {
    state.geom = computeGearPairGeometry(state.params);
    state.clientReport = computeClientAnalysis(state.params, state.geom, state.printer);
    updateDerivedBadges();
    updateDiagnosticsUI();
    requestRender();
  }

  function rebuildScene(fastInteractive) {
    const p = state.params;
    const fast = Boolean(fastInteractive);
    state.geom = computeGearPairGeometry(p);
    state.contourG1 = buildGear2DContour(p, state.geom, "pinion", 12, 0.0);
    state.contourG2 = buildGear2DContour(p, state.geom, "gear", 12, 0.0);
    state.clientReport = computeClientAnalysis(p, state.geom, state.printer);

    if (gl) {
      uploadCollectorToPart("pinion", buildGear3DMeshData(p, state.geom, "pinion", fast));
      uploadCollectorToPart("gear", buildGear3DMeshData(p, state.geom, "gear", fast));

      if (state.vpView === "fit_kit" || (state.vpView === "plater" && (p.export_target === "fit_test_kit" || p.export_target === "full_suite"))) {
        uploadCollectorToPart("sector_pinion", buildFitKitSectorMesh(p, state.geom, "pinion"));
        uploadCollectorToPart("sector_gear", buildFitKitSectorMesh(p, state.geom, "gear"));
        const jg = buildFitKitJigAndGaugeMeshes(p, state.geom);
        uploadCollectorToPart("jig_base", jg.jig);
        uploadCollectorToPart("bore_gauge", jg.gauge);
      }
    }

    updateDerivedBadges();
    updateDiagnosticsUI();
    requestRender();
  }

  const sliderRefs = {};

  function buildSliderWidgets() {
    for (let i = 0; i < SLIDER_SPECS.length; i++) {
      const spec = SLIDER_SPECS[i];
      const host = document.querySelector('[data-slider="' + spec.path + '"]');
      if (!host) continue;

      const decs = spec.step < 0.05 ? 2 : (spec.step < 1 ? 1 : 0);
      const initVal = getByPath(state.params, spec.path);
      const dualHtml = spec.dualMm
        ? '<span class="dual-mm-badge" data-dual-badge="' + spec.path + '">0.00 mm</span>'
        : "";

      host.className = "ctrl-row";
      host.innerHTML =
        '<div class="ctrl-top">' +
          '<span class="ctrl-label" data-spec-label="' + spec.path + '">' + (state.lang === "en" ? spec.en : spec.pt) + '</span>' +
          '<div class="ctrl-val-wrap">' +
            dualHtml +
            '<input class="ctrl-num" type="number" min="' + spec.min + '" max="' + spec.max + '" step="' + spec.step + '" value="' + Number(initVal).toFixed(decs) + '" />' +
            '<span class="ctrl-unit">' + spec.unit + '</span>' +
          '</div>' +
        '</div>' +
        '<input class="orca-slider" type="range" min="' + spec.min + '" max="' + spec.max + '" step="' + spec.step + '" value="' + initVal + '" />';

      const rangeEl = host.querySelector('input[type="range"]');
      const numEl = host.querySelector('input[type="number"]');
      const labelEl = host.querySelector("[data-spec-label]");
      const dualEl = host.querySelector("[data-dual-badge]");

      sliderRefs[spec.path] = { spec: spec, rangeEl: rangeEl, numEl: numEl, labelEl: labelEl, dualEl: dualEl, decs: decs };

      const applyParamEdit = function (rawVal, isLiveDrag) {
        if (spec.path === "helix_angle_deg" && rawVal > 0.5 && state.params.gear_type === "spur") {
          state.params.gear_type = "helical";
        }
        setByPath(state.params, spec.path, rawVal);
        state.params = normalizeParams(state.params);
        state.hostReport = null;
        const normV = getByPath(state.params, spec.path);
        if (numEl && document.activeElement !== numEl) numEl.value = Number(normV).toFixed(decs);
        if (rangeEl && document.activeElement !== rangeEl) rangeEl.value = String(normV);

        // Fast rigid-body update when only center_distance_offset_mm or input_torque_nm changes!
        if (spec.path === "center_distance_offset_mm" || spec.path === "input_torque_nm") {
          recomputeKinematicsAndLoupeOnly();
        } else {
          rebuildScene(isLiveDrag);
        }
      };

      if (rangeEl) {
        rangeEl.addEventListener("pointerdown", function () {
          beginUndoGesture();
          state.isInteracting = true;
        });
        rangeEl.addEventListener("input", function () {
          applyParamEdit(Number(rangeEl.value), true);
        });
        const finishRange = function () {
          if (!state.isInteracting) return;
          state.isInteracting = false;
          commitUndoGesture();
          rebuildScene(false);
          scheduleHostAnalyze();
        };
        rangeEl.addEventListener("pointerup", finishRange);
        rangeEl.addEventListener("change", finishRange);
      }

      if (numEl) {
        numEl.addEventListener("change", function () {
          const before = deepClone(state.params);
          applyParamEdit(Number(numEl.value), false);
          numEl.value = Number(getByPath(state.params, spec.path)).toFixed(decs);
          pushUndoSnapshot(before);
          scheduleHostAnalyze();
        });
      }
    }
  }

  function syncSlidersOnly() {
    const paths = Object.keys(sliderRefs);
    for (let i = 0; i < paths.length; i++) {
      const ref = sliderRefs[paths[i]];
      const v = getByPath(state.params, paths[i]);
      if (v === undefined) continue;
      if (ref.rangeEl) ref.rangeEl.value = String(v);
      if (ref.numEl) ref.numEl.value = Number(v).toFixed(ref.decs);
    }
  }

  function updateDerivedBadges() {
    const p = state.params;
    const g = state.geom || computeGearPairGeometry(p);
    const mN = p.module_mm;

    // 1. Dual Tooth-Height Badges (`Factor × | Real mm`) + Total Tooth Height `h = (2*h_a* + c*) * m_n`
    const dualKeys = ["addendum_coeff", "clearance_coeff", "root_fillet_coeff", "tip_chamfer_coeff"];
    for (let i = 0; i < dualKeys.length; i++) {
      const k = dualKeys[i];
      const ref = sliderRefs[k];
      if (ref && ref.dualEl) {
        const factor = Number(p[k]);
        const realMm = factor * mN;
        ref.dualEl.textContent = factor.toFixed(2) + "× (" + realMm.toFixed(2) + " mm)";
      }
    }
    const totalToothMm = (2.0 * p.addendum_coeff + p.clearance_coeff) * mN;
    const hBadge = document.getElementById("badge-total-tooth-h");
    if (hBadge) hBadge.textContent = "h = " + totalToothMm.toFixed(2) + " mm";

    const tpBtns = document.querySelectorAll("[data-tooth-preset]");
    for (let i = 0; i < tpBtns.length; i++) {
      const kind = tpBtns[i].getAttribute("data-tooth-preset");
      const match =
        (kind === "iso" && Math.abs(p.addendum_coeff - 1.00) < 0.02) ||
        (kind === "stub" && Math.abs(p.addendum_coeff - 0.75) < 0.02) ||
        (kind === "high" && Math.abs(p.addendum_coeff - 1.20) < 0.02);
      tpBtns[i].classList.toggle("active", match);
    }

    // 2. Ratio, Gear Type, Helix Pills & Hand
    const ratioBadge = document.getElementById("badge-ratio");
    if (ratioBadge) {
      ratioBadge.textContent = "1 : " + g.ratio.toFixed(2) + " (" + p.pinion.teeth + ":" + p.gear.teeth + ")";
    }

    const gtBtns = document.querySelectorAll("[data-gear-type]");
    for (let i = 0; i < gtBtns.length; i++) {
      gtBtns[i].classList.toggle("active", gtBtns[i].getAttribute("data-gear-type") === p.gear_type);
    }

    const effBeta = effectiveHelixAngleDeg(p);
    const effBadge = document.getElementById("badge-eff-helix");
    if (effBadge) {
      effBadge.textContent = "β_eff " + effBeta.toFixed(1) + "°";
    }

    const hPills = document.querySelectorAll("[data-helix-pill]");
    for (let i = 0; i < hPills.length; i++) {
      const hv = Number(hPills[i].getAttribute("data-helix-pill"));
      const isAct = (hv === 0 && effBeta < 0.2) || (hv > 0 && p.gear_type !== "spur" && Math.abs(p.helix_angle_deg - hv) < 0.4);
      hPills[i].classList.toggle("active", isAct);
    }

    const handBtns = document.querySelectorAll("[data-helix-hand]");
    for (let i = 0; i < handBtns.length; i++) {
      handBtns[i].classList.toggle("active", handBtns[i].getAttribute("data-helix-hand") === p.helix_hand);
    }

    const modPills = document.querySelectorAll("[data-mod-pill]");
    for (let i = 0; i < modPills.length; i++) {
      const mv = Number(modPills[i].getAttribute("data-mod-pill"));
      modPills[i].classList.toggle("active", Math.abs(p.module_mm - mv) < 0.02);
    }

    // 3. Effective Profile Shifts Readout
    const shiftNote = document.getElementById("badge-eff-shifts");
    if (shiftNote) {
      const fmtS = function (v) { return (v >= 0 ? "+" : "") + v.toFixed(2); };
      shiftNote.textContent = "x₁ efetivo: " + fmtS(g.x1) + " · x₂ efetivo: " + fmtS(g.x2) +
        (g.pinion.undercut || g.gear.undercut ? " ⚠ Undercut" : " ✓ Sem Undercut");
    }

    // 4. Body Pane Visibility & Conditional Bore / Hub / Recess / Lightening Controls
    const isG1 = state.activeBodyTab === "pinion";
    const tabG1 = document.getElementById("btn-body-tab-pinion");
    const tabG2 = document.getElementById("btn-body-tab-gear");
    const paneG1 = document.getElementById("body-pane-pinion");
    const paneG2 = document.getElementById("body-pane-gear");
    if (tabG1) tabG1.classList.toggle("active", isG1);
    if (tabG2) tabG2.classList.toggle("active-g2", !isG1);
    if (paneG1) paneG1.style.display = isG1 ? "flex" : "none";
    if (paneG2) paneG2.style.display = isG1 ? "none" : "flex";

    const syncBodySubBoxes = function (who) {
      const b = p[who];
      const boreDims = document.getElementById("box-" + who + "-bore-dims");
      const dflat = document.getElementById("box-" + who + "-dflat");
      const kw = document.getElementById("box-" + who + "-keyway");
      const hub = document.getElementById("box-" + who + "-hub");
      const rec = document.getElementById("box-" + who + "-recess");
      const web = document.getElementById("box-" + who + "-web");
      const holes = document.getElementById("box-" + who + "-holes");

      if (boreDims) boreDims.style.display = b.bore_type === "none" ? "none" : "flex";
      if (dflat) dflat.style.display = (b.bore_type === "d_shaft" || b.bore_type === "double_d") ? "flex" : "none";
      if (kw) kw.style.display = b.bore_type === "keyway" ? "flex" : "none";
      if (hub) hub.style.display = b.hub_enabled ? "flex" : "none";
      if (rec) rec.style.display = b.recess_enabled ? "flex" : "none";
      if (web) web.style.display = b.lightening_mode === "web_recess" ? "flex" : "none";
      if (holes) holes.style.display = b.lightening_mode === "lightening_holes" ? "flex" : "none";
    };
    syncBodySubBoxes("pinion");
    syncBodySubBoxes("gear");

    // 5. Simulation Transport & Live Delta_a Bar Sync
    const playBtn = document.getElementById("btn-sim-play");
    if (playBtn) {
      playBtn.textContent = state.simPlaying
        ? (state.lang === "en" ? "⏸ Pause" : "⏸ Pausar")
        : (state.lang === "en" ? "▶ Play" : "▶ Girar");
    }
    const dirBtn = document.getElementById("btn-sim-dir");
    if (dirBtn) {
      dirBtn.textContent = p.sim_direction === "cw" ? "CW ↻" : "CCW ↺";
    }
    const rpmInp = document.getElementById("inp-sim-rpm");
    const rpmLbl = document.getElementById("lbl-sim-rpm");
    if (rpmInp && document.activeElement !== rpmInp) rpmInp.value = String(Math.round(p.sim_rpm));
    if (rpmLbl) rpmLbl.textContent = Math.round(p.sim_rpm) + " rpm";

    const daInp = document.getElementById("inp-sim-delta-a");
    const daLbl = document.getElementById("lbl-sim-delta-a");
    if (daInp && document.activeElement !== daInp) {
      daInp.value = String(Math.max(-1.0, Math.min(2.0, p.center_distance_offset_mm)));
    }
    if (daLbl) {
      const da = p.center_distance_offset_mm;
      daLbl.textContent = (da >= 0 ? "+" : "") + da.toFixed(2) + " mm";
      daLbl.style.color = da < -0.15 ? "var(--status-crit)" : "";
    }

    // 6. Export Target Helper Note
    const expNote = document.getElementById("export-target-note");
    if (expNote) {
      if (p.export_target === "fit_test_kit") expNote.textContent = tr("note_exp_kit");
      else if (p.export_target === "full_suite") expNote.textContent = tr("note_exp_full");
      else if (p.export_target === "pair_separated") expNote.textContent = tr("note_exp_pair");
      else expNote.textContent = tr("note_exp_single");
    }
  }

  function updateDiagnosticsUI() {
    const cRep = state.clientReport;
    if (!cRep) return;
    // Prefer host Python `analysis_result` when idle & fresh; fallback seamlessly to live JS solver while dragging!
    const rep = (!state.isInteracting && state.hostReport && state.hostReport.contact) ? state.hostReport : cRep;
    const contact = rep.contact || cRep.contact;
    const fit = rep.fit || cRep.fit;
    const kin = rep.kinematics || cRep.kinematics;
    const prt = rep.printability || cRep.printability;
    const isJammed = Boolean(fit.jammed || cRep.fit.jammed || state.liveCollision.collided);
    const status = isJammed ? "critical" : (rep.status || cRep.status || "ok");

    const setTxt = function (id, txt, color) {
      const el = document.getElementById(id);
      if (el) {
        el.textContent = txt;
        el.style.color = color || "";
      }
    };

    // Viewport Right HUD
    const hudPill = document.getElementById("hud-status-pill");
    const diagPill = document.getElementById("diag-status-pill");
    const cls = status === "critical" ? "crit" : (status === "warn" ? "warn" : "ok");
    const stText = status === "critical" ? tr("status_crit") : (status === "warn" ? tr("status_warn") : tr("status_ok"));
    if (hudPill) { hudPill.className = "hud-status-pill " + cls; hudPill.textContent = stText; }
    if (diagPill) { diagPill.className = "hud-status-pill " + cls; diagPill.textContent = stText; }

    setTxt("hud-cd", Number(fit.center_distance_mm).toFixed(2) + " mm");
    setTxt("hud-ft", Number(kin.tangential_force_n).toFixed(1) + " N");
    setTxt("hud-fr", Number(kin.radial_force_n).toFixed(1) + " N");
    const faVal = Number(kin.axial_force_n || 0);
    setTxt("hud-fa", faVal.toFixed(1) + " N", faVal > 0.5 ? "#f59e0b" : "var(--status-ok)");

    const thrustNote = document.getElementById("hud-thrust-note");
    if (thrustNote) {
      const balanced = Boolean(kin.axial_thrust_balanced);
      thrustNote.classList.toggle("axial-active", !balanced && faVal > 0.1);
      if (state.params.gear_type === "spur" || state.geom.beta_deg < 0.1) {
        thrustNote.textContent = tr("thrust_zero_spur");
      } else if (state.params.gear_type === "herringbone") {
        thrustNote.textContent = tr("thrust_zero_hb");
      } else {
        thrustNote.textContent = tr("thrust_helical_fmt")
          .replace("{fa}", faVal.toFixed(1))
          .replace("{b}", state.geom.beta_deg.toFixed(0));
      }
    }

    // Right Column Diagnostics Grid
    setTxt("dv-eps-a", Number(contact.transverse_ratio).toFixed(2), contact.transverse_ratio < 1.15 ? "var(--status-warn)" : "");
    setTxt("dv-eps-b", Number(contact.axial_overlap_ratio).toFixed(2));
    setTxt("dv-eps-g", Number(contact.total_contact_ratio).toFixed(2), "var(--orca-accent-hover)");
    setTxt("dv-loa", Number(contact.line_of_action_length_mm).toFixed(2) + " mm");

    const da = state.params.center_distance_offset_mm;
    setTxt("dv-cd", Number(fit.center_distance_mm).toFixed(2) + " (" + (da >= 0 ? "+" : "") + da.toFixed(2) + ")");
    const clrVal = isJammed ? 0.0 : Number(fit.min_tooth_clearance_mm);
    setTxt("dv-clr", isJammed ? "0.00 (COLISÃO)" : clrVal.toFixed(3) + " mm", isJammed ? "var(--status-crit)" : "var(--status-ok)");
    setTxt("dv-t2", Number(kin.torque_g2_nm).toFixed(2) + " N·m");
    setTxt("dv-rpm2", Number(kin.rpm_g2).toFixed(1) + " rpm · " + Number(kin.pitch_line_velocity_mm_s).toFixed(0) + " mm/s");

    const ovh = Number(prt.helix_overhang_deg || 0);
    setTxt("dv-ovh", ovh.toFixed(0) + "° " + (prt.supports_needed ? "⚠ Suporte" : "✓ Livre"), prt.supports_needed ? "var(--status-warn)" : "var(--status-ok)");
    setTxt("dv-walls", String(prt.recommended_wall_loops || 4) + " loops + Gyroid");
    setTxt("dv-wgt", "~" + Math.max(1, Math.round(prt.estimated_weight_g || 20)) + " g · " + Math.max(5, Math.round(prt.estimated_print_time_min || 25)) + " min");
    const fp = Array.isArray(prt.pair_footprint_mm) ? prt.pair_footprint_mm : [100, 60];
    setTxt("dv-bed", Math.round(fp[0]) + "×" + Math.round(fp[1]) + " mm", prt.fits_bed === false ? "var(--status-crit)" : "");

    // Issues List
    const issuesEl = document.getElementById("diag-issues-list");
    if (issuesEl) {
      issuesEl.innerHTML = "";
      const list = Array.isArray(rep.issues) && rep.issues.length ? rep.issues : cRep.issues;
      for (let i = 0; i < list.length; i++) {
        const it = list[i];
        const div = document.createElement("div");
        if (typeof it === "string") {
          div.className = "issue-item warn";
          div.textContent = it;
        } else {
          const sev = String(it.severity || "ok").toLowerCase();
          div.className = "issue-item " + (sev === "critical" || sev === "crit" ? "critical" : (sev === "warn" || sev === "warning" ? "warn" : "ok"));
          div.textContent = state.lang === "en" ? (it.en || it.message_en || it.pt || "") : (it.pt || it.message_pt || it.en || "");
        }
        issuesEl.appendChild(div);
      }
    }
  }

  function syncControlsFromState() {
    const p = state.params;
    const setVal = function (id, v) {
      const el = document.getElementById(id);
      if (el) el.value = v;
    };
    const setChk = function (id, v) {
      const el = document.getElementById(id);
      if (el) el.checked = Boolean(v);
    };

    setVal("inp-gear-name", p.name);
    setChk("chk-auto-shift", p.auto_profile_shift);
    setChk("chk-auto-slicer", p.auto_configure_slicer);
    setVal("sel-export-target", p.export_target);

    setVal("sel-pinion-bore-type", p.pinion.bore_type);
    setChk("chk-pinion-hub", p.pinion.hub_enabled);
    setChk("chk-pinion-recess", p.pinion.recess_enabled);
    setVal("sel-pinion-recess-side", p.pinion.recess_side);
    setVal("sel-pinion-lightening", p.pinion.lightening_mode);

    setVal("sel-gear-bore-type", p.gear.bore_type);
    setChk("chk-gear-hub", p.gear.hub_enabled);
    setChk("chk-gear-recess", p.gear.recess_enabled);
    setVal("sel-gear-recess-side", p.gear.recess_side);
    setVal("sel-gear-lightening", p.gear.lightening_mode);

    syncSlidersOnly();
    updateDerivedBadges();
  }

  function makePresetMiniSvg(presetParams) {
    const p = normalizeParams(presetParams);
    const gt = p.gear_type;
    let slash = "";
    if (gt === "helical") {
      slash = '<line x1="8" y1="21" x2="14" y2="11" stroke="#00bfa5" stroke-width="1.5"/>';
    } else if (gt === "herringbone") {
      slash = '<polyline points="8,21 12,16 8,11" fill="none" stroke="#f59e0b" stroke-width="1.4"/>';
    }
    return '<svg width="32" height="32" viewBox="0 0 32 32">' +
      '<circle cx="11" cy="16" r="7.5" fill="rgba(0,191,165,0.18)" stroke="#00bfa5" stroke-width="1.6" stroke-dasharray="2.5 1.5"/>' +
      '<circle cx="22.5" cy="16" r="5.5" fill="rgba(79,156,249,0.18)" stroke="#4f9cf9" stroke-width="1.5" stroke-dasharray="2.2 1.4"/>' +
      slash +
      '</svg>';
  }

  function matchesPresetCategory(item, filterCat) {
    if (filterCat === "all") return true;
    if (filterCat === "user") return Boolean(item._isUser);
    const cat = String(item.category || "").toLowerCase();
    const gt = item.params && item.params.gear_type ? item.params.gear_type : "";
    if (filterCat === "spur_ind") return gt === "spur" || cat.includes("ind") || cat.includes("stand") || cat.includes("prec");
    if (filterCat === "helical") return gt === "helical" || cat === "helical";
    if (filterCat === "herringbone") return gt === "herringbone" || cat === "herringbone";
    if (filterCat === "robotics_cal") return cat.includes("robot") || cat.includes("cal") || (item.params && item.params.export_target === "fit_test_kit");
    return true;
  }

  function renderPresetsGrid() {
    const gridEl = document.getElementById("presets-grid");
    if (!gridEl) return;
    gridEl.innerHTML = "";

    const combined = [];
    for (let i = 0; i < state.userPresets.length; i++) {
      combined.push(Object.assign({}, state.userPresets[i], { _isUser: true }));
    }
    for (let i = 0; i < state.builtinPresets.length; i++) {
      combined.push(Object.assign({}, state.builtinPresets[i], { _isUser: false }));
    }

    for (let i = 0; i < combined.length; i++) {
      const item = combined[i];
      if (!matchesPresetCategory(item, state.presetFilter)) continue;

      const card = document.createElement("div");
      card.className = "preset-card" + (item.id === state.activePresetId ? " active" : "");

      const title = state.lang === "en"
        ? (item.name_en || item.title_en || item.name || item.name_pt || "Preset")
        : (item.name_pt || item.title_pt || item.name || item.name_en || "Preset");
      const desc = state.lang === "en"
        ? (item.desc_en || item.description_en || item.category || "")
        : (item.desc_pt || item.description_pt || item.category || "");

      card.innerHTML =
        '<div class="preset-thumb">' + makePresetMiniSvg(item.params || {}) + '</div>' +
        '<div class="preset-meta">' +
          '<div class="preset-name"></div>' +
          '<div class="preset-sub"></div>' +
        '</div>';

      const nmEl = card.querySelector(".preset-name");
      const sbEl = card.querySelector(".preset-sub");
      if (nmEl) nmEl.textContent = title;
      if (sbEl) sbEl.textContent = desc;
      card.title = title + (desc ? " — " + desc : "");

      if (item._isUser) {
        const delBtn = document.createElement("button");
        delBtn.className = "preset-del-btn";
        delBtn.textContent = "×";
        delBtn.title = "Delete";
        delBtn.addEventListener("click", function (ev) {
          ev.stopPropagation();
          if (!sendToHost({ type: "preset_delete", id: item.id })) {
            state.userPresets = state.userPresets.filter(function (u) { return u.id !== item.id; });
            renderPresetsGrid();
          }
        });
        card.appendChild(delBtn);
      }

      card.addEventListener("click", function () {
        pushUndoSnapshot(state.params);
        state.activePresetId = item.id;
        state.params = normalizeParams(item.params);
        if (title) state.params.name = title.slice(0, 80);
        state.hostReport = null;

        // If calibration preset selected, showcase the 3D Fit-Test Kit automatically!
        if (state.params.export_target === "fit_test_kit") {
          setViewportMode("fit_kit");
        } else if (state.vpView === "fit_kit") {
          setViewportMode("meshed");
        }

        renderPresetsGrid();
        syncControlsFromState();
        rebuildScene(false);
        fitCameraToScene();
        scheduleHostAnalyze();
      });

      gridEl.appendChild(card);
    }
  }

  function setViewportMode(nextMode) {
    state.vpView = nextMode;
    const btns = document.querySelectorAll("[data-vp-view]");
    for (let i = 0; i < btns.length; i++) {
      btns[i].classList.toggle("active", btns[i].getAttribute("data-vp-view") === nextMode);
    }
    rebuildScene(false);
    fitCameraToScene();
  }

  function applyThemeAndLanguage() {
    if (typeof document === "undefined") return;
    document.documentElement.setAttribute("data-theme", state.theme);
    document.documentElement.setAttribute("lang", state.lang);
    if (document.body) document.body.setAttribute("data-mode", state.mode);

    const langBtn = document.getElementById("btn-lang");
    if (langBtn) langBtn.textContent = state.lang.toUpperCase();
    const themeBtn = document.getElementById("btn-theme");
    if (themeBtn) themeBtn.textContent = state.theme === "dark" ? "☾" : "☀";

    const printerText = document.getElementById("printer-pill-text");
    if (printerText) {
      const pr = state.printer;
      printerText.textContent =
        (pr.name || "Printer") + " · " +
        Math.round(pr.bed_x || 220) + "×" +
        Math.round(pr.bed_y || 220) + "×" +
        Math.round(pr.max_z || 250) + " mm · " +
        Number(pr.nozzle_mm || 0.4).toFixed(1) + "mm";
    }

    const nodes = document.querySelectorAll("[data-i18n]");
    for (let i = 0; i < nodes.length; i++) {
      const k = nodes[i].getAttribute("data-i18n");
      if (k) nodes[i].textContent = tr(k);
    }

    const paths = Object.keys(sliderRefs);
    for (let i = 0; i < paths.length; i++) {
      const ref = sliderRefs[paths[i]];
      if (ref.labelEl) ref.labelEl.textContent = state.lang === "en" ? ref.spec.en : ref.spec.pt;
    }

    updateDerivedBadges();
    renderPresetsGrid();
    updateDiagnosticsUI();
    requestRender();
  }

  function updateUndoButtons() {
    const u = document.getElementById("btn-undo");
    const r = document.getElementById("btn-redo");
    if (u) u.disabled = state.undoStack.length === 0;
    if (r) r.disabled = state.redoStack.length === 0;
  }

  function setActionButtonsBusy(busy) {
    state.busyAction = busy;
    const btns = document.querySelectorAll("[data-action]");
    for (let i = 0; i < btns.length; i++) btns[i].disabled = busy;
  }

  let toastTimer = null;
  function showToast(text, isError) {
    const el = document.getElementById("toast-banner");
    if (!el) return;
    el.textContent = text;
    el.classList.toggle("error", Boolean(isError));
    el.classList.add("visible");
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      el.classList.remove("visible");
    }, 3600);
  }

  function localPrintableRandomize(seedNum) {
    let s = (seedNum || Date.now()) >>> 0;
    const rand = function () {
      s = (Math.imul(s ^ (s >>> 15), 2246822519) + 3266489917) >>> 0;
      return (s >>> 0) / 4294967295.0;
    };
    const pick = function (arr) { return arr[Math.floor(rand() * arr.length)]; };
    const p = deepClone(state.params);
    p.gear_type = pick(["spur", "helical", "herringbone"]);
    p.helix_angle_deg = p.gear_type === "spur" ? 30.0 : pick([20, 25, 30, 35, 45]);
    p.module_mm = pick([1.25, 1.5, 1.75, 2.0, 2.5]);
    p.face_width_mm = pick([10, 12, 14, 16]);
    p.addendum_coeff = pick([0.85, 1.0, 1.0, 1.15]);
    p.center_distance_offset_mm = 0.0;
    p.auto_profile_shift = true;
    p.pinion.teeth = Math.floor(10 + rand() * 14);
    p.gear.teeth = Math.min(64, Math.round(p.pinion.teeth * pick([1.5, 2.0, 2.5, 3.0, 3.5])));
    p.pinion.bore_type = pick(["d_shaft", "round", "hex"]);
    p.gear.bore_type = pick(["round", "hex", "keyway"]);
    p.gear.lightening_mode = p.gear.teeth >= 26 ? "lightening_holes" : "solid";
    return normalizeParams(p);
  }

  function sanitizeExportStem(name) {
    const clean = String(name || "engrenagens").replace(/[^\w\-. ]+/g, "").trim().replace(/\s+/g, "_");
    return clean || "engrenagens";
  }

  // ==========================================================================
  // 12. UI Event Wiring & Boot
  // ==========================================================================
  function bindUIControls() {
    const on = function (id, evt, fn) {
      const el = document.getElementById(id);
      if (el) el.addEventListener(evt, fn);
    };

    on("inp-gear-name", "change", function (e) {
      state.params.name = String(e.target.value || "").trim().slice(0, 80) || "Par Engrenagens";
    });

    on("btn-undo", "click", performUndo);
    on("btn-redo", "click", performRedo);

    on("btn-randomize", "click", function () {
      const seed = Math.floor(Math.random() * 99999) + 1;
      if (!sendToHost({ type: "randomize", seed: seed, params: deepClone(state.params) })) {
        pushUndoSnapshot(state.params);
        state.params = localPrintableRandomize(seed);
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        fitCameraToScene();
        showToast(tr("toast_randomized"), false);
      }
    });

    on("btn-reset", "click", function () {
      pushUndoSnapshot(state.params);
      state.params = normalizeParams(JS_DEFAULT_PARAMS);
      state.hostReport = null;
      state.crossCutPct = 0;
      state.vpView = "meshed";
      const cutEl = document.getElementById("inp-cross-cut");
      const cutLbl = document.getElementById("lbl-cross-cut");
      if (cutEl) cutEl.value = "0";
      if (cutLbl) cutLbl.textContent = "Off";
      syncControlsFromState();
      setViewportMode("meshed");
      scheduleHostAnalyze();
    });

    on("btn-lang", "click", function () {
      state.lang = state.lang === "pt" ? "en" : "pt";
      applyThemeAndLanguage();
    });

    on("btn-theme", "click", function () {
      state.theme = state.theme === "dark" ? "light" : "dark";
      applyThemeAndLanguage();
    });

    // Dock Mode Tabs
    const tabBtns = document.querySelectorAll(".dock-tab-btn");
    for (let i = 0; i < tabBtns.length; i++) {
      tabBtns[i].addEventListener("click", function () {
        const tab = tabBtns[i].getAttribute("data-tab") || "gears";
        if (document.body) document.body.setAttribute("data-dock-tab", tab);
        for (let k = 0; k < tabBtns.length; k++) {
          tabBtns[k].classList.toggle("active", tabBtns[k] === tabBtns[i]);
        }
        requestRender();
      });
    }

    // Presets Save & Filter Chips
    on("btn-toggle-save-preset", "click", function () {
      const bar = document.getElementById("save-preset-bar");
      const inp = document.getElementById("inp-save-preset-name");
      if (bar) {
        const open = !bar.classList.contains("open");
        bar.classList.toggle("open", open);
        if (open && inp) {
          inp.value = state.params.name || "Meu Redutor";
          inp.focus?.();
        }
      }
    });

    on("btn-confirm-save-preset", "click", function () {
      const inp = document.getElementById("inp-save-preset-name");
      const bar = document.getElementById("save-preset-bar");
      const name = String(inp && inp.value ? inp.value : state.params.name || "Meu Redutor").trim() || "Meu Redutor";
      state.params.name = name.slice(0, 80);
      const nmMain = document.getElementById("inp-gear-name");
      if (nmMain) nmMain.value = state.params.name;

      if (!sendToHost({ type: "preset_save", name: state.params.name, params: deepClone(state.params) })) {
        state.userPresets.push({
          id: "local_" + Date.now(),
          name: state.params.name,
          name_pt: state.params.name,
          name_en: state.params.name,
          category: "user",
          params: deepClone(state.params)
        });
        renderPresetsGrid();
      }
      if (bar) bar.classList.remove("open");
      showToast(tr("toast_preset_saved"), false);
    });

    const filterChips = document.querySelectorAll("#preset-filters .filter-chip");
    for (let i = 0; i < filterChips.length; i++) {
      filterChips[i].addEventListener("click", function () {
        state.presetFilter = filterChips[i].getAttribute("data-cat") || "all";
        for (let k = 0; k < filterChips.length; k++) {
          filterChips[k].classList.toggle("active", filterChips[k] === filterChips[i]);
        }
        renderPresetsGrid();
      });
    }

    // Gear Type Buttons (`spur`, `helical`, `herringbone`)
    const gtBtns = document.querySelectorAll("[data-gear-type]");
    for (let i = 0; i < gtBtns.length; i++) {
      gtBtns[i].addEventListener("click", function () {
        const gt = gtBtns[i].getAttribute("data-gear-type");
        if (!gt || state.params.gear_type === gt) return;
        pushUndoSnapshot(state.params);
        state.params.gear_type = gt;
        if (gt !== "spur" && state.params.helix_angle_deg < 1.0) {
          state.params.helix_angle_deg = 30.0;
        }
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
    }

    // Helix Quick Pills (`0°`, `15°`, `30°`, `45°` — 1-click switches `spur` -> `helical` for 15/30/45!)
    const hPills = document.querySelectorAll("[data-helix-pill]");
    for (let i = 0; i < hPills.length; i++) {
      hPills[i].addEventListener("click", function () {
        const deg = Number(hPills[i].getAttribute("data-helix-pill"));
        pushUndoSnapshot(state.params);
        if (deg <= 0.0) {
          state.params.gear_type = "spur";
          state.params.helix_angle_deg = 0.0;
        } else {
          if (state.params.gear_type === "spur") {
            state.params.gear_type = "helical";
          }
          state.params.helix_angle_deg = deg;
        }
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
    }

    // Helix Hand (`right` / `left`)
    const handBtns = document.querySelectorAll("[data-helix-hand]");
    for (let i = 0; i < handBtns.length; i++) {
      handBtns[i].addEventListener("click", function () {
        const hh = handBtns[i].getAttribute("data-helix-hand");
        if (!hh || state.params.helix_hand === hh) return;
        pushUndoSnapshot(state.params);
        state.params.helix_hand = hh;
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
    }

    // Swap Z1 <-> Z2
    on("btn-swap-teeth", "click", function () {
      pushUndoSnapshot(state.params);
      const t1 = state.params.pinion.teeth;
      state.params.pinion.teeth = state.params.gear.teeth;
      state.params.gear.teeth = t1;
      state.hostReport = null;
      syncControlsFromState();
      rebuildScene(false);
      fitCameraToScene();
      scheduleHostAnalyze();
    });

    // Quick Module Pills
    const modPills = document.querySelectorAll("[data-mod-pill]");
    for (let i = 0; i < modPills.length; i++) {
      modPills[i].addEventListener("click", function () {
        const mv = Number(modPills[i].getAttribute("data-mod-pill"));
        pushUndoSnapshot(state.params);
        state.params.module_mm = mv;
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        fitCameraToScene();
        scheduleHostAnalyze();
      });
    }

    // Dual Tooth-Height Quick Presets (`ISO 1.00×`, `Stub 0.75×`, `High Contact 1.20×`)
    const tpBtns = document.querySelectorAll("[data-tooth-preset]");
    for (let i = 0; i < tpBtns.length; i++) {
      tpBtns[i].addEventListener("click", function () {
        const kind = tpBtns[i].getAttribute("data-tooth-preset");
        pushUndoSnapshot(state.params);
        if (kind === "stub") {
          state.params.addendum_coeff = 0.75;
          state.params.clearance_coeff = 0.25;
          state.params.root_fillet_coeff = 0.38;
          state.params.tip_chamfer_coeff = 0.05;
        } else if (kind === "high") {
          state.params.addendum_coeff = 1.20;
          state.params.clearance_coeff = 0.30;
          state.params.root_fillet_coeff = 0.26;
          state.params.tip_chamfer_coeff = 0.06;
        } else {
          state.params.addendum_coeff = 1.00;
          state.params.clearance_coeff = 0.25;
          state.params.root_fillet_coeff = 0.30;
          state.params.tip_chamfer_coeff = 0.06;
        }
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
    }

    on("chk-auto-shift", "change", function (e) {
      pushUndoSnapshot(state.params);
      state.params.auto_profile_shift = Boolean(e.target.checked);
      state.hostReport = null;
      rebuildScene(false);
      scheduleHostAnalyze();
    });

    // Pinion G1 vs Gear G2 Body Tabs & Controls
    on("btn-body-tab-pinion", "click", function () {
      state.activeBodyTab = "pinion";
      updateDerivedBadges();
    });
    on("btn-body-tab-gear", "click", function () {
      state.activeBodyTab = "gear";
      updateDerivedBadges();
    });

    const bindBodyControls = function (who) {
      on("sel-" + who + "-bore-type", "change", function (e) {
        pushUndoSnapshot(state.params);
        state.params[who].bore_type = e.target.value;
        state.params = normalizeParams(state.params);
        state.hostReport = null;
        updateDerivedBadges();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
      on("chk-" + who + "-hub", "change", function (e) {
        pushUndoSnapshot(state.params);
        state.params[who].hub_enabled = Boolean(e.target.checked);
        updateDerivedBadges();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
      on("chk-" + who + "-recess", "change", function (e) {
        pushUndoSnapshot(state.params);
        state.params[who].recess_enabled = Boolean(e.target.checked);
        updateDerivedBadges();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
      on("sel-" + who + "-recess-side", "change", function (e) {
        pushUndoSnapshot(state.params);
        state.params[who].recess_side = e.target.value;
        rebuildScene(false);
        scheduleHostAnalyze();
      });
      on("sel-" + who + "-lightening", "change", function (e) {
        pushUndoSnapshot(state.params);
        state.params[who].lightening_mode = e.target.value;
        updateDerivedBadges();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
    };
    bindBodyControls("pinion");
    bindBodyControls("gear");

    on("btn-608-gear", "click", function () {
      pushUndoSnapshot(state.params);
      state.params.gear.bore_type = "round";
      state.params.gear.bore_diameter_mm = 8.0;
      state.params.gear.recess_enabled = true;
      state.params.gear.recess_diameter_mm = 22.2;
      state.params.gear.recess_depth_mm = Math.min(7.0, Math.max(2.0, state.params.face_width_mm - 2.0));
      syncControlsFromState();
      rebuildScene(false);
      scheduleHostAnalyze();
    });

    // Viewport Toolbar Controls
    const vpBtns = document.querySelectorAll("[data-vp-view]");
    for (let i = 0; i < vpBtns.length; i++) {
      vpBtns[i].addEventListener("click", function () {
        setViewportMode(vpBtns[i].getAttribute("data-vp-view") || "meshed");
      });
    }

    on("btn-vp-heatmap", "click", function () {
      state.heatmap = !state.heatmap;
      const b = document.getElementById("btn-vp-heatmap");
      const leg = document.getElementById("heatmap-legend");
      if (b) b.classList.toggle("active", state.heatmap);
      if (leg) leg.classList.toggle("visible", state.heatmap);
      requestRender();
    });

    on("btn-vp-forces", "click", function () {
      state.showForces = !state.showForces;
      const b = document.getElementById("btn-vp-forces");
      if (b) b.classList.toggle("active", state.showForces);
      requestRender();
    });

    on("btn-vp-wire", "click", function () {
      state.wireframe = !state.wireframe;
      const b = document.getElementById("btn-vp-wire");
      if (b) b.classList.toggle("active", state.wireframe);
      requestRender();
    });

    // Camera Presets (`Perspectiva`, `Topo (Engrenamento)`, `Frontal (Hélice)`, `Reset`)
    const camBtns = document.querySelectorAll("[data-cam]");
    for (let i = 0; i < camBtns.length; i++) {
      camBtns[i].addEventListener("click", function () {
        const kind = camBtns[i].getAttribute("data-cam");
        if (kind === "iso") { camera.yaw = -0.72; camera.pitch = 0.56; fitCameraToScene(); }
        else if (kind === "top") { camera.yaw = -Math.PI * 0.5; camera.pitch = 1.47; fitCameraToScene(); }
        else if (kind === "front") { camera.yaw = -Math.PI * 0.5; camera.pitch = 0.08; fitCameraToScene(); }
        else if (kind === "reset") { camera.yaw = -0.72; camera.pitch = 0.56; fitCameraToScene(); }
      });
    }

    // Z / Y Cross-Section Clipping Bar
    on("lbl-cut-axis", "click", function () {
      state.crossCutAxis = state.crossCutAxis === "z" ? "y" : "z";
      const lbl = document.getElementById("lbl-cut-axis");
      if (lbl) lbl.textContent = state.crossCutAxis === "z" ? "✂ Corte Z" : "✂ Corte Y";
      requestRender();
    });

    on("inp-cross-cut", "input", function (e) {
      state.crossCutPct = clampInt(e.target.value, 0, 0, 100);
      const lbl = document.getElementById("lbl-cross-cut");
      if (lbl) lbl.textContent = state.crossCutPct === 0 ? "Off" : (state.crossCutPct + "%");
      requestRender();
    });

    on("btn-cut-half", "click", function () {
      state.crossCutPct = state.crossCutPct === 50 ? 0 : 50;
      const inp = document.getElementById("inp-cross-cut");
      const lbl = document.getElementById("lbl-cross-cut");
      if (inp) inp.value = String(state.crossCutPct);
      if (lbl) lbl.textContent = state.crossCutPct === 0 ? "Off" : "50%";
      requestRender();
    });

    // Micro-Simulation Transport Controls
    on("btn-sim-play", "click", function () {
      state.simPlaying = !state.simPlaying;
      state.lastFrameMs = 0;
      updateDerivedBadges();
      requestRender();
    });

    on("btn-sim-dir", "click", function () {
      state.params.sim_direction = state.params.sim_direction === "cw" ? "ccw" : "cw";
      updateDerivedBadges();
      requestRender();
    });

    on("inp-sim-rpm", "input", function (e) {
      state.params.sim_rpm = clampFloat(e.target.value, 24.0, 1.0, 300.0);
      recomputeKinematicsAndLoupeOnly();
    });
    on("inp-sim-rpm", "change", scheduleHostAnalyze);

    // Manual Degree Scrub Slider & Precision Step Buttons (`-1°`, `-0.2°`, `+0.2°`, `+1°`)
    on("inp-sim-angle", "input", function (e) {
      state.simPlaying = false;
      const deg = clampFloat(e.target.value, 0.0, 0.0, 360.0);
      state.theta1Rad = deg * DEG2RAD;
      updateAngleReadoutsOnly();
      updateDerivedBadges();
      requestRender();
    });

    const stepBtns = document.querySelectorAll("[data-angle-step]");
    for (let i = 0; i < stepBtns.length; i++) {
      stepBtns[i].addEventListener("click", function () {
        state.simPlaying = false;
        const deltaDeg = Number(stepBtns[i].getAttribute("data-angle-step") || 0);
        state.theta1Rad = ((state.theta1Rad + deltaDeg * DEG2RAD) % TWO_PI + TWO_PI) % TWO_PI;
        updateAngleReadoutsOnly();
        updateDerivedBadges();
        requestRender();
      });
    }

    // Live Center-Distance Offset (Delta_a) Slider in Simulation Bar!
    const simDa = document.getElementById("inp-sim-delta-a");
    if (simDa) {
      simDa.addEventListener("pointerdown", beginUndoGesture);
      simDa.addEventListener("input", function (e) {
        state.params.center_distance_offset_mm = clampFloat(e.target.value, 0.0, -1.0, 2.0);
        state.hostReport = null;
        syncSlidersOnly();
        recomputeKinematicsAndLoupeOnly();
      });
      const finishDa = function () {
        commitUndoGesture();
        scheduleHostAnalyze();
      };
      simDa.addEventListener("pointerup", finishDa);
      simDa.addEventListener("change", finishDa);
    }

    on("btn-sim-delta-reset", "click", function () {
      if (Math.abs(state.params.center_distance_offset_mm) < 1e-5) return;
      pushUndoSnapshot(state.params);
      state.params.center_distance_offset_mm = 0.0;
      state.hostReport = null;
      syncSlidersOnly();
      recomputeKinematicsAndLoupeOnly();
      scheduleHostAnalyze();
    });

    // 2D Loupe Zoom & Collapse
    const zoomBtns = document.querySelectorAll("[data-loupe-zoom]");
    for (let i = 0; i < zoomBtns.length; i++) {
      zoomBtns[i].addEventListener("click", function () {
        state.loupeZoom = Number(zoomBtns[i].getAttribute("data-loupe-zoom") || 1.7);
        requestRender();
      });
    }

    on("btn-loupe-collapse", "click", function () {
      state.loupeCollapsed = !state.loupeCollapsed;
      const panel = document.getElementById("loupe-panel");
      const btn = document.getElementById("btn-loupe-collapse");
      if (panel) panel.classList.toggle("collapsed", state.loupeCollapsed);
      if (btn) btn.textContent = state.loupeCollapsed ? "▴" : "▾";
      requestRender();
    });

    // Export Target & Mechanical Slicer Auto-Config
    on("sel-export-target", "change", function (e) {
      state.params.export_target = toChoice(e.target.value, "pair_separated", VALID_EXPORT_TARGETS);
      if (state.params.export_target === "fit_test_kit") {
        setViewportMode("fit_kit");
      } else if (state.vpView === "plater") {
        rebuildScene(false);
      }
      updateDerivedBadges();
    });

    on("chk-auto-slicer", "change", function (e) {
      state.params.auto_configure_slicer = Boolean(e.target.checked);
    });

    // Primary OrcaSlicer Plater & Export Actions
    const actionBtns = document.querySelectorAll("[data-action]");
    for (let i = 0; i < actionBtns.length; i++) {
      actionBtns[i].addEventListener("click", function () {
        const act = actionBtns[i].getAttribute("data-action");
        if (act === "send_to_plater") {
          setActionButtonsBusy(true);
          if (!sendToHost({
            type: "send_to_plater",
            export_target: state.params.export_target,
            params: deepClone(state.params)
          })) {
            setActionButtonsBusy(false);
            showToast("OrcaSlicer host bridge not connected (Standalone Preview).", true);
          }
        } else if (act === "export_3mf" || act === "export_stl") {
          const fmt = act === "export_3mf" ? "3mf" : "stl";
          const fname = sanitizeExportStem(state.params.name) + "." + fmt;
          setActionButtonsBusy(true);
          if (!sendToHost({
            type: "export_file",
            format: fmt,
            export_target: state.params.export_target,
            params: deepClone(state.params),
            filename: fname
          })) {
            setActionButtonsBusy(false);
            showToast("OrcaSlicer host bridge not connected (Standalone Preview).", true);
          }
        } else if (act === "open_folder") {
          sendToHost({ type: "open_exports_folder" });
        }
      });
    }

    // Global Keyboard Shortcuts: Space = Play/Pause, Ctrl+Z = Undo, Ctrl+Y / Ctrl+Shift+Z = Redo
    document.addEventListener("keydown", function (e) {
      const tag = (e.target && e.target.tagName) ? String(e.target.tagName).toUpperCase() : "";
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (e.code === "Space") {
        e.preventDefault();
        state.simPlaying = !state.simPlaying;
        state.lastFrameMs = 0;
        updateDerivedBadges();
        requestRender();
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") {
        e.preventDefault();
        if (e.shiftKey) performRedo();
        else performUndo();
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "y") {
        e.preventDefault();
        performRedo();
      }
    });
  }

  function bootStudioUI() {
    if (typeof document === "undefined" || !document.getElementById) return;
    const hostTheme = detectHostInjectedTheme();
    if (hostTheme) state.theme = hostTheme;
    buildSliderWidgets();
    initWebGLViewport();
    bindUIControls();
    applyThemeAndLanguage();
    syncControlsFromState();
    rebuildScene(false);
    fitCameraToScene();
    connectOrcaBridge();
  }

  bootStudioUI();
})();
</script>
</body>
</html>
"""


def get_studio_html(mode: str = "page", initial_context: dict[str, Any] | None = None) -> str:
    """Return the complete 100% offline self-contained Orca Gear Studio HTML5/WebGL2 application.

    Args:
        mode: `"page"` for the wide 3-column OrcaSlicer tab, or `"dock"` for the
            compact right-side docked panel beside OrcaSlicer's 3D Plater.
        initial_context: Optional initial state dictionary (`lang`, `theme`,
            `printer`, `builtin_presets`, `user_presets`, `params`, `export_dir`).
    """
    norm_mode = "dock" if str(mode or "").strip().lower() == "dock" else "page"
    ctx: dict[str, Any] = copy.deepcopy(initial_context) if isinstance(initial_context, dict) else {}

    lang_raw = str(ctx.get("lang") or "pt").strip().lower()
    norm_lang = "en" if lang_raw.startswith("en") else "pt"

    theme_raw = str(ctx.get("theme") or "dark").strip().lower()
    norm_theme = "light" if theme_raw == "light" else "dark"

    fallback_params = copy.deepcopy(DEFAULT_PARAMS) if isinstance(DEFAULT_PARAMS, dict) else None
    fallback_presets = copy.deepcopy(BUILTIN_PRESETS) if isinstance(BUILTIN_PRESETS, list) else []

    boot_payload: dict[str, Any] = {
        "mode": norm_mode,
        "initial_context": ctx,
        "fallback_params": fallback_params,
        "fallback_presets": fallback_presets,
    }

    html = _STUDIO_UI_HTML_TEMPLATE
    html = html.replace("__INITIAL_LANG__", norm_lang)
    html = html.replace("__INITIAL_THEME__", norm_theme)
    html = html.replace("__INITIAL_MODE__", norm_mode)
    html = html.replace("__ORCA_GEAR_STUDIO_BOOT_JSON__", _studio_ui_safe_json(boot_payload))
    return html
