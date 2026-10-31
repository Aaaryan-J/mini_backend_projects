# Number Guessing Game

A command-line number guessing game built with Python.

This is my implementation of the [Number Guessing Game project](https://roadmap.sh/projects/number-guessing-game) from roadmap.sh. I am building it as backend practice while learning about user input, validation, loops, randomness, file handling, and storing data with JSON.

## Features

- Choose between Easy, Medium, and Hard difficulty
- Guess a randomly selected number between 1 and 100
- Receive hints when a guess is too high or too low
- Ask for an even-or-odd hint
- Track the time taken and number of attempts
- Save personal high scores for each difficulty level
- Play multiple rounds

## Difficulty levels

| Level | Attempts |
|---|---:|
| Easy | 10 |
| Medium | 5 |
| Hard | 3 |

Using a hint uses one attempt.

## Requirements

- Python 3

The game uses only Python's standard library, so no additional packages are required.

## Usage

Run the game from the `number_guess_game_cli` directory:

```powershell
python main.py
```

The game will ask for a username and then let you choose a difficulty level.

During the game, enter a number between `1` and `100`:

```text
Enter your guess (or type 'hint' for a hint):
```

You can also type:

```text
hint
```

## Example

```text
Enter your username: Aaaryan

Please select the difficulty level:
1. Easy (10 chances)
2. Medium (5 chances)
3. Hard (3 chances)
Enter choice: 1

Great! You have selected Easy difficulty level.
Let's start the game.

Enter your guess (or type 'hint' for a hint): 50
Incorrect! The number is greater than 50

Enter your guess (or type 'hint' for a hint): 75
Congratulations! You guessed the number in 2 attempts.
New high score for Easy: 2 attempts!
```

## High scores

High scores are stored in `high_scores.json` in the same directory as the game.

Scores are saved separately for each username and difficulty level. A new score replaces the saved score only when it uses fewer attempts.

Example:

```json
{
  "Aaaryan": {
    "easy": 2,
    "medium": 3,
    "hard": 2
  }
}
```

## Project purpose

This is a small practice project. It focuses on building a complete command-line program with input validation, game logic, persistent data, and a simple user experience.
