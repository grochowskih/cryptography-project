import generators.generator
import DSA.dsa
import random

if __name__ == "__main__":
    used_ks = []
    while True:
        print("----- 3DES OFB + DSA-SHA-384 -----")
        print("A. Wygeneruj podpis cyfrowy \nB. Zweryfikuj podpis cyfrowy")
        action = input("Podaj opcję: ")
        if action == "A":
            choice = input(
                "Czy chcesz podać własne parametry do algorytmu DSA, czy chcesz, aby zostałe wylosowane? Wciśnij A, jeśli własne, cokolwiek innego, jeśli inne: ")
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
            else:
                print("Domyślne parametry to L = 1024, N = 160 (dopuszczalne przez NIST)")
                L = 1024
                N = 160 # do p,q ,x,k bedzie losowanie/generowanie, wrzucam na razie jakies przykladowe zgodnie z testowymi wektorami
                p = int("86F5CA03DCFEB225063FF830A0C769B9DD9D6153AD91D7CE27F787C43278B447E6533B86B18BED6E8A48B784A14C252C5BE0DBF60B86D6385BD2F12FB763ED8873ABFD3F5BA2E0A8C0A59082EAC056935E529DAF7C610467899C77ADEDFC846C881870B7B19B2B58F9BE0521A17002E3BDD6B86685EE90B3D9A1B02B782B1779", 16)
                q = int("996F967F6C8E388D9E28D01E205FBA957A5698B1", 16)
                #g = generators.generator.group_generator(p, q)
                g = int("07B0F92546150B62514BB771E2A0C0CE387F03BDA6C56B505209FF25FD3C133D89BBCD97E904E09114D9A7DEFDEADFC9078EA544D2E401AEECC40BB9FBBF78FD87995A10A1C27CB7789B594BA7EFB5C4326A9FE59A070E136DB77175464ADCA417BE5DCE2F40D10A46A3A3943F26AB7FD9C0398FF8C76EE0A56826A8A88F1DBD", 16)
                x = int("411602CB19A6CCC34494D79D98EF1E7ED5AF25F7", 16)
                k = int("95897CD7BBB944AA932DBC579C1C09EB6FCFC595", 16)
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






