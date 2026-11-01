"""Cinquième, Cercles et disques: the ninth chapter of the Senegal Cinquième course, written in French.

The contents follow the lesson "Cercles" of the Côte d'Ivoire Cinquième programme (the position of a point relative to a circle and to a disc, the circle through the three vertices
of a triangle, and the particular case of the right triangle), which was read for this chapter. Every explanation, example, figure and exercise was written independently, with our own
numbers. It builds on the Sixième chapter on circles and on the Cinquième chapters on the perpendicular bisector and on special triangles. Constructions with a compass cannot be done on a
screen: they are described. Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a "verify"
expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .figures import Figure, figure
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-5e-cercles"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")
PI = Fraction(314, 100)

# ----- Figures -----
POSITIONS = (Figure().point("O", 170, 105, -4, 24).point("M", 215, 80, 8, -6).point("N", 245, 105, 8, 4).point("P", 285, 60, 8, -4)
             .circle("O", 75).segment("O", "N", "fig-dash"))
CIRCUM = (Figure().point("O", 170, 110, 8, 22).point("A", 170, 30, 8, -4).point("B", 101, 150, -16, 14).point("C", 239, 150, 8, 14).circle("O", 80)
          .segment("A", "B").segment("B", "C").segment("C", "A").segment("O", "A", "fig-dash").segment("O", "B", "fig-dash").segment("O", "C", "fig-dash"))
RIGHT = (Figure().point("O", 170, 110, 8, 22).point("A", 170, 30, 8, -4).point("B", 90, 110, -16, 6).point("C", 250, 110, 8, 6).circle("O", 80)
         .segment("A", "B").segment("B", "C").segment("C", "A").right_angle("A", "B", "C", 12))

# ----- Section 1: the position of a point -----
S1 = Section(
    "position", "La position d'un point par rapport à un cercle", 22, "position",
    "Décider si un point est sur un cercle, à l'intérieur ou à l'extérieur, en comparant sa distance au centre avec le rayon.",
    [
        para("Un cercle partage le plan en trois : la ligne qui le dessine, l'intérieur et l'extérieur. Pour savoir où se trouve un point, on mesure sa distance au centre et on la compare au rayon."),
        rule("Position d'un point",
             "Pour un cercle de centre O et de rayon r, et un point M : " + N("OM = r") + " signifie que M est sur le cercle ; " + N("OM < r") + " signifie que M est à l'intérieur du cercle ; "
             + N("OM > r") + " signifie que M est à l'extérieur. Le disque de centre O et de rayon r est formé des points tels que " + N("OM \\le r") + "."),
        figure(POSITIONS, "Un cercle de centre O avec un point M à l'intérieur, un point N sur le cercle et un point P à l'extérieur.", "M est à l'intérieur (OM < r), N est sur le cercle (ON = r, en pointillés), P est à l'extérieur (OP > r)."),
        example("Exemple 1", "Le cercle a pour centre O et pour rayon 5 cm. On a OM = 3 cm, ON = 5 cm et OP = 7 cm. Où sont M, N et P ?",
                "On compare chaque distance à 5 cm.",
                [("OM = 3 est plus petit que 5", "M est à l'intérieur du cercle."),
                 ("ON = 5 est égal à 5", "N est sur le cercle."),
                 ("OP = 7 est plus grand que 5", "P est à l'extérieur du cercle.")],
                "M à l'intérieur, N sur le cercle, P à l'extérieur.", "3<5 and 5==5 and 7>5"),
        example("Exemple 2", "Un disque a pour rayon 4,5 cm. Le point M est à 4,5 cm du centre. Appartient-il au disque ? au cercle ?",
                "Le disque contient le cercle et son intérieur.",
                [("OM = 4,5 est égal au rayon", "M est sur le cercle."),
                 ("OM ≤ 4,5", "M appartient aussi au disque.")],
                "M est sur le cercle, donc il appartient au disque.", "d('4,5')<=d('4,5')"),
        example("Exemple 3", "Un cercle de centre O et de rayon 6 cm. M est tel que OM = 2 × 3,5 cm. M est-il à l'intérieur, sur ou à l'extérieur du cercle ?",
                "On calcule OM, puis on compare à 6.",
                [(N("OM = 2 \\times 3,5") + " = " + N("7"), "OM vaut 7 cm."),
                 ("7 est plus grand que 6", "M est à l'extérieur.")],
                "M est à l'extérieur du cercle.", "2*d('3,5')==7 and 7>6"),
        example("Exemple 4", "Combien de points d'un cercle de rayon 5 cm sont à 5 cm de son centre ? Et à 3 cm ?",
                "Tous les points du cercle sont à la même distance du centre.",
                [("Sur le cercle, tous les points sont à 5 cm de O", "Il y en a une infinité."),
                 ("À 3 cm de O, les points sont à l'intérieur du cercle", "Ils ne sont pas sur le cercle.")],
                "Une infinité sur le cercle ; aucun à 3 cm.", "5==5"),
        warning("Le cercle est la ligne ; le disque est la surface : un point à l'intérieur est dans le disque mais pas sur le cercle. Et pour comparer, utilise toujours la distance au centre, pas la distance à un autre point du cercle."),
    ],
    [
        choice("s1-g1", "position", "Un cercle de rayon 8 cm. OM = 5 cm. Où est M ?", ["À l'intérieur", "Sur le cercle", "À l'extérieur"], 0, hints=["Compare 5 à 8."], solution=["5 < 8 : M est à l'intérieur."], wrong={1: "Il faudrait OM = 8.", 2: "Il faudrait OM > 8."}),
        choice("s1-g2", "position", "Un cercle de rayon 8 cm. OM = 8 cm. Où est M ?", ["À l'intérieur", "Sur le cercle", "À l'extérieur"], 1, hints=["Compare 8 à 8."], solution=["OM = 8 : M est sur le cercle."], wrong={0: "OM n'est pas plus petit que 8.", 2: "OM n'est pas plus grand que 8."}),
        choice("s1-g3", "position", "Un cercle de rayon 8 cm. OM = 11 cm. Où est M ?", ["À l'intérieur", "Sur le cercle", "À l'extérieur"], 2, hints=["Compare 11 à 8."], solution=["11 > 8 : M est à l'extérieur."], wrong={0: "OM est plus grand que 8.", 1: "OM n'est pas égal à 8."}),
        number("s1-g4", "position", "Un point M est à 6,5 cm du centre d'un cercle de rayon 5 cm. De combien de centimètres est-il à l'extérieur du cercle ?", d("1,5"), units=["cm"], hints=["6,5 − 5."], solution=["6,5 − 5 = 1,5 cm."]),
        choice("s1-g5", "position", "Un point appartient au disque de centre O et de rayon r si :", ["OM ≤ r", "OM = r seulement", "OM > r"], 0, hints=["Le disque inclut son bord."], solution=["Le disque contient les points avec OM ≤ r."], wrong={1: "Cela décrit le cercle.", 2: "Cela décrit l'extérieur."}),
    ])

# ----- Section 2: the circle through three points -----
S2 = Section(
    "circonscrit", "Le cercle circonscrit à un triangle", 24, "circonscrit",
    "Savoir ce qu'est le cercle circonscrit à un triangle, trouver son centre avec les médiatrices, et utiliser l'égalité OA = OB = OC.",
    [
        para("Peut-on faire passer un cercle par les trois sommets d'un triangle ? Oui, toujours, et un seul. C'est le cercle circonscrit au triangle."),
        definition("Cercle circonscrit",
                   "Le cercle circonscrit à un triangle ABC est le cercle qui passe par ses trois sommets A, B et C. Son centre O est à égale distance des trois sommets : " + N("OA = OB = OC") + ". "
                   "Il est situé à l'intersection des trois médiatrices du triangle, et son rayon est la distance de O à un sommet."),
        figure(CIRCUM, "Un triangle ABC inscrit dans un cercle de centre O, avec les trois rayons OA, OB et OC en pointillés.", "Le cercle circonscrit passe par A, B et C. Son centre O est à égale distance des trois sommets."),
        rule("Pourquoi les médiatrices",
             "Un point à égale distance de A et de B est sur la médiatrice de [AB]. Le centre O vérifie OA = OB et OB = OC : il est sur la médiatrice de [AB] et sur celle de [BC]. "
             "Les trois médiatrices du triangle se coupent donc en un même point, le centre du cercle circonscrit."),
        example("Exemple 1", "O est le centre du cercle circonscrit à ABC et OA = 5 cm. Quelles sont les longueurs OB et OC ? Quel est le rayon ?",
                "O est à égale distance des trois sommets.",
                [(N("OB = OC = OA") + " = " + N("5"), "OA = OB = OC.")],
                N("OB = OC = 5") + " cm ; le rayon est " + N("5") + " cm.", "5==5"),
        example("Exemple 2", "O est le centre du cercle circonscrit à ABC, OA = 4 cm, AB = 6 cm. Quel est le périmètre du triangle OAB ?",
                "OB = OA car O est équidistant de A et de B.",
                [(N("OB = OA") + " = " + N("4"), "Égalité des distances."),
                 (N("4 + 4 + 6") + " = " + N("14"), "Périmètre : OA + OB + AB.")],
                N("14") + " cm.", "4+4+6==14"),
        example("Exemple 3", "Un cercle a pour rayon 7 cm. Un triangle ABC a ses trois sommets sur ce cercle. Que peut-on dire de la distance du centre O aux sommets ?",
                "Les trois sommets sont sur le cercle.",
                [("A, B et C sont sur le cercle de centre O et de rayon 7", "Donc OA = OB = OC = 7 cm."),
                 ("Le cercle est le cercle circonscrit au triangle ABC", "Il passe par les trois sommets.")],
                N("OA = OB = OC = 7") + " cm.", "7==7"),
        example("Exemple 4", "Un triangle équilatéral ABC a pour côté 9 cm. Combien de médiatrices a-t-il ? Où est le centre du cercle circonscrit ?",
                "Chaque côté a une médiatrice, et elles se coupent toutes au même point.",
                [("Trois côtés, donc trois médiatrices", "Une pour chaque côté."),
                 ("Elles se coupent en O, centre du cercle circonscrit", "Dans un triangle équilatéral, c'est aussi le centre du triangle.")],
                "Trois médiatrices ; le centre est leur point commun.", "3*1==3"),
        warning("Le cercle circonscrit passe par les trois sommets : un cercle qui passe par seulement deux d'entre eux n'est pas le cercle circonscrit. Et le centre n'est pas toujours à l'intérieur du triangle : il peut être à l'extérieur si le triangle a un angle obtus."),
    ],
    [
        number("s2-g1", "circonscrit", "O est le centre du cercle circonscrit à ABC et OA = 6,5 cm. Quelle est la longueur OC, en cm ?", d("6,5"), units=["cm"], hints=["OA = OB = OC."], solution=["OC = OA = 6,5 cm."]),
        number("s2-g2", "circonscrit", "O est le centre du cercle circonscrit à ABC, OA = 5 cm et AB = 8 cm. Quel est le périmètre du triangle OAB, en cm ?", Fraction(18), units=["cm"], hints=["OB = OA."], solution=["5 + 5 + 8 = 18 cm."]),
        number("s2-g3", "circonscrit", "Combien de médiatrices faut-il tracer pour trouver le centre du cercle circonscrit à un triangle (au minimum) ?", Fraction(2), hints=["Deux droites se coupent en un point."], solution=["Deux médiatrices suffisent : elles se coupent au centre."]),
        choice("s2-g4", "circonscrit", "Le cercle circonscrit à un triangle ABC passe par :", ["A, B et C", "A et B seulement", "le milieu de chaque côté"], 0, hints=["Les trois sommets."], solution=["Il passe par les trois sommets."], wrong={1: "Il passe aussi par C.", 2: "Le cercle des milieux est un autre cercle."}),
        number("s2-g5", "circonscrit", "Les sommets d'un triangle sont sur un cercle de diamètre 18 cm. Quelle est la distance du centre à chaque sommet, en cm ?", Fraction(9), units=["cm"], hints=["Le rayon est la moitié du diamètre."], solution=["18 ÷ 2 = 9 cm."]),
    ])

# ----- Section 3: right triangles -----
S3 = Section(
    "rectangle", "Le cercle circonscrit à un triangle rectangle", 24, "rectangle",
    "Savoir que le centre du cercle circonscrit à un triangle rectangle est le milieu de l'hypoténuse, et utiliser cette propriété dans les deux sens.",
    [
        para("Pour un triangle rectangle, le cercle circonscrit est particulièrement simple à trouver : son centre est le milieu de l'hypoténuse."),
        rule("Triangle rectangle et cercle circonscrit",
             "Si un triangle est rectangle en A, alors le centre du cercle circonscrit est le milieu O de l'hypoténuse [BC], et le rayon est la moitié de l'hypoténuse : " + N("OA = OB = OC = \\dfrac{BC}{2}") + ". "
             "Réciproquement, si un triangle est inscrit dans un cercle et si l'un de ses côtés est un diamètre de ce cercle, alors le triangle est rectangle, et l'angle droit est opposé à ce diamètre."),
        figure(RIGHT, "Un triangle ABC rectangle en A inscrit dans un cercle dont le diamètre est l'hypoténuse [BC] qui passe par le centre O.", "Le triangle ABC est rectangle en A : son hypoténuse [BC] est un diamètre du cercle circonscrit, dont le centre est le milieu O de [BC]."),
        example("Exemple 1", "ABC est rectangle en A et BC = 10 cm. Quel est le rayon du cercle circonscrit ? Où est son centre ?",
                "L'hypoténuse est un diamètre.",
                [("Le centre est le milieu de [BC]", "Propriété du triangle rectangle."),
                 (N("r = 10 \\div 2") + " = " + N("5"), "Le rayon est la moitié de l'hypoténuse.")],
                "Rayon " + N("5") + " cm, centre au milieu de [BC].", "10//2==5"),
        example("Exemple 2", "Le cercle circonscrit à un triangle rectangle a pour rayon 6,5 cm. Quelle est la longueur de l'hypoténuse ?",
                "L'hypoténuse est un diamètre : elle mesure le double du rayon.",
                [(N("BC = 2 \\times 6,5") + " = " + N("13"), "Diamètre = 2 × rayon.")],
                N("13") + " cm.", "2*d('6,5')==13"),
        example("Exemple 3", "ABC est inscrit dans un cercle de centre O, avec [BC] diamètre. Que peut-on dire du triangle ?",
                "Un côté qui est un diamètre du cercle circonscrit donne un triangle rectangle.",
                [("[BC] est un diamètre du cercle circonscrit", "Réciproque de la propriété."),
                 ("Le triangle est rectangle en A", "L'angle droit est opposé au diamètre.")],
                "ABC est rectangle en A.", "180//2==90"),
        example("Exemple 4", "ABC est rectangle en A, avec le milieu O de [BC] et OA = 7 cm. Quelle est la longueur BC ?",
                "O est le centre du cercle circonscrit : OA est le rayon.",
                [(N("OA = OB = OC = 7"), "Le milieu de l'hypoténuse est équidistant des trois sommets."),
                 (N("BC = 2 \\times 7") + " = " + N("14"), "BC est un diamètre.")],
                N("BC = 14") + " cm.", "2*7==14"),
        warning("C'est l'hypoténuse (le côté opposé à l'angle droit) qui est un diamètre, pas un autre côté. Et pour utiliser la réciproque, il faut que les trois sommets soient sur le cercle et qu'un côté en soit un diamètre : un côté qui n'est pas un diamètre ne donne pas d'angle droit."),
    ],
    [
        number("s3-g1", "rectangle", "ABC est rectangle en A et BC = 14 cm. Quel est le rayon du cercle circonscrit, en cm ?", Fraction(7), units=["cm"], hints=["Moitié de l'hypoténuse."], solution=["14 ÷ 2 = 7 cm."]),
        number("s3-g2", "rectangle", "Le cercle circonscrit à un triangle rectangle a pour rayon 8 cm. Quelle est la longueur de l'hypoténuse, en cm ?", Fraction(16), units=["cm"], hints=["Le double."], solution=["2 × 8 = 16 cm."]),
        number("s3-g3", "rectangle", "ABC est rectangle en A, O est le milieu de [BC] et OA = 4,5 cm. Quelle est la longueur BC, en cm ?", Fraction(9), units=["cm"], hints=["BC = 2 × OA."], solution=["2 × 4,5 = 9 cm."]),
        choice("s3-g4", "rectangle", "ABC est inscrit dans un cercle et [BC] est un diamètre. Que peut-on dire ?", ["ABC est rectangle en A", "ABC est équilatéral", "ABC est rectangle en B"], 0, hints=["L'angle droit est opposé au diamètre."], solution=["Le triangle est rectangle en A, le sommet opposé au diamètre."], wrong={1: "Rien n'indique trois côtés égaux.", 2: "L'angle droit est en A, opposé à [BC]."}),
        choice("s3-g5", "rectangle", "Où est le centre du cercle circonscrit à un triangle rectangle ?", ["Au milieu de l'hypoténuse", "Au sommet de l'angle droit", "Au milieu du plus petit côté"], 0, hints=["L'hypoténuse est un diamètre."], solution=["Au milieu de l'hypoténuse."], wrong={1: "Le sommet de l'angle droit est sur le cercle.", 2: "Ce n'est pas un diamètre."}),
    ])

# ----- Section 4: problems -----
S4 = Section(
    "problemes", "Problèmes avec des cercles", 22, "problemes",
    "Combiner les positions d'un point, le cercle circonscrit et les triangles rectangles pour résoudre un problème, avec le périmètre et l'aire.",
    [
        para("Les problèmes de cercles mélangent la position d'un point, les distances et les propriétés des triangles. On commence par dire ce qu'on sait, puis on choisit la règle qui convient."),
        example("Exemple 1", "Un cercle de centre O et de rayon 5 cm. A est sur le cercle, B est tel que OB = 3 cm. Quelle est la longueur minimale de AB ? la maximale ?",
                "A est à 5 cm de O et B à 3 cm de O : AB varie selon leurs positions.",
                [("AB est au minimum 5 − 3", N("5 - 3") + " = " + N("2") + " (A et B alignés avec O, du même côté)."),
                 ("AB est au maximum 5 + 3", N("5 + 3") + " = " + N("8") + " (A et B alignés avec O, de part et d'autre).")],
                "AB est entre " + N("2") + " cm et " + N("8") + " cm.", "5-3==2 and 5+3==8"),
        example("Exemple 2", "Un triangle rectangle a pour hypoténuse 20 cm. Quelle est la longueur du cercle circonscrit (son périmètre) avec π = 3,14 ?",
                "Le rayon est la moitié de l'hypoténuse, puis P = 2 × π × r.",
                [(N("r = 20 \\div 2") + " = " + N("10"), "Rayon du cercle circonscrit."),
                 (N("2 \\times 3,14 \\times 10") + " = " + N("62,8"), "Périmètre du cercle.")],
                N("62,8") + " cm.", "20//2==10 and 2*d('3,14')*10==d('62,8')"),
        example("Exemple 3", "ABC est rectangle en A avec le cercle circonscrit de centre O. Si BC = 12 cm, quelle est l'aire du disque (π = 3,14) ?",
                "Rayon = 6 cm, puis aire = π × r × r.",
                [(N("r = 12 \\div 2") + " = " + N("6"), "Le rayon."),
                 (N("3,14 \\times 6 \\times 6") + " = " + N("113,04"), "L'aire du disque.")],
                N("113,04") + " cm².", "12//2==6 and d('3,14')*6*6==d('113,04')"),
        example("Exemple 4", "Un triangle ABC est tel que O est équidistant de A, B et C, avec OA = 5 cm. Le cercle de centre O et de rayon 6 cm contient-il le point B dans son intérieur ?",
                "OB = OA = 5, à comparer au rayon 6.",
                [(N("OB = OA") + " = " + N("5"), "O est équidistant des sommets."),
                 ("5 est plus petit que 6", "B est à l'intérieur du cercle de rayon 6.")],
                "Oui, B est à l'intérieur de ce cercle.", "5<6"),
        warning("Dans un problème de cercle, dessine toujours la figure et note les distances connues. Et distingue bien la position d'un point (avec OM et r) du cercle circonscrit (avec OA = OB = OC) : ce sont deux outils différents."),
    ],
    [
        number("s4-g1", "problemes", "Un cercle de rayon 7 cm. A est sur le cercle, OB = 4 cm. Quelle est la plus petite valeur possible de AB, en cm ?", Fraction(3), units=["cm"], hints=["7 − 4."], solution=["7 − 4 = 3 cm."]),
        number("s4-g2", "problemes", "Un triangle rectangle a une hypoténuse de 16 cm. Quel est le périmètre de son cercle circonscrit, en cm ? (π = 3,14)", d("50,24"), units=["cm"], hints=["r = 8, puis 2 × π × r."], solution=["r = 8 cm.", "2 × 3,14 × 8 = 50,24 cm."]),
        number("s4-g3", "problemes", "ABC est rectangle en A et BC = 10 cm. Quelle est l'aire du disque circonscrit, en cm² ? (π = 3,14)", d("78,5"), units=["cm2", "cm²"], hints=["r = 5."], solution=["3,14 × 5 × 5 = 78,5 cm²."]),
        choice("s4-g4", "problemes", "OA = OB = OC = 4 cm. Quelle est la position de O par rapport au triangle ABC ?", ["O est le centre du cercle circonscrit", "O est le milieu de [AB]", "O est un sommet"], 0, hints=["Égalité des trois distances."], solution=["O est à égale distance des trois sommets : centre du cercle circonscrit."], wrong={1: "Le milieu de [AB] n'est pas forcément à égale distance de C.", 2: "O n'est pas un sommet."}),
        number("s4-g5", "problemes", "Deux cercles de même centre ont pour rayons 4 cm et 7 cm. Quelle est la largeur de la couronne entre eux, en cm ?", Fraction(3), units=["cm"], hints=["7 − 4."], solution=["7 − 4 = 3 cm."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    choice("p1", "position", "Cercle de rayon 10 cm, OM = 6 cm. Où est M ?", ["À l'intérieur", "Sur le cercle", "À l'extérieur"], 0, 1, ["Compare 6 et 10."], ["6 < 10 : à l'intérieur."], wrong={1: "6 ≠ 10.", 2: "6 < 10."}),
    choice("p2", "position", "Cercle de rayon 10 cm, OM = 10 cm. Où est M ?", ["À l'intérieur", "Sur le cercle", "À l'extérieur"], 1, 1, ["Égal."], ["Sur le cercle."], wrong={0: "OM = r.", 2: "OM = r."}),
    choice("p3", "position", "Cercle de rayon 10 cm, OM = 13 cm. Où est M ?", ["À l'intérieur", "Sur le cercle", "À l'extérieur"], 2, 1, ["13 > 10."], ["À l'extérieur."], wrong={0: "13 > 10.", 1: "13 ≠ 10."}),
    choice("p4", "position", "Cercle de rayon 3,5 cm, OM = 3,05 cm. Où est M ?", ["À l'intérieur", "Sur le cercle", "À l'extérieur"], 0, 2, ["3,05 < 3,5."], ["À l'intérieur."], wrong={1: "3,05 ≠ 3,5.", 2: "3,05 < 3,5."}),
    number("p5", "position", "Un point M est à 9 cm du centre d'un cercle de rayon 6,5 cm. À quelle distance du cercle est-il, en cm ?", d("2,5"), 2, ["9 − 6,5."], ["2,5 cm."], units=["cm"]),
    number("p6", "position", "Un point M est à 2 cm du centre d'un cercle de rayon 5 cm. À quelle distance du cercle est-il (vers l'intérieur), en cm ?", Fraction(3), 2, ["5 − 2."], ["3 cm."], units=["cm"]),
    choice("p7", "position", "Un point M est tel que OM < r. Il appartient :", ["au disque, pas au cercle", "au cercle", "ni au disque ni au cercle"], 0, 2, ["Intérieur."], ["Au disque, pas au cercle."], wrong={1: "Il n'est pas sur la ligne.", 2: "Il est dans le disque."}),
    choice("p8", "position", "Léa dit : « le point à 5 cm du centre d'un cercle de rayon 5 cm est à l'intérieur ». Qu'en penses-tu ?", ["Il est sur le cercle, pas à l'intérieur", "Elle a raison", "Il est à l'extérieur"], 0, 2, ["OM = r."], ["Il est sur le cercle."], wrong={1: "OM = r : sur le cercle.", 2: "OM n'est pas plus grand que r."}),
    number("p9", "circonscrit", "O est le centre du cercle circonscrit à ABC, OB = 3,8 cm. Quelle est la longueur OA, en cm ?", d("3,8"), 1, ["Égalité."], ["3,8 cm."], units=["cm"]),
    number("p10", "circonscrit", "O est le centre du cercle circonscrit à ABC, OA = 7 cm et BC = 10 cm. Quel est le périmètre du triangle OBC, en cm ?", Fraction(24), 2, ["OB = OC = OA."], ["7 + 7 + 10 = 24."], units=["cm"]),
    number("p11", "circonscrit", "Le cercle circonscrit à un triangle a pour diamètre 15 cm. Quelle est la distance du centre à un sommet, en cm ?", d("7,5"), 1, ["Rayon."], ["7,5 cm."], units=["cm"]),
    number("p12", "circonscrit", "Combien de sommets d'un triangle sont sur son cercle circonscrit ?", Fraction(3), 1, ["Tous."], ["3."]),
    number("p13", "circonscrit", "Un triangle équilatéral a un côté de 9 cm. Combien de médiatrices a-t-il ?", Fraction(3), 1, ["Une par côté."], ["3."]),
    choice("p14", "circonscrit", "Le centre du cercle circonscrit à un triangle est à l'intersection :", ["des médiatrices", "des hauteurs", "des côtés"], 0, 1, ["Équidistant des sommets."], ["Des trois médiatrices."], wrong={1: "Les hauteurs se coupent en l'orthocentre, un autre point.", 2: "Les côtés se coupent aux sommets."}),
    choice("p15", "circonscrit", "OA = 5, OB = 5 et OC = 6. O est-il le centre du cercle circonscrit à ABC ?", ["Non, OC est différent", "Oui", "On ne sait pas"], 0, 2, ["Il faut OA = OB = OC."], ["OC ≠ OA : non."], wrong={1: "OC = 6.", 2: "OC ≠ OA permet de conclure."}),
    number("p16", "circonscrit", "O est le centre du cercle circonscrit à ABC, OA = 5 cm. Quel est le diamètre de ce cercle, en cm ?", Fraction(10), 1, ["2 × rayon."], ["10 cm."], units=["cm"]),
    number("p17", "rectangle", "ABC est rectangle en A, BC = 18 cm. Quel est le rayon du cercle circonscrit, en cm ?", Fraction(9), 1, ["Moitié de BC."], ["9 cm."], units=["cm"]),
    number("p18", "rectangle", "ABC est rectangle en A, BC = 11 cm. Quel est le rayon du cercle circonscrit, en cm ?", d("5,5"), 1, ["Moitié de BC."], ["5,5 cm."], units=["cm"]),
    number("p19", "rectangle", "ABC est rectangle en A et son cercle circonscrit a pour rayon 12 cm. Quelle est la longueur BC, en cm ?", Fraction(24), 2, ["Le double."], ["24 cm."], units=["cm"]),
    number("p20", "rectangle", "ABC est rectangle en A, O milieu de [BC], OA = 6,5 cm. Quelle est la longueur BC, en cm ?", Fraction(13), 2, ["2 × OA."], ["13 cm."], units=["cm"]),
    choice("p21", "rectangle", "[BC] est un diamètre du cercle circonscrit à ABC. Où est l'angle droit ?", ["En A", "En B", "En C"], 0, 2, ["Opposé au diamètre."], ["En A."], wrong={1: "B est une extrémité du diamètre.", 2: "C est une extrémité du diamètre."}),
    choice("p22", "rectangle", "Dans un triangle rectangle en A, quel segment est un diamètre du cercle circonscrit ?", ["[BC]", "[AB]", "[AC]"], 0, 1, ["L'hypoténuse."], ["[BC]."], wrong={1: "[AB] est un côté de l'angle droit.", 2: "[AC] est un côté de l'angle droit."}),
    number("p23", "rectangle", "ABC est rectangle en A, AB = 6 et AC = 8. L'hypoténuse mesure 10 cm. Quel est le rayon du cercle circonscrit, en cm ?", Fraction(5), 2, ["10 ÷ 2."], ["5 cm."], units=["cm"]),
    number("p24", "rectangle", "Le triangle ABC est rectangle en A, avec BC = 20 cm. Quelle est la distance du milieu de [BC] au sommet A, en cm ?", Fraction(10), 2, ["Rayon."], ["10 cm."], units=["cm"]),
    number("p25", "problemes", "Cercle de rayon 5 cm, A sur le cercle, OB = 2 cm. Quelle est la plus grande valeur possible de AB, en cm ?", Fraction(7), 2, ["5 + 2."], ["7 cm."], units=["cm"]),
    number("p26", "problemes", "ABC est rectangle en A avec BC = 14 cm. Quelle est l'aire du disque circonscrit, en cm² ? (π = 3,14)", d("153,86"), 3, ["r = 7."], ["3,14 × 49 = 153,86 cm²."], units=["cm2", "cm²"]),
    number("p27", "problemes", "ABC est rectangle en A avec BC = 8 cm. Quel est le périmètre du cercle circonscrit, en cm ? (π = 3,14)", d("25,12"), 2, ["r = 4."], ["2 × 3,14 × 4 = 25,12 cm."], units=["cm"]),
    number("p28", "problemes", "Deux cercles de même centre ont pour rayons 3 cm et 8,5 cm. Quelle est la largeur de la couronne, en cm ?", d("5,5"), 1, ["8,5 − 3."], ["5,5 cm."], units=["cm"]),
    number("p29", "problemes", "Un cercle de rayon 6 cm. M est tel que OM = 2 × 4 cm. Quelle est la distance de M au cercle, en cm ?", Fraction(2), 2, ["OM = 8."], ["8 − 6 = 2 cm."], units=["cm"]),
    choice("p30", "problemes", "Un cercle de rayon 5 cm contient-il dans son disque un point à 5 cm du centre ?", ["Oui, car le disque inclut le cercle", "Non", "Seulement si c'est le centre"], 0, 2, ["Disque : OM ≤ r."], ["Oui : OM = r, donc OM ≤ r."], wrong={1: "Le disque inclut son bord.", 2: "Tous les points avec OM ≤ r appartiennent au disque."}),
    choice("p31", "problemes", "O est équidistant de A, B et C (OA = OB = OC = 5). Quelle est la position de A par rapport au cercle de centre O et de rayon 5 ?", ["Sur le cercle", "À l'intérieur", "À l'extérieur"], 0, 2, ["OA = r."], ["Sur le cercle."], wrong={1: "OA n'est pas plus petit que r.", 2: "OA n'est pas plus grand que r."}),
    number("p32", "problemes", "ABC est rectangle en A. Le cercle circonscrit a un diamètre de 30 cm. Quelle est la longueur du segment qui joint A au milieu de [BC], en cm ?", Fraction(15), 3, ["C'est un rayon."], ["15 cm."], units=["cm"]),
]

SUMMARY = [
    rule("Position d'un point", "Cercle de centre O et de rayon r : OM = r (sur le cercle), OM < r (à l'intérieur), OM > r (à l'extérieur). Le disque : OM ≤ r."),
    definition("Cercle circonscrit", "Le cercle circonscrit à ABC passe par A, B et C. Son centre O vérifie OA = OB = OC : c'est le point commun des trois médiatrices."),
    rule("Triangle rectangle", "Dans un triangle rectangle, le centre du cercle circonscrit est le milieu de l'hypoténuse, et le rayon est la moitié de l'hypoténuse. Réciproquement, un triangle inscrit dont un côté est un diamètre est rectangle."),
    para("Les erreurs à éviter : confondre le cercle (la ligne) et le disque (la surface) ; croire qu'un cercle passant par deux sommets est circonscrit ; prendre un autre côté que l'hypoténuse pour le diamètre."),
]

CONCEPTS = {
    "position": ("Position d'un point par rapport à un cercle", "position"),
    "circonscrit": ("Cercle circonscrit à un triangle", "circonscrit"),
    "rectangle": ("Triangle rectangle et cercle circonscrit", "rectangle"),
    "problemes": ("Problèmes avec des cercles", "problemes"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    cm, cm2 = ["cm"], ["cm2", "cm²"]
    options = ["À l'intérieur", "Sur le cercle", "À l'extérieur"]
    # 1-2. position of a point
    r = rng.randint(4, 15)
    for index, name in ((1, "a1"), (2, "a2")):
        kind = rng.choice([0, 1, 2])
        distance = [r - rng.randint(1, 3), r, r + rng.randint(1, 4)][kind]
        questions.append(choice(name, "position", f"Un cercle de rayon {r} cm. OM = {distance} cm. Où est le point M ?", options, kind, 1, ["Compare OM au rayon."], [f"OM = {distance}, r = {r} : " + ["à l'intérieur.", "sur le cercle.", "à l'extérieur."][kind]]))
        r = rng.randint(4, 15)
    # 3. the distance to the circle
    r, om = rng.randint(3, 10), rng.randint(11, 20)
    questions.append(number("a3", "position", f"Un point M est à {om} cm du centre d'un cercle de rayon {r} cm. À quelle distance du cercle est-il, en cm ?", Fraction(om - r), 2, ["OM − r."], [f"{om} − {r} = {om - r} cm."], units=cm))
    # 4. the length from the circumscribed circle
    oa = rng.randint(3, 12)
    questions.append(number("a4", "circonscrit", f"O est le centre du cercle circonscrit à ABC et OA = {show(Fraction(oa))} cm. Quelle est la longueur OB, en cm ?", Fraction(oa), 1, ["OA = OB = OC."], [f"OB = OA = {oa} cm."], units=cm))
    # 5. a perimeter with the circumscribed circle
    oa, ab = rng.randint(4, 12), rng.randint(3, 15)
    questions.append(number("a5", "circonscrit", f"O est le centre du cercle circonscrit à ABC, OA = {oa} cm et AB = {ab} cm. Quel est le périmètre du triangle OAB, en cm ?", Fraction(2 * oa + ab), 2, ["OB = OA."], [f"{oa} + {oa} + {ab} = {2 * oa + ab} cm."], units=cm))
    # 6. the radius from the diameter
    diameter = 2 * rng.randint(4, 25)
    questions.append(number("a6", "circonscrit", f"Le cercle circonscrit à un triangle a pour diamètre {diameter} cm. Quelle est la distance du centre à un sommet, en cm ?", Fraction(diameter // 2), 1, ["Rayon = moitié du diamètre."], [f"{diameter} ÷ 2 = {diameter // 2} cm."], units=cm))
    # 7. the radius of the circumscribed circle of a right triangle
    hyp = rng.randint(5, 40)
    questions.append(number("a7", "rectangle", f"ABC est rectangle en A et BC = {hyp} cm. Quel est le rayon du cercle circonscrit, en cm ?", Fraction(hyp, 2), 1, ["Moitié de l'hypoténuse."], [f"{hyp} ÷ 2 = {show(Fraction(hyp, 2))} cm."], units=cm))
    # 8. the hypotenuse from the radius
    radius = rand_decimal(rng, 2, 15, 1)
    questions.append(number("a8", "rectangle", f"Le cercle circonscrit à un triangle rectangle a pour rayon {show(radius)} cm. Quelle est la longueur de l'hypoténuse, en cm ?", 2 * radius, 2, ["Le double du rayon."], [f"2 × {show(radius)} = {show(2 * radius)} cm."], units=cm))
    # 9. the median to the hypotenuse
    hyp = 2 * rng.randint(4, 30)
    questions.append(number("a9", "rectangle", f"ABC est rectangle en A, O est le milieu de [BC] et BC = {hyp} cm. Quelle est la longueur OA, en cm ?", Fraction(hyp // 2), 2, ["OA est un rayon."], [f"{hyp} ÷ 2 = {hyp // 2} cm."], units=cm))
    # 10. the perimeter of the circumscribed circle
    hyp = rng.randint(4, 30)
    questions.append(number("a10", "problemes", f"ABC est rectangle en A, BC = {hyp} cm. Quel est le périmètre du cercle circonscrit, en cm ? (π = 3,14)", PI * hyp, 3, ["P = π × diamètre."], [f"3,14 × {hyp} = {show(PI * hyp)} cm."], units=cm))
    # 11. the area of the circumscribed disc
    hyp = 2 * rng.randint(2, 15)
    questions.append(number("a11", "problemes", f"ABC est rectangle en A, BC = {hyp} cm. Quelle est l'aire du disque circonscrit, en cm² ? (π = 3,14)", PI * (hyp // 2) ** 2, 3, ["r = BC ÷ 2, puis π × r × r."],
                            [f"r = {hyp // 2} cm.", f"3,14 × {hyp // 2} × {hyp // 2} = {show(PI * (hyp // 2) ** 2)} cm²."], units=cm2))
    # 12. the smallest and the greatest distance
    r, ob = rng.randint(6, 15), rng.randint(2, 5)
    if rng.random() < 0.5:
        questions.append(number("a12", "problemes", f"Un cercle de rayon {r} cm. A est sur le cercle, OB = {ob} cm. Quelle est la plus petite valeur possible de AB, en cm ?", Fraction(r - ob), 3, ["r − OB."], [f"{r} − {ob} = {r - ob} cm."], units=cm))
    else:
        questions.append(number("a12", "problemes", f"Un cercle de rayon {r} cm. A est sur le cercle, OB = {ob} cm. Quelle est la plus grande valeur possible de AB, en cm ?", Fraction(r + ob), 3, ["r + OB."], [f"{r} + {ob} = {r + ob} cm."], units=cm))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=9, title="Cercles, disques et cercle circonscrit", language="fr",
    intro="Où est un point par rapport à un cercle ? Peut-on faire passer un cercle par les trois sommets d'un triangle ? "
          "Ce chapitre t'apprend à comparer une distance au rayon, à trouver le cercle circonscrit à un triangle et à utiliser le cas du triangle rectangle.",
    objectives=["Décider si un point est sur un cercle, à l'intérieur ou à l'extérieur.",
                "Connaître le cercle circonscrit à un triangle et son centre.",
                "Connaître le cercle circonscrit à un triangle rectangle et sa réciproque.",
                "Résoudre un problème avec des cercles, des périmètres et des aires."],
    prerequisites=[{"text": "Connaître le cercle, le disque et la médiatrice.", "chapter": "sn-5e-segments"},
                   {"text": "Connaître le triangle rectangle et ses angles.", "chapter": "sn-5e-triangles"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Ninth chapter of the Senegal Cinquième course. Its contents follow the circles lesson of the Côte d'Ivoire Cinquième programme (the position of a point relative to a circle and to a disc, the circumscribed circle of a triangle and of a right triangle), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. Constructions with a compass cannot be done on a screen, so they are described and not covered. "
                "It has not been checked against the official Senegalese programme.",
)
