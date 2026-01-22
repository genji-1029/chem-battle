import streamlit as st
import random
import time

# --- ゲームの設定データ（難易度別に分類） ---
QUESTIONS = {
    "Level 1 (初級)": [
        {"latex": r"H_2 + O_2 \rightarrow H_2O", "reactants": ["H₂", "O₂"], "products": ["H₂O"], "answers": [2, 1, 2]},
        {"latex": r"N_2 + H_2 \rightarrow NH_3", "reactants": ["N₂", "H₂"], "products": ["NH₃"], "answers": [1, 3, 2]},
        {"latex": r"C + O_2 \rightarrow CO_2", "reactants": ["C", "O₂"], "products": ["CO₂"], "answers": [1, 1, 1]},
    ],
    "Level 2 (中級)": [
        {"latex": r"CH_4 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["CH₄", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 2, 1, 2]},
        {"latex": r"Mg + HCl \rightarrow MgCl_2 + H_2", "reactants": ["Mg", "HCl"], "products": ["MgCl₂", "H₂"], "answers": [1, 2, 1, 1]},
        {"latex": r"AgNO_3 + Cu \rightarrow Cu(NO_3)_2 + Ag", "reactants": ["AgNO₃", "Cu"], "products": ["Cu(NO₃)₂", "Ag"], "answers": [2, 1, 1, 2]},
    ],
    "Level 3 (上級)": [
        {"latex": r"C_3H_8 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₃H₈", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 5, 3, 4]},
        {"latex": r"Al + HCl \rightarrow AlCl_3 + H_2", "reactants": ["Al", "HCl"], "products": ["AlCl₃", "H₂"], "answers": [2, 6, 2, 3]},
        {"latex": r"C_2H_6 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₂H₆", "O₂"], "products": ["CO₂", "H₂O"], "answers": [2, 7, 4, 6]},
    ]
}

def init_game():
    if 'score' not in st.session_state: st.session_state['score'] = 0
    if 'correct_count' not in st.session_state: st.session_state['correct_count'] = 0
    if 'start_time' not in st.session_state: st.session_state['start_time'] = time.time()
    if 'game_over' not in st.session_state: st.session_state['game_over'] = False
    if 'current_q' not in st.session_state: 
        st.session_state['current_q'] = random.choice(QUESTIONS["Level 1 (初級)"])

def next_question():
    count = st.session_state['correct_count']
    if count < 3:
        level = "Level 1 (初級)"
    elif count < 7:
        level = "Level 2 (中級)"
    else:
        level = "Level 3 (上級)"
    
    st.session_state['current_q'] = random.choice(QUESTIONS[level])

def main():
    st.set_page_config(page_title="化学反応バトル：タイムアタック")
    init_game()
    
    # 制限時間の設定（3分 = 180秒）
    TIME_LIMIT = 180
    elapsed_time = time.time() - st.session_state['start_time']
    remaining_time = max(0, int(TIME_LIMIT - elapsed_time))

    if remaining_time <= 0:
        st.session_state['game_over'] = True

    st.title("⚔️ 化学反応バトル：タイムアタック")
    
    # 状況表示
    c1, c2, c3 = st.columns(3)
    c1.metric("🏆 Score", st.session_state['score'])
    c2.metric("⏱ 残り時間", f"{remaining_time}秒")
    c3.metric("✅ 正解数", st.session_state['correct_count'])

    if st.session_state['game_over']:
        st.error(f"⌛ タイムアップ！ 最終スコア: {st.session_state['score']}")
        if st.button("もう一度挑戦する"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        return

    # 問題表示
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
            # スコア計算：基本100点 ＋ 残り時間ボーナス
            bonus = remaining_time
            st.session_state['score'] += (100 + bonus)
            st.session_state['correct_count'] += 1
            st.success(f"✅ 正解！ +{100 + bonus}点 (タイムボーナス含む)")
            next_question()
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ 係数が違います！")

    # 画面を自動更新するための仕組み（1秒ごとにリロード）
    if not st.session_state['game_over']:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
