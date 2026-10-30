"""Sixième, Symétrie centrale: the fifteenth chapter of the Senegal Sixième course, written in French.

The contents follow lesson 7 "Figures symétriques par rapport à un point" of the Côte d'Ivoire Sixième programme (the symmetric of a point, a segment, a line, an angle and a circle,
and the centre of symmetry of a figure), which was read for this chapter. Every explanation, example, figure and exercise was written independently, with our own numbers.
The figures are drawn from constants by figures.py. Constructing a symmetric figure with a ruler and a compass cannot be done on a screen: it is described, and said to be done on paper.
Points on a grid are given by their coordinates, written (x ; y), so that the symmetric of a point can be calculated and checked exactly.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .figures import Figure, figure
from .kit import N, d, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-6e-symetrie"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")

# ----- Figures -----
POINT = (Figure().point("A", 80, 60, -14, -8).point("O", 170, 105, 8, 20).point("A'", 260, 150, 8, 22)
         .segment("A", "A'", "fig-dash").tick("A", "O", 1).tick("O", "A'", 1))
SEGMENT = (Figure().point("A", 70, 60, -14, -8).point("B", 130, 40, 0, -10).point("O", 170, 105, 8, 20).point("A'", 270, 150, 8, 22).point("B'", 210, 170, -8, 22)
           .segment("A", "B").segment("A'", "B'").segment("A", "A'", "fig-dash").segment("B", "B'", "fig-dash").arrow_mark("A", "B", 1).arrow_mark("A'", "B'", 1))
CIRCLE = (Figure().point("A", 100, 105, -6, -14).point("O", 170, 105, 0, 22).point("A'", 240, 105, 6, -14)
          .circle("A", 40).circle("A'", 40).segment("A", "A'", "fig-dash"))
CENTER = (Figure().point("A", 60, 150, -14, 22).point("B", 220, 150, 6, 22).point("C", 290, 60, 8, -4).point("D", 130, 60, -14, -6).point("O", 175, 105, 16, 26)
          .segment("A", "B").segment("B", "C").segment("C", "D").segment("D", "A").segment("A", "C", "fig-dash").segment("B", "D", "fig-dash")
          .tick("A", "O", 1).tick("O", "C", 1).tick("B", "O", 2).tick("O", "D", 2))

# ----- Section 1: the symmetric of a point -----
S1 = Section(
    "point", "Le symétrique d'un point par rapport à un point", 22, "point",
    "Comprendre ce qu'est le symétrique d'un point par rapport à un point O, utiliser le milieu et calculer avec des coordonnées sur un quadrillage.",
    [
        para("Quand tu tournes une feuille d'un demi-tour autour d'une punaise plantée en O, chaque point de la feuille vient prendre la place d'un autre point, de l'autre côté de la punaise et à la même distance. "
             "Deux points qui s'échangent ainsi sont symétriques par rapport au point O."),
        definition("Symétrique d'un point",
                   "Le symétrique du point A par rapport au point O est le point A' tel que O est le milieu du segment [AA']. On a donc " + N("OA' = OA") + " et " + N("AA' = 2 \\times OA") + ", et les points A, O et A' sont alignés. "
                   "Le symétrique de O par rapport à O est O lui-même."),
        figure(POINT, "Un point A, un point O et le point A' placé de l'autre côté de O, avec le même nombre de traits sur [AO] et sur [OA'].", "A' est le symétrique de A par rapport à O : O est le milieu de [AA'], donc OA = OA'."),
        rule("Sur un quadrillage",
             "Si O a pour coordonnées " + N("(a ; b)") + " et A a pour coordonnées " + N("(x ; y)") + ", le symétrique A' a pour coordonnées " + N("(2a - x ; 2b - y)") + ". "
             "En effet, on obtient A' en faisant à partir de O le trajet inverse de celui de O à A : si A est 3 carreaux à droite et 2 carreaux en haut de O, A' est 3 carreaux à gauche et 2 carreaux en bas."),
        example("Exemple 1", "Le point A est à 4 cm du point O. A' est le symétrique de A par rapport à O. Calculer OA' et AA'.",
                "O est le milieu de [AA'] : OA' est égal à OA, et AA' est le double.",
                [(N("OA' = OA") + " = " + N("4") + " cm", "O est le milieu de [AA']."),
                 (N("AA' = 2 \\times 4") + " = " + N("8") + " cm", "[AA'] est formé de [AO] et [OA'].")],
                N("OA' = 4") + " cm et " + N("AA' = 8") + " cm.", "4==4 and 2*4==8"),
        example("Exemple 2", "O a pour coordonnées (2 ; 3) et A a pour coordonnées (5 ; 7). Quelles sont les coordonnées de A', symétrique de A par rapport à O ?",
                "On utilise A' = (2a − x ; 2b − y), ou on fait le trajet inverse de O à A.",
                [("De O à A : on avance de 5 − 2 = 3 vers la droite et de 7 − 3 = 4 vers le haut", "C'est le trajet de O vers A."),
                 ("De O à A' : on recule de 3 et de 4 : 2 − 3 = −1 et 3 − 4 = −1", "Trajet inverse."),
                 ("Avec la formule : 2 × 2 − 5 = −1 et 2 × 3 − 7 = −1", "On retrouve les mêmes coordonnées.")],
                "A' a pour coordonnées " + N("(-1 ; -1)") + ".", "2*2-5==-1 and 2*3-7==-1 and (5-2)==3"),
        example("Exemple 3", "A a pour coordonnées (6 ; 1) et A' a pour coordonnées (2 ; 5). Quelles sont les coordonnées de O, centre de symétrie qui échange A et A' ?",
                "O est le milieu de [AA'] : chaque coordonnée de O est la moyenne des coordonnées de A et de A'.",
                [(N("(6 + 2) \\div 2") + " = " + N("4"), "Abscisse de O."),
                 (N("(1 + 5) \\div 2") + " = " + N("3"), "Ordonnée de O.")],
                "O a pour coordonnées " + N("(4 ; 3)") + ".", "(6+2)//2==4 and (1+5)//2==3"),
        example("Exemple 4", "Quel est le symétrique du point O par rapport à O ? Quel est le symétrique de A' par rapport à O ?",
                "On utilise la définition : O est le milieu du segment qui joint un point à son symétrique.",
                [("O est déjà le milieu de lui-même", "Le symétrique de O est O."),
                 ("Si A' est le symétrique de A, alors A est le symétrique de A'", "Le symétrique de A' est A.")],
                "O et A.", "0+0==0"),
        warning("Le symétrique de A par rapport à O n'est pas le point « de l'autre côté de la feuille » à n'importe quelle distance : il est exactement à la même distance de O, sur la droite (AO). "
                "Et ne confonds pas avec la symétrie par rapport à une droite, qui est une autre transformation et n'est pas le sujet de ce chapitre."),
    ],
    [
        number("s1-g1", "point", "A est à 7 cm de O. A' est son symétrique par rapport à O. Quelle est la longueur OA', en cm ?", Fraction(7), units=["cm"],
               hints=["O est le milieu de [AA']."], solution=["OA' = OA = 7 cm."]),
        number("s1-g2", "point", "A est à 5,5 cm de O. A' est son symétrique par rapport à O. Quelle est la longueur AA', en cm ?", Fraction(11), units=["cm"],
               hints=["AA' = 2 × OA."], solution=["AA' = 2 × 5,5 = 11 cm."]),
        number("s1-g3", "point", "AA' = 18 cm et A' est le symétrique de A par rapport à O. Quelle est la longueur OA, en cm ?", Fraction(9), units=["cm"],
               hints=["OA est la moitié de AA'."], solution=["OA = 18 ÷ 2 = 9 cm."]),
        ordered("s1-g4", "point", "O a pour coordonnées (1 ; 2) et A (4 ; 6). Écris les coordonnées de A', symétrique de A par rapport à O, sous la forme abscisse ; ordonnée.", [Fraction(-2), Fraction(-2)],
                hints=["A' = (2a − x ; 2b − y)."], solution=["2 × 1 − 4 = −2 et 2 × 2 − 6 = −2.", "A' (−2 ; −2)."]),
        ordered("s1-g5", "point", "A (7 ; 1) et A' (3 ; 5) sont symétriques par rapport à O. Écris les coordonnées de O sous la forme abscisse ; ordonnée.", [Fraction(5), Fraction(3)],
                hints=["O est le milieu de [AA']."], solution=["(7 + 3) ÷ 2 = 5 et (1 + 5) ÷ 2 = 3.", "O (5 ; 3)."]),
    ])

# ----- Section 2: the symmetric of a figure -----
S2 = Section(
    "figures", "Le symétrique d'un segment, d'une droite, d'un angle et d'un cercle", 24, "figures",
    "Connaître les propriétés de la symétrie centrale : elle conserve les longueurs, les angles, l'alignement, le parallélisme et les cercles.",
    [
        para("Un demi-tour ne déforme rien : la figure retournée a exactement la même forme et la même taille. C'est ce qu'expriment les propriétés de la symétrie centrale."),
        rule("Propriétés de la symétrie centrale",
             "Le symétrique d'un segment [AB] est un segment [A'B'] de même longueur : " + N("A'B' = AB") + ". Le symétrique d'une droite est une droite parallèle. Le symétrique d'une demi-droite est une demi-droite. "
             "Le symétrique d'un angle est un angle de même mesure. Des points alignés ont des symétriques alignés. Le symétrique d'un cercle de rayon r est un cercle de même rayon. "
             "Deux droites perpendiculaires ont des symétriques perpendiculaires, et deux droites parallèles ont des symétriques parallèles."),
        figure(SEGMENT, "Un segment [AB], son symétrique [A'B'] de l'autre côté du point O, et les deux segments marqués par les mêmes chevrons parce qu'ils sont parallèles.", "Le symétrique du segment [AB] est le segment [A'B'] : il a la même longueur et il est parallèle à [AB]."),
        figure(CIRCLE, "Deux cercles de même rayon, symétriques par rapport au point O, milieu des deux centres.", "Le symétrique du cercle de centre A est le cercle de centre A', de même rayon : O est le milieu de [AA']."),
        example("Exemple 1", "[A'B'] est le symétrique du segment [AB] par rapport à O. AB = 6,5 cm. Calculer A'B'.",
                "La symétrie centrale conserve les longueurs.",
                [(N("A'B' = AB") + " = " + N("6,5"), "Le symétrique d'un segment a la même longueur.")],
                N("A'B' = 6,5") + " cm.", "d('6,5')==d('6,5')"),
        example("Exemple 2", "L'angle " + N("\\widehat{ABC}") + " mesure 47°. Quelle est la mesure de son symétrique " + N("\\widehat{A'B'C'}") + " ?",
                "La symétrie centrale conserve les angles.",
                [("Le symétrique d'un angle est un angle de même mesure", "Propriété de la symétrie centrale.")],
                N("\\widehat{A'B'C'} = 47") + "°.", "47==47"),
        example("Exemple 3", "Un cercle de centre A et de rayon 3 cm a pour symétrique par rapport à O un cercle de centre A'. Quel est le rayon de ce cercle ? Quelle est la distance AA' si OA = 5 cm ?",
                "Le symétrique d'un cercle est un cercle de même rayon, dont le centre est le symétrique du centre.",
                [("Le rayon est conservé", "Le cercle de centre A' a pour rayon 3 cm."),
                 (N("AA' = 2 \\times 5") + " = " + N("10"), "A' est le symétrique de A : AA' est le double de OA.")],
                "Le rayon est " + N("3") + " cm et " + N("AA' = 10") + " cm.", "3==3 and 2*5==10"),
        example("Exemple 4", "Un triangle ABC a des côtés de 5 cm, 6 cm et 7 cm. Son symétrique A'B'C' par rapport à un point O a quel périmètre ? Quelle aire si l'aire de ABC est 14 cm² ?",
                "Les longueurs sont conservées, donc le périmètre aussi ; la figure garde la même taille, donc l'aire aussi.",
                [(N("5 + 6 + 7") + " = " + N("18"), "Le périmètre de A'B'C' est le même que celui de ABC."),
                 ("L'aire est conservée", "L'aire de A'B'C' est 14 cm².")],
                "Périmètre " + N("18") + " cm et aire " + N("14") + " cm².", "5+6+7==18"),
        warning("Le symétrique d'une droite est une droite parallèle, pas la même droite (sauf si elle passe par O). Et la symétrie centrale ne change jamais les longueurs ni les angles : si tes mesures changent, c'est que la figure est mal construite."),
    ],
    [
        number("s2-g1", "figures", "[A'B'] est le symétrique de [AB] par rapport à O. AB = 9 cm. Quelle est la longueur A'B', en cm ?", Fraction(9), units=["cm"],
               hints=["La symétrie centrale conserve les longueurs."], solution=["A'B' = AB = 9 cm."]),
        number("s2-g2", "figures", "Un angle mesure 62°. Quelle est la mesure de son symétrique par rapport à un point O, en degrés ?", Fraction(62), units=["°", "degrés", "degré"],
               hints=["La symétrie centrale conserve les angles."], solution=["Le symétrique a la même mesure : 62°."]),
        number("s2-g3", "figures", "Un cercle de rayon 4,5 cm a pour symétrique un cercle par rapport à O. Quel est le rayon de ce cercle, en cm ?", d("4,5"), units=["cm"],
               hints=["Le symétrique d'un cercle est un cercle de même rayon."], solution=["Le rayon est conservé : 4,5 cm."]),
        choice("s2-g4", "figures", "Que peut-on dire du symétrique d'une droite (d) par rapport à un point O qui n'est pas sur (d) ?", ["C'est une droite parallèle à (d)", "C'est une droite perpendiculaire à (d)", "C'est la même droite (d)"], 0,
               hints=["Un demi-tour renverse la direction mais ne la change pas."], solution=["Le symétrique d'une droite est une droite parallèle."],
               wrong={1: "Un demi-tour ne tourne pas la direction d'un quart de tour.", 2: "La droite ne revient sur elle-même que si elle passe par O."}),
        number("s2-g5", "figures", "Un triangle a un périmètre de 24 cm. Quel est le périmètre de son symétrique par rapport à un point, en cm ?", Fraction(24), units=["cm"],
               hints=["Les longueurs sont conservées."], solution=["Les trois côtés gardent leur longueur : le périmètre est 24 cm."]),
    ])

# ----- Section 3: centre of symmetry -----
S3 = Section(
    "centre", "Centre de symétrie d'une figure", 22, "centre",
    "Reconnaître le centre de symétrie d'un segment, d'un cercle et d'un parallélogramme, et l'utiliser pour calculer des longueurs.",
    [
        para("Certaines figures se retrouvent exactement identiques après un demi-tour : une pièce de monnaie, une roue, un cadre en parallélogramme. Le point autour duquel on tourne s'appelle le centre de symétrie de la figure."),
        definition("Centre de symétrie",
                   "Un point O est un centre de symétrie d'une figure si le symétrique de la figure par rapport à O est la figure elle-même. Une figure a au plus un centre de symétrie, sauf des cas très particuliers comme une droite entière."),
        rule("Centres de symétrie à connaître",
             "Le centre de symétrie d'un segment est son milieu. Le centre de symétrie d'un cercle ou d'un disque est son centre. Le centre de symétrie d'un parallélogramme est le point d'intersection de ses diagonales. "
             "Un triangle n'a pas de centre de symétrie."),
        figure(CENTER, "Un parallélogramme ABCD avec ses diagonales qui se coupent en O, et des traits égaux sur OA et OC, OB et OD.", "Le point O, intersection des diagonales, est le centre de symétrie du parallélogramme ABCD : A et C sont symétriques, B et D aussi."),
        example("Exemple 1", "ABCD est un parallélogramme de centre O et AC = 14 cm. Quelle est la longueur OC ?",
                "O est le centre de symétrie, donc A et C sont symétriques par rapport à O : O est le milieu de [AC].",
                [("C est le symétrique de A par rapport à O", "O est le centre de symétrie."),
                 (N("OC = AC \\div 2") + " = " + N("14 \\div 2") + " = " + N("7"), "O est le milieu de [AC].")],
                N("OC = 7") + " cm.", "14//2==7"),
        example("Exemple 2", "Un segment [PQ] mesure 10 cm. Quel est son centre de symétrie ? À quelle distance est-il de P ?",
                "Le centre de symétrie d'un segment est son milieu.",
                [("Le centre est le milieu M de [PQ]", "Un demi-tour autour de M échange P et Q."),
                 (N("PM = 10 \\div 2") + " = " + N("5"), "Le milieu est à 5 cm de P.")],
                "Le milieu de [PQ], à " + N("5") + " cm de P.", "10//2==5"),
        example("Exemple 3", "Un cercle a un diamètre de 12 cm. A est un point du cercle et A' est son symétrique par rapport au centre O. Quelle est la longueur AA' ?",
                "Le centre du cercle est son centre de symétrie : A' est l'autre extrémité du diamètre qui passe par A.",
                [(N("OA = 12 \\div 2") + " = " + N("6"), "Le rayon est 6 cm."),
                 (N("AA' = 2 \\times 6") + " = " + N("12"), "AA' est un diamètre.")],
                N("AA' = 12") + " cm.", "12//2==6 and 2*6==12"),
        example("Exemple 4", "Un triangle a-t-il un centre de symétrie ? Un rectangle ? Un cercle ?",
                "On cherche si un demi-tour autour d'un point laisse la figure inchangée.",
                [("Un triangle", "Un demi-tour le retourne sans le superposer : il n'a pas de centre de symétrie."),
                 ("Un rectangle", "C'est un parallélogramme : son centre de symétrie est l'intersection de ses diagonales."),
                 ("Un cercle", "Son centre est son centre de symétrie.")],
                "Triangle : non ; rectangle : oui ; cercle : oui.", "3-1==2"),
        warning("Le centre de symétrie d'un parallélogramme n'est pas un sommet : c'est le point où se coupent les diagonales. Et il n'est pas forcément sur la figure : le centre d'un cercle n'est pas sur le cercle, mais au milieu du disque."),
    ],
    [
        number("s3-g1", "centre", "ABCD est un parallélogramme de centre O. AC = 20 cm. Quelle est la longueur OA, en cm ?", Fraction(10), units=["cm"],
               hints=["O est le milieu de [AC]."], solution=["OA = AC ÷ 2 = 10 cm."]),
        number("s3-g2", "centre", "Un segment mesure 16 cm. À quelle distance de chaque extrémité est son centre de symétrie, en cm ?", Fraction(8), units=["cm"],
               hints=["Le centre de symétrie d'un segment est son milieu."], solution=["16 ÷ 2 = 8 cm."]),
        number("s3-g3", "centre", "Un cercle a pour rayon 7 cm. A est un point du cercle et A' est son symétrique par rapport au centre. Quelle est la longueur AA', en cm ?", Fraction(14), units=["cm"],
               hints=["AA' est un diamètre."], solution=["AA' = 2 × 7 = 14 cm."]),
        choice("s3-g4", "centre", "Quelle figure n'a pas de centre de symétrie ?", ["Le cercle", "Le parallélogramme", "Le triangle"], 2,
               hints=["Pense au demi-tour."], solution=["Un demi-tour ne ramène pas un triangle sur lui-même : il n'a pas de centre de symétrie."], wrong={0: "Le cercle a son centre pour centre de symétrie.", 1: "Le parallélogramme a pour centre de symétrie l'intersection de ses diagonales."}),
        choice("s3-g5", "centre", "Où est le centre de symétrie d'un parallélogramme ?", ["À un sommet", "À l'intersection de ses diagonales", "Au milieu d'un côté"], 1,
               hints=["C'est le milieu de chaque diagonale."], solution=["Le centre de symétrie est le point d'intersection des diagonales, milieu de chacune d'elles."], wrong={0: "Un sommet est échangé avec le sommet opposé : il ne peut pas être fixe.", 2: "Le milieu d'un côté n'est pas fixe."}),
    ])

# ----- Section 4: problems -----
S4 = Section(
    "problemes", "Problèmes de symétrie centrale", 22, "problemes",
    "Résoudre des problèmes qui combinent distances, coordonnées, périmètres et aires avec la symétrie centrale.",
    [
        para("Les propriétés de la symétrie centrale permettent de résoudre des problèmes sans mesurer : on déduit une longueur, un angle ou un point à partir de ce qu'on connaît déjà. "
             "Dans chaque problème, cherche d'abord le centre de symétrie et les points qui s'échangent."),
        example("Exemple 1", "ABCD est un parallélogramme de centre O. On sait que OA = 6 cm et OB = 4 cm. Calculer AC et BD, puis le périmètre du triangle OAB si AB = 7 cm.",
                "O est le milieu des diagonales : AC et BD sont des doubles. Le périmètre du triangle est la somme de ses côtés.",
                [(N("AC = 2 \\times 6") + " = " + N("12"), "O est le milieu de [AC]."),
                 (N("BD = 2 \\times 4") + " = " + N("8"), "O est le milieu de [BD]."),
                 (N("OA + OB + AB") + " = " + N("6 + 4 + 7") + " = " + N("17"), "Périmètre de OAB.")],
                N("AC = 12") + " cm, " + N("BD = 8") + " cm, périmètre " + N("17") + " cm.", "2*6==12 and 2*4==8 and 6+4+7==17"),
        example("Exemple 2", "A (1 ; 5) a pour symétrique A' (7 ; 1). B (2 ; 2) a pour symétrique B'. Trouver O, puis B'.",
                "On trouve O avec le milieu de [AA'], puis on applique la formule à B.",
                [(N("(1 + 7) \\div 2") + " = " + N("4") + " et " + N("(5 + 1) \\div 2") + " = " + N("3"), "O a pour coordonnées (4 ; 3)."),
                 (N("2 \\times 4 - 2") + " = " + N("6") + " et " + N("2 \\times 3 - 2") + " = " + N("4"), "B' a pour coordonnées (6 ; 4).")],
                "O (4 ; 3) et B' (6 ; 4).", "(1+7)//2==4 and (5+1)//2==3 and 2*4-2==6 and 2*3-2==4"),
        example("Exemple 3", "Un cercle de centre A et de rayon 3 cm a pour symétrique, par rapport à O, un cercle de centre A'. OA = 8 cm. Les deux cercles se coupent-ils ?",
                "On compare la distance entre les centres à la somme des rayons.",
                [(N("AA' = 2 \\times 8") + " = " + N("16"), "Les centres sont à 16 cm l'un de l'autre."),
                 (N("3 + 3") + " = " + N("6"), "La somme des rayons est 6 cm."),
                 ("16 est plus grand que 6", "Les deux cercles ne se touchent pas.")],
                "Non, les deux cercles ne se coupent pas.", "2*8==16 and 3+3==6 and 16>6"),
        example("Exemple 4", "Un rectangle ABCD a une longueur de 8 cm et une largeur de 5 cm. Quel est le périmètre et l'aire de son symétrique par rapport à O ?",
                "La symétrie centrale conserve les longueurs et les aires.",
                [(N("2 \\times (8 + 5)") + " = " + N("26"), "Périmètre : 26 cm."),
                 (N("8 \\times 5") + " = " + N("40"), "Aire : 40 cm².")],
                "Périmètre " + N("26") + " cm et aire " + N("40") + " cm².", "2*(8+5)==26 and 8*5==40"),
        warning("Dans un problème, ne mélange pas le centre de symétrie et le centre d'un cercle : si le cercle est son propre symétrique, ses deux centres sont confondus ; sinon A' n'est pas le centre. "
                "Et pour les coordonnées, vérifie toujours que O est bien le milieu de [AA'] en recalculant les moyennes."),
    ],
    [
        number("s4-g1", "problemes", "ABCD est un parallélogramme de centre O. OA = 5 cm et OB = 3 cm. Quelle est la longueur AC + BD, en cm ?", Fraction(16), units=["cm"],
               hints=["AC = 2 × OA et BD = 2 × OB."], solution=["AC = 10 cm et BD = 6 cm.", "10 + 6 = 16 cm."]),
        ordered("s4-g2", "problemes", "O (3 ; 4) et A (8 ; 1). Écris les coordonnées de A', symétrique de A par rapport à O, sous la forme abscisse ; ordonnée.", [Fraction(-2), Fraction(7)],
                hints=["A' = (2a − x ; 2b − y)."], solution=["2 × 3 − 8 = −2 et 2 × 4 − 1 = 7.", "A' (−2 ; 7)."]),
        ordered("s4-g3", "problemes", "A (9 ; 2) et A' (3 ; 8) sont symétriques par rapport à O. Écris les coordonnées de O sous la forme abscisse ; ordonnée.", [Fraction(6), Fraction(5)],
                hints=["O est le milieu de [AA']."], solution=["(9 + 3) ÷ 2 = 6 et (2 + 8) ÷ 2 = 5.", "O (6 ; 5)."]),
        number("s4-g4", "problemes", "Un rectangle de 12 cm sur 7 cm a un symétrique par rapport à un point O. Quelle est l'aire de ce symétrique, en cm² ?", Fraction(84), units=["cm2", "cm²"],
               hints=["La symétrie centrale conserve les aires."], solution=["12 × 7 = 84 cm²."]),
        number("s4-g5", "problemes", "Un cercle de rayon 5 cm et son symétrique par rapport à un point O ont leurs centres à 30 cm l'un de l'autre. Quelle est la distance de O à chacun des centres, en cm ?", Fraction(15), units=["cm"],
               hints=["O est le milieu des deux centres."], solution=["30 ÷ 2 = 15 cm."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "point", "A est à 12 cm de O. A' est son symétrique par rapport à O. Quelle est la longueur OA', en cm ?", Fraction(12), 1, ["O est le milieu de [AA']."], ["OA' = OA = 12 cm."], units=["cm"]),
    number("p2", "point", "A est à 8,5 cm de O. A' est son symétrique par rapport à O. Quelle est la longueur AA', en cm ?", Fraction(17), 1, ["AA' = 2 × OA."], ["2 × 8,5 = 17 cm."], units=["cm"]),
    number("p3", "point", "AA' = 25 cm, A' étant le symétrique de A par rapport à O. Quelle est la longueur OA, en cm ?", d("12,5"), 2, ["OA est la moitié de AA'."], ["25 ÷ 2 = 12,5 cm."], units=["cm"]),
    ordered("p4", "point", "O (0 ; 0) et A (3 ; 5). Écris les coordonnées de A', symétrique de A par rapport à O, sous la forme abscisse ; ordonnée.", [Fraction(-3), Fraction(-5)], 1, ["Avec O à l'origine, A' = (−x ; −y)."], ["A' (−3 ; −5)."]),
    ordered("p5", "point", "O (2 ; 2) et A (6 ; 3). Écris les coordonnées de A', symétrique de A par rapport à O, sous la forme abscisse ; ordonnée.", [Fraction(-2), Fraction(1)], 2, ["A' = (2a − x ; 2b − y)."], ["2 × 2 − 6 = −2 et 2 × 2 − 3 = 1.", "A' (−2 ; 1)."]),
    ordered("p6", "point", "O (5 ; 4) et A (1 ; 7). Écris les coordonnées de A', symétrique de A par rapport à O, sous la forme abscisse ; ordonnée.", [Fraction(9), Fraction(1)], 2, ["A' = (2a − x ; 2b − y)."], ["2 × 5 − 1 = 9 et 2 × 4 − 7 = 1.", "A' (9 ; 1)."]),
    ordered("p7", "point", "A (2 ; 8) et A' (10 ; 4) sont symétriques par rapport à O. Écris les coordonnées de O sous la forme abscisse ; ordonnée.", [Fraction(6), Fraction(6)], 2, ["O est le milieu de [AA']."], ["(2 + 10) ÷ 2 = 6 et (8 + 4) ÷ 2 = 6.", "O (6 ; 6)."]),
    ordered("p8", "point", "A (−3 ; 2) et A' (5 ; −4) sont symétriques par rapport à O. Écris les coordonnées de O sous la forme abscisse ; ordonnée.", [Fraction(1), Fraction(-1)], 3, ["O est le milieu de [AA']."], ["(−3 + 5) ÷ 2 = 1 et (2 + (−4)) ÷ 2 = −1.", "O (1 ; −1)."]),
    choice("p9", "point", "A' est le symétrique de A par rapport à O. Que peut-on affirmer ?", ["O est le milieu de [AA']", "O est sur la médiatrice de [AA'] seulement", "A et A' sont confondus"], 0, 1, ["Définition du symétrique."], ["O est le milieu de [AA']."], wrong={1: "O est le milieu : il est même sur [AA'].", 2: "A et A' ne sont confondus que si A = O."}),
    choice("p10", "point", "Quel est le symétrique de O par rapport à O ?", ["Un point différent de O", "O lui-même", "Il n'existe pas"], 1, 1, ["O est le milieu de [OO]."], ["O est le milieu de [OO] : son symétrique est O."], wrong={0: "O est déjà à la même distance de lui-même.", 2: "Chaque point a un symétrique."}),
    number("p11", "figures", "[A'B'] est le symétrique de [AB] par rapport à O. AB = 3,8 cm. Quelle est la longueur A'B', en cm ?", d("3,8"), 1, ["Les longueurs sont conservées."], ["A'B' = AB = 3,8 cm."], units=["cm"]),
    number("p12", "figures", "L'angle ∠ABC mesure 113°. Quelle est la mesure de son symétrique, en degrés ?", Fraction(113), 1, ["Les angles sont conservés."], ["Même mesure : 113°."], units=["°", "degrés", "degré"]),
    number("p13", "figures", "Un triangle a pour côtés 9 cm, 12 cm et 15 cm. Quel est le périmètre de son symétrique par rapport à un point O, en cm ?", Fraction(36), 2, ["Les longueurs sont conservées."], ["9 + 12 + 15 = 36 cm."], units=["cm"]),
    number("p14", "figures", "Un cercle de diamètre 10 cm a pour symétrique un cercle par rapport à un point O. Quel est le rayon de ce cercle, en cm ?", Fraction(5), 2, ["Le rayon est conservé."], ["Rayon = 10 ÷ 2 = 5 cm, et il est conservé."], units=["cm"]),
    choice("p15", "figures", "Les droites (d) et (d') sont parallèles. Que peut-on dire de leurs symétriques par rapport à O ?", ["Elles sont parallèles", "Elles sont perpendiculaires", "Elles sont confondues"], 0, 2, ["La symétrie centrale conserve le parallélisme."], ["Deux droites parallèles ont des symétriques parallèles."], wrong={1: "La symétrie centrale ne change pas la position relative des droites.", 2: "Les symétriques ne sont pas confondus en général."}),
    choice("p16", "figures", "Les droites (d) et (d') sont perpendiculaires. Que peut-on dire de leurs symétriques ?", ["Elles sont parallèles", "Elles sont perpendiculaires", "Elles sont confondues"], 1, 2, ["La symétrie centrale conserve les angles."], ["Deux droites perpendiculaires ont des symétriques perpendiculaires."], wrong={0: "Les angles sont conservés, un angle droit reste droit.", 2: "Les symétriques ne sont pas confondus en général."}),
    number("p17", "figures", "Un triangle a une aire de 36 cm². Quelle est l'aire de son symétrique par rapport à un point O, en cm² ?", Fraction(36), 2, ["La symétrie centrale conserve les aires."], ["Même aire : 36 cm²."], units=["cm2", "cm²"]),
    number("p18", "figures", "Les points A, B et C sont alignés, avec AB = 4 cm et BC = 5 cm, B entre A et C. Leurs symétriques A', B' et C' sont alignés. Quelle est la longueur A'C', en cm ?", Fraction(9), 3, ["A'C' = AC."], ["AC = 4 + 5 = 9 cm.", "A'C' = AC = 9 cm."], units=["cm"]),
    number("p19", "centre", "ABCD est un parallélogramme de centre O. BD = 18 cm. Quelle est la longueur OB, en cm ?", Fraction(9), 1, ["O est le milieu de [BD]."], ["OB = 18 ÷ 2 = 9 cm."], units=["cm"]),
    number("p20", "centre", "ABCD est un parallélogramme de centre O. OC = 4,6 cm. Quelle est la longueur AC, en cm ?", d("9,2"), 2, ["AC = 2 × OC."], ["AC = 2 × 4,6 = 9,2 cm."], units=["cm"]),
    number("p21", "centre", "Un segment mesure 15 cm. À quelle distance de chaque extrémité est son centre de symétrie, en cm ?", d("7,5"), 2, ["C'est son milieu."], ["15 ÷ 2 = 7,5 cm."], units=["cm"]),
    number("p22", "centre", "Un cercle a un diamètre de 20 cm. A est un point du cercle et A' son symétrique par rapport au centre. Quelle est la longueur AA', en cm ?", Fraction(20), 2, ["AA' est un diamètre."], ["AA' = 20 cm."], units=["cm"]),
    choice("p23", "centre", "Quelle figure a un centre de symétrie ?", ["Un triangle quelconque", "Un parallélogramme", "Un triangle équilatéral"], 1, 1, ["Pense au demi-tour."], ["Le parallélogramme a pour centre de symétrie l'intersection de ses diagonales."], wrong={0: "Un triangle n'a pas de centre de symétrie.", 2: "Un triangle équilatéral non plus."}),
    choice("p24", "centre", "Le centre de symétrie d'un segment est :", ["son milieu", "une extrémité", "n'importe quel point du segment"], 0, 1, ["Un demi-tour doit échanger les extrémités."], ["Le centre de symétrie d'un segment est son milieu."], wrong={1: "Une extrémité resterait fixe, l'autre irait loin du segment.", 2: "Il faut un point précis."}),
    choice("p25", "centre", "Combien de centres de symétrie un parallélogramme a-t-il ?", ["Aucun", "Un", "Quatre"], 1, 2, ["C'est l'intersection de ses diagonales."], ["Un seul : l'intersection de ses diagonales."], wrong={0: "Il en a un.", 2: "Il n'y en a qu'un."}),
    number("p26", "problemes", "ABCD est un parallélogramme de centre O. OA = 3,5 cm et OB = 2,5 cm. Quelle est la somme des diagonales AC + BD, en cm ?", Fraction(12), 2, ["AC = 2 × OA et BD = 2 × OB."], ["AC = 7 et BD = 5.", "7 + 5 = 12 cm."], units=["cm"]),
    ordered("p27", "problemes", "O (4 ; 1) et A (9 ; 6). Écris les coordonnées de A', symétrique de A par rapport à O, sous la forme abscisse ; ordonnée.", [Fraction(-1), Fraction(-4)], 3, ["A' = (2a − x ; 2b − y)."], ["2 × 4 − 9 = −1 et 2 × 1 − 6 = −4.", "A' (−1 ; −4)."]),
    ordered("p28", "problemes", "A (0 ; 0) et A' (8 ; 6) sont symétriques par rapport à O. Écris les coordonnées de O sous la forme abscisse ; ordonnée.", [Fraction(4), Fraction(3)], 2, ["O est le milieu de [AA']."], ["(0 + 8) ÷ 2 = 4 et (0 + 6) ÷ 2 = 3.", "O (4 ; 3)."]),
    number("p29", "problemes", "Un rectangle de 9 cm sur 6 cm a un symétrique par rapport à O. Quel est son périmètre, en cm ?", Fraction(30), 2, ["Les longueurs sont conservées."], ["2 × (9 + 6) = 30 cm."], units=["cm"]),
    number("p30", "problemes", "Deux cercles symétriques par rapport à O ont leurs centres à 24 cm l'un de l'autre. Quelle est la distance de O à chaque centre, en cm ?", Fraction(12), 2, ["O est le milieu des deux centres."], ["24 ÷ 2 = 12 cm."], units=["cm"]),
    choice("p31", "problemes", "Léa dit : « le symétrique d'une droite par rapport à un point est toujours la même droite ». Qu'en penses-tu ?", ["Elle a raison", "Elle a tort : c'est une droite parallèle, la même seulement si elle passe par O", "Elle a tort : c'est une droite perpendiculaire"], 1, 3, ["Un demi-tour renverse la droite sans la tourner."], ["Le symétrique est une droite parallèle ; c'est la même droite seulement si elle passe par O."], wrong={0: "Ce n'est vrai que pour une droite qui passe par O.", 2: "Un demi-tour ne tourne pas d'un quart de tour."}),
    number("p32", "problemes", "A est à 6 cm de O. B est à 10 cm de O. A' et B' sont leurs symétriques. Quelle est la longueur A'B' + AA', sachant que A, O, B sont alignés avec O entre A et B ? (A'B' = AB)", Fraction(28), 3, ["AB = AO + OB, et A'B' = AB. AA' = 2 × OA."], ["AB = 6 + 10 = 16 cm, donc A'B' = 16.", "AA' = 2 × 6 = 12.", "16 + 12 = 28 cm."], units=["cm"]),
]

SUMMARY = [
    definition("Symétrique d'un point", "A' est le symétrique de A par rapport à O si O est le milieu de [AA'] : OA' = OA, AA' = 2 × OA, et A, O, A' sont alignés. Le symétrique de O est O. Sur un quadrillage, A' = (2a − x ; 2b − y) pour O (a ; b) et A (x ; y)."),
    rule("Propriétés", "La symétrie centrale conserve les longueurs, les angles, l'alignement, le parallélisme, la perpendicularité, les aires et les cercles (même rayon). Le symétrique d'une droite est une droite parallèle."),
    rule("Centre de symétrie", "Segment : son milieu. Cercle et disque : leur centre. Parallélogramme : l'intersection de ses diagonales. Un triangle n'a pas de centre de symétrie."),
    para("Les erreurs à éviter : confondre symétrie centrale et symétrie par rapport à une droite ; croire que le symétrique d'une droite est la même droite ; placer le symétrique à une distance différente de O ; prendre un sommet pour le centre d'un parallélogramme."),
]

CONCEPTS = {
    "point": ("Symétrique d'un point", "point"),
    "figures": ("Symétrique d'un segment, d'une droite, d'un angle, d'un cercle", "figures"),
    "centre": ("Centre de symétrie d'une figure", "centre"),
    "problemes": ("Problèmes de symétrie centrale", "problemes"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    cm, cm2 = ["cm"], ["cm2", "cm²"]
    # 1. symmetric coordinates
    a, b, x, y = rng.randint(1, 9), rng.randint(1, 9), rng.randint(1, 12), rng.randint(1, 12)
    questions.append(ordered("a1", "point", f"O ({a} ; {b}) et A ({x} ; {y}). Écris les coordonnées de A', symétrique de A par rapport à O, sous la forme abscisse ; ordonnée.", [Fraction(2 * a - x), Fraction(2 * b - y)], 2,
                             ["A' = (2a − x ; 2b − y)."], [f"2 × {a} − {x} = {2 * a - x} et 2 × {b} − {y} = {2 * b - y}.", f"A' ({2 * a - x} ; {2 * b - y})."]))
    # 2. the whole segment AA'
    r = rng.randint(3, 20)
    questions.append(number("a2", "point", f"A est à {r} cm de O. A' est son symétrique par rapport à O. Quelle est la longueur AA', en cm ?", Fraction(2 * r), 1,
                            ["AA' = 2 × OA."], [f"2 × {r} = {2 * r} cm."], units=cm))
    # 3. half the segment
    r = rng.randint(4, 24)
    questions.append(number("a3", "point", f"AA' = {2 * r} cm, A' étant le symétrique de A par rapport à O. Quelle est la longueur OA, en cm ?", Fraction(r), 1,
                            ["OA est la moitié de AA'."], [f"{2 * r} ÷ 2 = {r} cm."], units=cm))
    # 4. the length of the symmetric segment
    ab = Fraction(rng.randint(2, 30)) + rng.choice([0, Fraction(1, 2)])
    questions.append(number("a4", "figures", f"[A'B'] est le symétrique de [AB] par rapport à O. AB = {show(ab)} cm. Quelle est la longueur A'B', en cm ?", ab, 1,
                            ["Les longueurs sont conservées."], ["A'B' = AB."], units=cm))
    # 5. the angle of the symmetric
    angle = rng.randint(10, 170)
    questions.append(number("a5", "figures", f"Un angle mesure {angle}°. Quelle est la mesure de son symétrique par rapport à un point O, en degrés ?", Fraction(angle), 1,
                            ["Les angles sont conservés."], [f"Même mesure : {angle}°."], units=["°", "degrés", "degré"]))
    # 6. the radius of the symmetric circle
    diameter = 2 * rng.randint(2, 15)
    questions.append(number("a6", "figures", f"Un cercle de diamètre {diameter} cm a pour symétrique un cercle par rapport à un point O. Quel est le rayon de ce cercle, en cm ?", Fraction(diameter // 2), 2,
                            ["Le rayon est conservé."], [f"{diameter} ÷ 2 = {diameter // 2} cm."], units=cm))
    # 7. the perimeter of the symmetric triangle
    sides = rng.sample(range(4, 20), 3)
    questions.append(number("a7", "figures", f"Un triangle a pour côtés {sides[0]} cm, {sides[1]} cm et {sides[2]} cm. Quel est le périmètre de son symétrique par rapport à un point O, en cm ?", Fraction(sum(sides)), 2,
                            ["Les longueurs sont conservées."], [f"{sides[0]} + {sides[1]} + {sides[2]} = {sum(sides)} cm."], units=cm))
    # 8. the area of the symmetric
    u, v = rng.randint(3, 15), rng.randint(3, 15)
    questions.append(number("a8", "figures", f"Un rectangle de {u} cm sur {v} cm a un symétrique par rapport à un point O. Quelle est l'aire de ce symétrique, en cm² ?", Fraction(u * v), 2,
                            ["Les aires sont conservées."], [f"{u} × {v} = {u * v} cm²."], units=cm2))
    # 9. which figure has a centre of symmetry
    good = rng.choice(["Un parallélogramme", "Un cercle", "Un segment"])
    bad = rng.sample(["Un triangle quelconque", "Un triangle équilatéral", "Un triangle rectangle"], 2)
    options = [good] + bad
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a9", "centre", "Quelle figure a un centre de symétrie ?", [options[i] for i in order], order.index(0), 2,
                            ["Pense au demi-tour : la figure doit se retrouver identique."], ["Un triangle n'a pas de centre de symétrie : la bonne réponse est la figure qui en a un."],
                            wrong={order.index(1): "Un triangle n'a pas de centre de symétrie.", order.index(2): "Un triangle n'a pas de centre de symétrie."}))
    # 10. the centre from two symmetric points
    a, b = rng.randint(1, 9), rng.randint(1, 9)
    x, y = rng.randint(1, 9), rng.randint(1, 9)
    xp, yp = 2 * a - x, 2 * b - y
    questions.append(ordered("a10", "problemes", f"A ({x} ; {y}) et A' ({xp} ; {yp}) sont symétriques par rapport à O. Écris les coordonnées de O sous la forme abscisse ; ordonnée.", [Fraction(a), Fraction(b)], 3,
                             ["O est le milieu de [AA']."], [f"({x} + {xp}) ÷ 2 = {a} et ({y} + {yp}) ÷ 2 = {b}.", f"O ({a} ; {b})."]))
    # 11. the diagonals of a parallelogram
    oa, ob = rng.randint(2, 12), rng.randint(2, 12)
    questions.append(number("a11", "centre", f"ABCD est un parallélogramme de centre O. OA = {oa} cm et OB = {ob} cm. Quelle est la longueur AC + BD, en cm ?", Fraction(2 * (oa + ob)), 2,
                            ["AC = 2 × OA et BD = 2 × OB."], [f"AC = {2 * oa} et BD = {2 * ob}.", f"{2 * oa} + {2 * ob} = {2 * (oa + ob)} cm."], units=cm))
    # 12. distance between the centres of symmetric circles
    half = rng.randint(5, 40)
    questions.append(number("a12", "problemes", f"Deux cercles symétriques par rapport à O ont leurs centres à {2 * half} cm l'un de l'autre. Quelle est la distance de O à chacun des centres, en cm ?", Fraction(half), 2,
                            ["O est le milieu des deux centres."], [f"{2 * half} ÷ 2 = {half} cm."], units=cm))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=15, title="La symétrie centrale", language="fr",
    intro="Quand on tourne une feuille d'un demi-tour autour d'une punaise, chaque point va de l'autre côté de la punaise, à la même distance. "
          "Ce chapitre t'apprend à trouver le symétrique d'un point par rapport à un point, les propriétés de cette transformation et le centre de symétrie d'une figure.",
    objectives=["Reconnaître et calculer le symétrique d'un point par rapport à un point, avec le milieu et avec des coordonnées.",
                "Connaître les propriétés de la symétrie centrale : longueurs, angles, alignement, parallélisme et cercles conservés.",
                "Reconnaître le centre de symétrie d'un segment, d'un cercle et d'un parallélogramme.",
                "Résoudre des problèmes avec la symétrie centrale."],
    prerequisites=[{"text": "Connaître le milieu d'un segment et les droites parallèles.", "chapter": "sn-6e-droites-cercles"},
                   {"text": "Connaître le parallélogramme et ses diagonales.", "chapter": "sn-6e-parallelogramme"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Fifteenth chapter of the Senegal Sixième course. Its contents follow lesson 7 of the Côte d'Ivoire Sixième programme (the symmetric of a point, a segment, a line, an angle and a circle, and the centre of symmetry of a figure), which was read for it, "
                "so it is also offered there, but the programme's own situations are not reproduced. The figures are drawn by the app. Constructing a symmetric figure with a ruler and a compass cannot be done on a screen, so it is not covered. "
                "It has not been checked against the official Senegalese programme.",
)
