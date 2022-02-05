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
        dig = int(sha_dig[:n], 2)  # Bierzemy pierwsze n bitów zgodnie ze standardem
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

# Można użyć do testów, na podstawie danych z IETF
# https://www.ietf.org/rfc/rfc6979.txt
# p1 = int("86F5CA03DCFEB225063FF830A0C769B9DD9D6153AD91D7CE27F787C43278B447E6533B86B18BED6E8A48B784A14C252C5BE0DBF60B86D6385BD2F12FB763ED8873ABFD3F5BA2E0A8C0A59082EAC056935E529DAF7C610467899C77ADEDFC846C881870B7B19B2B58F9BE0521A17002E3BDD6B86685EE90B3D9A1B02B782B1779", 16)
# q1 = int("996F967F6C8E388D9E28D01E205FBA957A5698B1",16)
# g1 = int("07B0F92546150B62514BB771E2A0C0CE387F03BDA6C56B505209FF25FD3C133D89BBCD97E904E09114D9A7DEFDEADFC9078EA544D2E401AEECC40BB9FBBF78FD87995A10A1C27CB7789B594BA7EFB5C4326A9FE59A070E136DB77175464ADCA417BE5DCE2F40D10A46A3A3943F26AB7FD9C0398FF8C76EE0A56826A8A88F1DBD", 16)
# x1 = int("411602CB19A6CCC34494D79D98EF1E7ED5AF25F7", 16)
# y1 = int("5DF5E01DED31D0297E274E1691C192FE5868FEF9E19A84776454B100CF16F65392195A38B90523E2542EE61871C0440CB87C322FC4B4D2EC5E1E7EC766E1BE8D4CE935437DC11C3C8FD426338933EBFE739CB3465F4D3668C5E473508253B1E682F65CBDC4FAE93C2EA212390E54905A86E2223170B44EAA7DA5DD9FFCFB7F3B", 16)
# k1 = int("95897CD7BBB944AA932DBC579C1C09EB6FCFC595", 16)
# r1 = int("07F2108557EE0E3921BC1774F1CA9B410B4CE65A", 16)
# s1 = int("54DF70456C86FAC10FAB47C1949AB83F2C6F7595", 16)
# message = bin(int("sample".encode('utf-8').hex(), 16))[2:]
# print(message)
# N1 = 160
# signature = generate_dsa(N1, p1, q1, g1, x1, k1, message)
# print(signature)
# print([r1,s1])
# print(verify_dsa(N1, p1, q1, g1, y1, signature, message)) # should be true, dziala!
