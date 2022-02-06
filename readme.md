3DES OFB + DSA-SHA-384:
-

Projekt z przedmiotu *Wprowadzenie do współczesnej kryptologii* wykonany przez:
* Jakub Bezubik
* Hubert Grochowski
* Filip Tobiasz

**Uruchomienie aplikacji**


Aplikacja jest napisana w języku Python 3.10. Sprawdzana była na systemie Windows.
Aby uruchomić program należy w wierszu poleceń przenieść się do katalogu
z wypakowanym repozytorium, a następnie w konsoli podać:
> python main.py

W przypadku, gdyby aplikacja nie działała problemem mogą być ściezki - prosimy o kontakt, jakby były problemy.

**Testy**

Przykłady danych, dla których był testowany algorytm DSA są dołączone w katalogu *examples* pod nazwą *dsa-test-data.txt*.
Są to dane rekomendowane do testów przez NIST i można znaleźć je pod adresem: https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/digital-signatures. Testy dla tych danych wypadły pozytywnie.

Przykłady danych, dla których odbyły się testu szyfru TDES w trybie OFB znajdują się w katalogu *examples* pod nazwą *TDES-test-data.txt*.
Są to dane rekomendowane do testów przez NIST i można znaleźć je pod adresem: https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/TDES_OFB.pdf. Testy dla tych danych wypadły pozytywnie.

**Uwagi**

* Generator podgrupy multiplikatywnej do algorytmu DSA miał problemy sprzętowe z liczeniem dla dużych parametrów L,N. W związku z tym jest on liczony dla najmniejszych możliwych. W innych przypadkach jako "losowanie" są podane parametry p,q,g rekomendowane w danych testowych przez NIST.
* Standard NIST poza podanym algorytmem tworzenia generatora g podaje algorytmy weryfikacji, czy jest on faktycznie generatorem. Jest to już jednak bardziej skomplikowany kod. Dlatego wygenerowany generator wcale nie musi być istotnie generatorem (tak jak w standardzie NIST).

