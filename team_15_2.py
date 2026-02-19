import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo 15-2 Pro Tracker", layout="wide")

# --- INITIALIZATION ---
if 'roster' not in st.session_state:
    st.session_state.roster = [
        "20 - Hadyn", "30 - Zooey", "1 - Taytem", "2 - Ella", "3 - Aditi", 
        "11 - Luna", "12 - Joy", "98 - Bria", "21 - Avery", "22 - Kannon"
    ]

# The Column Order (We can re-order these exactly how you want next)
stat_cols = [
    'Played', 'Atk ATM', 'Atk K', 'Atk ERR', 'Atk %', 
    'Set AST', 'Srv ATM', 'Srv ACE', 'Srv ERR', 'Srv %', 
    'DIG', 'DIG ERR', 'SrvRev ERR', 'SrvRev 1', 'SrvRev 2', 
    'SrvRev 3', 'SrvRev Avg', 'Blk ERR', 'Blk S', 'Blk AS'
]

# Create the empty dataframes if they don't exist
if 'set1_df' not in st.session_state:
    st.session_state.set1_df = pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols)
if 'set2_df' not in st.session_state:
    st.session_state.set2_df = pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols)
if 'set3_df' not in st.session_state:
    st.session_state.set3_df = pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols)

# --- TABS ---
st.title("🏐 Voodoo Live Scorebook")
t1, t2, t3 = st.tabs(["Set 1", "Set 2", "Set 3"])

# Function to calculate percentages for the grid
def apply_math(df):
    df = df.copy()
    # Atk % = (K-E)/Total
    df['Atk %'] = ((df['Atk K'] - df['Atk ERR']) / df['Atk ATM'].replace(0,1)).round(3)
    # Srv % = (Total-E)/Total
    df['Srv %'] = (((df['Srv ATM'] - df['Srv ERR']) / df['Srv ATM'].replace(0,1)) * 100).round(1)
    # SrvRev Avg = (1*1 + 2*2 + 3*3) / Total Passes
    total_passes = df['SrvRev ERR'] + df['SrvRev 1'] + df['SrvRev 2'] + df['SrvRev 3']
    pass_pts = (df['SrvRev 1']*1) + (df['SrvRev 2']*2) + (df['SrvRev 3']*3)
    df['SrvRev Avg'] = (pass_pts / total_passes.replace(0,1)).round(2)
    return df

# --- SET 1 ---
with t1:
    st.session_state.set1_df = st.data_editor(
        apply_math(st.session_state.set1_df),
        key="editor_set1",
        use_container_width=True,
        height=450
    )

# --- SET 2 ---
with t2:
    st.session_state.set2_df = st.data_editor(
        apply_math(st.session_state.set2_df),
        key="editor_set2",
        use_container_width=True,
        height=450
    )

# --- SET 3 ---
with t3:
    st.session_state.set3_df = st.data_editor(
        apply_math(st.session_state.set3_df),
        key="editor_set3",
        use_container_width=True,
        height=450
    )

# --- DOWNLOAD FOR RECORD ---
st.divider()
if st.button("Generate Final Match Report"):
    match_total = st.session_state.set1_df + st.session_state.set2_df + st.session_state.set3_df
    # Re-apply math to totals
    match_total = apply_math(match_total)
    st.write("### Combined Match Totals")
    st.dataframe(match_total, use_container_width=True)
    
    csv = match_total.to_csv().encode('utf-8')
    st.download_button("Download Match CSV", csv, "match_totals.csv", "text/csv")
