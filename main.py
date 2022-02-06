import generators.generator
import DSA.dsa
import random
import TDES.OFB

if __name__ == "__main__":
    used_ks = []
    while True:
        print("----- TDES OFB + DSA-SHA-384 -----")
        print("A. Wygeneruj podpis cyfrowy \nB. Zweryfikuj podpis cyfrowy \nC. Zaszyfruj wiadomość \nD. Odszyfruj wiadomość ")
        action = input("Podaj opcję: ")
        if action == "A":
            choice = input(
                "Czy chcesz podać własne parametry do algorytmu DSA, czy chcesz, aby przykłady zostały wylosowane? Wciśnij A jeśli chcesz, aby wylosował: ")
            if choice == "A":
                try:
                    params = generators.generator.generate_primes_length_dsa()
                    L = params[0]
                    N = params[1]

                    if L > 3000:
                        p_hex = "a410d23ed9ad9964d3e401cb9317a25213f75712acbc5c12191abf3f1c0e723e2333b49eb1f95b0f9748d952f04a5ae358859d384403ce364aa3f58dd9769909b45048548c55872a6afbb3b15c54882f96c20df1b2df164f0bac849ca17ad2df63abd75c881922e79a5009f00b7d631622e90e7fa4e980618575e1d6bd1a72d5b6a50f4f6a68b793937c4af95fc11541759a1736577d9448b87792dff07232415512e933755e12250d466e9cc8df150727d747e51fea7964158326b1365d580cb190f4518291598221fdf36c6305c8b8a8ed05663dd7b006e945f592abbecae460f77c71b6ec649d3fd5394202ed7bbbd040f7b8fd57cb06a99be254fa25d71a3760734046c2a0db383e02397913ae67ce65870d9f6c6f67a9d00497be1d763b21937cf9cbf9a24ef97bbcaa07916f8894e5b7fb03258821ac46140965b23c5409ca49026efb2bf95bce025c4183a5f659bf6aaeef56d7933bb29697d7d541348c871fa01f869678b2e34506f6dc0a4c132b689a0ed27dc3c8d53702aa584877"
                        q_hex = "abc67417725cf28fc7640d5de43825f416ebfa80e191c42ee886303338f56045"
                        g_hex = "867d5fb72f5936d1a14ed3b60499662f3124686ef108c5b3da6663a0e86197ec2cc4c9460193a74ff16028ac9441b0c7d27c2272d483ac7cd794d598416c4ff9099a61679d417d478ce5dd974bf349a14575afe74a88b12dd5f6d1cbd3f91ddd597ed68e79eba402613130c224b94ac28714a1f1c552475a5d29cfcdd8e08a6b1d65661e28ef313514d1408f5abd3e06ebe3a7d814d1ede316bf495273ca1d574f42b482eea30db53466f454b51a175a0b89b3c05dda006e719a2e6371669080d768cc038cdfb8098e9aad9b8d83d4b759f43ac9d22b353ed88a33723550150de0361b7a376f37b45d437f71cb711f2847de671ad1059516a1d45755224a15d37b4aeada3f58c69a136daef0636fe38e3752064afe598433e80089fda24b144a462734bef8f77638845b00e59ce7fa4f1daf487a2cada11eaba72bb23e1df6b66a183edd226c440272dd9b06bec0e57f1a0822d2e00212064b6dba64562085f5a75929afa5fe509e0b78e630aaf12f91e4980c9b0d6f7e059a2ea3e23479d930"
                        p, q = int(p_hex, 16), int(q_hex, 16)
                        x = random.randrange(1, q)
                        x_hex = hex(x)[2:]
                        k = random.randrange(1, q)  # Generowanie parametrów x,k wymagałoby zapoznawania się z kolejnymi standardami
                        k_hex = hex(k)[2:]
                    elif L > 2000:
                        p_hex = "a6bb5333ce343c31c9b2c878ab91eef2fdea35c6db0e716762bfc0d436d87506e865a4d2c8cfbbd626ce8bfe64563ca5686cd8cf081490f02445b289087982495fb69976b10242d6d50fc23b4dbdb0bef78305d9a4d05d9eae65d87a893eaf397e04e39baa85a26c8ffbdef1233287b5f5b6ef6a90f27a69481a932ee47b18d5d27eb107ffb05025e646e8876b5cb567fec1dd35835d42082198531fafbe5ae280c575a1fb0e62e9b3ca37e197ad96d9dde1f33f2cec7d27deae261c83ee8e2002af7eb6e82f6a14796af037577a1032bbc709129caabd8addf870ae2d0595c8fdb37155748f0dea34b44d4f82ed58c2f5b1b8481662ac53473c693410082fbd"
                        q_hex = "8c3ee5bd9a2aaf068bd5845bd55ecf27417055307577bbc3770ec68b"
                        g_hex = "43b5a6b6d0bb962ec9766a377c32cc4124f1311188c2ecf95c0cd4a4fa097225b7618cb1276c474578d3bf564c145199c092a1b14baa929c2f3f0f36e0c2dae91eba08be30992a889f2952e0442c37af484a4ecdc3243ccfcb9e3413cf5cdd6630b09fe17efbfde14d8725493019b7b73d1f782b48ef30bec36e00e02ba336d2254fc202a69612cd9446f91d76b739ffa6d8b86052f8dc5f1145801c56241af5ba9037241bd89e6338b58e01310671c268eb5e33acb57d1f99f16440a675827d4017754d601a17ada2fbedf904554a90b01530da8c93cd14ce293cb2bd3e7937e934b79e310fe4d80c13f92f63381355bd80a1abee1a73fdfb6da24ef28002a3"
                        p, q = int(p_hex, 16), int(q_hex, 16)
                        x = random.randrange(1, q)
                        x_hex = hex(x)[2:]
                        k = random.randrange(1, q)  # Generowanie parametrów x,k wymagałoby zapoznawania się z kolejnymi standardami
                        k_hex = hex(k)[2:]
                    else:
                        p_hex = params[2]
                        q_hex = params[3]
                        p, q = int(p_hex, 16), int(q_hex, 16)
                        x = random.randrange(1, q)
                        x_hex = hex(x)[2:]
                        k = random.randrange(1, q)  # Generowanie parametrów x,k wymagałoby zapoznawania się z kolejnymi standardami
                        k_hex = hex(k)[2:]
                        g = generators.generator.group_generator(p, q)
                        g_hex = hex(g)[2:]
                    print("Propozycje parametrów (L,N jako int, reszta w szesnastkowym, pamiętać o uwadze z generatorem):")
                    print("L = ", L, "\nN = ", N, "\np = ", p_hex, "\nq = ", q_hex, "\ng = ", g_hex, "\nx = ", x_hex,
                          "\nk = ", k_hex)
                except Exception as ex:
                    print(ex)
                    print("Błędne generowanie!")
            choice_1 = input("Wybierz A, jeśli chcesz przejść do podawania parametrów. Możesz podać cokolwiek innego - użyje domyślnych wartości parametrów. Wybór: ")
            if choice_1 == "A":
                print("Parametry (Poza N, L - te jako całkowitoliczbowe) podawaj jako liczby w systemie szesnastkowym.")
                try:
                    N = int(input("Podaj parametr N: "))
                    L = int(input("Podaj parametr L: "))
                    p_hex = input("Podaj parametr p: ")
                    q_hex = input("Podaj parametr q: ")
                    g_hex = input("Podaj parametr g: ")
                    x_hex = input("Podaj parametr x: ")
                    k_hex = input("Podaj parametr k: ")
                    p, q, g, x, k = int(p_hex, 16), int(q_hex, 16), int(g_hex, 16), int(x_hex, 16), int(k_hex, 16)
                except:
                    print("Błędny format wejścia.")
            else:
                print("Domyślne parametry to L = 1024, N = 160. Na podstawie: https://www.ietf.org/rfc/rfc6979.txt.")
                L = 1024
                N = 160
                p_hex = "86F5CA03DCFEB225063FF830A0C769B9DD9D6153AD91D7CE27F787C43278B447E6533B86B18BED6E8A48B784A14C252C5BE0DBF60B86D6385BD2F12FB763ED8873ABFD3F5BA2E0A8C0A59082EAC056935E529DAF7C610467899C77ADEDFC846C881870B7B19B2B58F9BE0521A17002E3BDD6B86685EE90B3D9A1B02B782B1779"
                q_hex = "996F967F6C8E388D9E28D01E205FBA957A5698B1"
                g_hex = "07B0F92546150B62514BB771E2A0C0CE387F03BDA6C56B505209FF25FD3C133D89BBCD97E904E09114D9A7DEFDEADFC9078EA544D2E401AEECC40BB9FBBF78FD87995A10A1C27CB7789B594BA7EFB5C4326A9FE59A070E136DB77175464ADCA417BE5DCE2F40D10A46A3A3943F26AB7FD9C0398FF8C76EE0A56826A8A88F1DBD"
                x_hex = "411602CB19A6CCC34494D79D98EF1E7ED5AF25F7"
                k_hex = "95897CD7BBB944AA932DBC579C1C09EB6FCFC595"
                p, q, g, x, k = int(p_hex, 16), int(q_hex, 16), int(g_hex, 16), int(x_hex, 16), int(k_hex, 16)
            print("Wybrane parametry to (w szesnastkowym z wyjątkiem N,L): ")
            try:
                y = pow(g, x, p)
                y_hex = hex(y)[2:]
            except:
                print("Blad!")
            print("L = ", L,"\nN = ", N,"\np = ", p_hex,"\nq = ", q_hex,"\ng = ", g_hex,"\nx = ", x_hex,"\nk = ", k_hex,"\ny = ", y_hex)
            msg_text = input("Podaj wiadomość, dla której chcesz obliczyć podpis cyfrowy: ")
            is_hex = input("Czy podana wiadomość jest w systemie szesnastkowym? Wybierz 1, jak tak. Wybór: ")
            if is_hex == "1":
                try:
                    msg_bin = bin(int(msg_text, 16))[2:]
                except:
                    print("Błąd - to nie jest szesnastkowy!")
            else:
                msg_bin = bin(int(msg_text.encode("utf-8").hex(), 16))[2:] # Wiadomość binarnie, bo tak przyjmuje nasze DSA
            try:
                sign = DSA.dsa.generate_dsa(N, L, p, q, g, x, k, msg_bin, used_ks)
                print("Wygenerowany podpis to: ", sign)
                print("Wygenerowany podpis w szesnastkowym to: ", [hex(sign[0])[2:], hex(sign[1])[2:]])
            except Exception as ex:
                print("Przechwycono wyjątek!")
                print(ex)
        elif action == "B":
            print("Podaj parametry do weryfikacji podpisu. " + "Parametry (Poza N, L, r, s - te jako int) podawaj jako liczby w systemie szesnastkowym.")
            try:
                N = int(input("Podaj parametr N: "))
                L = int(input("Podaj parametr L: "))
                p_hex = input("Podaj parametr p: ")
                q_hex = input("Podaj parametr q: ")
                g_hex = input("Podaj parametr g: ")
                y_hex = input("Podaj parametr y: ")
                r = int(input("Podaj parametr r (pierwsza pozycja podpisu): "))
                s = int(input("Podaj parametr s (druga pozycja podpisu): "))
                p, q, g, y = int(p_hex, 16), int(q_hex, 16), int(g_hex, 16), int(y_hex, 16)
            except:
                print("Błędny format podano!")
            msg_text = input("Podaj wiadomość (tekst), dla której chcesz zweryfikować podpis cyfrowy: ")
            is_hex = input("Czy podana wiadomość jest w systemie szesnastkowym? Wyybierz 1, jak tak. Wybór: ")
            if is_hex == "1":
                try:
                    msg_bin = bin(int(msg_text, 16))[2:]
                except:
                    print("Błąd - to nie jest szesnastkowy!")
            else:
                msg_bin = bin(int(msg_text.encode("utf-8").hex(), 16))[2:]  # Wiadomość binarnie, bo tak przyjmuje nasze DSA
            try:
                correct = DSA.dsa.verify_dsa(N, L, p, q, g, y, [r, s], msg_bin)
                print("Czy podpis jest poprawny? ", correct)
            except Exception as ex:
                print(ex)
                print("Przechwyciłem wyjątek!")
        elif action == "C":
            plaintext = input("Podaj tekst, który chcesz zaszyfrować: ")
            choice2 = input("Jeśli twój tekst jest już w systemie szesnastkowym, wciśnij 1. Jeśli nie, wciśnij "
                            "cokolwiek innego: ")
            choice1 = input("Jeśli chcesz sam podać klucze i wektor inicjalizujący, wciśnij 1. Jeśli nie, wciśnij "
                            "cokolwiek innego: ")
            if choice1 == '1':
                choice3 = input("Jeśli twoje klucze i wektor inicjalizujący są w systemie szesnastkowym, wcisnij 1. "
                                "Jeśli nie, wciśnij cokolwiek innego: ")
                Iv = input("Podaj wektor inicjalizujący: ")
                if choice3 != '1':
                    while len(TDES.OFB.hex_to_binary(Iv.encode("utf-8").hex())) != 64:
                        Iv = input("Zła długość wektora inicjalizującego. Podaj nowy wektor inicjalizujący: ")
                else:
                    while len(TDES.OFB.hex_to_binary(Iv)) != 64:
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

                    if choice3 != '1':
                        while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64 or \
                              len(TDES.OFB.hex_to_binary(key2.encode("utf-8").hex())) != 64 or \
                              len(TDES.OFB.hex_to_binary(key3.encode("utf-8").hex())) != 64:
                            print("Długość kluczy jest zła.")
                            key1 = input("Podaj pierwszy klucz: ")
                            key2 = input("Podaj drugi klucz: ")
                            key3 = input("Podaj trzeci klucz: ")
                    else:
                        while len(TDES.OFB.hex_to_binary(key1)) != 64 or \
                              len(TDES.OFB.hex_to_binary(key2)) != 64 or \
                              len(TDES.OFB.hex_to_binary(key3)) != 64:
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
                    if choice3 != '1':
                        while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64 or \
                              len(TDES.OFB.hex_to_binary(key2.encode("utf-8").hex())) != 64:
                            print("Długość kluczy jest zła.")
                            key1 = input("Podaj pierwszy klucz: ")
                            key2 = input("Podaj drugi klucz: ")
                    else:
                        while len(TDES.OFB.hex_to_binary(key1)) != 64 or \
                              len(TDES.OFB.hex_to_binary(key2)) != 64:
                            print("Długość kluczy jest zła.")
                            key1 = input("Podaj pierwszy klucz: ")
                            key2 = input("Podaj drugi klucz: ")
                    key3 = key1

                elif choice == "3":
                    key1 = input("Podaj klucz: ")
                    if choice3 != '1':
                        while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64:
                            key1 = input("Zła długość klucza. Podaj nowy klucz: ")
                    else:
                        while len(TDES.OFB.hex_to_binary(key1)) != 64:
                            key1 = input("Zła długość klucza. Podaj nowy klucz: ")
                    key2 = key1
                    key3 = key1
                if choice3 != '1':
                    key1 = key1.encode("utf-8").hex()
                    key2 = key2.encode("utf-8").hex()
                    key3 = key3.encode("utf-8").hex()
                    Iv = Iv.encode("utf-8").hex()
                if choice2 != '1':
                    plaintext = plaintext.encode("utf-8").hex()
                print("Oto Twoja zaszyfrowana wiadomość (w systemie szesnastkowym): ", TDES.OFB.ofb_encrypt(plaintext,key1,key2,key3,Iv))

            else:
                key1 = generators.generator.generate_key()
                key2 = generators.generator.generate_key()
                key3 = generators.generator.generate_key()
                Iv = generators.generator.generate_iv()
                if choice2 != '1':
                    plaintext = plaintext.encode("utf-8").hex()
                print("Twój Iv, pierwszy klucz, drugi klucz, trzeci klucz: ", Iv, key1, key2, key3)
                print("Oto Twoja zaszyfrowana wiadomość (w systemie szesnastkowym): ", TDES.OFB.ofb_encrypt(plaintext, key1, key2, key3, Iv))

        elif action == "D":
            ciphertext = input("Podaj tekst, który chcesz odszyfrować: ")
            choice2 = input("Jeśli twój tekst jest już w systemie szesnastkowym, wciśnij 1. Jeśli nie, wciśnij "
                            "cokolwiek innego: ")
            choice1 = input("Jeśli chcesz sam podać klucze i wektor inicjalizujący, wciśnij 1. Jeśli nie, wciśnij "
                            "cokolwiek innggo: ")
            if choice1 == '1':
                choice3 = input("Jeśli twoje klucze i wektor inicjalizujący są w systemie szesnastkowym, wcisnij 1. "
                                "Jeśli nie, wciśnij cokolwiek innego: ")
                Iv = input("Podaj wektor inicjalizujący 64-bitowy: ")
                if choice3 != '1':
                    while len(TDES.OFB.hex_to_binary(Iv.encode("utf-8").hex())) != 64:
                        Iv = input("Zła długość wektora inicjalizującego. Podaj nowy wektor inicjalizujący: ")
                else:
                    while len(TDES.OFB.hex_to_binary(Iv)) != 64:
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

                    if choice3 != '1':
                        while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64 or \
                              len(TDES.OFB.hex_to_binary(key2.encode("utf-8").hex())) != 64 or \
                              len(TDES.OFB.hex_to_binary(key3.encode("utf-8").hex())) != 64:
                            print("Długość kluczy jest zła.")
                            key1 = input("Podaj pierwszy klucz: ")
                            key2 = input("Podaj drugi klucz: ")
                            key3 = input("Podaj trzeci klucz: ")
                    else:
                        while len(TDES.OFB.hex_to_binary(key1)) != 64 or \
                              len(TDES.OFB.hex_to_binary(key2)) != 64 or \
                              len(TDES.OFB.hex_to_binary(key3)) != 64:
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

                    if choice3 != '1':
                        while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64 or \
                                len(TDES.OFB.hex_to_binary(key2.encode("utf-8").hex())) != 64:
                            print("Długość kluczy jest zła.")
                            key1 = input("Podaj pierwszy klucz: ")
                            key2 = input("Podaj drugi klucz: ")
                    else:
                        while len(TDES.OFB.hex_to_binary(key1)) != 64 or \
                                len(TDES.OFB.hex_to_binary(key2)) != 64:
                            print("Długość kluczy jest zła.")
                            key1 = input("Podaj pierwszy klucz: ")
                            key2 = input("Podaj drugi klucz: ")
                    key3 = key1

                elif choice == "3":
                    key1 = input("Podaj klucz: ")

                    if choice3 != '1':
                        while len(TDES.OFB.hex_to_binary(key1.encode("utf-8").hex())) != 64:
                            key1 = input("Zła długość klucza. Podaj nowy klucz: ")
                    else:
                        while len(TDES.OFB.hex_to_binary(key1)) != 64:
                            key1 = input("Zła długość klucza. Podaj nowy klucz: ")
                    key2 = key1
                    key3 = key1

                if choice3 != '1':
                    key1 = key1.encode("utf-8").hex()
                    key2 = key2.encode("utf-8").hex()
                    key3 = key3.encode("utf-8").hex()
                    Iv = Iv.encode("utf-8").hex()
                if choice2 != '1':
                    ciphertext = ciphertext.encode("utf-8").hex()
                print("Oto Twoja odszyfrowana wiadomość (w systemie szesnastkowym): ", TDES.OFB.ofb_decrypt(ciphertext, key1, key2, key3, Iv))

            else:
                key1 = generators.generator.generate_key()
                key2 = generators.generator.generate_key()
                key3 = generators.generator.generate_key()
                Iv = generators.generator.generate_iv()
                if choice2 != '1':
                    ciphertext = ciphertext.encode("utf-8").hex()
                print("Twój Iv, pierwszy klucz, drugi klucz, trzeci klucz: ", Iv, key1, key2, key3)
                print("Oto Twoja odszyfrowana wiadomość (w systemie szesnastkowym): ", TDES.OFB.ofb_decrypt(ciphertext, key1, key2, key3, Iv))
