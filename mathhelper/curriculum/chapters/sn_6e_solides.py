"""Sixième, Pavés droits, cubes et cylindres droits: the tenth chapter of the Senegal Sixième course, written in French.

The contents follow lesson 8 "Pavés droits et cylindres droits" of the Côte d'Ivoire Sixième programme (identifying and describing a box, a cube and a cylinder,
counting their vertices, edges and faces, their nets, and the formulas for area and volume of a box and of a cylinder), which was read for this chapter.
Every explanation, example and exercise was written independently, with our own numbers. The chapter uses text descriptions and no figures: a teacher or a
drawing of a real box is the natural companion of this chapter, and that is said to the student. Every calculation takes 3,14 for the number pi.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
import math
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .kit import N, d, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-6e-solides"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")
PI = Fraction(314, 100)

# ----- Section 1: the solids and their parts -----
S1 = Section(
    "elements", "Reconnaître les solides et leurs éléments", 20, "elements",
    "Nommer un pavé droit, un cube et un cylindre droit, compter leurs faces, arêtes et sommets, et décrire leurs patrons.",
    [
        para("Une boîte d'allumettes, un dé, une boîte de conserve : ces objets ont des formes de solides. Pour bien les étudier, il vaut mieux avoir un vrai objet sous les yeux, "
             "le tourner dans ses mains et le compter. Les nombres de la première section se vérifient avec une vraie boîte."),
        definition("Pavé droit et cube",
                   "Un pavé droit est un solide qui a 6 faces rectangulaires. Les faces opposées sont égales. Il a 12 arêtes (les segments où deux faces se rencontrent) et 8 sommets (les coins). "
                   "Un cube est un pavé droit dont les 6 faces sont des carrés égaux : toutes ses arêtes ont la même longueur."),
        definition("Cylindre droit",
                   "Un cylindre droit est un solide qui a deux bases, qui sont des disques égaux dans des plans parallèles, et une surface latérale qui les relie ; la droite qui joint les centres des disques est perpendiculaire aux bases. Il n'a aucun sommet. "
                   "La hauteur " + N("h") + " est la distance entre les deux bases ; le rayon " + N("r") + " est le rayon de chaque disque."),
        rule("Les patrons",
             "Un patron est le dessin du solide déplié à plat. Le patron d'un pavé droit est formé de 6 rectangles. Le patron d'un cylindre droit est formé de 2 disques et d'un rectangle : "
             "la hauteur de ce rectangle est la hauteur " + N("h") + " du cylindre, et sa longueur est le périmètre d'une base, " + N("2 \\times 3,14 \\times r") + "."),
        para("Pour fabriquer un pavé droit en carton, on dessine son patron, on le découpe et on le plie : il y a plusieurs patrons possibles pour un même solide, mais toujours 6 rectangles, qui doivent se replier sans se chevaucher. "
             "Sur une face, deux arêtes qui se touchent sont perpendiculaires, et deux arêtes opposées sont parallèles. Fabriquer vraiment un patron est un excellent exercice à faire avec ton enseignant."),
        example("Exemple 1", "Compter les faces, les arêtes et les sommets d'un pavé droit.",
                "On compte par parties : les faces du dessus et du dessous, les faces de côté, et les arêtes de chaque face.",
                [("Faces : dessus, dessous, devant, derrière, gauche, droite", "Il y a 6 faces rectangulaires."),
                 ("Sommets : 4 en haut et 4 en bas", "Il y a 8 sommets."),
                 ("Arêtes : 4 en haut, 4 en bas, et 4 qui montent du bas vers le haut", "Il y a 4 + 4 + 4 = 12 arêtes.")],
                "6 faces, 8 sommets, 12 arêtes", "4+4+4==12 and 4+4==8"),
        example("Exemple 2", "Quelle est la longueur totale des arêtes d'un cube dont l'arête mesure 5 cm ?",
                "Toutes les arêtes d'un cube ont la même longueur, et il y en a 12.",
                [("Un cube a 12 arêtes de même longueur", "Toutes mesurent 5 cm."),
                 (N("12 \\times 5") + " = " + N("60"), "La longueur totale est 60 cm.")],
                N("60") + " cm", "12*5==60"),
        example("Exemple 3", "Quelle est la longueur totale des arêtes d'un pavé droit de 6 cm de long, 4 cm de large et 3 cm de haut ?",
                "Un pavé droit a 4 arêtes de chaque dimension : 4 longueurs, 4 largeurs et 4 hauteurs.",
                [(N("4 \\times 6") + " = " + N("24"), "4 arêtes de 6 cm."),
                 (N("4 \\times 4") + " = " + N("16"), "4 arêtes de 4 cm."),
                 (N("4 \\times 3") + " = " + N("12"), "4 arêtes de 3 cm."),
                 (N("24 + 16 + 12") + " = " + N("52"), "Total : 52 cm. On peut aussi écrire 4 × (6 + 4 + 3) = 52.")],
                N("52") + " cm", "4*6+4*4+4*3==52==4*(6+4+3)"),
        example("Exemple 4", "Un cylindre droit a pour rayon 3 cm. Quelle est la longueur du rectangle de son patron ? (On prend 3,14 pour pi.)",
                "La longueur du rectangle est le périmètre d'une base, c'est-à-dire d'un cercle de rayon 3 cm.",
                [("Périmètre = " + N("2 \\times 3,14 \\times 3"), "Périmètre d'un cercle = 2 × pi × rayon."),
                 (N("2 \\times 3,14") + " = " + N("6,28"), "2 × 3,14 = 6,28."),
                 (N("6,28 \\times 3") + " = " + N("18,84"), "628 × 3 = 1 884, avec 2 chiffres après la virgule.")],
                N("18,84") + " cm", "2*d('3,14')*3==d('18,84')"),
        warning("Un cylindre n'a ni sommet ni arête droite (ses bords sont deux cercles). Sa surface latérale est courbe, ce n'est pas une face plate, mais elle devient un rectangle quand on la déplie. Et ne confonds pas les arêtes d'un cube (12) avec ses faces (6)."),
    ],
    [
        number("s1-g1", "elements", "Combien de faces a un pavé droit ?", Fraction(6), hints=["Dessus, dessous et quatre côtés."], solution=["2 + 4 = 6 faces."]),
        number("s1-g2", "elements", "Combien d'arêtes a un cube ?", Fraction(12), hints=["4 en haut, 4 en bas et 4 qui relient."], solution=["4 + 4 + 4 = 12 arêtes."]),
        number("s1-g3", "elements", "Combien de sommets a un pavé droit ?", Fraction(8), hints=["Les coins du solide."], solution=["4 sommets en haut et 4 en bas : 8."]),
        number("s1-g4", "elements", "Quelle est la longueur totale des arêtes d'un cube dont l'arête mesure 7 cm, en cm ?", Fraction(84), units=["cm"],
               hints=["Combien d'arêtes a un cube ?"], solution=["12 arêtes de 7 cm.", "12 × 7 = 84 cm."]),
        number("s1-g5", "elements", "Quelle est la longueur totale des arêtes d'un pavé droit de 5 cm sur 3 cm sur 2 cm, en cm ?", Fraction(40), units=["cm"],
               hints=["4 arêtes pour chaque dimension."], solution=["4 × (5 + 3 + 2) = 4 × 10 = 40 cm."]),
    ])

# ----- Section 2: areas of a box and of a cube -----
S2 = Section(
    "aires", "L'aire d'un pavé droit et d'un cube", 24, "aires",
    "Calculer l'aire d'une face, l'aire latérale et l'aire totale d'un pavé droit et d'un cube.",
    [
        para("Pour peindre une boîte ou la recouvrir de papier, il faut connaître l'aire de toute sa surface. Le pavé droit est formé de rectangles : on calcule l'aire de chacun avec la formule de l'aire d'un rectangle, "
             + N("\\text{longueur} \\times \\text{largeur}") + ", puis on additionne."),
        rule("Aire latérale et aire totale d'un pavé droit",
             "Pour un pavé droit de longueur " + N("L") + ", de largeur " + N("\\ell") + " et de hauteur " + N("h") + " : l'aire latérale (les quatre faces de côté) est le périmètre de la base multiplié par la hauteur, "
             + N("2 \\times (L + \\ell) \\times h") + ". L'aire totale ajoute les deux bases : " + N("2 \\times (L \\times \\ell + L \\times h + \\ell \\times h)") + ". "
             "Pour un cube d'arête " + N("c") + ", l'aire totale est " + N("6 \\times c \\times c") + ", car il a 6 faces carrées."),
        example("Exemple 1", "Calculer l'aire totale d'un pavé droit de 6 cm de long, 4 cm de large et 3 cm de haut.",
                "Il y a trois sortes de faces, qui vont par deux : dessus et dessous, devant et derrière, gauche et droite.",
                [(N("6 \\times 4") + " = " + N("24"), "Dessus et dessous : 24 cm² chacune."),
                 (N("6 \\times 3") + " = " + N("18"), "Devant et derrière : 18 cm² chacune."),
                 (N("4 \\times 3") + " = " + N("12"), "Gauche et droite : 12 cm² chacune."),
                 (N("2 \\times (24 + 18 + 12)") + " = " + N("2 \\times 54") + " = " + N("108"), "On additionne les trois aires et on double.")],
                N("108") + " cm²", "2*(6*4+6*3+4*3)==108"),
        example("Exemple 2", "Calculer l'aire latérale du même pavé droit, puis retrouver l'aire totale.",
                "L'aire latérale est le périmètre de la base fois la hauteur.",
                [("Périmètre de la base : " + N("2 \\times (6 + 4)") + " = " + N("20"), "La base est un rectangle de 6 cm sur 4 cm."),
                 (N("20 \\times 3") + " = " + N("60"), "Aire latérale : 60 cm²."),
                 (N("60 + 2 \\times 24") + " = " + N("108"), "On ajoute les deux bases de 24 cm² : on retrouve 108 cm².")],
                N("60") + " cm² et " + N("108") + " cm²", "2*(6+4)*3==60 and 60+2*(6*4)==108"),
        example("Exemple 3", "Calculer l'aire totale d'un cube d'arête 5 cm.",
                "Les 6 faces sont des carrés de côté 5 cm.",
                [(N("5 \\times 5") + " = " + N("25"), "Aire d'une face : 25 cm²."),
                 (N("6 \\times 25") + " = " + N("150"), "6 faces : 150 cm².")],
                N("150") + " cm²", "6*5*5==150"),
        example("Exemple 4", "Une boîte sans couvercle mesure 80 cm de long, 50 cm de large et 40 cm de haut. Quelle surface faut-il peindre à l'extérieur ?",
                "Il n'y a pas de couvercle : on compte les quatre faces de côté et le fond.",
                [("Fond : " + N("80 \\times 50") + " = " + N("4000"), "4 000 cm²."),
                 ("Quatre faces de côté : " + N("2 \\times 80 \\times 40 + 2 \\times 50 \\times 40") + " = " + N("6400 + 4000") + " = " + N("10400"), "Devant et derrière : 2 × 3 200 = 6 400. Gauche et droite : 2 × 2 000 = 4 000."),
                 (N("4000 + 10400") + " = " + N("14400"), "Total : 14 400 cm², soit 1,44 m².")],
                N("14400") + " cm²", "80*50+2*80*40+2*50*40==14400"),
        warning("L'aire se mesure en unités carrées (cm², m²) et le volume en unités cubiques (cm³, m³). N'oublie pas de compter toutes les faces : un pavé droit en a 6, pas 3."),
    ],
    [
        number("s2-g1", "aires", "Quelle est l'aire d'une face carrée d'un cube d'arête 4 cm, en cm² ?", Fraction(16), units=["cm2", "cm²"], hints=["Aire d'un carré : côté × côté."], solution=["4 × 4 = 16 cm²."]),
        number("s2-g2", "aires", "Quelle est l'aire totale d'un cube d'arête 3 cm, en cm² ?", Fraction(54), units=["cm2", "cm²"], hints=["6 faces carrées."], solution=["Une face : 3 × 3 = 9.", "6 × 9 = 54 cm²."]),
        number("s2-g3", "aires", "Quelle est l'aire latérale d'un pavé droit dont la base mesure 5 cm sur 3 cm et la hauteur 4 cm, en cm² ?", Fraction(64), units=["cm2", "cm²"],
               hints=["Périmètre de la base fois hauteur."], solution=["Périmètre de la base : 2 × (5 + 3) = 16.", "16 × 4 = 64 cm²."]),
        number("s2-g4", "aires", "Quelle est l'aire totale d'un pavé droit de 5 cm sur 3 cm sur 2 cm, en cm² ?", Fraction(62), units=["cm2", "cm²"],
               hints=["Trois sortes de faces : 5×3, 5×2 et 3×2."], solution=["5 × 3 = 15, 5 × 2 = 10, 3 × 2 = 6.", "2 × (15 + 10 + 6) = 2 × 31 = 62 cm²."]),
        choice("s2-g5", "aires", "Combien de faces faut-il compter pour l'aire totale d'une boîte fermée en forme de pavé droit ?", ["3", "4", "6"], 2, hints=["Dessus, dessous et quatre côtés."],
               solution=["Une boîte fermée a 6 faces."], wrong={0: "3 est le nombre de sortes de faces, mais chacune existe en double.", 1: "4 est le nombre de faces de côté ; il y a aussi le dessus et le dessous."}),
    ])

# ----- Section 3: volume of a box and of a cube -----
S3 = Section(
    "volumes", "Le volume d'un pavé droit et d'un cube", 26, "volumes",
    "Calculer le volume d'un pavé droit et d'un cube, et passer des unités de volume aux litres.",
    [
        para("Le volume mesure la place qu'occupe un solide. On le compte en petits cubes. Un cube d'arête 1 cm a un volume de 1 cm³. Si on range des cubes de 1 cm dans une boîte de 4 cm sur 3 cm sur 2 cm, "
             "il y en a 4 par rangée, 3 rangées par couche, et 2 couches : 4 × 3 × 2 = 24 cubes, donc 24 cm³."),
        rule("Volume d'un pavé droit et d'un cube",
             "Le volume d'un pavé droit est " + N("V = L \\times \\ell \\times h") + ". Le volume d'un cube d'arête " + N("c") + " est " + N("V = c \\times c \\times c") + ". "
             "Les trois dimensions doivent être dans la même unité."),
        rule("Volumes et litres",
             "Un cube de 10 cm d'arête contient 10 × 10 × 10 = 1 000 cm³ : c'est 1 dm³, et il contient exactement 1 litre. Donc 1 dm³ = 1 000 cm³ = 1 L, et 1 m³ = 1 000 dm³ = 1 000 L. Pour passer d'une unité de volume à la suivante (m³, dm³, cm³), on multiplie ou on divise par 1 000."),
        example("Exemple 1", "Calculer le volume d'un pavé droit de 6 cm sur 4 cm sur 3 cm.",
                "On multiplie les trois dimensions.",
                [(N("6 \\times 4") + " = " + N("24"), "Aire de la base : 24 cm²."),
                 (N("24 \\times 3") + " = " + N("72"), "Volume = aire de la base × hauteur = 24 × 3 = 72 cm³.")],
                N("72") + " cm³", "6*4*3==72"),
        example("Exemple 2", "Calculer le volume d'un cube d'arête 2,5 dm, en dm³ puis en litres.",
                "On multiplie l'arête trois fois par elle-même, et on utilise 1 dm³ = 1 L.",
                [(N("2,5 \\times 2,5") + " = " + N("6,25"), "25 × 25 = 625, avec 2 chiffres après la virgule."),
                 (N("6,25 \\times 2,5") + " = " + N("15,625"), "625 × 25 = 15 625, avec 2 + 1 = 3 chiffres après la virgule."),
                 ("15,625 dm³ = 15,625 L", "Car 1 dm³ = 1 L.")],
                N("15,625") + " dm³, soit " + N("15,625") + " L", "d('2,5')**3==d('15,625')"),
        example("Exemple 3", "Une bassine a la forme d'un pavé droit de 80 cm de long, 50 cm de large et 40 cm de haut. Quelle quantité d'eau, en litres, peut-elle contenir ?",
                "On calcule le volume en cm³, puis on convertit : 1 000 cm³ = 1 L.",
                [(N("80 \\times 50 \\times 40") + " = " + N("160000"), "80 × 50 = 4 000, puis 4 000 × 40 = 160 000 cm³."),
                 (N("160000 \\div 1000") + " = " + N("160"), "On divise par 1 000 pour passer des cm³ aux litres.")],
                N("160") + " L", "80*50*40==160000 and 160000/1000==160"),
        example("Exemple 4", "Convertir 3 500 cm³ en litres, puis 0,2 m³ en litres.",
                "1 L = 1 000 cm³ et 1 m³ = 1 000 L.",
                [(N("3500 \\div 1000") + " = " + N("3,5"), "3 500 cm³ = 3,5 L."),
                 (N("0,2 \\times 1000") + " = " + N("200"), "0,2 m³ = 200 L.")],
                "3,5 L et 200 L", "d('3500')/1000==d('3,5') and d('0,2')*1000==200"),
        warning("Les trois dimensions doivent être dans la même unité avant de multiplier : un pavé de 1 m sur 50 cm sur 40 cm se calcule en cm (100 × 50 × 40) ou en m (1 × 0,5 × 0,4), jamais en mélangeant. Et ne confonds pas cm³ et cm²."),
    ],
    [
        number("s3-g1", "volumes", "Quel est le volume d'un pavé droit de 5 cm sur 3 cm sur 4 cm, en cm³ ?", Fraction(60), units=["cm3", "cm³"], hints=["Multiplie les trois dimensions."], solution=["5 × 3 = 15, puis 15 × 4 = 60 cm³."]),
        number("s3-g2", "volumes", "Quel est le volume d'un cube d'arête 3 cm, en cm³ ?", Fraction(27), units=["cm3", "cm³"], hints=["3 × 3 × 3."], solution=["3 × 3 = 9, puis 9 × 3 = 27 cm³."]),
        number("s3-g3", "volumes", "Convertis 4 500 cm³ en litres.", d("4,5"), units=["L"], hints=["1 L = 1 000 cm³."], solution=["4 500 ÷ 1 000 = 4,5 L."]),
        number("s3-g4", "volumes", "Un bac a la forme d'un pavé droit de 1 m sur 0,5 m sur 0,4 m. Combien de litres d'eau contient-il quand il est plein ?", Fraction(200), units=["L"],
               hints=["Volume en m³, puis 1 m³ = 1 000 L."], solution=["1 × 0,5 × 0,4 = 0,2 m³.", "0,2 × 1 000 = 200 L."]),
        number("s3-g5", "volumes", "Un pavé droit a un volume de 120 cm³, une longueur de 6 cm et une largeur de 5 cm. Quelle est sa hauteur, en cm ?", Fraction(4), units=["cm"],
               hints=["Volume = longueur × largeur × hauteur : quelle opération pour trouver la hauteur ?"], solution=["6 × 5 = 30 cm² de base.", "120 ÷ 30 = 4 cm."]),
    ])

# ----- Section 4: the cylinder -----
S4 = Section(
    "cylindre", "Le cylindre droit : aires et volume", 26, "cylindre",
    "Calculer l'aire latérale, l'aire totale et le volume d'un cylindre droit, et résoudre un problème de contenance.",
    [
        para("Un seau, une boîte de conserve, un tuyau : des cylindres. Pour calculer leur aire et leur volume, on utilise le disque de la base. Dans ce chapitre on prend 3,14 pour le nombre pi, ce qui donne des résultats un peu approchés."),
        para("Le nombre pi est le rapport entre le périmètre d'un cercle et son diamètre : il vaut environ 3,14 pour tous les cercles. Le périmètre d'un cercle de rayon r est donc 3,14 × 2 × r. "
             "L'aire d'un disque de rayon r, 3,14 × r × r, est donnée ici comme une formule à connaître. Le volume d'un cylindre se comprend comme celui d'un pavé : on empile des disques identiques, autant que la hauteur le permet, donc volume = aire de la base × hauteur."),
        rule("Aire d'un disque, aire latérale et volume d'un cylindre",
             "Un disque de rayon " + N("r") + " a pour aire " + N("3,14 \\times r \\times r") + ". Pour un cylindre droit de rayon " + N("r") + " et de hauteur " + N("h") + " : l'aire latérale est " + N("2 \\times 3,14 \\times r \\times h")
             + " (le rectangle du patron), l'aire totale ajoute les deux bases, " + N("2 \\times 3,14 \\times r \\times h + 2 \\times 3,14 \\times r \\times r") + ", et le volume est l'aire de la base fois la hauteur, " + N("3,14 \\times r \\times r \\times h") + "."),
        example("Exemple 1", "Calculer l'aire d'une base d'un cylindre de rayon 5 cm.",
                "La base est un disque de rayon 5 cm.",
                [(N("5 \\times 5") + " = " + N("25"), "r × r = 25."),
                 (N("3,14 \\times 25") + " = " + N("78,5"), "314 × 25 = 7 850, avec 2 chiffres après la virgule : 78,50 = 78,5.")],
                N("78,5") + " cm²", "d('3,14')*25==d('78,5')"),
        example("Exemple 2", "Calculer l'aire latérale et l'aire totale du cylindre de rayon 5 cm et de hauteur 10 cm.",
                "L'aire latérale est le rectangle du patron : périmètre de la base fois hauteur.",
                [(N("2 \\times 3,14 \\times 5") + " = " + N("31,4"), "Périmètre de la base : 31,4 cm."),
                 (N("31,4 \\times 10") + " = " + N("314"), "Aire latérale : 314 cm²."),
                 (N("314 + 2 \\times 78,5") + " = " + N("471"), "On ajoute les deux bases de 78,5 cm² : aire totale 471 cm².")],
                N("314") + " cm² et " + N("471") + " cm²", "2*d('3,14')*5*10==314 and 314+2*d('78,5')==471"),
        example("Exemple 3", "Calculer le volume du même cylindre, en cm³ puis en litres.",
                "Volume = aire de la base × hauteur.",
                [(N("78,5 \\times 10") + " = " + N("785"), "Volume : 785 cm³."),
                 (N("785 \\div 1000") + " = " + N("0,785"), "En litres : 0,785 L.")],
                N("785") + " cm³, soit " + N("0,785") + " L", "d('78,5')*10==785 and d('785')/1000==d('0,785')"),
        example("Exemple 4", "Une bassine contient 160 L quand elle est pleine. Un seau cylindrique a un rayon de 10 cm et une hauteur de 20 cm. Combien de seaux pleins faut-il, au minimum, pour remplir la bassine ?",
                "On calcule la contenance du seau en litres, puis on divise la contenance de la bassine par celle du seau. Le résultat n'est pas entier : on arrondit à l'entier supérieur.",
                [(N("3,14 \\times 10 \\times 10 \\times 20") + " = " + N("6280"), "Volume du seau : 6 280 cm³."),
                 (N("6280 \\div 1000") + " = " + N("6,28"), "Le seau contient 6,28 L."),
                 (N("160 \\div 6,28") + " ≈ " + N("25,5"), "On cherche combien de fois 6,28 L entre dans 160 L. On ne peut pas utiliser une partie de seau : on prend l'entier juste au-dessus."),
                 ("25 × 6,28 = 157 est plus petit que 160 ; 26 × 6,28 = 163,28 est plus grand", "25 seaux ne suffisent pas, 26 seaux remplissent la bassine (et débordent un peu).")],
                "Il faut 26 seaux.", "d('3,14')*10*10*20==6280 and 25*d('6,28')<160<26*d('6,28')"),
        warning("Le rayon est la moitié du diamètre : un cylindre de diamètre 10 cm a un rayon de 5 cm. Et dans la formule de l'aire du disque, on multiplie le rayon par lui-même, on ne le double pas."),
    ],
    [
        number("s4-g1", "cylindre", "Quelle est l'aire d'un disque de rayon 2 cm, en cm² ? (pi = 3,14)", d("12,56"), units=["cm2", "cm²"], hints=["Aire = 3,14 × r × r."], solution=["2 × 2 = 4.", "3,14 × 4 = 12,56 cm²."]),
        number("s4-g2", "cylindre", "Quel est le périmètre d'un cercle de rayon 4 cm, en cm ? (pi = 3,14)", d("25,12"), units=["cm"], hints=["Périmètre = 2 × 3,14 × r."], solution=["2 × 3,14 = 6,28.", "6,28 × 4 = 25,12 cm."]),
        number("s4-g3", "cylindre", "Quelle est l'aire latérale d'un cylindre de rayon 3 cm et de hauteur 5 cm, en cm² ? (pi = 3,14)", d("94,2"), units=["cm2", "cm²"],
               hints=["Périmètre de la base fois hauteur."], solution=["Périmètre : 2 × 3,14 × 3 = 18,84.", "18,84 × 5 = 94,2 cm²."]),
        number("s4-g4", "cylindre", "Quel est le volume d'un cylindre de rayon 2 cm et de hauteur 10 cm, en cm³ ? (pi = 3,14)", d("125,6"), units=["cm3", "cm³"],
               hints=["Aire de la base fois hauteur."], solution=["Base : 3,14 × 2 × 2 = 12,56.", "12,56 × 10 = 125,6 cm³."]),
        choice("s4-g5", "cylindre", "Un cylindre a un diamètre de 12 cm. Quel est son rayon ?", ["12 cm", "6 cm", "24 cm"], 1, hints=["Le rayon est la moitié du diamètre."], solution=["12 ÷ 2 = 6 cm."],
               wrong={0: "12 cm est le diamètre, pas le rayon.", 2: "24 cm serait le double du diamètre."}),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "elements", "Combien d'arêtes a un pavé droit ?", Fraction(12), 1, ["4 en haut, 4 en bas, 4 verticales."], ["12."]),
    number("p2", "elements", "Combien de sommets a un cube ?", Fraction(8), 1, ["Un cube est un pavé droit."], ["8."]),
    number("p3", "elements", "Combien de rectangles faut-il pour dessiner le patron d'un pavé droit ?", Fraction(6), 1, ["Le patron a autant de pièces que le pavé a de faces."], ["6 rectangles."]),
    number("p4", "elements", "Combien de pièces faut-il pour dessiner le patron d'un cylindre droit ?", Fraction(3), 2, ["Deux bases et une surface latérale."], ["2 disques et 1 rectangle : 3 pièces."]),
    number("p5", "elements", "Quelle est la longueur totale des arêtes d'un cube de 9 cm d'arête, en cm ?", Fraction(108), 2, ["12 arêtes."], ["12 × 9 = 108 cm."], units=["cm"]),
    number("p6", "elements", "Quelle est la longueur totale des arêtes d'un pavé droit de 8 cm sur 5 cm sur 3 cm, en cm ?", Fraction(64), 2, ["4 × (L + l + h)."], ["4 × (8 + 5 + 3) = 4 × 16 = 64 cm."], units=["cm"]),
    number("p7", "elements", "Quelle est la longueur du rectangle du patron d'un cylindre de rayon 5 cm, en cm ? (pi = 3,14)", d("31,4"), 3, ["C'est le périmètre d'une base."], ["2 × 3,14 × 5 = 31,4 cm."], units=["cm"]),
    choice("p8", "elements", "Quel solide n'a aucun sommet ?", ["Le cube", "Le pavé droit", "Le cylindre droit"], 2, 2, ["Pense aux coins."], ["Un cylindre n'a pas de coins."], wrong={0: "Un cube a 8 sommets.", 1: "Un pavé droit a 8 sommets."}),
    number("p9", "aires", "Quelle est l'aire totale d'un cube d'arête 6 cm, en cm² ?", Fraction(216), 1, ["6 × arête × arête."], ["6 × 36 = 216 cm²."], units=["cm2", "cm²"]),
    number("p10", "aires", "Quelle est l'aire totale d'un pavé droit de 4 cm sur 3 cm sur 2 cm, en cm² ?", Fraction(52), 2, ["2 × (4×3 + 4×2 + 3×2)."], ["12 + 8 + 6 = 26.", "2 × 26 = 52 cm²."], units=["cm2", "cm²"]),
    number("p11", "aires", "Quelle est l'aire latérale d'un pavé droit dont la base mesure 7 cm sur 3 cm et la hauteur 5 cm, en cm² ?", Fraction(100), 2, ["Périmètre de la base fois hauteur."], ["Périmètre : 2 × (7 + 3) = 20.", "20 × 5 = 100 cm²."], units=["cm2", "cm²"]),
    number("p12", "aires", "Une boîte fermée a la forme d'un cube de 10 cm d'arête. Quelle surface de papier faut-il pour la recouvrir entièrement, en cm² ?", Fraction(600), 2, ["6 faces carrées."], ["6 × 10 × 10 = 600 cm²."], units=["cm2", "cm²"]),
    number("p13", "aires", "Une boîte sans couvercle mesure 30 cm de long, 20 cm de large et 10 cm de haut. Quelle surface faut-il peindre à l'extérieur, en cm² ? (fond et quatre côtés)", Fraction(1600), 3,
           ["Fond, puis deux grands côtés et deux petits côtés."], ["Fond : 30 × 20 = 600.", "Côtés : 2 × 30 × 10 + 2 × 20 × 10 = 600 + 400 = 1 000.", "Total : 1 600 cm²."], units=["cm2", "cm²"]),
    number("p14", "aires", "L'aire totale d'un cube est 150 cm². Quelle est l'aire d'une face, en cm² ?", Fraction(25), 2, ["Un cube a 6 faces égales."], ["150 ÷ 6 = 25 cm²."], units=["cm2", "cm²"]),
    number("p15", "aires", "Un cube a une aire totale de 150 cm². Quelle est la longueur de son arête, en cm ?", Fraction(5), 3, ["Cherche le nombre dont le carré est l'aire d'une face."], ["Une face : 150 ÷ 6 = 25.", "5 × 5 = 25 : l'arête mesure 5 cm."], units=["cm"]),
    choice("p16", "aires", "Léa calcule l'aire totale d'un pavé droit de 6 cm sur 4 cm sur 3 cm en faisant 6×4 + 6×3 + 4×3 = 54 cm². Quelle est son erreur ?", ["Elle a oublié de doubler : chaque sorte de face existe en deux exemplaires", "Elle s'est trompée dans une multiplication", "Elle a calculé le volume"], 0, 3,
           ["Combien de faces a un pavé droit ?"], ["Les 54 cm² sont l'aire de 3 faces seulement.", "Il faut doubler : 2 × 54 = 108 cm²."], wrong={1: "Les trois produits sont corrects.", 2: "Le volume se calcule avec une seule multiplication de trois nombres."}),
    number("p17", "volumes", "Quel est le volume d'un pavé droit de 10 cm sur 4 cm sur 3 cm, en cm³ ?", Fraction(120), 1, ["Multiplie les trois dimensions."], ["10 × 4 × 3 = 120 cm³."], units=["cm3", "cm³"]),
    number("p18", "volumes", "Quel est le volume d'un cube d'arête 5 cm, en cm³ ?", Fraction(125), 1, ["5 × 5 × 5."], ["25 × 5 = 125 cm³."], units=["cm3", "cm³"]),
    number("p19", "volumes", "Convertis 2 750 cm³ en litres.", d("2,75"), 1, ["Divise par 1 000."], ["2 750 ÷ 1 000 = 2,75 L."], units=["L"]),
    number("p20", "volumes", "Convertis 3,5 m³ en litres.", Fraction(3500), 2, ["1 m³ = 1 000 L."], ["3,5 × 1 000 = 3 500 L."], units=["L"]),
    number("p21", "volumes", "Un aquarium a la forme d'un pavé droit de 60 cm sur 30 cm sur 40 cm. Combien de litres d'eau contient-il quand il est plein ?", Fraction(72), 2, ["Volume en cm³, puis ÷ 1 000."], ["60 × 30 × 40 = 72 000 cm³.", "72 000 ÷ 1 000 = 72 L."], units=["L"]),
    number("p22", "volumes", "Un pavé droit a un volume de 150 cm³, une base de 10 cm sur 5 cm. Quelle est sa hauteur, en cm ?", Fraction(3), 3, ["Aire de la base d'abord."], ["10 × 5 = 50 cm².", "150 ÷ 50 = 3 cm."], units=["cm"]),
    number("p23", "volumes", "Quel est le volume d'un cube d'arête 1,2 dm, en dm³ ?", d("1,728"), 3, ["1,2 × 1,2 × 1,2."], ["1,2 × 1,2 = 1,44.", "1,44 × 1,2 = 1,728 dm³."], units=["dm3", "dm³"]),
    number("p24", "volumes", "Un réservoir en forme de pavé droit mesure 2 m sur 1,5 m sur 1 m. Combien de litres contient-il, en L ?", Fraction(3000), 3, ["Volume en m³, puis × 1 000."], ["2 × 1,5 × 1 = 3 m³.", "3 × 1 000 = 3 000 L."], units=["L"]),
    number("p25", "volumes", "Combien de cubes de 1 cm d'arête peut-on ranger dans une boîte de 6 cm sur 5 cm sur 2 cm ?", Fraction(60), 2, ["C'est le volume en cm³."], ["6 × 5 × 2 = 60 cubes."]),
    choice("p26", "volumes", "Karim dit : « le volume d'un cube d'arête 3 cm est 9 cm³ ». Quelle est son erreur ?", ["Il a calculé 3 × 3 au lieu de 3 × 3 × 3", "Il a calculé 6 × 3 au lieu de 3 × 3 × 3", "Il a doublé l'arête"], 0, 3,
           ["Combien de dimensions faut-il multiplier pour un volume ?"], ["Le volume d'un cube est arête × arête × arête = 27 cm³.", "3 × 3 = 9 est l'aire d'une face."], wrong={1: "6 × 3 = 18, pas 9.", 2: "Doubler l'arête donnerait 6, pas 9."}),
    number("p27", "cylindre", "Quelle est l'aire d'un disque de rayon 10 cm, en cm² ? (pi = 3,14)", Fraction(314), 1, ["3,14 × r × r."], ["10 × 10 = 100.", "3,14 × 100 = 314 cm²."], units=["cm2", "cm²"]),
    number("p28", "cylindre", "Quel est le périmètre d'un cercle de rayon 7 cm, en cm ? (pi = 3,14)", d("43,96"), 2, ["2 × 3,14 × r."], ["6,28 × 7 = 43,96 cm."], units=["cm"]),
    number("p29", "cylindre", "Quelle est l'aire latérale d'un cylindre de rayon 2 cm et de hauteur 10 cm, en cm² ? (pi = 3,14)", d("125,6"), 2, ["Périmètre de la base fois hauteur."], ["2 × 3,14 × 2 = 12,56.", "12,56 × 10 = 125,6 cm²."], units=["cm2", "cm²"]),
    number("p30", "cylindre", "Quel est le volume d'un cylindre de diamètre 10 cm et de hauteur 4 cm, en cm³ ? (pi = 3,14)", Fraction(314), 3, ["Le rayon est la moitié du diamètre."], ["Rayon : 5 cm. Base : 3,14 × 25 = 78,5.", "78,5 × 4 = 314 cm³."], units=["cm3", "cm³"]),
    number("p31", "cylindre", "Un bidon cylindrique a un rayon de 10 cm et une hauteur de 30 cm. Quelle est sa contenance, en litres ? (pi = 3,14)", d("9,42"), 3, ["Volume en cm³, puis ÷ 1 000."], ["3,14 × 100 × 30 = 9 420 cm³.", "9 420 ÷ 1 000 = 9,42 L."], units=["L"]),
    number("p32", "cylindre", "Un seau cylindrique contient 6,28 L. Combien de seaux pleins faut-il, au minimum, pour remplir un bac de 100 L ?", Fraction(16), 3, ["100 ÷ 6,28 n'est pas un nombre entier."], ["16 × 6,28 = 100,48 est plus grand que 100 ; 15 × 6,28 = 94,2 est plus petit.", "Il faut 16 seaux."]),
]

SUMMARY = [
    definition("Les solides", "Un pavé droit a 6 faces rectangulaires, 12 arêtes et 8 sommets. Un cube est un pavé droit dont les faces sont des carrés égaux. Un cylindre droit a deux bases (disques égaux), une surface latérale et aucun sommet. Le patron d'un pavé droit : 6 rectangles ; d'un cylindre : 2 disques et 1 rectangle."),
    rule("Aires", "Pavé droit : aire latérale = périmètre de la base × hauteur ; aire totale = 2 × (L × l + L × h + l × h). Cube : 6 × c × c. Cylindre : aire d'un disque = 3,14 × r × r ; aire latérale = 2 × 3,14 × r × h ; aire totale = aire latérale + 2 bases."),
    rule("Volumes", "Pavé droit : L × l × h. Cube : c × c × c. Cylindre : aire de la base × h. Les dimensions sont dans la même unité. 1 dm³ = 1 L, 1 L = 1 000 cm³, 1 m³ = 1 000 L."),
    para("Les erreurs à éviter : oublier des faces dans l'aire totale ; mélanger les unités (cm et m) ; confondre aire et volume ; confondre rayon et diamètre ; oublier de convertir en litres."),
]

CONCEPTS = {
    "elements": ("Solides, faces, arêtes, sommets", "elements"),
    "aires": ("Aires d'un pavé droit et d'un cube", "aires"),
    "volumes": ("Volumes et litres", "volumes"),
    "cylindre": ("Le cylindre droit", "cylindre"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    cm2, cm3 = ["cm2", "cm²"], ["cm3", "cm³"]
    box = lambda: (rng.randint(3, 12), rng.randint(2, 9), rng.randint(2, 9))
    # 1. total length of the edges
    length, width, height = box()
    questions.append(number("a1", "elements", f"Quelle est la longueur totale des arêtes d'un pavé droit de {length} cm sur {width} cm sur {height} cm, en cm ?", Fraction(4 * (length + width + height)), 2,
                            ["4 arêtes pour chaque dimension."], [f"4 × ({length} + {width} + {height}) = 4 × {length + width + height} = {4 * (length + width + height)} cm."], units=["cm"]))
    # 2. total edge length of a cube
    edge = rng.choice([e for e in range(2, 16) if e not in (5, 7, 9)])
    questions.append(number("a2", "elements", f"Un cube a une arête de {edge} cm. Quelle est la longueur totale de ses arêtes, en cm ?", Fraction(12 * edge), 1, ["Un cube a 12 arêtes égales."], [f"12 × {edge} = {12 * edge} cm."], units=["cm"]))
    # 3. lateral area
    length, width, height = box()
    questions.append(number("a3", "aires", f"Quelle est l'aire latérale d'un pavé droit dont la base mesure {length} cm sur {width} cm et la hauteur {height} cm, en cm² ?", Fraction(2 * (length + width) * height), 2,
                            ["Périmètre de la base fois hauteur."], [f"Périmètre : 2 × ({length} + {width}) = {2 * (length + width)}.", f"{2 * (length + width)} × {height} = {2 * (length + width) * height} cm²."], units=cm2))
    # 4. total area of a box
    length, width, height = box()
    total = 2 * (length * width + length * height + width * height)
    questions.append(number("a4", "aires", f"Quelle est l'aire totale d'un pavé droit de {length} cm sur {width} cm sur {height} cm, en cm² ?", Fraction(total), 3, ["Trois sortes de faces, chacune en double."],
                            [f"{length} × {width} = {length * width}, {length} × {height} = {length * height}, {width} × {height} = {width * height}.", f"2 × ({length * width} + {length * height} + {width * height}) = {total} cm²."], units=cm2))
    # 5. total area of a cube
    edge = rng.randint(7, 15)
    questions.append(number("a5", "aires", f"Quelle est l'aire totale d'un cube d'arête {edge} cm, en cm² ?", Fraction(6 * edge * edge), 2, ["6 faces carrées."], [f"Une face : {edge} × {edge} = {edge * edge}.", f"6 × {edge * edge} = {6 * edge * edge} cm²."], units=cm2))
    # 6. volume of a box
    length, width, height = box()
    questions.append(number("a6", "volumes", f"Quel est le volume d'un pavé droit de {length} cm sur {width} cm sur {height} cm, en cm³ ?", Fraction(length * width * height), 1, ["Multiplie les trois dimensions."],
                            [f"{length} × {width} = {length * width}.", f"{length * width} × {height} = {length * width * height} cm³."], units=cm3))
    # 7. volume of a cube
    edge = rng.randint(6, 12)
    questions.append(number("a7", "volumes", f"Quel est le volume d'un cube d'arête {edge} cm, en cm³ ?", Fraction(edge**3), 2, ["Arête × arête × arête."], [f"{edge} × {edge} = {edge * edge}.", f"{edge * edge} × {edge} = {edge**3} cm³."], units=cm3))
    # 8. a conversion
    cm3_value = rng.randrange(1100, 19000, 50)
    questions.append(number("a8", "volumes", f"Convertis {cm3_value} cm³ en litres.", Fraction(cm3_value, 1000), 2, ["1 L = 1 000 cm³."], [f"{cm3_value} ÷ 1 000 = {show(Fraction(cm3_value, 1000))} L."], units=["L"]))
    # 9. the missing height
    length, width, height = rng.randint(3, 12), rng.randint(2, 9), rng.randint(2, 9)
    while height in (length, width):
        height = rng.randint(2, 9)
    questions.append(number("a9", "volumes", f"Un pavé droit a un volume de {length * width * height} cm³, une longueur de {length} cm et une largeur de {width} cm. Quelle est sa hauteur, en cm ?", Fraction(height), 3,
                            ["Aire de la base d'abord, puis divise le volume par cette aire."], [f"Base : {length} × {width} = {length * width} cm².", f"{length * width * height} ÷ {length * width} = {height} cm."], units=["cm"]))
    # 10. volume of a cylinder
    radius, height = rng.randint(2, 9), rng.randint(3, 15)
    volume = PI * radius * radius * height
    questions.append(number("a10", "cylindre", f"Quel est le volume d'un cylindre de rayon {radius} cm et de hauteur {height} cm, en cm³ ? (pi = 3,14)", volume, 3, ["Aire de la base fois hauteur."],
                            [f"Base : 3,14 × {radius} × {radius} = {show(PI * radius * radius)}.", f"{show(PI * radius * radius)} × {height} = {show(volume)} cm³."], units=cm3))
    # 11. lateral area of a cylinder
    radius, height = rng.randint(3, 9), rng.randint(3, 15)
    lateral = 2 * PI * radius * height
    questions.append(number("a11", "cylindre", f"Quelle est l'aire latérale d'un cylindre de rayon {radius} cm et de hauteur {height} cm, en cm² ? (pi = 3,14)", lateral, 3, ["Périmètre de la base fois hauteur."],
                            [f"Périmètre : 2 × 3,14 × {radius} = {show(2 * PI * radius)}.", f"{show(2 * PI * radius)} × {height} = {show(lateral)} cm²."], units=cm2))
    # 12. the classic mistake with a cube
    edge = rng.randint(4, 9)
    options = [f"Il a calculé {edge} × {edge} au lieu de {edge} × {edge} × {edge}", f"Il a calculé {edge} + {edge} + {edge} au lieu de {edge} × {edge} × {edge}", "Il a doublé l'arête"]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a12", "volumes", f"Karim dit : « le volume d'un cube d'arête {edge} cm est {edge * edge} cm³ ». Quelle est son erreur ?", [options[i] for i in order], order.index(0), 3,
                            ["Combien de dimensions multiplie-t-on pour un volume ?"], [f"{edge} × {edge} = {edge * edge} est l'aire d'une face.", f"Le volume est {edge} × {edge} × {edge} = {edge**3} cm³."],
                            wrong={order.index(1): "Une addition ne donne pas le volume, et le résultat annoncé est différent.", order.index(2): "Doubler l'arête ne donne pas ce nombre."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=10, title="Pavés droits, cubes et cylindres droits", language="fr",
    intro="Une boîte, un seau, un aquarium : pour savoir combien de peinture il faut ou combien de litres ils contiennent, on calcule des aires et des volumes. "
          "Ce chapitre t'apprend à reconnaître les solides, à calculer leurs aires et leurs volumes, et à passer des unités de volume aux litres.",
    objectives=["Nommer un pavé droit, un cube et un cylindre droit, et compter leurs faces, arêtes et sommets.",
                "Décrire le patron d'un pavé droit et d'un cylindre droit.",
                "Calculer l'aire latérale et l'aire totale d'un pavé droit, d'un cube et d'un cylindre droit.",
                "Calculer le volume d'un pavé droit, d'un cube et d'un cylindre droit, et convertir en litres.",
                "Résoudre un problème de contenance."],
    prerequisites=[{"text": "Multiplier et diviser des nombres décimaux.", "chapter": "sn-6e-division"},
                   {"text": "Connaître le périmètre et l'aire d'un rectangle et d'un carré."}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Tenth chapter of the Senegal Sixième course. Its contents follow lesson 8 of the Côte d'Ivoire Sixième programme (box, cube and cylinder, their parts and nets, areas and volumes), which was read for it, "
                "so it is also offered there, but the programme's own situations are not reproduced. This chapter has no figures: it is meant to be studied with a real box, and it takes 3,14 for pi. Building a net or a solid by hand, which that lesson also asks for, is not covered. It has not been checked against the official Senegalese programme.",
)
