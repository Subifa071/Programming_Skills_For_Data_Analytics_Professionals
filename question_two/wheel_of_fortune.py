import random

# Function to simulate spinning the wheel
def spin_wheel():
    # Possible point values on the wheel
    wheel_values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    return random.choice(wheel_values)

# Function to display the word/phrase with underscores
def display_word(word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

# Function to play the Wheel of Fortune game
def play_game():
    # Step 1: Get word or phrase from the player
    word = input("Enter a word or phrase for the player to guess: ").lower()
    guessed_letters = set()  # Track guessed letters
    total_points = 0  # Track total points
    attempts_left = len(word) + 5  # Allow a few extra guesses

    # Step 2: Game loop
    while attempts_left > 0:
        # Display the current state of the word
        print(f"Current word: {display_word(word, guessed_letters)}")
        print(f"Total points: {total_points}")
        print(f"Attempts left: {attempts_left}")
        
        # Step 3: Spin the wheel and get a point value
        spin_value = spin_wheel()
        print(f"Wheel spin! You got: {spin_value} points.")
        
        # Step 4: Get the player's guess
        guess = input("Guess a letter: ").lower()

        # Ensure valid input
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a valid letter.")
            continue
        
        # If the letter has already been guessed, skip it
        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue
        
        guessed_letters.add(guess)  # Add the guessed letter to the set
        
        # Step 5: Check if the guessed letter is in the word
        if guess in word:
            occurrences = word.count(guess)  # Count how many times the letter appears in the word
            points = occurrences * spin_value
            total_points += points  # Add points to the total
            print(f"Correct! The letter '{guess}' appeared {occurrences} time(s). You earned {points} points.")
        else:
            print(f"Sorry, the letter '{guess}' is not in the word.")
        
        # Step 6: Check if the player has guessed all letters
        if all(letter in guessed_letters for letter in word if letter != ' '):
            print(f"Congratulations! You've guessed the word/phrase: {word}")
            print(f"Total points: {total_points}")
            break
        
        attempts_left -= 1  # Deduct an attempt for each guess

    # If attempts are over
    if attempts_left == 0:
        print("Game over! You've run out of attempts.")
        print(f"The word/phrase was: {word}")
        print(f"Total points: {total_points}")

# Run the game
if __name__ == "__main__":
    play_game()


# Handling of special characters