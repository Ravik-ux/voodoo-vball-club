import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo 15-2 Tracker", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .header-attack { color: white; background-color: #0077b6; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 5px; }
    .header-set { color: white; background-color: #2b9348; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 5px; }
    .header-block { color: black; background-color: #ffee32; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 5px; }
    .header-dig { color: white; background-color: #f25c54; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 5px; }
    .header-serve { color: white; background-color: #7209b7; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 10px; }

    div.stButton > button { height: 3.5em; font-weight: bold; font-size: 15px; border: 1px solid #ddd; }
    
    .score-box { background-color: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 10px; 
                 text-align: center; border: 2px solid #444; }
    .score-number { font-size: 40px; font-weight: bold; }
    
    .selected-player { background: linear-gradient(90deg, #702963 0%, #480ca8 100%); color: white; border-radius: 10px; 
                       padding: 15px; text-align: center; margin-bottom: 20px; font-size: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
if 'roster' not in st.session_state:
    st.session_state.roster = sorted(["Zooey", "Aditi", "Taytem", "Hadyn", "Avery", "Bria", "Luna", "Joy", "Kannon", "Ella"])

if 'df' not in st.session_state:
    columns = ['Attack-Kill', 'Attack-Err', 'Attack-Att', 'Set-Assist', 'Set-Err', 'Set-Att', 'Block-Solo', 'Block-Ast', 'Block-Err', 'Dig-Succ', 'Dig-Err', 'Serve-Good', 'Serve-Ace', 'Serve-Err']
    st.session_state.df = pd.DataFrame(0, index=st.session_state.roster, columns=columns)

if 'active_player' not in st.session_state:
    st.session_state.active_player = st.session_state.roster[0]

if 'history' not in st.session_state:
    st.session_state.history = []

if 'voodoo_score' not in st.session_state:
    st.session_state.voodoo_score = 0
if 'opp_score' not in st.session_state:
    st.session_state.opp_score = 0

# --- LOGIC ---
def update_stat(stat):
    player = st.session_state.active_player
    st.session_state.df.at[player, stat] += 1
    st.session_state.history.append((player, stat))
    
    if stat in ['Attack-Kill', 'Attack-Err']:
        st.session_state.df.at[player, 'Attack-Att'] += 1
    
    if stat in ['Attack-Kill', 'Serve-Ace', 'Block-Solo']:
        st.session_state.voodoo_score += 1
        
    if stat in ['Attack-Err', 'Serve-Err', 'Set-Err', 'Block-Err', 'Dig-Err']:
        st.session_state.opp_score += 1

def undo_last():
    if st.session_state.history:
        player, stat = st.session_state.history.pop()
        st.session_state.df.at[player, stat] -= 1
        if stat in ['Attack-Kill', 'Attack-Err']:
            st.session_state.df.at[player, 'Attack-Att'] -= 1
        if stat in ['Attack-Kill', 'Serve-Ace', 'Block-Solo']:
            st.session_state.voodoo_score = max(0, st.session_state.voodoo_score - 1)
        if stat in ['Attack-Err', 'Serve-Err', 'Set-Err', 'Block-Err', 'Dig-Err']:
            st.session_state.opp_score = max(0, st.session_state.opp_score - 1)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏐 Match Setup")
    opponent = st.text_input("Opponent Name", "Opponent")
    match_set = st.selectbox("Current Set", ["Set 1", "Set 2", "Set 3", "Set 4", "Set 5"])
    st.divider()
    if st.button("⏪ UNDO LAST ACTION", use_container_width=True):
        undo_last()
        st.rerun()
    if st.button("Reset Everything"):
        st.session_state.df[:] = 0
        st.session_state.voodoo_score = 0
        st.session_state.opp_score = 0
        st.session_state.history = []
        st.rerun()
    st.divider()
    csv = st.session_state.df.to_csv().encode('utf-8')
    st.download_button("📥 Download Stats", csv, f"Voodoo_Stats.csv", "text/csv")

# --- MAIN DASHBOARD ---
st.title(f"Voodoo 15-2 Tracker")

# 1. SCOREBOARD SECTION (With Manual Controls)
sc1, sc2, sc3 = st.columns([2, 1, 2])
with sc1:
    st.markdown(f"<div class='score-box'>VOODOO<br><span class='score-number'>{st.session_state.voodoo_score}</span></div>", unsafe_allow_html=True)
    b_add, b_sub = st.columns(2)
    if b_add.button("➕ Point", key="v_add", use_container_width=True): 
        st.session_state.voodoo_score += 1
        st.rerun()
    if b_sub.button("➖ Point", key="v_sub", use_container_width=True): 
        st.session_state.voodoo_score = max(0, st.session_state.voodoo_score - 1)
        st.rerun()

with sc2:
    st.markdown("<div style='text-align:center; font-size:30px; padding-top:15px;'>VS</div>", unsafe_allow_html=True)

with sc3:
    st.markdown(f"<div class='score-box'>{opponent.upper()}<br><span class='score-number'>{st.session_state.opp_score}</span></div>", unsafe_allow_html=True)
    o_add, o_sub = st.columns(2)
    if o_add.button("➕ Point", key="o_add", use_container_width=True): 
        st.session_state.opp_score += 1
        st.rerun()
    if o_sub.button("➖ Point", key="o_sub", use_container_width=True): 
        st.session_state.opp_score = max(0, st.session_state.opp_score - 1)
        st.rerun()

st.divider()

# 2. PLAYER SELECTION
st.subheader("1. Select Player")
p_cols = st.columns(5)
for i, name in enumerate(st.session_state.roster):
    active = st.session_state.active_player == name
    if p_cols[i % 5].button(name, key=f"sel_{name}", use_container_width=True, type="primary" if active else "secondary"):
        st.session_state.active_player = name
        st.rerun()

st.markdown(f"<div class='selected-player'>LOGGING: {st.session_state.active_player}</div>", unsafe_allow_html=True)

# 3. ACTION GRID
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("<div class='header-attack'>ATTACK</div>", unsafe_allow_html=True)
    st.button("🔥 Attack-Kill", on_click=update_stat, args=('Attack-Kill',), use_container_width=True)
    st.button("💀 Attack-Err", on_click=update_stat, args=('Attack-Err',), use_container_width=True)
    st.button("🏐 Attack-Att", on_click=update_stat, args=('Attack-Att',), use_container_width=True)
with c2:
    st.markdown("<div class='header-set'>SET</div>", unsafe_allow_html=True)
    st.button("🪄 Set-Assist", on_click=update_stat, args=('Set-Assist',), use_container_width=True)
    st.button("⚠️ Set-Err", on_click=update_stat, args=('Set-Err',), use_container_width=True)
    st.button("🏐 Set-Att", on_click=update_stat, args=('Set-Att',), use_container_width=True)
with c3:
    st.markdown("<div class='header-block'>BLOCK</div>", unsafe_allow_html=True)
    st.button("🧱 Block-Solo", on_click=update_stat, args=('Block-Solo',), use_container_width=True)
    st.button("🤝 Block-Ast", on_click=update_stat, args=('Block-Ast',), use_container_width=True)
    st.button("❌ Block-Err", on_click=update_stat, args=('Block-Err',), use_container_width=True)
with c4:
    st.markdown("<div class='header-dig'>DIG</div>", unsafe_allow_html=True)
    st.button("🛡️ Dig-Succ", on_click=update_stat, args=('Dig-Succ',), use_container_width=True)
    st.button("❌ Dig-Err", on_click=update_stat, args=('Dig-Err',), use_container_width=True)

st.divider()
st.markdown("<div class='header-serve'>SERVE</div>", unsafe_allow_html=True)
s1, s2, s3 = st.columns(3)
s1.button("✅ Serve-Good", on_click=update_stat, args=('Serve-Good',), use_container_width=True)
s2.button("🎯 Serve-Ace", on_click=update_stat, args=('Serve-Ace',), use_container_width=True)
s3.button("❌ Serve-Err", on_click=update_stat, args=('Serve-Err',), use_container_width=True)

# 4. TABLES
st.divider()
st.subheader("Player Breakdown")
df_display = st.session_state.df.copy()
p_atts = df_display['Attack-Att'].replace(0, 1)
df_display['Hit %'] = ((df_display['Attack-Kill'] - df_display['Attack-Err']) / p_atts).apply(lambda x: f"{x:.3f}")
st.dataframe(df_display, use_container_width=True)

st.divider()
st.subheader("🚨 TEAM TOTALS")
team_sum = st.session_state.df.sum().to_frame().T
team_sum.index = ["TEAM TOTAL"]
t_k, t_e, t_a = team_sum['Attack-Kill'].values[0], team_sum['Attack-Err'].values[0], team_sum['Attack-Att'].values[0]
team_sum['Hit %'] = f"{(t_k - t_e) / (t_a if t_a > 0 else 1):.3f}"

st.table(team_sum)
