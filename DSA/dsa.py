import random
import SHA.sha384


def generate_dsa(N, L, p, q, g, x, k, msg, ks):
    """
    Funkcja generująca podpis cyfrowy z użyciem algorytmu DSA.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
    :param N: Parametr N ze standardu
    :param L: Parametr L ze standardu
    :param p: Liczba pierwsza p o długości L bitów zgodnie ze standardem
    :param q: Liczba pierwsza q będąca dzielnikiem liczby p-1 o długości N bitów zgodnie ze standardem
    :param g: Generator podgrupy multiplikatywnej ciała Galois o liczności p
    :param x: Klucz prywatny (większy od 0, mniejszy od q)
    :param k: Parametr przyporządkowany do wiadomości
    :param msg: Wiadomość, dla której obliczamy podpis cyfrowy (w bitach)
    :param ks: Użyte wartości k, gdyż mają być unikalne
    :return: Podpis cyfrowy wiadomości msg przechowywany jako lista dwuelementowa liczb całkowitych
    """
    if p >= pow(2, L) or p < pow(2, L - 1):
        raise Exception("Błędne parametry dla DSA! - Błędna długość p w bitach")
    if q >= pow(2, N) or q < pow(2, N - 1):
        raise Exception("Błędne parametry dla DSA - Błędna długość q w bitach")
    if ((p - 1) % q != 0):
        raise Exception("Błędne parametry dla DSA - q nie jest dzielnikiem p-1!")
    if k < 0 or k >= q or k in ks:
        raise Exception("Błędne parametry dla DSA - Błędna wartość parametru k")
    if x >= q or x < 0:
        raise Exception("Błędne parametry dla DSA - Błędny klucz prywatny!")
    if g >= p or g <= 1:
        raise Exception("Błędne parametry dla DSA - Błędny generator grupy!")
    if not (L == 1024 and N == 160) \
       and not (L == 2048 and N == 224) and not (L == 2048 and N == 256) and not (L == 3072 and N == 256):
        raise Exception("Błędne parametry dla DSA - Błędne parametry L,N!")

    s = 0
    while s == 0:  # Zaczynamy od s==0 zeby zaczac, potem jest taki warunek sprawdzany, zamiennik petli do while
        r = pow(g, k, p) % q  # obliczenie wartosci r
        while r == 0:
            k = random.randint(2, q)
            r = pow(g, k, p) % q
        sha_dig = SHA.sha384.sha384(msg)
        n = min([N, len(sha_dig)])
        dig = int(sha_dig[:n], 2) # Bierzemy pierwsze n bitów zgodnie ze standardem
        s = (pow(k, -1, q) * (dig + x * r)) % q  # Obliczamy wartość

    ks.append(k) # To k było już wykorzystane
    return [r, s]  # W standardzie jest przechowywany wynik jako tuple, przechowujemy jako lista integerów


def verify_dsa(N, L, p, q, g, y, sign, msg1):
    """
    Funkcja weryfikująca poprawność podpisu cyfrowego dla algorytmu DSA.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
    :param N: Parametr N ze standardu
    :param L: Parametr L ze standardu
    :param p: Liczba pierwsza p o długości L bitów zgodnie ze standardem
    :param q: Liczba pierwsza q będąca dzielnikiem liczby p-1 o długości N bitów zgodnie ze standardem
    :param g: Generator podgrupy multiplikatywnej ciała Galois o liczności p
    :param y: Klucz publiczny
    :param sign: Weryfikowany podpis
    :param msg1: Otrzymana wiadomość, dla której weryfikowany jest podpis (w bitach)
    :return: Informacja, czy podpis cyfrowy wiadomości jest poprawny
    """
    if p >= pow(2, L) or p < pow(2, L - 1):
        raise Exception("Błędne parametry dla DSA! - Błędna długość p w bitach")
    if q >= pow(2, N) or q < pow(2, N - 1):
        raise Exception("Błędne parametry dla DSA - Błędna długość q w bitach")
    if ((p - 1) % q != 0):
        raise Exception("Błędne parametry dla DSA - q nie jest dzielnikiem p-1!")
    if g >= p or g <= 1:
        raise Exception("Błędne parametry dla DSA - Błędny generator grupy!")
    if not (L == 1024 and N == 160) \
            and not (L == 2048 and N == 224) and not (L == 2048 and N == 256) and not (L == 3072 and N == 256):
        raise Exception("Błędne parametry dla DSA - Błędne parametry L,N!")
    if sign[0] >= q or sign[0] <= 0 or sign[1] <= 0 or sign[1] >= q:
        return False
    w = pow(sign[1], -1, q)
    sha_dig = SHA.sha384.sha384(msg1)
    n = min([N, len(sha_dig)]) # krótsza z wartości, tak jak w standardzie
    dig = int(sha_dig[:n], 2) # wzięcie n pierwszych eltów, tak jak w standardzie
    u_1 = int((dig * w) % q)
    u_2 = int((sign[0] * w) % q)
    ver = ((pow(g, u_1, p) * pow(y, u_2, p)) % p) % q

    return ver == sign[0]

