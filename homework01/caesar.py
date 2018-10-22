def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:
        i = ord(i)
        if (ord('A') <= i <= ord('Z')) or (ord('a') <= i <= ord('z')):
            if ord('x') <= i <= ord('z'):
                i = i - ord('z') + 2 + ord('a')
            elif ord('X') <= i <= ord('Z'):
                i = i - ord('Z') + 2 + ord('A')
            else:
                i += 3
        ciphertext += chr(i)
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in ciphertext:
        i = ord(i)
        if (ord('A') <= i <= ord('Z')) or (ord('a') <= i <= ord('z')):
            if ord('a') <= i <= ord('c'):
                i = i - ord('c') + 2 + ord('x')
            elif ord('A') <= i <= ord('C'):
                i = i - ord('C') + 2 + ord('X')
            else:
                i -= 3
        plaintext += chr(i)
    return plaintext
