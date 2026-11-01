"""Cinquième, Puissances, division et nombres premiers: the first chapter of the Senegal Cinquième course, written in French.

The contents follow lesson 1 "Nombres premiers" of the Côte d'Ivoire Cinquième programme (powers of a natural number, the Euclidean division and the bracketing between two
consecutive multiples, prime numbers, and the decomposition into prime factors), which was read for this chapter. Every explanation, example and exercise was written independently,
with our own numbers. Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .kit import N, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-5e-premiers"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")


def pw(base, exponent):
    """Write a power as math, with braces around the exponent."""
    return f"{base}^{{{exponent}}}"


def is_prime(n):
    """Return True when n is a prime number."""
    return n > 1 and all(n % k for k in range(2, int(n**0.5) + 1))


def prime_factors(n):
    """Return the prime factors of n, with repeats, in increasing order."""
    out, k = [], 2
    while n > 1:
        while n % k == 0:
            out.append(k)
            n //= k
        k += 1
    return out


def factor_text(n):
    """Write the decomposition of n as a product of prime factors, with powers."""
    parts = []
    for p in sorted(set(prime_factors(n))):
        count = prime_factors(n).count(p)
        parts.append(f"{p}" if count == 1 else pw(p, count))
    return " \\times ".join(parts)


# ----- Section 1: powers -----
S1 = Section(
    "puissances", "Les puissances d'un nombre entier", 22, "puissances",
    "Comprendre ce qu'est une puissance, calculer une puissance, utiliser les égalités sur les produits de puissances et la priorité de la puissance dans un calcul.",
    [
        para("Une coopérative scolaire range des œufs : 20 cartons, qui contiennent chacun 20 plaquettes, qui contiennent chacune 20 œufs. Pour compter, on multiplie " + N("20 \\times 20 \\times 20") + ". "
             "Quand on multiplie plusieurs fois le même nombre, on utilise une écriture courte : une puissance."),
        definition("Puissance d'un nombre",
                   "Pour un nombre entier naturel " + N("a") + " et un entier " + N("n") + " au moins égal à 1, la puissance " + N("a^n") + " est le produit de n facteurs égaux à a : " + N("a^n = a \\times a \\times \\dots \\times a") + ". "
                   "On lit « a puissance n ». Le nombre n s'appelle l'exposant. On a " + N("a^1 = a") + ". " + N("a^2") + " s'appelle « a au carré » et " + N("a^3") + " « a au cube »."),
        rule("Deux égalités à connaître",
             "Pour multiplier deux puissances d'un même nombre, on additionne les exposants : " + N("a^n \\times a^m = a^{n + m}") + ". Pour une puissance d'un produit, on met chaque facteur à la puissance : "
             + N("(a \\times b)^n = a^n \\times b^n") + "."),
        rule("Priorité de la puissance",
             "Dans une suite d'opérations sans parenthèses, on calcule d'abord les puissances, puis les multiplications et les divisions, puis les additions et les soustractions."),
        example("Exemple 1", "Calculer " + N("2^5") + ".",
                "On multiplie 5 facteurs égaux à 2, en avançant pas à pas.",
                [(N("2 \\times 2") + " = " + N("4"), "Deux facteurs."),
                 (N("4 \\times 2") + " = " + N("8") + " puis " + N("8 \\times 2") + " = " + N("16"), "Quatre facteurs."),
                 (N("16 \\times 2") + " = " + N("32"), "Cinq facteurs : c'est 2 puissance 5.")],
                N("2^5 = 32") + ".", "2**5==32"),
        example("Exemple 2", "Écrire " + N("3^2 \\times 3^4") + " sous la forme d'une seule puissance, puis la calculer.",
                "Les deux puissances ont la même base 3 : on additionne les exposants.",
                [(N("3^2 \\times 3^4 = 3^{2 + 4}") + " = " + N("3^6"), "2 + 4 = 6."),
                 (N("3^6") + " = " + N("729"), "3² = 9, 3³ = 27, 3⁴ = 81, 3⁵ = 243, 3⁶ = 729.")],
                N("3^6 = 729") + ".", "3**2*3**4==3**6==729"),
        example("Exemple 3", "Calculer " + N("(2 \\times 5)^3") + " de deux façons.",
                "On peut calculer le produit d'abord, ou mettre chaque facteur au cube.",
                [(N("(2 \\times 5)^3 = 10^3") + " = " + N("1000"), "Le produit 2 × 5 vaut 10."),
                 (N("2^3 \\times 5^3 = 8 \\times 125") + " = " + N("1000"), "On retrouve le même résultat.")],
                N("1000") + ".", "(2*5)**3==2**3*5**3==1000"),
        example("Exemple 4", "Calculer " + N("4 + 2 \\times 3^2") + ".",
                "On calcule la puissance d'abord, puis la multiplication, puis l'addition.",
                [(N("3^2") + " = " + N("9"), "Priorité à la puissance."),
                 (N("2 \\times 9") + " = " + N("18"), "Puis la multiplication."),
                 (N("4 + 18") + " = " + N("22"), "Enfin l'addition.")],
                N("22") + ".", "4+2*3**2==22"),
        example("Exemple 5", "Une coopérative range 20 cartons de 20 plaquettes de 20 œufs. Elle vend chaque œuf 25 F après avoir dépensé 150 000 F. Combien de livres à 2 500 F peut-elle acheter avec le bénéfice ?",
                "On calcule le nombre d'œufs avec une puissance, puis la recette, le bénéfice et le nombre de livres.",
                [(N("20^3") + " = " + N("8000"), "20 × 20 = 400, puis 400 × 20 = 8 000 œufs."),
                 (N("8000 \\times 25") + " = " + N("200000"), "La recette est de 200 000 F."),
                 (N("200000 - 150000") + " = " + N("50000"), "Le bénéfice est de 50 000 F."),
                 (N("50000 \\div 2500") + " = " + N("20"), "Elle peut acheter 20 livres.")],
                N("20") + " livres.", "20**3==8000 and 8000*25==200000 and 200000-150000==50000 and 50000//2500==20"),
        warning(N("2^3") + " ne veut pas dire " + N("2 \\times 3") + " : c'est " + N("2 \\times 2 \\times 2") + " = 8, et non 6. De même " + N("(2 + 3)^2") + " = 25 n'est pas " + N("2^2 + 3^2") + " = 13. "
                "Et dans " + N("2 \\times 3^2") + " seul le 3 est au carré : le résultat est 18, et non 36."),
    ],
    [
        number("s1-g1", "puissances", "Calcule " + N("4^3") + ".", Fraction(64), hints=["4 × 4 × 4."], solution=["4 × 4 = 16.", "16 × 4 = 64."]),
        number("s1-g2", "puissances", "Calcule " + N("5^2 \\times 5^3") + ".", Fraction(3125), hints=["On additionne les exposants : 5^5."], solution=["5² × 5³ = 5⁵.", "5 × 5 × 5 × 5 × 5 = 3 125."]),
        number("s1-g3", "puissances", "Calcule " + N("(2 \\times 3)^2") + ".", Fraction(36), hints=["Calcule le produit entre parenthèses d'abord."], solution=["2 × 3 = 6.", "6² = 36."]),
        number("s1-g4", "puissances", "Calcule " + N("3 + 2 \\times 4^2") + ".", Fraction(35), hints=["La puissance d'abord."], solution=["4² = 16.", "2 × 16 = 32.", "3 + 32 = 35."]),
        choice("s1-g5", "puissances", "Que vaut " + N("2^4") + " ?", [N("8"), N("16"), N("6")], 1, hints=["2 × 2 × 2 × 2."], solution=["2 × 2 = 4, 4 × 2 = 8, 8 × 2 = 16."],
               wrong={0: "8 est 2³ : il y a quatre facteurs, pas trois.", 2: "6 serait 2 × 3 ou 2 + 2 + 2 : l'exposant dit combien de fois on multiplie."}),
    ])

# ----- Section 2: Euclidean division -----
S2 = Section(
    "division", "La division dans les entiers naturels et l'encadrement", 22, "division",
    "Écrire et utiliser l'égalité de la division euclidienne, et encadrer un nombre entre deux multiples consécutifs d'un autre.",
    [
        para("Partager 47 billes entre 6 enfants : chacun en reçoit 7, et il en reste 5. On peut écrire cette situation avec une seule égalité : " + N("47 = 6 \\times 7 + 5") + ". "
             "C'est l'égalité de la division euclidienne."),
        rule("Division euclidienne",
             "Pour des entiers naturels a et b, avec b différent de 0, il existe deux entiers q (le quotient) et r (le reste) tels que " + N("a = b \\times q + r") + " avec " + N("0 \\le r < b") + ". "
             "Le reste est toujours plus petit que le diviseur. Si le reste est 0, a est un multiple de b."),
        rule("Encadrer entre deux multiples consécutifs",
             "Si " + N("a = b \\times q + r") + " et si r n'est pas nul, alors " + N("b \\times q < a < b \\times (q + 1)") + " : a est entre deux multiples consécutifs de b."),
        example("Exemple 1", "Effectuer la division euclidienne de 47 par 6.",
                "On cherche le plus grand multiple de 6 qui ne dépasse pas 47.",
                [("6 × 7 = 42 et 6 × 8 = 48", "48 dépasse 47, donc le quotient est 7."),
                 (N("47 - 42") + " = " + N("5"), "Le reste est 5, et 5 est plus petit que 6.")],
                N("47 = 6 \\times 7 + 5") + ".", "47==6*7+5 and 5<6"),
        example("Exemple 2", "Encadrer 47 par deux multiples consécutifs de 6.",
                "On utilise le résultat de la division : 47 = 6 × 7 + 5.",
                [(N("6 \\times 7") + " = " + N("42"), "Le multiple juste en dessous."),
                 (N("6 \\times 8") + " = " + N("48"), "Le multiple juste au-dessus.")],
                N("42 < 47 < 48") + ".", "6*7<47<6*8"),
        example("Exemple 3", "Un nombre a est tel que a = 9 × 13 + 4. Calculer a, et donner le quotient et le reste de sa division par 9.",
                "L'égalité est déjà celle d'une division euclidienne, car 4 est plus petit que 9.",
                [(N("9 \\times 13") + " = " + N("117"), "Le produit."),
                 (N("117 + 4") + " = " + N("121"), "On ajoute le reste."),
                 ("Le reste 4 est plus petit que 9", "Le quotient est 13 et le reste est 4.")],
                N("a = 121") + ", quotient " + N("13") + ", reste " + N("4") + ".", "9*13+4==121 and 4<9"),
        example("Exemple 4", "Un commerçant a 380 kg de riz à mettre dans des sacs de 25 kg. Combien de sacs pleins peut-il remplir ? Combien de kilogrammes restent ?",
                "On divise 380 par 25 : le quotient est le nombre de sacs, le reste est ce qui reste.",
                [("25 × 15 = 375 et 25 × 16 = 400", "400 dépasse 380 : on peut remplir 15 sacs."),
                 (N("380 - 375") + " = " + N("5"), "Il reste 5 kg.")],
                N("15") + " sacs pleins et " + N("5") + " kg restants.", "25*15==375 and 380-375==5 and 5<25"),
        warning("Le reste doit être plus petit que le diviseur : " + N("100 = 7 \\times 13 + 9") + " n'est pas une division euclidienne, car 9 est plus grand que 7. Ici on peut encore mettre un 7 de plus : 100 = 7 × 14 + 2."),
    ],
    [
        number("s2-g1", "division", "Quel est le quotient de la division euclidienne de 53 par 7 ?", Fraction(7), hints=["Cherche le plus grand multiple de 7 qui ne dépasse pas 53."], solution=["7 × 7 = 49 et 7 × 8 = 56 dépasse 53.", "Le quotient est 7."]),
        number("s2-g2", "division", "Quel est le reste de la division euclidienne de 53 par 7 ?", Fraction(4), hints=["53 moins le multiple de 7 juste en dessous."], solution=["53 − 49 = 4."]),
        ordered("s2-g3", "division", "Encadre 100 par deux multiples consécutifs de 12. Écris-les sous la forme petit ; grand.", [Fraction(96), Fraction(108)],
                hints=["12 × 8 = 96."], solution=["12 × 8 = 96 et 12 × 9 = 108.", "96 < 100 < 108."]),
        number("s2-g4", "division", "Calcule a si a = 8 × 11 + 3.", Fraction(91), hints=["Multiplie d'abord."], solution=["8 × 11 = 88.", "88 + 3 = 91."]),
        choice("s2-g5", "division", "Laquelle de ces égalités est une division euclidienne de 50 par 8 ?", [N("50 = 8 \\times 5 + 10"), N("50 = 8 \\times 6 + 2"), N("50 = 8 \\times 7 - 6")], 1,
               hints=["Le reste doit être plus petit que 8 et positif."], solution=["8 × 6 = 48 et 50 − 48 = 2, avec 2 < 8."],
               wrong={0: "Le reste 10 est plus grand que le diviseur 8.", 2: "Un reste ne peut pas être négatif."}),
    ])

# ----- Section 3: prime numbers -----
S3 = Section(
    "premiers", "Les nombres premiers", 24, "premiers",
    "Reconnaître un nombre premier, connaître les premiers nombres premiers et savoir si un nombre de deux ou trois chiffres est premier.",
    [
        para("Certains nombres ne se découpent qu'en 1 et en eux-mêmes : on ne peut pas ranger 7 objets en rectangle autrement qu'en une seule ligne. Ces nombres sont les briques de tous les autres."),
        definition("Nombre premier",
                   "Un nombre entier naturel est premier s'il a exactement deux diviseurs : 1 et lui-même. Les nombres premiers inférieurs à 30 sont " + N("2, 3, 5, 7, 11, 13, 17, 19, 23, 29") + ". "
                   "Le nombre 1 n'est pas premier, car il n'a qu'un seul diviseur. Le nombre 2 est le seul nombre premier pair."),
        rule("Reconnaître un nombre premier",
             "Pour savoir si un nombre n est premier, on essaie de le diviser par les nombres premiers 2, 3, 5, 7, 11... dont le carré ne dépasse pas n. Si aucune de ces divisions ne tombe juste, n est premier. "
             "Dès qu'une division tombe juste (le reste est 0), n n'est pas premier."),
        example("Exemple 1", "Le nombre 29 est-il premier ?",
                "On teste les nombres premiers dont le carré ne dépasse pas 29 : 2, 3 et 5 (car 5² = 25, mais 7² = 49 dépasse 29).",
                [("29 ÷ 2 : reste 1", "29 est impair."),
                 ("29 ÷ 3 : reste 2", "La somme des chiffres 11 n'est pas un multiple de 3."),
                 ("29 ÷ 5 : reste 4", "29 ne finit ni par 0 ni par 5.")],
                "29 est premier.", "all(29 % p for p in (2, 3, 5)) and 5*5<=29<7*7"),
        example("Exemple 2", "Le nombre 91 est-il premier ?",
                "On teste 2, 3, 5 et 7 (7² = 49 ≤ 91 et 11² = 121 dépasse 91).",
                [("91 n'est divisible ni par 2, ni par 3, ni par 5", "Il est impair, 9 + 1 = 10 et 91 ne finit pas par 0 ou 5."),
                 (N("91 \\div 7") + " = " + N("13"), "7 × 13 = 91 : la division tombe juste.")],
                "91 n'est pas premier : " + N("91 = 7 \\times 13") + ".", "91 % 2 and 91 % 3 and 91 % 5 and 91 == 7*13"),
        example("Exemple 3", "Le nombre 157 est-il premier ?",
                "On teste les nombres premiers dont le carré ne dépasse pas 157 : 2, 3, 5, 7, 11 (12² = 144 mais 13² = 169 dépasse 157).",
                [("157 n'est divisible ni par 2, ni par 5, ni par 3", "Car 1 + 5 + 7 = 13, qui n'est pas multiple de 3."),
                 (N("157 = 7 \\times 22 + 3") + " et " + N("157 = 11 \\times 14 + 3"), "Les restes ne sont pas nuls.")],
                "157 est premier.", "all(157 % p for p in (2, 3, 5, 7, 11)) and 11*11<=157<13*13"),
        example("Exemple 4", "Combien y a-t-il de nombres premiers entre 40 et 60 ?",
                "On teste les nombres impairs entre 40 et 60 avec 3, 5 et 7.",
                [("Candidats impairs : 41, 43, 45, 47, 49, 51, 53, 55, 57, 59", "Les pairs ne sont pas premiers."),
                 ("45, 55 sont multiples de 5 ; 51, 57 de 3 ; 49 = 7 × 7", "Ces cinq-là sont éliminés."),
                 ("Restent 41, 43, 47, 53 et 59", "Cinq nombres premiers.")],
                N("5") + " nombres premiers.", "[n for n in range(41, 60) if n > 1 and all(n % k for k in range(2, int(n**0.5) + 1))]==[41, 43, 47, 53, 59]"),
        warning("1 n'est pas un nombre premier. Et tous les nombres impairs ne sont pas premiers : 9, 15, 21, 25, 27, 33, 35... sont impairs mais ne sont pas premiers. "
                "Pour montrer qu'un nombre n'est pas premier, il suffit de trouver un diviseur ; pour montrer qu'il l'est, il faut tester tous les nombres premiers dont le carré ne dépasse pas ce nombre."),
    ],
    [
        choice("s3-g1", "premiers", "Lequel de ces nombres est premier ?", [N("51"), N("53"), N("57")], 1, hints=["51 et 57 sont des multiples de 3."], solution=["51 = 3 × 17 et 57 = 3 × 19, mais 53 n'est divisible par aucun de 2, 3, 5, 7."],
               wrong={0: "51 = 3 × 17.", 2: "57 = 3 × 19."}),
        number("s3-g2", "premiers", "Combien y a-t-il de nombres premiers entre 1 et 20 ?", Fraction(8), hints=["2, 3, 5, 7, ..."], solution=["2, 3, 5, 7, 11, 13, 17, 19 : 8 nombres premiers."]),
        number("s3-g3", "premiers", "Quel est le plus petit nombre premier ?", Fraction(2), hints=["1 n'est pas premier."], solution=["2 est le plus petit nombre premier."]),
        number("s3-g4", "premiers", "Quel est le plus grand nombre premier inférieur à 50 ?", Fraction(47), hints=["Teste 49, 48, 47."], solution=["49 = 7 × 7 et 48 est pair.", "47 n'est divisible ni par 2, 3, 5 : il est premier."]),
        number("s3-g5", "premiers", "Combien un nombre premier a-t-il de diviseurs ?", Fraction(2), hints=["1 et lui-même."], solution=["Un nombre premier a exactement deux diviseurs."]),
    ])

# ----- Section 4: decomposition -----
S4 = Section(
    "decomposition", "Décomposer un nombre en produit de facteurs premiers", 24, "decomposition",
    "Décomposer un nombre entier en produit de facteurs premiers, écrire cette décomposition avec des puissances et utiliser la décomposition dans un problème.",
    [
        para("Tout nombre entier supérieur à 1 s'écrit comme un produit de nombres premiers, et il n'y a qu'une seule façon de le faire (à l'ordre des facteurs près). C'est comme la carte d'identité du nombre."),
        rule("Méthode de décomposition",
             "On divise le nombre par le plus petit nombre premier qui le divise, puis le quotient obtenu par le plus petit nombre premier qui le divise, et ainsi de suite jusqu'à obtenir 1. Les diviseurs successifs sont les facteurs premiers. "
             "On regroupe les facteurs égaux avec des puissances : " + N("60 = 2 \\times 2 \\times 3 \\times 5 = 2^2 \\times 3 \\times 5") + "."),
        example("Exemple 1", "Décomposer 84 en produit de facteurs premiers.",
                "On divise par 2 tant qu'on peut, puis par 3, puis par 5, puis par 7...",
                [(N("84 \\div 2") + " = " + N("42") + " puis " + N("42 \\div 2") + " = " + N("21"), "Deux facteurs 2."),
                 (N("21 \\div 3") + " = " + N("7"), "Un facteur 3."),
                 (N("7 \\div 7") + " = " + N("1"), "Un facteur 7.")],
                N("84 = 2^2 \\times 3 \\times 7") + ".", "2*2*3*7==84"),
        example("Exemple 2", "Décomposer 360 en produit de facteurs premiers, avec des puissances.",
                "Même méthode, avec des divisions plus longues.",
                [(N("360 \\div 2 = 180") + ", " + N("180 \\div 2 = 90") + ", " + N("90 \\div 2 = 45"), "Trois facteurs 2."),
                 (N("45 \\div 3 = 15") + ", " + N("15 \\div 3 = 5"), "Deux facteurs 3."),
                 (N("5 \\div 5 = 1"), "Un facteur 5.")],
                N("360 = 2^3 \\times 3^2 \\times 5") + ".", "2**3*3**2*5==360"),
        example("Exemple 3", "Un nombre a pour décomposition " + N("2^2 \\times 3 \\times 7") + ". Quel est ce nombre ?",
                "On calcule le produit, en commençant par les puissances.",
                [(N("2^2") + " = " + N("4"), "La puissance d'abord."),
                 (N("4 \\times 3 \\times 7") + " = " + N("84"), "12 × 7 = 84.")],
                N("84") + ".", "2**2*3*7==84"),
        example("Exemple 4", "Combien de facteurs premiers (comptés avec répétitions) y a-t-il dans la décomposition de 100 ? Quelle est la décomposition ?",
                "On divise 100 par 2 puis par 5.",
                [(N("100 \\div 2 = 50") + ", " + N("50 \\div 2 = 25"), "Deux facteurs 2."),
                 (N("25 \\div 5 = 5") + ", " + N("5 \\div 5 = 1"), "Deux facteurs 5.")],
                N("100 = 2^2 \\times 5^2") + " : 4 facteurs.", "2*2*5*5==100"),
        warning("N'oublie pas de continuer jusqu'à obtenir 1, et vérifie ton résultat en refaisant le produit. Un facteur de la décomposition doit être un nombre premier : écrire " + N("12 = 3 \\times 4") + " n'est pas une décomposition en facteurs premiers, car 4 n'est pas premier."),
    ],
    [
        ordered("s4-g1", "decomposition", "Décompose 30 en facteurs premiers. Écris les facteurs dans l'ordre croissant, séparés par des points-virgules.", [Fraction(2), Fraction(3), Fraction(5)],
                hints=["30 ÷ 2, puis 15 ÷ 3, puis 5 ÷ 5."], solution=["30 = 2 × 15.", "15 = 3 × 5.", "30 = 2 × 3 × 5."]),
        ordered("s4-g2", "decomposition", "Décompose 36 en facteurs premiers. Écris les facteurs dans l'ordre croissant, séparés par des points-virgules.", [Fraction(2), Fraction(2), Fraction(3), Fraction(3)],
                hints=["36 = 2 × 18."], solution=["36 = 2 × 18 = 2 × 2 × 9 = 2 × 2 × 3 × 3."]),
        ordered("s4-g3", "decomposition", "Décompose 100 en facteurs premiers. Écris les facteurs dans l'ordre croissant, séparés par des points-virgules.", [Fraction(2), Fraction(2), Fraction(5), Fraction(5)],
                hints=["100 = 2 × 50."], solution=["100 = 2 × 2 × 25 = 2 × 2 × 5 × 5."]),
        number("s4-g4", "decomposition", "Quel est le nombre dont la décomposition est " + N("2^3 \\times 3^2") + " ?", Fraction(72), hints=["2³ = 8 et 3² = 9."], solution=["8 × 9 = 72."]),
        choice("s4-g5", "decomposition", "Quelle est la décomposition de 45 en facteurs premiers ?", [N("3 \\times 15"), N("3^2 \\times 5"), N("9 \\times 5")], 1,
               hints=["Les facteurs doivent être premiers."], solution=["45 = 3 × 15 = 3 × 3 × 5 = 3² × 5."], wrong={0: "15 n'est pas un nombre premier (15 = 3 × 5).", 2: "9 n'est pas un nombre premier (9 = 3 × 3)."}),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "puissances", "Calcule " + N("3^4") + ".", Fraction(81), 1, ["3 × 3 × 3 × 3."], ["9 × 9 = 81."]),
    number("p2", "puissances", "Calcule " + N("10^5") + ".", Fraction(100000), 1, ["1 suivi de 5 zéros."], ["10^5 = 100 000."]),
    number("p3", "puissances", "Calcule " + N("2^3 \\times 2^4") + ".", Fraction(128), 2, ["2^7."], ["2³ × 2⁴ = 2⁷ = 128."]),
    number("p4", "puissances", "Calcule " + N("(3 \\times 4)^2") + ".", Fraction(144), 2, ["12²."], ["3 × 4 = 12, puis 12² = 144."]),
    number("p5", "puissances", "Calcule " + N("5 + 3 \\times 2^3") + ".", Fraction(29), 2, ["La puissance d'abord."], ["2³ = 8.", "3 × 8 = 24.", "5 + 24 = 29."]),
    number("p6", "puissances", "Calcule " + N("20 - 2^4") + ".", Fraction(4), 2, ["2⁴ = 16."], ["20 − 16 = 4."]),
    number("p7", "puissances", "Calcule " + N("(7 - 4)^3") + ".", Fraction(27), 2, ["Parenthèses d'abord."], ["7 − 4 = 3.", "3³ = 27."]),
    number("p8", "puissances", "Calcule " + N("2^2 \\times 5^2") + ".", Fraction(100), 2, ["4 × 25, ou (2 × 5)²."], ["2² × 5² = (2 × 5)² = 10² = 100."]),
    number("p9", "puissances", "Un cube a des arêtes de 6 cm. Quel est son volume, en cm³ ?", Fraction(216), 2, ["Volume d'un cube = arête³."], ["6³ = 6 × 6 × 6 = 216 cm³."], units=["cm3", "cm³"]),
    number("p10", "puissances", "Une salle a 12 rangées de 12 tables de 12 places. Combien de places y a-t-il ?", Fraction(1728), 3, ["12 × 12 × 12."], ["12³ = 144 × 12 = 1 728."]),
    choice("p11", "puissances", "Laquelle de ces égalités est vraie ?", [N("2^3 = 6"), N("2^3 = 8"), N("2^3 = 9")], 1, 1, ["2 × 2 × 2."], ["2³ = 8."], wrong={0: "6 serait 2 × 3.", 2: "9 serait 3²."}),
    choice("p12", "puissances", "Laquelle de ces égalités est vraie ?", [N("(2 + 3)^2 = 2^2 + 3^2"), N("(2 \\times 3)^2 = 2^2 \\times 3^2"), N("2^2 \\times 2^3 = 2^6")], 1, 3, ["Teste avec les valeurs numériques."], ["(2 × 3)² = 36 = 4 × 9 ; mais (2 + 3)² = 25 ≠ 13 et 2² × 2³ = 2⁵ = 32 ≠ 64."], wrong={0: "25 n'est pas égal à 13.", 2: "On additionne les exposants : 2² × 2³ = 2⁵."}),
    number("p13", "division", "Quel est le quotient de la division euclidienne de 200 par 17 ?", Fraction(11), 1, ["17 × 11 = 187."], ["17 × 11 = 187 et 17 × 12 = 204 dépasse 200."]),
    number("p14", "division", "Quel est le reste de la division euclidienne de 200 par 17 ?", Fraction(13), 1, ["200 − 187."], ["200 − 187 = 13."]),
    number("p15", "division", "Calcule a si a = 15 × 9 + 7.", Fraction(142), 1, ["15 × 9 = 135."], ["135 + 7 = 142."]),
    ordered("p16", "division", "Encadre 250 par deux multiples consécutifs de 40. Écris-les sous la forme petit ; grand.", [Fraction(240), Fraction(280)], 2, ["40 × 6 = 240."], ["40 × 6 = 240 et 40 × 7 = 280."]),
    ordered("p17", "division", "Encadre 77 par deux multiples consécutifs de 9. Écris-les sous la forme petit ; grand.", [Fraction(72), Fraction(81)], 2, ["9 × 8 = 72."], ["9 × 8 = 72 et 9 × 9 = 81."]),
    number("p18", "division", "On range 500 œufs dans des boîtes de 12. Combien de boîtes pleines ?", Fraction(41), 2, ["12 × 41 = 492."], ["12 × 41 = 492 et 12 × 42 = 504 dépasse 500."]),
    number("p19", "division", "On range 500 œufs dans des boîtes de 12. Combien d'œufs ne sont pas dans une boîte pleine ?", Fraction(8), 2, ["500 − 492."], ["500 − 492 = 8 œufs."]),
    number("p20", "division", "Une division euclidienne par 13 donne le quotient 8 et le reste 5. Quel est le nombre divisé ?", Fraction(109), 2, ["13 × 8 + 5."], ["13 × 8 = 104.", "104 + 5 = 109."]),
    number("p21", "division", "Dans la division euclidienne d'un nombre par 7, quel est le plus grand reste possible ?", Fraction(6), 2, ["Le reste est plus petit que 7."], ["Les restes possibles vont de 0 à 6 : le plus grand est 6."]),
    choice("p22", "division", "Quelle égalité est une division euclidienne de 75 par 9 ?", [N("75 = 9 \\times 7 + 12"), N("75 = 9 \\times 8 + 3"), N("75 = 9 \\times 9 - 6")], 1, 2, ["Le reste doit être plus petit que 9."], ["9 × 8 = 72 et 75 − 72 = 3, avec 3 < 9."], wrong={0: "Le reste 12 dépasse 9.", 2: "Le reste ne peut pas être négatif."}),
    choice("p23", "premiers", "Lequel de ces nombres est premier ?", [N("39"), N("41"), N("49")], 1, 1, ["39 = 3 × 13 et 49 = 7 × 7."], ["41 n'est divisible ni par 2, 3, 5."], wrong={0: "39 = 3 × 13.", 2: "49 = 7 × 7."}),
    choice("p24", "premiers", "Lequel de ces nombres n'est pas premier ?", [N("37"), N("43"), N("51")], 2, 1, ["Cherche un diviseur autre que 1 et le nombre."], ["51 = 3 × 17."], wrong={0: "37 est premier.", 1: "43 est premier."}),
    number("p25", "premiers", "Combien y a-t-il de nombres premiers entre 20 et 40 ?", Fraction(4), 2, ["23, 29, 31, 37."], ["23, 29, 31 et 37 : 4 nombres premiers."]),
    number("p26", "premiers", "Quel est le plus petit nombre premier supérieur à 90 ?", Fraction(97), 3, ["Teste 91, 93, 95, 97."], ["91 = 7 × 13, 93 = 3 × 31, 95 = 5 × 19 et 97 est premier."]),
    choice("p27", "premiers", "Le nombre 1 est-il premier ?", ["Oui", "Non, il n'a qu'un seul diviseur", "Oui, car il est impair"], 1, 1, ["Un nombre premier a exactement deux diviseurs."], ["1 n'a qu'un diviseur : il n'est pas premier."], wrong={0: "Il faudrait deux diviseurs.", 2: "Être impair ne suffit pas."}),
    choice("p28", "premiers", "Combien de nombres premiers sont pairs ?", ["Aucun", "Un seul : 2", "Tous"], 1, 2, ["Un nombre pair est divisible par 2."], ["Tout nombre pair plus grand que 2 a le diviseur 2 en plus de 1 et de lui-même : seul 2 est premier."], wrong={0: "2 est pair et premier.", 2: "4, 6, 8... ne sont pas premiers."}),
    choice("p29", "premiers", "Karim dit : « 91 est premier car il n'est divisible ni par 2, ni par 3, ni par 5 ». Qu'en penses-tu ?", ["Il a raison", "Il a tort : 91 = 7 × 13", "Il a tort : 91 est pair"], 1, 3, ["Teste aussi 7."], ["91 = 7 × 13 : il faut tester tous les premiers dont le carré est inférieur à 91, jusqu'à 7."], wrong={0: "7 divise 91.", 2: "91 est impair."}),
    number("p30", "premiers", "Combien de diviseurs a le nombre 13 ?", Fraction(2), 1, ["13 est premier."], ["1 et 13 : 2 diviseurs."]),
    ordered("p31", "decomposition", "Décompose 18 en facteurs premiers (ordre croissant, séparés par des points-virgules).", [Fraction(2), Fraction(3), Fraction(3)], 1, ["18 = 2 × 9."], ["18 = 2 × 3 × 3."]),
    ordered("p32", "decomposition", "Décompose 60 en facteurs premiers (ordre croissant, séparés par des points-virgules).", [Fraction(2), Fraction(2), Fraction(3), Fraction(5)], 2, ["60 = 2 × 30."], ["60 = 2 × 2 × 3 × 5."]),
    ordered("p33", "decomposition", "Décompose 90 en facteurs premiers (ordre croissant, séparés par des points-virgules).", [Fraction(2), Fraction(3), Fraction(3), Fraction(5)], 2, ["90 = 2 × 45."], ["90 = 2 × 3 × 3 × 5."]),
    ordered("p34", "decomposition", "Décompose 126 en facteurs premiers (ordre croissant, séparés par des points-virgules).", [Fraction(2), Fraction(3), Fraction(3), Fraction(7)], 3, ["126 = 2 × 63."], ["126 = 2 × 63 = 2 × 3 × 21 = 2 × 3 × 3 × 7."]),
    ordered("p35", "decomposition", "Décompose 210 en facteurs premiers (ordre croissant, séparés par des points-virgules).", [Fraction(2), Fraction(3), Fraction(5), Fraction(7)], 3, ["210 = 2 × 105."], ["210 = 2 × 3 × 5 × 7."]),
    number("p36", "decomposition", "Quel est le nombre dont la décomposition est " + N("2^2 \\times 3^2 \\times 5") + " ?", Fraction(180), 2, ["4 × 9 × 5."], ["4 × 9 = 36.", "36 × 5 = 180."]),
    number("p37", "decomposition", "Quel est le nombre dont la décomposition est " + N("2 \\times 3 \\times 5 \\times 7") + " ?", Fraction(210), 1, ["Multiplie les quatre facteurs."], ["2 × 3 = 6, 6 × 5 = 30, 30 × 7 = 210."]),
    number("p38", "decomposition", "Combien de facteurs premiers (avec répétitions) y a-t-il dans la décomposition de 72 ?", Fraction(5), 3, ["72 = 2 × 2 × 2 × 3 × 3."], ["72 = 2³ × 3² : 3 + 2 = 5 facteurs."]),
    choice("p39", "decomposition", "Léa écrit « 24 = 4 × 6 est la décomposition de 24 en facteurs premiers ». Quelle est son erreur ?", ["4 et 6 ne sont pas premiers", "24 n'a pas de décomposition", "Elle a oublié l'exposant"], 0, 2, ["Les facteurs doivent être premiers."], ["4 = 2 × 2 et 6 = 2 × 3 : la décomposition est 24 = 2³ × 3."], wrong={1: "Tout entier supérieur à 1 a une décomposition.", 2: "Le problème est dans les facteurs, pas dans l'exposant."}),
]

SUMMARY = [
    definition("Puissances", "a^n est le produit de n facteurs égaux à a. a^n × a^m = a^(n + m) et (a × b)^n = a^n × b^n. Dans un calcul, la puissance se fait d'abord, puis × et ÷, puis + et −."),
    rule("Division euclidienne", "a = b × q + r avec 0 ≤ r < b. Si r ≠ 0, b × q < a < b × (q + 1) : a est encadré par deux multiples consécutifs de b. Si r = 0, a est un multiple de b."),
    rule("Nombres premiers", "Un nombre premier a exactement deux diviseurs : 1 et lui-même. 1 n'est pas premier ; 2 est le seul premier pair. Pour tester n, on divise par les nombres premiers dont le carré ne dépasse pas n."),
    rule("Décomposition", "Tout entier supérieur à 1 s'écrit de façon unique comme produit de facteurs premiers : 60 = 2² × 3 × 5. On divise par le plus petit premier possible jusqu'à obtenir 1."),
    para("Les erreurs à éviter : confondre a^n et a × n ; oublier la priorité de la puissance ; donner un reste plus grand que le diviseur ; croire que 1 est premier ; s'arrêter trop tôt en testant la primalité ; mettre dans la décomposition un facteur qui n'est pas premier."),
]

CONCEPTS = {
    "puissances": ("Puissances d'un nombre entier", "puissances"),
    "division": ("Division euclidienne et encadrement", "division"),
    "premiers": ("Nombres premiers", "premiers"),
    "decomposition": ("Décomposition en facteurs premiers", "decomposition"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    # 1. a power
    base, exponent = rng.randint(2, 9), rng.randint(2, 4)
    questions.append(number("a1", "puissances", f"Calcule ${pw(base, exponent)}$.", Fraction(base**exponent), 1, ["Multiplie l'entier par lui-même autant de fois que l'exposant."],
                            [" × ".join([str(base)] * exponent) + f" = {base**exponent}."]))
    # 2. a product of powers of the same base
    base = rng.randint(2, 5)
    n, m = rng.randint(1, 3), rng.randint(1, 3)
    questions.append(number("a2", "puissances", f"Calcule ${pw(base, n)} \\times {pw(base, m)}$.", Fraction(base ** (n + m)), 2, ["On additionne les exposants."],
                            [f"{base}^{n} × {base}^{m} = {base}^{n + m}.", f"{base}^{n + m} = {base ** (n + m)}."]))
    # 3. a power of a product
    a, b, k = rng.randint(2, 5), rng.randint(2, 5), rng.randint(2, 3)
    questions.append(number("a3", "puissances", f"Calcule $({a} \\times {b})^{k}$.", Fraction((a * b) ** k), 2, ["Calcule le produit entre parenthèses d'abord."],
                            [f"{a} × {b} = {a * b}.", f"{a * b}^{k} = {(a * b) ** k}."]))
    # 4. the priority of the power
    x, y, z = rng.randint(2, 9), rng.randint(2, 6), rng.randint(2, 4)
    questions.append(number("a4", "puissances", f"Calcule ${x} + {y} \\times {z}^2$.", Fraction(x + y * z * z), 2, ["La puissance d'abord, puis la multiplication."],
                            [f"{z}² = {z * z}.", f"{y} × {z * z} = {y * z * z}.", f"{x} + {y * z * z} = {x + y * z * z}."]))
    # 5. the quotient and 6. the remainder of a Euclidean division
    b = rng.randint(6, 19)
    q = rng.randint(5, 25)
    r = rng.randint(1, b - 1)
    a = b * q + r
    questions.append(number("a5", "division", f"Quel est le quotient de la division euclidienne de {a} par {b} ?", Fraction(q), 2, ["Cherche le plus grand multiple du diviseur qui ne dépasse pas le nombre."],
                            [f"{b} × {q} = {b * q} et {b} × {q + 1} = {b * (q + 1)} dépasse {a}.", f"Le quotient est {q}."]))
    b = rng.randint(6, 19)
    q = rng.randint(5, 25)
    r = rng.randint(1, b - 1)
    a = b * q + r
    questions.append(number("a6", "division", f"Quel est le reste de la division euclidienne de {a} par {b} ?", Fraction(r), 2, ["Retire du nombre le plus grand multiple du diviseur qui ne le dépasse pas."],
                            [f"{b} × {q} = {b * q}.", f"{a} − {b * q} = {r}."]))
    # 7. bracketing between two consecutive multiples
    b = rng.randint(6, 25)
    q = rng.randint(4, 20)
    a = b * q + rng.randint(1, b - 1)
    questions.append(ordered("a7", "division", f"Encadre {a} par deux multiples consécutifs de {b}. Écris-les sous la forme petit ; grand.", [Fraction(b * q), Fraction(b * (q + 1))], 2,
                             ["Cherche le plus grand multiple de " + str(b) + " qui ne dépasse pas " + str(a) + "."], [f"{b} × {q} = {b * q} et {b} × {q + 1} = {b * (q + 1)}.", f"{b * q} < {a} < {b * (q + 1)}."]))
    # 8. which number is prime
    prime = rng.choice([p for p in range(31, 100) if is_prime(p)])
    composites = rng.sample([n for n in range(31, 100) if n % 2 and not is_prime(n)], 2)
    options = [prime] + composites
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a8", "premiers", "Lequel de ces nombres est premier ?", [str(options[i]) for i in order], order.index(0), 2, ["Cherche un diviseur autre que 1 et le nombre."],
                            [f"{composites[0]} et {composites[1]} ont un diviseur de plus ; seul {prime} est premier."],
                            wrong={order.index(1): f"{composites[0]} = {prime_factors(composites[0])[0]} × {composites[0] // prime_factors(composites[0])[0]}.", order.index(2): f"{composites[1]} = {prime_factors(composites[1])[0]} × {composites[1] // prime_factors(composites[1])[0]}."}))
    # 9. count the primes in a range
    start = rng.randint(10, 80)
    count = sum(1 for n in range(start, start + 20) if is_prime(n))
    questions.append(number("a9", "premiers", f"Combien y a-t-il de nombres premiers de {start} à {start + 19}, ces deux nombres compris ?", Fraction(count), 3, ["Teste chaque nombre impair avec les petits nombres premiers."],
                            ["Les nombres premiers sont : " + ", ".join(str(n) for n in range(start, start + 20) if is_prime(n)) + f". Il y en a {count}."]))
    # 10. a decomposition
    n = rng.choice([x for x in range(30, 400) if len(prime_factors(x)) in (3, 4) and max(prime_factors(x)) <= 13])
    questions.append(ordered("a10", "decomposition", f"Décompose {n} en facteurs premiers (ordre croissant, séparés par des points-virgules).", [Fraction(p) for p in prime_factors(n)], 3,
                             ["Divise par le plus petit nombre premier possible jusqu'à obtenir 1."], [" × ".join(str(p) for p in prime_factors(n)) + f" = {n}."]))
    # 11. a value from a decomposition
    e2, e3, e5 = rng.randint(1, 3), rng.randint(1, 2), rng.randint(0, 1)
    value = 2**e2 * 3**e3 * 5**e5
    text = f"{pw(2, e2) if e2 > 1 else '2'} \\times {pw(3, e3) if e3 > 1 else '3'}" + (" \\times 5" if e5 else "")
    questions.append(number("a11", "decomposition", f"Quel est le nombre dont la décomposition est ${text}$ ?", Fraction(value), 2, ["Calcule d'abord les puissances."],
                            [f"{2**e2} × {3**e3}" + (" × 5" if e5 else "") + f" = {value}."]))
    # 12. a power in a problem
    side = rng.randint(7, 30)
    questions.append(number("a12", "puissances", f"Une salle a {side} rangées de {side} tables de {side} places. Combien de places y a-t-il ?", Fraction(side**3), 3, ["C'est une puissance."],
                            [f"{side}³ = {side} × {side} × {side} = {side ** 3}."]))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=1, title="Puissances, division et nombres premiers", language="fr",
    intro="Pour compter des œufs rangés en cartons, en plaquettes et en alvéoles, ou pour partager des sacs de riz, on multiplie et on divise avec des nombres entiers. "
          "Ce chapitre t'apprend les puissances, la division avec reste, les nombres premiers et la décomposition d'un nombre en facteurs premiers.",
    objectives=["Calculer une puissance d'un nombre entier et utiliser les égalités sur les puissances.",
                "Écrire et utiliser l'égalité de la division euclidienne, et encadrer un nombre entre deux multiples consécutifs.",
                "Reconnaître un nombre premier de deux ou trois chiffres.",
                "Décomposer un nombre entier en produit de facteurs premiers."],
    prerequisites=[{"text": "Connaître les multiples, les diviseurs et les critères de divisibilité.", "chapter": "sn-6e-entiers"},
                   {"text": "Multiplier et diviser des nombres entiers."}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="First chapter of the Senegal Cinquième course. Its contents follow lesson 1 of the Côte d'Ivoire Cinquième programme (powers, the Euclidean division and bracketing between multiples, prime numbers, decomposition into prime factors), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. It has not been checked against the official Senegalese programme.",
)
