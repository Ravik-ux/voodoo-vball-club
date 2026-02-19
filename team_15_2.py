import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo 15-2 Color Dashboard", layout="wide")

# --- INITIALIZATION ---
if 'roster' not in st.session_state:
    st.session_state.roster = [
        "20 - Hadyn", "30 - Zooey", "1 - Taytem", "2 - Ella", "3 - Aditi", 
        "11 - Luna", "12 - Joy", "98 - Bria", "21 - Avery", "22 - Kannon"
    ]

# Define Groups for Coloring
atk_cols = ['Atk ATM', 'Atk K', 'Atk ERR', 'Atk %']
srv_cols = ['Srv ATM', 'Srv ACE', 'Srv ERR', 'Srv %']
rec_cols = ['SrvRev ERR', 'SrvRev 1', 'SrvRev 2', 'SrvRev 3', 'SrvRev Avg']
def_cols = ['DIG', 'DIG ERR', 'Blk ERR', 'Blk S', 'Blk AS']
stat_cols = atk_cols + ['Set AST'] + srv_cols + def_cols + rec_cols

# Create DataFrames
if 'set_dfs' not in st.session_state:
    st.session_state.set_dfs = {
        "Set 1": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols),
        "Set 2": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols),
        "Set 3": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols)
    }

# --- STYLING LOGIC ---
def apply_voodoo_style(df):
    df = df.copy()
    # Math Calculations
    df['Atk %'] = ((df['Atk K'] - df['Atk ERR']) / df['Atk ATM'].replace(0,1)).round(3)
    df['Srv %'] = (((df['Srv ATM'] - df['Srv ERR']) / df['Srv ATM'].replace(0,1)) * 100).round(1)
    total_passes = df['SrvRev ERR'] + df['SrvRev 1'] + df['SrvRev 2'] + df['SrvRev 3']
    pass_pts = (df['SrvRev 1']*1) + (df['SrvRev 2']*2) + (df['SrvRev 3']*3)
    df['SrvRev Avg'] = (pass_pts / total_passes.replace(0,1)).round(2)
    
    # Assign colors to player rows
    player_colors = {
        "20 - Hadyn": "#FFEBEE", "30 - Zooey": "#E3F2FD", "1 - Taytem": "#F3E5F5",
        "2 - Ella": "#E8F5E9", "3 - Aditi": "#FFF3E0", "11 - Luna": "#F1F8E9",
        "12 - Joy": "#E0F2F1", "98 - Bria": "#FFF9C4", "21 - Avery": "#FCE4EC", "22 - Kannon": "#EFEBE9"
    }

    styled = df.style.apply(lambda x: [f'background-color: {player_colors.get(x.name, "")}' for i in x], axis=1)
    
    # Highlight specific stat columns with distinct headers
    styled = styled.set_properties(subset=atk_cols, **{'border': '1px solid #2196F3'}) \
                   .set_properties(subset=srv_cols, **{'border': '1px solid #9C27B0'}) \
                   .set_properties(subset=rec_cols, **{'border': '1px solid #4CAF50'})
    return styled

# --- UI TABS ---
st.title("🏐 Voodoo 15-2 Stat Entry")
current_set = st.radio("Select Active Set:", ["Set 1", "Set 2", "Set 3"], horizontal=True)

# THE INPUT BOX (The Grid you touch)
st.subheader(f"Edit {current_set} Data Below:")
st.session_state.set_dfs[current_set] = st.data_editor(
    st.session_state.set_dfs[current_set],
    use_container_width=True,
    height=400,
    key=f"editor_{current_set}"
)

# THE LIVE SCOREBOARD (The Colorful View)
st.divider()
st.subheader(f"📊 {current_set} Live Scoreboard (Calculated)")
st.table(apply_voodoo_style(st.session_state.set_dfs[current_set]))
