import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo 15-2 Stat Pro", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .floating-nav {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        background-color: #702963;
        padding: 10px 20px;
        border-radius: 30px;
        border: 2px solid white;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .stDownloadButton > button {
        background-color: #2e7d32 !important;
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "Input"

if 'roster' not in st.session_state:
    st.session_state.roster = [
        "20 - Hadyn", "30 - Zooey", "1 - Taytem", "2 - Ella", "3 - Aditi", 
        "11 - Luna", "12 - Joy", "98 - Bria", "21 - Avery", "22 - Kannon"
    ]

# Column Definition
atk_cols = ['Atk ATM', 'Atk K', 'Atk ERR', 'Atk %']
srv_cols = ['Srv ATM', 'Srv ACE', 'Srv ERR', 'Srv %']
rec_cols = ['SrvRev ERR', 'SrvRev 1', 'SrvRev 2', 'SrvRev 3', 'SrvRev Avg']
def_cols = ['DIG', 'DIG ERR', 'Blk ERR', 'Blk S', 'Blk AS']
stat_cols = atk_cols + ['Set AST'] + srv_cols + def_cols + rec_cols

if 'set_dfs' not in st.session_state:
    st.session_state.set_dfs = {
        "Set 1": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols),
        "Set 2": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols),
        "Set 3": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols)
    }

# --- STATS CALCULATION & STYLING ---
def process_stats(df):
    df = df.copy()
    df['Atk %'] = ((df['Atk K'] - df['Atk ERR']) / df['Atk ATM'].replace(0,1)).round(3)
    df['Srv %'] = (((df['Srv ATM'] - df['Srv ERR']) / df['Srv ATM'].replace(0,1)) * 100).round(1)
    total_passes = df['SrvRev ERR'] + df['SrvRev 1'] + df['SrvRev 2'] + df['SrvRev 3']
    pass_pts = (df['SrvRev 1']*1) + (df['SrvRev 2']*2) + (df['SrvRev 3']*3)
    df['SrvRev Avg'] = (pass_pts / total_passes.replace(0,1)).round(2)
    return df

def apply_voodoo_style(df):
    player_colors = {
        "20 - Hadyn": "#FFEBEE", "30 - Zooey": "#E3F2FD", "1 - Taytem": "#F3E5F5",
        "2 - Ella": "#E8F5E9", "3 - Aditi": "#FFF3E0", "11 - Luna": "#F1F8E9",
        "12 - Joy": "#E0F2F1", "98 - Bria": "#FFF9C4", "21 - Avery": "#FCE4EC", "22 - Kannon": "#EFEBE9"
    }
    return df.style.apply(lambda x: [f'background-color: {player_colors.get(x.name, "")}' for i in x], axis=1)

# --- NAVIGATION BUTTON ---
st.markdown('<div class="floating-nav">', unsafe_allow_html=True)
if st.button(f"VIEW {'SCOREBOARD' if st.session_state.view_mode == 'Input' else 'ENTRY PAGE'}"):
    st.session_state.view_mode = "Scoreboard" if st.session_state.view_mode == "Input" else "Input"
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE ROUTING ---
if st.session_state.view_mode == "Input":
    st.title("⌨️ Entry Mode")
    active_set = st.radio("Current Set:", ["Set 1", "Set 2", "Set 3"], horizontal=True)
    st.session_state.set_dfs[active_set] = st.data_editor(
        st.session_state.set_dfs[active_set],
        use_container_width=True,
        height=500,
        key=f"edit_{active_set}"
    )
else:
    st.title("📊 Match Scoreboard")
    view_set = st.radio("Display:", ["Set 1", "Set 2", "Set 3", "Match Totals"], horizontal=True)
    
    if view_set == "Match Totals":
        raw_df = st.session_state.set_dfs["Set 1"] + st.session_state.set_dfs["Set 2"] + st.session_state.set_dfs["Set 3"]
    else:
        raw_df = st.session_state.set_dfs[view_set]
    
    final_df = process_stats(raw_df)
    st.table(apply_voodoo_style(final_df))
    
    # DOWNLOAD SECTION
    st.divider()
    st.subheader("💾 Export Match Data")
    csv = final_df.to_csv().encode('utf-8')
    st.download_button(
        label="Download Stats as CSV",
        data=csv,
        file_name=f"Voodoo_Stats_{view_set}.csv",
        mime='text/csv',
    )
