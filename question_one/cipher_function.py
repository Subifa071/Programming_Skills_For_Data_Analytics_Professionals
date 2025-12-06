def shift_cipher(word, shift):
    """
    Shifts each letter of the input word by the given shift value.
    This function works for both uppercase and lowercase letters.
    Non-alphabetic characters remain unchanged.
    
    :param word: The word to be scrambled.
    :param shift: The number of positions to shift each letter (X).
    :return: The scrambled word.
    """
    result = []  # This will store the scrambled word
    
    for char in word:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            start = 65 if char.isupper() else 97  # ASCII value of 'A' (65) and 'a' (97)
            # Shift the character and handle wrapping with modulo 26
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(shifted_char)
        else:
            # Non-alphabetic characters (e.g., spaces, punctuation) are added unchanged
            result.append(char)

    return ''.join(result)
