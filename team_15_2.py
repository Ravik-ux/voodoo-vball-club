import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo 15-2 Stat Pro", layout="wide")

# --- CUSTOM CSS FOR THE MODE SWITCHER ---
st.markdown("""
    <style>
    .floating-nav {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        background-color: #702963;
        padding: 15px 30px;
        border-radius: 50px;
        border: 3px solid #ffee32;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.5);
    }
    .stButton > button {
        font-size: 18px !important;
        font-weight: bold !important;
        color: white !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "ENTRY"

if 'roster' not in st.session_state:
    st.session_state.roster = [
        "20 - Hadyn", "30 - Zooey", "1 - Taytem", "2 - Ella", "3 - Aditi", 
        "11 - Luna", "12 - Joy", "98 - Bria", "21 - Avery", "22 - Kannon"
    ]

# Define Official Column Order
stat_cols = [
    'Played', 
    'Atk ATM', 'Atk K', 'Atk ERR', 'Atk %', 
    'Set AST', 
    'Srv ATM', 'Srv ACE', 'Srv ERR', 'Srv %', 
    'DIG', 'DIG ERR', 'Blk ERR', 'Blk S', 'Blk AS',
    'SrvRev ERR', 'SrvRev 1', 'SrvRev 2', 'SrvRev 3', 'SrvRev Avg'
]

if 'set_dfs' not in st.session_state:
    st.session_state.set_dfs = {
        "Set 1": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols),
        "Set 2": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols),
        "Set 3": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols)
    }

# --- LOGIC FUNCTIONS ---
def process_stats(df):
    df = df.copy()
    df['Atk %'] = ((df['Atk K'] - df['Atk ERR']) / df['Atk ATM'].replace(0,1)).round(3)
    df['Srv %'] = (((df['Srv ATM'] - df['Srv ERR']) / df['Srv ATM'].replace(0,1)) * 100).round(1)
    total_passes = df['SrvRev ERR'] + df['SrvRev 1'] + df['SrvRev 2'] + df['SrvRev 3']
    pass_pts = (df['SrvRev 1']*1) + (df['SrvRev 2']*2) + (df['SrvRev 3']*3)
    df['SrvRev Avg'] = (pass_pts / total_passes.replace(0,1)).round(2)
    return df

def apply_voodoo_style(df):
    # Distinct pastel colors for each player row
    player_colors = {
        "20 - Hadyn": "#FFEBEE", "30 - Zooey": "#E3F2FD", "1 - Taytem": "#F3E5F5",
        "2 - Ella": "#E8F5E9", "3 - Aditi": "#FFF3E0", "11 - Luna": "#F1F8E9",
        "12 - Joy": "#E0F2F1", "98 - Bria": "#FFF9C4", "21 - Avery": "#FCE4EC", "22 - Kannon": "#EFEBE9"
    }
    return df.style.apply(lambda x: [f'background-color: {player_colors.get(x.name, "#FFFFFF")}' for _ in x], axis=1)

# --- THE FLOATING SWITCHER ICON ---
st.markdown('<div class="floating-nav">', unsafe_allow_html=True)
button_label = "📊 SWITCH TO SUMMARY MODE" if st.session_state.view_mode == "ENTRY" else "⌨️ SWITCH TO ENTRY MODE"
if st.button(button_label):
    st.session_state.view_mode = "SUMMARY" if st.session_state.view_mode == "ENTRY" else "ENTRY"
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE ROUTING ---
if st.session_state.view_mode == "ENTRY":
    st.title("🏐 STAT ENTRY MODE")
    active_set = st.radio("Current Match Set:", ["Set 1", "Set 2", "Set 3"], horizontal=True)
    
    st.info("Tap a box below to enter stats. Use the purple button at the bottom to see colors.")
    
    st.session_state.set_dfs[active_set] = st.data_editor(
        st.session_state.set_dfs[active_set],
        use_container_width=True,
        height=500,
        key=f"editor_{active_set}"
    )

else:
    st.title("🏆 STAT SUMMARY MODE")
    view_set = st.radio("View Totals For:", ["Set 1", "Set 2", "Set 3", "Full Match"], horizontal=True)
    
    if view_set == "Full Match":
        # Sum only numeric columns
        raw_df = st.session_state.set_dfs["Set 1"] + st.session_state.set_dfs["Set 2"] + st.session_state.set_dfs["Set 3"]
    else:
        raw_df = st.session_state.set_dfs[view_set]
    
    final_df = process_stats(raw_df)
    
    st.subheader(f"Calculated Leaderboard: {view_set}")
    st.table(apply_voodoo_style(final_df))
    
    # DOWNLOAD OPTION
    csv = final_df.to_csv().encode('utf-8')
    st.download_button("📩 DOWNLOAD FINAL BOX SCORE", csv, f"Voodoo_{view_set}.csv", "text/csv")
