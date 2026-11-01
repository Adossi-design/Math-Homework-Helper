"""Cinquième, Nombres décimaux relatifs: the second chapter of the Senegal Cinquième course, written in French.

The contents follow lesson 2 "Nombres décimaux relatifs" of the Côte d'Ivoire Cinquième programme (compare and order relative decimal numbers, the difference, the algebraic sum,
the product, and the equation x + b = a), which was read for this chapter. Every explanation, example and exercise was written independently, with our own numbers.
It builds on the Sixième chapter on relative numbers, which only adds. Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation,
and each worked example carries a "verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-5e-relatifs"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")


def rel(value):
    """Write a relative number between parentheses with its sign, as math."""
    value = Fraction(value)
    return f"({'-' if value < 0 else '+'}{show(abs(value)).replace(',', '{,}')})"


def plain(value):
    """Write a relative number as math, with a decimal comma and a minus sign when negative."""
    value = Fraction(value)
    return ("-" if value < 0 else "") + show(abs(value)).replace(",", "{,}")


# ----- Section 1: subtracting and comparing -----
S1 = Section(
    "difference", "Soustraire des nombres relatifs, comparer et ranger", 24, "difference",
    "Soustraire un nombre relatif en ajoutant son opposé, calculer un écart, et comparer et ranger des décimaux relatifs.",
    [
        para("En classe de Sixième, tu as appris à additionner des nombres relatifs. Pour comparer deux températures, par exemple 8 °C le jour et -5 °C la nuit, on veut aussi savoir de combien elles diffèrent : "
             "c'est une soustraction. Une soustraction de nombres relatifs se transforme toujours en addition."),
        rule("Soustraire, c'est ajouter l'opposé",
             "Pour soustraire un nombre relatif, on ajoute son opposé : " + N("a - b = a + (-b)") + ". Par exemple " + N("(+7) - (+10) = (+7) + (-10) = -3") + " et " + N("(-4) - (-9) = (-4) + (+9) = +5") + ". "
             "Le résultat d'une soustraction s'appelle la différence."),
        rule("Comparer et ranger",
             "Tout nombre négatif est plus petit que 0 et que tout nombre positif. Entre deux nombres négatifs, le plus petit est celui qui a la plus grande partie sans signe : " + N("-3,25 < -3,2") + ". "
             "Ranger dans l'ordre croissant, c'est écrire du plus petit au plus grand ; dans l'ordre décroissant, du plus grand au plus petit."),
        example("Exemple 1", "Calculer " + N("(+7) - (+10)") + ".",
                "On remplace la soustraction par l'addition de l'opposé.",
                [("L'opposé de +10 est -10", "On change le signe du deuxième nombre."),
                 (N("(+7) + (-10)") + " = " + N("-3"), "Signes contraires : 10 − 7 = 3, avec le signe de la plus grande partie sans signe.")],
                N("-3") + ".", "7-10==-3"),
        example("Exemple 2", "Calculer " + N("(-4) - (-9)") + ".",
                "Soustraire -9, c'est ajouter son opposé +9.",
                [("L'opposé de -9 est +9", "On change le signe."),
                 (N("(-4) + (+9)") + " = " + N("5"), "Signes contraires : 9 − 4 = 5, avec le signe de 9.")],
                N("5") + ".", "-4-(-9)==5"),
        example("Exemple 3", "Calculer " + N("(-2,5) - (+1,5)") + ".",
                "Même méthode avec des décimaux.",
                [(N("(-2,5) + (-1,5)"), "L'opposé de +1,5 est -1,5."),
                 (N("-2,5 - 1,5") + " = " + N("-4"), "Même signe : on additionne 2,5 et 1,5 et on garde le signe moins.")],
                N("-4") + ".", "d('-2,5')-d('1,5')==-4"),
        example("Exemple 4", "Ranger dans l'ordre croissant les nombres " + N("-3,2") + ", " + N("-3,02") + ", " + N("3,2") + " et " + N("-3,25") + ".",
                "On sépare les négatifs du positif, puis on compare les parties sans signe des négatifs.",
                [("Négatifs : -3,25 ; -3,2 ; -3,02", "Parties sans signe 3,25 ; 3,20 ; 3,02 : la plus grande est 3,25."),
                 ("Le plus petit est -3,25, puis -3,2, puis -3,02", "Entre négatifs, c'est à l'envers."),
                 ("Le positif 3,2 est le plus grand", "Tout positif est plus grand que tout négatif.")],
                N("-3,25 < -3,2 < -3,02 < 3,2") + ".", "d('-3,25')<d('-3,2')<d('-3,02')<d('3,2')"),
        example("Exemple 5", "La température maximale est de 8 °C et la température minimale de -5 °C. Quel est l'écart entre les deux ?",
                "L'écart est la différence entre la plus grande et la plus petite valeur.",
                [(N("8 - (-5)"), "Grande valeur moins petite valeur."),
                 (N("8 + 5") + " = " + N("13"), "Soustraire -5, c'est ajouter +5.")],
                "L'écart est de " + N("13") + " °C.", "8-(-5)==13"),
        warning("Soustraire un nombre négatif fait augmenter : " + N("5 - (-2) = 7") + " et non 3. Et ne confonds pas le signe moins de la soustraction avec le signe moins du nombre : dans " + N("(-4) - (-9)") + ", il y a trois signes moins, qui ne jouent pas le même rôle."),
    ],
    [
        number("s1-g1", "difference", "Calcule " + N("(+5) - (+9)") + ".", Fraction(-4), hints=["Ajoute l'opposé de +9."], solution=["(+5) + (-9) = -4."]),
        number("s1-g2", "difference", "Calcule " + N("(-6) - (-2)") + ".", Fraction(-4), hints=["L'opposé de -2 est +2."], solution=["(-6) + (+2) = -4."]),
        number("s1-g3", "difference", "Calcule " + N("(-1,5) - (+2)") + ".", d("-3,5"), hints=["L'opposé de +2 est -2."], solution=["(-1,5) + (-2) = -3,5."]),
        number("s1-g4", "difference", "La température maximale est de 12 °C et la minimale de -7 °C. Quel est l'écart, en °C ?", Fraction(19), units=["°C"], hints=["Grande valeur moins petite valeur."], solution=["12 − (−7) = 12 + 7 = 19 °C."]),
        ordered("s1-g5", "difference", "Range dans l'ordre croissant : -2 ; 1,5 ; -2,5 ; 0. Écris les nombres séparés par des points-virgules.", [d("-2,5"), Fraction(-2), Fraction(0), d("1,5")],
                hints=["Les négatifs d'abord, du plus grand au plus petit en valeur absolue."], solution=["-2,5 < -2 < 0 < 1,5."]),
    ])

# ----- Section 2: algebraic sum -----
S2 = Section(
    "somme", "La somme algébrique", 22, "somme",
    "Supprimer les parenthèses dans une suite d'additions et de soustractions de nombres relatifs, puis calculer en regroupant les positifs et les négatifs.",
    [
        para("Une suite d'additions et de soustractions de nombres relatifs s'appelle une somme algébrique. On la simplifie en supprimant les parenthèses, ce qui donne une écriture plus courte et plus facile à calculer."),
        rule("Supprimer les parenthèses",
             "Ajouter un nombre positif, ou soustraire un nombre négatif, revient à ajouter la partie sans signe : " + N("a + (+b) = a + b") + " et " + N("a - (-b) = a + b") + ". "
             "Ajouter un nombre négatif, ou soustraire un nombre positif, revient à soustraire la partie sans signe : " + N("a + (-b) = a - b") + " et " + N("a - (+b) = a - b") + "."),
        rule("Calculer une somme algébrique",
             "Après avoir supprimé les parenthèses, on additionne tous les nombres précédés de + (les termes positifs), on additionne tous les nombres précédés de - (les termes négatifs), puis on calcule la différence des deux totaux avec le signe du plus grand."),
        example("Exemple 1", "Calculer " + N("(+8) + (-3) - (-5) - (+2)") + ".",
                "On supprime les parenthèses, puis on regroupe.",
                [(N("8 - 3 + 5 - 2"), "+(-3) devient -3 ; -(-5) devient +5 ; -(+2) devient -2."),
                 ("Positifs : 8 + 5 = 13. Négatifs : 3 + 2 = 5", "On regroupe les termes de même signe."),
                 (N("13 - 5") + " = " + N("8"), "On fait la différence.")],
                N("8") + ".", "8-3+5-2==8"),
        example("Exemple 2", "Calculer " + N("-7 + 4 - 9 + 6") + ".",
                "Il n'y a pas de parenthèses : on regroupe directement.",
                [("Positifs : 4 + 6 = 10", "Les termes précédés de +."),
                 ("Négatifs : 7 + 9 = 16", "Les termes précédés de -."),
                 (N("10 - 16") + " = " + N("-6"), "Le plus grand total est celui des négatifs : le résultat est négatif.")],
                N("-6") + ".", "-7+4-9+6==-6"),
        example("Exemple 3", "Calculer " + N("-2,5 + 4,1 - 1,6") + ".",
                "Même méthode avec des décimaux.",
                [("Positifs : 4,1", "Un seul terme positif."),
                 ("Négatifs : 2,5 + 1,6 = 4,1", "Deux termes négatifs."),
                 (N("4,1 - 4,1") + " = " + N("0"), "Les deux totaux sont égaux : le résultat est 0.")],
                N("0") + ".", "d('-2,5')+d('4,1')-d('1,6')==0"),
        example("Exemple 4", "Sur un compte, on a enregistré : +2 000 F, -3 500 F, +1 200 F, -800 F. Quel est le total ?",
                "Le total est la somme algébrique de ces nombres.",
                [("Positifs : 2 000 + 1 200 = 3 200", "Les dépôts."),
                 ("Négatifs : 3 500 + 800 = 4 300", "Les retraits."),
                 (N("3200 - 4300") + " = " + N("-1100"), "Le compte est en négatif de 1 100 F.")],
                "Le total est de " + N("-1100") + " F.", "2000-3500+1200-800==-1100"),
        warning("Ne mélange pas les signes : " + N("a - (-b)") + " donne " + N("a + b") + ", pas " + N("a - b") + ". Et quand tu regroupes, fais attention à ne pas oublier le signe d'un terme : dans " + N("5 - 8 + 3") + ", le 8 est négatif, pas positif."),
    ],
    [
        number("s2-g1", "somme", "Calcule " + N("6 - 9 + 4") + ".", Fraction(1), hints=["Positifs : 6 + 4. Négatifs : 9."], solution=["10 − 9 = 1."]),
        number("s2-g2", "somme", "Calcule " + N("(-3) + (-5) - (-8)") + ".", Fraction(0), hints=["Supprime les parenthèses : -3 - 5 + 8."], solution=["-3 − 5 + 8 = 0."]),
        number("s2-g3", "somme", "Calcule " + N("-2,5 + 1,75 - 0,25") + ".", Fraction(-1), hints=["Positifs : 1,75. Négatifs : 2,5 + 0,25."], solution=["2,5 + 0,25 = 2,75.", "1,75 − 2,75 = -1."]),
        number("s2-g4", "somme", "Calcule " + N("12 - (+7) + (-6)") + ".", Fraction(-1), hints=["Supprime les parenthèses : 12 - 7 - 6."], solution=["12 − 7 − 6 = -1."]),
        choice("s2-g5", "somme", "Quelle écriture simplifiée est égale à " + N("(-4) - (-6) + (+2)") + " ?", [N("-4 + 6 + 2"), N("-4 - 6 + 2"), N("-4 - 6 - 2")], 0,
               hints=["- (-6) devient + 6 et + (+2) devient + 2."], solution=["-4 + 6 + 2 = 4."], wrong={1: "Soustraire -6 revient à ajouter 6.", 2: "Ajouter +2 revient à ajouter 2."}),
    ])

# ----- Section 3: product -----
S3 = Section(
    "produit", "Le produit de nombres relatifs", 24, "produit",
    "Calculer le produit de deux ou plusieurs nombres relatifs avec la règle des signes.",
    [
        para("Perdre 500 F chaque jour pendant 3 jours fait perdre 1 500 F : " + N("3 \\times (-500) = -1500") + ". Et si on enlève 3 jours de pertes de 500 F, on gagne 1 500 F : " + N("(-3) \\times (-500) = +1500") + ". Ces situations expliquent la règle des signes."),
        rule("Règle des signes",
             "Le produit de deux nombres de même signe est positif : " + N("(+3) \\times (+4) = +12") + " et " + N("(-3) \\times (-4) = +12") + ". Le produit de deux nombres de signes contraires est négatif : " + N("(+3) \\times (-4) = -12") + ". "
             "On calcule d'abord le signe, puis le produit des parties sans signe."),
        rule("Plusieurs facteurs",
             "Dans un produit de plusieurs nombres non nuls, le résultat est positif s'il y a un nombre pair de facteurs négatifs, et négatif s'il y en a un nombre impair. Un produit dont un facteur est nul vaut 0."),
        example("Exemple 1", "Calculer " + N("(+3) \\times (+4)") + ", " + N("(-3) \\times (-4)") + " et " + N("(+3) \\times (-4)") + ".",
                "On cherche le signe avec la règle, puis on multiplie les parties sans signe.",
                [("(+3) × (+4) : même signe, positif", N("3 \\times 4") + " = " + N("12") + "."),
                 ("(-3) × (-4) : même signe, positif", N("3 \\times 4") + " = " + N("12") + "."),
                 ("(+3) × (-4) : signes contraires, négatif", N("3 \\times 4") + " = 12, donc " + N("-12") + ".")],
                N("12") + ", " + N("12") + " et " + N("-12") + ".", "3*4==12 and (-3)*(-4)==12 and 3*(-4)==-12"),
        example("Exemple 2", "Calculer " + N("(-2,5) \\times (+4)") + ".",
                "Signes contraires : le produit est négatif.",
                [(N("2,5 \\times 4") + " = " + N("10"), "Produit des parties sans signe."),
                 ("Signes contraires : négatif", "Le résultat est -10.")],
                N("-10") + ".", "d('-2,5')*4==-10"),
        example("Exemple 3", "Calculer " + N("(-2) \\times (-3) \\times (-5)") + ".",
                "On compte les facteurs négatifs : il y en a 3, un nombre impair.",
                [("3 facteurs négatifs : le résultat est négatif", "Nombre impair de facteurs négatifs."),
                 (N("2 \\times 3 \\times 5") + " = " + N("30"), "Produit des parties sans signe.")],
                N("-30") + ".", "(-2)*(-3)*(-5)==-30"),
        example("Exemple 4", "Calculer " + N("(-1,5) \\times (-2) \\times (+4)") + ".",
                "Deux facteurs négatifs : un nombre pair, donc le résultat est positif.",
                [(N("1,5 \\times 2") + " = " + N("3"), "Premier produit."),
                 (N("3 \\times 4") + " = " + N("12"), "Second produit."),
                 ("Nombre pair de facteurs négatifs : positif", "Le résultat est +12.")],
                N("12") + ".", "d('-1,5')*(-2)*4==12"),
        warning("La règle des signes pour le produit ne s'applique pas à la somme : " + N("(-3) + (-4) = -7") + " mais " + N("(-3) \\times (-4) = +12") + ". "
                "Et un produit avec un facteur nul vaut 0, même s'il y a des facteurs négatifs : " + N("(-5) \\times 0 \\times (-2) = 0") + "."),
    ],
    [
        number("s3-g1", "produit", "Calcule " + N("(-6) \\times (+3)") + ".", Fraction(-18), hints=["Signes contraires."], solution=["6 × 3 = 18, négatif : -18."]),
        number("s3-g2", "produit", "Calcule " + N("(-4) \\times (-5)") + ".", Fraction(20), hints=["Même signe."], solution=["4 × 5 = 20, positif : 20."]),
        number("s3-g3", "produit", "Calcule " + N("(-2,5) \\times (-4)") + ".", Fraction(10), hints=["Même signe."], solution=["2,5 × 4 = 10, positif."]),
        number("s3-g4", "produit", "Calcule " + N("(-1) \\times (-1) \\times (-1) \\times (-1) \\times (-1)") + ".", Fraction(-1), hints=["Combien de facteurs négatifs ?"], solution=["5 facteurs négatifs, un nombre impair : -1."]),
        choice("s3-g5", "produit", "Quel est le signe de " + N("(-7) \\times (-2) \\times (+3) \\times (-1)") + " ?", ["Positif", "Négatif", "Nul"], 1,
               hints=["Compte les facteurs négatifs."], solution=["Il y a 3 facteurs négatifs, un nombre impair : le produit est négatif."], wrong={0: "Avec 3 facteurs négatifs, le produit est négatif.", 2: "Aucun facteur n'est nul."}),
    ])

# ----- Section 4: equations -----
S4 = Section(
    "equation", "Résoudre une équation du type x + b = a", 24, "equation",
    "Résoudre une équation du type x + b = a avec des nombres relatifs, vérifier la solution et résoudre un petit problème.",
    [
        para("Une température a baissé de 6 °C et elle est maintenant de -2 °C. Quelle était-elle avant ? On cherche un nombre x tel que " + N("x + (-6) = -2") + ". C'est une équation : une égalité avec un nombre inconnu x."),
        rule("Résoudre " + "x + b = a",
             "Pour trouver x dans " + N("x + b = a") + ", on retire b des deux côtés : " + N("x = a - b") + ". On vérifie en remplaçant x par la valeur trouvée : on doit retrouver a. "
             "Si l'équation est " + N("x - b = a") + ", on ajoute b : " + N("x = a + b") + "."),
        example("Exemple 1", "Résoudre " + N("x + 5 = 2") + ".",
                "On retire 5 des deux côtés.",
                [(N("x = 2 - 5"), "x + 5 = 2 donne x = 2 − 5."),
                 (N("2 - 5") + " = " + N("-3"), "Le résultat est négatif."),
                 ("Vérification : " + N("-3 + 5") + " = " + N("2"), "On retrouve le second membre.")],
                N("x = -3") + ".", "2-5==-3 and -3+5==2"),
        example("Exemple 2", "Résoudre " + N("x + (-4) = 7") + ".",
                "On retire -4 des deux côtés, c'est-à-dire qu'on ajoute 4.",
                [(N("x = 7 - (-4)") + " = " + N("7 + 4"), "Soustraire -4, c'est ajouter 4."),
                 (N("7 + 4") + " = " + N("11"), "Le résultat est 11."),
                 ("Vérification : " + N("11 + (-4)") + " = " + N("7"), "On retrouve 7.")],
                N("x = 11") + ".", "7-(-4)==11 and 11+(-4)==7"),
        example("Exemple 3", "Résoudre " + N("x - 2,5 = -1") + ".",
                "On ajoute 2,5 des deux côtés.",
                [(N("x = -1 + 2,5"), "x − 2,5 = −1 donne x = −1 + 2,5."),
                 (N("-1 + 2,5") + " = " + N("1,5"), "Signes contraires : 2,5 − 1 = 1,5, positif."),
                 ("Vérification : " + N("1,5 - 2,5") + " = " + N("-1"), "On retrouve -1.")],
                N("x = 1,5") + ".", "d('-1')+d('2,5')==d('1,5') and d('1,5')-d('2,5')==-1"),
        example("Exemple 4", "Une température a baissé de 6 °C et elle est maintenant de -2 °C. Quelle était la température avant ?",
                "On écrit l'équation x + (-6) = -2, puis on la résout.",
                [(N("x + (-6) = -2"), "La baisse de 6 °C s'écrit +(-6)."),
                 (N("x = -2 - (-6)") + " = " + N("-2 + 6") + " = " + N("4"), "On ajoute 6 des deux côtés.")],
                "Avant, la température était de " + N("4") + " °C.", "-2-(-6)==4 and 4+(-6)==-2"),
        warning("Vérifie toujours ta solution en la remplaçant dans l'équation : c'est le seul moyen d'être sûr, surtout avec des nombres négatifs. Et ne confonds pas " + N("x + 5 = 2") + " (où l'on soustrait 5) avec " + N("x - 5 = 2") + " (où l'on ajoute 5)."),
    ],
    [
        number("s4-g1", "equation", "Résous " + N("x + 3 = 1") + ".", Fraction(-2), hints=["x = 1 − 3."], solution=["x = 1 − 3 = -2.", "Vérification : -2 + 3 = 1."]),
        number("s4-g2", "equation", "Résous " + N("x + (-5) = -9") + ".", Fraction(-4), hints=["x = -9 − (-5)."], solution=["x = -9 + 5 = -4.", "Vérification : -4 + (-5) = -9."]),
        number("s4-g3", "equation", "Résous " + N("x - 1,5 = 2") + ".", d("3,5"), hints=["Ajoute 1,5."], solution=["x = 2 + 1,5 = 3,5."]),
        number("s4-g4", "equation", "On retire 8 à un nombre x et on obtient -3 : x - 8 = -3. Quel est x ?", Fraction(5), hints=["Ajoute 8."], solution=["x = -3 + 8 = 5."]),
        number("s4-g5", "equation", "Résous " + N("x + 7 = 0") + ".", Fraction(-7), hints=["x est l'opposé de 7."], solution=["x = 0 − 7 = -7."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "difference", "Calcule " + N("(+9) - (+14)") + ".", Fraction(-5), 1, ["Ajoute l'opposé."], ["9 + (-14) = -5."]),
    number("p2", "difference", "Calcule " + N("(-3) - (+8)") + ".", Fraction(-11), 1, ["Ajoute l'opposé de +8."], ["(-3) + (-8) = -11."]),
    number("p3", "difference", "Calcule " + N("(-7) - (-12)") + ".", Fraction(5), 1, ["L'opposé de -12 est +12."], ["-7 + 12 = 5."]),
    number("p4", "difference", "Calcule " + N("(+4,5) - (-1,5)") + ".", Fraction(6), 2, ["L'opposé de -1,5 est +1,5."], ["4,5 + 1,5 = 6."]),
    number("p5", "difference", "Calcule " + N("(-0,8) - (-2,3)") + ".", d("1,5"), 2, ["-0,8 + 2,3."], ["-0,8 + 2,3 = 1,5."]),
    number("p6", "difference", "À midi il fait 15 °C et à minuit -4 °C. Quel est l'écart de température, en °C ?", Fraction(19), 1, ["Grande valeur moins petite valeur."], ["15 − (−4) = 19 °C."], units=["°C"]),
    number("p7", "difference", "Un plongeur est à -18 m et un oiseau à 25 m au-dessus de l'eau. Quelle distance les sépare, en m ?", Fraction(43), 2, ["25 − (−18)."], ["25 + 18 = 43 m."], units=["m"]),
    ordered("p8", "difference", "Range dans l'ordre croissant : 0,5 ; -1 ; -1,2 ; 1 ; -0,1. Écris les nombres séparés par des points-virgules.", [d("-1,2"), Fraction(-1), d("-0,1"), d("0,5"), Fraction(1)], 2, ["Les négatifs d'abord."], ["-1,2 < -1 < -0,1 < 0,5 < 1."]),
    ordered("p9", "difference", "Range dans l'ordre décroissant : -4 ; 3,5 ; -3,5 ; 0. Écris les nombres séparés par des points-virgules.", [d("3,5"), Fraction(0), d("-3,5"), Fraction(-4)], 2, ["Du plus grand au plus petit."], ["3,5 > 0 > -3,5 > -4."]),
    choice("p10", "difference", "Quel est le plus petit de ces nombres ?", [N("-0,5"), N("-0,05"), N("-0,55"), N("0")], 2, 2, ["Parmi les négatifs, le plus petit a la plus grande partie sans signe."], ["Parties sans signe 0,5 ; 0,05 ; 0,55 : la plus grande est 0,55."], wrong={0: "-0,5 est plus grand que -0,55.", 1: "-0,05 est le plus grand des négatifs.", 3: "0 est plus grand que les négatifs."}),
    number("p11", "somme", "Calcule " + N("5 - 12 + 4") + ".", Fraction(-3), 1, ["Positifs : 5 + 4. Négatifs : 12."], ["9 − 12 = -3."]),
    number("p12", "somme", "Calcule " + N("-8 + 3 - 2 + 10") + ".", Fraction(3), 1, ["Positifs : 3 + 10. Négatifs : 8 + 2."], ["13 − 10 = 3."]),
    number("p13", "somme", "Calcule " + N("(-4) + (+9) - (-3)") + ".", Fraction(8), 2, ["-4 + 9 + 3."], ["-4 + 9 + 3 = 8."]),
    number("p14", "somme", "Calcule " + N("(+6) - (+8) - (-5) + (-2)") + ".", Fraction(1), 2, ["6 - 8 + 5 - 2."], ["11 − 10 = 1."]),
    number("p15", "somme", "Calcule " + N("-3,2 + 5,7 - 1,5") + ".", Fraction(1), 2, ["Positifs : 5,7. Négatifs : 3,2 + 1,5."], ["5,7 − 4,7 = 1."]),
    number("p16", "somme", "Calcule " + N("2,4 - 3,9 + 0,5") + ".", Fraction(-1), 2, ["Positifs : 2,4 + 0,5. Négatifs : 3,9."], ["2,9 − 3,9 = -1."]),
    number("p17", "somme", "Un compte enregistre +5 000 F, -2 500 F, -1 800 F et +700 F. Quel est le total, en F ?", Fraction(1400), 2, ["Somme algébrique."], ["5 000 + 700 = 5 700 et 2 500 + 1 800 = 4 300.", "5 700 − 4 300 = 1 400 F."], units=["F"]),
    number("p18", "somme", "Un ascenseur part de l'étage -1, monte de 6 étages, descend de 4, puis monte de 3. À quel étage est-il ?", Fraction(4), 3, ["-1 + 6 - 4 + 3."], ["-1 + 6 = 5, 5 − 4 = 1, 1 + 3 = 4."]),
    choice("p19", "somme", "Quelle écriture simplifiée est égale à " + N("5 - (-3) + (-2)") + " ?", [N("5 + 3 - 2"), N("5 - 3 - 2"), N("5 - 3 + 2")], 0, 2, ["- (-3) devient + 3."], ["5 + 3 − 2 = 6."], wrong={1: "Soustraire -3 revient à ajouter 3.", 2: "Ajouter -2 revient à soustraire 2."}),
    number("p20", "produit", "Calcule " + N("(-7) \\times (+6)") + ".", Fraction(-42), 1, ["Signes contraires."], ["7 × 6 = 42, négatif."]),
    number("p21", "produit", "Calcule " + N("(-8) \\times (-9)") + ".", Fraction(72), 1, ["Même signe."], ["8 × 9 = 72, positif."]),
    number("p22", "produit", "Calcule " + N("(+0,5) \\times (-12)") + ".", Fraction(-6), 2, ["Signes contraires."], ["0,5 × 12 = 6, négatif."]),
    number("p23", "produit", "Calcule " + N("(-1,5) \\times (-1,5)") + ".", d("2,25"), 2, ["Même signe."], ["1,5 × 1,5 = 2,25, positif."]),
    number("p24", "produit", "Calcule " + N("(-2) \\times (-3) \\times (-4)") + ".", Fraction(-24), 2, ["3 facteurs négatifs."], ["2 × 3 × 4 = 24, négatif."]),
    number("p25", "produit", "Calcule " + N("(-5) \\times (-2) \\times (+3) \\times (-1)") + ".", Fraction(-30), 3, ["3 facteurs négatifs."], ["5 × 2 × 3 × 1 = 30, négatif."]),
    number("p26", "produit", "Calcule " + N("(-6) \\times 0 \\times (-2,5)") + ".", Fraction(0), 1, ["Un facteur est nul."], ["Un produit avec un facteur nul vaut 0."]),
    number("p27", "produit", "Une machine perd 3,5 L d'eau par heure. Quelle est la variation du volume en 4 heures, en L ?", Fraction(-14), 2, ["La perte est -3,5 par heure."], ["4 × (−3,5) = −14 L."], units=["L"]),
    choice("p28", "produit", "Quel est le signe de " + N("(-3) \\times (-3)") + " ?", ["Positif", "Négatif", "Nul"], 0, 1, ["Même signe."], ["Deux facteurs négatifs : produit positif, 9."], wrong={1: "Deux négatifs donnent un positif.", 2: "Aucun facteur n'est nul."}),
    choice("p29", "produit", "Léa dit : « (-3) + (-4) = 12 comme (-3) × (-4) ». Quelle est son erreur ?", ["Elle confond la somme et le produit : (-3) + (-4) = -7", "Elle a oublié le signe de 12", "Elle a mélangé 3 et 4"], 0, 3, ["La règle des signes est pour le produit."], ["Pour la somme de deux négatifs, on additionne et on garde le signe moins : -7."], wrong={1: "12 est bien le produit.", 2: "Les nombres sont corrects."}),
    number("p30", "equation", "Résous " + N("x + 8 = 3") + ".", Fraction(-5), 1, ["x = 3 − 8."], ["x = -5.", "Vérification : -5 + 8 = 3."]),
    number("p31", "equation", "Résous " + N("x + (-3) = 10") + ".", Fraction(13), 2, ["x = 10 + 3."], ["x = 13.", "Vérification : 13 + (-3) = 10."]),
    number("p32", "equation", "Résous " + N("x - 4 = -6") + ".", Fraction(-2), 2, ["Ajoute 4."], ["x = -6 + 4 = -2.", "Vérification : -2 - 4 = -6."]),
    number("p33", "equation", "Résous " + N("x + 2,5 = 1") + ".", d("-1,5"), 2, ["x = 1 − 2,5."], ["x = -1,5.", "Vérification : -1,5 + 2,5 = 1."]),
    number("p34", "equation", "Résous " + N("x - (-3) = 5") + ".", Fraction(2), 3, ["x - (-3) = x + 3."], ["x + 3 = 5, donc x = 2."]),
    number("p35", "equation", "Après une baisse de 9 °C, la température est de -3 °C. Quelle était-elle avant, en °C ?", Fraction(6), 2, ["x + (-9) = -3."], ["x = -3 + 9 = 6 °C."], units=["°C"]),
    number("p36", "equation", "Un plongeur est à -15 m. Il remonte de x mètres et se trouve à -4 m. Quelle est la valeur de x, en m ?", Fraction(11), 3, ["-15 + x = -4."], ["x = -4 − (-15) = -4 + 15 = 11 m."], units=["m"]),
]

SUMMARY = [
    rule("Soustraire", "a − b = a + (−b) : soustraire, c'est ajouter l'opposé. Tout négatif est plus petit que 0 et que tout positif ; entre deux négatifs, le plus petit a la plus grande partie sans signe."),
    rule("Somme algébrique", "a + (+b) = a + b ; a − (−b) = a + b ; a + (−b) = a − b ; a − (+b) = a − b. On regroupe les positifs et les négatifs, puis on fait la différence des totaux."),
    rule("Produit", "Même signe : produit positif. Signes contraires : produit négatif. Avec plusieurs facteurs non nuls : positif si le nombre de facteurs négatifs est pair, négatif s'il est impair ; nul si un facteur est nul."),
    rule("Équation x + b = a", "x = a − b. Pour x − b = a, x = a + b. On vérifie en remplaçant x par la solution."),
    para("Les erreurs à éviter : appliquer la règle du produit à une somme ; oublier qu'on soustrait l'opposé ; se tromper de signe en supprimant les parenthèses ; ne pas vérifier la solution d'une équation."),
]

CONCEPTS = {
    "difference": ("Soustraire, comparer et ranger", "difference"),
    "somme": ("Somme algébrique", "somme"),
    "produit": ("Produit de nombres relatifs", "produit"),
    "equation": ("Équation x + b = a", "equation"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []

    def pick(low, high, places=0):
        """Return a random relative number, with a random sign, with a given number of decimals."""
        value = Fraction(rng.randint(low, high)) if places == 0 else rand_decimal(rng, low, high, places)
        return value if rng.random() < 0.5 else -value

    # 1. a difference of integers
    a, b = pick(2, 15), pick(2, 15)
    questions.append(number("a1", "difference", f"Calcule ${rel(a)} - {rel(b)}$.", a - b, 1, ["Ajoute l'opposé du deuxième nombre."], [f"{a} − ({b}) = {a} + ({-b}) = {a - b}."]))
    # 2. a difference of decimals
    a, b = pick(1, 9, 1), pick(1, 9, 1)
    questions.append(number("a2", "difference", f"Calcule ${rel(a)} - {rel(b)}$.", a - b, 2, ["Ajoute l'opposé du deuxième nombre."], [f"{show(a)} − ({show(b)}) = {show(a - b)}."]))
    # 3. a gap between two temperatures
    high, low = rng.randint(5, 40), -rng.randint(2, 20)
    questions.append(number("a3", "difference", f"La température maximale est de {high} °C et la minimale de {low} °C. Quel est l'écart, en °C ?", Fraction(high - low), 1,
                            ["Grande valeur moins petite valeur."], [f"{high} − ({low}) = {high} + {-low} = {high - low} °C."], units=["°C"]))
    # 4. an algebraic sum of four terms
    terms = [pick(1, 15) for _ in range(4)]
    text = "".join((" + " if t > 0 else " - ") + str(abs(t)) if i else ("-" if t < 0 else "") + str(abs(t)) for i, t in enumerate(terms))
    questions.append(number("a4", "somme", f"Calcule ${text}$.", sum(terms), 2, ["Regroupe les termes positifs et les termes négatifs."],
                            [f"Positifs : {sum(t for t in terms if t > 0)}. Négatifs : {-sum(t for t in terms if t < 0)}.", f"Résultat : {sum(terms)}."]))
    # 5. an algebraic sum with parentheses
    a, b, c = pick(2, 12), pick(2, 12), pick(2, 12)
    questions.append(number("a5", "somme", f"Calcule ${rel(a)} + {rel(b)} - {rel(c)}$.", a + b - c, 2, ["Supprime les parenthèses, puis regroupe."], [f"{a} + ({b}) − ({c}) = {a + b - c}."]))
    # 6. a bank account
    flows = [rng.choice([1, -1]) * rng.randint(2, 30) * 100 for _ in range(4)]
    names = ", ".join((f"+{f}" if f > 0 else f"-{-f}") + " F" for f in flows)
    questions.append(number("a6", "somme", f"Un compte enregistre {names}. Quel est le total, en F ?", Fraction(sum(flows)), 2,
                            ["Somme algébrique."], [f"Positifs : {sum(f for f in flows if f > 0)}. Négatifs : {-sum(f for f in flows if f < 0)}.", f"Total : {sum(flows)} F."], units=["F"]))
    # 7. a product of two relative numbers
    a, b = pick(2, 12), pick(2, 12)
    questions.append(number("a7", "produit", f"Calcule ${rel(a)} \\times {rel(b)}$.", a * b, 1, ["Règle des signes, puis produit des parties sans signe."], [f"{abs(a)} × {abs(b)} = {abs(a * b)}, {'positif' if a * b > 0 else 'négatif'} : {a * b}."]))
    # 8. a product with decimals
    a, b = pick(1, 9, 1), Fraction(rng.choice([2, 4, 5, 10])) * rng.choice([1, -1])
    questions.append(number("a8", "produit", f"Calcule ${rel(a)} \\times {rel(b)}$.", a * b, 2, ["Règle des signes, puis produit des parties sans signe."], [f"{show(abs(a))} × {abs(b)} = {show(abs(a * b))}, {'positif' if a * b > 0 else 'négatif'}."]))
    # 9. the sign of a long product
    count = rng.randint(2, 6)
    signs = [rng.choice([1, -1]) for _ in range(count)]
    negatives = signs.count(-1)
    factors = " \\times ".join(rel(s * rng.randint(1, 9)) for s in signs)
    options = ["Positif", "Négatif", "Nul"]
    questions.append(choice("a9", "produit", f"Quel est le signe de ${factors}$ ?", options, 0 if negatives % 2 == 0 else 1, 2, ["Compte les facteurs négatifs."],
                            [f"Il y a {negatives} facteur(s) négatif(s), un nombre {'pair' if negatives % 2 == 0 else 'impair'} : le produit est {'positif' if negatives % 2 == 0 else 'négatif'}."]))
    # 10. an equation x + b = a
    b, a = pick(2, 15), pick(2, 15)
    bs = f"+ {b}" if b > 0 else f"- {-b}"
    questions.append(number("a10", "equation", f"Résous $x {bs} = {plain(a)}$.", a - b, 2, ["Retire b des deux côtés."], [f"x = {a} − ({b}) = {a - b}.", f"Vérification : {a - b} + ({b}) = {a}."]))
    # 11. an equation with a decimal
    b, a = pick(1, 9, 1), pick(1, 9, 1)
    bs = f"+ {plain(b)}" if b > 0 else f"- {plain(-b)}"
    questions.append(number("a11", "equation", f"Résous $x {bs} = {plain(a)}$.", a - b, 3, ["Retire b des deux côtés."], [f"x = {show(a)} − ({show(b)}) = {show(a - b)}."]))
    # 12. a temperature problem
    drop, now = rng.randint(2, 15), rng.randint(-10, 10)
    questions.append(number("a12", "equation", f"Après une baisse de {drop} °C, la température est de {now} °C. Quelle était la température avant, en °C ?", Fraction(now + drop), 2,
                            ["x + (-baisse) = température actuelle."], [f"x + (-{drop}) = {now}, donc x = {now} + {drop} = {now + drop} °C."], units=["°C"]))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=2, title="Les nombres décimaux relatifs", language="fr",
    intro="Une température qui baisse, un compte qui se vide, un plongeur qui remonte : les nombres relatifs décrivent ces situations. "
          "Après l'addition apprise en Sixième, ce chapitre t'apprend à soustraire, à calculer une somme algébrique, à multiplier avec la règle des signes et à résoudre une équation simple.",
    objectives=["Soustraire des nombres relatifs et calculer un écart.",
                "Comparer et ranger des nombres décimaux relatifs.",
                "Calculer une somme algébrique en supprimant les parenthèses.",
                "Calculer le produit de nombres relatifs avec la règle des signes.",
                "Résoudre une équation du type x + b = a."],
    prerequisites=[{"text": "Additionner des nombres relatifs et les comparer.", "chapter": "sn-6e-relatifs"},
                   {"text": "Calculer avec des nombres décimaux.", "chapter": "sn-6e-division"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Second chapter of the Senegal Cinquième course. Its contents follow lesson 2 of the Côte d'Ivoire Cinquième programme (comparing and ordering, the difference, the algebraic sum, the product and the equation x + b = a), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. It has not been checked against the official Senegalese programme.",
)
