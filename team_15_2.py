import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Voodoo 15-2 Stat Tracker", layout="wide")

# --- MOBILE CSS ---
st.markdown("""
    <style>
    div.stButton > button { height: 3.5em; font-weight: bold; border-radius: 8px; margin-bottom: 5px; }
    .score-box { background-color: #1e1e1e; color: #00ff00; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #444; }
    .score-val { font-size: 32px; font-weight: bold; }
    .section-header { padding: 4px; border-radius: 4px; text-align: center; font-weight: bold; margin-top: 10px; color: white; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
if 'roster' not in st.session_state:
    st.session_state.roster = [
        "20 - Hadyn", "30 - Zooey", "1 - Taytem", "2 - Ella", "3 - Aditi", 
        "11 - Luna", "12 - Joy", "98 - Bria", "21 - Avery", "22 - Kannon"
    ]

if 'set_data' not in st.session_state:
    # Columns matching your photo's logic
    cols = [
        'Atk-ATM', 'Atk-K', 'Atk-ERR', 
        'Srv-ATM', 'Srv-ACE', 'Srv-ERR',
        'Dig-DIG', 'Dig-ERR',
        'SrvRev-ERR', 'SrvRev-1', 'SrvRev-2', 'SrvRev-3',
        'Blk-ERR', 'Blk-S', 'Blk-AS'
    ]
    st.session_state.set_data = {
        "Set 1": pd.DataFrame(0, index=st.session_state.roster, columns=cols),
        "Set 2": pd.DataFrame(0, index=st.session_state.roster, columns=cols),
        "Set 3": pd.DataFrame(0, index=st.session_state.roster, columns=cols)
    }
    st.session_state.scores = {"Set 1": [0,0], "Set 2": [0,0], "Set 3": [0,0]}
    st.session_state.active_player = st.session_state.roster[0]

# --- SET TABS ---
set_tabs = st.tabs(["Set 1", "Set 2", "Set 3"])

for i, set_label in enumerate(["Set 1", "Set 2", "Set 3"]):
    with set_tabs[i]:
        df = st.session_state.set_data[set_label]
        
        # Scoreboard
        c1, c2, c3 = st.columns([2,1,2])
        with c1:
            st.markdown(f"<div class='score-box'>VOODOO<br><span class='score-val'>{st.session_state.scores[set_label][0]}</span></div>", unsafe_allow_html=True)
            if st.button("➕ Pt", key=f"v_up_{set_label}"):
                st.session_state.scores[set_label][0] += 1
                st.rerun()
        with c3:
            st.markdown(f"<div class='score-box'>OPP<br><span class='score-val'>{st.session_state.scores[set_label][1]}</span></div>", unsafe_allow_html=True)
            if st.button("➕ Pt", key=f"o_up_{set_label}"):
                st.session_state.scores[set_label][1] += 1
                st.rerun()

        # Input Section
        col_p, col_a = st.columns([1, 2])
        
        with col_p:
            st.write("**Player**")
            for player in st.session_state.roster:
                is_active = st.session_state.active_player == player
                if st.button(player, key=f"sel_{player}_{set_label}", type="primary" if is_active else "secondary"):
                    st.session_state.active_player = player
                    st.rerun()
        
        with col_a:
            active = st.session_state.active_player
            st.write(f"**Logging: {active}**")
            
            # ATTACK
            st.markdown("<div class='section-header' style='background-color:#0077b6;'>ATTACK</div>", unsafe_allow_html=True)
            a1, a2, a3 = st.columns(3)
            if a1.button("K", key=f"k_{set_label}"): 
                df.at[active, 'Atk-K'] += 1
                df.at[active, 'Atk-ATM'] += 1
                st.session_state.scores[set_label][0] += 1
            if a2.button("ERR", key=f"ae_{set_label}"): 
                df.at[active, 'Atk-ERR'] += 1
                df.at[active, 'Atk-ATM'] += 1
                st.session_state.scores[set_label][1] += 1
            if a3.button("ATM", key=f"aa_{set_label}"): df.at[active, 'Atk-ATM'] += 1

            # SERVE
            st.markdown("<div class='section-header' style='background-color:#7209b7;'>SERVE</div>", unsafe_allow_html=True)
            s1, s2, s3 = st.columns(3)
            if s1.button("ACE", key=f"ace_{set_label}"): 
                df.at[active, 'Srv-ACE'] += 1
                df.at[active, 'Srv-ATM'] += 1
                st.session_state.scores[set_label][0] += 1
            if s2.button("ERR", key=f"se_{set_label}"): 
                df.at[active, 'Srv-ERR'] += 1
                df.at[active, 'Srv-ATM'] += 1
                st.session_state.scores[set_label][1] += 1
            if s3.button("ATM", key=f"sa_{set_label}"): df.at[active, 'Srv-ATM'] += 1

            # SERVE RECEIVE
            st.markdown("<div class='section-header' style='background-color:#2b9348;'>SERVE RECEIVE</div>", unsafe_allow_html=True)
            sr0, sr1, sr2, sr3 = st.columns(4)
            if sr0.button("0", key=f"sr0_{set_label}"): 
                df.at[active, 'SrvRev-ERR'] += 1
                st.session_state.scores[set_label][1] += 1
            if sr1.button("1", key=f"sr1_{set_label}"): df.at[active, 'SrvRev-1'] += 1
            if sr2.button("2", key=f"sr2_{set_label}"): df.at[active, 'SrvRev-2'] += 1
            if sr3.button("3", key=f"sr3_{set_label}"): df.at[active, 'SrvRev-3'] += 1

            # DEFENSE
            st.markdown("<div class='section-header' style='background-color:#f25c54;'>BLOCK & DIG</div>", unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3)
            if b1.button("S-Blk", key=f"sb_{set_label}"): 
                df.at[active, 'Blk-S'] += 1
                st.session_state.scores[set_label][0] += 1
            if b2.button("AS-Blk", key=f"ab_{set_label}"): df.at[active, 'Blk-AS'] += 1
            if b3.button("DIG", key=f"dg_{set_label}"): df.at[active, 'Dig-DIG'] += 1

# --- BOX SCORE (AT THE BOTTOM) ---
st.divider()
st.header("Match Statistics")
view = st.radio("View:", ["Current Set", "Match Totals"], horizontal=True)

if view == "Match Totals":
    final_df = st.session_state.set_data["Set 1"] + st.session_state.set_data["Set 2"] + st.session_state.set_data["Set 3"]
else:
    # Logic to show the set currently being viewed is simpler as a selectbox for now
    s_choice = st.selectbox("Show stats for:", ["Set 1", "Set 2", "Set 3"])
    final_df = st.session_state.set_data[s_choice].copy()

# Calculations
final_df['Atk %'] = ((final_df['Atk-K'] - final_df['Atk-ERR']) / final_df['Atk-ATM'].replace(0,1)).round(3)
total_passes = final_df['SrvRev-ERR'] + final_df['SrvRev-1'] + final_df['SrvRev-2'] + final_df['SrvRev-3']
pass_points = (final_df['SrvRev-1'] * 1) + (final_df['SrvRev-2'] * 2) + (final_df['SrvRev-3'] * 3)
final_df['SrvRev Avg'] = (pass_points / total_passes.replace(0,1)).round(2)

st.dataframe(final_df, use_container_width=True)

# Download button for local saving
csv = final_df.to_csv().encode('utf-8')
st.download_button("Download CSV", csv, "voodoo_stats.csv", "text/csv")
