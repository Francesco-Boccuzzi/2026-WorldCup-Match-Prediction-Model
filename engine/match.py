import numpy as np
from scipy.stats import poisson

def calculate_expected_goals(team_a, team_b, shape=1.0, host_discount=0.1):
    """
    Calculates expected goals for a match between two teams using the 
    feature engineering approach from spec.md.
    """
    # Calculate effective ranks incorporating host advantage
    eff_rank_a = team_a.fifa_rank * (1 - (host_discount if team_a.is_host else 0))
    eff_rank_b = team_b.fifa_rank * (1 - (host_discount if team_b.is_host else 0))
    
    # Calculate offensive win expectation (feature from spec.md)
    # Note: In a full model, you would track separate offensive/defensive ranks.
    # Here we demonstrate the structural formula.
    off_win_exp = 1 / (1 + (eff_rank_a / eff_rank_b) ** shape)
    
    # In a real Bivariate Poisson model, lambda (expected goals) 
    # would be derived from these offensive/defensive expectations.
    lambda_a = off_win_exp * 2.0  # Placeholder: scaling factor for goals
    lambda_b = (1 - off_win_exp) * 2.0
    
    return lambda_a, lambda_b

def get_match_probabilities(lambda_a, lambda_b, max_goals=5):
    """
    Calculates the probability matrix for scores up to max_goals.
    Uses scipy.stats.poisson.pmf.
    """
    probs = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            # Poisson PMF: P(X=k) = (lambda^k * e^-lambda) / k!
            probs[i, j] = poisson.pmf(i, lambda_a) * poisson.pmf(j, lambda_b)
    return probs