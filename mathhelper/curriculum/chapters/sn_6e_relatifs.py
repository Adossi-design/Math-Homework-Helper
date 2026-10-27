"""Sixième, Les nombres relatifs: the seventh chapter of the Senegal Sixième course, written in French.

The contents follow lesson 10 "Nombres décimaux relatifs" of the Côte d'Ivoire Sixième programme (relative integers and decimals, the opposite of a number,
comparing, adding, the abscissa of a point on a graduated line), which was read for this chapter, and the relative numbers exercises of the ADEM-Dakar
Sixième booklet. Subtraction of relative numbers is not part of this level in the programme and is not taught here.
Every explanation, example and exercise was written independently, with our own numbers.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-6e-relatifs"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")


def signed(value):
    """Write a relative number between parentheses, with its sign, as it appears in a sum."""
    value = Fraction(value)
    text = show(abs(value))
    return f"(+{text})" if value >= 0 else f"(-{text})"


# ----- Section 1: relative numbers, opposites and the graduated line -----
S1 = Section(
    "sens", "Les nombres relatifs, l'opposé et la droite graduée", 24, "sens",
    "Reconnaître des nombres positifs et négatifs, trouver l'opposé d'un nombre et lire ou placer un point sur une droite graduée.",
    [
        para("Il fait 4 °C à Dakar, mais la température de l'eau d'un congélateur est de 18 degrés en dessous de zéro. Une altitude peut être 120 m au-dessus de la mer ou 40 m en dessous. "
             "Pour écrire ces nombres, les entiers naturels ne suffisent pas : on a besoin de nombres avec un signe. Le signe + dit « au-dessus de zéro », le signe − dit « en dessous de zéro »."),
        definition("Nombres relatifs",
                   "Un nombre relatif est un nombre précédé d'un signe : positif (+) ou négatif (−). Par exemple " + N("+3") + ", " + N("-2,5") + " et " + N("-18") + ". "
                   "On écrit souvent un nombre positif sans le signe + : " + N("+3") + " et " + N("3") + " sont le même nombre. Le nombre 0 n'est ni positif ni négatif. "
                   "Les entiers relatifs forment l'ensemble " + "$\\mathbb{Z}$" + " : " + N("... -3, -2, -1, 0, 1, 2, 3 ...") + ". Un nombre relatif peut aussi être décimal, comme " + N("-2,5") + "."),
        definition("L'opposé d'un nombre",
                   "Deux nombres relatifs qui ont la même partie sans signe et des signes contraires sont opposés. L'opposé de " + N("5") + " est " + N("-5") + ", l'opposé de " + N("-3,5") + " est " + N("3,5") + ". "
                   "L'opposé de 0 est 0. La somme de deux nombres opposés est 0 : " + N("5 + (-5) = 0") + "."),
        definition("Droite graduée et abscisse",
                   "Sur une droite graduée, on choisit un point origine O associé au nombre 0 et une unité de longueur. Les nombres positifs sont placés à droite de O, les nombres négatifs à gauche. "
                   "Le nombre associé à un point s'appelle son abscisse. Deux points d'abscisses opposées sont à la même distance de O, de part et d'autre de O."),
        example("Exemple 1", "Sur une droite graduée de 1 en 1, le point A est à 3 graduations à gauche de O et le point B à 4 graduations à droite de O. Quelles sont leurs abscisses ?",
                "À gauche de O, les nombres sont négatifs. À droite, ils sont positifs.",
                [("A est à gauche de O, à 3 graduations", "Son abscisse est négative et sa distance à O est 3 : " + N("-3") + "."),
                 ("B est à droite de O, à 4 graduations", "Son abscisse est positive : " + N("+4") + ", qu'on écrit " + N("4") + "."),
                 ("A et B ne sont pas à la même distance de O", "Ce n'est pas le cas de deux points d'abscisses opposées, comme -3 et 3.")],
                "A a pour abscisse " + N("-3") + " et B a pour abscisse " + N("4"), "-3 < 0 < 4"),
        example("Exemple 2", "Placer le point C d'abscisse " + N("-2,5") + " sur une droite graduée de 0,5 en 0,5.",
                "On part de O, on va vers la gauche, et on compte les graduations de 0,5.",
                [("Chaque graduation vaut 0,5", "Pour aller jusqu'à 2,5 il faut 2,5 ÷ 0,5 = 5 graduations."),
                 ("Le nombre est négatif : on va 5 graduations à gauche de O", "-2,5 est entre -3 et -2, à égale distance des deux."),
                 ("Le point C est à 5 graduations à gauche de O", "Vérification : son opposé 2,5 serait à 5 graduations à droite.")],
                "C est à 5 graduations à gauche de O.", "d('2,5')/d('0,5')==5"),
        example("Exemple 3", "Donner l'opposé de " + N("7") + ", de " + N("-3,5") + " et de " + N("0") + ".",
                "L'opposé garde la même partie sans signe, mais change de signe.",
                [("L'opposé de " + N("7") + " est " + N("-7"), "7 est positif : son opposé est négatif."),
                 ("L'opposé de " + N("-3,5") + " est " + N("3,5"), "-3,5 est négatif : son opposé est positif."),
                 ("L'opposé de " + N("0") + " est " + N("0"), "0 n'a pas de signe.")],
                N("-7") + " ; " + N("3,5") + " ; " + N("0"), "-7+7==0 and d('-3,5')+d('3,5')==0"),
        example("Exemple 4", "Dans la liste " + N("12") + ", " + N("-3") + ", " + N("0") + ", " + N("4,5") + ", " + N("-0,8") + ", combien de nombres sont des entiers relatifs négatifs ?",
                "Un entier relatif négatif est un entier avec le signe moins : il ne doit pas avoir de partie décimale.",
                [("12 est un entier positif", "Il n'est pas négatif."),
                 ("-3 est un entier négatif", "Il compte."),
                 ("0 n'est ni positif ni négatif ; 4,5 est positif et décimal ; -0,8 est négatif mais décimal", "Aucun de ces trois nombres ne compte."),
                 ("Il y a un seul entier relatif négatif : " + N("-3"), "Les entiers sont -3, 0 et 12, et un seul d'entre eux est négatif.")],
                "Un seul : " + N("-3"), "sum(1 for x in (12, -3, 0, d('4,5'), d('-0,8')) if x < 0 and x == int(x))==1"),
        warning("Le signe − devant un nombre n'est pas une soustraction : " + N("-3") + " est un nombre, à gauche de zéro sur la droite graduée. Et ne mélange pas -3 et 3 : ils sont opposés, pas égaux."),
    ],
    [
        number("s1-g1", "sens", "Quel est l'opposé de " + N("-7") + " ?", Fraction(7), hints=["L'opposé a le signe contraire."], solution=["L'opposé de -7 est 7."]),
        number("s1-g2", "sens", "Quel est l'opposé de " + N("4,5") + " ?", d("-4,5"), hints=["Le nombre est positif : quel signe pour son opposé ?"], solution=["L'opposé de 4,5 est -4,5."]),
        number("s1-g3", "sens", "Sur une droite graduée de 1 en 1, le point A est à 3 graduations à gauche de O. Quelle est son abscisse ?", Fraction(-3),
               hints=["À gauche de O, les abscisses sont négatives."], solution=["A est à gauche de O : son abscisse est négative.", "Il est à 3 graduations, donc son abscisse est -3."]),
        choice("s1-g4", "sens", "Quel nombre est un entier relatif négatif ?", [N("5"), N("-5"), N("-2,5"), N("0")], 1,
               hints=["Il faut un signe moins et aucune partie décimale."], solution=["-5 est négatif et entier.", "5 est positif, -2,5 est décimal, 0 n'est ni positif ni négatif."],
               wrong={2: "-2,5 est négatif, mais ce n'est pas un entier : il a une partie décimale.", 3: "0 n'est ni positif ni négatif."}),
        number("s1-g5", "sens", "La température est de 3 °C en dessous de zéro. Écris-la comme un nombre relatif.", Fraction(-3),
               hints=["En dessous de zéro : quel signe ?"], solution=["En dessous de zéro, le nombre est négatif : -3 °C."]),
    ])

# ----- Section 2: comparing relative numbers -----
S2 = Section(
    "comparer", "Comparer des nombres relatifs", 22, "comparer",
    "Comparer et ranger des nombres relatifs, en s'aidant de la droite graduée.",
    [
        para("Quelle température est la plus froide : -7 °C ou -2 °C ? Beaucoup pensent -2 °C parce que 2 est plus petit que 7. Mais -7 °C est plus loin sous zéro : il fait plus froid à -7 °C. "
             "Pour comparer des nombres relatifs, on s'aide de la droite graduée : le plus grand nombre est celui qui est le plus à droite."),
        rule("Règles de comparaison",
             "Un nombre négatif est plus petit que 0, et 0 est plus petit qu'un nombre positif. Donc tout nombre négatif est plus petit que tout nombre positif. "
             "Deux nombres positifs se comparent comme d'habitude. Deux nombres négatifs se comparent à l'envers : le plus grand est celui qui a la plus petite partie sans signe (il est le plus proche de 0)."),
        example("Exemple 1", "Comparer " + N("-3") + " et " + N("2") + ", puis " + N("-7") + " et " + N("-2") + ".",
                "On utilise les règles : négatif contre positif, puis deux négatifs.",
                [(N("-3 < 2"), "-3 est négatif, 2 est positif : tout négatif est plus petit que tout positif."),
                 ("Parties sans signe : 7 et 2 ; 7 est plus grand que 2", "Pour deux négatifs, c'est l'inverse."),
                 (N("-7 < -2"), "-7 est plus loin de 0 à gauche que -2 : il est plus petit.")],
                N("-3 < 2") + " et " + N("-7 < -2"), "-3<2 and -7<-2"),
        example("Exemple 2", "Comparer " + N("-2,5") + " et " + N("-2,05") + ".",
                "Pour deux négatifs, on compare d'abord les parties sans signe, 2,5 et 2,05, comme des décimaux positifs.",
                [(N("2,5") + " = " + N("2,50"), "On donne le même nombre de chiffres après la virgule."),
                 ("2,50 est plus grand que 2,05", "50 centièmes sont plus que 5 centièmes."),
                 (N("-2,5 < -2,05"), "Pour des négatifs, on inverse : le nombre qui a la plus grande partie sans signe est le plus petit.")],
                N("-2,5 < -2,05"), "d('-2,5')<d('-2,05')"),
        example("Exemple 3", "Ranger dans l'ordre croissant : " + N("-4") + ", " + N("0") + ", " + N("2,5") + ", " + N("-0,5") + ", " + N("-4,5") + ".",
                "On sépare les négatifs, 0 et les positifs, puis on range les négatifs en comparant leurs parties sans signe à l'envers.",
                [("Les négatifs : -4 ; -0,5 ; -4,5", "Parties sans signe : 4 ; 0,5 ; 4,5."),
                 ("Du plus petit au plus grand : -4,5 puis -4 puis -0,5", "Plus la partie sans signe est grande, plus le nombre est petit."),
                 (N("-4,5 < -4 < -0,5 < 0 < 2,5"), "Ensuite 0, puis le positif 2,5.")],
                N("-4,5 < -4 < -0,5 < 0 < 2,5"), "d('-4,5')<-4<d('-0,5')<0<d('2,5')"),
        example("Exemple 4", "Quel est le plus petit entier relatif plus grand que " + N("-3") + " ?",
                "Sur la droite graduée de 1 en 1, on avance d'un cran vers la droite à partir de -3.",
                [("À droite de -3 se trouve -2", "Un entier relatif de plus."),
                 (N("-3 < -2"), "-2 est donc le plus petit entier relatif plus grand que -3.")],
                N("-2"), "-3<-2 and -2-(-3)==1"),
        warning("Ne confonds pas « plus grand » et « plus loin de zéro » : " + N("-8") + " est plus loin de zéro que " + N("-3") + ", mais il est plus petit. Sur la droite, le plus grand est à droite."),
    ],
    [
        choice("s2-g1", "comparer", "Quel signe faut-il entre " + N("-8") + " et " + N("-3") + " ?", [N("-8 < -3"), N("-8 > -3"), N("-8 = -3")], 0,
               hints=["Compare les parties sans signe, puis inverse."], solution=["8 est plus grand que 3, donc -8 est plus petit que -3.", "-8 < -3."],
               wrong={1: "Pour deux négatifs c'est l'inverse : -8 est plus loin à gauche de 0 que -3, donc plus petit."}),
        ordered("s2-g2", "comparer", "Range dans l'ordre croissant, en séparant par des points-virgules : " + N("-2") + " ; " + N("1,5") + " ; " + N("-4") + " ; " + N("0") + ".",
                [Fraction(-4), Fraction(-2), Fraction(0), d("1,5")],
                hints=["Commence par les négatifs, du plus petit au plus grand, puis 0, puis les positifs."], solution=["Les négatifs : -4 est plus petit que -2.", "-4 < -2 < 0 < 1,5."]),
        number("s2-g3", "comparer", "Quel est le plus petit de ces trois nombres : " + N("-0,3") + ", " + N("-0,03") + ", " + N("-3") + " ?", Fraction(-3),
               hints=["Parmi des négatifs, le plus petit a la plus grande partie sans signe."], solution=["Parties sans signe : 0,3 ; 0,03 ; 3. La plus grande est 3.", "Le plus petit nombre est -3."]),
        between("s2-g4", "comparer", "Écris un nombre décimal relatif compris entre " + N("-2") + " et " + N("-1") + ".", Fraction(-2), Fraction(-1),
                hints=["Il est négatif. Sa partie sans signe est entre 1 et 2."], solution=["Tout nombre de -1,9 à -1,1 convient, par exemple -1,5."]),
        number("s2-g5", "comparer", "Quel est le plus petit entier relatif plus grand que " + N("-7") + " ?", Fraction(-6),
               hints=["Avance d'un cran vers la droite à partir de -7."], solution=["À droite de -7 se trouve -6.", "-7 < -6."]),
    ])

# ----- Section 3: adding relative numbers -----
S3 = Section(
    "addition", "Additionner des nombres relatifs", 28, "addition",
    "Additionner deux nombres relatifs de même signe ou de signes contraires, et résoudre des problèmes avec des gains et des pertes.",
    [
        para("Une équipe de football marque 3 buts et en encaisse 1 : son goal-différentiel est +2. Au match suivant, elle marque 1 but et en encaisse 4 : son goal-différentiel est -3. Après les deux matchs, son bilan est " + N("(+2) + (-3)") + ". "
             "Ajouter des nombres relatifs, c'est cumuler des gains (positifs) et des pertes (négatifs). On peut aussi le voir sur la droite graduée : ajouter un nombre positif fait avancer vers la droite, ajouter un négatif fait reculer vers la gauche."),
        rule("Additionner deux nombres de même signe",
             "La somme garde le signe commun, et sa partie sans signe est la somme des parties sans signe. " + N("(+3) + (+4) = +7") + " et " + N("(-3) + (-4) = -7") + " : deux pertes font une plus grande perte."),
        rule("Additionner deux nombres de signes contraires",
             "La somme a le signe du nombre qui a la plus grande partie sans signe, et sa partie sans signe est la différence des deux parties sans signe (la plus grande moins la plus petite). "
             + N("(-7) + (+4) = -3") + " : 7 − 4 = 3 et le signe est celui de -7. Si les parties sans signe sont égales, la somme est 0 : deux opposés."),
        example("Exemple 1", "Calculer " + N("(-3) + (-4)") + ".",
                "Même signe : on garde le signe − et on additionne 3 et 4.",
                [("Les deux nombres sont négatifs", "Deux pertes : 3 puis 4."),
                 (N("3 + 4") + " = " + N("7"), "On additionne les parties sans signe."),
                 (N("(-3) + (-4)") + " = " + N("-7"), "On garde le signe commun, −."),
                 ("Sur la droite graduée : de 0 on recule de 3 puis de 4", "On arrive à -7.")],
                N("-7"), "-3+(-4)==-7"),
        example("Exemple 2", "Calculer " + N("(-7) + (+4)") + ".",
                "Signes contraires : on compare les parties sans signe, 7 et 4.",
                [("Parties sans signe : 7 et 4. La plus grande est 7, celle de -7", "Le signe de la somme sera le signe de -7, c'est-à-dire −."),
                 (N("7 - 4") + " = " + N("3"), "La partie sans signe de la somme est 7 − 4 = 3."),
                 (N("(-7) + (+4)") + " = " + N("-3"), "Sur la droite : de 0 on recule de 7, puis on avance de 4 : on arrive à -3.")],
                N("-3"), "-7+4==-3"),
        example("Exemple 3", "Calculer " + N("6 + (-6)") + " et " + N("(-2,5) + 1,5") + ".",
                "Dans le premier cas, les deux nombres sont opposés. Dans le second, les signes sont contraires.",
                [(N("6 + (-6)") + " = " + N("0"), "Deux nombres opposés ont une somme égale à 0 : on avance de 6 puis on recule de 6."),
                 ("Pour " + N("(-2,5) + 1,5") + " : parties sans signe 2,5 et 1,5, la plus grande est 2,5 (négative)", "Le signe est −."),
                 (N("2,5 - 1,5") + " = " + N("1") + " donc " + N("(-2,5) + 1,5") + " = " + N("-1"), "On soustrait les parties sans signe, puis on met le signe −.")],
                N("0") + " et " + N("-1"), "6+(-6)==0 and d('-2,5')+d('1,5')==-1"),
        example("Exemple 4", "Un tournoi de football : lors du premier match, une équipe marque 3 buts et en encaisse 1. Lors du second, elle marque 1 but et en encaisse 4. Quel est son goal-différentiel total ?",
                "Le goal-différentiel d'un match est le nombre de buts marqués moins le nombre de buts encaissés. On additionne ensuite les deux résultats.",
                [("Match 1 : 3 − 1 = +2", "Elle a marqué plus qu'elle n'a encaissé : positif."),
                 ("Match 2 : 1 − 4 = -3", "Elle a encaissé plus qu'elle n'a marqué : négatif."),
                 (N("(+2) + (-3)") + " : parties sans signe 2 et 3, la plus grande est 3 (négative)", "Signes contraires."),
                 (N("3 - 2") + " = " + N("1") + " donc le total est " + N("-1"), "Son goal-différentiel total est -1.")],
                "Le goal-différentiel total est " + N("-1") + ".", "(3-1)+(1-4)==-1"),
        example("Exemple 5", "Le matin, la température est de -3 °C. Elle monte de 5 °C. Quelle est la nouvelle température ?",
                "Monter de 5 degrés, c'est ajouter +5.",
                [(N("(-3) + (+5)"), "Signes contraires : parties sans signe 3 et 5, la plus grande est 5 (positive)."),
                 (N("5 - 3") + " = " + N("2"), "La somme est positive : +2."),
                 ("Sur la droite : de -3 on avance de 5 : on passe par 0 puis on arrive à 2", "La température est de 2 °C.")],
                "La température est " + N("2") + " °C.", "-3+5==2"),
        warning("Ne soustrais pas à la place d'additionner quand les signes sont les mêmes : " + N("(-3) + (-4) = -7") + " et non " + N("-1") + ". Et pour deux signes contraires, regarde bien quelle partie sans signe est la plus grande : " + N("(-7) + 4 = -3") + " mais " + N("7 + (-4) = +3") + "."),
    ],
    [
        number("s3-g1", "addition", "Calcule " + N("(-5) + (-2)") + ".", Fraction(-7), hints=["Même signe : que fait-on des parties sans signe ?"], solution=["Deux négatifs : 5 + 2 = 7 et le signe est −.", "(-5) + (-2) = -7."]),
        number("s3-g2", "addition", "Calcule " + N("(-9) + (+4)") + ".", Fraction(-5), hints=["Signes contraires : quelle partie sans signe est la plus grande ?"], solution=["9 est plus grand que 4, et 9 est la partie sans signe de -9 : le signe est −.", "9 − 4 = 5, donc (-9) + 4 = -5."]),
        number("s3-g3", "addition", "Calcule " + N("6 + (-10)") + ".", Fraction(-4), hints=["Quelle partie sans signe est la plus grande, celle de 6 ou celle de -10 ?"], solution=["10 est plus grand que 6 : le signe est celui de -10, donc −.", "10 − 6 = 4, donc 6 + (-10) = -4."]),
        number("s3-g4", "addition", "Calcule " + N("(-3,5) + (+3,5)") + ".", Fraction(0), hints=["Ces deux nombres ont quelque chose de particulier."], solution=["-3,5 et 3,5 sont opposés : leur somme est 0."]),
        number("s3-g5", "addition", "Awa a une dette de 1 500 F, puis elle reçoit 4 000 F. Quelle est sa situation, en F ? (Une dette est un nombre négatif.)", Fraction(2500), units=["F"],
               hints=["Écris la dette comme un nombre négatif, puis additionne."], solution=["Dette : -1 500. Gain : +4 000.", "(-1 500) + 4 000 = 2 500 : Awa a 2 500 F."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "sens", "Quel est l'opposé de " + N("-12") + " ?", Fraction(12), 1, ["Change le signe."], ["L'opposé de -12 est 12."]),
    number("p2", "sens", "Quel est l'opposé de " + N("3,8") + " ?", d("-3,8"), 1, ["Change le signe."], ["L'opposé de 3,8 est -3,8."]),
    number("p3", "sens", "Sur une droite graduée de 1 en 1, le point B est à 5 graduations à droite de O. Quelle est son abscisse ?", Fraction(5), 1, ["À droite, les nombres sont positifs."], ["5."]),
    number("p4", "sens", "Sur une droite graduée de 0,5 en 0,5, un point est à 7 graduations à gauche de O. Quelle est son abscisse ?", d("-3,5"), 2, ["Chaque graduation vaut 0,5. L'abscisse est négative."], ["7 × 0,5 = 3,5, à gauche donc négatif : -3,5."]),
    number("p5", "sens", "Un plongeur est à 12 m sous le niveau de la mer. Écris sa position comme un nombre relatif, en m.", Fraction(-12), 1, ["Sous le niveau de la mer : quel signe ?"], ["Sous le niveau de la mer, c'est négatif : -12 m."], units=["m"]),
    number("p6", "sens", "Dans la liste 15 ; -7 ; 0 ; -2,5 ; 8 ; -1 ; 3,6, combien de nombres sont des entiers relatifs négatifs ?", Fraction(2), 2, ["Il faut un signe − et aucune partie décimale."], ["-7 et -1 sont des entiers négatifs. -2,5 est négatif mais décimal.", "Il y en a 2."]),
    number("p7", "sens", "Quel est l'opposé de l'opposé de " + N("-4,2") + " ?", d("-4,2"), 3, ["Calcule l'opposé de -4,2, puis l'opposé du résultat."], ["L'opposé de -4,2 est 4,2.", "L'opposé de 4,2 est -4,2 : on revient au nombre de départ."]),
    choice("p8", "sens", "Quelle affirmation est vraie ?", ["0 est un nombre positif", "0 n'est ni positif ni négatif", "0 est un nombre négatif"], 1, 2, ["Pense au rôle de 0 sur la droite graduée."], ["0 est l'origine : ni positif ni négatif."],
           wrong={0: "0 est à l'origine, il n'est pas du côté positif.", 2: "0 est à l'origine, il n'est pas du côté négatif."}),
    choice("p9", "comparer", "Quel signe faut-il entre " + N("-5") + " et " + N("2") + " ?", [N("-5 < 2"), N("-5 > 2"), N("-5 = 2")], 0, 1, ["Tout négatif est plus petit que tout positif."], ["-5 < 2."],
           wrong={1: "Un nombre négatif est toujours plus petit qu'un nombre positif."}),
    choice("p10", "comparer", "Quel signe faut-il entre " + N("-1,2") + " et " + N("-1,02") + " ?", [N("-1,2 < -1,02"), N("-1,2 > -1,02"), N("-1,2 = -1,02")], 0, 2, ["Compare 1,2 et 1,02, puis inverse."], ["1,2 = 1,20 est plus grand que 1,02, donc -1,2 est plus petit que -1,02."],
           wrong={1: "Pour deux négatifs, le plus grand est celui qui a la plus petite partie sans signe."}),
    ordered("p11", "comparer", "Range dans l'ordre croissant, en séparant par des points-virgules : " + N("3") + " ; " + N("-1") + " ; " + N("-6") + " ; " + N("0") + " ; " + N("-0,5") + ".",
            [Fraction(-6), Fraction(-1), d("-0,5"), Fraction(0), Fraction(3)], 2, ["Négatifs d'abord, du plus petit au plus grand."], ["-6 < -1 < -0,5 < 0 < 3."]),
    ordered("p12", "comparer", "Range dans l'ordre décroissant, en séparant par des points-virgules : " + N("-2,5") + " ; " + N("-2") + " ; " + N("-2,05") + " ; " + N("0,2") + ".",
            [d("0,2"), Fraction(-2), d("-2,05"), d("-2,5")], 3, ["Le positif est le plus grand. Pour les négatifs, compare les parties sans signe 2 ; 2,05 ; 2,5."], ["0,2 est positif : le plus grand.", "Négatifs : -2 > -2,05 > -2,5, car 2 < 2,05 < 2,5."]),
    number("p13", "comparer", "Quel est le plus grand entier relatif plus petit que " + N("-4") + " ?", Fraction(-5), 2, ["Avance d'un cran vers la gauche à partir de -4."], ["À gauche de -4 se trouve -5."]),
    choice("p14", "comparer", "Une ville a une température de -9 °C et une autre de -4 °C. Laquelle est la plus froide ?", ["La première, -9 °C", "La seconde, -4 °C"], 0, 2, ["Le plus petit nombre est la température la plus basse."], ["-9 < -4 : -9 °C est plus bas, donc plus froid."],
           wrong={1: "-4 est plus grand que -9 : il fait moins froid à -4 °C."}),
    between("p15", "comparer", "Écris un nombre décimal relatif compris entre " + N("-0,5") + " et " + N("-0,4") + ".", d("-0,5"), d("-0,4"), 3, ["Utilise des centièmes."], ["Tout nombre de -0,49 à -0,41 convient, par exemple -0,45."]),
    number("p16", "addition", "Calcule " + N("(-4) + (-6)") + ".", Fraction(-10), 1, ["Même signe."], ["4 + 6 = 10, signe − : -10."]),
    number("p17", "addition", "Calcule " + N("(+8) + (-3)") + ".", Fraction(5), 1, ["Signes contraires."], ["8 − 3 = 5, signe de 8 : +5."]),
    number("p18", "addition", "Calcule " + N("(-8) + (+3)") + ".", Fraction(-5), 1, ["Signes contraires."], ["8 − 3 = 5, signe de -8 : -5."]),
    number("p19", "addition", "Calcule " + N("(-2,5) + (-1,5)") + ".", Fraction(-4), 2, ["Même signe : additionne 2,5 et 1,5."], ["2,5 + 1,5 = 4, signe − : -4."]),
    number("p20", "addition", "Calcule " + N("(-0,8) + (+1,3)") + ".", d("0,5"), 2, ["1,3 est plus grand que 0,8."], ["1,3 − 0,8 = 0,5, signe de 1,3 : +0,5."]),
    number("p21", "addition", "Calcule " + N("(-7,5) + (+2,25)") + ".", d("-5,25"), 3, ["7,5 est plus grand que 2,25."], ["7,5 − 2,25 = 5,25, signe de -7,5 : -5,25."]),
    number("p22", "addition", "Calcule " + N("(-12) + 12") + ".", Fraction(0), 1, ["Deux opposés."], ["La somme de deux nombres opposés est 0."]),
    number("p23", "addition", "Calcule " + N("(-5) + 8 + (-6)") + ".", Fraction(-3), 3, ["Va de gauche à droite : (-5) + 8, puis le résultat + (-6)."], ["(-5) + 8 = 3.", "3 + (-6) = -3."]),
    number("p24", "addition", "Une équipe a marqué 4 buts et encaissé 2 au premier match, puis marqué 0 et encaissé 3 au second. Quel est son goal-différentiel total ?", Fraction(-1), 3,
           ["Calcule le goal-différentiel de chaque match, puis additionne."], ["Match 1 : 4 − 2 = +2. Match 2 : 0 − 3 = -3.", "(+2) + (-3) = -1."]),
    number("p25", "addition", "La température est de -6 °C le matin et monte de 9 °C. Quelle est la température, en °C ?", Fraction(3), 2, ["Monter de 9, c'est ajouter +9."], ["(-6) + 9 = 3 °C."], units=["°C"]),
    number("p26", "addition", "Moussa doit 2 000 F à un ami et reçoit 1 200 F de sa mère qu'il donne à l'ami. Quelle est la situation de Moussa avec son ami, en F ? (Une dette est négative.)", Fraction(-800), 3,
           ["Dette -2 000, paiement +1 200."], ["(-2 000) + 1 200 = -800 : il lui doit encore 800 F."], units=["F"]),
    choice("p27", "addition", "Léa a calculé " + N("(-3) + (-4) = -1") + ". Quelle est son erreur ?", ["Elle a soustrait les parties sans signe au lieu de les additionner", "Elle a oublié le signe", "Elle a ajouté 3 et 4 et trouvé 1"], 0, 2,
           ["Deux pertes font une perte plus grande."], ["Deux nombres négatifs : on additionne les parties sans signe, 3 + 4 = 7.", "(-3) + (-4) = -7."]),
    choice("p28", "addition", "Quelle est la valeur de " + N("(-9) + 5") + " ?", [N("4"), N("-4"), N("-14")], 1, 1, ["La plus grande partie sans signe est 9, celle d'un négatif."], ["9 − 5 = 4, signe −."],
           wrong={0: "Le signe est celui du nombre qui a la plus grande partie sans signe : c'est -9, donc le résultat est négatif.", 2: "-14 serait la somme de (-9) et (-5), deux négatifs."}),
    number("p29", "addition", "Un sous-marin est à 40 m sous l'eau. Il remonte de 15 m puis redescend de 10 m. Quelle est sa position finale, en m ? (Sous l'eau = négatif.)", Fraction(-35), 3,
           ["Position -40, puis +15, puis -10."], ["(-40) + 15 = -25.", "(-25) + (-10) = -35 m."], units=["m"]),
    number("p30", "addition", "Calcule " + N("(-1,75) + (-0,25) + 3") + ".", Fraction(1), 3, ["Additionne d'abord les deux négatifs."], ["(-1,75) + (-0,25) = -2.", "(-2) + 3 = 1."]),
]

SUMMARY = [
    definition("Nombres relatifs", "Un nombre relatif est un nombre avec un signe, + ou −. Les entiers relatifs forment l'ensemble " + "$\\mathbb{Z}$" + ". 0 n'est ni positif ni négatif. L'opposé d'un nombre a la même partie sans signe et le signe contraire ; la somme de deux opposés est 0."),
    rule("Droite graduée", "Les nombres positifs sont à droite de l'origine, les négatifs à gauche. L'abscisse d'un point est le nombre associé à ce point. Le plus grand de deux nombres est celui qui est le plus à droite."),
    rule("Comparer", "Tout négatif est plus petit que 0, et 0 est plus petit que tout positif. Deux négatifs se comparent à l'envers : le plus grand est celui qui a la plus petite partie sans signe."),
    rule("Additionner", "Même signe : on garde le signe et on additionne les parties sans signe. Signes contraires : le signe est celui de la plus grande partie sans signe, et on soustrait la petite de la grande."),
    para("Les erreurs à éviter : prendre -8 plus grand que -3 ; soustraire au lieu d'additionner pour deux nombres de même signe ; oublier de regarder la plus grande partie sans signe ; confondre un signe moins et une soustraction."),
]

CONCEPTS = {
    "sens": ("Nombres relatifs, opposé, droite graduée", "sens"),
    "comparer": ("Comparer des nombres relatifs", "comparer"),
    "addition": ("Additionner des nombres relatifs", "addition"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []

    def sample(low, high, places):
        value = rand_decimal(rng, low, high, places) if places else Fraction(rng.randint(low, high))
        return -value if rng.random() < 0.5 else value

    # 1. opposite
    x = sample(1, 40, rng.choice([0, 1]))
    questions.append(number("a1", "sens", "Quel est l'opposé de " + N(show(x)) + " ?", -x, 1, ["Change le signe."], [f"L'opposé de {show(x)} est {show(-x)}."]))
    # 2. abscissa from graduations
    unit, count = rng.choice([(Fraction(1), 3), (Fraction(1), 5), (Fraction(1, 2), 7), (Fraction(2), 4), (Fraction(1, 2), 9)])
    left = rng.random() < 0.5
    value = -unit * count if left else unit * count
    side = "gauche" if left else "droite"
    questions.append(number("a2", "sens", f"Sur une droite graduée de {show(unit)} en {show(unit)}, un point est à {count} graduations à {side} de l'origine O. Quelle est son abscisse ?", value, 2,
                            ["À gauche de O les abscisses sont négatives, à droite elles sont positives."],
                            [f"Chaque graduation vaut {show(unit)}, donc la distance à O est {count} × {show(unit)} = {show(unit * count)}.", f"Le point est à {side} de O : abscisse {show(value)}."]))
    # 3. compare two relative numbers
    while True:
        a, b = sample(1, 30, rng.choice([0, 1])), sample(1, 30, rng.choice([0, 1]))
        if a != b:
            break
    right = 0 if a < b else 1
    options = [N(f"{show(a)} < {show(b)}"), N(f"{show(a)} > {show(b)}"), N(f"{show(a)} = {show(b)}")]
    questions.append(choice("a3", "comparer", "Quel signe faut-il entre " + N(show(a)) + " et " + N(show(b)) + " ?", options, right, 2, ["Pense à la droite graduée : le plus grand est à droite."],
                            [f"{show(a)} est {'plus petit' if a < b else 'plus grand'} que {show(b)}."], wrong={1 - right: "Pense à la droite graduée : le plus grand nombre est le plus à droite."}))
    # 4. order four numbers
    values = set()
    while len(values) < 4:
        values.add(sample(1, 20, rng.choice([0, 1])))
    ascending = sorted(values)
    shuffled = ascending[:]
    rng.shuffle(shuffled)
    questions.append(ordered("a4", "comparer", "Range dans l'ordre croissant, en séparant par des points-virgules : " + " ; ".join(N(show(v)) for v in shuffled) + ".", ascending, 3,
                            ["Les négatifs sont plus petits que les positifs. Entre négatifs, c'est à l'envers."], ["Dans l'ordre croissant : " + " < ".join(show(v) for v in ascending) + "."]))
    # 5. smallest of three negatives
    triple = set()
    while len(triple) < 3:
        triple.add(-rand_decimal(rng, 0, 9, rng.choice([1, 2])))
    triple = sorted(triple)
    options = [N(show(v)) for v in triple]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a5", "comparer", "Quel est le plus petit de ces trois nombres ?", [options[i] for i in order], order.index(0), 3, ["Parmi des négatifs, le plus petit a la plus grande partie sans signe."],
                            [f"Parties sans signe : {' ; '.join(show(abs(v)) for v in triple)}.", f"La plus grande est {show(abs(triple[0]))} : le plus petit nombre est {show(triple[0])}."],
                            wrong={order.index(2): "C'est le plus grand des trois, car il est le plus proche de 0."}))
    # 6. same sign
    a, b = rng.randint(1, 20), rng.randint(1, 20)
    sign = rng.choice([-1, 1])
    questions.append(number("a6", "addition", "Calcule " + N(f"{signed(sign * a)} + {signed(sign * b)}") + ".", Fraction(sign * (a + b)), 1, ["Même signe : on additionne les parties sans signe et on garde le signe."],
                            [f"{a} + {b} = {a + b}, signe {'−' if sign < 0 else '+'} : {sign * (a + b)}."]))
    # 7. opposite signs
    a, b = rng.randint(1, 20), rng.randint(1, 20)
    if a == b:
        b += 1
    first_negative = rng.random() < 0.5
    x, y = (-a, b) if first_negative else (a, -b)
    questions.append(number("a7", "addition", "Calcule " + N(f"{signed(x)} + {signed(y)}") + ".", Fraction(x + y), 2, ["Signes contraires : le signe est celui de la plus grande partie sans signe."],
                            [f"La plus grande partie sans signe est {max(a, b)}, celle de {show(x if a > b else y)}.", f"{max(a, b)} − {min(a, b)} = {abs(x + y)}, donc {show(x + y)}."]))
    # 8. decimals
    x, y = sample(1, 9, 1), sample(1, 9, 1)
    questions.append(number("a8", "addition", "Calcule " + N(f"{signed(x)} + {signed(y)}") + ".", x + y, 2, ["Regarde les signes : même signe ou signes contraires ?"],
                            [f"{show(x)} + {show(y)} = {show(x + y)}."]))
    # 9. three terms
    x, y, z = rng.randint(1, 15), rng.randint(1, 15), rng.randint(1, 15)
    sx, sy, sz = rng.choice([-1, 1]), rng.choice([-1, 1]), rng.choice([-1, 1])
    questions.append(number("a9", "addition", "Calcule " + N(f"{signed(sx * x)} + {signed(sy * y)} + {signed(sz * z)}") + ".", Fraction(sx * x + sy * y + sz * z), 3,
                            ["Additionne de gauche à droite : les deux premiers, puis le troisième."],
                            [f"{show(sx * x)} + {show(sy * y)} = {show(sx * x + sy * y)}.", f"{show(sx * x + sy * y)} + {show(sz * z)} = {show(sx * x + sy * y + sz * z)}."]))
    # 10. a temperature problem
    start, change = -rng.randint(2, 12), rng.randint(3, 18)
    if rng.random() < 0.5:
        questions.append(number("a10", "addition", f"La température est de {start} °C le matin. Elle monte de {change} °C. Quelle est la nouvelle température, en °C ?", Fraction(start + change), 2,
                                ["Monter de n degrés, c'est ajouter +n."], [f"({start}) + {change} = {start + change} °C."], units=["°C"]))
    else:
        questions.append(number("a10", "addition", f"La température est de {abs(start)} °C. Elle baisse de {abs(start) + change} °C. Quelle est la nouvelle température, en °C ?", Fraction(-change), 2,
                                ["Baisser de n degrés, c'est ajouter -n."], [f"{abs(start)} + (-{abs(start) + change}) = {-change} °C."], units=["°C"]))
    # 11. goal difference over several matches
    matches = [(rng.randint(0, 5), rng.randint(0, 5)) for _ in range(3)]
    total = sum(for_ - against for for_, against in matches)
    text = ", ".join(f"{for_} marqués et {against} encaissés" for for_, against in matches)
    questions.append(number("a11", "addition", f"Une équipe joue trois matchs : {text}. Quel est son goal-différentiel total ? (buts marqués moins buts encaissés)", Fraction(total), 3,
                            ["Calcule le goal-différentiel de chaque match, puis additionne les trois nombres relatifs."],
                            ["Goal-différentiels : " + " ; ".join(show(Fraction(for_ - against)) for for_, against in matches) + ".", f"Total : {total}."]))
    # 12. the classic mistake with negatives
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    while a == b:
        b = rng.randint(2, 9)
    low, high = sorted((-a, -b))
    options = [f"Il a tort : {low} est plus petit que {high}, car {abs(low)} est plus grand que {abs(high)}", f"Il a raison : {abs(low)} est plus grand que {abs(high)}", "Il a tort : -a et -b sont égaux"]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a12", "comparer", f"Moussa dit : « {low} est plus grand que {high}, parce que {abs(low)} est plus grand que {abs(high)} ». A-t-il raison ?", [options[i] for i in order], order.index(0), 3,
                            ["Place les deux nombres sur la droite graduée."], [f"Sur la droite graduée, {low} est plus à gauche que {high}.", f"Donc {low} < {high} : pour deux négatifs, c'est à l'envers."],
                            wrong={order.index(1): "Pour deux nombres négatifs, la comparaison est à l'envers : le plus grand est celui qui est le plus proche de 0.", order.index(2): "Ces deux nombres sont différents."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=7, title="Les nombres relatifs", language="fr",
    intro="La température sous zéro, l'altitude sous le niveau de la mer, une dette, le bilan d'une équipe de football : certaines quantités ont besoin d'un signe. "
          "Ce chapitre t'apprend à lire et à placer les nombres relatifs, à les comparer et à les additionner.",
    objectives=["Reconnaître des nombres entiers et décimaux relatifs, positifs et négatifs, et donner l'opposé d'un nombre.",
                "Lire et placer un point d'abscisse donnée sur une droite régulièrement graduée.",
                "Comparer et ranger des nombres relatifs.",
                "Additionner deux nombres relatifs, de même signe ou de signes contraires.",
                "Résoudre des problèmes avec des gains, des pertes et des températures."],
    prerequisites=[{"text": "Comparer et ranger des nombres décimaux positifs.", "chapter": "sn-6e-decimaux"},
                   {"text": "Additionner et soustraire des nombres entiers.", "course": "whole-numbers", "lesson": "add-subtract"}],
    sections=[S1, S2, S3], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Seventh chapter of the Senegal Sixième course. Its contents follow lesson 10 of the Côte d'Ivoire Sixième programme (relative integers and decimals, opposite, comparing, adding, abscissa on a graduated line), which was read for it, "
                "so it is also offered there, but the programme's own situations and activities are not reproduced. It has not been checked against the official Senegalese programme.",
)
