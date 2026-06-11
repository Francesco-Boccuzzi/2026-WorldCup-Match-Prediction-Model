import json
import multiprocessing
from collections import Counter
from engine.sim import Tournament
from engine.bracket import Bracket
from engine.logger import MatchLogger

# Define file paths
TEAMS_JSON_PATH = 'data/wc_2026_teams.json'
MATRIX_JSON_PATH = 'data/pairing_matrix.json'

def run_single_tournament(run_id):
    """
    Executes a single instance of the entire 2026 World Cup simulation.
    """
    logger = MatchLogger() if run_id == 0 else None

    tournament = Tournament(TEAMS_JSON_PATH, logger=logger)
    tournament.play_group_stage()

    # 1. Group Stage
    tournament = Tournament(TEAMS_JSON_PATH)
    tournament.play_group_stage()
    
    # 2. Get Advancing Teams (32 teams)
    advancing_teams = tournament.advance_to_knockout()
    
    # 3. Knockout Stage Setup
    with open(MATRIX_JSON_PATH, 'r') as f:
        pairing_matrix = json.load(f)
        
    bracket = Bracket(advancing_teams, pairing_matrix)
    bracket.seed_round_of_32()
    
    # 4. Play Knockout Rounds to Completion
    current_round_teams = advancing_teams

    while len(current_round_teams) > 1:
        # Play the current round and get advancing teams
        advancing_to_next_round = bracket.play_round()
        
        # Stop if we've reached the final (1 team left = winner)
        if len(advancing_to_next_round) == 1:
            break
        
        # Setup next round matches
        current_round_teams = advancing_to_next_round
        bracket.create_next_round_matches(current_round_teams)

    # 5. Extract the tournament winner
    winner = advancing_to_next_round[0].name if advancing_to_next_round else advancing_teams[0]['name'] 
   
    return winner

def run_batch_simulation(num_runs=10000):
    """
    Orchestrates the Monte Carlo simulation using multiprocessing.
    """
    print(f"Starting Monte Carlo Simulation with {num_runs} iterations...")
    
    # Determine the number of CPU cores available to maximize parallel processing
    num_cores = multiprocessing.cpu_count()
    print(f"Utilizing {num_cores} CPU cores.")
    
    # Create a multiprocessing Pool
    with multiprocessing.Pool(processes=num_cores) as pool:
        # pool.map distributes the run_single_tournament function across your cores
        # We pass a simple range just to act as the run_id
        results = pool.map(run_single_tournament, range(num_runs))
        
    # Aggregate the results
    winner_counts = Counter(results)
    
    # Calculate and print probabilities
    print("\n--- TOURNAMENT WIN PROBABILITIES ---")
    for team, wins in winner_counts.most_common(15):
        win_probability = (wins / num_runs) * 100
        print(f"{team}: {win_probability:.2f}% ({wins} wins)")

if __name__ == "__main__":
    # Start with 100 runs to test speed and stability, then scale up to 10,000+
    run_batch_simulation(num_runs=10000)