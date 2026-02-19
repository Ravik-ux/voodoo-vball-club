import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo Tournament Stats", layout="wide")

# --- CSS TO MAKE IT LOOK LIKE THE PRO TABLE ---
st.markdown("""
    <style>
    .stDataFrame { border: 1px solid #444; }
    div.stButton > button { height: 3em; font-size: 14px !important; font-weight: bold; border-radius: 4px; }
    .score-text { font-size: 24px; font-weight: bold; color: #00ff00; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
if 'roster' not in st.session_state:
    # Exact order and names/numbers
    st.session_state.roster = [
        "20 - Hadyn", "30 - Zooey", "1 - Taytem", "2 - Ella", "3 - Aditi", 
        "11 - Luna", "12 - Joy", "98 - Bria", "21 - Avery", "22 - Kannon"
    ]

# Columns in the EXACT order shown in the photo
stat_cols = [
    'Played', 'Atk ATM', 'Atk K', 'Atk ERR', 'Atk %', 
    'Set AST', 'Srv ATM', 'Srv ACE', 'Srv ERR', 'Srv %', 
    'DIG', 'DIG ERR', 'SrvRev ERR', 'SrvRev 1', 'SrvRev 2', 
    'SrvRev 3', 'SrvRev Avg', 'Blk ERR', 'Blk S', 'Blk AS'
]

if 'set_data' not in st.session_state:
    st.session_state.set_data = {
        "Set 1": pd.DataFrame(0.0, index=st.session_state.roster, columns=stat_cols),
        "Set 2": pd.DataFrame(0.0, index=st.session_state.roster, columns=stat_cols),
        "Set 3": pd.DataFrame(0.0, index=st.session_state.roster, columns=stat_cols)
    }
    st.session_state.scores = {"Set 1": [0,0], "Set 2": [0,0], "Set 3": [0,0]}
    st.session_state.active_player = st.session_state.roster[0]

# --- TOP NAVIGATION (SETS) ---
st.write(f"### Match vs. Opponent")
st_tab1, st_tab2, st_tab3 = st.tabs(["Set 1", "Set 2", "Set 3"])

def render_set(set_name):
    df = st.session_state.set_data[set_name]
    
    # Header: Score and Active Player
    c1, c2, c3 = st.columns([1,2,1])
    with c1:
        st.write(f"**VOODOO: {st.session_state.scores[set_name][0]}**")
    with c2:
        st.session_state.active_player = st.selectbox(f"Select Player to Stat ({set_name})", st.session_state.roster, key=f"select_{set_name}")
    with c3:
        st.write(f"**OPP: {st.session_state.scores[set_name][1]}**")

    # ACTION BUTTONS (Compact Grid)
    active = st.session_state.active_player
    
    col_atk, col_srv, col_rec, col_def = st.columns(4)
    
    with col_atk:
        st.caption("ATTACK")
        bt1, bt2 = st.columns(2)
        if bt1.button("K", key=f"k_{set_name}"):
            df.at[active, 'Atk K'] += 1
            df.at[active, 'Atk ATM'] += 1
            st.session_state.scores[set_name][0] += 1
        if bt2.button("E", key=f"e_{set_name}"):
            df.at[active, 'Atk ERR'] += 1
            df.at[active, 'Atk ATM'] += 1
            st.session_state.scores[set_name][1] += 1
            
    with col_srv:
        st.caption("SERVE")
        bs1, bs2 = st.columns(2)
        if bs1.button("ACE", key=f"ace_{set_name}"):
            df.at[active, 'Srv ACE'] += 1
            df.at[active, 'Srv ATM'] += 1
            st.session_state.scores[set_name][0] += 1
        if bs2.button("ERR", key=f"se_{set_name}"):
            df.at[active, 'Srv ERR'] += 1
            df.at[active, 'Srv ATM'] += 1
            st.session_state.scores[set_name][1] += 1

    with col_rec:
        st.caption("PASS (0-3)")
        r1, r2, r3, r4 = st.columns(4)
        if r1.button("0", key=f"r0_{set_name}"): 
            df.at[active, 'SrvRev ERR'] += 1
            st.session_state.scores[set_name][1] += 1
        if r2.button("1", key=f"r1_{set_name}"): df.at[active, 'SrvRev 1'] += 1
        if r3.button("2", key=f"r2_{set_name}"): df.at[active, 'SrvRev 2'] += 1
        if r4.button("3", key=f"r3_{set_name}"): df.at[active, 'SrvRev 3'] += 1

    with col_def:
        st.caption("BLOCK/DIG")
        d1, d2, d3 = st.columns(3)
        if d1.button("S", key=f"s_{set_name}"): 
            df.at[active, 'Blk S'] += 1
            st.session_state.scores[set_name][0] += 1
        if d2.button("AS", key=f"as_{set_name}"): df.at[active, 'Blk AS'] += 1
        if d3.button("D", key=f"d_{set_name}"): df.at[active, 'DIG'] += 1

    # CALCULATIONS
    df['Atk %'] = ((df['Atk K'] - df['Atk ERR']) / df['Atk ATM'].replace(0,1)).round(3)
    df['Srv %'] = ((df['Srv ATM'] - df['Srv ERR']) / df['Srv ATM'].replace(0,1)).round(2)
    
    total_passes = df['SrvRev ERR'] + df['SrvRev 1'] + df['SrvRev 2'] + df['SrvRev 3']
    pass_pts = (df['SrvRev 1']*1) + (df['SrvRev 2']*2) + (df['SrvRev 3']*3)
    df['SrvRev Avg'] = (pass_pts / total_passes.replace(0,1)).round(2)

    # THE GRID (The Main Attraction)
    st.write("### Live Set Statistics")
    st.dataframe(df.style.format(precision=3), use_container_width=True, height=450)

with st_tab1: render_set("Set 1")
with st_tab2: render_set("Set 2")
with st_tab3: render_set("Set 3")

# --- MATCH TOTALS AT THE VERY BOTTOM ---
st.divider()
if st.checkbox("Show Match Totals"):
    total_df = st.session_state.set_data["Set 1"] + st.session_state.set_data["Set 2"] + st.session_state.set_data["Set 3"]
    st.write("### Full Match Totals")
    st.dataframe(total_df, use_container_width=True)
