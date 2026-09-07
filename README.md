# Winners & Losers Fantasy League

Independent 2026 Winners & Losers fantasy football dashboard.

## Included
- 16-manager league roster migrated into this independent repository.
- Current scoring from NFL and college results.
- Mobile-first dashboard with standings, manager rosters, team tracker and live/scheduled games.
- Projected points using remaining scheduled games; ESPN win probabilities are used when available, otherwise a transparent 50/50 baseline is used.
- Scheduled GitHub Actions refresh every hour.
- GitHub Pages deployment workflow.

## Scoring
Winner picks earn one point per win. Loser picks earn one point per loss. Ties earn zero. Postseason results count.

## Data
The synchronizer uses ESPN public scoreboard feeds and writes `data/standings.json`. The roster is stored locally in `data/rosters.json`; the original repository is not used as a runtime dependency.

## GitHub Pages
Enable **Settings → Pages → Source → GitHub Actions** if Pages is not already enabled for the repository. After that, pushes to `main` deploy automatically.