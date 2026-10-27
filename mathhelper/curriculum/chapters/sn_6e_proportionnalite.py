"""Sixième, La proportionnalité: the fifth chapter of the Senegal Sixième course, written in French.

The topics follow the proportionality chapter of the ADEM-Dakar Sixième booklet. The list of contents was also checked against lesson 12
"Proportionnalité" of the Côte d'Ivoire Sixième programme (proportional quantities, coefficient, tables, linearity, percentages, scale), so the
chapter is offered to Côte d'Ivoire students as well. Every explanation, example and exercise was written independently, with our own numbers.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..checker import show
from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .kit import N, d, definition, example, make_kit, para, rand_decimal, rule, warning

CHAPTER_ID = "sn-6e-proportionnalite"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")

# ----- Section 1: recognising proportional quantities -----
S1 = Section(
    "reconnaitre", "Reconnaître une situation de proportionnalité", 22, "reconnaitre",
    "Reconnaître un tableau de proportionnalité, trouver son coefficient et justifier qu'une situation n'est pas proportionnelle.",
    [
        para("Un kilogramme de sucre coûte 600 F. Deux kilogrammes coûtent 1 200 F, trois kilogrammes coûtent 1 800 F. Quand la quantité double, le prix double ; quand elle triple, le prix triple. "
             "On dit que la quantité de sucre et le prix sont des grandeurs proportionnelles."),
        definition("Tableau de proportionnalité et coefficient",
                   "Deux suites de nombres sont proportionnelles quand on passe de chaque nombre de la première suite au nombre correspondant de la seconde en le multipliant toujours par le même nombre. "
                   "Ce nombre s'appelle le coefficient de proportionnalité. Le tableau qui les range en deux lignes est un tableau de proportionnalité."),
        rule("Les propriétés de linéarité",
             "Dans un tableau de proportionnalité : si on multiplie un nombre de la première ligne par k, le nombre correspondant de la seconde ligne est aussi multiplié par k ; "
             "et la somme de deux nombres de la première ligne correspond à la somme des deux nombres correspondants de la seconde ligne."),
        example("Exemple 1", "Le tableau donne le prix du sucre : 1 kg → 600 F, 2 kg → 1 200 F, 5 kg → 3 000 F. Est-ce un tableau de proportionnalité ? Quel est le coefficient ?",
                "On cherche le nombre par lequel on multiplie chaque quantité pour trouver le prix, et on vérifie que c'est toujours le même.",
                [(N("600 \\div 1") + " = " + N("600"), "Pour 1 kg, le prix est 600 F : le coefficient pourrait être 600."),
                 (N("1200 \\div 2") + " = " + N("600"), "Pour 2 kg : 1 200 ÷ 2 = 600. Même nombre."),
                 (N("3000 \\div 5") + " = " + N("600"), "Pour 5 kg : 3 000 ÷ 5 = 600. Toujours le même nombre."),
                 ("C'est un tableau de proportionnalité, de coefficient 600", "Le coefficient est le prix d'un kilogramme : 600 F par kg.")],
                "Oui, avec le coefficient " + N("600") + ".", "1200/2==600 and 3000/5==600 and 600/1==600"),
        example("Exemple 2", "Un enfant mesure 100 cm à 5 ans et 140 cm à 10 ans. La taille est-elle proportionnelle à l'âge ?",
                "On calcule le coefficient pour chaque ligne : s'il change, ce n'est pas un tableau de proportionnalité.",
                [(N("100 \\div 5") + " = " + N("20"), "À 5 ans, la taille divisée par l'âge vaut 20."),
                 (N("140 \\div 10") + " = " + N("14"), "À 10 ans, elle vaut 14. Ce n'est pas le même nombre."),
                 ("Ce n'est pas un tableau de proportionnalité", "L'âge a doublé, mais la taille n'a pas doublé : 200 cm serait impossible à 10 ans.")],
                "Non, la taille n'est pas proportionnelle à l'âge.", "100/5==20 and 140/10==14 and 20!=14"),
        example("Exemple 3", "Dans un tableau de proportionnalité, 4 correspond à 14. Quel est le coefficient ? Compléter avec 6 et 10.",
                "Le coefficient est le nombre qui fait passer de 4 à 14 : on le trouve par une division.",
                [(N("14 \\div 4") + " = " + N("3,5"), "Le coefficient est 3,5. Vérification : 4 × 3,5 = 14."),
                 (N("6 \\times 3,5") + " = " + N("21"), "À 6 correspond 6 × 3,5 = 21."),
                 (N("10 \\times 3,5") + " = " + N("35"), "À 10 correspond 10 × 3,5 = 35.")],
                "Coefficient " + N("3,5") + ", donc 6 correspond à " + N("21") + " et 10 à " + N("35"), "d('14')/4==d('3,5') and 6*d('3,5')==21 and 10*d('3,5')==35"),
        example("Exemple 4", "Pour 4 personnes, une recette demande 600 g de riz. Quelle quantité faut-il pour 6 personnes et pour 10 personnes ?",
                "Le nombre de personnes et la quantité de riz sont proportionnels. Le coefficient est la quantité de riz par personne.",
                [(N("600 \\div 4") + " = " + N("150"), "Il faut 150 g de riz par personne : c'est le coefficient."),
                 (N("6 \\times 150") + " = " + N("900"), "Pour 6 personnes : 900 g."),
                 (N("10 \\times 150") + " = " + N("1500"), "Pour 10 personnes : 1 500 g."),
                 ("Vérification par linéarité : $6 + 4 = 10$ et $900 + 600 = 1500$", "La somme des quantités de riz pour 6 et 4 personnes est la quantité pour 10 personnes.")],
                N("900") + " g et " + N("1500") + " g", "600/4==150 and 6*150==900 and 10*150==1500 and 900+600==1500"),
        warning("Des nombres qui augmentent ensemble ne forment pas toujours un tableau de proportionnalité. Ajouter le même nombre n'est pas multiplier par le même nombre : "
                "les nombres 2, 4, 6 et 5, 7, 9 augmentent ensemble, mais 5 ÷ 2 = 2,5 et 7 ÷ 4 = 1,75 ne sont pas égaux."),
    ],
    [
        number("s1-g1", "reconnaitre", "Dans un tableau de proportionnalité, 5 correspond à 40. Quel est le coefficient ?", Fraction(8),
               hints=["Par quel nombre faut-il multiplier 5 pour obtenir 40 ?"], solution=["Le coefficient est 40 ÷ 5 = 8.", "Vérification : 5 × 8 = 40."]),
        number("s1-g2", "reconnaitre", "Dans un tableau de proportionnalité de coefficient 2,5, quel nombre correspond à 6 ?", Fraction(15),
               hints=["On multiplie par le coefficient."], solution=["6 × 2,5 = 15."]),
        choice("s1-g3", "reconnaitre", "Quel tableau est un tableau de proportionnalité ? (première ligne et deuxième ligne)",
               [N("2 ; 5 ; 7") + " et " + N("6 ; 15 ; 21"), N("2 ; 5 ; 7") + " et " + N("6 ; 9 ; 11"), N("2 ; 5 ; 7") + " et " + N("5 ; 8 ; 10")], 0,
               hints=["Calcule le rapport de chaque nombre de la deuxième ligne à celui de la première."],
               solution=["Pour le premier tableau : 6 ÷ 2 = 3, 15 ÷ 5 = 3 et 21 ÷ 7 = 3 : le coefficient est toujours 3.", "Dans les deux autres, les rapports ne sont pas tous égaux."],
               wrong={1: "6 ÷ 2 = 3 mais 9 ÷ 5 = 1,8 : le rapport change, ce n'est pas un tableau de proportionnalité.",
                      2: "Ici on passe de la première à la deuxième ligne en ajoutant 3, pas en multipliant : ce n'est pas de la proportionnalité."}),
        number("s1-g4", "reconnaitre", "3 mètres de tissu coûtent 4 500 F. Quel est le coefficient de proportionnalité (le prix d'un mètre, en F) ?", Fraction(1500), units=["F"],
               hints=["Le coefficient est le prix pour 1 mètre."], solution=["4 500 ÷ 3 = 1 500.", "Un mètre coûte 1 500 F."]),
        choice("s1-g5", "reconnaitre", "Une fillette mesure 80 cm à 2 ans et 120 cm à 6 ans. La taille est-elle proportionnelle à l'âge ?", ["Oui, car les deux nombres augmentent", "Non, car le rapport 80 ÷ 2 = 40 est différent de 120 ÷ 6 = 20", "Oui, car 120 est plus grand que 80"], 1,
               hints=["Calcule la taille divisée par l'âge dans chaque cas."], solution=["80 ÷ 2 = 40 et 120 ÷ 6 = 20 : le rapport change.", "La taille n'est pas proportionnelle à l'âge."],
               wrong={0: "Les deux nombres augmentent, mais cela ne suffit pas : il faut que le rapport reste le même.", 2: "Le fait que 120 soit plus grand que 80 ne prouve rien. Il faut comparer les rapports."}),
    ])

# ----- Section 2: computing a missing value -----
S2 = Section(
    "calculer", "Calculer une valeur manquante", 24, "calculer",
    "Trouver un nombre manquant dans une situation de proportionnalité par le coefficient, le passage à l'unité ou la linéarité.",
    [
        para("Dans un tableau de proportionnalité, quand un nombre est inconnu, on peut le retrouver par plusieurs méthodes. On choisit celle qui rend le calcul le plus simple. "
             "Ce nombre inconnu s'appelle la quatrième proportionnelle, parce qu'on connaît trois nombres du tableau et qu'on cherche le quatrième."),
        rule("Trois méthodes",
             "Par le coefficient : on calcule le coefficient avec la colonne complète, puis on multiplie. Par le passage à l'unité : on cherche d'abord la valeur pour 1, puis on multiplie. "
             "Par la linéarité : on multiplie ou on additionne des colonnes entre elles."),
        example("Exemple 1", "7 m de tissu coûtent 10 500 F. Combien coûtent 12 m ? (méthode du coefficient)",
                "On calcule le prix d'un mètre, qui est le coefficient, puis on multiplie.",
                [(N("10500 \\div 7") + " = " + N("1500"), "Le coefficient est 1 500 : un mètre coûte 1 500 F."),
                 (N("12 \\times 1500") + " = " + N("18000"), "12 m coûtent 12 × 1 500 = 18 000 F.")],
                "12 m coûtent 18 000 F.", "10500/7==1500 and 12*1500==18000"),
        example("Exemple 2", "5 cahiers coûtent 1 250 F. Combien coûtent 8 cahiers ? (passage à l'unité)",
                "On cherche le prix d'un seul cahier, puis le prix de 8 cahiers.",
                [(N("1250 \\div 5") + " = " + N("250"), "Un cahier coûte 250 F."),
                 (N("8 \\times 250") + " = " + N("2000"), "8 cahiers coûtent 8 × 250 = 2 000 F.")],
                "8 cahiers coûtent 2 000 F.", "1250/5==250 and 8*250==2000"),
        example("Exemple 3", "5 stylos coûtent 750 F. Combien coûtent 15 stylos et 20 stylos ? (linéarité)",
                "15 est le triple de 5 : le prix est aussi triplé. 20 est la somme de 15 et de 5 : le prix est la somme des deux prix.",
                [(N("15 = 3 \\times 5") + " donc " + N("3 \\times 750") + " = " + N("2250"), "Linéarité du produit : 15 stylos coûtent 2 250 F."),
                 (N("20 = 15 + 5") + " donc " + N("2250 + 750") + " = " + N("3000"), "Linéarité de la somme : 20 stylos coûtent 3 000 F.")],
                "15 stylos : 2 250 F ; 20 stylos : 3 000 F.", "3*750==2250 and 2250+750==3000 and 20*(750//5)==3000"),
        example("Exemple 4", "Pour 9 mesures de farine, un gâteau demande 6 mesures d'eau. Combien d'eau faut-il pour 15 mesures de farine ?",
                "Le coefficient n'est pas un nombre entier, mais le passage par une petite quantité aide : 9 et 6 sont tous les deux multiples de 3.",
                [("9 mesures de farine ↔ 6 mesures d'eau", "On part des nombres connus."),
                 (N("9 \\div 3 = 3") + " et " + N("6 \\div 3 = 2"), "On divise les deux nombres par 3 : 3 mesures de farine ↔ 2 mesures d'eau."),
                 (N("15 = 5 \\times 3") + " donc " + N("5 \\times 2") + " = " + N("10"), "15 mesures de farine, c'est 5 fois 3 mesures : il faut 5 × 2 = 10 mesures d'eau.")],
                "Il faut 10 mesures d'eau.", "6*15/9==10 and 5*2==10"),
        example("Exemple 5", "Un cycliste roule à vitesse constante : il parcourt 120 km en 1,5 h. Quelle distance parcourt-il en 4 h ?",
                "À vitesse constante, la distance est proportionnelle au temps. Le coefficient est la distance parcourue en 1 heure.",
                [(N("120 \\div 1,5") + " = " + N("80"), "En 1 h, il parcourt 80 km : 120 ÷ 1,5 = 1 200 ÷ 15 = 80."),
                 (N("4 \\times 80") + " = " + N("320"), "En 4 h, il parcourt 4 × 80 = 320 km.")],
                "Il parcourt 320 km.", "d('120')/d('1,5')==80 and 4*80==320"),
        warning("Avant de calculer, vérifie que la situation est bien proportionnelle. Si 1 maçon construit un mur en 12 jours, 2 maçons ne le construisent pas en 24 jours : plus de maçons, moins de jours. Ce n'est pas de la proportionnalité."),
    ],
    [
        number("s2-g1", "calculer", "Dans un tableau de proportionnalité, 6 correspond à 15. Quel nombre correspond à 10 ?", Fraction(25),
               hints=["Trouve d'abord le coefficient."], solution=["Le coefficient est 15 ÷ 6 = 2,5.", "10 × 2,5 = 25."]),
        number("s2-g2", "calculer", "6 kg de riz coûtent 3 600 F. Combien coûtent 10 kg ? (passage à l'unité)", Fraction(6000), units=["F"],
               hints=["Quel est le prix de 1 kg ?"], solution=["1 kg coûte 3 600 ÷ 6 = 600 F.", "10 kg coûtent 10 × 600 = 6 000 F."]),
        number("s2-g3", "calculer", "Dans un tableau de proportionnalité, 4 correspond à 10. Quel nombre correspond à 12 ? (linéarité)", Fraction(30),
               hints=["12 est le triple de 4 : que se passe-t-il pour l'autre nombre ?"], solution=["12 = 3 × 4, donc le nombre correspondant est 3 × 10 = 30."]),
        number("s2-g4", "calculer", "Dans un tableau de proportionnalité, 2 correspond à 5 et 3 correspond à 7,5. Quel nombre correspond à 5 ?", d("12,5"),
               hints=["5 est la somme de deux nombres de la première ligne. Lesquels ?"], solution=["5 = 2 + 3, donc le nombre correspondant est 5 + 7,5 = 12,5."], form="decimal"),
        number("s2-g5", "calculer", "Une recette demande 8 œufs pour 6 personnes. Combien d'œufs faut-il pour 15 personnes ?", Fraction(20),
               hints=["8 œufs pour 6 personnes : trouve combien d'œufs pour 3 personnes."], solution=["6 personnes ↔ 8 œufs, donc 3 personnes ↔ 4 œufs.", "15 = 5 × 3, donc 5 × 4 = 20 œufs."]),
    ])

# ----- Section 3: percentages and scales -----
S3 = Section(
    "pourcentage", "Pourcentages et échelles", 24, "pourcentage",
    "Calculer un pourcentage d'une quantité, exprimer une proportion en pourcentage et utiliser une échelle.",
    [
        para("Dans un magasin, une affiche annonce « 20 % de réduction ». Que veut dire 20 % ? Un pourcentage est une proportion pour 100. Dire 20 %, c'est dire « 20 pour 100 », "
             "c'est-à-dire 20 sur chaque tranche de 100."),
        definition("Pourcentage",
                   "Dire que " + N("p") + " % d'une quantité, c'est prendre " + N("p") + " pour chaque 100 de cette quantité : " + N("p\\ \\%") + " = " + "$\\dfrac{p}{100}$" + ". "
                   "Par exemple " + N("25\\ \\%") + " = " + N("25/100") + " = " + N("0,25") + ". Pour calculer " + N("p\\ \\%") + " d'une quantité, on la multiplie par " + "$\\dfrac{p}{100}$" + "."),
        example("Exemple 1", "Calculer 20 % de 450 F.",
                "20 % = 20/100 = 0,2 : on multiplie 450 par 0,2.",
                [(N("20\\ \\%") + " = " + N("20/100") + " = " + N("0,2"), "On écrit le pourcentage sous forme décimale."),
                 (N("450 \\times 0,2") + " = " + N("90"), "450 × 2 = 900, avec un chiffre après la virgule : 90,0 = 90."),
                 ("Vérification par proportionnalité : 10 % de 450 est 45, donc 20 % est 90", "10 % c'est la dixième partie : 450 ÷ 10 = 45, et 20 % est le double.")],
                "20 % de 450 F sont 90 F.", "d('0,2')*450==90 and 450/10*2==90"),
        example("Exemple 2", "Un article coûte 2 000 F. Une réduction de 15 % est annoncée. Quel est le prix à payer ?",
                "On calcule la réduction, puis on la retire du prix.",
                [(N("15\\ \\%") + " de 2 000 : " + N("2000 \\times 0,15") + " = " + N("300"), "2 000 × 15 = 30 000, avec 2 chiffres après la virgule : 300,00 = 300."),
                 (N("2000 - 300") + " = " + N("1700"), "On retire la réduction du prix de départ.")],
                "Le prix à payer est 1 700 F.", "2000*d('0,15')==300 and 2000-300==1700"),
        example("Exemple 3", "Dans une classe de 24 élèves, 18 sont des filles. Quel est le pourcentage de filles ?",
                "On cherche la proportion de filles sur 100 élèves : on écrit la fraction, puis on la ramène à 100.",
                [(N("18/24") + " = " + N("18 \\div 24") + " = " + N("0,75"), "La fraction de filles est 18/24, c'est-à-dire 0,75."),
                 (N("0,75") + " = " + N("75/100") + " = " + N("75\\ \\%"), "0,75 = 75 centièmes : 75 sur 100.")],
                "75 % des élèves sont des filles.", "d('18')/24==d('0,75') and d('0,75')==d('75')/100"),
        definition("Échelle",
                   "Sur une carte à l'échelle " + "$\\dfrac{1}{50000}$" + ", une longueur de 1 cm sur la carte représente 50 000 cm sur le terrain. Les longueurs sur la carte et sur le terrain sont proportionnelles, "
                   "et le coefficient pour passer de la carte au terrain est 50 000, l'inverse de l'échelle."),
        example("Exemple 4", "Sur une carte à l'échelle 1/50 000, deux villages sont séparés de 6 cm. Quelle est la distance réelle ?",
                "Chaque centimètre de la carte représente 50 000 cm. On multiplie, puis on convertit.",
                [(N("6 \\times 50000") + " = " + N("300000"), "6 cm sur la carte représentent 300 000 cm sur le terrain."),
                 (N("300000") + " cm = " + N("3000") + " m = " + N("3") + " km", "300 000 cm ÷ 100 = 3 000 m, puis 3 000 m ÷ 1 000 = 3 km.")],
                "La distance réelle est 3 km.", "6*50000==300000 and 300000/100/1000==3"),
        example("Exemple 5", "Sur la même carte, quelle longueur représente une distance réelle de 2,5 km ?",
                "On convertit la distance réelle en centimètres, puis on divise par 50 000.",
                [(N("2,5") + " km = " + N("2500") + " m = " + N("250000") + " cm", "2,5 km × 1 000 = 2 500 m, puis × 100 = 250 000 cm."),
                 (N("250000 \\div 50000") + " = " + N("5"), "250 000 ÷ 50 000 = 25 ÷ 5 = 5.")],
                "Sur la carte, la longueur est 5 cm.", "d('2,5')*1000*100/50000==5"),
        warning("Un pourcentage s'applique à une quantité : « 20 % » seul ne veut rien dire. 20 % de 450 F fait 90 F, mais 20 % de 1 000 F fait 200 F. Et ne confonds pas échelle 1/50 000 et 50 000 : sur la carte c'est une longueur 50 000 fois plus petite."),
    ],
    [
        number("s3-g1", "pourcentage", "Calcule 25 % de 80.", Fraction(20),
               hints=["25 % = 25/100 = 0,25. Que faut-il faire avec 80 ?"], solution=["25 % = 0,25.", "80 × 0,25 = 20."]),
        number("s3-g2", "pourcentage", "Calcule 15 % de 200 F.", Fraction(30), units=["F"],
               hints=["Écris 15 % sous forme décimale."], solution=["15 % = 0,15.", "200 × 0,15 = 30 F."]),
        number("s3-g3", "pourcentage", "Dans une classe de 40 élèves, 12 ont plus de 12 ans. Quel pourcentage cela représente-t-il ? (en %)", Fraction(30),
               hints=["Écris la fraction 12/40 sous forme décimale, puis en centièmes."], solution=["12 ÷ 40 = 0,3.", "0,3 = 30/100 = 30 %."], units=["%"]),
        number("s3-g4", "echelle", "Sur un plan à l'échelle 1/1 000, une longueur mesure 4 cm. Quelle est la longueur réelle, en mètres ?", Fraction(40), units=["m"],
               hints=["1 cm sur le plan représente 1 000 cm dans la réalité."], solution=["4 × 1 000 = 4 000 cm.", "4 000 cm = 40 m."]),
        number("s3-g5", "pourcentage", "Un sac coûte 5 000 F. Il est soldé avec 10 % de réduction. Combien paie-t-on, en F ?", Fraction(4500), units=["F"],
               hints=["Calcule d'abord la réduction, puis retire-la."], solution=["10 % de 5 000 = 5 000 × 0,1 = 500 F.", "5 000 − 500 = 4 500 F."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    number("p1", "reconnaitre", "Dans un tableau de proportionnalité, 2 correspond à 9. Quel est le coefficient ?", d("4,5"), 1, ["Divise 9 par 2."], ["9 ÷ 2 = 4,5. Vérification : 2 × 4,5 = 9."], form="decimal"),
    number("p2", "reconnaitre", "Dans un tableau de proportionnalité de coefficient 12, quel nombre correspond à 5 ?", Fraction(60), 1, ["Multiplie par le coefficient."], ["5 × 12 = 60."]),
    choice("p3", "reconnaitre", "Quel tableau est de proportionnalité ? (première ligne et deuxième ligne)", [N("1 ; 2 ; 4") + " et " + N("3 ; 6 ; 12"), N("1 ; 2 ; 4") + " et " + N("3 ; 5 ; 9"), N("1 ; 2 ; 4") + " et " + N("2 ; 3 ; 5")], 0, 1,
           ["Calcule les rapports."], ["3 ÷ 1 = 3, 6 ÷ 2 = 3, 12 ÷ 4 = 3 : le coefficient est toujours 3."],
           wrong={1: "5 ÷ 2 = 2,5 alors que 3 ÷ 1 = 3 : le rapport change.", 2: "On passe de la première à la deuxième ligne en ajoutant 1 : ce n'est pas de la proportionnalité."}),
    choice("p4", "reconnaitre", "2 stylos coûtent 300 F et 3 stylos coûtent 400 F. Le prix est-il proportionnel au nombre de stylos ?", ["Oui", "Non, car 300 ÷ 2 = 150 et 400 ÷ 3 n'est pas égal à 150", "On ne peut pas savoir"], 1, 2,
           ["Calcule le prix par stylo dans chaque cas."], ["300 ÷ 2 = 150 mais 400 ÷ 3 = 133,33... : le prix par stylo change, donc ce n'est pas proportionnel."],
           wrong={0: "Si le prix était proportionnel, 3 stylos coûteraient 450 F, pas 400 F."}),
    number("p5", "reconnaitre", "Un kilogramme de poisson coûte 600 F. Combien coûtent 3,5 kg ?", Fraction(2100), 2, ["Le coefficient est 600."], ["3,5 × 600 = 2 100 F."], units=["F"]),
    number("p6", "reconnaitre", "Dans un tableau de proportionnalité de coefficient 0,25, quel nombre correspond à 36 ?", Fraction(9), 2, ["Multiplie par 0,25 : c'est prendre le quart."], ["36 × 0,25 = 9."]),
    choice("p7", "reconnaitre", "Awa a 8 ans et pèse 25 kg. Elle dit : « À 16 ans, je pèserai 50 kg, car mon âge doublera ». A-t-elle raison ?", ["Oui, car 16 est le double de 8", "Non : le poids d'une personne n'est pas proportionnel à son âge", "Oui, car 50 est le double de 25"], 1, 3,
           ["Pense à un adulte de 80 ans : pèserait-il 250 kg ?"], ["Avec ce raisonnement, à 80 ans elle pèserait 250 kg, ce qui est absurde.", "Le poids et l'âge ne sont pas des grandeurs proportionnelles."],
           wrong={0: "Les nombres sont bien doublés, mais cela ne suffit pas : il faut que la situation soit réellement proportionnelle, ce qui n'est pas le cas du poids et de l'âge.", 2: "Doubler le poids parce que l'âge double suppose la proportionnalité, qui est ici fausse."}),
    number("p8", "reconnaitre", "Dans un tableau de proportionnalité, 3 correspond à 12 et 7 correspond à 28. Quel nombre correspond à 10 ?", Fraction(40), 2, ["10 = 3 + 7 : utilise la linéarité de la somme."], ["12 + 28 = 40."]),
    number("p9", "calculer", "9 m de tissu coûtent 13 500 F. Combien coûtent 4 m ?", Fraction(6000), 2, ["Prix d'un mètre ?"], ["13 500 ÷ 9 = 1 500 F le mètre.", "4 × 1 500 = 6 000 F."], units=["F"]),
    number("p10", "calculer", "8 cahiers coûtent 2 000 F. Combien coûtent 5 cahiers ?", Fraction(1250), 1, ["Prix d'un cahier ?"], ["2 000 ÷ 8 = 250.", "5 × 250 = 1 250 F."], units=["F"]),
    number("p11", "calculer", "3 kg de mangues coûtent 2 100 F. Combien coûtent 5 kg ?", Fraction(3500), 2, ["Passage à l'unité."], ["2 100 ÷ 3 = 700 F le kilogramme.", "5 × 700 = 3 500 F."], units=["F"]),
    number("p12", "calculer", "Une voiture roule à vitesse constante et parcourt 240 km en 3 h. Quelle distance parcourt-elle en 5 h ?", Fraction(400), 2, ["Distance parcourue en 1 heure ?"], ["240 ÷ 3 = 80 km en 1 h.", "5 × 80 = 400 km."], units=["km"]),
    number("p13", "calculer", "Pour 5 personnes, une recette demande 750 g de riz. Combien faut-il de riz pour 8 personnes, en g ?", Fraction(1200), 2, ["Riz par personne ?"], ["750 ÷ 5 = 150 g par personne.", "8 × 150 = 1 200 g."], units=["g"]),
    number("p14", "calculer", "Une voiture consomme 20 L pour 300 km. Quelle quantité de carburant faut-il pour 450 km, en L ?", Fraction(30), 3, ["300 km → 20 L : combien de litres pour 150 km ?"], ["450 = 300 + 150. Pour 150 km (la moitié de 300) il faut 10 L.", "20 + 10 = 30 L."], units=["L"]),
    number("p15", "calculer", "12 kg de farine coûtent 9 000 F. Combien coûtent 5 kg ?", Fraction(3750), 3, ["Prix d'un kilogramme ?"], ["9 000 ÷ 12 = 750 F le kilogramme.", "5 × 750 = 3 750 F."], units=["F"]),
    number("p16", "calculer", "7 stylos coûtent 1 050 F. Combien coûtent 12 stylos ?", Fraction(1800), 2, ["Prix d'un stylo ?"], ["1 050 ÷ 7 = 150 F.", "12 × 150 = 1 800 F."], units=["F"]),
    number("p17", "calculer", "Dans un tableau de proportionnalité, 6 correspond à 15 et 10 correspond à ?", Fraction(25), 2, ["Coefficient : 15 ÷ 6 = 2,5."], ["15 ÷ 6 = 2,5.", "10 × 2,5 = 25."]),
    number("p18", "calculer", "Un robinet remplit 18 L en 4 minutes. Combien de litres coule-t-il en 10 minutes, à débit constant ?", d("45"), 3, ["Litres par minute : 18 ÷ 4 = 4,5."], ["18 ÷ 4 = 4,5 L par minute.", "10 × 4,5 = 45 L."], units=["L"]),
    number("p19", "pourcentage", "Calcule 50 % de 360.", Fraction(180), 1, ["50 % = la moitié."], ["50 % de 360 = 360 × 0,5 = 180."]),
    number("p20", "pourcentage", "Calcule 10 % de 4 500 F.", Fraction(450), 1, ["10 % = 0,1."], ["4 500 × 0,1 = 450 F."], units=["F"]),
    number("p21", "pourcentage", "Calcule 25 % de 120.", Fraction(30), 1, ["25 % = le quart."], ["120 × 0,25 = 30."]),
    number("p22", "pourcentage", "Sur 120 élèves, 30 sont absents. Quel pourcentage cela représente-t-il ? (en %)", Fraction(25), 2, ["30/120 = ?"], ["30 ÷ 120 = 0,25.", "0,25 = 25/100 = 25 %."], units=["%"]),
    number("p23", "pourcentage", "45 élèves sur 60 ont réussi un test. Quel pourcentage ? (en %)", Fraction(75), 2, ["Écris 45/60 sous forme décimale."], ["45 ÷ 60 = 0,75 = 75 %."], units=["%"]),
    number("p24", "pourcentage", "Un article coûte 3 500 F. Il est soldé avec 20 % de réduction. Quel est le prix à payer, en F ?", Fraction(2800), 2, ["Réduction d'abord."], ["20 % de 3 500 = 700 F.", "3 500 − 700 = 2 800 F."], units=["F"]),
    number("p25", "pourcentage", "Dans une école de 400 élèves, 35 % sont des filles du cycle de base. Combien d'élèves cela fait-il ?", Fraction(140), 2, ["35 % = 0,35."], ["400 × 0,35 = 140 élèves."]),
    number("p26", "pourcentage", "Calcule 12 % de 250.", Fraction(30), 3, ["12 % = 0,12."], ["250 × 0,12 = 30."]),
    number("p27", "echelle", "Sur un plan à l'échelle 1/10 000, une rue mesure 3 cm. Quelle est sa longueur réelle, en m ?", Fraction(300), 2, ["3 × 10 000 = 30 000 cm : convertis en mètres."], ["3 cm × 10 000 = 30 000 cm.", "30 000 cm = 300 m."], units=["m"]),
    number("p28", "echelle", "Sur une carte à l'échelle 1/25 000, deux points sont séparés de 8 cm. Quelle est la distance réelle, en km ?", Fraction(2), 2, ["8 × 25 000 = 200 000 cm."], ["200 000 cm = 2 000 m = 2 km."], units=["km"]),
    number("p29", "echelle", "Deux villes sont distantes de 3 km. Quelle longueur les sépare sur une carte à l'échelle 1/50 000, en cm ?", Fraction(6), 3, ["3 km = 300 000 cm."], ["300 000 ÷ 50 000 = 6 cm."], units=["cm"]),
    number("p30", "echelle", "Sur un plan à l'échelle 1/500, une pièce mesure 7 cm de long. Quelle est sa longueur réelle, en m ?", d("35"), 3, ["7 × 500 = 3 500 cm."], ["3 500 cm = 35 m."], units=["m"]),
    choice("p31", "echelle", "Que signifie l'échelle 1/200 sur un plan ?", ["1 cm sur le plan représente 200 cm dans la réalité", "1 cm dans la réalité représente 200 cm sur le plan", "Le plan fait 200 cm de long"], 0, 1,
           ["Le plan est une réduction de la réalité."], ["Sur un plan à l'échelle 1/200, chaque longueur est 200 fois plus petite que dans la réalité : 1 cm sur le plan représente 200 cm réels."],
           wrong={1: "Le plan représente la réalité en plus petit : une longueur sur le plan est plus petite que la longueur réelle."}),
    number("p32", "echelle", "Sur une carte, 3 cm représentent 15 km sur le terrain. À quoi correspond 1 cm sur la carte, en cm sur le terrain ?", Fraction(500000), 3,
           ["Convertis 15 km en cm, puis divise par 3."], ["15 km = 1 500 000 cm.", "1 500 000 ÷ 3 = 500 000 : l'échelle est 1/500 000."], units=["cm"]),
]

SUMMARY = [
    definition("Proportionnalité", "Deux grandeurs sont proportionnelles quand on passe des valeurs de l'une aux valeurs de l'autre en multipliant toujours par le même nombre, le coefficient de proportionnalité. "
                                   "Pour le vérifier, on calcule le rapport de chaque valeur de la seconde ligne à la valeur correspondante de la première : il doit être toujours le même."),
    rule("Trouver une valeur manquante", "Par le coefficient (on le calcule avec une colonne complète), par le passage à l'unité (la valeur pour 1), ou par la linéarité (multiplier ou additionner des colonnes)."),
    rule("Pourcentage", N("p\\ \\%") + " = " + "$\\dfrac{p}{100}$" + ". Pour calculer " + N("p\\ \\%") + " d'une quantité, on la multiplie par " + "$\\dfrac{p}{100}$" + ". Pour exprimer une proportion en pourcentage, on écrit la fraction, puis on la ramène à 100."),
    rule("Échelle", "À l'échelle 1/n, une longueur sur la carte est n fois plus petite que la longueur réelle. Pour passer de la carte à la réalité, on multiplie par n ; pour passer de la réalité à la carte, on divise par n."),
    para("Les erreurs à éviter : croire que deux nombres qui augmentent ensemble sont proportionnels ; mélanger les lignes d'un tableau ; oublier de convertir les unités avec une échelle ; appliquer un pourcentage à la mauvaise quantité."),
]

CONCEPTS = {
    "reconnaitre": ("Reconnaître la proportionnalité", "reconnaitre"),
    "calculer": ("Calculer une valeur manquante", "calculer"),
    "pourcentage": ("Pourcentages", "pourcentage"),
    "echelle": ("Échelles", "pourcentage"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    # 1. find the coefficient
    k = rng.choice([Fraction(3), Fraction(4), Fraction(5), Fraction(25, 10), Fraction(15, 10), Fraction(12)])
    base = rng.randint(2, 9)
    questions.append(number("a1", "reconnaitre", f"Dans un tableau de proportionnalité, {base} correspond à {show(base * k)}. Quel est le coefficient ?", k, 1,
                            [f"Divise {show(base * k)} par {base}."], [f"{show(base * k)} ÷ {base} = {show(k)}.", f"Vérification : {base} × {show(k)} = {show(base * k)}."], form="decimal"))
    # 2. complete with the coefficient
    k = rng.choice([Fraction(3), Fraction(6), Fraction(25, 10), Fraction(15, 10), Fraction(8)])
    base, other = rng.randint(2, 9), rng.randint(10, 20)
    questions.append(number("a2", "calculer", f"Dans un tableau de proportionnalité, {base} correspond à {show(base * k)}. Quel nombre correspond à {other} ?", other * k, 2,
                            ["Trouve d'abord le coefficient."], [f"Coefficient : {show(base * k)} ÷ {base} = {show(k)}.", f"{other} × {show(k)} = {show(other * k)}."]))
    # 3. unit method
    n, unit_price, m = rng.randint(3, 9), rng.choice([150, 200, 250, 300, 350, 400, 450, 600]), rng.randint(2, 12)
    while m == n:
        m = rng.randint(2, 12)
    questions.append(number("a3", "calculer", f"{n} cahiers coûtent {n * unit_price} F. Combien coûtent {m} cahiers, en F ?", Fraction(m * unit_price), 2, ["Calcule le prix d'un cahier."],
                            [f"{n * unit_price} ÷ {n} = {unit_price} F le cahier.", f"{m} × {unit_price} = {m * unit_price} F."], units=["F"]))
    # 4. linearity, multiple
    a, b = rng.randint(2, 7), rng.randint(3, 9) * 5
    times = rng.randint(2, 6)
    questions.append(number("a4", "calculer", f"Dans un tableau de proportionnalité, {a} correspond à {b}. Quel nombre correspond à {a * times} ? (linéarité)", Fraction(b * times), 2,
                            [f"{a * times} est combien de fois {a} ?"], [f"{a * times} = {times} × {a}, donc le nombre correspondant est {times} × {b} = {b * times}."]))
    # 5. linearity, sum
    a, c = rng.randint(2, 6), rng.randint(2, 6)
    k = rng.choice([Fraction(3), Fraction(5), Fraction(25, 10), Fraction(15, 10)])
    if (a, c, k) == (2, 3, Fraction(25, 10)):
        k = Fraction(3)
    questions.append(number("a5", "calculer", f"Dans un tableau de proportionnalité, {a} correspond à {show(a * k)} et {c} correspond à {show(c * k)}. Quel nombre correspond à {a + c} ?", (a + c) * k, 3,
                            [f"{a + c} est la somme de {a} et de {c}."], [f"{a + c} = {a} + {c}, donc le nombre correspondant est {show(a * k)} + {show(c * k)} = {show((a + c) * k)}."]))
    # 6. which table is proportional
    k = rng.randint(2, 6)
    xs = [rng.randint(1, 3), rng.randint(4, 6), rng.randint(7, 9)]
    good = f"{N(' ; '.join(map(str, xs)))} et {N(' ; '.join(str(x * k) for x in xs))}"
    shift = k + rng.randint(1, 3)
    additive = f"{N(' ; '.join(map(str, xs)))} et {N(' ; '.join(str(x + shift) for x in xs))}"
    mixed = f"{N(' ; '.join(map(str, xs)))} et {N(' ; '.join(str(x * k + (1 if i == 1 else 0)) for i, x in enumerate(xs)))}"
    options = [good, additive, mixed]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a6", "reconnaitre", "Quel tableau est un tableau de proportionnalité ? (première ligne et deuxième ligne)", [options[i] for i in order], order.index(0), 2,
                            ["Calcule les rapports de la deuxième ligne à la première."],
                            [f"Le premier tableau de la bonne réponse a pour coefficient {k} : chaque nombre est multiplié par {k}.", "Dans les autres tableaux, les rapports ne sont pas tous égaux."],
                            wrong={order.index(1): "Ici on passe d'une ligne à l'autre en ajoutant le même nombre, pas en multipliant : ce n'est pas de la proportionnalité.",
                                   order.index(2): "Presque tous les nombres sont multipliés par le même coefficient, mais un seul ne l'est pas : le tableau n'est pas proportionnel."}))
    # 7. percentage of a quantity
    p = rng.choice([10, 20, 25, 30, 40, 50, 60, 75])
    quantity = rng.choice([40, 60, 80, 120, 200, 240, 360, 400, 500])
    if (p, quantity) in {(50, 360), (25, 120), (25, 80), (10, 4500), (12, 250)}:
        p = 30
    questions.append(number("a7", "pourcentage", f"Calcule {p} % de {quantity}.", Fraction(p * quantity, 100), 1, [f"{p} % = {show(Fraction(p, 100))}."],
                            [f"{p} % = {show(Fraction(p, 100))}.", f"{quantity} × {show(Fraction(p, 100))} = {show(Fraction(p * quantity, 100))}."]))
    # 8. discount
    price, p = rng.choice([1000, 1500, 2500, 3000, 4000, 6000, 8000]), rng.choice([10, 20, 25, 30, 40])
    questions.append(number("a8", "pourcentage", f"Un article coûte {price} F. Il est soldé avec {p} % de réduction. Combien paie-t-on, en F ?", Fraction(price * (100 - p), 100), 3, ["Calcule la réduction, puis retire-la."],
                            [f"Réduction : {p} % de {price} = {show(Fraction(price * p, 100))} F.", f"{price} − {show(Fraction(price * p, 100))} = {show(Fraction(price * (100 - p), 100))} F."], units=["F"]))
    # 9. fraction to percentage
    total = rng.choice([20, 25, 40, 50, 80])
    part = rng.randint(1, total - 1)
    questions.append(number("a9", "pourcentage", f"Dans un groupe de {total} élèves, {part} portent des lunettes. Quel pourcentage cela représente-t-il ? (en %)", Fraction(part * 100, total), 2,
                            ["Écris la fraction, puis ramène-la à 100."], [f"{part} ÷ {total} = {show(Fraction(part, total))}.", f"{show(Fraction(part, total))} = {show(Fraction(part * 100, total))} %."], units=["%"]))
    # 10. scale: map to ground
    scale, cm = rng.choice([10000, 25000, 50000, 100000]), rng.randint(2, 12)
    if (scale, cm) in {(50000, 6), (25000, 8), (10000, 3), (50000, 5)}:
        cm += 1
    real_km = Fraction(cm * scale, 100000)
    questions.append(number("a10", "echelle", f"Sur une carte à l'échelle 1/{scale}, deux villages sont séparés de {cm} cm. Quelle est la distance réelle, en km ?", real_km, 2,
                            ["Multiplie par l'échelle, puis convertis les centimètres en kilomètres."],
                            [f"{cm} × {scale} = {cm * scale} cm.", f"{cm * scale} cm = {show(Fraction(cm * scale, 100))} m = {show(real_km)} km."], units=["km"], form="decimal"))
    # 11. scale: ground to plan
    scale, meters = rng.choice([(100, 20), (200, 30), (500, 50), (1000, 120)])
    plan_cm = Fraction(meters * 100, scale)
    questions.append(number("a11", "echelle", f"Une longueur réelle de {meters} m est dessinée sur un plan à l'échelle 1/{scale}. Quelle longueur mesure-t-elle sur le plan, en cm ?", plan_cm, 3,
                            ["Convertis les mètres en centimètres, puis divise par l'échelle."], [f"{meters} m = {meters * 100} cm.", f"{meters * 100} ÷ {scale} = {show(plan_cm)} cm."], units=["cm"], form="decimal"))
    # 12. the classic mistake
    age1, size1, age2 = rng.choice([2, 4, 5]), rng.choice([80, 90, 100]), rng.choice([8, 10, 12])
    options = ["Il a raison, car la taille augmente avec l'âge",
               "Il a tort : la taille d'un enfant n'est pas proportionnelle à son âge",
               "Il a tort : il faut diviser au lieu de multiplier"]
    order = [0, 1, 2]
    rng.shuffle(order)
    questions.append(choice("a12", "reconnaitre", f"Karim mesure {size1} cm à {age1} ans. Il dit : « À {age2} ans, je mesurerai {show(Fraction(size1 * age2, age1))} cm, car la taille est proportionnelle à l'âge ». A-t-il raison ?",
                            [options[i] for i in order], order.index(1), 3, ["Réfléchis : la taille continue-t-elle à grandir de la même façon toute la vie ?"],
                            [f"Avec ce raisonnement, à 60 ans il mesurerait {show(Fraction(size1 * 60, age1))} cm, ce qui est impossible.", "L'âge et la taille ne sont pas des grandeurs proportionnelles."],
                            wrong={order.index(0): "Une grandeur qui augmente avec l'autre n'est pas forcément proportionnelle : ici la taille n'augmente pas de la même façon que l'âge.",
                                   order.index(2): "Le problème n'est pas l'opération : c'est que la situation n'est pas proportionnelle."}))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=5, title="La proportionnalité", language="fr",
    intro="Le prix de 3 kg de sucre, la distance parcourue à vitesse constante, la réduction annoncée dans un magasin, la distance sur une carte : toutes ces situations utilisent la proportionnalité. "
          "Ce chapitre t'apprend à la reconnaître, à calculer une valeur manquante, à calculer des pourcentages et à utiliser une échelle.",
    objectives=["Reconnaître un tableau de proportionnalité et trouver son coefficient.",
                "Compléter un tableau de proportionnalité par le coefficient, le passage à l'unité ou la linéarité.",
                "Calculer un pourcentage d'une quantité et exprimer une proportion en pourcentage.",
                "Utiliser une échelle pour passer d'une longueur sur un plan à une longueur réelle, et inversement.",
                "Justifier qu'une situation n'est pas une situation de proportionnalité."],
    prerequisites=[{"text": "Multiplier et diviser des nombres décimaux.", "course": "whole-numbers", "lesson": "multiply-divide"},
                   {"text": "Comprendre les décimaux et leurs conversions avec les fractions.", "course": "fractions-decimals", "lesson": "decimals"}],
    sections=[S1, S2, S3], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Fifth chapter of the Senegal Sixième course. Its topics follow the proportionality chapter of the ADEM-Dakar booklet, with our own explanations and exercises. "
                "The list of contents was checked against lesson 12 of the Côte d'Ivoire Sixième programme (proportional quantities, coefficient, tables, linearity, percentages, scale), "
                "so it is also offered there, but the programme's own situations and activities are not reproduced. It has not been checked against the official Senegalese programme.",
)
