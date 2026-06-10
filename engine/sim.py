from engine.core import load_teams
from engine.match import calculate_expected_goals, get_match_probabilities
import numpy as np

class Tournament:
    def __init__(self, json_path):
        self.teams = load_teams(json_path)
        # Groups: Dictionary mapping group_id (A-L) to a list of Team objects
        self.groups = self._organize_groups()
        # Standings: Nested dict {group_id: {team_name: {"points": 0, "gd": 0}}}
        self.standings = self._initialize_standings()

    def _organize_groups(self):
        # Assumes your JSON has groups A-L
        # You may need to add a 'group_id' attribute to your Team dataclass
        # or map them here based on the JSON structure.
        return {group_id: [t for t in self.teams if t.group == group_id] 
                for group_id in "ABCDEFGHIJKL"}

    def _initialize_standings(self):
        return {gid: {t.name: {"pts": 0, "gd": 0} for t in group} 
                for gid, group in self.groups.items()}

    def play_group_stage(self):
        """Iterates through all round-robin matches in each group."""
        for gid, group in self.groups.items():
            # Round Robin: Every team plays every other team in the group
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    self._run_match(gid, group[i], group[j])

    def _run_match(self, gid, team_a, team_b):
        # Use your match engine
        la, lb = calculate_expected_goals(team_a, team_b)
        probs = get_match_probabilities(la, lb)
        
        # Sample score
        flat_probs = probs.flatten()
        sampled_index = np.random.choice(np.arange(len(flat_probs)), p=flat_probs/flat_probs.sum())
        sa, sb = np.unravel_index(sampled_index, probs.shape)
        
        # Update points and goal difference
        self.standings[gid][team_a.name]["gd"] += (sa - sb)
        self.standings[gid][team_b.name]["gd"] += (sb - sa)
        
        if sa > sb:
            self.standings[gid][team_a.name]["pts"] += 3
        elif sb > sa:
            self.standings[gid][team_b.name]["pts"] += 3
        else:
            self.standings[gid][team_a.name]["pts"] += 1
            self.standings[gid][team_b.name]["pts"] += 1

    def get_advancing_teams(self):
        """Returns the top 2 teams from each group."""
        advancing = {}
        for gid, results in self.standings.items():
            # Sort by points descending, then goal difference descending
            sorted_teams = sorted(results.items(), key=lambda x: (x[1]["pts"], x[1]["gd"]), reverse=True)
            advancing[gid] = sorted_teams[:2]
        return advancing