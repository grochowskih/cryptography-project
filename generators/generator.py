import random


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
