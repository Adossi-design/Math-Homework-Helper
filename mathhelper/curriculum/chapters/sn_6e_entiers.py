"""Sixième, Les nombres entiers naturels: the eighth chapter of the Senegal Sixième course, written in French.

The contents follow lesson 9 "Nombres entiers naturels" of the Côte d'Ivoire Sixième programme (consecutive natural numbers, multiples and divisors,
divisibility by 2, 3, 5, 9, 10, 100 and 1000, the symbols of membership and inclusion), which was read for this chapter, and the divisibility exercises of
the ADEM-Dakar Sixième booklet. Every explanation, example and exercise was written independently, with our own numbers.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .kit import N, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-6e-entiers"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")
NAT = "$\\mathbb{N}$"


def divisors(n):
    """Return every divisor of a natural number, in increasing order."""
    return [k for k in range(1, n + 1) if n % k == 0]


def digit_sum(n):
    """Return the sum of the digits of a natural number."""
    return sum(int(c) for c in str(n))


# ----- Section 1: consecutive natural numbers -----
S1 = Section(
    "consecutifs", "Les entiers naturels et les entiers consécutifs", 20, "consecutifs",
    "Utiliser les symboles d'appartenance et d'inclusion, trouver des entiers consécutifs et compter les entiers compris entre deux nombres.",
    [
        para("Les nombres 0, 1, 2, 3, ... qui servent à compter sont les entiers naturels. Ils forment l'ensemble " + NAT + ". Chacun a un suivant, qu'on obtient en ajoutant 1, et chacun, sauf 0, a un précédent."),
        definition("Appartenance, inclusion, entiers consécutifs",
                   "On écrit " + "$7 \\in \\mathbb{N}$" + " (« 7 appartient à N ») car 7 est un entier naturel, et " + "$2{,}5 \\notin \\mathbb{N}$" + " (« 2,5 n'appartient pas à N »). "
                   "Le symbole " + "$\\subset$" + " relie deux ensembles : " + "$\\mathbb{N} \\subset \\mathbb{D}$" + " veut dire que tous les entiers naturels sont des décimaux. "
                   "Deux entiers naturels sont consécutifs quand le second est le suivant du premier : 47 et 48 sont consécutifs."),
        rule("Compter les entiers entre deux nombres",
             "Entre deux entiers " + N("a") + " et " + N("b") + " avec " + N("a < b") + ", le nombre d'entiers strictement compris entre " + N("a") + " et " + N("b") + " (sans compter " + N("a") + " ni " + N("b") + ") est " + N("b - a - 1")
             + ". Si on compte aussi " + N("a") + " et " + N("b") + ", il y en a " + N("b - a + 1") + "."),
        example("Exemple 1", "Donner les entiers consécutifs qui entourent 99, puis recopier chaque affirmation avec le bon symbole : 8 … N ; 3,5 … N.",
                "On utilise le précédent et le suivant, puis la définition de l'ensemble N.",
                [("Précédent de 99 : 99 − 1 = 98. Suivant : 99 + 1 = 100", "98, 99 et 100 sont trois entiers consécutifs."),
                 ("8 est un entier naturel : " + "$8 \\in \\mathbb{N}$", "Il appartient à N."),
                 ("3,5 a une partie décimale non nulle : " + "$3{,}5 \\notin \\mathbb{N}$", "Il n'appartient pas à N.")],
                "98 et 100 ; " + "$8 \\in \\mathbb{N}$" + " ; " + "$3{,}5 \\notin \\mathbb{N}$", "99-1==98 and 99+1==100"),
        example("Exemple 2", "Combien d'entiers naturels sont strictement compris entre 12 et 20 ? Et combien y en a-t-il si on compte 12 et 20 ?",
                "On liste les entiers, puis on vérifie avec la règle.",
                [("Les entiers entre 12 et 20 : 13, 14, 15, 16, 17, 18, 19", "On n'écrit ni 12 ni 20."),
                 ("On en compte 7. Avec la règle : " + N("20 - 12 - 1") + " = " + N("7"), "20 − 12 = 8 et on retire 1."),
                 ("Avec 12 et 20 compris : " + N("20 - 12 + 1") + " = " + N("9"), "On ajoute les deux extrémités : 7 + 2 = 9.")],
                "7 entiers, ou 9 en comptant 12 et 20", "20-12-1==7 and 20-12+1==9 and len(range(13, 20))==7"),
        definition("Nombres pairs et impairs",
                   "Un nombre pair est un multiple de 2 : son chiffre des unités est 0, 2, 4, 6 ou 8 (0 est pair). Un nombre impair n'est pas un multiple de 2 : son chiffre des unités est 1, 3, 5, 7 ou 9. "
                   "Deux entiers consécutifs sont toujours un pair et un impair."),
        example("Exemple 3", "Parmi 48, 1 305 et 270, lesquels sont pairs ? Quel est l'entier pair qui suit 1 305 ?",
                "On regarde le chiffre des unités de chaque nombre.",
                [("48 se termine par 8 et 270 par 0", "Ces deux nombres sont pairs."),
                 ("1 305 se termine par 5", "Il est impair."),
                 ("Le suivant de 1 305 est 1 306, qui se termine par 6", "C'est le nombre pair qui suit 1 305.")],
                "48 et 270 ; 1 306", "48%2==0 and 270%2==0 and 1305%2==1 and 1306%2==0"),
        example("Exemple 4", "Quel est le plus grand entier de 3 chiffres ? le plus petit de 4 chiffres ? Que remarque-t-on ?",
                "On cherche le nombre qui précède et le nombre qui suit.",
                [("Le plus grand entier de 3 chiffres est 999", "Tous ses chiffres sont les plus grands possibles."),
                 ("Le plus petit entier de 4 chiffres est 1 000", "Il faut un 1 suivi de trois zéros."),
                 (N("999 + 1") + " = " + N("1000"), "Ce sont deux entiers consécutifs : 1 000 est le suivant de 999.")],
                "999 et 1 000, deux entiers consécutifs", "999+1==1000 and len(str(999))==3 and len(str(1000))==4"),
        warning("Entre 12 et 20, il y a 7 entiers (et non 8) si on ne compte pas les extrémités. Ne confonds pas la différence 20 − 12 = 8 avec le nombre d'entiers qui les séparent."),
    ],
    [
        number("s1-g1", "consecutifs", "Quel est l'entier naturel qui suit 349 ?", Fraction(350), hints=["Ajoute 1."], solution=["349 + 1 = 350."]),
        number("s1-g2", "consecutifs", "Quel est l'entier naturel qui précède 1 000 ?", Fraction(999), hints=["Retire 1."], solution=["1 000 − 1 = 999."]),
        number("s1-g3", "consecutifs", "Combien d'entiers naturels sont strictement compris entre 47 et 63 ?", Fraction(15), hints=["Utilise la règle : différence moins 1."], solution=["63 − 47 = 16.", "16 − 1 = 15 entiers."]),
        number("s1-g4", "consecutifs", "Combien d'entiers naturels y a-t-il de 30 à 45, ces deux nombres compris ?", Fraction(16), hints=["On compte aussi les deux extrémités."], solution=["45 − 30 = 15.", "15 + 1 = 16 entiers."]),
        choice("s1-g5", "consecutifs", "Quelle écriture est correcte ?", ["$6{,}2 \\in \\mathbb{N}$", "$6{,}2 \\notin \\mathbb{N}$", "$6 \\notin \\mathbb{N}$"], 1,
               hints=["6,2 est-il un entier naturel ?"], solution=["6,2 a une partie décimale non nulle : ce n'est pas un entier naturel.", "6,2 n'appartient pas à N."],
               wrong={0: "6,2 n'est pas un entier naturel : il est entre 6 et 7.", 2: "6 est un entier naturel : il appartient à N."}),
    ])

# ----- Section 2: multiples and divisors -----
S2 = Section(
    "multiples", "Multiples et diviseurs", 24, "multiples",
    "Reconnaître un multiple et un diviseur, lister les multiples d'un nombre et tous les diviseurs d'un nombre inférieur à 1 000.",
    [
        para("Si on range 12 oranges en tas de 3, il n'en reste aucune : 12 = 3 × 4. On dit que 12 est un multiple de 3 et que 3 est un diviseur de 12. En revanche, 12 oranges en tas de 5 laissent un reste : 5 n'est pas un diviseur de 12."),
        definition("Multiple, diviseur, divisible",
                   "Un entier naturel " + N("a") + " est un multiple d'un entier naturel " + N("b") + " s'il existe un entier naturel " + N("k") + " tel que " + N("a = b \\times k") + ". "
                   "On dit alors que " + N("a") + " est divisible par " + N("b") + " (avec " + N("b") + " différent de 0) et que " + N("b") + " est un diviseur de " + N("a") + ". Le reste de la division de " + N("a") + " par " + N("b") + " est alors 0."),
        rule("Trouver les diviseurs d'un nombre",
             "On cherche les entiers qui divisent le nombre en testant 1, 2, 3, ... dans l'ordre. Chaque fois qu'on en trouve un, son quotient en est un autre, ce qui donne les diviseurs par paires. On s'arrête quand le diviseur dépasse le quotient. 1 et le nombre lui-même sont toujours des diviseurs."),
        example("Exemple 1", "Lister les cinq premiers multiples non nuls de 7, puis dire si 91 est un multiple de 7.",
                "Les multiples de 7 sont 7 × 1, 7 × 2, 7 × 3, ...",
                [("7 × 1 = 7 ; 7 × 2 = 14 ; 7 × 3 = 21 ; 7 × 4 = 28 ; 7 × 5 = 35", "Les cinq premiers multiples non nuls : 7, 14, 21, 28, 35. Le multiple 0 est 7 × 0."),
                 ("91 ÷ 7 = 13, reste 0", "7 × 13 = 91."),
                 ("91 = 7 × 13 donc 91 est un multiple de 7", "Il est aussi divisible par 7, et 7 est un diviseur de 91.")],
                "7, 14, 21, 28, 35 ; oui, 91 = 7 × 13", "[7*k for k in range(1, 6)]==[7, 14, 21, 28, 35] and 7*13==91"),
        example("Exemple 2", "Trouver tous les diviseurs de 36.",
                "On teste les entiers à partir de 1 et on note chaque paire de diviseurs.",
                [("1 divise 36 : 36 = 1 × 36", "Paire : 1 et 36."),
                 ("2 divise 36 : 36 = 2 × 18", "Paire : 2 et 18."),
                 ("3 divise 36 : 36 = 3 × 12 ; 4 divise 36 : 36 = 4 × 9", "Paires : 3 et 12, 4 et 9. 5 ne divise pas 36 (36 ÷ 5 = 7, reste 1)."),
                 ("6 divise 36 : 36 = 6 × 6", "Le quotient est 6 aussi : on s'arrête, car les diviseurs suivants (7, 8...) donneraient des quotients déjà trouvés."),
                 ("Les diviseurs de 36 sont : 1, 2, 3, 4, 6, 9, 12, 18, 36", "Il y en a 9.")],
                "1, 2, 3, 4, 6, 9, 12, 18, 36", "[k for k in range(1, 37) if 36 % k == 0]==[1, 2, 3, 4, 6, 9, 12, 18, 36]"),
        example("Exemple 3", "Quel est le plus petit multiple de 8 supérieur à 50 ?",
                "On cherche le premier multiple de 8 qui dépasse 50.",
                [("50 ÷ 8 = 6, reste 2", "8 × 6 = 48 est plus petit que 50."),
                 ("8 × 7 = 56", "56 est plus grand que 50 : c'est le premier multiple de 8 qui dépasse 50.")],
                N("56"), "8*6==48<50<56==8*7"),
        example("Exemple 4", "36 est-il un multiple de 9 ? 36 est-il un diviseur de 72 ?",
                "On cherche un entier k tel que 36 = 9 × k, puis un entier k tel que 72 = 36 × k.",
                [("36 = 9 × 4", "4 est un entier : 36 est un multiple de 9."),
                 ("72 = 36 × 2", "2 est un entier : 72 est un multiple de 36, donc 36 est un diviseur de 72.")],
                "Oui et oui", "36==9*4 and 72==36*2"),
        warning("Un multiple n'est pas un diviseur : 12 est un multiple de 3, mais 3 est un diviseur de 12. Et 0 est un multiple de tous les nombres, mais on ne peut jamais diviser par 0."),
    ],
    [
        number("s2-g1", "multiples", "Quel est le plus petit multiple de 9 supérieur à 40 ?", Fraction(45), hints=["9 × 4 = 36, 9 × 5 = ?"], solution=["9 × 4 = 36 est trop petit.", "9 × 5 = 45 est le premier multiple de 9 qui dépasse 40."]),
        number("s2-g2", "multiples", "Combien y a-t-il de multiples de 7 entre 1 et 100 ?", Fraction(14), hints=["Combien de fois 7 entre-t-il dans 100 ?"], solution=["100 ÷ 7 = 14, reste 2.", "Les multiples sont 7 × 1, 7 × 2, ..., 7 × 14 = 98 : il y en a 14."]),
        number("s2-g3", "multiples", "Combien de diviseurs a 48 ?", Fraction(10), hints=["Trouve-les par paires : 1 et 48, 2 et 24, ..."], solution=["1 × 48, 2 × 24, 3 × 16, 4 × 12, 6 × 8.", "Les diviseurs sont 1, 2, 3, 4, 6, 8, 12, 16, 24, 48 : il y en a 10."]),
        choice("s2-g4", "multiples", "Lequel de ces nombres est un diviseur de 45 ?", ["7", "9", "8", "12"], 1, hints=["Teste chaque nombre : 45 ÷ 7, 45 ÷ 9..."], solution=["45 ÷ 9 = 5, reste 0 : 9 est un diviseur de 45.", "Ni 7, ni 8, ni 12 ne divisent 45 exactement."],
               wrong={0: "45 ÷ 7 = 6, reste 3 : 7 ne divise pas 45.", 2: "45 ÷ 8 = 5, reste 5 : 8 ne divise pas 45.", 3: "45 ÷ 12 = 3, reste 9 : 12 ne divise pas 45."}),
        number("s2-g5", "multiples", "Quel est le plus grand diviseur de 60 différent de 60 ?", Fraction(30), hints=["Le plus petit diviseur autre que 1 est 2. Quel est son quotient ?"], solution=["60 ÷ 2 = 30 et 2 est le plus petit diviseur différent de 1.", "Le plus grand diviseur différent de 60 est 30."]),
    ])

# ----- Section 3: divisibility rules -----
S3 = Section(
    "criteres", "Les critères de divisibilité", 26, "criteres",
    "Reconnaître sans diviser si un nombre est divisible par 2, 3, 5, 9, 10, 100 ou 1 000.",
    [
        para("Savoir si 4 785 est divisible par 5, ou si 5 439 est divisible par 3, sans poser la division, c'est utile. Des critères permettent de répondre en regardant simplement les chiffres du nombre."),
        rule("Divisibilité par 2, 5, 10, 100, 1 000",
             "Un nombre est divisible par 2 si son chiffre des unités est 0, 2, 4, 6 ou 8. Il est divisible par 5 si son chiffre des unités est 0 ou 5. Il est divisible par 10 si son chiffre des unités est 0. "
             "Il est divisible par 100 si ses deux derniers chiffres sont 00, et par 1 000 si ses trois derniers chiffres sont 000."),
        rule("Divisibilité par 3 et par 9",
             "Un nombre est divisible par 3 si la somme de ses chiffres est divisible par 3. Il est divisible par 9 si la somme de ses chiffres est divisible par 9."),
        example("Exemple 1", "Pourquoi 4 785 est-il divisible par 5, et 4 780 par 10 ?",
                "Les critères par 2, 5 et 10 viennent du fait que 10, 100 et 1 000 sont des multiples de 2, de 5 et de 10.",
                [("4 785 = 4 × 1 000 + 7 × 100 + 8 × 10 + 5", "On décompose le nombre selon la valeur de ses chiffres."),
                 ("4 × 1 000, 7 × 100 et 8 × 10 sont des multiples de 5", "Car 1 000, 100 et 10 sont des multiples de 5."),
                 ("Il reste le chiffre des unités, 5, qui est un multiple de 5", "Donc 4 785 est un multiple de 5."),
                 ("De même 4 785 = 4 780 + 5 : 4 780 est un multiple de 10, donc de 2 et de 5", "Pour 2, c'est donc le chiffre des unités qui décide : 4 785 est impair.")],
                N("4785") + " est divisible par 5", "4785%5==0 and 4*1000+7*100+8*10+5==4785"),
        example("Exemple 1 bis", "Un nombre est-il divisible par 100 ? par 1 000 ? Étudier 12 000 et 7 450.",
                "Un nombre est divisible par 100 s'il se termine par deux zéros, et par 1 000 s'il se termine par trois zéros.",
                [("12 000 = 12 × 1 000", "C'est un multiple de 1 000, donc aussi de 100."),
                 ("7 450 = 74 × 100 + 50", "50 n'est pas un multiple de 100 : 7 450 n'est pas divisible par 100."),
                 ("7 450 ne se termine pas par trois zéros", "Il n'est pas divisible par 1 000 non plus.")],
                N("12000") + " est divisible par 100 et par 1 000, pas " + N("7450"), "12000%1000==0 and 7450%100!=0 and 7450%1000!=0"),
        example("Exemple 2", "Pourquoi le critère de divisibilité par 3 et 9 marche-t-il ? Étudier 5 439.",
                "On écrit chaque puissance de 10 sous la forme (multiple de 9) + 1.",
                [("10 = 9 + 1 ; 100 = 99 + 1 ; 1 000 = 999 + 1", "99 et 999 sont des multiples de 9 (et de 3)."),
                 ("5 439 = 5 × 999 + 5 + 4 × 99 + 4 + 3 × 9 + 3 + 9", "On remplace 1 000 par 999 + 1, 100 par 99 + 1, 10 par 9 + 1."),
                 ("5 439 = (multiples de 9) + (5 + 4 + 3 + 9)", "Il reste la somme des chiffres, 5 + 4 + 3 + 9 = 21."),
                 ("21 est divisible par 3 mais pas par 9", "Donc 5 439 est divisible par 3 mais pas par 9.")],
                N("5439") + " est divisible par 3 mais pas par 9", "5439%3==0 and 5439%9!=0 and 5+4+3+9==21"),
        example("Exemple 3", "Quels nombres de la liste 135 ; 142 ; 250 ; 99 sont divisibles par 2 ? par 5 ? par 3 ?",
                "On applique chaque critère à chaque nombre.",
                [("Par 2 (chiffre des unités pair) : 142 et 250", "135 et 99 se terminent par 5 et 9."),
                 ("Par 5 (chiffre des unités 0 ou 5) : 135 et 250", "142 et 99 non."),
                 ("Par 3 (somme des chiffres) : 135 (1+3+5=9) et 99 (9+9=18)", "142 (1+4+2=7) et 250 (2+5+0=7) ne sont pas divisibles par 3.")],
                "par 2 : 142, 250 ; par 5 : 135, 250 ; par 3 : 135, 99", "[n for n in (135, 142, 250, 99) if n%2==0]==[142, 250] and [n for n in (135, 142, 250, 99) if n%3==0]==[135, 99]"),
        example("Exemple 4", "Quel chiffre mettre à la place de c pour que le nombre 47c soit divisible par 9 ?",
                "La somme des chiffres doit être un multiple de 9.",
                [("4 + 7 + c = 11 + c", "On additionne les chiffres connus."),
                 ("11 + c doit être un multiple de 9 : le multiple de 9 qui suit 11 est 18", "Car 9 est trop petit et 18 est le premier multiple de 9 supérieur à 11."),
                 ("c = 18 − 11 = 7", "Vérification : 477 = 9 × 53.")],
                "c = " + N("7"), "477%9==0 and 4+7+7==18"),
        warning("Un nombre divisible par 3 n'est pas forcément divisible par 9 : 12 est divisible par 3 (1 + 2 = 3) mais pas par 9. Mais un nombre divisible par 9 est toujours divisible par 3."),
    ],
    [
        choice("s3-g1", "criteres", "Lequel de ces nombres est divisible par 5 ?", ["2 346", "7 205", "8 112", "4 913"], 1, hints=["Regarde le chiffre des unités."], solution=["7 205 se termine par 5."],
               wrong={0: "2 346 se termine par 6.", 2: "8 112 se termine par 2.", 3: "4 913 se termine par 3."}),
        number("s3-g2", "criteres", "Parmi 84 ; 95 ; 126 ; 207 ; 330, combien de nombres sont divisibles par 3 ?", Fraction(4), hints=["Calcule la somme des chiffres de chaque nombre."],
               solution=["84 : 12 oui. 95 : 14 non. 126 : 9 oui. 207 : 9 oui. 330 : 6 oui.", "Il y en a 4."]),
        number("s3-g3", "criteres", "Quel chiffre c faut-il mettre pour que le nombre 52c soit divisible par 3, le plus petit possible ?", Fraction(2), hints=["La somme 5 + 2 + c doit être un multiple de 3."],
               solution=["5 + 2 = 7. Le multiple de 3 suivant est 9, donc c = 2.", "Vérification : 522 = 3 × 174."]),
        choice("s3-g4", "criteres", "Lequel de ces nombres est divisible par 9 ?", ["1 234", "5 239", "9 117", "7 421"], 2, hints=["La somme des chiffres doit être un multiple de 9."],
               solution=["9 117 : 9 + 1 + 1 + 7 = 18, multiple de 9."], wrong={0: "1 + 2 + 3 + 4 = 10, qui n'est pas un multiple de 9.", 1: "5 + 2 + 3 + 9 = 19, qui n'est pas un multiple de 9.", 3: "7 + 4 + 2 + 1 = 14, qui n'est pas un multiple de 9."}),
        number("s3-g5", "criteres", "Parmi 1 200 ; 3 450 ; 7 000 ; 9 100, combien sont divisibles par 100 ?", Fraction(3), hints=["Regarde les deux derniers chiffres."], solution=["1 200, 7 000 et 9 100 se terminent par 00.", "3 450 se termine par 50 : non. Il y en a 3."]),
    ])

PRACTICE = [
    number("p1", "consecutifs", "Quel est l'entier naturel qui suit 2 999 ?", Fraction(3000), 1, ["Ajoute 1."], ["2 999 + 1 = 3 000."]),
    number("p2", "consecutifs", "Combien d'entiers naturels sont strictement compris entre 105 et 120 ?", Fraction(14), 2, ["Différence moins 1."], ["120 − 105 − 1 = 14."]),
    number("p3", "consecutifs", "Combien d'entiers naturels y a-t-il de 200 à 215, ces deux nombres compris ?", Fraction(16), 2, ["Différence plus 1."], ["215 − 200 + 1 = 16."]),
    number("p4", "consecutifs", "Trois entiers consécutifs ont pour somme 87. Quel est le plus petit des trois ?", Fraction(28), 3, ["Les trois nombres sont n, n + 1 et n + 2. Que vaut leur somme ?"], ["La somme est 3 × n + 3 = 87, donc 3 × n = 84 et n = 28.", "28 + 29 + 30 = 87."]),
    choice("p5", "consecutifs", "Quelle écriture est correcte ?", ["$0 \\in \\mathbb{N}$", "$0 \\notin \\mathbb{N}$"], 0, 1, ["0 est le plus petit entier naturel."], ["0 appartient à l'ensemble N."], wrong={1: "L'ensemble N commence à 0."}),
    number("p6", "consecutifs", "Quel est l'entier naturel qui précède 1 ?", Fraction(0), 1, ["Retire 1 à 1."], ["1 − 1 = 0."]),
    number("p7", "multiples", "Quel est le plus petit multiple de 12 supérieur à 100 ?", Fraction(108), 2, ["12 × 8 = 96, 12 × 9 = ?"], ["12 × 8 = 96 est trop petit. 12 × 9 = 108."]),
    number("p8", "multiples", "Combien y a-t-il de multiples de 6 entre 1 et 100 ?", Fraction(16), 2, ["100 ÷ 6 = ?"], ["100 ÷ 6 = 16, reste 4 : il y a 16 multiples de 6 (6 × 16 = 96)."]),
    number("p9", "multiples", "Combien de diviseurs a 30 ?", Fraction(8), 2, ["Cherche les paires."], ["1 × 30, 2 × 15, 3 × 10, 5 × 6.", "Les diviseurs : 1, 2, 3, 5, 6, 10, 15, 30 : il y en a 8."]),
    number("p10", "multiples", "Combien de diviseurs a 17 ?", Fraction(2), 2, ["17 est-il divisible par 2, 3, 4 ?"], ["Seuls 1 et 17 divisent 17 : il y en a 2."]),
    number("p11", "multiples", "Quel est le plus grand diviseur de 84 différent de 84 ?", Fraction(42), 2, ["Divise 84 par son plus petit diviseur autre que 1."], ["84 ÷ 2 = 42."]),
    choice("p12", "multiples", "Le nombre 96 est-il un multiple de 8 ?", ["Oui, car 96 = 8 × 12", "Non, car 96 ÷ 8 n'est pas un entier"], 0, 1, ["Divise 96 par 8."], ["96 ÷ 8 = 12, reste 0."], wrong={1: "96 ÷ 8 = 12 exactement."}),
    number("p13", "multiples", "Un commerçant range 36 mangues en tas égaux de plus d'une mangue, sans reste. Combien de tailles de tas différentes peut-il faire, en comptant le tas de 36 ?", Fraction(8), 3,
           ["Le nombre de mangues par tas est un diviseur de 36 autre que 1."], ["Diviseurs de 36 : 1, 2, 3, 4, 6, 9, 12, 18, 36.", "On enlève 1 : 8 tailles possibles."]),
    number("p14", "multiples", "Deux feux clignotent : l'un toutes les 4 secondes, l'autre toutes les 6 secondes. Ils s'allument ensemble à 0 s. Au bout de combien de secondes s'allument-ils ensemble pour la première fois après 0 s ?", Fraction(12), 3,
           ["Cherche le plus petit multiple commun non nul de 4 et de 6."], ["Multiples de 4 : 4, 8, 12, ... Multiples de 6 : 6, 12, ...", "Le plus petit multiple commun est 12."], units=["s"]),
    choice("p15", "multiples", "Moussa dit : « 5 est un multiple de 15 ». A-t-il raison ?", ["Oui", "Non : 5 est un diviseur de 15, pas un multiple"], 1, 3, ["15 = 5 × 3."], ["15 est un multiple de 5, et 5 est un diviseur de 15. Moussa a mélangé les deux mots."], wrong={0: "Un multiple de 15 est au moins 15 (ou 0)."}),
    choice("p16", "criteres", "Lequel de ces nombres est divisible par 2 ?", ["3 475", "6 218", "9 001", "1 233"], 1, 1, ["Regarde le chiffre des unités."], ["6 218 se termine par 8, un chiffre pair."], wrong={0: "3 475 se termine par 5.", 2: "9 001 se termine par 1.", 3: "1 233 se termine par 3."}),
    number("p17", "criteres", "Parmi 120 ; 225 ; 400 ; 505 ; 710, combien sont divisibles par 10 ?", Fraction(3), 1, ["Le chiffre des unités doit être 0."], ["120, 400 et 710. Il y en a 3."]),
    number("p18", "criteres", "Quel chiffre c faut-il pour que 3c4 soit divisible par 9, le plus petit possible ?", Fraction(2), 3, ["La somme 3 + c + 4 doit être un multiple de 9."], ["3 + 4 = 7. Le multiple de 9 suivant est 9, donc c = 2.", "324 = 9 × 36."]),
    number("p19", "criteres", "Parmi 63 ; 81 ; 104 ; 222 ; 459, combien sont divisibles par 9 ?", Fraction(3), 2, ["Calcule la somme des chiffres de chacun."], ["63 : 9 oui. 81 : 9 oui. 104 : 5 non. 222 : 6 non. 459 : 18 oui.", "Il y en a 3."]),
    number("p20", "criteres", "Parmi 135 ; 250 ; 90 ; 165, combien sont divisibles à la fois par 3 et par 5 ?", Fraction(3), 3, ["Utilise les deux critères."], ["135 : 9 oui, se termine par 5 oui. 250 : 7 non. 90 : 9 oui, se termine par 0 oui. 165 : 12 oui, 5 oui.", "Il y en a 3."]),
    choice("p21", "criteres", "Léa dit : « 123 est divisible par 9 parce que 1 + 2 + 3 = 6 et 6 est divisible par 3 ». Quelle est la bonne réponse ?",
           ["Elle a tort : 6 n'est pas divisible par 9, donc 123 n'est pas divisible par 9", "Elle a raison", "Elle a tort : 123 est divisible par 2"], 0, 3, ["Quel critère faut-il pour 9 ?"], ["Pour 9, la somme des chiffres doit être divisible par 9. 6 ne l'est pas.", "123 est divisible par 3 mais pas par 9."],
           wrong={1: "Le critère par 9 demande une somme de chiffres divisible par 9, pas par 3.", 2: "123 se termine par 3 : il n'est pas divisible par 2."}),
    number("p22", "criteres", "Quel est le plus petit nombre de trois chiffres divisible par 5 et par 9 ?", Fraction(135), 3, ["Il se termine par 0 ou 5 et la somme de ses chiffres est un multiple de 9."], ["Candidats : 100, 105, 110, ... La somme des chiffres doit être 9 ou 18.", "135 : 1 + 3 + 5 = 9 et il se termine par 5 : 135 = 9 × 15."]),
    number("p23", "criteres", "Combien de nombres entre 1 et 50 sont divisibles par 5 ?", Fraction(10), 1, ["5, 10, 15, ..."], ["5 × 10 = 50 : il y en a 10."]),
    number("p25", "consecutifs", "Combien de nombres pairs y a-t-il entre 1 et 20, ces deux nombres compris ?", Fraction(10), 1, ["Un nombre sur deux est pair."], ["2, 4, 6, ..., 20 : 20 ÷ 2 = 10 nombres pairs."]),
    choice("p26", "consecutifs", "Quel nombre est impair ?", ["1 408", "3 615", "250"], 1, 1, ["Regarde le chiffre des unités."], ["3 615 se termine par 5 : il est impair."], wrong={0: "1 408 se termine par 8 : il est pair.", 2: "250 se termine par 0 : il est pair."}),
    number("p27", "criteres", "Parmi 3 000 ; 4 500 ; 6 200 ; 8 000, combien sont divisibles par 1 000 ?", Fraction(2), 2, ["Il faut trois zéros à la fin."], ["3 000 et 8 000 se terminent par trois zéros : 2 nombres."]),
    number("p28", "consecutifs", "Combien de nombres pairs y a-t-il strictement entre 11 et 31 ?", Fraction(10), 2, ["Écris-les : 12, 14, ..."], ["12, 14, 16, 18, 20, 22, 24, 26, 28, 30 : 10 nombres pairs."]),
    number("p29", "multiples", "Quel est le plus grand multiple de 9 inférieur à 100 ?", Fraction(99), 2, ["11 × 9 = 99."], ["9 × 11 = 99 et 9 × 12 = 108 dépasse 100 : c'est 99."]),
    number("p30", "multiples", "Combien de diviseurs a 28 ?", Fraction(6), 3, ["Cherche-les par paires : 1 × 28, 2 × 14, ..."], ["1 × 28, 2 × 14, 4 × 7 : les diviseurs sont 1, 2, 4, 7, 14, 28, soit 6 diviseurs."]),
    number("p24", "criteres", "Quel chiffre c faut-il pour que 6c5 soit divisible par 3, le plus grand possible ?", Fraction(7), 3, ["La somme 6 + c + 5 doit être un multiple de 3."], ["6 + 5 = 11. Les multiples de 3 possibles : 12, 15, 18, ...", "c = 1, 4 ou 7. Le plus grand est 7 : 675 = 3 × 225."]),
]

SUMMARY = [
    definition("Vocabulaire", "N est l'ensemble des entiers naturels. " + "$7 \\in \\mathbb{N}$" + " (appartient) et " + "$2{,}5 \\notin \\mathbb{N}$" + " (n'appartient pas). a est un multiple de b si a = b × k avec k entier ; alors a est divisible par b et b est un diviseur de a."),
    rule("Compter", "Entre a et b (a < b), il y a b − a − 1 entiers si on ne compte pas les extrémités, b − a + 1 si on les compte."),
    rule("Diviseurs", "On cherche les diviseurs par paires en testant 1, 2, 3, ... et on s'arrête quand le diviseur dépasse le quotient. 1 et le nombre sont toujours des diviseurs."),
    rule("Critères", "Par 2 : unités 0, 2, 4, 6, 8. Par 5 : unités 0 ou 5. Par 10 : unités 0. Par 100 : deux derniers chiffres 00. Par 3 ou 9 : somme des chiffres divisible par 3 ou par 9."),
    para("Les erreurs à éviter : confondre multiple et diviseur ; compter les extrémités par erreur ; utiliser le critère de 3 pour 9 ; penser qu'un nombre qui se termine par 5 est divisible par 10."),
]

CONCEPTS = {
    "consecutifs": ("Entiers consécutifs et ensemble N", "consecutifs"),
    "multiples": ("Multiples et diviseurs", "multiples"),
    "criteres": ("Critères de divisibilité", "criteres"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    # 1. strictly between
    a = rng.randint(10, 400)
    b = a + rng.randint(5, 40)
    questions.append(number("a1", "consecutifs", f"Combien d'entiers naturels sont strictement compris entre {a} et {b} ?", Fraction(b - a - 1), 2, ["Différence moins 1."], [f"{b} − {a} = {b - a}.", f"{b - a} − 1 = {b - a - 1}."]))
    # 2. both ends included
    a = rng.randint(10, 400)
    b = a + rng.randint(5, 40)
    questions.append(number("a2", "consecutifs", f"Combien d'entiers naturels y a-t-il de {a} à {b}, ces deux nombres compris ?", Fraction(b - a + 1), 2, ["Différence plus 1."], [f"{b} − {a} = {b - a}.", f"{b - a} + 1 = {b - a + 1}."]))
    # 3. the three consecutive numbers
    n = rng.randint(10, 200)
    questions.append(number("a3", "consecutifs", f"Trois entiers consécutifs ont pour somme {3 * n + 3}. Quel est le plus petit des trois ?", Fraction(n), 3, ["Les trois nombres sont n, n + 1 et n + 2."],
                            [f"Somme = 3 × n + 3 = {3 * n + 3}, donc 3 × n = {3 * n} et n = {n}.", f"{n} + {n + 1} + {n + 2} = {3 * n + 3}."]))
    # 4. smallest multiple above a bound
    k = rng.randint(6, 19)
    bound = rng.randint(50, 200)
    answer = (bound // k + 1) * k
    questions.append(number("a4", "multiples", f"Quel est le plus petit multiple de {k} supérieur à {bound} ?", Fraction(answer), 2, [f"{bound} ÷ {k} = ?"],
                            [f"{bound} ÷ {k} = {bound // k}, reste {bound % k}.", f"{k} × {bound // k} = {k * (bound // k)} est trop petit, {k} × {bound // k + 1} = {answer}."]))
    # 5. number of divisors
    n = rng.choice([12, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 64, 72])
    questions.append(number("a5", "multiples", f"Combien de diviseurs a {n} ?", Fraction(len(divisors(n))), 3, ["Cherche les diviseurs par paires."],
                            ["Les diviseurs de " + str(n) + " : " + ", ".join(map(str, divisors(n))) + f". Il y en a {len(divisors(n))}."]))
    # 6. largest proper divisor
    n = rng.choice([24, 27, 28, 30, 36, 40, 45, 48, 49, 50, 54, 56, 63, 72, 75, 80, 81, 90, 96, 100])
    biggest = max(k for k in divisors(n) if k != n)
    questions.append(number("a6", "multiples", f"Quel est le plus grand diviseur de {n} différent de {n} ?", Fraction(biggest), 3, ["Divise par le plus petit diviseur autre que 1."],
                            [f"Le plus petit diviseur de {n} autre que 1 est {divisors(n)[1]}.", f"{n} ÷ {divisors(n)[1]} = {biggest}."]))
    # 7. which number is a multiple
    k = rng.choice([4, 6, 7, 8, 9, 11, 12, 13])
    multiple = k * rng.randint(5, 20)
    others = set()
    while len(others) < 3:
        candidate = multiple + rng.choice([-3, -2, -1, 1, 2, 3, k + 1, -(k + 1)])
        if candidate % k != 0 and candidate > 0:
            others.add(candidate)
    options = [multiple] + sorted(others)
    order = [0, 1, 2, 3]
    rng.shuffle(order)
    questions.append(choice("a7", "multiples", f"Lequel de ces nombres est un multiple de {k} ?", [str(options[i]) for i in order], order.index(0), 2, [f"Divise chaque nombre par {k}."],
                            [f"{multiple} = {k} × {multiple // k}.", f"Les autres nombres laissent un reste quand on les divise par {k}."]))
    # 8. digit for divisibility by 3
    first, last = rng.randint(1, 9), rng.randint(1, 9)
    total = first + last
    digit = min(c for c in range(10) if (total + c) % 3 == 0 and (total + c) > 0)
    questions.append(number("a8", "criteres", f"Quel chiffre c faut-il pour que le nombre {first}c{last} soit divisible par 3, le plus petit possible ?", Fraction(digit), 3, ["La somme des chiffres doit être un multiple de 3."],
                            [f"{first} + {last} = {total}.", f"Le plus petit chiffre c tel que {total} + c soit un multiple de 3 est {digit}."]))
    # 9. digit for divisibility by 9
    first, last = rng.randint(1, 9), rng.randint(1, 9)
    total = first + last
    digit = min(c for c in range(10) if (total + c) % 9 == 0)
    questions.append(number("a9", "criteres", f"Quel chiffre c faut-il pour que le nombre {first}c{last} soit divisible par 9, le plus petit possible ?", Fraction(digit), 3, ["La somme des chiffres doit être un multiple de 9."],
                            [f"{first} + {last} = {total}.", f"{total} + c doit être un multiple de 9 : le plus petit chiffre est c = {digit}."]))
    # 10. count with two criteria
    pool = rng.sample([n for n in range(100, 700) if n % 5 == 0] + [n for n in range(100, 700) if n % 3 == 0 and n % 5 != 0], 6)
    count = sum(1 for n in pool if n % 15 == 0)
    questions.append(number("a10", "criteres", "Parmi " + " ; ".join(map(str, pool)) + ", combien de nombres sont divisibles à la fois par 3 et par 5 ?", Fraction(count), 3, ["Applique le critère par 5, puis celui par 3."],
                            [", ".join(f"{n} : {'oui' if n % 15 == 0 else 'non'}" for n in pool) + f". Il y en a {count}."]))
    # 11. a sharing problem
    n = rng.choice([24, 30, 36, 40, 42, 48, 60])
    parts = len(divisors(n)) - 1
    questions.append(number("a11", "multiples", f"Un commerçant range {n} oranges en tas égaux de plus d'une orange, sans reste. Combien de tailles de tas différentes peut-il faire, en comptant le tas de {n} ?", Fraction(parts), 3,
                            ["Le nombre d'oranges par tas est un diviseur de " + str(n) + " autre que 1."], ["Diviseurs de " + str(n) + " : " + ", ".join(map(str, divisors(n))) + ".", f"On enlève 1 : {parts} tailles possibles."]))
    # 12. the classic mistake with 3 and 9
    n = rng.choice([12, 15, 21, 24, 30, 33, 42, 51, 57, 60, 66, 69])
    options = [f"Elle a tort : la somme des chiffres de {n} est {digit_sum(n)}, qui n'est pas divisible par 9", f"Elle a raison, car {n} est divisible par 3", f"Elle a tort : {n} n'est divisible par aucun nombre"]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a12", "criteres", f"Awa dit : « {n} est divisible par 9 parce qu'il est divisible par 3 ». A-t-elle raison ?", [options[i] for i in order], order.index(0), 3,
                            ["Quel critère faut-il pour 9 ?"], [f"La somme des chiffres de {n} est {digit_sum(n)}.", f"{digit_sum(n)} n'est pas divisible par 9 : {n} n'est pas divisible par 9."],
                            wrong={order.index(1): "Un nombre divisible par 3 n'est pas forcément divisible par 9.", order.index(2): f"{n} est divisible par 1, par lui-même, et par d'autres nombres."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=8, title="Les entiers naturels : multiples, diviseurs et divisibilité", language="fr",
    intro="Ranger 36 mangues en tas égaux, savoir si un nombre peut se partager en 3 sans reste, deviner si un grand nombre est divisible par 5 : tout cela repose sur les multiples, les diviseurs et les critères de divisibilité. "
          "Ce chapitre t'apprend à les utiliser, et à comprendre pourquoi les critères marchent.",
    objectives=["Utiliser les symboles d'appartenance et d'inclusion avec l'ensemble des entiers naturels.",
                "Trouver des entiers consécutifs et compter les entiers compris entre deux nombres.",
                "Reconnaître un multiple et un diviseur, lister des multiples et tous les diviseurs d'un nombre inférieur à 1 000.",
                "Reconnaître sans diviser si un nombre est divisible par 2, 3, 5, 9, 10, 100 ou 1 000.",
                "Résoudre des problèmes de partage en tas égaux."],
    prerequisites=[{"text": "Multiplier et diviser des nombres entiers."},
                   {"text": "Lire et écrire les nombres entiers et connaître le rang des chiffres."}],
    sections=[S1, S2, S3], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Eighth chapter of the Senegal Sixième course. Its contents follow lesson 9 of the Côte d'Ivoire Sixième programme (consecutive natural numbers, multiples and divisors, divisibility by 2, 3, 5, 9, 10, 100, 1000), which was read for it, "
                "so it is also offered there, but the programme's own situations and activities are not reproduced. It has not been checked against the official Senegalese programme.",
)
