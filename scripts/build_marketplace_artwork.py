"""Build editable marketplace SVG panels from the plugin's real meshes and screenshots.

Development tool only. Rasterize the SVGs with render_marketplace_artwork.cjs.
"""
from __future__ import annotations

import base64
from html import escape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gear_studio.mesh_generator import generate_gear_mesh, generate_fit_test_kit
from gear_studio.schema import normalize_params
import numpy as np

OUT = ROOT / "assets" / "marketplace"
ACCENT = "#15dfae"
LANG = "en"


def tr(en, pt):
    return pt if LANG == "pt-BR" else en


def text(x, y, value, size=26, color="#eaf4f0", weight=400, spacing=0):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}">{escape(value)}</text>'


def frame(height, section):
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{height}" viewBox="0 0 1600 {height}">',
             '<style>text{font-family:Segoe UI,Arial,sans-serif}.mono{font-family:Consolas,monospace}</style>',
             '<defs><radialGradient id="glow"><stop stop-color="#17483e"/><stop offset="1" stop-color="#11191b"/></radialGradient></defs>',
             f'<rect width="1600" height="{height}" fill="#11191b"/>',
             f'<ellipse cx="1200" cy="{height*.5}" rx="660" ry="500" fill="url(#glow)"/>',
             '<path d="M64 112H1536" stroke="#30443f"/>',
             text(64, 71, "ORCA GEAR STUDIO", 25, ACCENT, 700, 3),
             text(1536, 71, section, 18, "#9cb8af", 400, 2).replace('<text ', '<text text-anchor="end" ', 1),
             f'<path d="M64 {height-70}H1536" stroke="#30443f"/>',
             text(64, height-29, tr("PARAMETRIC GEARS  /  NATIVE ORCASLICER PLUGIN", "ENGRENAGENS PARAMÉTRICAS  /  PLUGIN NATIVO DO ORCASLICER"), 16, "#9cb8af", 400, 1.5),
             text(1536, height-46, tr("FREE + OPEN SOURCE", "GRATUITO + CÓDIGO ABERTO"), 14, ACCENT, 600, 1.5).replace('<text ', '<text text-anchor="end" ', 1),
             text(1536, height-15, "By @VictorFernande", 20, "#eaf4f0", 600).replace('<text ', '<text text-anchor="end" ', 1)]
    return lines


def mesh_svg(mesh, x, y, width, height, color=(21, 223, 174), azimuth=-45, altitude=32):
    """Orthographic editorial view of actual mesh triangles; no invented tooth shapes."""
    az, al = np.radians([azimuth, altitude])
    right = np.array([-np.sin(az), np.cos(az), 0.0])
    camera = np.array([np.cos(az)*np.cos(al), np.sin(az)*np.cos(al), np.sin(al)])
    up = np.cross(camera, right)
    verts = mesh.vertices.astype(float)
    xy = np.column_stack((verts @ right, -(verts @ up)))
    lo, hi = xy.min(axis=0), xy.max(axis=0)
    scale = min(width/(hi[0]-lo[0]), height/(hi[1]-lo[1]))
    xy = (xy-(lo+hi)/2)*scale + [x+width/2, y+height/2]
    depth = verts @ camera
    faces = mesh.triangles
    normals = mesh.face_normals.astype(float)
    visible = np.flatnonzero(normals @ camera > 1e-6)
    visible = visible[np.argsort(depth[faces[visible]].mean(axis=1))]
    light = np.array([-.35, -.45, 1.0]); light /= np.linalg.norm(light)
    shade = np.clip(.43 + .57*np.maximum(0, normals @ light), .35, 1)
    parts = ['<g stroke-linejoin="round">']
    last_fill, paths = None, []
    def flush():
        if paths:
            parts.append(f'<path d="{"".join(paths)}" fill="{last_fill}" stroke="{last_fill}" stroke-width="0.35"/>')
            paths.clear()
    for i in visible:
        rgb = np.clip(np.array(color)*shade[i], 0, 255).astype(int)
        fill = '#'+''.join(f'{v:02x}' for v in rgb)
        if fill != last_fill:
            flush()
            last_fill = fill
        points = xy[faces[i]]
        paths.append(f'M{points[0,0]:.3f},{points[0,1]:.3f}L{points[1,0]:.3f},{points[1,1]:.3f}L{points[2,0]:.3f},{points[2,1]:.3f}Z')
    flush()
    parts.append('</g>')
    return ''.join(parts)


def params(kind="herringbone"):
    return normalize_params({"gear_type": kind, "module_mm": 2, "helix_angle_deg": 35,
                             "face_width_mm": 16, "gear": {"teeth": 28, "bore_type": "round",
                             "bore_diameter_mm": 9, "lightening_mode": "solid"}})


def write(name, parts):
    target = OUT / (name + '.svg')
    target.write_text('\n'.join(parts) + '\n</svg>\n', encoding='utf-8', newline='\n')
    print(f'{target.name}: {target.stat().st_size:,} bytes')


def main():
    global LANG
    OUT.mkdir(parents=True, exist_ok=True)
    meshes = {kind: generate_gear_mesh(params(kind), which="gear", resolution="low")
              for kind in ("spur", "helical", "herringbone")}
    screenshot = base64.b64encode((ROOT/'assets'/'Gear2.png').read_bytes()).decode('ascii')
    kit = generate_fit_test_kit(params('spur'))
    # Geometry is shared; only the editorial text changes between languages.
    views = {kind: mesh_svg(mesh, 0, 0, 432, 280) for kind,mesh in meshes.items()}
    for LANG in ("en", "pt-BR"):
        p = frame(900, tr("01 / DESIGN", "01 / PROJETE"))
        p += [text(64, 202, tr("FROM AN IDEA", "DA IDEIA À PEÇA"), 21, ACCENT, 600, 3),
              text(58, 309, tr("YOUR GEARS.", "ENGRENAGENS."), tr(88, 73), weight=750),
              text(58, 411, tr("YOUR RULES.", "DO SEU JEITO."), tr(88, 73), ACCENT, 750),
              text(64, 493, tr("Design, inspect and export gears.", "Projete, inspecione e exporte."), 30),
              text(64, 539, tr("Without leaving OrcaSlicer.", "Sem sair do OrcaSlicer."), 30, "#9cb8af"),
              '<rect x="64" y="601" width="610" height="56" rx="28" fill="#19362e" stroke="#2e6b57"/>',
              text(88, 638, tr("SPUR  /  HELICAL  /  HERRINGBONE", "RETAS  /  HELICOIDAIS  /  ESPINHA DE PEIXE"), 20, ACCENT, 600),
              text(64, 748, tr("LIVE PREVIEW", "PRÉVIA INTERATIVA"), 19, weight=700, spacing=2),
              text(64, 783, tr("3D simulation + 2D meshing loupe", "Simulação 3D + lupa 2D de engrenamento"), 23, "#9cb8af"),
              mesh_svg(meshes["herringbone"], 795, 155, 750, 590),
              text(1030, 788, tr("ACTUAL PLUGIN GEOMETRY", "GEOMETRIA REAL DO PLUGIN"), 16, "#9cb8af", 400, 2)]
        write('01-gear-studio-'+LANG, p)

        p = frame(900, tr("02 / PROFILES", "02 / PERFIS"))
        p += [text(64, 204, tr("ONE STUDIO. THREE TOOTH STYLES.", "UM ESTÚDIO. TRÊS TIPOS DE DENTES."), 55, weight=700),
              text(64, 253, tr("Set the ratio, module, face width and shaft connection for your mechanism.", "Ajuste a relação, o módulo, a largura e a conexão com o eixo do seu mecanismo."), 26, "#9cb8af")]
        cards = [('spur',tr('SPUR','RETAS'),tr('Straight teeth. A classic starting point.','Dentes retos. Um ponto de partida clássico.')),
                 ('helical',tr('HELICAL','HELICOIDAIS'),tr('Angled teeth with adjustable helix.','Dentes inclinados, com hélice ajustável.')),
                 ('herringbone',tr('HERRINGBONE','ESPINHA DE PEIXE'),tr('Opposed helices in one gear body.','Duas hélices opostas no mesmo corpo.'))]
        for i,(kind,title,subtitle) in enumerate(cards):
            x = 64 + i*500
            p += [f'<rect x="{x}" y="300" width="472" height="480" rx="20" fill="#172123" stroke="#30443f"/>',
                  text(x+25, 347, f'0{i+1}', 19, ACCENT, 600, 2),
                  f'<g transform="translate({x+20},370)">{views[kind]}</g>',
                  text(x+25, 713, title, 28, weight=700),
                  text(x+25, 754, subtitle, 18, "#9cb8af")]
        write('02-tooth-styles-'+LANG, p)

        p = frame(900, tr("03 / INSPECT", "03 / INSPECIONE"))
        p += [text(64, 247, tr("EVERY ADJUSTMENT.", "CADA AJUSTE."), 58, weight=700),
              text(64, 325, tr("IN VIEW.", "À SUA VISTA."), 64, ACCENT, 700),
              text(64, 417, tr("Parametric controls and live 3D.", "Controles paramétricos e prévia 3D."), 28),
              text(64, 462, tr("Explore meshing in the same workspace.", "Explore o engrenamento no mesmo lugar."), 26, "#9cb8af"),
              text(64, 573, tr("01   PRESETS + CUSTOM VALUES", "01   PRESETS + AJUSTES LIVRES"), 22, ACCENT, 600),
              text(64, 635, tr("02   ROTATION + 2D LOUPE", "02   SIMULAÇÃO + LUPA 2D"), 22, ACCENT, 600),
              text(64, 697, tr("03   STL / 3MF EXPORT", "03   EXPORTAÇÃO STL / 3MF"), 22, ACCENT, 600),
              '<rect x="704" y="175" width="832" height="580" rx="14" fill="#1d2528" stroke="#496057"/>',
              f'<image href="data:image/png;base64,{screenshot}" x="716" y="187" width="808" height="556" preserveAspectRatio="xMidYMid meet"/>',
              text(925, 788, tr("ACTUAL PLUGIN SCREENSHOT", "CAPTURA REAL DO PLUGIN"), 16, "#9cb8af", 400, 2)]
        write('03-live-workspace-'+LANG, p)

        p = frame(900, tr("04 / CALIBRATE", "04 / CALIBRE"))
        p += [text(64, 212, tr("START SMALL.", "TESTE ANTES."), 71, weight=750),
              text(64, 302, tr("CALIBRATE", "AJUSTE O"), 71, ACCENT, 750),
              text(64, 392, tr("THE FIT.", "ENCAIXE."), 71, ACCENT, 750),
              text(64, 472, tr("Check tooth engagement and shaft clearance", "Confira o engrenamento e a folga do eixo"), 26),
              text(64, 514, tr("with the dedicated fit-test kit.", "com o kit de teste de encaixe."), 26, "#9cb8af"),
              text(64, 607, tr("01  TWO TOOTH SECTORS", "01  DOIS SETORES DENTADOS"), 22, weight=600, spacing=1),
              text(64, 659, tr("02  TWO-PIN CENTER-DISTANCE JIG", "02  GABARITO DE CENTROS COM DOIS PINOS"), 22, weight=600, spacing=1),
              text(64, 711, tr("03  FOUR-STEP BORE GAUGE", "03  RÉGUA DE FUROS COM QUATRO FOLGAS"), 22, weight=600, spacing=1),
              text(64, 788, tr("Fit depends on material and printer calibration.", "O encaixe depende do material e da calibração."), 20, "#9cb8af")]
        layout = [('sector_pinion', 810, 170, tr('PINION SECTOR','SETOR DO PINHÃO')), ('sector_gear',1190,170,tr('GEAR SECTOR','SETOR DA COROA')),
                  ('center_jig_base',810,500,tr('CENTER-DISTANCE JIG','GABARITO DE CENTROS')), ('bore_fit_gauge',1190,500,tr('BORE GAUGE','RÉGUA DE FUROS'))]
        for key,x,y,label in layout:
            p += [f'<rect x="{x-12}" y="{y-15}" width="350" height="300" rx="18" fill="#172123" stroke="#30443f"/>',
                  mesh_svg(kit[key],x+5,y+10,310,210, (239,176,99) if key=='bore_fit_gauge' else (21,223,174)),
                  text(x+9,y+261,label,17,"#9cb8af",600,1)]
        write('04-fit-test-kit-'+LANG,p)


if __name__ == '__main__':
    main()
