"""Sixième, Triangles: the thirteenth chapter of the Senegal Sixième course, written in French.

The contents follow lesson 5 "Triangles" of the Côte d'Ivoire Sixième programme (the kinds of triangle, heights, medians, perimeter and area), which was read for this chapter.
Every explanation, example, figure and exercise was written independently, with our own numbers. The figures are drawn from constants by figures.py. Building a triangle with a
ruler and a compass cannot be done on a screen: it is described, and said to be done on paper. The sum of the angles of a triangle is not taught here, it is not part of the lesson.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .figures import Figure, figure
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-6e-triangles"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")

# ----- Figures -----
ANY = Figure().point("A", 60, 150, -8, 22).point("B", 280, 160, 8, 22).point("C", 170, 40, 8, -6).segment("A", "B").segment("B", "C").segment("C", "A")
ISOSCELES = (Figure().point("A", 170, 40, 8, -6).point("B", 90, 160, -14, 22).point("C", 250, 160, 6, 22).segment("A", "B").segment("B", "C").segment("C", "A")
             .tick("A", "B", 1).tick("A", "C", 1))
EQUILATERAL = (Figure().point("A", 170, 35, 8, -6).point("B", 95, 165, -14, 22).point("C", 245, 165, 6, 22).segment("A", "B").segment("B", "C").segment("C", "A")
               .tick("A", "B", 2).tick("B", "C", 2).tick("C", "A", 2))
RIGHT = (Figure().point("A", 70, 160, -14, 22).point("B", 70, 40, 8, -4).point("C", 270, 160, 6, 22).segment("A", "B").segment("B", "C").segment("C", "A")
         .right_angle("A", "B", "C", 16))
HEIGHT = (Figure().point("A", 50, 160, -14, 22).point("B", 290, 160, 6, 22).point("C", 200, 40, 8, -6).point("H", 200, 160, 6, 22)
          .segment("A", "B").segment("B", "C").segment("C", "A").segment("C", "H", "fig-dash").right_angle("H", "B", "C", 12))
MEDIAN = (Figure().point("A", 60, 160, -14, 22).point("B", 280, 160, 6, 22).point("C", 150, 35, 8, -6).point("M", 170, 160, -4, 22)
          .segment("A", "B").segment("B", "C").segment("C", "A").segment("C", "M", "fig-dash").tick("A", "M", 1).tick("M", "B", 1))

# ----- Section 1: kinds of triangle -----
S1 = Section(
    "natures", "Reconnaître un triangle : isocèle, équilatéral et rectangle", 22, "natures",
    "Nommer les éléments d'un triangle et reconnaître un triangle isocèle, équilatéral ou rectangle à partir des longueurs de ses côtés ou d'un angle droit.",
    [
        para("Les motifs d'une nappe, la forme d'un toit, un panneau de signalisation : les triangles sont partout. Un triangle est la figure la plus simple qui entoure une surface, "
             "et on en distingue plusieurs sortes selon la longueur des côtés ou la présence d'un angle droit."),
        definition("Triangle",
                   "Un triangle est formé de trois points non alignés, ses sommets, et des trois segments qui les relient, ses côtés. Le triangle de sommets A, B et C se note " + N("ABC") + ". "
                   "Ses côtés sont [AB], [BC] et [CA]."),
        figure(ANY, "Un triangle ABC dont les trois côtés ont des longueurs différentes.", "Un triangle quelconque : trois sommets A, B et C, trois côtés [AB], [BC] et [CA]."),
        definition("Triangle isocèle et triangle équilatéral",
                   "Un triangle isocèle a deux côtés de même longueur. Un triangle équilatéral a ses trois côtés de même longueur : c'est un cas particulier de triangle isocèle. "
                   "Sur un dessin, on marque les côtés de même longueur avec le même nombre de petits traits."),
        figure(ISOSCELES, "Un triangle ABC dont les côtés [AB] et [AC] portent le même trait.", "Le triangle ABC est isocèle en A : AB = AC. Le sommet A, où se rejoignent les deux côtés égaux, est le sommet principal."),
        figure(EQUILATERAL, "Un triangle dont les trois côtés portent deux traits.", "Le triangle est équilatéral : AB = BC = CA."),
        definition("Triangle rectangle",
                   "Un triangle rectangle a un angle droit. Le côté opposé à l'angle droit, qui est le plus long des trois, s'appelle l'hypoténuse."),
        figure(RIGHT, "Un triangle ABC avec un petit carré à l'angle A.", "Le triangle ABC est rectangle en A. L'hypoténuse est le côté [BC], le plus long des trois."),
        example("Exemple 1", "Un triangle a pour côtés 5 cm, 5 cm et 8 cm. Quelle est sa nature ?",
                "On compare les longueurs des côtés.",
                [("Deux côtés mesurent 5 cm", "Ils sont de même longueur."),
                 ("Le troisième côté mesure 8 cm, différent", "Les trois côtés ne sont pas tous égaux.")],
                "Le triangle est isocèle (et pas équilatéral).", "5==5 and 5!=8"),
        example("Exemple 2", "Un triangle a pour côtés 6 cm, 6 cm et 6 cm. Quelle est sa nature ?",
                "On compare les longueurs des trois côtés.",
                [("Les trois côtés mesurent 6 cm", "Ils sont tous de même longueur."),
                 ("Un triangle équilatéral est aussi isocèle", "Il a bien deux côtés égaux.")],
                "Le triangle est équilatéral.", "6==6==6"),
        example("Exemple 3", "Un triangle isocèle a deux côtés de 7 cm et un périmètre de 20 cm. Quelle est la longueur du troisième côté ?",
                "Le périmètre est la somme des trois côtés : on retire les deux côtés connus.",
                [(N("7 + 7") + " = " + N("14"), "Les deux côtés égaux font 14 cm ensemble."),
                 (N("20 - 14") + " = " + N("6"), "Il reste 6 cm pour le troisième côté.")],
                "Le troisième côté mesure " + N("6") + " cm.", "20-7-7==6"),
        example("Exemple 4", "Un triangle équilatéral a un périmètre de 27 cm. Quelle est la longueur de chaque côté ?",
                "Les trois côtés sont égaux : on partage le périmètre en trois.",
                [(N("27 \\div 3") + " = " + N("9"), "Chaque côté mesure un tiers du périmètre.")],
                "Chaque côté mesure " + N("9") + " cm.", "27/3==9 and 9*3==27"),
        warning("Un triangle équilatéral est aussi isocèle, mais un triangle isocèle n'est pas toujours équilatéral. Et un dessin ne suffit pas : pour dire que deux côtés sont égaux, il faut une donnée, un trait de codage ou une mesure."),
    ],
    [
        choice("s1-g1", "natures", "Un triangle a pour côtés 4 cm, 4 cm et 6 cm. Quelle est sa nature ?", ["Isocèle non équilatéral", "Équilatéral", "Quelconque"], 0,
               hints=["Compare les trois longueurs."], solution=["Deux côtés sont égaux (4 et 4), le troisième est différent (6) : isocèle, mais pas équilatéral."],
               wrong={1: "Il faudrait trois côtés égaux.", 2: "Il a deux côtés égaux : il est isocèle."}),
        choice("s1-g2", "natures", "Un triangle a pour côtés 5 cm, 5 cm et 5 cm. Quelle est sa nature ?", ["Isocèle non équilatéral", "Équilatéral", "Quelconque"], 1,
               hints=["Les trois côtés ont la même longueur."], solution=["Trois côtés égaux : le triangle est équilatéral."],
               wrong={0: "Un triangle isocèle non équilatéral a un troisième côté différent.", 2: "Les côtés sont tous égaux."}),
        number("s1-g3", "natures", "Un triangle isocèle a deux côtés de 9 cm et un périmètre de 25 cm. Quelle est la longueur du troisième côté, en cm ?", Fraction(7), units=["cm"],
               hints=["Retire les deux côtés égaux du périmètre."], solution=["9 + 9 = 18.", "25 − 18 = 7 cm."]),
        number("s1-g4", "natures", "Un triangle équilatéral a un périmètre de 36 cm. Quelle est la longueur d'un côté, en cm ?", Fraction(12), units=["cm"],
               hints=["Divise le périmètre par 3."], solution=["36 ÷ 3 = 12 cm."]),
        choice("s1-g5", "natures", "Comment s'appelle le côté opposé à l'angle droit d'un triangle rectangle ?", ["La base", "L'hypoténuse", "La médiane"], 1,
               hints=["C'est le plus long côté."], solution=["Le côté opposé à l'angle droit est l'hypoténuse."], wrong={0: "La base n'est pas un côté particulier du triangle rectangle.", 2: "Une médiane est un segment qui joint un sommet au milieu du côté opposé."}),
    ])

# ----- Section 2: perimeter -----
S2 = Section(
    "perimetre", "Le périmètre d'un triangle", 22, "perimetre",
    "Calculer le périmètre d'un triangle quelconque, isocèle ou équilatéral, et retrouver un côté à partir du périmètre.",
    [
        para("Pour entourer un terrain triangulaire d'une clôture, il faut connaître la longueur de son contour. Cette longueur est le périmètre du triangle."),
        rule("Périmètre d'un triangle",
             "Le périmètre d'un triangle est la somme des longueurs de ses trois côtés : " + N("P = AB + BC + CA") + ". Pour un triangle isocèle dont les côtés égaux mesurent a et la base b, " + N("P = 2 \\times a + b") + ". "
             "Pour un triangle équilatéral de côté a, " + N("P = 3 \\times a") + ". Le périmètre se mesure dans la même unité que les côtés."),
        example("Exemple 1", "Un triangle a pour côtés 4,5 cm, 6 cm et 7,5 cm. Calculer son périmètre.",
                "On additionne les trois longueurs, dans la même unité.",
                [(N("4,5 + 6 + 7,5"), "Somme des trois côtés."),
                 (N("4,5 + 7,5") + " = " + N("12"), "On regroupe 4,5 et 7,5."),
                 (N("12 + 6") + " = " + N("18"), "On ajoute le troisième côté.")],
                "Le périmètre est " + N("18") + " cm.", "d('4,5')+6+d('7,5')==18"),
        example("Exemple 2", "Un triangle isocèle a deux côtés de 8 cm et une base de 5 cm. Calculer son périmètre.",
                "Les deux côtés égaux comptent deux fois.",
                [(N("P = 2 \\times 8 + 5"), "Formule du périmètre d'un triangle isocèle."),
                 (N("16 + 5") + " = " + N("21"), "2 × 8 = 16, puis 16 + 5 = 21.")],
                "Le périmètre est " + N("21") + " cm.", "2*8+5==8+8+5==21"),
        example("Exemple 3", "Un terrain triangulaire a pour côtés 30 m, 40 m et 50 m. On l'entoure d'un grillage à 1 500 F le mètre. Quel est le prix du grillage ?",
                "On calcule d'abord le périmètre, puis le prix.",
                [(N("30 + 40 + 50") + " = " + N("120"), "Le périmètre est 120 m."),
                 (N("120 \\times 1500") + " = " + N("180000"), "12 × 15 = 180, puis on ajoute 3 zéros : 180 000.")],
                "Le grillage coûte " + N("180000") + " F.", "30+40+50==120 and 120*1500==180000"),
        example("Exemple 4", "Un triangle a un périmètre de 24 cm. Deux de ses côtés mesurent 7 cm et 9 cm. Quelle est la longueur du troisième côté ?",
                "On retire les deux côtés connus du périmètre.",
                [(N("7 + 9") + " = " + N("16"), "Les deux côtés connus."),
                 (N("24 - 16") + " = " + N("8"), "Il reste 8 cm pour le troisième côté.")],
                "Le troisième côté mesure " + N("8") + " cm.", "24-7-9==8"),
        warning("Pour calculer un périmètre, toutes les longueurs doivent être dans la même unité : 3 m, 40 cm et 2 m ne s'additionnent pas tels quels. Convertis d'abord, par exemple 40 cm = 0,4 m. "
                "Et le périmètre se mesure en cm ou en m, pas en cm²."),
    ],
    [
        number("s2-g1", "perimetre", "Un triangle a pour côtés 3 cm, 4 cm et 5 cm. Quel est son périmètre, en cm ?", Fraction(12), units=["cm"],
               hints=["Additionne les trois côtés."], solution=["3 + 4 + 5 = 12 cm."]),
        number("s2-g2", "perimetre", "Un triangle isocèle a deux côtés de 6,5 cm et une base de 4 cm. Quel est son périmètre, en cm ?", Fraction(17), units=["cm"],
               hints=["Les deux côtés égaux comptent deux fois."], solution=["2 × 6,5 = 13.", "13 + 4 = 17 cm."]),
        number("s2-g3", "perimetre", "Un triangle équilatéral a un côté de 8,5 cm. Quel est son périmètre, en cm ?", d("25,5"), units=["cm"],
               hints=["Trois côtés égaux."], solution=["3 × 8,5 = 25,5 cm."]),
        number("s2-g4", "perimetre", "Un triangle a un périmètre de 30 cm. Deux côtés mesurent 11 cm et 8 cm. Quelle est la longueur du troisième côté, en cm ?", Fraction(11), units=["cm"],
               hints=["Retire les deux côtés connus de 30."], solution=["11 + 8 = 19.", "30 − 19 = 11 cm."]),
        number("s2-g5", "perimetre", "Un champ triangulaire a pour côtés 20 m, 35 m et 45 m. On le clôture avec un fil qui coûte 200 F le mètre. Quel est le prix, en F ?", Fraction(20000), units=["F"],
               hints=["Périmètre d'abord, puis prix."], solution=["20 + 35 + 45 = 100 m.", "100 × 200 = 20 000 F."]),
    ])

# ----- Section 3: area -----
S3 = Section(
    "aire", "L'aire d'un triangle", 24, "aire",
    "Connaître la hauteur d'un triangle, calculer l'aire d'un triangle à partir d'un côté et de la hauteur correspondante, et retrouver une hauteur ou une base.",
    [
        para("Pour peindre un pignon de toit triangulaire ou acheter de l'étoffe pour un fanion, on doit connaître l'aire du triangle. Elle se déduit de celle du rectangle : "
             "un triangle est la moitié d'un rectangle de même base et de même hauteur."),
        definition("Hauteur d'un triangle",
                   "Une hauteur d'un triangle est un segment qui part d'un sommet et qui est perpendiculaire à la droite qui porte le côté opposé. Ce côté s'appelle la base correspondante. "
                   "La longueur de la hauteur est la distance du sommet à la base."),
        figure(HEIGHT, "Un triangle ABC dont la hauteur [CH] est tracée en pointillés, perpendiculaire à la base [AB].", "[CH] est la hauteur issue de C : elle est perpendiculaire à [AB] et part du sommet C. [AB] est la base correspondante."),
        rule("Aire d'un triangle",
             "L'aire d'un triangle est égale à la base multipliée par la hauteur correspondante, divisée par 2 : " + N("A = \\dfrac{b \\times h}{2}") + ". "
             "Pour un triangle rectangle, les deux côtés de l'angle droit sont une base et sa hauteur : " + N("A = \\dfrac{a \\times b}{2}") + ". L'aire se mesure en unités carrées."),
        example("Exemple 1", "Un triangle a une base de 8 cm et une hauteur correspondante de 5 cm. Calculer son aire.",
                "On utilise la formule A = b × h ÷ 2.",
                [(N("8 \\times 5") + " = " + N("40"), "Le produit de la base par la hauteur."),
                 (N("40 \\div 2") + " = " + N("20"), "On divise par 2 : le triangle est la moitié du rectangle.")],
                "L'aire est " + N("20") + " cm².", "8*5/2==20"),
        example("Exemple 2", "Un triangle rectangle a pour côtés de l'angle droit 6 cm et 8 cm. Calculer son aire.",
                "Les deux côtés de l'angle droit sont l'un la base, l'autre la hauteur.",
                [(N("6 \\times 8") + " = " + N("48"), "Produit des deux côtés de l'angle droit."),
                 (N("48 \\div 2") + " = " + N("24"), "On divise par 2.")],
                "L'aire est " + N("24") + " cm².", "6*8/2==24"),
        example("Exemple 3", "Un triangle a une aire de 30 cm² et une base de 10 cm. Quelle est la hauteur correspondante ?",
                "On a A = b × h ÷ 2, donc b × h = 2 × A : on cherche le facteur manquant.",
                [(N("2 \\times 30") + " = " + N("60"), "Le produit base × hauteur est le double de l'aire."),
                 (N("60 \\div 10") + " = " + N("6"), "La hauteur est 60 ÷ 10.")],
                "La hauteur mesure " + N("6") + " cm.", "2*30==60 and 60/10==6 and 10*6/2==30"),
        example("Exemple 4", "Un pignon triangulaire a une base de 7,5 m et une hauteur de 4 m. On le peint avec une peinture qui couvre 5 m² par litre. Combien de litres faut-il ?",
                "On calcule l'aire, puis on divise par la surface couverte par un litre.",
                [(N("7,5 \\times 4") + " = " + N("30"), "Produit de la base par la hauteur."),
                 (N("30 \\div 2") + " = " + N("15"), "L'aire est 15 m²."),
                 (N("15 \\div 5") + " = " + N("3"), "Il faut 3 litres.")],
                "Il faut " + N("3") + " litres.", "d('7,5')*4/2==15 and 15/5==3"),
        warning("La hauteur n'est pas forcément un côté du triangle : c'est la distance perpendiculaire entre le sommet et la base. Dans un triangle rectangle, un côté de l'angle droit est une hauteur, mais pas l'hypoténuse. "
                "Et n'oublie pas de diviser par 2 : sans cela, on calcule l'aire du rectangle, qui est le double."),
    ],
    [
        number("s3-g1", "aire", "Un triangle a une base de 10 cm et une hauteur de 6 cm. Quelle est son aire, en cm² ?", Fraction(30), units=["cm2", "cm²"],
               hints=["A = b × h ÷ 2."], solution=["10 × 6 = 60.", "60 ÷ 2 = 30 cm²."]),
        number("s3-g2", "aire", "Un triangle rectangle a pour côtés de l'angle droit 5 cm et 12 cm. Quelle est son aire, en cm² ?", Fraction(30), units=["cm2", "cm²"],
               hints=["Les côtés de l'angle droit sont une base et sa hauteur."], solution=["5 × 12 = 60.", "60 ÷ 2 = 30 cm²."]),
        number("s3-g3", "aire", "Un triangle a une aire de 24 cm² et une base de 8 cm. Quelle est la hauteur correspondante, en cm ?", Fraction(6), units=["cm"],
               hints=["b × h = 2 × aire."], solution=["2 × 24 = 48.", "48 ÷ 8 = 6 cm."]),
        number("s3-g4", "aire", "Un triangle a une base de 9 cm et une hauteur de 4 cm. Quelle est son aire, en cm² ?", Fraction(18), units=["cm2", "cm²"],
               hints=["9 × 4 = 36 puis divise par 2."], solution=["9 × 4 = 36.", "36 ÷ 2 = 18 cm²."]),
        choice("s3-g5", "aire", "Un rectangle de base 10 cm et de hauteur 6 cm a une aire de 60 cm². Quelle est l'aire d'un triangle de même base et de même hauteur ?", ["60 cm²", "30 cm²", "120 cm²"], 1,
               hints=["Le triangle est la moitié du rectangle."], solution=["Le triangle est la moitié du rectangle : 60 ÷ 2 = 30 cm²."], wrong={0: "60 cm² est l'aire du rectangle, pas du triangle.", 2: "120 cm² serait le double du rectangle."}),
    ])

# ----- Section 4: remarkable lines -----
S4 = Section(
    "droites", "Hauteur, médiane et médiatrice dans un triangle", 22, "droites",
    "Reconnaître une médiane, une hauteur et la médiatrice d'un côté, et calculer avec une médiane.",
    [
        para("Dans un triangle, certaines droites jouent un rôle particulier. Une médiane relie un sommet au milieu du côté opposé, une hauteur tombe à angle droit sur la base, "
             "et la médiatrice d'un côté passe par le milieu de ce côté à angle droit."),
        definition("Médiane",
                   "Une médiane d'un triangle est un segment qui joint un sommet au milieu du côté opposé. Un triangle a trois médianes, une par sommet."),
        figure(MEDIAN, "Un triangle ABC avec le milieu M du côté [AB] et le segment [CM] en pointillés, avec des traits égaux sur [AM] et [MB].", "[CM] est la médiane issue de C : M est le milieu de [AB], donc AM = MB."),
        definition("Médiatrice d'un côté",
                   "La médiatrice d'un côté du triangle est la droite perpendiculaire à ce côté qui passe par son milieu. Elle ne passe pas forcément par le sommet opposé."),
        rule("Les droites du triangle",
             "Une hauteur est perpendiculaire à la base. Une médiane passe par le milieu du côté. La médiatrice est perpendiculaire au côté ET passe par son milieu. "
             "Une médiane partage le triangle en deux triangles de même aire, parce que les deux triangles ont des bases égales et la même hauteur."),
        example("Exemple 1", "[AM] est une médiane du triangle ABC (M est sur [BC]) et BC = 12 cm. Calculer BM.",
                "M est le milieu de [BC] : BM est la moitié de BC.",
                [(N("BM = BC \\div 2"), "Propriété du milieu."),
                 (N("12 \\div 2") + " = " + N("6"), "La moitié de 12 est 6.")],
                N("BM = 6") + " cm.", "12//2==6"),
        example("Exemple 2", "Un triangle ABC a une aire de 30 cm². M est le milieu de [BC]. Quelle est l'aire du triangle ABM ?",
                "Une médiane partage le triangle en deux triangles de même aire.",
                [("Les triangles ABM et ACM ont des bases BM et MC égales, et la même hauteur issue de A", "Ils ont donc la même aire."),
                 (N("30 \\div 2") + " = " + N("15"), "Chacun a une aire de 15 cm².")],
                "L'aire de ABM est " + N("15") + " cm².", "30/2==15"),
        example("Exemple 3", "Dans un triangle rectangle en A, avec AB = 6 cm et AC = 8 cm, calculer l'aire de ce triangle, puis la hauteur issue de A vers l'hypoténuse [BC], sachant que BC = 10 cm.",
                "On calcule l'aire avec les côtés de l'angle droit, puis on l'utilise avec la base [BC].",
                [(N("A = 6 \\times 8 \\div 2") + " = " + N("24"), "L'aire est 24 cm²."),
                 (N("2 \\times 24") + " = " + N("48"), "Avec la base [BC], b × h = 2 × A."),
                 (N("48 \\div 10") + " = " + N("4,8"), "La hauteur issue de A mesure 4,8 cm.")],
                "L'aire est " + N("24") + " cm² et la hauteur issue de A mesure " + N("4,8") + " cm.", "6*8/2==24 and d('48')/10==d('4,8')"),
        example("Exemple 4", "Les trois médianes d'un triangle ABC sont tracées. Combien y a-t-il de médianes ? Combien de hauteurs ?",
                "Chaque sommet donne une médiane et une hauteur.",
                [("Trois sommets", "Il y a une médiane par sommet : 3 médianes."),
                 ("Une hauteur par sommet aussi", "Il y a 3 hauteurs.")],
                N("3") + " médianes et " + N("3") + " hauteurs.", "3*1==3"),
        warning("Ne confonds pas médiane et hauteur : la médiane passe par le milieu du côté, mais n'est pas forcément perpendiculaire à ce côté ; la hauteur est perpendiculaire à la base, mais ne tombe pas forcément au milieu. "
                "Dans un triangle isocèle, la droite issue du sommet principal est les deux à la fois."),
    ],
    [
        number("s4-g1", "droites", "[AM] est une médiane du triangle ABC, M étant sur [BC]. BC = 18 cm. Quelle est la longueur BM, en cm ?", Fraction(9), units=["cm"],
               hints=["M est le milieu de [BC]."], solution=["BM = 18 ÷ 2 = 9 cm."]),
        number("s4-g2", "droites", "Un triangle ABC a une aire de 48 cm². M est le milieu de [BC]. Quelle est l'aire du triangle ABM, en cm² ?", Fraction(24), units=["cm2", "cm²"],
               hints=["Une médiane partage le triangle en deux triangles de même aire."], solution=["48 ÷ 2 = 24 cm²."]),
        choice("s4-g3", "droites", "Quel segment joint un sommet au milieu du côté opposé ?", ["La hauteur", "La médiane", "La base"], 1,
               hints=["Pense au mot milieu."], solution=["La médiane joint un sommet au milieu du côté opposé."], wrong={0: "La hauteur est perpendiculaire à la base.", 2: "La base est un côté, pas un segment intérieur."}),
        choice("s4-g4", "droites", "Quelle est la médiatrice d'un côté d'un triangle ?", ["Le segment qui joint un sommet au milieu du côté opposé", "La droite perpendiculaire à ce côté qui passe par son milieu", "Le segment perpendiculaire issu du sommet opposé"], 1,
               hints=["Elle fait deux choses : perpendiculaire et par le milieu."], solution=["La médiatrice est la droite perpendiculaire au côté qui passe par son milieu."],
               wrong={0: "C'est la définition de la médiane.", 2: "C'est la définition de la hauteur."}),
        number("s4-g5", "droites", "Un triangle rectangle a pour côtés de l'angle droit 9 cm et 12 cm. Quelle est son aire, en cm² ?", Fraction(54), units=["cm2", "cm²"],
               hints=["Les côtés de l'angle droit sont base et hauteur."], solution=["9 × 12 = 108.", "108 ÷ 2 = 54 cm²."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    choice("p1", "natures", "Un triangle a pour côtés 7 cm, 7 cm et 7 cm. Quelle est sa nature ?", ["Quelconque", "Isocèle non équilatéral", "Équilatéral"], 2, 1, ["Compare les trois côtés."], ["Trois côtés égaux : équilatéral."], wrong={0: "Les côtés sont égaux.", 1: "Le troisième côté n'est pas différent."}),
    choice("p2", "natures", "Un triangle a pour côtés 3 cm, 4 cm et 5 cm. Quelle est sa nature d'après les côtés ?", ["Quelconque", "Isocèle", "Équilatéral"], 0, 1, ["Compare les trois longueurs."], ["Les trois côtés sont différents : il est quelconque."], wrong={1: "Il faudrait deux côtés égaux.", 2: "Il faudrait trois côtés égaux."}),
    choice("p3", "natures", "Un triangle a pour côtés 6 cm, 9 cm et 6 cm. Quelle est sa nature ?", ["Quelconque", "Isocèle non équilatéral", "Équilatéral"], 1, 1, ["Deux côtés sont-ils égaux ?"], ["Deux côtés mesurent 6 cm, le troisième 9 cm : isocèle."], wrong={0: "Deux côtés sont égaux.", 2: "Le troisième côté est différent."}),
    choice("p4", "natures", "Quel triangle est à la fois isocèle et équilatéral ?", ["Un triangle de côtés 5, 5 et 8", "Un triangle de côtés 6, 6 et 6", "Un triangle de côtés 3, 4 et 5"], 1, 2, ["Un triangle équilatéral est un cas particulier d'isocèle."], ["Le triangle de côtés 6, 6 et 6 a trois côtés égaux : il est équilatéral, donc aussi isocèle."], wrong={0: "5, 5 et 8 est isocèle seulement.", 2: "3, 4 et 5 est quelconque."}),
    number("p5", "natures", "Un triangle isocèle a deux côtés de 12 cm et un périmètre de 40 cm. Quelle est la longueur du troisième côté, en cm ?", Fraction(16), 2, ["Périmètre moins les deux côtés égaux."], ["12 + 12 = 24.", "40 − 24 = 16 cm."], units=["cm"]),
    number("p6", "natures", "Un triangle équilatéral a un périmètre de 51 cm. Quelle est la longueur d'un côté, en cm ?", Fraction(17), 1, ["Divise par 3."], ["51 ÷ 3 = 17 cm."], units=["cm"]),
    number("p7", "natures", "Un triangle isocèle a un côté égal de 10 cm et un périmètre de 32 cm. Quelle est la longueur de la base, en cm ?", Fraction(12), 3, ["Les deux côtés égaux mesurent 10 cm."], ["2 × 10 = 20.", "32 − 20 = 12 cm."], units=["cm"]),
    choice("p8", "natures", "Léa dit : « mon triangle a deux côtés égaux, donc il est équilatéral ». Qu'en penses-tu ?", ["Elle a raison", "Elle a tort : il est isocèle, mais équilatéral demande trois côtés égaux", "Elle a tort : il est rectangle"], 1, 2, ["Compte les côtés égaux."], ["Deux côtés égaux donnent un triangle isocèle. Équilatéral demande que les trois côtés soient égaux."], wrong={0: "Il manque un côté égal.", 2: "Rien n'indique un angle droit."}),
    number("p9", "perimetre", "Un triangle a pour côtés 7 cm, 8 cm et 9 cm. Quel est son périmètre, en cm ?", Fraction(24), 1, ["Additionne les côtés."], ["7 + 8 + 9 = 24 cm."], units=["cm"]),
    number("p10", "perimetre", "Un triangle a pour côtés 2,4 cm, 3,6 cm et 4,5 cm. Quel est son périmètre, en cm ?", d("10,5"), 2, ["Additionne les côtés."], ["2,4 + 3,6 = 6.", "6 + 4,5 = 10,5 cm."], units=["cm"]),
    number("p11", "perimetre", "Un triangle isocèle a deux côtés de 9 cm et une base de 6 cm. Quel est son périmètre, en cm ?", Fraction(24), 1, ["2 × 9 + 6."], ["2 × 9 = 18.", "18 + 6 = 24 cm."], units=["cm"]),
    number("p12", "perimetre", "Un triangle équilatéral a un côté de 12,5 cm. Quel est son périmètre, en cm ?", d("37,5"), 2, ["3 × 12,5."], ["3 × 12,5 = 37,5 cm."], units=["cm"]),
    number("p13", "perimetre", "Un triangle a un périmètre de 45 cm. Deux côtés mesurent 14 cm et 17 cm. Quelle est la longueur du troisième côté, en cm ?", Fraction(14), 2, ["Retire les deux côtés connus."], ["14 + 17 = 31.", "45 − 31 = 14 cm."], units=["cm"]),
    number("p14", "perimetre", "Un terrain triangulaire a pour côtés 60 m, 80 m et 100 m. Quelle est la longueur de la clôture pour en faire le tour, en m ?", Fraction(240), 1, ["Périmètre du triangle."], ["60 + 80 + 100 = 240 m."], units=["m"]),
    number("p15", "perimetre", "Un triangle a pour côtés 1,2 m, 80 cm et 1 m. Quel est son périmètre, en m ?", d("3"), 3, ["Convertis 80 cm en mètres."], ["80 cm = 0,8 m.", "1,2 + 0,8 + 1 = 3 m."], units=["m"]),
    number("p16", "perimetre", "Un triangle équilatéral a un périmètre de 4,5 m. Quelle est la longueur d'un côté, en m ?", d("1,5"), 2, ["Divise par 3."], ["4,5 ÷ 3 = 1,5 m."], units=["m"]),
    number("p17", "perimetre", "On entoure un champ triangulaire de côtés 25 m, 30 m et 45 m avec un grillage à 800 F le mètre. Quel est le prix, en F ?", Fraction(80000), 2, ["Périmètre, puis prix."], ["25 + 30 + 45 = 100 m.", "100 × 800 = 80 000 F."], units=["F"]),
    number("p18", "aire", "Un triangle a une base de 12 cm et une hauteur de 7 cm. Quelle est son aire, en cm² ?", Fraction(42), 1, ["b × h ÷ 2."], ["12 × 7 = 84.", "84 ÷ 2 = 42 cm²."], units=["cm2", "cm²"]),
    number("p19", "aire", "Un triangle a une base de 5 cm et une hauteur de 3,2 cm. Quelle est son aire, en cm² ?", Fraction(8), 2, ["5 × 3,2 ÷ 2."], ["5 × 3,2 = 16.", "16 ÷ 2 = 8 cm²."], units=["cm2", "cm²"]),
    number("p20", "aire", "Un triangle rectangle a pour côtés de l'angle droit 7 cm et 10 cm. Quelle est son aire, en cm² ?", Fraction(35), 1, ["Côtés de l'angle droit : base et hauteur."], ["7 × 10 = 70.", "70 ÷ 2 = 35 cm²."], units=["cm2", "cm²"]),
    number("p21", "aire", "Un triangle a une aire de 36 cm² et une hauteur de 9 cm. Quelle est la base correspondante, en cm ?", Fraction(8), 3, ["b × h = 2 × aire."], ["2 × 36 = 72.", "72 ÷ 9 = 8 cm."], units=["cm"]),
    number("p22", "aire", "Un triangle a une aire de 45 cm² et une base de 15 cm. Quelle est la hauteur correspondante, en cm ?", Fraction(6), 3, ["b × h = 2 × aire."], ["2 × 45 = 90.", "90 ÷ 15 = 6 cm."], units=["cm"]),
    number("p23", "aire", "Un fanion triangulaire a une base de 30 cm et une hauteur de 50 cm. Quelle est son aire, en cm² ?", Fraction(750), 2, ["b × h ÷ 2."], ["30 × 50 = 1 500.", "1 500 ÷ 2 = 750 cm²."], units=["cm2", "cm²"]),
    number("p24", "aire", "Un triangle a une base de 8 m et une hauteur de 5 m. Une peinture couvre 4 m² par litre. Combien de litres faut-il pour le peindre ?", Fraction(5), 3, ["Aire d'abord."], ["8 × 5 ÷ 2 = 20 m².", "20 ÷ 4 = 5 litres."]),
    number("p25", "aire", "Un rectangle a une base de 14 cm et une hauteur de 6 cm. Quelle est l'aire d'un triangle de même base et de même hauteur, en cm² ?", Fraction(42), 2, ["Moitié du rectangle."], ["14 × 6 = 84.", "84 ÷ 2 = 42 cm²."], units=["cm2", "cm²"]),
    choice("p26", "aire", "Karim calcule l'aire d'un triangle de base 10 cm et de hauteur 4 cm : « 10 × 4 = 40 cm² ». Quelle est son erreur ?", ["Il a oublié de diviser par 2", "Il a oublié l'unité", "Il a mélangé base et hauteur"], 0, 2, ["Un triangle est la moitié d'un rectangle."], ["10 × 4 = 40 est l'aire du rectangle. Le triangle a pour aire 40 ÷ 2 = 20 cm²."], wrong={1: "Les cm² sont présents.", 2: "Multiplier la base par la hauteur est correct, c'est la suite qui manque."}),
    number("p27", "droites", "[AM] est une médiane du triangle ABC (M sur [BC]). BM = 7 cm. Quelle est la longueur BC, en cm ?", Fraction(14), 1, ["M est le milieu de [BC]."], ["BC = 2 × BM = 14 cm."], units=["cm"]),
    number("p28", "droites", "Un triangle a une aire de 70 cm². Une médiane le partage en deux triangles. Quelle est l'aire de chacun, en cm² ?", Fraction(35), 2, ["Même aire."], ["70 ÷ 2 = 35 cm²."], units=["cm2", "cm²"]),
    number("p29", "droites", "Combien de hauteurs a un triangle ?", Fraction(3), 1, ["Une par sommet."], ["Un triangle a trois sommets et une hauteur par sommet : 3."]),
    choice("p30", "droites", "Dans un triangle ABC, quel segment est perpendiculaire à la base [AB] et part du sommet C ?", ["La médiane issue de C", "La hauteur issue de C", "La médiatrice de [AB]"], 1, 1, ["Pense à « perpendiculaire à la base »."], ["C'est la hauteur issue de C."], wrong={0: "La médiane passe par le milieu de [AB], sans être forcément perpendiculaire.", 2: "La médiatrice est une droite qui passe par le milieu de [AB]."}),
    number("p31", "droites", "Un triangle rectangle a pour côtés de l'angle droit 9 cm et 12 cm, et pour hypoténuse 15 cm. Quelle est la hauteur issue du sommet de l'angle droit vers l'hypoténuse, en cm ?", d("7,2"), 3, ["Aire avec les côtés de l'angle droit, puis avec l'hypoténuse comme base."], ["Aire : 9 × 12 ÷ 2 = 54 cm².", "54 = 15 × h ÷ 2, donc h = 108 ÷ 15 = 7,2 cm."], units=["cm"]),
    number("p32", "droites", "Les trois médianes d'un triangle sont tracées. Combien de médianes y a-t-il ?", Fraction(3), 1, ["Une par sommet."], ["Trois sommets : 3 médianes."]),
]

SUMMARY = [
    definition("Triangles particuliers", "Un triangle a trois sommets et trois côtés. Isocèle : deux côtés égaux. Équilatéral : trois côtés égaux (aussi isocèle). Rectangle : un angle droit, avec l'hypoténuse opposée à l'angle droit."),
    rule("Périmètre", "P = AB + BC + CA. Isocèle : P = 2 × a + b. Équilatéral : P = 3 × a. Toutes les longueurs dans la même unité."),
    rule("Aire", "A = base × hauteur ÷ 2, la hauteur étant perpendiculaire à la base. Pour un triangle rectangle, A = produit des côtés de l'angle droit ÷ 2. On retrouve une hauteur ou une base avec b × h = 2 × A."),
    rule("Droites du triangle", "Hauteur : perpendiculaire à la base, issue du sommet opposé. Médiane : joint un sommet au milieu du côté opposé, et partage le triangle en deux triangles de même aire. Médiatrice d'un côté : perpendiculaire au côté, par son milieu."),
    para("Les erreurs à éviter : oublier de diviser par 2 pour l'aire ; prendre un côté qui n'est pas la hauteur ; confondre médiane et hauteur ; mélanger des unités dans un périmètre ; dire équilatéral pour deux côtés égaux seulement."),
]

CONCEPTS = {
    "natures": ("Triangle isocèle, équilatéral, rectangle", "natures"),
    "perimetre": ("Périmètre d'un triangle", "perimetre"),
    "aire": ("Aire d'un triangle", "aire"),
    "droites": ("Hauteur, médiane, médiatrice", "droites"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    cm, cm2 = ["cm"], ["cm2", "cm²"]
    # 1. nature from the sides
    kind = rng.choice(["iso", "equi", "any"])
    if kind == "iso":
        a, b = rng.randint(3, 12), rng.randint(3, 12)
        while b == a:
            b = rng.randint(3, 12)
        sides = [a, a, b]
    elif kind == "equi":
        a = rng.randint(3, 12)
        sides = [a, a, a]
    else:
        sides = rng.sample(range(3, 13), 3)
    rng.shuffle(sides)
    right = {"iso": 0, "equi": 1, "any": 2}[kind]
    questions.append(choice("a1", "natures", f"Un triangle a pour côtés {sides[0]} cm, {sides[1]} cm et {sides[2]} cm. Quelle est sa nature ?", ["Isocèle non équilatéral", "Équilatéral", "Quelconque"], right, 1,
                            ["Compare les trois longueurs."], ["Compte les côtés égaux : " + ["deux seulement, isocèle.", "trois, équilatéral.", "aucun, quelconque."][right]]))
    # 2. perimeter with decimals
    x, y, z = rand_decimal(rng, 2, 9, 1), rand_decimal(rng, 2, 9, 1), rand_decimal(rng, 2, 9, 1)
    questions.append(number("a2", "perimetre", f"Un triangle a pour côtés {show(x)} cm, {show(y)} cm et {show(z)} cm. Quel est son périmètre, en cm ?", x + y + z, 1,
                            ["Additionne les trois côtés."], [f"{show(x)} + {show(y)} + {show(z)} = {show(x + y + z)} cm."], units=cm))
    # 3. perimeter of an isosceles triangle
    a, b = rng.randint(4, 14), rng.randint(3, 10)
    questions.append(number("a3", "perimetre", f"Un triangle isocèle a deux côtés de {a} cm et une base de {b} cm. Quel est son périmètre, en cm ?", Fraction(2 * a + b), 1,
                            ["2 × côté égal + base."], [f"2 × {a} = {2 * a}.", f"{2 * a} + {b} = {2 * a + b} cm."], units=cm))
    # 4. equilateral side from the perimeter
    a = rng.randint(4, 20)
    questions.append(number("a4", "natures", f"Un triangle équilatéral a un périmètre de {3 * a} cm. Quelle est la longueur d'un côté, en cm ?", Fraction(a), 1,
                            ["Divise le périmètre par 3."], [f"{3 * a} ÷ 3 = {a} cm."], units=cm))
    # 5. the missing side
    p, s1, s2 = rng.randint(30, 60), rng.randint(8, 14), rng.randint(8, 14)
    questions.append(number("a5", "perimetre", f"Un triangle a un périmètre de {p} cm. Deux côtés mesurent {s1} cm et {s2} cm. Quelle est la longueur du troisième côté, en cm ?", Fraction(p - s1 - s2), 2,
                            ["Retire les deux côtés connus du périmètre."], [f"{s1} + {s2} = {s1 + s2}.", f"{p} − {s1 + s2} = {p - s1 - s2} cm."], units=cm))
    # 6. area from base and height
    base, height = 2 * rng.randint(3, 12), rng.randint(3, 15)
    questions.append(number("a6", "aire", f"Un triangle a une base de {base} cm et une hauteur de {height} cm. Quelle est son aire, en cm² ?", Fraction(base * height, 2), 1,
                            ["A = b × h ÷ 2."], [f"{base} × {height} = {base * height}.", f"{base * height} ÷ 2 = {base * height // 2} cm²."], units=cm2))
    # 7. area of a right triangle
    u, v = rng.randint(3, 14), rng.randint(4, 15)
    while u * v % 2:
        v = rng.randint(4, 15)
    questions.append(number("a7", "aire", f"Un triangle rectangle a pour côtés de l'angle droit {u} cm et {v} cm. Quelle est son aire, en cm² ?", Fraction(u * v, 2), 2,
                            ["Les côtés de l'angle droit sont base et hauteur."], [f"{u} × {v} = {u * v}.", f"{u * v} ÷ 2 = {u * v // 2} cm²."], units=cm2))
    # 8. the height from the area
    base, height = rng.randint(4, 14), rng.randint(3, 12)
    questions.append(number("a8", "aire", f"Un triangle a une aire de {show(Fraction(base * height, 2))} cm² et une base de {base} cm. Quelle est la hauteur correspondante, en cm ?", Fraction(height), 3,
                            ["b × h = 2 × aire."], [f"2 × aire = {base * height}.", f"{base * height} ÷ {base} = {height} cm."], units=cm))
    # 9. a median halves a side
    half = rng.randint(3, 20)
    questions.append(number("a9", "droites", f"[AM] est une médiane du triangle ABC, avec M sur [BC]. BC = {2 * half} cm. Quelle est la longueur BM, en cm ?", Fraction(half), 1,
                            ["M est le milieu de [BC]."], [f"{2 * half} ÷ 2 = {half} cm."], units=cm))
    # 10. the cost of a fence
    s = rng.sample(range(10, 41), 3)
    price = rng.choice([100, 200, 250, 500])
    questions.append(number("a10", "perimetre", f"Un champ triangulaire a pour côtés {s[0]} m, {s[1]} m et {s[2]} m. On le clôture avec un grillage à {price} F le mètre. Quel est le prix, en F ?", Fraction(sum(s) * price), 3,
                            ["Périmètre d'abord, puis prix."], [f"{s[0]} + {s[1]} + {s[2]} = {sum(s)} m.", f"{sum(s)} × {price} = {sum(s) * price} F."], units=["F"]))
    # 11. a median halves the area
    area = 2 * rng.randint(8, 60)
    questions.append(number("a11", "droites", f"Un triangle ABC a une aire de {area} cm². M est le milieu de [BC]. Quelle est l'aire du triangle ABM, en cm² ?", Fraction(area // 2), 2,
                            ["Une médiane partage le triangle en deux triangles de même aire."], [f"{area} ÷ 2 = {area // 2} cm²."], units=cm2))
    # 12. the classic mistake
    base, height = 2 * rng.randint(2, 9), rng.randint(3, 9)
    options = ["Il a oublié de diviser par 2", "Il a oublié l'unité", "Il a mélangé la base et la hauteur"]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a12", "aire", f"Karim calcule l'aire d'un triangle de base {base} cm et de hauteur {height} cm : « {base} × {height} = {base * height} cm² ». Quelle est son erreur ?", [options[i] for i in order], order.index(0), 3,
                            ["Un triangle est la moitié d'un rectangle."], [f"{base} × {height} = {base * height} est l'aire du rectangle.", f"L'aire du triangle est {base * height} ÷ 2 = {base * height // 2} cm²."],
                            wrong={order.index(1): "L'unité est présente.", order.index(2): "Multiplier la base par la hauteur est correct."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=13, title="Les triangles", language="fr",
    intro="Le toit d'une case, un panneau, un fanion : le triangle est la figure la plus simple qui entoure une surface. "
          "Ce chapitre t'apprend à reconnaître les triangles particuliers, à calculer leur périmètre et leur aire, et à utiliser leurs hauteurs et leurs médianes.",
    objectives=["Reconnaître un triangle isocèle, équilatéral ou rectangle à partir de ses côtés ou d'un angle droit.",
                "Calculer le périmètre d'un triangle et retrouver un côté à partir du périmètre.",
                "Connaître la hauteur d'un triangle et calculer son aire.",
                "Connaître la médiane et la médiatrice d'un côté, et calculer avec une médiane."],
    prerequisites=[{"text": "Connaître les segments, le milieu d'un segment et les droites perpendiculaires.", "chapter": "sn-6e-droites-cercles"},
                   {"text": "Calculer l'aire d'un rectangle.", "chapter": "sn-6e-solides"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Thirteenth chapter of the Senegal Sixième course. Its contents follow lesson 5 of the Côte d'Ivoire Sixième programme (the kinds of triangle, heights, medians, perimeter and area), which was read for it, "
                "so it is also offered there, but the programme's own situations are not reproduced. The figures are drawn by the app. Building a triangle with a ruler and a compass cannot be done on a screen, so it is not covered, "
                "and the sum of the angles of a triangle is not taught. It has not been checked against the official Senegalese programme.",
)
