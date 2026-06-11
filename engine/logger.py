import os

class MatchLogger:
    def __init__(self, filename="group_stage_results.md"):
        self.filename = filename
        # Clear existing file if starting new
        if os.path.exists(self.filename):
            os.remove(self.filename)
            
    def log_match(self, group, team_a, team_b, sa, sb):
        with open(self.filename, "a") as f:
            # Write a table header if file is empty
            if f.tell() == 0:
                f.write("| Group | Home Team | Away Team | Score |\n")
                f.write("|-------|-----------|-----------|-------|\n")
            
            f.write(f"| {group} | {team_a} | {team_b} | {sa} - {sb} |\n")