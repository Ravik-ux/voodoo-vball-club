import streamlit as st
import pandas as pd
import numpy as np

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo 15-2 Stable Tracker", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .floating-nav {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        z-index: 9999; background-color: #702963; padding: 15px 30px;
        border-radius: 50px; border: 3px solid #ffee32;
    }
    .stButton > button { font-weight: bold; color: white; }
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

stat_cols = [
    'Played', 'Atk ATM', 'Atk K', 'Atk ERR', 'Atk %', 
    'Set AST', 'Srv ATM', 'Srv ACE', 'Srv ERR', 'Srv %', 
    'DIG', 'DIG ERR', 'Blk ERR', 'Blk S', 'Blk AS',
    'SrvRev ERR', 'SrvRev 1', 'SrvRev 2', 'SrvRev 3', 'SrvRev Avg'
]

if 'master_data' not in st.session_state:
    st.session_state.master_data = {
        "Set 1": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols),
        "Set 2": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols),
        "Set 3": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols)
    }

# --- LOGIC ---
def calculate_metrics(df):
    df = df.copy()
    # Ensure all data is numeric before math
    for col in df.columns:
        if col not in ['Atk %', 'Srv %', 'SrvRev Avg']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
    # Atk % Calculation
    df['Atk %'] = ((df['Atk K'] - df['Atk ERR']) / df['Atk ATM'].replace(0, np.nan))
    
    # Srv % Calculation
    df['Srv %'] = ((df['Srv ATM'] - df['Srv ERR']) / df['Srv ATM'].replace(0, np.nan)) * 100
    
    # SrvRev Avg Calculation
    total_passes = df['SrvRev ERR'] + df['SrvRev 1'] + df['SrvRev 2'] + df['SrvRev 3']
    pass_pts = (df['SrvRev 1']*1) + (df['SrvRev 2']*2) + (df['SrvRev 3']*3)
    df['SrvRev Avg'] = (pass_pts / total_passes.replace(0, np.nan))
    
    return df.fillna(0) # Replace NaNs with 0 for the final display

# --- NAVIGATION ---
st.markdown('<div class="floating-nav">', unsafe_allow_html=True)
label = "📊 VIEW SUMMARY" if st.session_state.view_mode == "ENTRY" else "⌨️ RETURN TO ENTRY"
if st.button(label):
    st.session_state.view_mode = "SUMMARY" if st.session_state.view_mode == "ENTRY" else "ENTRY"
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- PAGES ---
if st.session_state.view_mode == "ENTRY":
    st.title("🏐 DATA ENTRY")
    active_set = st.radio("Current Set:", ["Set 1", "Set 2", "Set 3"], horizontal=True)
    
    # Grid Entry
    edited_df = st.data_editor(
        st.session_state.master_data[active_set],
        use_container_width=True,
        height=500,
        key=f"editor_{active_set}"
    )
    st.session_state.master_data[active_set] = edited_df

else:
    st.title("🏆 SUMMARY MODE")
    view_set = st.radio("Show Stats for:", ["Set 1", "Set 2", "Set 3", "Match Totals"], horizontal=True)
    
    if view_set == "Match Totals":
        raw = st.session_state.master_data["Set 1"] + st.session_state.master_data["Set 2"] + st.session_state.master_data["Set 3"]
    else:
        raw = st.session_state.master_data[view_set]
    
    final_df = calculate_metrics(raw)
    
    # FIXED STYLING (Removed set_precision)
    st.table(
        final_df.style.format({
            'Atk %': '{:.3f}', 
            'Srv %': '{:.1f}%', 
            'SrvRev Avg': '{:.2f}'
        }).background_gradient(cmap='Greens', subset=['Atk %', 'SrvRev Avg'])
    )
