"""Sixième, Diviser des nombres décimaux: the third chapter of the Senegal Sixième course, written in French.

The topics follow the division chapter of the ADEM-Dakar Sixième booklet (exact quotient, fractions as quotients, dividing by a decimal,
approximate quotients), but every explanation, example and exercise was written independently, with our own numbers.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-6e-division"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")


def terminates(value):
    """Return True when a fraction has a finite decimal writing, that is when only 2 and 5 divide its denominator."""
    denominator = Fraction(value).denominator
    for prime in (2, 5):
        while denominator % prime == 0:
            denominator //= prime
    return denominator == 1


def below(value, places):
    """Return the approximation by default (the largest decimal with this many places that is not above the value)."""
    scale = 10**places
    return Fraction((Fraction(value) * scale) // 1, scale)


def nearest(value, places):
    """Return the decimal with this many places that is closest to the value."""
    low = below(value, places)
    high = low + Fraction(1, 10**places)
    return low if Fraction(value) - low <= high - Fraction(value) else high


def digits(value, places):
    """Write the first decimals of a value without rounding, with a trailing ellipsis."""
    cut = below(value, places)
    return f"{int(cut)},{str(int((cut - int(cut)) * 10**places)).rjust(places, '0')}..."


# ----- Section 1: the quotient of two numbers -----
S1 = Section(
    "quotient", "Le quotient de deux nombres", 24, "quotient",
    "Effectuer une division dont le quotient est un nombre décimal, la vérifier et écrire une fraction sous forme décimale.",
    [
        para("On partage un ruban de 12 m en 8 morceaux de même longueur. Chaque morceau ne mesure pas un nombre entier de mètres : 8 × 1 = 8 m ne suffit pas et 8 × 2 = 16 m est trop. "
             "Le résultat est un nombre décimal, et il s'obtient en continuant la division après la virgule."),
        definition("Quotient, dividende, diviseur",
                   "Diviser un nombre " + N("a") + " (le dividende) par un nombre " + N("b") + " (le diviseur, différent de 0), c'est chercher le nombre " + N("q") + " (le quotient) tel que " + N("b \\times q = a")
                   + ". On écrit " + N("a \\div b = q") + ". Pour vérifier une division, on multiplie le quotient par le diviseur : on doit retrouver le dividende."),
        example("Exemple 1", "Calculer " + N("12 \\div 8") + ".",
                "On pose la division. Quand il reste quelque chose, on continue après la virgule en transformant le reste en dixièmes, puis en centièmes si besoin.",
                [("12 = 1 × 8 + 4", "Dans 12 il y a 1 fois 8, et il reste 4."),
                 ("On écrit 1 au quotient, puis une virgule", "Il reste 4 unités à partager : on les transforme en dixièmes."),
                 ("4 unités = 40 dixièmes et 40 ÷ 8 = 5", "On écrit 5 au quotient, juste après la virgule : le reste est 0, la division est terminée."),
                 (N("12 \\div 8") + " = " + N("1,5"), "Vérification : 8 × 1,5 = 12.")],
                N("1,5"), "d('12')/8==d('1,5') and 8*d('1,5')==12"),
        example("Exemple 2", "Calculer " + N("7,56 \\div 3") + ".",
                "On divise comme pour un entier. Quand on abaisse le premier chiffre après la virgule, on met la virgule au quotient.",
                [("7 ÷ 3 = 2, reste 1", "On écrit 2 au quotient. 3 × 2 = 6, et 7 − 6 = 1."),
                 ("On abaisse le 5 : 15 ÷ 3 = 5, reste 0", "On a franchi la virgule du dividende, donc on écrit une virgule au quotient, puis 5."),
                 ("On abaisse le 6 : 6 ÷ 3 = 2, reste 0", "On écrit 2 au quotient : 2,52."),
                 (N("7,56 \\div 3") + " = " + N("2,52"), "Vérification : 2,52 × 3 = 7,56.")],
                N("2,52"), "d('7,56')/3==d('2,52') and d('2,52')*3==d('7,56')"),
        example("Exemple 3", "Calculer " + N("9 \\div 4") + ".",
                "Le dividende est un entier : on ajoute une virgule et des zéros, c'est-à-dire qu'on écrit 9 = 9,00.",
                [("9 ÷ 4 = 2, reste 1", "4 × 2 = 8 et 9 − 8 = 1."),
                 ("1 unité = 10 dixièmes, 10 ÷ 4 = 2, reste 2", "On écrit la virgule puis 2 au quotient : 2,2. 4 × 2 = 8 et 10 − 8 = 2."),
                 ("2 dixièmes = 20 centièmes, 20 ÷ 4 = 5, reste 0", "On écrit 5 au quotient : 2,25."),
                 (N("9 \\div 4") + " = " + N("2,25"), "Vérification : 4 × 2,25 = 9.")],
                N("2,25"), "d('9')/4==d('2,25') and 4*d('2,25')==9"),
        rule("Une fraction est un quotient",
             "Le quotient de " + N("a") + " par " + N("b") + " s'écrit aussi comme la fraction " + "$\\dfrac{a}{b}$" + ". Pour écrire une fraction sous forme décimale, on effectue la division : "
             + N("3/4 = 3 \\div 4 = 0,75") + "."),
        example("Exemple 4", "Écrire " + N("3/8") + " sous forme décimale.",
                "On divise 3 par 8 en continuant après la virgule.",
                [("3 ÷ 8 = 0, reste 3", "3 est plus petit que 8 : on écrit 0 au quotient, puis une virgule."),
                 ("3 unités = 30 dixièmes, 30 ÷ 8 = 3, reste 6", "8 × 3 = 24 et 30 − 24 = 6. On écrit 3 : 0,3."),
                 ("6 dixièmes = 60 centièmes, 60 ÷ 8 = 7, reste 4", "8 × 7 = 56 et 60 − 56 = 4. On écrit 7 : 0,37."),
                 ("4 centièmes = 40 millièmes, 40 ÷ 8 = 5, reste 0", "On écrit 5 : 0,375."),
                 (N("3/8") + " = " + N("0,375"), "Vérification : 8 × 0,375 = 3.")],
                N("0,375"), "d('3')/8==d('0,375') and 8*d('0,375')==3"),
        warning("On ne peut pas diviser par 0 : " + N("7 \\div 0") + " n'a pas de résultat, car aucun nombre multiplié par 0 ne donne 7. Et diviser un petit nombre par un grand donne un nombre inférieur à 1 : " + N("3 \\div 4 = 0,75") + "."),
    ],
    [
        number("s1-g1", "quotient", "Calcule " + N("15 \\div 6") + ".", d("2,5"),
               hints=["15 = 2 × 6 + 3. Que fait-on du reste 3 ?", "3 unités = 30 dixièmes. Combien de fois 6 dans 30 ?"],
               solution=["15 ÷ 6 = 2, reste 3.", "3 unités = 30 dixièmes et 30 ÷ 6 = 5.", "15 ÷ 6 = 2,5. Vérification : 6 × 2,5 = 15."], form="decimal"),
        number("s1-g2", "quotient", "Calcule " + N("4,56 \\div 4") + ".", d("1,14"),
               hints=["Divise comme pour un entier, et mets la virgule au quotient quand tu abaisses le premier chiffre après la virgule."],
               solution=["4 ÷ 4 = 1, reste 0.", "On abaisse le 5 : 5 ÷ 4 = 1, reste 1, on écrit la virgule puis 1.", "On abaisse le 6 : 16 ÷ 4 = 4, d'où 1,14. Vérification : 4 × 1,14 = 4,56."]),
        number("s1-g3", "quotient", "Écris " + N("7/8") + " sous forme décimale.", d("0,875"),
               hints=["Une fraction est un quotient : effectue 7 ÷ 8 en continuant après la virgule."],
               solution=["7 ÷ 8 = 0, reste 7. 70 ÷ 8 = 8 reste 6 ; 60 ÷ 8 = 7 reste 4 ; 40 ÷ 8 = 5.", "7/8 = 0,875."], form="decimal"),
        choice("s1-g4", "quotient", "Quel calcul permet de vérifier que " + N("9,84 \\div 4 = 2,46") + " ?", [N("2,46 \\times 4 = 9,84"), N("2,46 + 4 = 6,46"), N("9,84 \\times 4 = 39,36")], 0,
               hints=["Si b × q = a, alors a ÷ b = q. Quel produit doit-on retrouver ?"],
               solution=["On multiplie le quotient par le diviseur : 2,46 × 4 = 9,84, c'est le dividende."],
               wrong={1: "Une addition ne vérifie pas une division. Il faut multiplier le quotient par le diviseur."}),
        number("s1-g5", "quotient", "Écris " + N("7/4") + " sous forme décimale.", d("1,75"),
               hints=["7 ÷ 4 = 1, reste 3. Continue après la virgule."],
               solution=["7 ÷ 4 = 1, reste 3. 30 ÷ 4 = 7, reste 2. 20 ÷ 4 = 5.", "7/4 = 1,75."], form="decimal"),
    ])

# ----- Section 2: dividing by a decimal number -----
S2 = Section(
    "diviseur_decimal", "Diviser par un nombre décimal", 24, "diviseur_decimal",
    "Diviser un nombre par un décimal en se ramenant à un diviseur entier, et expliquer pourquoi le quotient ne change pas.",
    [
        para("Combien de verres de 0,5 L peut-on remplir avec 6 L d'eau ? Il faut calculer " + N("6 \\div 0,5") + ". Comme un demi-litre est la moitié d'un litre, il y a 2 verres par litre, donc 12 verres. "
             "On va voir comment faire pour tous les nombres, sans deviner."),
        rule("On ne change pas un quotient en multipliant le dividende et le diviseur par le même nombre",
             "Si " + N("b \\times q = a") + ", alors " + N("(10 \\times b) \\times q = 10 \\times a") + ". Le quotient de " + N("10a") + " par " + N("10b") + " est donc le même que celui de " + N("a") + " par " + N("b")
             + ". On multiplie par 10, 100 ou 1 000 pour que le diviseur devienne un nombre entier, puis on divise."),
        example("Exemple 0", "Rappel : calculer " + N("756 \\div 18") + ".",
                "Quand le diviseur a deux chiffres, on estime chaque chiffre du quotient avec les premiers chiffres du dividende, puis on vérifie par une multiplication.",
                [("75 centaines et dizaines : combien de fois 18 dans 75 ?", "On regarde les deux premiers chiffres du dividende, 75. 18 × 4 = 72 est le plus grand multiple de 18 qui ne dépasse pas 75."),
                 ("On écrit 4 au quotient. 75 − 72 = 3", "Il reste 3 dizaines. On abaisse le chiffre suivant, 6 : on obtient 36."),
                 ("Combien de fois 18 dans 36 ? 18 × 2 = 36", "On écrit 2 au quotient. Le reste est 0."),
                 (N("756 \\div 18") + " = " + N("42"), "Vérification : 18 × 42 = 18 × 40 + 18 × 2 = 720 + 36 = 756.")],
                N("42"), "756/18==42 and 18*42==756"),
        example("Exemple 1", "Calculer " + N("7,5 \\div 0,25") + ".",
                "On multiplie le dividende et le diviseur par 100 pour que le diviseur soit entier.",
                [(N("7,5 \\times 100") + " = " + N("750"), "On multiplie le dividende par 100."),
                 (N("0,25 \\times 100") + " = " + N("25"), "On multiplie le diviseur par 100 : il devient entier."),
                 (N("7,5 \\div 0,25") + " = " + N("750 \\div 25") + " = " + N("30"), "25 × 30 = 750. Vérification : 0,25 × 30 = 7,5.")],
                N("30"), "d('7,5')/d('0,25')==30 and 750/25==30 and d('0,25')*30==d('7,5')"),
        example("Exemple 2", "Calculer " + N("4,68 \\div 0,6") + ".",
                "On multiplie par 10 : le diviseur 0,6 devient 6, et le dividende devient 46,8.",
                [(N("4,68 \\times 10") + " = " + N("46,8") + " et " + N("0,6 \\times 10") + " = " + N("6"), "On multiplie les deux nombres par 10."),
                 (N("46,8 \\div 6") + " = " + N("7,8"), "46 ÷ 6 = 7, reste 4 ; 48 ÷ 6 = 8. Donc 4,68 ÷ 0,6 = 7,8."),
                 ("Vérification : $0{,}6 \\times 7{,}8 = 4{,}68$", "6 × 78 = 468, avec 2 chiffres après la virgule.")],
                N("7,8"), "d('4,68')/d('0,6')==d('7,8') and d('0,6')*d('7,8')==d('4,68')"),
        example("Exemple 3", "Calculer " + N("9 \\div 1,5") + ".",
                "Le dividende est entier : on multiplie quand même par 10 pour rendre le diviseur entier.",
                [(N("9 \\times 10") + " = " + N("90") + " et " + N("1,5 \\times 10") + " = " + N("15"), "On multiplie les deux nombres par 10."),
                 (N("90 \\div 15") + " = " + N("6"), "15 × 6 = 90. Donc 9 ÷ 1,5 = 6.")],
                N("6"), "d('9')/d('1,5')==6"),
        example("Exemple 4", "Un bidon contient 12,5 L. On remplit des bouteilles de 0,25 L. Combien de bouteilles peut-on remplir ?",
                "Le nombre de bouteilles est le nombre de fois que 0,25 L entre dans 12,5 L : c'est une division.",
                [("Nombre de bouteilles = " + N("12,5 \\div 0,25"), "On cherche combien de fois 0,25 entre dans 12,5."),
                 (N("12,5 \\div 0,25") + " = " + N("1250 \\div 25") + " = " + N("50"), "On multiplie par 100 : 1 250 ÷ 25 = 50."),
                 ("Vérification : $50 \\times 0{,}25 = 12{,}5$", "50 × 25 = 1 250, avec 2 chiffres après la virgule.")],
                "On peut remplir 50 bouteilles.", "d('12,5')/d('0,25')==50"),
        warning("Diviser par un nombre plus petit que 1 donne un résultat plus grand : " + N("6 \\div 0,5 = 12") + ". Et on multiplie le dividende ET le diviseur par le même nombre, pas seulement le diviseur."),
    ],
    [
        number("s2-g1", "diviseur_decimal", "Calcule " + N("3,6 \\div 0,9") + ".", Fraction(4),
               hints=["Par quel nombre multiplier 3,6 et 0,9 pour que le diviseur soit entier ?"],
               solution=["On multiplie par 10 : 36 ÷ 9.", "36 ÷ 9 = 4."]),
        number("s2-g2", "diviseur_decimal", "Calcule " + N("5,4 \\div 0,06") + ".", Fraction(90),
               hints=["0,06 a deux chiffres après la virgule : par quel nombre faut-il multiplier ?"],
               solution=["On multiplie par 100 : 540 ÷ 6.", "540 ÷ 6 = 90. Vérification : 0,06 × 90 = 5,4."]),
        number("s2-g3", "diviseur_decimal", "Calcule " + N("2,45 \\div 0,5") + ".", d("4,9"),
               hints=["Multiplie par 10, puis divise un décimal par un entier."],
               solution=["On multiplie par 10 : 24,5 ÷ 5.", "24 ÷ 5 = 4, reste 4 ; 45 ÷ 5 = 9. Donc 4,9."], form="decimal"),
        choice("s2-g4", "diviseur_decimal", "Pour calculer " + N("8,4 \\div 0,12") + ", par quel nombre multiplie-t-on le dividende et le diviseur ?", [N("10"), N("100"), N("1000")], 1,
               hints=["Combien de chiffres après la virgule a le diviseur ?"],
               solution=["Le diviseur 0,12 a deux chiffres après la virgule : × 100 le rend entier (12).", "On calcule alors 840 ÷ 12 = 70."],
               wrong={0: "Avec 10, le diviseur 0,12 deviendrait 1,2 : il ne serait pas encore entier."}),
        number("s2-g5", "diviseur_decimal", "Un sac contient 4,5 kg de riz. On fait des sachets de 0,75 kg. Combien de sachets peut-on faire ?", Fraction(6),
               hints=["Combien de fois 0,75 kg entre-t-il dans 4,5 kg ?"],
               solution=["Nombre de sachets = 4,5 ÷ 0,75.", "On multiplie par 100 : 450 ÷ 75 = 6.", "On peut faire 6 sachets. Vérification : 6 × 0,75 = 4,5."]),
    ])

# ----- Section 3: dividing by 10, 100, 1000, 0.1, 0.01 -----
S3 = Section(
    "decalage_div", "Diviser par 10, 100, 1 000 et par 0,1, 0,01", 18, "decalage_div",
    "Diviser rapidement en décalant la virgule et convertir des mesures.",
    [
        para("Pour passer de 4 250 g à des kilogrammes, on divise par 1 000. Comme multiplier par 10, 100 ou 1 000, diviser par 10, 100 ou 1 000 se fait en déplaçant la virgule : c'est l'opération contraire."),
        rule("Diviser par 10, 100, 1 000",
             "Diviser par 10, c'est rendre chaque chiffre dix fois plus petit : il passe au rang juste à droite. La virgule se déplace d'un rang vers la gauche. Pour 100, de deux rangs, pour 1 000, de trois rangs. "
             "On ajoute des zéros devant si besoin. Diviser par 10 revient à multiplier par 0,1."),
        example("Exemple 1", "Calculer " + N("345 \\div 10") + " et " + N("7,2 \\div 100") + ".",
                "On déplace la virgule vers la gauche : d'un rang, puis de deux rangs.",
                [(N("345 \\div 10") + " = " + N("34,5"), "345 s'écrit 345,0. Un rang vers la gauche : 34,50 = 34,5."),
                 (N("7,2 \\div 100") + " = " + N("0,072"), "Deux rangs vers la gauche : 7,2 devient 0,072. Il faut ajouter des zéros devant.")],
                N("34,5") + " ; " + N("0,072"), "d('345')/10==d('34,5') and d('7,2')/100==d('0,072')"),
        rule("Diviser par 0,1, 0,01",
             "Il y a 10 dixièmes dans une unité : diviser par 0,1, c'est compter combien de dixièmes il y a, donc multiplier par 10. La virgule se déplace d'un rang vers la droite. "
             "Diviser par 0,01, c'est multiplier par 100 : la virgule se déplace de deux rangs vers la droite."),
        example("Exemple 2", "Calculer " + N("62,19 \\div 0,1") + " et " + N("3,8 \\div 0,01") + ".",
                "On déplace la virgule vers la droite : d'un rang, puis de deux rangs.",
                [(N("62,19 \\div 0,1") + " = " + N("621,9"), "Un rang vers la droite. On peut aussi multiplier par 10 le dividende et le diviseur : 621,9 ÷ 1."),
                 (N("3,8 \\div 0,01") + " = " + N("380"), "Deux rangs vers la droite : 3,8 devient 380 (on ajoute un zéro).")],
                N("621,9") + " ; " + N("380"), "d('62,19')/d('0,1')==d('621,9') and d('3,8')/d('0,01')==380"),
        example("Exemple 3", "Convertir " + N("4250") + " g en kilogrammes, puis " + N("2500") + " mL en litres.",
                "1 kg = 1 000 g et 1 L = 1 000 mL. Pour aller d'une petite unité à la grande, on divise par 1 000.",
                [(N("4250 \\div 1000") + " = " + N("4,25"), "Trois rangs vers la gauche : 4 250 g = 4,25 kg."),
                 (N("2500 \\div 1000") + " = " + N("2,5"), "2 500 mL = 2,5 L.")],
                "4 250 g = 4,25 kg et 2 500 mL = 2,5 L", "d('4250')/1000==d('4,25') and d('2500')/1000==d('2,5')"),
        example("Exemple 4", "Calculer " + N("0,35 \\div 0,01") + " et " + N("45 \\div 0,001") + ".",
                "Diviser par 0,01 revient à multiplier par 100, et diviser par 0,001 à multiplier par 1 000 : la virgule se décale vers la droite.",
                [(N("0,35 \\div 0,01") + " = " + N("35"), "Deux rangs vers la droite : 0,35 devient 35."),
                 (N("45 \\div 0,001") + " = " + N("45000"), "Trois rangs vers la droite : on ajoute trois zéros à 45.")],
                N("35") + " et " + N("45000"), "d('0,35')/d('0,01')==35 and 45/d('0,001')==45000"),
        warning("Diviser par 0,1 agrandit : " + N("8 \\div 0,1 = 80") + " et non 0,8. Et diviser par 10 rend dix fois plus petit : " + N("8 \\div 10 = 0,8") + "."),
    ],
    [
        number("s3-g1", "decalage_div", "Calcule " + N("83 \\div 10") + ".", d("8,3"),
               hints=["Dans quel sens se déplace la virgule quand on divise par 10 ?"], solution=["83 s'écrit 83,0. Un rang vers la gauche : 8,3."]),
        number("s3-g2", "decalage_div", "Calcule " + N("5,6 \\div 100") + ".", d("0,056"),
               hints=["Deux rangs vers la gauche : faut-il ajouter des zéros devant ?"], solution=["5,6 : deux rangs vers la gauche donne 0,056."]),
        number("s3-g3", "decalage_div", "Calcule " + N("4,7 \\div 0,1") + ".", Fraction(47),
               hints=["Il y a combien de dixièmes dans une unité ?"], solution=["Diviser par 0,1, c'est multiplier par 10.", "4,7 × 10 = 47."]),
        number("s3-g4", "decalage_div", "Calcule " + N("0,35 \\div 0,01") + ".", Fraction(35),
               hints=["Diviser par 0,01, c'est multiplier par combien ?"], solution=["Diviser par 0,01, c'est multiplier par 100.", "0,35 × 100 = 35."]),
        number("s3-g5", "decalage_div", "Convertis " + N("3750") + " m en kilomètres.", d("3,75"), units=["km"],
               hints=["1 km = 1 000 m. Faut-il diviser ou multiplier par 1 000 ?"], solution=["Pour passer des mètres aux kilomètres, on divise par 1 000.", "3 750 ÷ 1 000 = 3,75 : 3 750 m = 3,75 km."]),
    ])

# ----- Section 4: approximate quotients -----
S4 = Section(
    "approche", "Les quotients approchés", 24, "approche",
    "Donner un quotient approché par défaut, par excès ou arrondi quand la division ne se termine pas.",
    [
        para("Partageons 10 F entre 3 personnes : chacune reçoit 3 F, il reste 1 F ; en continuant, " + N("10 \\div 3") + " = 3,333... et les 3 ne s'arrêtent jamais. On ne peut pas écrire ce quotient exactement avec un nombre fini de chiffres. "
             "On donne alors une valeur proche, avec une précision choisie."),
        definition("Quotient approché par défaut et par excès",
                   "Le quotient approché par défaut à 0,1 près de " + N("a \\div b") + " est le plus grand nombre à un chiffre après la virgule qui n'est pas plus grand que le quotient. Le quotient approché par excès est le plus petit nombre à un chiffre après la virgule qui n'est pas plus petit que le quotient. "
                   "Quand la division ne se termine pas, c'est le nombre suivant, 0,1 de plus : on a un encadrement du quotient entre deux nombres consécutifs, et l'écart entre le quotient et chacun d'eux est inférieur à 0,1. Si le quotient s'arrête avant (par exemple 2,5), il est lui-même sa valeur approchée par défaut et par excès. "
                   "On définit de même l'approximation à l'unité près, à 0,01 près, à 0,001 près."),
        rule("Trouver un quotient approché",
             "On pose la division et on s'arrête au rang demandé : le nombre obtenu est le quotient approché par défaut. On y ajoute une unité de ce rang pour avoir le quotient approché par excès. "
             "L'arrondi est celui des deux qui est le plus proche du quotient : on regarde le chiffre suivant (0 à 4 : par défaut, 5 à 9 : par excès)."),
        example("Exemple 1", "Donner les quotients approchés de " + N("10 \\div 3") + " à 0,1 près.",
                "On pose la division jusqu'au chiffre des dixièmes.",
                [("10 ÷ 3 = 3, reste 1", "3 × 3 = 9 et 10 − 9 = 1."),
                 ("1 unité = 10 dixièmes, 10 ÷ 3 = 3, reste 1", "On écrit la virgule puis 3 : le quotient approché par défaut est 3,3."),
                 ("Par excès : 3,3 + 0,1 = 3,4", "Vérification : 3 × 3,3 = 9,9 qui est plus petit que 10, et 3 × 3,4 = 10,2 qui est plus grand que 10."),
                 (N("3,3 < 10 \\div 3 < 3,4"), "Le chiffre suivant est 3 (plus petit que 5) : l'arrondi au dixième est le quotient par défaut, 3,3.")],
                "par défaut " + N("3,3") + ", par excès " + N("3,4"), "d('3,3')*3<10<d('3,4')*3"),
        example("Exemple 2", "Donner le quotient approché par défaut et par excès de " + N("20 \\div 7") + " à 0,01 près, puis l'arrondi.",
                "On pose la division jusqu'au chiffre des centièmes, puis on compare les deux approximations avec le vrai quotient.",
                [("20 ÷ 7 = 2, reste 6", "7 × 2 = 14 et 20 − 14 = 6."),
                 ("60 ÷ 7 = 8, reste 4 ; 40 ÷ 7 = 5, reste 5", "Après la virgule : 8 puis 5. Le quotient approché par défaut est 2,85."),
                 ("Par excès : 2,85 + 0,01 = 2,86", "Vérification : 7 × 2,85 = 19,95 (moins de 20) et 7 × 2,86 = 20,02 (plus de 20)."),
                 ("L'écart avec 20 : 20 − 19,95 = 0,05 et 20,02 − 20 = 0,02", "20,02 est plus proche de 20 : le quotient est plus proche de 2,86. L'arrondi au centième est donc 2,86.")],
                "par défaut " + N("2,85") + ", par excès " + N("2,86") + ", arrondi " + N("2,86"),
                "d('2,85')*7<20<d('2,86')*7 and d('20')-d('2,85')*7==d('0,05') and d('2,86')*7-20==d('0,02')"),
        example("Exemple 3", "Donner le quotient approché de " + N("47 \\div 6") + " à l'unité près, par défaut et par excès.",
                "À l'unité près, on s'arrête avant la virgule : c'est le quotient entier de la division euclidienne.",
                [("47 = 7 × 6 + 5", "7 × 6 = 42 et 47 − 42 = 5. Le quotient entier est 7."),
                 ("Par défaut : 7. Par excès : 7 + 1 = 8", "Vérification : 6 × 7 = 42 est plus petit que 47, et 6 × 8 = 48 est plus grand."),
                 (N("7 < 47 \\div 6 < 8"), "Le quotient exact est un peu plus de 7,8 : l'arrondi à l'unité est 8.")],
                "par défaut " + N("7") + ", par excès " + N("8"), "6*7<47<6*8"),
        example("Exemple 4", "Un fil de 100 m est coupé en 7 morceaux égaux. Quelle est la longueur d'un morceau, au centimètre (0,01 m) près par défaut ?",
                "On cherche le quotient approché par défaut à 0,01 près de 100 ÷ 7.",
                [("100 ÷ 7 = 14, reste 2", "7 × 14 = 98 et 100 − 98 = 2."),
                 ("20 ÷ 7 = 2, reste 6 ; 60 ÷ 7 = 8, reste 4", "Après la virgule : 2 puis 8. Le quotient approché par défaut est 14,28."),
                 ("Vérification : 7 × 14,28 = 99,96 et 7 × 14,29 = 100,03", "Le vrai quotient est entre 14,28 et 14,29.")],
                "Un morceau mesure " + N("14,28") + " m (par défaut).", "d('14,28')*7<100<d('14,29')*7"),
        example("Exemple 5", "Donner les quotients approchés de " + N("5,3 \\div 0,9") + " à 0,1 près.",
                "On commence par rendre le diviseur entier en multipliant par 10, puis on approche le quotient.",
                [(N("5,3 \\div 0,9") + " = " + N("53 \\div 9"), "On multiplie le dividende et le diviseur par 10."),
                 ("53 ÷ 9 = 5, reste 8 ; 80 ÷ 9 = 8, reste 8 ; 80 ÷ 9 = 8...", "Le quotient est 5,888... : il ne se termine pas."),
                 ("Par défaut : 5,8. Par excès : 5,8 + 0,1 = 5,9", "Vérification : 9 × 5,8 = 52,2 est plus petit que 53, et 9 × 5,9 = 53,1 est plus grand."),
                 ("Le chiffre suivant est 8 (au moins 5) : l'arrondi au dixième est le quotient par excès, 5,9.", N("5,8 < 5,3 \\div 0,9 < 5,9"))],
                "par défaut " + N("5,8") + ", par excès " + N("5,9") + ", arrondi " + N("5,9"), "d('5,8')*9<53<d('5,9')*9 and d('5,3')/d('0,9')>d('5,8')"),
        warning("Un quotient approché n'est pas le quotient exact : " + N("3,3 \\times 3 = 9,9") + " et non 10. Dis toujours « par défaut », « par excès » ou « arrondi », et à quelle précision."),
    ],
    [
        number("s4-g1", "approche", "Donne le quotient approché par défaut à l'unité près de " + N("29 \\div 4") + ".", Fraction(7),
               hints=["Combien de fois 4 entre-t-il entièrement dans 29 ?"], solution=["4 × 7 = 28 est plus petit que 29, et 4 × 8 = 32 est plus grand.", "Le quotient par défaut à l'unité près est 7."]),
        number("s4-g2", "approche", "Donne le quotient approché par excès à 0,1 près de " + N("5 \\div 3") + ".", d("1,7"),
               hints=["Trouve d'abord le quotient par défaut au dixième, puis ajoute 0,1."], solution=["5 ÷ 3 = 1,666... Par défaut à 0,1 près : 1,6.", "Par excès : 1,6 + 0,1 = 1,7. Vérification : 3 × 1,6 = 4,8 < 5 < 3 × 1,7 = 5,1."], form="decimal"),
        number("s4-g3", "approche", "Donne le quotient approché par défaut à 0,01 près de " + N("2 \\div 7") + ".", d("0,28"),
               hints=["Pose la division de 2 par 7 et arrête-toi au chiffre des centièmes."], solution=["2 ÷ 7 : 0, puis 20 ÷ 7 = 2 reste 6, puis 60 ÷ 7 = 8 reste 4.", "Par défaut à 0,01 près : 0,28. Vérification : 7 × 0,28 = 1,96 < 2 < 7 × 0,29 = 2,03."], form="decimal"),
        number("s4-g4", "approche", "Donne l'arrondi au dixième de " + N("22 \\div 7") + ".", d("3,1"),
               hints=["Calcule les deux approximations à 0,1 près, puis choisis la plus proche du quotient.", "22 ÷ 7 = 3,142..."],
               solution=["22 ÷ 7 = 3, reste 1 ; 10 ÷ 7 = 1 reste 3 ; 30 ÷ 7 = 4 reste 2 : 22 ÷ 7 = 3,14...", "Par défaut : 3,1 ; par excès : 3,2. Le chiffre suivant est 4 (plus petit que 5) : l'arrondi est 3,1."], form="decimal"),
        choice("s4-g5", "approche", "On sait que " + N("2,3 < 7 \\div 3 < 2,4") + ". Quel est le quotient approché par excès à 0,1 près ?", [N("2,3"), N("2,4"), N("2,33")], 1,
               hints=["Le quotient par excès est le plus grand des deux nombres de l'encadrement."], solution=["Le quotient par défaut est le plus petit, 2,3, et le quotient par excès est le plus grand, 2,4."],
               wrong={0: "2,3 est le quotient approché par défaut. Par excès, c'est le nombre de l'encadrement qui est plus grand que le quotient."}),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "quotient", "Calcule " + N("18 \\div 8") + ".", d("2,25"), 1, ["18 = 2 × 8 + 2. Continue après la virgule."], ["18 ÷ 8 = 2, reste 2. 20 ÷ 8 = 2, reste 4. 40 ÷ 8 = 5.", "18 ÷ 8 = 2,25. Vérification : 8 × 2,25 = 18."], form="decimal"),
    number("p2", "quotient", "Calcule " + N("6,3 \\div 5") + ".", d("1,26"), 1, ["6 ÷ 5 = 1, reste 1. Que fait-on ensuite ?"], ["6 ÷ 5 = 1, reste 1. On abaisse le 3 : 13 ÷ 5 = 2, reste 3. 30 ÷ 5 = 6.", "6,3 ÷ 5 = 1,26."]),
    number("p3", "quotient", "Calcule " + N("0,9 \\div 4") + ".", d("0,225"), 2, ["9 dixièmes ÷ 4 = 2 dixièmes, reste 1 dixième. Continue."], ["0,9 ÷ 4 : 9 ÷ 4 = 2 reste 1 ; 10 ÷ 4 = 2 reste 2 ; 20 ÷ 4 = 5.", "0,9 ÷ 4 = 0,225."]),
    number("p4", "quotient", "Calcule " + N("21 \\div 4") + ".", d("5,25"), 1, ["21 = 5 × 4 + 1."], ["21 ÷ 4 = 5 reste 1. 10 ÷ 4 = 2 reste 2. 20 ÷ 4 = 5.", "21 ÷ 4 = 5,25."]),
    number("p5", "quotient", "Écris " + N("5/8") + " sous forme décimale.", d("0,625"), 2, ["Une fraction est un quotient : calcule 5 ÷ 8."], ["50 ÷ 8 = 6 reste 2 ; 20 ÷ 8 = 2 reste 4 ; 40 ÷ 8 = 5.", "5/8 = 0,625."], form="decimal"),
    number("p6", "quotient", "Calcule " + N("7,35 \\div 7") + ".", d("1,05"), 2, ["Attention au zéro : 7 ÷ 7 = 1, puis 3 ÷ 7 = 0."], ["7 ÷ 7 = 1. On abaisse le 3 : 3 ÷ 7 = 0, on écrit la virgule puis 0. On abaisse le 5 : 35 ÷ 7 = 5.", "7,35 ÷ 7 = 1,05. Vérification : 7 × 1,05 = 7,35."]),
    number("p7", "problemes", "Un ruban de 10,5 m est coupé en 6 morceaux égaux. Quelle est la longueur d'un morceau, en mètres ?", d("1,75"), 2, ["Une longueur partagée en parties égales : quelle opération ?"],
           ["Longueur d'un morceau = 10,5 ÷ 6.", "10 ÷ 6 = 1 reste 4 ; 45 ÷ 6 = 7 reste 3 ; 30 ÷ 6 = 5. Donc 1,75 m.", "Vérification : 6 × 1,75 = 10,5."], units=["m"]),
    number("p8", "problemes", "Huit amis se partagent une facture de 3 750 F à parts égales. Combien paie chacun, en F ?", d("468,75"), 3, ["Partage 3 750 par 8 en continuant après la virgule."],
           ["3 750 ÷ 8 = 468, reste 6 ; 60 ÷ 8 = 7 reste 4 ; 40 ÷ 8 = 5.", "Chacun paie 468,75 F. Vérification : 8 × 468,75 = 3 750."], units=["F"]),
    choice("p9", "quotient", "Awa a calculé " + N("3 \\div 4 = 1,33") + ". Quelle est son erreur ?", ["Elle a divisé 4 par 3 au lieu de 3 par 4", "Elle a oublié de placer la virgule", "Elle a multiplié au lieu de diviser"], 0, 3,
           ["Estime le résultat : 3 ÷ 4, est-ce plus grand ou plus petit que 1 ?"], ["3 est plus petit que 4 : 3 ÷ 4 est plus petit que 1, et Awa trouve 1,33.", "Elle a calculé 4 ÷ 3 = 1,33... Le bon calcul : 3 ÷ 4 = 0,75."]),
    choice("p10", "quotient", "Peut-on calculer " + N("5 \\div 0") + " ?", ["Oui, le résultat est 0", "Oui, le résultat est 5", "Non, on ne peut pas diviser par 0"], 2, 1,
           ["Cherche un nombre q tel que 0 × q = 5."], ["Quel que soit q, 0 × q = 0 et jamais 5.", "On ne peut pas diviser par 0."],
           wrong={0: "Si 5 ÷ 0 = 0, alors 0 × 0 devrait faire 5, ce qui est faux.", 1: "Si 5 ÷ 0 = 5, alors 0 × 5 devrait faire 5, ce qui est faux."}),
    number("p11", "diviseur_decimal", "Calcule " + N("4,8 \\div 0,6") + ".", Fraction(8), 1, ["Multiplie par 10 le dividende et le diviseur."], ["48 ÷ 6 = 8."]),
    number("p12", "diviseur_decimal", "Calcule " + N("0,72 \\div 0,08") + ".", Fraction(9), 2, ["Multiplie par 100."], ["72 ÷ 8 = 9."]),
    number("p13", "diviseur_decimal", "Calcule " + N("9 \\div 0,25") + ".", Fraction(36), 2, ["Multiplie par 100."], ["900 ÷ 25 = 36. Vérification : 0,25 × 36 = 9."]),
    number("p14", "diviseur_decimal", "Calcule " + N("15,6 \\div 1,2") + ".", Fraction(13), 2, ["Multiplie par 10."], ["156 ÷ 12 = 13. Vérification : 1,2 × 13 = 15,6."]),
    number("p15", "diviseur_decimal", "Calcule " + N("7,2 \\div 0,45") + ".", Fraction(16), 3, ["Multiplie par 100 le dividende et le diviseur."], ["720 ÷ 45 = 16. Vérification : 0,45 × 16 = 7,2."]),
    choice("p16", "diviseur_decimal", "Combien vaut " + N("6 \\div 0,5") + " ?", [N("3"), N("12"), N("0,3")], 1, 2, ["Combien de demi-litres dans 6 litres ?"], ["On multiplie par 10 : 60 ÷ 5 = 12."],
           wrong={0: "3 est la moitié de 6 : tu as divisé par 2. Diviser par 0,5 donne un nombre plus grand que 6.", 2: "0,3 est trop petit : 6 contient beaucoup de fois 0,5."}),
    number("p17", "problemes", "On remplit des verres de 0,25 L avec 7,5 L de jus. Combien de verres peut-on remplir ?", Fraction(30), 2, ["Combien de fois 0,25 entre-t-il dans 7,5 ?"], ["7,5 ÷ 0,25 = 750 ÷ 25 = 30 verres."]),
    number("p18", "problemes", "Un fil de 3,6 m est coupé en morceaux de 0,15 m. Combien de morceaux obtient-on ?", Fraction(24), 3, ["Multiplie par 100 le dividende et le diviseur."], ["3,6 ÷ 0,15 = 360 ÷ 15 = 24 morceaux.", "Vérification : 24 × 0,15 = 3,6."]),
    number("p19", "decalage_div", "Calcule " + N("460 \\div 10") + ".", Fraction(46), 1, ["Un rang vers la gauche."], ["460 ÷ 10 = 46."]),
    number("p20", "decalage_div", "Calcule " + N("9,6 \\div 100") + ".", d("0,096"), 2, ["Deux rangs vers la gauche, avec des zéros devant."], ["9,6 ÷ 100 = 0,096."]),
    number("p21", "decalage_div", "Calcule " + N("53 \\div 1000") + ".", d("0,053"), 2, ["Trois rangs vers la gauche."], ["53 ÷ 1 000 = 0,053."]),
    number("p22", "decalage_div", "Calcule " + N("8,6 \\div 0,1") + ".", Fraction(86), 1, ["Diviser par 0,1 revient à multiplier par ?"], ["8,6 ÷ 0,1 = 8,6 × 10 = 86."]),
    number("p23", "decalage_div", "Calcule " + N("0,75 \\div 0,01") + ".", Fraction(75), 2, ["Diviser par 0,01 revient à multiplier par ?"], ["0,75 ÷ 0,01 = 0,75 × 100 = 75."]),
    number("p24", "decalage_div", "Convertis " + N("3600") + " g en kilogrammes.", d("3,6"), 1, ["1 kg = 1 000 g."], ["3 600 ÷ 1 000 = 3,6 kg."], units=["kg"]),
    number("p25", "decalage_div", "Convertis " + N("1750") + " mL en litres.", d("1,75"), 1, ["1 L = 1 000 mL."], ["1 750 ÷ 1 000 = 1,75 L."], units=["L"]),
    choice("p26", "decalage_div", "Diviser par 0,1 revient à multiplier par :", [N("10"), N("0,1"), N("100")], 0, 2, ["Combien de dixièmes dans une unité ?"], ["Il y a 10 dixièmes dans 1 unité : diviser par 0,1 donne un nombre 10 fois plus grand."],
           wrong={1: "Multiplier par 0,1 donnerait un nombre plus petit. Diviser par 0,1 donne un nombre plus grand."}),
    number("p27", "approche", "Donne le quotient approché par défaut à l'unité près de " + N("38 \\div 7") + ".", Fraction(5), 1, ["7 × 5 = 35 et 7 × 6 = 42."], ["Le quotient par défaut à l'unité près est 5."]),
    number("p28", "approche", "Donne le quotient approché par excès à l'unité près de " + N("38 \\div 7") + ".", Fraction(6), 1, ["C'est le quotient par défaut plus 1."], ["Par excès : 5 + 1 = 6."]),
    number("p29", "approche", "Donne le quotient approché par défaut à 0,1 près de " + N("14 \\div 3") + ".", d("4,6"), 2, ["Pose la division jusqu'aux dixièmes."], ["14 ÷ 3 = 4,666... Par défaut à 0,1 près : 4,6."], form="decimal"),
    number("p30", "approche", "Donne le quotient approché par excès à 0,01 près de " + N("30 \\div 7") + ".", d("4,29"), 2, ["Trouve d'abord le quotient par défaut à 0,01 près."], ["30 ÷ 7 = 4,285... Par défaut : 4,28 ; par excès : 4,29."], form="decimal"),
    number("p31", "approche", "Donne l'arrondi au dixième de " + N("17 \\div 6") + ".", d("2,8"), 2, ["17 ÷ 6 = 2,8333..."], ["Par défaut 2,8 et par excès 2,9. Le chiffre suivant est 3, l'arrondi est 2,8."], form="decimal"),
    number("p32", "approche", "Donne le quotient approché par défaut à 0,01 près de " + N("1 \\div 6") + ".", d("0,16"), 3, ["1 ÷ 6 = 0,1666..."], ["10 ÷ 6 = 1 reste 4 ; 40 ÷ 6 = 6 reste 4. Par défaut à 0,01 près : 0,16."], form="decimal"),
    number("p33", "problemes", "On verse 50 L d'eau dans 7 bidons identiques. Quelle quantité par bidon, au centilitre (0,01 L) près par défaut, en L ?", d("7,14"), 3, ["Calcule 50 ÷ 7 jusqu'aux centièmes."],
           ["50 ÷ 7 = 7 reste 1 ; 10 ÷ 7 = 1 reste 3 ; 30 ÷ 7 = 4 reste 2.", "Par défaut à 0,01 près : 7,14 L."], units=["L"], form="decimal"),
    choice("p34", "approche", "Le quotient approché par défaut à 0,01 près de " + N("5 \\div 6") + " est :", [N("0,83"), N("0,84"), N("0,8")], 0, 3, ["5 ÷ 6 = 0,8333... Quel est le plus grand nombre à deux chiffres après la virgule qui n'est pas au-dessus ?"],
           ["50 ÷ 6 = 8 reste 2 ; 20 ÷ 6 = 3 reste 2 ; 5 ÷ 6 = 0,83...", "Par défaut à 0,01 près : 0,83."],
           wrong={1: "0,84 est le quotient par excès. 6 × 0,84 = 5,04 est plus grand que 5.", 2: "0,8 est une approximation à 0,1 près, pas à 0,01 près."}),
    number("p35", "approche", "Donne le quotient approché par défaut à 0,1 près de " + N("4,7 \\div 0,9") + ".", d("5,2"), 3, ["Multiplie par 10 le dividende et le diviseur, puis approche 47 ÷ 9."], ["4,7 ÷ 0,9 = 47 ÷ 9 = 5,222...", "Par défaut à 0,1 près : 5,2."], form="decimal"),
    number("p36", "problemes", "Un fil de 14,4 m est coupé en morceaux de 0,6 m. Chaque morceau est vendu 250 F. Combien rapporte la vente de tous les morceaux, en F ?", Fraction(6000), 3, ["Combien de morceaux ? Puis le prix total."],
           ["Nombre de morceaux = 14,4 ÷ 0,6 = 144 ÷ 6 = 24.", "24 × 250 = 6 000 F."], units=["F"]),
    number("p37", "problemes", "Un robinet débite 4,5 L par minute. Combien de minutes faut-il pour remplir un réservoir de 63 L ?", Fraction(14), 3, ["Combien de fois 4,5 L entre-t-il dans 63 L ?"], ["63 ÷ 4,5 = 630 ÷ 45 = 14 minutes.", "Vérification : 14 × 4,5 = 63."]),
]

SUMMARY = [
    definition("Quotient", "Diviser " + N("a") + " par " + N("b") + " (différent de 0), c'est trouver le nombre " + N("q") + " tel que " + N("b \\times q = a") + ". On vérifie en multipliant le quotient par le diviseur. Une fraction " + "$\\dfrac{a}{b}$" + " est le quotient " + N("a \\div b") + "."),
    rule("Diviser par un décimal", "On ne change pas un quotient en multipliant le dividende et le diviseur par le même nombre (10, 100...). On rend ainsi le diviseur entier, puis on divise."),
    rule("Diviser par 10, 100, 1 000, 0,1, 0,01", "Diviser par 10, 100, 1 000 : la virgule se déplace de 1, 2, 3 rangs vers la gauche. Diviser par 0,1 ou 0,01, c'est multiplier par 10 ou par 100 : la virgule se déplace vers la droite."),
    rule("Quotient approché", "Quand la division ne se termine pas, on donne un quotient approché à une précision choisie : par défaut (on s'arrête au rang demandé), par excès (on ajoute une unité de ce rang) ou arrondi (le plus proche des deux)."),
    para("Les erreurs à éviter : diviser par 0 ; inverser dividende et diviseur ; multiplier seulement le diviseur par 10 ; croire qu'une division rend toujours plus petit ; confondre quotient par défaut et quotient par excès."),
]

CONCEPTS = {
    "quotient": ("Le quotient et les fractions", "quotient"),
    "diviseur_decimal": ("Diviser par un décimal", "diviseur_decimal"),
    "decalage_div": ("Diviser par 10, 100, 0,1, 0,01", "decalage_div"),
    "approche": ("Quotients approchés", "approche"),
    "problemes": ("Résoudre un problème", "diviseur_decimal"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []

    # 1. exact quotient of two whole numbers
    k = rng.choice([2, 4, 5, 8])
    n = rng.randint(3, 99)
    if n % k == 0:
        n += 1
    questions.append(number("a1", "quotient", "Calcule " + N(f"{n} \\div {k}") + ".", Fraction(n, k), 1, ["Continue la division après la virgule."],
                            [f"{n} ÷ {k} : quotient entier {n // k}, reste {n % k}.", f"On continue après la virgule : {show(Fraction(n, k))}.", f"Vérification : {k} × {show(Fraction(n, k))} = {n}."], form="decimal"))

    # 2. a decimal divided by a whole number
    divisor = rng.randint(2, 9)
    q = rand_decimal(rng, 1, 9, 2)
    dividend = q * divisor
    questions.append(number("a2", "quotient", "Calcule " + N(f"{show(dividend)} \\div {divisor}") + ".", q, 2, ["Divise comme pour un entier et place la virgule au bon moment."],
                            [f"{show(dividend)} ÷ {divisor} = {show(q)}.", f"Vérification : {show(q)} × {divisor} = {show(dividend)}."]))

    # 3. a fraction as a decimal
    b = rng.choice([4, 5, 8, 20, 25])
    a = rng.randint(1, 3 * b)
    if a % b == 0:
        a += 1
    questions.append(number("a3", "quotient", "Écris " + N(f"{a}/{b}") + " sous forme décimale.", Fraction(a, b), 2, ["Une fraction est un quotient : divise le numérateur par le dénominateur."],
                            [f"{a}/{b} = {a} ÷ {b} = {show(Fraction(a, b))}.", f"Vérification : {b} × {show(Fraction(a, b))} = {a}."], form="decimal"))

    # 4. sharing problem
    people = rng.choice([4, 5, 8])
    total = rand_decimal(rng, 20, 90, 1) * 5
    questions.append(number("a4", "problemes", f"On partage {show(total)} m de corde entre {people} personnes, à parts égales. Quelle longueur reçoit chacune, en mètres ?", total / people, 3,
                            ["Un partage en parts égales est une division."],
                            [f"Longueur par personne = {show(total)} ÷ {people} = {show(total / people)} m.", f"Vérification : {people} × {show(total / people)} = {show(total)}."], units=["m"]))

    # 5. a decimal divisor with a whole quotient
    divisor = rng.choice([Fraction(2, 10), Fraction(4, 10), Fraction(5, 10), Fraction(6, 10), Fraction(25, 100), Fraction(5, 100), Fraction(15, 100)])
    q = rng.randint(3, 40)
    scale = 10 ** len(show(divisor).split(",")[1])
    questions.append(number("a5", "diviseur_decimal", "Calcule " + N(f"{show(divisor * q)} \\div {show(divisor)}") + ".", Fraction(q), 2,
                            ["Multiplie le dividende et le diviseur par 10 ou 100 pour que le diviseur soit entier."],
                            [f"On multiplie par {scale} : {show(divisor * q * scale)} ÷ {int(divisor * scale)}.", f"{show(divisor * q)} ÷ {show(divisor)} = {q}.", f"Vérification : {show(divisor)} × {q} = {show(divisor * q)}."]))

    # 6. a decimal divisor with a decimal quotient
    divisor = rng.choice([Fraction(4, 10), Fraction(6, 10), Fraction(8, 10), Fraction(12, 10), Fraction(15, 10)])
    q = rand_decimal(rng, 1, 9, 1)
    questions.append(number("a6", "diviseur_decimal", "Calcule " + N(f"{show(divisor * q)} \\div {show(divisor)}") + ".", q, 3,
                            ["Multiplie le dividende et le diviseur par 10."],
                            [f"On multiplie par 10 : {show(divisor * q * 10)} ÷ {int(divisor * 10)}.", f"{show(divisor * q)} ÷ {show(divisor)} = {show(q)}.", f"Vérification : {show(divisor)} × {show(q)} = {show(divisor * q)}."]))

    # 7. divide by a power of ten
    power = rng.choice([10, 100, 1000])
    x = rand_decimal(rng, 1, 999, rng.choice([1, 2]))
    questions.append(number("a7", "decalage_div", "Calcule " + N(f"{show(x)} \\div {power}") + ".", x / power, 1, ["Dans quel sens se déplace la virgule ? De combien de rangs ?"],
                            [f"Diviser par {power}, c'est déplacer la virgule de {len(str(power)) - 1} rang{'s' if power > 10 else ''} vers la gauche.", f"{show(x)} ÷ {power} = {show(x / power)}."]))

    # 8. divide by 0.1 or 0.01
    small = rng.choice([Fraction(1, 10), Fraction(1, 100)])
    x = rand_decimal(rng, 1, 99, rng.choice([1, 2]))
    questions.append(number("a8", "decalage_div", "Calcule " + N(f"{show(x)} \\div {show(small)}") + ".", x / small, 2, ["Diviser par 0,1, c'est multiplier par 10 ; par 0,01, par 100."],
                            [f"Diviser par {show(small)}, c'est multiplier par {10 if small == Fraction(1, 10) else 100}.", f"{show(x)} × {10 if small == Fraction(1, 10) else 100} = {show(x / small)}."]))

    # 9. approximation by default
    b = rng.choice([3, 6, 7, 9, 11])
    a = rng.randint(2, 60)
    while terminates(Fraction(a, b)):
        a += 1
    places = rng.choice([0, 1, 2])
    precision = {0: "à l'unité près", 1: "à 0,1 près", 2: "à 0,01 près"}[places]
    questions.append(number("a9", "approche", "Donne le quotient approché par défaut " + precision + " de " + N(f"{a} \\div {b}") + ".", below(Fraction(a, b), places), 2,
                            ["Pose la division et arrête-toi au rang demandé, sans arrondir."],
                            [f"{a} ÷ {b} = {digits(Fraction(a, b), 4)}", f"Par défaut {precision} : {show(below(Fraction(a, b), places))}."], form="decimal"))

    # 10. approximation by excess
    b = rng.choice([3, 6, 7, 9, 11])
    a = rng.randint(2, 60)
    while terminates(Fraction(a, b)):
        a += 1
    places = rng.choice([1, 2])
    precision = {1: "à 0,1 près", 2: "à 0,01 près"}[places]
    low = below(Fraction(a, b), places)
    questions.append(number("a10", "approche", "Donne le quotient approché par excès " + precision + " de " + N(f"{a} \\div {b}") + ".", low + Fraction(1, 10**places), 3,
                            ["Trouve d'abord le quotient par défaut, puis ajoute une unité du dernier rang."],
                            [f"Par défaut {precision} : {show(low)}.", f"Par excès : {show(low)} + {show(Fraction(1, 10 ** places))} = {show(low + Fraction(1, 10 ** places))}."], form="decimal"))

    # 11. the rounded value
    b = rng.choice([3, 6, 7, 9, 11])
    a = rng.randint(2, 60)
    while terminates(Fraction(a, b)):
        a += 1
    places = rng.choice([1, 2])
    precision = {1: "au dixième", 2: "au centième"}[places]
    near = nearest(Fraction(a, b), places)
    questions.append(number("a11", "approche", "Donne l'arrondi " + precision + " de " + N(f"{a} \\div {b}") + ".", near, 3,
                            ["Calcule les quotients par défaut et par excès, puis choisis celui qui est le plus proche."],
                            [f"Par défaut : {show(below(Fraction(a, b), places))} ; par excès : {show(below(Fraction(a, b), places) + Fraction(1, 10 ** places))}.", f"Le plus proche de {a} ÷ {b} est {show(near)}."], form="decimal"))

    # 12. dividing does not always make smaller
    whole, f = rng.randint(2, 20), rng.choice([Fraction(5, 10), Fraction(2, 10), Fraction(25, 100), Fraction(4, 10), Fraction(1, 10)])
    claim = N(f"{whole} \\div {show(f)}")
    options = ["Il a raison : diviser rend toujours plus petit", f"Il a tort : {show(f)} est plus petit que 1, donc le quotient est plus grand que {whole}", "Il a tort : on ne peut pas diviser par un nombre à virgule"]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a12", "diviseur_decimal", f"Moussa dit : « {claim} est plus petit que {whole} parce qu'on divise ». Quelle est la bonne réponse ?",
                            [options[i] for i in order], order.index(1), 3, ["Calcule le quotient et compare-le avec " + str(whole) + "."],
                            [f"{whole} ÷ {show(f)} = {show(whole / f)}.", f"{show(whole / f)} est plus grand que {whole} : diviser par un nombre plus petit que 1 rend plus grand."],
                            wrong={order.index(0): "Diviser ne rend pas toujours plus petit : diviser par un nombre plus petit que 1 rend plus grand.",
                                   order.index(2): "On peut diviser par un nombre décimal : on multiplie le dividende et le diviseur pour rendre le diviseur entier."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=3, title="Diviser des nombres décimaux", language="fr",
    intro="Partager 12 m de ruban en 8 morceaux, remplir des bouteilles de 0,25 L, convertir des grammes en kilogrammes : ces situations demandent une division. "
          "Ce chapitre t'apprend à diviser avec des nombres décimaux, à vérifier tes résultats, à diviser par un décimal, et à donner une valeur approchée quand la division ne se termine pas.",
    objectives=["Effectuer une division dont le quotient est un nombre décimal, la vérifier, et écrire une fraction sous forme décimale.",
                "Diviser par un nombre décimal en se ramenant à un diviseur entier.",
                "Diviser par 10, 100, 1 000, 0,1 et 0,01 en déplaçant la virgule, et convertir des mesures.",
                "Donner un quotient approché par défaut, par excès ou arrondi quand la division ne se termine pas.",
                "Résoudre des problèmes de partage et de contenance."],
    prerequisites=[{"text": "Avoir terminé le chapitre sur la multiplication des nombres décimaux : multiplier, décaler la virgule.", "chapter": "sn-6e-multiplication"},
                   {"text": "Connaître la division des nombres entiers : quotient et reste."}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E],
    status_note="Third chapter of the Senegal Sixième course. Its topics follow the division chapter of the ADEM-Dakar booklet, with our own explanations and exercises. It has not been checked against the official Senegalese programme.",
)
