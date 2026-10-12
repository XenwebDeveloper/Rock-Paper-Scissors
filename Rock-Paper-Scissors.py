import os
import random
from datetime import datetime

# Absolute path: history.txt will be created right next to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "history.txt")


# ---------- History File Handling ----------
def init_history_file():
    """Create the history file with a header if it doesn't exist."""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write("date,player_name,player_choice,computer_choice,result\n")
        print(f"📁 History file created at: {HISTORY_FILE}")
    else:
        print(f"📁 Using existing history file: {HISTORY_FILE}")


def save_result(player_name, player_choice, computer_choice, result):
    """Append the result of each round to history.txt."""
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{now},{player_name},{player_choice},{computer_choice},{result}\n")


def show_history():
    """Display all recorded games from history.txt."""
    if not os.path.exists(HISTORY_FILE):
        print("❌ No games have been recorded yet!")
        return

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) <= 1:
        print("❌ History is empty!")
        return

    print("\n📜 Game History:")
    print("-" * 70)
    for line in lines:
        print(line.strip())
    print("-" * 70)


def clear_history():
    """Wipe the history file (with user confirmation)."""
    confirm = input("⚠️ Are you sure you want to delete all history? (y/n): ").strip().lower()
    if confirm == "y":
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write("date,player_name,player_choice,computer_choice,result\n")
        print("🗑️ History cleared!")
    else:
        print("✅ Cancelled.")


# ---------- Game Logic ----------
def get_winner(player, computer):
    """Return 'win', 'lose', or 'tie' based on the game rules."""
    if player == computer:
        return "tie"
    wins = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper",
    }
    if wins[player] == computer:
        return "win"
    return "lose"


def play_round(player_name, scores):
    """Play a single round of Rock, Paper, Scissors."""
    choices = ["rock", "paper", "scissors"]
    print("\nMake your choice:")
    print("  1) Rock")
    print("  2) Paper")
    print("  3) Scissors")

    user_input = input("Enter the number (1/2/3) or the name: ").strip().lower()

    # Accept both numbers and words as input
    mapping = {"1": "rock", "2": "paper", "3": "scissors"}
    if user_input in mapping:
        player_choice = mapping[user_input]
    elif user_input in choices:
        player_choice = user_input
    else:
        print("⚠️ Invalid input!")
        return

    computer_choice = random.choice(choices)
    result = get_winner(player_choice, computer_choice)

    print(f"\n🧑 You: {player_choice}")
    print(f"🤖 Computer: {computer_choice}")

    # Update session score
    if result == "win":
        print("✅ You win!")
        scores["win"] += 1
    elif result == "lose":
        print("❌ You lose!")
        scores["lose"] += 1
    else:
        print("🤝 It's a tie!")
        scores["tie"] += 1

    # Save this round to the separate history file
    save_result(player_name, player_choice, computer_choice, result)


# ---------- Main Menu ----------
def main():
    init_history_file()

    print("=" * 40)
    print("  🎮 Rock, Paper, Scissors 🎮")
    print("=" * 40)

    player_name = input("Enter your name: ").strip() or "Anonymous"
    scores = {"win": 0, "lose": 0, "tie": 0}

    while True:
        print("\n--- Menu ---")
        print("1) Play")
        print("2) Show history")
        print("3) Show score")
        print("4) Clear history")
        print("5) Exit")

        option = input("Choose: ").strip()

        if option == "1":
            play_round(player_name, scores)
        elif option == "2":
            show_history()
        elif option == "3":
            print(f"\n📊 Score → Wins: {scores['win']} | Losses: {scores['lose']} | Ties: {scores['tie']}")
        elif option == "4":
            clear_history()
        elif option == "5":
            print(f"\n👋 Goodbye {player_name}! Final score: {scores}")
            print(f"📁 Your history is saved in: {HISTORY_FILE}")
            break
        else:
            print("⚠️ Invalid option!")


# ---------- Entry Point ----------
if __name__ == "__main__":
    main()