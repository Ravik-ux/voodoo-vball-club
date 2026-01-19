import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo 15-2 Tracker", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    div.stButton > button { height: 3.5em; font-weight: bold; font-size: 16px; }
    .selected-player { background-color: #702963; color: white; border-radius: 10px; 
                       padding: 15px; text-align: center; margin-bottom: 20px; 
                       font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
if 'roster' not in st.session_state:
    st.session_state.roster = sorted(["Zooey", "Aditi", "Taytem", "Hadyn", "Avery", "Bria", "Luna", "Joy", "Kannon", "Ella"])

if 'df' not in st.session_state:
    columns = ['Kills', 'Att_Errors', 'Total_Attacks', 'Aces', 'Serv_Errors', 'Digs', 'Blocks']
    st.session_state.df = pd.DataFrame(0, index=st.session_state.roster, columns=columns)

if 'active_player' not in st.session_state:
    st.session_state.active_player = st.session_state.roster[0]

if 'history' not in st.session_state:
    st.session_state.history = []

# --- HELPER FUNCTIONS ---
def update_stat(stat):
    player = st.session_state.active_player
    st.session_state.df.at[player, stat] += 1
    st.session_state.history.append((player, stat))
    if stat in ['Kills', 'Att_Errors']:
        st.session_state.df.at[player, 'Total_Attacks'] += 1

def undo_last():
    if st.session_state.history:
        player, stat = st.session_state.history.pop()
        st.session_state.df.at[player, stat] -= 1
        if stat in ['Kills', 'Att_Errors']:
            st.session_state.df.at[player, 'Total_Attacks'] -= 1

# --- SIDEBAR: CONTROLS ---
with st.sidebar:
    st.title("🏐 Voodoo 15-2")
    
    # ADMIN LOCK: Only show buttons if this is checked
    st.header("🔒 Access Control")
    is_admin = st.checkbox("Enable Entry Mode (Loggers Only)", value=False)
    
    st.divider()
    st.subheader("Match Info")
    current_set = st.selectbox("Set", ["Set 1", "Set 2", "Set 3", "Set 4", "Set 5"])
    opponent = st.text_input("Opponent", "Opponent Name")
    
    if is_admin:
        if st.button("⏪ UNDO LAST CLICK", use_container_width=True):
            undo_last()
            st.rerun()
        if st.button("Reset All Stats"):
            st.session_state.df[:] = 0
            st.session_state.history = []
            st.rerun()

    st.divider()
    st.header("📊 Final Report")
    csv = st.session_state.df.to_csv().encode('utf-8')
    st.download_button("Download CSV for Coach", csv, f"Voodoo_vs_{opponent}_{current_set}.csv", "text/csv")

# --- MAIN INTERFACE ---
st.title("Voodoo VolleyBall 15-2 | Live Stats")

if is_admin:
    # 1. PLAYER SELECTION
    st.subheader("1. Select Player")
    cols_per_row = 5
    rows = [st.session_state.roster[i:i + cols_per_row] for i in range(0, len(st.session_state.roster), cols_per_row)]
    for row in rows:
        cols = st.columns(cols_per_row)
        for i, name in enumerate(row):
            active = st.session_state.active_player == name
            if cols[i].button(name, key=f"sel_{name}", use_container_width=True, type="primary" if active else "secondary"):
                st.session_state.active_player = name
                st.rerun()

    st.markdown(f"<div class='selected-player'>TRACKING: {st.session_state.active_player}</div>", unsafe_allow_html=True)

    # 2. ACTION BUTTONS
    st.subheader("2. Record Action")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.button("🔥 KILL", on_click=update_stat, args=('Kills',), use_container_width=True)
        st.button("🎯 ACE", on_click=update_stat, args=('Aces',), use_container_width=True)
    with c2:
        st.button("💀 ATT ERR", on_click=update_stat, args=('Att_Errors',), use_container_width=True)
        st.button("❌ SERV ERR", on_click=update_stat, args=('Serv_Errors',), use_container_width=True)
    with c3:
        st.button("🛡️ DIG", on_click=update_stat, args=('Digs',), use_container_width=True)
        st.button("🚫 BLOCK", on_click=update_stat, args=('Blocks',), use_container_width=True)
    with c4:
        st.button("🏐 TOTAL ATT", on_click=update_stat, args=('Total_Attacks',), use_container_width=True)
else:
    st.info("👋 Viewing Mode: Buttons are hidden. Toggle 'Enable Entry Mode' in the sidebar to record stats.")

# --- BOX SCORE (Always Visible) ---
st.divider()
st.header(f"Live Box Score vs {opponent}")
df_display = st.session_state.df.copy()
denom = df_display['Total_Attacks'].replace(0, 1)
df_display['Hitting %'] = ((df_display['Kills'] - df_display['Att_Errors']) / denom).apply(lambda x: f"{x:.3f}")
st.dataframe(df_display, use_container_width=True)
