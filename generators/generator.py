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
    k = 0
    for i in range(64):
        temp = random.randint(0, 1)
        if i not in range(7,64,8):
            key += str(temp)
            k += temp

        else:
            if k % 2 == 1:
                key += str(0)
            else:
                key += str(1)
            k = 0
    return binary_to_hex(key)

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


def generate_primes_length_dsa():
    """
    Funkcja generująca parametry p,q,N,L dla DSA.
    Opisany w NIST sposób był skomplikowany - stąd przy użyciu zewnętrznego narzędzia
    generującego zgodnie ze standardem NIST wygenerowaliśmy kilka
    przykładowych parametrów.
    :return: Parametry L,N,p,q.
    """
    lengths = random.choice(
        [[1024, 160], [2048, 224], [3072, 256]])  # są 3 z 4 możliwości, bo dla takich wygenerowaliśmy przykładowe p,q
    L, N = lengths[0], lengths[1]
    if L == 1024:
        params = random.choice([
            [
                "8a862119d2ac16be6b657d7530ecbc67658c5559f24b27dfbc9f0206310e62d65cea1bc3c9659af173ceff4b5348fde64466b77e4f5265135505fe41bbc1631a0859a867971c827b1042e94b9ef093c7cbb5bafcddecd33aef1b6ee1d15c4c78834de33950b9595d0f233ec19dd51e2a8de9da2cf2a8a0f27ce1156590fa9221"
                , "a2fb58b0bd6f9487f748cbd49ab187e661ce9f3b"],
            [
                "9d94f60918fc2b290fd6fc344f143df6aabf5f948447c45710835f4f2c2509d8f842f5850e810be4a5507db4c46f8da114ca2fd3835566789dae1c8151361d171399abf56b7027179948c6178afbfc22d34fd83a6d7c51784b4a12b969e9949300b3f4f855ae438c02755519757339ad1601a0ef2ef7538d3a638c8f61af7ec7"
                , "deb88bb278a3a9e9adc59d0bded7bb85e6ecab01"],
            [
                "e9d18b644f7807df976e4c73f44ecbb84d28b51b64c48c86afac53027aeb88d3b8b8ead8a2e089bee95a7aa27b7c29fae90b3fa9cca571afa763d55339633531c33fc7176808748d735e542c4fa7d0aaebcfe9f0bda5d0b5bdeb1b4bb6e8a8bb7aff9365118a05fbb4745693cff1baaf3a092772df334793a462e09bfa0d5fed"
                , "bd6f324139ddc81a8ee92513d3d989fbccbf0641"],
            [
                "f6e9cfcf22c71aea911fd23e20f1be3ba439fc434f647f25a5869106800004c8de6ad4797f5c9d754486503ee9c396ec2b257cfb3561561b4ddf0a8aa869fdeb270b41819c284f264b8a6daa4bc0b45f39ea3899a67c070dc7dec5aeee77df01886e0d6171fa6123f4eef31731c442abb7444dfcbe0bb0a5fc9df7e661a3562d"
                , "c82c9d4fe0974876454a56fc6b5705d6741011e5"],
            [
                "d59811831da86d9de1a996d15c3afeed475a045cfd8e2ac36a46ed32b6ed182b6108372e2e891321a133624121844c29b042aa7c12d4b39f1051054404f3873b90164a78bd4e0b55f6b1d1d5ecfae99e8e0ebd9e2a94160400d32e06b5cdbe57745b72cc61765e6f76dfef00c7dff59a5d47fb038ea092268404304648051605"
                , "b3aaae4461a4c2da7899d6adb601cbb530d1e3ab"],
            [
                "9db66c38b6a3d02bd6c0ad50e4b47f50a39fb184cbc9bf6bc984767c9ecbda1e3f8932aa737c9c2cda80ebe1eaedab2a9b8de8a83a5a191db8590d0865b26e62a6dd7cba680e6dc18cc64c602bb1dca080a36e887b4946f69de6e5f2e23c5f07e817dbed38843db9b8f828d062f301e3e2cc6f3458c92dd0f45b108eaa0766e1"
                , "bc26ce363ec3008ff2a2a3bf3022363201707fef"],
            [
                "8fb5351275c2d48b3540fa428f31c0b32d143dec39e4d492c75b46f4e3c113ec0642ad9996838f7ba77ae222df04bc2edff3e61f994978640e21e161c0157bbe0ebad42daaac9519ee2e033a667dd5ae34aec3454b16f2c53e260dde4b934e1453a95464907cf395ce03b91d9ec79a46d173f5bf1cb45e84335b0f49091fa301"
                , "b51fb03fadea981f06e633a2267df0ef0dc3dd15"],
            [
                "eeb7d63dd31b598dc34ab480a2a073c1930cae48857de576fc86b67969e161ce869d1bf0f774c45b249ed02202f98872a5faf0801e08c2f4bdbe5a153f124db1d6f702f9ea461debc6953a23b0cb24d1302d70b6c0cc819724fa93c05b32a7a2fa216d5f833600fcf3eb957e78945bedf6fcfee18d3d40d460ed4edbfc8f4543"
                , "ec237d2372d18b007ca01c2b90baed11da699a0f"],
            [
                "879fe55a19c92f04b599d0f0c0907443c00d3222944e48d9830f9bec18c909c52ed59cae246958d9999b66e4a8e97f563c68f8eab2e52da3d55b1b1334c19298bb92aa5bfee6dbcba6d09ad3311e3608b0bbbb1196e6f889ea55f7cd1d0efdc73465a2de813933a30e4da5041f13e3660bc295659671b534fcb53246da792d1b"
                , "ad5885ea3d86cad5034261a9bca58b5edf67ae3f"],
            [
                "959c5224ea0bbfd2df200f27b7c9e6a5ceba98ab29d6f401e8ed0db823747b269031e3cc488f510c065cf50b91881539744f641f9bfbdba4e90949c44f9bffac863294c94c152d1dce545725d103392099b21dc6ef8164ad74a0c563e7cc221902db77dc0f1f4f6fdb54c1eebf337a43facdf1c86b3db94ae5d0a355174b787b"
                , "8eec8c2f33893fab90d1e8f1d4219db3a86a7335"]])
    elif L == 2048:
        params = random.choice([
            [
                "dc4fd54a143041422830cd20053b7cb57a7e68e13aed505ac9448c0cf721266b992c610d6696fd0bb63e6278ccbac4248b1e158525abfdfa78e8fe7d32dfc1b2bdb6f1ddbd11ad7c11a9285149f57073eb91143ad04887a7da88e3309b1ec49c6c0527786ee0e74e37a4891b7e429252a2ba8c5e5bec51689d94094ff3120801ee48f25a75a4013a3416554eba5b9f7df2f1006267da8a0a348a7f73a755d8f489b9bdba842a6c7fd736396ea941a65418f8ed6f2cd32df017a1381415e6d62851038587b82612dfcd41009e9054b26a551ddb7e232ef6776a1d71bddb54d4734773e6919e9ad6f25e7b2fe1c905c4b05e70bda7301d9394f03c1d4d43303c93"
                , "d7cab9e5f2d668086402752b85c849a9e34a46cf73ae843ea48fd0db"],
            [
                "c2ef76007b314abd2830a1da3d2caf23bdf9d7fa400944790c4bc0c5b6fe60576a4c96d9ea9db10148c6075ed30c628742818b0f748c2791c4d0fd5bb2f036e3d69771913b35fb7a45577bfa4eefbd34432cd3754b6cbe7f4c8368a5f61e98d411b4640184add837a4729e4cab255316861fbd6cc7c76c2f75b79cdd6784dce4bf7d58ba5826d92fb8b7a718133c0b98b22fab02b6570a3e4f8e764ebd5843d536a8293cfb730a870eba576900a12464c8cbb1740c038f7ce0d751d8792ddd454677026d012fb48460ee5e1b73801b7082ffc5af450824bad432a5abddc7d9120d8e0ebc9b5d0cbe2d38b09ca186a8ad6f53d2d3c47bc08805e0a7494af8541d"
                , "c6738147c5418678441e39a86078ec03e1685fd190a19d36173e02b5"],
            [
                "bc7bcac8046136803cbe158e12dc3a2c6ae9c40e2f57756315ee3ef111805f94227b8ea8ac7c2dcd24a1ad7e2aa76715da202832656a97918632f873e2158bf1f46d349df03d3972024b16bbc344700ea35f1e368bd18b9aff3b9623b6efb5fc4846288741e10e77f06c91bdac5494f72a03e9599395dd9a76521497c73384ffd9b1798b265f79ff12e71eadaf4be1520a70588c78899f0157bdf4c78601b68f7dfab72f261fb4ca14b7c45595440310d3191e0c9df3eb7f0e463a8dbb051ff202230878fdbead6b1c37003f0c4b20186a75cd50518d5a0ba50b36bbae728cb0c6b000a6493d09b4d02b2ea6121771e2b5dd4625f59019f50d165c976d9c40c3"
                , "911ca153a0bc18adaee7b37cdbd03457b860449fe1087e21b222fa9d"],
            [
                "f820b3baa75467f0f2d05d3288620ff5745efaeecec603ba1deca7e4c5502d87c50ebd83a67156b30dead1a5437fb431e69d32eb8e6cfff0ea2f135b59efc3aebb9abcf2a1a5d754c933b18da80976055f5792fc4b0252bd2d274213ca83ebb25c87ada1db86188fab6e3d0dc142d506da3beb5e436477f8cbe89a975b4ae2e6b2199dbc49a8d6d366ed032551382f9865c6114dcd0cb5b3a7dab5aff598e1fa2007b11991bac43272b18894e5da9985fed4e5158d69b83fc2c4265c5cb87c1b5aa5ca7d5cd1edac74c71c01c45c51bdf872a08a5b88e2e79c263491abc0ce2212adedefb79fdf884d37fe8435b55fcc3befec34f6fb16324df38334ff80de8b"
                , "b3595e5f9a4ffc28e021c613e588a54dcef8eaf223060a89ec7775cb"],
            [
                "980954302ad46047669243be2ae5e439f95fed9f7ca447b2afb7a96032fd7466bb18b6400e26c3ebaa8ed7b609ad2ba63e5f4d9cb46bf47c459a1d3f002ac6b82b22b577a341215d79b435cc75973ed89f19345c3bdfb4dcf01d62712665ad42c642b848671c563f84d2f65c699b51621ebdbfcfd49446662d1cbdcf343f428ea09aa916b6dd43e6460b10107791f6654d50084731960c0b71cd59142353833606067dd52f88909fee0662109ba96593db2a1385408633cc6f010bfd2511e25d143816cec60654fd784df7e3ed0d08abe0534951c43b1f0d56457efea9601da8faed3d21714a26e02225043d7b109846d866fe32ef2a06c0502f5365a76a106b"
                , "89430062dadc0197a7f75cf64b15fa12fca6ee8d6039f39eaab25205"],
            [
                "ddd86a08dc1e030c184b681f67af66509c3350af3eb80cbdd4cb38dc0cc096cfa136f9d78583c125e5cf8d030158b50f3a89f34bb4e8e7de236b7d3003e1d433087bd50e6ed78feff5cf0c85de9cd724d6bd2ea108e508d881b55164237cc5c0c0db54c300c5d78058ac4c686853fbee7071ec529202d5ff745dd4e22acc12c87cefd7fa91eff2c973cf3812750f8309f9afb7816ea0576952085aa89b2cc4d1cd363473a524c7bf0b5c09e28b632472540c0e73ee74174cdd69397f57f87981eee22a7a6c70bb4b5bc641356fa30cd856d8d9e5084e331778afc8ce7cf3e69611c8182234736e45a8c19640d5f4ab99a65ddec9762a1602c9f1c9e64c367f91"
                , "f53065884dd46b1b7c272f0a2d552d2fb712124c91760c1d1c7cac45"],
            [
                "8b918b31513df17cab6184622ca59e8b0ec4594dfe51244074b2233a9f8070668ff9fbb62897ca674adfb8988af5d4af2139ea477b0191b2bfeda15c34334f517a186bc631805c59d1de7eb38711436bbd7acf1a21915792ac6837dadb4e47763d934bd9e2f02394e5d1dfc2236ccbe0ce829602c2249476ef2762c723978dab553d31e250dbd28251c321c5833f04038b19f19f30864df14af2510eaed5edbce16883fe949e5895ccc23236ea6c664f832c6b3c6c2b46b6be7d69a27bb2454f7f9ca2bbe86ae7117b9e60a2025e54784f359fc285e45b85b0c29b536b2f1e7c61940832d0deaa4ab43ec286a6e53ffb914e012530f41a0e03ee0b219d7cfd6f"
                , "f7195afac9eba56f2732c65efdf2457f5b7ed0b54a33c0988acabbe7"],
            [
                "9a8320390927a1046f10eda662bf66637082a531846efbbbe3f9cbe1b4ae5424d3aad2867ba2b4a947b062bdc9b4af5c3f38535cf5cc82d345106b8e87e4cb7152ef59bb6b8a533fd65ceba8e4935360e7761ff09d151d34369df8f9af38c472748c766a802a75aa046ee1b9482337c65e7635dd6ed2300370794ccbee485add937f413617dc01eab34d387a2d2dbd62bb5cdb42a7730eb8120d0652b32bf2961ce2b5527b472ca8817ddebd35180261abbfb28384863f650aad579ef4de160c9d8d6e10c1f3bc4db6498afc00d5649e3025dae435627b46ade99a36fdba8392b5dc09d1fdd6e0153b81f45cf2461c1598b54e82c2dd56cbaa57794d84138231"
                , "bc9d0fc6618e13e5197b2e2feae89078f523d38ff5535ec841c36295"],
            [
                "ce562d963b38f9e9e2e55d060d24dae4049d788787bbda9223d22eb173744a578959d9c70f496b354b0e1afc3f771ea542d7c8814043dbd4d5c2ad869b8280d80f7cd124adbd64556cd4bfcd53784882fcf8507ab4c14444670d6c3926a52128df35db751b18a7736dcdb9ec32e1aa9f24d20dafa4921184e7dc04e8c73722c24773bdd730b6b2baeb23d28b0cea97efd222d22f8363f489bb478553d0a998198d4a9c52d2257ed76b1d2c18167e54cbff2c2db212319cb196ee4a18410eddaeea11d3b8a7c493bd5c4144aca4d7de6f6c9170bd32fe6c7ed779b09c966e1a027e0e8c19b0b5d0db088e7d2329f98505c732a6097b3383b595ab9221eb1e8fb3"
                , "e5fdca85cd979ba38165af7e94c3d456b78e3b7242f159122bf3038b"],
            [
                "f5c7c694586c16a6cb51df763280c98c64c9b725c65756de05aaf5ede064a5b0853f266096075d692322ab5d3ba7b60dbbf70ee3e4a379810e5f5d2847866566b56cbf905ef0e56b9517e3ea32982046373891dc111bc6b376a359ea092a4eb5c5565e759d0bf558342ed7c14ea4b253dcf2a8ed1023bc1df16f32be7654846c261f50b2a68f9f59c84c650c5cc37388b2d3d01bf8b43ebd0967c9e4df18e004917381766868368f3cfa44901d6012f0e5ad6250e5fc7560cdc93bcfa02343300eb9969c1aeb29f9655c45b8049e0f38c124fd0a8f6ef76c00ba2fe9da418c9abfcaf9456ec23bcab7dab164a93d38bea98b0191fe8434456eb3a3e38569cfe5"
                , "f94d45b55f06e1e21b6136117b119250d63a574eda0fc10b65277729"]
        ])
    else:
        params = random.choice([
            [
                "8bb21a3ab7c805c304c7e61f7fba087582a36e2c45161ebf812af1d1ee21c078fdbde31e4183ca182da4e9134488aacf0c81781f5bc012073c32edfa0237579e9d525b8185494bb9be6df9fd547e626bd7e7c3757d798958a33fbeb58712df59a26f278fad3a8e0344fe232f8b613268d617f5aa5fe35385ac90ae83b40a0d55bb786b113f378ed9660095e4e4f22161fcd73444f918f5ba4438b7a4626c34d934dc03e7d2588ee0bf0f1aa8633d04ccbf4d33a6cc5efb371deda490e6c837c15e582954e9d5d3e51e7396aecde26ab71a30200c64599091524cf16702e4b33ae3fccf1d56e45106495da073696444d3cfc9c9836d3c4323f9b12c1762b8f717991c085f029f7dfc58f641a82fdb35cf5b4333a04e50399390e15a88b3abfa012a03c1b59e9c5026dbc19cd5fb25a65148fbaa4fbf50f05d13c82173a70a414956fc7de641d711f8d5ce3ff0aaa859d232cc3e0ccfbb22ff6b7dee21497a6054410051038fe6f14ad3a0a732737fd2fc8bb0b79f97047bc0050e0624aad5b495"
                , "d9c0057381e2a1544f39e2990cb9ad798932ea49b2823f633ae253447c4f2205"],
            [
                "dba6aae4f1cfe438035c89bd96ab96354078eb1eb3d67333ea9b6b6abe100fce3a316309159a19a0a3b5ea72ba6656518f64dcd233703c401abd9197159cff0cd7c79d6555b513b89e31f1fefd58e924c1cacb73c5c3d0a1c7077097bac63b61e58a28cecd48f24a2165ec1f9e0e92364229c3667614c7c073f863f311fc79f1125571bdbc98d083d75ad7f29a21b1787e4aa8f77fa63daf6a24b747a1f01b13d6c7d0bb77150f25aa00abc8e2765f42918df6fc8473c0bb9bcb8961f472792377cddd318babf4e76118692d4d7589ad135cfbe2d3274e764c34222e4b7209787b0c54579bde316778a13401337db4be7c9e335f99d20a881d3851dda2ddbb5bb2a133ee2cbd492a2a24164d80234ae5fa98eb64fcb6a3fb84b7df3dc7192b35c4201fe0802c3807d48d6a273a7ca09b6283263e006aa9f0086109b7c9bb4c38063e049beb61e957ca03ec485de0687ce481b0e7907c75848ae8c2e3d030f0738e4283d837334ff5549471d95c5ac49dd108cb8fa6caca51349ad55703599e7b"
                , "e4c23d927d6910f5a08a4efac9a0f67046096c541dcabf109952169435beac2b"],
            [
                "a24fa64ef8e314671f9d2c4dabf526cbd6374d1f109d6487f18a14ba601c634fe7f184533cdaeadec9f89e2ab037ab1d7844317da89f83897881be785a3b9c26561bbcdf2f0966e107b9e0a7ab22002e2b14293f07d46187182f039a54004181cf9fcc26a2aa1a34952126c99e01f6fc5fbf1e133b19b830fa14b5dcbf3c3dc3ce6f820452421d7a69b782ec7d850184697d37e94c907ee561654e35396a353ddec858843fac06683433aa0773b26e43dd02fb779522d49df6c880a4ffa53317380be73d85f7be28d07cfec28258b61a3ab3ebba6f4f41d9d3309e1e20c201bbf396900811af0c7a3650ee591166ddb5b250e2018d34493100e6993bf9b6360e1e2b09e63546de9f8ab76ffd4f3ab57bcb5358bf310df8c789df1ee13c54a07a95ee0ec48d8f6a626267eda0b7a92a777fc52add4ec266b639b50776514eec01fbfb3adc363a53a92d5a008d911b506da9d50dc0d6532817f05e5768da8bf9704099d9d865aac91fb9102ca2db6af754c89b9c7bb09a640ba5e94ae96b7b6421"
                , "8b45be5f8c2ed9b745c0b1f188e7cc2f7b06baab06726a791079c4b662f3fe9f"]
        ])
    return [L, N, params[0], params[1]]
