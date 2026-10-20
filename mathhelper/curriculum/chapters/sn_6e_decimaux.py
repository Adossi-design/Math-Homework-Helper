"""Sixième, Les nombres décimaux arithmétiques: the reference chapter, written in French.

The topics follow the first chapters of the ADEM-Dakar Sixième booklet (decimal numbers, ordering, addition, subtraction), but the order of
sections is our own (ordering comes before addition) and every explanation, example and exercise was written independently. Several
exercise types (rank of a digit, integer part, missing term, arranging digit cards, rounding to estimate a sum, bounding a number) are standard in
any textbook on this topic and also appear in the ADEM booklet, but their wording and numbers here are our own.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
import re
from fractions import Fraction

from ..checker import Answer, parse_number, show
from ..model import Chapter, Exercise, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E

CHAPTER_ID = "sn-6e-decimaux"
D = "$\\mathbb{D}$"
NAT = "$\\mathbb{N}$"


def N(text):
    """Write numbers as math: a decimal comma that LaTeX does not space out, and a/b drawn as a stacked fraction."""
    text = re.sub(r"(\d+)/(\d+)", lambda m: "\\dfrac{" + m.group(1) + "}{" + m.group(2) + "}", text)
    return "$" + text.replace(",", "{,}") + "$"


def d(text):
    """Read a number or fraction written with a decimal comma as an exact fraction."""
    return parse_number(text)


def number(exercise_id, concept, prompt, value, level=1, hints=(), solution=(), units=(), form="", wrong=None):
    """Build an exercise whose answer is one number, given as an exact fraction."""
    return Exercise(f"{CHAPTER_ID}/{exercise_id}", concept, prompt, Answer("number", value, tuple(units), form),
                    list(hints), list(solution), level=level, wrong=wrong or {})


def choice(exercise_id, concept, prompt, options, right, level=1, hints=(), solution=(), wrong=None):
    """Build a multiple choice exercise, the right answer is the index of the option."""
    return Exercise(f"{CHAPTER_ID}/{exercise_id}", concept, prompt, Answer("choice", right), list(hints), list(solution),
                    options=list(options), level=level, wrong=wrong or {})


def ordered(exercise_id, concept, prompt, values, level=1, hints=(), solution=()):
    """Build an exercise whose answer is a list of numbers in a given order."""
    return Exercise(f"{CHAPTER_ID}/{exercise_id}", concept, prompt, Answer("numbers", tuple(values)), list(hints), list(solution), level=level)


def between(exercise_id, concept, prompt, low, high, level=1, hints=(), solution=()):
    """Build an exercise where any number strictly between two values is a correct answer."""
    return Exercise(f"{CHAPTER_ID}/{exercise_id}", concept, prompt, Answer("between", low, high=high, form="decimal"), list(hints), list(solution), level=level)


def join_equal(line):
    """Merge '$a$ = $b$' into one formula '$a = b$', so a calculation reads as one connected line."""
    return re.sub(r"\$ (=|<|>) \$", r" \1 ", line)


def example(title, problem, method, steps, answer, verify, formula=""):
    """Build a worked example: a method, then each line of working with the reason for it."""
    return {"type": "example", "title": title, "problem": problem, "formula": formula, "method": method,
            "steps": [{"math": join_equal(math), "why": why} for math, why in steps], "answer": answer, "verify": verify}


def para(text):
    """A paragraph of explanation."""
    return {"type": "p", "text": text}


def definition(title, text):
    """A definition box."""
    return {"type": "definition", "title": title, "text": text}


def rule(title, text):
    """A property or rule box."""
    return {"type": "property", "title": title, "text": text}


def warning(text):
    """A box about a typical mistake."""
    return {"type": "warning", "text": text}


def column(sign, top, bottom, result=""):
    """Draw an addition or a subtraction in columns, with the commas under each other."""
    bar = " \\\\ \\hline " + result if result else " \\\\ \\hline"
    gap = "\\ " if sign == "+" else "\\ \\ "
    return ("$$\\begin{array}{r} " + top.replace(",", "{,}") + " \\\\ " + sign + gap + bottom.replace(",", "{,}") + bar.replace(",", "{,}") + " \\end{array}$$")


# ----- Section 1: from whole numbers to decimal numbers -----
S1 = Section(
    "ecritures", "Des nombres entiers aux nombres décimaux", 15, "ecritures",
    "Reconnaître une fraction décimale et passer de l'écriture en fraction à l'écriture à virgule, et inversement.",
    [
        para("Une couturière mesure un ruban : il fait 2 m et 35 cm. Combien de mètres cela fait-il ? Ce n'est pas 2 m, car il y a un "
             "morceau en plus. Ce n'est pas 3 m non plus, car il manque 65 cm. La longueur est entre 2 et 3, et aucun nombre entier "
             "ne convient. Pour écrire des nombres entre deux entiers, on utilise les nombres décimaux."),
        para("Rappel sur les fractions : la fraction " + "$\\dfrac{a}{b}$" + " s'obtient en partageant l'unité en " + N("b") + " parts égales et en en prenant " + N("a")
             + ". Si on partage l'unité en 10 parts égales, une part est un dixième, c'est-à-dire " + N("1/10") + ". Avec 100 parts égales, une part est un centième, "
             + N("1/100") + ". Avec 1 000 parts, c'est un millième, " + N("1/1000") + "."),
        definition("Fraction décimale",
                   "Une fraction décimale est une fraction dont le dénominateur est 10, 100, 1 000, 10 000, et ainsi de suite. "
                   "Exemples : " + N("7/10") + " ; " + N("235/100") + " ; " + N("4/1000") + ". Les fractions " + N("5/7") + " et " + N("2/3")
                   + " ne sont pas des fractions décimales."),
        definition("Écriture à virgule",
                   "On convient d'écrire " + N("1/10") + " = " + N("0,1") + ", " + N("1/100") + " = " + N("0,01") + " et " + N("1/1000") + " = " + N("0,001")
                   + ". Un nombre qui s'écrit avec une partie entière, une virgule et des chiffres après la virgule est un nombre à virgule."),
        para("Comme 1 m = 100 cm, on a 35 cm = " + N("35/100") + " m, donc la longueur du ruban est " + N("2 + 35/100") + " m. Or " + N("35/100") + " = "
             + N("30/100 + 5/100") + " = " + N("3/10 + 5/100") + ". Le ruban mesure donc 2 unités, 3 dixièmes et 5 centièmes : on l'écrit " + N("2,35") + " m."),
        definition("Nombre décimal arithmétique",
                   "Un nombre décimal arithmétique est un nombre positif ou nul qui peut s'écrire comme une fraction décimale. Il a donc une écriture à virgule. "
                   "L'ensemble de ces nombres se note " + D + "."),
        para("Un nombre entier naturel est aussi un nombre décimal : " + N("7") + " = " + N("70/10") + " = " + N("7,0") + ". Chaque entier naturel appartient donc à " + D
             + ". Voici les symboles qu'on utilise : « " + "$\\in$" + " » se lit « appartient à », « " + "$\\notin$" + " » se lit « n'appartient pas à », et « "
             + "$\\subset$" + " » se lit « est contenu dans ». On écrit " + "$\\mathbb{N} \\subset \\mathbb{D}$" + " : tous les entiers naturels sont des décimaux. "
             "L'inverse est faux : " + "$2{,}35 \\in \\mathbb{D}$" + " mais " + "$2{,}35 \\notin \\mathbb{N}$" + "."),
        rule("Passer d'une fraction décimale à l'écriture à virgule",
             "Le dénominateur " + N("10") + ", " + N("100") + " ou " + N("1000") + " indique le rang du dernier chiffre : les dixièmes, les centièmes ou les millièmes. "
             "Il y a donc un, deux ou trois chiffres après la virgule. On écrit le numérateur, puis on place la virgule en comptant ce nombre de chiffres depuis la droite. "
             "S'il manque des chiffres, on ajoute des zéros devant."),
        example("Exemple 1", "Écrire " + N("7/10") + ", " + N("235/100") + " et " + N("4/1000") + " avec une virgule.",
                "Le nombre de zéros du dénominateur donne le nombre de chiffres après la virgule.",
                [(N("7/10") + " = " + N("0,7"), "Le dénominateur 10 a un zéro : un chiffre après la virgule. Le numérateur 7 n'a qu'un chiffre, donc la partie entière est 0."),
                 (N("235/100") + " = " + N("2,35"), "Le dénominateur 100 a deux zéros : deux chiffres après la virgule. On compte deux chiffres depuis la droite de 235 : 35. Il reste 2."),
                 (N("4/1000") + " = " + N("0,004"), "Le dénominateur 1 000 a trois zéros : trois chiffres après la virgule. Le numérateur 4 n'a qu'un chiffre, on ajoute deux zéros devant : 004.")],
                N("0,7") + " ; " + N("2,35") + " ; " + N("0,004"),
                "d('7/10')==d('0,7') and d('235/100')==d('2,35') and d('4/1000')==d('0,004')"),
        example("Exemple 2", "Écrire " + N("6,25") + ", " + N("12,5") + " et " + N("0,07") + " sous la forme d'une fraction décimale.",
                "On lit le nombre de chiffres après la virgule, on supprime la virgule, et on met 1 suivi d'autant de zéros au dénominateur.",
                [(N("6,25") + " = " + N("625/100"), "Il y a deux chiffres après la virgule : le dénominateur est 100. Sans la virgule, le numérateur est 625."),
                 (N("12,5") + " = " + N("125/10"), "Il y a un chiffre après la virgule : le dénominateur est 10. Le numérateur est 125."),
                 (N("0,07") + " = " + N("7/100"), "Il y a deux chiffres après la virgule : le dénominateur est 100. Sans la virgule on obtient 007, soit 7.")],
                N("625/100") + " ; " + N("125/10") + " ; " + N("7/100"),
                "d('6,25')==d('625/100') and d('12,5')==d('125/10') and d('0,07')==d('7/100')"),
        example("Exemple 3", "Montrer que " + N("235/100") + " s'écrit " + N("2,35") + ", sans appliquer la règle des zéros.",
                "On découpe le numérateur selon les rangs : centaines de centièmes, dizaines de centièmes, centièmes.",
                [(N("235/100") + " = " + N("200/100 + 30/100 + 5/100"), "On décompose 235 en 200 + 30 + 5."),
                 ("$= 2 + \\dfrac{3}{10} + \\dfrac{5}{100}$", "200/100 = 2, et 30/100 = 3/10 car on peut diviser le numérateur et le dénominateur par 10."),
                 ("$= 2 + 0{,}3 + 0{,}05$", "3/10 s'écrit 0,3 et 5/100 s'écrit 0,05."),
                 ("$= 2{,}35$", "2 unités, 3 dixièmes et 5 centièmes : c'est l'écriture 2,35. La règle des zéros n'est que ce calcul fait plus vite.")],
                N("2,35"), "d('235/100')==d('2')+d('3/10')+d('5/100')"),
        example("Exemple 4", "Écrire " + N("3/5") + " avec une virgule.",
                "Le dénominateur 5 n'est pas 10, 100 ou 1 000. On cherche une fraction égale dont le dénominateur est 10.",
                [(N("3/5") + " = " + "$\\dfrac{3 \\times 2}{5 \\times 2}$", "On multiplie le numérateur et le dénominateur par le même nombre, ici 2, pour ne pas changer la valeur. Le but est d'obtenir 10 au dénominateur."),
                 ("$= \\dfrac{6}{10}$", "On calcule : 3 × 2 = 6 et 5 × 2 = 10."),
                 ("$= 0{,}6$", "Le dénominateur 10 donne un chiffre après la virgule.")],
                N("0,6"), "d('3/5')==d('0,6')", "Fractions égales : on ne change pas une fraction en multipliant son numérateur et son dénominateur par le même nombre."),
        para("Toutes les fractions ne s'écrivent pas avec une virgule qui s'arrête. La fraction " + N("1/3") + " n'est égale à aucune fraction décimale : on ne peut pas "
             "l'écrire avec un nombre fini de chiffres après la virgule, donc " + N("1/3") + " n'est pas un nombre décimal. C'est pour cela que le mot « décimal » a un sens précis."),
        warning("Les zéros à la fin de la partie décimale ne changent pas la valeur : " + N("3,50") + " = " + N("3,5") + " et " + N("9,0")
                + " = " + N("9") + ". Les zéros placés juste après la virgule, eux, changent tout : " + N("0,05") + " est dix fois plus petit que " + N("0,5") + "."),
    ],
    [
        number("s1-g1", "ecritures", "Écris " + N("47/100") + " avec une virgule.", d("0,47"), form="decimal",
               hints=["Combien de zéros y a-t-il au dénominateur ? Cela donne le nombre de chiffres après la virgule.",
                      "Place la virgule pour qu'il y ait autant de chiffres après elle que de zéros au dénominateur."],
               solution=["Le dénominateur 100 a deux zéros, donc deux chiffres après la virgule.", "47/100 = 0,47."]),
        number("s1-g2", "ecritures", "Écris " + N("3,125") + " sous la forme d'une fraction décimale (numérateur entier, dénominateur 10, 100, 1000...).",
               d("3,125"), form="decimal_fraction",
               hints=["Combien de chiffres y a-t-il après la virgule ?", "Le dénominateur dépend de ce nombre de chiffres. Le numérateur est le nombre sans la virgule."],
               solution=["Il y a trois chiffres après la virgule : le dénominateur est 1 000.", "Sans la virgule on lit 3125 : 3,125 = 3125/1000."]),
        choice("s1-g3", "ecritures", "Un seul de ces nombres est un entier naturel. Lequel ?", [N("8,5"), N("0,8"), N("8,0"), N("0,08")], 2,
               hints=["Un entier naturel est un nombre sans partie décimale non nulle. Un zéro placé à la fin de la partie décimale change-t-il la valeur d'un nombre ?"],
               solution=["8,0 = 8 : un zéro à la fin de la partie décimale ne change pas la valeur, donc 8,0 est l'entier naturel 8.", "8,5 ; 0,8 et 0,08 ont des chiffres non nuls après la virgule."],
               wrong={1: "0,8 est plus petit que 1 : ce n'est pas un entier naturel. Cherche le nombre dont les chiffres après la virgule sont tous nuls."}),
        number("s1-g4", "ecritures", "Parmi " + N("3/10") + " ; " + N("5/7") + " ; " + N("12/100") + " ; " + N("2/3") + ", combien sont des fractions décimales ?", Fraction(2),
               hints=["Regarde seulement les dénominateurs. Lesquels sont 10, 100, 1 000... ?"],
               solution=["3/10 a pour dénominateur 10 et 12/100 a pour dénominateur 100 : ce sont des fractions décimales.", "5/7 et 2/3 ont pour dénominateurs 7 et 3 : ce ne sont pas des fractions décimales.", "Il y en a 2."]),
    ])

# ----- Section 2: integer part, decimal part and rank of digits -----
S2 = Section(
    "rang", "Partie entière, partie décimale et rang des chiffres", 18, "rang",
    "Lire un nombre décimal chiffre par chiffre : donner le rang et la valeur de chaque chiffre, et passer d'un rang à l'autre.",
    [
        para("Dans un nombre entier, chaque chiffre a une valeur qui dépend de sa place : dans 372, le 3 vaut 300. Pour les nombres décimaux, "
             "on garde la même idée et on la prolonge à droite de la virgule. Le tableau suivant place le nombre " + N("137,405") + "."),
        {"type": "table", "head": ["centaines", "dizaines", "unités", ",", "dixièmes", "centièmes", "millièmes"],
         "rows": [["1", "3", "7", ",", "4", "0", "5"]]},
        definition("Partie entière et partie décimale",
                   "La partie entière d'un nombre décimal est le nombre écrit à gauche de la virgule. La partie décimale est la suite des chiffres écrits à droite de la virgule ; "
                   "elle représente un nombre plus petit que 1. Dans " + N("137,405") + " la partie entière est " + N("137") + ". La partie décimale est composée des chiffres 4, 0 et 5 ; "
                   "elle représente le nombre " + N("0,405") + ". Un nombre entier n'a aucun chiffre après la virgule : sa partie décimale est " + N("0") + "."),
        rule("Le rang d'un chiffre",
             "À droite de la virgule, les rangs sont les dixièmes, les centièmes, les millièmes. Un dixième vaut " + N("1/10") + " = " + N("0,1")
             + ", un centième vaut " + N("1/100") + " = " + N("0,01") + ", un millième vaut " + N("1/1000") + " = " + N("0,001")
             + ". Chaque rang vaut dix fois le rang qui est à sa droite."),
        rule("La valeur d'un chiffre",
             "La valeur d'un chiffre est le chiffre multiplié par la valeur de son rang. Dans " + N("137,405") + ", le chiffre 4 est au rang des dixièmes, "
             "sa valeur est " + N("4 \\times 0,1") + " = " + N("0,4") + ". Le chiffre 5 est au rang des millièmes, sa valeur est " + N("5 \\times 0,001") + " = " + N("0,005") + "."),
        rule("Passer d'un rang à l'autre",
             "Comme chaque rang vaut dix fois le suivant : 1 unité = 10 dixièmes = 100 centièmes = 1 000 millièmes, et 1 dixième = 10 centièmes = 100 millièmes, "
             "et 1 centième = 10 millièmes. On peut donc compter un nombre dans un seul rang : " + N("2,35") + " = 2 unités + 3 dixièmes + 5 centièmes = 200 centièmes + 30 centièmes + 5 centièmes = 235 centièmes."),
        example("Exemple 1", "Dans " + N("24,76") + ", donner le rang et la valeur du chiffre 7, puis du chiffre 6.",
                "On repère la place de chaque chiffre par rapport à la virgule, puis on multiplie par la valeur du rang.",
                [("Chiffre 7 : rang des dixièmes", "Il est juste après la virgule."),
                 (N("7 \\times 0,1") + " = " + N("0,7"), "Valeur du chiffre 7 : on multiplie 7 par un dixième."),
                 ("Chiffre 6 : rang des centièmes", "Il est à la deuxième place après la virgule."),
                 (N("6 \\times 0,01") + " = " + N("0,06"), "Valeur du chiffre 6 : on multiplie 6 par un centième.")],
                "7 vaut " + N("0,7") + " ; 6 vaut " + N("0,06"), "d('7')*d('0,1')==d('0,7') and d('6')*d('0,01')==d('0,06')"),
        example("Exemple 2", "Donner la partie entière et la partie décimale de " + N("508,04") + ".",
                "On sépare le nombre à la virgule. Les zéros comptent : ils occupent un rang.",
                [("Partie entière : " + N("508"), "C'est tout ce qui est à gauche de la virgule."),
                 ("Partie décimale : les chiffres 0 et 4, qui représentent " + N("0,04"), "À droite de la virgule on lit 0 puis 4 : 0 au rang des dixièmes, 4 au rang des centièmes."),
                 (N("508,04") + " = " + N("508 + 0,04"), "On vérifie : partie entière plus partie décimale redonne le nombre.")],
                "partie entière " + N("508") + ", partie décimale " + N("0,04"), "d('508')+d('0,04')==d('508,04')"),
        example("Exemple 3", "Décomposer " + N("35,206") + " en additionnant la valeur de chaque chiffre.",
                "On écrit chaque chiffre multiplié par la valeur de son rang. Les chiffres 0 valent 0 mais il faut quand même les écrire pour garder la place des autres.",
                [(N("35,206") + " = " + N("3 \\times 10 + 5 \\times 1 + 2 \\times 0,1 + 0 \\times 0,01 + 6 \\times 0,001"), "3 est au rang des dizaines, 5 des unités, 2 des dixièmes, 0 des centièmes, 6 des millièmes."),
                 ("$= 30 + 5 + 0{,}2 + 0 + 0{,}006$", "On calcule chaque produit."),
                 ("$= 35{,}206$", "On additionne : la somme redonne le nombre de départ, ce qui confirme la décomposition.")],
                N("35,206") + " = " + N("30 + 5 + 0,2 + 0,006"), "d('30')+d('5')+d('0,2')+d('0,006')==d('35,206')"),
        example("Exemple 4", "Combien y a-t-il de centièmes dans " + N("2,35") + " ? Et combien de dixièmes dans " + N("4,7") + " ?",
                "On convertit tout dans le rang demandé, avec 1 unité = 10 dixièmes = 100 centièmes et 1 dixième = 10 centièmes.",
                [("2 unités = 200 centièmes", "Une unité vaut 100 centièmes, donc 2 unités valent 2 × 100 = 200 centièmes."),
                 ("3 dixièmes = 30 centièmes", "Un dixième vaut 10 centièmes, donc 3 dixièmes valent 30 centièmes."),
                 ("200 + 30 + 5 = 235", "On additionne les centièmes de chaque rang : 2,35 contient 235 centièmes."),
                 ("4 unités = 40 dixièmes, et 40 + 7 = 47", "De même 4,7 contient 47 dixièmes.")],
                N("2,35") + " = 235 centièmes ; " + N("4,7") + " = 47 dixièmes", "d('2,35')==d('235/100') and d('4,7')==d('47/10')"),
        example("Exemple 5", "Avec les cartes 3, 8 et 6, chacune utilisée une seule fois, on forme un nombre de la forme " + N("A,BC") + ". Quel est le plus petit nombre possible ?",
                "Le rang qui compte le plus est celui qui est le plus à gauche : on y met le plus petit chiffre, puis on continue vers la droite.",
                [("Unités : 3", "Le plus petit chiffre à gauche donne le plus petit nombre : 3 unités est plus petit que 6 ou 8 unités."),
                 ("Dixièmes : 6", "Parmi 6 et 8, le plus petit va au rang suivant, celui des dixièmes."),
                 ("Centièmes : 8", "Il reste 8 pour les centièmes."),
                 (N("3,68"), "On assemble. Le rang des unités compte le plus, puis les dixièmes, puis les centièmes.")],
                N("3,68"), "d('3,68')<d('3,86') and d('3,68')<d('6,38') and d('3,68')<d('8,36') and d('3,68')<d('6,83') and d('3,68')<d('8,63')"),
        warning("Ne confonds pas dizaine et dixième. La dizaine est un rang à gauche de la virgule (10 unités), le dixième est un rang à droite (une unité partagée en 10 parts)."),
    ],
    [
        number("s2-g1", "rang", "Quel est le chiffre des centièmes dans " + N("48,371") + " ?", Fraction(7),
               hints=["Repère la virgule. Les chiffres à sa droite sont dans l'ordre : dixièmes, centièmes, millièmes.", "Écris les trois chiffres après la virgule, puis choisis celui du deuxième rang."],
               solution=["Les chiffres après la virgule sont 3 (dixièmes), 7 (centièmes), 1 (millièmes).", "Le chiffre des centièmes est 7."],
               wrong={"3": "3 est le chiffre des dixièmes. Les centièmes sont la deuxième place après la virgule."}),
        number("s2-g2", "rang", "Quelle est la valeur du chiffre 6 dans " + N("12,064") + " ?", d("0,06"),
               hints=["Dans quel rang se trouve le 6 ? Compte les places après la virgule.", "Une fois le rang trouvé, multiplie 6 par la valeur d'une unité de ce rang."],
               solution=["Après la virgule on lit 0 (dixièmes), 6 (centièmes), 4 (millièmes).", "La valeur du 6 est 6 × 0,01 = 0,06."],
               wrong={"6": "6 est le chiffre, pas sa valeur. Le 6 est au rang des centièmes : sa valeur est 6 × 0,01.",
                      "0,6": "0,6 serait la valeur de 6 au rang des dixièmes. Ici il y a un 0 entre la virgule et le 6."}),
        number("s2-g3", "rang", "Complète la décomposition : " + N("9,057 = 9 + 0,05 + ?"), d("0,007"),
               hints=["Quels chiffres de 9,057 ont déjà été écrits dans la somme ? Lequel n'y est pas encore ?", "Trouve le rang de ce dernier chiffre, puis sa valeur."],
               solution=["9 est la partie entière, 0,05 est la valeur du chiffre 5 (centièmes).", "Il manque le chiffre 7 au rang des millièmes : 7 × 0,001 = 0,007."]),
        choice("s2-g4", "rang", "Dans " + N("57,26") + ", le chiffre 2 est au rang des :", ["dizaines", "dixièmes", "centièmes"], 1,
               hints=["Le 2 est-il à gauche ou à droite de la virgule ?"],
               solution=["Le 2 est juste après la virgule : c'est le rang des dixièmes.", "Les dizaines sont à gauche de la virgule : dans 57,26, le chiffre des dizaines est 5."],
               wrong={0: "Les dizaines sont à gauche de la virgule. Ici le 2 est à droite de la virgule : ne confonds pas dizaine et dixième."}),
        number("s2-g5", "rang", "Écris la partie décimale de " + N("52,708") + " sous la forme d'un nombre plus petit que 1.", d("0,708"),
               hints=["La partie décimale, ce sont les chiffres à droite de la virgule. Quel nombre représentent-ils ?"],
               solution=["Les chiffres à droite de la virgule sont 7, 0 et 8.", "Ils représentent le nombre 0,708."]),
    ])

# ----- Section 3: compare and order -----
S3 = Section(
    "comparer", "Comparer, ranger, encadrer et intercaler", 20, "comparer",
    "Comparer deux nombres décimaux, les ranger dans l'ordre, encadrer un nombre et intercaler un nombre entre deux autres.",
    [
        para("Quel nombre est le plus grand : " + N("2,5") + " ou " + N("2,35") + " ? Beaucoup d'élèves répondent " + N("2,35") + " parce que 35 est plus grand que 5. "
             "C'est une erreur, et il est important de comprendre pourquoi. " + N("2,5") + " veut dire 2 unités et 5 dixièmes. " + N("2,35")
             + " veut dire 2 unités, 3 dixièmes et 5 centièmes. Il y a plus de dixièmes dans le premier."),
        rule("Comparer deux nombres décimaux",
             "On compare d'abord les parties entières. Si elles sont différentes, le plus grand nombre est celui qui a la plus grande partie entière. "
             "Si elles sont égales, on compare les chiffres des dixièmes, puis ceux des centièmes, et ainsi de suite, jusqu'à trouver deux chiffres différents."),
        rule("La méthode des zéros",
             "Quand les parties entières sont égales, on peut ajouter des zéros à la fin de la partie décimale pour que les deux nombres aient autant de chiffres après la virgule. "
             "Cela ne change pas leur valeur, car 1 dixième = 10 centièmes : " + N("2,5") + " = " + N("2,50") + ". On compare alors les parties décimales comme deux nombres entiers : 50 centièmes sont plus que 35 centièmes."),
        definition("Ranger",
                   "Ranger des nombres dans l'ordre croissant, c'est les écrire du plus petit au plus grand avec le signe <. Dans l'ordre décroissant, "
                   "on les écrit du plus grand au plus petit avec le signe >."),
        example("Exemple 1", "Comparer " + N("7,48") + " et " + N("7,5") + ".",
                "Méthode des zéros : on donne le même nombre de chiffres après la virgule aux deux nombres.",
                [("Les parties entières sont égales : 7 et 7.", "On ne peut pas conclure avec les parties entières, il faut regarder après la virgule."),
                 (N("7,5") + " = " + N("7,50"), "On ajoute un zéro à 7,5 pour avoir deux chiffres après la virgule, comme 7,48."),
                 ("Parties décimales : 48 et 50", "Comparées comme des entiers, 48 est plus petit que 50."),
                 (N("7,48 < 7,5"), "Donc 7,48 est plus petit que 7,5.")],
                N("7,48 < 7,5"), "d('7,48')<d('7,5')"),
        example("Exemple 2", "Ranger dans l'ordre croissant : " + N("3,05") + " ; " + N("3,5") + " ; " + N("3,45") + " ; " + N("0,999") + ".",
                "On compare les parties entières, puis on utilise la méthode des zéros pour les nombres qui ont la même partie entière.",
                [(N("0,999") + " a pour partie entière 0", "Les trois autres ont pour partie entière 3. Donc 0,999 est le plus petit."),
                 (N("3,05") + " = " + N("3,050") + " ; " + N("3,5") + " = " + N("3,500") + " ; " + N("3,45") + " = " + N("3,450"), "Ces trois nombres ont la même partie entière : on leur donne trois chiffres après la virgule."),
                 ("Parties décimales : 050 ; 500 ; 450", "En ordre croissant : 050 < 450 < 500."),
                 (N("0,999 < 3,05 < 3,45 < 3,5"), "On remet les nombres dans le bon ordre, avec leur écriture de départ.")],
                N("0,999 < 3,05 < 3,45 < 3,5"), "d('0,999')<d('3,05')<d('3,45')<d('3,5')"),
        para("Entre deux nombres décimaux différents, on peut toujours en intercaler un autre. Entre 4,6 et 4,7 il y a 4,65. Mais entre 4,6 et 4,65 il y a encore 4,62, et entre 4,6 et 4,62 il y a 4,61, "
             "et ainsi de suite sans jamais s'arrêter : il y a une infinité de nombres décimaux entre deux décimaux différents. Ce n'est pas le cas pour les entiers : entre 4 et 5, il n'y a aucun entier."),
        example("Exemple 3", "Intercaler un nombre décimal entre " + N("4,6") + " et " + N("4,7") + ".",
                "Intercaler un nombre, c'est trouver un nombre plus grand que le premier et plus petit que le second. Entre 4,6 et 4,7 il n'y a pas de nombre à un seul chiffre après la virgule, alors on utilise les centièmes.",
                [(N("4,6") + " = " + N("4,60") + " et " + N("4,7") + " = " + N("4,70"), "On écrit les deux nombres avec deux chiffres après la virgule."),
                 ("Parties décimales : 60 et 70", "On cherche un entier entre 60 et 70, par exemple 65."),
                 (N("4,60 < 4,65 < 4,70"), "Le nombre 4,65 est entre 4,6 et 4,7.")],
                N("4,65") + " (ou " + N("4,61") + ", " + N("4,66") + ", etc.)", "d('4,6')<d('4,65')<d('4,7')"),
        definition("Encadrer",
                   "Encadrer un nombre, c'est trouver un nombre plus petit et un nombre plus grand, les plus proches possibles, qui l'entourent. "
                   "Encadrer à l'unité près, c'est choisir deux entiers consécutifs (qui se suivent). Encadrer au dixième près, c'est choisir deux nombres à un chiffre après la virgule qui se suivent, "
                   "par exemple 13,7 et 13,8."),
        example("Exemple 4", "Encadrer " + N("27,318") + " à l'unité près, puis au dixième près.",
                "On garde la partie entière, puis les chiffres jusqu'au rang demandé ; le nombre plus grand s'obtient en ajoutant une unité de ce rang.",
                [("Partie entière : 27", "Le nombre est supérieur à 27 car il a une partie décimale non nulle, et inférieur à 28."),
                 (N("27 < 27,318 < 28"), "Encadrement à l'unité près : 27 et 28 sont deux entiers consécutifs."),
                 ("Chiffre des dixièmes : 3", "On garde 27,3 comme nombre plus petit. Le suivant à un chiffre après la virgule est 27,4."),
                 (N("27,3 < 27,318 < 27,4"), "Encadrement au dixième près : 27,300 < 27,318 < 27,400 avec trois chiffres.")],
                N("27 < 27,318 < 28") + " et " + N("27,3 < 27,318 < 27,4"), "d('27')<d('27,318')<d('28') and d('27,3')<d('27,318')<d('27,4')"),
        warning("Avoir plus de chiffres ne veut pas dire être plus grand. " + N("5,099") + " est plus petit que " + N("5,1") + " : en ajoutant des zéros, 5,099 contre 5,100. "
                "Et la méthode des zéros ne s'applique qu'entre nombres de même partie entière : on ne compare pas les parties décimales de 0,999 et de 3,05."),
    ],
    [
        choice("s3-g1", "comparer", "Quel est le plus grand de ces trois nombres ?", [N("5,09"), N("5,9"), N("5,099")], 1,
               hints=["Les parties entières sont toutes égales à 5. Donne le même nombre de chiffres après la virgule aux trois nombres.", "Compare ensuite les parties décimales comme des nombres entiers."],
               solution=["5,09 = 5,090 ; 5,9 = 5,900 ; 5,099.", "Les parties décimales sont 090, 900 et 099 : la plus grande est 900.", "Le plus grand nombre est 5,9."],
               wrong={2: "5,099 a plus de chiffres, mais ce n'est pas ce qui compte. Compare 5,099 avec 5,900."}),
        ordered("s3-g2", "comparer", "Range dans l'ordre croissant, en séparant par des points-virgules : " + N("6,2") + " ; " + N("6,02") + " ; " + N("6,25") + " ; " + N("5,98") + ".",
                [d("5,98"), d("6,02"), d("6,2"), d("6,25")],
                hints=["Commence par les parties entières : lequel est le plus petit ?", "Pour les autres, qui ont la même partie entière, donne-leur le même nombre de chiffres après la virgule."],
                solution=["5,98 a pour partie entière 5, c'est le plus petit.", "6,2 = 6,20. Les parties décimales sont 20, 02 et 25 : 02 < 20 < 25.", "5,98 < 6,02 < 6,2 < 6,25."]),
        between("s3-g3", "comparer", "Écris un nombre décimal compris entre " + N("1,3") + " et " + N("1,4") + ".", d("1,3"), d("1,4"),
                hints=["Il n'y a pas de nombre à un seul chiffre après la virgule entre 1,3 et 1,4. Combien de chiffres faut-il ?", "Écris 1,3 et 1,4 avec ce nombre de chiffres après la virgule, puis choisis un nombre entre les deux."],
                solution=["1,3 = 1,30 et 1,4 = 1,40.", "Tout nombre de 1,31 à 1,39 convient, par exemple 1,35."]),
        number("s3-g4", "comparer", "Encadre " + N("8,64") + " à l'unité près. Quel est le plus petit des deux entiers ?", Fraction(8),
               hints=["Quelle est la partie entière de 8,64 ? Le nombre est-il plus grand ou plus petit qu'elle ?"],
               solution=["8,64 a pour partie entière 8, et il est plus petit que 9.", "L'encadrement est 8 < 8,64 < 9. Le plus petit des deux entiers est 8."]),
    ])

# ----- Section 4: addition -----
S4 = Section(
    "addition", "Additionner des nombres décimaux", 22, "addition",
    "Additionner en colonnes, utiliser les propriétés de l'addition pour calculer efficacement, et donner un ordre de grandeur.",
    [
        para("Additionner des nombres décimaux revient à additionner des unités avec des unités, des dixièmes avec des dixièmes, des centièmes avec des centièmes. "
             "C'est pour cela qu'on aligne les chiffres de même rang les uns sous les autres, donc les virgules sont alignées."),
        rule("Poser une addition",
             "On écrit les nombres l'un sous l'autre en alignant les virgules. On complète par des zéros pour que chaque nombre ait autant de chiffres après la virgule. "
             "On additionne en partant de la droite, en retenant quand une colonne dépasse 9, parce que 10 d'un rang font 1 du rang à gauche. On place la virgule du résultat sous les autres virgules."),
        rule("Propriétés de l'addition",
             "Commutativité : on peut changer l'ordre de deux termes, " + N("a + b = b + a") + ". Associativité : on peut regrouper les termes comme on veut, "
             + N("(a + b) + c = a + (b + c)") + ". Élément neutre : ajouter 0 ne change rien, " + N("a + 0 = a") + ", par exemple " + N("6,25 + 0 = 6,25") + "."),
        example("Exemple 1", "Vérifier avec " + N("a = 2,5") + " et " + N("b = 3,75") + " que l'on peut changer l'ordre des termes.",
                "On calcule les deux sommes et on compare. Un exemple ne prouve pas la propriété, mais il montre comment on l'utilise.",
                [(N("2,5 + 3,75") + " = " + N("2,50 + 3,75") + " = " + N("6,25"), "On complète 2,5 par un zéro, puis on additionne : 50 + 75 = 125 centièmes, soit 1 unité et 25 centièmes."),
                 (N("3,75 + 2,5") + " = " + N("3,75 + 2,50") + " = " + N("6,25"), "On change l'ordre : on trouve le même résultat."),
                 (N("2,5 + 3,75") + " = " + N("3,75 + 2,5"), "C'est la commutativité de l'addition.")],
                N("6,25"), "d('2,5')+d('3,75')==d('3,75')+d('2,5')==d('6,25')"),
        example("Exemple 2", "Calculer " + N("36,45 + 12,8") + ".",
                "Addition posée en colonnes avec les virgules alignées.",
                [(column("+", "36,45", "12,80"), "On écrit 12,8 sous la forme 12,80 pour que les deux nombres aient deux chiffres après la virgule et que les virgules soient l'une sous l'autre."),
                 ("Centièmes : 5 + 0 = 5. Dixièmes : 4 + 8 = 12.", "12 dixièmes, c'est 1 unité et 2 dixièmes : on écrit 2 et on retient 1."),
                 ("Unités : 6 + 2 + 1 (retenue) = 9. Dizaines : 3 + 1 = 4.", "On additionne les unités avec la retenue, puis les dizaines."),
                 (column("+", "36,45", "12,80", "49,25"), "On place la virgule du résultat sous les autres virgules : 36,45 + 12,8 = 49,25. Un calcul rapide le confirme : 36 + 13 = 49.")],
                N("49,25"), "d('36,45')+d('12,8')==d('49,25')"),
        example("Exemple 3", "Calculer efficacement " + N("4,6 + 3,7 + 5,4 + 6,3") + ".",
                "On cherche des termes dont la somme est un nombre entier, puis on les regroupe grâce aux propriétés de l'addition.",
                [(N("4,6 + 3,7 + 5,4 + 6,3") + " = " + N("4,6 + 5,4 + 3,7 + 6,3"), "Commutativité : on change l'ordre des termes pour rapprocher 4,6 et 5,4, puis 3,7 et 6,3."),
                 ("$= (4{,}6 + 5{,}4) + (3{,}7 + 6{,}3)$", "Associativité : on groupe les termes par deux."),
                 ("$= 10 + 10$", "4,6 + 5,4 = 10 car 6 + 4 = 10 dixièmes, soit 1 unité en plus. De même 3,7 + 6,3 = 10."),
                 ("$= 20$", "On additionne les deux dizaines.")],
                N("20"), "d('4,6')+d('3,7')+d('5,4')+d('6,3')==d('20')"),
        rule("Arrondir à la dizaine la plus proche",
             "On regarde le chiffre des unités. S'il est 0, 1, 2, 3 ou 4, on garde la dizaine et on remplace les unités par 0. S'il est 5, 6, 7, 8 ou 9, on passe à la dizaine suivante. "
             "Exemples : " + N("48,7") + " devient 50 ; " + N("31,2") + " devient 30 ; " + N("45") + " devient 50."),
        para("Un ordre de grandeur est un résultat approché, qu'on trouve de tête en arrondissant les nombres. Il sert à vérifier qu'un résultat exact est plausible : si l'ordre de grandeur est 100 et si on trouve 1 005, il y a une erreur."),
        example("Exemple 4", "Estimer " + N("48,7 + 19,6 + 31,2") + " en arrondissant chaque nombre à la dizaine la plus proche, puis calculer la somme exacte.",
                "On arrondit chaque terme avec la règle des unités, on additionne les nombres arrondis, puis on compare avec le résultat exact.",
                [("48,7 devient 50 ; 19,6 devient 20 ; 31,2 devient 30", "Chiffres des unités : 8 (on passe à la dizaine suivante), 9 (idem), 1 (on garde la dizaine)."),
                 (N("50 + 20 + 30") + " = " + N("100"), "La somme des nombres arrondis est l'ordre de grandeur."),
                 (N("48,7 + 19,6 + 31,2") + " = " + N("99,5"), "Le calcul exact donne 99,5 (48,7 + 19,6 = 68,3 puis 68,3 + 31,2 = 99,5)."),
                 ("99,5 est proche de 100", "Le résultat exact est cohérent avec l'ordre de grandeur.")],
                "ordre de grandeur " + N("100") + ", somme exacte " + N("99,5"), "d('48,7')+d('19,6')+d('31,2')==d('99,5')"),
        example("Exemple 5", "Awa achète 2,5 kg de sucre, 0,75 kg de sel et 4 kg de farine. Quelle est la masse totale de ses achats ?",
                "Une masse totale se trouve par une addition. On vérifie en refaisant le calcul dans un autre ordre.",
                [("Masse totale = " + N("2,5 + 0,75 + 4"), "On additionne les trois masses."),
                 ("$2{,}50 + 0{,}75 = 3{,}25$", "On écrit 2,5 sous la forme 2,50 : 250 + 75 = 325 centièmes, soit 3,25."),
                 ("$3{,}25 + 4 = 7{,}25$", "On ajoute 4 unités."),
                 ("Vérification : $4 + 2{,}5 = 6{,}5$ puis $6{,}5 + 0{,}75 = 7{,}25$", "On change l'ordre des termes (commutativité) : on trouve le même résultat.")],
                "La masse totale est " + N("7,25") + " kg.", "d('2,5')+d('0,75')+d('4')==d('7,25') and d('4')+d('2,5')+d('0,75')==d('7,25')"),
        warning("N'oublie pas de compléter par des zéros et d'aligner les virgules. Si tu alignes les nombres à droite sans regarder les virgules, tu additionnes des dixièmes avec des centièmes, et le résultat est faux."),
    ],
    [
        number("s4-g1", "addition", "Calcule " + N("17,6 + 4,85") + ".", d("22,45"),
               hints=["Complète 17,6 avec un zéro pour avoir deux chiffres après la virgule.", "Pose l'addition avec les virgules alignées et commence par les centièmes."],
               solution=["17,6 = 17,60.", "Centièmes : 0 + 5 = 5. Dixièmes : 6 + 8 = 14, on écrit 4 et on retient 1.", "Unités : 7 + 4 + 1 = 12, on écrit 2 et on retient 1. Dizaines : 1 + 1 = 2.", "17,6 + 4,85 = 22,45."]),
        number("s4-g2", "addition", "Calcule en regroupant : " + N("2,8 + 6,5 + 3,2 + 1,5") + ".", Fraction(14),
               hints=["Cherche deux nombres dont la somme est un entier.", "Pour chaque nombre, regarde le chiffre des dixièmes : quel autre nombre le complète à 10 dixièmes ?"],
               solution=["(2,8 + 3,2) + (6,5 + 1,5) : on a changé l'ordre (commutativité) et regroupé (associativité).", "2,8 + 3,2 = 6 et 6,5 + 1,5 = 8.", "6 + 8 = 14."]),
        number("s4-g3", "addition", "Estime " + N("38,4 + 51,7 + 9,2") + " en arrondissant chaque nombre à la dizaine la plus proche.", Fraction(100),
               hints=["Pour arrondir à la dizaine la plus proche, regarde le chiffre des unités de chaque nombre.", "Arrondis les trois nombres, puis additionne les résultats."],
               solution=["38,4 : le chiffre des unités est 8, on passe à 40. 51,7 : le chiffre des unités est 1, on garde 50. 9,2 : le chiffre des unités est 9, on passe à 10.", "40 + 50 + 10 = 100."]),
        choice("s4-g4", "addition", "Pour calculer " + N("1,2 + 4,5 + 3,8") + ", on écrit " + N("(1,2 + 3,8) + 4,5") + ". Quelles propriétés a-t-on utilisées ?",
               ["La commutativité seulement", "L'associativité seulement", "La commutativité, puis l'associativité"], 2,
               hints=["Compare l'ordre des termes avant et après : a-t-il changé ? Les termes sont-ils ensuite regroupés ?"],
               solution=["Dans la somme de départ, 4,5 est avant 3,8. Dans (1,2 + 3,8) + 4,5, il est après : on a changé l'ordre des termes (commutativité).", "Ensuite on regroupe 1,2 et 3,8 entre parenthèses : c'est l'associativité."],
               wrong={0: "Changer l'ordre ne suffit pas : on a aussi mis des parenthèses autour de 1,2 + 3,8, donc regroupé des termes.",
                      1: "Regrouper ne suffit pas : pour avoir 1,2 à côté de 3,8, il a d'abord fallu changer l'ordre des termes."}),
    ])

# ----- Section 5: subtraction -----
S5 = Section(
    "soustraction", "Soustraire des nombres décimaux", 22, "soustraction",
    "Soustraire en colonnes, vérifier une soustraction par une addition et résoudre des problèmes.",
    [
        para("Soustraire, c'est enlever une quantité ou chercher la différence entre deux quantités. Comme pour l'addition, on soustrait les unités des unités, "
             "les dixièmes des dixièmes, les centièmes des centièmes, donc on aligne les virgules."),
        rule("Poser une soustraction",
             "On écrit le plus grand nombre en haut, le plus petit en dessous, avec les virgules alignées, et on complète par des zéros jusqu'au même nombre de chiffres après la virgule. "
             "On soustrait en partant de la droite. Si le chiffre du haut est plus petit que celui du bas, on « emprunte » une unité du rang de gauche, qui vaut 10 unités du rang courant."),
        rule("Vérifier une soustraction",
             "Une soustraction et une addition vont ensemble : si " + N("a - b = c") + ", alors " + N("c + b = a") + ". On vérifie donc son résultat en l'additionnant au nombre enlevé : on doit retrouver le premier nombre."),
        rule("Enlever deux quantités de suite",
             "Enlever " + N("b") + " puis " + N("c") + " à " + N("a") + ", c'est enlever leur somme : " + N("a - b - c = a - (b + c)") + "."),
        para("Pour l'instant, on soustrait toujours le plus petit nombre du plus grand. Par exemple " + N("9 - 4 = 5") + ", mais " + N("4 - 9")
             + " n'est pas possible dans ce chapitre : les nombres négatifs viendront plus tard. On ne peut donc pas échanger les deux nombres d'une soustraction, contrairement à ceux d'une addition."),
        example("Exemple 1", "Calculer " + N("12,5 - 4,75") + " et vérifier.",
                "Soustraction posée en colonnes. Le chiffre du haut est plus petit que celui du bas dans plusieurs colonnes, on emprunte.",
                [("12,5 = 12,50", "On complète avec un zéro pour avoir deux chiffres après la virgule."),
                 ("Centièmes : 0 − 5 impossible. On emprunte 1 dixième = 10 centièmes : 10 − 5 = 5.", "Le chiffre des dixièmes passe de 5 à 4."),
                 ("Dixièmes : 4 − 7 impossible. On emprunte 1 unité = 10 dixièmes : 14 − 7 = 7.", "Le chiffre des unités passe de 2 à 1."),
                 ("Unités : 1 − 4 impossible. On emprunte 1 dizaine = 10 unités : 11 − 4 = 7. Dizaines : 0.", "Le chiffre des dizaines passe de 1 à 0."),
                 (column("-", "12,50", "4,75", "7,75"), "Vérification : 7,75 + 4,75 = 12,50, on retrouve bien 12,5.")],
                N("7,75"), "d('12,5')-d('4,75')==d('7,75') and d('7,75')+d('4,75')==d('12,5')"),
        example("Exemple 2", "Calculer " + N("20 - 6,38") + ".",
                "Un nombre entier est un décimal : on écrit 20 sous la forme 20,00. Les unités et les dixièmes de 20,00 valent 0 : l'emprunt se fait en chaîne.",
                [(column("-", "20,00", "6,38"), "On ajoute la virgule et deux zéros, et on aligne les virgules."),
                 ("Centièmes : 0 − 8 impossible, mais les dixièmes et les unités valent 0. On emprunte à la dizaine.", "20 = 19 unités + 9 dixièmes + 10 centièmes : on a transformé 1 dizaine en 9 unités, 9 dixièmes et 10 centièmes."),
                 ("Centièmes : 10 − 8 = 2. Dixièmes : 9 − 3 = 6. Unités : 9 − 6 = 3. Dizaines : 1.", "On soustrait colonne par colonne."),
                 (column("-", "20,00", "6,38", "13,62"), "Vérification : 13,62 + 6,38 = 20 car 62 + 38 = 100 centièmes = 1 unité, puis 13 + 6 + 1 = 20.")],
                N("13,62"), "d('20')-d('6,38')==d('13,62') and d('13,62')+d('6,38')==d('20')"),
        example("Exemple 3", "Un ruban mesure 3,2 m. On coupe 1,85 m. Quelle longueur reste-t-il ?",
                "On cherche ce qui reste : c'est une soustraction.",
                [("Reste = " + N("3,2 - 1,85"), "On enlève la longueur coupée à la longueur totale."),
                 ("$3{,}20 - 1{,}85 = 1{,}35$", "On écrit 3,2 sous la forme 3,20. Centièmes : 10 − 5 = 5 après emprunt. Dixièmes : 1 − 8 impossible, on emprunte : 11 − 8 = 3. Unités : 2 − 1 = 1."),
                 ("$1{,}35 + 1{,}85 = 3{,}20$", "Vérification : on retrouve la longueur de départ.")],
                "Il reste " + N("1,35") + " m de ruban.", "d('3,2')-d('1,85')==d('1,35')"),
        example("Exemple 4", "Trouver le nombre qui, ajouté à " + N("7,3") + ", donne " + N("10") + ".",
                "On cherche un terme manquant dans une addition : c'est une soustraction.",
                [(N("7,3 + ? = 10"), "On traduit la question."),
                 ("$? = 10 - 7{,}3$", "Le nombre cherché est la différence entre le total et le terme connu."),
                 ("$? = 2{,}7$", "10,0 − 7,3 : 10 unités = 100 dixièmes, 100 − 73 = 27 dixièmes. Vérification : 7,3 + 2,7 = 10.")],
                N("2,7"), "d('10')-d('7,3')==d('2,7')"),
        warning("Dans " + N("5 - 2,3") + ", on ne calcule pas 5 − 2 = 3 puis « ,3 ». Il faut écrire 5 = 5,0 et soustraire 2,3 : on trouve " + N("2,7") + ", pas 3,3. Vérifie : 2,7 + 2,3 = 5."),
    ],
    [
        number("s5-g1", "soustraction", "Calcule " + N("25,4 - 8,67") + ".", d("16,73"),
               hints=["Écris 25,4 avec deux chiffres après la virgule.", "Pose la soustraction avec les virgules alignées ; commence par les centièmes et emprunte si le chiffre du haut est trop petit."],
               solution=["25,4 = 25,40.", "Centièmes : 0 − 7 impossible, on emprunte : 10 − 7 = 3. Dixièmes : 3 − 6 impossible, on emprunte : 13 − 6 = 7. Unités : 4 − 8 impossible, on emprunte : 14 − 8 = 6. Dizaines : 1.", "25,4 − 8,67 = 16,73. Vérification : 16,73 + 8,67 = 25,40."]),
        number("s5-g2", "soustraction", "Calcule " + N("6 - 2,45") + ".", d("3,55"),
               hints=["Un entier est un décimal : comment l'écrire avec deux chiffres après la virgule ?", "Pose la soustraction avec les virgules alignées et soustrais les centièmes en premier."],
               solution=["6 = 6,00.", "Centièmes : 10 − 5 = 5 après emprunt. Dixièmes : 9 − 4 = 5. Unités : 5 − 2 = 3.", "6 − 2,45 = 3,55. Vérification : 3,55 + 2,45 = 6."],
               wrong={"4,45": "Tu as fait 6 − 2 = 4 puis tu as recopié ,45. Il faut compléter 6 par 6,00 et soustraire les centièmes aussi."}),
        number("s5-g3", "soustraction", "Une corde mesure 9 m. On en coupe 3,75 m, puis 2,5 m. Quelle longueur reste-t-il ?", d("2,75"), units=["m"],
               hints=["Il y a deux morceaux coupés. Tu peux soustraire l'un puis l'autre, ou enlever leur somme.", "Calcule d'abord la longueur coupée en tout."],
               solution=["Longueur coupée en tout : 3,75 + 2,50 = 6,25 m.", "Longueur restante : 9 − 6,25 = 2,75 m.", "Vérification : 2,75 + 6,25 = 9."]),
        number("s5-g4", "soustraction", "Quel nombre faut-il ajouter à " + N("3,6") + " pour obtenir " + N("8") + " ?", d("4,4"),
               hints=["Un terme manquant dans une addition se trouve par une soustraction. Laquelle ?"],
               solution=["Le nombre cherché est 8 − 3,6.", "8 = 8,0. Dixièmes : 10 − 6 = 4 après emprunt. Unités : 7 − 3 = 4.", "Le nombre cherché est 4,4. Vérification : 3,6 + 4,4 = 8."],
               wrong={"5,6": "Tu as calculé 8 − 3 = 5 puis tu as recopié ,6. Écris 8 sous la forme 8,0 et soustrais aussi les dixièmes."}),
    ])

# ----- Independent practice, from easy to hard -----
PRACTICE = [
    number("p1", "ecritures", "Écris " + N("358/100") + " avec une virgule.", d("3,58"), 1,
           ["Le dénominateur a deux zéros : combien de chiffres après la virgule ?"], ["358/100 = 3,58."], form="decimal"),
    number("p2", "ecritures", "Écris " + N("0,009") + " sous la forme d'une fraction décimale.", d("0,009"), 1, ["Combien de chiffres après la virgule ?"],
           ["Trois chiffres après la virgule : dénominateur 1 000. 0,009 = 9/1000."], form="decimal_fraction"),
    number("p3", "ecritures", "Écris " + N("13/1000") + " avec une virgule.", d("0,013"), 2,
           ["Trois chiffres après la virgule, mais 13 n'en a que deux. Que faut-il ajouter ?"], ["13/1000 = 0,013."], form="decimal"),
    number("p4", "ecritures", "Écris " + N("7/20") + " avec une virgule.", d("0,35"), 3,
           ["Par quel nombre faut-il multiplier 20 pour obtenir 100 ? Que faut-il faire du numérateur ?"],
           ["20 × 5 = 100, donc 7/20 = (7 × 5)/(20 × 5) = 35/100.", "35/100 = 0,35."], form="decimal"),
    number("p5", "ecritures", "Complète : " + "$2{,}35 = 2 + \\dfrac{3}{10} + \\dfrac{?}{100}$", Fraction(5), 2,
           ["Quel est le rang du chiffre 5 dans 2,35 ?"], ["Le chiffre 5 est au rang des centièmes : il vaut 5/100.", "Donc 2,35 = 2 + 3/10 + 5/100."]),
    choice("p6", "ecritures", "Quel nombre appartient à " + D + " mais n'appartient pas à " + NAT + " ?", [N("7"), N("7,0"), N("7,5"), N("70")], 2, 1,
           ["Lesquels de ces nombres sont égaux à un entier naturel ?"], ["7, 7,0 (qui vaut 7) et 70 sont des entiers naturels.", "7,5 est un décimal qui n'est pas entier : c'est le seul."]),
    number("p7", "rang", "Quelle est la partie entière de " + N("804,19") + " ?", Fraction(804), 1, ["C'est ce qui est à gauche de la virgule."], ["La partie entière est 804."]),
    number("p8", "rang", "Quel est le chiffre des dixièmes de " + N("20,968") + " ?", Fraction(9), 1, ["C'est le premier chiffre après la virgule."], ["Après la virgule : 9 (dixièmes), 6 (centièmes), 8 (millièmes)."]),
    number("p9", "rang", "Quelle est la valeur du chiffre 4 dans " + N("31,642") + " ?", d("0,04"), 2,
           ["Quel est le rang du 4 ? Après la virgule on lit 6, puis 4, puis 2."], ["Le 4 est au rang des centièmes : 4 × 0,01 = 0,04."],
           wrong={"4": "4 est le chiffre. Sa valeur dépend de son rang : il est au rang des centièmes.", "0,4": "0,4 serait la valeur du 4 au rang des dixièmes. Ici le 4 est au rang suivant."}),
    number("p10", "rang", "Écris la partie décimale de " + N("90,305") + " sous la forme d'un nombre plus petit que 1.", d("0,305"), 2,
           ["La partie décimale, ce sont les chiffres à droite de la virgule."], ["Les chiffres à droite de la virgule sont 3, 0 et 5.", "Ils représentent 0,305."]),
    number("p11", "rang", "Combien de centièmes y a-t-il dans " + N("6,08") + " ?", Fraction(608), 2,
           ["1 unité = 100 centièmes et 1 dixième = 10 centièmes. Combien de dixièmes y a-t-il dans 6,08 ?"], ["6 unités = 600 centièmes, 0 dixième = 0 centième, et 8 centièmes.", "600 + 0 + 8 = 608 centièmes."]),
    number("p12", "rang", "Combien de dixièmes y a-t-il dans " + N("3,9") + " ?", Fraction(39), 2,
           ["1 unité = 10 dixièmes."], ["3 unités = 30 dixièmes, et il y a 9 dixièmes de plus.", "30 + 9 = 39 dixièmes."]),
    number("p13", "rang", "Écris en chiffres : sept unités et huit dixièmes.", d("7,8"), 1,
           ["Les unités sont à gauche de la virgule, les dixièmes juste à droite."], ["7 unités donnent la partie entière 7, 8 dixièmes donnent le chiffre 8 après la virgule.", "Le nombre est 7,8."]),
    number("p14", "rang", "Avec les cartes 4, 0 et 9, chacune utilisée une seule fois, on forme un nombre de la forme " + N("A,BC") + ". Quel est le plus grand nombre possible ?", d("9,4"), 3,
           ["Le rang le plus à gauche compte le plus : quel chiffre y mettre pour avoir un grand nombre ?"],
           ["Les unités comptent le plus : 9. Puis les dixièmes : 4. Il reste 0 pour les centièmes.", "Le nombre est 9,40, qui s'écrit aussi 9,4."]),
    choice("p15", "comparer", "Quel signe faut-il entre 3,7 et 3,07 ?", [N("3,7 < 3,07"), N("3,7 > 3,07"), N("3,7 = 3,07")], 1, 1,
           ["Écris les deux nombres avec deux chiffres après la virgule."], ["3,7 = 3,70. Les parties décimales sont 70 et 07 : 70 > 07.", "3,7 > 3,07."]),
    ordered("p16", "comparer", "Range dans l'ordre décroissant, en séparant par des points-virgules : " + N("0,8") + " ; " + N("0,78") + " ; " + N("0,087") + " ; " + N("0,807") + ".",
            [d("0,807"), d("0,8"), d("0,78"), d("0,087")], 2, ["Donne trois chiffres après la virgule à chaque nombre."],
            ["0,800 ; 0,780 ; 0,087 ; 0,807. Les parties décimales sont 800, 780, 087, 807.", "De la plus grande à la plus petite : 807 > 800 > 780 > 087.", "0,807 > 0,8 > 0,78 > 0,087."]),
    between("p17", "comparer", "Écris un nombre décimal compris strictement entre " + N("2,45") + " et " + N("2,46") + ".", d("2,45"), d("2,46"), 2,
            ["Il n'y a pas de nombre à deux chiffres après la virgule entre les deux. Combien de chiffres faut-il ?"],
            ["2,45 = 2,450 et 2,46 = 2,460.", "Tout nombre de 2,451 à 2,459 convient, par exemple 2,455."]),
    number("p18", "comparer", "Encadre " + N("15,078") + " au dixième près. Quel est le plus grand des deux nombres de l'encadrement ?", d("15,1"), 2,
           ["Le plus petit des deux est obtenu en gardant les chiffres jusqu'aux dixièmes. Que faut-il ajouter pour obtenir le suivant ?"],
           ["15,078 est compris entre 15,0 et 15,1, car 15,000 < 15,078 < 15,100.", "L'encadrement est 15,0 < 15,078 < 15,1. Le plus grand des deux nombres est 15,1."]),
    number("p19", "comparer", "Quel est le plus petit entier plus grand que " + N("99,9") + " ?", Fraction(100), 1,
           ["Encadre 99,9 à l'unité près."], ["99 < 99,9 < 100.", "Le plus petit entier plus grand que 99,9 est 100."]),
    choice("p20", "comparer", "Marie dit : « 4,12 est plus grand que 4,8 parce que 12 est plus grand que 8 ». Quelle est la bonne réponse ?",
           ["Elle a raison, 12 est plus grand que 8", "Elle a tort : 4,8 = 4,80 et 80 est plus grand que 12", "Elle a tort : un nombre avec plus de chiffres est toujours plus petit"], 1, 3,
           ["Que se passe-t-il quand on donne le même nombre de chiffres après la virgule aux deux nombres ?"],
           ["On ne peut pas comparer 12 et 8 directement : ce ne sont pas des nombres de même rang.", "4,8 = 4,80. Avec deux chiffres après la virgule, on compare 12 et 80 : 80 > 12.", "Donc 4,8 > 4,12. Et ce n'est pas le nombre de chiffres qui décide : 4,12 est petit, mais 4,125 serait aussi plus petit que 4,8."],
           wrong={2: "Le nombre de chiffres ne décide pas : 4,125 a trois chiffres après la virgule mais il est plus petit que 4,8, alors que 4,81 en a deux et il est plus grand que 4,8. Ce qui compte, c'est la comparaison rang par rang."}),
    number("p21", "addition", "Calcule " + N("6,4 + 2,35") + ".", d("8,75"), 1, ["Écris 6,4 avec deux chiffres après la virgule."], ["6,40 + 2,35 = 8,75."]),
    number("p22", "addition", "Calcule en regroupant astucieusement : " + N("0,9 + 12 + 0,75 + 7,1") + ".", d("20,75"), 2,
           ["Cherche deux termes dont la somme est un entier."], ["0,9 + 7,1 = 8.", "8 + 12 = 20, puis 20 + 0,75 = 20,75."]),
    number("p23", "addition", "Calcule " + N("0,999 + 0,001") + ".", Fraction(1), 2,
           ["Écris l'addition en colonnes. Que se passe-t-il à chaque colonne ?"], ["Millièmes : 9 + 1 = 10, on écrit 0 et on retient 1. Centièmes : 9 + 1 = 10, on écrit 0 et on retient 1. Dixièmes : 9 + 1 = 10, on écrit 0 et on retient 1.", "Unités : 0 + 0 + 1 = 1. Le résultat est 1,000 = 1."]),
    number("p24", "addition", "Estime " + N("61,4 + 28,9 + 9,5") + " en arrondissant chaque nombre à la dizaine la plus proche.", Fraction(100), 2,
           ["Regarde le chiffre des unités de chaque nombre."], ["61,4 : unités 1, on garde 60. 28,9 : unités 8, on passe à 30. 9,5 : unités 9, on passe à 10.", "60 + 30 + 10 = 100."]),
    choice("p25", "addition", "Léa a calculé " + N("4,6 + 3,25 = 3,71") + ". Quelle erreur a-t-elle faite ?",
           ["Elle n'a pas aligné les virgules", "Elle a oublié une retenue", "Elle a soustrait au lieu d'additionner"], 0, 2,
           ["Compare son résultat avec un ordre de grandeur : 4,6 + 3,25 est proche de 5 + 3."],
           ["Un ordre de grandeur donne environ 8, et Léa trouve 3,71 : le résultat est trop petit.", "Elle a additionné 46 et 325 comme des entiers, sans aligner les virgules : 46 + 325 = 371.", "Le bon calcul est 4,60 + 3,25 = 7,85."]),
    choice("p26", "addition", "On écrit " + N("(1,2 + 3,8) + 4,5 = 1,2 + (3,8 + 4,5)") + ". Quelle propriété utilise-t-on ?", ["La commutativité", "L'associativité", "L'élément neutre"], 1, 2,
           ["L'ordre des termes change-t-il ?"], ["L'ordre des termes est le même des deux côtés ; seuls les regroupements changent.", "C'est l'associativité."]),
    number("p27", "problemes", "Au marché, Awa achète 12,5 kg de riz, 8,75 kg de mil et 6,25 kg d'arachides. Quelle est la masse totale de ses achats, en kg ?", d("27,5"), 3,
           ["Quelle opération donne une masse totale ?", "Cherche deux nombres dont la somme est un entier."],
           ["Masse totale = 12,5 + 8,75 + 6,25.", "8,75 + 6,25 = 15, puis 12,5 + 15 = 27,5.", "Awa achète 27,5 kg."], units=["kg"]),
    number("p28", "soustraction", "Calcule " + N("9,8 - 3,5") + ".", d("6,3"), 1, ["Les deux nombres ont un chiffre après la virgule."], ["98 dixièmes − 35 dixièmes = 63 dixièmes.", "9,8 − 3,5 = 6,3."]),
    number("p29", "soustraction", "Calcule " + N("15 - 7,26") + ".", d("7,74"), 2, ["Écris 15 avec deux chiffres après la virgule."], ["15 = 15,00. Centièmes : 10 − 6 = 4 après emprunt. Dixièmes : 9 − 2 = 7. Unités : 14 − 7 = 7.", "15 − 7,26 = 7,74. Vérification : 7,74 + 7,26 = 15."],
           wrong={"8,26": "Tu as soustrait 7 de 15 puis tu as recopié ,26. Il faut compléter 15 par 15,00 et emprunter."}),
    number("p30", "soustraction", "Quel nombre faut-il ajouter à " + N("4,35") + " pour obtenir " + N("10") + " ?", d("5,65"), 2,
           ["Un terme manquant se trouve par une soustraction."], ["? = 10 − 4,35 = 10,00 − 4,35 = 5,65.", "Vérification : 4,35 + 5,65 = 10."]),
    number("p31", "soustraction", "Calcule " + N("100 - 0,01") + ".", d("99,99"), 3,
           ["Écris 100 avec deux chiffres après la virgule. Que se passe-t-il avec tous ces zéros ?"], ["100 = 100,00. Il faut emprunter à la centaine, en chaîne : 100 = 99 unités + 9 dixièmes + 10 centièmes.", "10 − 1 = 9 centièmes, 9 dixièmes et 99 unités : le résultat est 99,99. Vérification : 99,99 + 0,01 = 100."]),
    number("p32", "soustraction", "Calcule " + N("1000 - 99,99") + ".", d("900,01"), 3,
           ["Écris 1000 avec deux chiffres après la virgule."], ["1000 = 1000,00 : 100 000 centièmes − 9 999 centièmes = 90 001 centièmes.", "90 001 centièmes, c'est 900,01. Vérification : 900,01 + 99,99 = 1000."]),
    choice("p33", "soustraction", "Karim a calculé " + N("9 - 4,7 = 5,7") + ". Quelle erreur a-t-il faite ?",
           ["Il a calculé 9 − 4 = 5 puis il a recopié ,7", "Il a oublié une retenue dans les unités", "Il a additionné au lieu de soustraire"], 0, 3,
           ["Vérifie son résultat : additionne 5,7 et 4,7. Trouves-tu 9 ?"],
           ["5,7 + 4,7 = 10,4, et non 9 : son résultat est faux.", "Il a fait 9 − 4 = 5 puis il a recopié ,7. Il faut écrire 9 = 9,0 et emprunter.", "Le bon résultat est 4,3. Vérification : 4,3 + 4,7 = 9."]),
    number("p34", "problemes", "Un réservoir contient 50 L d'eau. On en retire 18,75 L puis 13,5 L. Combien de litres reste-t-il ?", d("17,75"), 3,
           ["On peut soustraire deux fois, ou calculer d'abord ce qui est retiré en tout."],
           ["Eau retirée en tout : 18,75 + 13,50 = 32,25 L.", "Eau restante : 50 − 32,25 = 17,75 L.", "Vérification : 17,75 + 32,25 = 50."], units=["L"]),
]

SUMMARY = [
    definition("Définitions", "Une fraction décimale a pour dénominateur 10, 100, 1 000... Un nombre décimal arithmétique est un nombre positif ou nul qui s'écrit comme une fraction décimale. "
                              "On a " + "$\\mathbb{N} \\subset \\mathbb{D}$" + ". La partie entière est à gauche de la virgule, la partie décimale (les chiffres à droite) représente un nombre plus petit que 1."),
    rule("Rangs et valeurs", "Les rangs à droite de la virgule sont les dixièmes (" + N("0,1") + "), les centièmes (" + N("0,01") + ") et les millièmes (" + N("0,001") + "). "
                             "La valeur d'un chiffre est le chiffre multiplié par la valeur de son rang. 1 unité = 10 dixièmes = 100 centièmes = 1 000 millièmes."),
    rule("Fraction décimale et écriture à virgule", "Autant de zéros au dénominateur qu'il y a de chiffres après la virgule : " + N("235/100 = 2,35") + "."),
    rule("Comparer", "On compare les parties entières, puis les chiffres des dixièmes, des centièmes... Si les parties entières sont égales, on peut ajouter des zéros pour avoir le même nombre de chiffres après la virgule."),
    rule("Ranger, encadrer, intercaler", "Ranger, c'est ordonner (< croissant, > décroissant). Encadrer à l'unité près, c'est donner deux entiers consécutifs ; au dixième près, deux nombres consécutifs à un chiffre après la virgule. "
                                         "On peut toujours intercaler un nombre décimal entre deux décimaux différents, en ajoutant des zéros."),
    rule("Additionner", "On aligne les virgules, on complète par des zéros et on additionne de droite à gauche. Propriétés : " + N("a + b = b + a") + ", " + N("(a + b) + c = a + (b + c)") + ", " + N("a + 0 = a") + "."),
    rule("Ordre de grandeur", "On arrondit chaque nombre (par exemple à la dizaine la plus proche : on regarde le chiffre des unités, 0 à 4 on garde, 5 à 9 on passe à la dizaine suivante), puis on calcule. Cela permet de vérifier un résultat."),
    rule("Soustraire", "On aligne les virgules, on complète par des zéros et on soustrait de droite à gauche, en empruntant si besoin. On vérifie avec l'addition : si " + N("a - b = c") + " alors " + N("c + b = a") + ". On ne peut pas échanger les deux nombres d'une soustraction."),
    para("Les erreurs à éviter : croire que plus de chiffres après la virgule veut dire plus grand ; oublier de compléter par des zéros avant de soustraire ; confondre dizaine et dixième ; additionner sans aligner les virgules."),
]

CONCEPTS = {
    "ecritures": ("Écritures d'un nombre décimal", "ecritures"),
    "rang": ("Rang, valeur et parties d'un nombre décimal", "rang"),
    "comparer": ("Comparer, ranger, encadrer, intercaler", "comparer"),
    "addition": ("Additionner des décimaux", "addition"),
    "soustraction": ("Soustraire des décimaux", "soustraction"),
    "problemes": ("Résoudre un problème", "soustraction"),
}


def rand_decimal(rng, low, high, places):
    """Return a random number with exactly this many decimals whose last decimal is not 0."""
    last = rng.randint(1, 9)
    middle = rng.randint(0, 10 ** (places - 1) - 1) if places > 1 else 0
    return Fraction(rng.randint(low, high) * 10**places + middle * 10 + last, 10**places)


def spaced(value, places):
    """Write a value with exactly this many decimals, padding with zeros."""
    return show(value) if places == 0 else f"{int(value)},{str(int((value - int(value)) * 10**places)).rjust(places, '0')}"


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    n = lambda value, places=None: N(spaced(value, places) if places is not None else show(value))
    questions = []

    # 1. fraction décimale -> écriture à virgule, sometimes with zeros to add in front
    places = rng.choice([1, 2, 3])
    top = rng.randint(1, 10 ** (places - 1) - 1) if places > 1 and rng.random() < 0.5 else rng.randint(2, 9 * 10**places)
    top += 1 if top % 10 == 0 else 0
    questions.append(number("a1", "ecritures", "Écris " + N(f"{top}/{10 ** places}") + " avec une virgule.", Fraction(top, 10**places), 1,
                            [f"Le dénominateur {10 ** places} a {places} zéro" + ("s" if places > 1 else "") + ", donc autant de chiffres après la virgule. S'il manque des chiffres, ajoute des zéros devant."],
                            [f"Le dénominateur a {places} zéro" + ("s" if places > 1 else "") + f", donc {places} chiffre" + ("s" if places > 1 else "") + " après la virgule.",
                             f"{top}/{10 ** places} = {show(Fraction(top, 10 ** places))}."], form="decimal"))

    # 2. écriture à virgule -> fraction décimale
    places = rng.choice([1, 2, 3])
    value = rand_decimal(rng, 0, 20, places)
    questions.append(number("a2", "ecritures", "Écris " + n(value, places) + " sous la forme d'une fraction décimale (numérateur entier, dénominateur 10, 100, 1000...).",
                            value, 1, ["Compte les chiffres après la virgule : cela donne le dénominateur."],
                            [f"Il y a {places} chiffre" + ("s" if places > 1 else "") + f" après la virgule : le dénominateur est {10 ** places}.",
                             f"Sans la virgule on lit {int(value * 10 ** places)} : {spaced(value, places)} = {int(value * 10 ** places)}/{10 ** places}."], form="decimal_fraction"))

    # 3 and 4. rank and value of a digit, with five different digits so the question has one answer
    digits = rng.sample(range(10), 5)
    if digits[0] == 0:
        digits[0], digits[1] = digits[1], digits[0]
    text = f"{digits[0]}{digits[1]},{digits[2]}{digits[3]}{digits[4]}"
    rank = rng.choice([0, 1, 2])
    names = ["dixièmes", "centièmes", "millièmes"]
    questions.append(number("a3", "rang", "Quel est le chiffre des " + names[rank] + " dans " + N(text) + " ?", Fraction(digits[2 + rank]), 1,
                            ["Les chiffres après la virgule sont, dans l'ordre : dixièmes, centièmes, millièmes."],
                            [f"Après la virgule on lit {digits[2]} (dixièmes), {digits[3]} (centièmes), {digits[4]} (millièmes).", f"Le chiffre des {names[rank]} est {digits[2 + rank]}."]))
    pick = rng.choice([p for p in (2, 3, 4) if digits[p] != 0])
    place_value = Fraction(1, 10 ** (pick - 1))
    value = digits[pick] * place_value
    questions.append(number("a4", "rang", "Quelle est la valeur du chiffre " + str(digits[pick]) + " dans " + N(text) + " ?", value, 2,
                            ["Trouve d'abord son rang, puis multiplie le chiffre par la valeur de ce rang."],
                            [f"Le chiffre {digits[pick]} est au rang des {names[pick - 2]}.", f"Sa valeur est {digits[pick]} × {show(place_value)} = {show(value)}."],
                            wrong={str(digits[pick]): "C'est le chiffre, pas sa valeur. Multiplie par la valeur de son rang."}))

    # 5. largest of three
    whole = rng.randint(1, 20)
    tenth = rng.randint(2, 8)
    if rng.random() < 0.5:
        values = [Fraction(whole * 10 + tenth, 10), Fraction(whole * 100 + tenth, 100), Fraction(whole * 1000 + (tenth - 1) * 100 + 99, 1000)]
    else:
        # The largest has two decimals, and the number with the most decimals is still a distractor.
        values = [Fraction(whole * 10 + tenth, 10), Fraction(whole * 100 + tenth * 10 + 5, 100), Fraction(whole * 1000 + (tenth - 1) * 100 + 99, 1000)]
    shown = [N(spaced(v, p)) for v, p in zip(values, (1, 2, 3))]
    order = [0, 1, 2]
    rng.shuffle(order)
    options = [shown[i] for i in order]
    right = order.index(max(range(3), key=lambda i: values[i]))
    longest = order.index(2)
    questions.append(choice("a5", "comparer", "Quel est le plus grand de ces trois nombres ?", options, right, 2,
                            ["Les parties entières sont égales. Écris les trois nombres avec trois chiffres après la virgule."],
                            ["On écrit les nombres avec trois chiffres après la virgule : " + " ; ".join(spaced(v, 3) for v in values) + ".",
                             "Le plus grand est " + spaced(max(values), 3) + "."],
                            wrong={longest: "Plus de chiffres après la virgule ne veut pas dire plus grand. Compare les nombres avec le même nombre de chiffres."} if right != longest else {}))

    # 6. order four numbers
    base = rng.randint(1, 9)
    pool = {Fraction(base * 10 + rng.randint(1, 9), 10), Fraction(base * 100 + rng.randint(1, 9), 100), Fraction(base * 1000 + rng.randint(1, 99), 1000),
            Fraction((base + 1) * 10 - rng.randint(1, 3), 10)}
    while len(pool) < 4:
        pool.add(Fraction(base * 100 + rng.randint(10, 99), 100))
    four = sorted(pool)
    shuffled = four[:]
    rng.shuffle(shuffled)
    questions.append(ordered("a6", "comparer", "Range dans l'ordre croissant, en séparant par des points-virgules : " + " ; ".join(N(show(v)) for v in shuffled) + ".", four, 2,
                             ["Compare d'abord les parties entières, puis écris les nombres avec le même nombre de chiffres après la virgule."],
                             ["Avec trois chiffres après la virgule : " + " ; ".join(spaced(v, 3) for v in shuffled) + ".", "Dans l'ordre croissant : " + " < ".join(show(v) for v in four) + "."]))

    # 7. addition with different numbers of decimals
    a, b = rand_decimal(rng, 10, 90, 1), rand_decimal(rng, 2, 40, 2)
    if rng.random() < 0.5:
        a, b = b, a
    questions.append(number("a7", "addition", "Calcule " + N(f"{show(a)} + {show(b)}") + ".", a + b, 2,
                            ["Complète par des zéros pour que les deux nombres aient autant de chiffres après la virgule."],
                            [f"{show(a)} = {spaced(a, 2)} et {show(b)} = {spaced(b, 2)}.", f"En centièmes : {int(a * 100)} + {int(b * 100)} = {int((a + b) * 100)}.", f"{spaced(a, 2)} + {spaced(b, 2)} = {show(a + b)}."]))

    # 8. subtraction with borrowing
    big_value = rand_decimal(rng, 10, 80, 1) if rng.random() < 0.7 else Fraction(rng.randint(10, 90))
    small = rand_decimal(rng, 1, 9, 2)
    questions.append(number("a8", "soustraction", "Calcule " + N(f"{show(big_value)} - {show(small)}") + ".", big_value - small, 2,
                            ["Écris le premier nombre avec deux chiffres après la virgule, puis soustrais en colonnes en empruntant si besoin."],
                            [f"{show(big_value)} = {spaced(big_value, 2) if big_value.denominator != 1 else str(int(big_value)) + ',00'}.",
                             f"En centièmes : {int(big_value * 100)} − {int(small * 100)} = {int((big_value - small) * 100)}.",
                             f"Donc {show(big_value)} − {show(small)} = {show(big_value - small)}.", f"Vérification : {show(big_value - small)} + {show(small)} = {show(big_value)}."]))

    # 9. problem with two steps
    total = rand_decimal(rng, 8, 20, 1)
    first, second = rand_decimal(rng, 1, 4, 2), rand_decimal(rng, 1, 3, 1)
    if first + second >= total:
        total = first + second + 5
    rest = total - first - second
    questions.append(number("a9", "problemes", f"Un tailleur a {show(total)} m de tissu. Il en utilise {show(first)} m pour une chemise et {show(second)} m pour un pantalon. Quelle longueur de tissu lui reste-t-il, en mètres ?",
                            rest, 3, ["Calcule d'abord la longueur utilisée en tout, puis soustrais-la."],
                            [f"Longueur utilisée : {show(first)} + {show(second)} = {show(first + second)} m.", f"Longueur restante : {show(total)} − {show(first + second)} = {show(rest)} m.", f"Vérification : {show(rest)} + {show(first + second)} = {show(total)}."],
                            units=["m"]))

    # 10. insert a number between two close decimals
    hundredths = rng.randint(10, 98)
    low, high = Fraction(300 + hundredths, 100), Fraction(300 + hundredths + 1, 100)
    questions.append(between("a10", "comparer", "Écris un nombre décimal compris strictement entre " + N(show(low)) + " et " + N(show(high)) + ".", low, high, 3,
                             ["Il n'y a pas de nombre à deux chiffres après la virgule entre les deux : combien de chiffres faut-il ?"],
                             [f"{show(low)} = {spaced(low, 3)} et {show(high)} = {spaced(high, 3)}.", f"Tout nombre de {spaced(low + Fraction(1, 1000), 3)} à {spaced(high - Fraction(1, 1000), 3)} convient."]))

    # 11. bound a number to the nearest whole numbers
    whole = rng.randint(10, 99)
    bounded = Fraction(whole * 1000 + rng.randint(1, 999), 1000)
    questions.append(number("a11", "comparer", "Encadre " + N(show(bounded)) + " à l'unité près. Quel est le plus grand des deux entiers de l'encadrement ?", Fraction(whole + 1), 2,
                            ["Quelle est la partie entière du nombre ? L'autre entier est celui qui la suit."],
                            [f"La partie entière de {show(bounded)} est {whole}, et le nombre n'est pas entier.", f"{whole} < {show(bounded)} < {whole + 1}. Le plus grand des deux entiers est {whole + 1}."]))

    # 12. explain a typical mistake
    unit = rng.randint(1, 9)
    tenths = rng.randint(4, 9)
    short = f"{unit},{tenths}"
    tail = f"{rng.randint(1, tenths - 1)}{rng.randint(0, 9)}"
    long = f"{unit},{tail}"
    options = [f"Il a raison : on compare {tail} et {tenths} comme des entiers",
               f"Il a tort : {short} = {unit},{tenths}0 et {tenths}0 est plus grand que {tail}",
               "Il a tort : un nombre avec plus de chiffres après la virgule est toujours plus petit"]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a12", "comparer", f"Moussa dit : « {N(long)} est plus grand que {N(short)} parce que {tail} est plus grand que {tenths} ». Quelle est la bonne réponse ?",
                            [options[i] for i in order], order.index(1), 3,
                            ["Écris les deux nombres avec le même nombre de chiffres après la virgule avant de les comparer."],
                            [f"On écrit {short} = {unit},{tenths}0 pour avoir deux chiffres après la virgule.", f"On compare les parties décimales {tail} et {tenths}0 : {tenths}0 est plus grand.",
                             f"Donc {short} > {long}. Moussa a comparé {tail} et {tenths} comme des entiers, sans tenir compte du rang des chiffres."],
                            wrong={order.index(2): "Le nombre de chiffres ne décide pas du plus grand. Écris les deux nombres avec le même nombre de chiffres après la virgule, puis compare."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=1, title="Les nombres décimaux arithmétiques", language="fr",
    intro="Les nombres décimaux sont partout : les prix, les longueurs, les masses, les temps de course. Quand on mesure un tissu, un sac de riz ou une distance, "
          "le résultat tombe rarement sur un nombre entier. Ce chapitre t'apprend à lire, écrire, comparer et ranger ces nombres, puis à les additionner et à les soustraire sans te tromper.",
    objectives=["Reconnaître une fraction décimale et l'écrire avec une virgule, et inversement.",
                "Donner la partie entière, la partie décimale, le rang et la valeur de chaque chiffre d'un nombre décimal, et passer d'un rang à l'autre.",
                "Comparer et ranger des nombres décimaux, en intercaler un entre deux autres et les encadrer.",
                "Additionner des nombres décimaux en colonnes et avec les propriétés de l'addition, et donner un ordre de grandeur.",
                "Soustraire des nombres décimaux, vérifier le résultat et résoudre des problèmes de la vie courante."],
    prerequisites=[{"text": "Comprendre ce que veut dire une fraction : partager l'unité en parts égales et en prendre quelques-unes.", "course": "fractions-decimals", "lesson": "fraction-meaning"},
                   {"text": "Lire et écrire un nombre entier et connaître le rang de ses chiffres (unités, dizaines, centaines).", "course": "whole-numbers", "lesson": "place-value"},
                   {"text": "Additionner et soustraire des nombres entiers, avec retenue et emprunt.", "course": "whole-numbers", "lesson": "add-subtract"}],
    sections=[S1, S2, S3, S4, S5], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E],
    status_note="Reference chapter. Its topics follow the first chapters of the ADEM-Dakar Sixième booklet, with our own order, explanations and exercises (some exercise types are common to the booklet). It has not been checked against the official Senegalese programme.",
)
