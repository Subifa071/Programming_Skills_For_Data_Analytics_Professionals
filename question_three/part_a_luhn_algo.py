"""
Implements the Luhn (mod 10) algorithm to:
    - Validate account / credit card numbers
    - Compute the required validation digit
"""
# Function to calculate the checksum using the Luhn algorithm
def luhn_algorithm(account_number):
    """
    Applies the Luhn algorithm to determine validity.

    Parameters:
        number (int or str): Account or card number without validation digit
    Returns:
        tuple: (is_valid (bool), checksum_total (int))
    """

    digits = [int(digit) for digit in str(account_number)]  # Convert number to list of digits
    # Reverse the digits for processing from right to left
    digits.reverse()

    checksum = 0

    # Step 1: Double every second digit and sum its digits
    for i in range(len(digits)):
        if i % 2 == 1:  # Every second digit (starting from the right)
            doubled = digits[i] * 2
            # Add the sum of the digits of the doubled number (e.g., 14 -> 1 + 4)
            checksum += doubled // 10 + doubled % 10 #why
        else:
            checksum += digits[i]  # Add non-doubled digits

    # Step 2: Check if checksum is divisible by 10
    is_valid = checksum % 10 == 0
    return is_valid, checksum

# Function to find the correct validation digit for an invalid sequence
def find_validation_digit(account_number):
    digits = [int(digit) for digit in str(account_number)]  # Convert number to list of digits
    checksum = 0
    # Reverse the digits for processing from right to left
    digits.reverse()

    for i in range(len(digits)):
        if i % 2 == 1:  # Every second digit (starting from the right)
            doubled = digits[i] * 2
            # Add the sum of the digits of the doubled number
            checksum += doubled // 10 + doubled % 10
        else:
            checksum += digits[i]  # Add non-doubled digits

    # Calculate the check digit that will make the checksum divisible by 10
    return (10 - (checksum % 10)) % 10

# Testing the Luhn algorithm
account_numbers = [453201234567, 601112345678, 7992739871]

for number in account_numbers:
    valid, checksum = luhn_algorithm(number)
    print(f"Account Number: {number}")
    if valid:
        print(f"Valid: {valid} - Checksum: {checksum}")
    else:
        print(f"Invalid: {valid} - Checksum: {checksum}")
        # Calculate the validation digit for invalid numbers
        validation_digit = find_validation_digit(number)
        print(f"Corrected Account Number: {str(number) + str(validation_digit)}")
    print("-" * 50)
