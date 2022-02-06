from TDES.DES_code import TripleDesEncrypt

binary_hex_conversion_table = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'A': '1010',
    'b': '1011',
    'B': '1011',
    'c': '1100',
    'C': '1100',
    'd': '1101',
    'D': '1101',
    'e': '1110',
    'E': '1110',
    'f': '1111',
    'F': '1111'
}


def hex_to_binary(s):
    """
    Przekształcamy tekst z systemu szesnastkowego na binarny.
    :param s: Tekst w systemie szesnastkowym.
    :return: Tekst w systemie binarnym.
    """

    binary_string = ""
    for character in s:
        binary_string += binary_hex_conversion_table[character]
    return binary_string


def binary_to_hex(b):
    """
    Przekształcamy tekst z systemu binarnego na szesnatskowy.
    :param b: Tekst w systemie binarnym.
    :return: Tekst w systemie szesnastkowym.
    """
    hex_string = format(int(b, 2), 'x')
    hex_string.rjust(4, '0')
    if len(hex_string) % 16 == 0:
        return hex_string
    return '0'*(16-(len(hex_string) % 16)) + hex_string


def ofb_encrypt(plaintext, key1, key2, key3, iv):
    # https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf
    # IV wybiera użytkownik lub generator, generator inkrementuje iv więc jest ono za każdym razem inne.
    # Standard mówi, że IV musi być nonce, u nas jest o ile tworzy je generator, użytkownik może wpisać cokolwiek
    """
    Funkcja szyfruje podany tekst, przy pomocy podanego klucza oraz iv.
    :param plaintext: Tekst który chcemy zaszyfrować w systemie szesnastkowym.
    :param key: Klucz, którym chcemy zaszyfrować tekst (w systemie szesnastkowym).
    :param iv: Wektor inicjalizujacy (w systemie szesnastkowym).
    :return: Zaszyfrowany tekst w systemie szesnastkowym.
    """
    plaintext = hex_to_binary(plaintext)
    iv = hex_to_binary(iv)
    key1 = hex_to_binary(key1)
    key2 = hex_to_binary(key2)
    key3 = hex_to_binary(key3)

    blocks = []
    encrypted_blocks = []
    for i in range(0, len(plaintext), 64):
        blocks.append(plaintext[i: i + 64])

    current_vector = iv

    for i in range(0, len(blocks)):
        current_vector = TripleDesEncrypt(current_vector, key1, key2, key3)
        xor = int(blocks[i], 2) ^ int(current_vector, 2)
        encrypted_blocks.append('{0:b}'.format(xor))

    enc_hex = []
    for i in range(0, len(blocks)):
        enc_hex.append(binary_to_hex(encrypted_blocks[i]))

    return ''.join(enc_hex)


def ofb_decrypt(ciphertext, key1, key2, key3, iv):
    # https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf
    """
    Funkcja deszyfruje podany tekst, przy pomocy podanego klucza oraz iv.
    :param ciphertext: Szyfr który chcemy odszyfrować w systemie szesnastkowym.
    :param key: Klucz, którym chcemy odszyfrować tekst (w systemie szesnastkowym).
    :return: Odszyfrowany tekst w systemie szesnastkowym.
    """
    return ofb_encrypt(ciphertext, key1, key2, key3, iv)


