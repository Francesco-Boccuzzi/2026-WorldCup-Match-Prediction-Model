# World Cup 2026 Prediction Simulation Specification

## 1. Overview
This project simulates the 2026 FIFA World Cup to predict tournament outcomes using a Poisson-based machine learning model. The approach emphasizes simplicity and robustness, using a single feature ("offensive win expectation") to drive predictions, anchored by historical FIFA rankings and dynamic Elo-style rank updates.

## 2. Data Requirements
- **Match Data:** Historical records from 1930–2022 via the `jfjelstul/worldcup` dataset.
- **2026 Roster:** `data/wc_2026_teams.json` (48 teams, FIFA rankings, confederations, host status).
- **FIFA Rankings:** `data/dataset.json` (pre-tournament historical rankings, 1998–2022).

## 3. Core Model Logic
- **Goal Prediction:** Bivariate Poisson regression to estimate expected goals for both teams.
- **Match Outcome:** Sampled from the distribution using static Dixon-Coles correction parameters derived from historical World Cup match data.
- **Feature Engineering:**
  - `off_win_exp = 1 / (1 + (eff_off_rank / eff_opp_def_rank) ^ shape)`
  - `eff_rank = rank * (1 - host_discount * is_host)`
- **Dynamic Ranks:** Track General, Offensive, and Defensive ranks per team.
  - Updates scaled by `log(1 + |rank_diff|)` (upset weighting).
  - **Mean Reversion:** `new_rank = (1 - reversion_rate) * dynamic_rank + reversion_rate * base_rank` to maintain statistical anchor to pre-tournament FIFA rankings.

## 4. Simulation Engine
- **Workflow:** 1. Initialize teams with base FIFA rankings.
  2. Simulate match results sequentially.
  3. Update ranks dynamically post-match.
  4. Perform multiple tournament iterations (Monte Carlo approach).
- **Optimization:** Use Optuna to tune global parameters (shape, k-factors, reversion_rate, host_discount) against the historical `dataset.json`.

## 5. Implementation Notes
- The model should be language-agnostic but is currently prototyped in R/Jupyter; migration to Python (e.g., using `scipy.stats` for Poisson distributions) is recommended for production scaling.
- Focus on maintaining the 48-team group stage logic distinct from the knockout phases.