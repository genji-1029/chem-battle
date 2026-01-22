import streamlit as st
import random
import time
import pandas as pd
import os
import streamlit.components.v1 as components

# --- ゲームの設定データ (100問規模) ---
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
    ],
    "Level 2 (中級: 各150点)": [
        {"latex": r"Mg + HCl \rightarrow MgCl_2 + H_2", "reactants": ["Mg", "HCl"], "products": ["MgCl₂", "H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"Zn + HCl \rightarrow ZnCl_2 + H_2", "reactants": ["Zn", "HCl"], "products": ["ZnCl₂", "H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"AgNO_3 + Cu \rightarrow Cu(NO_3)_2 + Ag", "reactants": ["AgNO₃", "Cu"], "products": ["Cu(NO₃)₂", "Ag"], "answers": [2, 1, 1, 2], "point": 150},
        {"latex": r"H_2O_2 \rightarrow H_2O + O_2", "reactants": ["H₂O₂"], "products": ["H₂O", "O₂"], "answers": [2, 2, 1], "point": 150},
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
    ]
}

# --- 音声再生用コンポーネント ---
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
    # 6問目から中級へ
    count = st.session_state['correct_count']
    level_key = "Level 1 (初級: 各50点)" if count < 6 else "Level 2 (中級: 各150点)"
    all_q = QUESTIONS[level_key]
    
    # 重複回避ロジック
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
        st.write("3分間で全50問以上の反応式を攻略せよ！")
        name = st.text_input("ニックネームを入力", max_chars=10)
        if st.button("スタート！", use_container_width=True):
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

    # タイマーとスコア
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
        if st.button("もう一度遊ぶ"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
        return

    # 中央の大きな正解・不正解表示
    if st.session_state['last_result'] == "correct":
        st.success("✨ 正解！！ 次の問題へ ✨")
        play_sound("correct")
        st.session_state['last_result'] = None
    elif st.session_state['last_result'] == "wrong":
        st.error("💥 係数が違うぞ！ -50点 💥")
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
