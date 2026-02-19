import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo High-Viz Tracker", layout="wide")

# --- CUSTOM CSS FOR BUTTONS AND LAYOUT ---
st.markdown("""
    <style>
    .stDataFrame { border: 2px solid #702963; border-radius: 10px; }
    div.stButton > button { background-color: #702963; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'roster' not in st.session_state:
    st.session_state.roster = [
        "20 - Hadyn", "30 - Zooey", "1 - Taytem", "2 - Ella", "3 - Aditi", 
        "11 - Luna", "12 - Joy", "98 - Bria", "21 - Avery", "22 - Kannon"
    ]

# Define Column Groups for Coloring
atk_cols = ['Atk ATM', 'Atk K', 'Atk ERR', 'Atk %']
srv_cols = ['Srv ATM', 'Srv ACE', 'Srv ERR', 'Srv %']
rec_cols = ['SrvRev ERR', 'SrvRev 1', 'SrvRev 2', 'SrvRev 3', 'SrvRev Avg']
def_cols = ['DIG', 'DIG ERR', 'Blk ERR', 'Blk S', 'Blk AS']

stat_cols = atk_cols + ['Set AST'] + srv_cols + def_cols + rec_cols

if 'set1_df' not in st.session_state:
    st.session_state.set1_df = pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols)
# (Repeat for Set 2 and 3 in your full code)

# --- STYLING FUNCTION ---
def style_voodoo_df(df):
    # Apply Math
    df = df.copy()
    df['Atk %'] = ((df['Atk K'] - df['Atk ERR']) / df['Atk ATM'].replace(0,1)).round(3)
    df['Srv %'] = (((df['Srv ATM'] - df['Srv ERR']) / df['Srv ATM'].replace(0,1)) * 100).round(1)
    
    total_passes = df['SrvRev ERR'] + df['SrvRev 1'] + df['SrvRev 2'] + df['SrvRev 3']
    pass_pts = (df['SrvRev 1']*1) + (df['SrvRev 2']*2) + (df['SrvRev 3']*3)
    df['SrvRev Avg'] = (pass_pts / total_passes.replace(0,1)).round(2)

    # Apply Colors to Metric Groups
    return df.style \
        .set_properties(subset=atk_cols, **{'background-color': '#e3f2fd', 'color': 'black'}) \
        .set_properties(subset=srv_cols, **{'background-color': '#f3e5f5', 'color': 'black'}) \
        .set_properties(subset=rec_cols, **{'background-color': '#e8f5e9', 'color': 'black'}) \
        .set_properties(subset=def_cols, **{'background-color': '#fff3e0', 'color': 'black'}) \
        .apply(lambda x: ['background-color: #f9f9f9' if i % 2 == 0 else '' for i in range(len(x))], axis=0)

# --- UI ---
st.title("🏐 Voodoo 15-2 Pro Color Tracker")
t1, t2, t3 = st.tabs(["Set 1", "Set 2", "Set 3"])

with t1:
    # We display the styled version but edit the raw version
    st.session_state.set1_df = st.data_editor(
        style_voodoo_df(st.session_state.set1_df),
        use_container_width=True,
        height=480,
        key="color_editor_s1"
    )

# --- TOTALS ---
st.divider()
if st.checkbox("Show Colorful Match Totals"):
    combined = st.session_state.set1_df # Plus others
    st.dataframe(style_voodoo_df(combined), use_container_width=True)
