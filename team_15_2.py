import streamlit as st
import pandas as pd
import numpy as np
import matplotlib

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo 15-2 Tracker", layout="wide")

# --- IPAD OPTIMIZED CSS ---
st.markdown("""
    <style>
    /* Dark theme for easier eyes in bright gyms */
    .stApp { background-color: #0e1117; }
    
    /* The Entry Grid Styling */
    [data-testid="stDataEditor"] {
        background-color: #1a1c23; 
        border: 2px solid #3d4452;
        border-radius: 12px;
    }

    /* The Floating Mode Switcher at Bottom Middle */
    .floating-nav {
        position: fixed; 
        bottom: 30px; 
        left: 50%; 
        transform: translateX(-50%);
        z-index: 9999; 
        background-color: #00ffcc; 
        padding: 10px 30px;
        border-radius: 50px; 
        border: 2px solid #ffffff;
        box-shadow: 0px 10px 30px rgba(0,255,204,0.4);
    }
    
    /* Mode Switch Button Text */
    .floating-nav button {
        color: #000000 !important;
        font-weight: bold !important;
        background-color: transparent !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161920;
        border-right: 1px solid #3d4452;
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

# Default Order of Stats (Until you send the drawing!)
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

# --- MATH LOGIC ---
def calculate_metrics(df):
    df = df.copy()
    for col in df.columns:
        if col not in ['Atk %', 'Srv %', 'SrvRev Avg']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Hitting %: (K-E)/Att
    df['Atk %'] = (df['Atk K'] - df['Atk ERR']) / df['Atk ATM'].replace(0, np.nan)
    
    # Serve %: (Att-E)/Att * 100
    df['Srv %'] = ((df['Srv ATM'] - df['Srv ERR']) / df['Srv ATM'].replace(0, np.nan)) * 100
    
    # Pass Rating: Weighted average
    total_passes = df['SrvRev ERR'] + df['SrvRev 1'] + df['SrvRev 2'] + df['SrvRev 3']
    pass_pts = (df['SrvRev 1']*1) + (df['SrvRev 2']*2) + (df['SrvRev 3']*3)
    df['SrvRev Avg'] = pass_pts / total_passes.replace(0, np.nan)
    
    return df.fillna(0)

# --- SIDEBAR (Download & Match Totals) ---
with st.sidebar:
    st.title("🏐 VOODOO 15-2")
    st.write("---")
    st.subheader("Match Export")
    
    # Quick Match Totals Math
    full_match = st.session_state.master_data["Set 1"] + st.session_state.master_data["Set 2"] + st.session_state.master_data["Set 3"]
    match_report = calculate_metrics(full_match)
    
    csv = match_report.to_csv().encode('utf-8')
    st.download_button(
        label="📩 DOWNLOAD CSV REPORT",
        data=csv,
        file_name="Voodoo_Full_Match.csv",
        mime='text/csv',
    )
    st.write("---")
    st.caption("Tip: Switch to Summary Mode to see player-by-player percentages.")

# --- NAVIGATION BUTTON ---
st.markdown('<div class="floating-nav">', unsafe_allow_html=True)
label = "📊 VIEW SUMMARY MODE" if st.session_state.view_mode == "ENTRY" else "⌨️ RETURN TO ENTRY"
if st.button(label):
    st.session_state.view_mode = "SUMMARY" if st.session_state.view_mode == "ENTRY" else "ENTRY"
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE ROUTING ---
if st.session_state.view_mode == "ENTRY":
    st.title("⌨️ STAT ENTRY")
    active_set = st.radio("Select Set:", ["Set 1", "Set 2", "Set 3"], horizontal=True)
    
    # Data Entry Grid (Math is disabled here for stability)
    edited_df = st.data_editor(
        st.session_state.master_data[active_set],
        use_container_width=True,
        height=550,
        key=f"editor_{active_set}"
    )
    st.session_state.master_data[active_set] = edited_df

else:
    st.title("🏆 SUMMARY MODE")
    view_set = st.radio("Display:", ["Set 1", "Set 2", "Set 3", "Match Totals"], horizontal=True)
    
    if view_set == "Match Totals":
        raw = st.session_state.master_data["Set 1"] + st.session_state.master_data["Set 2"] + st.session_state.master_data["Set 3"]
    else:
        raw = st.session_state.master_data[view_set]
    
    final_df = calculate_metrics(raw)
    
    # High-Contrast Color Table
    st.table(
        final_df.style.format({
            'Atk %': '{:.3f}', 
            'Srv %': '{:.1f}%', 
            'SrvRev Avg': '{:.2f}'
        }).background_gradient(cmap='Greens', subset=['Atk %', 'SrvRev Avg'])
    )
