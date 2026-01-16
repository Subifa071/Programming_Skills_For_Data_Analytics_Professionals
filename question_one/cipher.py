# Import the modular function to perform the cipher shift
from cipher_helpers import shift_cipher

def main():
    # Step 1: Prompt user for input
    # The input can include spaces and punctuation
    word = input("Enter a word to scramble: ")  # Word to scramble

    # Step 2: Validate shift input
    # Loop continues until the user enters a valid integer
    while True:
        try:
            shift = int(input("Enter the number of positions to shift (X): "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer value.")

    # Step 3: Normalize shift to range 0–25
    # Using modulo ensures the shift always stays within 0–25
    shift = shift % 26

    # Step 4: Apply the cipher using the imported helper function
    scrambled_word = shift_cipher(word, shift)

    # Print the scrambled word
    print(f"The scrambled word is: {scrambled_word}")

# Ensures this file runs only when executed directly
if __name__ == "__main__":
    main()
