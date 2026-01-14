def shift_cipher(word, shift):
    """
    Shifts each letter of the input word by the given shift value.
    This function works for both uppercase and lowercase letters.
    Non-alphabetic characters remain unchanged.
    
    Parameters:
        word (str): The word or text to be scrambled.
        shift (int): The number of positions to shift each letter (X).
    Returns:
        str: The scrambled word after applying the cipher.    
    """
    result = []  # This will store the scrambled word
    
    for char in word:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            # ASCII starting point depends on case
            start = 65 if char.isupper() else 97  # ASCII value of 'A' (65) and 'a' (97)

            # Shift the character and handle wrapping with modulo 26
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(shifted_char)
        else:
            # Preserve spaces, punctuation, and digits
            result.append(char)

    return ''.join(result)
