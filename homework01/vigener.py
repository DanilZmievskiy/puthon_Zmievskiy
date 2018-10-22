def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    j = 0
    for i in plaintext:
        if ord('a') <= ord(keyword[j]) <= ord('z'):
            numb = ord(keyword[j]) - 122 + 25
        elif ord('A') <= ord(keyword[j]) <= ord('Z'):
            numb = ord(keyword[j]) - 90 + 25
        i = ord(i)
        if ord('a') <= i <= ord('z'):
                i += numb
                if i > 122:
                    i -= 122
                    i = 96 + i
        elif ord('A') <= i <= ord('Z'):
            i += numb
            if i > 90:
                i -= 90
                i = 64 + i
        ciphertext += chr(i)
        j += 1
        if j > len(keyword) - 1:
            j = 0
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    j = 0
    for i in ciphertext:
        if ord('a') <= ord(keyword[j]) <= ord('z'):
            numb = ord(keyword[j]) - 122 + 25
        elif ord('A') <= ord(keyword[j]) <= ord('Z'):
            numb = ord(keyword[j]) - 90 + 25
        i = ord(i)
        if ord('a') <= i <= ord('z'):
                i -= numb
                if i < 97:
                    i -= 97
                    i = 123 + i
        elif ord('A') <= i <= ord('Z'):
            i -= numb
            if i < 65:
                i -= 65
                i = 91 + i
        plaintext += chr(i)
        j += 1
        if j > len(keyword) - 1:
            j = 0
    return plaintext
