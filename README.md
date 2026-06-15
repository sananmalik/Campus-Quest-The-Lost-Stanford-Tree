# Campus Quest: The Lost Stanford Tree

A terminal-based text adventure built in Python. Explore a university campus, collect clues, solve puzzles, and find the missing Stanford Tree before the celebration begins.

---

## Demo

> Run it and see — no install required, just Python.

---

## Getting Started

```bash
python main.py
```

Or paste `main.py` into the [Code in Place IDE](https://codeinplace.stanford.edu) and run it there.

---

## How to Play

| Command | What it does |
|---|---|
| `look` | Describe your current location |
| `go [direction]` | Move north, south, east, or west |
| `take` | Pick up an item |
| `solve` | Attempt the puzzle at this location |
| `inventory` | Show what you're carrying |
| `status` | Check your score and progress |
| `help` | List all commands |
| `quit` | Exit the game |

---

## How It Works

- **Dictionary-driven world** — every location stores its own description, connected paths, item, and puzzle state in one place, making the map easy to extend
- **Inventory and scoring system** — tracks items collected and puzzles solved across the whole run
- **Random feedback messages** — puzzle responses vary so replaying feels different
- **Clean input loop** — parses natural language commands without any external libraries

---

## Requirements

- Python 3.x
- No external dependencies
