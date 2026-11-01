"""Cinquième, Triangles particuliers: the eighth chapter of the Senegal Cinquième course, written in French.

The contents follow the lesson "Triangles" of the Côte d'Ivoire Cinquième programme (the axes of symmetry of the special triangles, their characteristics, how to show that a triangle is
isosceles, equilateral or right, and the bisector of an angle), which was read for this chapter. Every explanation, example, figure and exercise was written independently, with our own
numbers. It builds on the Sixième chapter on triangles and on the Cinquième chapter on angles. Constructions with a ruler and a compass cannot be done on a screen: they are described.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a "verify" expression that the tests evaluate.
The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .figures import Figure, figure
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-5e-triangles"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")
DEG = ["°", "degrés", "degré", "deg", "degres"]

# ----- Figures -----
ISO_AXIS = (Figure().point("A", 170, 35, 8, -6).point("B", 80, 165, -14, 22).point("C", 260, 165, 6, 22).point("H", 170, 165, 8, 22)
            .segment("A", "B").segment("B", "C").segment("C", "A").segment("A", "H", "fig-dash").right_angle("H", "C", "A", 12).tick("A", "B", 1).tick("A", "C", 1).tick("B", "H", 2).tick("H", "C", 2))
EQUI_AXES = (Figure().point("A", 170, 35, 8, -6).point("B", 95, 165, -14, 22).point("C", 245, 165, 6, 22).point("O", 170, 118, 8, 4)
             .segment("A", "B").segment("B", "C").segment("C", "A").segment("A", "O", "fig-dash").segment("B", "O", "fig-dash").segment("C", "O", "fig-dash"))
RIGHT_ISO = (Figure().point("A", 80, 165, -14, 22).point("B", 80, 45, 8, -4).point("C", 240, 165, 6, 22)
             .segment("A", "B").segment("B", "C").segment("C", "A").right_angle("A", "B", "C", 16).tick("A", "B", 1).tick("A", "C", 1).segment("A", "B", "fig-seg"))
BISECTOR = (Figure().point("A", 60, 160, -14, 22).point("B", 290, 160, 6, 22).point("C", 120, 40, -14, -6).point("D", 215, 100, 8, 8)
            .segment("A", "B").segment("A", "C").segment("B", "C").segment("A", "D", "fig-dash").arc("A", "B", "D", 40).arc("A", "D", "C", 52))

# ----- Section 1: axes of symmetry -----
S1 = Section(
    "axes", "Les axes de symétrie des triangles particuliers", 24, "axes",
    "Savoir ce qu'est un axe de symétrie, compter les axes de symétrie d'un triangle quelconque, isocèle, équilatéral et rectangle, et en déduire des propriétés.",
    [
        para("Plie un triangle isocèle en papier le long de la droite qui passe par son sommet principal et le milieu de la base : les deux moitiés se recouvrent exactement. Cette droite est un axe de symétrie."),
        definition("Axe de symétrie",
                   "Une droite est un axe de symétrie d'une figure si, quand on plie la figure le long de cette droite, les deux moitiés se superposent. Une figure peut avoir un axe, plusieurs axes ou aucun."),
        rule("Axes des triangles",
             "Un triangle quelconque n'a pas d'axe de symétrie. Un triangle isocèle a un axe de symétrie : la médiatrice de la base. Un triangle équilatéral a trois axes de symétrie, les trois médiatrices de ses côtés. "
             "Un triangle rectangle isocèle a un axe de symétrie. Un triangle rectangle qui n'est pas isocèle n'en a pas."),
        figure(ISO_AXIS, "Un triangle isocèle ABC en A avec son axe de symétrie (AH) en pointillés, perpendiculaire à la base [BC] en son milieu H.", "L'axe de symétrie (AH) du triangle isocèle ABC est la médiatrice de la base [BC] : il passe par le sommet A et par le milieu H de [BC]."),
        rule("Conséquences pour un triangle isocèle",
             "Dans un triangle isocèle de sommet principal A, l'axe de symétrie est à la fois la hauteur, la médiane, la médiatrice de la base et la bissectrice de l'angle au sommet. "
             "Les deux angles à la base sont égaux et les deux côtés égaux sont symétriques l'un de l'autre."),
        figure(EQUI_AXES, "Un triangle équilatéral ABC avec ses trois axes de symétrie en pointillés qui se croisent au centre O.", "Un triangle équilatéral a trois axes de symétrie, qui se coupent en un même point."),
        example("Exemple 1", "Combien d'axes de symétrie a un triangle équilatéral ? un triangle isocèle non équilatéral ? un triangle quelconque ?",
                "On utilise le tableau des axes de symétrie des triangles.",
                [("Équilatéral : un axe par sommet", "Trois axes."),
                 ("Isocèle non équilatéral : un seul axe", "Celui qui passe par le sommet principal."),
                 ("Quelconque : aucun axe", "Aucun pli ne superpose les deux moitiés.")],
                "3, 1 et 0.", "3+1+0==4"),
        example("Exemple 2", "ABC est isocèle en A, H est le milieu de [BC] et BC = 10 cm. Quelle est la longueur BH ? Que peut-on dire de la droite (AH) ?",
                "(AH) est l'axe de symétrie : elle passe par le milieu de la base.",
                [(N("BH = 10 \\div 2") + " = " + N("5"), "H est le milieu de [BC]."),
                 ("(AH) est la hauteur, la médiane et la médiatrice", "Propriétés de l'axe d'un triangle isocèle.")],
                N("BH = 5") + " cm ; (AH) est aussi la hauteur issue de A.", "10//2==5"),
        example("Exemple 3", "Dans le triangle isocèle ABC en A, l'angle au sommet mesure 40°. L'axe (AH) coupe cet angle en deux angles égaux. Quelle est la mesure de l'angle BAH ?",
                "L'axe est la bissectrice de l'angle au sommet.",
                [(N("40 \\div 2") + " = " + N("20"), "La bissectrice partage l'angle en deux angles égaux.")],
                N("\\widehat{BAH} = 20") + "°.", "40//2==20"),
        example("Exemple 4", "Un triangle rectangle isocèle a un angle droit en A. Quelle est la mesure de chacun des deux autres angles ? Combien d'axes a-t-il ?",
                "Les deux angles aigus sont égaux et complémentaires.",
                [(N("90 \\div 2") + " = " + N("45"), "Chaque angle aigu mesure 45°."),
                 ("Un seul axe : la médiatrice de l'hypoténuse", "Il passe par l'angle droit.")],
                N("45") + "° et un seul axe de symétrie.", "90//2==45"),
        warning("Un axe de symétrie est une droite : pour le dessiner, on le prolonge au-delà de la figure. Et un triangle isocèle non équilatéral n'a qu'un axe : pas un par côté. Attention aussi : tous les triangles rectangles n'ont pas d'axe, seulement le rectangle isocèle."),
    ],
    [
        number("s1-g1", "axes", "Combien d'axes de symétrie a un triangle équilatéral ?", Fraction(3), hints=["Un par sommet."], solution=["3 axes."]),
        number("s1-g2", "axes", "Combien d'axes de symétrie a un triangle isocèle qui n'est pas équilatéral ?", Fraction(1), hints=["La médiatrice de la base."], solution=["1 axe."]),
        number("s1-g3", "axes", "Combien d'axes de symétrie a un triangle dont les trois côtés ont des longueurs différentes ?", Fraction(0), hints=["Aucun pli ne marche."], solution=["Aucun axe."]),
        number("s1-g4", "axes", "ABC est isocèle en A, H est le milieu de [BC] et BC = 14 cm. Quelle est la longueur BH, en cm ?", Fraction(7), units=["cm"], hints=["H est le milieu."], solution=["14 ÷ 2 = 7 cm."]),
        number("s1-g5", "axes", "ABC est isocèle en A, avec un angle au sommet de 64°. L'axe (AH) est la bissectrice de cet angle. Quelle est la mesure de l'angle BAH, en degrés ?", Fraction(32), units=DEG, hints=["La moitié."], solution=["64 ÷ 2 = 32°."]),
    ])

# ----- Section 2: isosceles triangles -----
S2 = Section(
    "isocele", "Montrer qu'un triangle est isocèle, et calculer avec ses angles", 24, "isocele",
    "Utiliser l'égalité de deux côtés ou de deux angles pour montrer qu'un triangle est isocèle, et calculer des longueurs et des angles.",
    [
        para("Un triangle est isocèle si deux de ses côtés sont égaux. On peut le savoir en mesurant, mais aussi en regardant les angles : les deux propriétés vont ensemble."),
        rule("Triangle isocèle : côtés et angles",
             "Si un triangle a deux côtés égaux, alors il a deux angles égaux (les angles opposés à ces côtés). Réciproquement, si un triangle a deux angles égaux, alors il a deux côtés égaux : il est isocèle, et les côtés égaux sont ceux qui sont opposés aux angles égaux."),
        example("Exemple 1", "Le triangle ABC a des angles B = 50° et C = 50°. Que peut-on dire ? Quelle est la mesure de l'angle A ?",
                "Deux angles sont égaux : on applique la réciproque. Puis on utilise la somme des angles.",
                [("Les angles en B et en C sont égaux", "Le triangle est isocèle en A : AB = AC."),
                 (N("180 - (50 + 50)") + " = " + N("80"), "Somme des angles.")],
                "ABC est isocèle en A, et " + N("\\widehat{A} = 80") + "°.", "180-(50+50)==80"),
        example("Exemple 2", "Le triangle ABC est isocèle en A, avec B = 65°. Que valent les angles C et A ?",
                "Les angles à la base sont égaux.",
                [(N("\\widehat{C} = \\widehat{B}") + " = " + N("65") + "°", "Angles à la base d'un triangle isocèle."),
                 (N("180 - (65 + 65)") + " = " + N("50"), "Somme des angles.")],
                N("\\widehat{C} = 65") + "° et " + N("\\widehat{A} = 50") + "°.", "180-(65+65)==50"),
        example("Exemple 3", "Un triangle a des côtés de 7 cm, 7 cm et 5 cm. Quel est son périmètre ? Dans quel sommet est-il isocèle ?",
                "Deux côtés sont égaux : leur point commun est le sommet principal.",
                [(N("7 + 7 + 5") + " = " + N("19"), "Périmètre."),
                 ("Les côtés égaux se rejoignent au sommet opposé au côté de 5 cm", "Le sommet principal est opposé à la base.")],
                "Périmètre " + N("19") + " cm.", "7+7+5==19"),
        example("Exemple 4", "ABC est isocèle en A, avec un périmètre de 32 cm et une base BC = 12 cm. Quelle est la longueur de chaque côté égal ?",
                "On retire la base du périmètre, puis on partage en deux côtés égaux.",
                [(N("32 - 12") + " = " + N("20"), "Les deux côtés égaux font 20 cm ensemble."),
                 (N("20 \\div 2") + " = " + N("10"), "Chacun mesure 10 cm.")],
                N("AB = AC = 10") + " cm.", "32-12==20 and 20//2==10"),
        warning("Dans un triangle isocèle, les angles égaux sont à la base, donc ils sont opposés aux côtés égaux, pas adjacents à eux. Et un triangle isocèle peut avoir un angle obtus : alors c'est l'angle au sommet, jamais un angle à la base (deux angles obtus dépasseraient 180°)."),
    ],
    [
        number("s2-g1", "isocele", "Un triangle a des angles de 70° et de 70°. Quelle est la mesure du troisième, en degrés ?", Fraction(40), units=DEG, hints=["180 − 140."], solution=["180 − 140 = 40°."]),
        number("s2-g2", "isocele", "ABC est isocèle en A, avec B = 72°. Quelle est la mesure de l'angle A, en degrés ?", Fraction(36), units=DEG, hints=["C = B, puis la somme."], solution=["C = 72°.", "180 − 144 = 36°."]),
        number("s2-g3", "isocele", "ABC est isocèle en A, avec l'angle au sommet A = 100°. Quelle est la mesure de l'angle B, en degrés ?", Fraction(40), units=DEG, hints=["(180 − 100) ÷ 2."], solution=["80 ÷ 2 = 40°."]),
        number("s2-g4", "isocele", "ABC est isocèle en A, de périmètre 40 cm, avec BC = 14 cm. Quelle est la longueur de AB, en cm ?", Fraction(13), units=["cm"], hints=["(40 − 14) ÷ 2."], solution=["26 ÷ 2 = 13 cm."]),
        choice("s2-g5", "isocele", "Un triangle a deux angles égaux. Que peut-on dire ?", ["Il est isocèle", "Il est équilatéral", "Il est rectangle"], 0, hints=["Réciproque."], solution=["Deux angles égaux : deux côtés égaux, donc isocèle."], wrong={1: "Il faudrait trois angles égaux.", 2: "Rien n'indique un angle droit."}),
    ])

# ----- Section 3: equilateral and right triangles -----
S3 = Section(
    "equilateral", "Triangles équilatéraux et triangles rectangles", 22, "equilateral",
    "Montrer qu'un triangle est équilatéral ou rectangle avec des angles ou des longueurs, et connaître leurs propriétés.",
    [
        para("Les mêmes idées s'appliquent aux triangles équilatéraux et rectangles : on cherche des angles ou des côtés égaux, ou un angle droit."),
        rule("Équilatéral",
             "Un triangle est équilatéral si ses trois côtés sont égaux, ou si ses trois angles sont égaux (60° chacun), ou s'il est isocèle avec un angle de 60°. Il a trois axes de symétrie."),
        rule("Rectangle",
             "Un triangle est rectangle s'il a un angle droit. Si deux de ses angles sont complémentaires (leur somme est 90°), le troisième est droit et le triangle est rectangle. "
             "Un triangle rectangle isocèle a deux angles de 45° et un angle droit."),
        figure(RIGHT_ISO, "Un triangle ABC rectangle en A avec deux côtés AB et AC égaux marqués par un trait.", "Le triangle ABC est rectangle et isocèle en A : AB = AC et ses angles en B et en C mesurent 45°."),
        example("Exemple 1", "Un triangle a des angles de 60° et de 60°. Que peut-on dire ?",
                "On calcule le troisième angle, puis on compare.",
                [(N("180 - 120") + " = " + N("60"), "Le troisième angle mesure aussi 60°."),
                 ("Trois angles égaux", "Le triangle est équilatéral.")],
                "Il est équilatéral.", "180-120==60"),
        example("Exemple 2", "Un triangle ABC a des angles A = 38° et B = 52°. Que peut-on dire ?",
                "On calcule la somme de A et de B.",
                [(N("38 + 52") + " = " + N("90"), "Les deux angles sont complémentaires."),
                 (N("\\widehat{C} = 180 - 90") + " = " + N("90"), "Le troisième angle est droit.")],
                "Le triangle est rectangle en C.", "38+52==90 and 180-90==90"),
        example("Exemple 3", "Un triangle rectangle isocèle a des côtés égaux de 6 cm. Quelle est l'aire du triangle ?",
                "Les deux côtés de l'angle droit sont la base et la hauteur.",
                [(N("6 \\times 6 \\div 2") + " = " + N("18"), "Aire = base × hauteur ÷ 2.")],
                N("18") + " cm².", "6*6//2==18"),
        example("Exemple 4", "Un triangle équilatéral a un périmètre de 27 cm. Quelle est la longueur d'un côté ? Quelle est la mesure d'un angle ?",
                "Les trois côtés sont égaux et les trois angles mesurent 60°.",
                [(N("27 \\div 3") + " = " + N("9"), "Chaque côté mesure 9 cm."),
                 ("Chaque angle mesure 60°", "Triangle équilatéral.")],
                N("9") + " cm et " + N("60") + "°.", "27//3==9"),
        warning("Deux angles de 60° suffisent pour être équilatéral, car le troisième est alors forcé à 60°. Mais un seul angle de 60° ne suffit pas : un triangle isocèle avec un angle à la base de 60° est équilatéral, alors qu'un triangle avec un angle de 60° quelconque ne l'est pas toujours."),
    ],
    [
        choice("s3-g1", "equilateral", "Un triangle a des angles de 60°, 60° et 60°. Que peut-on dire ?", ["Il est équilatéral", "Il est rectangle", "Il est quelconque"], 0, hints=["Trois angles égaux."], solution=["Trois angles égaux : équilatéral."], wrong={1: "Il n'a pas d'angle droit.", 2: "Ses côtés sont égaux."}),
        choice("s3-g2", "equilateral", "Un triangle a des angles de 40° et de 50°. Que peut-on dire ?", ["Il est rectangle", "Il est isocèle", "Il est équilatéral"], 0, hints=["40 + 50 = 90."], solution=["Le troisième angle est 90° : rectangle."], wrong={1: "Les angles sont différents.", 2: "Les angles ne sont pas tous égaux."}),
        number("s3-g3", "equilateral", "Un triangle équilatéral a un périmètre de 45 cm. Quelle est la longueur d'un côté, en cm ?", Fraction(15), units=["cm"], hints=["45 ÷ 3."], solution=["15 cm."]),
        number("s3-g4", "equilateral", "Un triangle rectangle isocèle a des côtés égaux de 10 cm. Quelle est son aire, en cm² ?", Fraction(50), units=["cm2", "cm²"], hints=["Base × hauteur ÷ 2."], solution=["10 × 10 ÷ 2 = 50 cm²."]),
        number("s3-g5", "equilateral", "Un triangle rectangle isocèle : quelle est la mesure de chacun des deux angles aigus, en degrés ?", Fraction(45), units=DEG, hints=["90 ÷ 2."], solution=["45°."]),
    ])

# ----- Section 4: the bisector -----
S4 = Section(
    "bissectrice", "La bissectrice d'un angle dans un triangle", 22, "bissectrice",
    "Connaître la bissectrice d'un angle, la décrire avec la règle et le compas, et calculer avec elle dans un triangle.",
    [
        para("La bissectrice d'un angle est la demi-droite qui le partage en deux angles égaux : c'est l'axe de symétrie de l'angle. Dans un triangle, la bissectrice issue d'un sommet partage l'angle de ce sommet."),
        definition("Bissectrice",
                   "La bissectrice d'un angle est la demi-droite qui a pour origine le sommet de l'angle et qui le partage en deux angles de même mesure. "
                   "Pour la construire avec la règle et le compas : on trace un arc de cercle de centre le sommet qui coupe les deux côtés ; de ces deux points d'intersection, on trace deux arcs de même rayon qui se coupent ; la demi-droite qui passe par le sommet et par ce point est la bissectrice."),
        figure(BISECTOR, "Un triangle ABC avec la bissectrice (AD) de l'angle A en pointillés, qui partage l'angle BAC en deux angles égaux marqués par des arcs.", "La bissectrice [AD) partage l'angle BAC en deux angles égaux : BAD = DAC."),
        example("Exemple 1", "Dans le triangle ABC, l'angle A mesure 70° et [AD) est la bissectrice de l'angle A. Quelle est la mesure de l'angle BAD ?",
                "La bissectrice partage l'angle en deux angles égaux.",
                [(N("70 \\div 2") + " = " + N("35"), "BAD = DAC = 35°.")],
                N("\\widehat{BAD} = 35") + "°.", "70//2==35"),
        example("Exemple 2", "Dans le triangle ABC, B = 50° et C = 70°. La bissectrice [AD) coupe [BC] en D. Quelle est la mesure de BAD ?",
                "On calcule A avec la somme des angles, puis on prend la moitié.",
                [(N("\\widehat{A} = 180 - (50 + 70)") + " = " + N("60"), "Somme des angles."),
                 (N("60 \\div 2") + " = " + N("30"), "La bissectrice partage A en deux.")],
                N("\\widehat{BAD} = 30") + "°.", "180-(50+70)==60 and 60//2==30"),
        example("Exemple 3", "Dans le triangle ABD, BAD = 30° et B = 50°. Quelle est la mesure de l'angle ADB ?",
                "Dans le triangle ABD, la somme des angles est 180°.",
                [(N("30 + 50") + " = " + N("80"), "Somme de BAD et de B."),
                 (N("180 - 80") + " = " + N("100"), "Troisième angle.")],
                N("\\widehat{ADB} = 100") + "°.", "180-(30+50)==100"),
        example("Exemple 4", "Dans un triangle isocèle ABC en A, l'axe de symétrie (AH) est la bissectrice de l'angle A. Si l'angle B mesure 64°, quelle est la mesure de l'angle BAH ?",
                "On calcule A avec la somme, puis la moitié.",
                [(N("\\widehat{A} = 180 - 2 \\times 64") + " = " + N("52"), "C = B = 64°."),
                 (N("52 \\div 2") + " = " + N("26"), "BAH est la moitié de A.")],
                N("\\widehat{BAH} = 26") + "°.", "180-2*64==52 and 52//2==26"),
        warning("La bissectrice partage l'angle, pas le côté opposé : elle ne passe pas forcément par le milieu de [BC] (sauf dans un triangle isocèle en A). Et elle est une demi-droite issue du sommet, pas un segment qui s'arrête au côté opposé."),
    ],
    [
        number("s4-g1", "bissectrice", "[AD) est la bissectrice de l'angle A = 84° dans le triangle ABC. Quelle est la mesure de BAD, en degrés ?", Fraction(42), units=DEG, hints=["La moitié."], solution=["84 ÷ 2 = 42°."]),
        number("s4-g2", "bissectrice", "Dans le triangle ABC, B = 40° et C = 60°. [AD) est la bissectrice de A. Quelle est la mesure de BAD, en degrés ?", Fraction(40), units=DEG, hints=["A = 180 − 100."], solution=["A = 80°.", "BAD = 40°."]),
        number("s4-g3", "bissectrice", "Dans le triangle ABD, BAD = 25° et B = 65°. Quelle est la mesure de ADB, en degrés ?", Fraction(90), units=DEG, hints=["180 − 90."], solution=["25 + 65 = 90.", "180 − 90 = 90°."]),
        number("s4-g4", "bissectrice", "ABC est isocèle en A avec B = 70°. L'axe (AH) est la bissectrice de A. Quelle est la mesure de BAH, en degrés ?", Fraction(20), units=DEG, hints=["A = 180 − 140."], solution=["A = 40°.", "BAH = 20°."]),
        choice("s4-g5", "bissectrice", "La bissectrice d'un angle est :", ["la demi-droite qui le partage en deux angles égaux", "le segment qui joint les extrémités des côtés", "la droite perpendiculaire à un côté"], 0, hints=["Deux angles égaux."], solution=["C'est la demi-droite qui partage l'angle en deux angles égaux."], wrong={1: "Ce segment est une corde, pas la bissectrice.", 2: "La bissectrice n'est pas perpendiculaire en général."}),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "axes", "Combien d'axes de symétrie a un triangle rectangle isocèle ?", Fraction(1), 1, ["La médiatrice de l'hypoténuse."], ["1 axe."]),
    number("p2", "axes", "Combien d'axes de symétrie a un triangle rectangle dont les côtés de l'angle droit sont différents ?", Fraction(0), 1, ["Aucun pli ne marche."], ["0 axe."]),
    number("p3", "axes", "ABC est isocèle en A, BC = 9 cm, H milieu de [BC]. Quelle est la longueur HC, en cm ?", d("4,5"), 1, ["La moitié."], ["4,5 cm."], units=["cm"]),
    number("p4", "axes", "ABC est isocèle en A avec A = 50°. L'axe (AH) coupe A en deux. Quelle est la mesure de BAH, en degrés ?", Fraction(25), 1, ["La moitié."], ["25°."], units=DEG),
    choice("p5", "axes", "Quel triangle a trois axes de symétrie ?", ["L'équilatéral", "L'isocèle", "Le rectangle"], 0, 1, ["Un par sommet."], ["Le triangle équilatéral."], wrong={1: "Un isocèle non équilatéral n'a qu'un axe.", 2: "Un rectangle n'a au plus qu'un axe."}),
    choice("p6", "axes", "Quelle droite est l'axe de symétrie d'un triangle isocèle ?", ["La médiatrice de la base", "La médiatrice d'un côté égal", "Une droite parallèle à la base"], 0, 2, ["Elle passe par le sommet principal."], ["La médiatrice de la base."], wrong={1: "Un côté égal n'est pas échangé avec lui-même.", 2: "Un axe doit passer par le sommet."}),
    choice("p7", "axes", "Dans un triangle isocèle, l'axe de symétrie est aussi :", ["la hauteur, la médiane et la bissectrice de l'angle au sommet", "seulement la hauteur", "la droite parallèle à la base"], 0, 2, ["Plusieurs rôles à la fois."], ["Hauteur, médiane, médiatrice de la base et bissectrice de l'angle au sommet."], wrong={1: "Il joue plusieurs rôles.", 2: "Il est perpendiculaire à la base."}),
    number("p8", "axes", "Un triangle équilatéral a un côté de 8 cm. Combien de côtés égaux a-t-il ?", Fraction(3), 1, ["Équilatéral."], ["3 côtés égaux."]),
    number("p9", "isocele", "ABC est isocèle en A avec B = 55°. Quelle est la mesure de A, en degrés ?", Fraction(70), 1, ["C = B."], ["180 − 110 = 70°."], units=DEG),
    number("p10", "isocele", "ABC est isocèle en A avec A = 36°. Quelle est la mesure de B, en degrés ?", Fraction(72), 2, ["(180 − 36) ÷ 2."], ["72°."], units=DEG),
    number("p11", "isocele", "Un triangle a des angles de 40° et de 100°. Quelle est la mesure du troisième angle, en degrés ?", Fraction(40), 2, ["180 − 140."], ["40° : deux angles de 40° égaux, donc isocèle."], units=DEG),
    number("p12", "isocele", "ABC est isocèle en A, avec AB = 12 cm et BC = 8 cm. Quel est son périmètre, en cm ?", Fraction(32), 1, ["AC = AB."], ["12 + 12 + 8 = 32 cm."], units=["cm"]),
    number("p13", "isocele", "ABC est isocèle en A, de périmètre 50 cm, avec AB = 18 cm. Quelle est la longueur BC, en cm ?", Fraction(14), 2, ["50 − 36."], ["14 cm."], units=["cm"]),
    number("p14", "isocele", "Un triangle isocèle a un angle de 80°. Si c'est un angle à la base, quelle est la mesure de l'angle au sommet, en degrés ?", Fraction(20), 3, ["180 − 160."], ["20°."], units=DEG),
    number("p15", "isocele", "Un triangle isocèle a un angle de 80°. Si c'est l'angle au sommet, quelle est la mesure d'un angle à la base, en degrés ?", Fraction(50), 3, ["(180 − 80) ÷ 2."], ["50°."], units=DEG),
    choice("p16", "isocele", "Un triangle a un angle de 110°. Peut-il être isocèle ?", ["Oui, avec 110° au sommet", "Non", "Oui, avec 110° à la base"], 0, 3, ["Deux angles de 110° dépasseraient 180°."], ["L'angle de 110° est l'angle au sommet, les deux angles à la base mesurent 35°."], wrong={1: "Isocèle avec angle au sommet de 110°.", 2: "Deux angles à 110° font 220°."}),
    number("p17", "equilateral", "Quelle est la mesure d'un angle d'un triangle équilatéral, en degrés ?", Fraction(60), 1, ["180 ÷ 3."], ["60°."], units=DEG),
    number("p18", "equilateral", "Un triangle équilatéral a un périmètre de 36 cm. Quelle est la longueur d'un côté, en cm ?", Fraction(12), 1, ["36 ÷ 3."], ["12 cm."], units=["cm"]),
    number("p19", "equilateral", "Un triangle isocèle a un angle de 60°. Les deux autres angles mesurent ensemble combien de degrés ?", Fraction(120), 2, ["180 − 60."], ["120° : si c'est un angle à la base, il est équilatéral."], units=DEG),
    choice("p20", "equilateral", "Un triangle a des angles de 30° et de 60°. Que peut-on dire ?", ["Il est rectangle", "Il est équilatéral", "Il est isocèle"], 0, 2, ["30 + 60 = 90."], ["Le troisième angle mesure 90°."], wrong={1: "Ses angles ne sont pas tous égaux.", 2: "Aucun angle n'est égal à un autre."}),
    number("p21", "equilateral", "Un triangle rectangle isocèle a des côtés égaux de 12 cm. Quelle est son aire, en cm² ?", Fraction(72), 2, ["12 × 12 ÷ 2."], ["72 cm²."], units=["cm2", "cm²"]),
    number("p22", "equilateral", "Un triangle rectangle a un angle de 34°. Quelle est la mesure de l'autre angle aigu, en degrés ?", Fraction(56), 1, ["90 − 34."], ["56°."], units=DEG),
    number("p23", "equilateral", "Un triangle rectangle isocèle a une hypoténuse de 10 cm. Combien d'angles de 45° a-t-il ?", Fraction(2), 2, ["Les deux angles aigus."], ["2 angles de 45°."]),
    number("p24", "equilateral", "Un triangle équilatéral a un périmètre de 24 cm. Combien d'axes de symétrie a-t-il ?", Fraction(3), 1, ["Un par sommet."], ["3 axes."]),
    number("p25", "bissectrice", "[AD) est la bissectrice de A = 90°. Quelle est la mesure de BAD, en degrés ?", Fraction(45), 1, ["La moitié."], ["45°."], units=DEG),
    number("p26", "bissectrice", "Dans le triangle ABC, B = 30° et C = 50°. [AD) est la bissectrice de A. Quelle est la mesure de BAD, en degrés ?", Fraction(50), 2, ["A = 100°."], ["A = 180 − 80 = 100°.", "BAD = 50°."], units=DEG),
    number("p27", "bissectrice", "Dans le triangle ABD, BAD = 20° et B = 70°. Quelle est la mesure de ADB, en degrés ?", Fraction(90), 2, ["180 − 90."], ["90°."], units=DEG),
    number("p28", "bissectrice", "ABC est isocèle en A avec B = 75°. L'axe (AH) est la bissectrice de A. Quelle est la mesure de BAH, en degrés ?", Fraction(15), 3, ["A = 30°."], ["A = 180 − 150 = 30°.", "BAH = 15°."], units=DEG),
    number("p29", "bissectrice", "[AD) est la bissectrice de l'angle A d'un triangle. Si BAD = 28°, quelle est la mesure de A, en degrés ?", Fraction(56), 2, ["Le double."], ["56°."], units=DEG),
    number("p30", "bissectrice", "Dans le triangle ABC, A = 80°. [AD) est la bissectrice, B = 60°. Quelle est la mesure de l'angle ADB, en degrés ?", Fraction(80), 3, ["Triangle ABD : BAD = 40°, B = 60°."], ["BAD = 40°.", "ADB = 180 − 100 = 80°."], units=DEG),
    choice("p31", "bissectrice", "La bissectrice de l'angle A passe-t-elle toujours par le milieu du côté opposé ?", ["Non, seulement dans un triangle isocèle en A", "Oui, toujours", "Non, jamais"], 0, 3, ["Cas particulier."], ["Seulement dans un triangle isocèle en A, où elle est aussi médiane."], wrong={1: "C'est vrai dans un cas particulier.", 2: "C'est vrai dans le cas isocèle."}),
    choice("p32", "bissectrice", "Un triangle équilatéral a trois angles de 60°. Que mesure chaque angle formé par une bissectrice ?", ["30°", "60°", "45°"], 0, 2, ["60 ÷ 2."], ["30°."], wrong={1: "60° est l'angle entier.", 2: "45° serait la moitié de 90°."}),
]

SUMMARY = [
    rule("Axes de symétrie", "Triangle quelconque : 0 axe. Isocèle : 1 axe (médiatrice de la base). Équilatéral : 3 axes. Rectangle isocèle : 1 axe. Dans un triangle isocèle, l'axe est hauteur, médiane, médiatrice de la base et bissectrice de l'angle au sommet."),
    rule("Triangles particuliers", "Deux côtés égaux ⇔ deux angles égaux (isocèle). Trois angles de 60° ⇔ équilatéral. Deux angles complémentaires ⇒ rectangle. Rectangle isocèle : 45°, 45° et 90°."),
    rule("Bissectrice", "La bissectrice d'un angle est la demi-droite qui le partage en deux angles égaux. Dans un triangle, on trouve l'angle manquant avec la somme 180°, puis la moitié."),
    para("Les erreurs à éviter : croire qu'un triangle isocèle a plusieurs axes ; placer les angles égaux à côté des côtés égaux ; oublier qu'un angle obtus ne peut être qu'au sommet ; croire que la bissectrice passe par le milieu du côté opposé."),
]

CONCEPTS = {
    "axes": ("Axes de symétrie des triangles", "axes"),
    "isocele": ("Triangle isocèle", "isocele"),
    "equilateral": ("Triangles équilatéral et rectangle", "equilateral"),
    "bissectrice": ("Bissectrice d'un angle", "bissectrice"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    # 1. the number of axes
    kinds = [("un triangle équilatéral", 3), ("un triangle isocèle qui n'est pas équilatéral", 1), ("un triangle dont les trois côtés sont différents", 0), ("un triangle rectangle isocèle", 1)]
    name, axes = rng.choice(kinds)
    questions.append(number("a1", "axes", f"Combien d'axes de symétrie a {name} ?", Fraction(axes), 1, ["Pense au pli."], [f"{axes} axe(s)."]))
    # 2. half of the base
    base = 2 * rng.randint(3, 25)
    questions.append(number("a2", "axes", f"ABC est isocèle en A, H est le milieu de [BC] et BC = {base} cm. Quelle est la longueur BH, en cm ?", Fraction(base // 2), 1, ["H est le milieu."], [f"{base} ÷ 2 = {base // 2} cm."], units=["cm"]))
    # 3. half of the top angle
    top = 2 * rng.randint(10, 80)
    questions.append(number("a3", "axes", f"ABC est isocèle en A avec A = {top}°. L'axe (AH) est la bissectrice de A. Quelle est la mesure de BAH, en degrés ?", Fraction(top // 2), 2, ["La moitié."], [f"{top} ÷ 2 = {top // 2}°."], units=DEG))
    # 4. the top angle
    b = rng.randint(30, 80)
    questions.append(number("a4", "isocele", f"ABC est isocèle en A avec B = {b}°. Quelle est la mesure de A, en degrés ?", Fraction(180 - 2 * b), 1, ["C = B."], [f"180 − {2 * b} = {180 - 2 * b}°."], units=DEG))
    # 5. a base angle
    top = 2 * rng.randint(10, 80)
    questions.append(number("a5", "isocele", f"ABC est isocèle en A avec A = {top}°. Quelle est la mesure de B, en degrés ?", Fraction(180 - top, 2), 2, ["(180 − A) ÷ 2."], [f"{180 - top} ÷ 2 = {(180 - top) // 2}°."], units=DEG))
    # 6. a side of an isosceles triangle
    side = rng.randint(5, 20)
    base = rng.randint(3, 2 * side - 1)
    questions.append(number("a6", "isocele", f"ABC est isocèle en A, de périmètre {2 * side + base} cm, avec BC = {base} cm. Quelle est la longueur de AB, en cm ?", Fraction(side), 2, ["(périmètre − base) ÷ 2."], [f"{2 * side + base} − {base} = {2 * side}.", f"{2 * side} ÷ 2 = {side} cm."], units=["cm"]))
    # 7. an equilateral triangle
    side = rng.randint(3, 25)
    questions.append(number("a7", "equilateral", f"Un triangle équilatéral a un périmètre de {3 * side} cm. Quelle est la longueur d'un côté, en cm ?", Fraction(side), 1, ["Divise par 3."], [f"{3 * side} ÷ 3 = {side} cm."], units=["cm"]))
    # 8. rectangle, isosceles or neither
    a = rng.choice([n for n in range(15, 76) if n not in (45, 60)])
    pairs = [("rectangle", a, 90 - a), ("isocèle", a, a)]
    kind, x, y = rng.choice(pairs)
    options = ["rectangle", "isocèle", "équilatéral"]
    questions.append(choice("a8", "equilateral", f"Un triangle a des angles de {x}° et de {y}°. Que peut-on dire ?", options, 0 if kind == "rectangle" else 1, 2, ["Compare ou additionne les deux angles."],
                            [f"{x} + {y} = {x + y}." if kind == "rectangle" else f"Deux angles égaux : isocèle."]))
    # 9. the area of a right isosceles triangle
    side = 2 * rng.randint(2, 15)
    questions.append(number("a9", "equilateral", f"Un triangle rectangle isocèle a des côtés égaux de {side} cm. Quelle est son aire, en cm² ?", Fraction(side * side, 2), 2, ["Base × hauteur ÷ 2."], [f"{side} × {side} ÷ 2 = {side * side // 2} cm²."], units=["cm2", "cm²"]))
    # 10. the bisector of A
    a_angle = 2 * rng.randint(20, 80)
    questions.append(number("a10", "bissectrice", f"[AD) est la bissectrice de l'angle A = {a_angle}° du triangle ABC. Quelle est la mesure de BAD, en degrés ?", Fraction(a_angle // 2), 1, ["La moitié."], [f"{a_angle} ÷ 2 = {a_angle // 2}°."], units=DEG))
    # 11. the bisector with two angles known
    b, c = rng.randint(20, 80), rng.randint(20, 80)
    while (180 - b - c) % 2 or b + c >= 150:
        b, c = rng.randint(20, 80), rng.randint(20, 80)
    questions.append(number("a11", "bissectrice", f"Dans le triangle ABC, B = {b}° et C = {c}°. [AD) est la bissectrice de A. Quelle est la mesure de BAD, en degrés ?", Fraction(180 - b - c, 2), 3, ["A = 180 − (B + C), puis la moitié."],
                            [f"A = 180 − {b + c} = {180 - b - c}°.", f"BAD = {(180 - b - c) // 2}°."], units=DEG))
    # 12. the third angle of a small triangle
    bad, b = rng.randint(10, 50), rng.randint(30, 100)
    questions.append(number("a12", "bissectrice", f"Dans le triangle ABD, BAD = {bad}° et B = {b}°. Quelle est la mesure de ADB, en degrés ?", Fraction(180 - bad - b), 2, ["180 − somme."], [f"{bad} + {b} = {bad + b}.", f"180 − {bad + b} = {180 - bad - b}°."], units=DEG))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=8, title="Triangles particuliers et bissectrice", language="fr",
    intro="Plie un triangle en deux : parfois les moitiés se recouvrent. Les triangles isocèles et équilatéraux ont cette particularité, qui donne des égalités de côtés et d'angles. "
          "Ce chapitre t'apprend leurs axes de symétrie, à reconnaître un triangle particulier, et la bissectrice d'un angle.",
    objectives=["Connaître les axes de symétrie des triangles particuliers.",
                "Montrer qu'un triangle est isocèle, équilatéral ou rectangle avec des angles ou des longueurs.",
                "Calculer des angles et des longueurs dans un triangle particulier.",
                "Connaître la bissectrice d'un angle et calculer avec elle."],
    prerequisites=[{"text": "Connaître la somme des angles d'un triangle.", "chapter": "sn-5e-angles"},
                   {"text": "Connaître la médiatrice d'un segment.", "chapter": "sn-5e-segments"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Eighth chapter of the Senegal Cinquième course. Its contents follow the triangles lesson of the Côte d'Ivoire Cinquième programme (axes of symmetry and characteristics of the special triangles, how to show that a triangle is isosceles, equilateral or right, the bisector), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. Constructions with a ruler and a compass cannot be done on a screen, so they are described and not covered. "
                "It has not been checked against the official Senegalese programme.",
)
