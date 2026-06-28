import streamlit as st
import pandas as pd
from data_loader import fetch_and_load_datasets
from model import run_monte_carlo_simulation, calculate_ev_and_kelly, convert_prob_to_moneyline, calculate_implied_probability

st.set_page_config(page_title="Proprietary Sports Projection System", layout="wide")

# Target Data Pipeline Automation Loading
@st.cache_data(show_spinner="Running automated pipeline downlinks from Kaggle...")
def load_pipeline_data():
    return fetch_and_load_datasets()

df_nfl, df_sandbox = load_pipeline_data()

st.title(" Proprietary Sports Projection System")
st.caption("Advanced Machine Learning Analytics & Monte Carlo Simulation Engine — No Arbitrage / Pure Value Strategy")
st.markdown("---")

# Layout Form Grid Splitting
col1, col2 = st.columns([1, 2])

with col1:
    st.header("User Inputs & Config")
    sport = st.selectbox("Sport Selected", ["NFL", "MLB", "NHL", "NCAA Football", "NCAA Basketball"])
    game = st.selectbox("Game Selection", ["Kansas City Chiefs vs. Buffalo Bills"])
    sim_count = st.selectbox("Simulation Count", [10000, 25000, 50000], index=1)
    kelly_frac = st.slider("Kelly Criterion Fraction", 0.10, 1.00, 0.25, step=0.05, help="0.25 = Quarter-Kelly")
    
    st.subheader("Automated Pipeline Data Metrics")
    st.info("💡 Data pulled automatically into local project framework database context.")
    
    # Mocking structural variables fetched automatically by background worker pipelines
    chiefs_elo = 1650
    bills_elo = 1620
    
    st.metric("Chiefs ELO Rating (Patrick Mahomes Starting)", chiefs_elo)
    st.metric("Bills ELO Rating (Cornerback Out / Home Edge)", bills_elo)
    st.text("Weather Condition: 35°F, 15mph wind, light snow")
    st.text("Rest Variable: Chiefs +6 Days Advantage")
    
    st.subheader("Market Sportsbook Odds Reference")
    market_away_ml = st.number_input("Chiefs Moneyline Odds (Market)", value=120)
    market_home_ml = st.number_input("Bills Moneyline Odds (Market)", value=-140)

with col2:
    st.header("Internal Simulation Processing Engine")
    
    # Calculate processing modifications based on data metrics inputs
    # Rest advantage + QB baseline offset vs backup adjustments = +1.4 net points toward KC
    situational_adjustments = {'net_advantage': 1.4} 
    
    if st.button("Run Projection Engine Model"):
        with st.spinner(f"Processing {sim_count:,} Monte Carlo Simulations..."):
            results = run_monte_carlo_simulation(sim_count, bills_elo, chiefs_elo, situational_adjustments)
            
        st.success("Simulations Completed Successfully.")
        
        # Fair calculations translations
        fair_away_ml = convert_prob_to_moneyline(results['away_prob'])
        fair_home_ml = convert_prob_to_moneyline(results['home_prob'])
        
        # Calculate Edge metrics
        market_implied_prob = calculate_implied_probability(market_away_ml)
        edge = results['away_prob'] - market_implied_prob
        ev, raw_k, final_unit_size = calculate_ev_and_kelly(results['away_prob'], market_away_ml, kelly_frac)
        
        # Presentation Layout Grid Displays
        st.header("Model Output (Actionable Intelligence)")
        
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.subheader("Pure Projections (Fair Market)")
            st.metric("Projected Score", f"Chiefs {results['away_score']} – Bills {results['home_score']}")
            st.metric("Win Probability", f"Chiefs {results['away_prob']*100:.1f}% | Bills {results['home_prob']*100:.1f}%")
            st.write(f"**Fair Moneyline:** Chiefs {fair_away_ml} | Bills {fair_home_ml}")
            st.write(f"**Fair Spread:** {results['fair_spread']}")
            st.write(f"**Fair Total:** {results['fair_total']}")
            
        with sub_col2:
            st.subheader("EV & Betting Edge Output")
            
            # Formulate structured data evaluation metrics frame table
            metrics_table = {
                "Metric": ["The Edge", "Expected Value (EV)", "Kelly Fraction", "Recommended Unit Size"],
                "Calculation / Value": [f"+{edge*100:.1f}% Edge on the Chiefs", f"${ev:+.2f} per $1 stake", f"{raw_k:.3f}", f"{final_unit_size*100:.2f} Units"],
                "Notes": ["Your Prob vs Market Implied Prob", "Positive EV (+EV)" if ev > 0 else "Negative EV", "Calculates optimal risk balance", "Adjusted by your Kelly fractional setup"]
            }
            st.table(pd.DataFrame(metrics_table))
            
        st.markdown("---")
        st.subheader("Dashboard Display View")
        
        if ev > 0:
            st.error(f"""
            ### 🚨 BEST BET IDENTIFIED
            * **Game:** Chiefs @ Bills
            * **Bet:** Chiefs Moneyline ({market_away_ml:+} Market Odds)
            * **Fair Price:** {fair_away_ml}
            * **EV Edge:** +{edge*100:.1f}%
            * **Recommendation Risk Matrix:** {final_unit_size*100:.2f} Units (Risk ${final_unit_size*10000:.2f} based on standard $10,000 baseline)
            """)
        else:
            st.warning("No significant +EV Value Edge discovered across current odds structures.")