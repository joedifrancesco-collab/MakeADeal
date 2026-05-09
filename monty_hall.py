"""
Monty Hall Problem Simulator

This program demonstrates the Monty Hall problem by allowing users to:
1. Play a single interactive game
2. Run automated simulations to prove the theory
"""

import random
from typing import Tuple, Dict


class MontyHallGame:
    """Manages the Monty Hall game logic."""
    
    def __init__(self):
        """Initialize the game with doors and car placement."""
        self.doors = [False, False, False]  # False = goat, True = car
        self.car_position = random.randint(0, 2)
        self.doors[self.car_position] = True
        self.user_choice = None
        self.revealed_door = None
        
    def player_selects_door(self, door_number: int) -> None:
        """Record the player's initial door selection (1-3)."""
        if door_number not in [1, 2, 3]:
            raise ValueError("Door must be 1, 2, or 3")
        self.user_choice = door_number - 1  # Convert to 0-indexed
        
    def host_reveals_goat(self) -> int:
        """
        Host reveals a door with a goat (not user's choice, not the car).
        Returns the revealed door number (1-indexed).
        """
        # Find doors that are not the user's choice and don't have a car
        available_doors = []
        for i in range(3):
            if i != self.user_choice and not self.doors[i]:
                available_doors.append(i)
        
        self.revealed_door = random.choice(available_doors)
        return self.revealed_door + 1  # Convert to 1-indexed
    
    def get_remaining_door(self) -> int:
        """Get the unopened door the player can switch to (1-indexed)."""
        for i in range(3):
            if i != self.user_choice and i != self.revealed_door:
                return i + 1
        
    def check_win_stay(self) -> bool:
        """Check if player wins by staying with original choice."""
        return self.doors[self.user_choice]
    
    def check_win_switch(self) -> bool:
        """Check if player wins by switching to the remaining door."""
        for i in range(3):
            if i != self.user_choice and i != self.revealed_door:
                return self.doors[i]
        return False


def get_valid_input(prompt: str, valid_options: list) -> str:
    """
    Get validated user input.
    
    Args:
        prompt: The prompt to display
        valid_options: List of valid responses
        
    Returns:
        The valid user input
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please enter one of: {', '.join(valid_options)}")


def play_single_game() -> None:
    """Play a single interactive game of Monty Hall."""
    print("\n" + "="*60)
    print("WELCOME TO THE MONTY HALL PROBLEM SIMULATOR")
    print("="*60)
    
    game = MontyHallGame()
    
    # Player selects initial door
    print("\nYou are presented with 3 doors:")
    print("  Door 1: Unknown")
    print("  Door 2: Unknown")
    print("  Door 3: Unknown")
    print("\nBehind one door is a CAR. Behind the other two are GOATS.")
    
    while True:
        try:
            choice = int(input("\nWhich door do you choose? (1-3): "))
            game.player_selects_door(choice)
            break
        except ValueError:
            print("Please enter a number between 1 and 3.")
    
    print(f"\nYou chose Door {game.user_choice + 1}")
    
    # Host reveals a goat
    revealed = game.host_reveals_goat()
    print(f"\nThe host opens Door {revealed} and reveals a GOAT!")
    
    remaining_door = game.get_remaining_door()
    print(f"The remaining unopened doors are: Door {game.user_choice + 1} (your choice) and Door {remaining_door}")
    
    # Player decides to stick or switch
    decision = get_valid_input(
        "\nDo you want to STICK with your original door or SWITCH? (stick/switch): ",
        ["stick", "switch"]
    )
    
    # Determine outcome
    print("\n" + "-"*60)
    if decision == "stick":
        won = game.check_win_stay()
        final_door = game.user_choice + 1
    else:
        won = game.check_win_switch()
        final_door = remaining_door
    
    print(f"Your final choice: Door {final_door}")
    
    # Reveal all doors
    for i in range(3):
        door_num = i + 1
        content = "CAR 🚗" if game.doors[i] else "GOAT"
        marker = " <- Your choice" if door_num == final_door else ""
        print(f"  Door {door_num}: {content}{marker}")
    
    print("\n" + "-"*60)
    if won:
        print("🎉 CONGRATULATIONS! You won the CAR!")
    else:
        print("😞 Sorry, you got a GOAT. Better luck next time!")
    print("="*60 + "\n")


def run_simulation(num_rounds: int) -> Dict[str, Dict[str, int]]:
    """
    Run automated simulations with both stick and switch strategies.
    
    Args:
        num_rounds: Number of games to simulate
        
    Returns:
        Dictionary with results for stick and switch strategies
    """
    results = {
        "stick": {"wins": 0, "losses": 0},
        "switch": {"wins": 0, "losses": 0}
    }
    
    print(f"\nRunning {num_rounds} simulations...")
    print("Progress: ", end="", flush=True)
    
    for round_num in range(num_rounds):
        # Show progress every 10% of rounds
        if (round_num + 1) % max(1, num_rounds // 10) == 0:
            print(f"{((round_num + 1) // max(1, num_rounds // 10)) * 10}%...", end="", flush=True)
        
        game = MontyHallGame()
        
        # Player randomly selects a door
        initial_choice = random.randint(1, 3)
        game.player_selects_door(initial_choice)
        
        # Host reveals a goat
        game.host_reveals_goat()
        
        # Simulate STICK strategy
        if game.check_win_stay():
            results["stick"]["wins"] += 1
        else:
            results["stick"]["losses"] += 1
        
        # Simulate SWITCH strategy
        if game.check_win_switch():
            results["switch"]["wins"] += 1
        else:
            results["switch"]["losses"] += 1
    
    print(" Done!\n")
    return results


def display_simulation_results(results: Dict[str, Dict[str, int]], num_rounds: int) -> None:
    """
    Display formatted simulation results.
    
    Args:
        results: Dictionary containing win/loss data
        num_rounds: Total number of rounds simulated
    """
    print("="*60)
    print("SIMULATION RESULTS")
    print("="*60)
    
    for strategy in ["stick", "switch"]:
        wins = results[strategy]["wins"]
        losses = results[strategy]["losses"]
        win_percentage = (wins / num_rounds) * 100
        
        print(f"\n{strategy.upper()} Strategy:")
        print(f"  Wins:  {wins:5d} ({win_percentage:6.2f}%)")
        print(f"  Losses: {losses:5d} ({100 - win_percentage:6.2f}%)")
    
    # Calculate the advantage
    stick_wins = results["stick"]["wins"]
    switch_wins = results["switch"]["wins"]
    
    print("\n" + "-"*60)
    print("ANALYSIS:")
    print(f"  Switching won {switch_wins - stick_wins} more games than sticking")
    print(f"  Switching advantage: {((switch_wins - stick_wins) / num_rounds) * 100:.2f}%")
    print("\nTHEORY VERIFICATION:")
    print(f"  Expected stick rate:   33.33% ± 2%")
    print(f"  Expected switch rate:  66.67% ± 2%")
    print(f"  Actual stick rate:     {(stick_wins / num_rounds) * 100:.2f}%")
    print(f"  Actual switch rate:    {(switch_wins / num_rounds) * 100:.2f}%")
    print("="*60 + "\n")


def get_simulation_rounds() -> int:
    """
    Get the number of simulation rounds from user (1-1000000).
    
    Returns:
        Number of rounds to simulate
    """
    while True:
        try:
            rounds = int(input("How many rounds to simulate? (1-1000000): "))
            if 1 <= rounds <= 1000000:
                return rounds
            else:
                print("Please enter a number between 1 and 1000000.")
        except ValueError:
            print("Please enter a valid number.")


def main_menu() -> None:
    """Display main menu and handle user selections."""
    while True:
        print("\n" + "="*60)
        print("MONTY HALL PROBLEM SIMULATOR")
        print("="*60)
        print("1. Play a single game")
        print("2. Run simulation (auto-play multiple rounds)")
        print("3. Exit")
        print("="*60)
        
        choice = get_valid_input("Select an option (1-3): ", ["1", "2", "3"])
        
        if choice == "1":
            play_single_game()
        elif choice == "2":
            num_rounds = get_simulation_rounds()
            results = run_simulation(num_rounds)
            display_simulation_results(results, num_rounds)
        elif choice == "3":
            print("\nThank you for playing! Goodbye!")
            break


if __name__ == "__main__":
    main_menu()
