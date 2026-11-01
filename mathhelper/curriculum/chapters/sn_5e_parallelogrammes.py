"""Cinquième, Parallélogrammes particuliers: the tenth chapter of the Senegal Cinquième course, written in French.

The contents follow the lesson "Parallélogrammes particuliers" of the Côte d'Ivoire Cinquième programme (the rectangle, the rhombus and the square, their definitions, the direct and
converse properties of their diagonals, the perimeter and the area of a rhombus, and how to show that a quadrilateral is one of them), which was read for this chapter. Every explanation,
example, figure and exercise was written independently, with our own numbers. It builds on the Sixième chapter on the parallelogram. Constructions with instruments cannot be done on a
screen: they are described. The length of a diagonal from the sides is not asked, because it needs a Quatrième property. Fixed answers are written as exact fractions and re-checked by
tests against an independent recalculation, and each worked example carries a "verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .figures import Figure, figure
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-5e-parallelogrammes"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")
DEG = ["°", "degrés", "degré", "deg", "degres"]

# ----- Figures -----
RECT = (Figure().point("A", 60, 60, -14, -6).point("B", 280, 60, 8, -6).point("C", 280, 160, 8, 14).point("D", 60, 160, -14, 14).point("O", 170, 110, 8, 22)
        .segment("A", "B").segment("B", "C").segment("C", "D").segment("D", "A").segment("A", "C", "fig-dash").segment("B", "D", "fig-dash").right_angle("A", "B", "D", 12))
RHOMBUS = (Figure().point("A", 170, 20, 8, -4).point("B", 260, 105, 8, 6).point("C", 170, 190, 8, 14).point("D", 80, 105, -16, 6).point("O", 170, 105, 8, 22)
           .segment("A", "B").segment("B", "C").segment("C", "D").segment("D", "A").segment("A", "C", "fig-dash").segment("B", "D", "fig-dash").right_angle("O", "B", "A", 12)
           .tick("A", "B", 1).tick("B", "C", 1).tick("C", "D", 1).tick("D", "A", 1))
SQUARE = (Figure().point("A", 100, 35, -14, -4).point("B", 240, 35, 8, -4).point("C", 240, 175, 8, 14).point("D", 100, 175, -14, 14).point("O", 170, 105, 8, 22)
          .segment("A", "B").segment("B", "C").segment("C", "D").segment("D", "A").segment("A", "C", "fig-dash").segment("B", "D", "fig-dash").right_angle("A", "B", "D", 12)
          .tick("A", "B", 1).tick("B", "C", 1).tick("C", "D", 1).tick("D", "A", 1).right_angle("O", "B", "A", 10))

# ----- Section 1: the rectangle -----
S1 = Section(
    "rectangle", "Le rectangle", 22, "rectangle",
    "Connaître la définition du rectangle et les propriétés de ses diagonales, calculer son périmètre et son aire, et montrer qu'un parallélogramme est un rectangle.",
    [
        para("Une porte, une feuille, un terrain de football : ces figures sont des rectangles. Un rectangle est un parallélogramme qui a en plus des angles droits."),
        definition("Rectangle",
                   "Un rectangle est un quadrilatère qui a quatre angles droits. Un rectangle est un parallélogramme : ses côtés opposés sont parallèles et égaux, et ses diagonales se coupent en leur milieu. "
                   "Un parallélogramme qui a un angle droit est un rectangle."),
        rule("Diagonales d'un rectangle",
             "Les diagonales d'un rectangle ont la même longueur : " + N("AC = BD") + ". Comme elles se coupent en leur milieu O, on a " + N("OA = OB = OC = OD") + ". "
             "Réciproquement, un parallélogramme dont les diagonales ont la même longueur est un rectangle."),
        figure(RECT, "Un rectangle ABCD avec ses deux diagonales en pointillés qui se coupent en O et un petit carré marquant un angle droit.", "Dans le rectangle ABCD, les diagonales [AC] et [BD] ont la même longueur et se coupent en leur milieu O."),
        rule("Périmètre et aire",
             "Pour un rectangle de longueur L et de largeur l : " + N("P = 2 \\times (L + l)") + " et " + N("A = L \\times l") + "."),
        example("Exemple 1", "ABCD est un rectangle avec AC = 14 cm. Quelles sont les longueurs BD et OA, où O est le point d'intersection des diagonales ?",
                "Les diagonales d'un rectangle sont égales et se coupent en leur milieu.",
                [(N("BD = AC") + " = " + N("14"), "Diagonales égales."),
                 (N("OA = AC \\div 2") + " = " + N("7"), "O est le milieu de [AC].")],
                N("BD = 14") + " cm et " + N("OA = 7") + " cm.", "14==14 and 14//2==7"),
        example("Exemple 2", "Un rectangle a une longueur de 12 cm et une largeur de 5 cm. Calculer son périmètre et son aire.",
                "On applique les deux formules.",
                [(N("2 \\times (12 + 5)") + " = " + N("34"), "Périmètre."),
                 (N("12 \\times 5") + " = " + N("60"), "Aire.")],
                N("34") + " cm et " + N("60") + " cm².", "2*(12+5)==34 and 12*5==60"),
        example("Exemple 3", "Un parallélogramme ABCD a ses diagonales AC = 10 cm et BD = 10 cm. Que peut-on dire ?",
                "Les diagonales sont égales : on utilise la réciproque.",
                [("AC = BD", "Les deux diagonales ont la même longueur."),
                 ("Un parallélogramme dont les diagonales sont égales est un rectangle", "ABCD est un rectangle.")],
                "ABCD est un rectangle.", "10==10"),
        example("Exemple 4", "ABCD est un parallélogramme avec un angle droit en A. Que peut-on dire ? Quelle est la mesure de l'angle en B ?",
                "Un parallélogramme qui a un angle droit est un rectangle ; les angles consécutifs sont supplémentaires.",
                [("Un angle droit : c'est un rectangle", "Les quatre angles sont droits."),
                 (N("180 - 90") + " = " + N("90"), "L'angle en B est supplémentaire de l'angle en A.")],
                "ABCD est un rectangle et l'angle B mesure " + N("90") + "°.", "180-90==90"),
        warning("Des diagonales égales ne suffisent pas toutes seules : il faut que ce soit un parallélogramme (diagonales qui se coupent en leur milieu) pour conclure à un rectangle. Et un rectangle n'a pas ses diagonales perpendiculaires, sauf si c'est un carré."),
    ],
    [
        number("s1-g1", "rectangle", "ABCD est un rectangle avec AC = 18 cm. Quelle est la longueur BD, en cm ?", Fraction(18), units=["cm"], hints=["Diagonales égales."], solution=["BD = AC = 18 cm."]),
        number("s1-g2", "rectangle", "ABCD est un rectangle de diagonales qui se coupent en O, avec BD = 13 cm. Quelle est la longueur OA, en cm ?", d("6,5"), units=["cm"], hints=["OA = OB = BD ÷ 2."], solution=["OA = BD ÷ 2 = 6,5 cm."]),
        number("s1-g3", "rectangle", "Un rectangle a une longueur de 9 cm et une largeur de 4 cm. Quel est son périmètre, en cm ?", Fraction(26), units=["cm"], hints=["2 × (L + l)."], solution=["2 × 13 = 26 cm."]),
        number("s1-g4", "rectangle", "Un rectangle a une longueur de 9 cm et une largeur de 4 cm. Quelle est son aire, en cm² ?", Fraction(36), units=["cm2", "cm²"], hints=["L × l."], solution=["9 × 4 = 36 cm²."]),
        choice("s1-g5", "rectangle", "Un parallélogramme a ses diagonales égales. Que peut-on dire ?", ["C'est un rectangle", "C'est un losange", "C'est un carré"], 0, hints=["Réciproque."], solution=["Diagonales égales : rectangle."], wrong={1: "Un losange a ses diagonales perpendiculaires.", 2: "Il faudrait aussi des diagonales perpendiculaires."}),
    ])

# ----- Section 2: the rhombus -----
S2 = Section(
    "losange", "Le losange", 24, "losange",
    "Connaître la définition du losange et les propriétés de ses diagonales, calculer son périmètre et son aire, et montrer qu'un parallélogramme est un losange.",
    [
        para("Le losange est le « carré penché » : un quadrilatère dont les quatre côtés ont la même longueur. Un cerf-volant, un pagne à motifs en diamant ou un damier tourné de 45° en donnent des exemples."),
        definition("Losange",
                   "Un losange est un quadrilatère dont les quatre côtés ont la même longueur. Un losange est un parallélogramme : ses côtés opposés sont parallèles et ses diagonales se coupent en leur milieu. "
                   "Un parallélogramme qui a deux côtés consécutifs égaux est un losange."),
        rule("Diagonales d'un losange",
             "Les diagonales d'un losange sont perpendiculaires, et elles se coupent en leur milieu. Chaque diagonale partage les angles du losange en deux angles égaux. "
             "Réciproquement, un parallélogramme dont les diagonales sont perpendiculaires est un losange."),
        figure(RHOMBUS, "Un losange ABCD avec ses quatre côtés marqués d'un même trait, ses diagonales en pointillés qui se coupent en O à angle droit.", "Dans le losange ABCD, les quatre côtés sont égaux et les diagonales se coupent en leur milieu O, perpendiculairement."),
        rule("Périmètre et aire",
             "Pour un losange de côté c : " + N("P = 4 \\times c") + ". Pour un losange de diagonales D et d : " + N("A = \\dfrac{D \\times d}{2}") + ". C'est la moitié du rectangle dont les côtés sont les deux diagonales."),
        example("Exemple 1", "Un losange a des côtés de 7 cm. Quel est son périmètre ?",
                "Les quatre côtés sont égaux.",
                [(N("4 \\times 7") + " = " + N("28"), "P = 4 × c.")],
                N("28") + " cm.", "4*7==28"),
        example("Exemple 2", "Un losange a des diagonales de 10 cm et de 6 cm. Quelle est son aire ?",
                "On applique la formule A = D × d ÷ 2.",
                [(N("10 \\times 6") + " = " + N("60"), "Produit des diagonales."),
                 (N("60 \\div 2") + " = " + N("30"), "On divise par 2.")],
                N("30") + " cm².", "10*6//2==30"),
        example("Exemple 3", "ABCD est un losange dont les diagonales se coupent en O. On sait que AC = 12 cm et BD = 8 cm. Calculer OA et OB.",
                "Les diagonales se coupent en leur milieu.",
                [(N("OA = 12 \\div 2") + " = " + N("6"), "O est le milieu de [AC]."),
                 (N("OB = 8 \\div 2") + " = " + N("4"), "O est le milieu de [BD].")],
                N("OA = 6") + " cm et " + N("OB = 4") + " cm.", "12//2==6 and 8//2==4"),
        example("Exemple 4", "ABCD est un parallélogramme avec AB = BC. Que peut-on dire ? Sachant que AB = 6 cm, quel est son périmètre ?",
                "Un parallélogramme qui a deux côtés consécutifs égaux est un losange.",
                [("AB = BC : deux côtés consécutifs égaux", "ABCD est un losange."),
                 (N("4 \\times 6") + " = " + N("24"), "Les quatre côtés mesurent 6 cm.")],
                "ABCD est un losange de périmètre " + N("24") + " cm.", "4*6==24"),
        example("Exemple 5", "Un losange a un angle de 60° en A. Quelle est la mesure de l'angle en B ? Quelle est la mesure de l'angle que fait la diagonale [AC] avec le côté [AB] ?",
                "Les angles consécutifs sont supplémentaires, et la diagonale partage l'angle en deux.",
                [(N("180 - 60") + " = " + N("120"), "L'angle en B."),
                 (N("60 \\div 2") + " = " + N("30"), "La diagonale [AC] partage l'angle A en deux angles de 30°.")],
                N("120") + "° et " + N("30") + "°.", "180-60==120 and 60//2==30"),
        warning("Un losange n'a pas forcément d'angle droit : les diagonales sont perpendiculaires entre elles, mais les côtés ne le sont pas. Et l'aire d'un losange n'est pas « côté × côté » (c'est celle d'un carré) : il faut les diagonales, ou une base et une hauteur."),
    ],
    [
        number("s2-g1", "losange", "Un losange a des côtés de 8,5 cm. Quel est son périmètre, en cm ?", Fraction(34), units=["cm"], hints=["4 × côté."], solution=["4 × 8,5 = 34 cm."]),
        number("s2-g2", "losange", "Un losange a des diagonales de 14 cm et de 8 cm. Quelle est son aire, en cm² ?", Fraction(56), units=["cm2", "cm²"], hints=["D × d ÷ 2."], solution=["14 × 8 = 112.", "112 ÷ 2 = 56 cm²."]),
        number("s2-g3", "losange", "ABCD est un losange de diagonales qui se coupent en O, avec AC = 16 cm. Quelle est la longueur OC, en cm ?", Fraction(8), units=["cm"], hints=["O est le milieu."], solution=["16 ÷ 2 = 8 cm."]),
        number("s2-g4", "losange", "Un losange a un angle de 70°. Quelle est la mesure de l'angle consécutif, en degrés ?", Fraction(110), units=DEG, hints=["Supplémentaires."], solution=["180 − 70 = 110°."]),
        choice("s2-g5", "losange", "Un parallélogramme a ses diagonales perpendiculaires. Que peut-on dire ?", ["C'est un losange", "C'est un rectangle", "C'est un carré"], 0, hints=["Réciproque."], solution=["Diagonales perpendiculaires : losange."], wrong={1: "Un rectangle a des diagonales égales.", 2: "Il faudrait aussi qu'elles soient égales."}),
    ])

# ----- Section 3: the square -----
S3 = Section(
    "carre", "Le carré", 22, "carre",
    "Connaître la définition du carré, qui est à la fois un rectangle et un losange, ses propriétés, son périmètre et son aire.",
    [
        para("Un carré a quatre côtés égaux et quatre angles droits : il réunit le rectangle et le losange. Il en hérite donc toutes les propriétés."),
        definition("Carré",
                   "Un carré est un quadrilatère qui a quatre côtés égaux et quatre angles droits. C'est à la fois un rectangle et un losange, donc aussi un parallélogramme."),
        rule("Propriétés du carré",
             "Les diagonales d'un carré ont la même longueur, sont perpendiculaires et se coupent en leur milieu. Chaque diagonale fait un angle de 45° avec les côtés. "
             "Pour un carré de côté c : " + N("P = 4 \\times c") + " et " + N("A = c \\times c") + "."),
        figure(SQUARE, "Un carré ABCD avec ses quatre côtés marqués d'un même trait, ses diagonales en pointillés qui se coupent en O à angle droit, et un angle droit en A.", "Dans le carré ABCD, les diagonales sont égales, perpendiculaires et se coupent en leur milieu O."),
        rule("Pour montrer qu'un quadrilatère est un carré",
             "On peut montrer que c'est un rectangle qui a deux côtés consécutifs égaux, ou un losange qui a un angle droit, ou un parallélogramme dont les diagonales sont à la fois égales et perpendiculaires."),
        example("Exemple 1", "Un carré a des côtés de 9 cm. Calculer son périmètre et son aire.",
                "On applique les deux formules.",
                [(N("4 \\times 9") + " = " + N("36"), "Périmètre."),
                 (N("9 \\times 9") + " = " + N("81"), "Aire.")],
                N("36") + " cm et " + N("81") + " cm².", "4*9==36 and 9*9==81"),
        example("Exemple 2", "ABCD est un carré avec AC = 16 cm. Quelle est la longueur BD ? Quelle est la mesure de l'angle entre la diagonale [AC] et le côté [AB] ?",
                "Les diagonales sont égales et font 45° avec les côtés.",
                [(N("BD = AC") + " = " + N("16"), "Diagonales égales."),
                 (N("90 \\div 2") + " = " + N("45"), "La diagonale partage l'angle droit en deux.")],
                N("BD = 16") + " cm et " + N("45") + "°.", "16==16 and 90//2==45"),
        example("Exemple 3", "Un carré a un périmètre de 28 cm. Quel est son côté ? Quelle est son aire ?",
                "On divise le périmètre par 4, puis on élève au carré.",
                [(N("28 \\div 4") + " = " + N("7"), "Le côté."),
                 (N("7 \\times 7") + " = " + N("49"), "L'aire.")],
                N("7") + " cm et " + N("49") + " cm².", "28//4==7 and 7*7==49"),
        example("Exemple 4", "Un parallélogramme ABCD a des diagonales de même longueur et perpendiculaires. Que peut-on dire ?",
                "Diagonales égales : rectangle. Diagonales perpendiculaires : losange.",
                [("Diagonales égales : c'est un rectangle", "Réciproque pour le rectangle."),
                 ("Diagonales perpendiculaires : c'est un losange", "Réciproque pour le losange."),
                 ("Un rectangle qui est aussi un losange est un carré", "ABCD est un carré.")],
                "ABCD est un carré.", "1+1==2"),
        warning("Tout carré est un rectangle et un losange, mais tout rectangle ou tout losange n'est pas un carré. Et pour l'aire d'un carré, n'écris pas « 4 × côté » (c'est le périmètre) mais « côté × côté »."),
    ],
    [
        number("s3-g1", "carre", "Un carré a des côtés de 12 cm. Quel est son périmètre, en cm ?", Fraction(48), units=["cm"], hints=["4 × côté."], solution=["48 cm."]),
        number("s3-g2", "carre", "Un carré a des côtés de 12 cm. Quelle est son aire, en cm² ?", Fraction(144), units=["cm2", "cm²"], hints=["Côté × côté."], solution=["144 cm²."]),
        number("s3-g3", "carre", "Un carré a un périmètre de 36 cm. Quel est son côté, en cm ?", Fraction(9), units=["cm"], hints=["36 ÷ 4."], solution=["9 cm."]),
        number("s3-g4", "carre", "ABCD est un carré de centre O, avec BD = 20 cm. Quelle est la longueur OA, en cm ?", Fraction(10), units=["cm"], hints=["AC = BD, O est le milieu."], solution=["AC = 20 cm, OA = 10 cm."]),
        choice("s3-g5", "carre", "Quel quadrilatère a des diagonales égales, perpendiculaires et qui se coupent en leur milieu ?", ["Le carré", "Le rectangle", "Le losange"], 0, hints=["Les trois propriétés."], solution=["Le carré."], wrong={1: "Un rectangle n'a pas des diagonales perpendiculaires en général.", 2: "Un losange n'a pas des diagonales égales en général."}),
    ])

# ----- Section 4: problems -----
S4 = Section(
    "problemes", "Montrer qu'un quadrilatère est particulier, et résoudre des problèmes", 24, "problemes",
    "Utiliser les propriétés et les réciproques pour reconnaître un rectangle, un losange ou un carré, et résoudre des problèmes de périmètre et d'aire.",
    [
        para("Pour montrer qu'un quadrilatère est un rectangle, un losange ou un carré, on commence presque toujours par montrer que c'est un parallélogramme, puis on ajoute une propriété supplémentaire."),
        rule("Tableau de décision",
             "Parallélogramme + un angle droit ou diagonales égales : rectangle. Parallélogramme + deux côtés consécutifs égaux ou diagonales perpendiculaires : losange. Rectangle + deux côtés consécutifs égaux, ou losange + un angle droit : carré."),
        example("Exemple 1", "ABCD est un quadrilatère dont les diagonales se coupent en leur milieu, sont égales (10 cm) et sont perpendiculaires. Que peut-on dire ? Quelle est son aire ?",
                "Diagonales qui se coupent en leur milieu : parallélogramme. Égales : rectangle. Perpendiculaires : losange. Donc carré. L'aire se calcule avec les diagonales.",
                [("Parallélogramme, rectangle et losange", "C'est un carré."),
                 (N("10 \\times 10 \\div 2") + " = " + N("50"), "Aire d'un losange (D × d ÷ 2) : 50 cm²."),
                 ("Le côté est tel que c × c = 50", "L'aire d'un carré est aussi c × c, ce qui donne une autre façon de voir l'aire.")],
                "C'est un carré d'aire " + N("50") + " cm².", "10*10//2==50"),
        example("Exemple 2", "Un jardin en forme de rectangle de 30 m sur 20 m est entouré d'un grillage à 800 F le mètre. Quel est le prix ?",
                "On calcule le périmètre, puis on multiplie par le prix.",
                [(N("2 \\times (30 + 20)") + " = " + N("100"), "Périmètre : 100 m."),
                 (N("100 \\times 800") + " = " + N("80000"), "Prix : 80 000 F.")],
                N("80000") + " F.", "2*(30+20)==100 and 100*800==80000"),
        example("Exemple 3", "Un losange a un périmètre de 36 cm et une diagonale de 10 cm. L'autre diagonale mesure 12 cm. Quel est son côté ? Quelle est son aire ?",
                "Le côté est le quart du périmètre. L'aire se calcule avec les diagonales.",
                [(N("36 \\div 4") + " = " + N("9"), "Le côté."),
                 (N("10 \\times 12 \\div 2") + " = " + N("60"), "L'aire.")],
                "Côté " + N("9") + " cm, aire " + N("60") + " cm².", "36//4==9 and 10*12//2==60"),
        example("Exemple 4", "Un terrain carré de 40 m de côté est entouré d'un chemin de 2 m de large à l'extérieur. Quelle est l'aire du chemin ?",
                "On calcule l'aire du grand carré, puis on soustrait celle du terrain.",
                [(N("(40 + 2 \\times 2)^2") + " = " + N("44^2") + " = " + N("1936"), "Grand carré : 44 m de côté."),
                 (N("1936 - 40^2") + " = " + N("1936 - 1600") + " = " + N("336"), "On retire le terrain.")],
                N("336") + " m².", "44**2==1936 and 1936-1600==336"),
        warning("Pour conclure, il faut citer une propriété et sa condition : « c'est un parallélogramme avec deux côtés consécutifs égaux, donc c'est un losange ». Dire « ça a l'air d'un carré » n'est pas une preuve."),
    ],
    [
        choice("s4-g1", "problemes", "ABCD est un parallélogramme avec AB = BC et un angle droit en A. Que peut-on dire ?", ["C'est un carré", "C'est un losange seulement", "C'est un rectangle seulement"], 0, hints=["Deux côtés consécutifs égaux : losange. Un angle droit : rectangle."], solution=["À la fois losange et rectangle : carré."], wrong={1: "Il a aussi un angle droit.", 2: "Il a aussi deux côtés consécutifs égaux."}),
        number("s4-g2", "problemes", "Un champ rectangulaire de 50 m sur 30 m est entouré d'un grillage à 500 F le mètre. Quel est le prix, en F ?", Fraction(80000), units=["F"], hints=["Périmètre d'abord."], solution=["2 × 80 = 160 m.", "160 × 500 = 80 000 F."]),
        number("s4-g3", "problemes", "Un losange a des diagonales de 20 cm et de 15 cm. Quelle est son aire, en cm² ?", Fraction(150), units=["cm2", "cm²"], hints=["D × d ÷ 2."], solution=["20 × 15 ÷ 2 = 150 cm²."]),
        number("s4-g4", "problemes", "Un carré de 10 cm de côté est entouré d'une bordure de 1 cm de large. Quelle est l'aire de la bordure, en cm² ?", Fraction(44), units=["cm2", "cm²"], hints=["12 × 12 − 10 × 10."], solution=["144 − 100 = 44 cm²."]),
        choice("s4-g5", "problemes", "ABCD est un parallélogramme avec AC ⊥ BD. Que peut-on dire ?", ["C'est un losange", "C'est un rectangle", "C'est un trapèze"], 0, hints=["Diagonales perpendiculaires."], solution=["Losange."], wrong={1: "Un rectangle a des diagonales égales.", 2: "Un parallélogramme n'est pas un trapèze ici."}),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "rectangle", "ABCD est un rectangle avec BD = 25 cm. Quelle est la longueur AC, en cm ?", Fraction(25), 1, ["Diagonales égales."], ["25 cm."], units=["cm"]),
    number("p2", "rectangle", "ABCD est un rectangle, O est le point d'intersection des diagonales et OA = 7,5 cm. Quelle est la longueur BD, en cm ?", Fraction(15), 2, ["BD = AC = 2 × OA."], ["15 cm."], units=["cm"]),
    number("p3", "rectangle", "Un rectangle a une longueur de 15 cm et une largeur de 8 cm. Quel est son périmètre, en cm ?", Fraction(46), 1, ["2 × (15 + 8)."], ["46 cm."], units=["cm"]),
    number("p4", "rectangle", "Un rectangle a une longueur de 15 cm et une largeur de 8 cm. Quelle est son aire, en cm² ?", Fraction(120), 1, ["15 × 8."], ["120 cm²."], units=["cm2", "cm²"]),
    number("p5", "rectangle", "Un rectangle a un périmètre de 40 cm et une largeur de 6 cm. Quelle est sa longueur, en cm ?", Fraction(14), 2, ["Demi-périmètre − largeur."], ["20 − 6 = 14 cm."], units=["cm"]),
    number("p6", "rectangle", "Un rectangle a une aire de 84 cm² et une longueur de 12 cm. Quelle est sa largeur, en cm ?", Fraction(7), 2, ["Aire ÷ longueur."], ["84 ÷ 12 = 7 cm."], units=["cm"]),
    choice("p7", "rectangle", "ABCD est un parallélogramme avec un angle droit. Que peut-on dire ?", ["C'est un rectangle", "C'est un losange", "C'est un carré"], 0, 1, ["Parallélogramme + angle droit."], ["Rectangle."], wrong={1: "Il faudrait deux côtés consécutifs égaux.", 2: "Il faudrait aussi deux côtés consécutifs égaux."}),
    choice("p8", "rectangle", "Karim dit : « un quadrilatère à diagonales égales est un rectangle ». Qu'en penses-tu ?", ["Il faut aussi que ce soit un parallélogramme", "Il a raison", "Il faut que les diagonales soient perpendiculaires"], 0, 3, ["Les diagonales d'un rectangle se coupent en leur milieu."], ["Diagonales égales ET qui se coupent en leur milieu."], wrong={1: "Il manque la condition de milieu.", 2: "C'est la condition du losange."}),
    number("p9", "losange", "Un losange a des côtés de 11 cm. Quel est son périmètre, en cm ?", Fraction(44), 1, ["4 × 11."], ["44 cm."], units=["cm"]),
    number("p10", "losange", "Un losange a un périmètre de 50 cm. Quelle est la longueur d'un côté, en cm ?", d("12,5"), 1, ["50 ÷ 4."], ["12,5 cm."], units=["cm"]),
    number("p11", "losange", "Un losange a des diagonales de 9 cm et de 12 cm. Quelle est son aire, en cm² ?", Fraction(54), 2, ["9 × 12 ÷ 2."], ["54 cm²."], units=["cm2", "cm²"]),
    number("p12", "losange", "Un losange a une aire de 48 cm² et une diagonale de 12 cm. Quelle est l'autre diagonale, en cm ?", Fraction(8), 3, ["D × d = 96."], ["2 × 48 = 96.", "96 ÷ 12 = 8 cm."], units=["cm"]),
    number("p13", "losange", "ABCD est un losange de diagonales qui se coupent en O, avec BD = 9 cm. Quelle est la longueur OB, en cm ?", d("4,5"), 1, ["Moitié."], ["4,5 cm."], units=["cm"]),
    number("p14", "losange", "Un losange a un angle de 50°. Quelle est la mesure de l'angle consécutif, en degrés ?", Fraction(130), 1, ["180 − 50."], ["130°."], units=DEG),
    number("p15", "losange", "Un losange a un angle de 80° en A. Quelle est la mesure de l'angle que fait la diagonale [AC] avec le côté [AB], en degrés ?", Fraction(40), 2, ["La moitié."], ["40°."], units=DEG),
    number("p16", "losange", "Quel est l'angle entre les deux diagonales d'un losange, en degrés ?", Fraction(90), 1, ["Perpendiculaires."], ["90°."], units=DEG),
    choice("p17", "losange", "ABCD est un parallélogramme avec AB = AD. Que peut-on dire ?", ["C'est un losange", "C'est un rectangle", "C'est un trapèze"], 0, 1, ["Deux côtés consécutifs égaux."], ["Losange."], wrong={1: "Un rectangle n'est pas forcé d'avoir deux côtés consécutifs égaux.", 2: "Un parallélogramme a deux paires de côtés parallèles."}),
    number("p18", "carre", "Un carré a des côtés de 7,5 cm. Quel est son périmètre, en cm ?", Fraction(30), 1, ["4 × 7,5."], ["30 cm."], units=["cm"]),
    number("p19", "carre", "Un carré a des côtés de 7,5 cm. Quelle est son aire, en cm² ?", d("56,25"), 2, ["7,5 × 7,5."], ["56,25 cm²."], units=["cm2", "cm²"]),
    number("p20", "carre", "Un carré a un périmètre de 44 cm. Quelle est son aire, en cm² ?", Fraction(121), 2, ["Côté = 11."], ["11 × 11 = 121 cm²."], units=["cm2", "cm²"]),
    number("p21", "carre", "ABCD est un carré avec AC = 30 cm. Quelle est la longueur OB (O au centre), en cm ?", Fraction(15), 2, ["BD = AC."], ["OB = 15 cm."], units=["cm"]),
    number("p22", "carre", "Quelle est la mesure de l'angle que fait une diagonale d'un carré avec un côté, en degrés ?", Fraction(45), 1, ["90 ÷ 2."], ["45°."], units=DEG),
    choice("p23", "carre", "Tout carré est-il un losange ?", ["Oui", "Non"], 0, 1, ["Quatre côtés égaux."], ["Oui, un carré est un losange avec des angles droits."], wrong={1: "Quatre côtés égaux : losange."}),
    choice("p24", "carre", "Tout rectangle est-il un carré ?", ["Non", "Oui"], 0, 1, ["Pense à une feuille."], ["Non, seulement s'il a deux côtés consécutifs égaux."], wrong={1: "Une feuille A4 est un rectangle, pas un carré."}),
    choice("p25", "carre", "Quel quadrilatère a quatre côtés égaux et quatre angles droits ?", ["Le carré", "Le rectangle", "Le losange"], 0, 1, ["Les deux conditions."], ["Le carré."], wrong={1: "Les côtés ne sont pas tous égaux.", 2: "Les angles ne sont pas tous droits."}),
    number("p26", "problemes", "Un terrain rectangulaire de 60 m sur 40 m est entouré d'une clôture à 1 200 F le mètre. Quel est le prix, en F ?", Fraction(240000), 2, ["2 × 100."], ["200 × 1 200 = 240 000 F."], units=["F"]),
    number("p27", "problemes", "Une cour carrée de 25 m de côté est carrelée. Combien de mètres carrés faut-il carreler ?", Fraction(625), 1, ["25 × 25."], ["625 m²."], units=["m2", "m²"]),
    number("p28", "problemes", "Un losange a des côtés de 10 cm et une aire de 96 cm². Une diagonale mesure 12 cm. Quelle est l'autre, en cm ?", Fraction(16), 3, ["D × d = 192."], ["2 × 96 = 192.", "192 ÷ 12 = 16 cm."], units=["cm"]),
    number("p29", "problemes", "Un carré de 8 cm de côté est entouré d'une bordure de 2 cm. Quelle est l'aire de la bordure, en cm² ?", Fraction(80), 3, ["12 × 12 − 8 × 8."], ["144 − 64 = 80 cm²."], units=["cm2", "cm²"]),
    choice("p30", "problemes", "ABCD est un parallélogramme avec des diagonales égales et perpendiculaires. Que peut-on dire ?", ["C'est un carré", "C'est un losange seulement", "C'est un rectangle seulement"], 0, 2, ["Les deux réciproques."], ["Carré."], wrong={1: "Les diagonales sont aussi égales.", 2: "Les diagonales sont aussi perpendiculaires."}),
    number("p31", "problemes", "Un rectangle de 18 cm sur 10 cm et un carré ont le même périmètre. Quel est le côté du carré, en cm ?", Fraction(14), 3, ["Périmètre du rectangle : 56."], ["2 × 28 = 56.", "56 ÷ 4 = 14 cm."], units=["cm"]),
    number("p32", "problemes", "Un rectangle de 18 cm sur 10 cm et un carré ont le même périmètre. Quelle figure a la plus grande aire ? Réponds 1 pour le rectangle, 2 pour le carré.", Fraction(2), 3, ["Rectangle : 180. Carré : 196."], ["Rectangle : 18 × 10 = 180 cm².", "Carré de 14 cm : 196 cm². Le carré a la plus grande aire."]),
]

SUMMARY = [
    definition("Rectangle, losange, carré", "Rectangle : 4 angles droits (parallélogramme à diagonales égales). Losange : 4 côtés égaux (parallélogramme à diagonales perpendiculaires). Carré : à la fois rectangle et losange."),
    rule("Diagonales", "Rectangle : diagonales égales, qui se coupent en leur milieu. Losange : diagonales perpendiculaires, qui se coupent en leur milieu. Carré : égales, perpendiculaires et se coupent en leur milieu, et font 45° avec les côtés."),
    rule("Périmètre et aire", "Rectangle : P = 2 × (L + l), A = L × l. Losange : P = 4 × c, A = D × d ÷ 2. Carré : P = 4 × c, A = c × c."),
    para("Les erreurs à éviter : conclure avec seulement le dessin ; oublier que les diagonales d'un rectangle ne sont pas perpendiculaires ; calculer l'aire d'un losange avec côté × côté ; confondre périmètre et aire d'un carré."),
]

CONCEPTS = {
    "rectangle": ("Le rectangle", "rectangle"),
    "losange": ("Le losange", "losange"),
    "carre": ("Le carré", "carre"),
    "problemes": ("Reconnaître et résoudre des problèmes", "problemes"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    cm, cm2 = ["cm"], ["cm2", "cm²"]
    # 1. the diagonal of a rectangle
    ac = rand_decimal(rng, 5, 30, 1)
    questions.append(number("a1", "rectangle", f"ABCD est un rectangle avec AC = {show(ac)} cm. Quelle est la longueur BD, en cm ?", ac, 1, ["Diagonales égales."], [f"BD = AC = {show(ac)} cm."], units=cm))
    # 2. half a diagonal
    bd = 2 * rng.randint(4, 25)
    questions.append(number("a2", "rectangle", f"ABCD est un rectangle, O est le point d'intersection des diagonales et BD = {bd} cm. Quelle est la longueur OA, en cm ?", Fraction(bd // 2), 2, ["OA = BD ÷ 2."], [f"{bd} ÷ 2 = {bd // 2} cm."], units=cm))
    # 3. the perimeter of a rectangle
    length, width = rng.randint(8, 30), rng.randint(3, 15)
    questions.append(number("a3", "rectangle", f"Un rectangle a une longueur de {length} cm et une largeur de {width} cm. Quel est son périmètre, en cm ?", Fraction(2 * (length + width)), 1, ["2 × (L + l)."], [f"2 × {length + width} = {2 * (length + width)} cm."], units=cm))
    # 4. the area of a rectangle
    length, width = rng.randint(8, 30), rng.randint(3, 15)
    questions.append(number("a4", "rectangle", f"Un rectangle a une longueur de {length} cm et une largeur de {width} cm. Quelle est son aire, en cm² ?", Fraction(length * width), 1, ["L × l."], [f"{length} × {width} = {length * width} cm²."], units=cm2))
    # 5. the perimeter of a rhombus
    c = rand_decimal(rng, 3, 20, 1)
    questions.append(number("a5", "losange", f"Un losange a des côtés de {show(c)} cm. Quel est son périmètre, en cm ?", 4 * c, 1, ["4 × côté."], [f"4 × {show(c)} = {show(4 * c)} cm."], units=cm))
    # 6. the area of a rhombus
    dd, d_ = 2 * rng.randint(3, 15), rng.randint(4, 20)
    questions.append(number("a6", "losange", f"Un losange a des diagonales de {dd} cm et de {d_} cm. Quelle est son aire, en cm² ?", Fraction(dd * d_, 2), 2, ["D × d ÷ 2."], [f"{dd} × {d_} = {dd * d_}.", f"{dd * d_} ÷ 2 = {dd * d_ // 2} cm²."], units=cm2))
    # 7. the missing diagonal of a rhombus
    big, small = rng.randint(6, 24), rng.randint(4, 20)
    area = Fraction(big * small, 2)
    questions.append(number("a7", "losange", f"Un losange a une aire de {show(area)} cm² et une diagonale de {big} cm. Quelle est l'autre diagonale, en cm ?", Fraction(small), 3, ["D × d = 2 × aire."], [f"2 × {show(area)} = {big * small}.", f"{big * small} ÷ {big} = {small} cm."], units=cm))
    # 8. an angle of a rhombus
    angle = rng.randint(20, 80)
    questions.append(number("a8", "losange", f"Un losange a un angle de {angle}°. Quelle est la mesure de l'angle consécutif, en degrés ?", Fraction(180 - angle), 1, ["Angles consécutifs supplémentaires."], [f"180 − {angle} = {180 - angle}°."], units=DEG))
    # 9. the area of a square
    side = rand_decimal(rng, 2, 12, 1)
    questions.append(number("a9", "carre", f"Un carré a des côtés de {show(side)} cm. Quelle est son aire, en cm² ?", side * side, 2, ["Côté × côté."], [f"{show(side)} × {show(side)} = {show(side * side)} cm²."], units=cm2))
    # 10. the side from the perimeter
    c = rng.randint(3, 40)
    questions.append(number("a10", "carre", f"Un carré a un périmètre de {4 * c} cm. Quelle est son aire, en cm² ?", Fraction(c * c), 3, ["Côté = périmètre ÷ 4."], [f"{4 * c} ÷ 4 = {c}.", f"{c} × {c} = {c * c} cm²."], units=cm2))
    # 11. the nature of a quadrilateral
    options = ["Un rectangle", "Un losange", "Un carré"]
    kind = rng.choice([0, 1, 2])
    given = ["Un parallélogramme dont les diagonales sont égales", "Un parallélogramme dont les diagonales sont perpendiculaires", "Un parallélogramme dont les diagonales sont égales et perpendiculaires"][kind]
    questions.append(choice("a11", "problemes", f"{given} est :", options, kind, 2, ["Utilise les réciproques."], [["Diagonales égales : rectangle.", "Diagonales perpendiculaires : losange.", "Les deux à la fois : carré."][kind]]))
    # 12. the border of a square
    side, border = rng.randint(5, 30), rng.randint(1, 4)
    questions.append(number("a12", "problemes", f"Un carré de {side} cm de côté est entouré d'une bordure de {border} cm de large. Quelle est l'aire de la bordure, en cm² ?", Fraction((side + 2 * border) ** 2 - side**2), 3, ["Grand carré moins petit carré."],
                            [f"({side} + {2 * border})² = {(side + 2 * border) ** 2}.", f"{(side + 2 * border) ** 2} − {side ** 2} = {(side + 2 * border) ** 2 - side ** 2} cm²."], units=cm2))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=10, title="Parallélogrammes particuliers : rectangle, losange et carré", language="fr",
    intro="Un terrain de football, un cerf-volant, un carrelage : toutes ces formes sont des parallélogrammes particuliers. "
          "Ce chapitre t'apprend leurs propriétés, surtout celles de leurs diagonales, à reconnaître chacun d'eux et à calculer leurs périmètres et leurs aires.",
    objectives=["Connaître le rectangle, le losange et le carré et leurs propriétés.",
                "Utiliser les propriétés et les réciproques sur les diagonales pour montrer qu'un quadrilatère est particulier.",
                "Calculer le périmètre et l'aire d'un rectangle, d'un losange et d'un carré.",
                "Résoudre des problèmes de périmètre et d'aire."],
    prerequisites=[{"text": "Connaître le parallélogramme et ses diagonales.", "chapter": "sn-6e-parallelogramme"},
                   {"text": "Connaître les triangles particuliers.", "chapter": "sn-5e-triangles"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Tenth chapter of the Senegal Cinquième course. Its contents follow the special parallelograms lesson of the Côte d'Ivoire Cinquième programme (the rectangle, the rhombus and the square, the properties of their diagonals and their converses, perimeter and area), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. Constructions with instruments cannot be done on a screen, so they are described and not covered. "
                "It has not been checked against the official Senegalese programme.",
)
