"""Sixième, Angles: the twelfth chapter of the Senegal Sixième course, written in French.

The contents follow lesson 4 "Angles" of the Côte d'Ivoire Sixième programme (identify, name and measure an angle in degrees, the kinds of angle, the bisector), which was read for this chapter.
Every explanation, example, figure and exercise was written independently, with our own numbers. The figures are drawn from constants by figures.py. Measuring with a protractor and constructing
an angle with a protractor or a compass cannot be done on a screen: they are described, and said to be done on paper with a teacher.
Fixed answers are written as exact fractions and re-checked by tests against an independent recalculation, and each worked example carries a
"verify" expression that the tests evaluate. The step texts and solution lines are not machine-checked, they were reviewed by hand.
"""
from fractions import Fraction

from ..model import Chapter, Section
from ..sources import ADEM_SN_6E, CI_PROGRAMME_6E
from .figures import Figure, figure
from .kit import N, definition, example, make_kit, para, rule, warning

CHAPTER_ID = "sn-6e-angles"
number, choice, ordered, between = make_kit(CHAPTER_ID, default_form="decimal")

# ----- Figures -----
ACUTE = Figure().point("O", 60, 150, -14, 22).point("A", 280, 150, -4, 22).point("B", 220, 50, 10, -6).ray("O", "A").ray("O", "B").arc("O", "A", "B", 40)
RIGHT = Figure().point("O", 80, 150, -14, 22).point("A", 280, 150, -4, 22).point("B", 80, 30, 10, 4).ray("O", "A").ray("O", "B").right_angle("O", "A", "B", 16)
OBTUSE = Figure().point("O", 170, 150, -4, 22).point("A", 300, 150, -4, 22).point("B", 60, 60, -8, -10).ray("O", "A").ray("O", "B").arc("O", "A", "B", 34)
FLAT = Figure().point("A", 40, 120, -4, 24).point("O", 170, 120, -4, 24).point("B", 300, 120, -4, 24).line("A", "B")
ADJACENT = (Figure().point("O", 60, 150, -14, 22).point("A", 290, 150, -4, 22).point("B", 210, 50, 10, 4).point("C", 110, 40, -6, -10)
            .ray("O", "A").ray("O", "B").ray("O", "C").arc("O", "A", "B", 44).arc("O", "B", "C", 44))
BISECT = (Figure().point("O", 60, 160, -14, 22).point("A", 290, 160, -4, 22).point("B", 250, 35, 10, 0).point("M", 252, 103, 10, 4)
          .ray("O", "A").ray("O", "B").ray("O", "M", "fig-seg").arc("O", "A", "M", 36).arc("O", "M", "B", 48))
CLOCK = (Figure().point("C", 170, 105, 8, 20).point("12", 170, 25, -10, -8).point("4", 239, 145, 10, 14).circle("C", 80).segment("C", "12").segment("C", "4").arc("C", "12", "4", 30))

# ----- Section 1: what an angle is -----
S1 = Section(
    "angle", "Qu'est-ce qu'un angle ? Sommet, côtés et notation", 20, "angle",
    "Reconnaître un angle, nommer son sommet et ses côtés, le noter avec trois lettres et compter les angles formés par plusieurs demi-droites.",
    [
        para("Un gardien de but, un ballon et un poteau : pour savoir s'il peut arrêter un tir, on regarde l'ouverture entre deux directions. Cette ouverture s'appelle un angle. "
             "Une porte entrouverte, les deux branches d'un compas, les aiguilles d'une horloge forment aussi des angles."),
        definition("Angle, sommet et côtés",
                   "Un angle est formé de deux demi-droites de même origine. L'origine commune est le sommet de l'angle, et les deux demi-droites sont ses côtés. "
                   "L'angle formé par les demi-droites [OA) et [OB) se note " + N("\\widehat{AOB}") + " : on lit « angle AOB ». La lettre du milieu est toujours celle du sommet."),
        figure(ACUTE, "Un angle de sommet O dont les côtés sont les demi-droites [OA) et [OB).", "L'angle AOB a pour sommet O et pour côtés [OA) et [OB). L'arc orange marque l'ouverture entre les deux côtés."),
        rule("Un angle ne dépend pas de la longueur des côtés",
             "La mesure d'un angle ne change pas quand on dessine les côtés plus longs ou plus courts : elle ne dépend que de l'ouverture entre les deux demi-droites. "
             "Un angle se mesure en degrés, avec le symbole °."),
        example("Exemple 1", "Quel est le sommet de l'angle " + N("\\widehat{RST}") + " ? Quels sont ses côtés ?",
                "Dans la notation à trois lettres, la lettre du milieu est le sommet.",
                [("La lettre du milieu est S", "Le sommet de l'angle est le point S."),
                 ("Les deux autres lettres sont R et T", "Les côtés sont les demi-droites [SR) et [ST).")],
                "Sommet S, côtés [SR) et [ST).", "'RST'[1]=='S'"),
        example("Exemple 2", "Trois demi-droites [OA), [OB) et [OC) ont la même origine O. Combien d'angles forment-elles deux à deux ?",
                "Chaque angle est formé par deux demi-droites : on compte les paires.",
                [("Les paires de demi-droites : [OA)[OB), [OA)[OC), [OB)[OC)", "Il y a 3 paires."),
                 ("Chaque paire forme un angle : AOB, AOC, BOC", "Donc 3 angles.")],
                N("3") + " angles.", "3*2//2==3"),
        example("Exemple 3", "Quatre demi-droites ont la même origine. Combien d'angles forment-elles deux à deux ?",
                "Même méthode : on compte les paires de demi-droites.",
                [("Paires avec la première demi-droite : 3", "Elle forme un angle avec chacune des trois autres."),
                 ("Paires sans la première : 2 + 1 = 3", "Il reste trois demi-droites, donc 3 paires."),
                 (N("3 + 3") + " = " + N("6"), "On additionne.")],
                N("6") + " angles.", "4*3//2==6"),
        example("Exemple 4", "Deux élèves dessinent l'angle AOB, l'un avec des côtés de 5 cm, l'autre avec des côtés de 10 cm. L'ouverture est la même. Ont-ils le même angle ?",
                "On se rappelle que la longueur des côtés n'a pas d'importance : les demi-droites sont infinies.",
                [("Les côtés sont des demi-droites, qui ne s'arrêtent pas", "Dessiner 5 cm ou 10 cm n'en montre qu'un morceau."),
                 ("L'ouverture est la même", "Les deux angles ont la même mesure.")],
                "Oui, ils ont le même angle.", "5*2==10"),
        warning("Dans la notation " + N("\\widehat{AOB}") + ", la lettre du milieu est le sommet : l'angle " + N("\\widehat{AOB}") + " et l'angle " + N("\\widehat{OAB}") + " sont des angles différents. "
                "Et ne confonds pas l'angle avec l'arc dessiné : l'arc ne sert qu'à montrer quelle ouverture on mesure."),
    ],
    [
        choice("s1-g1", "angle", "Quel est le sommet de l'angle ∠XYZ ?", ["X", "Y", "Z"], 1,
               hints=["La lettre du milieu."], solution=["Dans ∠XYZ, la lettre du milieu est Y : c'est le sommet."], wrong={0: "X est l'extrémité d'un côté, pas le sommet.", 2: "Z est l'extrémité d'un côté, pas le sommet."}),
        number("s1-g2", "angle", "Cinq demi-droites ont la même origine. Combien d'angles forment-elles deux à deux ?", Fraction(10),
               hints=["Compte les paires : 4, puis 3, puis 2, puis 1."], solution=["4 + 3 + 2 + 1 = 10 paires de demi-droites.", "10 angles."]),
        choice("s1-g3", "angle", "Quels sont les côtés de l'angle ∠AOB ?", ["[OA) et [OB)", "[AO) et [AB)", "[BO) et [BA)"], 0,
               hints=["Les côtés partent du sommet O."], solution=["Le sommet est O : les côtés sont les demi-droites [OA) et [OB)."], wrong={1: "[AO) part de A, pas du sommet.", 2: "[BO) part de B, pas du sommet."}),
        choice("s1-g4", "angle", "Un élève dessine un angle avec des côtés de 3 cm, un autre avec des côtés de 12 cm, même ouverture. Que peut-on dire ?", ["Le second angle est plus grand", "Les deux angles ont la même mesure", "Le premier angle est plus grand"], 1,
               hints=["Les côtés sont des demi-droites qui ne s'arrêtent pas."], solution=["La mesure d'un angle ne dépend que de l'ouverture, pas de la longueur des côtés dessinés."], wrong={0: "12 cm est seulement un plus long morceau des côtés.", 2: "3 cm est seulement un plus court morceau des côtés."}),
        number("s1-g5", "angle", "Six demi-droites ont la même origine. Combien d'angles forment-elles deux à deux ?", Fraction(15),
               hints=["5 + 4 + 3 + 2 + 1."], solution=["5 + 4 + 3 + 2 + 1 = 15 paires de demi-droites.", "15 angles."]),
    ])

# ----- Section 2: measuring and the kinds of angle -----
S2 = Section(
    "mesure", "Mesurer un angle en degrés et reconnaître les types d'angles", 24, "mesure",
    "Connaître le degré, mesurer un angle avec un rapporteur, et classer un angle : nul, aigu, droit, obtus ou plat.",
    [
        para("Pour comparer des angles, il faut une unité. On partage un tour complet en 360 parties égales : chaque partie est un degré, noté 1°. Un demi-tour fait 180° et un quart de tour fait 90°."),
        rule("Les types d'angles",
             "Un angle nul mesure 0°. Un angle aigu mesure entre 0° et 90° (plus petit que l'angle droit). Un angle droit mesure 90°. Un angle obtus mesure entre 90° et 180°. Un angle plat mesure 180° : ses côtés sont dans le prolongement l'un de l'autre. "
             "Un tour complet mesure 360°."),
        figure(RIGHT, "Un angle droit de sommet O, marqué par un petit carré.", "Un angle droit mesure 90°. On le marque avec un petit carré."),
        figure(OBTUSE, "Un angle obtus de sommet O, plus ouvert qu'un angle droit.", "Cet angle est obtus : il est plus ouvert qu'un angle droit, mais moins qu'un angle plat."),
        figure(FLAT, "Trois points A, O et B alignés, avec O entre A et B : les demi-droites [OA) et [OB) forment un angle plat.", "Quand A, O et B sont alignés avec O entre A et B, l'angle AOB est plat : il mesure 180°."),
        rule("Mesurer avec un rapporteur",
             "On pose le centre du rapporteur sur le sommet, la graduation 0 sur l'un des côtés, et on lit la graduation que le second côté traverse. Un rapporteur a deux séries de nombres : on part de la série qui commence par 0 sur le côté choisi. "
             "Un angle aigu a une mesure inférieure à 90 : c'est un bon moyen de vérifier qu'on n'a pas lu la mauvaise série. Cette manipulation se fait sur le papier, avec un vrai rapporteur."),
        example("Exemple 1", "Classer les angles de 35°, de 90°, de 120°, de 180° et de 0°.",
                "On compare chaque mesure à 0°, 90° et 180°.",
                [("35° est entre 0° et 90°", "C'est un angle aigu."),
                 ("90° est exactement la mesure de l'angle droit", "C'est un angle droit."),
                 ("120° est entre 90° et 180°", "C'est un angle obtus."),
                 ("180° et 0°", "180° est un angle plat et 0° est un angle nul.")],
                "35° aigu ; 90° droit ; 120° obtus ; 180° plat ; 0° nul.", "0<35<90 and 90<120<180"),
        example("Exemple 2", "Combien de degrés fait un quart de tour ? un demi-tour ? trois quarts de tour ?",
                "Un tour complet fait 360° : on prend la fraction du tour.",
                [(N("360 \\div 4") + " = " + N("90"), "Un quart de tour est un angle droit."),
                 (N("360 \\div 2") + " = " + N("180"), "Un demi-tour est un angle plat."),
                 (N("3 \\times 90") + " = " + N("270"), "Trois quarts de tour font trois angles droits.")],
                "90°, 180° et 270°.", "360//4==90 and 360//2==180 and 3*90==270"),
        example("Exemple 3", "Un angle mesure 47°. Un autre mesure 133°. Les classer.",
                "On compare chaque mesure à 90°.",
                [("47° est plus petit que 90°", "C'est un angle aigu."),
                 ("133° est plus grand que 90° et plus petit que 180°", "C'est un angle obtus.")],
                "47° est aigu et 133° est obtus.", "47<90<133<180"),
        example("Exemple 4", "Le rapporteur donne deux lectures, 38 et 142, pour un angle dont un côté passe par la graduation 0 du rapporteur et l'autre côté semble très ouvert. Laquelle choisir ?",
                "On vérifie avec le type de l'angle : un angle très ouvert est obtus, donc plus grand que 90°.",
                [("Les deux lectures s'ajoutent à 180", N("38 + 142") + " = " + N("180") + " : ce sont les deux séries du rapporteur."),
                 ("L'angle est très ouvert : plus grand que 90°", "On choisit la lecture qui dépasse 90.")],
                N("142") + "°.", "38+142==180 and 142>90"),
        warning("Ne dis pas qu'un angle de 100° est plus grand qu'un angle de 80° « parce que ses côtés sont plus longs » : seule l'ouverture compte. Et un angle obtus n'est pas un angle plat : 180° est exactement le demi-tour."),
    ],
    [
        choice("s2-g1", "mesure", "Un angle mesure 65°. Quel est son type ?", ["Aigu", "Droit", "Obtus", "Plat"], 0,
               hints=["Compare 65 à 90."], solution=["65° est plus petit que 90° : l'angle est aigu."], wrong={1: "Un angle droit mesure exactement 90°.", 2: "Un angle obtus est plus grand que 90°.", 3: "Un angle plat mesure 180°."}),
        choice("s2-g2", "mesure", "Un angle mesure 125°. Quel est son type ?", ["Aigu", "Droit", "Obtus", "Plat"], 2,
               hints=["Compare 125 à 90 et à 180."], solution=["125° est entre 90° et 180° : l'angle est obtus."], wrong={0: "Un angle aigu est plus petit que 90°.", 1: "Un angle droit mesure exactement 90°.", 3: "Un angle plat mesure 180°."}),
        number("s2-g3", "mesure", "Combien de degrés mesure trois quarts de tour ?", Fraction(270), units=["°", "degrés", "degré"],
               hints=["Un quart de tour mesure 90°."], solution=["3 × 90 = 270°."]),
        number("s2-g4", "mesure", "Un tour complet mesure 360°. Combien de degrés mesure un huitième de tour ?", Fraction(45), units=["°", "degrés", "degré"],
               hints=["Divise 360 par 8."], solution=["360 ÷ 8 = 45°."]),
        choice("s2-g5", "mesure", "Les points A, O et B sont alignés, O est entre A et B. Que dire de l'angle ∠AOB ?", ["Il est droit", "Il est plat", "Il est nul"], 1,
               hints=["Les demi-droites [OA) et [OB) sont dans le prolongement l'une de l'autre."], solution=["Les côtés sont opposés : l'angle est plat et mesure 180°."], wrong={0: "Un angle droit demande un quart de tour.", 2: "Un angle nul a ses deux côtés confondus."}),
    ])

# ----- Section 3: calculating with angles -----
S3 = Section(
    "calculs", "Calculer avec des angles : somme, angle plat et angle droit", 24, "calculs",
    "Additionner des angles adjacents, utiliser l'angle plat et l'angle droit pour trouver un angle manquant, et résoudre un petit problème d'angles.",
    [
        para("Quand on ouvre une porte en deux temps, l'ouverture totale est la somme des deux ouvertures. Les angles s'additionnent comme des longueurs, à condition de se placer côte à côte, sans se chevaucher."),
        figure(ADJACENT, "Trois demi-droites [OA), [OB) et [OC) de même origine O, avec deux angles AOB et BOC côte à côte.", "Les angles AOB et BOC sont côte à côte : ils ont le côté [OB) en commun. L'angle AOC est la réunion des deux."),
        rule("Addition d'angles",
             "Si la demi-droite [OB) est entre [OA) et [OC), alors " + N("\\widehat{AOC} = \\widehat{AOB} + \\widehat{BOC}") + ". En particulier, deux angles qui forment ensemble un angle plat ont une somme de 180°, "
             "et deux angles qui forment ensemble un angle droit ont une somme de 90°."),
        example("Exemple 1", "[OB) est entre [OA) et [OC). On a " + N("\\widehat{AOB} = 35") + "° et " + N("\\widehat{BOC} = 50") + "°. Calculer " + N("\\widehat{AOC}") + ".",
                "Les deux angles sont côte à côte : on les additionne.",
                [(N("\\widehat{AOC} = \\widehat{AOB} + \\widehat{BOC}"), "Propriété de l'addition d'angles."),
                 (N("35 + 50") + " = " + N("85"), "On additionne les mesures.")],
                N("\\widehat{AOC} = 85") + "°.", "35+50==85"),
        example("Exemple 2", "[OB) est entre [OA) et [OC). On a " + N("\\widehat{AOC} = 120") + "° et " + N("\\widehat{AOB} = 45") + "°. Calculer " + N("\\widehat{BOC}") + ".",
                "On retire l'angle connu de l'angle total.",
                [(N("\\widehat{BOC} = \\widehat{AOC} - \\widehat{AOB}"), "On part de AOC = AOB + BOC."),
                 (N("120 - 45") + " = " + N("75"), "On soustrait.")],
                N("\\widehat{BOC} = 75") + "°.", "120-45==75"),
        example("Exemple 3", "Les points A, O et B sont alignés, avec O entre A et B. C est un point hors de la droite et " + N("\\widehat{AOC} = 110") + "°. Calculer " + N("\\widehat{COB}") + ".",
                "Les angles AOC et COB sont côte à côte et forment l'angle plat AOB, qui mesure 180°.",
                [(N("\\widehat{AOC} + \\widehat{COB} = 180"), "Les deux angles forment un angle plat."),
                 (N("\\widehat{COB} = 180 - 110") + " = " + N("70"), "On retire l'angle connu de 180.")],
                N("\\widehat{COB} = 70") + "°.", "180-110==70 and 110+70==180"),
        example("Exemple 4", "Deux angles côte à côte forment un angle droit. L'un mesure 28°. Quelle est la mesure de l'autre ?",
                "L'angle droit mesure 90° : on retire l'angle connu de 90.",
                [(N("90 - 28") + " = " + N("62"), "L'autre angle mesure 62°."),
                 ("Vérification : " + N("28 + 62") + " = " + N("90"), "On retrouve bien l'angle droit.")],
                N("62") + "°.", "90-28==62 and 28+62==90"),
        warning("Les angles ne s'additionnent que s'ils sont côte à côte, sans se chevaucher : si les deux angles se recouvrent, la somme est trop grande. "
                "Et n'oublie pas la différence entre 90° (angle droit, quart de tour) et 180° (angle plat, demi-tour) quand tu cherches un angle manquant."),
    ],
    [
        number("s3-g1", "calculs", "[OB) est entre [OA) et [OC). ∠AOB = 40° et ∠BOC = 55°. Quelle est la mesure de ∠AOC, en degrés ?", Fraction(95), units=["°", "degrés", "degré"],
               hints=["Additionne les deux angles."], solution=["∠AOC = ∠AOB + ∠BOC = 40° + 55° = 95°."]),
        number("s3-g2", "calculs", "[OB) est entre [OA) et [OC). ∠AOC = 130° et ∠BOC = 60°. Quelle est la mesure de ∠AOB, en degrés ?", Fraction(70), units=["°", "degrés", "degré"],
               hints=["Retire l'angle connu de l'angle total."], solution=["∠AOB = ∠AOC − ∠BOC = 130° − 60° = 70°."]),
        number("s3-g3", "calculs", "Deux angles côte à côte forment un angle plat. L'un mesure 115°. Quelle est la mesure de l'autre, en degrés ?", Fraction(65), units=["°", "degrés", "degré"],
               hints=["Un angle plat mesure 180°."], solution=["180° − 115° = 65°."]),
        number("s3-g4", "calculs", "Deux angles côte à côte forment un angle droit. L'un mesure 37°. Quelle est la mesure de l'autre, en degrés ?", Fraction(53), units=["°", "degrés", "degré"],
               hints=["Un angle droit mesure 90°."], solution=["90° − 37° = 53°."]),
        choice("s3-g5", "calculs", "Léa dit : « deux angles de 100° et de 90° côte à côte font un angle de 190°, donc un angle plat ». Quelle est son erreur ?",
               ["190° dépasse 180° : les deux angles ne peuvent pas être côte à côte dans un angle plat", "Elle a oublié l'unité", "Elle a additionné au lieu de soustraire"], 0,
               hints=["Un angle plat mesure 180°."], solution=["Deux angles côte à côte dans un angle plat ont une somme de 180° exactement : 190° est trop grand."],
               wrong={1: "L'unité est présente : ce sont des degrés.", 2: "Pour des angles côte à côte, on additionne : l'erreur est ailleurs."}),
    ])

# ----- Section 4: the bisector and problems -----
S4 = Section(
    "bissectrice", "Bissectrice d'un angle et problèmes d'angles", 24, "bissectrice",
    "Connaître la bissectrice d'un angle, calculer avec elle, et résoudre des problèmes avec une horloge et des tours.",
    [
        para("Un angle peut être partagé en deux angles égaux par une demi-droite : c'est la bissectrice. C'est l'idée du pliage : on plie le papier en faisant coïncider les deux côtés, et le pli est la bissectrice."),
        definition("Bissectrice d'un angle",
                   "La bissectrice d'un angle est la demi-droite, de même origine que l'angle, qui le partage en deux angles de même mesure. Si [OM) est la bissectrice de " + N("\\widehat{AOB}") + ", alors "
                   + N("\\widehat{AOM} = \\widehat{MOB} = \\widehat{AOB} \\div 2") + "."),
        figure(BISECT, "Un angle AOB partagé par la demi-droite [OM) en deux angles égaux, marqués par deux arcs.", "[OM) est la bissectrice de l'angle AOB : les angles AOM et MOB sont égaux."),
        definition("L'horloge et les angles",
                   "Le cadran d'une horloge est un tour complet de 360° partagé en 12 heures. Entre deux nombres voisins du cadran, il y a donc " + N("360 \\div 12") + " = " + N("30") + "°. "
                   "À une heure pile, l'angle entre les deux aiguilles est le nombre d'heures depuis 12, multiplié par 30°, ou son complément à 360° si on veut le plus petit angle."),
        figure(CLOCK, "Un cadran d'horloge avec deux aiguilles, l'une vers le 12 et l'autre vers le 4, et un arc entre elles.", "À 4 heures pile, les aiguilles forment un angle de 4 × 30° = 120°."),
        example("Exemple 1", "[OM) est la bissectrice de l'angle " + N("\\widehat{AOB}") + " qui mesure 70°. Calculer " + N("\\widehat{AOM}") + ".",
                "La bissectrice partage l'angle en deux angles égaux : on prend la moitié.",
                [(N("\\widehat{AOM} = \\widehat{AOB} \\div 2"), "Définition de la bissectrice."),
                 (N("70 \\div 2") + " = " + N("35"), "La moitié de 70 est 35.")],
                N("\\widehat{AOM} = 35") + "°.", "70//2==35"),
        example("Exemple 2", "[OM) est la bissectrice de l'angle " + N("\\widehat{AOB}") + ". On a " + N("\\widehat{AOM} = 28") + "°. Calculer " + N("\\widehat{AOB}") + ".",
                "Les deux angles égaux font ensemble l'angle total : on prend le double.",
                [(N("\\widehat{AOB} = 2 \\times \\widehat{AOM}"), "Les deux moitiés sont égales."),
                 (N("2 \\times 28") + " = " + N("56"), "Le double de 28 est 56.")],
                N("\\widehat{AOB} = 56") + "°.", "2*28==56"),
        example("Exemple 3", "Quel est l'angle entre les aiguilles d'une horloge à 4 heures ? à 2 heures ? à 7 heures (le plus petit des deux angles) ?",
                "On compte les nombres du cadran entre les aiguilles et on multiplie par 30°.",
                [("4 heures : 4 nombres entre le 12 et le 4", N("4 \\times 30") + " = " + N("120") + "°."),
                 ("2 heures : 2 nombres entre le 12 et le 2", N("2 \\times 30") + " = " + N("60") + "°."),
                 ("7 heures : 7 nombres dans un sens, donc 210°, mais le plus petit angle est dans l'autre sens : " + N("360 - 210") + " = " + N("150"), "On prend toujours le plus petit angle entre les deux aiguilles.")],
                "120°, 60° et 150°.", "4*30==120 and 2*30==60 and 360-7*30==150"),
        example("Exemple 4", "Une roue de vélo tourne de 3 quarts de tour. Un tourniquet fait un tour et demi. De combien de degrés chacun a-t-il tourné ?",
                "Un tour complet fait 360° : on prend la fraction.",
                [(N("3 \\times 90") + " = " + N("270"), "La roue a tourné de 270°."),
                 (N("360 + 180") + " = " + N("540"), "Un tour et demi, c'est 360° plus 180°.")],
                "270° pour la roue et 540° pour le tourniquet.", "3*90==270 and 360+180==540"),
        warning("Une bissectrice est une demi-droite qui partage un angle en deux angles égaux, pas en deux angles quelconques. Et pour l'horloge, ne prends pas l'angle le plus long : on demande presque toujours le plus petit des deux angles entre les aiguilles."),
    ],
    [
        number("s4-g1", "bissectrice", "[OM) est la bissectrice de ∠AOB = 84°. Quelle est la mesure de ∠AOM, en degrés ?", Fraction(42), units=["°", "degrés", "degré"],
               hints=["La bissectrice partage l'angle en deux moitiés."], solution=["84 ÷ 2 = 42°."]),
        number("s4-g2", "bissectrice", "[OM) est la bissectrice de ∠AOB. ∠AOM = 33°. Quelle est la mesure de ∠AOB, en degrés ?", Fraction(66), units=["°", "degrés", "degré"],
               hints=["Prends le double."], solution=["2 × 33 = 66°."]),
        number("s4-g3", "bissectrice", "Il est 5 heures pile. Quel est le plus petit angle entre les deux aiguilles, en degrés ?", Fraction(150), units=["°", "degrés", "degré"],
               hints=["Une heure du cadran mesure 30°."], solution=["Entre 12 et 5 : 5 × 30 = 150°. C'est moins que 180° : c'est le plus petit angle."]),
        number("s4-g4", "bissectrice", "Il est 8 heures pile. Quel est le plus petit angle entre les deux aiguilles, en degrés ?", Fraction(120), units=["°", "degrés", "degré"],
               hints=["8 × 30 = 240° dans un sens : prends l'autre sens."], solution=["8 × 30 = 240°, qui dépasse 180°.", "L'autre angle est 360 − 240 = 120°."]),
        number("s4-g5", "bissectrice", "Une porte tourne de 135°. Combien de degrés a-t-elle encore à tourner pour être ouverte à 180° ?", Fraction(45), units=["°", "degrés", "degré"],
               hints=["Retire 135 de 180."], solution=["180 − 135 = 45°."]),
    ])

# ----- Independent practice -----
PRACTICE = [
    choice("p1", "angle", "Quel est le sommet de l'angle ∠EFG ?", ["E", "F", "G"], 1, 1, ["La lettre du milieu."], ["Dans ∠EFG, le sommet est F."], wrong={0: "E est l'extrémité d'un côté.", 2: "G est l'extrémité d'un côté."}),
    number("p2", "angle", "Sept demi-droites ont la même origine. Combien d'angles forment-elles deux à deux ?", Fraction(21), 3, ["6 + 5 + 4 + 3 + 2 + 1."], ["6 + 5 + 4 + 3 + 2 + 1 = 21 paires de demi-droites.", "21 angles."]),
    number("p3", "angle", "Deux demi-droites de même origine forment combien d'angles ?", Fraction(1), 1, ["Une seule paire."], ["Deux demi-droites forment 1 paire, donc 1 angle."]),
    choice("p4", "angle", "L'angle ∠ABC et l'angle ∠CBA sont :", ["les mêmes angles", "deux angles différents", "des angles opposés"], 0, 2, ["Dans les deux notations, la lettre du milieu est la même."], ["∠ABC et ∠CBA ont le même sommet B et les mêmes côtés : c'est le même angle."], wrong={1: "Le sommet et les côtés sont les mêmes.", 2: "Il n'y a pas d'angles opposés ici."}),
    choice("p5", "mesure", "Un angle mesure 90°. Quel est son type ?", ["Aigu", "Droit", "Obtus", "Plat"], 1, 1, ["C'est le quart de tour."], ["90° est l'angle droit."], wrong={0: "Un angle aigu est plus petit que 90°.", 2: "Un angle obtus est plus grand que 90°.", 3: "Un angle plat mesure 180°."}),
    choice("p6", "mesure", "Un angle mesure 18°. Quel est son type ?", ["Aigu", "Droit", "Obtus", "Plat"], 0, 1, ["Compare 18 à 90."], ["18° est plus petit que 90° : aigu."], wrong={1: "Droit : 90° exactement.", 2: "Obtus : plus de 90°.", 3: "Plat : 180°."}),
    choice("p7", "mesure", "Un angle mesure 172°. Quel est son type ?", ["Aigu", "Droit", "Obtus", "Plat"], 2, 1, ["Compare 172 à 90 et à 180."], ["172° est entre 90° et 180° : obtus."], wrong={0: "Aigu : moins de 90°.", 1: "Droit : 90° exactement.", 3: "Plat : exactement 180°."}),
    choice("p8", "mesure", "Quel angle est obtus ?", ["89°", "90°", "91°", "180°"], 2, 2, ["Un angle obtus est entre 90° et 180°."], ["Seul 91° est entre 90° et 180° : il est obtus."], wrong={0: "89° est aigu.", 1: "90° est droit.", 3: "180° est plat."}),
    number("p9", "mesure", "Combien de degrés mesure un demi-tour ?", Fraction(180), 1, ["Un tour fait 360°."], ["360 ÷ 2 = 180°."], units=["°", "degrés", "degré"]),
    number("p10", "mesure", "Combien de degrés mesurent cinq quarts de tour ?", Fraction(450), 2, ["Un quart de tour fait 90°."], ["5 × 90 = 450°."], units=["°", "degrés", "degré"]),
    number("p11", "mesure", "Un tour complet fait 360°. Combien de degrés mesure un sixième de tour ?", Fraction(60), 2, ["Divise 360 par 6."], ["360 ÷ 6 = 60°."], units=["°", "degrés", "degré"]),
    number("p12", "mesure", "Une roue fait 2 tours et demi. De combien de degrés a-t-elle tourné ?", Fraction(900), 3, ["Un tour fait 360° ; un demi-tour 180°."], ["2 × 360 = 720°.", "720 + 180 = 900°."], units=["°", "degrés", "degré"]),
    number("p13", "calculs", "[OB) est entre [OA) et [OC). ∠AOB = 25° et ∠BOC = 70°. Quelle est la mesure de ∠AOC, en degrés ?", Fraction(95), 1, ["Additionne."], ["25 + 70 = 95°."], units=["°", "degrés", "degré"]),
    number("p14", "calculs", "[OB) est entre [OA) et [OC). ∠AOC = 150° et ∠AOB = 62°. Quelle est la mesure de ∠BOC, en degrés ?", Fraction(88), 2, ["Retire AOB de AOC."], ["150 − 62 = 88°."], units=["°", "degrés", "degré"]),
    number("p15", "calculs", "Deux angles côte à côte forment un angle plat. L'un mesure 73°. Quelle est la mesure de l'autre, en degrés ?", Fraction(107), 1, ["180 moins l'angle connu."], ["180 − 73 = 107°."], units=["°", "degrés", "degré"]),
    number("p16", "calculs", "Deux angles côte à côte forment un angle droit. L'un mesure 41°. Quelle est la mesure de l'autre, en degrés ?", Fraction(49), 1, ["90 moins l'angle connu."], ["90 − 41 = 49°."], units=["°", "degrés", "degré"]),
    number("p17", "calculs", "Trois angles côte à côte forment un angle plat. Deux mesurent 50° et 75°. Quelle est la mesure du troisième, en degrés ?", Fraction(55), 2, ["Additionne les deux angles connus, puis retire de 180."], ["50 + 75 = 125°.", "180 − 125 = 55°."], units=["°", "degrés", "degré"]),
    number("p18", "calculs", "Deux angles complémentaires (ils font ensemble 90°) sont tels que l'un est le double de l'autre. Quelle est la mesure du plus petit, en degrés ?", Fraction(30), 3, ["Le plus petit est 1 part, l'autre 2 parts : 3 parts font 90°."], ["1 + 2 = 3 parts. 90 ÷ 3 = 30°."], units=["°", "degrés", "degré"]),
    number("p19", "calculs", "Deux angles côte à côte forment un angle plat. L'un est le triple de l'autre. Quelle est la mesure du plus petit, en degrés ?", Fraction(45), 3, ["1 part et 3 parts : 4 parts font 180°."], ["1 + 3 = 4 parts. 180 ÷ 4 = 45°."], units=["°", "degrés", "degré"]),
    number("p20", "calculs", "Les points A, O et B sont alignés, O entre A et B. C est hors de la droite et ∠AOC = 2 × ∠COB. Quelle est la mesure de ∠COB, en degrés ?", Fraction(60), 3, ["∠AOC + ∠COB = 180°."], ["2 parts + 1 part = 3 parts font 180°.", "180 ÷ 3 = 60°."], units=["°", "degrés", "degré"]),
    choice("p21", "calculs", "Deux angles de 80° et de 110° côte à côte peuvent-ils former un angle plat ?", ["Oui, 80 + 110 = 180", "Non, 80 + 110 = 190 dépasse 180", "Oui, parce qu'un angle plat mesure 190°"], 1, 2, ["Additionne les deux mesures."], ["80 + 110 = 190, qui est plus grand que 180 : ils ne peuvent pas former un angle plat."], wrong={0: "80 + 110 = 190, pas 180.", 2: "Un angle plat mesure 180°."}),
    number("p22", "bissectrice", "[OM) est la bissectrice de ∠AOB = 110°. Quelle est la mesure de ∠AOM, en degrés ?", Fraction(55), 1, ["La moitié."], ["110 ÷ 2 = 55°."], units=["°", "degrés", "degré"]),
    number("p23", "bissectrice", "[OM) est la bissectrice de ∠AOB. ∠MOB = 47°. Quelle est la mesure de ∠AOB, en degrés ?", Fraction(94), 1, ["Le double."], ["2 × 47 = 94°."], units=["°", "degrés", "degré"]),
    number("p24", "bissectrice", "La bissectrice d'un angle droit partage cet angle en deux angles égaux. Quelle est la mesure de chacun, en degrés ?", Fraction(45), 2, ["L'angle droit mesure 90°."], ["90 ÷ 2 = 45°."], units=["°", "degrés", "degré"]),
    number("p25", "bissectrice", "La bissectrice d'un angle plat partage cet angle en deux angles égaux. Quelle est la mesure de chacun, en degrés ?", Fraction(90), 2, ["L'angle plat mesure 180°."], ["180 ÷ 2 = 90° : ce sont deux angles droits."], units=["°", "degrés", "degré"]),
    number("p26", "bissectrice", "Il est 3 heures pile. Quel est le plus petit angle entre les deux aiguilles, en degrés ?", Fraction(90), 1, ["3 × 30."], ["3 × 30 = 90°."], units=["°", "degrés", "degré"]),
    number("p27", "bissectrice", "Il est 10 heures pile. Quel est le plus petit angle entre les deux aiguilles, en degrés ?", Fraction(60), 2, ["10 × 30 = 300° dans un sens : prends l'autre sens."], ["10 × 30 = 300°, qui dépasse 180°.", "360 − 300 = 60°."], units=["°", "degrés", "degré"]),
    number("p28", "bissectrice", "Il est 6 heures pile. Quel est l'angle entre les deux aiguilles, en degrés ?", Fraction(180), 1, ["Les aiguilles sont opposées."], ["6 × 30 = 180° : les deux aiguilles forment un angle plat."], units=["°", "degrés", "degré"]),
    number("p29", "bissectrice", "Entre deux nombres voisins du cadran d'une horloge, quel est l'angle, en degrés ?", Fraction(30), 1, ["Un tour de 360° partagé en 12."], ["360 ÷ 12 = 30°."], units=["°", "degrés", "degré"]),
    number("p30", "bissectrice", "Une porte s'ouvre de 35°, puis de 50° de plus. Quelle est son ouverture totale, en degrés ?", Fraction(85), 2, ["Additionne les deux ouvertures."], ["35 + 50 = 85°."], units=["°", "degrés", "degré"]),
    number("p31", "bissectrice", "Un volet doit s'ouvrir à 120°. Il est ouvert à 75°. De combien de degrés faut-il encore l'ouvrir ?", Fraction(45), 2, ["Retire 75 de 120."], ["120 − 75 = 45°."], units=["°", "degrés", "degré"]),
    choice("p32", "bissectrice", "[OM) est la bissectrice de ∠AOB. Laquelle de ces égalités est vraie ?", [N("\\widehat{AOM} = \\widehat{MOB}"), N("\\widehat{AOM} = \\widehat{AOB}"), N("\\widehat{AOM} = 2 \\times \\widehat{AOB}")], 0, 1, ["La bissectrice partage l'angle en deux angles égaux."], ["∠AOM et ∠MOB sont égaux, et chacun est la moitié de ∠AOB."], wrong={1: "∠AOM est seulement la moitié de ∠AOB.", 2: "∠AOM est la moitié de ∠AOB, pas son double."}),
    choice("p33", "bissectrice", "Une horloge indique 12 heures pile. Quel est l'angle entre les deux aiguilles ?", ["0°", "90°", "180°"], 0, 1, ["Les deux aiguilles pointent vers le 12."], ["Les aiguilles sont confondues : l'angle est nul, 0°."], wrong={1: "À 3 heures, l'angle serait de 90°.", 2: "À 6 heures, l'angle serait de 180°."}),
]

SUMMARY = [
    definition("L'angle", "Un angle est formé de deux demi-droites de même origine, le sommet. ∠AOB se note avec la lettre du sommet au milieu. La mesure d'un angle ne dépend que de l'ouverture, pas de la longueur des côtés dessinés. Elle se mesure en degrés (°)."),
    rule("Les types d'angles", "Nul : 0°. Aigu : entre 0° et 90°. Droit : 90°. Obtus : entre 90° et 180°. Plat : 180°. Un tour complet : 360°, un demi-tour : 180°, un quart de tour : 90°."),
    rule("Calculer avec des angles", "Si [OB) est entre [OA) et [OC), ∠AOC = ∠AOB + ∠BOC. Deux angles côte à côte qui forment un angle plat font 180° ; qui forment un angle droit, 90°."),
    rule("Bissectrice et horloge", "La bissectrice de ∠AOB est la demi-droite [OM) telle que ∠AOM = ∠MOB = ∠AOB ÷ 2. Sur le cadran d'une horloge, deux nombres voisins font 30° : à h heures pile, l'angle entre les aiguilles est h × 30°, ou 360° moins cet angle s'il dépasse 180°."),
    para("Les erreurs à éviter : confondre le sommet avec une extrémité ; croire qu'un angle est plus grand parce que ses côtés sont plus longs ; additionner des angles qui se chevauchent ; confondre 90° et 180°."),
]

CONCEPTS = {
    "angle": ("Angle, sommet, côtés, notation", "angle"),
    "mesure": ("Mesure et types d'angles", "mesure"),
    "calculs": ("Calculer avec des angles", "calculs"),
    "bissectrice": ("Bissectrice, horloge et tours", "bissectrice"),
}


def assessment(rng):
    """Build twelve fresh questions covering every concept, from a seeded random generator."""
    questions = []
    deg = ["°", "degrés", "degré"]
    types = [("Aigu", 0), ("Droit", 1), ("Obtus", 2), ("Plat", 3)]
    # 1. the type of an angle from its measure
    measure = rng.choice([12, 25, 38, 47, 59, 73, 84, 90, 96, 108, 117, 124, 135, 149, 163, 171, 180])
    right = 1 if measure == 90 else 3 if measure == 180 else 0 if measure < 90 else 2
    questions.append(choice("a1", "mesure", f"Un angle mesure {measure}°. Quel est son type ?", [t for t, _ in types], right, 1,
                            ["Compare la mesure à 90 et à 180."], [f"{measure}° : " + ["aigu (moins de 90°).", "droit (90°).", "obtus (entre 90° et 180°).", "plat (180°)."][right]],
                            wrong={i: "Compare la mesure à 90° et à 180°." for i in range(4) if i != right}))
    # 2. the sum of two adjacent angles
    x, y = rng.randint(15, 80), rng.randint(15, 85)
    questions.append(number("a2", "calculs", f"[OB) est entre [OA) et [OC). ∠AOB = {x}° et ∠BOC = {y}°. Quelle est la mesure de ∠AOC, en degrés ?", Fraction(x + y), 1,
                            ["Additionne les deux angles."], [f"{x} + {y} = {x + y}°."], units=deg))
    # 3. the missing angle in a flat angle
    x = rng.randint(21, 159)
    questions.append(number("a3", "calculs", f"Deux angles côte à côte forment un angle plat. L'un mesure {x}°. Quelle est la mesure de l'autre, en degrés ?", Fraction(180 - x), 1,
                            ["Un angle plat mesure 180°."], [f"180 − {x} = {180 - x}°."], units=deg))
    # 4. the missing angle in a right angle
    x = rng.randint(11, 79)
    questions.append(number("a4", "calculs", f"Deux angles côte à côte forment un angle droit. L'un mesure {x}°. Quelle est la mesure de l'autre, en degrés ?", Fraction(90 - x), 1,
                            ["Un angle droit mesure 90°."], [f"90 − {x} = {90 - x}°."], units=deg))
    # 5. half of an angle
    x = 2 * rng.randint(15, 85)
    questions.append(number("a5", "bissectrice", f"[OM) est la bissectrice de ∠AOB = {x}°. Quelle est la mesure de ∠AOM, en degrés ?", Fraction(x // 2), 2,
                            ["La bissectrice partage l'angle en deux moitiés."], [f"{x} ÷ 2 = {x // 2}°."], units=deg))
    # 6. a clock
    hour = rng.randint(1, 11)
    smallest = min(30 * hour, 360 - 30 * hour)
    questions.append(number("a6", "bissectrice", f"Il est {hour} heures pile. Quel est le plus petit angle entre les deux aiguilles, en degrés ?", Fraction(smallest), 2,
                            ["Une heure du cadran mesure 30°."], [f"{hour} × 30 = {30 * hour}°." + ("" if 30 * hour <= 180 else f" Le plus petit angle est 360 − {30 * hour} = {smallest}°.")], units=deg))
    # 7. angles formed by half-lines
    n = rng.randint(3, 9)
    questions.append(number("a7", "angle", f"{n} demi-droites ont la même origine. Combien d'angles forment-elles deux à deux ?", Fraction(n * (n - 1) // 2), 2,
                            ["Compte les paires de demi-droites."], [f"{n} × {n - 1} ÷ 2 = {n * (n - 1) // 2}."]))
    # 8. quarter turns
    n = rng.randint(3, 11)
    questions.append(number("a8", "mesure", f"Une roue fait {n} quarts de tour. De combien de degrés a-t-elle tourné ?", Fraction(90 * n), 1,
                            ["Un quart de tour fait 90°."], [f"{n} × 90 = {90 * n}°."], units=deg))
    # 9. a missing adjacent angle
    total, part = rng.randint(100, 170), rng.randint(20, 90)
    questions.append(number("a9", "calculs", f"[OB) est entre [OA) et [OC). ∠AOC = {total}° et ∠AOB = {part}°. Quelle est la mesure de ∠BOC, en degrés ?", Fraction(total - part), 2,
                            ["Retire l'angle connu de l'angle total."], [f"{total} − {part} = {total - part}°."], units=deg))
    # 10. which of four angles is obtuse
    values = rng.sample([10, 25, 40, 55, 70, 85], 3) + [rng.choice([97, 110, 126, 143, 158, 170])]
    rng.shuffle(values)
    questions.append(choice("a10", "mesure", "Quel angle est obtus ?", [f"{v}°" for v in values], next(i for i, v in enumerate(values) if v > 90), 2,
                            ["Un angle obtus est entre 90° et 180°."], ["Un seul angle dépasse 90° : c'est l'angle obtus."]))
    # 11. double of an angle
    x = rng.randint(12, 88)
    questions.append(number("a11", "bissectrice", f"[OM) est la bissectrice de ∠AOB. ∠AOM = {x}°. Quelle est la mesure de ∠AOB, en degrés ?", Fraction(2 * x), 2,
                            ["Prends le double."], [f"2 × {x} = {2 * x}°."], units=deg))
    # 12. complementary angles in a ratio
    k = rng.choice([2, 4, 5, 8, 9])
    questions.append(number("a12", "calculs", f"Deux angles côte à côte forment un angle droit, et l'un est {k} fois l'autre. Quelle est la mesure du plus petit, en degrés ?", Fraction(90, k + 1), 3,
                            [f"Le plus petit est 1 part, l'autre {k} parts."], [f"1 + {k} = {k + 1} parts. 90 ÷ {k + 1} = {90 // (k + 1)}°."], units=deg))
    return questions


CHAPTER = Chapter(
    id=CHAPTER_ID, country="sn", level="6e", number=12, title="Les angles", language="fr",
    intro="Une porte entrouverte, les branches d'un compas, les aiguilles d'une horloge : toutes ces situations forment des angles. "
          "Ce chapitre t'apprend à nommer un angle, à le mesurer en degrés, à reconnaître ses types, à calculer avec des angles et à utiliser la bissectrice.",
    objectives=["Reconnaître un angle, nommer son sommet et ses côtés et le noter avec trois lettres.",
                "Connaître le degré et les types d'angles : nul, aigu, droit, obtus et plat.",
                "Additionner des angles côte à côte et trouver un angle manquant avec un angle plat ou un angle droit.",
                "Connaître la bissectrice d'un angle et calculer avec elle.",
                "Résoudre des problèmes avec une horloge, des quarts de tour et des tours complets."],
    prerequisites=[{"text": "Connaître les demi-droites et les points alignés.", "chapter": "sn-6e-droites-cercles"},
                   {"text": "Additionner et soustraire des nombres entiers et décimaux.", "chapter": "sn-6e-division"}],
    sections=[S1, S2, S3, S4], practice=PRACTICE, summary=SUMMARY, concepts=CONCEPTS, assessment=assessment,
    sources=[ADEM_SN_6E, CI_PROGRAMME_6E], also_for=("ci",),
    status_note="Twelfth chapter of the Senegal Sixième course. Its contents follow lesson 4 of the Côte d'Ivoire Sixième programme (angles, their measure in degrees, the kinds of angle and the bisector), which was read for it, "
                "so it is also offered there, but the programme's own situations are not reproduced. The figures are drawn by the app. Measuring with a protractor and constructing an angle with a protractor or a compass cannot be done on a screen, "
                "so the chapter describes them and they are not covered. It has not been checked against the official Senegalese programme.",
)
