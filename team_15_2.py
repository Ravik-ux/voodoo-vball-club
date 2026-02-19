import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo Live Grid", layout="wide")

# --- DATA INITIALIZATION ---
if 'roster' not in st.session_state:
    st.session_state.roster = [
        "20 - Hadyn", "30 - Zooey", "1 - Taytem", "2 - Ella", "3 - Aditi", 
        "11 - Luna", "12 - Joy", "98 - Bria", "21 - Avery", "22 - Kannon"
    ]

# Columns in the EXACT order of your photo
stat_cols = [
    'Played', 'Atk ATM', 'Atk K', 'Atk ERR', 'Atk %', 
    'Set AST', 'Srv ATM', 'Srv ACE', 'Srv ERR', 'Srv %', 
    'DIG', 'DIG ERR', 'SrvRev ERR', 'SrvRev 1', 'SrvRev 2', 
    'SrvRev 3', 'SrvRev Avg', 'Blk ERR', 'Blk S', 'Blk AS'
]

if 'set_data' not in st.session_state:
    # Initialize with 0s
    st.session_state.set_data = {
        "Set 1": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols),
        "Set 2": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols),
        "Set 3": pd.DataFrame(0, index=st.session_state.roster, columns=stat_cols)
    }

# --- TOP NAVIGATION ---
st.title("🏐 Voodoo 15-2 Live Stats")
tabs = st.tabs(["Set 1", "Set 2", "Set 3"])

for i, set_name in enumerate(["Set 1", "Set 2", "Set 3"]):
    with tabs[i]:
        st.write(f"### {set_name} - Edit Boxes Directly")
        
        # This makes the table interactive
        edited_df = st.data_editor(
            st.session_state.set_data[set_name],
            use_container_width=True,
            height=500,
            key=f"editor_{set_name}"
        )
        
        # Auto-calculate percentages based on your edits
        # (These update whenever you click off a cell)
        edited_df['Atk %'] = ((edited_df['Atk K'] - edited_df['Atk ERR']) / edited_df['Atk ATM'].replace(0,1)).round(3)
        
        srv_total = edited_df['Srv ATM'].replace(0,1)
        edited_df['Srv %'] = ((edited_df['Srv ATM'] - edited_df['Srv ERR']) / srv_total * 100).round(1)
        
        total_passes = edited_df['SrvRev ERR'] + edited_df['SrvRev 1'] + edited_df['SrvRev 2'] + edited_df['SrvRev 3']
        pass_pts = (edited_df['SrvRev 1']*1) + (edited_df['SrvRev 2']*2) + (edited_df['SrvRev 3']*3)
        edited_df['SrvRev Avg'] = (pass_pts / total_passes.replace(0,1)).round(2)

        # Save the changes back to state
        st.session_state.set_data[set_name] = edited_df

# --- TOTALS SUMMARY ---
st.divider()
if st.checkbox("Show Combined Match Totals"):
    match_total = st.session_state.set_data["Set 1"] + st.session_state.set_data["Set 2"] + st.session_state.set_data["Set 3"]
    st.write("### Season/Match Record")
    st.dataframe(match_total, use_container_width=True)
