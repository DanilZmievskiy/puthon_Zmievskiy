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
    j = 0
    ciphertext = ""
    for i in plaintext:
        if ord('a') <= ord(keyword[j]) <= ord('z'):
            numb = ord(keyword[j]) - 122 + 25
        elif ord('A') <= ord(keyword[j]) <= ord('Z'):
            numb = ord(keyword[j]) - 90 + 25
        i = ord(i)
        if (ord('a') <= i <= ord('z')):
            i += numb
            if i > 122:
                i -= 122
                a = 96 + i
                a = chr(a)
            else:
                a = chr(i)
        elif (ord('A') <= i <= ord('Z')):
            i += numb
            if i > 90:
                i -= 90
                a = 64 + i
                a = chr(a)
            else:
                a = chr(i)
        else:
            a = chr(i)
        ciphertext += a
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
    # PUT YOUR CODE HERE
    return plaintext
