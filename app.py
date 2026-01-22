import streamlit as st
import random
import time
import pandas as pd
import os
import streamlit.components.v1 as components

# --- ゲームの設定データ (100問フルセット) ---
QUESTIONS = {
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
        {"latex": r"CH_4 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["CH₄", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 2, 1, 2], "point": 50},
        {"latex": r"Zn + O_2 \rightarrow ZnO", "reactants": ["Zn", "O₂"], "products": ["ZnO"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"HgO \rightarrow Hg + O_2", "reactants": ["HgO"], "products": ["Hg", "O₂"], "answers": [2, 2, 1], "point": 50},
        {"latex": r"Al + O_2 \rightarrow Al_2O_3", "reactants": ["Al", "O₂"], "products": ["Al₂O₃"], "answers": [4, 3, 2], "point": 50},
        {"latex": r"Cu + S \rightarrow Cu_2S", "reactants": ["Cu", "S"], "products": ["Cu₂S"], "answers": [2, 1, 1], "point": 50},
        {"latex": r"NO + O_2 \rightarrow NO_2", "reactants": ["NO", "O₂"], "products": ["NO₂"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"SO_2 + O_2 \rightarrow SO_3", "reactants": ["SO₂", "O₂"], "products": ["SO₃"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"H_2 + Cl_2 \rightarrow HCl", "reactants": ["H₂", "Cl₂"], "products": ["HCl"], "answers": [1, 1, 2], "point": 50},
        {"latex": r"Mg + N_2 \rightarrow Mg_3N_2", "reactants": ["Mg", "N₂"], "products": ["Mg₃N₂"], "answers": [3, 1, 1], "point": 50},
        {"latex": r"Li + O_2 \rightarrow Li_2O", "reactants": ["Li", "O₂"], "products": ["Li₂O"], "answers": [4, 1, 2], "point": 50},
        {"latex": r"Na + O_2 \rightarrow Na_2O", "reactants": ["Na", "O₂"], "products": ["Na₂O"], "answers": [4, 1, 2], "point": 50},
        {"latex": r"Ag + S \rightarrow Ag_2S", "reactants": ["Ag", "S"], "products": ["Ag₂S"], "answers": [2, 1, 1], "point": 50},
        {"latex": r"Ca + O_2 \rightarrow CaO", "reactants": ["Ca", "O₂"], "products": ["CaO"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"Ba + O_2 \rightarrow BaO", "reactants": ["Ba", "O₂"], "products": ["BaO"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"Zn + S \rightarrow ZnS", "reactants": ["Zn", "S"], "products": ["ZnS"], "answers": [1, 1, 1], "point": 50},
        {"latex": r"N_2 + O_2 \rightarrow NO", "reactants": ["N₂", "O₂"], "products": ["NO"], "answers": [1, 1, 2], "point": 50},
        {"latex": r"C + H_2 \rightarrow CH_4", "reactants": ["C", "H₂"], "products": ["CH₄"], "answers": [1, 2, 1], "point": 50},
        {"latex": r"H_2 + F_2 \rightarrow HF", "reactants": ["H₂", "F₂"], "products": ["HF"], "answers": [1, 1, 2], "point": 50},
        {"latex": r"H_2 + Br_2 \rightarrow HBr", "reactants": ["H₂", "Br₂"], "products": ["HBr"], "answers": [1, 1, 2], "point": 50},
        {"latex": r"H_2 + I_2 \rightarrow HI", "reactants": ["H₂", "I₂"], "products": ["HI"], "answers": [1, 1, 2], "point": 50},
        {"latex": r"N_2O_4 \rightarrow NO_2", "reactants": ["N₂O₄"], "products": ["NO₂"], "answers": [1, 2], "point": 50},
        {"latex": r"O_2 \rightarrow O_3", "reactants": ["O₂"], "products": ["O₃"], "answers": [3, 2], "point": 50},
        {"latex": r"CO_2 + C \rightarrow CO", "reactants": ["CO₂", "C"], "products": ["CO"], "answers": [1, 1, 2], "point": 50},
        {"latex": r"Fe + Cl_2 \rightarrow FeCl_3", "reactants": ["Fe", "Cl₂"], "products": ["FeCl₃"], "answers": [2, 3, 2], "point": 50},
        {"latex": r"Al + Cl_2 \rightarrow AlCl_3", "reactants": ["Al", "Cl₂"], "products": ["AlCl₃"], "answers": [2, 3, 2], "point": 50},
        {"latex": r"Na + Cl_2 \rightarrow NaCl", "reactants": ["Na", "Cl₂"], "products": ["NaCl"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"P + Cl_2 \rightarrow PCl_3", "reactants": ["P", "Cl₂"], "products": ["PCl₃"], "answers": [2, 3, 2], "point": 50},
        {"latex": r"P + Cl_2 \rightarrow PCl_5", "reactants": ["P", "Cl₂"], "products": ["PCl₅"], "answers": [2, 5, 2], "point": 50},
        {"latex": r"Si + Cl_2 \rightarrow SiCl_4", "reactants": ["Si", "Cl₂"], "products": ["SiCl₄"], "answers": [1, 2, 1], "point": 50},
        {"latex": r"H_2O_2 \rightarrow H_2O + O_2", "reactants": ["H₂O₂"], "products": ["H₂O", "O₂"], "answers": [2, 2, 1], "point": 50},
        {"latex": r"Cu + AgNO_3 \rightarrow Cu(NO_3)_2 + Ag", "reactants": ["Cu", "AgNO₃"], "products": ["Cu(NO₃)₂", "Ag"], "answers": [1, 2, 1, 2], "point": 50},
        {"latex": r"CH_4 + Cl_2 \rightarrow CH_3Cl + HCl", "reactants": ["CH₄", "Cl₂"], "products": ["CH₃Cl", "HCl"], "answers": [1, 1, 1, 1], "point": 50},
        {"latex": r"Fe_3O_4 + H_2 \rightarrow Fe + H_2O", "reactants": ["Fe₃O₄", "H₂"], "products": ["Fe", "H₂O"], "answers": [1, 4, 3, 4], "point": 50},
        {"latex": r"Na_2O + H_2O \rightarrow NaOH", "reactants": ["Na₂O", "H₂O"], "products": ["NaOH"], "answers": [1, 1, 2], "point": 50},
        {"latex": r"CaO + H_2O \rightarrow Ca(OH)_2", "reactants": ["CaO", "H₂O"], "products": ["Ca(OH)₂"], "answers": [1, 1, 1], "point": 50},
    ],
    "Level 2 (中級: 各150点)": [
        {"latex": r"Mg + HCl \rightarrow MgCl_2 + H_2", "reactants": ["Mg", "HCl"], "products": ["MgCl₂", "H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"Zn + HCl \rightarrow ZnCl_2 + H_2", "reactants": ["Zn", "HCl"], "products": ["ZnCl₂", "H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"Al + HCl \rightarrow AlCl_3 + H_2", "reactants": ["Al", "HCl"], "products": ["AlCl₃", "H₂"], "answers": [2, 6, 2, 3], "point": 150},
        {"latex": r"C_2H_5OH + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₂H₅OH", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 3, 2, 3], "point": 150},
        {"latex": r"Al + H_2SO_4 \rightarrow Al_2(SO_4)_3 + H_2", "reactants": ["Al", "H₂SO₄"], "products": ["Al₂(SO₄)₃", "H₂"], "answers": [2, 3, 1, 3], "point": 150},
        {"latex": r"NaOH + H_2SO_4 \rightarrow Na_2SO_4 + H_2O", "reactants": ["NaOH", "H₂SO₄"], "products": ["Na₂SO₄", "H₂O"], "answers": [2, 1, 1, 2], "point": 150},
        {"latex": r"Ca(OH)_2 + HCl \rightarrow CaCl_2 + H_2O", "reactants": ["Ca(OH)₂", "HCl"], "products": ["CaCl₂", "H₂O"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"BaCl_2 + Na_2SO_4 \rightarrow BaSO_4 + NaCl", "reactants": ["BaCl₂", "Na₂SO₄"], "products": ["BaSO₄", "NaCl"], "answers": [1, 1, 1, 2], "point": 150},
        {"latex": r"CuSO_4 + NaOH \rightarrow Cu(OH)_2 + Na_2SO_4", "reactants": ["CuSO₄", "NaOH"], "products": ["Cu(OH)₂", "Na₂SO₄"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"Fe_2O_3 + CO \rightarrow Fe + CO_2", "reactants": ["Fe₂O₃", "CO"], "products": ["Fe", "CO₂"], "answers": [1, 3, 2, 3], "point": 150},
        {"latex": r"MnO_2 + HCl \rightarrow MnCl_2 + H_2O + Cl_2", "reactants": ["MnO₂", "HCl"], "products": ["MnCl₂", "H₂O", "Cl₂"], "answers": [1, 4, 1, 2, 1], "point": 150},
        {"latex": r"C_3H_8 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₃H₈", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 5, 3, 4], "point": 150},
        {"latex": r"NH_3 + O_2 \rightarrow NO + H_2O", "reactants": ["NH₃", "O₂"], "products": ["NO", "H₂O"], "answers": [4, 5, 4, 6], "point": 150},
        {"latex": r"C_2H_2 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₂H₂", "O₂"], "products": ["CO₂", "H₂O"], "answers": [2, 5, 4, 2], "point": 150},
        {"latex": r"C_2H_4 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₂H₄", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 3, 2, 2], "point": 150},
        {"latex": r"CH_3OH + O_2 \rightarrow CO_2 + H_2O", "reactants": ["CH₃OH", "O₂"], "products": ["CO₂", "H₂O"], "answers": [2, 3, 2, 4], "point": 150},
        {"latex": r"Pb(NO_3)_2 + KI \rightarrow PbI_2 + KNO_3", "reactants": ["Pb(NO₃)₂", "KI"], "products": ["PbI₂", "KNO₃"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"Al + NaOH + H_2O \rightarrow Na[Al(OH)_4] + H_2", "reactants": ["Al", "NaOH", "H₂O"], "products": ["Na[Al(OH)₄]", "H₂"], "answers": [2, 2, 6, 2, 3], "point": 150},
        {"latex": r"CaC_2 + H_2O \rightarrow Ca(OH)_2 + C_2H_2", "reactants": ["CaC₂", "H₂O"], "products": ["Ca(OH)₂", "C₂H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"H_2S + SO_2 \rightarrow S + H_2O", "reactants": ["H₂S", "SO₂"], "products": ["S", "H₂O"], "answers": [2, 1, 3, 2], "point": 150},
        {"latex": r"Fe_2O_3 + Al \rightarrow Al_2O_3 + Fe", "reactants": ["Fe₂O₃", "Al"], "products": ["Al₂O₃", "Fe"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"Cu + H_2SO_4 \rightarrow CuSO_4 + H_2O + SO_2", "reactants": ["Cu", "H₂SO₄"], "products": ["CuSO₄", "H₂O", "SO₂"], "answers": [1, 2, 1, 2, 1], "point": 150},
        {"latex": r"CaCO_3 + HCl \rightarrow CaCl_2 + H_2O + CO_2", "reactants": ["CaCO₃", "HCl"], "products": ["CaCl₂", "H₂O", "CO₂"], "answers": [1, 2, 1, 1, 1], "point": 150},
        {"latex": r"K + H_2O \rightarrow KOH + H_2", "reactants": ["K", "H₂O"], "products": ["KOH", "H₂"], "answers": [2, 2, 2, 1], "point": 150},
        {"latex": r"Na + H_2O \rightarrow NaOH + H_2", "reactants": ["Na", "H₂O"], "products": ["NaOH", "H₂"], "answers": [2, 2, 2, 1], "point": 150},
        {"latex": r"Ba(OH)_2 + H_2SO_4 \rightarrow BaSO_4 + H_2O", "reactants": ["Ba(OH)₂", "H₂SO₄"], "products": ["BaSO₄", "H₂O"], "answers": [1, 1, 1, 2], "point": 150},
        {"latex": r"NaCl + AgNO_3 \rightarrow AgCl + NaNO_3", "reactants": ["NaCl", "AgNO₃"], "products": ["AgCl", "NaNO₃"], "answers": [1, 1, 1, 1], "point": 150},
        {"latex": r"AgNO_3 + CaCl_2 \rightarrow AgCl + Ca(NO_3)_2", "reactants": ["AgNO₃", "CaCl₂"], "products": ["AgCl", "Ca(NO₃)₂"], "answers": [2, 1, 2, 1], "point": 150},
        {"latex": r"Cu + HNO_3 \rightarrow Cu(NO_3)_2 + H_2O + NO", "reactants": ["Cu", "HNO₃"], "products": ["Cu(NO₃)₂", "H₂O", "NO"], "answers": [3, 8, 3, 4, 2], "point": 150},
        {"latex": r"Cu + HNO_3 \rightarrow Cu(NO_3)_2 + H_2O + NO_2", "reactants": ["Cu", "HNO₃"], "products": ["Cu(NO₃)₂", "H₂O", "NO₂"], "answers": [1, 4, 1, 2, 2], "point": 150},
        {"latex": r"KMnO_4 + HCl \rightarrow KCl + MnCl_2 + H_2O + Cl_2", "reactants": ["KMnO₄", "HCl"], "products": ["KCl", "MnCl₂", "H₂O", "Cl₂"], "answers": [2, 16, 2, 2, 8, 5], "point": 150},
        {"latex": r"K_2Cr_2O_7 + HCl \rightarrow KCl + CrCl_3 + H_2O + Cl_2", "reactants": ["K₂Cr₂O₇", "HCl"], "products": ["KCl", "CrCl₃", "H₂O", "Cl₂"], "answers": [1, 14, 2, 2, 7, 3], "point": 150},
        {"latex": r"SO_2 + H_2S \rightarrow S + H_2O", "reactants": ["SO₂", "H₂S"], "products": ["S", "H₂O"], "answers": [1, 2, 3, 2], "point": 150},
        {"latex": r"Cl_2 + H_2O \rightarrow HCl + HClO", "reactants": ["Cl₂", "H₂O"], "products": ["HCl", "HClO"], "answers": [1, 1, 1, 1], "point": 150},
        {"latex": r"CuSO_4 + H_2S \rightarrow CuS + H_2SO_4", "reactants": ["CuSO₄", "H₂S"], "products": ["CuS", "H₂SO₄"], "answers": [1, 1, 1, 1], "point": 150},
        {"latex": r"FeS + HCl \rightarrow FeCl_2 + H_2S", "reactants": ["FeS", "HCl"], "products": ["FeCl₂", "H₂S"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"NH_4Cl + Ca(OH)_2 \rightarrow CaCl_2 + H_2O + NH_3", "reactants": ["NH₄Cl", "Ca(OH)₂"], "products": ["CaCl₂", "H₂O", "NH₃"], "answers": [2, 1, 1, 2, 2], "point": 150},
        {"latex": r"CaF_2 + H_2SO_4 \rightarrow CaSO_4 + HF", "reactants": ["CaF₂", "H₂SO₄"], "products": ["CaSO₄", "HF"], "answers": [1, 1, 1, 2], "point": 150},
        {"latex": r"Ca_3(PO_4)_2 + H_2SO_4 \rightarrow CaSO_4 + H_3PO_4", "reactants": ["Ca₃(PO₄)₂", "H₂SO₄"], "products": ["CaSO₄", "H₃PO₄"], "answers": [1, 3, 3, 2], "point": 150},
        {"latex": r"Fe_2O_3 + C \rightarrow Fe + CO_2", "reactants": ["Fe₂O₃", "C"], "products": ["Fe", "CO₂"], "answers": [2, 3, 4, 3], "point": 150},
        {"latex": r"Fe_2O_3 + C \rightarrow Fe + CO", "reactants": ["Fe₂O₃", "C"], "products": ["Fe", "CO"], "answers": [1, 3, 2, 3], "point": 150},
        {"latex": r"Na_2CO_3 + HCl \rightarrow NaCl + H_2O + CO_2", "reactants": ["Na₂CO₃", "HCl"], "products": ["NaCl", "H₂O", "CO₂"], "answers": [1, 2, 2, 1, 1], "point": 150},
        {"latex": r"KClO_3 \rightarrow KCl + O_2", "reactants": ["KClO₃"], "products": ["KCl", "O₂"], "answers": [2, 2, 3], "point": 150},
        {"latex": r"Mg(OH)_2 + HCl \rightarrow MgCl_2 + H_2O", "reactants": ["Mg(OH)₂", "HCl"], "products": ["MgCl₂", "H₂O"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"Al_2O_3 + HCl \rightarrow AlCl_3 + H_2O", "reactants": ["Al₂O₃", "HCl"], "products": ["AlCl₃", "H₂O"], "answers": [1, 6, 2, 3], "point": 150},
        {"latex": r"Al(OH)_3 + H_2SO_4 \rightarrow Al_2(SO_4)_3 + H_2O", "reactants": ["Al(OH)₃", "H₂SO₄"], "products": ["Al₂(SO₄)₃", "H₂O"], "answers": [2, 3, 1, 6], "point": 150},
        {"latex": r"SiCl_4 + H_2O \rightarrow SiO_2 + HCl", "reactants": ["SiCl₄", "H₂O"], "products": ["SiO₂", "HCl"], "answers": [1, 2, 1, 4], "point": 150},
        {"latex": r"P_4O_{10} + H_2O \rightarrow H_3PO_4", "reactants": ["P₄O₁₀", "H₂O"], "products": ["H₃PO₄"], "answers": [1, 6, 4], "point": 150},
        {"latex": r"Ca(OH)_2 + CO_2 \rightarrow CaCO_3 + H_2O", "reactants": ["Ca(OH)₂", "CO₂"], "products": ["CaCO₃", "H₂O"], "answers": [1, 1, 1, 1], "point": 150},
        {"latex": r"NaOH + CO_2 \rightarrow Na_2CO_3 + H_2O", "reactants": ["NaOH", "CO₂"], "products": ["Na₂CO₃", "H₂O"], "answers": [2, 1, 1, 1], "point": 150},
    ]
}

def play_sound(sound_type):
    sounds = {
        "correct": "https://actions.google.com/sounds/v1/cartoon/wood_plank_flick.ogg",
        "wrong": "https://actions.google.com/sounds/v1/cartoon/pop.ogg",
        "hurry": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
        "finish": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"
    }
    sound_url = sounds.get(sound_type)
    components.html(f'<audio autoplay><source src="{sound_url}" type="audio/ogg"></audio>', height=0)

def load_ranking():
    try:
        if not os.path.exists('ranking.csv') or os.stat('ranking.csv').st_size == 0:
            return pd.DataFrame(columns=['Name', 'Score'])
        return pd.read_csv('ranking.csv')
    except:
        return pd.DataFrame(columns=['Name', 'Score'])

def save_ranking(name, score):
    df = load_ranking()
    new_data = pd.DataFrame({'Name': [name], 'Score': [score]})
    df = pd.concat([df, new_data], ignore_index=True)
    df = df.sort_values(by='Score', ascending=False).head(10)
    df.to_csv('ranking.csv', index=False)

def init_game():
    if 'game_started' not in st.session_state: st.session_state['game_started'] = False
    if 'score' not in st.session_state: st.session_state['score'] = 0
    if 'correct_count' not in st.session_state: st.session_state['correct_count'] = 0
    if 'game_over' not in st.session_state: st.session_state['game_over'] = False
    if 'used_indices' not in st.session_state: st.session_state['used_indices'] = []
    if 'player_name' not in st.session_state: st.session_state['player_name'] = ""
    if 'question_id' not in st.session_state: st.session_state['question_id'] = 0
    if 'last_result' not in st.session_state: st.session_state['last_result'] = None

def get_new_question():
    count = st.session_state['correct_count']
    level_key = "Level 1 (初級: 各50点)" if count < 6 else "Level 2 (中級: 各150点)"
    all_q = QUESTIONS[level_key]
    available_indices = [i for i in range(len(all_q)) if i not in st.session_state['used_indices']]
    if not available_indices:
        st.session_state['used_indices'] = []
        available_indices = list(range(len(all_q)))
    chosen_idx = random.choice(available_indices)
    st.session_state['used_indices'].append(chosen_idx)
    st.session_state['current_q'] = all_q[chosen_idx]
    st.session_state['question_id'] += 1

def main():
    st.set_page_config(page_title="化学反応バトル", layout="centered")
    init_game()

    if not st.session_state['game_started']:
        st.title("⚔️ 化学反応バトル")
        ranking_df = load_ranking()
        if not ranking_df.empty:
            top_player = ranking_df.iloc[0]['Name']
            top_score = ranking_df.iloc[0]['Score']
            st.markdown(f"""
                <div style="background-color:#FFF9C4; padding:15px; border-radius:10px; border:2px solid #FBC02D; text-align:center; margin-bottom:20px;">
                    <span style="font-size:1.2rem; color:#f57f17; font-weight:bold;">👑 現在の歴代最高記録 👑</span><br>
                    <span style="font-size:1.5rem; font-weight:bold; color:black;">{top_player} さん</span><br>
                    <span style="font-size:2rem; font-weight:bold; color:#d32f2f;">{top_score}点</span>
                </div>
            """, unsafe_allow_html=True)
        st.write("3分間でハイスコアを目指せ！(全100問)")
        name = st.text_input("ニックネームを入力", max_chars=10)
        if st.button("ゲームスタート！", use_container_width=True):
            if name.strip():
                st.session_state['player_name'] = name
                st.session_state['game_started'] = True
                st.session_state['start_time'] = time.time()
                get_new_question()
                st.rerun()
        return

    TIME_LIMIT = 180 
    elapsed_time = time.time() - st.session_state['start_time']
    remaining_time = max(0, int(TIME_LIMIT - elapsed_time))

    if remaining_time <= 0 and not st.session_state['game_over']:
        st.session_state['game_over'] = True
        save_ranking(st.session_state['player_name'], st.session_state['score'])
        play_sound("finish")

    c1, c2, c3 = st.columns(3)
    c1.metric("🏆 Score", st.session_state['score'])
    if remaining_time <= 30:
        c2.markdown(f"<h2 style='color:red; text-align:center; animation: blink 1s infinite;'>⏱ {remaining_time}s</h2>", unsafe_allow_html=True)
        if remaining_time % 5 == 0: play_sound("hurry")
    else:
        c2.metric("⏱ 残り時間", f"{remaining_time}s")
    c3.metric("✅ 正解数", st.session_state['correct_count'])

    if st.session_state['game_over']:
        st.balloons()
        st.error(f"⌛ タイムアップ！ スコア: {st.session_state['score']}")
        st.table(load_ranking().head(5))
        if st.button("タイトルに戻る"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
        return

    if st.session_state['last_result'] == "correct":
        st.success("✨ 正解！！ ✨")
        play_sound("correct")
        st.session_state['last_result'] = None
    elif st.session_state['last_result'] == "wrong":
        st.error("💥 係数が違うぞ！ 💥")
        play_sound("wrong")
        st.session_state['last_result'] = None

    q = st.session_state['current_q']
    st.markdown("---")
    st.latex(q['latex'])
    
    parts = q['reactants'] + q['products']
    cols = st.columns(len(parts))
    user_inputs = []
    for i, part in enumerate(parts):
        with cols[i]:
            val = st.number_input(f"{part}", min_value=1, max_value=20, value=1, key=f"in_{st.session_state['question_id']}_{i}")
            user_inputs.append(val)

    if st.button("🔥 攻撃!", use_container_width=True):
        if user_inputs == q['answers']:
            st.session_state['score'] += (q['point'] + remaining_time)
            st.session_state['correct_count'] += 1
            st.session_state['last_result'] = "correct"
            get_new_question()
            st.rerun()
        else:
            st.session_state['score'] = max(0, st.session_state['score'] - 50)
            st.session_state['last_result'] = "wrong"
            st.rerun()

    st.markdown("<style>@keyframes blink {0%{opacity:1;} 50%{opacity:0;} 100%{opacity:1;}}</style>", unsafe_allow_html=True)
    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    main()
