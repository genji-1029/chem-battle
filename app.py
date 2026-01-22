import streamlit as st
import random

# --- ゲームの設定データ ---
QUESTIONS = [
    {"id": 1, "latex": r"H_2 + O_2 \rightarrow H_2O", "reactants": ["H₂", "O₂"], "products": ["H₂O"], "answers": [2, 1, 2]},
    {"id": 2, "latex": r"N_2 + H_2 \rightarrow NH_3", "reactants": ["N₂", "H₂"], "products": ["NH₃"], "answers": [1, 3, 2]},
    {"id": 3, "latex": r"CH_4 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["CH₄", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 2, 1, 2]},
    {"id": 4, "latex": r"C_3H_8 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₃H₈", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 5, 3, 4]},
    {"id": 5, "latex": r"Al + HCl \rightarrow AlCl_3 + H_2", "reactants": ["Al", "HCl"], "products": ["AlCl₃", "H₂"], "answers": [2, 6, 2, 3]}
]

def init_game():
    if 'score' not in st.session_state: st.session_state['score'] = 0
    if 'hp' not in st.session_state: st.session_state['hp'] = 3
    if 'current_q' not in st.session_state: st.session_state['current_q'] = random.choice(QUESTIONS)
    if 'message' not in st.session_state: st.session_state['message'] = ""

def next_question():
    st.session_state['current_q'] = random.choice(QUESTIONS)
    st.session_state['message'] = ""

def main():
    st.set_page_config(page_title="化学反応バトル")
    init_game()
    st.title("⚔️ 化学反応バトル：係数マスター")
    
    col1, col2 = st.columns(2)
    col1.metric("🏆 Score", st.session_state['score'])
    col2.metric("❤️ HP", st.session_state['hp'])

    if st.session_state['hp'] <= 0:
        st.error("💀 GAME OVER")
        if st.button("リトライ"):
            st.session_state.update({'score': 0, 'hp': 3})
            next_question()
            st.rerun()
        return

    q = st.session_state['current_q']
    st.latex(q['latex'])
    
    parts = q['reactants'] + q['products']
    user_inputs = []
    cols = st.columns(len(parts))
    for i, part in enumerate(parts):
        with cols[i]:
            val = st.number_input(f"{part}", min_value=1, max_value=20, value=1, key=f"in_{i}")
            user_inputs.append(val)

    if st.button("🔥 攻撃!"):
        if user_inputs == q['answers']:
            st.session_state['score'] += 100
            st.success("✅ 正解！")
            st.button("次の敵へ", on_click=next_question)
        else:
            st.session_state['hp'] -= 1
            st.error("❌ 攻撃ミス！")

if __name__ == "__main__":
    main()
