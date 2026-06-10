from engine.match import calculate_expected_goals, get_match_probabilities
import numpy as np

class Bracket:
    def __init__(self, advancing_data, pairing_matrix):
        """
        advancing_data: list of dicts -> [{'name': 'Brazil', 'gid': 'C', 'rank': 1}, ...]
        pairing_matrix: loaded JSON dict containing the 3rd-place combinations
        """
        self.teams = advancing_data
        self.pairing_matrix = pairing_matrix
        
        # Initialize the 16 matches for the Round of 32 (Matches 73-88)
        self.matches = {i: {"team_a": None, "team_b": None} for i in range(73, 89)}
        
        # Create a quick lookup dictionary for 1st and 2nd place teams.
        # This turns [{'name': 'Brazil', 'gid': 'C', 'rank': 1}] into {'1C': 'Brazil'}
        self.team_lookup = {
            f"{t['rank']}{t['gid']}": t['team_obj'] 
            for t in self.teams if t['rank'] in [1, 2]
        }
        
        # Isolate the 8 third-place teams
        self.thirds = [t for t in self.teams if t['rank'] == 3]

    def seed_round_of_32(self):
        """
        Maps teams to Matches 73-88 based on the official FIFA schedule.
        """
        # 1. Identify the combination of 3rd-place groups (e.g., "CDEFGHIJ")
        third_place_groups = sorted([t['gid'] for t in self.thirds])
        combo_key = "".join(third_place_groups) 
        
        # 2. Fetch the specific assignments for this combination from the matrix
        # Expected format from JSON: {"74": "E", "77": "I", "79": "F", ...}
        third_pairings = self.pairing_matrix.get(combo_key, {})

        def get_third(gid):
            """Helper to find the Team object of the 3rd place team from a specific group."""
            if not gid: return None
            # CHANGED: Returning t['team_obj'] instead of t['name']
            return next(t['team_obj'] for t in self.thirds if t['gid'] == gid)

        # 3. Map the matches according to the FIFA schedule
        self.matches[73] = {"team_a": self.team_lookup["2A"], "team_b": self.team_lookup["2B"]}
        self.matches[74] = {"team_a": self.team_lookup["1E"], "team_b": get_third(third_pairings.get("74"))}
        self.matches[75] = {"team_a": self.team_lookup["1F"], "team_b": self.team_lookup["2C"]}
        self.matches[76] = {"team_a": self.team_lookup["1C"], "team_b": self.team_lookup["2F"]}
        self.matches[77] = {"team_a": self.team_lookup["1I"], "team_b": get_third(third_pairings.get("77"))}
        self.matches[78] = {"team_a": self.team_lookup["2E"], "team_b": self.team_lookup["2I"]}
        self.matches[79] = {"team_a": self.team_lookup["1A"], "team_b": get_third(third_pairings.get("79"))}
        self.matches[80] = {"team_a": self.team_lookup["1L"], "team_b": get_third(third_pairings.get("80"))}
        self.matches[81] = {"team_a": self.team_lookup["1D"], "team_b": get_third(third_pairings.get("81"))}
        self.matches[82] = {"team_a": self.team_lookup["1G"], "team_b": get_third(third_pairings.get("82"))}
        self.matches[83] = {"team_a": self.team_lookup["2K"], "team_b": self.team_lookup["2L"]}
        self.matches[84] = {"team_a": self.team_lookup["1H"], "team_b": self.team_lookup["2J"]}
        self.matches[85] = {"team_a": self.team_lookup["1B"], "team_b": get_third(third_pairings.get("85"))}
        self.matches[86] = {"team_a": self.team_lookup["1J"], "team_b": self.team_lookup["2H"]}
        self.matches[87] = {"team_a": self.team_lookup["1K"], "team_b": get_third(third_pairings.get("87"))}
        self.matches[88] = {"team_a": self.team_lookup["2D"], "team_b": self.team_lookup["2G"]}

    def play_round(self):
        """Simulates all matches in the current round and returns winners."""
        winners = []
        for match_id, teams in self.matches.items():
            # Call engine.match.calculate_expected_goals here
            la, lb = calculate_expected_goals(teams["team_a"], teams["team_b"])
            probs = get_match_probabilities(la, lb)
            
            # Simulate and add winner to 'winners' list
            flat_probs = probs.flatten()
            sampled_index = np.random.choice(np.arange(len(flat_probs)), p=flat_probs/flat_probs.sum())
            sa, sb = np.unravel_index(sampled_index, probs.shape)
            winner = teams["team_a"] if sa > sb else teams["team_b"]
            winners.append(winner)
            
        return winners
    
    def create_next_round_matches(self, advancing_teams):
        """
        Sets up matches for the next round based on the advancing teams.
        Pairs teams according to bracket structure (1 vs 2, 3 vs 4, etc.).
        """
        # Clear previous matches
        self.matches = {}
        
        # Pair advancing teams: 1st with 2nd, 3rd with 4th, etc.
        match_id = 89  # Start after Round of 32 (matches 73-88)
        
        for i in range(0, len(advancing_teams), 2):
            if i + 1 < len(advancing_teams):
                self.matches[match_id] = {
                    "team_a": advancing_teams[i],
                    "team_b": advancing_teams[i + 1]
                }
                match_id += 1