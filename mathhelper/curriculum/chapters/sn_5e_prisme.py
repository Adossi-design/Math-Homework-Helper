"""Cinquième, Prisme droit: the eleventh chapter of the Senegal Cinquième course, written in French.

The contents follow the lesson "Prisme droit" of the Côte d'Ivoire Cinquième programme (faces, edges and vertices, the net, the lateral and the total area, and the volume), which was read for
this chapter. Every explanation, example and exercise was written independently, with our own numbers. It builds on the Sixième chapter on solids. A solid cannot be drawn faithfully in this
chapter's flat figures, so no drawing is claimed: the prism is described in words. Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and
each worked example carries a "verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .kit import N, d, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-5e-prisme"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")
CM, CM2, CM3 = ["cm"], ["cm2", "cm²"], ["cm3", "cm³"]

# ----- Section 1: elements -----
S1 = Section(
    "elements", "Le prisme droit et ses éléments", 20, "elements",
    "Reconnaître un prisme droit, nommer ses faces, ses arêtes et ses sommets, et les compter à partir de la base.",
    [
        para("Une boîte de craie, une tente en forme de toit ou une règle à section triangulaire sont des prismes droits. Un prisme droit est fait de deux bases identiques et parallèles, reliées par des rectangles."),
        definition("Prisme droit",
                   "Un prisme droit est un solide qui a deux faces parallèles et superposables, les bases, qui sont des polygones, et dont les autres faces, les faces latérales, sont des rectangles. "
                   "La hauteur est la longueur des arêtes qui relient les deux bases. Le pavé droit est un prisme droit dont les bases sont des rectangles."),
        rule("Compter les éléments",
             "Un prisme droit dont la base a n côtés a " + N("n + 2") + " faces (n faces latérales et 2 bases), " + N("3 \\times n") + " arêtes et " + N("2 \\times n") + " sommets."),
        example("Exemple 1", "Un prisme droit a pour base un triangle. Combien a-t-il de faces, d'arêtes et de sommets ?",
                "Ici n = 3 : on applique les trois formules.",
                [(N("3 + 2") + " = " + N("5"), "Faces : 3 rectangles et 2 triangles."),
                 (N("3 \\times 3") + " = " + N("9"), "Arêtes."),
                 (N("2 \\times 3") + " = " + N("6"), "Sommets.")],
                N("5") + " faces, " + N("9") + " arêtes et " + N("6") + " sommets.", "3+2==5 and 3*3==9 and 2*3==6"),
        example("Exemple 2", "Un prisme droit a pour base un hexagone. Combien a-t-il d'arêtes ?",
                "Ici n = 6.",
                [(N("3 \\times 6") + " = " + N("18"), "Six arêtes en haut, six en bas et six verticales.")],
                N("18") + " arêtes.", "3*6==18"),
        example("Exemple 3", "Un prisme droit a 12 arêtes. Quelle est sa base ?",
                "Les arêtes sont au nombre de 3 × n : on cherche n.",
                [(N("12 \\div 3") + " = " + N("4"), "La base a 4 côtés."),
                 ("Un polygone à 4 côtés est un quadrilatère", "La base est un quadrilatère, et le solide a " + N("4 + 2") + " = " + N("6") + " faces.")],
                "La base est un quadrilatère.", "12//3==4 and 4+2==6"),
        example("Exemple 4", "Vérifier la relation sommets − arêtes + faces pour un prisme à base triangulaire.",
                "On a 6 sommets, 9 arêtes et 5 faces.",
                [(N("6 - 9 + 5") + " = " + N("2"), "Le résultat est toujours 2 pour un prisme.")],
                N("2") + ".", "6-9+5==2"),
        warning("Les bases d'un prisme droit ne sont pas toujours en haut et en bas : ce sont les deux faces parallèles et identiques, quelle que soit la façon dont le solide est posé. Et dans un prisme droit, les faces latérales sont des rectangles, pas des parallélogrammes."),
    ],
    [
        number("s1-g1", "elements", "Un prisme droit a pour base un pentagone. Combien a-t-il de faces ?", Fraction(7), hints=["n + 2."], solution=["5 + 2 = 7."]),
        number("s1-g2", "elements", "Un prisme droit a pour base un pentagone. Combien a-t-il d'arêtes ?", Fraction(15), hints=["3 × n."], solution=["3 × 5 = 15."]),
        number("s1-g3", "elements", "Un prisme droit a pour base un pentagone. Combien a-t-il de sommets ?", Fraction(10), hints=["2 × n."], solution=["2 × 5 = 10."]),
        number("s1-g4", "elements", "Un prisme droit a 21 arêtes. Combien de côtés a sa base ?", Fraction(7), hints=["21 ÷ 3."], solution=["21 ÷ 3 = 7."]),
        choice("s1-g5", "elements", "Quelle est la forme des faces latérales d'un prisme droit ?", ["Des rectangles", "Des triangles", "Des cercles"], 0, hints=["Pense à une boîte."], solution=["Des rectangles."], wrong={1: "Les triangles peuvent être les bases, pas les faces latérales.", 2: "Un prisme n'a pas de face ronde."}),
    ])

# ----- Section 2: net and lateral area -----
S2 = Section(
    "patron", "Le patron et l'aire latérale", 22, "patron",
    "Décrire le patron d'un prisme droit et calculer son aire latérale.",
    [
        para("Si on découpe un prisme droit le long de certaines arêtes et qu'on l'aplatit, on obtient son patron. Les faces latérales forment une grande bande rectangulaire, avec une base collée en haut et une en bas."),
        rule("Aire latérale",
             "Les faces latérales, mises côte à côte, forment un rectangle de longueur égale au périmètre de la base et de largeur égale à la hauteur. " + N("A_{lat} = P_{base} \\times h") + "."),
        example("Exemple 1", "Un prisme droit a pour base un rectangle de 6 cm sur 4 cm, et sa hauteur est de 10 cm. Quelle est son aire latérale ?",
                "On calcule d'abord le périmètre de la base.",
                [(N("2 \\times (6 + 4)") + " = " + N("20"), "Périmètre de la base : 20 cm."),
                 (N("20 \\times 10") + " = " + N("200"), "Aire latérale.")],
                N("200") + " cm².", "2*(6+4)==20 and 20*10==200"),
        example("Exemple 2", "La base est un triangle dont les côtés mesurent 3 cm, 4 cm et 5 cm. La hauteur du prisme est de 8 cm. Quelle est l'aire latérale ?",
                "Le périmètre est la somme des trois côtés.",
                [(N("3 + 4 + 5") + " = " + N("12"), "Périmètre."),
                 (N("12 \\times 8") + " = " + N("96"), "Aire latérale.")],
                N("96") + " cm².", "3+4+5==12 and 12*8==96"),
        example("Exemple 3", "Un prisme droit a une aire latérale de 150 cm² et une hauteur de 5 cm. Quel est le périmètre de sa base ?",
                "On inverse la formule.",
                [(N("150 \\div 5") + " = " + N("30"), "Périmètre : 30 cm.")],
                N("30") + " cm.", "150//5==30"),
        example("Exemple 4", "Combien de rectangles contient le patron d'un prisme à base hexagonale, et combien de faces au total ?",
                "Il y a un rectangle par côté de la base, et deux bases.",
                [(N("6") + " rectangles", "Faces latérales."),
                 (N("6 + 2") + " = " + N("8"), "Faces du patron.")],
                N("6") + " rectangles et " + N("8") + " faces.", "6+2==8"),
        warning("L'aire latérale n'inclut pas les bases. Pour l'obtenir, multiplie le périmètre de la base par la hauteur, pas l'aire de la base."),
    ],
    [
        number("s2-g1", "patron", "La base d'un prisme droit est un rectangle de 8 cm sur 5 cm, et sa hauteur est de 7 cm. Quelle est son aire latérale, en cm² ?", Fraction(182), units=CM2, hints=["Périmètre × hauteur."], solution=["2 × 13 = 26.", "26 × 7 = 182 cm²."]),
        number("s2-g2", "patron", "La base d'un prisme droit est un triangle de périmètre 15 cm, et sa hauteur est de 6 cm. Quelle est son aire latérale, en cm² ?", Fraction(90), units=CM2, hints=["15 × 6."], solution=["90 cm²."]),
        number("s2-g3", "patron", "Un prisme droit a une aire latérale de 240 cm² et une hauteur de 12 cm. Quel est le périmètre de sa base, en cm ?", Fraction(20), units=CM, hints=["240 ÷ 12."], solution=["20 cm."]),
        number("s2-g4", "patron", "Combien de rectangles a le patron d'un prisme à base carrée ?", Fraction(4), hints=["Un par côté."], solution=["4."]),
    ])

# ----- Section 3: total area -----
S3 = Section(
    "aire", "L'aire totale", 22, "aire",
    "Calculer l'aire totale d'un prisme droit en ajoutant l'aire latérale et les deux bases.",
    [
        para("Pour peindre une boîte ou la recouvrir de papier, il faut connaître l'aire de toutes ses faces."),
        rule("Aire totale",
             N("A_{tot} = A_{lat} + 2 \\times A_{base}") + ". Pour un pavé droit de longueur L, de largeur l et de hauteur h : " + N("A = 2 \\times (L \\times l + L \\times h + l \\times h)") + "."),
        example("Exemple 1", "Un prisme droit a une base de 24 cm² et une aire latérale de 120 cm². Quelle est son aire totale ?",
                "On ajoute deux fois la base à l'aire latérale.",
                [(N("2 \\times 24") + " = " + N("48"), "Les deux bases."),
                 (N("120 + 48") + " = " + N("168"), "Aire totale.")],
                N("168") + " cm².", "2*24==48 and 120+48==168"),
        example("Exemple 2", "Quelle est l'aire totale d'un pavé droit de 5 cm, 4 cm et 3 cm ?",
                "On additionne les trois produits, puis on double.",
                [(N("5 \\times 4 + 5 \\times 3 + 4 \\times 3") + " = " + N("20 + 15 + 12") + " = " + N("47"), "Somme des trois types de faces."),
                 (N("2 \\times 47") + " = " + N("94"), "On double.")],
                N("94") + " cm².", "5*4+5*3+4*3==47 and 2*47==94"),
        example("Exemple 3", "Un prisme droit a pour base un triangle rectangle de côtés 6 cm et 8 cm autour de l'angle droit, et sa hauteur est de 10 cm. Le troisième côté du triangle mesure 10 cm. Quelle est son aire totale ?",
                "On calcule l'aire de la base, le périmètre, puis l'aire totale.",
                [(N("6 \\times 8 \\div 2") + " = " + N("24"), "Aire d'une base."),
                 (N("6 + 8 + 10") + " = " + N("24"), "Périmètre de la base."),
                 (N("24 \\times 10") + " = " + N("240"), "Aire latérale."),
                 (N("240 + 2 \\times 24") + " = " + N("288"), "Aire totale.")],
                N("288") + " cm².", "6*8//2==24 and 6+8+10==24 and 24*10==240 and 240+48==288"),
        example("Exemple 4", "Combien de papier faut-il pour recouvrir entièrement un cube de 3 cm d'arête ?",
                "Un cube a six faces carrées identiques.",
                [(N("3 \\times 3") + " = " + N("9"), "Une face."),
                 (N("6 \\times 9") + " = " + N("54"), "Six faces.")],
                N("54") + " cm².", "3*3==9 and 6*9==54"),
        warning("N'oublie pas les deux bases : l'aire totale est l'aire latérale plus deux fois l'aire d'une base, et pas une seule."),
    ],
    [
        number("s3-g1", "aire", "Un prisme droit a une base de 30 cm² et une aire latérale de 200 cm². Quelle est son aire totale, en cm² ?", Fraction(260), units=CM2, hints=["Lat + 2 bases."], solution=["200 + 60 = 260 cm²."]),
        number("s3-g2", "aire", "Quelle est l'aire totale d'un pavé droit de 6 cm, 5 cm et 2 cm, en cm² ?", Fraction(104), units=CM2, hints=["2 × (30 + 12 + 10)."], solution=["30 + 12 + 10 = 52.", "2 × 52 = 104 cm²."]),
        number("s3-g3", "aire", "Quelle est l'aire totale d'un cube de 5 cm d'arête, en cm² ?", Fraction(150), units=CM2, hints=["6 faces."], solution=["6 × 25 = 150 cm²."]),
        number("s3-g4", "aire", "Un prisme droit a une aire totale de 150 cm² et une aire latérale de 110 cm². Quelle est l'aire d'une base, en cm² ?", Fraction(20), units=CM2, hints=["Total − lat = 2 bases."], solution=["150 − 110 = 40.", "40 ÷ 2 = 20 cm²."]),
    ])

# ----- Section 4: volume -----
S4 = Section(
    "volume", "Le volume", 24, "volume",
    "Calculer le volume d'un prisme droit à partir de l'aire de sa base et de sa hauteur, et convertir un volume en litres.",
    [
        para("Le volume mesure la place occupée par un solide, ou la quantité de liquide qu'il peut contenir."),
        rule("Volume",
             "Le volume d'un prisme droit est le produit de l'aire de sa base par sa hauteur : " + N("V = A_{base} \\times h") + ". Pour un pavé droit : " + N("V = L \\times l \\times h") + ". "
             "On rappelle que " + N("1 \\text{ dm}^3 = 1 \\text{ L}") + " et que " + N("1\\,000 \\text{ cm}^3 = 1 \\text{ L}") + "."),
        example("Exemple 1", "Un pavé droit mesure 8 cm, 5 cm et 3 cm. Quel est son volume ?",
                "On multiplie les trois dimensions.",
                [(N("8 \\times 5 \\times 3") + " = " + N("120"), "Volume.")],
                N("120") + " cm³.", "8*5*3==120"),
        example("Exemple 2", "La base d'un prisme droit est un triangle de base 6 cm et de hauteur 4 cm. La hauteur du prisme est de 10 cm. Quel est son volume ?",
                "On calcule l'aire de la base, puis on multiplie par la hauteur du prisme.",
                [(N("6 \\times 4 \\div 2") + " = " + N("12"), "Aire de la base."),
                 (N("12 \\times 10") + " = " + N("120"), "Volume.")],
                N("120") + " cm³.", "6*4//2==12 and 12*10==120"),
        example("Exemple 3", "Un prisme droit a un volume de 360 cm³ et une base de 45 cm². Quelle est sa hauteur ?",
                "On inverse la formule.",
                [(N("360 \\div 45") + " = " + N("8"), "Hauteur.")],
                N("8") + " cm.", "360//45==8"),
        example("Exemple 4", "Un aquarium en forme de pavé droit mesure 50 cm de long, 30 cm de large et 40 cm de haut. Combien de litres d'eau contient-il quand il est plein ?",
                "On calcule le volume en cm³, puis on convertit.",
                [(N("50 \\times 30 \\times 40") + " = " + N("60000"), "Volume en cm³."),
                 (N("60000 \\div 1000") + " = " + N("60"), "En litres.")],
                N("60") + " L.", "50*30*40==60000 and 60000//1000==60"),
        warning("Ne confonds pas l'aire (en cm²) et le volume (en cm³). Et la hauteur du prisme n'est pas celle du triangle de la base : ce sont deux longueurs différentes."),
    ],
    [
        number("s4-g1", "volume", "Quel est le volume d'un pavé droit de 10 cm, 6 cm et 4 cm, en cm³ ?", Fraction(240), units=CM3, hints=["Les trois dimensions."], solution=["10 × 6 × 4 = 240 cm³."]),
        number("s4-g2", "volume", "Un prisme droit a une base de 35 cm² et une hauteur de 6 cm. Quel est son volume, en cm³ ?", Fraction(210), units=CM3, hints=["Base × hauteur."], solution=["35 × 6 = 210 cm³."]),
        number("s4-g3", "volume", "Un prisme droit a un volume de 500 cm³ et une hauteur de 10 cm. Quelle est l'aire de sa base, en cm² ?", Fraction(50), units=CM2, hints=["500 ÷ 10."], solution=["50 cm²."]),
        number("s4-g4", "volume", "Un réservoir a un volume de 8 000 cm³. Combien de litres contient-il ?", Fraction(8), units=["L", "l", "litres"], hints=["1 000 cm³ = 1 L."], solution=["8 000 ÷ 1 000 = 8 L."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "elements", "Un prisme droit a pour base un octogone. Combien a-t-il de faces ?", Fraction(10), 1, ["8 + 2."], ["10."]),
    number("p2", "elements", "Un prisme droit a pour base un octogone. Combien a-t-il d'arêtes ?", Fraction(24), 1, ["3 × 8."], ["24."]),
    number("p3", "elements", "Un prisme droit a pour base un octogone. Combien a-t-il de sommets ?", Fraction(16), 1, ["2 × 8."], ["16."]),
    number("p4", "elements", "Un prisme droit a 30 arêtes. Combien de côtés a sa base ?", Fraction(10), 2, ["30 ÷ 3."], ["10."]),
    number("p5", "elements", "Un prisme droit a 12 sommets. Combien de faces a-t-il ?", Fraction(8), 2, ["n = 12 ÷ 2 = 6, puis n + 2."], ["n = 6.", "6 + 2 = 8 faces."]),
    choice("p6", "elements", "Un pavé droit est-il un prisme droit ?", ["Oui, de base rectangulaire", "Non"], 0, 1, ["Deux rectangles parallèles reliés par des rectangles."], ["Oui."], wrong={1: "Il a deux bases rectangulaires et quatre faces latérales rectangulaires."}),
    choice("p7", "elements", "Quelle forme ont les bases d'un prisme droit qui a 5 faces ?", ["Des triangles", "Des carrés", "Des pentagones"], 0, 2, ["n + 2 = 5."], ["n = 3 : triangles."], wrong={1: "Une base carrée donne 6 faces.", 2: "Une base pentagonale donne 7 faces."}),
    number("p8", "patron", "La base d'un prisme droit est un carré de 5 cm de côté, et sa hauteur est de 9 cm. Quelle est son aire latérale, en cm² ?", Fraction(180), 1, ["20 × 9."], ["180 cm²."], units=CM2),
    number("p9", "patron", "La base d'un prisme droit est un rectangle de 12 cm sur 7 cm, et sa hauteur est de 5 cm. Quelle est son aire latérale, en cm² ?", Fraction(190), 1, ["38 × 5."], ["2 × 19 = 38.", "38 × 5 = 190 cm²."], units=CM2),
    number("p10", "patron", "La base d'un prisme droit est un triangle de côtés 5 cm, 12 cm et 13 cm, et sa hauteur est de 4 cm. Quelle est son aire latérale, en cm² ?", Fraction(120), 2, ["Périmètre : 30."], ["30 × 4 = 120 cm²."], units=CM2),
    number("p11", "patron", "Un prisme droit a une aire latérale de 360 cm² et un périmètre de base de 36 cm. Quelle est sa hauteur, en cm ?", Fraction(10), 2, ["360 ÷ 36."], ["10 cm."], units=CM),
    number("p12", "patron", "Combien de rectangles a le patron d'un prisme dont la base a 9 côtés ?", Fraction(9), 1, ["Un par côté."], ["9."]),
    number("p13", "aire", "Un prisme droit a une base de 18 cm² et une aire latérale de 96 cm². Quelle est son aire totale, en cm² ?", Fraction(132), 1, ["96 + 36."], ["132 cm²."], units=CM2),
    number("p14", "aire", "Quelle est l'aire totale d'un pavé droit de 4 cm, 3 cm et 2 cm, en cm² ?", Fraction(52), 2, ["2 × (12 + 8 + 6)."], ["2 × 26 = 52 cm²."], units=CM2),
    number("p15", "aire", "Quelle est l'aire totale d'un cube de 10 cm d'arête, en cm² ?", Fraction(600), 1, ["6 × 100."], ["600 cm²."], units=CM2),
    number("p16", "aire", "Quelle est l'aire totale d'un cube de 4 cm d'arête, en cm² ?", Fraction(96), 1, ["6 × 16."], ["96 cm²."], units=CM2),
    number("p17", "aire", "Un prisme droit a une aire totale de 200 cm² et deux bases de 25 cm² chacune. Quelle est son aire latérale, en cm² ?", Fraction(150), 2, ["200 − 50."], ["150 cm²."], units=CM2),
    number("p18", "aire", "Un prisme droit à base de triangle rectangle de côtés 3 cm, 4 cm et 5 cm autour de l'angle droit et de l'hypoténuse a une hauteur de 10 cm. Quelle est son aire totale, en cm² ?", Fraction(132), 3, ["Base : 6. Périmètre : 12."], ["Latérale : 12 × 10 = 120.", "Total : 120 + 2 × 6 = 132 cm²."], units=CM2),
    number("p19", "volume", "Quel est le volume d'un pavé droit de 7 cm, 5 cm et 2 cm, en cm³ ?", Fraction(70), 1, ["7 × 5 × 2."], ["70 cm³."], units=CM3),
    number("p20", "volume", "Quel est le volume d'un cube de 6 cm d'arête, en cm³ ?", Fraction(216), 1, ["6 × 6 × 6."], ["216 cm³."], units=CM3),
    number("p21", "volume", "Un prisme droit a une base de 28 cm² et une hauteur de 15 cm. Quel est son volume, en cm³ ?", Fraction(420), 1, ["28 × 15."], ["420 cm³."], units=CM3),
    number("p22", "volume", "Un prisme droit a un volume de 720 cm³ et une base de 60 cm². Quelle est sa hauteur, en cm ?", Fraction(12), 2, ["720 ÷ 60."], ["12 cm."], units=CM),
    number("p23", "volume", "La base d'un prisme droit est un triangle de base 10 cm et de hauteur 6 cm, et la hauteur du prisme est de 8 cm. Quel est son volume, en cm³ ?", Fraction(240), 2, ["Base : 30."], ["10 × 6 ÷ 2 = 30.", "30 × 8 = 240 cm³."], units=CM3),
    number("p24", "volume", "Une citerne a un volume de 12 000 cm³. Combien de litres contient-elle ?", Fraction(12), 2, ["÷ 1 000."], ["12 L."], units=["L", "l", "litres"]),
    number("p25", "volume", "Un bassin en forme de pavé droit mesure 2 m de long, 1 m de large et 0,5 m de profondeur. Quel est son volume, en m³ ?", Fraction(1), 2, ["2 × 1 × 0,5."], ["1 m³."], units=["m3", "m³"]),
    number("p26", "volume", "Un bassin de 1 m³ peut contenir combien de litres d'eau ?", Fraction(1000), 2, ["1 m³ = 1 000 dm³."], ["1 000 L."], units=["L", "l", "litres"]),
    number("p27", "volume", "Un pavé droit a un volume de 96 cm³, une longueur de 8 cm et une largeur de 4 cm. Quelle est sa hauteur, en cm ?", Fraction(3), 2, ["96 ÷ 32."], ["8 × 4 = 32.", "96 ÷ 32 = 3 cm."], units=CM),
    number("p28", "volume", "Une boîte de 20 cm sur 10 cm sur 5 cm est remplie de sucre en cubes de 1 cm d'arête. Combien de cubes y a-t-il ?", Fraction(1000), 2, ["Le volume en cm³."], ["20 × 10 × 5 = 1 000 cubes."]),
    number("p29", "volume", "Un prisme droit de volume 300 cm³ a une base de 25 cm². On le remplit d'eau à moitié de sa hauteur. Quel volume d'eau contient-il, en cm³ ?", Fraction(150), 3, ["La moitié du volume."], ["300 ÷ 2 = 150 cm³."], units=CM3),
    number("p30", "volume", "Deux prismes droits ont la même hauteur de 10 cm. Le premier a une base de 12 cm², le second une base de 20 cm². Quelle est la différence de volume, en cm³ ?", Fraction(80), 3, ["Calcule chaque volume."], ["120 et 200.", "200 − 120 = 80 cm³."], units=CM3),
    number("p31", "aire", "Une tente a la forme d'un prisme droit dont la base est un triangle de côtés 2 m, 2 m et 2 m, et dont la longueur est de 3 m. Quelle est son aire latérale, en m² ?", Fraction(18), 3, ["Périmètre × longueur."], ["Périmètre 6 m.", "6 × 3 = 18 m²."], units=["m2", "m²"]),
    number("p32", "volume", "Un cube a une arête de 2 cm. On double l'arête. Par combien est multiplié son volume ?", Fraction(8), 3, ["4³ ÷ 2³ ou 2³."], ["2 cm : 8 cm³. 4 cm : 64 cm³.", "64 ÷ 8 = 8."]),
]

SUMMARY = [
    definition("Prisme droit", "Deux bases parallèles et identiques, et des faces latérales rectangulaires. Si la base a n côtés : n + 2 faces, 3n arêtes et 2n sommets."),
    rule("Aires", "Aire latérale : périmètre de la base × hauteur. Aire totale : aire latérale + 2 × aire de la base. Cube d'arête a : 6 × a × a."),
    rule("Volume", "V = aire de la base × hauteur. Pavé droit : L × l × h. 1 000 cm³ = 1 L = 1 dm³."),
    para("Les erreurs à éviter : oublier les deux bases dans l'aire totale ; confondre la hauteur du prisme et celle du triangle de la base ; mélanger cm², cm³ et litres."),
]

CONCEPTS = {
    "elements": ("Faces, arêtes et sommets", "elements"),
    "patron": ("Patron et aire latérale", "patron"),
    "aire": ("Aire totale", "aire"),
    "volume": ("Volume", "volume"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    names = {3: "un triangle", 4: "un quadrilatère", 5: "un pentagone", 6: "un hexagone", 7: "un heptagone", 8: "un octogone"}
    n = rng.randint(3, 8)
    questions.append(number("a1", "elements", f"Un prisme droit a pour base {names[n]}. Combien a-t-il de faces ?", Fraction(n + 2), 1, ["n + 2."], [f"{n} + 2 = {n + 2}."]))
    n = rng.randint(3, 8)
    questions.append(number("a2", "elements", f"Un prisme droit a pour base {names[n]}. Combien a-t-il d'arêtes ?", Fraction(3 * n), 1, ["3 × n."], [f"3 × {n} = {3 * n}."]))
    n = rng.randint(3, 8)
    questions.append(number("a3", "elements", f"Un prisme droit a pour base {names[n]}. Combien a-t-il de sommets ?", Fraction(2 * n), 1, ["2 × n."], [f"2 × {n} = {2 * n}."]))
    length, width, h = rng.randint(3, 15), rng.randint(2, 12), rng.randint(2, 12)
    questions.append(number("a4", "volume", f"Quel est le volume d'un pavé droit de {length} cm, {width} cm et {h} cm, en cm³ ?", Fraction(length * width * h), 1, ["Les trois dimensions."], [f"{length} × {width} × {h} = {length * width * h} cm³."], units=CM3))
    length, width, h = rng.randint(3, 15), rng.randint(2, 12), rng.randint(2, 12)
    questions.append(number("a5", "patron", f"La base d'un prisme droit est un rectangle de {length} cm sur {width} cm, et sa hauteur est de {h} cm. Quelle est son aire latérale, en cm² ?", Fraction(2 * (length + width) * h), 2, ["Périmètre × hauteur."], [f"2 × {length + width} = {2 * (length + width)}.", f"{2 * (length + width)} × {h} = {2 * (length + width) * h} cm²."], units=CM2))
    length, width, h = rng.randint(3, 15), rng.randint(2, 12), rng.randint(2, 12)
    total = 2 * (length * width + length * h + width * h)
    questions.append(number("a6", "aire", f"Quelle est l'aire totale d'un pavé droit de {length} cm, {width} cm et {h} cm, en cm² ?", Fraction(total), 2, ["2 × (L×l + L×h + l×h)."], [f"{length * width} + {length * h} + {width * h} = {length * width + length * h + width * h}.", f"2 × {length * width + length * h + width * h} = {total} cm²."], units=CM2))
    base, h = rng.randint(5, 60), rng.randint(2, 20)
    questions.append(number("a7", "volume", f"Un prisme droit a une base de {base} cm² et une hauteur de {h} cm. Quel est son volume, en cm³ ?", Fraction(base * h), 1, ["Base × hauteur."], [f"{base} × {h} = {base * h} cm³."], units=CM3))
    base, h = rng.randint(5, 60), rng.randint(2, 20)
    questions.append(number("a8", "volume", f"Un prisme droit a un volume de {base * h} cm³ et une base de {base} cm². Quelle est sa hauteur, en cm ?", Fraction(h), 2, ["Volume ÷ base."], [f"{base * h} ÷ {base} = {h} cm."], units=CM))
    p, q = 2 * rng.randint(2, 8), rng.randint(3, 12)
    h = rng.randint(2, 15)
    questions.append(number("a9", "volume", f"La base d'un prisme droit est un triangle de base {p} cm et de hauteur {q} cm, et la hauteur du prisme est de {h} cm. Quel est son volume, en cm³ ?", Fraction(p * q * h, 2), 3, ["Aire du triangle : base × hauteur ÷ 2."], [f"{p} × {q} ÷ 2 = {p * q // 2}.", f"{p * q // 2} × {h} = {p * q * h // 2} cm³."], units=CM3))
    perimeter, h = rng.randint(6, 40), rng.randint(2, 15)
    questions.append(number("a10", "patron", f"La base d'un prisme droit a un périmètre de {perimeter} cm, et sa hauteur est de {h} cm. Quelle est son aire latérale, en cm² ?", Fraction(perimeter * h), 1, ["Périmètre × hauteur."], [f"{perimeter} × {h} = {perimeter * h} cm²."], units=CM2))
    liters = rng.randint(2, 40)
    questions.append(number("a11", "volume", f"Un réservoir a un volume de {liters * 1000} cm³. Combien de litres contient-il ?", Fraction(liters), 2, ["1 000 cm³ = 1 L."], [f"{liters * 1000} ÷ 1 000 = {liters} L."], units=["L", "l", "litres"]))
    a = rng.randint(2, 12)
    questions.append(number("a12", "aire", f"Quelle est l'aire totale d'un cube de {a} cm d'arête, en cm² ?", Fraction(6 * a * a), 2, ["6 faces carrées."], [f"{a} × {a} = {a * a}.", f"6 × {a * a} = {6 * a * a} cm²."], units=CM2))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=11, title="Prisme droit : faces, patron, aire et volume", language="fr",
    intro="Une boîte, une tente, un aquarium : ce sont des prismes droits. Ce chapitre t'apprend à compter leurs faces, à décrire leur patron, à calculer leur aire latérale, leur aire totale et leur volume.",
    objectives=["Reconnaître un prisme droit et compter ses faces, arêtes et sommets.",
                "Décrire un patron et calculer l'aire latérale.",
                "Calculer l'aire totale d'un prisme droit.",
                "Calculer le volume d'un prisme droit et le convertir en litres."],
    prerequisites=[{"text": "Connaître les solides usuels.", "chapter": "sn-6e-solides"},
                   {"text": "Calculer le périmètre et l'aire de figures usuelles.", "chapter": "sn-5e-parallelogrammes"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Eleventh chapter of the Senegal Cinquième course. Its contents follow the right prism lesson of the Côte d'Ivoire Cinquième programme (faces, edges and vertices, the net, the lateral and the total area, the volume), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. Solids are described in words and not drawn, and patterns cannot be cut out on a screen. "
                "It has not been checked against the official Senegalese programme.",
)
