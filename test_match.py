import numpy as np
# Assuming the previous scripts are in an 'engine' package
from engine.core import load_teams
from engine.match import calculate_expected_goals, get_match_probabilities

def run_dry_run():
    # 1. Load teams from your JSON
    all_teams = load_teams('data/wc_2026_teams.json')
    
    # 2. Select two teams for the test (e.g., Brazil and Morocco)
    team_a = next(t for t in all_teams if t.name == "Brazil")
    team_b = next(t for t in all_teams if t.name == "Morocco")
    
    # 3. Calculate expected goals (lambda values)
    lambda_a, lambda_b = calculate_expected_goals(team_a, team_b)
    
    # 4. Get probability matrix
    probs = get_match_probabilities(lambda_a, lambda_b)
    
    # 5. Simulate a result based on the probabilities
    # Flatten the 2D probability matrix to sample from it
    flat_probs = probs.flatten()
    indices = np.arange(len(flat_probs))
    sampled_index = np.random.choice(indices, p=flat_probs / flat_probs.sum())
    
    # Convert flat index back to score
    score_a, score_b = np.unravel_index(sampled_index, probs.shape)
    
    print(f"Matchup: {team_a.name} vs {team_b.name}")
    print(f"Expected Goals: {team_a.name}={lambda_a:.2f}, {team_b.name}={lambda_b:.2f}")
    print(f"Simulated Score: {score_a} - {score_b}")

if __name__ == "__main__":
    run_dry_run()