import re

INIT_VALUES_16 = ["cbbb9d5dc1059ed8", "629a292a367cd507", "9159015a3070dd17", "152fecd8f70e5939", "67332667ffc00b31",
                  "8eb44a8768581511", "db0c2e0d64f98fa7", "47b5481dbefa4fa4"]
INIT_VALUES = [int(el, 16) for el in INIT_VALUES_16]

CONST_VALUES_16 = ["428a2f98d728ae22", "7137449123ef65cd", "b5c0fbcfec4d3b2f", "e9b5dba58189dbbc",
                   "3956c25bf348b538", "59f111f1b605d019", "923f82a4af194f9b", "ab1c5ed5da6d8118",
                   "d807aa98a3030242", "12835b0145706fbe", "243185be4ee4b28c", "550c7dc3d5ffb4e2",
                   "72be5d74f27b896f", "80deb1fe3b1696b1", "9bdc06a725c71235", "c19bf174cf692694",
                   "e49b69c19ef14ad2", "efbe4786384f25e3", "0fc19dc68b8cd5b5", "240ca1cc77ac9c65",
                   "2de92c6f592b0275", "4a7484aa6ea6e483", "5cb0a9dcbd41fbd4", "76f988da831153b5",
                   "983e5152ee66dfab", "a831c66d2db43210", "b00327c898fb213f", "bf597fc7beef0ee4",
                   "c6e00bf33da88fc2", "d5a79147930aa725", "06ca6351e003826f", "142929670a0e6e70",
                   "27b70a8546d22ffc", "2e1b21385c26c926", "4d2c6dfc5ac42aed", "53380d139d95b3df",
                   "650a73548baf63de", "766a0abb3c77b2a8", "81c2c92e47edaee6", "92722c851482353b",
                   "a2bfe8a14cf10364", "a81a664bbc423001", "c24b8b70d0f89791", "c76c51a30654be30",
                   "d192e819d6ef5218", "d69906245565a910", "f40e35855771202a", "106aa07032bbd1b8",
                   "19a4c116b8d2d0c8", "1e376c085141ab53", "2748774cdf8eeb99", "34b0bcb5e19b48a8",
                   "391c0cb3c5c95a63", "4ed8aa4ae3418acb", "5b9cca4f7763e373", "682e6ff3d6b2b8a3",
                   "748f82ee5defb2fc", "78a5636f43172f60", "84c87814a1f0ab72", "8cc702081a6439ec",
                   "90befffa23631e28", "a4506cebde82bde9", "bef9a3f7b2c67915", "c67178f2e372532b",
                   "ca273eceea26619c", "d186b8c721c0c207", "eada7dd6cde0eb1e", "f57d4f7fee6ed178",
                   "06f067aa72176fba", "0a637dc5a2c898a6", "113f9804bef90dae", "1b710b35131c471b",
                   "28db77f523047d84", "32caab7b40c72493", "3c9ebe0a15c9bebc", "431d67c49c100d4c",
                   "4cc5d4becb3e42b6", "597f299cfc657e2a", "5fcb6fab3ad6faec", "6c44198c4a475817"]

CONST_VALUES = [int(el, 16) for el in CONST_VALUES_16]


def sigma_0(word):
    """
    Funkcja sigma_0 występująca w standardzie NIST
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
    :param word: Binarne słowo długości 64
    :return: Przekształcone słowo x
    """
    x = int(word, 2)
    return (rotr(word, 1)) ^ (rotr(word, 8)) ^ (x >> 7)


def sigma_1(word):
    """
    Funkcja sigma_1 występująca w standardzie NIST
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
    :param word: Binarne słowo długości 64
    :return: Przekształcone słowo x
    """
    x = int(word, 2)
    return (rotr(word, 19)) ^ (rotr(word, 61)) ^ (x >> 6)


def rotr(word, n):
    """
    Funkcja ROTR występująca w standardzie NIST.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
    :param word: Binarne słowo
    :param n: Przesunięcie w funkcji ROTR
    :return: ROTR(word)
    """
    x = int(word, 2)
    return (x >> n) | (x << (64 - n))


def ch(word_1, word_2, word_3):
    """
    Funkcja Ch występująca w standardzie NIST.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
    :param word_1: Binarne słowo
    :param word_2: Binarne słowo
    :param word_3: Binarne słowo
    :return: Ch(word_1, word_2, word_3)
    """
    x, y, z = int(word_1, 2), int(word_2, 2), int(word_3, 2)
    return (x & y) ^ (~x & z)


def maj(word_1, word_2, word_3):
    """
    Funkcja Maj występująca w standardzie NIST.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
    :param word_1: Binarne słowo
    :param word_2: Binarne słowo
    :param word_3: Binarne słowo
    :return: Maj(word_1, word_2, word_3)
    """
    x, y, z = int(word_1, 2), int(word_2, 2), int(word_3, 2)
    return (x & y) ^ (y & z) ^ (x & z)


def pad_1024(msg):
    """
    Funkcja dokonująca uzupełnienia wiadomości do długości będącej wielokrotnością 1024 bitów.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
    :param msg: Wiadomość, która ma zostać uzupełniona (w bitach)
    :return: Uzupełniona wiadomość msg
    """
    if re.match("^[01]+$", msg) is None:
        raise Exception("Błędna wiadomość do obliczenia skrótu!")

    # Wiadomość musi być tak, ze każdy znak jest długości 8, zatem jeśli nie jest tak, to musimy dostawić 0
    length_msg = len(msg)
    while length_msg % 8 != 0:
        msg = "0" + msg
        length_msg = len(msg)

    length_msg_moduli = length_msg % 1024
    k = (896 - 1 - length_msg_moduli) % 1024  # Rozwiązanie liniowej kongruencji występującej w paddingu

    length_bin = '{0:0128b}'.format(length_msg)  # Długość wiadomości zapisana za pomocą bitów długości 128

    return msg + "1" + ("0" * k) + length_bin


def sha384_algorithm(msg):
    """
    Funkcja obliczająca skrót wiadomość msg dla uzupełnionej wiadomości.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
    :param msg: Uzupełniona wiadomość, dla której obliczamy skrót (w bitach)
    :return: Skrót wiadomości msg
    """

    N = int(len(msg) / 1024)
    msg_blocks = [msg[i:i + 1024] for i in range(N)]
    h_seq = [['{0:064b}'.format(el) for el in INIT_VALUES]]  # Ustawienie wartości inicjalnych w formacie binarnym

    iterator = 0  # Dodatkowy iterator pętli dla ułatwienia zapisu
    for block in msg_blocks:  # Dla każdego bloku po kolei
        iterator = iterator + 1  # Wzrost iteratora
        w_seq = [block[i*64:i*64+64] for i in
                 range(int(1024 / 64))] # Wzięcie słów z bloku
        for k in range(16, 80):  # dla każdego k od 16 do 79
            w = '{0:064b}'.format(
                (int(sigma_1(w_seq[k - 2])) + int(w_seq[k - 7], 2) + int(sigma_0(w_seq[k - 15])) + int(
                    w_seq[k - 16], 2)) % pow(2, 64))  # Operacja wyznaczania kolejnych elementów ciągu W
            w_seq.append(w)

        a_seq = h_seq[iterator - 1].copy()  # Ustawienie wartości #A_k dla k od 0 do 7 - w standardzie NIST a,b,c,d,e,f,g,h
        for k in range(0, 80):  # Dla każdego k od 0 do 79 włącznie
            t_1 = '{0:064b}'.format((int(a_seq[7], 2) + (rotr(a_seq[4], 14) ^ rotr(a_seq[4], 18) ^ rotr(a_seq[4], 41)) +
                                     CONST_VALUES[k] + ch(a_seq[4], a_seq[5], a_seq[6])
                                     + int(w_seq[k], 2)) % pow(2, 64)) # Wartość parametru t1
            t_2 = '{0:064b}'.format(((rotr(a_seq[0], 28) ^ rotr(a_seq[0], 34) ^ rotr(a_seq[0], 39)) +
                                     maj(a_seq[0], a_seq[1], a_seq[2])) % pow(2, 64)) # Wartość parametru t2
            a_seq[7] = a_seq[6] # Sekwencja podstawien - w standardzie jako a,b,c,d,e,f,g,h
            a_seq[6] = a_seq[5]
            a_seq[5] = a_seq[4]
            a_seq[4] = '{0:064b}'.format((int(a_seq[3], 2) + int(t_1, 2)) % pow(2, 64))
            a_seq[3] = a_seq[2]
            a_seq[2] = a_seq[1]
            a_seq[1] = a_seq[0]
            a_seq[0] = '{0:064b}'.format((int(t_2, 2) + int(t_1, 2)) % pow(2, 64))

        new_h = ['{0:064b}'.format((int(a_seq[kk], 2) + int(h_seq[iterator - 1][kk], 2)) % pow(2, 64)) for kk in
                     range(8)]  # Wyliczenie H^i dla i-tego bloku
        h_seq.append(new_h)  # Dodanie go (H^i) do ciągu H

    return h_seq[N][0] + h_seq[N][1] + h_seq[N][2] + h_seq[N][3] + h_seq[N][4] + h_seq[N][5]


def sha384(msg):
    """
    Funkcja realizująca w całości funkcję SHA.
    :param msg: Wiadomość (w bitach)
    :return: Skrót wiadomości msg
    """
    pad_msg = pad_1024(msg)
    return sha384_algorithm(pad_msg)