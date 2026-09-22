# Health Journey

Goal: lose weight steadily and safely.

## How a day gets logged
Each day is one file in `log/`, named `YYYY-MM-DD.md`, built from `log/_template.md`.

1. **Morning weight** - owner gives it first thing.
2. **Food** - owner gives each item in grams. Vera calculates calories (and protein) from
   per-100g values in `foods.md`. New foods get added there so the same food always counts the same.
3. **Water** - logged in oz (or ml), running total against the daily target.
4. **Activity** - what, how long, and estimated calories burned (from MET values, using that
   morning's weight).
5. **End of day** - calories in, calories burned (BMR + activity), and net.

## Numbers used
- BMR: Mifflin-St Jeor, recalculated from each morning's weight.
- Calories burned from activity: MET x weight (kg) x hours.
- Daily targets live in `profile.md`.
- Calorie values are estimates. Brand labels win over `foods.md` when the owner has one.
