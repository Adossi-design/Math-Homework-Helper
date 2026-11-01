"""Cinquième, Segments et médiatrice: the seventh chapter of the Senegal Cinquième course, written in French.

The contents follow the lesson "Segments" of the Côte d'Ivoire Cinquième programme (the perpendicular bisector of a segment and its characterisation by equal distances, deciding
whether a point belongs to a segment, and whether three points are aligned), which was read for this chapter. Every explanation, example, figure and exercise was written independently,
with our own numbers. Constructing a perpendicular bisector with a ruler and a compass cannot be done on a screen: the construction is described and the student reasons with lengths.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a "verify" expression that the tests
evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .figures import Figure, figure
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-5e-segments"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")

# ----- Figures -----
BISECTOR = (Figure().point("A", 50, 120, -4, 24).point("B", 290, 120, -4, 24).point("I", 170, 120, 10, 22).point("M", 170, 40, 10, 6).point("N", 170, 190, 10, -2)
            .segment("A", "B").line("M", "N").tick("A", "I", 1).tick("I", "B", 1).right_angle("I", "B", "M").segment("M", "A", "fig-dash").segment("M", "B", "fig-dash"))
BETWEEN = Figure().point("A", 50, 120, -4, 24).point("M", 150, 120, -4, 24).point("B", 290, 120, -4, 24).segment("A", "B")
OUTSIDE = Figure().point("A", 50, 130, -4, 24).point("B", 290, 130, -4, 24).point("C", 170, 50, 8, -6).segment("A", "B").segment("A", "C").segment("C", "B")

# ----- Section 1: the perpendicular bisector -----
S1 = Section(
    "mediatrice", "La médiatrice d'un segment", 24, "mediatrice",
    "Connaître la médiatrice d'un segment, sa caractérisation par l'égalité des distances, et l'utiliser pour calculer des longueurs.",
    [
        para("Pour creuser un puits à égale distance de deux villages, on cherche tous les points qui sont aussi loin de l'un que de l'autre. Ces points forment une droite particulière : la médiatrice du segment qui relie les deux villages."),
        definition("Médiatrice d'un segment",
                   "La médiatrice d'un segment [AB] est la droite perpendiculaire à [AB] qui passe par son milieu I. Pour la construire, on trace avec un compas deux cercles de même rayon, centrés en A et en B, assez grands pour se couper ; la droite qui passe par leurs deux points d'intersection est la médiatrice."),
        rule("Caractérisation de la médiatrice",
             "Un point M est sur la médiatrice de [AB] si et seulement s'il est à égale distance de A et de B : " + N("MA = MB") + ". Autrement dit, tous les points de la médiatrice vérifient MA = MB, et tout point qui vérifie MA = MB est sur la médiatrice."),
        figure(BISECTOR, "Un segment [AB] avec son milieu I, une droite (MN) perpendiculaire à [AB] en I, et deux segments en pointillés MA et MB de même longueur.", "La droite (MN) est la médiatrice de [AB] : elle passe par le milieu I et est perpendiculaire à [AB]. Le point M est à la même distance de A et de B."),
        example("Exemple 1", "M est un point de la médiatrice de [AB]. On sait que MA = 5 cm. Quelle est la longueur MB ?",
                "On utilise la caractérisation : un point de la médiatrice est à égale distance des extrémités.",
                [(N("MB = MA"), "M est sur la médiatrice de [AB]."),
                 (N("MB = 5") + " cm", "Les deux distances sont égales.")],
                N("MB = 5") + " cm.", "5==5"),
        example("Exemple 2", "M est tel que MA = 7 cm et MB = 7 cm. Que peut-on dire de M ?",
                "Les deux distances sont égales : on applique la réciproque de la caractérisation.",
                [(N("MA = MB") + " = " + N("7"), "Le point est à égale distance de A et de B."),
                 ("Donc M est sur la médiatrice de [AB]", "Tout point à égale distance des extrémités est sur la médiatrice.")],
                "M est sur la médiatrice de [AB].", "7==7"),
        example("Exemple 3", "Le triangle MAB est tel que M est sur la médiatrice de [AB], MA = 6 cm et AB = 8 cm. Quel est son périmètre ?",
                "M est sur la médiatrice : MB = MA.",
                [(N("MB = MA") + " = " + N("6"), "Égalité des distances."),
                 (N("6 + 6 + 8") + " = " + N("20"), "Périmètre : MA + MB + AB.")],
                "Le périmètre est " + N("20") + " cm.", "6+6+8==20"),
        example("Exemple 4", "Un puits doit être à égale distance de deux villages A et B distants de 24 km, sur la route [AB] qui les relie. Où le creuser ? À quelle distance de A ?",
                "Sur la route, le seul point à égale distance de A et de B est le milieu de [AB].",
                [("Le point est le milieu I de [AB]", "C'est l'intersection de la route et de la médiatrice."),
                 (N("AI = 24 \\div 2") + " = " + N("12"), "Le puits est à 12 km de chaque village.")],
                "Au milieu de la route, à " + N("12") + " km de A.", "24//2==12"),
        warning("La médiatrice est une droite entière, qui n'a ni début ni fin : elle est perpendiculaire à [AB] au milieu, mais elle continue dans les deux sens. Et un point à égale distance de A et de B n'est pas forcément le milieu de [AB] : il est sur la médiatrice, mais peut être loin du segment."),
    ],
    [
        number("s1-g1", "mediatrice", "M est sur la médiatrice de [AB] et MA = 8,5 cm. Quelle est la longueur MB, en cm ?", d("8,5"), units=["cm"], hints=["Même distance."], solution=["MB = MA = 8,5 cm."]),
        choice("s1-g2", "mediatrice", "MA = 9 cm et MB = 9 cm. Où est le point M ?", ["Sur la médiatrice de [AB]", "Au milieu de [AB]", "Sur le cercle de centre A"], 0, hints=["Égalité des distances."], solution=["M est à égale distance de A et de B : il est sur la médiatrice."], wrong={1: "Il est sur la médiatrice, mais pas forcément au milieu du segment.", 2: "Cela ne dit rien du cercle de centre A."}),
        number("s1-g3", "mediatrice", "M est sur la médiatrice de [AB]. MA = 10 cm et AB = 12 cm. Quel est le périmètre du triangle MAB, en cm ?", Fraction(32), units=["cm"], hints=["MB = MA."], solution=["MB = 10 cm.", "10 + 10 + 12 = 32 cm."]),
        number("s1-g4", "mediatrice", "Un puits est creusé à égale distance de deux villages sur la route qui les relie. Les villages sont à 30 km l'un de l'autre. À quelle distance de chaque village est le puits, en km ?", Fraction(15), units=["km"], hints=["Au milieu."], solution=["30 ÷ 2 = 15 km."]),
        choice("s1-g5", "mediatrice", "Que peut-on dire de la médiatrice de [AB] ?", ["Elle est perpendiculaire à [AB] et passe par son milieu", "Elle est parallèle à [AB]", "Elle passe par A"], 0, hints=["Deux propriétés."], solution=["La médiatrice est perpendiculaire à [AB] et passe par son milieu."], wrong={1: "Elle coupe [AB].", 2: "Elle ne passe par A que dans un cas impossible."}),
    ])

# ----- Section 2: belonging to a segment -----
S2 = Section(
    "appartenance", "Un point appartient-il à un segment ?", 22, "appartenance",
    "Décider si un point appartient à un segment avec les longueurs : M est sur [AB] si et seulement si AM + MB = AB.",
    [
        para("Un point M est sur un segment [AB] quand il est entre A et B. On peut le savoir sans regarder le dessin, en comparant des longueurs : si on passe par M pour aller de A à B, on ne fait pas un détour."),
        figure(BETWEEN, "Un segment [AB] avec un point M placé entre A et B.", "M est entre A et B : AM + MB = AB."),
        rule("Appartenance à un segment",
             "Le point M appartient au segment [AB] si et seulement si " + N("AM + MB = AB") + ". Si " + N("AM + MB") + " est plus grand que AB, alors M n'est pas sur [AB] : aller de A à B en passant par M est un détour."),
        figure(OUTSIDE, "Un triangle ACB : le point C n'est pas sur le segment [AB], et les deux côtés AC et CB sont plus longs que le chemin direct.", "C n'est pas sur [AB] : le chemin A → C → B est plus long que le chemin direct AB."),
        example("Exemple 1", "On a AM = 4,5 cm, MB = 3,5 cm et AB = 8 cm. M est-il sur [AB] ?",
                "On compare la somme AM + MB à AB.",
                [(N("AM + MB = 4,5 + 3,5") + " = " + N("8"), "La somme vaut 8."),
                 ("8 = AB", "Les deux longueurs sont égales.")],
                "Oui, M appartient à [AB].", "d('4,5')+d('3,5')==8"),
        example("Exemple 2", "On a AC = 5 cm, CB = 6 cm et AB = 10 cm. C est-il sur [AB] ?",
                "On compare la somme AC + CB à AB.",
                [(N("AC + CB = 5 + 6") + " = " + N("11"), "La somme vaut 11."),
                 ("11 est plus grand que 10", "La somme est différente de AB.")],
                "Non, C n'appartient pas à [AB].", "5+6==11 and 11>10"),
        example("Exemple 3", "M est sur le segment [AB] avec AB = 12 cm et AM = 4,6 cm. Quelle est la longueur MB ?",
                "M est sur [AB] : AM + MB = AB.",
                [(N("MB = AB - AM") + " = " + N("12 - 4,6"), "On retire AM de AB."),
                 (N("12 - 4,6") + " = " + N("7,4"), "Le calcul.")],
                N("MB = 7,4") + " cm.", "12-d('4,6')==d('7,4')"),
        example("Exemple 4", "Un coureur va de A à B (500 m), mais passe par un point P avec AP = 300 m et PB = 250 m. P est-il sur le trajet direct ?",
                "On additionne les deux étapes et on compare au trajet direct.",
                [(N("300 + 250") + " = " + N("550"), "Le trajet par P mesure 550 m."),
                 ("550 est plus grand que 500", "Le coureur fait un détour de 50 m : P n'est pas sur le segment [AB].")],
                "Non : P n'est pas sur [AB], le détour est de " + N("50") + " m.", "300+250==550 and 550-500==50"),
        warning("Pour savoir si M est sur [AB], il faut comparer AM + MB à AB, pas deux longueurs seulement. Et la somme AM + MB n'est jamais plus petite que AB : le plus court chemin entre deux points est la ligne droite."),
    ],
    [
        choice("s2-g1", "appartenance", "AM = 3 cm, MB = 4 cm et AB = 7 cm. M est-il sur [AB] ?", ["Oui", "Non"], 0, hints=["3 + 4."], solution=["3 + 4 = 7 = AB : oui."], wrong={1: "La somme vaut AB."}),
        choice("s2-g2", "appartenance", "AM = 6 cm, MB = 5 cm et AB = 10 cm. M est-il sur [AB] ?", ["Oui", "Non"], 1, hints=["6 + 5."], solution=["6 + 5 = 11, qui est plus grand que 10 : non."], wrong={0: "La somme dépasse AB."}),
        number("s2-g3", "appartenance", "M est sur [AB], AB = 15 cm et MB = 6,5 cm. Quelle est la longueur AM, en cm ?", d("8,5"), units=["cm"], hints=["AB − MB."], solution=["15 − 6,5 = 8,5 cm."]),
        number("s2-g4", "appartenance", "Un trajet direct de A à B mesure 20 km. Un trajet par C mesure 12 km puis 11 km. De combien de kilomètres le détour par C est-il plus long ?", Fraction(3), units=["km"], hints=["Compare 12 + 11 à 20."], solution=["12 + 11 = 23.", "23 − 20 = 3 km."]),
        number("s2-g5", "appartenance", "M est sur [AB] avec AM = 2,5 cm et MB = 4 cm. Quelle est la longueur AB, en cm ?", d("6,5"), units=["cm"], hints=["AB = AM + MB."], solution=["2,5 + 4 = 6,5 cm."]),
    ])

# ----- Section 3: alignment -----
S3 = Section(
    "alignement", "Trois points sont-ils alignés ?", 22, "alignement",
    "Décider si trois points sont alignés avec les longueurs, et connaître l'inégalité entre un côté d'un triangle et la somme des deux autres.",
    [
        para("Trois bornes kilométriques sont-elles sur une même route droite ? On peut le vérifier sans règle, avec seulement les trois distances : il suffit de regarder si la plus grande est égale à la somme des deux autres."),
        rule("Alignement et distances",
             "Trois points A, B et C sont alignés (avec B entre A et C) si et seulement si " + N("AB + BC = AC") + ", la plus grande distance étant égale à la somme des deux autres. "
             "Sinon, les trois points forment un vrai triangle, et chaque côté est plus petit que la somme des deux autres : " + N("AC < AB + BC") + "."),
        example("Exemple 1", "On a AB = 3 cm, BC = 4 cm et AC = 7 cm. A, B et C sont-ils alignés ?",
                "On cherche la plus grande distance, puis on compare à la somme des deux autres.",
                [("La plus grande distance est AC = 7", "Les deux autres sont 3 et 4."),
                 (N("3 + 4") + " = " + N("7"), "La somme est égale à la plus grande distance.")],
                "Oui, les points sont alignés, avec B entre A et C.", "3+4==7"),
        example("Exemple 2", "On a AB = 5 cm, BC = 6 cm et AC = 10 cm. A, B et C sont-ils alignés ?",
                "La plus grande distance est AC = 10. On compare avec 5 + 6.",
                [(N("5 + 6") + " = " + N("11"), "La somme est 11."),
                 ("11 est différent de 10", "L'égalité n'est pas vérifiée.")],
                "Non : A, B et C forment un triangle (10 < 5 + 6).", "5+6==11 and 11!=10 and 10<11"),
        example("Exemple 3", "Peut-on construire un triangle de côtés 3 cm, 4 cm et 8 cm ?",
                "On vérifie que le plus grand côté est plus petit que la somme des deux autres.",
                [(N("3 + 4") + " = " + N("7"), "La somme des deux petits côtés."),
                 ("7 est plus petit que 8", "Le grand côté dépasse la somme : le triangle est impossible.")],
                "Non : on ne peut pas construire ce triangle.", "3+4==7 and 7<8"),
        example("Exemple 4", "Trois villages A, B et C sont tels que AB = 9 km, BC = 12 km et AC = 15 km. Sont-ils alignés ?",
                "On compare 9 + 12 à 15.",
                [(N("9 + 12") + " = " + N("21"), "La somme dépasse la plus grande distance."),
                 ("21 est plus grand que 15", "Les trois villages forment un triangle.")],
                "Non, ils ne sont pas alignés.", "9+12==21 and 21>15"),
        warning("Pour conclure à l'alignement, il faut une égalité exacte : si la somme est seulement proche de la plus grande distance, les points ne sont pas alignés. Et la plus grande distance n'est pas toujours la dernière écrite : cherche-la d'abord."),
    ],
    [
        choice("s3-g1", "alignement", "AB = 4 cm, BC = 5 cm et AC = 9 cm. A, B et C sont-ils alignés ?", ["Oui", "Non"], 0, hints=["4 + 5."], solution=["4 + 5 = 9 = AC : alignés."], wrong={1: "La somme est égale à AC."}),
        choice("s3-g2", "alignement", "AB = 6 cm, BC = 7 cm et AC = 12 cm. A, B et C sont-ils alignés ?", ["Oui", "Non"], 1, hints=["6 + 7."], solution=["6 + 7 = 13 ≠ 12 : non alignés."], wrong={0: "13 est différent de 12."}),
        choice("s3-g3", "alignement", "Peut-on construire un triangle de côtés 5 cm, 6 cm et 12 cm ?", ["Oui", "Non"], 1, hints=["5 + 6 = 11."], solution=["11 est plus petit que 12 : impossible."], wrong={0: "Le grand côté est trop long."}),
        number("s3-g4", "alignement", "A, B et C sont alignés, B entre A et C, avec AB = 7,5 cm et AC = 12 cm. Quelle est la longueur BC, en cm ?", d("4,5"), units=["cm"], hints=["BC = AC − AB."], solution=["12 − 7,5 = 4,5 cm."]),
        number("s3-g5", "alignement", "Deux côtés d'un triangle mesurent 5 cm et 8 cm. Quel est le plus grand nombre entier de centimètres possible pour le troisième côté ?", Fraction(12), units=["cm"], hints=["Il doit être plus petit que 5 + 8."], solution=["5 + 8 = 13.", "Le troisième côté doit être plus petit que 13 : le plus grand entier est 12 cm."]),
    ])

# ----- Section 4: problems -----
S4 = Section(
    "problemes", "Problèmes de distances", 22, "problemes",
    "Combiner la médiatrice, l'appartenance à un segment et l'alignement pour résoudre un problème de distances.",
    [
        para("Dans un problème de distances, on commence par dire ce qu'on sait (des égalités de longueurs, des points alignés), puis on utilise une des trois règles de ce chapitre pour trouver ce qui manque."),
        example("Exemple 1", "M est sur la médiatrice de [AB], MA = 5 cm, AB = 6 cm. I est le milieu de [AB]. Calculer le périmètre du triangle MAB, puis AI.",
                "M est sur la médiatrice : MB = MA. I est le milieu : AI est la moitié de AB.",
                [(N("MB = MA") + " = " + N("5"), "Caractérisation de la médiatrice."),
                 (N("5 + 5 + 6") + " = " + N("16"), "Périmètre de MAB."),
                 (N("AI = 6 \\div 2") + " = " + N("3"), "Le milieu partage AB en deux parts égales.")],
                "Périmètre " + N("16") + " cm ; " + N("AI = 3") + " cm.", "5+5+6==16 and 6//2==3"),
        example("Exemple 2", "A, B et C sont alignés avec B entre A et C. AB = 4 cm. B est le milieu de [AC]. Quelle est la longueur AC ? Où est la médiatrice de [AC] ?",
                "Si B est le milieu de [AC], AC = 2 × AB, et la médiatrice de [AC] passe par B.",
                [(N("AC = 2 \\times 4") + " = " + N("8"), "B est le milieu de [AC]."),
                 ("La médiatrice de [AC] passe par B", "C'est la perpendiculaire à (AC) menée en B.")],
                N("AC = 8") + " cm.", "2*4==8"),
        example("Exemple 3", "Trois points : AB = 6,5 cm, BC = 8,5 cm, AC = 15 cm. Que peut-on dire ? Quel est le périmètre du triangle si les points ne sont pas alignés ?",
                "On compare 6,5 + 8,5 à 15.",
                [(N("6,5 + 8,5") + " = " + N("15"), "La somme est égale à AC."),
                 ("Les points sont alignés", "Il n'y a pas de triangle, donc pas de périmètre de triangle.")],
                "A, B et C sont alignés, B entre A et C.", "d('6,5')+d('8,5')==15"),
        example("Exemple 4", "Sur un segment [AB] de 14 m, on place un point C tel que AC soit plus long que CB de 4 m. Quelles sont les longueurs AC et CB ?",
                "C est sur [AB] : AC + CB = 14. Et AC = CB + 4.",
                [(N("CB + 4 + CB = 14") + " donc " + N("2 \\times CB = 10"), "On remplace AC par CB + 4."),
                 (N("CB = 5") + " et " + N("AC = 5 + 4") + " = " + N("9"), "On vérifie : 9 + 5 = 14.")],
                N("AC = 9") + " m et " + N("CB = 5") + " m.", "9+5==14 and 9-5==4"),
        warning("Avant de conclure, vérifie bien l'égalité des distances ou la somme demandée : un résultat « presque égal » ne prouve rien. Et un dessin à la règle ne remplace pas un calcul avec les longueurs données."),
    ],
    [
        number("s4-g1", "problemes", "M est sur la médiatrice de [AB], MA = 7 cm et AB = 8 cm. Quel est le périmètre du triangle MAB, en cm ?", Fraction(22), units=["cm"], hints=["MB = MA."], solution=["7 + 7 + 8 = 22 cm."]),
        number("s4-g2", "problemes", "A, B et C sont alignés avec B milieu de [AC] et AB = 5,5 cm. Quelle est la longueur AC, en cm ?", Fraction(11), units=["cm"], hints=["AC = 2 × AB."], solution=["2 × 5,5 = 11 cm."]),
        choice("s4-g3", "problemes", "AB = 8 cm, BC = 15 cm et AC = 23 cm. Que peut-on dire ?", ["A, B et C sont alignés, B entre A et C", "A, B et C forment un triangle", "Le triangle est rectangle"], 0, hints=["8 + 15."], solution=["8 + 15 = 23 = AC : alignés."], wrong={1: "La somme est égale à AC : pas de triangle.", 2: "Il n'y a pas de triangle."}),
        number("s4-g4", "problemes", "Un trajet de A à B par C mesure 14 km + 9 km. Le trajet direct mesure 20 km. Quel est le détour, en km ?", Fraction(3), units=["km"], hints=["23 − 20."], solution=["14 + 9 = 23.", "23 − 20 = 3 km."]),
        number("s4-g5", "problemes", "I est le milieu de [AB] et M est sur la médiatrice de [AB] avec MA = 10 cm et AB = 12 cm. Quelle est la longueur AI, en cm ?", Fraction(6), units=["cm"], hints=["AI est la moitié de AB."], solution=["12 ÷ 2 = 6 cm."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "mediatrice", "M est sur la médiatrice de [AB] et MB = 4,2 cm. Quelle est la longueur MA, en cm ?", d("4,2"), 1, ["Même distance."], ["MA = MB = 4,2 cm."], units=["cm"]),
    number("p2", "mediatrice", "M est sur la médiatrice de [AB], MA = 5 cm et AB = 6 cm. Quel est le périmètre du triangle MAB, en cm ?", Fraction(16), 1, ["MB = MA."], ["5 + 5 + 6 = 16."], units=["cm"]),
    number("p3", "mediatrice", "I est le milieu de [AB], AB = 9 cm. Quelle est la longueur AI, en cm ?", d("4,5"), 1, ["Moitié."], ["9 ÷ 2 = 4,5 cm."], units=["cm"]),
    number("p4", "mediatrice", "Deux villages sont distants de 18 km. On creuse un puits sur la route à égale distance des deux. À quelle distance de chaque village, en km ?", Fraction(9), 1, ["Milieu."], ["9 km."], units=["km"]),
    choice("p5", "mediatrice", "MA = 6 cm et MB = 8 cm. Le point M est-il sur la médiatrice de [AB] ?", ["Oui", "Non"], 1, 1, ["Compare MA et MB."], ["6 ≠ 8 : non."], wrong={0: "Les distances sont différentes."}),
    choice("p6", "mediatrice", "La médiatrice de [AB] est-elle un segment ?", ["Non, c'est une droite", "Oui", "Oui, de longueur AB"], 0, 2, ["Elle n'a pas de bout."], ["La médiatrice est une droite."], wrong={1: "Une médiatrice est illimitée.", 2: "Elle n'a pas de longueur."}),
    number("p7", "mediatrice", "M est équidistant de A et de B, MA = 13 cm, AB = 10 cm. Quel est le périmètre du triangle MAB, en cm ?", Fraction(36), 2, ["MB = MA."], ["13 + 13 + 10 = 36."], units=["cm"]),
    number("p8", "mediatrice", "I est le milieu de [AB] et AI = 7,5 cm. Quelle est la longueur AB, en cm ?", Fraction(15), 1, ["Le double."], ["15 cm."], units=["cm"]),
    choice("p9", "appartenance", "AM = 2 cm, MB = 3 cm, AB = 5 cm. M est-il sur [AB] ?", ["Oui", "Non"], 0, 1, ["2 + 3."], ["2 + 3 = 5 : oui."], wrong={1: "La somme vaut AB."}),
    choice("p10", "appartenance", "AM = 4 cm, MB = 7 cm, AB = 10 cm. M est-il sur [AB] ?", ["Oui", "Non"], 1, 1, ["4 + 7."], ["4 + 7 = 11 > 10 : non."], wrong={0: "La somme dépasse AB."}),
    number("p11", "appartenance", "M est sur [AB], AB = 20 cm, AM = 8,5 cm. Quelle est la longueur MB, en cm ?", d("11,5"), 1, ["20 − 8,5."], ["11,5 cm."], units=["cm"]),
    number("p12", "appartenance", "M est sur [AB], AM = 3,2 cm et MB = 4,9 cm. Quelle est la longueur AB, en cm ?", d("8,1"), 1, ["Additionne."], ["3,2 + 4,9 = 8,1."], units=["cm"]),
    number("p13", "appartenance", "Pour aller de A à B (1 200 m), un marcheur passe par P : AP = 700 m et PB = 600 m. De combien est le détour, en m ?", Fraction(100), 2, ["Compare 1 300 à 1 200."], ["700 + 600 = 1 300.", "1 300 − 1 200 = 100 m."], units=["m"]),
    number("p14", "appartenance", "Pour aller de A à B (2,5 km), un cycliste passe par P : AP = 1,5 km et PB = 1 km. De combien est le détour, en km ?", Fraction(0), 2, ["Compare 2,5 à 2,5."], ["1,5 + 1 = 2,5 : aucun détour, P est sur [AB]."], units=["km"]),
    choice("p15", "appartenance", "Karim dit : « AM = 4 et MB = 4 donc M est sur [AB] ». Qu'en penses-tu ?", ["Il faut comparer AM + MB à AB", "Il a raison", "Il faut que AM soit plus grand que MB"], 0, 2, ["On a besoin de AB."], ["Sans la valeur de AB, on ne peut pas conclure : il faut AM + MB = AB."], wrong={1: "Il manque AB.", 2: "Cela n'a aucun lien avec l'appartenance."}),
    choice("p16", "appartenance", "AM = 5, MB = 5 et AB = 8. Que peut-on dire de M ?", ["M n'est pas sur [AB] mais il est sur la médiatrice de [AB]", "M est sur [AB]", "M est au milieu de [AB]"], 0, 3, ["5 + 5 = 10 > 8, et MA = MB."], ["M est à égale distance de A et de B (médiatrice) mais 5 + 5 = 10 ≠ 8 : il n'est pas sur [AB]."], wrong={1: "5 + 5 = 10 est différent de 8.", 2: "Un milieu serait sur le segment."}),
    choice("p17", "alignement", "AB = 3, BC = 5, AC = 8. A, B et C sont-ils alignés ?", ["Oui", "Non"], 0, 1, ["3 + 5."], ["3 + 5 = 8 : oui."], wrong={1: "La somme vaut AC."}),
    choice("p18", "alignement", "AB = 4, BC = 6, AC = 9. A, B et C sont-ils alignés ?", ["Oui", "Non"], 1, 1, ["4 + 6 = 10."], ["10 ≠ 9 : non."], wrong={0: "10 est différent de 9."}),
    choice("p19", "alignement", "Peut-on construire un triangle de côtés 7, 8 et 9 ?", ["Oui", "Non"], 0, 2, ["7 + 8 = 15 > 9."], ["Chaque côté est plus petit que la somme des autres."], wrong={1: "9 < 7 + 8."}),
    choice("p20", "alignement", "Peut-on construire un triangle de côtés 2, 3 et 6 ?", ["Oui", "Non"], 1, 2, ["2 + 3 = 5 < 6."], ["Le plus grand côté dépasse la somme des deux autres."], wrong={0: "6 est plus grand que 2 + 3."}),
    number("p21", "alignement", "A, B et C sont alignés, B entre A et C, avec BC = 5,5 cm et AC = 14 cm. Quelle est la longueur AB, en cm ?", d("8,5"), 1, ["AC − BC."], ["8,5 cm."], units=["cm"]),
    number("p22", "alignement", "Deux côtés d'un triangle mesurent 6 cm et 9 cm. Quel est le plus petit nombre entier de cm possible pour le troisième côté ?", Fraction(4), 3, ["Il doit être plus grand que 9 − 6."], ["Le troisième côté doit dépasser 3 : le plus petit entier est 4 cm."], units=["cm"]),
    number("p23", "alignement", "Deux côtés d'un triangle mesurent 6 cm et 9 cm. Quel est le plus grand nombre entier de cm possible pour le troisième côté ?", Fraction(14), 3, ["Il doit être plus petit que 15."], ["14 cm."], units=["cm"]),
    choice("p24", "alignement", "Les villes A, B, C sont à AB = 10 km, BC = 10 km, AC = 25 km. Que peut-on dire ?", ["Impossible : 25 > 10 + 10", "Alignées", "Elles forment un triangle"], 0, 3, ["10 + 10 = 20 < 25."], ["La plus grande distance dépasse la somme des deux autres : situation impossible."], wrong={1: "Alignées demanderait 20 = 25.", 2: "Un triangle demande 25 < 20."}),
    number("p25", "problemes", "M est sur la médiatrice de [AB], MA = 9 cm et AB = 10 cm. Quel est le périmètre du triangle MAB, en cm ?", Fraction(28), 2, ["MB = MA."], ["9 + 9 + 10 = 28."], units=["cm"]),
    number("p26", "problemes", "A, B et C sont alignés, B milieu de [AC], AB = 6,5 cm. Quelle est la longueur AC, en cm ?", Fraction(13), 2, ["Le double."], ["13 cm."], units=["cm"]),
    number("p27", "problemes", "Un trajet direct de A à B mesure 15 km. Le trajet par C mesure 8,5 km puis 9 km. Quel est le détour, en km ?", d("2,5"), 2, ["17,5 − 15."], ["8,5 + 9 = 17,5.", "17,5 − 15 = 2,5 km."], units=["km"]),
    number("p28", "problemes", "I est le milieu de [AB], AB = 16 cm. M est sur la médiatrice avec MI = 6 cm. Quelle est la longueur AI, en cm ?", Fraction(8), 2, ["AI est la moitié de AB."], ["16 ÷ 2 = 8 cm."], units=["cm"]),
    choice("p29", "problemes", "M est le milieu de [AB]. Quel point est à égale distance de A et de B ?", ["M, et tous les points de la médiatrice", "Seulement M", "Seulement A"], 0, 2, ["La médiatrice passe par M."], ["Tous les points de la médiatrice sont équidistants, M en fait partie."], wrong={1: "La médiatrice entière convient.", 2: "A est à distance 0 de lui-même, pas de B."}),
    number("p30", "problemes", "AB = 12 cm, BC = 5 cm, AC = 13 cm. Les points A, B et C sont-ils alignés ? Réponds 1 pour oui, 0 pour non.", Fraction(0), 3, ["12 + 5 = 17 ≠ 13."], ["12 + 5 = 17, différent de 13 : ils ne sont pas alignés."]),
    number("p31", "problemes", "Sur une route droite, les bornes A, B, C sont telles que AB = 3,2 km, BC = 4,8 km. Quelle est la distance AC si B est entre A et C, en km ?", Fraction(8), 1, ["Additionne."], ["3,2 + 4,8 = 8 km."], units=["km"]),
    number("p32", "problemes", "Trois piquets A, B, C vérifient AB = 4 m, BC = 4 m et AC = 8 m. Quelle est la distance de B au milieu de [AC], en m ?", Fraction(0), 3, ["B est entre A et C avec AB = BC."], ["AB + BC = AC : alignés, et B est le milieu de [AC] : distance 0 m."], units=["m"]),
]

SUMMARY = [
    definition("Médiatrice", "La médiatrice d'un segment [AB] est la droite perpendiculaire à [AB] passant par son milieu. M est sur la médiatrice si et seulement si MA = MB."),
    rule("Appartenance et alignement", "M est sur [AB] si et seulement si AM + MB = AB. A, B, C sont alignés (B entre A et C) si et seulement si AB + BC = AC. Sinon, chaque côté est plus petit que la somme des deux autres : AC < AB + BC."),
    para("Les erreurs à éviter : prendre la médiatrice pour un segment ; conclure sans comparer AM + MB à AB ; croire que MA = MB suffit pour que M soit sur [AB] ; ne pas chercher d'abord la plus grande distance."),
]

CONCEPTS = {
    "mediatrice": ("Médiatrice d'un segment", "mediatrice"),
    "appartenance": ("Appartenance à un segment", "appartenance"),
    "alignement": ("Alignement de trois points", "alignement"),
    "problemes": ("Problèmes de distances", "problemes"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    cm = ["cm"]
    # 1. equal distances
    x = rand_decimal(rng, 3, 15, 1)
    questions.append(number("a1", "mediatrice", f"M est sur la médiatrice de [AB] et MA = {show(x)} cm. Quelle est la longueur MB, en cm ?", x, 1, ["Même distance."], [f"MB = MA = {show(x)} cm."], units=cm))
    # 2. the perimeter with the bisector
    ma, ab = rng.randint(4, 15), rng.randint(3, 14)
    questions.append(number("a2", "mediatrice", f"M est sur la médiatrice de [AB], MA = {ma} cm et AB = {ab} cm. Quel est le périmètre du triangle MAB, en cm ?", Fraction(2 * ma + ab), 2, ["MB = MA."], [f"{ma} + {ma} + {ab} = {2 * ma + ab} cm."], units=cm))
    # 3. the midpoint
    ab = 2 * rng.randint(3, 20)
    questions.append(number("a3", "mediatrice", f"I est le milieu de [AB] et AB = {ab} cm. Quelle est la longueur AI, en cm ?", Fraction(ab // 2), 1, ["Moitié."], [f"{ab} ÷ 2 = {ab // 2} cm."], units=cm))
    # 4. is the point on the segment
    am, mb = rng.randint(2, 12), rng.randint(2, 12)
    on = rng.random() < 0.5
    ab = am + mb if on else am + mb - rng.randint(1, min(am, mb) - 1 if min(am, mb) > 1 else 1)
    questions.append(choice("a4", "appartenance", f"AM = {am} cm, MB = {mb} cm et AB = {ab} cm. M est-il sur [AB] ?", ["Oui", "Non"], 0 if on else 1, 1, ["Compare AM + MB à AB."], [f"{am} + {mb} = {am + mb}" + (f" = {ab} : oui." if on else f", différent de {ab} : non.")]))
    # 5. the missing length on a segment
    ab, am = rand_decimal(rng, 10, 30, 1), rand_decimal(rng, 2, 8, 1)
    questions.append(number("a5", "appartenance", f"M est sur [AB], AB = {show(ab)} cm et AM = {show(am)} cm. Quelle est la longueur MB, en cm ?", ab - am, 2, ["AB − AM."], [f"{show(ab)} − {show(am)} = {show(ab - am)} cm."], units=cm))
    # 6. the length of a detour
    direct = rng.randint(10, 40)
    first, second = rng.randint(5, direct - 2), rng.randint(5, direct - 2)
    while first + second <= direct:
        first, second = rng.randint(5, direct), rng.randint(5, direct)
    questions.append(number("a6", "appartenance", f"Un trajet direct de A à B mesure {direct} km. Un trajet par C mesure {first} km puis {second} km. Quel est le détour, en km ?", Fraction(first + second - direct), 2, ["Compare la somme au trajet direct."],
                            [f"{first} + {second} = {first + second}.", f"{first + second} − {direct} = {first + second - direct} km."], units=["km"]))
    # 7. alignment
    ab, bc = rng.randint(3, 12), rng.randint(3, 12)
    aligned = rng.random() < 0.5
    ac = ab + bc if aligned else ab + bc - rng.randint(1, 2)
    questions.append(choice("a7", "alignement", f"AB = {ab} cm, BC = {bc} cm et AC = {ac} cm. A, B et C sont-ils alignés ?", ["Oui", "Non"], 0 if aligned else 1, 2, ["Compare AB + BC à AC."], [f"{ab} + {bc} = {ab + bc}" + (f" = {ac} : alignés." if aligned else f", différent de {ac} : non alignés.")]))
    # 8. a possible triangle
    a, b = rng.randint(3, 9), rng.randint(3, 9)
    c = rng.choice([a + b + rng.randint(1, 4), abs(a - b) + rng.randint(1, a + b - abs(a - b) - 1) if a + b - abs(a - b) > 1 else a])
    sides = sorted([a, b, c])
    possible = sides[2] < sides[0] + sides[1]
    questions.append(choice("a8", "alignement", f"Peut-on construire un triangle de côtés {a} cm, {b} cm et {c} cm ?", ["Oui", "Non"], 0 if possible else 1, 2, ["Compare le plus grand côté à la somme des deux autres."],
                            [f"{sides[0]} + {sides[1]} = {sides[0] + sides[1]}" + (f" > {sides[2]} : oui." if possible else f" ≤ {sides[2]} : non.")]))
    # 9. the largest integer third side
    a, b = rng.randint(3, 12), rng.randint(3, 12)
    questions.append(number("a9", "alignement", f"Deux côtés d'un triangle mesurent {a} cm et {b} cm. Quel est le plus grand nombre entier de centimètres possible pour le troisième côté ?", Fraction(a + b - 1), 3, ["Il doit être plus petit que la somme."],
                            [f"{a} + {b} = {a + b} : le troisième côté est plus petit que {a + b}, donc au plus {a + b - 1} cm."], units=cm))
    # 10. the third length on a straight road
    ab, bc = rand_decimal(rng, 2, 15, 1), rand_decimal(rng, 2, 15, 1)
    questions.append(number("a10", "alignement", f"A, B et C sont alignés, B entre A et C, avec AB = {show(ab)} km et BC = {show(bc)} km. Quelle est la distance AC, en km ?", ab + bc, 1, ["Additionne."], [f"{show(ab)} + {show(bc)} = {show(ab + bc)} km."], units=["km"]))
    # 11. a point equidistant from two villages
    d_ = 2 * rng.randint(6, 40)
    questions.append(number("a11", "problemes", f"Deux villages sont distants de {d_} km. On creuse un puits sur la route qui les relie, à égale distance des deux. À quelle distance de chaque village est-il, en km ?", Fraction(d_ // 2), 1, ["Au milieu."], [f"{d_} ÷ 2 = {d_ // 2} km."], units=["km"]))
    # 12. a midpoint
    ab = rng.randint(3, 20)
    questions.append(number("a12", "problemes", f"A, B et C sont alignés, B milieu de [AC] et AB = {ab} cm. Quelle est la longueur AC, en cm ?", Fraction(2 * ab), 2, ["Le double."], [f"2 × {ab} = {2 * ab} cm."], units=cm))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=7, title="Segments et médiatrice", language="fr",
    intro="Où creuser un puits pour qu'il soit à égale distance de deux villages ? Trois bornes sont-elles sur une même route droite ? "
          "Ce chapitre t'apprend à répondre avec la médiatrice d'un segment et en comparant des longueurs.",
    objectives=["Connaître la médiatrice d'un segment et la caractériser par l'égalité des distances.",
                "Décider si un point appartient à un segment avec les longueurs.",
                "Décider si trois points sont alignés avec les longueurs et connaître la comparaison d'un côté d'un triangle aux deux autres.",
                "Résoudre un problème de distances."],
    prerequisites=[{"text": "Connaître le milieu d'un segment et la médiatrice.", "chapter": "sn-6e-droites-cercles"},
                   {"text": "Additionner et soustraire des nombres décimaux.", "chapter": "sn-6e-division"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Seventh chapter of the Senegal Cinquième course. Its contents follow the segments lesson of the Côte d'Ivoire Cinquième programme (perpendicular bisector and its characterisation, belonging to a segment, alignment of three points), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. Constructing a perpendicular bisector with a ruler and a compass cannot be done on a screen, so it is described and not covered. "
                "It has not been checked against the official Senegalese programme.",
)
