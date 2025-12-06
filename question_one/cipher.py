# Import the modular function to perform the cipher shift
from cipher_function import shift_cipher

def main():
    # Step 1: Prompt user for input
    word = input("Enter a word to scramble: ")  # Word to scramble
    shift = int(input("Enter the number of positions to shift (X): "))  # Shift value

    # Step 2: Call the cipher function
    scrambled_word = shift_cipher(word, shift)

    # Step 3: Print the scrambled word
    print(f"The scrambled word is: {scrambled_word}")

if __name__ == "__main__":
    main()
