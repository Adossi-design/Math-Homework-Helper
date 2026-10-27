"""Sixième, Organiser un calcul: the fourth chapter of the Senegal Sixième course, written in French.

The topics follow the "organisation d'un calcul" chapter of the ADEM-Dakar Sixième booklet (priority rules, parentheses, translating words
into a calculation), but every explanation, example and exercise was written independently, with our own numbers.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-6e-calcul"
number, choice, ordered, between = make_kit(CHAPTER_ID)

# ----- Section 1: priority rules without parentheses -----
S1 = Section(
    "priorites", "Les règles de priorité sans parenthèses", 22, "priorites",
    "Calculer une suite d'opérations sans parenthèses dans le bon ordre et expliquer pourquoi l'ordre compte.",
    [
        para("Deux élèves calculent " + N("3 + 4 \\times 2") + ". Le premier fait 3 + 4 = 7, puis 7 × 2 = 14. Le second fait 4 × 2 = 8, puis 3 + 8 = 11. Qui a raison ? "
             "Un même calcul ne peut pas avoir deux résultats : tout le monde doit suivre les mêmes règles. Imagine que tu achètes 3 bonbons à 1 F puis 4 sachets de 2 bonbons : tu as 3 + 4 × 2 = 11 bonbons. "
             "La multiplication est faite avant l'addition."),
        rule("Priorité de la multiplication et de la division",
             "Dans une suite d'opérations sans parenthèses, on effectue d'abord les multiplications et les divisions, puis les additions et les soustractions."),
        rule("Calculer de gauche à droite",
             "Quand il n'y a que des additions et des soustractions, ou que des multiplications et des divisions, on calcule de gauche à droite, dans l'ordre où on lit l'expression."),
        example("Exemple 1", "Calculer " + N("7 + 3 \\times 5") + ".",
                "On repère la multiplication, qui est prioritaire, et on la calcule en premier.",
                [(N("7 + 3 \\times 5"), "Il y a une addition et une multiplication : la multiplication passe d'abord."),
                 (N("7 + 15"), "3 × 5 = 15. On recopie le reste de l'expression sans le changer."),
                 (N("22"), "7 + 15 = 22.")],
                N("22"), "7+3*5==22"),
        example("Exemple 2", "Calculer " + N("6 \\times 5 - 24 \\div 4 + 8") + ".",
                "Il y a deux opérations prioritaires : 6 × 5 et 24 ÷ 4. On les calcule toutes les deux, puis on fait les additions et soustractions de gauche à droite.",
                [(N("6 \\times 5 - 24 \\div 4 + 8"), "Les opérations prioritaires sont 6 × 5 et 24 ÷ 4."),
                 (N("30 - 6 + 8"), "6 × 5 = 30 et 24 ÷ 4 = 6."),
                 (N("24 + 8"), "On va de gauche à droite : 30 − 6 = 24."),
                 (N("32"), "24 + 8 = 32.")],
                N("32"), "6*5-24/4+8==32"),
        example("Exemple 3", "Calculer " + N("40 - 12 + 5") + " et " + N("48 \\div 6 \\times 2") + ".",
                "Il n'y a que des opérations de même priorité : on calcule de gauche à droite.",
                [(N("40 - 12 + 5") + " = " + N("28 + 5") + " = " + N("33"), "40 − 12 = 28 d'abord, puis 28 + 5 = 33. Si on avait fait 12 + 5 d'abord, on aurait trouvé 23, ce qui est faux."),
                 (N("48 \\div 6 \\times 2") + " = " + N("8 \\times 2") + " = " + N("16"), "48 ÷ 6 = 8 d'abord, puis 8 × 2 = 16. Si on avait fait 6 × 2 d'abord, on aurait trouvé 4, ce qui est faux.")],
                N("33") + " ; " + N("16"), "40-12+5==33 and 48/6*2==16"),
        example("Exemple 4", "Calculer " + N("4,5 + 2,5 \\times 3") + ".",
                "Les règles sont les mêmes avec des nombres décimaux.",
                [(N("4,5 + 2,5 \\times 3"), "La multiplication est prioritaire."),
                 (N("4,5 + 7,5"), "2,5 × 3 = 7,5 : 25 × 3 = 75, avec un chiffre après la virgule."),
                 (N("12"), "4,5 + 7,5 = 12.")],
                N("12"), "d('4,5')+d('2,5')*3==12"),
        warning("On ne calcule pas toujours de gauche à droite : " + N("3 + 4 \\times 2") + " vaut 11, et non 14. C'est seulement entre opérations de même priorité qu'on va de gauche à droite."),
    ],
    [
        number("s1-g1", "priorites", "Calcule " + N("5 + 4 \\times 3") + ".", Fraction(17),
               hints=["Quelle opération est prioritaire ?"], solution=["La multiplication d'abord : 4 × 3 = 12.", "5 + 12 = 17."]),
        number("s1-g2", "priorites", "Calcule " + N("20 - 6 \\div 2") + ".", Fraction(17),
               hints=["Quelle opération est prioritaire, la soustraction ou la division ?"], solution=["La division d'abord : 6 ÷ 2 = 3.", "20 − 3 = 17."]),
        number("s1-g3", "priorites", "Calcule " + N("50 - 8 + 5") + ".", Fraction(47),
               hints=["Ces deux opérations ont la même priorité : dans quel ordre les fait-on ?"], solution=["De gauche à droite : 50 − 8 = 42.", "42 + 5 = 47."]),
        number("s1-g4", "priorites", "Calcule " + N("36 \\div 6 \\times 3") + ".", Fraction(18),
               hints=["Division et multiplication ont la même priorité : commence par la gauche."], solution=["36 ÷ 6 = 6.", "6 × 3 = 18."]),
        choice("s1-g5", "priorites", "Dans " + N("14 + 3 \\times 2 - 5") + ", quelle opération doit-on faire en premier ?", [N("14 + 3"), N("3 \\times 2"), N("2 - 5")], 1,
               hints=["Cherche l'opération qui a la priorité."], solution=["La multiplication 3 × 2 est prioritaire : on la calcule en premier.", "On obtient 14 + 6 − 5, puis 20 − 5 = 15."],
               wrong={0: "14 + 3 n'est pas prioritaire : le 3 appartient au produit 3 × 2, qui doit être fait avant l'addition."}),
    ])

# ----- Section 2: parentheses -----
S2 = Section(
    "parentheses", "Les parenthèses", 22, "parentheses",
    "Calculer une expression avec des parenthèses, y compris imbriquées, et voir comment elles changent le résultat.",
    [
        para("Si on veut vraiment additionner d'abord, il faut le dire. Les parenthèses servent à cela : elles regroupent ce qui doit être calculé en premier. "
             "Ainsi " + N("(3 + 4) \\times 2") + " vaut 14, alors que " + N("3 + 4 \\times 2") + " vaut 11."),
        rule("Priorité des parenthèses",
             "On calcule d'abord ce qui est entre parenthèses, en respectant les règles de priorité à l'intérieur. S'il y a des parenthèses dans des parenthèses, on commence par les plus intérieures."),
        example("Exemple 1", "Calculer " + N("(12,5 - 2,5) \\times 4 + 6") + ".",
                "On calcule la parenthèse, puis la multiplication, puis l'addition.",
                [(N("(12,5 - 2,5) \\times 4 + 6"), "La parenthèse est prioritaire."),
                 (N("10 \\times 4 + 6"), "12,5 − 2,5 = 10."),
                 (N("40 + 6"), "Maintenant la multiplication est prioritaire sur l'addition : 10 × 4 = 40."),
                 (N("46"), "40 + 6 = 46.")],
                N("46"), "(d('12,5')-d('2,5'))*4+6==46"),
        example("Exemple 2", "Calculer " + N("2 \\times (7 + 3 \\times 4)") + ".",
                "Dans la parenthèse, il y a une addition et une multiplication : on applique la règle de priorité à l'intérieur.",
                [(N("2 \\times (7 + 3 \\times 4)"), "On s'occupe de la parenthèse : 3 × 4 est prioritaire dedans."),
                 (N("2 \\times (7 + 12)"), "3 × 4 = 12."),
                 (N("2 \\times 19"), "7 + 12 = 19. La parenthèse est terminée."),
                 (N("38"), "2 × 19 = 38.")],
                N("38"), "2*(7+3*4)==38"),
        example("Exemple 3", "Calculer " + N("50 - (4 + (12 - 9) \\times 2)") + ".",
                "Il y a des parenthèses dans des parenthèses : on commence par les plus intérieures.",
                [(N("50 - (4 + (12 - 9) \\times 2)"), "La parenthèse la plus intérieure est (12 − 9)."),
                 (N("50 - (4 + 3 \\times 2)"), "12 − 9 = 3."),
                 (N("50 - (4 + 6)"), "Dans la grande parenthèse, la multiplication est prioritaire : 3 × 2 = 6."),
                 (N("50 - 10"), "4 + 6 = 10."),
                 (N("40"), "50 − 10 = 40.")],
                N("40"), "50-(4+(12-9)*2)==40"),
        example("Exemple 4", "Comparer " + N("12 - (5 - 2)") + " et " + N("12 - 5 - 2") + ".",
                "Les deux expressions ont les mêmes nombres, mais les parenthèses changent l'ordre des calculs.",
                [(N("12 - (5 - 2)") + " = " + N("12 - 3") + " = " + N("9"), "On calcule la parenthèse d'abord : 5 − 2 = 3."),
                 (N("12 - 5 - 2") + " = " + N("7 - 2") + " = " + N("5"), "Sans parenthèses, on va de gauche à droite : 12 − 5 = 7.")],
                N("9") + " et " + N("5") + ", donc elles ne sont pas égales", "12-(5-2)==9 and 12-5-2==5"),
        warning("On ne supprime pas des parenthèses sans réfléchir : " + N("12 - (5 - 2)") + " vaut 9, mais " + N("12 - 5 - 2") + " vaut 5."),
    ],
    [
        number("s2-g1", "parentheses", "Calcule " + N("(7 + 5) \\times 3") + ".", Fraction(36),
               hints=["Que fait-on en premier ?"], solution=["Parenthèse d'abord : 7 + 5 = 12.", "12 × 3 = 36."]),
        number("s2-g2", "parentheses", "Calcule " + N("4 \\times (9 - 6) + 2") + ".", Fraction(14),
               hints=["Calcule la parenthèse, puis la multiplication, puis l'addition."], solution=["9 − 6 = 3.", "4 × 3 = 12, puis 12 + 2 = 14."]),
        number("s2-g3", "parentheses", "Calcule " + N("30 - (8 + 7)") + ".", Fraction(15),
               hints=["La parenthèse est prioritaire."], solution=["8 + 7 = 15.", "30 − 15 = 15."]),
        number("s2-g4", "parentheses", "Calcule " + N("2 \\times (3 + 4 \\times 2)") + ".", Fraction(22),
               hints=["Dans la parenthèse, quelle opération est prioritaire ?"], solution=["Dans la parenthèse : 4 × 2 = 8, puis 3 + 8 = 11.", "2 × 11 = 22."]),
        choice("s2-g5", "parentheses", "Quelle est la valeur de " + N("(12 - 4) \\div 2 + 1") + " ?", [N("5"), N("9"), N("3")], 0,
               hints=["Calcule la parenthèse, puis la division, puis l'addition."], solution=["12 − 4 = 8.", "8 ÷ 2 = 4, puis 4 + 1 = 5."],
               wrong={1: "Tu as fait 4 + 1 avant la division. La division est prioritaire sur l'addition : 8 ÷ 2 d'abord, puis + 1.", 2: "Tu as fait 2 + 1 = 3 d'abord. 2 est le diviseur de 8, pas un terme de l'addition."}),
    ])

# ----- Section 3: translating words and solving problems -----
S3 = Section(
    "traduire", "Traduire une phrase en calcul et résoudre un problème", 24, "traduire",
    "Passer d'une phrase à une expression, et d'une expression à une phrase, puis résoudre des problèmes en plusieurs étapes.",
    [
        para("Pour résoudre un problème, il faut souvent écrire un calcul en une seule ligne. Les mots que tu connais te guident : la somme est le résultat d'une addition, la différence celui d'une soustraction, "
             "le produit celui d'une multiplication, le quotient celui d'une division."),
        rule("Le vocabulaire des opérations",
             "« la somme de a et b » se traduit " + N("a + b") + ". « la différence de a et b » se traduit " + N("a - b") + ". « le produit de a par b » se traduit " + N("a \\times b")
             + ". « le quotient de a par b » se traduit " + N("a \\div b") + ". Quand une opération est faite avec le résultat d'une autre, on utilise des parenthèses."),
        example("Exemple 1", "Traduire « le quotient de 36 par la somme de 4 et 5 » par une expression, puis la calculer.",
                "La somme de 4 et 5 est un nombre, qui sert de diviseur : il faut des parenthèses.",
                [("la somme de 4 et 5 : " + N("4 + 5"), "On traduit d'abord la partie qui sert de diviseur."),
                 (N("36 \\div (4 + 5)"), "Le quotient de 36 par cette somme. Sans parenthèses on lirait 36 ÷ 4 + 5, qui est autre chose."),
                 (N("36 \\div 9") + " = " + N("4"), "4 + 5 = 9, puis 36 ÷ 9 = 4.")],
                N("36 \\div (4 + 5) = 4"), "36/(4+5)==4"),
        example("Exemple 2", "Traduire « le double de la somme de 7 et 5, diminué de 4 » par une expression, puis la calculer.",
                "Le double de quelque chose, c'est 2 fois cette chose. « Diminué de 4 » veut dire qu'on retire 4 à la fin.",
                [("la somme de 7 et 5 : " + N("7 + 5"), "La partie à doubler."),
                 (N("2 \\times (7 + 5) - 4"), "Le double de cette somme, puis on retire 4."),
                 (N("2 \\times 12 - 4") + " = " + N("24 - 4") + " = " + N("20"), "7 + 5 = 12, puis 2 × 12 = 24, puis 24 − 4 = 20.")],
                N("2 \\times (7 + 5) - 4 = 20"), "2*(7+5)-4==20"),
        example("Exemple 3", "Un élève achète 3 cahiers à 250 F et 2 stylos à 100 F. Il paie avec un billet de 1 000 F. Combien lui rend-on ?",
                "On calcule d'abord la dépense totale, puis ce qu'on rend. On écrit tout en une ligne avec des parenthèses.",
                [("Dépense = " + N("3 \\times 250 + 2 \\times 100"), "3 cahiers à 250 F et 2 stylos à 100 F."),
                 ("Argent rendu = " + N("1000 - (3 \\times 250 + 2 \\times 100)"), "Le billet moins la dépense : les parenthèses regroupent toute la dépense."),
                 (N("1000 - (750 + 200)"), "Dans la parenthèse, les multiplications sont prioritaires : 3 × 250 = 750 et 2 × 100 = 200."),
                 (N("1000 - 950") + " = " + N("50"), "750 + 200 = 950, puis 1 000 − 950 = 50.")],
                "On lui rend 50 F.", "1000-(3*250+2*100)==50"),
        example("Exemple 4", "Traduire en phrase l'expression " + N("4,5 \\times (8 - 3)") + ", puis la calculer.",
                "On lit l'expression de l'intérieur vers l'extérieur.",
                [("la parenthèse " + N("8 - 3") + " est la différence de 8 et 3", "On nomme la partie entre parenthèses."),
                 ("L'expression est le produit de 4,5 par la différence de 8 et 3", "La multiplication porte sur 4,5 et sur cette différence."),
                 (N("4,5 \\times 5") + " = " + N("22,5"), "8 − 3 = 5, puis 4,5 × 5 = 22,5.")],
                N("22,5"), "d('4,5')*(8-3)==d('22,5')"),
        example("Exemple 5", "Awa achète 2,5 kg de riz à 600 F le kilogramme et 1,5 kg d'oignons à 400 F le kilogramme. Elle donne 2 500 F. Combien lui rend-on ?",
                "Même démarche : une ligne avec la dépense entre parenthèses.",
                [("Argent rendu = " + N("2500 - (2,5 \\times 600 + 1,5 \\times 400)"), "Le billet moins la dépense totale."),
                 (N("2500 - (1500 + 600)"), "2,5 × 600 = 1 500 et 1,5 × 400 = 600."),
                 (N("2500 - 2100") + " = " + N("400"), "1 500 + 600 = 2 100, puis 2 500 − 2 100 = 400.")],
                "On lui rend 400 F.", "2500-(d('2,5')*600+d('1,5')*400)==400"),
        warning("Quand une phrase parle de la somme ou de la différence « de quelque chose », ce quelque chose doit être entre parenthèses : « le produit de 3 par la somme de 4 et 5 » est " + N("3 \\times (4 + 5)") + " = 27, et non " + N("3 \\times 4 + 5") + " = 17."),
    ],
    [
        number("s3-g1", "traduire", "Écris et calcule : la somme de 12 et 8, multipliée par 3.", Fraction(60),
               hints=["La somme de 12 et 8 est calculée en premier : comment l'écrire ?"], solution=["(12 + 8) × 3.", "12 + 8 = 20, puis 20 × 3 = 60."]),
        number("s3-g2", "traduire", "Écris et calcule : le produit de 6 par 4, diminué de 5.", Fraction(19),
               hints=["« Diminué de 5 » veut dire qu'on retire 5 au résultat."], solution=["6 × 4 − 5.", "6 × 4 = 24, puis 24 − 5 = 19."]),
        number("s3-g3", "traduire", "Écris et calcule : la différence de 20 et de 6, divisée par 2.", Fraction(7),
               hints=["La différence est calculée avant la division : il faut des parenthèses."], solution=["(20 − 6) ÷ 2.", "20 − 6 = 14, puis 14 ÷ 2 = 7."]),
        number("s3-g4", "problemes", "Un élève achète 4 crayons à 150 F et 3 gommes à 100 F. Combien dépense-t-il, en F ?", Fraction(900), units=["F"],
               hints=["Écris le calcul en une ligne : 4 crayons, plus 3 gommes."], solution=["Dépense = 4 × 150 + 3 × 100.", "4 × 150 = 600 et 3 × 100 = 300, donc 600 + 300 = 900 F."]),
        choice("s3-g5", "traduire", "Quelle expression traduit « le produit de 3 par la somme de 4 et 5 » ?", [N("3 \\times 4 + 5"), N("3 \\times (4 + 5)"), N("(3 \\times 4) + 5")], 1,
               hints=["La somme de 4 et 5 doit être calculée avant le produit."], solution=["La somme de 4 et 5 est un nombre qui se multiplie par 3 : 3 × (4 + 5)."],
               wrong={0: "Dans 3 × 4 + 5, la multiplication se fait avant l'addition : on multiplierait 3 par 4 seulement, pas par la somme.", 2: "Les parenthèses de (3 × 4) + 5 ne changent rien : c'est la même expression que 3 × 4 + 5."}),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "priorites", "Calcule " + N("8 + 2 \\times 5") + ".", Fraction(18), 1, ["Quelle opération est prioritaire ?"], ["2 × 5 = 10 puis 8 + 10 = 18."]),
    number("p2", "priorites", "Calcule " + N("30 - 4 \\times 5") + ".", Fraction(10), 1, ["Multiplication d'abord."], ["4 × 5 = 20 puis 30 − 20 = 10."]),
    number("p3", "priorites", "Calcule " + N("6 \\times 7 - 12 \\div 3") + ".", Fraction(38), 2, ["Fais les deux opérations prioritaires, puis la soustraction."], ["6 × 7 = 42 et 12 ÷ 3 = 4.", "42 − 4 = 38."]),
    number("p4", "priorites", "Calcule " + N("100 - 25 + 5") + ".", Fraction(80), 1, ["Va de gauche à droite."], ["100 − 25 = 75 puis 75 + 5 = 80."]),
    number("p5", "priorites", "Calcule " + N("90 \\div 9 \\times 5") + ".", Fraction(50), 2, ["Division et multiplication ont la même priorité."], ["90 ÷ 9 = 10 puis 10 × 5 = 50."]),
    number("p6", "priorites", "Calcule " + N("2,5 + 1,5 \\times 4") + ".", d("8,5"), 2, ["Multiplication d'abord, puis addition."], ["1,5 × 4 = 6.", "2,5 + 6 = 8,5."], form="decimal"),
    number("p7", "priorites", "Calcule " + N("18 \\div 3 + 4 \\times 2,5") + ".", Fraction(16), 3, ["Il y a deux opérations prioritaires."], ["18 ÷ 3 = 6 et 4 × 2,5 = 10.", "6 + 10 = 16."]),
    number("p8", "priorites", "Calcule " + N("7,2 - 2 \\times 0,6 + 0,5") + ".", d("6,5"), 3, ["Multiplication d'abord, puis de gauche à droite."], ["2 × 0,6 = 1,2.", "7,2 − 1,2 = 6, puis 6 + 0,5 = 6,5."], form="decimal"),
    choice("p9", "priorites", "Moussa a calculé " + N("3 + 4 \\times 2 = 14") + ". Quelle erreur a-t-il faite ?", ["Il a fait l'addition avant la multiplication", "Il a fait une erreur de table de multiplication", "Il a oublié une parenthèse"], 0, 2,
           ["Refais le calcul en commençant par l'opération prioritaire."], ["La multiplication est prioritaire : 4 × 2 = 8 puis 3 + 8 = 11.", "Moussa a fait 3 + 4 = 7 puis 7 × 2 = 14 : il a ignoré la priorité."],
           wrong={2: "Il n'y a pas de parenthèse dans l'expression de départ : l'erreur vient de l'ordre des opérations."}),
    choice("p10", "priorites", "Quelle est la valeur de " + N("20 - 8 + 3") + " ?", [N("9"), N("15"), N("25")], 1, 1, ["Va de gauche à droite."], ["20 − 8 = 12 puis 12 + 3 = 15."],
           wrong={0: "Tu as calculé 8 + 3 = 11 d'abord. Entre opérations de même priorité, on va de gauche à droite."}),
    number("p11", "parentheses", "Calcule " + N("(9 + 6) \\times 4") + ".", Fraction(60), 1, ["Parenthèse d'abord."], ["9 + 6 = 15 puis 15 × 4 = 60."]),
    number("p12", "parentheses", "Calcule " + N("5 \\times (12 - 7)") + ".", Fraction(25), 1, ["Parenthèse d'abord."], ["12 − 7 = 5 puis 5 × 5 = 25."]),
    number("p13", "parentheses", "Calcule " + N("45 - (18 + 7)") + ".", Fraction(20), 1, ["Parenthèse d'abord."], ["18 + 7 = 25 puis 45 − 25 = 20."]),
    number("p14", "parentheses", "Calcule " + N("(7,5 - 2,5) \\times 4 + 3") + ".", Fraction(23), 2, ["Parenthèse, puis multiplication, puis addition."], ["7,5 − 2,5 = 5.", "5 × 4 = 20 puis 20 + 3 = 23."]),
    number("p15", "parentheses", "Calcule " + N("3 \\times (4 + 2 \\times 5)") + ".", Fraction(42), 2, ["Dans la parenthèse, quelle opération est prioritaire ?"], ["Dans la parenthèse : 2 × 5 = 10 puis 4 + 10 = 14.", "3 × 14 = 42."]),
    number("p16", "parentheses", "Calcule " + N("80 \\div (2 + 3)") + ".", Fraction(16), 2, ["Parenthèse d'abord, puis division."], ["2 + 3 = 5 puis 80 ÷ 5 = 16."]),
    number("p17", "parentheses", "Calcule " + N("(50 - 14) \\div 4 + 6") + ".", Fraction(15), 2, ["Parenthèse, division, addition."], ["50 − 14 = 36.", "36 ÷ 4 = 9 puis 9 + 6 = 15."]),
    number("p18", "parentheses", "Calcule " + N("100 - (20 + (15 - 5) \\times 2)") + ".", Fraction(60), 3, ["Commence par la parenthèse la plus intérieure."],
           ["15 − 5 = 10 : la parenthèse intérieure est terminée.", "Dans la grande parenthèse : 10 × 2 = 20 puis 20 + 20 = 40.", "100 − 40 = 60."]),
    choice("p19", "parentheses", "Fatou a calculé " + N("15 - (7 - 3) = 5") + ". Quelle erreur a-t-elle faite ?", ["Elle a supprimé les parenthèses et calculé 15 − 7 − 3", "Elle a fait une erreur de soustraction", "Elle a ajouté au lieu de soustraire"], 0, 3,
           ["Calcule d'abord ce qui est entre parenthèses."], ["7 − 3 = 4 puis 15 − 4 = 11.", "Fatou a trouvé 5 = 15 − 7 − 3 : elle n'a pas respecté la parenthèse."]),
    choice("p20", "parentheses", "Quelle est la valeur de " + N("12 - (4 + 3)") + " ?", [N("5"), N("11"), N("13")], 0, 1, ["Parenthèse d'abord."], ["4 + 3 = 7 puis 12 − 7 = 5."],
           wrong={1: "Tu as calculé 12 − 4 + 3 = 11. La parenthèse doit être calculée d'abord : 12 − (4 + 3) = 12 − 7."}),
    number("p21", "traduire", "Écris et calcule : le double de la somme de 6 et 9.", Fraction(30), 1, ["Le double de quelque chose, c'est 2 fois cette chose."], ["2 × (6 + 9) = 2 × 15 = 30."]),
    number("p22", "traduire", "Écris et calcule : le quotient de 48 par la différence de 11 et 5.", Fraction(8), 2, ["La différence est calculée avant le quotient."], ["48 ÷ (11 − 5) = 48 ÷ 6 = 8."]),
    number("p23", "traduire", "Écris et calcule : le produit de 2,5 par la somme de 3 et 1.", Fraction(10), 2, ["Écris la somme entre parenthèses."], ["2,5 × (3 + 1) = 2,5 × 4 = 10."]),
    number("p24", "traduire", "Écris et calcule : la somme du produit de 3 par 7 et du quotient de 20 par 4.", Fraction(26), 3, ["Il y a deux parties : un produit et un quotient, puis on les additionne."], ["3 × 7 + 20 ÷ 4.", "21 + 5 = 26."]),
    choice("p25", "traduire", "Quelle expression traduit « la différence de 50 et du produit de 4 par 6 » ?", [N("(50 - 4) \\times 6"), N("50 - 4 \\times 6"), N("50 - 4 + 6")], 1, 2,
           ["Le produit de 4 par 6 est retranché de 50."], ["On retranche à 50 le produit 4 × 6 : 50 − 4 × 6, et la multiplication est déjà prioritaire.", "50 − 24 = 26."],
           wrong={0: "Dans (50 − 4) × 6 on soustrait 4 d'abord, puis on multiplie par 6 : ce n'est pas ce que dit la phrase."}),
    number("p26", "problemes", "Un élève achète 3 cahiers à 350 F et un stylo à 125 F. Il paie avec 2 000 F. Combien lui rend-on, en F ?", Fraction(825), 3, ["Dépense d'abord, puis argent rendu."],
           ["Dépense = 3 × 350 + 125 = 1 050 + 125 = 1 175.", "2 000 − 1 175 = 825 F."], units=["F"]),
    number("p27", "problemes", "Un rectangle mesure 12,5 m de long et 8 m de large. Quel est son périmètre, en m ? (Périmètre = 2 × (longueur + largeur).)", Fraction(41), 2, ["Calcule d'abord la somme longueur + largeur."], ["2 × (12,5 + 8) = 2 × 20,5 = 41 m."], units=["m"]),
    number("p28", "problemes", "Un commerçant a 6 sacs de 25 kg. Il en vend 4. Quelle masse lui reste-t-il, en kg ?", Fraction(50), 2, ["Combien de sacs restent-ils ?"], ["(6 − 4) × 25 = 2 × 25 = 50 kg."], units=["kg"]),
    number("p29", "problemes", "Un livre coûte 1 800 F et un cahier 450 F. On achète un livre et deux cahiers, avec une remise de 300 F sur le total. Combien paie-t-on, en F ?", Fraction(2400), 3,
           ["Calcule le total avant la remise, puis retire la remise."], ["Total = 1 800 + 2 × 450 = 1 800 + 900 = 2 700.", "2 700 − 300 = 2 400 F."], units=["F"]),
    number("p30", "problemes", "Deux sacs contiennent 120 kg et 80 kg de riz, partagés à parts égales entre 4 familles. Quelle masse reçoit chaque famille, en kg ?", Fraction(50), 3,
           ["Le total est partagé : il faut des parenthèses."], ["(120 + 80) ÷ 4 = 200 ÷ 4 = 50 kg."], units=["kg"]),
]

SUMMARY = [
    rule("Les priorités", "Sans parenthèses, on calcule d'abord les multiplications et les divisions, puis les additions et les soustractions. Entre opérations de même priorité, on va de gauche à droite."),
    rule("Les parenthèses", "On calcule d'abord ce qui est entre parenthèses, en respectant les priorités à l'intérieur. Avec des parenthèses imbriquées, on commence par les plus intérieures. Les parenthèses peuvent changer le résultat : " + N("12 - (5 - 2) = 9") + " mais " + N("12 - 5 - 2 = 5") + "."),
    rule("Le vocabulaire", "Somme, différence, produit et quotient sont les résultats d'une addition, d'une soustraction, d'une multiplication et d'une division. « la somme de a et b » : " + N("a + b") + ". « le produit de a par b » : " + N("a \\times b") + ". Quand on opère avec ce résultat, on met des parenthèses."),
    para("Les erreurs à éviter : calculer toujours de gauche à droite sans regarder les priorités ; supprimer des parenthèses ; oublier de mettre en parenthèses une somme ou une différence dans une phrase."),
]

CONCEPTS = {
    "priorites": ("Règles de priorité", "priorites"),
    "parentheses": ("Parenthèses", "parentheses"),
    "traduire": ("Traduire une phrase en calcul", "traduire"),
    "problemes": ("Résoudre un problème en plusieurs étapes", "traduire"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    # 1. a + b x c
    a, b, c = rng.randint(2, 30), rng.randint(2, 9), rng.randint(2, 9)
    questions.append(number("a1", "priorites", "Calcule " + N(f"{a} + {b} \\times {c}") + ".", Fraction(a + b * c), 1, ["Quelle opération est prioritaire ?"],
                            [f"La multiplication d'abord : {b} × {c} = {b * c}.", f"{a} + {b * c} = {a + b * c}."]))
    # 2. a x b - c / d + e
    a, b, divisor, k, e = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 6), rng.randint(2, 9), rng.randint(1, 20)
    c = divisor * k
    questions.append(number("a2", "priorites", "Calcule " + N(f"{a} \\times {b} - {c} \\div {divisor} + {e}") + ".", Fraction(a * b - k + e), 2, ["Il y a deux opérations prioritaires."],
                            [f"{a} × {b} = {a * b} et {c} ÷ {divisor} = {k}.", f"{a * b} − {k} = {a * b - k}, puis {a * b - k} + {e} = {a * b - k + e}."]))
    # 3. left to right
    a = rng.randint(40, 90)
    b, c = rng.randint(5, 30), rng.randint(5, 30)
    questions.append(number("a3", "priorites", "Calcule " + N(f"{a} - {b} + {c}") + ".", Fraction(a - b + c), 1, ["Même priorité : de gauche à droite."],
                            [f"{a} − {b} = {a - b}.", f"{a - b} + {c} = {a - b + c}."]))
    # 4. with decimals
    x, y = rand_decimal(rng, 1, 9, 1), rng.randint(2, 6)
    z = rand_decimal(rng, 1, 9, 1)
    questions.append(number("a4", "priorites", "Calcule " + N(f"{show(x)} + {show(z)} \\times {y}") + ".", x + z * y, 3, ["La multiplication est prioritaire."],
                            [f"{show(z)} × {y} = {show(z * y)}.", f"{show(x)} + {show(z * y)} = {show(x + z * y)}."]))
    # 5. (a + b) x c
    a, b, c = rng.randint(2, 30), rng.randint(2, 30), rng.randint(2, 9)
    questions.append(number("a5", "parentheses", "Calcule " + N(f"({a} + {b}) \\times {c}") + ".", Fraction((a + b) * c), 1, ["Parenthèse d'abord."],
                            [f"{a} + {b} = {a + b}.", f"{a + b} × {c} = {(a + b) * c}."]))
    # 6. (a - b) x c + d x e
    b = rng.randint(2, 20)
    a = b + rng.randint(2, 20)
    c, dd, e = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
    questions.append(number("a6", "parentheses", "Calcule " + N(f"({a} - {b}) \\times {c} + {dd} \\times {e}") + ".", Fraction((a - b) * c + dd * e), 2,
                            ["Parenthèse d'abord, puis les deux multiplications, puis l'addition."],
                            [f"{a} − {b} = {a - b}.", f"({a - b}) × {c} = {(a - b) * c} et {dd} × {e} = {dd * e}.", f"{(a - b) * c} + {dd * e} = {(a - b) * c + dd * e}."]))
    # 7. nested parentheses
    c = rng.randint(5, 15)
    dd = rng.randint(1, c - 1)
    e, b = rng.randint(2, 6), rng.randint(2, 9)
    inner = (c - dd) * e
    a = b + inner + rng.randint(5, 30)
    questions.append(number("a7", "parentheses", "Calcule " + N(f"{a} - ({b} + ({c} - {dd}) \\times {e})") + ".", Fraction(a - (b + inner)), 3, ["Commence par la parenthèse la plus intérieure."],
                            [f"{c} − {dd} = {c - dd}.", f"Dans la grande parenthèse : {c - dd} × {e} = {inner}, puis {b} + {inner} = {b + inner}.", f"{a} − {b + inner} = {a - b - inner}."]))
    # 8. effect of parentheses
    c = rng.randint(2, 8)
    b = c + rng.randint(2, 9)
    a = b + rng.randint(2, 20)
    right, wrong_value = a - (b - c), a - b - c
    options = [N(str(right)), N(str(wrong_value)), N(str(a - b + c + 1))]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a8", "parentheses", "Quelle est la valeur de " + N(f"{a} - ({b} - {c})") + " ?", [options[i] for i in order], order.index(0), 2,
                            ["Calcule la parenthèse d'abord."],
                            [f"{b} − {c} = {b - c}.", f"{a} − {b - c} = {right}."],
                            wrong={order.index(1): "Tu as supprimé les parenthèses et calculé a − b − c. La parenthèse doit être calculée en premier."}))
    # 9. product of a by the sum of b and c
    a, b, c = rng.randint(2, 9), rng.randint(2, 20), rng.randint(2, 20)
    questions.append(number("a9", "traduire", f"Écris et calcule : le produit de {a} par la somme de {b} et {c}.", Fraction(a * (b + c)), 2, ["La somme est calculée avant le produit."],
                            [f"{a} × ({b} + {c}).", f"{b} + {c} = {b + c} puis {a} × {b + c} = {a * (b + c)}."]))
    # 10. quotient of x by the difference of y and z
    z = rng.randint(2, 9)
    y = z + rng.randint(2, 9)
    k = rng.randint(2, 12)
    questions.append(number("a10", "traduire", f"Écris et calcule : le quotient de {k * (y - z)} par la différence de {y} et {z}.", Fraction(k), 2, ["La différence est calculée avant le quotient."],
                            [f"{k * (y - z)} ÷ ({y} − {z}).", f"{y} − {z} = {y - z} puis {k * (y - z)} ÷ {y - z} = {k}."]))
    # 11. a shopping problem
    n1, p1, n2, p2 = rng.randint(2, 5), rng.choice([100, 150, 200, 250, 300]), rng.randint(1, 4), rng.choice([50, 75, 100, 125])
    bill = 2000 if n1 * p1 + n2 * p2 < 2000 else 5000
    questions.append(number("a11", "problemes", f"Un élève achète {n1} cahiers à {p1} F et {n2} stylos à {p2} F. Il paie avec {bill} F. Combien lui rend-on, en F ?", Fraction(bill - (n1 * p1 + n2 * p2)), 3,
                            ["Calcule la dépense, puis ce qu'on rend."],
                            [f"Dépense = {n1} × {p1} + {n2} × {p2} = {n1 * p1} + {n2 * p2} = {n1 * p1 + n2 * p2}.", f"{bill} − {n1 * p1 + n2 * p2} = {bill - n1 * p1 - n2 * p2} F."], units=["F"]))
    # 12. the classic order mistake
    p, q, r = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
    wrong_value = (p + q) * r
    right_value = p + q * r
    options = [f"Il a fait l'addition avant la multiplication : {p} + {q} = {p + q} puis {p + q} × {r}", "Il a fait une erreur de table de multiplication", "Il a calculé de droite à gauche"]
    order = [0, 1, 2]
    rng.shuffle(order)
    expression = N(f"{p} + {q} \\times {r} = {wrong_value}")
    questions.append(choice("a12", "priorites", f"Awa a écrit {expression}. D'où vient son erreur ?", [options[i] for i in order], order.index(0), 3,
                            ["Calcule l'expression en respectant la priorité et compare."],
                            [f"La multiplication d'abord : {q} × {r} = {q * r}, puis {p} + {q * r} = {right_value}.", f"Awa a trouvé {wrong_value} = ({p} + {q}) × {r} : elle a fait l'addition en premier."],
                            wrong={order.index(1): "Les produits sont corrects. L'erreur vient de l'ordre des opérations.", order.index(2): "Elle n'a pas calculé de droite à gauche : elle a fait l'addition en premier."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=4, title="Organiser un calcul", language="fr",
    intro="Un calcul comme 3 + 4 × 2 doit donner le même résultat pour tout le monde. Ce chapitre t'apprend les règles qui fixent l'ordre des opérations, le rôle des parenthèses, "
          "et comment écrire en une seule ligne un problème en plusieurs étapes.",
    objectives=["Calculer une suite d'opérations sans parenthèses en respectant les priorités.",
                "Calculer une expression avec des parenthèses, même imbriquées.",
                "Traduire une phrase en une expression, et une expression en phrase, avec le vocabulaire somme, différence, produit, quotient.",
                "Résoudre un problème en plusieurs étapes en l'écrivant en une seule ligne."],
    prerequisites=[{"text": "Avoir terminé les chapitres sur les quatre opérations avec les nombres décimaux.", "chapter": "sn-6e-division"},
                   {"text": "Connaître l'ordre des opérations sur les nombres entiers.", "course": "integers-expressions", "lesson": "order-of-operations"}],
    sections=[S1, S2, S3], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E],
    status_note="Fourth chapter of the Senegal Sixième course. Its topics follow the 'organisation d'un calcul' chapter of the ADEM-Dakar booklet, with our own explanations and exercises. It has not been checked against the official Senegalese programme.",
)
