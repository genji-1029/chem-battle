import streamlit as st
import random
import time
import pandas as pd
import os
import streamlit.components.v1 as components

# --- ゲームの設定データ (一部抜粋) ---
QUESTIONS = {
    "Level 1 (初級: 各50点)": [
        {"latex": r"H_2 + O_2 \rightarrow H_2O", "reactants": ["H₂", "O₂"], "products": ["H₂O"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"N_2 + H_2 \rightarrow NH_3", "reactants": ["N₂", "H₂"], "products": ["NH₃"], "answers": [1, 3, 2], "point": 50},
        {"latex": r"C + O_2 \rightarrow CO_2", "reactants": ["C", "O₂"], "products": ["CO₂"], "answers": [1, 1, 1], "point": 50},
        {"latex": r"Ag_2O \rightarrow Ag + O_2", "reactants": ["Ag₂O"], "products": ["Ag", "O₂"], "answers": [2, 4, 1], "point": 50},
        {"latex": r"Cu + O_2 \rightarrow CuO", "reactants": ["Cu", "O₂"], "products": ["CuO"], "answers": [2, 1, 2], "point": 50},
    ],
    "Level 2 (中級: 各150点)": [
        {"latex": r"CH_4 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["CH₄", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 2, 1, 2], "point": 150},
        {"latex": r"Mg + HCl \rightarrow MgCl_2 + H_2", "reactants": ["Mg", "HCl"], "products": ["MgCl₂", "H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"C_2H_5OH + O_2 \rightarrow CO_2 + H_2O", "reactants": ["C₂H₅OH", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 3, 2, 3], "point": 150},
        {"latex": r"Al + H_2SO_4 \rightarrow Al_2(SO_4)_3 + H_2", "reactants": ["Al", "H₂SO₄"], "products": ["Al₂(SO₄)₃", "H₂"], "answers": [2, 3, 1, 3], "point": 150},
    ]
}

# --- 音声再生用コンポーネント ---
def play_sound(sound_type):
    # 公開されているフリー音源のURLを使用
    sounds = {
        "correct": "https://actions.google.com/sounds/v1/cartoon/wood_plank_flick.ogg",
        "wrong": "https://actions.google.com/sounds/v1/cartoon/pop.ogg",
        "hurry": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
        "finish": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"
    }
    sound_url = sounds.get(sound_type)
    components.html(
        f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/ogg">
        </audio>
        """,
        height=0,
    )

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
        name = st.text_input("ニックネームを入力", max_chars=10)
        if st.button("スタート！", use_container_width=True):
            if name.strip():
                st.session_state['player_name'] = name
                st.session_state['game_started'] = True
                st.session_state['start_time'] = time.time()
                get_new_question()
                st.rerun()
        return

    # タイム計算
    TIME_LIMIT = 180 
    elapsed_time = time.time() - st.session_state['start_time']
    remaining_time = max(0, int(TIME_LIMIT - elapsed_time))

    if remaining_time <= 0 and not st.session_state['game_over']:
        st.session_state['game_over'] = True
        save_ranking(st.session_state['player_name'], st.session_state['score'])
        play_sound("finish")

    # ヘッダーとタイマー表示
    c1, c2, c3 = st.columns(3)
    c1.metric("🏆 Score", st.session_state['score'])
    
    # 残り時間が少なくなると赤くする
    if remaining_time <= 30:
        c2.markdown(f"<h2 style='color:red; text-align:center; animation: blink 1s infinite;'>⏱ {remaining_time}s</h2>", unsafe_allow_html=True)
        if remaining_time % 5 == 0: # 5秒おきに警告音
            play_sound("hurry")
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

    # 正解・不正解の大きな表示
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

    # 自動更新
    st.markdown("""
        <style>
        @keyframes blink { 0% {opacity:1;} 50% {opacity:0;} 100% {opacity:1;} }
        </style>
        """, unsafe_allow_html=True)
    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    main()
