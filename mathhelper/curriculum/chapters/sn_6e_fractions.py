"""Sixième, Les fractions: the sixth chapter of the Senegal Sixième course, written in French.

The contents follow lesson 11 "Fractions" of the Côte d'Ivoire Sixième programme (a fraction, a decimal fraction, equal fractions, simplifying, a distance on a
graduated segment, comparing and adding fractions, a fraction of a quantity), which was read for this chapter, and the fractions exercises of the ADEM-Dakar
Sixième booklet. Every explanation, example and exercise was written independently, with our own numbers.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
import math
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .kit import N, d, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-6e-fractions"
number, choice, ordered, between = make_kit(CHAPTER_ID)


def frac(value):
    """Write an exact fraction as a/b, or as a whole number when it is one."""
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


# ----- Section 1: what a fraction means -----
S1 = Section(
    "sens", "Le sens d'une fraction", 22, "sens",
    "Comprendre une fraction comme des parts d'une unité, la placer sur un segment gradué, la comparer à 1 et l'écrire en décimal.",
    [
        para("Une galette est coupée en 8 parts égales. Awa en mange 3. Quelle partie de la galette a-t-elle mangée ? Elle a mangé 3 parts sur 8, et on écrit " + N("3/8") + ". "
             "Il reste 5 parts sur 8, c'est-à-dire " + N("5/8") + " de la galette. Les nombres comme " + N("3/8") + " s'appellent des fractions."),
        definition("Fraction",
                   "Pour deux nombres entiers " + N("a") + " et " + N("b") + " (avec " + N("b") + " différent de 0), la fraction " + "$\\dfrac{a}{b}$" + " est obtenue en partageant l'unité en " + N("b")
                   + " parts égales et en prenant " + N("a") + " de ces parts. Le nombre du haut, " + N("a") + ", est le numérateur. Le nombre du bas, " + N("b") + ", est le dénominateur. "
                   "Les parts doivent être égales. Une fraction est aussi le quotient de " + N("a") + " par " + N("b") + " : " + "$\\dfrac{a}{b}$" + " = " + N("a \\div b") + "."),
        rule("Comparer une fraction à 1",
             "Si le numérateur est plus petit que le dénominateur, la fraction est plus petite que 1. S'ils sont égaux, la fraction vaut 1. Si le numérateur est plus grand que le dénominateur, la fraction est plus grande que 1."),
        example("Exemple 1", "Un segment gradué a pour unité la longueur de 0 à 1, partagée en 4 parts égales. Quelle fraction donne la distance du point A, situé à 7 graduations de l'origine ?",
                "Chaque graduation est un quart de l'unité. On compte combien de graduations séparent A de l'origine.",
                [("Une graduation vaut " + N("1/4") + " de l'unité", "L'unité est partagée en 4 parts égales."),
                 ("A est à 7 graduations de l'origine : " + N("7 \\times 1/4") + " = " + N("7/4"), "7 quarts de l'unité."),
                 (N("7/4") + " = " + N("4/4 + 3/4") + " = " + N("1 + 3/4"), "4 quarts font une unité entière, puis 3 quarts de plus : A est après le point 1."),
                 (N("7 \\div 4") + " = " + N("1,75"), "En décimal : 7/4 = 1,75, ce qui est cohérent.")],
                N("7/4") + " = " + N("1,75") + " de l'unité", "d('7')/4==d('1,75') and 7*d('1')/4>1"),
        example("Exemple 2", "Comparer à 1 les fractions " + N("5/8") + ", " + N("9/9") + " et " + N("11/6") + ".",
                "On compare le numérateur et le dénominateur.",
                [(N("5/8"), "5 est plus petit que 8 : cette fraction est plus petite que 1."),
                 (N("9/9"), "9 est égal à 9 : cette fraction vaut 1 (9 parts sur 9, c'est toute l'unité)."),
                 (N("11/6"), "11 est plus grand que 6 : cette fraction est plus grande que 1.")],
                N("5/8 < 1") + " ; " + N("9/9 = 1") + " ; " + N("11/6 > 1"), "d('5')/8<1 and d('9')/9==1 and d('11')/6>1"),
        definition("Fraction décimale",
                   "Une fraction décimale est une fraction dont le dénominateur est 10, 100, 1 000, et ainsi de suite. Par exemple " + N("7/10") + ", " + N("35/100") + " et " + N("125/1000") + ". "
                   "Elle s'écrit tout de suite avec une virgule : le nombre de zéros du dénominateur donne le nombre de chiffres après la virgule. " + N("35/100") + " = " + N("0,35") + " et " + N("125/100") + " = " + N("1,25") + ". "
                   "Inversement, un nombre décimal s'écrit comme une fraction décimale : " + N("0,35") + " = " + N("35/100") + ". Toutes les fractions ne sont pas décimales : " + N("1/3") + " ne l'est pas, et on ne peut pas l'écrire avec une virgule qui s'arrête."),
        example("Exemple 3", "Écrire " + N("3/4") + " en nombre décimal, puis " + N("0,6") + " en fraction décimale.",
                "Une fraction est un quotient : on divise. Un décimal s'écrit comme une fraction avec le rang de son dernier chiffre.",
                [(N("3 \\div 4") + " = " + N("0,75"), "3 ÷ 4 : 30 ÷ 4 = 7 reste 2, puis 20 ÷ 4 = 5. Donc 3/4 = 0,75."),
                 (N("0,6") + " = " + N("6/10"), "Un chiffre après la virgule : le dénominateur est 10.")],
                N("3/4 = 0,75") + " et " + N("0,6 = 6/10"), "d('3')/4==d('0,75') and d('6')/10==d('0,6')"),
        example("Exemple 4", "Écrire 2 unités et 3 quarts sous la forme d'une seule fraction.",
                "Une unité vaut 4 quarts : on compte tous les quarts.",
                [("2 unités = " + N("2 \\times 4") + " = " + N("8") + " quarts", "Chaque unité contient 4 quarts."),
                 ("8 quarts + 3 quarts = " + N("11") + " quarts", "On additionne les quarts."),
                 ("11 quarts s'écrivent " + N("11/4"), "Le dénominateur 4 dit qu'on compte des quarts.")],
                N("11/4"), "2*4+3==11"),
        warning("Les parts doivent être égales : si une galette est coupée en 4 parts de tailles différentes, une part n'est pas " + N("1/4") + " de la galette. Et le dénominateur ne peut jamais être 0 : on ne peut pas partager en 0 part."),
    ],
    [
        number("s1-g1", "sens", "Une tablette de chocolat a 12 carreaux. Moussa en mange 5. Quelle fraction de la tablette a-t-il mangée ?", Fraction(5, 12), form="fraction",
               hints=["Combien de parts égales au total ? Combien de parts mangées ?"], solution=["La tablette est partagée en 12 parts égales et Moussa en prend 5.", "Il a mangé 5/12 de la tablette."]),
        choice("s1-g2", "sens", "La fraction " + N("7/5") + " est :", ["plus petite que 1", "égale à 1", "plus grande que 1"], 2,
               hints=["Compare le numérateur et le dénominateur."], solution=["7 est plus grand que 5 : la fraction est plus grande que 1."],
               wrong={0: "7/5 est plus petit que 1 seulement si 7 est plus petit que 5, ce qui est faux.", 1: "Une fraction vaut 1 quand le numérateur est égal au dénominateur."}),
        number("s1-g3", "sens", "Écris " + N("11/8") + " en nombre décimal.", d("1,375"), form="decimal",
               hints=["Une fraction est un quotient : divise 11 par 8."], solution=["11 ÷ 8 = 1, reste 3 ; 30 ÷ 8 = 3, reste 6 ; 60 ÷ 8 = 7, reste 4 ; 40 ÷ 8 = 5.", "11/8 = 1,375."]),
        number("s1-g4", "sens", "Écris " + N("0,35") + " sous la forme d'une fraction décimale.", d("0,35"), form="decimal_fraction",
               hints=["Combien de chiffres après la virgule ?"], solution=["Deux chiffres après la virgule : le dénominateur est 100.", "0,35 = 35/100."]),
        number("s1-g5", "sens", "L'unité est partagée en 6 parts égales. Un point est situé à 10 graduations de l'origine. Quelle fraction de l'unité représente sa distance ?", Fraction(10, 6), form="fraction",
               hints=["Chaque graduation vaut un sixième."], solution=["Chaque graduation vaut 1/6 de l'unité.", "10 graduations valent 10 × 1/6 = 10/6, ce qui est plus grand que 1."]),
    ])

# ----- Section 2: equal fractions and simplifying -----
S2 = Section(
    "egales", "Fractions égales et simplification", 24, "egales",
    "Reconnaître des fractions égales, compléter une égalité de fractions et simplifier une fraction.",
    [
        para("La moitié d'une galette, c'est 1 part sur 2. Mais si on coupe la galette en 4 parts, la moitié, c'est 2 parts sur 4. Et si on la coupe en 8, c'est 4 parts sur 8. "
             "Ces trois fractions représentent la même quantité : " + N("1/2 = 2/4 = 4/8") + ". Elles sont égales."),
        rule("Fractions égales",
             "On ne change pas la valeur d'une fraction quand on multiplie son numérateur et son dénominateur par le même nombre (différent de 0) : " + "$\\dfrac{a}{b} = \\dfrac{a \\times k}{b \\times k}$" + ". "
             "On ne la change pas non plus quand on divise le numérateur et le dénominateur par un même nombre qui les divise tous les deux."),
        definition("Fraction irréductible",
                   "Simplifier une fraction, c'est la remplacer par une fraction égale avec un numérateur et un dénominateur plus petits. Une fraction est irréductible quand on ne peut plus la simplifier, c'est-à-dire "
                   "quand son numérateur et son dénominateur n'ont aucun diviseur commun autre que 1."),
        example("Exemple 1", "Simplifier " + N("4/6") + ".",
                "On cherche un nombre qui divise à la fois 4 et 6.",
                [("4 et 6 sont tous les deux divisibles par 2", "Ils sont pairs."),
                 (N("4/6") + " = " + "$\\dfrac{4 \\div 2}{6 \\div 2}$" + " = " + N("2/3"), "On divise le numérateur et le dénominateur par 2."),
                 ("2 et 3 n'ont pas de diviseur commun autre que 1", "La fraction 2/3 est irréductible.")],
                N("4/6 = 2/3"), "d('4')/6==d('2')/3"),
        example("Exemple 2", "Simplifier " + N("18/24") + " au maximum.",
                "On divise par le plus grand nombre qui divise 18 et 24, ou par étapes.",
                [("Diviseurs de 18 : 1, 2, 3, 6, 9, 18. Diviseurs de 24 : 1, 2, 3, 4, 6, 8, 12, 24", "Le plus grand diviseur commun est 6."),
                 (N("18/24") + " = " + "$\\dfrac{18 \\div 6}{24 \\div 6}$" + " = " + N("3/4"), "On divise par 6."),
                 ("3 et 4 n'ont pas de diviseur commun autre que 1", "3/4 est irréductible.")],
                N("3/4"), "d('18')/24==d('3')/4 and math.gcd(18, 24)==6 and math.gcd(3, 4)==1"),
        example("Exemple 3", "Compléter l'égalité " + N("3/5 = ?/20") + ".",
                "On cherche par quel nombre on est passé de 5 à 20 au dénominateur, et on fait la même chose au numérateur.",
                [("5 × 4 = 20", "Le dénominateur a été multiplié par 4."),
                 (N("3 \\times 4") + " = " + N("12"), "Le numérateur doit aussi être multiplié par 4."),
                 (N("3/5") + " = " + N("12/20"), "Vérification : 12 ÷ 20 = 0,6 et 3 ÷ 5 = 0,6.")],
                N("12/20"), "d('3')/5==d('12')/20"),
        example("Exemple 4", "Réduire " + N("2/3") + " et " + N("5/12") + " au même dénominateur.",
                "Le dénominateur 12 est un multiple de 3 : on garde 12 et on transforme 2/3.",
                [("12 = 3 × 4", "On multiplie le dénominateur de 2/3 par 4 pour obtenir 12."),
                 (N("2/3") + " = " + "$\\dfrac{2 \\times 4}{3 \\times 4}$" + " = " + N("8/12"), "On multiplie aussi le numérateur par 4."),
                 ("Les deux fractions s'écrivent maintenant avec le dénominateur 12 : " + N("8/12") + " et " + N("5/12"), "Elles sont prêtes à être comparées ou additionnées.")],
                N("8/12") + " et " + N("5/12"), "d('2')/3==d('8')/12"),
        warning("Ajouter le même nombre au numérateur et au dénominateur change la fraction : " + N("1/2") + " n'est pas égal à " + N("2/3") + " (1 + 1 et 2 + 1). Il faut multiplier ou diviser, pas ajouter."),
    ],
    [
        number("s2-g1", "egales", "Simplifie " + N("6/8") + " au maximum.", Fraction(3, 4), form="irreducible",
               hints=["Quel nombre divise à la fois 6 et 8 ?"], solution=["6 et 8 sont divisibles par 2 : 6 ÷ 2 = 3 et 8 ÷ 2 = 4.", "6/8 = 3/4, qui est irréductible."]),
        number("s2-g2", "egales", "Complète : " + "$\\dfrac{2}{5} = \\dfrac{?}{15}$" + ". Quel est le numérateur manquant ?", Fraction(6),
               hints=["Par quel nombre a-t-on multiplié 5 pour obtenir 15 ?"], solution=["5 × 3 = 15, donc le numérateur est multiplié par 3 aussi : 2 × 3 = 6.", "2/5 = 6/15."]),
        number("s2-g3", "egales", "Simplifie " + N("18/45") + " au maximum.", Fraction(2, 5), form="irreducible",
               hints=["Les deux nombres sont divisibles par 9."], solution=["18 ÷ 9 = 2 et 45 ÷ 9 = 5.", "18/45 = 2/5, irréductible."]),
        choice("s2-g4", "egales", "Quelle fraction est égale à " + N("3/4") + " ?", [N("6/8"), N("4/5"), N("3/8")], 0,
               hints=["Multiplie le numérateur et le dénominateur de 3/4 par le même nombre."], solution=["3/4 = (3 × 2)/(4 × 2) = 6/8."],
               wrong={1: "4/5 s'obtient en ajoutant 1 en haut et en bas, ce qui change la valeur.", 2: "3/8 a le même numérateur mais un dénominateur différent : sa valeur est plus petite."}),
        number("s2-g5", "egales", "Écris " + N("3/4") + " et " + N("5/8") + " avec le même dénominateur 8. Quel est le numérateur de " + N("3/4") + " ?", Fraction(6),
               hints=["Par quel nombre faut-il multiplier 4 pour obtenir 8 ?"], solution=["4 × 2 = 8, donc 3 × 2 = 6.", "3/4 = 6/8, à comparer avec 5/8."]),
    ])

# ----- Section 3: compare, add and subtract -----
S3 = Section(
    "operations", "Comparer, additionner et soustraire des fractions", 26, "operations",
    "Comparer des fractions, les additionner et les soustraire, avec le même dénominateur ou après les avoir réduites.",
    [
        rule("Comparer des fractions",
             "Si les fractions ont le même dénominateur, la plus grande est celle qui a le plus grand numérateur. Sinon, on les réduit d'abord au même dénominateur, puis on compare les numérateurs."),
        rule("Additionner et soustraire avec le même dénominateur",
             "Ajouter " + N("3/7") + " et " + N("2/7") + ", c'est ajouter 3 septièmes et 2 septièmes : cela fait 5 septièmes. On additionne les numérateurs et on garde le dénominateur : "
             + "$\\dfrac{a}{c} + \\dfrac{b}{c} = \\dfrac{a + b}{c}$" + ". C'est pareil pour la soustraction."),
        rule("Quand les dénominateurs sont différents",
             "On réduit d'abord les fractions au même dénominateur, puis on applique la règle précédente. On simplifie ensuite le résultat si c'est possible."),
        example("Exemple 1", "Comparer " + N("3/4") + " et " + N("5/6") + ".",
                "Les dénominateurs 4 et 6 sont différents. Ils ont un multiple commun, 12.",
                [("12 = 4 × 3 et 12 = 6 × 2", "On choisit 12 comme dénominateur commun."),
                 (N("3/4") + " = " + N("9/12") + " et " + N("5/6") + " = " + N("10/12"), "On multiplie 3 et 4 par 3, puis 5 et 6 par 2."),
                 (N("9/12 < 10/12"), "Même dénominateur : le plus petit numérateur donne la plus petite fraction."),
                 (N("3/4 < 5/6"), "Donc 3/4 est plus petit que 5/6.")],
                N("3/4 < 5/6"), "d('3')/4<d('5')/6 and d('9')/12<d('10')/12"),
        example("Exemple 2", "Calculer " + N("3/7 + 2/7") + " et " + N("9/10 - 4/10") + ".",
                "Les dénominateurs sont les mêmes : on calcule avec les numérateurs et on garde le dénominateur.",
                [(N("3/7 + 2/7") + " = " + N("5/7"), "3 + 2 = 5 septièmes."),
                 (N("9/10 - 4/10") + " = " + N("5/10"), "9 − 4 = 5 dixièmes."),
                 (N("5/10") + " = " + N("1/2"), "On simplifie par 5 : 1/2.")],
                N("5/7") + " et " + N("1/2"), "d('3')/7+d('2')/7==d('5')/7 and d('9')/10-d('4')/10==d('1')/2"),
        example("Exemple 3", "Calculer " + N("3/4 + 1/8") + ".",
                "8 est un multiple de 4 : on réduit 3/4 au dénominateur 8.",
                [(N("3/4") + " = " + N("6/8"), "On multiplie 3 et 4 par 2."),
                 (N("6/8 + 1/8") + " = " + N("7/8"), "Même dénominateur : 6 + 1 = 7 huitièmes."),
                 ("7/8 est irréductible", "7 et 8 n'ont pas de diviseur commun autre que 1.")],
                N("7/8"), "d('3')/4+d('1')/8==d('7')/8"),
        example("Exemple 4", "Calculer " + N("1/2 + 1/3") + ".",
                "Aucun dénominateur n'est un multiple de l'autre. On cherche un multiple commun : 6.",
                [("6 = 2 × 3 et 6 = 3 × 2", "6 est un multiple de 2 et de 3."),
                 (N("1/2") + " = " + N("3/6") + " et " + N("1/3") + " = " + N("2/6"), "On multiplie par 3 en haut et en bas, puis par 2 en haut et en bas."),
                 (N("3/6 + 2/6") + " = " + N("5/6"), "3 + 2 = 5 sixièmes.")],
                N("5/6"), "d('1')/2+d('1')/3==d('5')/6"),
        example("Exemple 5", "Un gâteau est partagé : Moussa mange 1/4 du gâteau et Awa mange 3/8. Quelle fraction a-t-on mangée ? Quelle fraction reste-t-il ?",
                "On additionne les parts mangées, puis on les retire du gâteau entier, qui vaut 1 = 8/8.",
                [(N("1/4") + " = " + N("2/8"), "On réduit au dénominateur 8."),
                 (N("2/8 + 3/8") + " = " + N("5/8"), "Part mangée en tout : 5 huitièmes."),
                 (N("1 - 5/8") + " = " + N("8/8 - 5/8") + " = " + N("3/8"), "Le gâteau entier vaut 8/8. Il reste 3 huitièmes.")],
                "On a mangé " + N("5/8") + " du gâteau et il en reste " + N("3/8") + ".", "d('1')/4+d('3')/8==d('5')/8 and 1-d('5')/8==d('3')/8"),
        warning("On n'additionne pas les dénominateurs : " + N("1/2 + 1/3") + " ne fait pas " + N("2/5") + ". Les dénominateurs disent la taille des parts : on ne les additionne pas, on les rend égaux."),
    ],
    [
        choice("s3-g1", "operations", "Quel signe faut-il entre " + N("5/8") + " et " + N("3/4") + " ?", [N("5/8 < 3/4"), N("5/8 > 3/4"), N("5/8 = 3/4")], 0,
               hints=["Réduis 3/4 au dénominateur 8."], solution=["3/4 = 6/8.", "5/8 est plus petit que 6/8 : 5/8 < 3/4."],
               wrong={1: "3/4 = 6/8 et 6 est plus grand que 5, donc c'est 3/4 qui est le plus grand."}),
        number("s3-g2", "operations", "Calcule " + N("5/11 + 3/11") + ".", Fraction(8, 11), form="irreducible",
               hints=["Même dénominateur : que fait-on des numérateurs ?"], solution=["5 + 3 = 8, on garde le dénominateur 11.", "5/11 + 3/11 = 8/11."]),
        number("s3-g3", "operations", "Calcule " + N("5/6 - 1/3") + ".", Fraction(1, 2), form="irreducible",
               hints=["Réduis 1/3 au dénominateur 6.", "Soustrais les numérateurs, puis simplifie."], solution=["1/3 = 2/6.", "5/6 − 2/6 = 3/6, qui se simplifie en 1/2."]),
        number("s3-g4", "operations", "Calcule " + N("1/2 + 1/4") + ".", Fraction(3, 4), form="irreducible",
               hints=["4 est un multiple de 2."], solution=["1/2 = 2/4.", "2/4 + 1/4 = 3/4."]),
        number("s3-g5", "operations", "Fatou mange 1/3 d'une tarte et Moussa mange 1/6. Quelle fraction de la tarte reste-t-il ?", Fraction(1, 2), form="irreducible",
               hints=["Additionne les parts mangées, puis retire-les de 6/6."], solution=["1/3 = 2/6. Parts mangées : 2/6 + 1/6 = 3/6.", "Il reste 6/6 − 3/6 = 3/6 = 1/2."]),
    ])

# ----- Section 4: a fraction of a quantity -----
S4 = Section(
    "quantite", "Prendre une fraction d'une quantité", 20, "quantite",
    "Calculer la fraction d'une quantité, et exprimer une part sous forme de fraction.",
    [
        para("Un sac contient 200 F. On en dépense les 3/5. Combien de francs dépense-t-on ? Pour prendre une fraction d'une quantité, on partage la quantité en autant de parts que le dénominateur, "
             "et on prend le nombre de parts indiqué par le numérateur."),
        rule("Fraction d'une quantité",
             "Pour calculer " + "$\\dfrac{a}{b}$" + " d'une quantité " + N("Q") + ", on divise " + N("Q") + " par " + N("b") + ", puis on multiplie le résultat par " + N("a") + " : "
             + "$\\dfrac{a}{b}$" + " de " + N("Q") + " = " + N("Q \\div b \\times a") + "."),
        example("Exemple 1", "Calculer " + N("3/5") + " de 200 F.",
                "On partage 200 F en 5 parts, et on en prend 3.",
                [(N("200 \\div 5") + " = " + N("40"), "Chaque cinquième vaut 40 F."),
                 (N("40 \\times 3") + " = " + N("120"), "Trois cinquièmes valent 3 × 40 = 120 F."),
                 ("Vérification : $\\dfrac{3}{5} = 0{,}6$ et $200 \\times 0{,}6 = 120$", "On retrouve 120.")],
                "On dépense 120 F.", "200//5*3==120 and 200*d('0,6')==120"),
        example("Exemple 2", "Calculer " + N("2/3") + " de 90 kg, puis " + N("3/4") + " de 1 m en centimètres.",
                "Même méthode : on divise par le dénominateur, on multiplie par le numérateur.",
                [(N("90 \\div 3") + " = " + N("30") + " puis " + N("30 \\times 2") + " = " + N("60"), "Les 2/3 de 90 kg font 60 kg."),
                 ("1 m = 100 cm. " + N("100 \\div 4") + " = " + N("25") + " puis " + N("25 \\times 3") + " = " + N("75"), "Les 3/4 d'un mètre font 75 cm.")],
                N("60") + " kg et " + N("75") + " cm", "90//3*2==60 and 100//4*3==75"),
        example("Exemple 3", "Dans une classe de 30 élèves, 12 sont des filles. Quelle fraction de la classe représentent-elles ? Simplifier.",
                "On écrit le nombre de filles sur le nombre total d'élèves, puis on simplifie.",
                [(N("12/30"), "12 parts sur 30."),
                 (N("12/30") + " = " + "$\\dfrac{12 \\div 6}{30 \\div 6}$" + " = " + N("2/5"), "12 et 30 sont divisibles par 6.")],
                "Les filles représentent " + N("2/5") + " de la classe.", "d('12')/30==d('2')/5"),
        example("Exemple 4", "7/12 d'un sac de 60 kg de riz sont vendus. Quelle masse est vendue, et quelle masse reste ?",
                "On calcule la masse vendue avec la fraction, puis le reste par soustraction.",
                [(N("60 \\div 12") + " = " + N("5"), "Chaque douzième pèse 5 kg."),
                 (N("5 \\times 7") + " = " + N("35"), "Les 7/12 pèsent 35 kg : c'est la masse vendue."),
                 (N("60 - 35") + " = " + N("25"), "Il reste 25 kg, c'est-à-dire 5/12 du sac.")],
                "On vend " + N("35") + " kg et il reste " + N("25") + " kg.", "60//12*7==35 and 60-35==25"),
        warning("Prendre les 3/4 de 80 ne veut pas dire ajouter 3/4 à 80 : on partage 80 en 4 parts de 20 et on en prend 3, ce qui fait 60."),
    ],
    [
        number("s4-g1", "quantite", "Calcule " + N("1/4") + " de 80.", Fraction(20),
               hints=["Divise 80 par le dénominateur."], solution=["80 ÷ 4 = 20.", "1/4 de 80 = 20."]),
        number("s4-g2", "quantite", "Calcule " + N("3/5") + " de 150.", Fraction(90),
               hints=["Divise par 5, puis multiplie par 3."], solution=["150 ÷ 5 = 30.", "30 × 3 = 90."]),
        number("s4-g3", "quantite", "Calcule " + N("2/3") + " de 45 kg.", Fraction(30), units=["kg"],
               hints=["Un tiers de 45, puis deux tiers."], solution=["45 ÷ 3 = 15.", "15 × 2 = 30 kg."]),
        number("s4-g4", "quantite", "Dans un panier de 24 fruits, 18 sont des mangues. Quelle fraction du panier est formée de mangues ? (fraction irréductible)", Fraction(3, 4), form="irreducible",
               hints=["Écris 18 sur 24, puis simplifie."], solution=["18/24 = 3/4 (on divise par 6)."]),
        number("s4-g5", "quantite", "Dans une école de 400 élèves, les 3/8 sont des filles du cycle de base. Combien d'élèves cela fait-il ?", Fraction(150),
               hints=["Divise 400 par 8, puis multiplie par 3."], solution=["400 ÷ 8 = 50.", "50 × 3 = 150 élèves."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "sens", "Une pizza est coupée en 8 parts égales. On en mange 3. Quelle fraction de la pizza reste-t-il ?", Fraction(5, 8), 1, ["Combien de parts restent-elles ?"], ["Il reste 8 − 3 = 5 parts sur 8 : 5/8."], form="fraction"),
    number("p2", "sens", "Écris " + N("9/4") + " en nombre décimal.", d("2,25"), 1, ["Divise 9 par 4."], ["9 ÷ 4 = 2,25."], form="decimal"),
    number("p3", "sens", "Écris " + N("0,7") + " sous la forme d'une fraction décimale.", Fraction(7, 10), 1, ["Un chiffre après la virgule."], ["0,7 = 7/10."], form="decimal_fraction"),
    choice("p4", "sens", "Quelle fraction est égale à 1 ?", [N("7/8"), N("8/8"), N("8/7")], 1, 1, ["Quand une fraction vaut-elle 1 ?"], ["8/8 = 1 : toutes les parts de l'unité."], wrong={0: "7/8 est plus petit que 1.", 2: "8/7 est plus grand que 1."}),
    number("p5", "sens", "L'unité d'un segment gradué est partagée en 5 parts égales. Un point est à 8 graduations de l'origine. Quelle fraction ?", Fraction(8, 5), 2, ["Chaque graduation vaut un cinquième."], ["8 graduations valent 8/5 de l'unité."], form="fraction"),
    number("p6", "sens", "Écris " + N("3/8") + " en nombre décimal.", d("0,375"), 2, ["Divise 3 par 8."], ["3 ÷ 8 = 0,375."], form="decimal"),
    choice("p7", "sens", "Awa coupe une bande de tissu en 5 morceaux de longueurs différentes et en garde un. Dit-elle qu'elle a gardé 1/5 de la bande ?", ["Oui", "Non, car les morceaux ne sont pas égaux"], 1, 2, ["Que faut-il pour une fraction ?"], ["Les parts doivent être égales pour parler de cinquième."],
           wrong={0: "Pour qu'un morceau soit 1/5, il faut que les 5 morceaux soient égaux."}),
    number("p8", "egales", "Simplifie " + N("10/15") + " au maximum.", Fraction(2, 3), 1, ["Les deux nombres sont divisibles par 5."], ["10 ÷ 5 = 2 et 15 ÷ 5 = 3 : 2/3."], form="irreducible"),
    number("p9", "egales", "Simplifie " + N("24/36") + " au maximum.", Fraction(2, 3), 2, ["Cherche le plus grand diviseur commun, 12."], ["24 ÷ 12 = 2 et 36 ÷ 12 = 3 : 2/3."], form="irreducible"),
    number("p10", "egales", "Complète : " + "$\\dfrac{4}{7} = \\dfrac{?}{35}$" + ". Numérateur manquant ?", Fraction(20), 2, ["Par quel nombre a-t-on multiplié 7 pour obtenir 35 ?"], ["7 × 5 = 35, donc 4 × 5 = 20."]),
    number("p11", "egales", "Simplifie " + N("35/60") + " au maximum.", Fraction(7, 12), 2, ["Le plus grand diviseur commun est 5."], ["35 ÷ 5 = 7 et 60 ÷ 5 = 12 : 7/12."], form="irreducible"),
    number("p12", "egales", "Complète : " + "$\\dfrac{5}{6} = \\dfrac{20}{?}$" + ". Dénominateur manquant ?", Fraction(24), 2, ["Par quel nombre a-t-on multiplié 5 pour obtenir 20 ?"], ["5 × 4 = 20, donc 6 × 4 = 24."]),
    choice("p13", "egales", "3/5 et 4/6 sont-elles égales, puisque 4/6 s'obtient en ajoutant 1 en haut et en bas ?", ["Oui", "Non : ajouter le même nombre ne conserve pas la valeur"], 1, 3, ["3/5 = 0,6 et 4/6 = 0,666..."], ["3/5 = 0,6 mais 4/6 est environ 0,67 : elles sont différentes.", "Il faut multiplier ou diviser, pas ajouter."]),
    number("p14", "egales", "Écris " + N("5/8") + " avec le dénominateur 40. Quel est le numérateur ?", Fraction(25), 2, ["40 = 8 × ?"], ["8 × 5 = 40, donc 5 × 5 = 25."]),
    number("p15", "egales", "Simplifie " + N("84/126") + " au maximum.", Fraction(2, 3), 3, ["Le plus grand diviseur commun est 42."], ["84 ÷ 42 = 2 et 126 ÷ 42 = 3 : 2/3."], form="irreducible"),
    choice("p16", "operations", "Quelle est la plus grande fraction ?", [N("2/5"), N("3/10"), N("1/2")], 2, 2, ["Réduis au dénominateur 10."], ["2/5 = 4/10 ; 3/10 ; 1/2 = 5/10.", "5/10 est le plus grand : 1/2."], wrong={0: "2/5 = 4/10 est plus petit que 1/2 = 5/10."}),
    ordered("p17", "operations", "Range dans l'ordre croissant, en séparant par des points-virgules : " + N("1/2") + " ; " + N("3/8") + " ; " + N("5/8") + " ; " + N("1/4") + ".", [Fraction(1, 4), Fraction(3, 8), Fraction(1, 2), Fraction(5, 8)], 3,
            ["Réduis toutes les fractions au dénominateur 8."], ["1/2 = 4/8 et 1/4 = 2/8.", "2/8 < 3/8 < 4/8 < 5/8, c'est-à-dire 1/4 < 3/8 < 1/2 < 5/8."]),
    number("p18", "operations", "Calcule " + N("4/9 + 2/9") + ".", Fraction(2, 3), 1, ["Même dénominateur."], ["4 + 2 = 6, 6/9 = 2/3 en simplifiant."], form="irreducible"),
    number("p19", "operations", "Calcule " + N("7/10 - 3/10") + ".", Fraction(2, 5), 1, ["Même dénominateur, puis simplifie."], ["7 − 3 = 4, 4/10 = 2/5."], form="irreducible"),
    number("p20", "operations", "Calcule " + N("2/3 + 1/6") + ".", Fraction(5, 6), 2, ["6 est un multiple de 3."], ["2/3 = 4/6.", "4/6 + 1/6 = 5/6."], form="irreducible"),
    number("p21", "operations", "Calcule " + N("3/4 - 1/8") + ".", Fraction(5, 8), 2, ["Réduis 3/4 au dénominateur 8."], ["3/4 = 6/8.", "6/8 − 1/8 = 5/8."], form="irreducible"),
    number("p22", "operations", "Calcule " + N("1/3 + 1/4") + ".", Fraction(7, 12), 3, ["Cherche un multiple commun de 3 et de 4."], ["Dénominateur commun 12 : 1/3 = 4/12 et 1/4 = 3/12.", "4/12 + 3/12 = 7/12."], form="irreducible"),
    number("p23", "operations", "Calcule " + N("5/6 - 1/2") + ".", Fraction(1, 3), 3, ["Réduis 1/2 au dénominateur 6."], ["1/2 = 3/6.", "5/6 − 3/6 = 2/6 = 1/3."], form="irreducible"),
    choice("p24", "operations", "Fatou a calculé " + N("2/3 + 1/4 = 3/7") + ". Quelle est son erreur ?", ["Elle a additionné les numérateurs et les dénominateurs", "Elle a oublié de simplifier", "Elle a soustrait au lieu d'additionner"], 0, 3,
           ["3/7 est-il plus grand que 2/3 ? Le résultat d'une addition doit dépasser chaque terme."], ["2/3 + 1/4 doit être plus grand que 2/3 (environ 0,67), mais 3/7 est environ 0,43.", "Elle a fait (2 + 1)/(3 + 4). Il faut réduire au dénominateur 12 : 8/12 + 3/12 = 11/12."]),
    number("p25", "operations", "Un sac de riz : on en utilise 1/4 le lundi et 1/2 le mardi. Quelle fraction du sac a-t-on utilisée ?", Fraction(3, 4), 2, ["Réduis 1/2 au dénominateur 4."], ["1/2 = 2/4.", "1/4 + 2/4 = 3/4."], form="irreducible"),
    number("p26", "quantite", "Calcule " + N("3/4") + " de 120.", Fraction(90), 1, ["Divise par 4, multiplie par 3."], ["120 ÷ 4 = 30 ; 30 × 3 = 90."]),
    number("p27", "quantite", "Calcule " + N("2/5") + " de 350 F.", Fraction(140), 2, ["Divise par 5, multiplie par 2."], ["350 ÷ 5 = 70 ; 70 × 2 = 140 F."], units=["F"]),
    number("p28", "quantite", "Calcule " + N("5/6") + " de 1 h, en minutes.", Fraction(50), 2, ["1 h = 60 min."], ["60 ÷ 6 = 10 ; 10 × 5 = 50 minutes."], units=["min"]),
    number("p29", "quantite", "Dans une classe de 36 élèves, 15 aiment le football. Quelle fraction ? (irréductible)", Fraction(5, 12), 2, ["Écris 15/36, puis simplifie."], ["15 et 36 sont divisibles par 3 : 5/12."], form="irreducible"),
    number("p30", "quantite", "Un commerçant avait 80 kg de mil. Il en vend les 3/8. Quelle masse vend-il, en kg ?", Fraction(30), 2, ["Divise par 8, multiplie par 3."], ["80 ÷ 8 = 10 ; 10 × 3 = 30 kg."], units=["kg"]),
    number("p31", "quantite", "Un terrain mesure 600 m². Les 2/5 sont plantés de manioc et 1/3 de maïs. Quelle surface reste libre, en m² ?", Fraction(160), 3, ["Calcule chaque surface, puis retire-les de 600."],
           ["2/5 de 600 = 240 m². 1/3 de 600 = 200 m².", "600 − 240 − 200 = 160 m²."], units=["m2", "m²"]),
    number("p32", "quantite", "Awa dépense les 3/5 de ses 2 000 F puis la moitié du reste. Combien lui reste-t-il, en F ?", Fraction(400), 3, ["Après la première dépense, quel est le reste ?"],
           ["3/5 de 2 000 = 1 200 F dépensés ; reste 800 F.", "La moitié de 800 = 400 F dépensés ; il reste 400 F."], units=["F"]),
]

SUMMARY = [
    definition("Fraction", "La fraction " + "$\\dfrac{a}{b}$" + " (b différent de 0) est obtenue en partageant l'unité en b parts égales et en prenant a parts. C'est aussi le quotient de a par b. Une fraction est plus petite que 1 si a < b, égale à 1 si a = b et plus grande que 1 si a > b."),
    rule("Fractions égales", "On ne change pas une fraction en multipliant ou en divisant son numérateur et son dénominateur par un même nombre non nul. Une fraction irréductible ne peut plus être simplifiée."),
    rule("Comparer, additionner, soustraire", "On réduit d'abord les fractions au même dénominateur. Avec le même dénominateur : la plus grande fraction a le plus grand numérateur, et on additionne ou on soustrait les numérateurs en gardant le dénominateur. On simplifie le résultat."),
    rule("Fraction d'une quantité", "Pour prendre " + "$\\dfrac{a}{b}$" + " d'une quantité, on la divise par b puis on multiplie par a."),
    para("Les erreurs à éviter : additionner les dénominateurs ; ajouter le même nombre en haut et en bas pour obtenir une fraction égale ; oublier de simplifier ; appliquer une fraction à la mauvaise quantité."),
]

CONCEPTS = {
    "sens": ("Le sens d'une fraction", "sens"),
    "egales": ("Fractions égales et simplification", "egales"),
    "operations": ("Comparer, additionner, soustraire", "operations"),
    "quantite": ("Fraction d'une quantité", "quantite"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    # 1. a fraction from parts
    total = rng.randint(5, 16)
    part = rng.randint(1, total - 1)
    questions.append(number("a1", "sens", f"Un gâteau est coupé en {total} parts égales. On en mange {part}. Quelle fraction du gâteau a-t-on mangée ?", Fraction(part, total), 1,
                            ["Parts mangées sur parts totales."], [f"{part} parts sur {total} : {part}/{total}."], form="fraction"))
    # 2. fraction to decimal
    b = rng.choice([2, 4, 5, 8, 20, 25])
    a = rng.randint(1, b - 1)
    while (a, b) in {(3, 4), (3, 8), (5, 8), (1, 2), (7, 8)}:
        b = rng.choice([2, 4, 5, 8, 20, 25])
        a = rng.randint(1, b - 1)
    questions.append(number("a2", "sens", "Écris " + N(f"{a}/{b}") + " en nombre décimal.", Fraction(a, b), 2, ["Une fraction est un quotient : divise le numérateur par le dénominateur."],
                            [f"{a} ÷ {b} = {show(Fraction(a, b))}."], form="decimal"))
    # 3. simplify
    p, q = rng.choice([(2, 3), (3, 4), (3, 5), (2, 5), (5, 6), (4, 7), (5, 8), (7, 9), (7, 12), (5, 12)])
    k = rng.choice([2, 3, 4, 5, 6, 7, 9])
    while (p * k, q * k) in {(6, 8), (18, 45), (10, 15), (35, 60), (4, 6), (18, 24), (24, 36), (84, 126), (12, 16)}:
        k = rng.choice([2, 3, 4, 5, 6, 7, 9])
    questions.append(number("a3", "egales", "Simplifie " + N(f"{p * k}/{q * k}") + " au maximum.", Fraction(p, q), 2, ["Cherche un nombre qui divise le numérateur et le dénominateur."],
                            [f"{p * k} et {q * k} sont divisibles par {k} : {p * k} ÷ {k} = {p}, {q * k} ÷ {k} = {q}.", f"{p * k}/{q * k} = {p}/{q}, irréductible."], form="irreducible"))
    # 4. complete an equality
    a, b = rng.choice([(2, 3), (3, 5), (1, 4), (5, 6), (3, 7), (4, 9)])
    k = rng.randint(2, 8)
    while (a, b, k) == (3, 5, 4):
        k = rng.randint(2, 8)
    questions.append(number("a4", "egales", "Complète : " + f"$\\dfrac{{{a}}}{{{b}}} = \\dfrac{{?}}{{{b * k}}}$" + ". Quel est le numérateur manquant ?", Fraction(a * k), 2, [f"Par quel nombre a-t-on multiplié {b} pour obtenir {b * k} ?"],
                            [f"{b} × {k} = {b * k}, donc {a} × {k} = {a * k}.", f"{a}/{b} = {a * k}/{b * k}."]))
    # 5. compare two fractions
    while True:
        b1, b2 = rng.choice([(4, 6), (3, 5), (2, 3), (3, 4), (5, 8), (4, 5), (6, 9), (2, 5)])
        a1, a2 = rng.randint(1, b1 - 1), rng.randint(1, b2 - 1)
        if Fraction(a1, b1) != Fraction(a2, b2):
            break
    first, second = Fraction(a1, b1), Fraction(a2, b2)
    signs = ["<", ">", "="]
    right = 0 if first < second else 1
    left_text, right_text = f"{a1}/{b1}", f"{a2}/{b2}"
    options = [N(f"{left_text} < {right_text}"), N(f"{left_text} > {right_text}"), N(f"{left_text} = {right_text}")]
    common = math.lcm(b1, b2)
    questions.append(choice("a5", "operations", "Quel signe faut-il entre " + N(left_text) + " et " + N(right_text) + " ?", options, right, 2, ["Réduis les deux fractions au même dénominateur."],
                            [f"Dénominateur commun {common} : {a1 * common // b1}/{common} et {a2 * common // b2}/{common}.", f"{a1 * common // b1} et {a2 * common // b2} : {'la première est plus petite' if first < second else 'la première est plus grande'}."],
                            wrong={1 - right: "Compare les numérateurs après avoir réduit au même dénominateur."}))
    # 6. same denominator
    c = rng.randint(5, 20)
    a1, a2 = rng.randint(1, c - 2), rng.randint(1, c - 2)
    if rng.random() < 0.5 or a1 + a2 >= c:
        a1, a2 = max(a1, a2), min(a1, a2)
        sign, value = "-", Fraction(a1 - a2, c)
    else:
        sign, value = "+", Fraction(a1 + a2, c)
    if value == 0:
        a1 += 1
        sign, value = "-", Fraction(a1 - a2, c)
    questions.append(number("a6", "operations", "Calcule " + N(f"{a1}/{c} {sign} {a2}/{c}") + ". Donne le résultat sous forme irréductible.", value, 2, ["Même dénominateur : calcule avec les numérateurs, puis simplifie."],
                            [f"{a1} {sign} {a2} = {a1 + a2 if sign == '+' else a1 - a2}, avec le dénominateur {c}.", f"Résultat simplifié : {frac(value)}."], form="irreducible"))
    # 7. denominator a multiple of the other, addition
    d1, k = rng.choice([2, 3, 4, 5]), rng.choice([2, 3])
    d2 = d1 * k
    a1, a2 = rng.randint(1, d1 - 1), rng.randint(1, d2 - 1)
    while Fraction(a1, d1) + Fraction(a2, d2) >= 1:
        d1, k = rng.choice([2, 3, 4, 5]), rng.choice([2, 3])
        d2 = d1 * k
        a1, a2 = rng.randint(1, d1 - 1), rng.randint(1, d2 - 1)
    value = Fraction(a1, d1) + Fraction(a2, d2)
    questions.append(number("a7", "operations", "Calcule " + N(f"{a1}/{d1} + {a2}/{d2}") + ". Donne le résultat sous forme irréductible.", value, 3, [f"Réduis la première fraction au dénominateur {d2}."],
                            [f"{a1}/{d1} = {a1 * k}/{d2}.", f"{a1 * k}/{d2} + {a2}/{d2} = {a1 * k + a2}/{d2} = {frac(value)}."], form="irreducible"))
    # 8. denominator a multiple of the other, subtraction
    d1, k = rng.choice([2, 3, 4, 5]), rng.choice([2, 3])
    d2 = d1 * k
    a2 = rng.randint(1, d2 - 1)
    a1 = rng.randint(1, d1 - 1)
    if Fraction(a1, d1) <= Fraction(a2, d2):
        a1, a2 = d1 - 1, 1
    value = Fraction(a1, d1) - Fraction(a2, d2)
    questions.append(number("a8", "operations", "Calcule " + N(f"{a1}/{d1} - {a2}/{d2}") + ". Donne le résultat sous forme irréductible.", value, 3, [f"Réduis la première fraction au dénominateur {d2}."],
                            [f"{a1}/{d1} = {a1 * k}/{d2}.", f"{a1 * k}/{d2} − {a2}/{d2} = {a1 * k - a2}/{d2} = {frac(value)}."], form="irreducible"))
    # 9. fraction of a quantity
    b = rng.choice([3, 4, 5, 6, 8, 10])
    a = rng.randint(1, b - 1)
    quantity = b * rng.randint(4, 30)
    questions.append(number("a9", "quantite", f"Calcule {N(f'{a}/{b}')} de {quantity}.", Fraction(quantity * a, b), 2, ["Divise par le dénominateur, puis multiplie par le numérateur."],
                            [f"{quantity} ÷ {b} = {quantity // b}.", f"{quantity // b} × {a} = {quantity * a // b}."]))
    # 10. a share written as a fraction
    total = rng.choice([20, 24, 30, 36, 40, 45, 60])
    part = rng.choice([x for x in range(2, total) if math.gcd(x, total) > 1])
    questions.append(number("a10", "quantite", f"Dans une classe de {total} élèves, {part} sont absents. Quelle fraction de la classe est absente ? Donne une fraction irréductible.", Fraction(part, total), 3,
                            ["Écris la fraction, puis simplifie."], [f"{part}/{total}, divisible par {math.gcd(part, total)} : {frac(Fraction(part, total))}."], form="irreducible"))
    # 11. leftover after two fractions
    while True:
        d1, k = rng.choice([3, 4, 5, 6]), rng.choice([2, 3])
        d2 = d1 * k
        a1, a2 = rng.randint(1, d1 - 1), rng.randint(1, d2 - 1)
        if Fraction(a1, d1) + Fraction(a2, d2) < 1 and (Fraction(a1, d1), Fraction(a2, d2)) not in {(Fraction(1, 4), Fraction(3, 8)), (Fraction(1, 3), Fraction(1, 6)), (Fraction(1, 4), Fraction(1, 2))}:
            break
    eaten = Fraction(a1, d1) + Fraction(a2, d2)
    value = 1 - eaten
    questions.append(number("a11", "operations", f"On utilise {N(f'{a1}/{d1}')} d'un sac de riz le lundi puis {N(f'{a2}/{d2}')} le mardi. Quelle fraction du sac reste-t-il ? Donne une fraction irréductible.", value, 3,
                            ["Additionne les parts utilisées, puis retire-les de 1."],
                            [f"{a1}/{d1} = {a1 * k}/{d2}. Utilisé : {a1 * k}/{d2} + {a2}/{d2} = {a1 * k + a2}/{d2}.", f"Reste : {d2}/{d2} − {a1 * k + a2}/{d2} = {frac(value)}."], form="irreducible"))
    # 12. the classic mistake
    pairs = [(2, 3), (3, 4), (2, 5), (3, 5)]
    x, y = rng.choice(pairs)
    options = ["Elle a additionné les numérateurs et les dénominateurs, alors qu'il faut réduire au même dénominateur", "Elle a oublié de simplifier", "Elle a soustrait au lieu d'additionner"]
    order = [0, 1, 2]
    rng.shuffle(order)
    claim = N(f"1/{x} + 1/{y} = 2/{x + y}")
    questions.append(choice("a12", "operations", f"Fatou a écrit {claim}. D'où vient son erreur ?", [options[i] for i in order], order.index(0), 3,
                            ["Le résultat d'une addition doit être plus grand que chacun des termes."],
                            [f"1/{x} + 1/{y} est plus grand que 1/{x}, mais 2/{x + y} est plus petit.", f"Le bon calcul : dénominateur commun {x * y} : {y}/{x * y} + {x}/{x * y} = {x + y}/{x * y}."],
                            wrong={order.index(1): "Même simplifiée, 2/" + str(x + y) + " ne serait pas le bon résultat.", order.index(2): "Elle a bien additionné, mais de la mauvaise façon."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=6, title="Les fractions", language="fr",
    intro="Un gâteau partagé en 8, les 3/4 d'un mètre de tissu, la moitié d'un sac de riz : les fractions décrivent des parts d'un tout. Ce chapitre t'apprend à lire une fraction, à reconnaître deux fractions égales, "
          "à comparer, additionner et soustraire des fractions, et à prendre une fraction d'une quantité.",
    objectives=["Comprendre une fraction comme des parts d'une unité, la placer sur un segment gradué et la comparer à 1.",
                "Écrire une fraction en nombre décimal et un décimal en fraction décimale.",
                "Reconnaître des fractions égales, les compléter et simplifier une fraction.",
                "Comparer, additionner et soustraire des fractions, en les réduisant au même dénominateur.",
                "Calculer la fraction d'une quantité et exprimer une part sous forme de fraction."],
    prerequisites=[{"text": "Comprendre ce que veut dire une fraction : partager l'unité en parts égales."},
                   {"text": "Multiplier et diviser des nombres entiers."}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Sixth chapter of the Senegal Sixième course. Its contents follow lesson 11 of the Côte d'Ivoire Sixième programme (fractions, decimal fractions, equal fractions, simplifying, comparing, adding, a fraction of a quantity), which was read for it, "
                "so it is also offered there, but the programme's own situations and activities are not reproduced. It has not been checked against the official Senegalese programme.",
)
