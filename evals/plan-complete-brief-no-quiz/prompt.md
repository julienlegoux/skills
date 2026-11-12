---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

Plan this and show me the plan here — don't write any file and don't build yet. A command-line tool for me only, on my Linux laptop: it reads a folder of bank statement CSV files (date, label, amount; one file per month), groups spending by category using keyword rules I keep in a rules.toml file, and prints a monthly table of totals per category, with an "uncategorised" row. Python 3.12, standard library only, tests with pytest. No network, no database, no GUI. Done means: I run `spend report ./statements` and get the table for every month present. Nothing needs an account or a key.
