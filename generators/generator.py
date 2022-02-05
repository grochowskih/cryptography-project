import random
from TDES.OFB import binary_to_hex

iv_start_table = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def generate_key():
    """
    Generuje klucz 64-bitowy zapisany w systemie szesnastkowym. Do generowania potrzebna jest źródło losowości.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-67r2.pdf
    :return: Wygenerowany klucz
    """
    key = ""
    for i in range(64):
        temp = str(random.randint(0, 1))
        key += temp
    return TDES.OFB.binary_to_hex(key)

def increment_bit(table, i):
    """
    Inkrementuje podany bit w tablicy. Jeśli element jest równy 2 to funkcja ustawia go na 0 i przechodzi wyżej
    aż do rozmiaru tablicy.
    :param table: Tablica reprezentująca tekst w systemie dwójkowym.
    :param i: Element tabeli który inkrementujemy.
    :return: Tablica reprezentująca liczbę w systemie dwójkowym powiększoną o 1.
    """
    table[i] += 1
    if table[i] == 2 & i == 0:
        return [0] * len(table)
    if(table[i]) == 2:
        table[i] = 0
        return increment_bit(table, i-1)
    return table


def increment_iv(table):
    # https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf
    # Zrobiliśmy counter który po osiągnieciu maksymalnej długości wraca do 0
    """
    Inkrementujemy liczbę.
    :return: IV powiększone o 1.
    """
    str_table = ""
    table = increment_bit(table, len(table) - 1)
    for i in range(0, len(table)):
        str_table += str(table[i])
    return binary_to_hex(str_table)


def generate_iv():
    # https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf
    """
    :return: Wektor inicjalizujący.
    """
    return increment_iv(iv_start_table)


def group_generator(p, q):
    """
    Funkcja wyznaczająca generator podgrupy multiplikatywnej potrzebny do algorytmu DSA.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf (Appendix A.2.1)
    :param p: Liczba pierwsza (jako int) zgodnie z DSA
    :param q: Liczba pierwsza (jako int) zgodnie z DSA
    :return: Generator podgrupy
    """
    e = int((p-1)/q) # q jest dzielnikiem p-1 w DSA w założenia
    tried_h = [] # Jakie h były próbowane?
    h = random.randint(2, p-1) # h jakiekolwiek od 2 do p-1
    g = pow(h, e, p)
    while g == 1:
        tried_h.append(h)
        h = random.randint(2, p - 1)
        while h in tried_h:
            h = random.randint(2, p - 1)
        g = pow(h, e, p)
    return g
