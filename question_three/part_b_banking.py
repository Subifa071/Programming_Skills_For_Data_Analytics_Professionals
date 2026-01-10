from part_a_luhn_algo import luhn_algorithm, find_validation_digit

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
