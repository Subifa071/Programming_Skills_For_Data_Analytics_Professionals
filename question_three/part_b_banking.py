from part_a_luhn_algo import luhn_algorithm, find_validation_digit

"""
Real-Life Application: How the Luhn algorithm protects the bank from common data entry errors and potential fraud?

The Luhn algorithm protects banks by using a checksum (mod 10) to validate account/card numbers before acceptance.
Most common typing mistakes—like a single wrong digit or swapping two adjacent digits—break the checksum, so the
system can instantly flag and reject the number. This reduces operational errors (e.g., wrong account lookups or
misrouted payments) and also blocks many randomly invented/fabricated numbers from passing basic validation,
adding a lightweight first layer of fraud prevention.
"""

# Find which invalid sequence requires the largest correction
def find_largest_correction(account_numbers):
    largest_correction = 0
    largest_correction_number = None

    for number in account_numbers:
        valid, checksum = luhn_algorithm(number)
        if not valid:
            validation_digit = find_validation_digit(number)
            correction = abs(validation_digit - (number % 10))  # Calculate correction required
            if correction > largest_correction:
                largest_correction = correction
                largest_correction_number = number
            print(f"Original Account: {number}, Corrected Account: {str(number) + str(validation_digit)}")

    return largest_correction_number, largest_correction

# Test account numbers
account_numbers = [453201234567, 601112345678, 7992739871]

# Check for the largest correction
largest_correction_number, largest_correction = find_largest_correction(account_numbers)

print(f"Largest correction is needed for account number: {largest_correction_number} with a correction of {largest_correction}")
