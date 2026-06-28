import numpy as np

def calculate_implied_probability(american_odds):
    """Converts moneyline odds to implied probability."""
    if american_odds > 0:
        return 100 / (american_odds + 100)
    else:
        return abs(american_odds) / (abs(american_odds) + 100)

def convert_prob_to_moneyline(prob):
    """Converts a pure probability raw decimal into traditional American Odds format."""
    if prob >= 0.5:
        odds = -int((prob / (1 - prob)) * 100)
    else:
        odds = int(((1 - prob) / prob) * 100)
    return f"+{odds}" if odds > 0 else str(odds)

def run_monte_carlo_simulation(sim_count, home_elo, away_elo, situational_adjustments):
    """
    Simulates thousands of matchups based on baseline Elo ratings
    plus situational parameters (e.g., weather, rest, missing personnel).
    """
    # Baseline projection adjusted by situational metrics
    base_spread = (home_elo - away_elo) / 25.0  # Simplified standard football Elo rule
    adjusted_spread = base_spread + situational_adjustments['net_advantage']
    
    # Add a standard deviation metric representing typical NFL game variance (~13.5 points)
    std_dev = 13.5
    
    # Generate distribution profiles
    simulated_margins = np.random.normal(loc=adjusted_spread, scale=std_dev, size=sim_count)
    
    # Calculations
    home_wins = np.sum(simulated_margins > 0)
    away_wins = sim_count - home_wins
    
    home_win_prob = home_wins / sim_count
    away_win_prob = away_wins / sim_count
    
    # Dynamic point score assignment projection mapping
    projected_total = 47.6
    away_score = np.round((projected_total - adjusted_spread) / 2, 1)
    home_score = np.round(projected_total - away_score, 1)
    
    return {
        "away_score": away_score,
        "home_score": home_score,
        "away_prob": away_win_prob,
        "home_prob": home_win_prob,
        "fair_total": projected_total,
        "fair_spread": np.round(-adjusted_spread, 1)
    }

def calculate_ev_and_kelly(win_prob, market_odds, kelly_fraction):
    """Calculates mathematical expected value and bankroll asset fractions."""
    # Convert traditional moneyline decimal multiplier
    if market_odds > 0:
        b = market_odds / 100.0
    else:
        b = 100.0 / abs(market_odds)
        
    p = win_prob
    q = 1.0 - p
    
    # Core Formula: EV = (P * Net Profit) - (Q * Stake)
    ev_per_dollar = (p * b) - q
    
    # Kelly Criterion Formula
    if b > 0 and ev_per_dollar > 0:
        raw_kelly = (b * p - q) / b
        recommended_kelly = raw_kelly * kelly_fraction
    else:
        raw_kelly = 0.0
        recommended_kelly = 0.0
        
    return ev_per_dollar, raw_kelly, recommended_kelly