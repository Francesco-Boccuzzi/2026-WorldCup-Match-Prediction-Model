import json
from dataclasses import dataclass

@dataclass
class Team:
    name: str
    confederation: str
    fifa_rank: int
    is_host: bool
    group: str = None  # Optional, can be set later based on JSON structure

def load_teams(file_path):
    """Reads the JSON file and returns a list of Team objects."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    teams = []
    # Iterate through the groups defined in the JSON structure
    for group_id, members in data['groups'].items():
        for member in members:
            team = Team(
                name=member['name'],
                confederation=member['confederation'],
                fifa_rank=member['fifa_rank'],
                is_host=member['host'],
                group=group_id  # Assign group based on JSON structure
            )
            teams.append(team)
    return teams

# Example usage:
# teams = load_teams('2026-WorldCup-Match-Prediction-Model/data/wc_2026_teams.json')
# for team in teams:
#     print(f"{team.name} (Rank: {team.fifa_rank})")