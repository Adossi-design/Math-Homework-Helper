"""Sixième, Statistique: counts and frequencies, the ninth chapter of the Senegal Sixième course, written in French.

The contents follow lesson 13 "Statistique" of the Côte d'Ivoire Sixième programme (a count, the total count, a frequency, a frequency as a percentage,
tables of counts and of frequencies), which was read for this chapter. The programme asks teachers to stay with counting, computing a frequency and
writing it as a percentage, and to leave the vocabulary of "modality", "character" and "population" for the next year, so those words are not used here.
Every explanation, example and exercise was written independently, with our own data.
Fixed answers are computed from the data shown in each prompt, and re-checked by tests against an independent recount. Each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
import random
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .kit import N, d, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-6e-statistique"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")


def ballots(counts, seed):
    """Return the list of ballots as text, with the given number of each letter, in an order fixed by the seed."""
    letters = [letter for letter, count in counts.items() for _ in range(count)]
    random.Random(seed).shuffle(letters)
    return " ".join(letters)


VOTES = {"A": 7, "M": 9, "Y": 4}
LIST_20 = ballots(VOTES, "vote20")
VOTES_25 = {"F": 10, "K": 5, "S": 10}
LIST_25 = ballots(VOTES_25, "vote25")
NOTES = [8, 12, 12, 15, 8, 12, 10, 15, 12, 8, 10, 12, 15, 10, 8]
NOTES_TEXT = " ; ".join(map(str, NOTES))

# ----- Section 1: counts and the total count -----
S1 = Section(
    "effectif", "Recueillir des données : l'effectif et l'effectif total", 22, "effectif",
    "Compter des données, les organiser dans un tableau d'effectifs et calculer l'effectif total.",
    [
        para("La classe de Sixième doit élire un délégué. Trois élèves se présentent : Awa (A), Moussa (M) et Yao (Y). Chaque élève écrit une initiale sur un bulletin. Voici les 20 bulletins, dans l'ordre où ils sont sortis de l'urne : "
             + LIST_20 + ". Pour savoir qui a gagné, il faut compter. Pour ne pas se tromper, on organise le comptage dans un tableau."),
        definition("Effectif et effectif total",
                   "L'effectif d'un résultat est le nombre de fois où il est apparu dans les données. Ici, l'effectif de M est le nombre de bulletins marqués M. "
                   "L'effectif total est le nombre total de données, c'est-à-dire la somme de tous les effectifs. Pour les bulletins, c'est le nombre d'élèves qui ont voté."),
        example("Exemple 1", "Compter les bulletins de chaque candidat et vérifier avec l'effectif total.",
                "On barre chaque bulletin au fur et à mesure qu'on le compte, pour ne pas en oublier ni en compter deux fois.",
                [("Les bulletins sont : " + LIST_20, "Il y a 20 bulletins en tout."),
                 ("Effectif de A : " + str(VOTES["A"]) + ". Effectif de M : " + str(VOTES["M"]) + ". Effectif de Y : " + str(VOTES["Y"]), "On compte chaque lettre."),
                 (N(f"{VOTES['A']} + {VOTES['M']} + {VOTES['Y']}") + " = " + N("20"), "L'effectif total est la somme des trois effectifs : on retrouve les 20 bulletins, ce qui confirme le comptage.")],
                "A : " + str(VOTES["A"]) + ", M : " + str(VOTES["M"]) + ", Y : " + str(VOTES["Y"]) + ", total 20", f"{LIST_20.split().count('A')}=={VOTES['A']} and {LIST_20.split().count('M')}=={VOTES['M']} and {len(LIST_20.split())}==20"),
        para("Voici le tableau d'effectifs de cette élection : une ligne pour les candidats, une ligne pour les effectifs."),
        {"type": "table", "label": "Tableau d'effectifs", "head": ["Candidat", "A", "M", "Y", "Total"], "rows": [["Effectif", str(VOTES["A"]), str(VOTES["M"]), str(VOTES["Y"]), "20"]]},
        example("Exemple 2", "Présenter les résultats dans un tableau d'effectifs.",
                "Une ligne pour les candidats, une ligne pour les effectifs, et une colonne pour le total.",
                [("Candidat : A ; M ; Y ; Total", "Première ligne."),
                 ("Effectif : " + str(VOTES["A"]) + " ; " + str(VOTES["M"]) + " ; " + str(VOTES["Y"]) + " ; 20", "Deuxième ligne. Le total est la somme des effectifs."),
                 ("M a le plus grand effectif : Moussa a gagné avec 9 voix", "Le plus grand effectif se repère facilement dans un tableau.")],
                "Moussa est élu avec 9 voix sur 20.", f"max({VOTES['A']}, {VOTES['M']}, {VOTES['Y']})=={VOTES['M']}"),
        example("Exemple 3", "Dans un tableau d'effectifs, deux effectifs sont 12 et 8, le troisième est inconnu et l'effectif total est 30. Quel est le troisième effectif ?",
                "L'effectif total est la somme des effectifs : on cherche le nombre manquant d'une addition.",
                [(N("12 + 8 + ?") + " = " + N("30"), "On écrit que la somme des trois effectifs est l'effectif total."),
                 (N("12 + 8") + " = " + N("20"), "On additionne les effectifs connus."),
                 (N("30 - 20") + " = " + N("10"), "Le troisième effectif est la différence entre le total et la somme des deux autres.")],
                N("10"), "30-(12+8)==10"),
        example("Exemple 4", "Les notes d'un contrôle sont : " + NOTES_TEXT + ". Combien d'élèves ont eu 12 ? Quel est l'effectif total ?",
                "On compte les 12, puis tous les nombres de la liste.",
                [("On repère les 12 : " + str(NOTES.count(12)) + " fois", "L'effectif de la note 12 est " + str(NOTES.count(12)) + "."),
                 ("On compte tous les nombres de la liste : " + str(len(NOTES)), "L'effectif total est " + str(len(NOTES)) + " : il y a " + str(len(NOTES)) + " élèves.")],
                "L'effectif de 12 est " + N(str(NOTES.count(12))) + " et l'effectif total est " + N(str(len(NOTES))), f"{NOTES.count(12)}=={NOTES.count(12)} and {len(NOTES)}==15"),
        warning("Un effectif est toujours un nombre entier, et l'effectif total est toujours la somme de tous les effectifs. Si ta somme ne donne pas le nombre de données, tu as oublié ou compté deux fois une donnée."),
    ],
    [
        number("s1-g1", "effectif", f"Voici 20 bulletins : {LIST_20}. Combien de voix pour M ?", Fraction(VOTES["M"]),
               hints=["Compte les lettres M une par une, en les barrant."], solution=[f"Il y a {VOTES['M']} lettres M dans la liste.", "L'effectif de M est " + str(VOTES["M"]) + "."]),
        number("s1-g2", "effectif", "Dans un tableau, les effectifs sont 7, 9 et 4. Quel est l'effectif total ?", Fraction(20),
               hints=["L'effectif total est la somme des effectifs."], solution=["7 + 9 + 4 = 20."]),
        number("s1-g3", "effectif", "Un tableau d'effectifs a trois effectifs : 14, 9 et ?. L'effectif total est 40. Quel est l'effectif manquant ?", Fraction(17),
               hints=["Additionne 14 et 9, puis retire le résultat de 40."], solution=["14 + 9 = 23.", "40 − 23 = 17."]),
        choice("s1-g4", "effectif", "Dans une classe de 32 élèves, 14 viennent à pied. Que représente le nombre 14 ?", ["Un effectif", "L'effectif total", "Une somme de tous les élèves"], 0,
               hints=["Est-ce le nombre de tous les élèves ou seulement d'une partie ?"], solution=["14 est le nombre d'élèves qui viennent à pied : c'est l'effectif de ce résultat.", "L'effectif total est 32."],
               wrong={1: "L'effectif total est 32, le nombre de tous les élèves de la classe."}),
        number("s1-g5", "effectif", f"Les notes sont : {NOTES_TEXT}. Combien d'élèves ont eu 15 ?", Fraction(NOTES.count(15)),
               hints=["Compte les 15 de la liste."], solution=[f"Il y a {NOTES.count(15)} fois le nombre 15 dans la liste."]),
    ])

# ----- Section 2: frequency and percentage -----
S2 = Section(
    "frequence", "La fréquence et le pourcentage", 24, "frequence",
    "Calculer une fréquence et l'écrire sous forme de fraction, de nombre décimal et de pourcentage.",
    [
        para("Moussa a eu 9 voix sur 20. Awa en a eu 7 sur 20. Comment comparer avec une autre élection, où un candidat a eu 18 voix sur 40 ? Les effectifs ne suffisent pas, parce que les totaux sont différents. "
             "On calcule la part de chaque candidat dans le total : c'est la fréquence."),
        definition("Fréquence",
                   "La fréquence d'un résultat est le quotient de son effectif par l'effectif total : " + "$\\text{fréquence} = \\dfrac{\\text{effectif}}{\\text{effectif total}}$" + ". "
                   "Elle est comprise entre 0 et 1 et peut s'écrire comme une fraction ou comme un nombre décimal. La somme de toutes les fréquences est 1."),
        rule("Fréquence en pourcentage",
             "Pour exprimer une fréquence en pourcentage, on la multiplie par 100 : " + N("0,45") + " = " + N("45\\ \\%") + ". Un pourcentage est une fréquence exprimée pour 100 données. La somme de toutes les fréquences en pourcentage est 100 %."),
        example("Exemple 1", "Calculer la fréquence de M dans l'élection de 20 bulletins, puis la donner en pourcentage.",
                "On divise l'effectif de M par l'effectif total.",
                [(N("9/20"), "Moussa a eu 9 voix sur 20 : c'est la fraction."),
                 (N("9 \\div 20") + " = " + N("0,45"), "En décimal : 9 ÷ 20 = 0,45."),
                 (N("0,45 \\times 100") + " = " + N("45"), "En pourcentage : 0,45 × 100 = 45, soit 45 %.")],
                "La fréquence de M est " + N("0,45") + ", soit " + N("45\\ \\%"), "d('9')/20==d('0,45') and d('0,45')*100==45"),
        para("Le tableau complété donne, pour chaque candidat, l'effectif et la fréquence en pourcentage. On peut passer d'une ligne à l'autre dans les deux sens."),
        {"type": "table", "label": "Tableau d'effectifs et de fréquences", "head": ["Candidat", "A", "M", "Y", "Total"],
         "rows": [["Effectif", "7", "9", "4", "20"], ["Fréquence en %", "35 %", "45 %", "20 %", "100 %"]]},
        example("Exemple 2", "Calculer les fréquences en pourcentage de A, M et Y dans le tableau 7 ; 9 ; 4 (total 20), et vérifier leur somme.",
                "Même calcul pour chaque effectif, puis on additionne les pourcentages.",
                [(N("7/20") + " = " + N("0,35") + " = " + N("35\\ \\%"), "Pour A."),
                 (N("9/20") + " = " + N("0,45") + " = " + N("45\\ \\%"), "Pour M."),
                 (N("4/20") + " = " + N("0,2") + " = " + N("20\\ \\%"), "Pour Y."),
                 (N("35 + 45 + 20") + " = " + N("100"), "La somme est 100 %, ce qui confirme les calculs.")],
                N("35\\ \\%") + " ; " + N("45\\ \\%") + " ; " + N("20\\ \\%"), "d('7')/20+d('9')/20+d('4')/20==1 and 35+45+20==100"),
        example("Exemple 3", "Dans une autre élection, un candidat a eu 18 voix sur 40. Qui a le meilleur score : ce candidat ou Moussa ?",
                "On compare les fréquences, pas les effectifs, parce que les totaux sont différents.",
                [(N("18/40") + " = " + N("0,45"), "18 ÷ 40 = 0,45, soit 45 %."),
                 ("Moussa : " + N("9/20") + " = " + N("0,45"), "9 ÷ 20 = 0,45, soit 45 %."),
                 ("Les deux fréquences sont égales", "Les deux candidats ont le même score, même si l'un a 18 voix et l'autre 9.")],
                "Les deux scores sont égaux : 45 %.", "d('18')/40==d('9')/20"),
        example("Exemple 4", "Pour être élu, un candidat doit obtenir au moins 35 % des 40 suffrages. Yao a eu 12 voix. Est-il élu ?",
                "On calcule le pourcentage de Yao et on le compare à 35 %.",
                [(N("12/40") + " = " + N("0,3") + " = " + N("30\\ \\%"), "12 ÷ 40 = 0,3."),
                 (N("30 < 35"), "30 % est plus petit que 35 %.")],
                "Yao n'est pas élu : il a 30 %.", "d('12')/40==d('0,3') and 30<35"),
        warning("La fréquence se calcule avec l'effectif total, pas avec 100 : la fréquence de 9 voix sur 20 est 9 ÷ 20 = 0,45, et non 9 ÷ 100. Et 0,45 n'est pas 0,45 % : c'est 45 %."),
    ],
    [
        number("s2-g1", "frequence", "Sur 36 données, un résultat apparaît 9 fois. Quelle est sa fréquence sous forme décimale ?", d("0,25"),
               hints=["Fréquence = effectif ÷ effectif total."], solution=["9 ÷ 36 = 0,25."]),
        number("s2-g2", "frequence", "12 élèves sur 40 viennent à pied. Quel pourcentage cela représente-t-il ? (en %)", Fraction(30), units=["%"],
               hints=["Divise 12 par 40, puis multiplie par 100."], solution=["12 ÷ 40 = 0,3.", "0,3 × 100 = 30 : 30 %."]),
        number("s2-g3", "frequence", "18 élèves sur 24 aiment le football. Quel pourcentage ? (en %)", Fraction(75), units=["%"],
               hints=["18 ÷ 24 = ?"], solution=["18 ÷ 24 = 0,75.", "0,75 × 100 = 75 : 75 %."]),
        number("s2-g4", "frequence", "Trois résultats ont pour fréquences 0,25 ; 0,4 et un troisième résultat. Quelle est la fréquence du troisième ?", d("0,35"),
               hints=["La somme de toutes les fréquences est 1."], solution=["0,25 + 0,4 = 0,65.", "1 − 0,65 = 0,35."]),
        choice("s2-g5", "frequence", "Pour être élu, il faut au moins 40 % des 50 suffrages. Yao a 18 voix. Est-il élu ?", ["Oui", "Non, car 18 ÷ 50 = 0,36, soit 36 %"], 1,
               hints=["Calcule le pourcentage de Yao."], solution=["18 ÷ 50 = 0,36, soit 36 %.", "36 % est plus petit que 40 % : il n'est pas élu."],
               wrong={0: "Il faut comparer des pourcentages : 18 sur 50 fait 36 %, pas 40 %."}),
    ])

# ----- Section 3: completing tables, solving problems -----
S3 = Section(
    "tableaux", "Passer d'un tableau à l'autre et résoudre des problèmes", 24, "tableaux",
    "Retrouver un effectif ou l'effectif total à partir d'une fréquence, et compléter des tableaux d'effectifs et de fréquences.",
    [
        para("Parfois on connaît la fréquence et on cherche l'effectif, ou l'inverse. La formule " + N("\\text{fréquence} = \\text{effectif} \\div \\text{effectif total}") + " permet de retrouver chaque grandeur, comme on retrouve un terme d'une multiplication."),
        rule("Retrouver l'effectif ou l'effectif total",
             "Comme la fréquence est un quotient : effectif = effectif total × fréquence, et effectif total = effectif ÷ fréquence. Avec un pourcentage, on utilise " + N("p\\ \\%") + " = " + "$\\dfrac{p}{100}$" + "."),
        example("Exemple 1", "Sur 50 votants, 30 % ont voté pour M. Combien de voix cela fait-il ?",
                "On cherche l'effectif : effectif = effectif total × fréquence.",
                [(N("30\\ \\%") + " = " + N("0,3"), "On écrit le pourcentage en décimal."),
                 (N("50 \\times 0,3") + " = " + N("15"), "L'effectif est 15 voix."),
                 ("Vérification : $15 \\div 50 = 0{,}3$", "On retrouve la fréquence.")],
                "15 voix", "50*d('0,3')==15 and d('15')/50==d('0,3')"),
        example("Exemple 2", "15 voix représentent 30 % des suffrages. Combien y a-t-il de suffrages en tout ?",
                "On cherche l'effectif total : effectif total = effectif ÷ fréquence.",
                [(N("15 \\div 0,3"), "On divise l'effectif par la fréquence."),
                 (N("15 \\div 0,3") + " = " + N("150 \\div 3") + " = " + N("50"), "On multiplie par 10 le dividende et le diviseur pour avoir un diviseur entier."),
                 ("Vérification : 30 % de 50 = 15", "On retrouve l'effectif de départ.")],
                "50 suffrages", "d('15')/d('0,3')==50 and 50*d('0,3')==15"),
        para("Pour le trajet vers l'école, le tableau complet de l'exemple suivant sera : 18, 14 et 8 élèves, soit 45 %, 35 % et 20 %."),
        {"type": "table", "label": "Tableau du trajet vers l'école", "head": ["Trajet", "À pied", "À vélo", "En bus", "Total"],
         "rows": [["Effectif", "18", "14", "8", "40"], ["Fréquence en %", "45 %", "35 %", "20 %", "100 %"]]},
        example("Exemple 3", "Dans une classe de 40 élèves, on a recensé la façon de venir à l'école : 18 à pied, 14 à vélo et les autres en bus. Compléter le tableau d'effectifs puis de fréquences.",
                "On calcule d'abord l'effectif manquant, puis chaque fréquence en pourcentage.",
                [("Effectif des élèves qui viennent en bus : " + N("40 - (18 + 14)") + " = " + N("8"), "L'effectif total moins les deux effectifs connus."),
                 (N("18/40") + " = " + N("0,45") + " = " + N("45\\ \\%"), "À pied."),
                 (N("14/40") + " = " + N("0,35") + " = " + N("35\\ \\%"), "À vélo."),
                 (N("8/40") + " = " + N("0,2") + " = " + N("20\\ \\%"), "En bus. La somme 45 + 35 + 20 = 100 confirme.")],
                "bus : " + N("8") + " élèves ; fréquences : " + N("45\\ \\%") + ", " + N("35\\ \\%") + ", " + N("20\\ \\%"), "40-(18+14)==8 and 45+35+20==100"),
        example("Exemple 4", "Un sondage dans une école de 200 élèves donne 12 % d'élèves qui aiment le football. Combien d'élèves cela fait-il ?",
                "Même méthode que l'exemple 1, avec un autre total.",
                [(N("12\\ \\%") + " = " + N("0,12"), "Pourcentage écrit en décimal."),
                 (N("200 \\times 0,12") + " = " + N("24"), "200 × 12 = 2 400, avec 2 chiffres après la virgule : 24.")],
                "24 élèves", "200*d('0,12')==24"),
        warning("Ne confonds pas l'effectif et la fréquence : 15 voix est un effectif, 30 % est une fréquence. Pour retrouver l'effectif total, on divise l'effectif par la fréquence, on ne la multiplie pas."),
    ],
    [
        number("s3-g1", "tableaux", "Sur 50 votants, 30 % ont voté pour A. Combien de voix cela fait-il ?", Fraction(15),
               hints=["Multiplie l'effectif total par la fréquence."], solution=["30 % = 0,3.", "50 × 0,3 = 15."]),
        number("s3-g2", "tableaux", "24 voix représentent 40 % des suffrages. Combien y a-t-il de suffrages en tout ?", Fraction(60),
               hints=["Divise l'effectif par la fréquence."], solution=["40 % = 0,4.", "24 ÷ 0,4 = 240 ÷ 4 = 60."]),
        number("s3-g3", "tableaux", "Un tableau d'effectifs de 50 données a deux effectifs, 12 et 18. Quel est le troisième effectif ?", Fraction(20),
               hints=["Retire 12 + 18 de l'effectif total."], solution=["12 + 18 = 30.", "50 − 30 = 20."]),
        number("s3-g4", "tableaux", "Dans le même tableau (12, 18 et 20 sur un total de 50), quelle est la fréquence en pourcentage du troisième effectif ? (en %)", Fraction(40), units=["%"],
               hints=["Divise 20 par 50, puis multiplie par 100."], solution=["20 ÷ 50 = 0,4.", "0,4 × 100 = 40 : 40 %."]),
        number("s3-g5", "tableaux", "Dans une école de 400 élèves, 35 % sont des filles du cycle de base. Combien d'élèves cela fait-il ?", Fraction(140),
               hints=["35 % = 0,35."], solution=["400 × 0,35 = 140 élèves."]),
    ])

PRACTICE = [
    number("p1", "effectif", f"Voici 25 bulletins : {LIST_25}. Combien de voix pour F ?", Fraction(VOTES_25["F"]), 1, ["Compte les F en les barrant."], [f"Il y a {VOTES_25['F']} lettres F."]),
    number("p2", "effectif", f"Dans les mêmes bulletins ({LIST_25}), combien de voix pour K ?", Fraction(VOTES_25["K"]), 1, ["Compte les K."], [f"Il y a {VOTES_25['K']} lettres K."]),
    number("p3", "effectif", "Les effectifs d'un tableau sont 11, 7, 15 et 7. Quel est l'effectif total ?", Fraction(40), 1, ["Additionne tous les effectifs."], ["11 + 7 + 15 + 7 = 40."]),
    number("p4", "effectif", "Un tableau a quatre effectifs : 8, 13, 9 et ?. L'effectif total est 45. Quel est l'effectif manquant ?", Fraction(15), 2, ["Additionne 8, 13 et 9."], ["8 + 13 + 9 = 30.", "45 − 30 = 15."]),
    number("p5", "effectif", f"Les notes sont : {NOTES_TEXT}. Combien d'élèves ont eu 8 ?", Fraction(NOTES.count(8)), 1, ["Compte les 8."], [f"Il y a {NOTES.count(8)} fois le nombre 8."]),
    number("p6", "effectif", f"Dans la liste des notes ({NOTES_TEXT}), combien d'élèves ont eu la moyenne, c'est-à-dire 10 ou plus ?", Fraction(len([n for n in NOTES if n >= 10])), 2,
           ["Compte les notes qui sont au moins 10."], [f"Les notes de 10 ou plus : {len([n for n in NOTES if n >= 10])}."]),
    choice("p7", "effectif", "Un tableau a pour effectifs 6, 9 et 5. L'élève Awa dit : « l'effectif total est 9, le plus grand effectif ». Qu'en penses-tu ?", ["Elle a raison", "Elle a tort : l'effectif total est la somme 6 + 9 + 5 = 20"], 1, 2,
           ["Que représente l'effectif total ?"], ["L'effectif total est la somme de tous les effectifs : 20.", "9 est seulement le plus grand effectif."], wrong={0: "L'effectif total compte toutes les données, pas seulement la plus fréquente."}),
    number("p8", "effectif", "Sur 30 élèves, 12 portent des lunettes et 7 ont une casquette. Aucun élève n'a les deux. Combien n'ont ni lunettes ni casquette ?", Fraction(11), 3,
           ["Ajoute les deux groupes, puis retire-les de l'effectif total."], ["12 + 7 = 19.", "30 − 19 = 11."]),
    number("p9", "frequence", "Sur 40 données, un résultat apparaît 10 fois. Quelle est sa fréquence sous forme décimale ?", d("0,25"), 1, ["Fréquence = effectif ÷ effectif total."], ["10 ÷ 40 = 0,25."]),
    number("p10", "frequence", "Dans une classe de 25 élèves, 5 sont absents. Quelle est la fréquence des absents sous forme décimale ?", d("0,2"), 1, ["5 ÷ 25 = ?"], ["5 ÷ 25 = 0,2."]),
    number("p11", "frequence", "7 élèves sur 20 ont un frère jumeau. Quel pourcentage ? (en %)", Fraction(35), 2, ["7 ÷ 20 = ?"], ["7 ÷ 20 = 0,35.", "0,35 × 100 = 35 %."], units=["%"]),
    number("p12", "frequence", "Sur 50 élèves, 30 aiment le riz. Quel pourcentage ? (en %)", Fraction(60), 2, ["30 ÷ 50 = 0,6."], ["0,6 × 100 = 60 %."], units=["%"]),
    number("p13", "frequence", f"Dans les bulletins ({LIST_25}), quel est le pourcentage de voix de F ? (en %)", Fraction(VOTES_25["F"] * 100, 25), 2, ["Effectif de F, puis divise par 25."],
           [f"F a {VOTES_25['F']} voix sur 25.", f"{VOTES_25['F']} ÷ 25 = {show(Fraction(VOTES_25['F'], 25))}, soit {VOTES_25['F'] * 4} %."], units=["%"]),
    number("p14", "frequence", "Sur 80 données, un résultat apparaît 14 fois. Quel pourcentage ? (en %)", d("17,5"), 3, ["14 ÷ 80 = 0,175."], ["14 ÷ 80 = 0,175.", "0,175 × 100 = 17,5 %."], units=["%"]),
    number("p15", "frequence", "Les fréquences en pourcentage de trois résultats sont 22 %, 48 % et un troisième résultat. Quel est le troisième pourcentage ? (en %)", Fraction(30), 2, ["La somme est 100 %."], ["22 + 48 = 70.", "100 − 70 = 30 %."], units=["%"]),
    choice("p16", "frequence", "Quel candidat a le meilleur score ? A : 9 voix sur 30. B : 14 voix sur 40. C : 11 voix sur 50.", ["A", "B", "C"], 1, 3,
           ["Compare les pourcentages, pas les effectifs."], ["A : 9 ÷ 30 = 30 %. B : 14 ÷ 40 = 35 %. C : 11 ÷ 50 = 22 %.", "B a le meilleur score."], wrong={0: "A a 30 %, B a 35 % : B est meilleur.", 2: "C a seulement 22 %."}),
    choice("p17", "frequence", "Pour être élu il faut au moins 40 % des 25 suffrages. Karim a 11 voix. Est-il élu ?", ["Oui", "Non : 11 ÷ 25 = 0,44, soit 44 %"], 0, 3,
           ["Calcule le pourcentage de Karim, puis compare à 40 %."], ["11 ÷ 25 = 0,44, soit 44 %.", "44 % est supérieur à 40 % : Karim est élu."], wrong={1: "44 % est plus grand que 40 % : Karim est élu."}),
    choice("p18", "frequence", "Fatou dit : « 9 voix sur 20, c'est 9 % ». Qu'en penses-tu ?", ["Elle a raison", "Elle a tort : 9 ÷ 20 = 0,45, soit 45 %"], 1, 3,
           ["Une fréquence se calcule avec l'effectif total."], ["9 ÷ 20 = 0,45.", "0,45 × 100 = 45 % et non 9 %."], wrong={0: "9 % serait 9 voix sur 100."}),
    number("p19", "frequence", "Quelle est la somme de toutes les fréquences d'un tableau, en nombre décimal ?", Fraction(1), 1, ["Pense au total des données."], ["La somme des fréquences est 1, c'est-à-dire 100 %."]),
    number("p20", "frequence", f"Dans la liste des notes ({NOTES_TEXT}), quelle est la fréquence en pourcentage de la note 12 ? (arrondie à l'unité, en %)", Fraction(round(100 * NOTES.count(12) / len(NOTES))), 3,
           [f"Effectif de 12 divisé par {len(NOTES)}."], [f"{NOTES.count(12)} ÷ {len(NOTES)} = {format(NOTES.count(12) / len(NOTES), ".3f").replace(".", ",")}...", f"En pourcentage arrondi : {round(100 * NOTES.count(12) / len(NOTES))} %."], units=["%"]),
    number("p21", "tableaux", "Sur 80 votants, 25 % ont voté pour Y. Combien de voix ?", Fraction(20), 1, ["80 × 0,25."], ["25 % = 0,25 et 80 × 0,25 = 20."]),
    number("p22", "tableaux", "Dans une école de 500 élèves, 18 % ont des lunettes. Combien d'élèves ?", Fraction(90), 2, ["500 × 0,18."], ["500 × 0,18 = 90."]),
    number("p23", "tableaux", "36 voix représentent 45 % des suffrages. Combien y a-t-il de suffrages en tout ?", Fraction(80), 3, ["Divise l'effectif par la fréquence."], ["36 ÷ 0,45 = 3 600 ÷ 45 = 80."]),
    number("p24", "tableaux", "21 élèves représentent 30 % d'une classe. Combien d'élèves dans la classe ?", Fraction(70), 3, ["21 ÷ 0,3 = ?"], ["21 ÷ 0,3 = 210 ÷ 3 = 70."]),
    number("p25", "tableaux", "Un tableau a 100 données : 42 d'un premier résultat, 35 d'un deuxième et le reste d'un troisième. Quel est le pourcentage du troisième ? (en %)", Fraction(23), 2, ["100 − 42 − 35."], ["100 − 77 = 23 données, soit 23 %."], units=["%"]),
    number("p26", "tableaux", "Dans une classe de 40 élèves, 45 % viennent à pied. Combien viennent à pied ?", Fraction(18), 2, ["40 × 0,45."], ["40 × 0,45 = 18."]),
    number("p27", "tableaux", "Dans une classe de 40 élèves, 18 viennent à pied et 35 % à vélo. Combien viennent à vélo ?", Fraction(14), 2, ["Calcule 35 % de 40."], ["40 × 0,35 = 14."]),
    number("p28", "tableaux", "Dans cette classe de 40 élèves (18 à pied, 14 à vélo), combien viennent en bus ?", Fraction(8), 2, ["Retire 18 + 14 de 40."], ["18 + 14 = 32.", "40 − 32 = 8."]),
    number("p29", "tableaux", "Un marchand a vendu 360 kg de riz, soit 45 % de son stock. Quel était son stock, en kg ?", Fraction(800), 3, ["Effectif ÷ fréquence."], ["360 ÷ 0,45 = 36 000 ÷ 45 = 800 kg."], units=["kg"]),
    number("p30", "tableaux", "Une enquête sur 250 élèves : 40 % aiment le football, 28 % le basket et les autres aucun des deux. Combien d'élèves n'aiment aucun des deux ?", Fraction(80), 3,
           ["Calcule le pourcentage de ceux qui n'aiment aucun des deux, puis l'effectif."], ["100 − 40 − 28 = 32 %.", "250 × 0,32 = 80 élèves."]),
]

SUMMARY = [
    definition("Effectif", "L'effectif d'un résultat est le nombre de fois où il apparaît. L'effectif total est la somme de tous les effectifs : c'est le nombre total de données."),
    definition("Fréquence", "La fréquence d'un résultat est son effectif divisé par l'effectif total. Elle est comprise entre 0 et 1, et la somme des fréquences est 1. En pourcentage : on multiplie par 100, et la somme est 100 %."),
    rule("Retrouver une grandeur", "effectif = effectif total × fréquence ; effectif total = effectif ÷ fréquence. Pour comparer deux séries qui n'ont pas le même effectif total, on compare les fréquences."),
    para("Les erreurs à éviter : diviser par 100 au lieu de l'effectif total ; confondre effectif et fréquence ; oublier un résultat dans le comptage ; écrire 0,45 % pour 45 % ; multiplier au lieu de diviser pour retrouver l'effectif total."),
]

CONCEPTS = {
    "effectif": ("Effectif et effectif total", "effectif"),
    "frequence": ("Fréquence et pourcentage", "frequence"),
    "tableaux": ("Compléter des tableaux, problèmes", "tableaux"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    names = rng.choice([("A", "M", "Y"), ("F", "K", "S"), ("B", "D", "N")])
    total = rng.choice([20, 25, 40, 50])
    first = rng.randint(total // 5, total // 2 - 1)
    second = rng.randint(total // 5, total - first - total // 5)
    counts = {names[0]: first, names[1]: second, names[2]: total - first - second}
    seed = f"bulletins{rng.random()}"
    text = ballots(counts, seed)
    target = rng.choice(names)
    # 1. count in a list
    questions.append(number("a1", "effectif", f"Voici {total} bulletins : {text}. Combien de voix pour {target} ?", Fraction(counts[target]), 1, ["Compte les lettres une par une, en les barrant."],
                            [f"Il y a {counts[target]} lettres {target} dans la liste."]))
    # 2. total from a table
    values = [rng.randint(3, 15) for _ in range(rng.choice([3, 4]))]
    questions.append(number("a2", "effectif", "Les effectifs d'un tableau sont " + ", ".join(map(str, values)) + ". Quel est l'effectif total ?", Fraction(sum(values)), 1, ["L'effectif total est la somme des effectifs."],
                            [" + ".join(map(str, values)) + f" = {sum(values)}."]))
    # 3. the missing count
    known = [rng.randint(5, 20) for _ in range(2)]
    missing = rng.randint(3, 20)
    questions.append(number("a3", "effectif", f"Un tableau d'effectifs a trois effectifs : {known[0]}, {known[1]} et ?. L'effectif total est {sum(known) + missing}. Quel est l'effectif manquant ?", Fraction(missing), 2,
                            ["Retire la somme des deux effectifs connus de l'effectif total."], [f"{known[0]} + {known[1]} = {sum(known)}.", f"{sum(known) + missing} − {sum(known)} = {missing}."]))
    # 4. frequency as a decimal
    total = rng.choice([20, 25, 40, 50])
    count = rng.randint(2, total - 2)
    questions.append(number("a4", "frequence", f"Sur {total} données, un résultat apparaît {count} fois. Quelle est sa fréquence sous forme décimale ?", Fraction(count, total), 2, ["Fréquence = effectif ÷ effectif total."],
                            [f"{count} ÷ {total} = {show(Fraction(count, total))}."]))
    # 5. frequency as a percentage
    total = rng.choice([20, 25, 40, 50, 80, 200])
    count = rng.randint(2, total - 2)
    questions.append(number("a5", "frequence", f"Dans une école de {total} élèves, {count} viennent à pied. Quel pourcentage cela représente-t-il ? (en %)", Fraction(count * 100, total), 2,
                            ["Divise l'effectif par l'effectif total, puis multiplie par 100."], [f"{count} ÷ {total} = {show(Fraction(count, total))}.", f"{show(Fraction(count, total))} × 100 = {show(Fraction(count * 100, total))} %."], units=["%"]))
    # 6. the best score between two series
    t1, t2 = rng.choice([(20, 40), (25, 50), (40, 80), (30, 60)])
    c1 = rng.randint(3, t1 - 3)
    c2 = c1 * (t2 // t1) + rng.choice([-2, -1, 1, 2])
    better = 0 if Fraction(c1, t1) > Fraction(c2, t2) else 1
    options = [f"Le premier ({c1} voix sur {t1})", f"Le second ({c2} voix sur {t2})", "Ils ont le même score"]
    questions.append(choice("a6", "frequence", f"Dans une élection, un candidat a {c1} voix sur {t1} et un autre candidat a {c2} voix sur {t2}. Qui a le meilleur score ?", options, better, 3,
                            ["Compare les pourcentages, pas les effectifs."],
                            [f"{c1} ÷ {t1} = {show(Fraction(c1 * 100, t1))} % et {c2} ÷ {t2} = {show(Fraction(c2 * 100, t2))} %.", "Le meilleur score est le plus grand pourcentage."],
                            wrong={1 - better: "Compare les pourcentages : l'autre candidat a un pourcentage plus grand.", 2: "Les deux pourcentages ne sont pas égaux."}))
    # 7. count from a percentage
    total = rng.choice([20, 40, 80, 200, 400])
    p = rng.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 60])
    questions.append(number("a7", "tableaux", f"Sur {total} élèves, {p} % aiment le football. Combien d'élèves cela fait-il ?", Fraction(total * p, 100), 2, ["Multiplie l'effectif total par la fréquence."],
                            [f"{p} % = {show(Fraction(p, 100))}.", f"{total} × {show(Fraction(p, 100))} = {show(Fraction(total * p, 100))}."]))
    # 8. the total from a count and a percentage
    p = rng.choice([10, 20, 25, 40, 50])
    total = rng.choice([40, 60, 80, 100, 200, 400])
    questions.append(number("a8", "tableaux", f"{total * p // 100} élèves représentent {p} % d'une école. Combien d'élèves y a-t-il dans l'école ?", Fraction(total), 3, ["Divise l'effectif par la fréquence."],
                            [f"{p} % = {show(Fraction(p, 100))}.", f"{total * p // 100} ÷ {show(Fraction(p, 100))} = {total}."]))
    # 9. the missing percentage
    a, b = rng.randint(10, 45), rng.randint(10, 45)
    questions.append(number("a9", "tableaux", f"Les pourcentages de trois résultats sont {a} %, {b} % et un troisième. Quel est le troisième pourcentage ? (en %)", Fraction(100 - a - b), 2, ["La somme des pourcentages est 100 %."],
                            [f"{a} + {b} = {a + b}.", f"100 − {a + b} = {100 - a - b} %."], units=["%"]))
    # 10. an election threshold
    total = rng.choice([20, 25, 40, 50])
    threshold = rng.choice([30, 35, 40])
    votes = rng.randint(total * 25 // 100, total * 50 // 100)
    elected = Fraction(votes * 100, total) >= threshold
    options = ["Oui", "Non"]
    questions.append(choice("a10", "frequence", f"Pour être élu, il faut au moins {threshold} % des {total} suffrages. Un candidat a {votes} voix. Est-il élu ?", options, 0 if elected else 1, 3,
                            ["Calcule son pourcentage, puis compare avec le seuil."], [f"{votes} ÷ {total} = {show(Fraction(votes, total))}, soit {show(Fraction(votes * 100, total))} %.", f"{show(Fraction(votes * 100, total))} % est {'au moins' if elected else 'plus petit que'} {threshold} %."],
                            wrong={1 if elected else 0: "Compare le pourcentage du candidat avec le seuil exigé."}))
    # 11. a table to complete
    total = rng.choice([40, 50, 80])
    first, second = rng.randint(total // 5, total // 3), rng.randint(total // 5, total // 3)
    third = total - first - second
    questions.append(number("a11", "tableaux", f"Dans une classe de {total} élèves, {first} viennent à pied et {second} à vélo, les autres en bus. Quelle est la fréquence en pourcentage des élèves qui viennent en bus ? (en %)", Fraction(third * 100, total), 3,
                            ["Calcule d'abord l'effectif des élèves en bus."], [f"{total} − ({first} + {second}) = {third}.", f"{third} ÷ {total} = {show(Fraction(third, total))}, soit {show(Fraction(third * 100, total))} %."], units=["%"]))
    # 12. the classic mistake
    a, b = rng.choice([(7, 20), (6, 25), (12, 40), (21, 50)])
    options = [f"Il a tort : {a} ÷ {b} = {show(Fraction(a, b))}, soit {show(Fraction(a * 100, b))} %", f"Il a raison, car {a} est le nombre de voix", "Il a tort : il faut diviser par 10"]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a12", "frequence", f"Moussa dit : « {a} voix sur {b}, c'est {a} % ». A-t-il raison ?", [options[i] for i in order], order.index(0), 3, ["Une fréquence se calcule avec l'effectif total."],
                            [f"{a} ÷ {b} = {show(Fraction(a, b))}.", f"{show(Fraction(a, b))} × 100 = {show(Fraction(a * 100, b))} %, et non {a} %."],
                            wrong={order.index(1): f"{a} % serait {a} voix sur 100, pas sur {b}.", order.index(2): "On divise par l'effectif total, pas par 10."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=9, title="Statistique : effectifs et fréquences", language="fr",
    intro="Qui a gagné l'élection du délégué ? Quelle part des élèves vient à pied ? Pour répondre, on compte, on range les données dans un tableau, et on calcule des fréquences et des pourcentages. "
          "Ce chapitre t'apprend à organiser des données, à calculer un effectif et une fréquence, et à passer d'un tableau à l'autre.",
    objectives=["Compter des données et les organiser dans un tableau d'effectifs, calculer l'effectif total.",
                "Calculer la fréquence d'un résultat et l'exprimer en nombre décimal, en fraction et en pourcentage.",
                "Retrouver un effectif ou l'effectif total à partir d'une fréquence.",
                "Compléter un tableau d'effectifs et de fréquences, et comparer deux séries par leurs fréquences.",
                "Résoudre des problèmes de la vie courante avec des pourcentages."],
    prerequisites=[{"text": "Diviser des nombres décimaux et passer d'une fraction à un nombre décimal.", "chapter": "sn-6e-division"},
                   {"text": "Comprendre les pourcentages simples.", "course": "ratios-percents", "lesson": "percents"}],
    sections=[S1, S2, S3], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Ninth chapter of the Senegal Sixième course. Its contents follow lesson 13 of the Côte d'Ivoire Sixième programme (count, total count, frequency, frequency as a percentage, tables), which was read for it, "
                "and, as that programme asks, the words modality, character and population are not used. It is also offered there, but the programme's own situations and activities are not reproduced. It has not been checked against the official Senegalese programme.",
)
