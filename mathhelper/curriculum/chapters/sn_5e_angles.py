"""Cinquième, Angles: the sixth chapter of the Senegal Cinquième course, written in French.

The contents follow the lesson "Angles" of the Côte d'Ivoire Cinquième programme (adjacent angles, complementary and supplementary angles, opposite angles at a vertex,
and the sum of the angles of a triangle), which was read for this chapter. Every explanation, example, figure and exercise was written independently, with our own numbers.
It builds on the Sixième chapter on angles. The figures are drawn from constants by figures.py. Fixed answers are written as exact fractions and re-checked by tests against an
independent recalculation, and each worked example carries a "verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked.
"""
from fractions import Fraction

from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .figures import Figure, figure
from .kit import N, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-5e-angles"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")
DEG = ["°", "degrés", "degré", "deg", "degres"]

# ----- Figures -----
ADJACENT = (Figure().point("O", 80, 150, -14, 22).point("A", 290, 150, -4, 22).point("B", 230, 50, 10, 0).point("C", 70, 40, -6, -10)
            .ray("O", "A").ray("O", "B").ray("O", "C").arc("O", "A", "B", 40).arc("O", "B", "C", 52))
FLAT = Figure().point("A", 40, 150, -4, 22).point("O", 170, 150, -4, 22).point("B", 300, 150, -4, 22).point("C", 100, 40, -6, -10).line("A", "B").ray("O", "C").arc("O", "A", "C", 34).arc("O", "C", "B", 46)
VERTICAL = (Figure().point("O", 170, 105, 8, 22).point("A", 70, 50, -14, -4).point("B", 270, 160, 8, 12).point("C", 80, 165, -14, 14).point("D", 260, 45, 8, -4)
            .line("A", "B").line("C", "D").arc("O", "A", "C", 28).arc("O", "B", "D", 28))
TRIANGLE = (Figure().point("A", 60, 160, -14, 22).point("B", 290, 160, 8, 22).point("C", 160, 40, 8, -6)
            .segment("A", "B").segment("B", "C").segment("C", "A").arc("A", "B", "C", 36).arc("B", "A", "C", 36).arc("C", "A", "B", 30))

# ----- Section 1: adjacent, complementary and supplementary angles -----
S1 = Section(
    "adjacents", "Angles adjacents, complémentaires et supplémentaires", 24, "adjacents",
    "Reconnaître des angles adjacents, complémentaires ou supplémentaires, et calculer la mesure d'un angle complémentaire ou supplémentaire.",
    [
        para("En Sixième, tu as additionné des angles qui se touchent. Ce chapitre donne des mots précis à ces situations, qui servent à raisonner dans toutes les figures du collège."),
        definition("Angles adjacents",
                   "Deux angles sont adjacents s'ils ont le même sommet, un côté commun, et s'ils sont de part et d'autre de ce côté commun (ils ne se chevauchent pas). "
                   "Si deux angles adjacents " + N("\\widehat{AOB}") + " et " + N("\\widehat{BOC}") + " forment ensemble l'angle " + N("\\widehat{AOC}") + ", alors " + N("\\widehat{AOC} = \\widehat{AOB} + \\widehat{BOC}") + "."),
        figure(ADJACENT, "Trois demi-droites [OA), [OB) et [OC) de même origine O, qui forment deux angles AOB et BOC côte à côte.", "Les angles AOB et BOC sont adjacents : ils ont le sommet O et le côté [OB) en commun."),
        definition("Angles complémentaires et supplémentaires",
                   "Deux angles sont complémentaires quand la somme de leurs mesures est 90°. Deux angles sont supplémentaires quand la somme de leurs mesures est 180°. "
                   "Des angles adjacents qui forment un angle droit sont complémentaires ; qui forment un angle plat, ils sont supplémentaires."),
        figure(FLAT, "Trois points A, O et B alignés, avec une demi-droite [OC) qui part de O : les angles AOC et COB sont adjacents et forment un angle plat.", "A, O et B sont alignés : les angles AOC et COB sont supplémentaires, leur somme est 180°."),
        example("Exemple 1", "Un angle mesure 35°. Quelle est la mesure d'un angle complémentaire ? d'un angle supplémentaire ?",
                "On retire 35 de 90, puis de 180.",
                [(N("90 - 35") + " = " + N("55"), "Angle complémentaire."),
                 (N("180 - 35") + " = " + N("145"), "Angle supplémentaire.")],
                N("55") + "° et " + N("145") + "°.", "90-35==55 and 180-35==145"),
        example("Exemple 2", "A, O et B sont alignés, O entre A et B. C est un point hors de la droite et " + N("\\widehat{AOC} = 112") + "°. Calculer " + N("\\widehat{COB}") + ".",
                "Les angles AOC et COB sont supplémentaires.",
                [(N("\\widehat{AOC} + \\widehat{COB} = 180"), "Ils forment un angle plat."),
                 (N("180 - 112") + " = " + N("68"), "On retire l'angle connu.")],
                N("\\widehat{COB} = 68") + "°.", "180-112==68"),
        example("Exemple 3", "Deux angles complémentaires sont tels que l'un mesure le double de l'autre. Quelles sont leurs mesures ?",
                "Si le petit vaut x, le grand vaut 2x et leur somme est 90.",
                [(N("x + 2x = 3x") + " = " + N("90"), "Trois parts égales."),
                 (N("x = 90 \\div 3") + " = " + N("30"), "Le petit angle mesure 30°."),
                 (N("2x") + " = " + N("60"), "Le grand angle mesure 60°.")],
                N("30") + "° et " + N("60") + "°.", "90//3==30 and 2*30==60 and 30+60==90"),
        example("Exemple 4", "Les angles de 48° et de 132° sont-ils complémentaires ? supplémentaires ?",
                "On calcule leur somme.",
                [(N("48 + 132") + " = " + N("180"), "La somme est 180°.")],
                "Ils sont supplémentaires, pas complémentaires.", "48+132==180"),
        warning("Complémentaire fait 90°, supplémentaire fait 180° : pour t'en souvenir, « C » vient avant « S » comme 90 vient avant 180. Et deux angles qui sont seulement complémentaires ou supplémentaires ne sont pas forcément adjacents : cela dépend de leur position."),
    ],
    [
        number("s1-g1", "adjacents", "Un angle mesure 62°. Quelle est la mesure d'un angle complémentaire, en degrés ?", Fraction(28), units=DEG, hints=["90 moins l'angle."], solution=["90 − 62 = 28°."]),
        number("s1-g2", "adjacents", "Un angle mesure 62°. Quelle est la mesure d'un angle supplémentaire, en degrés ?", Fraction(118), units=DEG, hints=["180 moins l'angle."], solution=["180 − 62 = 118°."]),
        number("s1-g3", "adjacents", "A, O et B sont alignés, O entre A et B. ∠AOC = 125°. Quelle est la mesure de ∠COB, en degrés ?", Fraction(55), units=DEG, hints=["Les deux angles sont supplémentaires."], solution=["∠COB = 180 − 125 = 55°."]),
        number("s1-g4", "adjacents", "Deux angles complémentaires : l'un mesure le triple de l'autre. Quelle est la mesure du plus petit, en degrés ?", Fraction(45, 2), units=DEG, hints=["1 part + 3 parts = 4 parts = 90°."], solution=["90 ÷ 4 = 22,5°."]),
        choice("s1-g5", "adjacents", "Des angles de 70° et de 20° sont :", ["complémentaires", "supplémentaires", "ni l'un ni l'autre"], 0, hints=["Additionne-les."], solution=["70 + 20 = 90 : complémentaires."], wrong={1: "180 serait la somme pour des supplémentaires.", 2: "La somme est 90."}),
    ])

# ----- Section 2: opposite angles -----
S2 = Section(
    "opposes", "Angles opposés par le sommet", 22, "opposes",
    "Reconnaître deux angles opposés par le sommet, savoir qu'ils ont la même mesure, et calculer les quatre angles formés par deux droites sécantes.",
    [
        para("Quand deux droites se croisent, elles forment quatre angles autour du point d'intersection. Ceux qui sont face à face, comme les deux pointes d'un papillon, s'appellent des angles opposés par le sommet."),
        definition("Angles opposés par le sommet",
                   "Deux droites sécantes en O forment quatre angles. Deux de ces angles sont opposés par le sommet quand leurs côtés sont les prolongements l'un de l'autre. Les angles opposés par le sommet ont la même mesure."),
        figure(VERTICAL, "Deux droites (AB) et (CD) qui se coupent en O : les angles AOC et BOD sont face à face, de même que AOD et BOC.", "Les angles AOC et BOD sont opposés par le sommet : ils ont la même mesure. Les angles AOC et COB sont supplémentaires."),
        rule("Pourquoi ils sont égaux",
             "Si l'angle AOC mesure x, alors l'angle COB, qui forme avec lui un angle plat, mesure 180 − x. L'angle BOD, qui forme avec COB un angle plat, mesure aussi 180 − (180 − x) = x. Les angles opposés par le sommet sont donc égaux."),
        example("Exemple 1", "Deux droites se coupent en O. L'angle AOC mesure 38°. Calculer BOD, puis AOD et BOC.",
                "BOD est opposé par le sommet à AOC ; AOD est supplémentaire de AOC.",
                [(N("\\widehat{BOD} = \\widehat{AOC}") + " = " + N("38") + "°", "Angles opposés par le sommet."),
                 (N("\\widehat{AOD} = 180 - 38") + " = " + N("142") + "°", "AOD et AOC forment un angle plat."),
                 (N("\\widehat{BOC} = \\widehat{AOD}") + " = " + N("142") + "°", "Angles opposés par le sommet.")],
                N("38") + "°, " + N("142") + "° et " + N("142") + "°.", "180-38==142 and 38+142==180"),
        example("Exemple 2", "Deux droites sécantes forment un angle de 90°. Que valent les trois autres angles ?",
                "Chaque angle est égal à son opposé ou supplémentaire de son voisin.",
                [(N("180 - 90") + " = " + N("90"), "Le voisin mesure 90°."),
                 ("L'opposé de 90° mesure 90°", "Les quatre angles sont droits.")],
                "Les quatre angles mesurent " + N("90") + "° : les droites sont perpendiculaires.", "180-90==90"),
        example("Exemple 3", "Deux angles opposés par le sommet mesurent x et 2x − 20. Quelle est la valeur de x ?",
                "Ils ont la même mesure : on écrit l'égalité.",
                [(N("x = 2x - 20"), "Les mesures sont égales."),
                 (N("20 = 2x - x") + " donc " + N("x = 20"), "On regroupe les x.")],
                N("x = 20") + "°.", "20==2*20-20"),
        example("Exemple 4", "Quelle est la somme des quatre angles formés par deux droites sécantes ?",
                "Deux angles voisins forment un angle plat, et il y a deux paires de voisins.",
                [(N("180 + 180") + " = " + N("360"), "Deux fois un angle plat : un tour complet.")],
                N("360") + "°.", "180+180==360"),
        warning("Deux angles opposés par le sommet sont égaux, mais deux angles égaux ne sont pas toujours opposés par le sommet. Et deux angles voisins (qui se touchent) ne sont pas égaux en général : ils sont supplémentaires."),
    ],
    [
        number("s2-g1", "opposes", "Deux droites se coupent en O. ∠AOC = 55°. Quelle est la mesure de l'angle ∠BOD, opposé par le sommet, en degrés ?", Fraction(55), units=DEG, hints=["Angles opposés par le sommet."], solution=["Ils ont la même mesure : 55°."]),
        number("s2-g2", "opposes", "Deux droites se coupent en O. ∠AOC = 55°. Quelle est la mesure de ∠AOD, en degrés ?", Fraction(125), units=DEG, hints=["AOD et AOC sont supplémentaires."], solution=["180 − 55 = 125°."]),
        number("s2-g3", "opposes", "Deux droites sécantes forment un angle de 72°. Quelle est la somme des deux angles qui l'entourent, en degrés ?", Fraction(216), units=DEG, hints=["Chaque voisin mesure 180 − 72."], solution=["180 − 72 = 108° pour chaque voisin.", "108 + 108 = 216°."]),
        number("s2-g4", "opposes", "Deux angles opposés par le sommet mesurent x et 3x − 30. Quelle est la valeur de x, en degrés ?", Fraction(15), units=DEG, hints=["x = 3x − 30."], solution=["30 = 3x − x = 2x, donc x = 15°."]),
        choice("s2-g5", "opposes", "Deux angles opposés par le sommet :", ["ont la même mesure", "sont supplémentaires", "sont complémentaires"], 0, hints=["Ils sont face à face."], solution=["Les angles opposés par le sommet sont égaux."], wrong={1: "Ce sont les angles voisins qui sont supplémentaires.", 2: "Ils ne sont complémentaires que si chacun mesure 45°."}),
    ])

# ----- Section 3: the sum of the angles of a triangle -----
S3 = Section(
    "triangle", "La somme des angles d'un triangle", 24, "triangle",
    "Connaître la somme des angles d'un triangle, calculer le troisième angle, et l'utiliser pour les triangles particuliers.",
    [
        para("Découpe un triangle en papier, déchire ses trois coins et mets-les côte à côte : ils forment un angle plat. C'est ce que dit la propriété de la somme des angles d'un triangle."),
        rule("Somme des angles d'un triangle",
             "Dans un triangle, la somme des mesures des trois angles est égale à 180° : " + N("\\widehat{A} + \\widehat{B} + \\widehat{C} = 180") + ". "
             "Dans un triangle rectangle, les deux angles aigus sont complémentaires. Dans un triangle équilatéral, les trois angles mesurent 60°. Dans un triangle isocèle, les deux angles à la base sont égaux."),
        figure(TRIANGLE, "Un triangle ABC avec un arc marquant chacun de ses trois angles.", "Les trois angles du triangle ABC ont pour somme 180°."),
        example("Exemple 1", "Dans un triangle, deux angles mesurent 48° et 75°. Calculer le troisième.",
                "On retire la somme des deux angles connus de 180.",
                [(N("48 + 75") + " = " + N("123"), "Somme des deux angles."),
                 (N("180 - 123") + " = " + N("57"), "Le troisième angle.")],
                N("57") + "°.", "180-(48+75)==57"),
        example("Exemple 2", "Un triangle est rectangle et un de ses angles aigus mesure 37°. Calculer l'autre angle aigu.",
                "L'angle droit mesure 90° : les deux autres font ensemble 90°.",
                [(N("180 - 90") + " = " + N("90"), "Reste pour les deux angles aigus."),
                 (N("90 - 37") + " = " + N("53"), "L'autre angle aigu.")],
                N("53") + "°.", "90-37==53"),
        example("Exemple 3", "Un triangle isocèle a un angle au sommet de 40°. Quelle est la mesure de chaque angle à la base ?",
                "Les deux angles à la base sont égaux, et leur somme est 180 − 40.",
                [(N("180 - 40") + " = " + N("140"), "Somme des deux angles à la base."),
                 (N("140 \\div 2") + " = " + N("70"), "Ils sont égaux.")],
                N("70") + "° chacun.", "180-40==140 and 140//2==70"),
        example("Exemple 4", "Quelle est la mesure de chaque angle d'un triangle équilatéral ?",
                "Les trois angles sont égaux et leur somme est 180°.",
                [(N("180 \\div 3") + " = " + N("60"), "Trois angles égaux.")],
                N("60") + "°.", "180//3==60"),
        warning("La somme des angles d'un triangle est toujours 180°, quelle que soit sa forme et sa taille : un grand triangle n'a pas de plus grands angles au total. Et un triangle ne peut avoir qu'un angle droit ou obtus au plus, parce que sinon la somme dépasserait 180°."),
    ],
    [
        number("s3-g1", "triangle", "Un triangle a deux angles de 50° et de 65°. Quelle est la mesure du troisième, en degrés ?", Fraction(65), units=DEG, hints=["180 moins la somme."], solution=["50 + 65 = 115.", "180 − 115 = 65°."]),
        number("s3-g2", "triangle", "Un triangle rectangle a un angle aigu de 28°. Quelle est la mesure de l'autre angle aigu, en degrés ?", Fraction(62), units=DEG, hints=["Les deux angles aigus font 90°."], solution=["90 − 28 = 62°."]),
        number("s3-g3", "triangle", "Un triangle isocèle a un angle au sommet de 100°. Quelle est la mesure de chaque angle à la base, en degrés ?", Fraction(40), units=DEG, hints=["180 − 100, puis divise par 2."], solution=["180 − 100 = 80.", "80 ÷ 2 = 40°."]),
        number("s3-g4", "triangle", "Un triangle isocèle a un angle à la base de 55°. Quelle est la mesure de l'angle au sommet, en degrés ?", Fraction(70), units=DEG, hints=["Il y a deux angles à la base."], solution=["55 + 55 = 110.", "180 − 110 = 70°."]),
        choice("s3-g5", "triangle", "Un triangle peut-il avoir deux angles de 100° ?", ["Non, la somme dépasserait 180°", "Oui", "Oui, s'il est isocèle"], 0, hints=["Additionne 100 + 100."], solution=["100 + 100 = 200 est plus grand que 180 : impossible."], wrong={1: "La somme des trois angles est 180°.", 2: "Même un triangle isocèle respecte la somme 180°."}),
    ])

# ----- Section 4: problems -----
S4 = Section(
    "problemes", "Problèmes avec des angles", 22, "problemes",
    "Combiner les propriétés des angles adjacents, opposés par le sommet et du triangle pour calculer des angles dans une figure.",
    [
        para("Dans une figure, on cherche souvent un angle qui n'est pas donné. On avance pas à pas : à chaque étape, on utilise une propriété sûre, et on ne mesure jamais avec le rapporteur ce qu'on peut calculer."),
        example("Exemple 1", "Deux droites se coupent en O et forment un angle AOC de 50°. D'autre part, un triangle ABC a un angle en A de 50° et un angle en B de 60°. Quel est l'angle en C ? Comparer avec l'angle BOD.",
                "On calcule l'angle manquant du triangle, et BOD par l'angle opposé par le sommet.",
                [(N("180 - (50 + 60)") + " = " + N("70"), "Troisième angle du triangle : 70°."),
                 (N("\\widehat{BOD} = \\widehat{AOC}") + " = " + N("50") + "°", "Angles opposés par le sommet.")],
                "L'angle en C mesure " + N("70") + "° et BOD mesure " + N("50") + "°.", "180-(50+60)==70"),
        example("Exemple 2", "Dans un triangle ABC, l'angle en A mesure 60° et l'angle en B est le double de l'angle en C. Calculer B et C.",
                "Si C vaut x, alors B vaut 2x, et A + B + C = 180.",
                [(N("60 + 2x + x = 180"), "Somme des angles."),
                 (N("3x = 120") + " donc " + N("x = 40"), "180 − 60 = 120, divisé par 3."),
                 (N("C = 40") + "° et " + N("B = 80") + "°", "B est le double de C.")],
                N("\\widehat{C} = 40") + "° et " + N("\\widehat{B} = 80") + "°.", "60+80+40==180"),
        example("Exemple 3", "Un angle et son complémentaire ont une différence de 20°. Quelles sont leurs mesures ?",
                "Si le plus petit vaut x, le plus grand vaut x + 20 et leur somme est 90.",
                [(N("x + (x + 20) = 90") + " donc " + N("2x = 70"), "On retire 20 de 90."),
                 (N("x = 35") + " et " + N("x + 20 = 55"), "On vérifie : 35 + 55 = 90.")],
                N("35") + "° et " + N("55") + "°.", "35+55==90 and 55-35==20"),
        example("Exemple 4", "Dans un triangle rectangle isocèle, quelles sont les mesures des angles ?",
                "Un angle est droit ; les deux autres sont égaux et complémentaires.",
                [(N("90 \\div 2") + " = " + N("45"), "Chaque angle aigu mesure 45°.")],
                N("90") + "°, " + N("45") + "° et " + N("45") + "°.", "90//2==45 and 90+45+45==180"),
        warning("Dans un problème d'angles, justifie chaque pas par une propriété : « angles opposés par le sommet », « angles supplémentaires », « somme des angles du triangle ». Une valeur trouvée au rapporteur n'est qu'une vérification, pas une preuve."),
    ],
    [
        number("s4-g1", "problemes", "Dans un triangle, l'angle en A mesure 70° et l'angle en B est le triple de l'angle en C. Quelle est la mesure de C, en degrés ?", Fraction(55, 2), units=DEG, hints=["B = 3x, C = x, et A + B + C = 180."], solution=["70 + 3x + x = 180, donc 4x = 110.", "x = 27,5°."]),
        number("s4-g2", "problemes", "Deux angles supplémentaires ont une différence de 40°. Quelle est la mesure du plus grand, en degrés ?", Fraction(110), units=DEG, hints=["x + (x + 40) = 180."], solution=["2x = 140, x = 70.", "Le plus grand : 70 + 40 = 110°."]),
        number("s4-g3", "problemes", "Dans un triangle rectangle, l'un des angles aigus est le double de l'autre. Quelle est la mesure du plus petit, en degrés ?", Fraction(30), units=DEG, hints=["x + 2x = 90."], solution=["3x = 90, x = 30°."]),
        number("s4-g4", "problemes", "Deux droites se coupent. Un des angles mesure 4 fois son voisin. Quelle est la mesure du plus petit angle, en degrés ?", Fraction(36), units=DEG, hints=["x + 4x = 180 (voisins)."], solution=["5x = 180, x = 36°."]),
        choice("s4-g5", "problemes", "Dans un triangle isocèle, un angle mesure 100°. Quelle est la mesure des deux autres ?", ["40° chacun", "80° chacun", "On ne peut pas savoir"], 0, hints=["100° ne peut pas être un angle à la base."], solution=["Deux angles de 100° dépasseraient 180° : 100° est l'angle au sommet. Les angles à la base mesurent (180 − 100) ÷ 2 = 40°."], wrong={1: "80 + 80 + 100 = 260, pas 180.", 2: "Un seul cas est possible."}),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "adjacents", "Quelle est la mesure du complémentaire d'un angle de 17°, en degrés ?", Fraction(73), 1, ["90 − 17."], ["73°."], units=DEG),
    number("p2", "adjacents", "Quelle est la mesure du supplémentaire d'un angle de 17°, en degrés ?", Fraction(163), 1, ["180 − 17."], ["163°."], units=DEG),
    number("p3", "adjacents", "Quelle est la mesure du complémentaire d'un angle de 45°, en degrés ?", Fraction(45), 1, ["90 − 45."], ["45°."], units=DEG),
    number("p4", "adjacents", "Quelle est la mesure du supplémentaire d'un angle droit, en degrés ?", Fraction(90), 1, ["180 − 90."], ["90°."], units=DEG),
    number("p5", "adjacents", "Deux angles supplémentaires : l'un mesure le quadruple de l'autre. Quelle est la mesure du plus petit, en degrés ?", Fraction(36), 3, ["x + 4x = 180."], ["5x = 180, x = 36°."], units=DEG),
    number("p6", "adjacents", "Deux angles complémentaires : l'un mesure 20° de plus que l'autre. Quelle est la mesure du plus petit, en degrés ?", Fraction(35), 3, ["x + x + 20 = 90."], ["2x = 70, x = 35°."], units=DEG),
    number("p7", "adjacents", "∠AOB = 42° et ∠BOC = 31° sont adjacents. Quelle est la mesure de ∠AOC, en degrés ?", Fraction(73), 1, ["Additionne."], ["42 + 31 = 73°."], units=DEG),
    choice("p8", "adjacents", "Des angles de 65° et de 115° sont :", ["supplémentaires", "complémentaires", "opposés par le sommet"], 0, 1, ["Additionne-les."], ["65 + 115 = 180."], wrong={1: "La somme est 180, pas 90.", 2: "Des angles opposés ont la même mesure."}),
    choice("p9", "adjacents", "Des angles de 38° et de 52° sont :", ["complémentaires", "supplémentaires", "égaux"], 0, 1, ["Additionne-les."], ["38 + 52 = 90."], wrong={1: "La somme est 90, pas 180.", 2: "38 et 52 sont différents."}),
    number("p10", "opposes", "Deux droites se coupent. Un angle mesure 112°. Quelle est la mesure de l'angle opposé par le sommet, en degrés ?", Fraction(112), 1, ["Même mesure."], ["112°."], units=DEG),
    number("p11", "opposes", "Deux droites se coupent. Un angle mesure 112°. Quelle est la mesure de chacun des deux autres angles, en degrés ?", Fraction(68), 2, ["180 − 112."], ["68°."], units=DEG),
    number("p12", "opposes", "Deux droites sécantes forment un angle de 30°. Combien mesure son voisin, en degrés ?", Fraction(150), 1, ["180 − 30."], ["150°."], units=DEG),
    number("p13", "opposes", "Deux angles opposés par le sommet mesurent 2x + 10 et 4x − 30. Quelle est la valeur de x ?", Fraction(20), 3, ["2x + 10 = 4x − 30."], ["40 = 2x, x = 20."]),
    number("p14", "opposes", "Deux droites sécantes forment quatre angles. Si un angle est droit, combien d'angles sont droits ?", Fraction(4), 2, ["Voisin et opposé."], ["Les quatre."]),
    choice("p15", "opposes", "Léa dit : « deux angles voisins formés par deux droites sécantes sont égaux ». Qu'en penses-tu ?", ["Non : ils sont supplémentaires, égaux seulement s'ils mesurent 90°", "Oui, toujours", "Non, ils sont complémentaires"], 0, 2, ["Voisins : angle plat."], ["Des angles voisins forment un angle plat : leur somme est 180°."], wrong={1: "Ce sont les angles opposés qui sont égaux.", 2: "Leur somme est 180°, pas 90°."}),
    number("p16", "triangle", "Un triangle a des angles de 40° et de 60°. Quelle est la mesure du troisième, en degrés ?", Fraction(80), 1, ["180 − 100."], ["80°."], units=DEG),
    number("p17", "triangle", "Un triangle a des angles de 23° et de 112°. Quelle est la mesure du troisième, en degrés ?", Fraction(45), 2, ["180 − 135."], ["45°."], units=DEG),
    number("p18", "triangle", "Un triangle rectangle a un angle aigu de 49°. Quelle est la mesure de l'autre, en degrés ?", Fraction(41), 1, ["90 − 49."], ["41°."], units=DEG),
    number("p19", "triangle", "Un triangle isocèle a un angle au sommet de 50°. Quelle est la mesure d'un angle à la base, en degrés ?", Fraction(65), 2, ["(180 − 50) ÷ 2."], ["65°."], units=DEG),
    number("p20", "triangle", "Un triangle isocèle a un angle à la base de 72°. Quelle est la mesure de l'angle au sommet, en degrés ?", Fraction(36), 2, ["180 − 144."], ["36°."], units=DEG),
    number("p21", "triangle", "Quelle est la mesure d'un angle d'un triangle équilatéral, en degrés ?", Fraction(60), 1, ["180 ÷ 3."], ["60°."], units=DEG),
    number("p22", "triangle", "Dans un triangle, les angles sont dans le rapport 1, 2 et 3. Quelle est la mesure du plus grand, en degrés ?", Fraction(90), 3, ["1 + 2 + 3 = 6 parts."], ["180 ÷ 6 = 30 ; 3 × 30 = 90°."], units=DEG),
    number("p23", "triangle", "Un triangle a trois angles égaux à x. Quelle est la valeur de x, en degrés ?", Fraction(60), 1, ["3x = 180."], ["60°."], units=DEG),
    choice("p24", "triangle", "Un triangle peut-il avoir un angle de 95°, un de 50° et un de 40° ?", ["Non, la somme est 185°", "Oui, la somme est 180°", "Oui, s'il est rectangle"], 0, 2, ["Additionne les trois."], ["95 + 50 + 40 = 185, pas 180."], wrong={1: "La somme est 185.", 2: "Il n'y a pas d'angle droit ici."}),
    choice("p25", "triangle", "Quel triangle a deux angles aigus complémentaires ?", ["Un triangle rectangle", "Un triangle équilatéral", "Un triangle obtusangle"], 0, 2, ["Un angle fait 90°."], ["Dans un triangle rectangle, les deux autres angles font 90°."], wrong={1: "Ses angles font 60° chacun.", 2: "Un angle dépasse 90°."}),
    number("p26", "problemes", "Dans un triangle, un angle mesure 84° et un autre est le double du troisième. Quelle est la mesure du plus petit, en degrés ?", Fraction(32), 3, ["x + 2x = 96."], ["180 − 84 = 96.", "3x = 96, x = 32°."], units=DEG),
    number("p27", "problemes", "Deux angles supplémentaires ont une différence de 30°. Quelle est la mesure du plus petit, en degrés ?", Fraction(75), 3, ["x + x + 30 = 180."], ["2x = 150, x = 75°."], units=DEG),
    number("p28", "problemes", "Deux droites se coupent. Un des angles mesure 3 fois son voisin. Quelle est la mesure du plus petit, en degrés ?", Fraction(45), 3, ["x + 3x = 180."], ["x = 45°."], units=DEG),
    number("p29", "problemes", "Dans un triangle isocèle, un angle mesure 80°. Si c'est un angle à la base, quelle est la mesure de l'angle au sommet, en degrés ?", Fraction(20), 3, ["180 − 160."], ["20°."], units=DEG),
    number("p30", "problemes", "Un triangle rectangle a un angle aigu qui mesure 4 fois l'autre. Quelle est la mesure du plus grand angle aigu, en degrés ?", Fraction(72), 3, ["x + 4x = 90."], ["5x = 90, x = 18 ; 4x = 72°."], units=DEG),
    choice("p31", "problemes", "Karim dit : « un triangle a des angles de 60°, 60° et 70° ». Qu'en penses-tu ?", ["Impossible : la somme est 190°", "Possible", "Possible si c'est un triangle isocèle"], 0, 1, ["Additionne."], ["60 + 60 + 70 = 190."], wrong={1: "La somme vaut 190, pas 180.", 2: "Un triangle isocèle a aussi une somme de 180."}),
    number("p32", "problemes", "Dans un triangle ABC, A = 35° et B = 85°. Quelle est la mesure de l'angle extérieur en C (supplémentaire de C), en degrés ?", Fraction(120), 3, ["Calcule C d'abord."], ["C = 180 − 120 = 60°.", "L'angle extérieur : 180 − 60 = 120°."], units=DEG),
]

SUMMARY = [
    definition("Angles adjacents, complémentaires, supplémentaires", "Adjacents : même sommet, un côté commun, de part et d'autre. Complémentaires : somme 90°. Supplémentaires : somme 180°."),
    rule("Angles opposés par le sommet", "Deux droites sécantes forment quatre angles. Les angles opposés par le sommet ont la même mesure ; les angles voisins sont supplémentaires. La somme des quatre angles est 360°."),
    rule("Somme des angles d'un triangle", "Dans un triangle, la somme des angles est 180°. Triangle rectangle : les deux angles aigus font 90°. Équilatéral : 60° chacun. Isocèle : les deux angles à la base sont égaux."),
    para("Les erreurs à éviter : confondre complémentaire (90°) et supplémentaire (180°) ; croire que des angles voisins sont égaux ; oublier de justifier chaque pas ; accepter un triangle dont la somme des angles n'est pas 180°."),
]

CONCEPTS = {
    "adjacents": ("Angles adjacents, complémentaires, supplémentaires", "adjacents"),
    "opposes": ("Angles opposés par le sommet", "opposes"),
    "triangle": ("Somme des angles d'un triangle", "triangle"),
    "problemes": ("Problèmes avec des angles", "problemes"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    # 1. the complement
    x = rng.randint(5, 85)
    questions.append(number("a1", "adjacents", f"Quelle est la mesure du complémentaire d'un angle de {x}°, en degrés ?", Fraction(90 - x), 1, ["90 moins l'angle."], [f"90 − {x} = {90 - x}°."], units=DEG))
    # 2. the supplement
    x = rng.randint(10, 170)
    questions.append(number("a2", "adjacents", f"Quelle est la mesure du supplémentaire d'un angle de {x}°, en degrés ?", Fraction(180 - x), 1, ["180 moins l'angle."], [f"180 − {x} = {180 - x}°."], units=DEG))
    # 3. complementary, supplementary or neither
    a = rng.randint(10, 80)
    kind = rng.choice([0, 1, 2])
    b = [90 - a, 180 - a, 90 - a + rng.choice([-7, 7, 10, -10])][kind]
    if kind == 2 and (a + b in (90, 180) or b <= 0):
        b = 90 - a + 11
    options = ["complémentaires", "supplémentaires", "ni l'un ni l'autre"]
    questions.append(choice("a3", "adjacents", f"Des angles de {a}° et de {b}° sont :", options, kind if kind < 2 else 2, 2, ["Additionne les deux mesures."], [f"{a} + {b} = {a + b}."]))
    # 4. an adjacent supplement in a figure
    x = rng.randint(25, 155)
    questions.append(number("a4", "adjacents", f"A, O et B sont alignés, O entre A et B. ∠AOC = {x}°. Quelle est la mesure de ∠COB, en degrés ?", Fraction(180 - x), 2, ["Les deux angles sont supplémentaires."], [f"180 − {x} = {180 - x}°."], units=DEG))
    # 5. opposite angles
    x = rng.randint(15, 165)
    questions.append(number("a5", "opposes", f"Deux droites se coupent en O. ∠AOC = {x}°. Quelle est la mesure de l'angle opposé par le sommet ∠BOD, en degrés ?", Fraction(x), 1, ["Angles opposés par le sommet."], ["Même mesure."], units=DEG))
    # 6. the neighbour
    x = rng.randint(15, 165)
    while x == 90:
        x = rng.randint(15, 165)
    questions.append(number("a6", "opposes", f"Deux droites se coupent en O. ∠AOC = {x}°. Quelle est la mesure de ∠AOD, l'angle voisin, en degrés ?", Fraction(180 - x), 2, ["Angles voisins : supplémentaires."], [f"180 − {x} = {180 - x}°."], units=DEG))
    # 7. the third angle of a triangle
    a, b = rng.randint(20, 80), rng.randint(20, 80)
    questions.append(number("a7", "triangle", f"Un triangle a deux angles de {a}° et de {b}°. Quelle est la mesure du troisième, en degrés ?", Fraction(180 - a - b), 1, ["180 moins la somme."], [f"{a} + {b} = {a + b}.", f"180 − {a + b} = {180 - a - b}°."], units=DEG))
    # 8. the acute angle of a right triangle
    x = rng.randint(10, 80)
    questions.append(number("a8", "triangle", f"Un triangle rectangle a un angle aigu de {x}°. Quelle est la mesure de l'autre angle aigu, en degrés ?", Fraction(90 - x), 1, ["Les deux angles aigus font 90°."], [f"90 − {x} = {90 - x}°."], units=DEG))
    # 9. the base angle of an isosceles triangle
    top = 2 * rng.randint(10, 80)
    questions.append(number("a9", "triangle", f"Un triangle isocèle a un angle au sommet de {top}°. Quelle est la mesure d'un angle à la base, en degrés ?", Fraction(180 - top, 2), 2, ["(180 − angle au sommet) ÷ 2."], [f"180 − {top} = {180 - top}.", f"{180 - top} ÷ 2 = {(180 - top) // 2}°."], units=DEG))
    # 10. an angle ratio in a triangle
    k = rng.choice([2, 3])
    third = rng.randint(30, 100)
    rest = 180 - third
    while rest % (k + 1):
        third = rng.randint(30, 100)
        rest = 180 - third
    questions.append(number("a10", "problemes", f"Dans un triangle, un angle mesure {third}° et un des deux autres est {k} fois le troisième. Quelle est la mesure du plus petit des deux, en degrés ?", Fraction(rest, k + 1), 3, [f"x + {k}x = {rest}."],
                            [f"{k + 1}x = {rest}, donc x = {rest // (k + 1)}°."], units=DEG))
    # 11. supplementary angles with a difference
    diff = rng.choice([10, 20, 30, 40, 50, 60])
    questions.append(number("a11", "problemes", f"Deux angles supplémentaires ont une différence de {diff}°. Quelle est la mesure du plus grand, en degrés ?", Fraction(180 + diff, 2), 3, ["x + (x + différence) = 180."], [f"2x = {180 - diff}, x = {(180 - diff) // 2}.", f"Le plus grand : {(180 + diff) // 2}°."], units=DEG))
    # 12. opposite angles with x
    x = rng.randint(12, 40)
    a, b = rng.choice([(2, 3), (3, 4), (2, 5), (4, 5)])
    # a*x + p = b*x - q with the same measure: choose p so that the equation has the solution x
    p = rng.randint(1, 20)
    q = (b - a) * x - p
    while q <= 0:
        p = rng.randint(1, 20)
        q = (b - a) * x - p
    questions.append(number("a12", "opposes", f"Deux angles opposés par le sommet mesurent {a}x + {p} et {b}x − {q}. Quelle est la valeur de x ?", Fraction(x), 3, ["Les deux angles sont égaux."], [f"{a}x + {p} = {b}x − {q}, donc {p + q} = {b - a}x et x = {x}."]))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=6, title="Les angles", language="fr",
    intro="Une porte qui s'ouvre, deux routes qui se croisent, les coins d'un triangle : on rencontre des angles partout. "
          "Ce chapitre t'apprend les angles adjacents, complémentaires et supplémentaires, les angles opposés par le sommet et la somme des angles d'un triangle.",
    objectives=["Reconnaître des angles adjacents, complémentaires et supplémentaires et calculer leurs mesures.",
                "Utiliser que les angles opposés par le sommet ont la même mesure.",
                "Calculer l'angle manquant d'un triangle avec la somme des angles.",
                "Résoudre des problèmes d'angles en justifiant chaque étape."],
    prerequisites=[{"text": "Connaître les angles, leur mesure en degrés, l'angle droit et l'angle plat.", "chapter": "sn-6e-angles"},
                   {"text": "Résoudre une équation simple.", "chapter": "sn-5e-relatifs"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Sixth chapter of the Senegal Cinquième course. Its contents follow the angles lesson of the Côte d'Ivoire Cinquième programme (adjacent, complementary and supplementary angles, opposite angles, the sum of the angles of a triangle), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. The figures are drawn by the app. It has not been checked against the official Senegalese programme.",
)
