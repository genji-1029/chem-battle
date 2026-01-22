import streamlit as st
import random
import time
import pandas as pd
import os
import streamlit.components.v1 as components

# --- 1. 反応式編 (計50問) ---
QUESTIONS_CHEM = {
    "Level 1 (初級: 各50点)": [
        {"latex": r"H_2 + O_2 \rightarrow H_2O", "reactants": ["H₂", "O₂"], "products": ["H₂O"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"N_2 + H_2 \rightarrow NH_3", "reactants": ["N₂", "H₂"], "products": ["NH₃"], "answers": [1, 3, 2], "point": 50},
        {"latex": r"C + O_2 \rightarrow CO_2", "reactants": ["C", "O₂"], "products": ["CO₂"], "answers": [1, 1, 1], "point": 50},
        {"latex": r"Fe + O_2 \rightarrow Fe_3O_4", "reactants": ["Fe", "O₂"], "products": ["Fe₃O₄"], "answers": [3, 2, 1], "point": 50},
        {"latex": r"Cu + O_2 \rightarrow CuO", "reactants": ["Cu", "O₂"], "products": ["CuO"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"Ag_2O \rightarrow Ag + O_2", "reactants": ["Ag₂O"], "products": ["Ag", "O₂"], "answers": [2, 4, 1], "point": 50},
        {"latex": r"NaHCO_3 \rightarrow Na_2CO_3 + H_2O + CO_2", "reactants": ["NaHCO₃"], "products": ["Na₂CO₃", "H₂O", "CO₂"], "answers": [2, 1, 1, 1], "point": 50},
        {"latex": r"S + O_2 \rightarrow SO_2", "reactants": ["S", "O₂"], "products": ["SO₂"], "answers": [1, 1, 1], "point": 50},
        {"latex": r"Mg + O_2 \rightarrow MgO", "reactants": ["Mg", "O₂"], "products": ["MgO"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"P + O_2 \rightarrow P_4O_{10}", "reactants": ["P", "O₂"], "products": ["P₄O₁₀"], "answers": [4, 5, 1], "point": 50},
        {"latex": r"CO + O_2 \rightarrow CO_2", "reactants": ["CO", "O₂"], "products": ["CO₂"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"KClO_3 \rightarrow KCl + O_2", "reactants": ["KClO₃"], "products": ["KCl", "O₂"], "answers": [2, 2, 3], "point": 50},
        {"latex": r"Al + S \rightarrow Al_2S_3", "reactants": ["Al", "S"], "products": ["Al₂S₃"], "answers": [2, 3, 1], "point": 50},
        {"latex": r"Fe + S \rightarrow FeS", "reactants": ["Fe", "S"], "products": ["FeS"], "answers": [1, 1, 1], "point": 50},
        {"latex": r"H_2O \rightarrow H_2 + O_2", "reactants": ["H₂O"], "products": ["H₂", "O₂"], "answers": [2, 2, 1], "point": 50},
        {"latex": r"Zn + O_2 \rightarrow ZnO", "reactants": ["Zn", "O₂"], "products": ["ZnO"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"HgO \rightarrow Hg + O_2", "reactants": ["HgO"], "products": ["Hg", "O₂"], "answers": [2, 2, 1], "point": 50},
        {"latex": r"Al + O_2 \rightarrow Al_2O_3", "reactants": ["Al", "O₂"], "products": ["Al₂O₃"], "answers": [4, 3, 2], "point": 50},
        {"latex": r"Cu + S \rightarrow Cu_2S", "reactants": ["Cu", "S"], "products": ["Cu₂S"], "answers": [2, 1, 1], "point": 50},
        {"latex": r"NO + O_2 \rightarrow NO_2", "reactants": ["NO", "O₂"], "products": ["NO₂"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"SO_2 + O_2 \rightarrow SO_3", "reactants": ["SO₂", "O₂"], "products": ["SO₃"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"H_2 + Cl_2 \rightarrow HCl", "reactants": ["H₂", "Cl₂"], "products": ["HCl"], "answers": [1, 1, 2], "point": 50},
        {"latex": r"Mg + N_2 \rightarrow Mg_3N_2", "reactants": ["Mg", "N₂"], "products": ["Mg₃N₂"], "answers": [3, 1, 1], "point": 50},
        {"latex": r"Na + O_2 \rightarrow Na_2O", "reactants": ["Na", "O₂"], "products": ["Na₂O"], "answers": [4, 1, 2], "point": 50},
        {"latex": r"Ag + S \rightarrow Ag_2S", "reactants": ["Ag", "S"], "products": ["Ag₂S"], "answers": [2, 1, 1], "point": 50}
    ],
    "Level 2 (中級: 各150点)": [
        {"latex": r"CH_4 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["CH₄", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"Mg + HCl \rightarrow MgCl_2 + H_2", "reactants": ["Mg", "HCl"], "products": ["MgCl₂", "H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"Zn + HCl \rightarrow ZnCl_2 + H_2", "reactants": ["Zn", "HCl"], "products": ["ZnCl₂", "H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"Al + HCl \rightarrow AlCl_3 + H_2", "reactants": ["Al", "HCl"], "products": ["AlCl₃", "H₂"], "answers": [2, 6, 2, 3], "point": 150},
        {"latex": r"C_2H_5OH + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₂H₅OH", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 3, 2, 3], "point": 150},
        {"latex": r"NaOH + H_2SO_4 \rightarrow Na_2SO_4 + H_2O", "reactants": ["NaOH", "H₂SO₄"], "products": ["Na₂SO₄", "H₂O"], "answers": [2, 1, 1, 2], "point": 150},
        {"latex": r"Ca(OH)_2 + HCl \rightarrow CaCl_2 + H_2O", "reactants": ["Ca(OH)₂", "HCl"], "products": ["CaCl₂", "H₂O"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"BaCl_2 + Na_2SO_4 \rightarrow BaSO_4 + NaCl", "reactants": ["BaCl₂", "Na₂SO₄"], "products": ["BaSO₄", "NaCl"], "answers": [1, 1, 1, 2], "point": 150},
        {"latex": r"CuSO_4 + NaOH \rightarrow Cu(OH)_2 + Na_2SO_4", "reactants": ["CuSO₄", "NaOH"], "products": ["Cu(OH)₂", "Na₂SO₄"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"Fe_2O_3 + CO \rightarrow Fe + CO_2", "reactants": ["Fe₂O₃", "CO"], "products": ["Fe", "CO₂"], "answers": [1, 3, 2, 3], "point": 150},
        {"latex": r"C_3H_8 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₃H₈", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 5, 3, 4], "point": 150},
        {"latex": r"NH_3 + O_2 \rightarrow NO + H_2O", "reactants": ["NH₃", "O₂"], "products": ["NO", "H₂O"], "answers": [4, 5, 4, 6], "point": 150},
        {"latex": r"C_2H_2 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₂H₂", "O₂"], "products": ["CO₂", "H₂O"], "answers": [2, 5, 4, 2], "point": 150},
        {"latex": r"Pb(NO_3)_2 + KI \rightarrow PbI_2 + KNO_3", "reactants": ["Pb(NO₃)₂", "KI"], "products": ["PbI₂", "KNO₃"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"H_2S + SO_2 \rightarrow S + H_2O", "reactants": ["H₂S", "SO₂"], "products": ["S", "H₂O"], "answers": [2, 1, 3, 2], "point": 150},
        {"latex": r"Cu + HNO_3 \rightarrow Cu(NO_3)_2 + H_2O + NO", "reactants": ["Cu", "HNO₃"], "products": ["Cu(NO₃)₂", "H₂O", "NO"], "answers": [3, 8, 3, 4, 2], "point": 150},
        {"latex": r"KMnO_4 + HCl \rightarrow KCl + MnCl_2 + H_2O + Cl_2", "reactants": ["KMnO₄", "HCl"], "products": ["KCl", "MnCl₂", "H₂O", "Cl₂"], "answers": [2, 16, 2, 2, 8, 5], "point": 150},
        {"latex": r"Al + NaOH + H_2O \rightarrow Na[Al(OH)_4] + H_2", "reactants": ["Al", "NaOH", "H₂O"], "products": ["Na[Al(OH)₄]", "H₂"], "answers": [2, 2, 6, 2, 3], "point": 150},
        {"latex": r"NH_4Cl + Ca(OH)_2 \rightarrow CaCl_2 + H_2O + NH_3", "reactants": ["NH₄Cl", "Ca(OH)₂"], "products": ["CaCl₂", "H₂O", "NH₃"], "answers": [2, 1, 1, 2, 2], "point": 150},
        {"latex": r"Fe_2O_3 + C \rightarrow Fe + CO_2", "reactants": ["Fe₂O₃", "C"], "products": ["Fe", "CO₂"], "answers": [2, 3, 4, 3], "point": 150},
        {"latex": r"Na_2CO_3 + HCl \rightarrow NaCl + H_2O + CO_2", "reactants": ["Na₂CO₃", "HCl"], "products": ["NaCl", "H₂O", "CO₂"], "answers": [1, 2, 2, 1, 1], "point": 150},
        {"latex": r"MnO_2 + HCl \rightarrow MnCl_2 + H_2O + Cl_2", "reactants": ["MnO₂", "HCl"], "products": ["MnCl₂", "H₂O", "Cl₂"], "answers": [1, 4, 1, 2, 1], "point": 150},
        {"latex": r"CaC_2 + H_2O \rightarrow Ca(OH)_2 + C_2H_2", "reactants": ["CaC₂", "H₂O"], "products": ["Ca(OH)₂", "C₂H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"Fe_2O_3 + Al \rightarrow Al_2O_3 + Fe", "reactants": ["Fe₂O₃", "Al"], "products": ["Al₂O₃", "Fe"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"P_4O_{10} + H_2O \rightarrow H_3PO_4", "reactants": ["P₄O₁₀", "H₂O"], "products": ["H₃PO₄"], "answers": [1, 6, 4], "point": 150}
    ]
}

# --- 2. mol計算編 (計50問) ---
QUESTIONS_MOL = {
    "Level 1 (初級: 各50点)": [
        {"q": "水 H2O 2.0mol の質量は何gか。(H=1, O=16)", "a": ["18g", "36g", "54g", "72g"], "correct": 1, "point": 50},
        {"q": "二酸化炭素 CO2 0.50mol の質量は何gか。(C=12, O=16)", "a": ["11g", "22g", "33g", "44g"], "correct": 1, "point": 50},
        {"q": "標準状態の酸素 O2 11.2L は何molか。", "a": ["0.25mol", "0.50mol", "1.0mol", "2.0mol"], "correct": 1, "point": 50},
        {"q": "銅原子 Cu 3.0×10^23個は何molか。(6.0×10^23/mol)", "a": ["0.2mol", "0.5mol", "1.0mol", "2.0mol"], "correct": 1, "point": 50},
        {"q": "ヘリウム He 4.0g は何molか。(He=4)", "a": ["0.5mol", "1.0mol", "2.0mol", "4.0mol"], "correct": 1, "point": 50},
        {"q": "標準状態の窒素 N2 5.6L は何gか。(N=14)", "a": ["3.5g", "7.0g", "14g", "28g"], "correct": 1, "point": 50},
        {"q": "塩化ナトリウム NaCl 0.10mol の質量は何gか。(Na=23, Cl=35.5)", "a": ["5.85g", "11.7g", "58.5g", "23g"], "correct": 0, "point": 50},
        {"q": "メタン CH4 32g は何molか。(C=12, H=1)", "a": ["0.5mol", "1.0mol", "2.0mol", "4.0mol"], "correct": 2, "point": 50},
        {"q": "アルミニウム Al 2.7g 中の原子の数は何個か。(Al=27, 6.0×10^23/mol)", "a": ["6.0×10^22", "6.0×10^23", "3.0×10^23", "1.2×10^23"], "correct": 0, "point": 50},
        {"q": "二酸化硫黄 SO2 1.5mol の標準状態での体積は何Lか。", "a": ["11.2L", "22.4L", "33.6L", "44.8L"], "correct": 2, "point": 50},
        {"q": "水素分子 H2 1.2×10^24個は何gか。(H=1, 6.0×10^23/mol)", "a": ["2.0g", "4.0g", "8.0g", "1.0g"], "correct": 1, "point": 50},
        {"q": "炭酸カルシウム CaCO3 20g は何molか。(Ca=40, C=12, O=16)", "a": ["0.1mol", "0.2mol", "0.5mol", "1.0mol"], "correct": 1, "point": 50},
        {"q": "銀 Ag 0.10mol の質量は何gか。(Ag=108)", "a": ["1.08g", "10.8g", "54g", "108g"], "correct": 1, "point": 50},
        {"q": "標準状態のアンモニア NH3 44.8L は何molか。", "a": ["1.0mol", "2.0mol", "3.0mol", "4.0mol"], "correct": 1, "point": 50},
        {"q": "酸素原子 O 0.40mol の質量は何gか。(O=16)", "a": ["3.2g", "6.4g", "12.8g", "16g"], "correct": 1, "point": 50},
        {"q": "マグネシウム Mg 1.2g は何molか。(Mg=24)", "a": ["0.01mol", "0.05mol", "0.1mol", "0.5mol"], "correct": 1, "point": 50},
        {"q": "一酸化炭素 CO 0.25mol は標準状態で何Lか。(C=12, O=16)", "a": ["2.24L", "4.48L", "5.6L", "11.2L"], "correct": 2, "point": 50},
        {"q": "塩化水素 HCl 7.3g は何molか。(H=1, Cl=35.5)", "a": ["0.1mol", "0.2mol", "0.5mol", "1.0mol"], "correct": 1, "point": 50},
        {"q": "鉄 Fe 2.0mol の質量は何gか。(Fe=56)", "a": ["28g", "56g", "112g", "168g"], "correct": 2, "point": 50},
        {"q": "標準状態のプロパン C3H8 2.24L は何gか。(C=12, H=1)", "a": ["2.2g", "4.4g", "8.8g", "44g"], "correct": 1, "point": 50},
        {"q": "水酸化ナトリウム NaOH 2.0g は何molか。(Na=23, O=16, H=1)", "a": ["0.05mol", "0.1mol", "0.5mol", "2.0mol"], "correct": 0, "point": 50},
        {"q": "ネオン Ne 0.50mol の標準状態での体積は何Lか。(Ne=20)", "a": ["5.6L", "11.2L", "22.4L", "44.8L"], "correct": 1, "point": 50},
        {"q": "塩素 Cl2 71g は何molか。(Cl=35.5)", "a": ["0.5mol", "1.0mol", "2.0mol", "35.5mol"], "correct": 1, "point": 50},
        {"q": "グルコース C6H12O6 18g は何molか。(C=12, H=1, O=16)", "a": ["0.01mol", "0.05mol", "0.1mol", "0.5mol"], "correct": 2, "point": 50},
        {"q": "カルシウム原子 Ca 1.2×10^23個は何gか。(Ca=40, 6.0×10^23/mol)", "a": ["4.0g", "8.0g", "16g", "40g"], "correct": 1, "point": 50}
    ],
    "Level 2 (中級: 各150点)": [
        {"q": "標準状態の二酸化炭素 5.6L に含まれる酸素原子は何個か。(6.0×10^23/mol)", "a": ["1.5×10^23", "3.0×10^23", "6.0×10^23", "1.2×10^24"], "correct": 1, "point": 150},
        {"q": "密度 1.25g/L の気体の分子量はいくらか。(標準状態)", "a": ["14", "28", "32", "44"], "correct": 1, "point": 150},
        {"q": "水酸化マグネシウム Mg(OH)2 5.8g 中のOH-は何molか。(Mg=24, O=16, H=1)", "a": ["0.1mol", "0.2mol", "0.3mol", "0.4mol"], "correct": 1, "point": 150},
        {"q": "ある気体3.2gが標準状態で2.24Lを占める。この分子量はいくらか。", "a": ["16", "28", "32", "44"], "correct": 2, "point": 150},
        {"q": "空気を窒素:酸素=4:1の混合気体とするとき、平均分子量はいくらか。(N=14, O=16)", "a": ["28.0", "28.8", "29.6", "32.0"], "correct": 1, "point": 150},
        {"q": "グルコース C6H12O6 0.50mol 中に含まれる炭素原子は何gか。(C=12)", "a": ["12g", "24g", "36g", "72g"], "correct": 2, "point": 150},
        {"q": "硫酸銅(II)五水和物 CuSO4・5H2O 25g は何molか。(Cu=64, S=32, O=16, H=1)", "a": ["0.01mol", "0.05mol", "0.1mol", "0.5mol"], "correct": 2, "point": 150},
        {"q": "メタン CH4 1.6g に含まれる水素原子の数は何個か。(C=12, H=1, 6.0×10^23/mol)", "a": ["6.0×10^22", "1.2×10^23", "2.4×10^23", "4.0×10^23"], "correct": 2, "point": 150},
        {"q": "標準状態で5.6Lを占めるアンモニア分子 NH3 の質量は何gか。(N=14, H=1)", "a": ["4.25g", "8.5g", "17g", "34g"], "correct": 0, "point": 150},
        {"q": "硫化水素 H2S 0.20mol に含まれる全原子の数は何個か。(6.0×10^23/mol)", "a": ["1.2×10^23", "3.6×10^23", "6.0×10^23", "1.2×10^24"], "correct": 1, "point": 150},
        {"q": "塩化カルシウム CaCl2 11.1g に含まれるイオンの総数は何molか。(Ca=40, Cl=35.5)", "a": ["0.1mol", "0.2mol", "0.3mol", "0.6mol"], "correct": 2, "point": 150},
        {"q": "密度 1.43g/L の気体の分子量はいくらか。(標準状態)", "a": ["16", "28", "32", "44"], "correct": 2, "point": 150},
        {"q": "水 H2O 3.0×10^24 個の質量は何gか。(H=1, O=16, 6.0×10^23/mol)", "a": ["18g", "54g", "90g", "180g"], "correct": 2, "point": 150},
        {"q": "エタノール C2H5OH 23g に含まれる酸素原子は何molか。(C=12, H=1, O=16)", "a": ["0.25mol", "0.50mol", "1.0mol", "2.0mol"], "correct": 1, "point": 150},
        {"q": "標準状態で 4.48L を占める酸素 O2 中に含まれる酸素原子は何gか。(O=16)", "a": ["3.2g", "6.4g", "12.8g", "16g"], "correct": 1, "point": 150},
        {"q": "0.10mol/Lの硫酸 200mL 中に含まれるH+は何molか。", "a": ["0.02mol", "0.04mol", "0.10mol", "0.20mol"], "correct": 1, "point": 150},
        {"q": "炭素原子 1個の質量は何gか。(C=12, 6.0×10^23/mol)", "a": ["1.0×10^-23", "2.0×10^-23", "12×10^-23", "0.5×10^-23"], "correct": 1, "point": 150},
        {"q": "ヘリウム 5.6L と 窒素 5.6L の混合気体の標準状態での質量は何gか。(He=4, N=14)", "a": ["4.0g", "8.0g", "16g", "32g"], "correct": 1, "point": 150},
        {"q": "ダイヤモンド 0.20g (1カラット) に含まれる炭素原子は何個か。(C=12, 6.0×10^23/mol)", "a": ["1.0×10^21", "1.0×10^22", "6.0×10^22", "1.2×10^23"], "correct": 1, "point": 150},
        {"q": "臭化マグネシウム MgBr2 1.84g 中のイオンの総数はいくつか。(Mg=24, Br=80, 6.0×10^23/mol)", "a": ["6.0×10^21", "1.2×10^22", "1.8×10^22", "6.0×10^22"], "correct": 2, "point": 150},
        {"q": "ある金属Mの酸化物 M2O3 10.2g 中にMが5.4g含まれる。Mの原子量はいくらか。(O=16)", "a": ["24", "27", "40", "56"], "correct": 1, "point": 150},
        {"q": "オゾン O3 0.10mol に含まれる酸素原子は何個か。(6.0×10^23/mol)", "a": ["6.0×10^22", "1.2×10^23", "1.8×10^23", "6.0×10^23"], "correct": 2, "point": 150},
        {"q": "ブタン C4H10 0.20mol を完全燃焼させたとき、生じる二酸化炭素は何molか。", "a": ["0.2mol", "0.4mol", "0.8mol", "1.0mol"], "correct": 2, "point": 150},
        {"q": "標準状態のプロパン C3H8 11.2L の密度は何g/Lか。(C=12, H=1)", "a": ["1.25", "1.96", "2.24", "4.40"], "correct": 1, "point": 150},
        {"q": "硫酸アルミニウム Al2(SO4)3 0.10mol 中に含まれる硫酸イオンは何molか。", "a": ["0.1mol", "0.2mol", "0.3mol", "0.5mol"], "correct": 2, "point": 150}
    ]
}

def play_sound(sound_type):
    sounds = {
        "correct": "https://actions.google.com/sounds/v1/cartoon/wood_plank_flick.ogg",
        "wrong": "https://actions.google.com/sounds/v1/cartoon/pop.ogg",
        "finish": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"
    }
    sound_url = sounds.get(sound_type)
    components.html(f'<audio autoplay><source src="{sound_url}" type="audio/ogg"></audio>', height=0)

def load_ranking(mode):
    file = f'ranking_{mode}.csv'
    if not os.path.exists(file) or os.stat(file).st_size == 0:
        return pd.DataFrame(columns=['Name', 'Score'])
    try: return pd.read_csv(file)
    except: return pd.DataFrame(columns=['Name', 'Score'])

def save_ranking(name, score, mode):
    df = load_ranking(mode)
    new_data = pd.DataFrame({'Name': [name], 'Score': [score]})
    df = pd.concat([df, new_data], ignore_index=True).sort_values(by='Score', ascending=False).head(10)
    df.to_csv(f'ranking_{mode}.csv', index=False)

def init_session(force_reset=False):
    if force_reset:
        keys_to_keep = ['player_name']
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
    defaults = {
        'page': 'menu', 'score': 0, 'correct_count': 0, 'game_over': False,
        'used_indices': [], 'player_name': '', 'question_id': 0, 'last_result': None,
        'start_time': None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_question(mode):
    count = st.session_state['correct_count']
    data = QUESTIONS_CHEM if mode == 'chem' else QUESTIONS_MOL
    level = "Level 1 (初級: 各50点)" if count < 6 else "Level 2 (中級: 各150点)"
    available = [i for i in range(len(data[level])) if i not in st.session_state['used_indices']]
    if not available:
        st.session_state['used_indices'] = []
        available = list(range(len(data[level])))
    idx = random.choice(available)
    st.session_state['used_indices'].append(idx)
    st.session_state['current_q'] = data[level][idx]
    st.session_state['question_id'] += 1

def main():
    st.set_page_config(page_title="化学・最強決定戦", layout="centered")
    init_session()

    if st.session_state['page'] == 'menu':
        st.title("🧪 化学・最強決定戦")
        st.write("挑戦するモードを選んでください")
        c1, c2 = st.columns(2)
        if c1.button("⚔️ 反応式バトル", use_container_width=True):
            st.session_state['page'] = 'start_chem'; st.rerun()
        if c2.button("🧮 mol計算バトル", use_container_width=True):
            st.session_state['page'] = 'start_mol'; st.rerun()
        return

    if st.session_state['page'].startswith('start'):
        mode = 'chem' if 'chem' in st.session_state['page'] else 'mol'
        st.title("🔥 エントリー")
        rdf = load_ranking(mode)
        if not rdf.empty:
            st.info(f"👑 現在の王者: {rdf.iloc[0]['Name']} ({rdf.iloc[0]['Score']}点)")
        
        name = st.text_input("ニックネーム", value=st.session_state['player_name'], max_chars=10)
        if st.button("バトル開始！"):
            if name.strip():
                st.session_state['player_name'] = name
                st.session_state['page'] = f'play_{mode}'
                st.session_state['start_time'] = time.time()
                st.session_state['used_indices'] = []
                get_question(mode)
                st.rerun()
        if st.button("戻る"):
            st.session_state['page'] = 'menu'; st.rerun()
        return

    mode = 'chem' if 'play_chem' in st.session_state['page'] else 'mol'
    rem = max(0, int(180 - (time.time() - st.session_state['start_time'])))

    if rem <= 0 and not st.session_state['game_over']:
        st.session_state['game_over'] = True
        save_ranking(st.session_state['player_name'], st.session_state['score'], mode)
        play_sound("finish")

    cols = st.columns(3)
    cols[0].metric("Score", st.session_state['score'])
    cols[1].metric("Time", f"{rem}s")
    cols[2].metric("Correct", st.session_state['correct_count'])

    if st.session_state['game_over']:
        st.balloons()
        st.error(f"⌛ タイムアップ！ スコア: {st.session_state['score']}")
        st.table(load_ranking(mode).head(5))
        if st.button("タイトルに戻る"):
            init_session(force_reset=True)
            st.rerun()
        return

    if st.session_state['last_result'] == "OK":
        st.success("✨ 正解！！")
        play_sound("correct")
        st.session_state['last_result'] = None
    elif st.session_state['last_result'] == "NG":
        st.error("💥 違うぞ！")
        play_sound("wrong")
        st.session_state['last_result'] = None

    q = st.session_state['current_q']
    st.markdown("---")

    if mode == 'chem':
        st.latex(q['latex'])
        parts = q['reactants'] + q['products']
        icols = st.columns(len(parts))
        user_in = [icols[i].number_input(p, 1, 20, 1, key=f"c_{st.session_state['question_id']}_{i}") for i, p in enumerate(parts)]
        if st.button("🔥 攻撃!", use_container_width=True):
            if user_in == q['answers']:
                st.session_state['score'] += (q['point'] + rem)
                st.session_state['correct_count'] += 1
                st.session_state['last_result'] = "OK"
                get_question(mode)
            else:
                st.session_state['score'] = max(0, st.session_state['score'] - 50)
                st.session_state['last_result'] = "NG"
            st.rerun()
    else:
        st.subheader(q['q'])
        icols = st.columns(2)
        for i, ans in enumerate(q['a']):
            if icols[i % 2].button(ans, use_container_width=True, key=f"m_{st.session_state['question_id']}_{i}"):
                if i == q['correct']:
                    st.session_state['score'] += (q['point'] + rem)
                    st.session_state['correct_count'] += 1
                    st.session_state['last_result'] = "OK"
                    get_question(mode)
                else:
                    st.session_state['score'] = max(0, st.session_state['score'] - 30)
                    st.session_state['last_result'] = "NG"
                st.rerun()

    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    main()
