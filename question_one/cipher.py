# Import the modular function to perform the cipher shift
from question_one.cipher_helpers import shift_cipher

def main():
    """
    Main program for the Parameterised Cipher exercise.

    Objective:
        - Prompt the user to enter a word or phrase
        - Ask for a shift value (X)
        - Apply a substitution cipher
        - Display the scrambled result

    This program demonstrates:
        - Modular programming
        - User input handling
        - Function importing
        - Clear program flow
    """

    # Step 1: Prompt user for input
    word = input("Enter a word to scramble: ")  # Word to scramble

    # Step 2: Validate shift input
    while True:
        try:
            shift = int(input("Enter the number of positions to shift (X): "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer value.")

    # Normalize shift to range 0–25
    shift = shift % 26

    # Step 3: Apply cipher
    scrambled_word = shift_cipher(word, shift)

    # Step 4: Print the scrambled word
    print(f"The scrambled word is: {scrambled_word}")

# Ensures this file runs only when executed directly
if __name__ == "__main__":
    main()
