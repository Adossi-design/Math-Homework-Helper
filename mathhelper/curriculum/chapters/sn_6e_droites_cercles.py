"""Sixième, Droites, segments, cercles et disques: the eleventh chapter of the Senegal Sixième course, written in French.

The contents follow lessons 1 to 3 of the Côte d'Ivoire Sixième programme (points and lines, segments and midpoints, circles and discs), which were read for this chapter.
Every explanation, example, figure and exercise was written independently, with our own numbers. The figures are drawn from constants by figures.py. Constructions with a ruler,
a set square or a compass are described but cannot be done on a screen, and that is said to the student. Every calculation takes 3,14 for the number pi.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .figures import Figure, figure
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-6e-droites-cercles"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")
PI = Fraction(314, 100)

# ----- Figures -----
ALIGNED = Figure().point("A", 50, 140, -4, 22).point("B", 160, 100, -4, 22).point("C", 270, 60, -4, 22).line("A", "B")
NOT_ALIGNED = Figure().point("A", 50, 140, -4, 22).point("B", 160, 100, -4, 22).point("C", 250, 165, 8, 4).line("A", "B")
RAY = Figure().point("A", 60, 110, -4, 24).point("B", 160, 110, -4, 24).ray("A", "B")
SEGMENT = Figure().point("A", 60, 110, -4, 24).point("B", 260, 110, -4, 24).segment("A", "B")
PARALLEL = (Figure().point("A", 40, 70, 0, -12).point("B", 300, 70, -8, -12).point("C", 40, 145, 0, 22).point("D", 300, 145, -8, 22)
            .line("A", "B").line("C", "D").arrow_mark("A", "B", 1, 0.3).arrow_mark("C", "D", 1, 0.3))
PERPENDICULAR = (Figure().point("A", 40, 130, 0, 22).point("B", 300, 130, -8, 22).point("C", 170, 30, 10, 6).point("D", 170, 190, 10, -2)
                 .point("O", 170, 130, 10, 22).line("A", "B").line("C", "D").right_angle("O", "B", "C"))
CIRCLE = Figure().point("A", 170, 105, -4, 24).point("M", 245, 105, 8, -8).circle("A", 75).segment("A", "M").tick("A", "M", 1)
CHORDS = (Figure().point("A", 170, 105, -4, 24).point("P", 95, 105, -16, 4).point("Q", 245, 105, 8, 4).point("R", 105, 68, -16, -4).point("S", 240, 79, 8, -4)
          .circle("A", 75).segment("P", "Q").segment("R", "S"))
MIDPOINT = Figure().point("A", 50, 120, -4, 24).point("M", 170, 120, -4, 24).point("B", 290, 120, -4, 24).segment("A", "B").tick("A", "M", 1).tick("M", "B", 1)
BISECTOR = (Figure().point("A", 50, 120, -4, 24).point("M", 170, 120, 10, 22).point("B", 290, 120, -4, 24).point("C", 170, 35, 10, 6).point("D", 170, 190, 10, -2)
            .segment("A", "B").line("C", "D").tick("A", "M", 1).tick("M", "B", 1).right_angle("M", "B", "C"))

# ----- Section 1: points, lines, rays and segments -----
S1 = Section(
    "points", "Points, droites, demi-droites et segments", 22, "points",
    "Reconnaître et noter une droite, une demi-droite et un segment, savoir si des points sont alignés, et calculer avec des longueurs de segments.",
    [
        para("Sur une carte, trois villes semblent être sur une même route droite. Pour le vérifier, on trace une ligne droite à la règle entre deux villes et on regarde si la troisième est sur la ligne. "
             "Ce chapitre donne les mots et les notations pour parler de ces figures sans se tromper."),
        definition("Point, droite et points alignés",
                   "Un point se note avec une lettre majuscule : A, B, C. Par deux points distincts A et B, il passe une seule droite, notée " + N("(AB)") + ". "
                   "Une droite n'a ni début ni fin. Des points sont alignés s'ils sont sur une même droite. On écrit " + N("A \\in (AB)") + " pour dire que A appartient à la droite (AB), et " + N("C \\notin (AB)") + " pour dire que C n'y appartient pas."),
        figure(ALIGNED, "Trois points A, B et C placés sur une même droite.", "Les points A, B et C sont alignés : ils sont sur la même droite (AB)."),
        figure(NOT_ALIGNED, "Deux points A et B sur une droite et un point C en dehors de cette droite.", "Le point C n'est pas sur la droite (AB) : A, B et C ne sont pas alignés."),
        definition("Demi-droite",
                   "La demi-droite " + N("[AB)") + " a pour origine A et passe par B. Elle a un début, A, mais pas de fin. Il y a une autre demi-droite d'origine A, qui part dans l'autre sens : c'est " + N("[AB')") + " si B' est un point de l'autre côté."),
        definition("Segment et longueur",
                   "Le segment " + N("[AB]") + " est la partie de la droite (AB) comprise entre A et B, extrémités comprises. Sa longueur se note " + N("AB") + ", sans crochets : " + N("AB = 5") + " cm veut dire que le segment mesure 5 cm. "
                   "Quand un point B est sur le segment [AC], entre A et C, on a " + N("AC = AB + BC") + "."),
        figure(RAY, "Une demi-droite qui part du point A, passe par B et continue.", "La demi-droite [AB) part de A, passe par B et ne s'arrête pas."),
        figure(SEGMENT, "Un segment dont les extrémités sont A et B.", "Le segment [AB] s'arrête en A et en B : on peut le mesurer."),
        example("Exemple 1", "Combien de droites passent par deux points distincts A et B ? Combien par un seul point A ?",
                "On utilise la propriété : par deux points distincts il passe une seule droite.",
                [("Par A et B distincts, il passe une seule droite : (AB)", "Deux points suffisent à fixer la droite."),
                 ("Par le seul point A, on peut tracer autant de droites qu'on veut", "Un point ne fixe pas la direction : il y a une infinité de droites.")],
                "Une seule droite par deux points, et une infinité de droites par un seul point.", "len({frozenset('AB')})==1"),
        example("Exemple 2", "Quatre points A, B, C et D ne sont pas alignés trois à trois. Combien de droites passent par deux d'entre eux ?",
                "On compte les paires de points : chaque paire donne une droite, et une droite ne contient que deux de ces points.",
                [("Paires avec A : AB, AC, AD", "Trois paires."),
                 ("Paires sans A : BC, BD, CD", "Trois autres paires."),
                 (N("3 + 3") + " = " + N("6"), "Il y a 6 droites : (AB), (AC), (AD), (BC), (BD) et (CD).")],
                N("6") + " droites.", "4*3//2==6"),
        example("Exemple 3", "Le point B est sur le segment [AC], entre A et C. On sait que " + N("AB = 5") + " cm et " + N("BC = 3") + " cm. Calculer AC.",
                "B est entre A et C : la longueur totale est la somme des deux morceaux.",
                [(N("AC = AB + BC"), "Propriété des points d'un segment."),
                 (N("AC = 5 + 3") + " = " + N("8"), "On additionne les deux longueurs.")],
                N("AC = 8") + " cm.", "5+3==8"),
        example("Exemple 4", "Les points A, B et C sont alignés, avec B entre A et C. On sait que " + N("AC = 9,5") + " cm et " + N("AB = 4") + " cm. Calculer BC.",
                "On part de AC = AB + BC et on cherche le morceau qui manque.",
                [(N("AC = AB + BC"), "B est entre A et C."),
                 (N("BC = AC - AB") + " = " + N("9,5 - 4"), "On retire AB de AC."),
                 (N("9,5 - 4") + " = " + N("5,5"), "9,5 − 4 = 5,5.")],
                N("BC = 5,5") + " cm.", "d('9,5')-4==d('5,5')"),
        warning("Une droite n'a pas de longueur et on ne peut pas la mesurer : seul un segment se mesure. Et " + N("AC = AB + BC") + " n'est vrai que si B est entre A et C, sur le segment [AC] : "
                "si les points ne sont pas alignés, la distance AC est plus courte que AB + BC."),
    ],
    [
        number("s1-g1", "points", "Combien de droites passent par deux points distincts A et B ?", Fraction(1),
               hints=["Deux points distincts fixent la direction de la droite."], solution=["Par deux points distincts, il passe une seule droite : 1."]),
        number("s1-g2", "points", "Cinq points sont placés de sorte que trois quelconques d'entre eux ne soient jamais alignés. Combien de droites passent par deux de ces points ?", Fraction(10),
               hints=["Compte les paires : 4 paires avec le premier, 3 avec le deuxième, ..."], solution=["4 + 3 + 2 + 1 = 10 paires de points.", "Chaque paire donne une droite : 10 droites."]),
        number("s1-g3", "points", "B est entre A et C, sur le segment [AC]. AB = 7 cm et BC = 4,5 cm. Quelle est la longueur AC, en cm ?", d("11,5"), units=["cm"],
               hints=["AC = AB + BC."], solution=["AC = 7 + 4,5.", "AC = 11,5 cm."]),
        number("s1-g4", "points", "A, B et C sont alignés, avec B entre A et C. AC = 12 cm et AB = 5 cm. Quelle est la longueur BC, en cm ?", Fraction(7), units=["cm"],
               hints=["BC = AC − AB."], solution=["BC = 12 − 5.", "BC = 7 cm."]),
        choice("s1-g5", "points", "Comment note-t-on la demi-droite d'origine A qui passe par B ?", [N("(AB)"), N("[AB]"), N("[AB)")], 2,
               hints=["Un crochet marque une extrémité qui existe, une parenthèse un côté qui continue sans fin."],
               solution=["La demi-droite a une origine, A, donc un crochet du côté de A, et elle continue au-delà de B : [AB)."],
               wrong={0: "(AB) est la droite entière, qui n'a pas d'origine.", 1: "[AB] est le segment, qui s'arrête en B."}),
    ])

# ----- Section 2: secant, perpendicular and parallel lines -----
S2 = Section(
    "paralleles", "Droites sécantes, perpendiculaires et parallèles", 22, "paralleles",
    "Distinguer des droites sécantes, perpendiculaires et parallèles, noter ces positions et utiliser leurs propriétés pour conclure.",
    [
        para("Deux droites tracées sur une feuille se coupent ou ne se coupent jamais. Les rails d'un chemin de fer ne se rejoignent pas, les bords d'une porte se coupent à angle droit : "
             "ce sont les deux situations les plus importantes de la géométrie du collège."),
        definition("Droites sécantes et perpendiculaires",
                   "Deux droites sécantes se coupent en un seul point. Deux droites perpendiculaires sont des droites sécantes qui forment un angle droit, comme les bords d'une feuille. "
                   "On écrit " + N("(d) \\perp (d')") + ". Un petit carré dessiné au point d'intersection marque l'angle droit."),
        figure(PERPENDICULAR, "Deux droites (AB) et (CD) qui se coupent au point O en formant un angle droit.", "Les droites (AB) et (CD) sont perpendiculaires : elles se coupent en O avec un angle droit."),
        definition("Droites parallèles",
                   "Deux droites parallèles ne se coupent jamais : elles gardent toujours le même écartement. On écrit " + N("(d) // (d')") + ". Deux droites confondues sont aussi considérées comme parallèles. "
                   "Sur un dessin, on marque des droites parallèles avec le même nombre de chevrons."),
        figure(PARALLEL, "Deux droites (AB) et (CD) qui ne se coupent pas, avec des chevrons identiques.", "Les droites (AB) et (CD) sont parallèles : (AB) // (CD)."),
        rule("Cinq propriétés",
             "1. Par un point donné, il passe une seule droite parallèle à une droite donnée. 2. Par un point donné, il passe une seule droite perpendiculaire à une droite donnée. "
             "3. Si deux droites sont perpendiculaires à une même droite, alors elles sont parallèles entre elles. 4. Si deux droites sont parallèles et si une troisième est perpendiculaire à l'une, alors elle est perpendiculaire à l'autre. "
             "5. Si deux droites sont parallèles à une même troisième, alors elles sont parallèles entre elles."),
        example("Exemple 1", "On a " + N("(d_1) \\perp (d)") + " et " + N("(d_2) \\perp (d)") + ". Que peut-on dire de (d₁) et (d₂) ?",
                "On cherche une propriété qui parle de deux droites perpendiculaires à une même troisième.",
                [("(d₁) et (d₂) sont toutes les deux perpendiculaires à (d)", "C'est la situation de la propriété 3."),
                 ("Donc (d₁) et (d₂) sont parallèles", "Deux droites perpendiculaires à une même droite sont parallèles.")],
                N("(d_1) // (d_2)") + ".", "90+90==180"),
        example("Exemple 2", "On a " + N("(d_1) // (d_2)") + " et " + N("(d_3) \\perp (d_1)") + ". Que peut-on dire de (d₃) et (d₂) ?",
                "Une droite perpendiculaire à l'une de deux droites parallèles est aussi perpendiculaire à l'autre.",
                [("(d₁) et (d₂) sont parallèles", "Première information."),
                 ("(d₃) est perpendiculaire à (d₁)", "Deuxième information : propriété 4."),
                 ("Donc (d₃) est perpendiculaire à (d₂)", "On l'écrit " + N("(d_3) \\perp (d_2)") + ".")],
                N("(d_3) \\perp (d_2)") + ".", "90==90"),
        example("Exemple 3", "Trois droites sont deux à deux sécantes, et aucun point n'est commun aux trois. Combien de points d'intersection y a-t-il ?",
                "Chaque paire de droites se coupe en un seul point : on compte les paires.",
                [("Les paires de droites : (d₁)(d₂), (d₁)(d₃), (d₂)(d₃)", "Il y a 3 paires."),
                 ("Chaque paire donne un point, tous différents", "Aucun point n'est commun aux trois droites.")],
                N("3") + " points d'intersection.", "3*2//2==3"),
        example("Exemple 4", "Quatre droites sont deux à deux sécantes, et trois quelconques d'entre elles ne passent jamais par le même point. Combien de points d'intersection y a-t-il ?",
                "On compte les paires de droites, comme pour les points de la section 1.",
                [("Paires avec la première droite : 3", "Elle coupe chacune des trois autres."),
                 ("Paires sans la première : 2 + 1 = 3", "Il reste trois droites, donc 3 paires.")],
                N("6") + " points d'intersection.", "4*3//2==6"),
        warning("Deux droites parallèles ne se coupent jamais, mais attention : sur le dessin, on ne voit qu'un morceau des droites. Deux droites peuvent sembler ne pas se couper sur la feuille alors qu'elles se coupent plus loin. "
                "Et on ne peut conclure qu'à partir d'une propriété, pas d'une impression visuelle."),
    ],
    [
        choice("s2-g1", "paralleles", "(d₁) ⟂ (d) et (d₂) ⟂ (d). Que peut-on dire de (d₁) et de (d₂) ?", ["Elles sont parallèles", "Elles sont perpendiculaires", "On ne peut rien dire"], 0,
               hints=["Pense à deux rails perpendiculaires à une même traverse."], solution=["Deux droites perpendiculaires à une même droite sont parallèles entre elles."],
               wrong={1: "Si elles étaient perpendiculaires entre elles, elles formeraient un angle droit, ce qui n'est pas le cas ici.", 2: "La propriété 3 permet de conclure."}),
        choice("s2-g2", "paralleles", "(d₁) // (d₂) et (d₃) ⟂ (d₁). Que peut-on dire de (d₃) et de (d₂) ?", ["Elles sont parallèles", "Elles sont perpendiculaires", "Elles sont confondues"], 1,
               hints=["Une droite perpendiculaire à l'une de deux parallèles est perpendiculaire à l'autre."], solution=["(d₃) est perpendiculaire à (d₁) qui est parallèle à (d₂) : (d₃) est perpendiculaire à (d₂)."],
               wrong={0: "(d₃) coupe (d₁) à angle droit : elle ne peut pas être parallèle à (d₂).", 2: "Rien n'indique que les droites sont confondues."}),
        number("s2-g3", "paralleles", "Cinq droites sont deux à deux sécantes, et trois quelconques d'entre elles ne passent jamais par le même point. Combien de points d'intersection y a-t-il ?", Fraction(10),
               hints=["Compte les paires de droites."], solution=["4 + 3 + 2 + 1 = 10 paires de droites.", "Chaque paire donne un point : 10 points."]),
        choice("s2-g4", "paralleles", "Combien de droites passent par un point A et sont parallèles à une droite (d) donnée ?", ["Aucune", "Une seule", "Une infinité"], 1,
               hints=["Une droite parallèle à (d) passant par A est unique."], solution=["Par un point donné, il passe une seule droite parallèle à une droite donnée."],
               wrong={0: "On peut toujours tracer la parallèle, sauf si A est sur (d), auquel cas c'est (d) elle-même.", 2: "Une seule droite a la même direction que (d) en passant par A."}),
        choice("s2-g5", "paralleles", "Deux droites sécantes qui forment un angle droit sont :", ["parallèles", "perpendiculaires", "confondues"], 1,
               hints=["Pense aux bords d'une feuille de papier."], solution=["Des droites sécantes qui forment un angle droit sont perpendiculaires."],
               wrong={0: "Des droites parallèles ne se coupent pas.", 2: "Des droites confondues sont les mêmes droites : elles ne se coupent pas en un seul point."}),
    ])

# ----- Section 3: circles and discs -----
S3 = Section(
    "cercles", "Le cercle et le disque", 24, "cercles",
    "Nommer les éléments d'un cercle, utiliser la relation entre rayon et diamètre, reconnaître un point d'un cercle par une égalité et calculer un périmètre et une aire.",
    [
        para("Autour d'un mât planté dans la cour, on plante des fleurs toutes à 2 m du pied du mât. Les fleurs dessinent un cercle. Les points de la cour qui sont à 2 m ou moins du mât forment un disque."),
        definition("Cercle et disque",
                   "Le cercle " + N("C(A ; r)") + " de centre A et de rayon r est l'ensemble des points M tels que " + N("AM = r") + ". Le disque " + N("D(A ; r)") + " est le cercle avec toute la surface qu'il entoure, c'est-à-dire les points M tels que " + N("AM \\le r") + ". "
                   "Un point est à l'intérieur du disque si " + N("AM < r") + " et à l'extérieur si " + N("AM > r") + "."),
        figure(CIRCLE, "Un cercle de centre A et un rayon [AM] dont l'extrémité M est sur le cercle.", "Le cercle de centre A : le point M est sur le cercle, donc AM = r. Le segment [AM] est un rayon."),
        definition("Rayon, diamètre et corde",
                   "Un rayon est un segment qui joint le centre à un point du cercle. Un diamètre est un segment qui joint deux points du cercle en passant par le centre : sa longueur est le double du rayon, " + N("d = 2 \\times r") + ". "
                   "Une corde est un segment qui joint deux points du cercle. Le diamètre est la plus longue des cordes."),
        figure(CHORDS, "Un cercle de centre A avec un diamètre [PQ] qui passe par A et une corde [RS] qui n'y passe pas.", "[PQ] est un diamètre, il passe par le centre A. [RS] est une corde qui ne passe pas par le centre : elle est plus courte."),
        rule("Périmètre et aire",
             "Le périmètre d'un cercle de rayon r est " + N("P = 2 \\times \\pi \\times r") + ", soit " + N("P = \\pi \\times d") + ". L'aire d'un disque de rayon r est " + N("A = \\pi \\times r \\times r") + ". "
             "Le nombre " + N("\\pi") + " est le rapport du périmètre à son diamètre, pour tous les cercles : on prend " + N("3,14") + " comme valeur approchée dans ce cours."),
        example("Exemple 1", "Un cercle a pour rayon 5 cm. Quel est son diamètre, son périmètre et l'aire de son disque ? (π = 3,14)",
                "On utilise d = 2 × r, puis P = π × d et A = π × r × r.",
                [(N("d = 2 \\times 5") + " = " + N("10") + " cm", "Le diamètre est le double du rayon."),
                 (N("P = 3,14 \\times 10") + " = " + N("31,4") + " cm", "Le périmètre est π fois le diamètre."),
                 (N("A = 3,14 \\times 5 \\times 5") + " = " + N("78,5") + " cm²", "5 × 5 = 25, puis 3,14 × 25 = 78,5.")],
                "Diamètre " + N("10") + " cm, périmètre " + N("31,4") + " cm, aire " + N("78,5") + " cm².", "2*5==10 and d('3,14')*10==d('31,4') and d('3,14')*5*5==d('78,5')"),
        example("Exemple 2", "Le cercle C(A ; 4 cm) est tracé. M est un point tel que AM = 4 cm, N un point tel que AN = 3 cm et P un point tel que AP = 6 cm. Où sont M, N et P par rapport au cercle ?",
                "On compare chaque distance au centre avec le rayon 4 cm.",
                [("AM = 4 : égal au rayon", "M est sur le cercle."),
                 ("AN = 3 : plus petit que le rayon", "N est à l'intérieur du disque."),
                 ("AP = 6 : plus grand que le rayon", "P est à l'extérieur du disque.")],
                "M est sur le cercle, N à l'intérieur, P à l'extérieur.", "4==4 and 3<4 and 6>4"),
        example("Exemple 3", "Le périmètre d'un cercle est 31,4 cm. Quel est son diamètre, puis son rayon ? (π = 3,14)",
                "On utilise P = π × d : on cherche le diamètre, puis on prend la moitié.",
                [(N("d = 31,4 \\div 3,14") + " = " + N("10"), "On divise le périmètre par π : 31,4 ÷ 3,14 se lit 3 140 ÷ 314 = 10."),
                 (N("r = 10 \\div 2") + " = " + N("5"), "Le rayon est la moitié du diamètre.")],
                "Diamètre " + N("10") + " cm, rayon " + N("5") + " cm.", "d('31,4')/d('3,14')==10 and 10/2==5"),
        example("Exemple 4", "Un jardin rond a un diamètre de 8 m. Quelle longueur de grillage faut-il pour l'entourer ? (π = 3,14)",
                "Le grillage entoure le jardin : c'est le périmètre du cercle.",
                [(N("P = 3,14 \\times 8") + " = " + N("25,12"), "On connaît le diamètre : P = π × d."),
                 ("314 × 8 = 2 512, avec 2 chiffres après la virgule", "Donc 25,12.")],
                "Il faut environ " + N("25,12") + " m de grillage.", "d('3,14')*8==d('25,12')"),
        warning("Le rayon est la moitié du diamètre : un cercle de diamètre 10 cm a un rayon de 5 cm. Et le périmètre se mesure en cm, l'aire en cm² : un cercle est une ligne, un disque est une surface. "
                "Enfin, un diamètre est une corde, mais une corde n'est un diamètre que si elle passe par le centre."),
    ],
    [
        number("s3-g1", "cercles", "Un cercle a un rayon de 7 cm. Quelle est la longueur de son diamètre, en cm ?", Fraction(14), units=["cm"],
               hints=["Le diamètre est le double du rayon."], solution=["d = 2 × 7 = 14 cm."]),
        number("s3-g2", "cercles", "Quel est le périmètre d'un cercle de rayon 3 cm, en cm ? (π = 3,14)", d("18,84"), units=["cm"],
               hints=["P = 2 × π × r."], solution=["P = 2 × 3,14 × 3.", "6,28 × 3 = 18,84 cm."]),
        number("s3-g3", "cercles", "Quelle est l'aire d'un disque de rayon 4 cm, en cm² ? (π = 3,14)", d("50,24"), units=["cm2", "cm²"],
               hints=["A = π × r × r."], solution=["4 × 4 = 16.", "3,14 × 16 = 50,24 cm²."]),
        choice("s3-g4", "cercles", "Le cercle a pour centre A et pour rayon 5 cm. On a AM = 5 cm. Où est le point M ?", ["Sur le cercle", "À l'intérieur du disque", "À l'extérieur du disque"], 0,
               hints=["Compare AM au rayon."], solution=["AM = r : M est sur le cercle."],
               wrong={1: "À l'intérieur, on aurait AM < 5 cm.", 2: "À l'extérieur, on aurait AM > 5 cm."}),
        choice("s3-g5", "cercles", "Quelle est la plus longue corde d'un cercle ?", ["Le diamètre", "Le rayon", "Toutes les cordes sont égales"], 0,
               hints=["Une corde qui passe par le centre est particulière."], solution=["Le diamètre, qui passe par le centre, est la plus longue des cordes."],
               wrong={1: "Le rayon n'est pas une corde : il joint le centre à un point du cercle.", 2: "Une corde qui est près du bord est plus courte que le diamètre."}),
    ])

# ----- Section 4: midpoint and comparing lengths -----
S4 = Section(
    "milieu", "Milieu d'un segment, médiatrice et comparaison de longueurs", 22, "milieu",
    "Reconnaître le milieu d'un segment, calculer avec les moitiés, comparer et reporter des longueurs, et connaître la médiatrice.",
    [
        para("Pour planter des fleurs à égale distance de deux cocotiers, il faut trouver le milieu du segment qui les relie, puis tous les points qui sont à égale distance des deux. "
             "Ce sont deux idées très utiles : le milieu et la médiatrice."),
        definition("Milieu d'un segment",
                   "Le milieu du segment [AB] est le point M du segment qui est à la même distance de A et de B : " + N("AM = MB") + ". On a alors " + N("AM = MB = AB \\div 2") + " et " + N("AB = 2 \\times AM") + ". "
                   "Sur un dessin, on marque deux segments de même longueur avec le même nombre de petits traits."),
        figure(MIDPOINT, "Un segment [AB] avec son milieu M et deux petits traits identiques sur [AM] et [MB].", "M est le milieu de [AB] : AM = MB. Les traits identiques indiquent des longueurs égales."),
        definition("Médiatrice d'un segment",
                   "La médiatrice d'un segment [AB] est la droite perpendiculaire à [AB] qui passe par son milieu. Tous les points de la médiatrice sont à la même distance de A et de B."),
        figure(BISECTOR, "Un segment [AB] avec son milieu M et une droite (CD) qui passe par M à angle droit.", "La droite (CD) est la médiatrice de [AB] : elle est perpendiculaire à [AB] en son milieu M."),
        example("Exemple 1", "M est le milieu de [AB] et AB = 9 cm. Calculer AM.",
                "Le milieu partage le segment en deux parties égales : on prend la moitié.",
                [(N("AM = AB \\div 2"), "M est le milieu de [AB]."),
                 (N("AM = 9 \\div 2") + " = " + N("4,5"), "La moitié de 9 est 4,5.")],
                N("AM = 4,5") + " cm.", "d('9')/2==d('4,5')"),
        example("Exemple 2", "M est le milieu de [AB] et AM = 6,5 cm. Calculer AB.",
                "AB est le double de AM, puisque AB = AM + MB et AM = MB.",
                [(N("AB = 2 \\times AM"), "Les deux moitiés sont égales."),
                 (N("AB = 2 \\times 6,5") + " = " + N("13"), "Le double de 6,5 est 13.")],
                N("AB = 13") + " cm.", "2*d('6,5')==13"),
        example("Exemple 3", "M est le milieu de [AB] et N est le milieu de [AM]. Sachant que AB = 12 cm, calculer AN.",
                "On prend la moitié deux fois.",
                [(N("AM = 12 \\div 2") + " = " + N("6"), "M est le milieu de [AB]."),
                 (N("AN = 6 \\div 2") + " = " + N("3"), "N est le milieu de [AM].")],
                N("AN = 3") + " cm, c'est le quart de AB.", "12/2==6 and 6/2==3 and 12/4==3"),
        example("Exemple 4", "On règle un compas sur 2,5 cm et on le reporte 4 fois, bout à bout, sur une droite à partir d'un point A. Quelle distance sépare le premier point A du dernier point marqué ?",
                "Chaque report ajoute 2,5 cm à la distance parcourue.",
                [(N("4 \\times 2,5") + " = " + N("10"), "4 reports de 2,5 cm font 10 cm."),
                 ("Le dernier point est à 10 cm de A", "Les reports se suivent sur la même droite, sans trou ni chevauchement.")],
                "10 cm.", "4*d('2,5')==10"),
        warning("Le milieu d'un segment est sur le segment, alors que la médiatrice est une droite, qui n'a ni début ni fin. Et « à égale distance de A et de B » ne veut pas dire « sur [AB] » : "
                "tous les points de la médiatrice sont à égale distance de A et de B, mais seul le milieu est aussi sur le segment."),
    ],
    [
        number("s4-g1", "milieu", "M est le milieu de [AB] et AB = 14 cm. Quelle est la longueur AM, en cm ?", Fraction(7), units=["cm"],
               hints=["AM est la moitié de AB."], solution=["AM = 14 ÷ 2 = 7 cm."]),
        number("s4-g2", "milieu", "M est le milieu de [AB] et AM = 3,2 cm. Quelle est la longueur AB, en cm ?", d("6,4"), units=["cm"],
               hints=["AB est le double de AM."], solution=["AB = 2 × 3,2 = 6,4 cm."]),
        number("s4-g3", "milieu", "M est le milieu de [AB] et N est le milieu de [AM]. AB = 20 cm. Quelle est la longueur AN, en cm ?", Fraction(5), units=["cm"],
               hints=["Prends la moitié deux fois."], solution=["AM = 20 ÷ 2 = 10 cm.", "AN = 10 ÷ 2 = 5 cm."]),
        number("s4-g4", "milieu", "On reporte 6 fois, bout à bout sur une droite, une longueur de 1,5 cm. Quelle distance sépare le premier et le dernier point, en cm ?", Fraction(9), units=["cm"],
               hints=["Multiplie le nombre de reports par la longueur reportée."], solution=["6 × 1,5 = 9 cm."]),
        choice("s4-g5", "milieu", "Quelle est la médiatrice du segment [AB] ?", ["La droite parallèle à (AB) qui passe par A", "La droite perpendiculaire à [AB] qui passe par son milieu", "Le segment qui relie A au milieu de [AB]"], 1,
               hints=["Elle fait deux choses : être perpendiculaire et passer par le milieu."], solution=["La médiatrice est la droite perpendiculaire à [AB] qui passe par son milieu."],
               wrong={0: "Une parallèle ne coupe pas (AB).", 2: "Ce segment est une moitié de [AB], pas une droite perpendiculaire."}),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "points", "Combien de droites passent par trois points alignés A, B et C ?", Fraction(1), 1, ["Si les trois points sont sur la même droite, il n'y en a qu'une."], ["A, B et C sont alignés : une seule droite les contient."]),
    number("p2", "points", "Quatre points sont placés de sorte que trois quelconques d'entre eux ne soient jamais alignés. Combien de droites passent par deux de ces points ?", Fraction(6), 2, ["Compte les paires."], ["3 + 2 + 1 = 6 paires, donc 6 droites."]),
    number("p3", "points", "Six points sont placés de sorte que trois quelconques d'entre eux ne soient jamais alignés. Combien de droites passent par deux de ces points ?", Fraction(15), 3, ["Combien de paires avec chaque point ?"], ["5 + 4 + 3 + 2 + 1 = 15 paires.", "15 droites."]),
    number("p4", "points", "B est entre A et C. AB = 8,5 cm et BC = 6,3 cm. Quelle est la longueur AC, en cm ?", d("14,8"), 1, ["AC = AB + BC."], ["8,5 + 6,3 = 14,8 cm."], units=["cm"]),
    number("p5", "points", "B est entre A et C. AC = 15 cm et BC = 6 cm. Quelle est la longueur AB, en cm ?", Fraction(9), 1, ["AB = AC − BC."], ["15 − 6 = 9 cm."], units=["cm"]),
    number("p6", "points", "A, B et C sont alignés, B entre A et C. AB = 2,8 cm et BC = 5 cm. Quelle est la longueur AC, en cm ?", d("7,8"), 2, ["AC = AB + BC."], ["2,8 + 5 = 7,8 cm."], units=["cm"]),
    choice("p7", "points", "Comment note-t-on le segment d'extrémités A et B ?", [N("(AB)"), N("[AB]"), N("[AB)")], 1, 1, ["Un segment a deux extrémités : deux crochets."], ["Le segment s'écrit [AB]."], wrong={0: "(AB) est la droite, qui ne s'arrête pas.", 2: "[AB) est une demi-droite."}),
    choice("p8", "points", "Comment note-t-on la droite qui passe par les points A et B ?", [N("[AB]"), N("(AB)"), N("[AB)")], 1, 1, ["Une droite n'a pas d'extrémités."], ["La droite s'écrit (AB) : des parenthèses car elle ne s'arrête d'aucun côté."], wrong={0: "[AB] est un segment, qui s'arrête en A et en B.", 2: "[AB) est une demi-droite."}),
    choice("p9", "points", "A, B et C sont trois points. On sait que AB + BC = AC. Que peut-on dire de B ?", ["B est sur le segment [AC]", "B est sur le cercle de centre A", "B est le milieu de [AC]"], 0, 3, ["Quand B est entre A et C, la longueur AC est la somme AB + BC."], ["Si AB + BC = AC, le chemin de A à C en passant par B n'est pas plus long : B est sur le segment [AC]."], wrong={1: "Rien ne dit que B est à la même distance de A que d'un rayon.", 2: "B peut être n'importe où sur [AC], pas forcément au milieu."}),
    choice("p10", "paralleles", "(d₁) // (d₂) et (d₂) // (d₃). Que peut-on dire de (d₁) et (d₃) ?", ["Elles sont parallèles", "Elles sont perpendiculaires", "Elles sont sécantes"], 0, 2, ["Deux droites parallèles à une même troisième sont parallèles entre elles."], ["(d₁) et (d₃) sont toutes les deux parallèles à (d₂) : elles sont parallèles."], wrong={1: "Rien n'indique un angle droit.", 2: "Des droites parallèles ne se coupent pas."}),
    choice("p11", "paralleles", "(d₁) ⟂ (d₂) et (d₂) // (d₃). Que peut-on dire de (d₁) et (d₃) ?", ["Elles sont parallèles", "Elles sont perpendiculaires", "On ne peut rien dire"], 1, 2, ["Une droite perpendiculaire à l'une de deux parallèles l'est à l'autre."], ["(d₁) est perpendiculaire à (d₂) qui est parallèle à (d₃) : (d₁) ⟂ (d₃)."], wrong={0: "(d₁) coupe (d₂) à angle droit : elle coupe aussi (d₃).", 2: "La propriété 4 permet de conclure."}),
    number("p12", "paralleles", "Six droites sont deux à deux sécantes, et trois quelconques d'entre elles ne passent jamais par le même point. Combien de points d'intersection y a-t-il ?", Fraction(15), 3, ["Compte les paires de droites."], ["5 + 4 + 3 + 2 + 1 = 15 paires de droites.", "15 points."]),
    number("p13", "paralleles", "Trois droites sont deux à deux parallèles. Combien de points d'intersection ont-elles, deux à deux ?", Fraction(0), 1, ["Des droites parallèles ne se coupent pas."], ["Aucune paire ne se coupe : 0 point."]),
    choice("p14", "paralleles", "Par un point A qui n'est pas sur la droite (d), combien de droites passent par A et sont perpendiculaires à (d) ?", ["Une seule", "Aucune", "Une infinité"], 0, 2, ["La perpendiculaire est unique."], ["Par un point donné, il passe une seule droite perpendiculaire à une droite donnée."], wrong={1: "On peut toujours la tracer avec une équerre.", 2: "Une seule direction fait un angle droit avec (d)."}),
    choice("p15", "paralleles", "Lisa dit : « sur mon dessin, (d₁) et (d₂) ne se coupent pas, donc elles sont parallèles ». Que penses-tu ?", ["Elle a raison : un dessin suffit", "Il faut une propriété ou une donnée : les droites peuvent se couper plus loin que la feuille", "Elle a tort : elles sont perpendiculaires"], 1, 3, ["Un dessin n'est qu'un morceau des droites."], ["Deux droites peuvent se couper en dehors de la feuille : on ne peut conclure que d'après une propriété ou une donnée."], wrong={0: "Un dessin ne prouve rien tout seul.", 2: "Rien n'indique un angle droit."}),
    number("p16", "cercles", "Un cercle a un diamètre de 18 cm. Quel est son rayon, en cm ?", Fraction(9), 1, ["Le rayon est la moitié du diamètre."], ["18 ÷ 2 = 9 cm."], units=["cm"]),
    number("p17", "cercles", "Quel est le périmètre d'un cercle de diamètre 10 cm, en cm ? (π = 3,14)", d("31,4"), 1, ["P = π × d."], ["3,14 × 10 = 31,4 cm."], units=["cm"]),
    number("p18", "cercles", "Quel est le périmètre d'un cercle de rayon 7 cm, en cm ? (π = 3,14)", d("43,96"), 2, ["P = 2 × π × r."], ["2 × 3,14 = 6,28.", "6,28 × 7 = 43,96 cm."], units=["cm"]),
    number("p19", "cercles", "Quelle est l'aire d'un disque de rayon 10 cm, en cm² ? (π = 3,14)", Fraction(314), 2, ["A = π × r × r."], ["10 × 10 = 100.", "3,14 × 100 = 314 cm²."], units=["cm2", "cm²"]),
    number("p20", "cercles", "Quelle est l'aire d'un disque de diamètre 12 cm, en cm² ? (π = 3,14)", d("113,04"), 3, ["Cherche d'abord le rayon."], ["r = 12 ÷ 2 = 6 cm.", "6 × 6 = 36.", "3,14 × 36 = 113,04 cm²."], units=["cm2", "cm²"]),
    number("p21", "cercles", "Le périmètre d'un cercle est 62,8 cm. Quel est son diamètre, en cm ? (π = 3,14)", Fraction(20), 3, ["d = P ÷ π."], ["62,8 ÷ 3,14 = 20 cm."], units=["cm"]),
    number("p22", "cercles", "Le périmètre d'un cercle est 37,68 cm. Quel est son rayon, en cm ? (π = 3,14)", Fraction(6), 3, ["Cherche le diamètre, puis la moitié."], ["37,68 ÷ 3,14 = 12 cm de diamètre.", "12 ÷ 2 = 6 cm de rayon."], units=["cm"]),
    choice("p23", "cercles", "Le cercle a pour centre O et pour rayon 6 cm. On a OM = 4,5 cm. Où est le point M ?", ["Sur le cercle", "À l'intérieur du disque", "À l'extérieur du disque"], 1, 1, ["Compare OM au rayon."], ["OM = 4,5 est plus petit que 6 : M est à l'intérieur du disque."], wrong={0: "Sur le cercle, on aurait OM = 6 cm.", 2: "À l'extérieur, on aurait OM > 6 cm."}),
    choice("p24", "cercles", "Le cercle a pour centre O et pour rayon 6 cm. On a OM = 8 cm. Où est le point M ?", ["Sur le cercle", "À l'intérieur du disque", "À l'extérieur du disque"], 2, 1, ["Compare OM au rayon."], ["OM = 8 est plus grand que 6 : M est à l'extérieur du disque."], wrong={0: "Sur le cercle, on aurait OM = 6 cm.", 1: "À l'intérieur, on aurait OM < 6 cm."}),
    choice("p25", "cercles", "[AB] est un segment qui joint deux points d'un cercle. Quand est-il un diamètre ?", ["Quand il passe par le centre", "Toujours", "Quand il est plus court que le rayon"], 0, 2, ["Pense à la définition du diamètre."], ["Un diamètre est une corde qui passe par le centre."], wrong={1: "Une corde qui ne passe pas par le centre n'est pas un diamètre.", 2: "Un diamètre est la plus longue corde, plus long que le rayon."}),
    number("p26", "cercles", "Un tourniquet rond a un diamètre de 4 m. Quel est son périmètre, en m ? (π = 3,14)", d("12,56"), 2, ["P = π × d."], ["3,14 × 4 = 12,56 m."], units=["m"]),
    number("p27", "cercles", "Une roue de rayon 30 cm fait un tour complet. Quelle distance parcourt-elle, en cm ? (π = 3,14)", d("188,4"), 3, ["Un tour de roue, c'est son périmètre."], ["P = 2 × 3,14 × 30 = 6,28 × 30.", "6,28 × 30 = 188,4 cm."], units=["cm"]),
    number("p28", "milieu", "M est le milieu de [AB] et AB = 7 cm. Quelle est la longueur AM, en cm ?", d("3,5"), 1, ["AM est la moitié de AB."], ["7 ÷ 2 = 3,5 cm."], units=["cm"]),
    number("p29", "milieu", "M est le milieu de [AB] et AM = 4,8 cm. Quelle est la longueur AB, en cm ?", d("9,6"), 1, ["AB est le double de AM."], ["2 × 4,8 = 9,6 cm."], units=["cm"]),
    number("p30", "milieu", "M est le milieu de [AB], N est le milieu de [AM] et AN = 2,5 cm. Quelle est la longueur AB, en cm ?", Fraction(10), 3, ["AM = 2 × AN, puis AB = 2 × AM."], ["AM = 2 × 2,5 = 5 cm.", "AB = 2 × 5 = 10 cm."], units=["cm"]),
    number("p31", "milieu", "On reporte 8 fois, bout à bout sur une droite, une longueur de 1,25 cm. Quelle distance sépare le premier et le dernier point, en cm ?", Fraction(10), 2, ["8 × 1,25."], ["8 × 1,25 = 10 cm."], units=["cm"]),
    choice("p32", "milieu", "M est le milieu de [AB]. Laquelle de ces égalités est vraie ?", [N("AM = MB"), N("AM = AB"), N("AM = 2 \\times AB")], 0, 1, ["Le milieu partage le segment en deux parties égales."], ["Au milieu, AM = MB, et AM est la moitié de AB."], wrong={1: "AM est la moitié de AB, pas AB tout entier.", 2: "AM est la moitié de AB, pas son double."}),
    choice("p33", "milieu", "Quel est le point de la médiatrice de [AB] qui est aussi sur le segment [AB] ?", ["Le milieu de [AB]", "L'extrémité A", "Il n'y en a pas"], 0, 2, ["La médiatrice coupe [AB] en un point particulier."], ["La médiatrice passe par le milieu de [AB] : c'est son seul point sur le segment."], wrong={1: "A n'est pas à égale distance de A et de B.", 2: "La médiatrice passe par le milieu de [AB]."}),
]

SUMMARY = [
    definition("Points, droites et segments", "Par deux points distincts passe une seule droite (AB). Des points sont alignés s'ils sont sur une même droite. [AB) est la demi-droite d'origine A qui passe par B, [AB] le segment, AB sa longueur. Si B est sur [AC], AC = AB + BC."),
    rule("Positions de deux droites", "Sécantes : un point commun. Perpendiculaires : sécantes avec un angle droit. Parallèles : aucun point commun. Deux droites perpendiculaires à une même droite sont parallèles ; une perpendiculaire à l'une de deux parallèles l'est à l'autre ; deux parallèles à une même droite sont parallèles."),
    rule("Le cercle", "C(A ; r) est l'ensemble des points M tels que AM = r. Diamètre = 2 × rayon. Périmètre = 2 × π × r = π × d, aire du disque = π × r × r, avec π ≈ 3,14. AM < r : M est à l'intérieur du disque ; AM > r : à l'extérieur."),
    rule("Milieu et médiatrice", "Le milieu M de [AB] vérifie AM = MB = AB ÷ 2. La médiatrice de [AB] est la droite perpendiculaire à [AB] qui passe par son milieu."),
    para("Les erreurs à éviter : mesurer une droite ; écrire AC = AB + BC sans que B soit entre A et C ; confondre rayon et diamètre ; confondre périmètre et aire ; conclure à partir d'un dessin seul."),
]

CONCEPTS = {
    "points": ("Points, droites, demi-droites, segments", "points"),
    "paralleles": ("Droites sécantes, perpendiculaires, parallèles", "paralleles"),
    "cercles": ("Cercle et disque", "cercles"),
    "milieu": ("Milieu, médiatrice, comparaison de longueurs", "milieu"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    cm, cm2 = ["cm"], ["cm2", "cm²"]
    # 1. AC = AB + BC
    x, y = rand_decimal(rng, 2, 14, 1), rand_decimal(rng, 2, 9, 1)
    questions.append(number("a1", "points", f"B est entre A et C, sur le segment [AC]. AB = {show(x)} cm et BC = {show(y)} cm. Quelle est la longueur AC, en cm ?", x + y, 1,
                            ["AC = AB + BC."], [f"AC = {show(x)} + {show(y)} = {show(x + y)} cm."], units=cm))
    # 2. BC = AC - AB
    ab = rng.randint(3, 12)
    total = ab + rng.randint(2, 11)
    questions.append(number("a2", "points", f"A, B et C sont alignés, B est entre A et C. AC = {total} cm et AB = {ab} cm. Quelle est la longueur BC, en cm ?", Fraction(total - ab), 1,
                            ["BC = AC − AB."], [f"BC = {total} − {ab} = {total - ab} cm."], units=cm))
    # 3. lines through points
    n = rng.randint(4, 8)
    questions.append(number("a3", "points", f"{n} points sont placés de sorte que trois quelconques d'entre eux ne soient jamais alignés. Combien de droites passent par deux de ces points ?", Fraction(n * (n - 1) // 2), 2,
                            ["Compte les paires de points."], [f"Chaque point forme une paire avec les {n - 1} autres, et chaque paire est comptée deux fois : {n} × {n - 1} ÷ 2 = {n * (n - 1) // 2}."]))
    # 4. a property of parallels and perpendiculars
    if rng.random() < 0.5:
        prompt, good, wrong = "(d₁) ⟂ (d) et (d₂) ⟂ (d). Que peut-on dire de (d₁) et de (d₂) ?", "Elles sont parallèles", ["Elles sont perpendiculaires", "Elles sont confondues"]
        why = "Deux droites perpendiculaires à une même droite sont parallèles entre elles."
    else:
        prompt, good, wrong = "(d₁) // (d₂) et (d₃) ⟂ (d₁). Que peut-on dire de (d₃) et de (d₂) ?", "Elles sont perpendiculaires", ["Elles sont parallèles", "Elles sont confondues"]
        why = "Une droite perpendiculaire à l'une de deux parallèles est perpendiculaire à l'autre."
    options = [good] + wrong
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a4", "paralleles", prompt, [options[i] for i in order], order.index(0), 2, ["Utilise une des propriétés sur les parallèles et les perpendiculaires."], [why],
                            wrong={order.index(1): "Cette position ne découle pas de ces deux données.", order.index(2): "Rien n'indique que les droites sont les mêmes."}))
    # 5. intersection points
    n = rng.randint(3, 9)
    questions.append(number("a5", "paralleles", f"{n} droites sont deux à deux sécantes, et trois quelconques d'entre elles ne passent jamais par le même point. Combien de points d'intersection y a-t-il ?", Fraction(n * (n - 1) // 2), 3,
                            ["Compte les paires de droites."], [f"{n} × {n - 1} ÷ 2 = {n * (n - 1) // 2} paires de droites, donc autant de points."]))
    # 6. perimeter from the diameter
    diameter = rng.randint(3, 25)
    questions.append(number("a6", "cercles", f"Un cercle a un diamètre de {diameter} cm. Quel est son périmètre, en cm ? (π = 3,14)", PI * diameter, 1,
                            ["P = π × d."], [f"3,14 × {diameter} = {show(PI * diameter)} cm."], units=cm))
    # 7. area from the radius
    radius = rng.randint(2, 14)
    questions.append(number("a7", "cercles", f"Quelle est l'aire d'un disque de rayon {radius} cm, en cm² ? (π = 3,14)", PI * radius * radius, 2,
                            ["A = π × r × r."], [f"{radius} × {radius} = {radius * radius}.", f"3,14 × {radius * radius} = {show(PI * radius * radius)} cm²."], units=cm2))
    # 8. radius from the perimeter
    radius = rng.randint(3, 20)
    perimeter = 2 * PI * radius
    questions.append(number("a8", "cercles", f"Le périmètre d'un cercle est {show(perimeter)} cm. Quel est son rayon, en cm ? (π = 3,14)", Fraction(radius), 3,
                            ["Divise le périmètre par π pour avoir le diamètre."], [f"{show(perimeter)} ÷ 3,14 = {2 * radius} cm de diamètre.", f"{2 * radius} ÷ 2 = {radius} cm de rayon."], units=cm))
    # 9. position of a point
    radius = rng.randint(3, 9)
    kind = rng.choice(["on", "in", "out"])
    distance = {"on": radius, "in": radius - rng.randint(1, 2), "out": radius + rng.randint(1, 3)}[kind]
    options = ["Sur le cercle", "À l'intérieur du disque", "À l'extérieur du disque"]
    index = {"on": 0, "in": 1, "out": 2}[kind]
    questions.append(choice("a9", "cercles", f"Le cercle a pour centre O et pour rayon {radius} cm. On a OM = {distance} cm. Où est le point M ?", options, index, 2,
                            ["Compare OM au rayon."], [f"OM = {distance} et r = {radius} : " + ["M est sur le cercle.", "M est à l'intérieur du disque.", "M est à l'extérieur du disque."][index]]))
    # 10. half of a segment
    length = rng.choice([x for x in range(5, 41) if x != 14 and x != 7])
    questions.append(number("a10", "milieu", f"M est le milieu de [AB] et AB = {length} cm. Quelle est la longueur AM, en cm ?", Fraction(length, 2), 1,
                            ["AM est la moitié de AB."], [f"AM = {length} ÷ 2 = {show(Fraction(length, 2))} cm."], units=cm))
    # 11. double of a segment
    half = rand_decimal(rng, 2, 15, 1)
    questions.append(number("a11", "milieu", f"M est le milieu de [AB] et AM = {show(half)} cm. Quelle est la longueur AB, en cm ?", 2 * half, 2,
                            ["AB est le double de AM."], [f"AB = 2 × {show(half)} = {show(2 * half)} cm."], units=cm))
    # 12. half of a half
    quarter = rng.randint(3, 12)
    total = 4 * quarter
    questions.append(number("a12", "milieu", f"M est le milieu de [AB] et N le milieu de [AM]. AB = {total} cm. Quelle est la longueur AN, en cm ?", Fraction(quarter), 3,
                            ["Prends la moitié deux fois."], [f"AM = {total} ÷ 2 = {total // 2} cm.", f"AN = {total // 2} ÷ 2 = {quarter} cm."], units=cm))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=11, title="Droites, segments, cercles et disques", language="fr",
    intro="Une route droite entre trois villes, les rails d'un chemin de fer, les fleurs plantées en rond autour d'un mât : ces situations utilisent des droites, des segments et des cercles. "
          "Ce chapitre t'apprend à les nommer, à les noter, à reconnaître leurs positions et à calculer avec leurs longueurs.",
    objectives=["Nommer et noter un point, une droite, une demi-droite et un segment, et reconnaître des points alignés.",
                "Calculer avec des longueurs de segments : AC = AB + BC et le milieu d'un segment.",
                "Reconnaître des droites sécantes, perpendiculaires et parallèles et utiliser leurs propriétés.",
                "Nommer les éléments d'un cercle, reconnaître un point d'un cercle par AM = r, et calculer un périmètre et une aire.",
                "Connaître la médiatrice d'un segment."],
    prerequisites=[{"text": "Mesurer une longueur avec une règle graduée et connaître le centimètre et le mètre."},
                   {"text": "Multiplier et diviser des nombres décimaux.", "chapter": "sn-6e-division"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Eleventh chapter of the Senegal Sixième course. Its contents follow lessons 1 to 3 of the Côte d'Ivoire Sixième programme (points and lines, segments and midpoints, circles and discs), which were read for it, "
                "so it is also offered there, but the programme's own situations are not reproduced. The figures are drawn by the app. Constructions with a ruler, a set square or a compass are described but cannot be done on a screen, "
                "so they are not covered. It has not been checked against the official Senegalese programme.",
)
