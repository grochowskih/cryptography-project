import re


def pad_1024(msg):
    """
    Funkcja dokonująca uzupełnienia wiadomości do długości będącej wielokrotnością 1024 bitów.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
    :param msg: Wiadomość, która ma zostać uzupełniona (w bitach)
    :return: Uzupełniona wiadomość msg
    """
    if re.match("^[01]+$", msg) is None:
        raise Exception("Błędna wiadomość do obliczenia skrótu!")

    length_msg = len(msg)
    length_msg_moduli = length_msg % 1024

    k = (896 - 1 - length_msg_moduli) % 1024 # Rozwiązanie liniowej kongruencji występującej w paddingu

    length_bin = '{0:0128b}'.format(length_msg) # Długość wiadomości zapisana za pomocą bitów długości 128

    return msg + "1" + ("0" * k) + length_bin


def sha384(msg):
    """
    Funkcja obliczająca skrót wiadomość msg.
    Na podstawie: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
    :param msg: Uzupełniona wiadomość, dla której obliczamy skrót (w bitach)
    :return: Skrót wiadomości msg
    """