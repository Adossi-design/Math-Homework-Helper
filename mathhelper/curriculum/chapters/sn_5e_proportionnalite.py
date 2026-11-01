"""Cinquième, Proportionnalité, vitesse, débit et masse volumique: the fourth chapter of the Senegal Cinquième course, written in French.

The contents follow the lesson "Proportionnalité" of the Côte d'Ivoire Cinquième programme (recognise a proportional situation from a table and from a graph, the coefficient, the average
speed, the average flow rate and the density), which was read for this chapter. Every explanation, example, graph and exercise was written independently, with our own numbers.
Drawing a graph on squared paper cannot be done on a screen: the graphs are drawn by the app and the student reads them. Fixed answers are written as exact fractions and re-checked by
tests against an independent recalculation, and each worked example carries a "verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import CI_PROGRAMME_5E
from .figures import Graph, figure
from .kit import N, d, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-5e-proportionnalite"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")

# ----- Graphs -----
LINE = Graph(30, 45, 5, 15, "Durée (en minutes)", "Distance (en km)").line(0, 0, 30, 45).point(5, 7.5).point(10, 15).point(20, 30).point(30, 45)
CURVE = Graph(30, 45, 5, 15, "Durée (en minutes)", "Distance (en km)").line(0, 0, 10, 15).line(10, 15, 30, 22.5, "fig-seg").point(10, 15).point(20, 18.75).point(30, 22.5)
FILL = Graph(12, 600, 2, 100, "Durée (en minutes)", "Volume d'eau (en L)").line(0, 0, 12, 600).point(4, 200).point(8, 400).point(12, 600)

# ----- Section 1: recognising proportionality -----
S1 = Section(
    "reconnaitre", "Reconnaître la proportionnalité avec un tableau et un graphique", 24, "reconnaitre",
    "Reconnaître une situation de proportionnalité à partir d'un tableau ou d'un graphique, lire des coordonnées et trouver le coefficient de proportionnalité.",
    [
        para("Un véhicule roule sur une route droite à vitesse constante : après 10 minutes il a fait 15 km, après 20 minutes 30 km. Les distances sont proportionnelles aux durées. "
             "On peut le voir dans un tableau, mais aussi sur un graphique, où les points se placent sur une même droite qui passe par le point de départ."),
        definition("Coordonnées d'un point",
                   "Dans un quadrillage avec deux axes, un point est repéré par deux nombres : son abscisse (lue sur l'axe horizontal) et son ordonnée (lue sur l'axe vertical). On écrit " + N("A(10 ; 15)") + " pour le point d'abscisse 10 et d'ordonnée 15."),
        rule("Proportionnalité et graphique",
             "Deux grandeurs sont proportionnelles si, dans le tableau, on passe de l'une à l'autre en multipliant toujours par le même nombre, le coefficient de proportionnalité " + N("k = \\dfrac{y}{x}") + ". "
             "Sur un graphique, la situation est proportionnelle si les points sont alignés sur une droite qui passe par l'origine (0 ; 0). Le coefficient se lit avec n'importe quel point : on divise l'ordonnée par l'abscisse."),
        figure(LINE, "Un graphique avec la durée en minutes en abscisse et la distance en kilomètres en ordonnée, où quatre points sont alignés sur une droite qui part de l'origine.", "Les points (5 ; 7,5), (10 ; 15), (20 ; 30) et (30 ; 45) sont alignés avec l'origine : la distance est proportionnelle à la durée."),
        example("Exemple 1", "Le tableau donne la distance parcourue : 5 min → 7,5 km ; 10 min → 15 km ; 20 min → 30 km. Est-ce un tableau de proportionnalité ?",
                "On calcule le quotient distance ÷ durée pour chaque colonne.",
                [(N("7,5 \\div 5") + " = " + N("1,5"), "Première colonne."),
                 (N("15 \\div 10") + " = " + N("1,5") + " et " + N("30 \\div 20") + " = " + N("1,5"), "Les autres colonnes donnent le même quotient.")],
                "Oui, le coefficient est " + N("1,5") + " km par minute.", "d('7,5')/5==d('1,5') and 15/10==d('1,5') and 30/20==d('1,5')"),
        example("Exemple 2", "Le tableau donne : 2 → 5 ; 4 → 9 ; 6 → 13. Est-ce un tableau de proportionnalité ?",
                "On calcule le quotient du deuxième nombre par le premier pour chaque colonne.",
                [(N("5 \\div 2") + " = " + N("2,5"), "Première colonne."),
                 (N("9 \\div 4") + " = " + N("2,25"), "Deuxième colonne : le quotient est différent.")],
                "Non, ce n'est pas un tableau de proportionnalité.", "d('5')/2!=d('9')/4"),
        example("Exemple 3", "Sur le graphique, le point P(20 ; 30) est sur la droite qui passe par l'origine. Quel est le coefficient de proportionnalité ?",
                "On divise l'ordonnée par l'abscisse.",
                [(N("30 \\div 20") + " = " + N("1,5"), "Ordonnée divisée par abscisse.")],
                "Le coefficient est " + N("1,5") + " : le véhicule parcourt 1,5 km par minute.", "d('30')/20==d('1,5')"),
        example("Exemple 4", "Avec le coefficient 1,5, quelle distance le véhicule parcourt-il en 40 minutes ?",
                "On multiplie la durée par le coefficient.",
                [(N("40 \\times 1,5") + " = " + N("60"), "40 × 1,5 = 60.")],
                N("60") + " km.", "40*d('1,5')==60"),
        figure(CURVE, "Un graphique où la droite se plie : les points ne sont plus alignés avec l'origine après le point (10 ; 15).", "Ici les points ne sont pas tous alignés avec l'origine : le véhicule a ralenti, la distance n'est pas proportionnelle à la durée."),
        warning("Des points alignés ne suffisent pas : la droite doit aussi passer par l'origine. Une droite qui coupe l'axe vertical ailleurs (par exemple un abonnement avec un prix fixe de départ) ne représente pas une situation de proportionnalité."),
    ],
    [
        choice("s1-g1", "reconnaitre", "Le tableau donne : 3 → 12 ; 5 → 20 ; 8 → 32. Est-ce un tableau de proportionnalité ?", ["Oui, le coefficient est 4", "Oui, le coefficient est 9", "Non"], 0,
               hints=["Divise le deuxième nombre par le premier."], solution=["12 ÷ 3 = 4, 20 ÷ 5 = 4 et 32 ÷ 8 = 4 : oui, le coefficient est 4."], wrong={1: "9 serait la différence 12 − 3 : ce n'est pas constant.", 2: "Tous les quotients sont égaux à 4."}),
        choice("s1-g2", "reconnaitre", "Le tableau donne : 2 → 7 ; 4 → 11 ; 6 → 15. Est-ce un tableau de proportionnalité ?", ["Oui", "Non"], 1,
               hints=["Calcule 7 ÷ 2, 11 ÷ 4, 15 ÷ 6."], solution=["7 ÷ 2 = 3,5 ; 11 ÷ 4 = 2,75 : les quotients sont différents."], wrong={0: "On ajoute 4 à chaque fois, mais cela ne suffit pas : il faut le même quotient."}),
        number("s1-g3", "reconnaitre", "Le point A(8 ; 20) est sur la droite d'un graphique de proportionnalité. Quel est le coefficient de proportionnalité ?", d("2,5"),
               hints=["Ordonnée divisée par abscisse."], solution=["20 ÷ 8 = 2,5."]),
        number("s1-g4", "reconnaitre", "Avec le coefficient 2,5 (prix en F pour 1 g), quel est le prix de 40 g, en F ?", Fraction(100), units=["F"],
               hints=["Multiplie 40 par 2,5."], solution=["40 × 2,5 = 100 F."]),
        choice("s1-g5", "reconnaitre", "À quoi reconnaît-on une situation de proportionnalité sur un graphique ?", ["Les points sont alignés sur une droite qui passe par l'origine", "Les points sont alignés sur n'importe quelle droite", "Les points forment une courbe"], 0,
               hints=["Il faut deux conditions."], solution=["Les points doivent être alignés et la droite doit passer par l'origine."], wrong={1: "Une droite qui ne passe pas par l'origine ne représente pas une proportionnalité.", 2: "Une courbe n'est pas une proportionnalité."}),
    ])

# ----- Section 2: average speed -----
S2 = Section(
    "vitesse", "La vitesse moyenne", 24, "vitesse",
    "Calculer une vitesse moyenne, une distance ou une durée, et convertir des vitesses entre km/h et m/s.",
    [
        para("Un autocar met 3 heures pour faire 240 km. Il n'a pas roulé tout le temps à la même vitesse, mais on peut calculer la vitesse qu'il aurait eue en roulant à vitesse constante : c'est la vitesse moyenne."),
        definition("Vitesse moyenne",
                   "La vitesse moyenne est la distance parcourue divisée par la durée du parcours : " + N("v = \\dfrac{d}{t}") + ". Si la distance est en km et la durée en h, la vitesse est en km/h. Si la distance est en m et la durée en s, elle est en m/s."),
        rule("Trois formules",
             N("v = \\dfrac{d}{t}") + ", " + N("d = v \\times t") + " et " + N("t = \\dfrac{d}{v}") + ". La distance est proportionnelle à la durée quand la vitesse est constante, et le coefficient de proportionnalité est la vitesse. "
             "Pour passer de m/s à km/h, on multiplie par 3,6 ; pour passer de km/h à m/s, on divise par 3,6."),
        example("Exemple 1", "Un autocar fait 240 km en 3 h. Quelle est sa vitesse moyenne ?",
                "On divise la distance par la durée.",
                [(N("v = 240 \\div 3") + " = " + N("80"), "Distance en km, durée en h : le résultat est en km/h.")],
                N("80") + " km/h.", "240/3==80"),
        example("Exemple 2", "Une voiture roule à 60 km/h pendant 2 h 30 min. Quelle distance parcourt-elle ?",
                "On convertit la durée en heures : 2 h 30 min = 2,5 h.",
                [(N("30 \\text{ min} = 0,5 \\text{ h}"), "30 min est une demi-heure."),
                 (N("d = 60 \\times 2,5") + " = " + N("150"), "d = v × t.")],
                N("150") + " km.", "60*d('2,5')==150"),
        example("Exemple 3", "Un cycliste parcourt 45 km à 15 km/h. Combien de temps roule-t-il ?",
                "On divise la distance par la vitesse.",
                [(N("t = 45 \\div 15") + " = " + N("3"), "Le résultat est en heures.")],
                N("3") + " h.", "45/15==3"),
        example("Exemple 4", "Un marcheur fait 6 km en 20 min. Quelle est sa vitesse en km/h ?",
                "20 min = 1/3 h : on convertit d'abord la durée en heures, ou on cherche la distance faite en 60 min.",
                [("En 20 min : 6 km. En 60 min = 3 × 20 min : 3 × 6 km", "La distance est proportionnelle à la durée."),
                 (N("3 \\times 6") + " = " + N("18"), "Il parcourt 18 km en 1 h.")],
                N("18") + " km/h.", "6*3==18 and d('6')/(d('1')/3)==18"),
        example("Exemple 5", "Convertir 72 km/h en m/s, puis 15 m/s en km/h.",
                "On divise par 3,6 pour aller de km/h à m/s, et on multiplie par 3,6 dans l'autre sens.",
                [(N("72 \\div 3,6") + " = " + N("20"), "72 km/h = 20 m/s. En effet 72 000 m en 3 600 s."),
                 (N("15 \\times 3,6") + " = " + N("54"), "15 m/s = 54 km/h.")],
                N("20") + " m/s et " + N("54") + " km/h.", "d('72')/d('3,6')==20 and 15*d('3,6')==54"),
        warning("La durée doit être dans la même unité que celle de la vitesse : 20 min ne se met pas directement dans une formule en km/h, il faut 1/3 h. Et une vitesse moyenne n'est pas la moyenne des vitesses : "
                "on divise toute la distance par toute la durée."),
    ],
    [
        number("s2-g1", "vitesse", "Un train fait 360 km en 4 h. Quelle est sa vitesse moyenne, en km/h ?", Fraction(90), units=["km/h"], hints=["Distance ÷ durée."], solution=["360 ÷ 4 = 90 km/h."]),
        number("s2-g2", "vitesse", "Une moto roule à 60 km/h pendant 2,5 h. Quelle distance parcourt-elle, en km ?", Fraction(150), units=["km"], hints=["d = v × t."], solution=["60 × 2,5 = 150 km."]),
        number("s2-g3", "vitesse", "Un camion fait 180 km à 90 km/h. Combien de temps roule-t-il, en heures ?", Fraction(2), units=["h"], hints=["t = d ÷ v."], solution=["180 ÷ 90 = 2 h."]),
        number("s2-g4", "vitesse", "Convertis 36 km/h en m/s.", Fraction(10), units=["m/s"], hints=["Divise par 3,6."], solution=["36 ÷ 3,6 = 10 m/s."]),
        number("s2-g5", "vitesse", "Un élève fait 12 km en 30 min. Quelle est sa vitesse en km/h ?", Fraction(24), units=["km/h"], hints=["30 min = 0,5 h."], solution=["En 60 min, il fait 2 × 12 = 24 km : 24 km/h."]),
    ])

# ----- Section 3: flow rate and density -----
S3 = Section(
    "debit", "Le débit moyen et la masse volumique", 24, "debit",
    "Calculer un débit moyen, un volume ou une durée, et calculer une masse volumique, une masse ou un volume.",
    [
        para("Un robinet remplit un seau, une pompe vide un puits, un tuyau arrose un champ : le volume d'eau est proportionnel à la durée quand le débit est constant. "
             "De même, la masse d'un morceau de matière est proportionnelle à son volume : le coefficient s'appelle la masse volumique."),
        definition("Débit moyen",
                   "Le débit moyen est le volume écoulé divisé par la durée de l'écoulement : " + N("q = \\dfrac{V}{t}") + ". Il s'exprime par exemple en L/min ou en m³/h. On a aussi " + N("V = q \\times t") + " et " + N("t = \\dfrac{V}{q}") + "."),
        definition("Masse volumique",
                   "La masse volumique d'une matière est la masse d'un morceau divisée par son volume : " + N("\\rho = \\dfrac{m}{V}") + ". Elle s'exprime par exemple en g/cm³ ou en kg/L. On a aussi " + N("m = \\rho \\times V") + " et " + N("V = \\dfrac{m}{\\rho}") + "."),
        figure(FILL, "Un graphique où le volume d'eau en litres, en ordonnée, est proportionnel à la durée en minutes, en abscisse : les points (4 ; 200), (8 ; 400) et (12 ; 600) sont alignés avec l'origine.", "Le débit d'un robinet : 50 L chaque minute. Le coefficient de proportionnalité est le débit, 50 L/min."),
        example("Exemple 1", "Un robinet remplit un bidon de 120 L en 8 min. Quel est son débit moyen ?",
                "On divise le volume par la durée.",
                [(N("q = 120 \\div 8") + " = " + N("15"), "Volume en L, durée en min : le débit est en L/min.")],
                N("15") + " L/min.", "120/8==15"),
        example("Exemple 2", "Un tuyau a un débit de 25 L/min. Quel volume d'eau fournit-il en 8 min ? Combien de temps faut-il pour remplir un fût de 300 L ?",
                "On utilise V = q × t, puis t = V ÷ q.",
                [(N("V = 25 \\times 8") + " = " + N("200"), "En 8 min : 200 L."),
                 (N("t = 300 \\div 25") + " = " + N("12"), "Pour 300 L : 12 min.")],
                N("200") + " L, et " + N("12") + " min.", "25*8==200 and 300/25==12"),
        example("Exemple 3", "Un morceau de fer a une masse de 780 g et un volume de 100 cm³. Quelle est sa masse volumique ?",
                "On divise la masse par le volume.",
                [(N("\\rho = 780 \\div 100") + " = " + N("7,8"), "Masse en g, volume en cm³ : la masse volumique est en g/cm³.")],
                N("7,8") + " g/cm³.", "d('780')/100==d('7,8')"),
        example("Exemple 4", "L'huile a une masse volumique de 0,9 kg/L. Quelle est la masse de 5 L d'huile ? Quel volume occupent 18 kg d'huile ?",
                "On utilise m = ρ × V, puis V = m ÷ ρ.",
                [(N("m = 0,9 \\times 5") + " = " + N("4,5"), "5 L d'huile pèsent 4,5 kg."),
                 (N("V = 18 \\div 0,9") + " = " + N("20"), "18 kg d'huile occupent 20 L.")],
                N("4,5") + " kg, et " + N("20") + " L.", "d('0,9')*5==d('4,5') and 18/d('0,9')==20"),
        warning("Garde bien les unités ensemble : un débit en L/min demande un volume en L et une durée en min. Si la durée est en heures, convertis-la. Et ne confonds pas masse (en g, kg) et volume (en cm³, L) : l'eau a une masse volumique de 1 g/cm³, soit 1 kg/L."),
    ],
    [
        number("s3-g1", "debit", "Une pompe fournit 600 L en 12 min. Quel est son débit moyen, en L/min ?", Fraction(50), units=["L/min"], hints=["Volume ÷ durée."], solution=["600 ÷ 12 = 50 L/min."]),
        number("s3-g2", "debit", "Un robinet a un débit de 25 L/min. Quel volume fournit-il en 8 min, en L ?", Fraction(200), units=["L"], hints=["V = q × t."], solution=["25 × 8 = 200 L."]),
        number("s3-g3", "debit", "Un morceau de métal a une masse de 540 g et un volume de 200 cm³. Quelle est sa masse volumique, en g/cm³ ?", d("2,7"), units=["g/cm3", "g/cm³"], hints=["Masse ÷ volume."], solution=["540 ÷ 200 = 2,7 g/cm³."]),
        number("s3-g4", "debit", "Un liquide a une masse volumique de 0,75 kg/L. Quel est le volume de 9 kg de ce liquide, en L ?", Fraction(12), units=["L"], hints=["V = m ÷ ρ."], solution=["9 ÷ 0,75 = 12 L."]),
        choice("s3-g5", "debit", "Quelle formule donne la masse volumique ?", [N("\\rho = \\dfrac{m}{V}"), N("\\rho = m \\times V"), N("\\rho = \\dfrac{V}{m}")], 0,
               hints=["Masse par unité de volume."], solution=["La masse volumique est la masse divisée par le volume."], wrong={1: "On ne multiplie pas : c'est un quotient.", 2: "C'est l'inverse : V ÷ m n'est pas une masse volumique."}),
    ])

# ----- Section 4: problems -----
S4 = Section(
    "problemes", "Résoudre des problèmes de proportionnalité", 24, "problemes",
    "Compléter un tableau de proportionnalité, comparer des vitesses, et résoudre un problème à plusieurs étapes avec vitesse, débit ou masse volumique.",
    [
        para("Les situations de proportionnalité se rencontrent partout. Pour les résoudre, on repère d'abord la grandeur qui sert de coefficient (la vitesse, le débit, la masse volumique, un prix), puis on calcule avec les trois formules."),
        example("Exemple 1", "Compléter le tableau de proportionnalité : durée 10 min → 15 km ; durée 30 min → ? km ; durée ? min → 60 km.",
                "On calcule le coefficient avec la première colonne, puis on s'en sert.",
                [(N("15 \\div 10") + " = " + N("1,5"), "Le coefficient est 1,5 km par minute."),
                 (N("30 \\times 1,5") + " = " + N("45"), "En 30 min : 45 km."),
                 (N("60 \\div 1,5") + " = " + N("40"), "Pour 60 km : 40 min.")],
                "30 min → " + N("45") + " km, et " + N("40") + " min → 60 km.", "d('15')/10==d('1,5') and 30*d('1,5')==45 and 60/d('1,5')==40"),
        example("Exemple 2", "Le véhicule A fait 150 km en 2 h. Le véhicule B fait 200 km en 3 h. Lequel est le plus rapide ?",
                "On calcule la vitesse de chacun.",
                [(N("150 \\div 2") + " = " + N("75"), "A roule à 75 km/h."),
                 (N("200 \\div 3") + " ≈ " + N("66,7"), "B roule à environ 66,7 km/h."),
                 ("75 est plus grand que 66,7", "A est plus rapide.")],
                "Le véhicule A est le plus rapide.", "d('150')/2>d('200')/3"),
        example("Exemple 3", "Un automobiliste fait 120 km à 60 km/h, puis 120 km à 40 km/h. Quelle est sa vitesse moyenne sur tout le trajet ?",
                "La vitesse moyenne est la distance totale divisée par la durée totale.",
                [(N("120 \\div 60") + " = " + N("2") + " h et " + N("120 \\div 40") + " = " + N("3") + " h", "Durée de chaque partie."),
                 (N("120 + 120") + " = " + N("240") + " km en " + N("2 + 3") + " = " + N("5") + " h", "Distance totale et durée totale."),
                 (N("240 \\div 5") + " = " + N("48"), "Vitesse moyenne.")],
                N("48") + " km/h, et non 50 km/h.", "120/60==2 and 120/40==3 and 240/5==48"),
        example("Exemple 4", "Un robinet A donne 20 L/min et un robinet B donne 30 L/min. Ouverts ensemble, en combien de minutes remplissent-ils un bassin de 600 L ?",
                "Les débits s'additionnent quand les robinets coulent en même temps.",
                [(N("20 + 30") + " = " + N("50"), "Débit total : 50 L/min."),
                 (N("600 \\div 50") + " = " + N("12"), "t = V ÷ q.")],
                N("12") + " minutes.", "20+30==50 and 600/50==12"),
        warning("Pour une vitesse moyenne sur plusieurs parties, ne fais pas la moyenne des vitesses : calcule la distance totale et la durée totale. Les débits de deux robinets ouverts ensemble s'additionnent."),
    ],
    [
        number("s4-g1", "problemes", "Un tableau de proportionnalité donne : 4 L → 10 F. Quel est le prix de 14 L, en F ?", Fraction(35), units=["F"], hints=["Coefficient : 10 ÷ 4."], solution=["10 ÷ 4 = 2,5 F par litre.", "14 × 2,5 = 35 F."]),
        number("s4-g2", "problemes", "Un automobiliste fait 100 km à 50 km/h puis 100 km à 100 km/h. Quelle est la durée totale du trajet, en heures ?", Fraction(3), units=["h"], hints=["Durée de chaque partie."], solution=["100 ÷ 50 = 2 h et 100 ÷ 100 = 1 h.", "2 + 1 = 3 h."]),
        number("s4-g3", "problemes", "Deux robinets de 15 L/min et 25 L/min coulent ensemble. En combien de minutes remplissent-ils un bassin de 400 L ?", Fraction(10), units=["min"], hints=["Additionne les débits."], solution=["15 + 25 = 40 L/min.", "400 ÷ 40 = 10 min."]),
        choice("s4-g4", "problemes", "A fait 90 km en 1,5 h. B fait 100 km en 2 h. Lequel est le plus rapide ?", ["A", "B", "Ils vont à la même vitesse"], 0, hints=["Calcule 90 ÷ 1,5 et 100 ÷ 2."], solution=["A : 60 km/h. B : 50 km/h. A est plus rapide."], wrong={1: "B roule à 50 km/h, A à 60.", 2: "60 et 50 sont différents."}),
        number("s4-g5", "problemes", "1 L d'eau pèse 1 kg. Quelle est la masse de 12,5 L d'eau, en kg ?", d("12,5"), units=["kg"], hints=["La masse volumique de l'eau est 1 kg/L."], solution=["12,5 × 1 = 12,5 kg."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    choice("p1", "reconnaitre", "Le tableau donne : 1 → 6 ; 4 → 24 ; 7 → 42. Est-ce un tableau de proportionnalité ?", ["Oui, le coefficient est 6", "Non", "Oui, le coefficient est 5"], 0, 1, ["Divise par la première ligne."], ["6, 6 et 6 : oui."], wrong={1: "Les quotients sont tous égaux à 6.", 2: "5 serait la différence 6 − 1."}),
    choice("p2", "reconnaitre", "Le tableau donne : 2 → 10 ; 3 → 16 ; 5 → 26. Est-ce un tableau de proportionnalité ?", ["Oui", "Non"], 1, 2, ["Calcule 10 ÷ 2, 16 ÷ 3, 26 ÷ 5."], ["5 ; 5,33 ; 5,2 : les quotients sont différents."], wrong={0: "Les quotients ne sont pas égaux."}),
    number("p3", "reconnaitre", "Le point B(6 ; 21) est sur la droite d'un graphique de proportionnalité. Quel est le coefficient ?", d("3,5"), 1, ["Ordonnée ÷ abscisse."], ["21 ÷ 6 = 3,5."]),
    number("p4", "reconnaitre", "Le coefficient est 0,8. Quelle est l'ordonnée du point d'abscisse 15 ?", Fraction(12), 2, ["Multiplie par le coefficient."], ["15 × 0,8 = 12."]),
    number("p5", "reconnaitre", "Le coefficient est 0,8. Quelle est l'abscisse du point d'ordonnée 20 ?", Fraction(25), 2, ["Divise par le coefficient."], ["20 ÷ 0,8 = 25."]),
    choice("p6", "reconnaitre", "Léa dit : « mes points sont alignés, donc c'est de la proportionnalité ». Qu'en penses-tu ?", ["Il faut aussi que la droite passe par l'origine", "Elle a raison", "Il faut que les points forment une courbe"], 0, 3, ["Deux conditions."], ["Alignés ET sur une droite qui passe par l'origine."], wrong={1: "Il manque une condition.", 2: "Une courbe n'est pas une proportionnalité."}),
    number("p7", "vitesse", "Une voiture fait 330 km en 5 h 30 min. Quelle est sa vitesse moyenne, en km/h ?", Fraction(60), 2, ["5 h 30 min = 5,5 h."], ["330 ÷ 5,5 = 60 km/h."], units=["km/h"]),
    number("p8", "vitesse", "Un cycliste roule à 18 km/h pendant 2 h 20 min. Quelle distance parcourt-il, en km ? (2 h 20 min = 7/3 h)", Fraction(42), 3, ["18 × 7/3."], ["18 × 7 = 126 ; 126 ÷ 3 = 42 km."], units=["km"]),
    number("p9", "vitesse", "Un marcheur parcourt 4,5 km à 3 km/h. Combien de temps marche-t-il, en heures ?", d("1,5"), 1, ["t = d ÷ v."], ["4,5 ÷ 3 = 1,5 h."], units=["h"]),
    number("p10", "vitesse", "Un avion vole à 800 km/h pendant 3 h. Quelle distance parcourt-il, en km ?", Fraction(2400), 1, ["d = v × t."], ["800 × 3 = 2 400 km."], units=["km"]),
    number("p11", "vitesse", "Convertis 90 km/h en m/s.", Fraction(25), 2, ["Divise par 3,6."], ["90 ÷ 3,6 = 25 m/s."], units=["m/s"]),
    number("p12", "vitesse", "Convertis 20 m/s en km/h.", Fraction(72), 2, ["Multiplie par 3,6."], ["20 × 3,6 = 72 km/h."], units=["km/h"]),
    number("p13", "vitesse", "Un coureur fait 100 m en 10 s. Quelle est sa vitesse en m/s ?", Fraction(10), 1, ["Distance ÷ durée."], ["100 ÷ 10 = 10 m/s."], units=["m/s"]),
    number("p14", "vitesse", "Un coureur fait 100 m en 10 s. Quelle est sa vitesse en km/h ?", Fraction(36), 2, ["10 m/s × 3,6."], ["10 × 3,6 = 36 km/h."], units=["km/h"]),
    number("p15", "vitesse", "Un train roule à 120 km/h. Quelle distance parcourt-il en 45 min ? (45 min = 0,75 h)", Fraction(90), 2, ["d = v × t."], ["120 × 0,75 = 90 km."], units=["km"]),
    number("p16", "vitesse", "Un bus fait 15 km en 20 min. Quelle est sa vitesse en km/h ?", Fraction(45), 3, ["En 60 min il fait 3 fois plus."], ["3 × 15 = 45 km/h."], units=["km/h"]),
    number("p17", "debit", "Un robinet remplit un bassin de 450 L en 18 min. Quel est son débit moyen, en L/min ?", Fraction(25), 1, ["Volume ÷ durée."], ["450 ÷ 18 = 25 L/min."], units=["L/min"]),
    number("p18", "debit", "Un tuyau a un débit de 40 L/min. Quel volume fournit-il en 15 min, en L ?", Fraction(600), 1, ["V = q × t."], ["40 × 15 = 600 L."], units=["L"]),
    number("p19", "debit", "Un puits fournit 12 L/min. Combien de minutes faut-il pour remplir un bidon de 90 L ?", d("7,5"), 2, ["t = V ÷ q."], ["90 ÷ 12 = 7,5 min."], units=["min"]),
    number("p20", "debit", "Un robinet fournit 18 m³ en 6 h. Quel est son débit moyen, en m³/h ?", Fraction(3), 2, ["18 ÷ 6."], ["18 ÷ 6 = 3 m³/h."], units=["m3/h", "m³/h"]),
    number("p21", "debit", "Un morceau de bois a une masse de 300 g et un volume de 400 cm³. Quelle est sa masse volumique, en g/cm³ ?", d("0,75"), 2, ["Masse ÷ volume."], ["300 ÷ 400 = 0,75 g/cm³."], units=["g/cm3", "g/cm³"]),
    number("p22", "debit", "Le fer a une masse volumique de 7,8 g/cm³. Quelle est la masse de 50 cm³ de fer, en g ?", Fraction(390), 2, ["m = ρ × V."], ["7,8 × 50 = 390 g."], units=["g"]),
    number("p23", "debit", "L'huile a une masse volumique de 0,9 kg/L. Quel volume occupent 4,5 kg d'huile, en L ?", Fraction(5), 2, ["V = m ÷ ρ."], ["4,5 ÷ 0,9 = 5 L."], units=["L"]),
    number("p24", "debit", "Le mercure a une masse volumique de 13,6 g/cm³. Quelle est la masse de 10 cm³ de mercure, en g ?", Fraction(136), 2, ["m = ρ × V."], ["13,6 × 10 = 136 g."], units=["g"]),
    choice("p25", "debit", "Un objet flotte dans l'eau si sa masse volumique est plus petite que celle de l'eau (1 g/cm³). Lequel flotte ?", ["Le bois de masse volumique 0,6 g/cm³", "Le fer de masse volumique 7,8 g/cm³", "Le plomb de masse volumique 11,3 g/cm³"], 0, 2, ["Compare à 1."], ["0,6 est plus petit que 1 : le bois flotte."], wrong={1: "7,8 est plus grand que 1 : le fer coule.", 2: "11,3 est plus grand que 1 : le plomb coule."}),
    number("p26", "problemes", "Un tableau de proportionnalité donne : 6 kg → 4 500 F. Quel est le prix de 10 kg, en F ?", Fraction(7500), 1, ["Prix d'un kilogramme : 750 F."], ["4 500 ÷ 6 = 750 F le kg.", "750 × 10 = 7 500 F."], units=["F"]),
    number("p27", "problemes", "Un cycliste fait 30 km à 15 km/h puis 30 km à 10 km/h. Quelle est sa durée totale, en heures ?", Fraction(5), 2, ["Durée de chaque partie."], ["30 ÷ 15 = 2 h et 30 ÷ 10 = 3 h.", "2 + 3 = 5 h."], units=["h"]),
    number("p28", "problemes", "Un cycliste fait 30 km à 15 km/h puis 30 km à 10 km/h. Quelle est sa vitesse moyenne sur tout le trajet, en km/h ?", Fraction(12), 3, ["Distance totale ÷ durée totale."], ["60 ÷ 5 = 12 km/h."], units=["km/h"]),
    number("p29", "problemes", "Deux robinets de 30 L/min et 45 L/min remplissent un bassin de 900 L. En combien de minutes ?", Fraction(12), 2, ["Additionne les débits."], ["75 L/min.", "900 ÷ 75 = 12 min."], units=["min"]),
    number("p30", "problemes", "Un robinet de 20 L/min remplit un bassin de 600 L, mais une fuite perd 5 L/min. En combien de minutes le bassin est-il plein ?", Fraction(40), 3, ["Débit réel : 20 − 5."], ["15 L/min de gain.", "600 ÷ 15 = 40 min."], units=["min"]),
    choice("p31", "problemes", "A fait 120 km en 2 h. B fait 150 km en 3 h. Lequel est le plus rapide ?", ["A", "B", "Même vitesse"], 0, 1, ["Calcule les deux vitesses."], ["A : 60 km/h. B : 50 km/h."], wrong={1: "B roule à 50 km/h.", 2: "60 et 50 sont différents."}),
    number("p32", "problemes", "Une citerne contient 3 000 L d'un liquide de masse volumique 0,8 kg/L. Quelle est la masse du liquide, en kg ?", Fraction(2400), 2, ["m = ρ × V."], ["0,8 × 3 000 = 2 400 kg."], units=["kg"]),
]

SUMMARY = [
    rule("Proportionnalité", "Deux grandeurs sont proportionnelles si le quotient y ÷ x est toujours le même : c'est le coefficient. Sur un graphique, les points sont alignés sur une droite qui passe par l'origine."),
    rule("Vitesse moyenne", "v = d ÷ t ; d = v × t ; t = d ÷ v. Durée en heures pour une vitesse en km/h. km/h → m/s : ÷ 3,6. m/s → km/h : × 3,6. Vitesse moyenne sur plusieurs parties : distance totale ÷ durée totale."),
    rule("Débit et masse volumique", "Débit q = V ÷ t, V = q × t, t = V ÷ q. Masse volumique ρ = m ÷ V, m = ρ × V, V = m ÷ ρ. L'eau : 1 g/cm³ = 1 kg/L."),
    para("Les erreurs à éviter : mélanger minutes et heures ; faire la moyenne des vitesses au lieu de diviser la distance totale par la durée totale ; croire que des points alignés suffisent sans passer par l'origine ; oublier de convertir les unités."),
]

CONCEPTS = {
    "reconnaitre": ("Reconnaître une proportionnalité", "reconnaitre"),
    "vitesse": ("Vitesse moyenne", "vitesse"),
    "debit": ("Débit moyen et masse volumique", "debit"),
    "problemes": ("Problèmes de proportionnalité", "problemes"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    # 1. a table of proportionality or not
    k = rng.choice([2, 3, 4, 5, 6, 7, 9])
    xs = rng.sample(range(2, 12), 3)
    proportional = rng.random() < 0.5
    ys = [k * x for x in xs] if proportional else [k * x + rng.choice([-1, 1, 2]) * i for i, x in enumerate(xs)]
    table = " ; ".join(f"{x} → {y}" for x, y in zip(xs, ys))
    questions.append(choice("a1", "reconnaitre", f"Le tableau donne : {table}. Est-ce un tableau de proportionnalité ?", ["Oui", "Non"], 0 if proportional else 1, 1, ["Divise le deuxième nombre par le premier."],
                            [", ".join(f"{y} ÷ {x} = {show(Fraction(y, x))}" for x, y in zip(xs, ys)) + "."]))
    # 2. the coefficient from a point
    x = rng.randint(2, 12)
    k = Fraction(rng.choice([3, 5, 7, 9, 11, 13]), 2)
    y = k * x
    questions.append(number("a2", "reconnaitre", f"Le point A({x} ; {show(y)}) est sur la droite d'un graphique de proportionnalité. Quel est le coefficient de proportionnalité ?", k, 1, ["Ordonnée ÷ abscisse."], [f"{show(y)} ÷ {x} = {show(k)}."]))
    # 3. a speed
    v, t = rng.choice([40, 45, 50, 60, 75, 80, 90, 100]), rng.randint(2, 6)
    questions.append(number("a3", "vitesse", f"Un véhicule fait {v * t} km en {t} h. Quelle est sa vitesse moyenne, en km/h ?", Fraction(v), 1, ["Distance ÷ durée."], [f"{v * t} ÷ {t} = {v} km/h."], units=["km/h"]))
    # 4. a distance
    v, t = rng.choice([30, 40, 60, 70, 90]), Fraction(rng.randint(2, 9), 2)
    questions.append(number("a4", "vitesse", f"Un véhicule roule à {v} km/h pendant {show(t)} h. Quelle distance parcourt-il, en km ?", v * t, 2, ["d = v × t."], [f"{v} × {show(t)} = {show(v * t)} km."], units=["km"]))
    # 5. a duration
    v, t = rng.choice([20, 30, 40, 60, 80]), rng.randint(2, 7)
    questions.append(number("a5", "vitesse", f"Un véhicule roule à {v} km/h et fait {v * t} km. Combien de temps roule-t-il, en heures ?", Fraction(t), 2, ["t = d ÷ v."], [f"{v * t} ÷ {v} = {t} h."], units=["h"]))
    # 6. km/h to m/s
    ms = rng.randint(4, 40)
    kmh = Fraction(36 * ms, 10)
    questions.append(number("a6", "vitesse", f"Convertis {show(kmh)} km/h en m/s.", Fraction(ms), 2, ["Divise par 3,6."], [f"{show(kmh)} ÷ 3,6 = {ms} m/s."], units=["m/s"]))
    # 7. a flow rate
    q, t = rng.choice([10, 12, 15, 18, 20, 25, 30]), rng.randint(3, 20)
    questions.append(number("a7", "debit", f"Un robinet fournit {q * t} L en {t} min. Quel est son débit moyen, en L/min ?", Fraction(q), 1, ["Volume ÷ durée."], [f"{q * t} ÷ {t} = {q} L/min."], units=["L/min"]))
    # 8. a volume from a flow rate
    q, t = rng.choice([8, 12, 15, 20, 25, 40]), rng.randint(3, 25)
    questions.append(number("a8", "debit", f"Un tuyau a un débit de {q} L/min. Quel volume fournit-il en {t} min, en L ?", Fraction(q * t), 2, ["V = q × t."], [f"{q} × {t} = {q * t} L."], units=["L"]))
    # 9. a density
    rho = rng.choice([Fraction(9, 10), Fraction(27, 10), Fraction(78, 10), Fraction(113, 10), Fraction(75, 100), Fraction(136, 10)])
    volume = rng.choice([20, 40, 50, 100, 200])
    questions.append(number("a9", "debit", f"Un morceau de matière de {volume} cm³ a une masse de {show(rho * volume)} g. Quelle est sa masse volumique, en g/cm³ ?", rho, 2, ["Masse ÷ volume."],
                            [f"{show(rho * volume)} ÷ {volume} = {show(rho)} g/cm³."], units=["g/cm3", "g/cm³"]))
    # 10. a mass from a density
    rho = rng.choice([Fraction(8, 10), Fraction(9, 10), Fraction(1), Fraction(3, 2), Fraction(25, 100)])
    volume = rng.choice([4, 10, 20, 30, 50])
    questions.append(number("a10", "debit", f"Un liquide a une masse volumique de {show(rho)} kg/L. Quelle est la masse de {volume} L de ce liquide, en kg ?", rho * volume, 2, ["m = ρ × V."], [f"{show(rho)} × {volume} = {show(rho * volume)} kg."], units=["kg"]))
    # 11. two robinets
    a, b = rng.choice([10, 15, 20, 25]), rng.choice([20, 30, 35, 40])
    t = rng.randint(4, 15)
    questions.append(number("a11", "problemes", f"Deux robinets de {a} L/min et de {b} L/min coulent ensemble. En combien de minutes remplissent-ils un bassin de {(a + b) * t} L ?", Fraction(t), 3, ["Additionne les débits."],
                            [f"{a} + {b} = {a + b} L/min.", f"{(a + b) * t} ÷ {a + b} = {t} min."], units=["min"]))
    # 12. an average speed over two parts
    v1, v2 = rng.choice([(60, 40), (30, 20), (60, 30), (90, 60), (60, 20)])
    distance = Fraction(v1 * v2, 10) * rng.randint(1, 3)
    total_time = distance / v1 + distance / v2
    average = 2 * distance / total_time
    questions.append(number("a12", "problemes", f"Un trajet se fait en deux parties de {show(distance)} km chacune : la première à {v1} km/h, la seconde à {v2} km/h. Quelle est la vitesse moyenne sur tout le trajet, en km/h ? (Réponds par un nombre décimal exact.)", average, 3,
                            ["Distance totale ÷ durée totale."], [f"{show(distance)} ÷ {v1} + {show(distance)} ÷ {v2} = {show(total_time)} h.", f"{show(2 * distance)} ÷ {show(total_time)} = {show(average)} km/h."], units=["km/h"]))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="5e", number=4, title="Proportionnalité, vitesse, débit et masse volumique", language="fr",
    intro="Un véhicule qui roule à vitesse constante, un robinet qui coule, un morceau de métal : dans chacune de ces situations, deux grandeurs sont proportionnelles. "
          "Ce chapitre t'apprend à le reconnaître avec un tableau et un graphique, puis à calculer des vitesses, des débits et des masses volumiques.",
    objectives=["Reconnaître une situation de proportionnalité avec un tableau et avec un graphique.",
                "Lire les coordonnées d'un point et trouver le coefficient de proportionnalité.",
                "Calculer une vitesse moyenne, une distance et une durée, et convertir des vitesses.",
                "Calculer un débit moyen et une masse volumique.",
                "Résoudre des problèmes de proportionnalité à plusieurs étapes."],
    prerequisites=[{"text": "Connaître la proportionnalité et les pourcentages.", "chapter": "sn-6e-proportionnalite"},
                   {"text": "Multiplier et diviser des nombres décimaux.", "chapter": "sn-6e-division"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[CI_PROGRAMME_5E], also_for=("ci",),
    status_note="Fourth chapter of the Senegal Cinquième course. Its contents follow the proportionality lesson of the Côte d'Ivoire Cinquième programme (tables and graphs of proportionality, average speed, average flow rate and density), "
                "which was read for it, so it is also offered there, but the programme's own situations are not reproduced. Graphs are drawn by the app and read by the student: plotting on squared paper is not covered. "
                "It has not been checked against the official Senegalese programme.",
)
