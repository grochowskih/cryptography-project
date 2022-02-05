import generators.generator
import DSA.dsa
import random
import TDES.OFB

if __name__ == "__main__":
    used_ks = []
    while True:
        print("----- 3DES OFB + DSA-SHA-384 -----")
        print("A. Wygeneruj podpis cyfrowy \nB. Zweryfikuj podpis cyfrowy \nC. Zaszyfruj wiadomość \nD. Odszyfruj wiadomość ")
        action = input("Podaj opcję: ")
        if action == "A":
            choice = input(
                "Czy chcesz podać własne parametry do algorytmu DSA, czy chcesz, aby zostałe wylosowane? Wciśnij A, jeśli własne, B, jeśli przykładowe, cokolwiek innego, jeśli losowe: ")
            if choice == "A":
                print("Parametry podawaj jako liczby całkowite.")
                try:
                    N = int(input("Podaj parametr N: "))
                    L = int(input("Podaj parametr L: "))
                    p = int(input("Podaj parametr p: "))
                    q = int(input("Podaj parametr q: "))
                    g = int(input("Podaj parametr g: "))
                    x = int(input("Podaj parametr x: "))
                    k = int(input("Podaj parametr k: "))
                except:
                    print("Błędny format wejścia.")
            elif choice == "B":
                print("Domyślne parametry to L = 1024, N = 160 (dopuszczalne przez NIST)")
                L = 1024
                N = 160
                p = int("86F5CA03DCFEB225063FF830A0C769B9DD9D6153AD91D7CE27F787C43278B447E6533B86B18BED6E8A48B784A14C252C5BE0DBF60B86D6385BD2F12FB763ED8873ABFD3F5BA2E0A8C0A59082EAC056935E529DAF7C610467899C77ADEDFC846C881870B7B19B2B58F9BE0521A17002E3BDD6B86685EE90B3D9A1B02B782B1779", 16)
                q = int("996F967F6C8E388D9E28D01E205FBA957A5698B1", 16)
                g = int("07B0F92546150B62514BB771E2A0C0CE387F03BDA6C56B505209FF25FD3C133D89BBCD97E904E09114D9A7DEFDEADFC9078EA544D2E401AEECC40BB9FBBF78FD87995A10A1C27CB7789B594BA7EFB5C4326A9FE59A070E136DB77175464ADCA417BE5DCE2F40D10A46A3A3943F26AB7FD9C0398FF8C76EE0A56826A8A88F1DBD", 16)
                x = int("411602CB19A6CCC34494D79D98EF1E7ED5AF25F7", 16)
                k = int("95897CD7BBB944AA932DBC579C1C09EB6FCFC595", 16)
            else:
                print("Domyślne parametry to L = 1024, N = 160 (dopuszczalne przez NIST)")
                L = 1024
                N = 160
                p = int("86F5CA03DCFEB225063FF830A0C769B9DD9D6153AD91D7CE27F787C43278B447E6533B86B18BED6E8A48B784A14C252C5BE0DBF60B86D6385BD2F12FB763ED8873ABFD3F5BA2E0A8C0A59082EAC056935E529DAF7C610467899C77ADEDFC846C881870B7B19B2B58F9BE0521A17002E3BDD6B86685EE90B3D9A1B02B782B1779",16)
                q = int("996F967F6C8E388D9E28D01E205FBA957A5698B1", 16)
                g = generators.generator.group_generator(p, q)
                x = random.randrange(1, q)
                k = random.randrange(1, q) # Generowanie parametrów x,k wymagałoby zapoznawania się z kolejnymi standardami
            print("Wybrane parametry to: ")
            y = pow(g, x, p)
            print("L = ", L,"\nN = ", N,"\np = ", p,"\nq = ", q,"\ng = ", g,"\nx = ", x,"\nk = ", k,"\ny = ", y)
            msg_text = input("Podaj wiadomość (tekst), dla której chcesz obliczyć podpis cyfrowy: ")
            msg_bin = bin(int(msg_text.encode("utf-8").hex(), 16))[2:] # Wiadomość binarnie, bo tak przyjmuje nasze DSA
            try:
                sign = DSA.dsa.generate_dsa(N, L, p, q, g, x, k, msg_bin, used_ks)
                print("Wygenerowany podpis to: ", sign)
            except Exception as ex:
                print("Przechwycono wyjątek!")
                print(ex)
        elif action == "B":
            print("Podaj parametry do weryfikacji podpisu (jako liczby całkowite)")
            try:
                N = int(input("Podaj parametr N: "))
                L = int(input("Podaj parametr L: "))
                p = int(input("Podaj parametr p: "))
                q = int(input("Podaj parametr q: "))
                g = int(input("Podaj parametr g: "))
                y = int(input("Podaj parametr y: "))
                r = int(input("Podaj parametr r (pierwsza pozycja podpisu): "))
                s = int(input("Podaj parametr s (druga pozycja podpisu): "))
            except:
                print("Błędny format podano!")
            msg_text = input("Podaj wiadomość (tekst), dla której chcesz zweryfikować podpis cyfrowy: ")
            msg_bin = bin(int(msg_text.encode("utf-8").hex(), 16))[2:]  # Wiadomość binarnie, bo tak przyjmuje nasze DSA
            try:
                correct = DSA.dsa.verify_dsa(N, L, p, q, g, y, [r,s], msg_bin)
                print("Czy podpis jest poprawny? ", correct)
            except:
                print("Przechwyciłem wyjątek!")
        elif action == "C":
            plaintext = input("Podaj tekst, który chcesz zaszyfrować: ")
            choice1 = input("Jeśli chcesz sam podać klucze i wektor inicjalizujący, wciśnij 1. Jeśli nie, wciśnij "
                            "cokolwiek innggo: ")
            if choice1 == '1':
                Iv = input("Podaj wektor inicjalizujący: ")
                while len(TDES.OFB.hex_to_binary(Iv.encode("utf-8").hex())) != 64:
                    Iv = input("Zła długość wektora inicjalizującego. Podaj nowy wektor inicjalizujący: ")
                print("Wybierz opcję kluczy. \n 1. Wszystkie klucze są różne i od siebie niezależne. "
                      "\n 2. Klucz pierwszy i klucz drugi są od siebie niezależne oraz klucz pierwszy jest taki sam jak klucz"
                      "trzeci. \n 3. Wszystkie klucze są takie same (TDES trywializuje się do DES)")
                choice = input("Wybierz 1, 2 lub 3: ")
                if choice == "1":
                    key1 = input("Podaj pierwszy klucz: ")
                    key2 = input("Podaj drugi klucz: ")
                    key3 = input("Podaj trzeci klucz: ")

                    while key1 == key2 or key1 == key3 or key2 == key3:
                        print("Klucze się powtarzają. Wybierz nowe klucze.")
                        key1 = input("Podaj pierwszy klucz: ")
                        key2 = input("Podaj drugi klucz: ")
                        key3 = input("Podaj trzeci klucz: ")

                    while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64 or \
                          len(TDES.OFB.hex_to_binary(key2.encode("utf-8").hex())) != 64 or \
                          len(TDES.OFB.hex_to_binary(key3.encode("utf-8").hex())) != 64:
                        print("Długość kluczy jest zła.")
                        key1 = input("Podaj pierwszy klucz: ")
                        key2 = input("Podaj drugi klucz: ")
                        key3 = input("Podaj trzeci klucz: ")

                elif choice == "2":
                    key1 = input("Podaj pierwszy klucz: ")
                    key2 = input("Podaj drugi klucz: ")

                    while key1 == key2:
                        print("Klucze się powtarzają. Wybierz nowe klucze.")
                        key1 = input("Podaj pierwszy klucz: ")
                        key2 = input("Podaj drugi klucz: ")

                    while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64 or \
                          len(TDES.OFB.hex_to_binary(key2.encode("utf-8").hex())) != 64:
                        print("Długość kluczy jest zła.")
                        key1 = input("Podaj pierwszy klucz: ")
                        key2 = input("Podaj drugi klucz: ")
                    key3 = key1

                elif choice == "3":
                    key1 = input("Podaj klucz: ")

                    while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64:
                        key1 = input("Zła długość klucza. Podaj nowy klucz: ")
                    key2 = key1
                    key3 = key1
                key1 = key1.encode("utf-8").hex()
                key2 = key2.encode("utf-8").hex()
                key3 = key3.encode("utf-8").hex()
                Iv = Iv.encode("utf-8").hex()
                plaintext = plaintext.encode("utf-8").hex()
                print("Oto Twoja zaszyfrowana wiadomość: ", TDES.OFB.ofb_encrypt(plaintext,key1,key2,key3,Iv))

            else:
                key1 = TDES.OFB.generate_iv()
                key2 = TDES.OFB.generate_iv()
                key3 = TDES.OFB.generate_iv()
                Iv = TDES.OFB.generate_iv()
                plaintext = plaintext.encode("utf-8").hex()
                print("Oto Twoja zaszyfrowana wiadomość: ", TDES.OFB.ofb_encrypt(plaintext, key1, key2, key3, Iv))

        elif action == "D":
            ciphertext = input("Podaj tekst, który chcesz odszyfrować: ")
            choice2 = input("Jeśli twój tekst jest już w systemie szesnastkowym, wciśnij 1. Jeśli nie, wciśnij "
                            "cokolwiek innego: ")
            choice1 = input("Jeśli chcesz sam podać klucze i wektor inicjalizujący, wciśnij 1. Jeśli nie, wciśnij "
                            "cokolwiek innggo: ")
            if choice1 == '1':
                Iv = input("Podaj wektor inicjalizujący 64-bitowy: ")
                while len(TDES.OFB.hex_to_binary(Iv.encode("utf-8").hex())) != 64:
                    Iv = input("Zła długość wektora inicjalizującego. Podaj nowy wektor inicjalizujący: ")
                print("Wybierz opcję kluczy. Niezależnie od wyboru, klucze muszą być 64-bitowe."
                      " \n 1. Wszystkie klucze są różne i od siebie niezależne. "
                      "\n 2. Klucz pierwszy i klucz drugi są od siebie niezależne oraz klucz pierwszy jest taki sam "
                      "jak klucz trzeci. \n 3. Wszystkie klucze są takie same (TDES trywializuje się do DES)")
                choice = input("Wybierz 1, 2 lub 3: ")
                if choice == "1":
                    key1 = input("Podaj pierwszy klucz: ")
                    key2 = input("Podaj drugi klucz: ")
                    key3 = input("Podaj trzeci klucz: ")

                    while key1 == key2 or key1 == key3 or key2 == key3:
                        print("Klucze się powtarzają. Wybierz nowe klucze.")
                        key1 = input("Podaj pierwszy klucz: ")
                        key2 = input("Podaj drugi klucz: ")
                        key3 = input("Podaj trzeci klucz: ")

                    while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64 or \
                            len(TDES.OFB.hex_to_binary(key2.encode("utf-8").hex())) != 64 or \
                            len(TDES.OFB.hex_to_binary(key3.encode("utf-8").hex())) != 64:
                        print("Długość kluczy jest zła.")
                        key1 = input("Podaj pierwszy klucz: ")
                        key2 = input("Podaj drugi klucz: ")
                        key3 = input("Podaj trzeci klucz: ")

                elif choice == "2":
                    key1 = input("Podaj pierwszy klucz: ")
                    key2 = input("Podaj drugi klucz: ")

                    while key1 == key2:
                        print("Klucze się powtarzają. Wybierz nowe klucze.")
                        key1 = input("Podaj pierwszy klucz: ")
                        key2 = input("Podaj drugi klucz: ")

                    while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64 or \
                            len(TDES.OFB.hex_to_binary(key2.encode("utf-8").hex())) != 64:
                        print("Długość kluczy jest zła.")
                        key1 = input("Podaj pierwszy klucz: ")
                        key2 = input("Podaj drugi klucz: ")
                    key3 = key1

                elif choice == "3":
                    key1 = input("Podaj klucz: ")

                    while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64:
                        key1 = input("Zła długość klucza. Podaj nowy klucz: ")
                    key2 = key1
                    key3 = key1
                key1 = key1.encode("utf-8").hex()
                key2 = key2.encode("utf-8").hex()
                key3 = key3.encode("utf-8").hex()
                Iv = Iv.encode("utf-8").hex()
                if choice2 != '1':
                    ciphertext = ciphertext.encode("utf-8").hex()
                print("Oto Twoja odszyfrowana wiadomość: ", TDES.OFB.ofb_decrypt(ciphertext, key1, key2, key3, Iv))

            else:
                key1 = TDES.OFB.generate_iv()
                key2 = TDES.OFB.generate_iv()
                key3 = TDES.OFB.generate_iv()
                Iv = TDES.OFB.generate_iv()
                if choice2 != '1':
                    ciphertext = ciphertext.encode("utf-8").hex()
                print("Oto Twoja odszyfrowana wiadomość: ", TDES.OFB.ofb_decrypt(ciphertext, key1, key2, key3, Iv))




