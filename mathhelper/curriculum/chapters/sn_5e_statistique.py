"""Cinquième, Statistique: the fifth chapter of the Senegal Cinquième course, written in French.

The contents follow the statistics lesson of the Côte d'Ivoire Cinquième programme (population, character and modalities, stick diagrams and bar diagrams, reading an effectif, a total
effectif and a frequency from a diagram), which was read for this chapter. Every explanation, example, diagram and exercise was written independently, with our own numbers.
Drawing a diagram on squared paper cannot be done on a screen: the diagrams are drawn by the app and read by the student, and the exercises ask for the numbers a diagram needs.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a "verify" expression that the tests evaluate.
The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .figures import Graph, figure
from .kit import N, d, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-5e-statistique"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")

# ----- Diagrams -----
BANDS = Graph(1, 20, 1, 5, "", "Effectif").bars([18, 10, 8, 4], ["Pied", "Vélo", "Bus", "Voiture"])
STICKS = Graph(1, 6, 1, 1, "Note sur 20", "Effectif").sticks([2, 3, 5, 6, 3, 1], ["8", "9", "10", "12", "14", "16"])
LEISURE = Graph(1, 40, 1, 10, "", "Fréquence (en %)").bars([25, 40, 15, 20], ["Lecture", "Musique", "Cinéma", "Sport"])

# ----- Section 1: vocabulary -----
S1 = Section(
    "vocabulaire", "Population, caractère, modalités et effectifs", 22, "vocabulaire",
    "Identifier la population et le caractère d'une enquête, dire s'il est qualitatif ou quantitatif, et lire les modalités, les effectifs et l'effectif total.",
    [
        para("Un club de classe interroge des élèves sur leur façon de venir à l'école. Pour présenter les réponses, il faut un vocabulaire précis : qui est interrogé, sur quoi, et quelles sont les réponses possibles."),
        definition("Population, individu et caractère",
                   "La population est l'ensemble des personnes ou des objets étudiés ; chacun d'eux est un individu. Le caractère est ce que l'on observe chez chaque individu. "
                   "Un caractère est qualitatif quand ses valeurs sont des mots (le mode de transport, la couleur) et quantitatif quand ses valeurs sont des nombres (une note, une taille)."),
        definition("Modalité, effectif et fréquence",
                   "Les valeurs que peut prendre le caractère s'appellent les modalités. L'effectif d'une modalité est le nombre d'individus qui la présentent ; l'effectif total est la somme de tous les effectifs. "
                   "La fréquence d'une modalité est " + N("\\dfrac{\\text{effectif}}{\\text{effectif total}}") + ", souvent écrite en pourcentage."),
        example("Exemple 1", "On interroge 40 élèves sur leur mode de transport : 18 viennent à pied, 10 à vélo, 8 en bus, 4 en voiture. Quels sont la population, le caractère et les modalités ?",
                "On répond à trois questions : qui, quoi, quelles réponses.",
                [("La population : les 40 élèves interrogés", "Chaque élève est un individu."),
                 ("Le caractère : le mode de transport", "Ses valeurs sont des mots : il est qualitatif."),
                 ("Les modalités : à pied, à vélo, en bus, en voiture", "Les effectifs sont 18, 10, 8 et 4.")],
                "Population : 40 élèves ; caractère qualitatif : mode de transport ; 4 modalités.", "18+10+8+4==40"),
        example("Exemple 2", "Les notes de 20 élèves sont : 8 (2 élèves), 9 (3), 10 (5), 12 (6), 14 (3), 16 (1). Quel est le caractère ? Quel est l'effectif total ?",
                "Les notes sont des nombres : le caractère est quantitatif.",
                [("Le caractère : la note sur 20", "Il est quantitatif : ses valeurs sont des nombres."),
                 (N("2 + 3 + 5 + 6 + 3 + 1") + " = " + N("20"), "L'effectif total est la somme des effectifs.")],
                "Caractère quantitatif ; effectif total " + N("20") + ".", "2+3+5+6+3+1==20"),
        example("Exemple 3", "Dans l'enquête sur les notes, quelle est la fréquence de la note 12 ?",
                "La fréquence est l'effectif de la modalité divisé par l'effectif total.",
                [(N("\\dfrac{6}{20} = 0,3"), "6 élèves sur 20."),
                 (N("0,3 = 30\\ \\%"), "En pourcentage : 30 %.")],
                N("30\\ \\%") + ".", "d('6')/20==d('0,3')"),
        example("Exemple 4", "Dans l'enquête sur le transport, quelle est la fréquence de la modalité « à vélo » ?",
                "10 élèves sur 40.",
                [(N("\\dfrac{10}{40} = 0,25"), "10 ÷ 40."),
                 (N("0,25 = 25\\ \\%"), "En pourcentage : 25 %.")],
                N("25\\ \\%") + ".", "d('10')/40==d('0,25')"),
        warning("Ne confonds pas la population (les individus que l'on interroge) et le caractère (ce que l'on observe). Et l'effectif est un nombre d'individus, pas une note : « 12 » est une modalité du caractère « note », et son effectif est 6."),
    ],
    [
        choice("s1-g1", "vocabulaire", "On demande à 30 élèves leur sport préféré. Quelle est la population ?", ["Les 30 élèves", "Le sport préféré", "Les sports possibles"], 0,
               hints=["Qui est interrogé ?"], solution=["La population est l'ensemble des 30 élèves interrogés."], wrong={1: "Le sport préféré est le caractère.", 2: "Les sports possibles sont les modalités."}),
        choice("s1-g2", "vocabulaire", "On mesure la taille de 25 élèves. Le caractère « taille » est :", ["qualitatif", "quantitatif"], 1,
               hints=["Les valeurs sont-elles des mots ou des nombres ?"], solution=["Les tailles sont des nombres : le caractère est quantitatif."], wrong={0: "Un caractère qualitatif a des mots pour valeurs."}),
        choice("s1-g3", "vocabulaire", "On demande la couleur des yeux. Le caractère « couleur des yeux » est :", ["qualitatif", "quantitatif"], 0,
               hints=["Marron, noir... sont des mots."], solution=["Les valeurs sont des mots : le caractère est qualitatif."], wrong={1: "Une couleur n'est pas un nombre."}),
        number("s1-g4", "vocabulaire", "Les effectifs d'une enquête sont 7, 12, 9 et 12. Quel est l'effectif total ?", Fraction(40), hints=["Additionne les effectifs."], solution=["7 + 12 + 9 + 12 = 40."]),
        number("s1-g5", "vocabulaire", "Sur 40 élèves, 8 viennent en bus. Quelle est la fréquence en pourcentage de la modalité « en bus », en % ?", Fraction(20), units=["%"], hints=["8 ÷ 40."], solution=["8 ÷ 40 = 0,2 = 20 %."]),
    ])

# ----- Section 2: bar diagrams -----
S2 = Section(
    "bandes", "Le diagramme à bandes", 24, "bandes",
    "Lire un diagramme à bandes, retrouver les effectifs, l'effectif total et les fréquences, et savoir comment le construire.",
    [
        para("Pour un caractère qualitatif, on dessine souvent un diagramme à bandes : une bande verticale par modalité, dont la hauteur est proportionnelle à l'effectif (ou à la fréquence)."),
        rule("Lire un diagramme à bandes",
             "Chaque bande correspond à une modalité. Pour lire l'effectif, on regarde la hauteur de la bande sur l'axe vertical. L'effectif total est la somme des hauteurs des bandes. La fréquence d'une modalité est son effectif divisé par l'effectif total."),
        rule("Construire un diagramme à bandes",
             "On choisit une échelle sur l'axe vertical (par exemple 1 carreau pour 2 élèves), on dessine une bande par modalité avec la même largeur et on laisse un petit espace entre les bandes. "
             "La hauteur d'une bande en carreaux est l'effectif divisé par le nombre d'élèves représentés par un carreau."),
        figure(BANDS, "Un diagramme à bandes du mode de transport de 40 élèves : à pied 18, à vélo 10, en bus 8, en voiture 4.", "Diagramme à bandes du mode de transport de 40 élèves : les hauteurs sont 18, 10, 8 et 4."),
        example("Exemple 1", "D'après le diagramme à bandes, quel est le mode de transport le plus fréquent ? Quelle est la fréquence de « à pied » ?",
                "On cherche la bande la plus haute, puis on divise son effectif par le total.",
                [("La bande la plus haute est « à pied » : effectif 18", "Elle atteint 18 sur l'axe vertical."),
                 (N("\\dfrac{18}{40} = 0,45") + " = " + N("45\\ \\%"), "L'effectif total est 18 + 10 + 8 + 4 = 40.")],
                "« À pied », avec une fréquence de " + N("45\\ \\%") + ".", "d('18')/40==d('0,45')"),
        example("Exemple 2", "Sur un diagramme, 1 carreau représente 5 élèves. Une bande a une hauteur de 6 carreaux. Quel est l'effectif de la modalité ?",
                "On multiplie le nombre de carreaux par l'échelle.",
                [(N("6 \\times 5") + " = " + N("30"), "6 carreaux de 5 élèves.")],
                N("30") + " élèves.", "6*5==30"),
        example("Exemple 3", "On veut représenter 24 élèves en football et 9 élèves en basket, avec 1 carreau pour 3 élèves. Quelle est la hauteur des deux bandes ?",
                "On divise chaque effectif par 3.",
                [(N("24 \\div 3") + " = " + N("8"), "Football : 8 carreaux."),
                 (N("9 \\div 3") + " = " + N("3"), "Basket : 3 carreaux.")],
                N("8") + " carreaux et " + N("3") + " carreaux.", "24//3==8 and 9//3==3"),
        example("Exemple 4", "Un diagramme à bandes représente les fréquences : lecture 25 %, musique 40 %, cinéma 15 %, sport 20 %. L'enquête porte sur 60 élèves. Combien d'élèves aiment la musique ?",
                "On multiplie l'effectif total par la fréquence.",
                [(N("40\\ \\% = 0,4"), "On écrit le pourcentage en nombre décimal."),
                 (N("60 \\times 0,4") + " = " + N("24"), "L'effectif est 24 élèves.")],
                N("24") + " élèves.", "60*d('0,4')==24"),
        figure(LEISURE, "Un diagramme à bandes des fréquences de quatre loisirs : lecture 25 %, musique 40 %, cinéma 15 %, sport 20 %.", "Diagramme à bandes des loisirs préférés : la somme des fréquences est de 100 %."),
        warning("Dans un diagramme à bandes, c'est la hauteur qui compte, pas la largeur ni l'aire : toutes les bandes ont la même largeur. Et la somme des fréquences d'un diagramme est toujours égale à 100 % : si elle ne l'est pas, il y a une erreur."),
    ],
    [
        number("s2-g1", "bandes", "Un diagramme à bandes a des bandes de hauteur 12, 8, 5 et 15 élèves. Quel est l'effectif total ?", Fraction(40), hints=["Additionne les hauteurs."], solution=["12 + 8 + 5 + 15 = 40."]),
        number("s2-g2", "bandes", "Dans un diagramme où 1 carreau représente 4 élèves, une bande a 7 carreaux. Quel est l'effectif ?", Fraction(28), hints=["7 × 4."], solution=["7 × 4 = 28."]),
        number("s2-g3", "bandes", "On veut représenter 36 élèves avec 1 carreau pour 4 élèves. Combien de carreaux pour la bande ?", Fraction(9), hints=["36 ÷ 4."], solution=["36 ÷ 4 = 9 carreaux."]),
        number("s2-g4", "bandes", "Sur 80 élèves, la fréquence de la modalité « musique » est 35 %. Quel est son effectif ?", Fraction(28), hints=["80 × 0,35."], solution=["80 × 0,35 = 28."]),
        number("s2-g5", "bandes", "Les fréquences d'un diagramme sont 30 %, 25 % et 20 %. La dernière modalité a quelle fréquence, en % ?", Fraction(25), units=["%"], hints=["La somme est 100 %."], solution=["100 − (30 + 25 + 20) = 25 %."]),
    ])

# ----- Section 3: stick diagrams -----
S3 = Section(
    "batons", "Le diagramme en bâtons", 24, "batons",
    "Lire un diagramme en bâtons pour un caractère quantitatif, retrouver les effectifs, l'effectif total et les fréquences, et calculer la moyenne simple d'une série.",
    [
        para("Pour un caractère quantitatif comme une note, on dessine souvent un diagramme en bâtons : un bâton vertical à l'abscisse de chaque valeur, dont la hauteur est l'effectif."),
        rule("Lire un diagramme en bâtons",
             "Chaque bâton correspond à une valeur du caractère (on lit la valeur sous le bâton) et sa hauteur donne l'effectif de cette valeur. L'effectif total est la somme des hauteurs. "
             "La fréquence d'une valeur est son effectif divisé par l'effectif total. Les bâtons sont rangés dans l'ordre croissant des valeurs."),
        figure(STICKS, "Un diagramme en bâtons des notes de 20 élèves : la note 8 pour 2 élèves, 9 pour 3, 10 pour 5, 12 pour 6, 14 pour 3 et 16 pour 1.", "Diagramme en bâtons des notes de 20 élèves : le bâton le plus haut correspond à la note 12 (6 élèves)."),
        example("Exemple 1", "D'après le diagramme en bâtons, combien d'élèves ont eu la note 10 ? Quelle est la note la plus fréquente ?",
                "On lit la hauteur du bâton situé sous la valeur 10, puis on cherche le bâton le plus haut.",
                [("Le bâton de la note 10 a pour hauteur 5", "5 élèves ont eu 10."),
                 ("Le bâton le plus haut est celui de la note 12, de hauteur 6", "C'est la note la plus fréquente.")],
                N("5") + " élèves ont eu 10 ; la note la plus fréquente est " + N("12") + ".", "max([2,3,5,6,3,1])==6"),
        example("Exemple 2", "Combien d'élèves ont eu au moins 12 ? Quelle est leur fréquence ?",
                "On additionne les effectifs des notes 12, 14 et 16, puis on divise par 20.",
                [(N("6 + 3 + 1") + " = " + N("10"), "10 élèves ont au moins 12."),
                 (N("\\dfrac{10}{20} = 0,5") + " = " + N("50\\ \\%"), "La fréquence est 50 %.")],
                N("10") + " élèves, soit " + N("50\\ \\%") + ".", "6+3+1==10 and d('10')/20==d('0,5')"),
        example("Exemple 3", "Calculer la moyenne des notes : 8 (2 élèves), 9 (3), 10 (5), 12 (6), 14 (3), 16 (1).",
                "On multiplie chaque note par son effectif, on additionne, puis on divise par l'effectif total.",
                [(N("8 \\times 2 + 9 \\times 3 + 10 \\times 5 + 12 \\times 6 + 14 \\times 3 + 16 \\times 1"), "Chaque note compte autant de fois que d'élèves."),
                 (N("16 + 27 + 50 + 72 + 42 + 16") + " = " + N("223"), "Somme de toutes les notes."),
                 (N("223 \\div 20") + " = " + N("11,15"), "Divisé par 20 élèves.")],
                "La moyenne est " + N("11,15") + ".", "8*2+9*3+10*5+12*6+14*3+16*1==223 and d('223')/20==d('11,15')"),
        example("Exemple 4", "Sur un diagramme en bâtons, les hauteurs sont 4, 7, 9 et 5 pour les valeurs 1, 2, 3 et 4. Quel est l'effectif total ? Quelle est la fréquence de la valeur 3 ?",
                "On additionne les hauteurs, puis on divise la hauteur du bâton 3 par le total.",
                [(N("4 + 7 + 9 + 5") + " = " + N("25"), "Effectif total."),
                 (N("\\dfrac{9}{25} = 0,36") + " = " + N("36\\ \\%"), "9 sur 25.")],
                N("25") + ", et " + N("36\\ \\%") + ".", "4+7+9+5==25 and d('9')/25==d('0,36')"),
        warning("Sous un bâton, on lit la valeur du caractère ; sa hauteur donne l'effectif. Ne confonds pas les deux : le bâton de la note 12 a pour hauteur 6, et non 12. Et pour la moyenne, il faut multiplier chaque valeur par son effectif avant de diviser par l'effectif total."),
    ],
    [
        number("s3-g1", "batons", "Un diagramme en bâtons a des bâtons de hauteur 3, 6, 8 et 3. Quel est l'effectif total ?", Fraction(20), hints=["Additionne les hauteurs."], solution=["3 + 6 + 8 + 3 = 20."]),
        number("s3-g2", "batons", "Dans une série de 25 notes, le bâton de la note 10 a pour hauteur 5. Quelle est la fréquence de la note 10, en % ?", Fraction(20), units=["%"], hints=["5 ÷ 25."], solution=["5 ÷ 25 = 0,2 = 20 %."]),
        number("s3-g3", "batons", "Notes : 6 (1 élève), 8 (3 élèves), 10 (4 élèves), 14 (2 élèves). Combien d'élèves ont au moins 10 ?", Fraction(6), hints=["Notes 10 et 14."], solution=["4 + 2 = 6 élèves."]),
        number("s3-g4", "batons", "Notes : 10 (2 élèves), 12 (3 élèves), 16 (5 élèves). Quelle est la moyenne ?", d("13,6"), hints=["Somme des notes ÷ 10."], solution=["10 × 2 + 12 × 3 + 16 × 5 = 20 + 36 + 80 = 136.", "136 ÷ 10 = 13,6."]),
        choice("s3-g5", "batons", "Sur un diagramme en bâtons, la hauteur d'un bâton représente :", ["l'effectif de la valeur", "la valeur du caractère", "la fréquence en pourcentage seulement"], 0,
               hints=["La valeur se lit sous le bâton."], solution=["La hauteur du bâton est l'effectif de la valeur."], wrong={1: "La valeur se lit sous le bâton.", 2: "On peut aussi lire des fréquences, mais seulement si l'axe est gradué en fréquences."}),
    ])

# ----- Section 4: problems -----
S4 = Section(
    "problemes", "Résoudre des problèmes de statistique", 22, "problemes",
    "Compléter un tableau d'effectifs et de fréquences, passer d'une fréquence à un effectif, et comparer deux séries.",
    [
        para("Un tableau d'effectifs et de fréquences résume une enquête. Il permet de compléter ce qui manque, de dessiner un diagramme et de comparer deux groupes de tailles différentes."),
        example("Exemple 1", "Transport de 50 élèves. À pied : effectif 20. À vélo : fréquence 30 %. En bus : 10 élèves de moins qu'à pied. Le reste des 50 élèves vient en voiture. Calculer les effectifs.",
                "On déduit chaque effectif à partir du total, puis on calcule les fréquences.",
                [("À pied : 20. À vélo : 30 % de 50 = 15", N("50 \\times 0,3") + " = " + N("15") + "."),
                 ("En bus : 10 de moins qu'à pied : 20 − 10 = 10", "Reste à vérifier avec le total."),
                 (N("20 + 15 + 10") + " = " + N("45"), "Il manque 5 élèves : la quatrième modalité compte 5 élèves, en voiture.")],
                "À pied 20, à vélo 15, en bus 10, en voiture 5.", "20+15+10+5==50 and 50*d('0,3')==15"),
        example("Exemple 2", "Deux classes ont voté pour leur sport : la classe A (25 élèves) compte 10 amateurs de football, la classe B (40 élèves) en compte 14. Dans quelle classe le football est-il le plus populaire ?",
                "On compare les fréquences, pas les effectifs.",
                [(N("\\dfrac{10}{25} = 0,4") + " = " + N("40\\ \\%"), "Classe A."),
                 (N("\\dfrac{14}{40} = 0,35") + " = " + N("35\\ \\%"), "Classe B."),
                 ("40 % est plus grand que 35 %", "Le football est plus populaire dans la classe A.")],
                "Dans la classe A (40 % contre 35 %).", "d('10')/25>d('14')/40"),
        example("Exemple 3", "Une enquête sur 200 personnes donne : musique 35 %, sport 25 %, lecture 30 %, autres. Combien de personnes sont dans « autres » ?",
                "On trouve la fréquence manquante, puis on la multiplie par 200.",
                [(N("100 - (35 + 25 + 30)") + " = " + N("10"), "« Autres » : 10 %."),
                 (N("200 \\times 0,1") + " = " + N("20"), "20 personnes.")],
                N("20") + " personnes.", "100-(35+25+30)==10 and 200*d('0,1')==20"),
        example("Exemple 4", "On a une série de notes : 5, 8, 8, 10, 12, 12, 12, 15. Quelle est la modalité de plus grand effectif ? Quelle est la moyenne ?",
                "On compte les effectifs, puis on additionne toutes les notes et on divise par 8.",
                [("Effectifs : 5 (1), 8 (2), 10 (1), 12 (3), 15 (1)", "La note 12 revient 3 fois : c'est la plus fréquente."),
                 (N("5 + 8 + 8 + 10 + 12 + 12 + 12 + 15") + " = " + N("82"), "Somme des 8 notes."),
                 (N("82 \\div 8") + " = " + N("10,25"), "La moyenne.")],
                "La note 12 ; moyenne " + N("10,25") + ".", "5+8+8+10+12+12+12+15==82 and d('82')/8==d('10,25')"),
        warning("Pour comparer deux groupes de tailles différentes, passe aux fréquences : 14 amateurs sur 40 élèves est moins que 10 sur 25, même si 14 est plus grand que 10. Et vérifie toujours que la somme des effectifs est l'effectif total et que la somme des fréquences est 100 %."),
    ],
    [
        number("s4-g1", "problemes", "Une enquête sur 60 élèves donne : lecture 25 %, musique 40 %, cinéma 15 %, sport le reste. Combien d'élèves aiment le sport ?", Fraction(12), hints=["Cherche la fréquence du sport."], solution=["100 − (25 + 40 + 15) = 20 %.", "60 × 0,2 = 12 élèves."]),
        choice("s4-g2", "problemes", "Classe A : 12 amateurs de basket sur 30 élèves. Classe B : 14 amateurs sur 35 élèves. Que peut-on dire ?", ["Même fréquence (40 %)", "A a la plus grande fréquence", "B a la plus grande fréquence"], 0,
               hints=["Calcule 12 ÷ 30 et 14 ÷ 35."], solution=["12 ÷ 30 = 0,4 et 14 ÷ 35 = 0,4 : même fréquence."], wrong={1: "Les deux fréquences sont égales à 40 %.", 2: "Les deux fréquences sont égales à 40 %."}),
        number("s4-g3", "problemes", "Notes : 6, 8, 8, 10, 13. Quelle est la moyenne ?", Fraction(9), hints=["Somme ÷ 5."], solution=["6 + 8 + 8 + 10 + 13 = 45.", "45 ÷ 5 = 9."]),
        number("s4-g4", "problemes", "Sur 150 élèves, 36 % viennent en bus. Combien d'élèves viennent en bus ?", Fraction(54), hints=["150 × 0,36."], solution=["150 × 0,36 = 54."]),
        number("s4-g5", "problemes", "Les effectifs d'une enquête sont 15, 25 et le reste. L'effectif total est 60. Quel est le reste ?", Fraction(20), hints=["60 − 40."], solution=["60 − (15 + 25) = 20."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    choice("p1", "vocabulaire", "On note le nombre de frères et sœurs de 28 élèves. Le caractère est :", ["quantitatif", "qualitatif"], 0, 1, ["Les valeurs sont des nombres."], ["Le nombre de frères et sœurs est un nombre : quantitatif."], wrong={1: "Ce n'est pas un mot."}),
    choice("p2", "vocabulaire", "On demande la couleur préférée de 35 élèves. Le caractère est :", ["quantitatif", "qualitatif"], 1, 1, ["Les valeurs sont des mots."], ["Les couleurs sont des mots : qualitatif."], wrong={0: "Ce n'est pas un nombre."}),
    choice("p3", "vocabulaire", "Dans l'enquête « mode de transport de 50 élèves », que sont les 50 élèves ?", ["La population", "Le caractère", "Les modalités"], 0, 1, ["Qui est interrogé ?"], ["L'ensemble des élèves interrogés est la population."], wrong={1: "Le caractère est le mode de transport.", 2: "Les modalités sont : à pied, vélo, bus..."}),
    number("p4", "vocabulaire", "Combien de modalités a le caractère « mode de transport » avec : à pied, à vélo, en bus, en voiture, en moto ?", Fraction(5), 1, ["Compte-les."], ["5 modalités."]),
    number("p5", "vocabulaire", "Les effectifs sont 11, 6, 8 et 15. Quel est l'effectif total ?", Fraction(40), 1, ["Additionne."], ["11 + 6 + 8 + 15 = 40."]),
    number("p6", "vocabulaire", "Sur 50 élèves, 15 aiment la lecture. Quelle est la fréquence, en % ?", Fraction(30), 1, ["15 ÷ 50."], ["15 ÷ 50 = 0,3 = 30 %."], units=["%"]),
    number("p7", "vocabulaire", "Sur 80 personnes, la fréquence de la modalité « oui » est 0,35. Quel est son effectif ?", Fraction(28), 2, ["80 × 0,35."], ["80 × 0,35 = 28."]),
    number("p8", "vocabulaire", "Une modalité a un effectif de 18 et une fréquence de 0,45. Quel est l'effectif total ?", Fraction(40), 3, ["18 ÷ 0,45."], ["18 ÷ 0,45 = 40."]),
    number("p9", "bandes", "Un diagramme à bandes a des bandes de hauteur 9, 14, 6 et 11. Quel est l'effectif total ?", Fraction(40), 1, ["Additionne les hauteurs."], ["9 + 14 + 6 + 11 = 40."]),
    number("p10", "bandes", "Dans un diagramme où 1 carreau représente 3 élèves, une bande a 9 carreaux. Quel est l'effectif ?", Fraction(27), 1, ["9 × 3."], ["27."]),
    number("p11", "bandes", "On veut représenter 45 élèves avec 1 carreau pour 5 élèves. Combien de carreaux ?", Fraction(9), 1, ["45 ÷ 5."], ["9 carreaux."]),
    number("p12", "bandes", "Les fréquences d'un diagramme sont 20 %, 35 %, 15 % et le reste. Quelle est la dernière fréquence, en % ?", Fraction(30), 2, ["La somme est 100 %."], ["100 − (20 + 35 + 15) = 30 %."], units=["%"]),
    number("p13", "bandes", "Sur 120 élèves, la fréquence de la modalité « football » est 45 %. Quel est son effectif ?", Fraction(54), 2, ["120 × 0,45."], ["120 × 0,45 = 54."]),
    number("p14", "bandes", "Un diagramme à bandes de fréquences a une bande de hauteur 25 % pour 160 élèves. Quel est l'effectif de cette modalité ?", Fraction(40), 2, ["160 × 0,25."], ["40."]),
    choice("p15", "bandes", "Quelle est la somme des fréquences de toutes les modalités d'une enquête ?", ["100 %", "Cela dépend", "50 %"], 0, 1, ["Toute la population est comptée."], ["La somme est 100 % (ou 1)."], wrong={1: "Elle ne dépend pas de l'enquête.", 2: "Toute la population est comptée, soit 100 %."}),
    choice("p16", "bandes", "Karim a dessiné des bandes de largeurs différentes pour représenter les modalités. Quelle est son erreur ?", ["Toutes les bandes doivent avoir la même largeur : la hauteur seule compte", "Il ne fallait pas de bandes", "Il fallait les dessiner en rouge"], 0, 2, ["La largeur n'a pas de sens."], ["Dans un diagramme à bandes, seule la hauteur compte : les bandes ont la même largeur."], wrong={1: "Les bandes sont justement le principe.", 2: "La couleur n'a pas d'importance."}),
    number("p17", "batons", "Notes : 7 (4 élèves), 10 (6 élèves), 13 (8 élèves), 16 (2 élèves). Quel est l'effectif total ?", Fraction(20), 1, ["Additionne les effectifs."], ["4 + 6 + 8 + 2 = 20."]),
    number("p18", "batons", "Notes : 7 (4 élèves), 10 (6 élèves), 13 (8 élèves), 16 (2 élèves). Combien d'élèves ont au moins 10 ?", Fraction(16), 2, ["6 + 8 + 2."], ["16 élèves."]),
    number("p19", "batons", "Notes : 7 (4 élèves), 10 (6 élèves), 13 (8 élèves), 16 (2 élèves). Quelle est la fréquence de la note 13, en % ?", Fraction(40), 2, ["8 ÷ 20."], ["0,4 = 40 %."], units=["%"]),
    number("p20", "batons", "Notes : 7 (4 élèves), 10 (6 élèves), 13 (8 élèves), 16 (2 élèves). Quelle est la moyenne ?", d("11,2"), 3, ["Somme ÷ 20."], ["28 + 60 + 104 + 32 = 224.", "224 ÷ 20 = 11,2."]),
    number("p21", "batons", "Tailles (en cm) : 150 (3 élèves), 155 (5), 160 (2). Quelle est la taille moyenne, en cm ?", Fraction(1545, 10), 3, ["Somme ÷ 10."], ["450 + 775 + 320 = 1 545.", "1 545 ÷ 10 = 154,5."], units=["cm"]),
    number("p22", "batons", "Un diagramme en bâtons a des bâtons de hauteur 2, 5, 7, 4 et 2 pour les valeurs 0, 1, 2, 3 et 4. Quel est l'effectif total ?", Fraction(20), 1, ["Additionne."], ["20."]),
    number("p23", "batons", "Pour les valeurs 0, 1, 2, 3 et 4 d'effectifs 2, 5, 7, 4 et 2, quelle est la moyenne ?", d("1,95"), 3, ["Somme ÷ 20."], ["0 + 5 + 14 + 12 + 8 = 39.", "39 ÷ 20 = 1,95."]),
    number("p24", "batons", "Quelle est la valeur la plus fréquente pour les valeurs 0, 1, 2, 3 et 4 d'effectifs 2, 5, 7, 4 et 2 ?", Fraction(2), 1, ["Le bâton le plus haut."], ["L'effectif 7 est le plus grand : la valeur 2."]),
    choice("p25", "batons", "Sous un bâton on lit :", ["la valeur du caractère", "l'effectif", "la fréquence"], 0, 1, ["Sur l'axe horizontal."], ["Sous le bâton, on lit la valeur du caractère."], wrong={1: "L'effectif se lit par la hauteur.", 2: "Ce n'est pas la fréquence."}),
    number("p26", "problemes", "Sur 80 élèves, 20 % aiment le football, 35 % le basket, 25 % le handball, le reste l'athlétisme. Combien aiment l'athlétisme ?", Fraction(16), 2, ["Cherche la fréquence manquante."], ["100 − (20 + 35 + 25) = 20 %.", "80 × 0,2 = 16."]),
    number("p27", "problemes", "Classe A : 9 amateurs de théâtre sur 30. Classe B : 12 amateurs sur 50. Quelle est la plus grande fréquence, en % ?", Fraction(30), 3, ["Calcule 9 ÷ 30 et 12 ÷ 50."], ["30 % et 24 % : la plus grande est 30 %."], units=["%"]),
    number("p28", "problemes", "Une enquête sur 250 personnes montre que 36 % aiment le café. Combien de personnes ?", Fraction(90), 2, ["250 × 0,36."], ["90."]),
    number("p29", "problemes", "Notes : 4, 6, 6, 8, 9, 9, 9, 13. Quelle est la moyenne ?", Fraction(8), 3, ["Somme ÷ 8."], ["4 + 6 + 6 + 8 + 9 + 9 + 9 + 13 = 64.", "64 ÷ 8 = 8."]),
    number("p30", "problemes", "Dans un diagramme, une bande représente 18 élèves et sa hauteur est 6 carreaux. Combien d'élèves par carreau ?", Fraction(3), 2, ["Effectif ÷ carreaux."], ["18 ÷ 6 = 3."]),
    choice("p31", "problemes", "Léa dit : « 14 amateurs c'est plus que 10, donc le football est plus populaire dans la classe où il y a 14 amateurs ». Qu'en penses-tu ?", ["Il faut comparer les fréquences, pas les effectifs", "Elle a raison", "Il faut comparer les tailles des classes seulement"], 0, 2, ["Les classes n'ont pas la même taille."], ["On compare 14 sur le total de sa classe à 10 sur le total de l'autre."], wrong={1: "Les effectifs seuls ne suffisent pas.", 2: "Il faut les deux : effectif et total, donc la fréquence."}),
    number("p32", "problemes", "Un diagramme en bâtons compte 40 élèves. Les bâtons ont pour hauteurs 8, 12, 12 et le dernier. Quelle est la hauteur du dernier ?", Fraction(8), 1, ["40 − 32."], ["8 + 12 + 12 = 32.", "40 − 32 = 8."]),
]

SUMMARY = [
    definition("Vocabulaire", "Population : les individus étudiés. Caractère : ce qu'on observe, qualitatif (des mots) ou quantitatif (des nombres). Modalités : ses valeurs. Effectif : nombre d'individus d'une modalité. Fréquence = effectif ÷ effectif total (en %)."),
    rule("Diagrammes", "Diagramme à bandes (caractère qualitatif) : une bande par modalité, de même largeur. Diagramme en bâtons (caractère quantitatif) : un bâton par valeur, dont la hauteur est l'effectif. L'effectif total est la somme des hauteurs, les fréquences ont pour somme 100 %."),
    rule("Moyenne d'une série", "Moyenne = (somme de valeur × effectif) ÷ effectif total."),
    para("Les erreurs à éviter : confondre population et caractère ; lire la valeur au lieu de la hauteur ; comparer des effectifs de groupes de tailles différentes ; oublier que la somme des fréquences est 100 % ; oublier de multiplier par l'effectif dans une moyenne."),
]

CONCEPTS = {
    "vocabulaire": ("Population, caractère, modalités", "vocabulaire"),
    "bandes": ("Diagramme à bandes", "bandes"),
    "batons": ("Diagramme en bâtons et moyenne", "batons"),
    "problemes": ("Problèmes de statistique", "problemes"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    # 1. a character, qualitative or quantitative
    pairs = [("la couleur des yeux", 0), ("le nombre de frères et sœurs", 1), ("le mode de transport", 0), ("la taille", 1), ("le sport préféré", 0), ("la note en mathématiques", 1), ("la ville de naissance", 0), ("le nombre de livres lus", 1)]
    name, kind = rng.choice(pairs)
    questions.append(choice("a1", "vocabulaire", f"On étudie {name} de 30 élèves. Le caractère est :", ["qualitatif", "quantitatif"], kind, 1, ["Les valeurs sont-elles des mots ou des nombres ?"],
                            [("Des nombres : quantitatif." if kind else "Des mots : qualitatif.")]))
    # 2. the total effectif
    counts = [rng.randint(3, 15) for _ in range(rng.randint(3, 5))]
    questions.append(number("a2", "vocabulaire", f"Les effectifs d'une enquête sont {', '.join(str(c) for c in counts)}. Quel est l'effectif total ?", Fraction(sum(counts)), 1, ["Additionne les effectifs."], [" + ".join(str(c) for c in counts) + f" = {sum(counts)}."]))
    # 3. a frequency as a percentage
    total = rng.choice([20, 25, 40, 50, 80])
    count = rng.randint(2, total - 2)
    while (Fraction(count * 100, total)).denominator != 1:
        count = rng.randint(2, total - 2)
    questions.append(number("a3", "vocabulaire", f"Sur {total} personnes, {count} choisissent la modalité « oui ». Quelle est sa fréquence, en % ?", Fraction(count * 100, total), 2, ["Effectif ÷ effectif total, puis × 100."], [f"{count} ÷ {total} = {show(Fraction(count, total))} = {count * 100 // total} %."], units=["%"]))
    # 4. a total from a diagram
    heights = [rng.randint(3, 15) for _ in range(4)]
    questions.append(number("a4", "bandes", f"Un diagramme à bandes a des bandes de hauteur {', '.join(str(h) for h in heights)} élèves. Quel est l'effectif total ?", Fraction(sum(heights)), 1, ["Additionne les hauteurs."], [" + ".join(str(h) for h in heights) + f" = {sum(heights)}."]))
    # 5. an effectif from a scale
    scale, squares = rng.choice([2, 3, 4, 5, 10]), rng.randint(3, 12)
    questions.append(number("a5", "bandes", f"Sur un diagramme où 1 carreau représente {scale} élèves, une bande a {squares} carreaux. Quel est l'effectif ?", Fraction(scale * squares), 1, ["Carreaux × échelle."], [f"{squares} × {scale} = {scale * squares}."]))
    # 6. squares for an effectif
    scale, squares = rng.choice([2, 3, 4, 5, 10]), rng.randint(3, 12)
    questions.append(number("a6", "bandes", f"On veut représenter {scale * squares} élèves avec 1 carreau pour {scale} élèves. Combien de carreaux ?", Fraction(squares), 2, ["Effectif ÷ échelle."], [f"{scale * squares} ÷ {scale} = {squares}."]))
    # 7. an effectif from a frequency
    total = rng.choice([40, 50, 60, 80, 100, 200])
    percent = rng.choice([p for p in range(5, 90, 5) if (Fraction(p * total, 100)).denominator == 1])
    questions.append(number("a7", "bandes", f"Sur {total} élèves, la fréquence de la modalité « musique » est {percent} %. Quel est son effectif ?", Fraction(percent * total, 100), 2, ["Effectif total × fréquence."], [f"{total} × {show(Fraction(percent, 100))} = {percent * total // 100}."]))
    # 8. the missing frequency
    parts = rng.sample(range(10, 40, 5), 3)
    questions.append(number("a8", "bandes", f"Les fréquences d'un diagramme sont {parts[0]} %, {parts[1]} %, {parts[2]} % et le reste. Quelle est la dernière fréquence, en % ?", Fraction(100 - sum(parts)), 2, ["La somme est 100 %."], [f"100 − ({parts[0]} + {parts[1]} + {parts[2]}) = {100 - sum(parts)} %."], units=["%"]))
    # 9. the number of pupils above a mark
    values = sorted(rng.sample(range(5, 18), 4))
    effs = [rng.randint(1, 8) for _ in range(4)]
    threshold = values[1]
    text = ", ".join(f"{v} ({e} élèves)" for v, e in zip(values, effs))
    questions.append(number("a9", "batons", f"Notes : {text}. Combien d'élèves ont au moins {threshold} ?", Fraction(sum(e for v, e in zip(values, effs) if v >= threshold)), 2, ["Additionne les effectifs des notes concernées."],
                            ["Notes " + ", ".join(str(v) for v in values if v >= threshold) + " : " + " + ".join(str(e) for v, e in zip(values, effs) if v >= threshold) + f" = {sum(e for v, e in zip(values, effs) if v >= threshold)}."]))
    # 10. a mean
    values = rng.sample(range(5, 19), 3)
    effs = [rng.randint(1, 6) for _ in range(3)]
    total = sum(effs)
    while any(total % p == 0 and False for p in (3, 7)) or Fraction(sum(v * e for v, e in zip(values, effs)), total).denominator not in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50):
        values = rng.sample(range(5, 19), 3)
        effs = [rng.randint(1, 6) for _ in range(3)]
        total = sum(effs)
    mean = Fraction(sum(v * e for v, e in zip(values, effs)), total)
    text = ", ".join(f"{v} ({e} élèves)" for v, e in zip(values, effs))
    questions.append(number("a10", "batons", f"Notes : {text}. Quelle est la moyenne ? (Réponds par un nombre décimal exact.)", mean, 3, ["Somme de valeur × effectif, divisée par l'effectif total."],
                            [" + ".join(f"{v} × {e}" for v, e in zip(values, effs)) + f" = {sum(v * e for v, e in zip(values, effs))}.", f"{sum(v * e for v, e in zip(values, effs))} ÷ {total} = {show(mean)}."]))
    # 11. a missing effectif
    total = rng.randint(30, 80)
    known = [rng.randint(5, total // 4) for _ in range(2)]
    questions.append(number("a11", "problemes", f"Les effectifs d'une enquête sont {known[0]}, {known[1]} et le reste. L'effectif total est {total}. Quel est le reste ?", Fraction(total - sum(known)), 1, ["Retire la somme du total."], [f"{total} − ({known[0]} + {known[1]}) = {total - sum(known)}."]))
    # 12. compare two groups
    a_total, b_total = rng.choice([(20, 25), (25, 40), (30, 50), (40, 50), (20, 40)])
    a_count, b_count = rng.randint(3, a_total - 2), rng.randint(3, b_total - 2)
    while Fraction(a_count, a_total) == Fraction(b_count, b_total):
        b_count = rng.randint(3, b_total - 2)
    right = 0 if Fraction(a_count, a_total) > Fraction(b_count, b_total) else 1
    questions.append(choice("a12", "problemes", f"Classe A : {a_count} amateurs sur {a_total} élèves. Classe B : {b_count} amateurs sur {b_total} élèves. Dans quelle classe la fréquence des amateurs est-elle la plus grande ?", ["La classe A", "La classe B"], right, 2,
                            ["Compare les fréquences."], [f"A : {a_count} ÷ {a_total} ≈ {float(Fraction(a_count, a_total)):.3f}. B : {b_count} ÷ {b_total} ≈ {float(Fraction(b_count, b_total)):.3f}."]))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=5, title="La statistique : diagrammes en bandes et en bâtons", language="fr",
    intro="Pour connaître les loisirs préférés d'une classe ou la répartition des notes, on interroge des élèves et on présente les résultats dans un diagramme. "
          "Ce chapitre t'apprend le vocabulaire de la statistique, à lire des diagrammes en bandes et en bâtons, et à calculer des effectifs, des fréquences et une moyenne.",
    objectives=["Identifier une population, un caractère qualitatif ou quantitatif et ses modalités.",
                "Lire un diagramme à bandes et un diagramme en bâtons : effectifs, effectif total, fréquences.",
                "Calculer l'effectif d'une modalité à partir d'une fréquence et inversement.",
                "Calculer la moyenne d'une série et comparer des fréquences.",
                "Résoudre un problème avec un tableau d'effectifs."],
    prerequisites=[{"text": "Connaître les effectifs, les fréquences et les pourcentages.", "chapter": "sn-6e-statistique"},
                   {"text": "Calculer avec des nombres décimaux."}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Fifth chapter of the Senegal Cinquième course. Its contents follow the statistics lesson of the Côte d'Ivoire Cinquième programme (population, character, modalities, bar and stick diagrams, effectif and frequency), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. Diagrams are drawn by the app and read by the student: drawing them on squared paper is not covered. "
                "It has not been checked against the official Senegalese programme.",
)
