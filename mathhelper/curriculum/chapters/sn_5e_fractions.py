"""Cinquième, Les fractions: the third chapter of the Senegal Cinquième course, written in French.

The contents follow lesson 3 "Fractions" of the Côte d'Ivoire Cinquième programme (the difference of two fractions, the product of a fraction by a natural number and of two fractions,
the power of a fraction, and the bracketing of a fraction between two consecutive decimal numbers of the same order), which was read for this chapter. Every explanation, example and exercise
was written independently, with our own numbers. Results are asked in irreducible form. Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation,
and each worked example carries a "verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .kit import N, d, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-5e-fractions"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="irreducible")
IRRED = "Écris le résultat sous la forme d'un nombre entier ou d'une fraction irréductible."


def frac(value):
    """Write a fraction as math."""
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"\\dfrac{{{value.numerator}}}{{{value.denominator}}}"


def plain_frac(value):
    """Write a fraction as plain text."""
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


# ----- Section 1: the difference of two fractions -----
S1 = Section(
    "difference", "La différence de deux fractions", 24, "difference",
    "Soustraire deux fractions, avec ou sans le même dénominateur, simplifier le résultat et résoudre un problème de partage.",
    [
        para("Un père partage une tablette de chocolat entre ses enfants et garde le reste pour leur mère. Pour savoir ce qui reste, il faut soustraire des fractions de la tablette. "
             "Tu sais déjà additionner des fractions : la soustraction suit la même idée, avec un dénominateur commun."),
        rule("Soustraire des fractions",
             "Avec le même dénominateur : " + N("\\dfrac{a}{c} - \\dfrac{b}{c} = \\dfrac{a - b}{c}") + " (on garde le dénominateur et on soustrait les numérateurs). "
             "Avec des dénominateurs différents, on commence par les réduire au même dénominateur, souvent le plus petit multiple commun, puis on soustrait. "
             "Pour soustraire une fraction d'un nombre entier, on écrit l'entier avec le même dénominateur : " + N("3 - \\dfrac{2}{5} = \\dfrac{15}{5} - \\dfrac{2}{5}") + "."),
        example("Exemple 1", "Calculer " + N("\\dfrac{7}{10} - \\dfrac{3}{10}") + ".",
                "Les deux fractions ont le même dénominateur 10.",
                [(N("\\dfrac{7 - 3}{10} = \\dfrac{4}{10}"), "On soustrait les numérateurs."),
                 (N("\\dfrac{4}{10} = \\dfrac{2}{5}"), "On simplifie en divisant par 2.")],
                N("\\dfrac{2}{5}") + ".", "d('7')/10-d('3')/10==d('2')/5"),
        example("Exemple 2", "Calculer " + N("\\dfrac{5}{6} - \\dfrac{1}{4}") + ".",
                "Les dénominateurs 6 et 4 sont différents : le plus petit multiple commun est 12.",
                [(N("\\dfrac{5}{6} = \\dfrac{10}{12}") + " et " + N("\\dfrac{1}{4} = \\dfrac{3}{12}"), "On multiplie haut et bas par 2, puis par 3."),
                 (N("\\dfrac{10}{12} - \\dfrac{3}{12} = \\dfrac{7}{12}"), "On soustrait les numérateurs.")],
                N("\\dfrac{7}{12}") + ".", "d('5')/6-d('1')/4==d('7')/12"),
        example("Exemple 3", "Calculer " + N("3 - \\dfrac{2}{5}") + ".",
                "On écrit 3 comme une fraction de dénominateur 5.",
                [(N("3 = \\dfrac{15}{5}"), "3 × 5 = 15."),
                 (N("\\dfrac{15}{5} - \\dfrac{2}{5} = \\dfrac{13}{5}"), "On soustrait les numérateurs.")],
                N("\\dfrac{13}{5}") + ".", "3-d('2')/5==d('13')/5"),
        example("Exemple 4", "Une tablette de chocolat est partagée : le cadet reçoit " + N("\\dfrac{1}{6}") + " de la tablette, l'aîné reçoit le double, la benjamine reçoit le tiers de la part du cadet. Quelle fraction de la tablette reste pour la mère ?",
                "On calcule chaque part, puis on retire leur somme de la tablette entière, qui vaut 1.",
                [(N("2 \\times \\dfrac{1}{6} = \\dfrac{1}{3}"), "L'aîné : le double de 1/6."),
                 (N("\\dfrac{1}{3} \\times \\dfrac{1}{6} = \\dfrac{1}{18}"), "La benjamine : le tiers de 1/6."),
                 (N("\\dfrac{1}{6} + \\dfrac{1}{3} + \\dfrac{1}{18} = \\dfrac{3 + 6 + 1}{18} = \\dfrac{10}{18}"), "On réduit au dénominateur 18 et on additionne."),
                 (N("1 - \\dfrac{10}{18} = \\dfrac{8}{18} = \\dfrac{4}{9}"), "Il reste 8/18, soit 4/9.")],
                "Il reste " + N("\\dfrac{4}{9}") + " de la tablette.", "1-(d('1')/6+d('1')/3+d('1')/18)==d('4')/9"),
        warning("On ne soustrait pas les dénominateurs : " + N("\\dfrac{5}{6} - \\dfrac{1}{4}") + " ne vaut pas " + N("\\dfrac{4}{2}") + ". Les dénominateurs doivent être les mêmes avant de soustraire, et ils ne changent pas dans le résultat."),
    ],
    [
        number("s1-g1", "difference", "Calcule " + N("\\dfrac{7}{8} - \\dfrac{3}{8}") + ". " + IRRED, Fraction(1, 2), hints=["Même dénominateur : soustrais les numérateurs, puis simplifie."], solution=["(7 − 3)/8 = 4/8.", "4/8 = 1/2."]),
        number("s1-g2", "difference", "Calcule " + N("\\dfrac{3}{4} - \\dfrac{1}{6}") + ". " + IRRED, Fraction(7, 12), hints=["Dénominateur commun : 12."], solution=["3/4 = 9/12 et 1/6 = 2/12.", "9/12 − 2/12 = 7/12."]),
        number("s1-g3", "difference", "Calcule " + N("2 - \\dfrac{3}{7}") + ". " + IRRED, Fraction(11, 7), hints=["2 = 14/7."], solution=["2 = 14/7.", "14/7 − 3/7 = 11/7."]),
        number("s1-g4", "difference", "Awa lit " + N("\\dfrac{2}{5}") + " d'un livre le lundi et " + N("\\dfrac{1}{4}") + " le mardi. Quelle fraction du livre lui reste-t-il à lire ? " + IRRED, Fraction(7, 20),
               hints=["Retire la somme des deux parts de 1."], solution=["2/5 + 1/4 = 8/20 + 5/20 = 13/20.", "1 − 13/20 = 7/20."]),
        choice("s1-g5", "difference", "Quelle est la valeur de " + N("\\dfrac{5}{6} - \\dfrac{1}{3}") + " ?", [N("\\dfrac{4}{3}"), N("\\dfrac{1}{2}"), N("\\dfrac{4}{6}")], 1,
               hints=["1/3 = 2/6."], solution=["5/6 − 2/6 = 3/6 = 1/2."], wrong={0: "On ne soustrait pas les dénominateurs, ni ne les additionne.", 2: "4/6 serait 5/6 − 1/6."}),
    ])

# ----- Section 2: the product -----
S2 = Section(
    "produit", "Le produit d'une fraction par un entier et de deux fractions", 24, "produit",
    "Multiplier une fraction par un entier ou par une autre fraction, simplifier avant de multiplier et calculer la fraction d'une fraction.",
    [
        para("Prendre les trois quarts de la moitié d'un champ, c'est multiplier deux fractions. Contrairement à la soustraction, on n'a pas besoin d'un dénominateur commun pour multiplier."),
        rule("Multiplier des fractions",
             "Pour multiplier une fraction par un entier : " + N("n \\times \\dfrac{a}{b} = \\dfrac{n \\times a}{b}") + ". Pour multiplier deux fractions, on multiplie les numérateurs entre eux et les dénominateurs entre eux : "
             + N("\\dfrac{a}{b} \\times \\dfrac{c}{d} = \\dfrac{a \\times c}{b \\times d}") + ". On peut simplifier avant de multiplier pour avoir des nombres plus petits."),
        example("Exemple 1", "Calculer " + N("3 \\times \\dfrac{2}{5}") + ".",
                "On multiplie le numérateur par 3 et on garde le dénominateur.",
                [(N("\\dfrac{3 \\times 2}{5} = \\dfrac{6}{5}"), "6/5 est irréductible : 6 et 5 n'ont pas de diviseur commun autre que 1.")],
                N("\\dfrac{6}{5}") + ".", "3*d('2')/5==d('6')/5"),
        example("Exemple 2", "Calculer " + N("\\dfrac{2}{3} \\times \\dfrac{4}{5}") + ".",
                "On multiplie les numérateurs et les dénominateurs.",
                [(N("\\dfrac{2 \\times 4}{3 \\times 5} = \\dfrac{8}{15}"), "Numérateurs : 8. Dénominateurs : 15. La fraction est irréductible.")],
                N("\\dfrac{8}{15}") + ".", "d('2')/3*d('4')/5==d('8')/15"),
        example("Exemple 3", "Calculer " + N("\\dfrac{4}{9} \\times \\dfrac{3}{8}") + " en simplifiant.",
                "On cherche les facteurs communs entre un numérateur et un dénominateur.",
                [(N("\\dfrac{4 \\times 3}{9 \\times 8}") + " : 4 et 8 se simplifient par 4, 3 et 9 par 3", "On simplifie avant de multiplier."),
                 (N("\\dfrac{1 \\times 1}{3 \\times 2} = \\dfrac{1}{6}"), "Il reste 1 au numérateur et 3 × 2 au dénominateur.")],
                N("\\dfrac{1}{6}") + ".", "d('4')/9*d('3')/8==d('1')/6"),
        example("Exemple 4", "Les " + N("\\dfrac{3}{4}") + " de " + N("\\dfrac{2}{5}") + " d'un champ sont plantés en maïs. Quelle fraction du champ est plantée en maïs ?",
                "Prendre les 3/4 d'une quantité, c'est la multiplier par 3/4.",
                [(N("\\dfrac{3}{4} \\times \\dfrac{2}{5} = \\dfrac{6}{20}"), "3 × 2 = 6 et 4 × 5 = 20."),
                 (N("\\dfrac{6}{20} = \\dfrac{3}{10}"), "On simplifie par 2.")],
                N("\\dfrac{3}{10}") + " du champ.", "d('3')/4*d('2')/5==d('3')/10"),
        example("Exemple 5", "Calculer les " + N("\\dfrac{2}{3}") + " de 90 kg de riz.",
                "Une fraction d'une quantité s'obtient en multipliant la quantité par la fraction.",
                [(N("\\dfrac{2}{3} \\times 90 = \\dfrac{2 \\times 90}{3}") + " = " + N("\\dfrac{180}{3}"), "Le produit au numérateur."),
                 (N("180 \\div 3") + " = " + N("60"), "On divise.")],
                N("60") + " kg.", "d('2')/3*90==60"),
        warning("Ne cherche pas de dénominateur commun pour multiplier : " + N("\\dfrac{1}{2} \\times \\dfrac{1}{3} = \\dfrac{1}{6}") + ", et non " + N("\\dfrac{2}{6}") + ". Et attention : multiplier par une fraction plus petite que 1 donne un résultat plus petit : "
                + N("\\dfrac{1}{2} \\times \\dfrac{1}{2} = \\dfrac{1}{4}") + "."),
    ],
    [
        number("s2-g1", "produit", "Calcule " + N("4 \\times \\dfrac{3}{5}") + ". " + IRRED, Fraction(12, 5), hints=["Multiplie le numérateur par 4."], solution=["4 × 3/5 = 12/5."]),
        number("s2-g2", "produit", "Calcule " + N("\\dfrac{2}{3} \\times \\dfrac{5}{7}") + ". " + IRRED, Fraction(10, 21), hints=["Numérateurs entre eux, dénominateurs entre eux."], solution=["(2 × 5)/(3 × 7) = 10/21."]),
        number("s2-g3", "produit", "Calcule " + N("\\dfrac{3}{8} \\times \\dfrac{4}{9}") + ". " + IRRED, Fraction(1, 6), hints=["Simplifie avant de multiplier."], solution=["(3 × 4)/(8 × 9) = 12/72.", "12/72 = 1/6."]),
        number("s2-g4", "produit", "Les " + N("\\dfrac{3}{4}") + " de " + N("\\dfrac{2}{5}") + " d'un champ sont plantés en manioc. Quelle fraction du champ ? " + IRRED, Fraction(3, 10),
               hints=["Multiplie les deux fractions."], solution=["3/4 × 2/5 = 6/20 = 3/10."]),
        choice("s2-g5", "produit", "Que vaut " + N("\\dfrac{1}{2} \\times \\dfrac{1}{2}") + " ?", [N("1"), N("\\dfrac{1}{4}"), N("\\dfrac{1}{2}")], 1,
               hints=["(1 × 1)/(2 × 2)."], solution=["1/4 : la moitié d'une moitié est un quart."], wrong={0: "Multiplier par 1/2 diminue : le résultat est plus petit que 1/2.", 2: "La moitié de 1/2 est 1/4."}),
    ])

# ----- Section 3: the power of a fraction -----
S3 = Section(
    "puissance", "La puissance d'une fraction", 22, "puissance",
    "Calculer une puissance d'une fraction et l'utiliser dans un calcul.",
    [
        para("Une puissance d'une fraction se calcule comme une puissance d'un entier : on multiplie plusieurs fois la même fraction. Et comme on multiplie des fractions terme à terme, le calcul se simplifie."),
        rule("Puissance d'une fraction",
             "Pour une fraction " + N("\\dfrac{a}{b}") + " et un entier n au moins égal à 1 : " + N("\\left(\\dfrac{a}{b}\\right)^n = \\dfrac{a^n}{b^n}") + ". On met le numérateur et le dénominateur à la puissance n. "
             "Dans un calcul, la puissance se fait avant la multiplication et l'addition."),
        example("Exemple 1", "Calculer " + N("\\left(\\dfrac{2}{3}\\right)^2") + ".",
                "On met 2 et 3 au carré.",
                [(N("\\dfrac{2^2}{3^2} = \\dfrac{4}{9}"), "2² = 4 et 3² = 9.")],
                N("\\dfrac{4}{9}") + ".", "(d('2')/3)**2==d('4')/9"),
        example("Exemple 2", "Calculer " + N("\\left(\\dfrac{1}{2}\\right)^4") + ".",
                "Le numérateur reste 1 : 1 puissance n vaut 1.",
                [(N("\\dfrac{1^4}{2^4} = \\dfrac{1}{16}"), "2⁴ = 16.")],
                N("\\dfrac{1}{16}") + ".", "(d('1')/2)**4==d('1')/16"),
        example("Exemple 3", "Calculer " + N("\\left(\\dfrac{3}{5}\\right)^3") + ".",
                "On met 3 et 5 au cube.",
                [(N("\\dfrac{3^3}{5^3} = \\dfrac{27}{125}"), "3³ = 27 et 5³ = 125.")],
                N("\\dfrac{27}{125}") + ".", "(d('3')/5)**3==d('27')/125"),
        example("Exemple 4", "Calculer " + N("1 + \\left(\\dfrac{1}{2}\\right)^2") + ".",
                "La puissance d'abord, puis l'addition.",
                [(N("\\left(\\dfrac{1}{2}\\right)^2 = \\dfrac{1}{4}"), "Priorité à la puissance."),
                 (N("1 + \\dfrac{1}{4} = \\dfrac{4}{4} + \\dfrac{1}{4} = \\dfrac{5}{4}"), "On écrit 1 avec le dénominateur 4.")],
                N("\\dfrac{5}{4}") + ".", "1+(d('1')/2)**2==d('5')/4"),
        warning("Le carré d'une fraction porte sur le numérateur et sur le dénominateur : " + N("\\left(\\dfrac{2}{3}\\right)^2") + " vaut " + N("\\dfrac{4}{9}") + ", et non " + N("\\dfrac{4}{3}") + " ni " + N("\\dfrac{2}{9}") + ". "
                "Et élever au carré une fraction plus petite que 1 donne un résultat plus petit : " + N("\\dfrac{4}{9}") + " est plus petit que " + N("\\dfrac{2}{3}") + "."),
    ],
    [
        number("s3-g1", "puissance", "Calcule " + N("\\left(\\dfrac{3}{4}\\right)^2") + ". " + IRRED, Fraction(9, 16), hints=["3² et 4²."], solution=["9/16."]),
        number("s3-g2", "puissance", "Calcule " + N("\\left(\\dfrac{1}{3}\\right)^3") + ". " + IRRED, Fraction(1, 27), hints=["1³ et 3³."], solution=["1/27."]),
        number("s3-g3", "puissance", "Calcule " + N("\\left(\\dfrac{2}{5}\\right)^2 \\times 5") + ". " + IRRED, Fraction(4, 5), hints=["La puissance d'abord."], solution=["(2/5)² = 4/25.", "4/25 × 5 = 20/25 = 4/5."]),
        number("s3-g4", "puissance", "Calcule " + N("\\left(\\dfrac{1}{2}\\right)^5") + ". " + IRRED, Fraction(1, 32), hints=["2⁵ = 32."], solution=["1/32."]),
        choice("s3-g5", "puissance", "Que vaut " + N("\\left(\\dfrac{2}{3}\\right)^2") + " ?", [N("\\dfrac{4}{9}"), N("\\dfrac{4}{3}"), N("\\dfrac{2}{9}")], 0,
               hints=["Carré du numérateur et carré du dénominateur."], solution=["2² = 4 et 3² = 9 : 4/9."], wrong={1: "Le dénominateur aussi est au carré.", 2: "Le numérateur aussi est au carré."}),
    ])

# ----- Section 4: bracketing a fraction -----
S4 = Section(
    "encadrement", "Encadrer une fraction par deux décimaux consécutifs", 22, "encadrement",
    "Écrire une fraction sous forme décimale quand c'est possible, l'encadrer par deux décimaux consécutifs et comparer deux fractions avec leurs encadrements.",
    [
        para("Certaines fractions ont une écriture décimale exacte (3/4 = 0,75), d'autres non (1/3 = 0,333...). Dans les deux cas, on peut situer une fraction entre deux décimaux consécutifs, comme on situe une ville entre deux bornes kilométriques."),
        rule("Encadrer une fraction",
             "On divise le numérateur par le dénominateur. Deux décimaux consécutifs d'ordre 0,1 sont deux nombres qui diffèrent de 0,1 : par exemple 2,3 et 2,4. On encadre en gardant un nombre décimal exact de chiffres. "
             "Pour comparer deux fractions, on peut comparer leurs valeurs décimales approchées ou les mettre au même dénominateur."),
        example("Exemple 1", "Encadrer " + N("\\dfrac{7}{3}") + " par deux décimaux consécutifs d'ordre 0,1, puis d'ordre 0,01.",
                "On calcule 7 ÷ 3 = 2,3333...",
                [("7 ÷ 3 = 2,3333...", "La division ne se termine pas."),
                 (N("2,3 < \\dfrac{7}{3} < 2,4"), "À 0,1 près : on garde un chiffre après la virgule, puis le suivant."),
                 (N("2,33 < \\dfrac{7}{3} < 2,34"), "À 0,01 près : deux chiffres après la virgule.")],
                N("2,3 < \\dfrac{7}{3} < 2,4") + " et " + N("2,33 < \\dfrac{7}{3} < 2,34") + ".", "d('23')/10<d('7')/3<d('24')/10 and d('233')/100<d('7')/3<d('234')/100"),
        example("Exemple 2", "Écrire " + N("\\dfrac{5}{8}") + " sous forme décimale.",
                "On divise 5 par 8.",
                [("5 ÷ 8 = 0,625", "La division se termine : l'écriture décimale est exacte.")],
                N("\\dfrac{5}{8} = 0,625") + ".", "d('5')/8==d('0,625')"),
        example("Exemple 3", "Encadrer " + N("\\dfrac{1}{7}") + " par deux décimaux consécutifs d'ordre 0,01.",
                "On calcule 1 ÷ 7 = 0,142857...",
                [("1 ÷ 7 = 0,142857...", "La division ne se termine pas."),
                 (N("0,14 < \\dfrac{1}{7} < 0,15"), "On garde deux chiffres après la virgule.")],
                N("0,14 < \\dfrac{1}{7} < 0,15") + ".", "d('14')/100<d('1')/7<d('15')/100"),
        example("Exemple 4", "Comparer " + N("\\dfrac{5}{7}") + " et " + N("\\dfrac{3}{4}") + ".",
                "On compare leurs valeurs décimales approchées.",
                [(N("\\dfrac{5}{7}") + " ≈ 0,714...", "5 ÷ 7 = 0,714..."),
                 (N("\\dfrac{3}{4} = 0,75"), "3 ÷ 4 = 0,75."),
                 ("0,714 est plus petit que 0,75", "Donc 5/7 est plus petit que 3/4.")],
                N("\\dfrac{5}{7} < \\dfrac{3}{4}") + ".", "d('5')/7<d('3')/4"),
        warning("Un encadrement donne deux bornes : la fraction est entre elles, et ne leur est pas égale. Et les deux bornes doivent être consécutives : " + N("2,3 < \\dfrac{7}{3} < 2,4") + " est un bon encadrement, " + N("2 < \\dfrac{7}{3} < 3") + " est correct mais moins précis."),
    ],
    [
        ordered("s4-g1", "encadrement", "Encadre " + N("\\dfrac{5}{3}") + " par deux décimaux consécutifs d'ordre 0,1. Écris-les sous la forme petit ; grand.", [d("1,6"), d("1,7")],
                hints=["5 ÷ 3 = 1,666..."], solution=["5 ÷ 3 = 1,666...", "1,6 < 5/3 < 1,7."]),
        ordered("s4-g2", "encadrement", "Encadre " + N("\\dfrac{2}{3}") + " par deux décimaux consécutifs d'ordre 0,01. Écris-les sous la forme petit ; grand.", [d("0,66"), d("0,67")],
                hints=["2 ÷ 3 = 0,666..."], solution=["2 ÷ 3 = 0,666...", "0,66 < 2/3 < 0,67."]),
        number("s4-g3", "encadrement", "Écris " + N("\\dfrac{3}{8}") + " sous forme décimale.", d("0,375"), form="decimal", hints=["3 ÷ 8."], solution=["3 ÷ 8 = 0,375."]),
        choice("s4-g4", "encadrement", "Quelle fraction est la plus grande : " + N("\\dfrac{5}{7}") + " ou " + N("\\dfrac{3}{4}") + " ?", [N("\\dfrac{5}{7}"), N("\\dfrac{3}{4}"), "Elles sont égales"], 1,
               hints=["Compare 0,714... et 0,75."], solution=["5/7 = 0,714... et 3/4 = 0,75 : 3/4 est plus grand."], wrong={0: "0,714 est plus petit que 0,75.", 2: "Elles ont des valeurs différentes."}),
        choice("s4-g5", "encadrement", "Entre quels entiers consécutifs se trouve " + N("\\dfrac{7}{6}") + " ?", ["1 et 2", "0 et 1", "2 et 3"], 0,
               hints=["7 ÷ 6 = 1,166..."], solution=["7 ÷ 6 = 1,166... : entre 1 et 2."], wrong={1: "7/6 est plus grand que 1.", 2: "7/6 est plus petit que 2."}),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "difference", "Calcule " + N("\\dfrac{9}{10} - \\dfrac{4}{10}") + ". " + IRRED, Fraction(1, 2), 1, ["Soustrais les numérateurs."], ["5/10 = 1/2."]),
    number("p2", "difference", "Calcule " + N("\\dfrac{11}{12} - \\dfrac{5}{12}") + ". " + IRRED, Fraction(1, 2), 1, ["6/12."], ["6/12 = 1/2."]),
    number("p3", "difference", "Calcule " + N("\\dfrac{3}{4} - \\dfrac{1}{3}") + ". " + IRRED, Fraction(5, 12), 2, ["Dénominateur commun : 12."], ["9/12 − 4/12 = 5/12."]),
    number("p4", "difference", "Calcule " + N("\\dfrac{7}{10} - \\dfrac{1}{5}") + ". " + IRRED, Fraction(1, 2), 2, ["1/5 = 2/10."], ["7/10 − 2/10 = 5/10 = 1/2."]),
    number("p5", "difference", "Calcule " + N("5 - \\dfrac{3}{4}") + ". " + IRRED, Fraction(17, 4), 2, ["5 = 20/4."], ["20/4 − 3/4 = 17/4."]),
    number("p6", "difference", "Calcule " + N("\\dfrac{13}{6} - \\dfrac{5}{4}") + ". " + IRRED, Fraction(11, 12), 3, ["Dénominateur commun : 12."], ["26/12 − 15/12 = 11/12."]),
    number("p7", "difference", "Un réservoir est plein aux " + N("\\dfrac{7}{8}") + ". On en utilise les " + N("\\dfrac{1}{4}") + " du réservoir. Quelle fraction reste-t-il ? " + IRRED, Fraction(5, 8), 2, ["1/4 = 2/8."], ["7/8 − 2/8 = 5/8."]),
    number("p8", "difference", "Moussa dépense " + N("\\dfrac{1}{3}") + " de son argent pour un livre et " + N("\\dfrac{1}{5}") + " pour un cahier. Quelle fraction lui reste-t-il ? " + IRRED, Fraction(7, 15), 3, ["Retire la somme de 1."], ["1/3 + 1/5 = 8/15.", "1 − 8/15 = 7/15."]),
    number("p9", "produit", "Calcule " + N("5 \\times \\dfrac{2}{7}") + ". " + IRRED, Fraction(10, 7), 1, ["5 × 2 sur 7."], ["10/7."]),
    number("p10", "produit", "Calcule " + N("6 \\times \\dfrac{3}{4}") + ". " + IRRED, Fraction(9, 2), 2, ["18/4, puis simplifie."], ["18/4 = 9/2."]),
    number("p11", "produit", "Calcule " + N("\\dfrac{3}{5} \\times \\dfrac{2}{7}") + ". " + IRRED, Fraction(6, 35), 1, ["Numérateurs, dénominateurs."], ["6/35."]),
    number("p12", "produit", "Calcule " + N("\\dfrac{5}{6} \\times \\dfrac{3}{10}") + ". " + IRRED, Fraction(1, 4), 2, ["Simplifie avant de multiplier."], ["15/60 = 1/4."]),
    number("p13", "produit", "Calcule " + N("\\dfrac{7}{12} \\times \\dfrac{4}{21}") + ". " + IRRED, Fraction(1, 9), 3, ["Simplifie 7 avec 21 et 4 avec 12."], ["28/252 = 1/9."]),
    number("p14", "produit", "Calcule les " + N("\\dfrac{3}{5}") + " de 200 F. Réponds par un nombre.", Fraction(120), 1, ["200 ÷ 5 × 3."], ["200 ÷ 5 = 40 ; 40 × 3 = 120 F."], units=["F"]),
    number("p15", "produit", "Calcule les " + N("\\dfrac{2}{3}") + " de " + N("\\dfrac{3}{4}") + " d'un gâteau. Quelle fraction du gâteau ? " + IRRED, Fraction(1, 2), 2, ["Multiplie les deux fractions."], ["2/3 × 3/4 = 6/12 = 1/2."]),
    number("p16", "produit", "Un sac contient 48 kg de riz. On en vend les " + N("\\dfrac{3}{8}") + ", puis les " + N("\\dfrac{1}{3}") + " du reste. Combien de kilogrammes restent-ils ?", Fraction(20), 3, ["Calcule la part vendue d'abord."], ["3/8 de 48 = 18 kg, reste 30 kg.", "1/3 de 30 = 10 kg, il reste 30 − 10 = 20 kg."], units=["kg"]),
    choice("p17", "produit", "Quel produit est égal à " + N("\\dfrac{1}{6}") + " ?", [N("\\dfrac{1}{2} \\times \\dfrac{1}{3}"), N("\\dfrac{1}{2} + \\dfrac{1}{3}"), N("\\dfrac{1}{2} \\times 3")], 0, 2, ["1 × 1 sur 2 × 3."], ["1/2 × 1/3 = 1/6."], wrong={1: "1/2 + 1/3 = 5/6.", 2: "1/2 × 3 = 3/2."}),
    number("p18", "puissance", "Calcule " + N("\\left(\\dfrac{1}{4}\\right)^2") + ". " + IRRED, Fraction(1, 16), 1, ["1² et 4²."], ["1/16."]),
    number("p19", "puissance", "Calcule " + N("\\left(\\dfrac{5}{2}\\right)^2") + ". " + IRRED, Fraction(25, 4), 1, ["5² et 2²."], ["25/4."]),
    number("p20", "puissance", "Calcule " + N("\\left(\\dfrac{2}{3}\\right)^3") + ". " + IRRED, Fraction(8, 27), 2, ["2³ et 3³."], ["8/27."]),
    number("p21", "puissance", "Calcule " + N("\\left(\\dfrac{3}{2}\\right)^4") + ". " + IRRED, Fraction(81, 16), 2, ["3⁴ = 81 et 2⁴ = 16."], ["81/16."]),
    number("p22", "puissance", "Calcule " + N("1 - \\left(\\dfrac{1}{3}\\right)^2") + ". " + IRRED, Fraction(8, 9), 2, ["La puissance d'abord."], ["(1/3)² = 1/9.", "1 − 1/9 = 8/9."]),
    number("p23", "puissance", "Calcule " + N("\\left(\\dfrac{1}{2}\\right)^2 + \\left(\\dfrac{1}{4}\\right)^2") + ". " + IRRED, Fraction(5, 16), 3, ["1/4 et 1/16."], ["1/4 + 1/16 = 4/16 + 1/16 = 5/16."]),
    number("p24", "puissance", "Une feuille est pliée en deux, puis encore en deux, puis encore en deux. Quelle fraction de la feuille d'origine représente un des morceaux ? " + IRRED, Fraction(1, 8), 2, ["(1/2)³."], ["(1/2)³ = 1/8."]),
    choice("p25", "puissance", "Léa dit : « (2/3)² = 4/3 ». Quelle est son erreur ?", ["Elle n'a pas mis le dénominateur au carré", "Elle n'a pas mis le numérateur au carré", "Elle a multiplié au lieu d'élever à la puissance"], 0, 2, ["Les deux termes sont au carré."], ["(2/3)² = 2²/3² = 4/9."], wrong={1: "Le numérateur est bien au carré : 4.", 2: "Elle a bien élevé au carré le numérateur."}),
    ordered("p26", "encadrement", "Encadre " + N("\\dfrac{4}{3}") + " par deux décimaux consécutifs d'ordre 0,1. Écris-les sous la forme petit ; grand.", [d("1,3"), d("1,4")], 1, ["4 ÷ 3 = 1,333..."], ["1,3 < 4/3 < 1,4."]),
    ordered("p27", "encadrement", "Encadre " + N("\\dfrac{5}{6}") + " par deux décimaux consécutifs d'ordre 0,01. Écris-les sous la forme petit ; grand.", [d("0,83"), d("0,84")], 2, ["5 ÷ 6 = 0,8333..."], ["0,83 < 5/6 < 0,84."]),
    ordered("p28", "encadrement", "Encadre " + N("\\dfrac{10}{7}") + " par deux décimaux consécutifs d'ordre 0,1. Écris-les sous la forme petit ; grand.", [d("1,4"), d("1,5")], 2, ["10 ÷ 7 = 1,428..."], ["1,4 < 10/7 < 1,5."]),
    number("p29", "encadrement", "Écris " + N("\\dfrac{7}{20}") + " sous forme décimale.", d("0,35"), 1, ["7 ÷ 20."], ["7 ÷ 20 = 0,35."], form="decimal"),
    number("p30", "encadrement", "Écris " + N("\\dfrac{9}{8}") + " sous forme décimale.", d("1,125"), 2, ["9 ÷ 8."], ["9 ÷ 8 = 1,125."], form="decimal"),
    choice("p31", "encadrement", "Quelle fraction est la plus petite : " + N("\\dfrac{4}{9}") + " ou " + N("\\dfrac{3}{7}") + " ?", [N("\\dfrac{4}{9}"), N("\\dfrac{3}{7}"), "Elles sont égales"], 1, 3, ["4/9 = 0,444... et 3/7 = 0,428..."], ["3/7 = 0,428... est plus petit que 4/9 = 0,444..."], wrong={0: "0,444 est plus grand que 0,428.", 2: "Les valeurs sont différentes."}),
    choice("p32", "encadrement", "Entre quels entiers consécutifs se trouve " + N("\\dfrac{23}{5}") + " ?", ["4 et 5", "3 et 4", "5 et 6"], 0, 1, ["23 ÷ 5 = 4,6."], ["4 × 5 = 20 et 5 × 5 = 25 : 4 < 23/5 < 5."], wrong={1: "23/5 = 4,6 est plus grand que 4.", 2: "23/5 = 4,6 est plus petit que 5."}),
]

SUMMARY = [
    rule("Différence", "Même dénominateur : a/c − b/c = (a − b)/c. Sinon, réduire au même dénominateur d'abord. Un entier n s'écrit n = (n × c)/c. On simplifie le résultat."),
    rule("Produit", "n × a/b = (n × a)/b et a/b × c/d = (a × c)/(b × d), sans dénominateur commun. On peut simplifier avant de multiplier. La fraction d'une quantité : multiplier la quantité par la fraction."),
    rule("Puissance", "(a/b)ⁿ = aⁿ/bⁿ. La puissance se calcule avant la multiplication et l'addition."),
    rule("Encadrement", "On divise le numérateur par le dénominateur. 7/3 = 2,333... est entre 2,3 et 2,4, et entre 2,33 et 2,34. Pour comparer deux fractions, on compare leurs valeurs décimales ou on les met au même dénominateur."),
    para("Les erreurs à éviter : soustraire les dénominateurs ; chercher un dénominateur commun pour multiplier ; oublier de mettre le dénominateur à la puissance ; oublier de simplifier ; confondre l'ordre 0,1 et l'ordre 0,01."),
]

CONCEPTS = {
    "difference": ("Différence de deux fractions", "difference"),
    "produit": ("Produit de fractions", "produit"),
    "puissance": ("Puissance d'une fraction", "puissance"),
    "encadrement": ("Encadrer une fraction", "encadrement"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []

    def fr(value):
        return plain_frac(value)

    def small():
        """Return a fraction smaller than 1 with a denominator between 2 and 12 that is not reduced to a whole number."""
        den = rng.randint(3, 12)
        num = rng.randint(1, den - 1)
        return Fraction(num, den)

    # 1. a difference with the same denominator
    den = rng.randint(5, 15)
    a, b = rng.randint(3, den + 6), rng.randint(1, 2)
    while a <= b or Fraction(a - b, den).denominator == 1:
        a, b = rng.randint(3, den + 6), rng.randint(1, 2)
    questions.append(number("a1", "difference", f"Calcule $\\dfrac{{{a}}}{{{den}}} - \\dfrac{{{b}}}{{{den}}}$. {IRRED}", Fraction(a - b, den), 1, ["Soustrais les numérateurs, puis simplifie."],
                            [f"({a} − {b})/{den} = {a - b}/{den} = {fr(Fraction(a - b, den))}."]))
    # 2. a difference with different denominators
    x, y = Fraction(rng.randint(1, 5), rng.choice([2, 3, 4, 6])), Fraction(rng.randint(1, 3), rng.choice([5, 8, 9, 10]))
    while x == y or x.denominator == 1 or y.denominator == 1:
        x = Fraction(rng.randint(1, 5), rng.choice([2, 3, 4, 6]))
        y = Fraction(rng.randint(1, 3), rng.choice([5, 8, 9, 10]))
    x, y = (x, y) if x > y else (y, x)
    questions.append(number("a2", "difference", f"Calcule ${frac(x)} - {frac(y)}$. {IRRED}", x - y, 2, ["Réduis au même dénominateur."], [f"{fr(x)} − {fr(y)} = {fr(x - y)}."]))
    # 3. an integer minus a fraction
    n, f = rng.randint(2, 6), small()
    questions.append(number("a3", "difference", f"Calcule ${n} - {frac(f)}$. {IRRED}", n - f, 2, ["Écris l'entier avec le même dénominateur."], [f"{n} = {n * f.denominator}/{f.denominator}.", f"{n} − {fr(f)} = {fr(n - f)}."]))
    # 4. what is left
    p, q = rng.choice([2, 3, 4, 5]), rng.choice([3, 4, 5, 6, 8])
    first, second = Fraction(1, p), Fraction(1, q)
    while first + second >= 1:
        p, q = rng.choice([2, 3, 4, 5]), rng.choice([3, 4, 5, 6, 8])
        first, second = Fraction(1, p), Fraction(1, q)
    questions.append(number("a4", "difference", f"On dépense ${frac(first)}$ de son argent pour du riz et ${frac(second)}$ pour de l'huile. Quelle fraction de son argent lui reste-t-il ? {IRRED}", 1 - first - second, 3,
                            ["Retire la somme des deux parts de 1."], [f"{fr(first)} + {fr(second)} = {fr(first + second)}.", f"1 − {fr(first + second)} = {fr(1 - first - second)}."]))
    # 5. an integer times a fraction
    n, f = rng.randint(2, 9), small()
    questions.append(number("a5", "produit", f"Calcule ${n} \\times {frac(f)}$. {IRRED}", n * f, 1, ["Multiplie le numérateur par l'entier, puis simplifie."], [f"{n} × {fr(f)} = {fr(n * f)}."]))
    # 6. a product of two fractions
    f, g = small(), small()
    questions.append(number("a6", "produit", f"Calcule ${frac(f)} \\times {frac(g)}$. {IRRED}", f * g, 2, ["Multiplie les numérateurs entre eux et les dénominateurs entre eux, puis simplifie."], [f"{fr(f)} × {fr(g)} = {fr(f * g)}."]))
    # 7. a fraction of a quantity
    f = small()
    quantity = f.denominator * rng.randint(3, 20)
    questions.append(number("a7", "produit", f"Calcule les ${frac(f)}$ de {quantity} kg. Réponds par un nombre.", f * quantity, 2, ["Quantité × fraction."], [f"{quantity} ÷ {f.denominator} = {quantity // f.denominator}.", f"{quantity // f.denominator} × {f.numerator} = {f * quantity} kg."], units=["kg"]))
    # 8. the power of a fraction
    num, den, k = rng.randint(1, 5), rng.randint(2, 6), rng.randint(2, 3)
    value = Fraction(num, den) ** k
    questions.append(number("a8", "puissance", f"Calcule $\\left(\\dfrac{{{num}}}{{{den}}}\\right)^{k}$. {IRRED}", value, 2, ["Mets le numérateur et le dénominateur à la puissance."], [f"({num}/{den})^{k} = {num ** k}/{den ** k} = {fr(value)}."]))
    # 9. a power in a calculation
    f = Fraction(1, rng.randint(2, 5))
    n = rng.randint(2, 4)
    questions.append(number("a9", "puissance", f"Calcule ${n} + \\left({frac(f)}\\right)^2$. {IRRED}", n + f * f, 3, ["La puissance d'abord, puis l'addition."], [f"({fr(f)})² = {fr(f * f)}.", f"{n} + {fr(f * f)} = {fr(n + f * f)}."]))
    # 10. bracketing at order 0.1
    den = rng.choice([3, 6, 7, 9, 11, 12])
    num = rng.randint(den + 1, 4 * den)
    while Fraction(num, den).denominator == 1 or (Fraction(num, den) * 10).denominator == 1:
        num = rng.randint(den + 1, 4 * den)
    low = Fraction(int(Fraction(num, den) * 10 // 1), 10)
    questions.append(ordered("a10", "encadrement", f"Encadre $\\dfrac{{{num}}}{{{den}}}$ par deux décimaux consécutifs d'ordre 0,1. Écris-les sous la forme petit ; grand.", [low, low + Fraction(1, 10)], 2,
                             ["Calcule la division et garde un chiffre après la virgule."], [f"{num} ÷ {den} = {float(Fraction(num, den)):.4f}...", f"{show(low)} < {num}/{den} < {show(low + Fraction(1, 10))}."]))
    # 11. bracketing at order 0.01
    den = rng.choice([3, 6, 7, 9, 11, 12])
    num = rng.randint(1, 2 * den)
    while (Fraction(num, den) * 100).denominator == 1:
        num = rng.randint(1, 2 * den)
    low = Fraction(int(Fraction(num, den) * 100 // 1), 100)
    questions.append(ordered("a11", "encadrement", f"Encadre $\\dfrac{{{num}}}{{{den}}}$ par deux décimaux consécutifs d'ordre 0,01. Écris-les sous la forme petit ; grand.", [low, low + Fraction(1, 100)], 3,
                             ["Calcule la division et garde deux chiffres après la virgule."], [f"{num} ÷ {den} = {float(Fraction(num, den)):.5f}...", f"{show(low)} < {num}/{den} < {show(low + Fraction(1, 100))}."]))
    # 12. compare two fractions
    f, g = Fraction(rng.randint(2, 8), rng.randint(5, 9)), Fraction(rng.randint(2, 8), rng.randint(5, 9))
    while f == g or abs(f - g) < Fraction(1, 40) or f.denominator == 1 or g.denominator == 1:
        f, g = Fraction(rng.randint(2, 8), rng.randint(5, 9)), Fraction(rng.randint(2, 8), rng.randint(5, 9))
    questions.append(choice("a12", "encadrement", f"Quelle fraction est la plus grande : ${frac(f)}$ ou ${frac(g)}$ ?", [f"${frac(f)}$", f"${frac(g)}$", "Elles sont égales"], 0 if f > g else 1, 2, ["Compare les valeurs décimales."],
                            [f"{fr(f)} ≈ {float(f):.3f} et {fr(g)} ≈ {float(g):.3f}."], wrong={2: "Les deux valeurs sont différentes."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=3, title="Les fractions", language="fr",
    intro="Partager une tablette de chocolat, prendre les trois quarts de la moitié d'un champ, plier une feuille plusieurs fois : ces situations utilisent des fractions. "
          "Ce chapitre t'apprend à soustraire des fractions, à les multiplier, à calculer leurs puissances et à les encadrer par des nombres décimaux.",
    objectives=["Soustraire deux fractions et simplifier le résultat.",
                "Multiplier une fraction par un entier et deux fractions entre elles.",
                "Calculer une puissance d'une fraction.",
                "Encadrer une fraction par deux décimaux consécutifs et comparer deux fractions.",
                "Résoudre un problème de partage avec des fractions."],
    prerequisites=[{"text": "Connaître les fractions, leur simplification et leur addition.", "chapter": "sn-6e-fractions"},
                   {"text": "Connaître les puissances d'un nombre entier.", "chapter": "sn-5e-premiers"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Third chapter of the Senegal Cinquième course. Its contents follow lesson 3 of the Côte d'Ivoire Cinquième programme (the difference of two fractions, the product, the power of a fraction and the bracketing between consecutive decimals), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. It has not been checked against the official Senegalese programme.",
)
