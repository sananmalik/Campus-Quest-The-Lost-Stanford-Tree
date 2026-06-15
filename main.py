"""
Campus Quest: The Lost Stanford Tree

A beginner-friendly text adventure made for a Code in Place final project.
The player explores campus locations, solves small puzzles, collects items,
and earns a final score.

Run:
    python main.py
"""

import random
import textwrap


WRAP_WIDTH = 78

LOCATIONS = {
    "quad": {
        "name": "Main Quad",
        "description": (
            "Sunlight spills across the stone arches. A note is taped to a "
            "pillar: 'The Tree is missing. Follow the clues before sunset.'"
        ),
        "paths": {
            "north": "library",
            "east": "cafe",
            "south": "lake",
            "west": "lab",
        },
        "item": "campus map",
    },
    "library": {
        "name": "Green Library",
        "description": (
            "Rows of books stretch into the quiet. A librarian points toward "
            "a locked display case with a tiny keypad."
        ),
        "paths": {"south": "quad", "east": "garden"},
        "item": "old clue card",
        "puzzle": "library",
    },
    "cafe": {
        "name": "Code Cafe",
        "description": (
            "Students debug programs over hot chocolate. The barista says "
            "they saw a leafy shadow rushing toward the lake."
        ),
        "paths": {"west": "quad", "south": "stadium"},
        "item": "energy cookie",
        "puzzle": "cafe",
    },
    "lab": {
        "name": "AI Lab",
        "description": (
            "Monitors glow with half-finished experiments. A robot assistant "
            "beeps: 'Probability of Tree recovery increases with teamwork.'"
        ),
        "paths": {"east": "quad", "north": "garden"},
        "item": "robot hint",
        "puzzle": "lab",
    },
    "lake": {
        "name": "Lagunita Lake",
        "description": (
            "Wind ripples the water. Something green and fuzzy has left "
            "footprints in the mud."
        ),
        "paths": {"north": "quad", "east": "stadium"},
        "item": "muddy footprint",
    },
    "garden": {
        "name": "Hidden Garden",
        "description": (
            "Flowers form a neat spiral. At the center sits a small wooden box "
            "covered with number patterns."
        ),
        "paths": {"south": "lab", "west": "library", "east": "stadium"},
        "item": "golden key",
        "puzzle": "garden",
    },
    "stadium": {
        "name": "Stanford Stadium",
        "description": (
            "The stands are empty, but you hear a rustle near the tunnel. "
            "This feels like the final stop."
        ),
        "paths": {"north": "cafe", "west": "lake", "east": "garden"},
        "puzzle": "final",
    },
}

PUZZLES = {
    "library": {
        "question": "Keypad puzzle: What is 7 * 6?",
        "answers": {"42"},
        "success": "The display case opens and reveals a clue about the garden.",
        "points": 15,
    },
    "cafe": {
        "question": "Barista riddle: I run but never walk. What am I?",
        "answers": {"water", "a river", "river"},
        "success": "The barista smiles and gives you an energy cookie.",
        "points": 15,
    },
    "lab": {
        "question": "Robot logic: If True and not False, is the result true or false?",
        "answers": {"true", "t"},
        "success": "The robot prints a useful hint: 'Bring the golden key.'",
        "points": 15,
    },
    "garden": {
        "question": "Garden box: What number comes next? 2, 4, 8, 16, __",
        "answers": {"32"},
        "success": "The box opens. Inside is a golden key.",
        "points": 20,
    },
    "final": {
        "question": (
            "Final challenge: Which item unlocks the stadium tunnel? "
            "Type the item name."
        ),
        "answers": {"golden key", "key"},
        "success": "The tunnel opens. You found the Stanford Tree!",
        "points": 30,
    },
}

COMMANDS = {
    "help": "Show the command list.",
    "look": "Read the current location again.",
    "go <direction>": "Move north, south, east, or west when available.",
    "take": "Pick up the item at your current location.",
    "inventory": "Show your collected items.",
    "solve": "Try the puzzle at your current location.",
    "status": "Show score, moves, and solved puzzles.",
    "quit": "End the game.",
}


def print_wrapped(text=""):
    """Print text wrapped to the terminal width used by the game."""
    if text == "":
        print()
        return
    for paragraph in text.split("\n"):
        print(textwrap.fill(paragraph, WRAP_WIDTH))


def print_title():
    print("=" * WRAP_WIDTH)
    print("CAMPUS QUEST: THE LOST STANFORD TREE".center(WRAP_WIDTH))
    print("=" * WRAP_WIDTH)
    print_wrapped(
        "The Stanford Tree has vanished just before the celebration. Explore "
        "campus, collect clues, solve puzzles, and bring the Tree home."
    )
    print()


def print_help():
    print("Commands")
    print("-" * 8)
    for command, description in COMMANDS.items():
        print(f"{command:<16} {description}")
    print()


def make_player():
    name = input("What is your name, explorer? ").strip()
    if name == "":
        name = "Explorer"
    return {
        "name": name,
        "location": "quad",
        "inventory": [],
        "solved": set(),
        "score": 0,
        "moves": 0,
        "game_over": False,
        "won": False,
    }


def describe_location(player):
    location = LOCATIONS[player["location"]]
    print()
    print(location["name"])
    print("-" * len(location["name"]))
    print_wrapped(location["description"])

    item = location.get("item")
    if item and item not in player["inventory"]:
        print_wrapped(f"You notice an item here: {item}.")

    paths = ", ".join(location["paths"].keys())
    print_wrapped(f"Available directions: {paths}")

    puzzle_name = location.get("puzzle")
    if puzzle_name and puzzle_name not in player["solved"]:
        print_wrapped("There is an unsolved puzzle here. Type 'solve' to try it.")
    print()


def show_inventory(player):
    if len(player["inventory"]) == 0:
        print_wrapped("Your backpack is empty. Time to collect some clues.")
        return
    print_wrapped("Inventory: " + ", ".join(player["inventory"]))


def show_status(player):
    print_wrapped(
        f"Score: {player['score']} | Moves: {player['moves']} | "
        f"Puzzles solved: {len(player['solved'])}/5"
    )


def take_item(player):
    location = LOCATIONS[player["location"]]
    item = location.get("item")

    if not item:
        print_wrapped("There is no item to take here.")
        return
    if item in player["inventory"]:
        print_wrapped("You already picked that up.")
        return

    if item == "golden key" and "garden" not in player["solved"]:
        print_wrapped("The golden key is locked inside the garden box. Solve the puzzle first.")
        return
    if item == "energy cookie" and "cafe" not in player["solved"]:
        print_wrapped("The barista is saving it for puzzle solvers. Try 'solve'.")
        return

    player["inventory"].append(item)
    player["score"] += 5
    print_wrapped(f"You picked up: {item}. +5 points")


def move_player(player, direction):
    location = LOCATIONS[player["location"]]
    paths = location["paths"]

    if direction not in paths:
        print_wrapped("You cannot go that way from here.")
        return

    player["location"] = paths[direction]
    player["moves"] += 1
    describe_location(player)


def solve_puzzle(player):
    location = LOCATIONS[player["location"]]
    puzzle_name = location.get("puzzle")

    if not puzzle_name:
        print_wrapped("There is no puzzle here.")
        return
    if puzzle_name in player["solved"]:
        print_wrapped("You already solved this puzzle.")
        return

    puzzle = PUZZLES[puzzle_name]

    if puzzle_name == "final" and "golden key" not in player["inventory"]:
        print_wrapped(
            "The stadium tunnel is locked. You need to find the golden key first."
        )
        return

    print_wrapped(puzzle["question"])
    answer = input("> ").strip().lower()

    if answer in puzzle["answers"]:
        player["solved"].add(puzzle_name)
        player["score"] += puzzle["points"]
        print_wrapped(puzzle["success"] + f" +{puzzle['points']} points")

        if puzzle_name == "final":
            player["won"] = True
            player["game_over"] = True
            celebrate_win(player)
    else:
        encouragements = [
            "Not quite. Try looking around for a clue.",
            "Close attempt. Think like a programmer and try again.",
            "That answer did not unlock it. You can solve this.",
        ]
        print_wrapped(random.choice(encouragements))


def celebrate_win(player):
    bonus = max(0, 25 - player["moves"])
    player["score"] += bonus

    print()
    print("*" * WRAP_WIDTH)
    print("YOU WIN!".center(WRAP_WIDTH))
    print("*" * WRAP_WIDTH)
    print_wrapped(
        f"{player['name']}, you found the Stanford Tree and saved the celebration. "
        f"Speed bonus: +{bonus} points."
    )
    print_wrapped(f"Final score: {player['score']}")
    print()


def parse_command(raw_command):
    command = raw_command.strip().lower()
    if command.startswith("go "):
        return "go", command[3:].strip()
    return command, ""


def handle_command(player, raw_command):
    command, argument = parse_command(raw_command)

    if command == "":
        print_wrapped("Type a command, or type 'help' if you want options.")
    elif command == "help":
        print_help()
    elif command == "look":
        describe_location(player)
    elif command == "inventory":
        show_inventory(player)
    elif command == "status":
        show_status(player)
    elif command == "take":
        take_item(player)
    elif command == "solve":
        solve_puzzle(player)
    elif command == "go":
        move_player(player, argument)
    elif command in {"north", "south", "east", "west"}:
        move_player(player, command)
    elif command == "quit":
        player["game_over"] = True
        print_wrapped("Thanks for playing. Your current score was " + str(player["score"]) + ".")
    else:
        print_wrapped("I do not know that command. Type 'help' to see what you can do.")


def play_again():
    answer = input("Play again? (yes/no) ").strip().lower()
    return answer in {"yes", "y"}


def main():
    print_title()
    print_help()

    keep_playing = True
    while keep_playing:
        player = make_player()
        describe_location(player)

        while not player["game_over"]:
            raw_command = input("> ")
            handle_command(player, raw_command)

        keep_playing = play_again()
        if keep_playing:
            print_title()

    print_wrapped("Goodbye, and congratulations on finishing your final project!")


if __name__ == "__main__":
    main()
