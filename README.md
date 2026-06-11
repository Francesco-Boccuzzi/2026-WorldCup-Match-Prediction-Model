# My 2026 World Cup Match Prediction Model
A fun ML program developed with the goal of predicting the outcomes of World Cup matches and thus helping me create the perfect 2026 World Cup bracket, using math and coding tools. 

## Overview
This project is a high-performance Monte Carlo simulation engine designed to project the outcomes of the 2026 FIFA World Cup. By utilizing a **Bivariate Poisson regression model** with **Dixon-Coles correction**, the engine simulates thousands of tournament iterations to provide probabilistic win outcomes for all 48 participating nations.

## Methodology
The simulation follows a rigorous data-driven pipeline:
1.  **Data Loading**: Teams are initialized using official FIFA rankings, with adjustments made for host-nation advantages.
2.  **Match Engine**: The "brain" of the project uses `scipy.stats.poisson` to model goal expectations. Features include offensive win expectation formulas that dynamically adjust based on the relative rank difference between opponents.
3.  **Tournament Orchestration**: The simulation manages a 12-group round-robin format, followed by a knockout bracket seeded according to the official FIFA 2026 pairing matrix.
4.  **Parallel Monte Carlo**: To ensure statistical significance, the simulation utilizes Python’s `multiprocessing` library to execute 10,000+ tournament iterations across all available CPU cores.

## Simulation Results (10,000 Iterations)
The model highlights the clear favorites for the 2026 tournament, France, Spain and Argentina. Unfortunately for me, a big fan of the Brazilian national team, our odds of winning the tournament are low.

| Team | Win Probability |
| :--- | :--- |
| **France** | 31.13% |
| **Spain** | 26.87% |
| **Argentina** | 16.50% |
| **England** | 8.46% |
| **Portugal** | 6.72% |
| **Belgium** | 1.98% |
| **Brazil** | 1.81% |
| **Croatia** | 1.04% |
| **Netherlands** | 0.79% |
| **Morocco** | 0.67% |
| **Germany** | 0.49% |
| **Colombia** | 0.48% |
| **Uruguay** | 0.45% |
| **USA** | 0.43% |
| **Iran** | 0.39% |

*The model suggests a strong concentration of probability at the top, reflecting the current dominance of these specific confederations in historical ranking data.*

## Personal Motivation
Every four years, my country stops to watch the World Cup and cheer for Brazil. During those weeks, I take part in various different rituals like collecting stickers, watching the games with family, and my favorite: building a world cup bracket. This year, I wanted to use my learnings from the CS and Math classes I have been taking at Northwestern University in order to attempt to make a mathematically optimal bracket.

## Game Results
In group_stage_results.md, you can find the simulated results for all group stage games across one iteration of the 10,000 iterations made

## Future Enhancements
* **Dynamic Elo**: Implementing real-time Elo updates after every match rather than static ranking anchors.
* **Live Results Tracking Website**: Creating a live dashboard which will keep track of the results and compare them to the predictions.
