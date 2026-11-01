"""Cinquième, Figures symétriques par rapport à une droite: the twelfth chapter of the Senegal Cinquième course, written in French.

The contents follow the lesson "Figures symétriques par rapport à une droite" of the Côte d'Ivoire Cinquième programme (the symmetric of a point, of a segment and of a figure, what the symmetry
keeps, and the axes of symmetry of a figure), which was read for this chapter. Every explanation, example, figure and exercise was written independently, with our own numbers. It builds on the
Sixième chapters on the perpendicular bisector and on central symmetry. Drawing a symmetric figure with a set square cannot be done on a screen: it is described. Fixed answers are written as
exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a "verify" expression that the tests evaluate. The step texts and solution lines
are not machine-checked.
"""
from fractions import Fraction

from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .figures import Figure, figure
from .kit import N, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-5e-symetrie-axiale"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")
CM, CM2 = ["cm"], ["cm2", "cm²"]
DEG = ["°", "degrés", "degré", "deg", "degres"]

# ----- Figures -----
POINT = (Figure().point("E", 170, 10, 8, 4).point("F", 170, 200, 8, -4).point("A", 80, 60, -14, -6).point("B", 260, 60, 8, -6).point("I", 170, 60, 8, 16)
         .line("E", "F").segment("A", "B", "fig-dash").right_angle("I", "A", "E", 12).tick("A", "I", 1).tick("I", "B", 1))
TRIANGLE = (Figure().point("E", 170, 8, 8, 4).point("F", 170, 202, 8, -4)
            .point("A", 90, 50, -14, -6).point("B", 40, 150, -14, 14).point("C", 140, 170, -14, 14)
            .point("D", 250, 50, 8, -6).point("G", 300, 150, 8, 14).point("H", 200, 170, 8, 14)
            .line("E", "F").segment("A", "B").segment("B", "C").segment("C", "A").segment("D", "G").segment("G", "H").segment("H", "D")
            .segment("A", "D", "fig-dash").segment("B", "G", "fig-dash").segment("C", "H", "fig-dash"))

# ----- Section 1: the symmetric of a point -----
S1 = Section(
    "point", "Le symétrique d'un point", 22, "point",
    "Connaître la définition du symétrique d'un point par rapport à une droite et en tirer des distances.",
    [
        para("Quand tu te regardes dans un miroir, ton reflet est au même éloignement du miroir que toi, mais de l'autre côté. C'est l'idée de la symétrie par rapport à une droite, appelée symétrie axiale."),
        definition("Symétrique d'un point",
                   "Soit d une droite et A un point n'appartenant pas à d. Le symétrique de A par rapport à d est le point A' tel que la droite d soit la médiatrice du segment [AA']. "
                   "Si A est sur d, son symétrique est lui-même."),
        figure(POINT, "Une droite verticale EF, deux points A à gauche et B à droite à la même hauteur, le segment AB en pointillés coupé à angle droit par la droite en I, avec des traits égaux sur AI et IB.", "B est le symétrique de A par rapport à la droite (EF) : la droite (EF) est la médiatrice de [AB], donc IA = IB et (AB) ⊥ (EF)."),
        rule("Conséquences",
             "Si A' est le symétrique de A par rapport à d, alors (AA') est perpendiculaire à d, et d passe par le milieu I de [AA']. La distance de A à d est donc " + N("AI = AA' \\div 2") + "."),
        example("Exemple 1", "Le point A est à 4 cm de la droite d. A' est son symétrique par rapport à d. Quelle est la longueur AA' ?",
                "A et A' sont de part et d'autre de d, à la même distance.",
                [(N("4 + 4") + " = " + N("8"), "La distance de A' à d est aussi 4 cm.")],
                N("AA' = 8") + " cm.", "4+4==8"),
        example("Exemple 2", "A et A' sont symétriques par rapport à d, et AA' = 14 cm. À quelle distance de d se trouve A ?",
                "d est la médiatrice de [AA'] : elle passe par son milieu.",
                [(N("14 \\div 2") + " = " + N("7"), "Moitié de AA'.")],
                N("7") + " cm.", "14//2==7"),
        example("Exemple 3", "Le point M est sur la droite d. Quel est son symétrique ?",
                "Un point de l'axe est à distance 0 de l'axe.",
                [("M est sur d", "Il est à la même distance (0) de chaque côté : son symétrique est M lui-même.")],
                "M est son propre symétrique.", "0+0==0"),
        example("Exemple 4", "A et B sont symétriques par rapport à d, et le point M est sur d. On donne MA = 5 cm. Quelle est la longueur MB ?",
                "Tout point de la médiatrice est à égale distance des extrémités du segment.",
                [("M est sur la médiatrice de [AB]", "d est la médiatrice de [AB]."),
                 ("MA = MB", "MB = 5 cm.")],
                N("MB = 5") + " cm.", "5==5"),
        warning("La distance entre A et A' est le double de la distance de A à la droite, pas la même. Et pour construire A', on trace la perpendiculaire à d passant par A : la parallèle ne convient pas."),
    ],
    [
        number("s1-g1", "point", "Le point A est à 6 cm de la droite d. Quelle est la distance AA' avec A' son symétrique, en cm ?", Fraction(12), units=CM, hints=["Le double."], solution=["6 × 2 = 12 cm."]),
        number("s1-g2", "point", "A et A' sont symétriques par rapport à d, avec AA' = 9 cm. À quelle distance de d est A, en cm ?", Fraction(9, 2), units=CM, hints=["La moitié."], solution=["9 ÷ 2 = 4,5 cm."]),
        number("s1-g3", "point", "M est sur l'axe d. A et B sont symétriques par rapport à d, avec MA = 8,5 cm. Quelle est la longueur MB, en cm ?", Fraction(17, 2), units=CM, hints=["M est sur la médiatrice."], solution=["MB = MA = 8,5 cm."]),
        number("s1-g4", "point", "Quelle est la mesure de l'angle entre la droite (AA') et l'axe d, en degrés ?", Fraction(90), units=DEG, hints=["d est la médiatrice."], solution=["90°."]),
        choice("s1-g5", "point", "Le point P est sur la droite d. Où est son symétrique par rapport à d ?", ["En P lui-même", "Sur l'autre côté de d", "On ne peut pas le dire"], 0, hints=["Distance 0."], solution=["En P."], wrong={1: "P est déjà sur d.", 2: "On le peut : P est son propre symétrique."}),
    ])

# ----- Section 2: segments and figures -----
S2 = Section(
    "figures", "Le symétrique d'une figure", 24, "figures",
    "Savoir que la symétrie axiale conserve les longueurs, les angles, les aires et les périmètres, et connaître le symétrique d'une droite, d'un segment, d'un cercle.",
    [
        para("Pour tracer le symétrique d'une figure, on construit le symétrique de ses points importants, puis on les relie. La symétrie axiale ne déforme rien : la figure et son image sont superposables, l'une étant retournée."),
        figure(TRIANGLE, "Un triangle ABC à gauche d'une droite verticale, et son symétrique DGH à droite ; les segments en pointillés joignent chaque sommet à son image.", "Le triangle de droite est le symétrique de celui de gauche : mêmes longueurs, mêmes angles, mais lu dans l'autre sens."),
        rule("Ce que la symétrie conserve",
             "La symétrie axiale conserve les distances, les mesures d'angles, les aires et les périmètres. Le symétrique d'un segment est un segment de même longueur, celui d'une droite est une droite, celui d'un cercle est un cercle de même rayon, dont le centre est le symétrique du centre."),
        example("Exemple 1", "ABC est un triangle de côtés 5 cm, 7 cm et 9 cm. A'B'C' est son symétrique par rapport à une droite. Quel est le périmètre de A'B'C' ?",
                "Les longueurs sont conservées.",
                [("A'B'C' a aussi des côtés de 5 cm, 7 cm et 9 cm", "La symétrie conserve les longueurs."),
                 (N("5 + 7 + 9") + " = " + N("21"), "Périmètre.")],
                N("21") + " cm.", "5+7+9==21"),
        example("Exemple 2", "L'angle ABC mesure 64°. A'B'C' est le symétrique. Quelle est la mesure de l'angle A'B'C' ?",
                "Les angles sont conservés.",
                [("La symétrie conserve les mesures d'angles", "A'B'C' mesure " + N("64") + "°.")],
                N("64") + "°.", "64==64"),
        example("Exemple 3", "Un cercle de centre O et de rayon 3 cm a pour symétrique un cercle de centre O'. Quel est son rayon ? Où est O' ?",
                "Le symétrique d'un cercle est un cercle de même rayon.",
                [("Rayon conservé", N("3") + " cm."),
                 ("Centre : le symétrique de O", "O' est le symétrique de O par rapport à la droite.")],
                "Rayon " + N("3") + " cm, de centre O'.", "3==3"),
        example("Exemple 4", "Un rectangle de 8 cm sur 3 cm a pour symétrique un rectangle. Quelle est l'aire du symétrique ?",
                "Les aires sont conservées.",
                [(N("8 \\times 3") + " = " + N("24"), "Aire du rectangle, donc aussi de son symétrique.")],
                N("24") + " cm².", "8*3==24"),
        warning("La symétrie axiale retourne la figure : les longueurs et les angles sont conservés, mais l'orientation est changée (la droite devient la gauche). Ne dis pas que le symétrique est « le même dessin glissé ». Et si le segment est parallèle à l'axe, son symétrique l'est aussi."),
    ],
    [
        number("s2-g1", "figures", "Le segment [AB] mesure 7,5 cm. Quelle est la longueur de son symétrique [A'B'], en cm ?", Fraction(15, 2), units=CM, hints=["Longueurs conservées."], solution=["7,5 cm."]),
        number("s2-g2", "figures", "Un angle mesure 48°. Quelle est la mesure de son symétrique, en degrés ?", Fraction(48), units=DEG, hints=["Angles conservés."], solution=["48°."]),
        number("s2-g3", "figures", "Un carré de 6 cm de côté a pour symétrique un carré. Quelle est l'aire du symétrique, en cm² ?", Fraction(36), units=CM2, hints=["Aires conservées."], solution=["6 × 6 = 36 cm²."]),
        number("s2-g4", "figures", "Un cercle de rayon 4 cm a un symétrique. Quel est le rayon de ce symétrique, en cm ?", Fraction(4), units=CM, hints=["Même rayon."], solution=["4 cm."]),
        choice("s2-g5", "figures", "Le symétrique d'une droite par rapport à une droite d est :", ["Une droite", "Un segment", "Un point"], 0, hints=["Pas de déformation."], solution=["Une droite."], wrong={1: "Il n'y a pas de bout.", 2: "Une droite ne devient pas un point."}),
    ])

# ----- Section 3: axes of symmetry -----
S3 = Section(
    "axes", "Axes de symétrie d'une figure", 22, "axes",
    "Reconnaître les axes de symétrie d'une figure usuelle et en donner le nombre.",
    [
        para("Une figure a un axe de symétrie quand elle est son propre symétrique par rapport à cette droite. On peut alors plier la figure le long de l'axe : les deux moitiés se recouvrent."),
        definition("Axe de symétrie", "Une droite d est un axe de symétrie d'une figure si le symétrique de la figure par rapport à d est la figure elle-même."),
        rule("Axes de symétrie des figures usuelles",
             "Le segment en a 2 (sa médiatrice et la droite qui le porte). Le triangle isocèle en a 1, le triangle équilatéral en a 3. Le rectangle (non carré) en a 2, le losange (non carré) en a 2, le carré en a 4. Le cercle en a une infinité (tous ses diamètres). L'angle en a 1 (sa bissectrice)."),
        example("Exemple 1", "Combien d'axes de symétrie a un triangle équilatéral ?",
                "Chaque hauteur est un axe, il y en a une par sommet.",
                [("Trois sommets, trois hauteurs", N("3") + " axes de symétrie.")],
                N("3") + " axes.", "3==3"),
        example("Exemple 2", "Combien d'axes de symétrie a un rectangle qui n'est pas un carré ? Et un carré ?",
                "Le rectangle a ses deux médianes ; le carré y ajoute ses deux diagonales.",
                [(N("2") + " pour le rectangle", "Les deux droites passant par les milieux des côtés opposés."),
                 (N("2 + 2") + " = " + N("4") + " pour le carré", "On ajoute les deux diagonales.")],
                N("2") + " et " + N("4") + ".", "2+2==4"),
        example("Exemple 3", "Un triangle ABC est isocèle en A, avec un angle de 40° en A. Quelle est la mesure de l'angle B ? Quel est son axe de symétrie ?",
                "L'axe est la médiatrice de [BC], qui passe par A. Les angles à la base sont égaux.",
                [(N("180 - 40") + " = " + N("140"), "Somme des deux autres angles."),
                 (N("140 \\div 2") + " = " + N("70"), "Les deux angles à la base sont égaux.")],
                N("70") + "°, et l'axe est la médiatrice de [BC].", "180-40==140 and 140//2==70"),
        example("Exemple 4", "Quels axes de symétrie a un losange qui n'est pas un carré ?",
                "Ses diagonales sont ses axes.",
                [("Les deux diagonales", N("2") + " axes de symétrie.")],
                N("2") + " axes, ses diagonales.", "1+1==2"),
        warning("Les diagonales d'un rectangle ne sont pas ses axes de symétrie (sauf pour le carré) : plie un rectangle de papier selon une diagonale, les deux moitiés ne se superposent pas. Et un parallélogramme quelconque n'a pas d'axe de symétrie."),
    ],
    [
        number("s3-g1", "axes", "Combien d'axes de symétrie a un carré ?", Fraction(4), hints=["Deux médianes et deux diagonales."], solution=["4."]),
        number("s3-g2", "axes", "Combien d'axes de symétrie a un triangle isocèle qui n'est pas équilatéral ?", Fraction(1), hints=["Un seul."], solution=["1."]),
        number("s3-g3", "axes", "Combien d'axes de symétrie a un losange qui n'est pas un carré ?", Fraction(2), hints=["Ses diagonales."], solution=["2."]),
        number("s3-g4", "axes", "Un triangle isocèle en A a un angle de 50° en B. Quelle est la mesure de l'angle C, en degrés ?", Fraction(50), units=DEG, hints=["Angles à la base égaux."], solution=["50°."]),
        choice("s3-g5", "axes", "La diagonale d'un rectangle (non carré) est-elle un axe de symétrie ?", ["Non", "Oui"], 0, hints=["Pense au pliage."], solution=["Non."], wrong={1: "Seules les diagonales d'un carré ou d'un losange le sont."}),
    ])

# ----- Section 4: problems -----
S4 = Section(
    "problemes", "Raisonner avec la symétrie axiale", 24, "problemes",
    "Utiliser la conservation des distances et des angles pour justifier une égalité, et lire une symétrie sur une droite graduée.",
    [
        para("La symétrie axiale permet de justifier des égalités sans calcul : si deux points ou deux figures sont symétriques, tout ce qui se mesure est égal."),
        rule("Symétrie par rapport à une droite verticale",
             "Sur une droite graduée horizontale, ou dans un repère, la symétrie par rapport à la droite verticale d'abscisse k envoie le point d'abscisse x sur le point d'abscisse " + N("2k - x") + ", et laisse l'ordonnée inchangée. L'abscisse k est donc le milieu de x et de " + N("2k - x") + "."),
        example("Exemple 1", "On considère la droite verticale d'abscisse 3. Quelle est l'abscisse du symétrique du point d'abscisse 7 ?",
                "On applique la formule 2k − x.",
                [(N("2 \\times 3 - 7") + " = " + N("6 - 7") + " = " + N("-1"), "Le symétrique est de l'autre côté de l'axe.")],
                N("-1") + ".", "2*3-7==-1"),
        example("Exemple 2", "A d'abscisse 2 et B d'abscisse 10 sont symétriques par rapport à une droite verticale. Quelle est l'abscisse de cette droite ?",
                "L'axe passe par le milieu de [AB].",
                [(N("(2 + 10) \\div 2") + " = " + N("6"), "Milieu des abscisses.")],
                N("6") + ".", "(2+10)//2==6"),
        example("Exemple 3", "ABC est un triangle isocèle en A, et I est le milieu de [BC]. On sait que BC = 12 cm. Que valent BI et l'angle AIB ?",
                "La médiatrice de [BC] passe par A : c'est l'axe de symétrie du triangle.",
                [(N("12 \\div 2") + " = " + N("6"), "BI est la moitié de BC."),
                 ("La médiane est aussi la hauteur", "(AI) est perpendiculaire à (BC) : l'angle AIB est droit, soit " + N("90") + "°.")],
                N("BI = 6") + " cm et " + N("90") + "°.", "12//2==6"),
        example("Exemple 4", "Un jardinier doit aller du point A au puits P sur la berge d, puis au point B, symétrique de A par rapport à d. Si AP = 8 m, quelle est la longueur du trajet A → P → B ?",
                "P est sur d, qui est la médiatrice de [AB] : PA = PB.",
                [(N("PB = PA") + " = " + N("8"), "P est sur la médiatrice."),
                 (N("8 + 8") + " = " + N("16"), "Longueur du trajet.")],
                N("16") + " m.", "8+8==16"),
        warning("« Elles ont l'air symétriques » n'est pas une preuve. Il faut dire quelle droite est l'axe, puis utiliser « la symétrie conserve les longueurs et les angles ». Et sur une droite graduée, ne mélange pas le milieu (l'axe) et le symétrique."),
    ],
    [
        number("s4-g1", "problemes", "L'axe est la droite verticale d'abscisse 5. Quelle est l'abscisse du symétrique du point d'abscisse 9 ?", Fraction(1), hints=["2 × 5 − 9."], solution=["10 − 9 = 1."]),
        number("s4-g2", "problemes", "A d'abscisse −4 et B d'abscisse 8 sont symétriques par rapport à une droite verticale. Quelle est l'abscisse de cette droite ?", Fraction(2), hints=["Le milieu."], solution=["(−4 + 8) ÷ 2 = 2."]),
        number("s4-g3", "problemes", "ABC est isocèle en A, avec BC = 18 cm. I est le milieu de [BC]. Quelle est la longueur CI, en cm ?", Fraction(9), units=CM, hints=["La moitié."], solution=["9 cm."]),
        number("s4-g4", "problemes", "A et B sont symétriques par rapport à d. P est un point de d avec PA = 7 cm. Quelle est la longueur du trajet A → P → B, en cm ?", Fraction(14), units=CM, hints=["PB = PA."], solution=["7 + 7 = 14 cm."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "point", "Le point A est à 3,5 cm de la droite d. Quelle est la distance AA' avec A' son symétrique, en cm ?", Fraction(7), 1, ["Le double."], ["7 cm."], units=CM),
    number("p2", "point", "A et A' sont symétriques par rapport à d, avec AA' = 11 cm. À quelle distance de d est A', en cm ?", Fraction(11, 2), 1, ["La moitié."], ["5,5 cm."], units=CM),
    number("p3", "point", "M est un point de la droite d. A et B sont symétriques par rapport à d, avec MB = 12 cm. Quelle est la longueur MA, en cm ?", Fraction(12), 1, ["Médiatrice."], ["12 cm."], units=CM),
    number("p4", "point", "A et A' sont symétriques par rapport à d. Quelle est la mesure de l'angle entre (AA') et d, en degrés ?", Fraction(90), 1, ["Médiatrice."], ["90°."], units=DEG),
    number("p5", "point", "A est à 2 cm de d et B est à 5 cm de d, du même côté. A' et B' sont leurs symétriques. À quelle distance de d est B', en cm ?", Fraction(5), 2, ["Même distance."], ["5 cm."], units=CM),
    number("p6", "point", "A est à 2 cm de d et B est à 5 cm de d, de part et d'autre de d. Quelle est la distance entre A et B si (AB) est perpendiculaire à d, en cm ?", Fraction(7), 3, ["Elles s'ajoutent."], ["2 + 5 = 7 cm."], units=CM),
    choice("p7", "point", "Si A' est le symétrique de A par rapport à d, alors d est :", ["La médiatrice de [AA']", "Parallèle à (AA')", "La médiane de [AA']"], 0, 1, ["Définition."], ["La médiatrice."], wrong={1: "Elle est perpendiculaire.", 2: "Une médiane est dans un triangle."}),
    number("p8", "figures", "Un triangle a un périmètre de 27 cm. Quel est le périmètre de son symétrique, en cm ?", Fraction(27), 1, ["Conservé."], ["27 cm."], units=CM),
    number("p9", "figures", "Un angle mesure 125°. Quelle est la mesure de son symétrique, en degrés ?", Fraction(125), 1, ["Conservé."], ["125°."], units=DEG),
    number("p10", "figures", "Un rectangle de 9 cm sur 4 cm a un symétrique. Quelle est son aire, en cm² ?", Fraction(36), 1, ["Conservée."], ["36 cm²."], units=CM2),
    number("p11", "figures", "Le diamètre d'un cercle est de 10 cm. Quel est le rayon de son symétrique, en cm ?", Fraction(5), 2, ["Rayon puis conservation."], ["10 ÷ 2 = 5 cm."], units=CM),
    number("p12", "figures", "Dans un triangle ABC, AB = 4 cm. Quelle est la longueur A'B' de son symétrique, en cm ?", Fraction(4), 1, ["Conservée."], ["4 cm."], units=CM),
    number("p13", "figures", "Un triangle d'aire 15 cm² est symétrisé. Quelle est l'aire du symétrique, en cm² ?", Fraction(15), 1, ["Conservée."], ["15 cm²."], units=CM2),
    choice("p14", "figures", "Laquelle de ces grandeurs n'est PAS conservée par la symétrie axiale ?", ["L'orientation (gauche et droite)", "Les longueurs", "Les angles"], 0, 2, ["Pense au reflet dans un miroir."], ["L'orientation change."], wrong={1: "Les longueurs sont conservées.", 2: "Les angles sont conservés."}),
    choice("p15", "figures", "Le symétrique d'une droite parallèle à l'axe d est :", ["Une droite parallèle à d", "Une droite perpendiculaire à d", "Un point"], 0, 3, ["Les distances sont conservées."], ["Parallèle à d."], wrong={1: "Une parallèle reste parallèle.", 2: "Une droite reste une droite."}),
    number("p16", "axes", "Combien d'axes de symétrie a un triangle équilatéral ?", Fraction(3), 1, ["Une hauteur par sommet."], ["3."]),
    number("p17", "axes", "Combien d'axes de symétrie a un rectangle qui n'est pas un carré ?", Fraction(2), 1, ["Deux médianes."], ["2."]),
    number("p18", "axes", "Combien d'axes de symétrie a un segment ?", Fraction(2), 2, ["Sa médiatrice et sa droite."], ["2."]),
    number("p19", "axes", "Combien d'axes de symétrie a un angle ?", Fraction(1), 2, ["Sa bissectrice."], ["1."]),
    number("p20", "axes", "Combien d'axes de symétrie a un carré ?", Fraction(4), 1, ["Médianes et diagonales."], ["4."]),
    number("p21", "axes", "Un triangle ABC est isocèle en A avec un angle de 80° en A. Quelle est la mesure de l'angle B, en degrés ?", Fraction(50), 2, ["(180 − 80) ÷ 2."], ["50°."], units=DEG),
    number("p22", "axes", "Un triangle ABC est isocèle en A avec un angle de 70° en B. Quelle est la mesure de l'angle A, en degrés ?", Fraction(40), 2, ["180 − 140."], ["B = C = 70.", "A = 180 − 140 = 40°."], units=DEG),
    choice("p23", "axes", "Un parallélogramme quelconque a-t-il un axe de symétrie ?", ["Non", "Oui, une diagonale", "Oui, la médiane"], 0, 2, ["Plie une feuille."], ["Non."], wrong={1: "Les deux moitiés ne se superposent pas.", 2: "Même chose."}),
    choice("p24", "axes", "Quelle figure a une infinité d'axes de symétrie ?", ["Le cercle", "Le carré", "Le triangle équilatéral"], 0, 2, ["Tous les diamètres."], ["Le cercle."], wrong={1: "Il en a 4.", 2: "Il en a 3."}),
    number("p25", "problemes", "L'axe est la droite verticale d'abscisse 4. Quelle est l'abscisse du symétrique du point d'abscisse 11 ?", Fraction(-3), 2, ["2 × 4 − 11."], ["8 − 11 = −3."]),
    number("p26", "problemes", "L'axe est la droite verticale d'abscisse −2. Quelle est l'abscisse du symétrique du point d'abscisse 1 ?", Fraction(-5), 3, ["2 × (−2) − 1."], ["−4 − 1 = −5."]),
    number("p27", "problemes", "A d'abscisse 3 et B d'abscisse 15 sont symétriques par rapport à une droite verticale. Quelle est l'abscisse de la droite ?", Fraction(9), 2, ["Le milieu."], ["(3 + 15) ÷ 2 = 9."]),
    number("p28", "problemes", "ABC est isocèle en A, I est le milieu de [BC] et AI = 5 cm avec BC = 12 cm. Quelle est la longueur BI, en cm ?", Fraction(6), 2, ["BC ÷ 2."], ["6 cm."], units=CM),
    number("p29", "problemes", "A et B sont symétriques par rapport à d, et P est un point de d tel que PA = 6,5 cm. Quelle est la longueur du trajet A → P → B, en cm ?", Fraction(13), 2, ["PB = PA."], ["13 cm."], units=CM),
    number("p30", "problemes", "ABCD est un losange. La diagonale [AC] est un axe de symétrie. Si AB = 5 cm, combien mesure AD, en cm ?", Fraction(5), 3, ["B et D sont symétriques par rapport à (AC)."], ["AD = AB = 5 cm."], units=CM),
    number("p31", "problemes", "Un triangle ABC est isocèle en A avec BC = 10 cm et un périmètre de 34 cm. Combien mesure AB, en cm ?", Fraction(12), 3, ["AB = AC."], ["34 − 10 = 24.", "24 ÷ 2 = 12 cm."], units=CM),
    number("p32", "problemes", "A, A' sont symétriques par rapport à d, et M est un point de d. Le triangle AMA' a MA = 5 cm et AA' = 6 cm. Quel est son périmètre, en cm ?", Fraction(16), 3, ["MA' = MA."], ["MA' = 5 cm.", "5 + 5 + 6 = 16 cm."], units=CM),
]

SUMMARY = [
    definition("Symétrique d'un point", "A' est le symétrique de A par rapport à d si d est la médiatrice de [AA']. Un point de d est son propre symétrique. Les distances de A et de A' à d sont égales."),
    rule("Conservation", "La symétrie axiale conserve les longueurs, les angles, les aires et les périmètres. Le symétrique d'une droite est une droite, celui d'un cercle un cercle de même rayon."),
    rule("Axes de symétrie", "Segment : 2. Triangle isocèle : 1. Triangle équilatéral : 3. Rectangle : 2. Losange : 2. Carré : 4. Cercle : une infinité. Angle : 1."),
    para("Les erreurs à éviter : prendre la parallèle au lieu de la perpendiculaire ; oublier que la distance AA' est le double ; dire que les diagonales d'un rectangle sont des axes ; justifier avec « ça se voit »."),
]

CONCEPTS = {
    "point": ("Symétrique d'un point", "point"),
    "figures": ("Symétrique d'une figure", "figures"),
    "axes": ("Axes de symétrie", "axes"),
    "problemes": ("Raisonner avec la symétrie", "problemes"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    p = rng.randint(2, 30)
    questions.append(number("a1", "point", f"Le point A est à {p} cm de la droite d. Quelle est la distance AA' avec A' son symétrique, en cm ?", Fraction(2 * p), 1, ["Le double."], [f"2 × {p} = {2 * p} cm."], units=CM))
    p = 2 * rng.randint(2, 30)
    questions.append(number("a2", "point", f"A et A' sont symétriques par rapport à d, avec AA' = {p} cm. À quelle distance de d est A, en cm ?", Fraction(p // 2), 1, ["La moitié."], [f"{p} ÷ 2 = {p // 2} cm."], units=CM))
    p = rng.randint(3, 40)
    questions.append(number("a3", "figures", f"Le segment [AB] mesure {p} cm. Quelle est la longueur de son symétrique [A'B'], en cm ?", Fraction(p), 1, ["Conservée."], [f"{p} cm."], units=CM))
    p = rng.randint(20, 160)
    questions.append(number("a4", "figures", f"Un angle mesure {p}°. Quelle est la mesure de son symétrique, en degrés ?", Fraction(p), 1, ["Conservée."], [f"{p}°."], units=DEG))
    sides = rng.sample(range(4, 20), 3)
    questions.append(number("a5", "figures", f"Un triangle a des côtés de {sides[0]} cm, {sides[1]} cm et {sides[2]} cm. Quel est le périmètre de son symétrique, en cm ?", Fraction(sum(sides)), 2, ["Périmètre conservé."], [f"{sides[0]} + {sides[1]} + {sides[2]} = {sum(sides)} cm."], units=CM))
    a, b = rng.randint(3, 20), rng.randint(2, 15)
    questions.append(number("a6", "figures", f"Un rectangle de {a} cm sur {b} cm a un symétrique. Quelle est son aire, en cm² ?", Fraction(a * b), 2, ["Aire conservée."], [f"{a} × {b} = {a * b} cm²."], units=CM2))
    r = rng.randint(2, 25)
    questions.append(number("a7", "figures", f"Un cercle de rayon {r} cm a un symétrique. Quel est le rayon de ce symétrique, en cm ?", Fraction(r), 1, ["Conservé."], [f"{r} cm."], units=CM))
    shapes = [("un carré", 4), ("un rectangle qui n'est pas un carré", 2), ("un losange qui n'est pas un carré", 2), ("un triangle équilatéral", 3), ("un triangle isocèle qui n'est pas équilatéral", 1)]
    name, axes = rng.choice(shapes)
    questions.append(number("a8", "axes", f"Combien d'axes de symétrie a {name} ?", Fraction(axes), 1, ["Pense au pliage."], [f"{axes} axe(s) de symétrie."]))
    k, x = rng.randint(-5, 8), rng.randint(-8, 14)
    questions.append(number("a9", "problemes", f"L'axe est la droite verticale d'abscisse {k}. Quelle est l'abscisse du symétrique du point d'abscisse {x} ?", Fraction(2 * k - x), 2, ["2 × k − x."], [f"2 × ({k}) − ({x}) = {2 * k - x}."]))
    pa = rng.randint(3, 40)
    questions.append(number("a10", "problemes", f"A et B sont symétriques par rapport à d, et P est un point de d tel que PA = {pa} cm. Quelle est la longueur du trajet A → P → B, en cm ?", Fraction(2 * pa), 2, ["PB = PA."], [f"{pa} + {pa} = {2 * pa} cm."], units=CM))
    apex = 2 * rng.randint(10, 40)
    questions.append(number("a11", "axes", f"Un triangle ABC est isocèle en A avec un angle de {apex}° en A. Quelle est la mesure de l'angle B, en degrés ?", Fraction(180 - apex, 2), 3, ["(180 − A) ÷ 2."], [f"180 − {apex} = {180 - apex}.", f"{180 - apex} ÷ 2 = {(180 - apex) // 2}°."], units=DEG))
    ab = rng.randint(-10, 10)
    gap = 2 * rng.randint(1, 8)
    questions.append(number("a12", "problemes", f"A d'abscisse {ab} et B d'abscisse {ab + gap} sont symétriques par rapport à une droite verticale. Quelle est l'abscisse de cette droite ?", Fraction(ab + gap // 2), 3, ["Le milieu."], [f"({ab} + {ab + gap}) ÷ 2 = {ab + gap // 2}."]))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=12, title="Figures symétriques par rapport à une droite", language="fr",
    intro="Le reflet dans un miroir, les ailes d'un papillon, un masque : toutes ces images sont symétriques. Ce chapitre t'apprend la symétrie axiale, ce qu'elle conserve, et les axes de symétrie des figures usuelles.",
    objectives=["Connaître le symétrique d'un point par rapport à une droite.",
                "Savoir ce que la symétrie axiale conserve.",
                "Trouver les axes de symétrie d'une figure usuelle.",
                "Utiliser la symétrie pour justifier une égalité."],
    prerequisites=[{"text": "Connaître la médiatrice d'un segment.", "chapter": "sn-6e-droites-cercles"},
                   {"text": "Connaître les triangles particuliers.", "chapter": "sn-5e-triangles"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Twelfth chapter of the Senegal Cinquième course. Its contents follow the lesson on figures symmetric about a line of the Côte d'Ivoire Cinquième programme (the symmetric of a point and of a figure, what the symmetry keeps, the axes of symmetry), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. Drawing a symmetric figure with a set square cannot be done on a screen, so it is described and not covered. "
                "It has not been checked against the official Senegalese programme.",
)
