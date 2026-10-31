import random
import time
import json
from pathlib import Path

SCORES_FILE = Path(__file__).with_name("high_scores.json")


def load_scores():
    if not SCORES_FILE.exists():
        return {}

    try:
        with SCORES_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise SystemExit("Could not read high_scores.json: invalid JSON.")


def save_scores(scores):
    with SCORES_FILE.open("w", encoding="utf-8") as file:
        json.dump(scores, file, indent=2)


def game(username):
    start_time = time.time()

    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("You have limited chances to guess the correct number.") 

    print("\nPlease select the difficulty level:")
    print("1. Easy (10 chances)\n2. Medium (5 chances)\n3. Hard (3 chances)")

    while True:
        try:
            level = int(input("Enter choice: "))
            if level in [1, 2, 3]:
                break
            print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Please enter a number.")    
        
    difficulties = ['Easy', 'Medium', 'Hard']
    chances = [10,5,3]
    difficulty = difficulties[level - 1].lower()

    chance = 1
    goal = random.randint(1,100)

    print(f"Great! You have selected {difficulties[level-1]} difficulty level.")
    print("Let's start the game.")

    while chance <= chances[level - 1]:
        user_input = input("\nEnter your guess(or type 'hint' for a hint): ").strip().lower()

        if user_input == 'hint':
            print(f"Hint: Number is {'even' if goal % 2 == 0 else 'odd'}.")
            chance += 1
            continue

        try:
            guess = int(user_input)
        except ValueError:
            print("Please enter a whole number or type 'hint'.")
            continue

        if not 1 <= guess <= 100:
            print("Please enter a number between 1 and 100.")
            continue

        if guess == goal:
            end_time = time.time()
            duration = end_time - start_time
            print(f"Congratulations! you guessed the number in {duration:.2f} seconds and took {chance} attempts.")

            scores = load_scores()
            user_scores = scores.setdefault(username, {})
            best_score = user_scores.get(difficulty)

            if best_score is None or chance < best_score:
                user_scores[difficulty] = chance
                save_scores(scores)
                print(f"New high score for {difficulties[level - 1]}: {chance} attempts!")
            else:
                print(
                    f"Your high score for {difficulties[level - 1]} "
                    f"is {best_score} attempts."
                )
            return
        elif guess < goal:
            print("Incorrect! The number is greater than", guess)
            chance += 1
            continue
        else:
            print("Incorrect! The number is less than", guess)
            chance += 1 
            continue
    print("Game Over! Out of chances.")
    return

username = input("Enter your username: ").strip()
while not username:
    print("Username cannot be empty.")
    username = input("Enter your username: ").strip()

while True:
    game(username)
    choice = input("\nDo you want to play again?(y/n)").strip().lower()
    if choice != 'y':
        break

print("\nExiting...")