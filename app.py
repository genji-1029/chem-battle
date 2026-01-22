import streamlit as st
import random
import time

# --- ゲームの設定データ ---
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
    ],
    "Level 2 (中級: 各150点)": [
        {"latex": r"CH_4 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["CH₄", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"Mg + HCl \rightarrow MgCl_2 + H_2", "reactants": ["Mg", "HCl"], "products": ["MgCl₂", "H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"Zn + HCl \rightarrow ZnCl_2 + H_2", "reactants": ["Zn", "HCl"], "products": ["ZnCl₂", "H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"AgNO_3 + Cu \rightarrow Cu(NO_3)_2 + Ag", "reactants": ["AgNO₃", "Cu"], "products": ["Cu(NO₃)₂", "Ag"], "answers": [2, 1, 1, 2], "point": 150},
        {"latex": r"H_2O_2 \rightarrow H_2O + O_2", "reactants": ["H₂O₂"], "products": ["H₂O", "O₂"], "answers": [2, 2, 1], "point": 150},
        {"latex": r"C_2H_5OH + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₂H₅OH", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 3, 2, 3], "point": 150},
        {"latex": r"Al + O_2 \rightarrow Al_2O_3", "reactants": ["Al", "O₂"], "products": ["Al₂O₃"], "answers": [4, 3, 2], "point": 150},
        {"latex": r"Al + H_2SO_4 \rightarrow Al_2(SO_4)_3 + H_2", "reactants": ["Al", "H₂SO₄"], "products": ["Al₂(SO₄)₃", "H₂"], "answers": [2, 3, 1, 3], "point": 150},
        {"latex": r"NaOH + H_2SO_4 \rightarrow Na_2SO_4 + H_2O", "reactants": ["NaOH", "H₂SO₄"], "products": ["Na₂SO₄", "H₂O"], "answers": [2, 1, 1, 2], "point": 150},
        {"latex": r"Ca(OH)_2 + HCl \rightarrow CaCl_2 + H_2O", "reactants": ["Ca(OH)₂", "HCl"], "products": ["CaCl₂", "H₂O"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"BaCl_2 + Na_2SO_4 \rightarrow BaSO_4 + NaCl", "reactants": ["BaCl₂", "Na₂SO₄"], "products": ["BaSO₄", "NaCl"], "answers": [1, 1, 1, 2], "point": 150},
        {"latex": r"CuSO_4 + NaOH \rightarrow Cu(OH)_2 + Na_2SO_4", "reactants": ["CuSO₄", "NaOH"], "products": ["Cu(OH)₂", "Na₂SO₄"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"Fe_2O_3 + CO \rightarrow Fe + CO_2", "reactants": ["Fe₂O₃", "CO"], "products": ["Fe", "CO₂"], "answers": [1, 3, 2, 3], "point": 150},
        {"latex": r"MnO_2 + HCl \rightarrow MnCl_2 + H_2O + Cl_2", "reactants": ["MnO₂", "HCl"], "products": ["MnCl₂", "H₂O", "Cl₂"], "answers": [1, 4, 1, 2, 1], "point": 150},
        {"latex": r"C_3H_8 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₃H₈", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 5, 3, 4], "point": 150},
        {"latex": r"NH_3 + O_2 \rightarrow NO + H_2O", "reactants": ["NH₃", "O₂"], "products": ["NO", "H₂O"], "answers": [4, 5, 4, 6], "point": 150},
    ]
}

def init_game():
    if 'score' not in st.session_state: st.session_state['score'] = 0
    if 'correct_count' not in st.session_state: st.session_state['correct_count'] = 0
    if 'start_time' not in st.session_state: st.session_state['start_time'] = time.time()
    if 'game_over' not in st.session_state: st.session_state['game_over'] = False
    if 'used_indices' not in st.session_state: st.session_state['used_indices'] = []
    if 'current_q' not in st.session_state: 
        get_new_question()

def get_new_question():
    count = st.session_state['correct_count']
    level_key = "Level 1 (初級: 各50点)" if count < 5 else "Level 2 (中級: 各150点)"
    
    # そのレベルの問題全リストのインデックス
    all_q = QUESTIONS[level_key]
    available_indices = [i for i in range(len(all_q)) if i not in st.session_state['used_indices']]
    
    # もし全問題を使い切ったらリストをリセット
    if not available_indices:
        st.session_state['used_indices'] = []
        available_indices = list(range(len(all_q)))
    
    chosen_idx = random.choice(available_indices)
    st.session_state['used_indices'].append(chosen_idx)
    st.session_state['current_q'] = all_q[chosen_idx]

def main():
    st.set_page_config(page_title="化学反応バトル")
    init_game()
    
    TIME_LIMIT = 180 
    elapsed_time = time.time() - st.session_state['start_time']
    remaining_time = max(0, int(TIME_LIMIT - elapsed_time))

    if remaining_time <= 0:
        st.session_state['game_over'] = True

    st.title("⚔️ 化学反応バトル")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("🏆 Score", st.session_state['score'])
    c2.metric("⏱ 残り時間", f"{remaining_time}秒")
    c3.metric("✅ 正解数", st.session_state['correct_count'])

    if st.session_state['game_over']:
        st.balloons()
        st.error(f"⌛ タイムアップ！ 最終スコア: {st.session_state['score']}")
        if st.button("もう一度挑戦"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
        return

    q = st.session_state['current_q']
    st.latex(q['latex'])
    
    parts = q['reactants'] + q['products']
    user_inputs = []
    cols = st.columns(len(parts))
    for i, part in enumerate(parts):
        with cols[i]:
            val = st.number_input(f"{part}", min_value=1, max_value=20, value=1, key=f"q_{st.session_state['correct_count']}_{i}")
            user_inputs.append(val)

    if st.button("🔥 攻撃!", use_container_width=True):
        if user_inputs == q['answers']:
            points_won = q['point'] + remaining_time
            st.session_state['score'] += points_won
            st.session_state['correct_count'] += 1
            st.success(f"✅ 正解！ +{points_won}点")
            get_new_question() # ここで重複チェックして次へ
            time.sleep(0.5)
            st.rerun()
        else:
            st.session_state['score'] = max(0, st.session_state['score'] - 50)
            st.error("❌ 係数が違います！ -50点")

    # 1秒おきにリロードしてタイマーを進める
    if not st.session_state['game_over']:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
