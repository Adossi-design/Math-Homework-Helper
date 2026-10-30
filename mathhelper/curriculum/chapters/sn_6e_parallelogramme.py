"""Sixième, Le parallélogramme: the fourteenth chapter of the Senegal Sixième course, written in French.

The contents follow lesson 6 "Parallélogramme" of the Côte d'Ivoire Sixième programme (the definition, the properties of opposite sides and of the diagonals with their converses,
how to justify that a quadrilateral is a parallelogram, the perimeter and the area), which was read for this chapter. Every explanation, example, figure and exercise was written
independently, with our own numbers. The figures are drawn from constants by figures.py. Constructing a parallelogram with instruments cannot be done on a screen: it is described.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .figures import Figure, figure
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-6e-parallelogramme"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")

# ----- Figures -----
SIDES = (Figure().point("A", 60, 150, -14, 22).point("B", 220, 150, 6, 22).point("C", 290, 60, 8, -4).point("D", 130, 60, -14, -6)
         .segment("A", "B").segment("B", "C").segment("C", "D").segment("D", "A")
         .arrow_mark("A", "B", 1).arrow_mark("D", "C", 1).arrow_mark("B", "C", 2).arrow_mark("A", "D", 2))
DIAGONALS = (Figure().point("A", 60, 150, -14, 22).point("B", 220, 150, 6, 22).point("C", 290, 60, 8, -4).point("D", 130, 60, -14, -6).point("O", 175, 105, 16, 26)
             .segment("A", "B").segment("B", "C").segment("C", "D").segment("D", "A").segment("A", "C", "fig-dash").segment("B", "D", "fig-dash")
             .tick("A", "O", 1).tick("O", "C", 1).tick("B", "O", 2).tick("O", "D", 2))
HEIGHT = (Figure().point("A", 60, 150, -14, 22).point("B", 220, 150, 6, 22).point("C", 290, 60, 8, -4).point("D", 130, 60, -14, -6).point("H", 130, 150, -4, 22)
          .segment("A", "B").segment("B", "C").segment("C", "D").segment("D", "A").segment("D", "H", "fig-dash").right_angle("H", "B", "D", 12))
HALVES = (Figure().point("A", 60, 150, -14, 22).point("B", 220, 150, 6, 22).point("C", 290, 60, 8, -4).point("D", 130, 60, -14, -6)
          .segment("A", "B").segment("B", "C").segment("C", "D").segment("D", "A").segment("A", "C", "fig-dash"))

# ----- Section 1: definition and properties -----
S1 = Section(
    "definition", "Le parallélogramme : définition et propriétés", 22, "definition",
    "Reconnaître un parallélogramme, connaître ses côtés opposés et ses diagonales, et utiliser leurs propriétés pour calculer des longueurs.",
    [
        para("Les motifs d'un pagne, la forme d'un cadre incliné, le cerf-volant : beaucoup de figures ressemblent à un rectangle penché. Ce sont des parallélogrammes."),
        definition("Quadrilatère et parallélogramme",
                   "Un quadrilatère est une figure à quatre sommets et quatre côtés. Un parallélogramme est un quadrilatère dont les côtés opposés sont parallèles deux à deux. "
                   "Le quadrilatère ABCD est un parallélogramme si " + N("(AB) // (DC)") + " et " + N("(AD) // (BC)") + ". Les sommets se nomment dans l'ordre en faisant le tour de la figure."),
        figure(SIDES, "Un parallélogramme ABCD dont les côtés opposés portent les mêmes chevrons : un chevron sur [AB] et [DC], deux chevrons sur [BC] et [AD].", "Les côtés opposés de ABCD sont parallèles : (AB) // (DC) et (AD) // (BC)."),
        rule("Propriétés du parallélogramme",
             "Dans un parallélogramme, les côtés opposés ont la même longueur : " + N("AB = DC") + " et " + N("AD = BC") + ". Les diagonales [AC] et [BD] se coupent en leur milieu O : " + N("OA = OC") + " et " + N("OB = OD") + "."),
        figure(DIAGONALS, "Un parallélogramme ABCD avec ses deux diagonales en pointillés qui se coupent en O, et des traits égaux sur OA et OC, OB et OD.", "Les diagonales [AC] et [BD] se coupent en O, qui est le milieu de chacune d'elles."),
        example("Exemple 1", "ABCD est un parallélogramme avec AB = 7 cm et BC = 4 cm. Calculer CD et DA.",
                "Dans un parallélogramme, les côtés opposés ont la même longueur.",
                [(N("CD = AB") + " = " + N("7"), "[CD] est le côté opposé à [AB]."),
                 (N("DA = BC") + " = " + N("4"), "[DA] est le côté opposé à [BC].")],
                N("CD = 7") + " cm et " + N("DA = 4") + " cm.", "7==7 and 4==4"),
        example("Exemple 2", "ABCD est un parallélogramme, ses diagonales [AC] et [BD] se coupent en O. On a AC = 12 cm et BD = 9 cm. Calculer OA et OB.",
                "O est le milieu de chaque diagonale : OA et OB sont des moitiés.",
                [(N("OA = AC \\div 2") + " = " + N("6"), "O est le milieu de [AC]."),
                 (N("OB = BD \\div 2") + " = " + N("4,5"), "O est le milieu de [BD].")],
                N("OA = 6") + " cm et " + N("OB = 4,5") + " cm.", "12//2==6 and d('9')/2==d('4,5')"),
        example("Exemple 3", "Dans un parallélogramme ABCD, les diagonales se coupent en O et OC = 5,5 cm. Calculer AC.",
                "O est le milieu de [AC] : AC est le double de OC.",
                [(N("AC = 2 \\times OC") + " = " + N("2 \\times 5,5"), "AO = OC puisque O est le milieu."),
                 (N("2 \\times 5,5") + " = " + N("11"), "Le double de 5,5 est 11.")],
                N("AC = 11") + " cm.", "2*d('5,5')==11"),
        example("Exemple 4", "ABCD est un parallélogramme. Combien de paires de côtés parallèles a-t-il ? Combien de côtés a-t-il de longueurs différentes au maximum ?",
                "On regarde les côtés opposés.",
                [("Les paires de côtés opposés : [AB] et [DC], [AD] et [BC]", "Il y a 2 paires de côtés parallèles."),
                 ("Dans chaque paire, les deux côtés ont la même longueur", "Il y a au plus 2 longueurs différentes : AB = DC et AD = BC.")],
                N("2") + " paires de côtés parallèles et au plus " + N("2") + " longueurs différentes.", "4//2==2"),
        warning("Dans le nom ABCD, l'ordre des lettres compte : A et C sont opposés, B et D aussi, les diagonales sont [AC] et [BD]. Et attention : seuls les côtés opposés sont parallèles et égaux, pas les côtés consécutifs comme [AB] et [BC]."),
    ],
    [
        number("s1-g1", "definition", "ABCD est un parallélogramme et AB = 9 cm. Quelle est la longueur CD, en cm ?", Fraction(9), units=["cm"],
               hints=["[CD] est le côté opposé à [AB]."], solution=["Dans un parallélogramme, les côtés opposés sont égaux : CD = AB = 9 cm."]),
        number("s1-g2", "definition", "ABCD est un parallélogramme de diagonales [AC] et [BD], qui se coupent en O. AC = 16 cm. Quelle est la longueur OA, en cm ?", Fraction(8), units=["cm"],
               hints=["O est le milieu de [AC]."], solution=["OA = AC ÷ 2 = 16 ÷ 2 = 8 cm."]),
        number("s1-g3", "definition", "ABCD est un parallélogramme de diagonales [AC] et [BD], qui se coupent en O. BD = 11 cm. Quelle est la longueur OB, en cm ?", d("5,5"), units=["cm"],
               hints=["O est le milieu de [BD]."], solution=["OB = BD ÷ 2 = 11 ÷ 2 = 5,5 cm."]),
        choice("s1-g4", "definition", "ABCD est un parallélogramme. Quelles diagonales a-t-il ?", ["[AB] et [CD]", "[AC] et [BD]", "[AD] et [BC]"], 1,
               hints=["Une diagonale joint deux sommets opposés."], solution=["A et C sont opposés, B et D sont opposés : les diagonales sont [AC] et [BD]."],
               wrong={0: "[AB] et [CD] sont des côtés.", 2: "[AD] et [BC] sont des côtés."}),
        choice("s1-g5", "definition", "ABCD est un parallélogramme. Laquelle de ces égalités est toujours vraie ?", ["AB = BC", "AB = CD", "AB = AC"], 1,
               hints=["Seuls les côtés opposés sont égaux."], solution=["[AB] et [CD] sont des côtés opposés : AB = CD."],
               wrong={0: "[AB] et [BC] sont consécutifs : ils n'ont pas toujours la même longueur.", 2: "[AC] est une diagonale, pas un côté."}),
    ])

# ----- Section 2: justifying a parallelogram -----
S2 = Section(
    "justifier", "Montrer qu'un quadrilatère est un parallélogramme", 22, "justifier",
    "Utiliser la définition et les réciproques des propriétés pour montrer qu'un quadrilatère est un parallélogramme.",
    [
        para("Pour être sûr qu'une figure est un parallélogramme, il ne suffit pas qu'elle en ait l'air. Il faut une raison. Heureusement, les propriétés vues à la section précédente marchent aussi dans l'autre sens."),
        rule("Trois façons de montrer qu'un quadrilatère est un parallélogramme",
             "1. Par la définition : si ses côtés opposés sont parallèles deux à deux. 2. Par les diagonales : si ses diagonales se coupent en leur milieu. 3. Par les côtés : si ses côtés opposés ont la même longueur deux à deux. "
             "Les propriétés 2 et 3 sont les réciproques des propriétés du parallélogramme, pour un quadrilatère non croisé (dont les côtés ne se traversent pas). On peut aussi montrer qu'un quadrilatère non croisé est un parallélogramme si deux de ses côtés opposés sont à la fois égaux et parallèles."),
        figure(HALVES, "Un parallélogramme ABCD avec sa diagonale [AC] en pointillés qui le partage en deux triangles.", "La diagonale [AC] partage le parallélogramme en deux triangles ABC et ACD de même aire."),
        example("Exemple 1", "ABCD est un quadrilatère avec AB = DC = 6 cm et AD = BC = 4 cm. Est-ce un parallélogramme ?",
                "On regarde si les côtés opposés sont égaux deux à deux.",
                [("AB = DC = 6 cm", "Une première paire de côtés opposés égaux."),
                 ("AD = BC = 4 cm", "Une deuxième paire de côtés opposés égaux."),
                 ("Ses côtés opposés ont la même longueur deux à deux", "C'est la réciproque de la propriété des côtés.")],
                "Oui, ABCD est un parallélogramme.", "6==6 and 4==4"),
        example("Exemple 2", "ABCD est un quadrilatère dont les diagonales se coupent en O avec OA = OC = 5 cm et OB = OD = 3 cm. Est-ce un parallélogramme ? Que valent AC et BD ?",
                "Les deux diagonales ont le même milieu : on applique la réciproque.",
                [("O est le milieu de [AC] et de [BD]", "OA = OC et OB = OD."),
                 ("Les diagonales se coupent en leur milieu", "ABCD est un parallélogramme."),
                 (N("AC = 2 \\times 5") + " = " + N("10") + " et " + N("BD = 2 \\times 3") + " = " + N("6"), "Les diagonales sont les doubles des demi-diagonales.")],
                "Oui, c'est un parallélogramme, avec " + N("AC = 10") + " cm et " + N("BD = 6") + " cm.", "5==5 and 3==3 and 2*5==10 and 2*3==6"),
        example("Exemple 3", "ABCD est un quadrilatère avec AB = DC = 5 cm, mais AD = 3 cm et BC = 4 cm. Est-ce un parallélogramme ?",
                "Dans un parallélogramme, les côtés opposés sont égaux deux à deux : on vérifie les deux paires.",
                [("AB = DC : la première paire de côtés opposés est égale", "Cette paire est compatible avec un parallélogramme."),
                 ("AD = 3 cm et BC = 4 cm : la deuxième paire n'est pas égale", "Dans un parallélogramme, on aurait AD = BC.")],
                "Non, ce n'est pas un parallélogramme.", "5==5 and 3!=4"),
        example("Exemple 4", "ABCD est un parallélogramme. On sait que AB = 8 cm, BC = 5 cm et que la diagonale [AC] mesure 9 cm. Quelle est la longueur OA, O étant le point d'intersection des diagonales ?",
                "O est le milieu de [AC] : OA est la moitié de AC.",
                [(N("OA = AC \\div 2") + " = " + N("9 \\div 2"), "Les diagonales se coupent en leur milieu."),
                 (N("9 \\div 2") + " = " + N("4,5"), "La moitié de 9 est 4,5.")],
                N("OA = 4,5") + " cm.", "d('9')/2==d('4,5')"),
        warning("Une seule paire de côtés égaux ne suffit pas : un quadrilatère peut avoir deux côtés opposés égaux sans être un parallélogramme. "
                "Il faut aussi que ces deux côtés soient parallèles, ou que l'autre paire de côtés soit égale. Et on ne conclut jamais à partir de la seule vue du dessin."),
    ],
    [
        choice("s2-g1", "justifier", "ABCD a AB = DC = 7 cm et AD = BC = 5 cm. Que peut-on affirmer ?", ["ABCD est un parallélogramme", "ABCD n'est pas un parallélogramme", "On ne peut rien affirmer"], 0,
               hints=["Les deux paires de côtés opposés sont égales."], solution=["Ses côtés opposés ont la même longueur deux à deux : c'est un parallélogramme."], wrong={1: "La réciproque s'applique.", 2: "La propriété des côtés opposés permet de conclure."}),
        choice("s2-g2", "justifier", "ABCD a AB = DC = 6 cm, mais AD = 4 cm et BC = 5 cm. Que peut-on affirmer ?", ["ABCD est un parallélogramme", "ABCD n'est pas un parallélogramme", "On ne peut rien affirmer"], 1,
               hints=["Dans un parallélogramme, les deux paires de côtés opposés sont égales."], solution=["Dans un parallélogramme, on aurait AD = BC. Ici AD = 4 cm et BC = 5 cm : ABCD n'est pas un parallélogramme."], wrong={0: "Les côtés AD et BC sont différents.", 2: "La propriété des côtés opposés permet de conclure."}),
        choice("s2-g3", "justifier", "Les diagonales de ABCD se coupent en O avec OA = OC et OB = OD. Que peut-on affirmer ?", ["ABCD est un parallélogramme", "ABCD est un cercle", "ABCD est un triangle"], 0,
               hints=["Les diagonales se coupent en leur milieu."], solution=["Si les diagonales se coupent en leur milieu, le quadrilatère est un parallélogramme."], wrong={1: "ABCD est un quadrilatère.", 2: "ABCD a quatre sommets."}),
        number("s2-g4", "justifier", "Les diagonales d'un quadrilatère ABCD se coupent en O avec OA = OC = 6 cm. Si ABCD est un parallélogramme, quelle est la longueur de la diagonale AC, en cm ?", Fraction(12), units=["cm"],
               hints=["AC = OA + OC."], solution=["AC = 6 + 6 = 12 cm."]),
        number("s2-g5", "justifier", "Combien de paires de côtés opposés un parallélogramme a-t-il ?", Fraction(2),
               hints=["Un quadrilatère a quatre côtés : on les groupe deux par deux."], solution=["Quatre côtés groupés par paires de côtés opposés : 2 paires."]),
    ])

# ----- Section 3: perimeter -----
S3 = Section(
    "perimetre", "Le périmètre d'un parallélogramme", 22, "perimetre",
    "Calculer le périmètre d'un parallélogramme et retrouver un côté à partir du périmètre.",
    [
        para("Pour entourer un terrain en forme de parallélogramme d'une clôture, on calcule son périmètre. Comme les côtés opposés sont égaux, le calcul se simplifie."),
        rule("Périmètre d'un parallélogramme",
             "Si deux côtés consécutifs d'un parallélogramme mesurent a et b, son périmètre est " + N("P = 2 \\times (a + b)") + ". Les deux autres côtés sont égaux aux premiers. "
             "Pour retrouver un côté : " + N("b = P \\div 2 - a") + "."),
        example("Exemple 1", "Un parallélogramme a pour côtés consécutifs 8 cm et 5 cm. Calculer son périmètre.",
                "On additionne deux côtés consécutifs, puis on double.",
                [(N("8 + 5") + " = " + N("13"), "La somme de deux côtés consécutifs."),
                 (N("2 \\times 13") + " = " + N("26"), "On double : les deux autres côtés sont égaux aux premiers.")],
                "Le périmètre est " + N("26") + " cm.", "2*(8+5)==26==8+5+8+5"),
        example("Exemple 2", "Un parallélogramme a pour côtés consécutifs 6,5 cm et 3,5 cm. Calculer son périmètre.",
                "Même formule avec des nombres décimaux.",
                [(N("6,5 + 3,5") + " = " + N("10"), "Somme de deux côtés consécutifs."),
                 (N("2 \\times 10") + " = " + N("20"), "On double.")],
                "Le périmètre est " + N("20") + " cm.", "2*(d('6,5')+d('3,5'))==20"),
        example("Exemple 3", "Un parallélogramme a un périmètre de 30 cm et un côté de 9 cm. Quelle est la longueur du côté consécutif ?",
                "On cherche le demi-périmètre, puis on retire le côté connu.",
                [(N("30 \\div 2") + " = " + N("15"), "Le demi-périmètre est a + b."),
                 (N("15 - 9") + " = " + N("6"), "On retire le côté connu.")],
                "Le côté consécutif mesure " + N("6") + " cm.", "30//2-9==6 and 2*(9+6)==30"),
        example("Exemple 4", "Un champ en forme de parallélogramme a pour côtés 40 m et 25 m. On le clôture avec un grillage à 1 000 F le mètre. Quel est le prix ?",
                "On calcule le périmètre, puis le prix.",
                [(N("2 \\times (40 + 25)") + " = " + N("130"), "Le périmètre est 130 m."),
                 (N("130 \\times 1000") + " = " + N("130000"), "Le prix est 130 000 F.")],
                "Le grillage coûte " + N("130000") + " F.", "2*(40+25)==130 and 130*1000==130000"),
        warning("Le périmètre d'un parallélogramme n'est pas « longueur × largeur » : c'est l'aire d'un rectangle. N'oublie pas de doubler la somme de deux côtés consécutifs, car il y a quatre côtés."),
    ],
    [
        number("s3-g1", "perimetre", "Un parallélogramme a pour côtés consécutifs 9 cm et 4 cm. Quel est son périmètre, en cm ?", Fraction(26), units=["cm"],
               hints=["2 × (a + b)."], solution=["9 + 4 = 13.", "2 × 13 = 26 cm."]),
        number("s3-g2", "perimetre", "Un parallélogramme a pour côtés consécutifs 7,5 cm et 2,5 cm. Quel est son périmètre, en cm ?", Fraction(20), units=["cm"],
               hints=["2 × (a + b)."], solution=["7,5 + 2,5 = 10.", "2 × 10 = 20 cm."]),
        number("s3-g3", "perimetre", "Un parallélogramme a un périmètre de 36 cm et un côté de 11 cm. Quelle est la longueur du côté consécutif, en cm ?", Fraction(7), units=["cm"],
               hints=["Demi-périmètre, puis retire le côté connu."], solution=["36 ÷ 2 = 18.", "18 − 11 = 7 cm."]),
        number("s3-g4", "perimetre", "Un parallélogramme a un périmètre de 50 cm et un côté de 15 cm. Quelle est la longueur du côté consécutif, en cm ?", Fraction(10), units=["cm"],
               hints=["Demi-périmètre, puis retire le côté connu."], solution=["50 ÷ 2 = 25.", "25 − 15 = 10 cm."]),
        number("s3-g5", "perimetre", "Un terrain en forme de parallélogramme a pour côtés 30 m et 20 m. On le clôture avec un grillage à 500 F le mètre. Quel est le prix, en F ?", Fraction(50000), units=["F"],
               hints=["Périmètre d'abord, puis prix."], solution=["2 × (30 + 20) = 100 m.", "100 × 500 = 50 000 F."]),
    ])

# ----- Section 4: area -----
S4 = Section(
    "aire", "L'aire d'un parallélogramme", 24, "aire",
    "Calculer l'aire d'un parallélogramme à partir d'une base et de la hauteur correspondante, retrouver une base ou une hauteur, et relier cette aire à celle d'un triangle.",
    [
        para("Un parallélogramme est un rectangle « penché » : en découpant un triangle d'un côté et en le recollant de l'autre, on obtient un rectangle de même base et de même hauteur, donc de même aire."),
        figure(HEIGHT, "Un parallélogramme ABCD dont la hauteur [DH] est tracée en pointillés, perpendiculaire à la base [AB].", "[DH] est la hauteur correspondant à la base [AB]. La hauteur n'est pas le côté [AD] : elle est perpendiculaire à la base."),
        rule("Aire d'un parallélogramme",
             "L'aire d'un parallélogramme est égale à une base multipliée par la hauteur correspondante : " + N("A = b \\times h") + ". "
             "Une diagonale partage le parallélogramme en deux triangles de même aire : l'aire de chaque triangle est la moitié de celle du parallélogramme."),
        example("Exemple 1", "Un parallélogramme a une base de 9 cm et une hauteur correspondante de 4 cm. Calculer son aire.",
                "On utilise A = b × h.",
                [(N("9 \\times 4") + " = " + N("36"), "Base × hauteur.")],
                "L'aire est " + N("36") + " cm².", "9*4==36"),
        example("Exemple 2", "Un parallélogramme a une aire de 60 cm² et une base de 12 cm. Quelle est la hauteur correspondante ?",
                "On cherche le facteur manquant de b × h = A.",
                [(N("60 \\div 12") + " = " + N("5"), "La hauteur est l'aire divisée par la base.")],
                "La hauteur mesure " + N("5") + " cm.", "60//12==5 and 12*5==60"),
        example("Exemple 3", "Une diagonale partage un parallélogramme d'aire 48 cm² en deux triangles. Quelle est l'aire de chaque triangle ?",
                "Les deux triangles ont la même aire : on prend la moitié.",
                [(N("48 \\div 2") + " = " + N("24"), "Chaque triangle a pour aire 24 cm².")],
                "Chaque triangle a pour aire " + N("24") + " cm².", "48//2==24"),
        example("Exemple 4", "Un champ en forme de parallélogramme a une base de 50 m et une hauteur de 30 m. On sème du maïs avec 2 kg de graines pour 100 m². Combien de kilogrammes faut-il ?",
                "On calcule l'aire, puis la quantité de graines.",
                [(N("50 \\times 30") + " = " + N("1500"), "L'aire est 1 500 m²."),
                 (N("1500 \\div 100") + " = " + N("15"), "1 500 m² font 15 fois 100 m²."),
                 (N("15 \\times 2") + " = " + N("30"), "Il faut 30 kg de graines.")],
                "Il faut " + N("30") + " kg de graines.", "50*30==1500 and 1500//100*2==30"),
        warning("La hauteur d'un parallélogramme n'est pas la longueur du côté penché : c'est la distance perpendiculaire entre deux côtés parallèles. Prendre le côté penché donne une aire trop grande. "
                "Et n'oublie pas la différence avec le triangle : l'aire du parallélogramme se calcule sans diviser par 2."),
    ],
    [
        number("s4-g1", "aire", "Un parallélogramme a une base de 10 cm et une hauteur de 6 cm. Quelle est son aire, en cm² ?", Fraction(60), units=["cm2", "cm²"],
               hints=["A = b × h."], solution=["10 × 6 = 60 cm²."]),
        number("s4-g2", "aire", "Un parallélogramme a une aire de 84 cm² et une hauteur de 7 cm. Quelle est la base correspondante, en cm ?", Fraction(12), units=["cm"],
               hints=["Divise l'aire par la hauteur."], solution=["84 ÷ 7 = 12 cm."]),
        number("s4-g3", "aire", "Un parallélogramme a une aire de 70 cm². Une diagonale le partage en deux triangles. Quelle est l'aire de chaque triangle, en cm² ?", Fraction(35), units=["cm2", "cm²"],
               hints=["Les deux triangles ont la même aire."], solution=["70 ÷ 2 = 35 cm²."]),
        number("s4-g4", "aire", "Un parallélogramme a une base de 8,5 cm et une hauteur de 4 cm. Quelle est son aire, en cm² ?", Fraction(34), units=["cm2", "cm²"],
               hints=["A = b × h."], solution=["8,5 × 4 = 34 cm²."]),
        choice("s4-g5", "aire", "Un parallélogramme et un rectangle ont la même base et la même hauteur. Quelle est la relation entre leurs aires ?", ["Elles sont égales", "L'aire du parallélogramme est la moitié", "L'aire du parallélogramme est le double"], 0,
               hints=["Un parallélogramme est un rectangle penché."], solution=["Les deux ont la même aire : base × hauteur."], wrong={1: "C'est le cas du triangle, pas du parallélogramme.", 2: "Il n'y a aucune raison que le parallélogramme soit plus grand."}),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "definition", "ABCD est un parallélogramme et BC = 6,5 cm. Quelle est la longueur AD, en cm ?", d("6,5"), 1, ["[AD] est le côté opposé à [BC]."], ["AD = BC = 6,5 cm."], units=["cm"]),
    number("p2", "definition", "ABCD est un parallélogramme de diagonales [AC] et [BD], qui se coupent en O. AC = 20 cm. Quelle est la longueur OC, en cm ?", Fraction(10), 1, ["O est le milieu de [AC]."], ["OC = AC ÷ 2 = 10 cm."], units=["cm"]),
    number("p3", "definition", "ABCD est un parallélogramme de diagonales qui se coupent en O. OB = 4,2 cm. Quelle est la longueur BD, en cm ?", d("8,4"), 2, ["BD = 2 × OB."], ["BD = 2 × 4,2 = 8,4 cm."], units=["cm"]),
    number("p4", "definition", "ABCD est un parallélogramme avec AB = 5 cm, BC = 3 cm. Quelle est la longueur DC, en cm ?", Fraction(5), 1, ["[DC] est le côté opposé à [AB]."], ["DC = AB = 5 cm."], units=["cm"]),
    choice("p5", "definition", "Dans le parallélogramme ABCD, quel côté est parallèle à [AB] ?", ["[BC]", "[DC]", "[AC]"], 1, 1, ["Le côté opposé à [AB]."], ["[DC] est opposé à [AB] : (AB) // (DC)."], wrong={0: "[BC] est consécutif à [AB], il coupe (AB) en B.", 2: "[AC] est une diagonale."}),
    choice("p6", "definition", "Dans le parallélogramme ABCD, quel côté est égal à [AD] ?", ["[AB]", "[BC]", "[CD]"], 1, 1, ["Le côté opposé à [AD]."], ["[BC] est opposé à [AD] : AD = BC."], wrong={0: "[AB] est consécutif à [AD].", 2: "[CD] est consécutif à [AD]."}),
    number("p7", "definition", "Les diagonales d'un parallélogramme mesurent 14 cm et 10 cm. Elles se coupent en O. Quelle est la somme OA + OB, en cm ?", Fraction(12), 3, ["OA = AC ÷ 2 et OB = BD ÷ 2."], ["OA = 14 ÷ 2 = 7 cm et OB = 10 ÷ 2 = 5 cm.", "7 + 5 = 12 cm."], units=["cm"]),
    choice("p8", "justifier", "ABCD a AB = DC = 8 cm et AD = BC = 3 cm. Que peut-on affirmer ?", ["ABCD est un parallélogramme", "ABCD n'est pas un parallélogramme", "On ne peut rien affirmer"], 0, 1, ["Côtés opposés égaux deux à deux."], ["Les côtés opposés sont égaux deux à deux : c'est un parallélogramme."], wrong={1: "La réciproque s'applique.", 2: "La propriété permet de conclure."}),
    choice("p9", "justifier", "ABCD a OA = OC = 4 cm et OB = 6 cm, OD = 5 cm (O est le point d'intersection des diagonales). Que peut-on affirmer ?", ["ABCD est un parallélogramme", "ABCD n'est pas un parallélogramme", "On ne peut rien affirmer"], 1, 2, ["Dans un parallélogramme, les deux diagonales se coupent en leur milieu."], ["Dans un parallélogramme, on aurait OB = OD. Ici OB = 6 cm et OD = 5 cm : ABCD n'est pas un parallélogramme."], wrong={0: "OB et OD ne sont pas égaux.", 2: "La propriété des diagonales permet de conclure."}),
    choice("p10", "justifier", "Léa dit : « mon quadrilatère a deux côtés opposés égaux, donc c'est un parallélogramme ». Qu'en penses-tu ?", ["Elle a raison", "Elle a tort : il faut les deux paires de côtés opposés égaux", "Elle a tort : il faut un angle droit"], 1, 2, ["Une seule paire ne suffit pas."], ["Il faut que les deux paires de côtés opposés soient égales (ou une paire égale et parallèle)."], wrong={0: "Une paire ne suffit pas.", 2: "Un parallélogramme n'a pas forcément d'angle droit."}),
    number("p11", "justifier", "ABCD est un parallélogramme de diagonales [AC] et [BD] qui se coupent en O. OA = 3,5 cm. Quelle est la longueur AC, en cm ?", Fraction(7), 1, ["AC = 2 × OA."], ["2 × 3,5 = 7 cm."], units=["cm"]),
    number("p12", "justifier", "Combien de diagonales un parallélogramme a-t-il ?", Fraction(2), 1, ["Elles joignent les sommets opposés."], ["[AC] et [BD] : 2 diagonales."]),
    number("p13", "justifier", "Combien de côtés un parallélogramme a-t-il en tout ?", Fraction(4), 1, ["Un quadrilatère."], ["Un quadrilatère a 4 côtés."]),
    number("p14", "perimetre", "Un parallélogramme a pour côtés consécutifs 12 cm et 7 cm. Quel est son périmètre, en cm ?", Fraction(38), 1, ["2 × (a + b)."], ["12 + 7 = 19.", "2 × 19 = 38 cm."], units=["cm"]),
    number("p15", "perimetre", "Un parallélogramme a pour côtés consécutifs 4,2 cm et 5,3 cm. Quel est son périmètre, en cm ?", d("19"), 2, ["2 × (a + b)."], ["4,2 + 5,3 = 9,5.", "2 × 9,5 = 19 cm."], units=["cm"]),
    number("p16", "perimetre", "Un parallélogramme a un périmètre de 42 cm et un côté de 8 cm. Quelle est la longueur du côté consécutif, en cm ?", Fraction(13), 2, ["Demi-périmètre moins le côté connu."], ["42 ÷ 2 = 21.", "21 − 8 = 13 cm."], units=["cm"]),
    number("p17", "perimetre", "Un parallélogramme a un périmètre de 25 cm et un côté de 6,5 cm. Quelle est la longueur du côté consécutif, en cm ?", Fraction(6), 3, ["Demi-périmètre moins le côté connu."], ["25 ÷ 2 = 12,5.", "12,5 − 6,5 = 6 cm."], units=["cm"]),
    number("p18", "perimetre", "Un champ en forme de parallélogramme a pour côtés 60 m et 45 m. Quelle est la longueur de la clôture pour en faire le tour, en m ?", Fraction(210), 1, ["2 × (60 + 45)."], ["60 + 45 = 105.", "2 × 105 = 210 m."], units=["m"]),
    number("p19", "perimetre", "Un parallélogramme a un périmètre de 64 cm. Ses deux côtés consécutifs sont dans le rapport suivant : l'un est le triple de l'autre. Quelle est la longueur du plus petit, en cm ?", Fraction(8), 3, ["Demi-périmètre = a + 3a = 4a."], ["64 ÷ 2 = 32.", "32 ÷ 4 = 8 cm."], units=["cm"]),
    number("p20", "perimetre", "Un cadre en forme de parallélogramme a pour côtés 80 cm et 50 cm. On colle un ruban qui coûte 20 F le mètre tout autour. Quel est le prix, en F ?", Fraction(52), 3, ["Périmètre en cm, puis en m."], ["2 × (80 + 50) = 260 cm = 2,6 m.", "2,6 × 20 = 52 F."], units=["F"]),
    number("p21", "aire", "Un parallélogramme a une base de 15 cm et une hauteur de 8 cm. Quelle est son aire, en cm² ?", Fraction(120), 1, ["b × h."], ["15 × 8 = 120 cm²."], units=["cm2", "cm²"]),
    number("p22", "aire", "Un parallélogramme a une base de 6,5 cm et une hauteur de 4 cm. Quelle est son aire, en cm² ?", Fraction(26), 2, ["b × h."], ["6,5 × 4 = 26 cm²."], units=["cm2", "cm²"]),
    number("p23", "aire", "Un parallélogramme a une aire de 96 cm² et une base de 12 cm. Quelle est la hauteur correspondante, en cm ?", Fraction(8), 2, ["Divise l'aire par la base."], ["96 ÷ 12 = 8 cm."], units=["cm"]),
    number("p24", "aire", "Un parallélogramme a une aire de 150 cm² et une hauteur de 6 cm. Quelle est la base correspondante, en cm ?", Fraction(25), 2, ["Divise l'aire par la hauteur."], ["150 ÷ 6 = 25 cm."], units=["cm"]),
    number("p25", "aire", "Une diagonale partage un parallélogramme en deux triangles. L'aire d'un triangle est 42 cm². Quelle est l'aire du parallélogramme, en cm² ?", Fraction(84), 2, ["Deux triangles de même aire."], ["2 × 42 = 84 cm²."], units=["cm2", "cm²"]),
    number("p26", "aire", "Un parallélogramme a pour côtés 10 cm et 7 cm. Sa hauteur relative au côté de 10 cm est 5 cm. Quelle est son aire, en cm² ?", Fraction(50), 3, ["La hauteur doit être relative à la base choisie."], ["Base 10 cm et hauteur correspondante 5 cm : 10 × 5 = 50 cm².", "Le côté de 7 cm n'est pas la hauteur."], units=["cm2", "cm²"]),
    number("p27", "aire", "Un champ en forme de parallélogramme a une base de 40 m et une hauteur de 25 m. On le laboure à raison de 200 F le m². Quel est le prix, en F ?", Fraction(200000), 3, ["Aire d'abord, puis prix."], ["40 × 25 = 1 000 m².", "1 000 × 200 = 200 000 F."], units=["F"]),
    choice("p28", "aire", "Karim calcule l'aire d'un parallélogramme de base 10 cm, de côté penché 6 cm et de hauteur 5 cm : « 10 × 6 = 60 cm² ». Quelle est son erreur ?", ["Il a pris le côté penché au lieu de la hauteur", "Il a oublié de diviser par 2", "Il a oublié l'unité"], 0, 3, ["La hauteur est perpendiculaire à la base."], ["La hauteur est 5 cm, pas 6 cm : A = 10 × 5 = 50 cm²."], wrong={1: "Pour un parallélogramme, on ne divise pas par 2.", 2: "L'unité est présente."}),
    number("p29", "aire", "Un triangle et un parallélogramme ont la même base et la même hauteur. Le parallélogramme a une aire de 56 cm². Quelle est l'aire du triangle, en cm² ?", Fraction(28), 2, ["Le triangle est la moitié du parallélogramme."], ["56 ÷ 2 = 28 cm²."], units=["cm2", "cm²"]),
    number("p30", "aire", "Un parallélogramme a une base de 5 m et une hauteur de 3,2 m. Quelle est son aire, en m² ?", Fraction(16), 2, ["b × h."], ["5 × 3,2 = 16 m²."], units=["m2", "m²"]),
    choice("p31", "aire", "Quelle formule donne l'aire d'un parallélogramme ?", [N("b \\times h"), N("b \\times h \\div 2"), N("2 \\times (b + h)")], 0, 1, ["Un parallélogramme est un rectangle penché."], ["A = base × hauteur."], wrong={1: "C'est la formule du triangle.", 2: "C'est le périmètre d'un rectangle."}),
    choice("p32", "justifier", "Dans un parallélogramme, les diagonales se coupent :", ["en leur milieu", "toujours à angle droit", "en trois parties égales"], 0, 1, ["Propriété des diagonales."], ["Les diagonales d'un parallélogramme se coupent en leur milieu."], wrong={1: "À angle droit seulement dans des cas particuliers.", 2: "Elles se coupent en deux parties égales."}),
]

SUMMARY = [
    definition("Le parallélogramme", "Un parallélogramme est un quadrilatère dont les côtés opposés sont parallèles deux à deux. Ses côtés opposés ont la même longueur. Ses diagonales se coupent en leur milieu."),
    rule("Justifier", "ABCD est un parallélogramme si ses côtés opposés sont parallèles deux à deux, ou si ses diagonales se coupent en leur milieu, ou si ses côtés opposés sont égaux deux à deux. Une seule paire de côtés égaux ne suffit pas."),
    rule("Périmètre et aire", "Périmètre : P = 2 × (a + b). Aire : A = base × hauteur correspondante (la hauteur est perpendiculaire à la base). Une diagonale partage le parallélogramme en deux triangles de même aire."),
    para("Les erreurs à éviter : prendre le côté penché pour la hauteur ; diviser par 2 l'aire d'un parallélogramme ; oublier de doubler pour le périmètre ; conclure qu'une figure est un parallélogramme à cause du dessin seul."),
]

CONCEPTS = {
    "definition": ("Définition et propriétés du parallélogramme", "definition"),
    "justifier": ("Montrer qu'un quadrilatère est un parallélogramme", "justifier"),
    "perimetre": ("Périmètre d'un parallélogramme", "perimetre"),
    "aire": ("Aire d'un parallélogramme", "aire"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    cm, cm2 = ["cm"], ["cm2", "cm²"]
    # 1. opposite sides are equal
    x, y = rand_decimal(rng, 3, 15, 1), rand_decimal(rng, 3, 12, 1)
    questions.append(number("a1", "definition", f"ABCD est un parallélogramme avec AB = {show(x)} cm et BC = {show(y)} cm. Quelle est la longueur CD + DA, en cm ?", x + y, 1,
                            ["CD est le côté opposé à AB et DA est le côté opposé à BC."], [f"CD = AB = {show(x)} cm et DA = BC = {show(y)} cm.", f"{show(x)} + {show(y)} = {show(x + y)} cm."], units=cm))
    # 2. half a diagonal
    y = 2 * rng.randint(4, 20)
    questions.append(number("a2", "definition", f"ABCD est un parallélogramme de diagonales [AC] et [BD], qui se coupent en O. AC = {y} cm. Quelle est la longueur OA, en cm ?", Fraction(y // 2), 1,
                            ["O est le milieu de [AC]."], [f"OA = {y} ÷ 2 = {y // 2} cm."], units=cm))
    # 3. a whole diagonal
    z = rand_decimal(rng, 2, 12, 1)
    questions.append(number("a3", "definition", f"ABCD est un parallélogramme de diagonales qui se coupent en O. OB = {show(z)} cm. Quelle est la longueur BD, en cm ?", 2 * z, 2,
                            ["BD = 2 × OB."], [f"BD = 2 × {show(z)} = {show(2 * z)} cm."], units=cm))
    # 4. perimeter
    a, b = rng.randint(4, 20), rng.randint(3, 15)
    questions.append(number("a4", "perimetre", f"Un parallélogramme a pour côtés consécutifs {a} cm et {b} cm. Quel est son périmètre, en cm ?", Fraction(2 * (a + b)), 1,
                            ["2 × (a + b)."], [f"{a} + {b} = {a + b}.", f"2 × {a + b} = {2 * (a + b)} cm."], units=cm))
    # 5. the missing side from the perimeter
    a, b = rng.randint(5, 20), rng.randint(4, 15)
    questions.append(number("a5", "perimetre", f"Un parallélogramme a un périmètre de {2 * (a + b)} cm et un côté de {a} cm. Quelle est la longueur du côté consécutif, en cm ?", Fraction(b), 2,
                            ["Demi-périmètre moins le côté connu."], [f"{2 * (a + b)} ÷ 2 = {a + b}.", f"{a + b} − {a} = {b} cm."], units=cm))
    # 6. area
    base, height = rng.randint(4, 20), rng.randint(3, 14)
    questions.append(number("a6", "aire", f"Un parallélogramme a une base de {base} cm et une hauteur de {height} cm. Quelle est son aire, en cm² ?", Fraction(base * height), 1,
                            ["A = b × h."], [f"{base} × {height} = {base * height} cm²."], units=cm2))
    # 7. the height from the area
    base, height = rng.randint(4, 15), rng.randint(3, 12)
    questions.append(number("a7", "aire", f"Un parallélogramme a une aire de {base * height} cm² et une base de {base} cm. Quelle est la hauteur correspondante, en cm ?", Fraction(height), 2,
                            ["Divise l'aire par la base."], [f"{base * height} ÷ {base} = {height} cm."], units=cm))
    # 8. the base from the area
    base, height = rng.randint(4, 15), rng.randint(3, 12)
    questions.append(number("a8", "aire", f"Un parallélogramme a une aire de {base * height} cm² et une hauteur de {height} cm. Quelle est la base correspondante, en cm ?", Fraction(base), 2,
                            ["Divise l'aire par la hauteur."], [f"{base * height} ÷ {height} = {base} cm."], units=cm))
    # 9. half the area
    area = 2 * rng.randint(10, 90)
    questions.append(number("a9", "aire", f"Une diagonale partage un parallélogramme d'aire {area} cm² en deux triangles de même aire. Quelle est l'aire d'un triangle, en cm² ?", Fraction(area // 2), 2,
                            ["La moitié de l'aire."], [f"{area} ÷ 2 = {area // 2} cm²."], units=cm2))
    # 10. which datum is enough
    good = ["Les deux paires de côtés opposés sont égales", "Les diagonales se coupent en leur milieu"]
    bad = ["Une seule paire de côtés opposés est égale", "Les diagonales ont la même longueur", "Deux côtés consécutifs sont égaux"]
    chosen = [rng.choice(good)] + rng.sample(bad, 2)
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a10", "justifier", "Quelle donnée suffit pour affirmer que le quadrilatère ABCD est un parallélogramme ?", [chosen[i] for i in order], order.index(0), 3,
                            ["Il faut une réciproque d'une propriété du parallélogramme."], ["Seule cette donnée correspond à une réciproque : côtés opposés égaux deux à deux, ou diagonales de même milieu."],
                            wrong={order.index(1): "Une donnée insuffisante : elle ne garantit pas le parallélisme.", order.index(2): "Une donnée insuffisante : elle ne garantit pas le parallélisme."}))
    # 11. the cost of a fence
    a, b, price = rng.randint(20, 60), rng.randint(15, 50), rng.choice([200, 500, 800, 1000])
    questions.append(number("a11", "perimetre", f"Un champ en forme de parallélogramme a pour côtés {a} m et {b} m. On le clôture avec un grillage à {price} F le mètre. Quel est le prix, en F ?", Fraction(2 * (a + b) * price), 3,
                            ["Périmètre d'abord, puis prix."], [f"2 × ({a} + {b}) = {2 * (a + b)} m.", f"{2 * (a + b)} × {price} = {2 * (a + b) * price} F."], units=["F"]))
    # 12. the classic mistake with the height
    base, side, height = rng.randint(6, 15), rng.randint(8, 12), rng.randint(3, 7)
    options = ["Il a pris le côté penché au lieu de la hauteur", "Il a oublié de diviser par 2", "Il a oublié l'unité"]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a12", "aire", f"Karim calcule l'aire d'un parallélogramme de base {base} cm, de côté penché {side} cm et de hauteur {height} cm : « {base} × {side} = {base * side} cm² ». Quelle est son erreur ?", [options[i] for i in order], order.index(0), 3,
                            ["La hauteur est perpendiculaire à la base."], [f"La hauteur est {height} cm, pas {side} cm : A = {base} × {height} = {base * height} cm²."],
                            wrong={order.index(1): "Pour un parallélogramme, on ne divise pas par 2.", order.index(2): "L'unité est présente."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=14, title="Le parallélogramme", language="fr",
    intro="Les motifs d'un pagne, un cadre incliné, un cerf-volant : le parallélogramme est un rectangle penché. "
          "Ce chapitre t'apprend à le reconnaître, à connaître ses propriétés, à montrer qu'une figure en est un, puis à calculer son périmètre et son aire.",
    objectives=["Reconnaître un parallélogramme et connaître ses côtés opposés et ses diagonales.",
                "Utiliser les propriétés des côtés opposés et des diagonales pour calculer des longueurs.",
                "Montrer qu'un quadrilatère est un parallélogramme avec la définition ou une réciproque.",
                "Calculer le périmètre et l'aire d'un parallélogramme, et retrouver un côté, une base ou une hauteur."],
    prerequisites=[{"text": "Connaître les droites parallèles et le milieu d'un segment.", "chapter": "sn-6e-droites-cercles"},
                   {"text": "Calculer le périmètre et l'aire d'un triangle.", "chapter": "sn-6e-triangles"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Fourteenth chapter of the Senegal Sixième course. Its contents follow lesson 6 of the Côte d'Ivoire Sixième programme (the parallelogram, its properties and their converses, perimeter and area), which was read for it, "
                "so it is also offered there, but the programme's own situations are not reproduced. The figures are drawn by the app. Constructing a parallelogram with instruments cannot be done on a screen, so it is not covered. "
                "It has not been checked against the official Senegalese programme.",
)
