"""Sixième, Multiplier des nombres décimaux: the second chapter of the Senegal Sixième course, written in French.

The topics follow the multiplication chapter of the ADEM-Dakar Sixième booklet (product, shifting the comma, properties, squares and cubes),
but every explanation, example and exercise was written independently, with our own numbers.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-6e-multiplication"
number, choice, ordered, between = make_kit(CHAPTER_ID)


def round_unit(value):
    """Round to the nearest whole number, halves going up, the way the lesson teaches."""
    return int(value + Fraction(1, 2))


# ----- Section 1: the product of two decimal numbers -----
S1 = Section(
    "produit", "Le produit de deux nombres décimaux", 24, "produit",
    "Multiplier deux nombres décimaux en colonnes, placer correctement la virgule, estimer un produit et résoudre un problème.",
    [
        para("Un mètre de tissu coûte 1 250 F. Pour 3 m, on calcule " + N("3 \\times 1250") + " = 3 750 F. Mais combien coûtent 2,5 m de ce tissu ? Cette fois, l'un des nombres "
             "à multiplier est un nombre décimal. Ce chapitre t'apprend à multiplier des nombres décimaux sans te tromper de virgule."),
        definition("Produit et facteurs",
                   "Le résultat d'une multiplication s'appelle le produit. Les nombres que l'on multiplie s'appellent les facteurs. Dans " + N("4 \\times 1,5 = 6") + ", les facteurs sont 4 et 1,5 et le produit est 6."),
        example("Exemple 1", "Calculer " + N("4 \\times 1,5") + " de deux façons.",
                "Multiplier par un entier, c'est additionner plusieurs fois le même nombre. On peut aussi oublier la virgule, multiplier, puis la remettre.",
                [(N("1,5 + 1,5 + 1,5 + 1,5") + " = " + N("6"), "Première façon : 4 fois 1,5, c'est 1,5 additionné 4 fois. 1,5 + 1,5 = 3, puis 3 + 3 = 6."),
                 (N("15 \\times 4") + " = " + N("60"), "Deuxième façon : 1,5 s'écrit 15 dixièmes. On multiplie 15 par 4 sans la virgule."),
                 (N("60 \\text{ dixièmes}") + " = " + N("6,0") + " = " + N("6"), "60 dixièmes, c'est 6 unités : on remet la virgule pour avoir un chiffre après la virgule, comme dans 1,5.")],
                N("6"), "d('1,5')*4==d('6') and 15*4==60"),
        para("Et si les deux facteurs sont décimaux ? Prenons " + N("2,5 \\times 1,3") + ". On a 2,5 = 25 dixièmes et 1,3 = 13 dixièmes. "
             "Un dixième multiplié par un dixième donne un centième : on partage en 10 une part qui est déjà un dixième, ce qui donne 100 parts de l'unité. "
             "Donc 25 dixièmes × 13 dixièmes = (25 × 13) centièmes = 325 centièmes = 3,25. "
             "De la même façon, un centième multiplié par un dixième donne un millième (1/100 × 1/10 = 1/1000) : à chaque fois, les nombres de chiffres après la virgule s'additionnent."),
        rule("Multiplier deux nombres décimaux",
             "On oublie les virgules et on multiplie les deux nombres comme des entiers. Ensuite on place la virgule dans le produit : le produit a autant de chiffres après la virgule "
             "que les deux facteurs en ont ensemble. Si un chiffre manque, on ajoute des zéros devant."),
        example("Exemple 2", "Calculer " + N("2,5 \\times 1,3") + ".",
                "On compte les chiffres après la virgule dans chaque facteur, on multiplie sans les virgules, puis on place la virgule.",
                [("2,5 a 1 chiffre après la virgule, 1,3 en a 1", "Le produit aura 1 + 1 = 2 chiffres après la virgule."),
                 (N("25 \\times 13") + " = " + N("325"), "On multiplie sans les virgules : 25 × 13 = 250 + 75 = 325."),
                 (N("325") + " centièmes = " + N("3,25"), "On place la virgule pour avoir 2 chiffres après elle.")],
                N("3,25"), "d('2,5')*d('1,3')==d('3,25') and 25*13==325"),
        example("Exemple 3", "Calculer " + N("6,35 \\times 4,2") + ".",
                "On multiplie sans les virgules, avec les produits partiels, puis on place la virgule.",
                [("6,35 a 2 chiffres après la virgule, 4,2 en a 1", "Le produit aura 2 + 1 = 3 chiffres après la virgule."),
                 (N("635 \\times 2") + " = " + N("1270"), "On multiplie d'abord 635 par les unités de 42, c'est-à-dire par 2. Les centièmes (2 chiffres) fois les dixièmes (1 chiffre) donnent des millièmes (3 chiffres)."),
                 (N("635 \\times 40") + " = " + N("25400"), "Puis par les dizaines de 42, c'est-à-dire par 40 : 635 × 4 = 2 540, et on multiplie encore par 10."),
                 (N("1270 + 25400") + " = " + N("26670"), "On additionne les produits partiels : 635 × 42 = 26 670."),
                 (N("26670") + " millièmes = " + N("26,670") + " = " + N("26,67"), "On place la virgule pour avoir 3 chiffres après elle. Le zéro final ne change pas la valeur.")],
                N("26,67"), "d('6,35')*d('4,2')==d('26,67') and 635*42==26670 and 635*2+635*40==26670"),
        rule("Arrondir à l'unité la plus proche",
             "On regarde le chiffre des dixièmes. S'il est 0, 1, 2, 3 ou 4, on garde la partie entière. S'il est 5, 6, 7, 8 ou 9, on ajoute 1 à la partie entière. "
             "Exemples : " + N("18,7") + " devient 19 ; " + N("4,2") + " devient 4 ; " + N("6,5") + " devient 7."),
        example("Exemple 4", "Estimer " + N("18,7 \\times 4,2") + " en arrondissant chaque facteur à l'unité la plus proche, puis calculer le produit exact.",
                "Un ordre de grandeur permet de vérifier la place de la virgule : le produit exact doit en être proche.",
                [("18,7 devient 19 ; 4,2 devient 4", "Chiffres des dixièmes : 7 (on ajoute 1) et 2 (on garde)."),
                 (N("19 \\times 4") + " = " + N("76"), "L'ordre de grandeur est 76."),
                 (N("187 \\times 42") + " = " + N("7854"), "Sans les virgules : 187 × 42 = 187 × 40 + 187 × 2 = 7 480 + 374 = 7 854."),
                 (N("7854") + " centièmes = " + N("78,54"), "Il y a 1 + 1 = 2 chiffres après la virgule. 78,54 est proche de 76 : la virgule est bien placée.")],
                N("78,54"), "d('18,7')*d('4,2')==d('78,54') and 187*42==7854 and round_unit(d('18,7'))*round_unit(d('4,2'))==76"),
        example("Exemple 5", "Un mètre de tissu coûte 1 250 F. Combien coûtent 2,5 m ?",
                "Le prix d'une longueur est le prix du mètre multiplié par le nombre de mètres.",
                [("Prix = " + N("2,5 \\times 1250"), "On multiplie le nombre de mètres par le prix d'un mètre."),
                 (N("25 \\times 1250") + " = " + N("31250"), "Sans la virgule : 25 × 1 250 = 25 × 1 000 + 25 × 250 = 25 000 + 6 250 = 31 250."),
                 (N("31250") + " dixièmes = " + N("3125"), "2,5 a un chiffre après la virgule, 1 250 n'en a pas : 1 chiffre après la virgule, 3 125,0 = 3 125."),
                 ("Vérification : 2 m coûtent 2 500 F et 0,5 m coûte 625 F", "2 500 + 625 = 3 125.")],
                "Les 2,5 m coûtent 3 125 F.", "d('2,5')*1250==3125 and 2*1250+d('0,5')*1250==3125"),
        warning("Multiplier ne rend pas toujours plus grand. Multiplier par un nombre plus petit que 1 rend plus petit : " + N("0,5 \\times 0,5 = 0,25") + ", et 0,25 est plus petit que 0,5."),
    ],
    [
        number("s1-g1", "produit", "Calcule " + N("3,2 \\times 2") + ".", d("6,4"),
               hints=["Oublie la virgule : combien font 32 × 2 ?", "3,2 a un chiffre après la virgule. Combien en aura le produit ?"],
               solution=["Sans la virgule : 32 × 2 = 64.", "Le produit a 1 chiffre après la virgule : 6,4."], form="decimal"),
        number("s1-g2", "produit", "Calcule " + N("1,4 \\times 0,6") + ".", d("0,84"),
               hints=["Multiplie 14 par 6.", "Chaque facteur a un chiffre après la virgule. Combien de chiffres après la virgule dans le produit ?"],
               solution=["Sans les virgules : 14 × 6 = 84.", "Le produit a 1 + 1 = 2 chiffres après la virgule : 0,84."]),
        number("s1-g3", "produit", "Calcule " + N("6,5 \\times 3,4") + ".", d("22,1"),
               hints=["Multiplie 65 par 34, avec les produits partiels 65 × 4 et 65 × 30.", "Place la virgule à 2 chiffres de la droite, puis simplifie le zéro final."],
               solution=["65 × 4 = 260 et 65 × 30 = 1 950.", "260 + 1 950 = 2 210, donc le produit sans virgule est 2 210.", "Il y a 2 chiffres après la virgule : 22,10, soit 22,1."]),
        number("s1-g4", "produit", "Estime " + N("28,6 \\times 3,2") + " en arrondissant chaque facteur à l'unité la plus proche.", Fraction(87),
               hints=["Regarde le chiffre des dixièmes de chaque facteur pour arrondir."],
               solution=["28,6 : le chiffre des dixièmes est 6, on passe à 29. 3,2 : le chiffre des dixièmes est 2, on garde 3.", "29 × 3 = 87."]),
        choice("s1-g5", "produit", "Combien vaut " + N("0,8 \\times 0,5") + " ?", [N("0,4"), N("4"), N("0,04")], 0,
               hints=["Multiplie 8 par 5, puis compte les chiffres après la virgule."],
               solution=["Sans les virgules : 8 × 5 = 40.", "Il y a 1 + 1 = 2 chiffres après la virgule : 0,40 = 0,4."],
               wrong={2: "0,04 aurait trois chiffres après la virgule. Ici il y en a 1 + 1 = 2, donc 40 centièmes, soit 0,40 = 0,4.",
                      1: "4 est trop grand : 0,8 et 0,5 sont plus petits que 1, donc leur produit est plus petit que chacun d'eux."}),
    ])

# ----- Section 2: multiplying by 10, 100, 1000, 0.1, 0.01 -----
S2 = Section(
    "decalage", "Multiplier par 10, 100, 1 000 et par 0,1, 0,01, 0,001", 18, "decalage",
    "Multiplier et convertir rapidement en décalant la virgule, et expliquer pourquoi cela marche.",
    [
        para("Quand on passe de 3,4 m à des centimètres, on multiplie par 100 et on trouve 340 cm. Il existe un moyen très rapide de multiplier par 10, 100 ou 1 000, "
             "et il repose sur la valeur des rangs que tu connais."),
        rule("Multiplier par 10, 100, 1 000",
             "Multiplier par 10, c'est rendre chaque chiffre dix fois plus grand : il passe au rang juste à gauche. La virgule semble donc se déplacer d'un rang vers la droite. "
             "Pour 100 elle se déplace de deux rangs, pour 1 000 de trois rangs. S'il n'y a plus de chiffre à droite de la virgule, on ajoute des zéros."),
        example("Exemple 1", "Montrer pourquoi " + N("3,47 \\times 10") + " = " + N("34,7") + ".",
                "On multiplie chaque chiffre par 10 en regardant son rang.",
                [("3 unités × 10 = 3 dizaines", "Le chiffre 3 passe du rang des unités au rang des dizaines."),
                 ("4 dixièmes × 10 = 4 unités", "Le chiffre 4 passe du rang des dixièmes au rang des unités."),
                 ("7 centièmes × 10 = 7 dixièmes", "Le chiffre 7 passe du rang des centièmes au rang des dixièmes."),
                 (N("3,47 \\times 10") + " = " + N("34,7"), "Chaque chiffre a avancé d'un rang vers la gauche : la virgule est maintenant un rang plus loin vers la droite.")],
                N("34,7"), "d('3,47')*10==d('34,7')"),
        example("Exemple 2", "Calculer " + N("6,238 \\times 100") + " et " + N("0,45 \\times 1000") + ".",
                "On déplace la virgule de 2 rangs, puis de 3 rangs vers la droite, en ajoutant des zéros si besoin.",
                [(N("6,238 \\times 100") + " = " + N("623,8"), "Deux rangs vers la droite : 6,238 devient 623,8."),
                 (N("0,45 \\times 1000") + " = " + N("450"), "Trois rangs vers la droite : 0,45 n'a que deux chiffres après la virgule, il en manque un, on ajoute un zéro : 450.")],
                N("623,8") + " ; " + N("450"), "d('6,238')*100==d('623,8') and d('0,45')*1000==450"),
        rule("Multiplier par 0,1, 0,01, 0,001",
             "Multiplier par 0,1, c'est prendre un dixième du nombre : chaque chiffre devient dix fois plus petit, il passe au rang juste à droite. La virgule se déplace d'un rang vers la gauche. "
             "Pour 0,01 elle se déplace de deux rangs, pour 0,001 de trois rangs. On ajoute des zéros devant si besoin."),
        example("Exemple 3", "Calculer " + N("38,5 \\times 0,1") + " et " + N("7 \\times 0,01") + ".",
                "On déplace la virgule vers la gauche de 1 rang, puis de 2 rangs.",
                [(N("38,5 \\times 0,1") + " = " + N("3,85"), "Un rang vers la gauche : 38,5 devient 3,85."),
                 (N("7 \\times 0,01") + " = " + N("0,07"), "7 s'écrit 7,0. Deux rangs vers la gauche : il faut ajouter des zéros devant, 0,07.")],
                N("3,85") + " ; " + N("0,07"), "d('38,5')*d('0,1')==d('3,85') and 7*d('0,01')==d('0,07')"),
        example("Exemple 4", "Convertir " + N("3,4") + " m en centimètres, puis " + N("275") + " cm en mètres.",
                "1 m = 100 cm. Pour passer des mètres aux centimètres, on multiplie par 100. Pour revenir, on multiplie par 0,01.",
                [(N("3,4 \\times 100") + " = " + N("340"), "Deux rangs vers la droite : 3,4 m = 340 cm."),
                 (N("275 \\times 0,01") + " = " + N("2,75"), "Deux rangs vers la gauche : 275 cm = 2,75 m.")],
                "3,4 m = 340 cm et 275 cm = 2,75 m", "d('3,4')*100==340 and 275*d('0,01')==d('2,75')"),
        warning("Ne te contente pas d'ajouter un zéro à la fin du nombre : " + N("2,5 \\times 10 = 25") + " et non " + N("2,50") + ", car 2,50 vaut 2,5. De même " + N("3,4 \\times 100 = 340") + " et non " + N("3,400")
                + ". Il faut déplacer la virgule."),
    ],
    [
        number("s2-g1", "decalage", "Calcule " + N("5,28 \\times 10") + ".", d("52,8"),
               hints=["Dans quel sens se déplace la virgule quand on multiplie par 10 ? De combien de rangs ?"],
               solution=["Multiplier par 10, c'est déplacer la virgule d'un rang vers la droite.", "5,28 × 10 = 52,8."]),
        number("s2-g2", "decalage", "Calcule " + N("0,058 \\times 100") + ".", d("5,8"),
               hints=["Déplace la virgule de deux rangs vers la droite."],
               solution=["0,058 : deux rangs vers la droite donne 05,8.", "Le zéro devant ne change rien : 0,058 × 100 = 5,8."]),
        number("s2-g3", "decalage", "Calcule " + N("125 \\times 0,01") + ".", d("1,25"),
               hints=["Multiplier par 0,01, c'est prendre un centième. Dans quel sens se déplace la virgule ?"],
               solution=["125 s'écrit 125,0. Deux rangs vers la gauche : 1,250.", "125 × 0,01 = 1,25."]),
        number("s2-g4", "decalage", "Par quel nombre faut-il multiplier " + N("4,26") + " pour obtenir " + N("426") + " ?", Fraction(100),
               hints=["Combien de rangs la virgule a-t-elle été déplacée, et dans quel sens ?"],
               solution=["Pour passer de 4,26 à 426, la virgule se déplace de deux rangs vers la droite.", "Il faut multiplier par 100."]),
        number("s2-g5", "decalage", "Convertis " + N("2,35") + " km en mètres.", Fraction(2350), units=["m"],
               hints=["1 km = 1 000 m. Faut-il multiplier par 1 000 ou par 0,001 ?"],
               solution=["Pour passer des kilomètres aux mètres, on multiplie par 1 000.", "2,35 × 1 000 = 2 350 : 2,35 km = 2 350 m."]),
    ])

# ----- Section 3: properties and efficient calculation -----
S3 = Section(
    "proprietes", "Les propriétés de la multiplication et le calcul efficace", 24, "proprietes",
    "Connaître les propriétés de la multiplication et s'en servir pour calculer plus vite et sans erreur.",
    [
        para("Certains calculs deviennent faciles si on choisit bien l'ordre des facteurs. Par exemple, " + N("25 \\times 6,3 \\times 4") + " est difficile de gauche à droite, "
             "mais facile si on calcule d'abord " + N("25 \\times 4") + ". Les propriétés de la multiplication expliquent pourquoi on a le droit de le faire."),
        rule("Commutativité et associativité",
             "On peut changer l'ordre de deux facteurs : " + N("a \\times b = b \\times a") + ". On peut regrouper les facteurs comme on veut : " + N("(a \\times b) \\times c = a \\times (b \\times c)") + "."),
        rule("Élément neutre et élément absorbant",
             "Multiplier par 1 ne change rien : " + N("a \\times 1 = a") + ", par exemple " + N("7,3 \\times 1 = 7,3") + ". Multiplier par 0 donne toujours 0 : " + N("a \\times 0 = 0") + ", par exemple " + N("7,3 \\times 0 = 0") + "."),
        rule("Distributivité de la multiplication sur l'addition et la soustraction",
             N("a \\times (b + c) = a \\times b + a \\times c") + " et " + N("a \\times (b - c) = a \\times b - a \\times c") + ". On peut l'utiliser dans les deux sens : pour développer, ou pour factoriser."),
        para("Pour comprendre la distributivité, regarde un rectangle de largeur " + N("a") + " et de longueur " + N("b + c") + ". Son aire est " + N("a \\times (b + c)") + ". "
             "Si on le coupe en deux rectangles, l'un de longueur " + N("b") + " et l'autre de longueur " + N("c") + ", les aires sont " + N("a \\times b") + " et " + N("a \\times c") + ", et leur somme est la même aire. "
             "Rappel : dans " + N("a \\times b + a \\times c") + ", les deux multiplications se font avant l'addition."),
        example("Exemple 1", "Vérifier la commutativité et l'associativité avec " + N("a = 2,5") + ", " + N("b = 0,4") + " et " + N("c = 3") + ".",
                "On calcule chaque côté de l'égalité et on compare. Un exemple ne prouve pas une propriété, mais il montre comment elle s'utilise.",
                [(N("2,5 \\times 0,4") + " = " + N("1"), "25 × 4 = 100, avec 2 chiffres après la virgule : 1,00 = 1."),
                 (N("0,4 \\times 2,5") + " = " + N("1"), "Dans l'autre ordre, on trouve le même résultat : c'est la commutativité."),
                 (N("(2,5 \\times 0,4) \\times 3") + " = " + N("1 \\times 3") + " = " + N("3"), "On calcule d'abord la parenthèse."),
                 (N("2,5 \\times (0,4 \\times 3)") + " = " + N("2,5 \\times 1,2") + " = " + N("3"), "25 × 12 = 300, avec 2 chiffres après la virgule : 3,00 = 3. On trouve le même résultat : c'est l'associativité.")],
                N("1") + " et " + N("3"), "d('2,5')*d('0,4')==d('0,4')*d('2,5')==1 and (d('2,5')*d('0,4'))*3==d('2,5')*(d('0,4')*3)==3"),
        example("Exemple 2", "Calculer efficacement " + N("25 \\times 6,3 \\times 4") + ".",
                "On cherche deux facteurs dont le produit est facile, comme 25 et 4, puis on les regroupe.",
                [(N("25 \\times 6,3 \\times 4") + " = " + N("25 \\times 4 \\times 6,3"), "Commutativité : on change l'ordre pour rapprocher 25 et 4."),
                 ("$= (25 \\times 4) \\times 6{,}3$", "Associativité : on regroupe 25 et 4."),
                 ("$= 100 \\times 6{,}3$", "25 × 4 = 100."),
                 ("$= 630$", "Multiplier par 100 déplace la virgule de deux rangs vers la droite.")],
                N("630"), "25*4*d('6,3')==630"),
        example("Exemple 3", "Calculer " + N("3,5 \\times 102") + " avec la distributivité.",
                "On écrit 102 comme 100 + 2, ce qui rend les deux produits faciles.",
                [(N("3,5 \\times 102") + " = " + N("3,5 \\times (100 + 2)"), "102 = 100 + 2."),
                 ("$= 3{,}5 \\times 100 + 3{,}5 \\times 2$", "Distributivité : on multiplie 3,5 par chaque terme de la somme."),
                 ("$= 350 + 7$", "3,5 × 100 = 350 et 3,5 × 2 = 7."),
                 ("$= 357$", "On additionne.")],
                N("357"), "d('3,5')*102==357 and d('3,5')*100+d('3,5')*2==357"),
        example("Exemple 4", "Calculer " + N("4,7 \\times 6 + 4,7 \\times 4") + " en factorisant.",
                "Les deux produits ont le facteur 4,7 en commun. On utilise la distributivité dans l'autre sens.",
                [(N("4,7 \\times 6 + 4,7 \\times 4") + " = " + N("4,7 \\times (6 + 4)"), "Distributivité : 4,7 est un facteur commun."),
                 ("$= 4{,}7 \\times 10$", "6 + 4 = 10."),
                 ("$= 47$", "Multiplier par 10 déplace la virgule d'un rang vers la droite.")],
                N("47"), "d('4,7')*6+d('4,7')*4==47"),
        example("Exemple 5", "Calculer " + N("12 \\times 4,99") + " sans poser la multiplication.",
                "4,99 est proche de 5 : on écrit 4,99 = 5 − 0,01 et on utilise la distributivité sur la soustraction.",
                [(N("12 \\times 4,99") + " = " + N("12 \\times (5 - 0,01)"), "4,99 = 5 − 0,01."),
                 ("$= 12 \\times 5 - 12 \\times 0{,}01$", "Distributivité sur la soustraction."),
                 ("$= 60 - 0{,}12$", "12 × 5 = 60 et 12 × 0,01 = 0,12."),
                 ("$= 59{,}88$", "60,00 − 0,12 = 59,88.")],
                N("59,88"), "12*d('4,99')==d('59,88') and 12*5-12*d('0,01')==d('59,88')"),
        warning("La distributivité s'applique à tous les termes de la parenthèse : " + N("3 \\times (2 + 5) = 3 \\times 2 + 3 \\times 5 = 21") + ", et non " + N("3 \\times 2 + 5 = 11") + "."),
    ],
    [
        choice("s3-g1", "proprietes", "On écrit " + N("7,5 \\times 4 = 4 \\times 7,5") + ". Quelle propriété utilise-t-on ?", ["La commutativité", "L'associativité", "La distributivité"], 0,
               hints=["Qu'est-ce qui change entre les deux membres de l'égalité : l'ordre des facteurs, ou le regroupement ?"],
               solution=["Les facteurs 7,5 et 4 sont échangés, sans parenthèses.", "C'est la commutativité de la multiplication."],
               wrong={1: "L'associativité concerne le regroupement de trois facteurs avec des parenthèses. Ici on échange seulement deux facteurs."}),
        number("s3-g2", "proprietes", "Calcule efficacement " + N("2 \\times 7,3 \\times 5") + ".", Fraction(73),
               hints=["Quels deux facteurs ont un produit facile ?", "Regroupe-les, puis multiplie par le facteur restant."],
               solution=["2 × 5 = 10, donc 2 × 7,3 × 5 = 10 × 7,3 (commutativité puis associativité).", "10 × 7,3 = 73."]),
        number("s3-g3", "proprietes", "Calcule " + N("4,2 \\times 101") + " en utilisant la distributivité.", d("424,2"),
               hints=["Écris 101 comme une somme de deux nombres faciles."],
               solution=["101 = 100 + 1, donc 4,2 × 101 = 4,2 × 100 + 4,2 × 1.", "4,2 × 100 = 420 et 4,2 × 1 = 4,2.", "420 + 4,2 = 424,2."]),
        number("s3-g4", "proprietes", "Calcule " + N("2,6 \\times 8 + 2,6 \\times 2") + " en factorisant.", Fraction(26),
               hints=["Quel facteur est commun aux deux produits ?"],
               solution=["2,6 est un facteur commun : 2,6 × 8 + 2,6 × 2 = 2,6 × (8 + 2).", "2,6 × 10 = 26."]),
    ])

# ----- Section 4: square and cube -----
S4 = Section(
    "puissances", "Le carré et le cube d'un nombre", 16, "puissances",
    "Calculer le carré et le cube d'un nombre décimal et les relier à l'aire d'un carré et au volume d'un cube.",
    [
        para("Un carré dont le côté mesure 3 cm a pour aire " + N("3 \\times 3") + " = 9 cm². Multiplier un nombre par lui-même arrive très souvent, c'est pourquoi on lui a donné un nom."),
        definition("Carré et cube",
                   "Le carré d'un nombre est ce nombre multiplié par lui-même : " + N("a^2 = a \\times a") + ". On lit « a au carré ». Le cube d'un nombre est ce nombre multiplié deux fois par lui-même : "
                   + N("a^3 = a \\times a \\times a") + ". On lit « a au cube ». Exemples : " + N("3^2 = 3 \\times 3 = 9") + " et " + N("2^3 = 2 \\times 2 \\times 2 = 8") + "."),
        example("Exemple 1", "Calculer " + N("(1,5)^2") + ".",
                "On écrit le carré comme un produit de deux facteurs, puis on multiplie comme à la première section.",
                [(N("(1,5)^2") + " = " + N("1,5 \\times 1,5"), "Le carré, c'est le nombre multiplié par lui-même."),
                 (N("15 \\times 15") + " = " + N("225"), "Sans les virgules : 15 × 15 = 150 + 75 = 225."),
                 (N("225") + " centièmes = " + N("2,25"), "Chaque facteur a 1 chiffre après la virgule : le produit en a 2.")],
                N("2,25"), "d('1,5')**2==d('2,25') and 15*15==225"),
        example("Exemple 2", "Calculer " + N("(1,2)^3") + ".",
                "On calcule le carré, puis on multiplie encore une fois par le nombre.",
                [(N("(1,2)^3") + " = " + N("1,2 \\times 1,2 \\times 1,2"), "Le cube, c'est le nombre écrit trois fois dans le produit."),
                 (N("1,2 \\times 1,2") + " = " + N("1,44"), "12 × 12 = 144, avec 2 chiffres après la virgule."),
                 (N("1,44 \\times 1,2") + " = " + N("1,728"), "144 × 12 = 1 440 + 288 = 1 728, avec 2 + 1 = 3 chiffres après la virgule.")],
                N("1,728"), "d('1,2')**3==d('1,728') and 12*12==144 and 144*12==1728"),
        example("Exemple 3", "Calculer " + N("(0,3)^2") + ", " + N("10^3") + " et " + N("(0,1)^3") + ".",
                "On utilise la règle des chiffres après la virgule et le décalage de la virgule.",
                [(N("(0,3)^2") + " = " + N("0,3 \\times 0,3") + " = " + N("0,09"), "3 × 3 = 9, avec 2 chiffres après la virgule. Le carré d'un nombre plus petit que 1 est plus petit que ce nombre."),
                 (N("10^3") + " = " + N("10 \\times 10 \\times 10") + " = " + N("1000"), "100 × 10 = 1 000."),
                 (N("(0,1)^3") + " = " + N("0,1 \\times 0,1 \\times 0,1") + " = " + N("0,001"), "1 × 1 × 1 = 1, avec 3 chiffres après la virgule.")],
                N("0,09") + " ; " + N("1000") + " ; " + N("0,001"), "d('0,3')**2==d('0,09') and 10**3==1000 and d('0,1')**3==d('0,001')"),
        example("Exemple 4", "Un carré a un côté de 2,5 m. Quelle est son aire ?",
                "L'aire d'un carré est le carré de la longueur de son côté.",
                [("Aire = " + N("(2,5)^2"), "Aire d'un carré = côté × côté."),
                 (N("2,5 \\times 2,5") + " = " + N("6,25"), "25 × 25 = 625, avec 2 chiffres après la virgule.")],
                "L'aire est " + N("6,25") + " m².", "d('2,5')**2==d('6,25')"),
        example("Exemple 5", "Un cube a une arête de 2,4 dm. Quel est son volume ?",
                "Le volume d'un cube est le cube de la longueur de son arête : on multiplie trois fois l'arête par elle-même.",
                [("Volume = " + N("(2,4)^3") + " = " + N("2,4 \\times 2,4 \\times 2,4"), "Volume d'un cube = arête × arête × arête."),
                 (N("2,4 \\times 2,4") + " = " + N("5,76"), "24 × 24 = 576, avec 2 chiffres après la virgule."),
                 (N("5,76 \\times 2,4") + " = " + N("13,824"), "576 × 24 = 13 824, avec 2 + 1 = 3 chiffres après la virgule.")],
                "Le volume est " + N("13,824") + " dm³.", "d('2,4')**3==d('13,824') and 576*24==13824"),
        warning("Ne confonds pas " + N("3^2") + " avec " + N("3 \\times 2") + ". Le petit nombre en haut dit combien de fois on écrit le nombre dans le produit : " + N("3^2 = 3 \\times 3 = 9") + ", et non 6."),
    ],
    [
        number("s4-g1", "puissances", "Calcule " + N("8^2") + ".", Fraction(64),
               hints=["Le carré de 8, c'est 8 multiplié par quoi ?"], solution=["8² = 8 × 8 = 64."]),
        number("s4-g2", "puissances", "Calcule " + N("(1,1)^2") + ".", d("1,21"),
               hints=["Écris le carré comme un produit, puis multiplie sans les virgules."],
               solution=["1,1² = 1,1 × 1,1.", "11 × 11 = 121, avec 2 chiffres après la virgule : 1,21."]),
        number("s4-g3", "puissances", "Calcule " + N("(0,2)^3") + ".", d("0,008"),
               hints=["Écris le cube comme un produit de trois facteurs.", "Compte les chiffres après la virgule dans les trois facteurs."],
               solution=["0,2³ = 0,2 × 0,2 × 0,2.", "2 × 2 × 2 = 8, avec 3 chiffres après la virgule : 0,008."]),
        choice("s4-g4", "puissances", "Quelle est la valeur de " + N("5^2") + " ?", [N("10"), N("25"), N("55")], 1,
               hints=["Combien de fois écrit-on le nombre 5 dans le produit ?"],
               solution=["5² = 5 × 5 = 25."],
               wrong={0: "Tu as calculé 5 × 2. Le petit 2 dit qu'on écrit le nombre 5 deux fois dans le produit : 5 × 5."}),
        number("s4-g5", "puissances", "Un carré a un côté de 3,5 m. Quelle est son aire, en m² ?", d("12,25"), units=["m2", "m²"],
               hints=["L'aire d'un carré est le carré de son côté."],
               solution=["Aire = 3,5² = 3,5 × 3,5.", "35 × 35 = 1 225, avec 2 chiffres après la virgule : 12,25 m²."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "produit", "Calcule " + N("5 \\times 2,4") + ".", Fraction(12), 1, ["Multiplie 5 par 24, puis compte les chiffres après la virgule."], ["5 × 24 = 120, avec 1 chiffre après la virgule : 12,0 = 12."]),
    number("p2", "produit", "Calcule " + N("0,3 \\times 4") + ".", d("1,2"), 1, ["Multiplie 3 par 4."], ["3 × 4 = 12, avec 1 chiffre après la virgule : 1,2."], form="decimal"),
    number("p3", "produit", "Calcule " + N("2,5 \\times 0,4") + ".", Fraction(1), 2, ["Multiplie 25 par 4. Combien de chiffres après la virgule dans le produit ?"], ["25 × 4 = 100, avec 2 chiffres après la virgule : 1,00 = 1."]),
    number("p4", "produit", "Calcule " + N("12,5 \\times 0,8") + ".", Fraction(10), 2, ["Multiplie 125 par 8."], ["125 × 8 = 1 000, avec 2 chiffres après la virgule : 10,00 = 10."]),
    number("p5", "produit", "Calcule " + N("4,05 \\times 6") + ".", d("24,3"), 2, ["Ne perds pas le zéro de 4,05 : multiplie 405 par 6."], ["405 × 6 = 2 430, avec 2 chiffres après la virgule : 24,30 = 24,3."]),
    number("p6", "produit", "Calcule " + N("3,14 \\times 2,5") + ".", d("7,85"), 3, ["Multiplie 314 par 25 : 314 × 25 = 314 × 100 divisé par 4, ou 314 × 20 + 314 × 5.", "Combien de chiffres après la virgule dans le produit ?"],
           ["314 × 20 = 6 280 et 314 × 5 = 1 570.", "6 280 + 1 570 = 7 850, avec 3 chiffres après la virgule : 7,850 = 7,85."]),
    number("p7", "produit", "Estime " + N("41,8 \\times 5,2") + " en arrondissant chaque facteur à l'unité la plus proche.", Fraction(210), 2,
           ["Regarde le chiffre des dixièmes de chaque facteur."], ["41,8 devient 42 et 5,2 devient 5.", "42 × 5 = 210."]),
    choice("p8", "produit", "Le produit de 0,6 par 0,7 est :", [N("4,2"), N("0,42"), N("0,042")], 1, 2,
           ["Multiplie 6 par 7 et compte les chiffres après la virgule dans les deux facteurs."], ["6 × 7 = 42, avec 1 + 1 = 2 chiffres après la virgule : 0,42."],
           wrong={0: "4,2 est plus grand que chacun des deux facteurs, ce qui est impossible pour deux nombres plus petits que 1.", 2: "0,042 aurait 3 chiffres après la virgule, il n'y en a que 2 dans le produit."}),
    number("p9", "problemes", "Un champ rectangulaire mesure 12,5 m de long et 8,4 m de large. Quelle est son aire, en m² ?", Fraction(105), 3, ["L'aire d'un rectangle est longueur × largeur."],
           ["Aire = 12,5 × 8,4.", "125 × 84 = 10 500, avec 2 chiffres après la virgule : 105,00 = 105.", "L'aire est 105 m²."], units=["m2", "m²"]),
    number("p10", "problemes", "Un mètre de tissu coûte 1 800 F. Combien coûtent 3,5 m ?", Fraction(6300), 2, ["Multiplie le prix d'un mètre par le nombre de mètres."],
           ["Prix = 3,5 × 1 800.", "35 × 1 800 = 63 000, avec 1 chiffre après la virgule : 6 300,0.", "Les 3,5 m coûtent 6 300 F."], units=["F"]),
    choice("p11", "produit", "Moussa a calculé " + N("0,5 \\times 0,5 = 2,5") + ". Quelle erreur a-t-il faite ?",
           ["Il n'a pas compté les chiffres après la virgule : 5 × 5 = 25 donne 0,25", "Il a additionné au lieu de multiplier", "Il a oublié une retenue"], 0, 3,
           ["Fais une estimation : 0,5 est la moitié de 1, donc la moitié de 0,5 vaut combien ?"],
           ["Multiplier par 0,5, c'est prendre la moitié : la moitié de 0,5 est 0,25, qui est plus petit que 0,5. Le résultat 2,5 est trop grand.", "5 × 5 = 25, et le produit a 1 + 1 = 2 chiffres après la virgule : 0,25."]),
    number("p12", "decalage", "Calcule " + N("7,3 \\times 10") + ".", Fraction(73), 1, ["Déplace la virgule d'un rang vers la droite."], ["7,3 × 10 = 73."]),
    number("p13", "decalage", "Calcule " + N("0,86 \\times 100") + ".", Fraction(86), 1, ["Déplace la virgule de deux rangs vers la droite."], ["0,86 × 100 = 86."]),
    number("p14", "decalage", "Calcule " + N("5,4 \\times 1000") + ".", Fraction(5400), 2, ["Trois rangs vers la droite : il manque des chiffres, que faut-il ajouter ?"], ["5,4 : trois rangs vers la droite, on ajoute deux zéros : 5 400."]),
    number("p15", "decalage", "Calcule " + N("640 \\times 0,1") + ".", Fraction(64), 2, ["Multiplier par 0,1, c'est prendre un dixième. Dans quel sens se déplace la virgule ?"], ["640 = 640,0. Un rang vers la gauche : 64,0 = 64."]),
    number("p16", "decalage", "Calcule " + N("9,5 \\times 0,01") + ".", d("0,095"), 2, ["Deux rangs vers la gauche : faut-il ajouter des zéros devant ?"], ["9,5 : deux rangs vers la gauche donne 0,095."]),
    number("p17", "decalage", "Convertis " + N("3,6") + " m en centimètres.", Fraction(360), 2, ["1 m = 100 cm."], ["3,6 × 100 = 360 : 3,6 m = 360 cm."], units=["cm"]),
    number("p18", "decalage", "Par quel nombre faut-il multiplier " + N("0,0725") + " pour obtenir " + N("72,5") + " ?", Fraction(1000), 3,
           ["De combien de rangs la virgule se déplace-t-elle, et vers où ?"], ["Pour passer de 0,0725 à 72,5, la virgule se déplace de trois rangs vers la droite.", "Il faut multiplier par 1 000."]),
    choice("p19", "decalage", "Combien vaut " + N("2,5 \\times 10") + " ?", [N("25"), N("2,50"), N("250")], 0, 1, ["Déplace la virgule d'un rang vers la droite."], ["2,5 × 10 = 25.", "2,50 est égal à 2,5, ce n'est pas le résultat."],
           wrong={1: "2,50 vaut 2,5 : on n'a rien multiplié. Multiplier par 10 rend le nombre dix fois plus grand.", 2: "250 est cent fois plus grand que 2,5. Multiplier par 10 déplace la virgule d'un seul rang."}),
    number("p20", "proprietes", "Calcule efficacement " + N("5 \\times 7,2 \\times 2") + ".", Fraction(72), 1, ["Quels facteurs ont un produit facile ?"], ["5 × 2 = 10 puis 10 × 7,2 = 72."]),
    number("p21", "proprietes", "Calcule efficacement " + N("4 \\times 8,5 \\times 25") + ".", Fraction(850), 2, ["Quel produit de deux facteurs donne 100 ?"], ["4 × 25 = 100 puis 100 × 8,5 = 850."]),
    number("p22", "proprietes", "Calcule " + N("6,5 \\times 102") + " avec la distributivité.", Fraction(663), 2, ["Décompose 102."], ["6,5 × 102 = 6,5 × 100 + 6,5 × 2.", "650 + 13 = 663."]),
    number("p23", "proprietes", "Calcule " + N("7,3 \\times 4 + 7,3 \\times 6") + " en factorisant.", Fraction(73), 2, ["Quel facteur est commun ?"], ["7,3 × (4 + 6) = 7,3 × 10 = 73."]),
    number("p24", "proprietes", "Calcule " + N("5,99 \\times 8") + " sans poser la multiplication.", d("47,92"), 3, ["5,99 est proche de 6 : écris 5,99 sous la forme 6 moins un petit nombre."],
           ["5,99 = 6 − 0,01, donc 5,99 × 8 = 6 × 8 − 0,01 × 8.", "48 − 0,08 = 47,92."]),
    choice("p25", "proprietes", "Quelle égalité est vraie ?", [N("3 \\times (2 + 5) = 3 \\times 2 + 5"), N("3 \\times (2 + 5) = 3 \\times 2 + 3 \\times 5"), N("3 \\times (2 + 5) = 3 \\times 2 \\times 5")], 1, 3,
           ["Calcule chaque membre pour vérifier."], ["3 × (2 + 5) = 3 × 7 = 21.", "3 × 2 + 3 × 5 = 6 + 15 = 21 : c'est la distributivité.", "3 × 2 + 5 = 11 et 3 × 2 × 5 = 30 : ces égalités sont fausses."]),
    choice("p26", "proprietes", "Quelle propriété dit que " + N("8,7 \\times 1 = 8,7") + " ?", ["La commutativité", "1 est l'élément neutre de la multiplication", "0 est l'élément absorbant de la multiplication"], 1, 1,
           ["Que se passe-t-il quand on multiplie par 1 ?"], ["Multiplier par 1 ne change pas le nombre : 1 est l'élément neutre."]),
    number("p27", "proprietes", "Calcule " + N("8,7 \\times 0 \\times 15") + ".", Fraction(0), 2, ["Que vaut un produit dont un facteur est 0 ?"], ["Un facteur est 0 : le produit est 0 (0 est l'élément absorbant)."]),
    number("p28", "puissances", "Calcule " + N("6^2") + ".", Fraction(36), 1, ["6² = 6 × ?"], ["6² = 6 × 6 = 36."]),
    number("p29", "puissances", "Calcule " + N("(0,5)^2") + ".", d("0,25"), 2, ["Multiplie 5 par 5 et compte les chiffres après la virgule."], ["0,5² = 0,5 × 0,5.", "5 × 5 = 25, avec 2 chiffres après la virgule : 0,25."]),
    number("p30", "puissances", "Calcule " + N("(2,5)^2") + ".", d("6,25"), 2, ["25 × 25 = ?"], ["25 × 25 = 625, avec 2 chiffres après la virgule : 6,25."]),
    number("p31", "puissances", "Calcule " + N("4^3") + ".", Fraction(64), 2, ["4³ = 4 × 4 × 4."], ["4 × 4 = 16 puis 16 × 4 = 64."]),
    number("p32", "puissances", "Calcule " + N("(0,3)^3") + ".", d("0,027"), 3, ["Écris le produit de trois facteurs puis compte les chiffres après la virgule."], ["0,3 × 0,3 × 0,3 : 3 × 3 × 3 = 27, avec 3 chiffres après la virgule : 0,027."]),
    choice("p33", "puissances", "Quelle est la valeur de " + N("2^3") + " ?", [N("6"), N("8"), N("9")], 1, 1, ["Combien de fois écrit-on 2 dans le produit ?"], ["2³ = 2 × 2 × 2 = 8."],
           wrong={0: "Tu as calculé 2 × 3. Le petit 3 dit qu'on écrit le nombre 2 trois fois : 2 × 2 × 2.", 2: "9 est le carré de 3. Ici il faut multiplier 2 par lui-même trois fois."}),
    number("p35", "problemes", "Un commerçant achète 12,5 kg de riz à 480 F le kilogramme et 8 kg de mil à 350 F le kilogramme. Combien dépense-t-il en tout, en F ?", Fraction(8800), 3, ["Calcule chaque achat, puis additionne."],
           ["Riz : 12,5 × 480 = 6 000 F. Mil : 8 × 350 = 2 800 F.", "6 000 + 2 800 = 8 800 F."], units=["F"]),
    number("p36", "problemes", "Un carreau carré a 0,4 m de côté. Quelle est l'aire de 50 carreaux, en m² ?", Fraction(8), 3, ["Aire d'un carreau d'abord, puis multiplie par 50."],
           ["Aire d'un carreau = 0,4² = 0,16 m².", "50 × 0,16 = 8 m²."], units=["m2", "m²"]),
    number("p34", "problemes", "Un cube a une arête de 1,5 dm. Quel est son volume, en dm³ ? (Volume d'un cube = arête × arête × arête.)", d("3,375"), 3,
           ["Le volume est le cube de l'arête."], ["Volume = 1,5³ = 1,5 × 1,5 × 1,5.", "1,5 × 1,5 = 2,25 puis 2,25 × 1,5 = 3,375.", "Le volume est 3,375 dm³."], units=["dm3", "dm³"]),
]

SUMMARY = [
    definition("Produit et facteurs", "Dans une multiplication, les nombres multipliés sont les facteurs et le résultat est le produit. Multiplier par un nombre plus petit que 1 donne un résultat plus petit."),
    rule("Multiplier deux décimaux", "On oublie les virgules, on multiplie comme des entiers, puis on place la virgule : autant de chiffres après la virgule que les deux facteurs en ont ensemble. On vérifie avec un ordre de grandeur en arrondissant à l'unité."),
    rule("Décaler la virgule", "Multiplier par 10, 100, 1 000 : la virgule se déplace de 1, 2, 3 rangs vers la droite. Multiplier par 0,1, 0,01, 0,001 : la virgule se déplace de 1, 2, 3 rangs vers la gauche. On ajoute des zéros si besoin."),
    rule("Propriétés", "Commutativité : " + N("a \\times b = b \\times a") + ". Associativité : " + N("(a \\times b) \\times c = a \\times (b \\times c)") + ". Neutre : " + N("a \\times 1 = a") + ". Absorbant : " + N("a \\times 0 = 0") + ". "
                       "Distributivité : " + N("a \\times (b + c) = a \\times b + a \\times c") + " et " + N("a \\times (b - c) = a \\times b - a \\times c") + "."),
    rule("Carré et cube", N("a^2 = a \\times a") + " et " + N("a^3 = a \\times a \\times a") + ". L'aire d'un carré de côté " + N("c") + " est " + N("c^2") + ", le volume d'un cube d'arête " + N("c") + " est " + N("c^3") + "."),
    para("Les erreurs à éviter : mal compter les chiffres après la virgule du produit ; croire qu'une multiplication agrandit toujours ; ajouter un zéro en multipliant un décimal par 10 ; confondre " + N("a^2") + " avec " + N("2a") + "."),
]

CONCEPTS = {
    "produit": ("Multiplier deux décimaux", "produit"),
    "decalage": ("Multiplier par 10, 100, 1 000, 0,1, 0,01", "decalage"),
    "proprietes": ("Propriétés et calcul efficace", "proprietes"),
    "puissances": ("Carré et cube", "puissances"),
    "problemes": ("Résoudre un problème", "produit"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    plural = lambda n, word: word if n < 2 else word + "s"

    # 1. a decimal times a whole number
    n, x = rng.randint(2, 9), rand_decimal(rng, 1, 9, 1)
    first, second = (n, x) if rng.random() < 0.5 else (x, n)
    questions.append(number("a1", "produit", "Calcule " + N(f"{show(first)} \\times {show(second)}") + ".", n * x, 1,
                            ["Oublie la virgule, multiplie, puis compte les chiffres après la virgule."],
                            [f"Sans la virgule : {int(x * 10)} × {n} = {int(x * 10) * n}.", f"Le produit a 1 chiffre après la virgule : {show(n * x)}."], form="decimal"))

    # 2. two decimals with one decimal each
    x, y = rand_decimal(rng, 1, 9, 1), rand_decimal(rng, 0, 9, 1)
    questions.append(number("a2", "produit", "Calcule " + N(f"{show(x)} \\times {show(y)}") + ".", x * y, 2,
                            ["Multiplie sans les virgules, puis place la virgule avec 1 + 1 chiffres après elle."],
                            [f"Sans les virgules : {int(x * 10)} × {int(y * 10)} = {int(x * 10) * int(y * 10)}.", f"Il y a 1 + 1 = 2 chiffres après la virgule : {show(x * y)}."]))

    # 3. two decimals with two and one decimals
    x, y = rand_decimal(rng, 1, 9, 2), rand_decimal(rng, 1, 5, 1)
    questions.append(number("a3", "produit", "Calcule " + N(f"{show(x)} \\times {show(y)}") + ".", x * y, 3,
                            ["Multiplie sans les virgules, puis place la virgule avec 2 + 1 chiffres après elle."],
                            [f"Sans les virgules : {int(x * 100)} × {int(y * 10)} = {int(x * 100) * int(y * 10)}.", f"Il y a 2 + 1 = 3 chiffres après la virgule : {show(x * y)}."]))

    # 4. an estimate
    x, y = rand_decimal(rng, 10, 40, 1), rand_decimal(rng, 2, 9, 1)
    estimate = round_unit(x) * round_unit(y)
    questions.append(number("a4", "produit", "Estime " + N(f"{show(x)} \\times {show(y)}") + " en arrondissant chaque facteur à l'unité la plus proche.", Fraction(estimate), 2,
                            ["Regarde le chiffre des dixièmes de chaque facteur : 0 à 4 on garde, 5 à 9 on ajoute 1."],
                            [f"{show(x)} devient {round_unit(x)} et {show(y)} devient {round_unit(y)}.", f"{round_unit(x)} × {round_unit(y)} = {estimate}."]))

    # 5. shift right
    power = rng.choice([10, 100, 1000])
    x = rand_decimal(rng, 0, 99, rng.choice([1, 2, 3]))
    questions.append(number("a5", "decalage", "Calcule " + N(f"{show(x)} \\times {power}") + ".", x * power, 1,
                            ["Dans quel sens se déplace la virgule ? De combien de rangs ?"],
                            [f"Multiplier par {power}, c'est déplacer la virgule de {len(str(power)) - 1} {plural(len(str(power)) - 1, 'rang')} vers la droite.", f"{show(x)} × {power} = {show(x * power)}."]))

    # 6. shift left
    small = rng.choice([Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000)])
    x = Fraction(rng.randint(11, 999)) if rng.random() < 0.5 else rand_decimal(rng, 1, 99, 1)
    questions.append(number("a6", "decalage", "Calcule " + N(f"{show(x)} \\times {show(small)}") + ".", x * small, 2,
                            ["Multiplier par un nombre comme 0,1 ou 0,01, c'est déplacer la virgule vers la gauche."],
                            [f"Multiplier par {show(small)}, c'est déplacer la virgule de {len(str(small.denominator)) - 1} {plural(len(str(small.denominator)) - 1, 'rang')} vers la gauche.", f"{show(x)} × {show(small)} = {show(x * small)}."]))

    # 7. find the missing power of ten
    factor = rng.choice([Fraction(10), Fraction(100), Fraction(1000), Fraction(1, 10), Fraction(1, 100)])
    x = rand_decimal(rng, 1, 99, 2)
    questions.append(number("a7", "decalage", "Par quel nombre faut-il multiplier " + N(show(x)) + " pour obtenir " + N(show(x * factor)) + " ?", factor, 3,
                            ["Compare les deux nombres : la virgule s'est déplacée de combien de rangs, et dans quel sens ?"],
                            [f"Pour passer de {show(x)} à {show(x * factor)}, la virgule se déplace vers la {'droite' if factor > 1 else 'gauche'}.", f"Il faut multiplier par {show(factor)}."]))

    # 8. efficient calculation
    a, c = rng.choice([(4, 25), (25, 4), (2, 50), (50, 2), (5, 20), (20, 5)])
    b = rand_decimal(rng, 2, 9, 1)
    questions.append(number("a8", "proprietes", "Calcule efficacement " + N(f"{a} \\times {show(b)} \\times {c}") + ".", 100 * b, 2,
                            ["Quels deux facteurs ont un produit facile à retenir ?"],
                            [f"{a} × {c} = 100, donc le produit est 100 × {show(b)} (commutativité et associativité).", f"100 × {show(b)} = {show(100 * b)}."]))

    # 9. distributivity
    x = rand_decimal(rng, 2, 9, 1)
    m, delta = rng.choice([(102, 2), (101, 1), (103, 3), (99, -1), (98, -2)])
    sign = "+" if delta > 0 else "-"
    questions.append(number("a9", "proprietes", "Calcule " + N(f"{show(x)} \\times {m}") + " en utilisant la distributivité.", x * m, 3,
                            [f"Écris {m} comme 100 {sign} {abs(delta)}."],
                            [f"{m} = 100 {sign} {abs(delta)}, donc {show(x)} × {m} = {show(x)} × 100 {sign} {show(x)} × {abs(delta)}.",
                             f"{show(x * 100)} {sign} {show(x * abs(delta))} = {show(x * m)}."]))

    # 10. square or cube
    if rng.random() < 0.5:
        base = rand_decimal(rng, 1, 9, 1)
        questions.append(number("a10", "puissances", "Calcule " + N(f"({show(base)})^2" if base.denominator != 1 else f"{show(base)}^2") + ".", base * base, 2,
                                ["Le carré est le nombre multiplié par lui-même."],
                                [f"({show(base)})² = {show(base)} × {show(base)}.", f"Sans les virgules : {int(base * 10)} × {int(base * 10)} = {int(base * 10) ** 2}.", f"2 chiffres après la virgule : {show(base * base)}."]))
    else:
        base = rng.choice([Fraction(2, 10), Fraction(3, 10), Fraction(5, 10), Fraction(11, 10), Fraction(12, 10), Fraction(2), Fraction(3), Fraction(4), Fraction(5)])
        questions.append(number("a10", "puissances", "Calcule " + N(f"({show(base)})^3" if base.denominator != 1 else f"{show(base)}^3") + ".", base**3, 3,
                                ["Le cube est le nombre écrit trois fois dans un produit."],
                                [f"{show(base)}³ = {show(base)} × {show(base)} × {show(base)}.", f"{show(base)} × {show(base)} = {show(base * base)}, puis {show(base * base)} × {show(base)} = {show(base**3)}."]))

    # 11. a problem
    if rng.random() < 0.5:
        length, width = rand_decimal(rng, 5, 30, 1), rand_decimal(rng, 2, 9, 1)
        questions.append(number("a11", "problemes", f"Un rectangle mesure {show(length)} m de long et {show(width)} m de large. Quelle est son aire, en m² ?", length * width, 3,
                                ["L'aire d'un rectangle est longueur × largeur."],
                                [f"Aire = {show(length)} × {show(width)}.", f"Sans les virgules : {int(length * 10)} × {int(width * 10)} = {int(length * 10) * int(width * 10)}, avec 2 chiffres après la virgule : {show(length * width)} m²."],
                                units=["m2", "m²"]))
    else:
        price, quantity = rng.choice(range(400, 1501, 50)), rng.choice([Fraction(k, 10) for k in range(15, 46)])
        questions.append(number("a11", "problemes", f"Le kilogramme de mangues coûte {price} F. Awa en achète {show(quantity)} kg. Combien paie-t-elle, en F ?", price * quantity, 3,
                                ["Le prix est le prix d'un kilogramme multiplié par le nombre de kilogrammes."],
                                [f"Prix = {show(quantity)} × {price}.", f"Sans la virgule : {int(quantity * 10)} × {price} = {int(quantity * 10) * price}, avec 1 chiffre après la virgule : {show(price * quantity)} F."], units=["F"]))

    # 12. multiplying by a number smaller than one
    whole, f = rng.randint(5, 20), rng.choice([Fraction(2, 10), Fraction(3, 10), Fraction(5, 10), Fraction(8, 10), Fraction(9, 10)])
    options = ["Elle a raison : multiplier agrandit toujours",
               f"Elle a tort : {show(f)} est plus petit que 1, donc le produit est plus petit que {whole}",
               "Elle a tort : on ne peut pas multiplier par un nombre à virgule"]
    order = [0, 1, 2]
    rng.shuffle(order)
    shown_product = N(f"{whole} \\times {show(f)}")
    questions.append(choice("a12", "produit", f"Léa dit : « {shown_product} est plus grand que {whole} parce qu'on multiplie ». Quelle est la bonne réponse ?",
                            [options[i] for i in order], order.index(1), 3,
                            ["Calcule le produit et compare-le à " + str(whole) + "."],
                            [f"{whole} × {show(f)} = {show(whole * f)}.", f"{show(whole * f)} est plus petit que {whole} : multiplier par un nombre plus petit que 1 rend plus petit."],
                            wrong={order.index(0): "Multiplier n'agrandit pas toujours : multiplier par un nombre plus petit que 1 rend plus petit.",
                                   order.index(2): "On peut multiplier par un nombre décimal, comme on l'a fait dans ce chapitre."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=2, title="Multiplier des nombres décimaux", language="fr",
    intro="Pour calculer le prix de 2,5 m de tissu, l'aire d'un champ ou la masse de plusieurs sacs, on multiplie des nombres décimaux. Ce chapitre t'apprend à multiplier sans te tromper de virgule, "
          "à multiplier très vite par 10, 100, 0,1 ou 0,01, à choisir l'ordre des facteurs pour calculer plus facilement, et à calculer le carré et le cube d'un nombre.",
    objectives=["Multiplier deux nombres décimaux en colonnes et placer correctement la virgule, estimer un produit.",
                "Multiplier un nombre décimal par 10, 100, 1 000, 0,1, 0,01 et 0,001 en déplaçant la virgule, et convertir des longueurs.",
                "Connaître les propriétés de la multiplication et les utiliser pour calculer efficacement.",
                "Calculer le carré et le cube d'un nombre décimal, et les relier à l'aire d'un carré et au volume d'un cube.",
                "Résoudre des problèmes de prix, d'aire et de volume qui utilisent des multiplications."],
    prerequisites=[{"text": "Avoir terminé le chapitre sur les nombres décimaux : rang des chiffres, comparer, additionner et soustraire.", "chapter": "sn-6e-decimaux"},
                   {"text": "Multiplier des nombres entiers."}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E],
    status_note="Second chapter of the Senegal Sixième course. Its topics follow the multiplication chapter of the ADEM-Dakar booklet, with our own explanations and exercises. It has not been checked against the official Senegalese programme.",
)
