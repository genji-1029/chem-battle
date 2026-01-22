import streamlit as st
import random
import time
import pandas as pd
import os
import streamlit.components.v1 as components

# --- 1. 問題データ定義 (反応式編) ---
QUESTIONS_CHEM = {
    "Level 1 (初級: 各50点)": [
        {"latex": r"H_2 + O_2 \rightarrow H_2O", "reactants": ["H₂", "O₂"], "products": ["H₂O"], "answers": [2, 1, 2], "point": 50},
        {"latex": r"N_2 + H_2 \rightarrow NH_3", "reactants": ["N₂", "H₂"], "products": ["NH₃"], "answers": [1, 3, 2], "point": 50},
        {"latex": r"C + O_2 \rightarrow CO_2", "reactants": ["C", "O₂"], "products": ["CO₂"], "answers": [1, 1, 1], "point": 50},
        {"latex": r"Fe + O_2 \rightarrow Fe_3O_4", "reactants": ["Fe", "O₂"], "products": ["Fe₃O₄"], "answers": [3, 2, 1], "point": 50},
        {"latex": r"Cu + O_2 \rightarrow CuO", "reactants": ["Cu", "O₂"], "products": ["CuO"], "answers": [2, 1, 2], "point": 50},
        # ... (ここに前回提供した50問以上を保持)
    ],
    "Level 2 (中級: 各150点)": [
        {"latex": r"Mg + HCl \rightarrow MgCl_2 + H_2", "reactants": ["Mg", "HCl"], "products": ["MgCl₂", "H₂"], "answers": [1, 2, 1, 1], "point": 150},
        {"latex": r"CH_4 + O_2 \rightarrow CO_2 + H_2O", "reactants": ["CH₄", "O₂"], "products": ["CO₂", "H₂O"], "answers": [1, 2, 1, 2], "point": 150},
        # ... (ここに前回提供した50問以上を保持)
    ]
}

# --- 2. 問題データ定義 (mol計算編) ---
QUESTIONS_MOL = {
    "Level 1 (初級: 各50点)": [
        {"q": "水 H2O 2.0mol の質量は何gか。(H=1.0, O=16)", "a": ["18g", "36g", "54g", "72g"], "correct": 1, "point": 50},
        {"q": "標準状態の酸素 O2 11.2L は何molか。", "a": ["0.25mol", "0.50mol", "1.0mol", "2.0mol"], "correct": 1, "point": 50},
        {"q": "アルミニウム原子 Al 3.0×10^23個は何molか。(6.0×10^23/mol)", "a": ["0.20mol", "0.50mol", "1.0mol", "2.0mol"], "correct": 1, "point": 50},
        # ... (ここに合計50問分追加)
    ],
    "Level 2 (中級: 各150点)": [
        {"q": "標準状態の二酸化炭素 5.6L に含まれる酸素原子 O は何個か。(6.0×10^23/mol)", "a": ["1.5×10^23個", "3.0×10^23個", "6.0×10^23個", "1.2×10^24個"], "correct": 1, "point": 150},
        {"q": "密度 1.25g/L の気体の分子量はいくらか。", "a": ["14", "28", "32", "44"], "correct": 1, "point": 150},
        # ... (ここに合計50問分追加)
    ]
}

# --- 音声・ランキング機能 ---
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
    return pd.read_csv(file)

def save_ranking(name, score, mode):
    df = load_ranking(mode)
    new_data = pd.DataFrame({'Name': [name], 'Score': [score]})
    df = pd.concat([df, new_data], ignore_index=True).sort_values(by='Score', ascending=False).head(10)
    df.to_csv(f'ranking_{mode}.csv', index=False)

# --- ゲーム管理 ---
def init_session():
    defaults = {
        'page': 'menu', 'score': 0, 'correct_count': 0, 'game_over': False,
        'used_indices': [], 'player_name': '', 'question_id': 0, 'last_result': None
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v

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

    # --- メニュー画面 ---
    if st.session_state['page'] == 'menu':
        st.title("🧪 化学・最強決定戦")
        st.write("挑戦するモードを選んでください")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⚔️ 反応式バトル\n(係数入力)", use_container_width=True):
                st.session_state['page'] = 'start_chem'
                st.rerun()
        with c2:
            if st.button("🧮 mol計算バトル\n(4択問題)", use_container_width=True):
                st.session_state['page'] = 'start_mol'
                st.rerun()
        return

    # --- スタート画面 (共通) ---
    if st.session_state['page'].startswith('start'):
        mode = 'chem' if 'chem' in st.session_state['page'] else 'mol'
        st.title("🔥 エントリー")
        rdf = load_ranking(mode)
        if not rdf.empty:
            st.warning(f"👑 現在の王者: {rdf.iloc[0]['Name']} ({rdf.iloc[0]['Score']}点)")
        
        name = st.text_input("ニックネーム", max_chars=10)
        if st.button("バトル開始！"):
            if name.strip():
                st.session_state['player_name'] = name
                st.session_state['page'] = f'play_{mode}'
                st.session_state['start_time'] = time.time()
                get_question(mode)
                st.rerun()
        if st.button("戻る"):
            st.session_state['page'] = 'menu'
            st.rerun()
        return

    # --- ゲーム本編 ---
    mode = 'chem' if 'play_chem' in st.session_state['page'] else 'mol'
    rem = max(0, int(180 - (time.time() - st.session_state['start_time'])))

    if rem <= 0 and not st.session_state['game_over']:
        st.session_state['game_over'] = True
        save_ranking(st.session_state['player_name'], st.session_state['score'], mode)
        play_sound("finish")

    # ヘッダー
    cols = st.columns(3)
    cols[0].metric("Score", st.session_state['score'])
    cols[1].metric("Time", f"{rem}s")
    cols[2].metric("Correct", st.session_state['correct_count'])

    if st.session_state['game_over']:
        st.balloons()
        st.error(f"⌛ タイムアップ！ スコア: {st.session_state['score']}")
        st.table(load_ranking(mode).head(5))
        if st.button("メニューに戻る"):
            page = st.session_state['page']
            name = st.session_state['player_name']
            st.session_state.clear()
            st.session_state['page'] = 'menu'
            st.rerun()
        return

    # 正誤演出
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

    # --- 各モードのUI ---
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
            if icols[i % 2].button(ans, use_container_width=True, key=f"m_{i}"):
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
