"""Small, offline source-text catalog. Geometry, identifiers and user text are never translated."""
from __future__ import annotations
import re

SUPPORTED_LANGUAGES = ("pt", "en", "es", "it", "fr", "de", "ja")
LANGUAGE_NAMES = ("Português", "English", "Español", "Italiano", "Français", "Deutsch", "日本語")


def normalize_language(value: object, default: str = "pt") -> str:
    raw = str(value or "").strip().lower().split(".", 1)[0].replace("_", "-")
    if not raw:
        return default if default in SUPPORTED_LANGUAGES else "en"
    short = raw.split("-", 1)[0]
    return short if short in SUPPORTED_LANGUAGES else "en"


# One English source and five translations per row; numeric placeholders stay verbatim.
# Kept as readable text in the wheel and source repository, with no online translator.
_GEAR_TRANSLATION_ROWS = """Randomize|Aleatorio|Casuale|Aléatoire|Zufällig|ランダム
Meshing|Engrane|Ingranamento|Engrènement|Zahneingriff|かみ合い
Shafts & Hubs|Ejes y cubos|Alberi e mozzi|Arbres et moyeux|Wellen und Naben|軸とハブ
Diagnostics|Diagnóstico|Diagnostica|Diagnostic|Diagnose|診断
Presets|Preajustes|Preimpostazioni|Préréglages|Vorlagen|プリセット
Mechanical Presets|Preajustes mecánicos|Preimpostazioni meccaniche|Préréglages mécaniques|Mechanische Vorlagen|機械プリセット
+ Save|+ Guardar|+ Salva|+ Enregistrer|+ Speichern|+ 保存
Save|Guardar|Salva|Enregistrer|Speichern|保存
All|Todos|Tutti|Tous|Alle|すべて
Spur/Ind|Rectos/Ind|Dritti/Ind|Droits/Ind|Gerade/Ind|平歯車・産業用
Helical|Helicoidal|Elicoidale|Hélicoïdal|Schrägverzahnt|はすば歯車
Herringbone|Doble hélice|Bielicoidale|Chevrons|Pfeilverzahnt|やまば歯車
Robotics/Fit|Robótica/Ajuste|Robotica/Accoppiamento|Robotique/Ajustage|Robotik/Passung|ロボット・はめあい
Saved|Guardados|Salvate|Enregistrés|Gespeichert|保存済み
Transmission & Helix|Transmisión y hélice|Trasmissione ed elica|Transmission et hélice|Übersetzung und Schrägung|伝達とねじれ
Spur|Dientes rectos|Denti dritti|Denture droite|Geradverzahnt|平歯車
Herringbone (V)|Doble hélice (V)|Bielicoidale (V)|Chevrons (V)|Pfeilverzahnt (V)|やまば歯車（V）
Quick Helix Angle|Ángulo de hélice rápido|Angolo d'elica rapido|Angle d'hélice rapide|Schrägungswinkel schnell|ねじれ角の簡易設定
Right-Hand (G1 R / G2 L)|Derecha (G1 D / G2 I)|Destra (G1 D / G2 S)|Droite (G1 D / G2 G)|Rechts (G1 R / G2 L)|右ねじれ（G1 右 / G2 左）
Left-Hand (G1 L / G2 R)|Izquierda (G1 I / G2 D)|Sinistra (G1 S / G2 D)|Gauche (G1 G / G2 D)|Links (G1 L / G2 R)|左ねじれ（G1 左 / G2 右）
⇄ Swap Pinion / Gear (Z1 ↔ Z2)|⇄ Invertir piñón / rueda (Z1 ↔ Z2)|⇄ Scambia pignone / ruota (Z1 ↔ Z2)|⇄ Inverser pignon / roue (Z1 ↔ Z2)|⇄ Ritzel / Rad tauschen (Z1 ↔ Z2)|⇄ ピニオン / 歯車を交換（Z1 ↔ Z2）
Tooth Height (Factor × | mm)|Altura del diente (factor × / mm)|Altezza del dente (fattore × / mm)|Hauteur de dent (facteur × / mm)|Zahnhöhe (Faktor × / mm)|歯たけ（係数 × / mm）
ISO Standard 1.00×|ISO estándar 1.00×|ISO standard 1.00×|ISO standard 1.00×|ISO Standard 1.00×|ISO 標準 1.00×
Heavy Stub 0.75×|Diente corto robusto 0.75×|Dente ribassato robusto 0.75×|Dent courte renforcée 0.75×|Robuste Kurzverzahnung 0.75×|高強度低歯 0.75×
High Contact 1.20×|Alto contacto 1.20×|Elevato ricoprimento 1.20×|Grand rapport de conduite 1.20×|Hohe Überdeckung 1.20×|高かみ合い率 1.20×
Auto Anti-Undercut Shift (x)|Corrección automática del socavado (x)|Correzione automatica del sottotaglio (x)|Déport automatique anti-détalonnage (x)|Automatische Unterschnittkorrektur (x)|切下げ防止の自動転位（x）
Bores, Hubs & Lightening|Agujeros, cubos y aligeramiento|Fori, mozzi e alleggerimento|Alésages, moyeux et allègement|Bohrungen, Naben und Gewichtsreduktion|穴・ハブ・肉抜き
⚙ Pinion G1 (Driver)|⚙ Piñón G1 (motriz)|⚙ Pignone G1 (motore)|⚙ Pignon G1 (menant)|⚙ Ritzel G1 (Antrieb)|⚙ ピニオン G1（駆動）
⚙ Gear G2 (Driven)|⚙ Rueda G2 (conducida)|⚙ Ruota G2 (condotta)|⚙ Roue G2 (menée)|⚙ Rad G2 (Abtrieb)|⚙ 歯車 G2（従動）
Shaft / Bore Type (G1)|Tipo de eje / agujero (G1)|Tipo albero / foro (G1)|Type d'arbre / alésage (G1)|Wellen- / Bohrungstyp (G1)|軸・穴の種類（G1）
Shaft / Bore Type (G2)|Tipo de eje / agujero (G2)|Tipo albero / foro (G2)|Type d'arbre / alésage (G2)|Wellen- / Bohrungstyp (G2)|軸・穴の種類（G2）
No Bore (Solid)|Sin agujero (macizo)|Senza foro (pieno)|Sans alésage (plein)|Ohne Bohrung (voll)|穴なし（中実）
Round Shaft|Eje redondo|Albero tondo|Arbre rond|Rundwelle|丸軸
D-Shaft (NEMA / Motor)|Eje D (NEMA / motor)|Albero a D (NEMA / motore)|Arbre en D (NEMA / moteur)|D-Welle (NEMA / Motor)|D 軸（NEMA・モーター）
Double-D Shaft|Eje doble D|Albero a doppia D|Arbre double D|Doppel-D-Welle|両側 D 軸
Hex Bore (Across-Flats)|Agujero hexagonal (entre caras)|Foro esagonale (tra facce)|Alésage hexagonal (sur plats)|Sechskantbohrung (Schlüsselweite)|六角穴（二面幅）
DIN Keyway Bore|Chavetero DIN|Foro con cava DIN|Alésage à clavette DIN|DIN-Passfedernut|DIN キー溝穴
Raised Central Hub|Cubo central saliente|Mozzo centrale sporgente|Moyeu central saillant|Vorstehende Zentralnabe|突き出しハブ
Bearing / Bolt Recess|Alojamiento de rodamiento / tornillo|Sede cuscinetto / vite|Logement de roulement / vis|Lager- / Schraubensenkung|ベアリング・ボルト座ぐり
Top (+Z)|Superior (+Z)|Superiore (+Z)|Dessus (+Z)|Oben (+Z)|上面（+Z）
Bottom (Z=0)|Inferior (Z=0)|Inferiore (Z=0)|Dessous (Z=0)|Unten (Z=0)|底面（Z=0）
Both Sides|Ambos lados|Entrambi i lati|Deux côtés|Beide Seiten|両側
Body Mass Lightening|Aligeramiento del cuerpo|Alleggerimento del corpo|Allègement du corps|Gewichtsreduktion des Körpers|本体の肉抜き
Solid Gear Body|Cuerpo macizo|Corpo pieno|Corps plein|Voller Radkörper|中実歯車
Recessed Web Pocket|Alma rebajada|Anima ribassata|Voile évidé|Vertiefter Steg|薄肉ウェブ
Circular Lightening Holes|Agujeros circulares de aligeramiento|Fori circolari di alleggerimento|Trous circulaires d'allègement|Runde Gewichtsreduktionsbohrungen|円形肉抜き穴
⚙ Meshed Pair|⚙ Par engranado|⚙ Coppia ingranata|⚙ Paire engrenée|⚙ Zahnradpaar im Eingriff|⚙ かみ合いペア
🖨 Build Plate|🖨 Placa de impresión|🖨 Piano di stampa|🖨 Plateau d'impression|🖨 Druckplatte|🖨 ビルドプレート
🧪 Quick Fit-Test Kit|🧪 Kit de ajuste rápido|🧪 Kit rapido di accoppiamento|🧪 Kit d'ajustage rapide|🧪 Schnell-Passungstest|🧪 簡易はめあい試験キット
🔥 Overhang|🔥 Voladizo|🔥 Sbalzo|🔥 Surplomb|🔥 Überhang|🔥 オーバーハング
⚡ 3D Forces|⚡ Fuerzas 3D|⚡ Forze 3D|⚡ Forces 3D|⚡ 3D-Kräfte|⚡ 3D 力表示
⌗ Wire|⌗ Malla|⌗ Reticolo|⌗ Filaire|⌗ Drahtgitter|⌗ ワイヤーフレーム
Loads & Mesh|Cargas y malla|Carichi e ingranamento|Charges et maillage|Lasten und Eingriff|荷重とかみ合い
Center Dist a|Distancia entre centros a|Interasse a|Entraxe a|Achsabstand a|中心距離 a
Tangential Ft|Tangencial Ft|Tangenziale Ft|Tangentielle Ft|Tangential Ft|接線力 Ft
Radial Fr|Radial Fr|Radiale Fr|Radiale Fr|Radial Fr|半径方向力 Fr
Axial Thrust Fa|Empuje axial Fa|Spinta assiale Fa|Poussée axiale Fa|Axialkraft Fa|軸方向力 Fa
Perspective|Perspectiva|Prospettiva|Perspective|Perspektive|透視図
Top (Meshing)|Superior (engrane)|Dall'alto (ingranamento)|Dessus (engrènement)|Oben (Eingriff)|上面（かみ合い）
Front (Helix)|Frontal (hélice)|Frontale (elica)|Face (hélice)|Vorne (Schrägung)|正面（ねじれ）
Reset|Restablecer|Ripristina|Réinitialiser|Zurücksetzen|リセット
Angle θ₁|Ángulo θ₁|Angolo θ₁|Angle θ₁|Winkel θ₁|角度 θ₁
Center-Distance Offset (Δa):|Desplazamiento entre centros (Δa):|Variazione interasse (Δa):|Décalage d'entraxe (Δa) :|Achsabstandsänderung (Δa):|中心距離の補正（Δa）：
Reset 0.00 mm|Restablecer 0.00 mm|Ripristina 0.00 mm|Réinitialiser 0.00 mm|Auf 0.00 mm zurücksetzen|0.00 mm に戻す
🔍 2D Tooth-Mesh Loupe & Pressure Line|🔍 Lupa 2D del engrane y línea de presión|🔍 Lente 2D dell'ingranamento e retta di pressione|🔍 Loupe 2D d'engrènement et ligne de pression|🔍 2D-Eingriffslupe und Eingriffslinie|🔍 2D かみ合い拡大・作用線
INTERFERENCE / JAMMING DETECTED|INTERFERENCIA / BLOQUEO DETECTADO|INTERFERENZA / BLOCCAGGIO RILEVATO|INTERFÉRENCE / BLOCAGE DÉTECTÉ|KOLLISION / BLOCKIERUNG ERKANNT|干渉・かじりを検出
FDM Clearances & Input Torque|Holguras FDM y par de entrada|Giochi FDM e coppia motrice|Jeux FDM et couple moteur|FDM-Spiel und Antriebsmoment|FDM すきまと入力トルク
Meshing & Fit Diagnostics|Diagnóstico de engrane y ajuste|Diagnostica ingranamento e accoppiamento|Diagnostic d'engrènement et d'ajustage|Eingriffs- und Passungsdiagnose|かみ合い・はめあい診断
Contact Ratio & Involute|Relación de contacto y evolvente|Ricoprimento ed evolvente|Rapport de conduite et développante|Überdeckung und Evolvente|かみ合い率とインボリュート
Transverse ε_α|Transversal ε_α|Trasversale ε_α|Transversal ε_α|Profilüberdeckung ε_α|正面かみ合い率 ε_α
Axial Overlap ε_β|Recubrimiento axial ε_β|Ricoprimento assiale ε_β|Recouvrement axial ε_β|Sprungüberdeckung ε_β|重なりかみ合い率 ε_β
Total Contact ε_γ|Contacto total ε_γ|Ricoprimento totale ε_γ|Conduite totale ε_γ|Gesamtüberdeckung ε_γ|全かみ合い率 ε_γ
Line of Action|Línea de acción|Retta d'azione|Ligne d'action|Eingriffslinie|作用線
Fit, Clearance & Kinematics|Ajuste, holgura y cinemática|Accoppiamento, gioco e cinematica|Ajustage, jeu et cinématique|Passung, Spiel und Kinematik|はめあい・すきま・運動学
Center Distance a|Distancia entre centros a|Interasse a|Entraxe a|Achsabstand a|中心距離 a
Min Tooth Clearance|Holgura mínima del diente|Gioco minimo tra denti|Jeu minimal entre dents|Mindestzahnspiel|最小歯面すきま
Output Torque (G2)|Par de salida (G2)|Coppia in uscita (G2)|Couple de sortie (G2)|Abtriebsmoment (G2)|出力トルク（G2）
Output Speed|Velocidad de salida|Velocità in uscita|Vitesse de sortie|Abtriebsdrehzahl|出力回転数
Mechanical FDM Printability|Impresión mecánica FDM|Stampabilità meccanica FDM|Imprimabilité mécanique FDM|Mechanische FDM-Druckbarkeit|機械部品の FDM 印刷性
Helix Overhang|Voladizo de hélice|Sbalzo dell'elica|Surplomb d'hélice|Schrägungsüberhang|ねじれのオーバーハング
Suggested Walls|Paredes recomendadas|Pareti consigliate|Parois conseillées|Empfohlene Wände|推奨外周数
Est. Weight / Time|Peso / tiempo estimados|Peso / tempo stimati|Poids / durée estimés|Geschätztes Gewicht / Zeit|推定重量・時間
Bed Footprint|Área en la placa|Ingombro sul piano|Emprise sur le plateau|Druckplattenfläche|プレート上の寸法
Export Package & Slicing|Paquete de exportación y laminado|Esportazione e slicing|Export et tranchage|Exportpaket und Slicing|書き出しとスライス
Target package:|Paquete de destino:|Pacchetto da esportare:|Éléments à exporter :|Zielpaket:|書き出す部品：
Separated Pair (Ready to Print)|Par separado (listo para imprimir)|Coppia separata (pronta da stampare)|Paire séparée (prête à imprimer)|Getrenntes Paar (druckbereit)|分離ペア（印刷用）
Pinion Only (G1)|Solo piñón (G1)|Solo pignone (G1)|Pignon seul (G1)|Nur Ritzel (G1)|ピニオンのみ（G1）
Driven Gear Only (G2)|Solo rueda conducida (G2)|Solo ruota condotta (G2)|Roue menée seule (G2)|Nur Abtriebsrad (G2)|従動歯車のみ（G2）
Quick Fit-Test Kit (Sectors + 2-Pin Jig + Shaft Gauge)|Kit rápido (sectores + base de 2 pines + calibre de eje)|Kit rapido (settori + dima a 2 perni + calibro albero)|Kit rapide (secteurs + gabarit à 2 axes + jauge d'arbre)|Schnelltest (Sektoren + 2-Stift-Lehre + Wellenlehre)|簡易キット（歯形片・2 ピン治具・軸ゲージ）
Full Suite (Gear Pair + Calibration Jigs)|Conjunto completo (par + calibres)|Set completo (coppia + dime)|Ensemble complet (paire + gabarits)|Komplettsatz (Paar + Kalibrierlehren)|全セット（歯車ペア・校正治具）
Places Pinion (G1) and Gear (G2) separated with safe gap on the build plate so teeth never fuse.|Coloca G1 y G2 separados con margen seguro para evitar la unión de dientes.|Posiziona G1 e G2 separati sul piano con un margine sicuro per evitare la fusione dei denti.|Place G1 et G2 séparés avec un écart sûr pour éviter la fusion des dents.|Platziert G1 und G2 mit sicherem Abstand auf der Druckplatte, damit die Zähne nicht verschmelzen.|歯同士が融着しないよう G1 と G2 を安全な間隔でプレートに配置します。
Exports only the selected gear centered on the printer build plate.|Exporta solo el engranaje elegido centrado en la placa.|Esporta solo l'ingranaggio selezionato al centro del piano.|Exporte uniquement la roue sélectionnée au centre du plateau.|Exportiert nur das gewählte Zahnrad mittig auf die Druckplatte.|選択した歯車だけをプレート中央に書き出します。
10-minute calibration print: two 5-tooth sectors + 2-pin center-distance base jig + 4-hole shaft gauge!|Calibración de unos 10 min: dos sectores de 5 dientes, base de 2 pines y calibre de 4 agujeros.|Calibrazione di circa 10 min: due settori da 5 denti, base a 2 perni e calibro a 4 fori.|Étalonnage d'environ 10 min : deux secteurs de 5 dents, base à 2 axes et jauge à 4 trous.|Kalibrierung in etwa 10 Min.: zwei 5-Zahn-Sektoren, 2-Stift-Achsabstandslehre und 4-Loch-Wellenlehre.|約 10 分を目標とする校正印刷：5 歯の歯形片 2 個・2 ピン中心距離治具・4 穴軸ゲージ。
Complete build plate suite: full G1 + G2 gear pair alongside center-distance jig and shaft gauge.|Placa completa con G1 + G2, base de distancia entre centros y calibre de eje.|Piano completo con G1 + G2, dima dell'interasse e calibro albero.|Plateau complet avec G1 + G2, gabarit d'entraxe et jauge d'arbre.|Komplette Druckplatte mit G1 + G2, Achsabstandslehre und Wellenlehre.|G1・G2 のペア、中心距離治具、軸ゲージをまとめて配置します。
Auto-Configure Mechanical Slicing (4–6 solid walls + Gyroid)|Configurar laminado mecánico (4–6 paredes + Gyroid)|Configura slicing meccanico (4–6 pareti + Gyroid)|Configurer le tranchage mécanique (4–6 parois + Gyroid)|Mechanisches Slicing konfigurieren (4–6 Wände + Gyroid)|機械用スライスを自動設定（外周 4～6 本・Gyroid）
Send to OrcaSlicer Plater|Enviar a la placa de OrcaSlicer|Invia al piano di OrcaSlicer|Envoyer au plateau OrcaSlicer|An OrcaSlicer-Druckplatte senden|OrcaSlicer のプレートへ送信
Export .3MF|Exportar .3MF|Esporta .3MF|Exporter .3MF|.3MF exportieren|.3MF 書き出し
Export .STL|Exportar .STL|Esporta .STL|Exporter .STL|.STL exportieren|.STL 書き出し
OPTIMAL|ÓPTIMO|OTTIMALE|OPTIMAL|OPTIMAL|良好
WARNING|ATENCIÓN|ATTENZIONE|ATTENTION|WARNUNG|注意
CRITICAL|CRÍTICO|CRITICO|CRITIQUE|KRITISCH|重大
Axial Thrust: 0.0 N (Spur)|Empuje axial: 0.0 N (rectos)|Spinta assiale: 0.0 N (dritti)|Poussée axiale : 0.0 N (droits)|Axialkraft: 0.0 N (gerade)|軸方向力：0.0 N（平歯車）
Axial Thrust: 0.0 N (Balanced V)|Empuje axial: 0.0 N (V equilibrada)|Spinta assiale: 0.0 N (V bilanciata)|Poussée axiale : 0.0 N (V équilibré)|Axialkraft: 0.0 N (V ausgeglichen)|軸方向力：0.0 N（平衡 V）
Axial Thrust Z: {fa} N ({b}° Helix)|Empuje axial Z: {fa} N (hélice {b}°)|Spinta assiale Z: {fa} N (elica {b}°)|Poussée axiale Z : {fa} N (hélice {b}°)|Axialkraft Z: {fa} N ({b}° Schrägung)|軸方向力 Z：{fa} N（ねじれ {b}°）
Generated printable gear pair!|¡Par de engranajes generado!|Coppia di ingranaggi generata!|Paire d'engrenages générée !|Zahnradpaar erzeugt!|歯車ペアを生成しました。
Mechanical preset saved!|¡Preajuste mecánico guardado!|Preimpostazione meccanica salvata!|Préréglage mécanique enregistré !|Mechanische Vorlage gespeichert!|機械プリセットを保存しました。
Helix Angle (β)|Ángulo de hélice (β)|Angolo d'elica (β)|Angle d'hélice (β)|Schrägungswinkel (β)|ねじれ角（β）
Pinion Teeth (G1)|Dientes del piñón (G1)|Denti del pignone (G1)|Dents du pignon (G1)|Ritzelzähne (G1)|ピニオンの歯数（G1）
Driven Gear Teeth (G2)|Dientes de la rueda (G2)|Denti della ruota (G2)|Dents de la roue (G2)|Rad-Zähnezahl (G2)|従動歯車の歯数（G2）
Normal Module (m_n)|Módulo normal (m_n)|Modulo normale (m_n)|Module normal (m_n)|Normalmodul (m_n)|歯直角モジュール（m_n）
Pressure Angle (α_n)|Ángulo de presión (α_n)|Angolo di pressione (α_n)|Angle de pression (α_n)|Eingriffswinkel (α_n)|歯直角圧力角（α_n）
Face Width (b)|Ancho de cara (b)|Larghezza fascia (b)|Largeur de denture (b)|Zahnbreite (b)|歯幅（b）
Addendum Coeff (h_a*)|Coeficiente de cabeza (h_a*)|Coefficiente di testa (h_a*)|Coefficient de saillie (h_a*)|Kopfhöhenfaktor (h_a*)|歯末のたけ係数（h_a*）
Root Clearance Coeff (c*)|Coeficiente de holgura de fondo (c*)|Coefficiente gioco di fondo (c*)|Coefficient de jeu de fond (c*)|Kopfspielfaktor (c*)|頂げき係数（c*）
Root Fillet Coeff (ρ_f*)|Coeficiente del radio de raíz (ρ_f*)|Coefficiente raccordo al piede (ρ_f*)|Coefficient de congé de pied (ρ_f*)|Fußrundungsfaktor (ρ_f*)|歯元すみ肉係数（ρ_f*）
Tip Chamfer Coeff (c_k*)|Coeficiente de chaflán de punta (c_k*)|Coefficiente smusso di testa (c_k*)|Coefficient de chanfrein de tête (c_k*)|Kopffasenfaktor (c_k*)|歯先面取り係数（c_k*）
Profile Shift G1 (x₁)|Desplazamiento de perfil G1 (x₁)|Spostamento profilo G1 (x₁)|Déport de profil G1 (x₁)|Profilverschiebung G1 (x₁)|転位係数 G1（x₁）
Profile Shift G2 (x₂)|Desplazamiento de perfil G2 (x₂)|Spostamento profilo G2 (x₂)|Déport de profil G2 (x₂)|Profilverschiebung G2 (x₂)|転位係数 G2（x₂）
Circumferential Backlash|Holgura circunferencial|Gioco circonferenziale|Jeu circonférentiel|Umfangsspiel|円周方向バックラッシ
FDM XY Compensation|Compensación XY FDM|Compensazione XY FDM|Compensation XY FDM|FDM-XY-Kompensation|FDM XY 補正
Anti-Elephant-Foot Chamfer|Chaflán antipata de elefante|Smusso anti piede d'elefante|Chanfrein anti-pied d'éléphant|Elefantenfußfase|象の足防止面取り
Center-Distance Offset (Δa)|Desplazamiento entre centros (Δa)|Variazione interasse (Δa)|Décalage d'entraxe (Δa)|Achsabstandsänderung (Δa)|中心距離補正（Δa）
Input Torque on G1 (T₁)|Par de entrada en G1 (T₁)|Coppia motrice G1 (T₁)|Couple moteur G1 (T₁)|Antriebsmoment G1 (T₁)|G1 の入力トルク（T₁）
Nominal Shaft Diameter|Diámetro nominal de eje|Diametro nominale albero|Diamètre nominal d'arbre|Wellennenndurchmesser|軸の呼び径
Diametral Bore Clearance|Holgura diametral del agujero|Gioco diametrale del foro|Jeu diamétral d'alésage|Diametrales Bohrungsspiel|穴の直径すきま
D-Flat Depth|Profundidad del plano D|Profondità piano D|Profondeur du méplat D|D-Abflachungstiefe|D カット深さ
Keyway Width|Ancho de chavetero|Larghezza cava|Largeur de rainure|Nutbreite|キー溝幅
Keyway Depth|Profundidad de chavetero|Profondità cava|Profondeur de rainure|Nuttiefe|キー溝深さ
Hub Diameter (G1)|Diámetro de cubo (G1)|Diametro mozzo (G1)|Diamètre de moyeu (G1)|Nabendurchmesser (G1)|ハブ径（G1）
Hub Height (G1)|Altura de cubo (G1)|Altezza mozzo (G1)|Hauteur de moyeu (G1)|Nabenhöhe (G1)|ハブ高さ（G1）
Recess Diameter (G1)|Diámetro del rebaje (G1)|Diametro sede (G1)|Diamètre de logement (G1)|Senkungsdurchmesser (G1)|座ぐり径（G1）
Recess Depth (G1)|Profundidad del rebaje (G1)|Profondità sede (G1)|Profondeur de logement (G1)|Senkungstiefe (G1)|座ぐり深さ（G1）
Web Thickness (G1)|Espesor de alma (G1)|Spessore anima (G1)|Épaisseur de voile (G1)|Stegdicke (G1)|ウェブ厚さ（G1）
Lightening Hole Count (G1)|Número de agujeros de aligeramiento (G1)|Numero fori di alleggerimento (G1)|Nombre de trous d'allègement (G1)|Anzahl Entlastungsbohrungen (G1)|肉抜き穴数（G1）
Lightening Hole Ø (G1)|Ø de agujeros de aligeramiento (G1)|Ø fori di alleggerimento (G1)|Ø des trous d'allègement (G1)|Ø Entlastungsbohrungen (G1)|肉抜き穴径（G1）
Hub Diameter (G2)|Diámetro de cubo (G2)|Diametro mozzo (G2)|Diamètre de moyeu (G2)|Nabendurchmesser (G2)|ハブ径（G2）
Hub Height (G2)|Altura de cubo (G2)|Altezza mozzo (G2)|Hauteur de moyeu (G2)|Nabenhöhe (G2)|ハブ高さ（G2）
Recess Diameter (G2)|Diámetro del rebaje (G2)|Diametro sede (G2)|Diamètre de logement (G2)|Senkungsdurchmesser (G2)|座ぐり径（G2）
Recess Depth (G2)|Profundidad del rebaje (G2)|Profondità sede (G2)|Profondeur de logement (G2)|Senkungstiefe (G2)|座ぐり深さ（G2）
Web Thickness (G2)|Espesor de alma (G2)|Spessore anima (G2)|Épaisseur de voile (G2)|Stegdicke (G2)|ウェブ厚さ（G2）
Lightening Hole Count (G2)|Número de agujeros de aligeramiento (G2)|Numero fori di alleggerimento (G2)|Nombre de trous d'allègement (G2)|Anzahl Entlastungsbohrungen (G2)|肉抜き穴数（G2）
Lightening Hole Ø (G2)|Ø de agujeros de aligeramiento (G2)|Ø fori di alleggerimento (G2)|Ø des trous d'allègement (G2)|Ø Entlastungsbohrungen (G2)|肉抜き穴径（G2）
Classic 1:2 Spur Reducer|Reductor recto clásico 1:2|Riduttore classico a denti dritti 1:2|Réducteur droit classique 1:2|Klassisches Stirnradgetriebe 1:2|標準平歯車減速機 1:2
Silent 45° Support-Free Helical|Helicoidal silencioso 45° sin soportes|Elicoidale silenzioso 45° senza supporti|Hélicoïdal silencieux 45° sans support|Leises 45°-Schrägrad ohne Stützen|静音 45° はすば歯車（サポート不要設計）
High-Torque Herringbone Extruder 1:4|Extrusor doble hélice de alto par 1:4|Estrusore bielicoidale ad alta coppia 1:4|Extrudeur à chevrons fort couple 1:4|Pfeilverzahnter Hochmoment-Extruder 1:4|高トルクやまば押出機 1:4
NEMA 17 5mm D-Shaft to M8 1:5|NEMA 17 eje D de 5 mm a M8 1:5|NEMA 17 albero D 5 mm a M8 1:5|NEMA 17 arbre D 5 mm vers M8 1:5|NEMA 17 D-Welle 5 mm auf M8 1:5|NEMA 17 D 軸 5 mm → M8 1:5
Heavy-Duty Stub Tooth Reducer|Reductor robusto de diente corto|Riduttore robusto a denti ribassati|Réducteur renforcé à dents courtes|Robustes Kurzverzahnungsgetriebe|高強度低歯減速機
Smooth High-Contact-Ratio Drive|Transmisión suave de alto contacto|Trasmissione fluida ad alto ricoprimento|Transmission douce à grand rapport de conduite|Ruhiger Antrieb mit hoher Überdeckung|高かみ合い率の滑らかな駆動
9-Tooth Shifted Micro Pinion|Micropiñón corregido de 9 dientes|Micropignone corretto a 9 denti|Micropignon déporté à 9 dents|Profilverschobenes 9-Zahn-Mikroritzel|9 歯転位マイクロピニオン
1:1 Synchronous 45° Helical|Helicoidal síncrono 45° 1:1|Elicoidale sincrono 45° 1:1|Hélicoïdal synchrone 45° 1:1|Synchrones 45°-Schrägrad 1:1|同期 45° はすば歯車 1:1
608ZZ Bearing-Seated Gear Pair|Par con alojamiento de rodamiento 608ZZ|Coppia con sede cuscinetto 608ZZ|Paire avec logement de roulement 608ZZ|Zahnradpaar mit 608ZZ-Lagersitz|608ZZ ベアリング座付きペア
Compact Robotics Module 1.25|Robótica compacta módulo 1.25|Robotica compatta modulo 1.25|Robotique compacte module 1.25|Kompakte Robotik Modul 1.25|小型ロボット用モジュール 1.25
Industrial Module 3.5 DIN Keyway|Industrial módulo 3.5 chavetero DIN|Industriale modulo 3.5 cava DIN|Industriel module 3.5 clavette DIN|Industrie Modul 3.5 DIN-Passfedernut|産業用モジュール 3.5 DIN キー溝
Quick FDM Fit Calibration Kit|Kit rápido de calibración FDM|Kit rapido di calibrazione FDM|Kit rapide d'étalonnage FDM|Schneller FDM-Passungskalibriersatz|簡易 FDM はめあい校正キット
Versatile ISO module 2.0 spur pair (16:32 teeth) with zero axial thrust.|Par recto ISO módulo 2.0 (16:32 dientes) sin empuje axial.|Coppia dritta ISO modulo 2.0 (16:32 denti), senza spinta assiale.|Paire droite ISO module 2.0 (16:32 dents), sans poussée axiale.|Vielseitiges ISO-Stirnradpaar Modul 2.0 (16:32 Zähne) ohne Axialkraft.|汎用 ISO モジュール 2.0 の平歯車ペア（16:32 歯）。軸方向力なし。
Support-free 45° helix angle for FDM with ultra-quiet progressive meshing (1:3).|Hélice FDM de 45° sin soportes con engrane progresivo silencioso (1:3).|Elica FDM 45° senza supporti e ingranamento progressivo silenzioso (1:3).|Hélice FDM à 45° sans support, engrènement progressif silencieux (1:3).|FDM-Schrägung 45° ohne Stützen mit leisem progressivem Eingriff (1:3).|FDM 向け 45° ねじれ角。サポート不要を目標とする静音の順次かみ合い（1:3）。
Self-centering V-shaped double helical pair (30°, 11:44) with zero net axial thrust.|Par doble hélice V autocentrante (30°, 11:44) sin empuje axial neto.|Coppia bielicoidale a V autocentrante (30°, 11:44) senza spinta assiale netta.|Paire à chevrons autocentrante (30°, 11:44), poussée axiale nette nulle.|Selbstzentrierendes V-Pfeilradpaar (30°, 11:44) ohne Nettoaxialkraft.|自己求心 V 型やまば歯車ペア（30°、11:44）。正味の軸方向力なし。
Direct 1:5 reduction stage coupling a NEMA 17 stepper (5mm D-shaft) to an M8 shaft.|Reducción directa 1:5 de motor NEMA 17 (eje D 5 mm) a eje M8.|Riduzione diretta 1:5 da NEMA 17 (albero D 5 mm) ad albero M8.|Réduction directe 1:5 de NEMA 17 (arbre D 5 mm) vers arbre M8.|Direkte Untersetzung 1:5 von NEMA 17 (5-mm-D-Welle) auf M8-Welle.|NEMA 17（5 mm D 軸）から M8 軸への直結 1:5 減速段。
Short stub tooth profile (0.75× addendum, 0.38× root fillet) for maximum bending strength.|Diente corto (cabeza 0.75×, radio de raíz 0.38×) para resistir flexión.|Dente ribassato (testa 0.75×, raccordo 0.38×) per resistenza a flessione.|Dent courte (saillie 0.75×, congé 0.38×) pour résistance en flexion.|Kurzverzahnung (Kopfhöhe 0.75×, Fußrundung 0.38×) für hohe Biegefestigkeit.|曲げ強度を重視した低歯形状（歯末 0.75×、すみ肉 0.38×）。
Tall addendum (1.20×) paired with a 35° helix for continuous multi-tooth load sharing.|Cabeza alta (1.20×) y hélice de 35° para repartir carga entre dientes.|Testa alta (1.20×) ed elica 35° per distribuire il carico su più denti.|Saillie haute (1.20×) et hélice 35° pour répartir la charge sur plusieurs dents.|Große Kopfhöhe (1.20×) und 35°-Schrägung für kontinuierliche Lastverteilung.|高い歯末（1.20×）と 35° ねじれで複数歯に連続的に荷重を分散。
Compact 9-tooth pinion with positive profile shift (+0.35) eliminating root undercut.|Piñón compacto de 9 dientes con corrección positiva (+0.35) contra socavado.|Pignone compatto a 9 denti con correzione positiva (+0.35) contro il sottotaglio.|Pignon compact à 9 dents et déport positif (+0.35) contre le détalonnage.|Kompaktes 9-Zahn-Ritzel mit positiver Profilverschiebung (+0.35) gegen Unterschnitt.|正転位（+0.35）で切下げを防ぐ小型 9 歯ピニオン。
Synchronous 1:1 pair (22:22 teeth) with 45° helix for smooth counter-rotating shafts.|Par síncrono 1:1 (22:22 dientes), hélice 45°, ejes contrarrotantes suaves.|Coppia sincrona 1:1 (22:22 denti), elica 45°, alberi controrotanti fluidi.|Paire synchrone 1:1 (22:22 dents), hélice 45°, arbres contrarotatifs fluides.|Synchronpaar 1:1 (22:22 Zähne), 45°-Schrägung für ruhigen Gegenlauf.|滑らかに逆回転する軸用の同期 1:1 ペア（22:22 歯、ねじれ 45°）。
Helical driven gear featuring a Ø22.2×7.0 mm pocket engineered for a standard 608ZZ bearing.|Rueda helicoidal con alojamiento Ø22.2×7.0 mm para rodamiento 608ZZ.|Ruota elicoidale con sede Ø22.2×7.0 mm per cuscinetto 608ZZ.|Roue hélicoïdale avec logement Ø22.2×7.0 mm pour roulement 608ZZ.|Schrägverzahntes Abtriebsrad mit Ø22.2×7.0-mm-Sitz für 608ZZ-Lager.|標準 608ZZ ベアリング用の Ø22.2×7.0 mm 座を備えた従動はすば歯車。
Fine-pitch herringbone drive (m=1.25, 35°, 16:48) with hex shaft/nut drive on the gear.|Doble hélice de paso fino (m=1.25, 35°, 16:48), eje/tuerca hexagonal en rueda.|Bielicoidale a passo fine (m=1.25, 35°, 16:48), albero/dado esagonale sulla ruota.|Chevrons à pas fin (m=1.25, 35°, 16:48), arbre/écrou hexagonal sur la roue.|Feines Pfeilradgetriebe (m=1.25, 35°, 16:48) mit Sechskantwelle/-mutter am Rad.|細かい歯のやまば駆動（m=1.25、35°、16:48）。従動側は六角軸・ナット用。
Heavy-duty module 3.5 gears (14:26) equipped with DIN keyway bores and reinforced hubs.|Engranajes robustos módulo 3.5 (14:26) con chaveteros DIN y cubos reforzados.|Ingranaggi robusti modulo 3.5 (14:26) con cave DIN e mozzi rinforzati.|Engrenages renforcés module 3.5 (14:26), rainures DIN et moyeux renforcés.|Robuste Zahnräder Modul 3.5 (14:26) mit DIN-Passfedernuten und verstärkten Naben.|DIN キー溝と補強ハブ付き高荷重用モジュール 3.5 歯車（14:26）。
Fast 10-minute calibration kit (45° sectors, 2-pin center-distance jig, and 4-step bore gauge).|Kit de calibración de unos 10 min (sectores 45°, base de 2 pines y calibre de 4 pasos).|Kit di calibrazione di circa 10 min (settori 45°, dima a 2 perni, calibro a 4 misure).|Kit d'étalonnage d'environ 10 min (secteurs 45°, gabarit à 2 axes, jauge à 4 mesures).|Kalibriersatz für etwa 10 Min. (45°-Sektoren, 2-Stift-Achsabstandslehre, 4-Stufen-Bohrungslehre).|約 10 分を目標とする校正キット（45° 歯形片・2 ピン中心距離治具・4 段階穴ゲージ）。
Ratio|Relación|Rapporto|Rapport|Übersetzung|歯数比
Out Speed|Velocidad de salida|Velocità in uscita|Vitesse de sortie|Abtriebsdrehzahl|出力回転数
Contact ε_γ|Contacto ε_γ|Ricoprimento ε_γ|Conduite ε_γ|Überdeckung ε_γ|かみ合い率 ε_γ
Clearance|Holgura|Gioco|Jeu|Spiel|すきま
COLLISION|COLISIÓN|COLLISIONE|COLLISION|KOLLISION|衝突
⚠ Supports|⚠ Soportes|⚠ Supporti|⚠ Supports|⚠ Stützen|⚠ サポート必要
✓ Support-free|✓ Sin soportes|✓ Senza supporti|✓ Sans support|✓ Stützenfrei|✓ サポート不要設計
⏸ Pause|⏸ Pausar|⏸ Pausa|⏸ Pause|⏸ Pause|⏸ 一時停止
▶ Play|▶ Girar|▶ Avvia|▶ Démarrer|▶ Start|▶ 再生
Delete|Eliminar|Elimina|Supprimer|Löschen|削除
Language|Idioma|Lingua|Langue|Sprache|言語
Undo (Ctrl+Z)|Deshacer (Ctrl+Z)|Annulla (Ctrl+Z)|Annuler (Ctrl+Z)|Rückgängig (Ctrl+Z)|元に戻す（Ctrl+Z）
Redo (Ctrl+Y)|Rehacer (Ctrl+Y)|Ripeti (Ctrl+Y)|Rétablir (Ctrl+Y)|Wiederholen (Ctrl+Y)|やり直し（Ctrl+Y）
Toggle Light/Dark Theme|Cambiar tema claro/oscuro|Tema chiaro/scuro|Thème clair/sombre|Hell/Dunkel umschalten|ライト・ダーク切替
Toggle Z / Y Cut Plane|Cambiar corte Z / Y|Cambia piano di taglio Z / Y|Plan de coupe Z / Y|Z-/Y-Schnittebene umschalten|Z・Y 断面を切替
Play / Pause (Space)|Girar / pausar (Espacio)|Avvia / pausa (Spazio)|Lecture / pause (Espace)|Start / Pause (Leertaste)|再生・一時停止（スペース）
Toggle CW / CCW|Cambiar horario / antihorario|Cambia orario / antiorario|Sens horaire / antihoraire|Rechts-/Linkslauf umschalten|時計・反時計回りを切替
Expand / Collapse 2D Loupe|Expandir / contraer lupa 2D|Espandi / riduci lente 2D|Déplier / replier la loupe 2D|2D-Lupe auf-/zuklappen|2D 拡大表示を開閉
Open export folder|Abrir carpeta de exportaciones|Apri cartella esportazioni|Ouvrir le dossier d'export|Exportordner öffnen|書き出しフォルダーを開く
Gear pair name|Nombre del par|Nome della coppia|Nom de la paire|Name des Zahnradpaars|歯車ペア名
Preset name|Nombre del preajuste|Nome della preimpostazione|Nom du préréglage|Vorlagenname|プリセット名
Cancel|Cancelar|Annulla|Annuler|Abbrechen|キャンセル
OrcaSlicer host bridge not connected (Standalone Preview).|Puente OrcaSlicer desconectado (vista independiente).|Bridge OrcaSlicer non connesso (anteprima autonoma).|Pont OrcaSlicer déconnecté (aperçu autonome).|OrcaSlicer-Verbindung fehlt (eigenständige Vorschau).|OrcaSlicer に未接続です（単独プレビュー）。
Export complete.|Exportación completada.|Esportazione completata.|Export terminé.|Export abgeschlossen.|書き出しが完了しました。
Files exported.|Archivos exportados.|File esportati.|Fichiers exportés.|Dateien exportiert.|ファイルを書き出しました。
Import request sent.|Solicitud de importación enviada.|Richiesta di importazione inviata.|Demande d'import envoyée.|Importanfrage gesendet.|読み込み要求を送信しました。
45° Support-free|45° Sin soportes|45° Senza supporti|45° Sans support|45° Stützenfrei|45° サポート不要設計
✂ Z cut|✂ Corte Z|✂ Taglio Z|✂ Coupe Z|✂ Z-Schnitt|✂ Z 断面
✂ Y cut|✂ Corte Y|✂ Taglio Y|✂ Coupe Y|✂ Y-Schnitt|✂ Y 断面
Off|Desactivado|Disattivato|Désactivé|Aus|オフ
Gear Type|Tipo de engranaje|Tipo di ingranaggio|Type d'engrenage|Zahnradtyp|歯車の種類
Studio Sections|Secciones|Sezioni|Sections|Bereiche|セクション
Active OrcaSlicer Printer Profile|Perfil de impresora activo de OrcaSlicer|Profilo stampante attivo di OrcaSlicer|Profil d'imprimante OrcaSlicer actif|Aktives OrcaSlicer-Druckerprofil|OrcaSlicer の使用中のプリンタープロファイル
🎯 608ZZ Bearing Preset (Ø22.2×7mm)|🎯 Preajuste rodamiento 608ZZ (Ø22.2×7mm)|🎯 Preimpostazione cuscinetto 608ZZ (Ø22.2×7mm)|🎯 Préréglage roulement 608ZZ (Ø22.2×7mm)|🎯 608ZZ-Lagervorlage (Ø22.2×7mm)|🎯 608ZZ ベアリング設定（Ø22.2×7mm）
x₁ effective: {x1} · x₂ effective: {x2}{detail}|x₁ efectivo: {x1} · x₂ efectivo: {x2}{detail}|x₁ effettivo: {x1} · x₂ effettivo: {x2}{detail}|x₁ effectif : {x1} · x₂ effectif : {x2}{detail}|x₁ wirksam: {x1} · x₂ wirksam: {x2}{detail}|x₁ 実効：{x1} · x₂ 実効：{x2}{detail}
MECHANICAL JAMMING: Center distance Δa too negative or excessive addendum — teeth collide!|BLOQUEO: Δa demasiado negativo o cabeza excesiva; los dientes colisionan.|BLOCCAGGIO: Δa troppo negativo o testa eccessiva; i denti collidono.|BLOCAGE : Δa trop négatif ou saillie excessive ; les dents se heurtent.|BLOCKIERUNG: Δa zu negativ oder Kopfhöhe zu groß; Zähne kollidieren.|かじり：Δa が負に大きすぎるか歯末が高すぎるため、歯が衝突しています。
Base-circle interference detected: enable Auto Anti-Undercut Shift (x) or increase tooth count.|Interferencia de base: active la corrección automática (x) o aumente los dientes.|Interferenza di base: attiva la correzione automatica (x) o aumenta i denti.|Interférence de base : activer le déport automatique (x) ou augmenter les dents.|Grundkreisinterferenz: automatische Profilverschiebung (x) aktivieren oder Zähnezahl erhöhen.|基礎円干渉：自動転位（x）を有効にするか歯数を増やしてください。
Root undercut detected: enable Auto Profile Shift (x) to strengthen tooth root.|Socavado: active la corrección automática (x) para reforzar la raíz.|Sottotaglio: attiva lo spostamento automatico (x) per rinforzare il piede.|Détalonnage : activer le déport automatique (x) pour renforcer le pied.|Unterschnitt: automatische Profilverschiebung (x) zur Fußverstärkung aktivieren.|切下げ：自動転位（x）を有効にして歯元を補強してください。
Low transverse contact ratio ({value}): reduce Δa or increase addendum.|Contacto transversal bajo ({value}): reduzca Δa o aumente la cabeza.|Ricoprimento trasversale basso ({value}): riduci Δa o aumenta la testa.|Rapport transversal faible ({value}) : réduire Δa ou augmenter la saillie.|Geringe Profilüberdeckung ({value}): Δa reduzieren oder Kopfhöhe erhöhen.|正面かみ合い率が低い（{value}）：Δa を減らすか歯末を高くしてください。
Significant axial thrust ({value} N): use thrust bearing or switch to Herringbone.|Empuje axial elevado ({value} N): use rodamiento axial o doble hélice.|Spinta assiale elevata ({value} N): usa un cuscinetto assiale o denti bielicoidali.|Poussée axiale élevée ({value} N) : utiliser une butée ou des chevrons.|Hohe Axialkraft ({value} N): Axiallager oder Pfeilverzahnung verwenden.|大きな軸方向力（{value} N）：スラスト軸受またはやまば歯車を使用してください。
Helix above 47° ({value}°): may require supports or thin layer height in FDM.|Hélice superior a 47° ({value}°): puede necesitar soportes o capas finas.|Elica oltre 47° ({value}°): possono servire supporti o strati sottili.|Hélice supérieure à 47° ({value}°) : supports ou couches fines possibles.|Schrägung über 47° ({value}°): eventuell Stützen oder dünne Schichten nötig.|ねじれが 47° 超（{value}°）：FDM ではサポートまたは薄い層が必要な場合があります。
Separated pair exceeds build plate ({x}×{y} mm): export G1/G2 individually.|El par supera la placa ({x}×{y} mm): exporte G1/G2 por separado.|La coppia supera il piano ({x}×{y} mm): esporta G1/G2 separatamente.|La paire dépasse le plateau ({x}×{y} mm) : exporter G1/G2 séparément.|Das Paar überschreitet die Druckplatte ({x}×{y} mm): G1/G2 einzeln exportieren.|ペアがプレート（{x}×{y} mm）を超えます。G1・G2 を個別に書き出してください。
Interference-free conjugate meshing with healthy FDM printing clearance.|Engrane conjugado sin interferencias, con holgura adecuada para FDM.|Ingranamento coniugato senza interferenze, con gioco adatto alla stampa FDM.|Engrènement conjugué sans interférence, avec un jeu adapté à la FDM.|Störungsfreier konjugierter Eingriff mit geeignetem FDM-Spiel.|干渉のない共役かみ合いで、FDM 印刷に適したすきまです。
Gears are disengaged (a = {a} mm >= r_a1 + r_a2 = {r} mm). Reduce center distance offset.|Engranajes desacoplados (a = {a} mm >= r_a1 + r_a2 = {r} mm). Reduzca el desplazamiento entre centros.|Ingranaggi disaccoppiati (a = {a} mm >= r_a1 + r_a2 = {r} mm). Riduci la variazione d'interasse.|Engrenages désengagés (a = {a} mm >= r_a1 + r_a2 = {r} mm). Réduire le décalage d'entraxe.|Zahnräder außer Eingriff (a = {a} mm >= r_a1 + r_a2 = {r} mm). Achsabstandsänderung reduzieren.|歯車が離れています（a = {a} mm >= r_a1 + r_a2 = {r} mm）。中心距離補正を減らしてください。
Physical mesh lockup / collision detected (a = {a} mm < min non-jam {minimum} mm, 2D clearance = {clearance} mm). Increase Δa or backlash.|Bloqueo / colisión (a = {a} mm < mínimo libre {minimum} mm, holgura 2D = {clearance} mm). Aumente Δa o la holgura.|Bloccaggio / collisione (a = {a} mm < minimo libero {minimum} mm, gioco 2D = {clearance} mm). Aumenta Δa o il gioco.|Blocage / collision (a = {a} mm < minimum libre {minimum} mm, jeu 2D = {clearance} mm). Augmenter Δa ou le jeu.|Blockierung / Kollision (a = {a} mm < klemmfreies Minimum {minimum} mm, 2D-Spiel = {clearance} mm). Δa oder Flankenspiel erhöhen.|かじり・衝突（a = {a} mm < 非干渉最小値 {minimum} mm、2D すきま = {clearance} mm）。Δa またはバックラッシを増やしてください。
Involute base-circle interference detected. Enable Auto Profile Shift (x) or reduce addendum coefficient.|Interferencia de evolvente. Active la corrección automática (x) o reduzca la cabeza.|Interferenza dell'evolvente. Attiva lo spostamento automatico (x) o riduci la testa.|Interférence de développante. Activer le déport automatique (x) ou réduire la saillie.|Evolventen-Grundkreisinterferenz. Automatische Profilverschiebung (x) aktivieren oder Kopfhöhenfaktor verringern.|インボリュート基礎円干渉。自動転位（x）を有効にするか歯末係数を減らしてください。
Critical total contact ratio (ε_γ = {value} < 1.00): loss of continuous mesh action.|Contacto total crítico (ε_γ = {value} < 1.00): pérdida de engrane continuo.|Ricoprimento totale critico (ε_γ = {value} < 1.00): ingranamento discontinuo.|Rapport total critique (ε_γ = {value} < 1.00) : perte de continuité d'engrènement.|Kritische Gesamtüberdeckung (ε_γ = {value} < 1.00): kein kontinuierlicher Eingriff.|全かみ合い率が不足（ε_γ = {value} < 1.00）：連続かみ合いが失われます。
Marginal contact ratio (ε_γ = {value} < 1.20). Consider helical teeth or higher tooth count for smoother operation.|Contacto justo (ε_γ = {value} < 1.20). Use hélice o más dientes para suavizar el giro.|Ricoprimento limitato (ε_γ = {value} < 1.20). Valuta denti elicoidali o più denti per maggiore fluidità.|Rapport limité (ε_γ = {value} < 1.20). Envisager une hélice ou plus de dents pour plus de douceur.|Knappes Überdeckungsverhältnis (ε_γ = {value} < 1.20). Schrägverzahnung oder mehr Zähne für ruhigeren Lauf erwägen.|かみ合い率に余裕がありません（ε_γ = {value} < 1.20）。ねじれや歯数増加で滑らかにしてください。
Effective backlash ({value} mm) is tight for FDM printing. Recommend >= 0.10 mm or printing the Quick Fit-Test Kit first.|Holgura efectiva ({value} mm) muy ajustada para FDM. Use >= 0.10 mm o imprima primero el kit.|Gioco effettivo ({value} mm) ridotto per FDM. Usa >= 0.10 mm o stampa prima il kit.|Jeu effectif ({value} mm) serré pour la FDM. Préférer >= 0.10 mm ou imprimer d'abord le kit.|Wirksames Flankenspiel ({value} mm) für FDM knapp. >= 0.10 mm oder zuerst den Passungstestsatz drucken.|実効バックラッシ（{value} mm）が FDM には小さめです。>= 0.10 mm または先に試験キットを印刷してください。
Root undercut risk on {gear}. Enable 'Auto Profile Shift' to strengthen tooth root.|Riesgo de socavado en {gear}. Active la corrección automática para reforzar la raíz.|Rischio di sottotaglio su {gear}. Attiva lo spostamento automatico per rinforzare il piede.|Risque de détalonnage sur {gear}. Activer le déport automatique pour renforcer le pied.|Unterschnittgefahr an {gear}. Automatische Profilverschiebung zur Fußverstärkung aktivieren.|{gear} に切下げの危険があります。自動転位で歯元を補強してください。
Bottom-side recess detected — verify bridging or enable supports in slicer.|Rebaje inferior: revise los puentes o active soportes en el laminador.|Sede inferiore: verifica i ponti o attiva supporti nello slicer.|Évidement inférieur : vérifier les ponts ou activer les supports dans le trancheur.|Unterseitige Senkung: Brücken prüfen oder Stützen im Slicer aktivieren.|底面の座ぐり：スライサーでブリッジを確認するかサポートを有効にしてください。
Unbalanced axial thrust of {value} N on single helical gear. Use thrust washers or switch to Herringbone to cancel axial thrust (0 N).|Empuje axial desequilibrado de {value} N. Use arandelas axiales o doble hélice para anularlo (0 N).|Spinta assiale sbilanciata di {value} N. Usa rondelle assiali o denti bielicoidali per annullarla (0 N).|Poussée axiale non équilibrée de {value} N. Utiliser des rondelles de butée ou des chevrons pour l'annuler (0 N).|Unausgeglichene Axialkraft {value} N am Schrägrad. Axialscheiben oder Pfeilverzahnung zum Ausgleich verwenden (0 N).|はすば歯車の不平衡軸方向力は {value} N です。スラストワッシャーまたはやまば歯車で相殺してください（0 N）。
Side-by-side pair ({x} x {y} mm) exceeds build plate ({bx} x {by} mm). Export Pinion and Gear individually.|El par ({x} x {y} mm) supera la placa ({bx} x {by} mm). Exporte piñón y rueda por separado.|La coppia ({x} x {y} mm) supera il piano ({bx} x {by} mm). Esporta pignone e ruota separatamente.|La paire ({x} x {y} mm) dépasse le plateau ({bx} x {by} mm). Exporter pignon et roue séparément.|Das Paar ({x} x {y} mm) überschreitet die Druckplatte ({bx} x {by} mm). Ritzel und Rad einzeln exportieren.|並べたペア（{x} x {y} mm）がプレート（{bx} x {by} mm）を超えます。ピニオンと歯車を別々に書き出してください。
Exported successfully ({count} file(s)): {filename}|Exportación completada ({count} archivo(s)): {filename}|Esportazione completata ({count} file): {filename}|Export réussi ({count} fichier(s)) : {filename}|Export erfolgreich ({count} Datei(en)): {filename}|書き出し完了（{count} ファイル）：{filename}
Sent to OrcaSlicer Plater ({count} part(s)).|Solicitud enviada a la placa OrcaSlicer ({count} pieza(s)).|Richiesta inviata al piano OrcaSlicer ({count} parti).|Demande envoyée au plateau OrcaSlicer ({count} pièce(s)).|Anfrage an OrcaSlicer-Druckplatte gesendet ({count} Teil(e)).|OrcaSlicer プレートへ要求を送信しました（{count} 部品）。
Exports folder: {path}|Carpeta de exportación: {path}|Cartella esportazioni: {path}|Dossier d'export : {path}|Exportordner: {path}|書き出しフォルダー：{path}
0° (Spur)|0° (rectos)|0° (dritti)|0° (droits)|0° (gerade)|0°（平歯車）
walls + Gyroid|paredes + Gyroid|pareti + Gyroid|parois + Gyroid|Wände + Gyroid|外周 + Gyroid
effective|efectivo|effettivo|effectif|wirksam|実効
⚠ Undercut|⚠ Socavado|⚠ Sottotaglio|⚠ Détalonnage|⚠ Unterschnitt|⚠ 切下げ
✓ No undercut|✓ Sin socavado|✓ Senza sottotaglio|✓ Sans détalonnage|✓ Kein Unterschnitt|✓ 切下げなし
Thin tooth tip (< {value} mm) for FDM nozzle extrusion. Reduce profile shift or addendum coefficient.|Punta fina (< {value} mm) para FDM. Reduzca la corrección o la cabeza.|Testa sottile (< {value} mm) per FDM. Riduci lo spostamento o la testa.|Sommet fin (< {value} mm) pour la FDM. Réduire le déport ou la saillie.|Dünner Zahnkopf (< {value} mm) für FDM. Profilverschiebung oder Kopfhöhenfaktor reduzieren.|歯先が FDM ノズルに対して薄すぎます（< {value} mm）。転位または歯末係数を減らしてください。
Steep helix overhang ({value}° > 48°): may require supports or thin layers (0.12 mm).|Hélice pronunciada ({value}° > 48°): puede requerir soportes o capas finas (0.12 mm).|Elica ripida ({value}° > 48°): possono servire supporti o strati sottili (0.12 mm).|Forte hélice ({value}° > 48°) : supports ou couches fines possibles (0.12 mm).|Steile Schrägung ({value}° > 48°): eventuell Stützen oder dünne Schichten (0.12 mm) nötig.|急なねじれ（{value}° > 48°）：サポートまたは薄い層（0.12 mm）が必要な場合があります。
"""


def _gear_build_catalog() -> dict[str, dict[str, str]]:
    result = {code: {} for code in SUPPORTED_LANGUAGES[2:]}
    for row in _GEAR_TRANSLATION_ROWS.splitlines():
        source, *values = row.rsplit("|", 5)
        if len(values) != 5 or not source:
            raise ValueError("Invalid Gear translation row")
        for code, value in zip(SUPPORTED_LANGUAGES[2:], values, strict=True):
            result[code][source] = value
    return result


TRANSLATION_CATALOG = _gear_build_catalog()
del _GEAR_TRANSLATION_ROWS


def translate_message(text: str, language: str) -> str:
    """Localize known host messages, preserving captured paths and filenames verbatim."""
    catalog = TRANSLATION_CATALOG.get(normalize_language(language), {})
    if text in catalog:
        return catalog[text]
    for source, target in catalog.items():
        pieces = re.split(r"(\{[a-z][a-z0-9_]*\})", source)
        names = [piece for piece in pieces if re.fullmatch(r"\{[a-z][a-z0-9_]*\}", piece)]
        if not names:
            continue
        pattern = "".join("(.+?)" if piece in names else re.escape(piece) for piece in pieces)
        match = re.fullmatch(pattern, text)
        if match:
            for name, value in zip(names, match.groups(), strict=True):
                target = target.replace(name, value)
            return target
    return text
