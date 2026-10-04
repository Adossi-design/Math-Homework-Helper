"""Middle school skills: integers, percents, ratios, geometry, data and chance."""
from fractions import Fraction
from math import comb, gcd
from statistics import median

from .core import L, Question, frac, m, mf, paren, pick, skill

ITEMS = [("notebooks", "cahiers"), ("pens", "stylos"), ("apples", "pommes"), ("tickets", "billets"), ("cupcakes", "gâteaux")]
STAT_NAMES = {"mean": "la moyenne", "median": "la médiane", "mode": "le mode", "range": "l'étendue"}
COLORS = {"red": ("rouge", "rouges"), "blue": ("bleue", "bleues"), "green": ("verte", "vertes")}
DIE_EVENTS = [
    ("an even number", "un nombre pair", [2, 4, 6]),
    ("a number greater than 4", "un nombre supérieur à 4", [5, 6]),
    ("a prime number", "un nombre premier", [2, 3, 5]),
    ("a multiple of 3", "un multiple de 3", [3, 6]),
    ("a number less than 3", "un nombre inférieur à 3", [1, 2]),
    ("a 6", "un 6", [6]),
]


def simplified(num, den, value):
    """Add a simplifies to note when a fraction reduces."""
    if value.denominator == den and value.numerator == num:
        return ""
    return L(f", which simplifies to ${frac(value)}$", f", qui se simplifie en ${frac(value)}$")


def series(values):
    """Write a list of numbers the way each language separates them."""
    return L(", ", ";\\ ").join(map(str, values))


def percent(value):
    """Write a number with a percent sign."""
    return L(f"{value}\\%", f"{value}\\,\\%")


@skill("integers", "Negative numbers", "Middle School", "Arithmetic",
       "Add, subtract, multiply and divide with negative numbers.")
def integers(rng):
    while True:
        a, b = rng.randint(-15, 15), rng.randint(-12, 12)
        if a and b and (a < 0 or b < 0):
            break
    op = rng.choice("+-*/")
    same_sign = L("Same signs give a positive result and different signs give a negative result.",
                  "Deux signes identiques donnent un résultat positif, deux signes différents un résultat négatif.")
    if op == "+":
        expr, c = f"{a} + {paren(b)}", a + b
        if (a > 0) == (b > 0):
            rule = L("The signs match, so add the sizes and keep the sign.",
                     "Les signes sont identiques : additionne les valeurs et garde le signe.")
        else:
            rule = L("The signs differ, so subtract the smaller size from the larger and keep the sign of the larger one.",
                     "Les signes sont différents : soustrais la plus petite valeur de la plus grande et garde le signe de la plus grande.")
        wrong = [-c, a - b, abs(a) + abs(b)]
    elif op == "-":
        expr, c = f"{a} - {paren(b)}", a - b
        rule = L(f"Subtracting a number means adding its opposite: ${a} - {paren(b)} = {a} + {paren(-b)}$.",
                 f"Soustraire un nombre revient à ajouter son opposé : ${a} - {paren(b)} = {a} + {paren(-b)}$.")
        wrong = [a + b, -c, -(abs(a) + abs(b))]
    elif op == "*":
        expr, c = f"{a} \\times {paren(b)}", a * b
        rule, wrong = same_sign, [-c, a + b, c + a]
    else:
        expr, c = f"{a * b} \\div {paren(b)}", a
        rule, wrong = same_sign, [-c, c + 1, b]
    prompt = L(f"What is ${expr}$?", f"Combien font ${expr}$ ?")
    return Question(prompt, *pick(rng, c, wrong, m), L(f"{rule} So ${expr} = {c}$.", f"{rule} Donc ${expr} = {c}$."))


@skill("order-of-operations", "Order of operations", "Middle School", "Arithmetic",
       "Brackets, then powers, then multiply and divide, then add and subtract.")
def order_of_operations(rng):
    a, b, c, d = (rng.randint(2, 9) for _ in range(4))
    kind = rng.randrange(4)
    if kind == 0:
        expr, value = f"{a} + {b} \\times {c}", a + b * c
        steps = L(f"Multiply first: ${b} \\times {c} = {b * c}$. Then add: ${a} + {b * c} = {value}$.",
                  f"D'abord la multiplication : ${b} \\times {c} = {b * c}$. Puis l'addition : ${a} + {b * c} = {value}$.")
        wrong = [(a + b) * c, a + b + c, a * b + c]
    elif kind == 1:
        expr, value = f"({a} + {b}) \\times {c} - {d}", (a + b) * c - d
        steps = L(
            f"Brackets first: ${a} + {b} = {a + b}$. Multiply: ${a + b} \\times {c} = {(a + b) * c}$. "
            f"Subtract: ${(a + b) * c} - {d} = {value}$.",
            f"D'abord les parenthèses : ${a} + {b} = {a + b}$. Multiplication : ${a + b} \\times {c} = {(a + b) * c}$. "
            f"Soustraction : ${(a + b) * c} - {d} = {value}$.",
        )
        wrong = [a + b * c - d, (a + b) * (c - d), (a + b) * c + d]
    elif kind == 2:
        q = rng.randint(2, 6)
        expr, value = f"{a} \\times {b} - {d * q} \\div {d}", a * b - q
        steps = L(
            f"Multiply and divide first: ${a} \\times {b} = {a * b}$ and ${d * q} \\div {d} = {q}$. "
            f"Then subtract: ${a * b} - {q} = {value}$.",
            f"D'abord la multiplication et la division : ${a} \\times {b} = {a * b}$ et ${d * q} \\div {d} = {q}$. "
            f"Puis la soustraction : ${a * b} - {q} = {value}$.",
        )
        wrong = [a * b - d * q, a * b + q, a * (b - q)]
    else:
        a = rng.randint(4, 9)
        expr, value = f"{a}^2 - {b} \\times {c}", a * a - b * c
        steps = L(
            f"Powers first: ${a}^2 = {a * a}$. Multiply: ${b} \\times {c} = {b * c}$. Subtract: ${a * a} - {b * c} = {value}$.",
            f"D'abord la puissance : ${a}^2 = {a * a}$. Multiplication : ${b} \\times {c} = {b * c}$. Soustraction : ${a * a} - {b * c} = {value}$.",
        )
        wrong = [(a * a - b) * c, 2 * a - b * c, a * a + b * c]
    prompt = L(f"What is ${expr}$?", f"Combien font ${expr}$ ?")
    return Question(prompt, *pick(rng, value, wrong, m), steps)


@skill("percentages", "Percentages", "Middle School", "Percentages",
       "Percent of a number, percent change and what percent one number is of another.")
def percentages(rng):
    kind = rng.randrange(3)
    if kind == 0:
        while True:
            p, n = rng.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 120, 150]), rng.randrange(20, 401, 10)
            if p * n % 100 == 0:
                break
        r = p * n // 100
        explain = L(
            f"${percent(p)}$ means ${p}$ out of $100$, so multiply: $\\frac{{{p}}}{{100}} \\times {n} = {r}$.",
            f"${percent(p)}$ signifie ${p}$ sur $100$, donc multiplie : $\\frac{{{p}}}{{100}} \\times {n} = {r}$.",
        )
        prompt = L(f"What is ${percent(p)}$ of ${n}$?", f"Combien font ${percent(p)}$ de ${n}$ ?")
        return Question(prompt, *pick(rng, r, [r * 10, n - r, r + p, r * 2], m), explain)

    if kind == 1:
        while True:
            old, k = rng.randrange(20, 201, 10), rng.choice([10, 20, 25, 30, 40, 50, 60, 75])
            if old * k % 100 == 0:
                break
        up = rng.random() < 0.5
        change = old * k // 100
        new = old + change if up else old - change
        words = {True: L("increase", "Hausse"), False: L("decrease", "Baisse")}
        label = lambda v, rising=up: L(f"${percent(v)}$ {words[rising]}", f"{words[rising]} de ${percent(v)}$")
        wrong = [label(k, not up), label(change), label(round(change / new * 100)), label(k + 5), label(k * 2)]
        explain = L(
            f"The change is ${change}$. Divide it by the starting price: "
            f"$\\frac{{{change}}}{{{old}}} = {percent(k)}$, so it is a ${percent(k)}$ {words[up]}.",
            f"La variation est ${change}$. Divise-la par le prix de départ : "
            f"$\\frac{{{change}}}{{{old}}} = {percent(k)}$, c'est donc une {words[up].lower()} de ${percent(k)}$.",
        )
        prompt = L(f"A price goes from ${old}$ dollars to ${new}$ dollars. What is the percent change?",
                   f"Un prix passe de ${old}$ euros à ${new}$ euros. Quelle est la variation en pourcentage ?")
        return Question(prompt, *pick(rng, label(k), wrong), explain)

    while True:
        whole, p = rng.choice([20, 25, 40, 50, 80, 200]), rng.randrange(5, 100, 5)
        if whole * p % 100 == 0:
            break
    part = whole * p // 100
    explain = L(
        f"Divide the part by the whole and multiply by $100$: $\\frac{{{part}}}{{{whole}}} \\times 100 = {percent(p)}$.",
        f"Divise la partie par le tout et multiplie par $100$ : $\\frac{{{part}}}{{{whole}}} \\times 100 = {percent(p)}$.",
    )
    wrong = [100 - p, round(whole / part * 100), part, p + 10]
    prompt = L(f"${part}$ is what percent of ${whole}$?", f"${part}$ représente quel pourcentage de ${whole}$ ?")
    return Question(prompt, *pick(rng, p, wrong, lambda v: m(percent(v))), explain)


@skill("ratios", "Ratios and proportions", "Middle School", "Ratios",
       "Scale ratios, share amounts fairly and find unit rates.")
def ratios(rng):
    kind = rng.randrange(3)
    if kind == 0:
        while True:
            a, b = rng.randint(1, 9), rng.randint(2, 9)
            if a != b and gcd(a, b) == 1:
                break
        k = rng.randint(2, 8)
        d, x = b * k, a * k
        explain = L(
            f"The bottom went from ${b}$ to ${d}$, which is times ${k}$. Do the same to the top: ${a} \\times {k} = {x}$.",
            f"Le bas passe de ${b}$ à ${d}$, soit une multiplication par ${k}$. Fais pareil en haut : ${a} \\times {k} = {x}$.",
        )
        equation = f"$\\frac{{{a}}}{{{b}}} = \\frac{{x}}{{{d}}}$"
        prompt = L(f"Solve for $x$: {equation}", f"Trouve $x$ : {equation}")
        return Question(prompt, *pick(rng, x, [a + d - b, x + k, x - k, d], m), explain)

    if kind == 1:
        while True:
            p, q = rng.sample(range(1, 8), 2)
            if gcd(p, q) == 1:
                break
        unit = rng.randint(3, 12)
        total, big = (p + q) * unit, max(p, q) * unit
        explain = L(
            f"There are ${p} + {q} = {p + q}$ equal parts, so one part is ${total} \\div {p + q} = {unit}$. "
            f"The larger share is ${max(p, q)} \\times {unit} = {big}$.",
            f"Il y a ${p} + {q} = {p + q}$ parts égales, donc une part vaut ${total} \\div {p + q} = {unit}$. "
            f"La plus grande part vaut ${max(p, q)} \\times {unit} = {big}$.",
        )
        prompt = L(f"Share ${total}$ sweets in the ratio ${p}:{q}$. How many sweets are in the larger share?",
                   f"Partage ${total}$ bonbons selon le rapport ${p}:{q}$. Combien de bonbons y a-t-il dans la plus grande part ?")
        return Question(prompt, *pick(rng, big, [min(p, q) * unit, total // 2, total - unit, big + unit], m), explain)

    item_en, item_fr = rng.choice(ITEMS)
    n, k = rng.sample(range(2, 10), 2)
    unit = rng.randint(2, 9)
    cost = n * unit
    explain = L(
        f"Find the cost of one: ${cost} \\div {n} = {unit}$ dollars. Then ${k} \\times {unit} = {k * unit}$ dollars.",
        f"Trouve le prix d'un seul : ${cost} \\div {n} = {unit}$ euros. Puis ${k} \\times {unit} = {k * unit}$ euros.",
    )
    prompt = L(f"${n}$ {item_en} cost ${cost}$ dollars. How many dollars do ${k}$ {item_en} cost?",
               f"${n}$ {item_fr} coûtent ${cost}$ euros. Combien d'euros coûtent ${k}$ {item_fr} ?")
    return Question(prompt, *pick(rng, k * unit, [cost + k - n, cost * k, unit * (k + 1)], m), explain)


@skill("area-perimeter", "Area and perimeter", "Middle School", "Geometry",
       "Measure rectangles, triangles and circles.")
def area_perimeter(rng):
    kind = rng.randrange(5)
    if kind < 2:
        l, w = rng.randint(3, 20), rng.randint(2, 15)
        if l == w:
            l += 1
        area, perim = l * w, 2 * (l + w)
        shape = L(f"A rectangle is ${l}$ cm long and ${w}$ cm wide.", f"Un rectangle mesure ${l}$ cm de long et ${w}$ cm de large.")
        if kind == 0:
            explain = L(
                f"Area of a rectangle is length times width: ${l} \\times {w} = {area}$ square centimeters.",
                f"L'aire d'un rectangle est la longueur fois la largeur : ${l} \\times {w} = {area}$ centimètres carrés.",
            )
            prompt = L(f"{shape} What is its area in square centimeters?", f"{shape} Quelle est son aire en centimètres carrés ?")
            return Question(prompt, *pick(rng, area, [perim, l + w, area * 2], m), explain)
        explain = L(
            f"Perimeter is the distance all the way around: $2 \\times ({l} + {w}) = {perim}$ cm.",
            f"Le périmètre est la longueur du tour complet : $2 \\times ({l} + {w}) = {perim}$ cm.",
        )
        prompt = L(f"{shape} What is its perimeter in centimeters?", f"{shape} Quel est son périmètre en centimètres ?")
        return Question(prompt, *pick(rng, perim, [area, l + w, 2 * l + w], m), explain)

    if kind == 2:
        while True:
            b, h = rng.randint(3, 16), rng.randint(2, 12)
            if b * h % 2 == 0:
                break
        area = b * h // 2
        explain = L(
            f"Area of a triangle is half of base times height: $\\frac{{1}}{{2}} \\times {b} \\times {h} = {area}$ square meters.",
            f"L'aire d'un triangle est la moitié de la base fois la hauteur : $\\frac{{1}}{{2}} \\times {b} \\times {h} = {area}$ mètres carrés.",
        )
        prompt = L(f"A triangle has a base of ${b}$ m and a height of ${h}$ m. What is its area in square meters?",
                   f"Un triangle a une base de ${b}$ m et une hauteur de ${h}$ m. Quelle est son aire en mètres carrés ?")
        return Question(prompt, *pick(rng, area, [b * h, b + h, area + b], m), explain)

    r = rng.randint(2, 10)
    with_pi = lambda v: m(f"{v}\\pi")
    if kind == 3:
        explain = L(
            f"Area of a circle is $\\pi r^2$: $\\pi \\times {r}^2 = {r * r}\\pi$ square centimeters.",
            f"L'aire d'un cercle est $\\pi r^2$ : $\\pi \\times {r}^2 = {r * r}\\pi$ centimètres carrés.",
        )
        prompt = L(f"A circle has a radius of ${r}$ cm. What is its area? Leave your answer in terms of $\\pi$.",
                   f"Un cercle a un rayon de ${r}$ cm. Quelle est son aire ? Donne la réponse en fonction de $\\pi$.")
        return Question(prompt, *pick(rng, r * r, [2 * r, 4 * r * r, r], with_pi), explain)
    explain = L(
        f"Circumference is $2\\pi r$: $2 \\times \\pi \\times {r} = {2 * r}\\pi$ cm.",
        f"La circonférence est $2\\pi r$ : $2 \\times \\pi \\times {r} = {2 * r}\\pi$ cm.",
    )
    prompt = L(f"A circle has a radius of ${r}$ cm. What is its circumference? Leave your answer in terms of $\\pi$.",
               f"Un cercle a un rayon de ${r}$ cm. Quelle est sa circonférence ? Donne la réponse en fonction de $\\pi$.")
    return Question(prompt, *pick(rng, 2 * r, [r * r, r, 4 * r], with_pi), explain)


@skill("statistics", "Mean, median, mode and range", "Middle School", "Statistics",
       "Summarize a small set of numbers four different ways.")
def statistics(rng):
    kind = rng.choice(["mean", "median", "mode", "range"])
    if kind == "mean":
        n, mean = rng.randint(4, 6), rng.randint(6, 20)
        while True:
            data = [rng.randint(mean - 6, mean + 6) for _ in range(n - 1)]
            last = mean * n - sum(data)
            if 1 <= last <= 40:
                break
        data.append(last)
        rng.shuffle(data)
        total = " + ".join(map(str, data))
        explain = L(
            f"Add the values: ${total} = {mean * n}$. Divide by how many there are: ${mean * n} \\div {n} = {mean}$.",
            f"Additionne les valeurs : ${total} = {mean * n}$. Divise par leur nombre : ${mean * n} \\div {n} = {mean}$.",
        )
        wrong = [Fraction(median(data)), mean * n, mean + 1, mean - 1]
        answer = mean
    elif kind == "median":
        n = rng.choice([5, 7])
        data = [rng.randint(1, 30) for _ in range(n)]
        ordered = sorted(data)
        answer = ordered[n // 2]
        explain = L(f"Sort the values: ${series(ordered)}$. The middle one is ${answer}$.",
                    f"Range les valeurs : ${series(ordered)}$. Celle du milieu est ${answer}$.")
        wrong = [data[n // 2], round(sum(data) / n), ordered[-1] - ordered[0], answer + 1]
    elif kind == "mode":
        answer = rng.randint(2, 20)
        others = rng.sample([v for v in range(1, 25) if v != answer], rng.randint(3, 5))
        data = [answer] * rng.randint(2, 3) + others
        rng.shuffle(data)
        explain = L(
            f"The mode is the value that appears most often. ${answer}$ appears ${data.count(answer)}$ times.",
            f"Le mode est la valeur qui apparaît le plus souvent. ${answer}$ apparaît ${data.count(answer)}$ fois.",
        )
        wrong = others[:3] + [len(data)]
    else:
        data = rng.sample(range(1, 50), rng.randint(5, 7))
        hi, lo = max(data), min(data)
        answer = hi - lo
        explain = L(f"Range is the largest value minus the smallest: ${hi} - {lo} = {answer}$.",
                    f"L'étendue est la plus grande valeur moins la plus petite : ${hi} - {lo} = {answer}$.")
        wrong = [hi, hi + lo, lo, answer + 1]
    prompt = L(f"What is the {kind} of ${series(data)}$?", f"Calcule {STAT_NAMES[kind]} de ${series(data)}$.")
    return Question(prompt, *pick(rng, answer, wrong, mf), explain)


@skill("probability", "Probability", "Middle School", "Probability",
       "Chances with marbles, dice and coins as simplified fractions.")
def probability(rng):
    kind = rng.randrange(4)
    if kind == 0:
        counts = {"red": rng.randint(1, 9), "blue": rng.randint(1, 9), "green": rng.randint(1, 9)}
        color = rng.choice(list(counts))
        want, total = counts[color], sum(counts.values())
        p = Fraction(want, total)
        one, many = COLORS[color]
        prompt = L(
            f"A bag has ${counts['red']}$ red, ${counts['blue']}$ blue and ${counts['green']}$ green marbles. "
            f"You pick one without looking. What is the probability it is {color}?",
            f"Un sac contient ${counts['red']}$ billes rouges, ${counts['blue']}$ bleues et ${counts['green']}$ vertes. "
            f"Tu en tires une au hasard. Quelle est la probabilité qu'elle soit {one} ?",
        )
        explain = L(
            f"There are ${want}$ {color} marbles out of ${total}$, so the probability is $\\frac{{{want}}}{{{total}}}${simplified(want, total, p)}.",
            f"Il y a ${want}$ billes {many} sur ${total}$, donc la probabilité est $\\frac{{{want}}}{{{total}}}${simplified(want, total, p)}.",
        )
        wrong = [Fraction(want, total - want), Fraction(total - want, total), Fraction(1, 3), Fraction(1, total)]
        return Question(prompt, *pick(rng, p, wrong, mf), explain)

    if kind == 1:
        name_en, name_fr, outcomes = rng.choice(DIE_EVENTS)
        p = Fraction(len(outcomes), 6)
        explain = L(
            f"The outcomes that count are ${series(outcomes)}$. "
            f"That is ${len(outcomes)}$ out of $6$, so the probability is ${frac(p)}$.",
            f"Les issues favorables sont ${series(outcomes)}$. "
            f"Cela fait ${len(outcomes)}$ sur $6$, donc la probabilité est ${frac(p)}$.",
        )
        wrong = [Fraction(len(outcomes), 12), Fraction(6 - len(outcomes), 6), Fraction(1, 6), Fraction(1, 2)]
        prompt = L(f"You roll a fair six sided die. What is the probability of rolling {name_en}?",
                   f"Tu lances un dé équilibré à six faces. Quelle est la probabilité d'obtenir {name_fr} ?")
        return Question(prompt, *pick(rng, p, wrong, mf), explain)

    if kind == 2:
        s = rng.randint(2, 12)
        ways = 6 - abs(s - 7)
        p = Fraction(ways, 36)
        explain = L(
            f"Two dice give $6 \\times 6 = 36$ equally likely pairs. ${ways}$ of them add up to ${s}$, "
            f"so the probability is $\\frac{{{ways}}}{{36}}${simplified(ways, 36, p)}.",
            f"Deux dés donnent $6 \\times 6 = 36$ paires de même probabilité. ${ways}$ d'entre elles ont pour somme ${s}$, "
            f"donc la probabilité est $\\frac{{{ways}}}{{36}}${simplified(ways, 36, p)}.",
        )
        wrong = [Fraction(1, 11), Fraction(ways, 12), Fraction(1, 36), Fraction(ways + 1, 36)]
        prompt = L(f"You roll two fair dice. What is the probability that they add up to ${s}$?",
                   f"Tu lances deux dés équilibrés. Quelle est la probabilité que leur somme soit ${s}$ ?")
        return Question(prompt, *pick(rng, p, wrong, mf), explain)

    n = rng.randint(2, 4)
    k = rng.randint(0, n)
    ways, outcomes = comb(n, k), 2 ** n
    p = Fraction(ways, outcomes)
    explain = L(
        f"Flipping ${n}$ coins gives $2^{n} = {outcomes}$ equally likely results. Exactly ${k}$ heads happens in "
        f"$\\binom{{{n}}}{{{k}}} = {ways}$ of them, so the probability is $\\frac{{{ways}}}{{{outcomes}}}${simplified(ways, outcomes, p)}.",
        f"Lancer ${n}$ pièces donne $2^{n} = {outcomes}$ résultats de même probabilité. Exactement ${k}$ fois face se produit dans "
        f"$\\binom{{{n}}}{{{k}}} = {ways}$ d'entre eux, donc la probabilité est $\\frac{{{ways}}}{{{outcomes}}}${simplified(ways, outcomes, p)}.",
    )
    wrong = [Fraction(1, outcomes), Fraction(k, n), Fraction(1, n + 1), Fraction(1, 2)]
    prompt = L(f"You flip a fair coin ${n}$ times. What is the probability of getting exactly ${k}$ heads?",
               f"Tu lances une pièce équilibrée ${n}$ fois. Quelle est la probabilité d'obtenir exactement ${k}$ fois face ?")
    return Question(prompt, *pick(rng, p, wrong, mf), explain)
