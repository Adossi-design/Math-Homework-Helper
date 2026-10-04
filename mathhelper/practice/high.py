"""High school skills: equations, lines, systems, quadratics, exponents and triangles."""
from fractions import Fraction
from math import sqrt

from .core import L, Question, frac, linear, m, mf, paren, pick, poly, skill

NONZERO = [n for n in range(-9, 10) if n]
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]


def move(b):
    """Describe how to clear a constant from one side of an equation."""
    if b > 0:
        return L(f"subtract ${b}$ from both sides", f"soustrais ${b}$ des deux côtés")
    return L(f"add ${-b}$ to both sides", f"ajoute ${-b}$ des deux côtés")


def point(x, y):
    """Write a point the way each language separates coordinates."""
    return L(f"({x}, {y})", f"({x};{y})")


@skill("linear-equations", "Linear equations", "High School", "Algebra",
       "Solve one variable equations in one, two or several steps.")
def linear_equations(rng):
    x = rng.choice(NONZERO + [10, -10])
    kind = rng.randrange(3)
    if kind == 0:
        a = rng.choice([n for n in NONZERO if abs(n) > 1])
        b = rng.choice([n for n in range(-20, 21) if n])
        c = a * x + b
        eq = f"{linear([(a, 'x'), (b, '')])} = {c}"
        explain = L(
            f"First {move(b)}: ${linear([(a, 'x')])} = {c - b}$. Then divide both sides by ${a}$: $x = {x}$.",
            f"D'abord, {move(b)} : ${linear([(a, 'x')])} = {c - b}$. Puis divise les deux côtés par ${a}$ : $x = {x}$.",
        )
        wrong = [Fraction(c + b, a), c - b, -x, x + 1]
    elif kind == 1:
        a = rng.choice([n for n in NONZERO if abs(n) > 1])
        b = rng.choice(NONZERO)
        c = a * (x + b)
        inner = linear([(1, "x"), (b, "")])
        eq = f"{a}({inner}) = {c}"
        explain = L(
            f"Divide both sides by ${a}$: ${inner} = {x + b}$. Then {move(b)}: $x = {x}$.",
            f"Divise les deux côtés par ${a}$ : ${inner} = {x + b}$. Puis {move(b)} : $x = {x}$.",
        )
        wrong = [Fraction(c, a) + b, Fraction(c, a), c - b, -x]
    else:
        a, c = rng.sample(NONZERO, 2)
        b = rng.randint(-15, 15)
        d = (a - c) * x + b
        eq = f"{linear([(a, 'x'), (b, '')])} = {linear([(c, 'x'), (d, '')])}"
        gathered = f"${linear([(a - c, 'x'), (b, '')])} = {d}$"
        cleared = f"${linear([(a - c, 'x')])} = {d - b}$"
        explain = L(
            f"Gather the $x$ terms on the left: {gathered}. " + (f"Next {move(b)}: {cleared}. " if b else "")
            + f"Divide by ${a - c}$: $x = {x}$.",
            f"Regroupe les termes en $x$ à gauche : {gathered}. " + (f"Ensuite, {move(b)} : {cleared}. " if b else "")
            + f"Divise par ${a - c}$ : $x = {x}$.",
        )
        wrong = [Fraction(d + b, a - c), -x, x + 2, x - 1]
        if a + c:
            wrong.insert(1, Fraction(d - b, a + c))
    prompt = L(f"Solve for $x$: ${eq}$", f"Trouve $x$ : ${eq}$")
    return Question(prompt, *pick(rng, x, wrong, mf), explain)


@skill("slope", "Slope and lines", "High School", "Functions",
       "Find slopes and pick the right line equation.")
def slope(rng):
    kind = rng.randrange(3)
    if kind == 0:
        while True:
            x1, y1, x2, y2 = (rng.randint(-8, 8) for _ in range(4))
            if x1 != x2 and y1 != y2:
                break
        s = Fraction(y2 - y1, x2 - x1)
        work = f"$\\frac{{{y2} - {paren(y1)}}}{{{x2} - {paren(x1)}}} = \\frac{{{y2 - y1}}}{{{x2 - x1}}}"
        if (s.numerator, s.denominator) != (y2 - y1, x2 - x1):
            work += f" = {frac(s)}"
        explain = L(f"Slope is rise over run: {work}$.", f"La pente est la variation de $y$ divisée par celle de $x$ : {work}$.")
        wrong = [1 / s, -s, s + 1, s - 1]
        if x1 + x2:
            wrong.insert(2, Fraction(y1 + y2, x1 + x2))
        prompt = L(f"What is the slope of the line through ${point(x1, y1)}$ and ${point(x2, y2)}$?",
                   f"Quelle est la pente de la droite passant par ${point(x1, y1)}$ et ${point(x2, y2)}$ ?")
        return Question(prompt, *pick(rng, s, wrong, mf), explain)

    if kind == 1:
        k = rng.choice([n for n in range(-5, 6) if n])
        p, q = rng.randint(-6, 6), rng.randint(-6, 6)
        b = q - k * p
        line = lambda intercept: m(f"y = {linear([(k, 'x'), (intercept, '')])}")
        explain = L(
            f"Start from $y = {linear([(k, 'x')])} + b$ and put in the point: ${q} = {k} \\times {paren(p)} + b$. "
            f"So $b = {q} - {paren(k * p)} = {b}$.",
            f"Pars de $y = {linear([(k, 'x')])} + b$ et remplace par le point : ${q} = {k} \\times {paren(p)} + b$. "
            f"Donc $b = {q} - {paren(k * p)} = {b}$.",
        )
        prompt = L(f"Which line has slope ${k}$ and passes through ${point(p, q)}$?",
                   f"Quelle droite a pour pente ${k}$ et passe par ${point(p, q)}$ ?")
        return Question(prompt, *pick(rng, b, [q + k * p, q, -b, b + k], line), explain)

    a, b = rng.sample(NONZERO, 2)
    c = rng.randint(-12, 12)
    s = Fraction(-a, b)
    isolated = f"${linear([(b, 'y')])} = {linear([(-a, 'x'), (c, '')])}$"
    reduced = f"$y = {linear([(s, 'x'), (Fraction(c, b), '')])}$"
    explain = L(
        f"Solve for $y$: {isolated}, so {reduced}. The slope is the number in front of $x$: ${frac(s)}$.",
        f"Isole $y$ : {isolated}, donc {reduced}. La pente est le coefficient de $x$ : ${frac(s)}$.",
    )
    equation = f"${linear([(a, 'x'), (b, 'y')])} = {c}$"
    prompt = L(f"What is the slope of the line {equation}?", f"Quelle est la pente de la droite {equation} ?")
    return Question(prompt, *pick(rng, s, [Fraction(a, b), Fraction(-b, a), Fraction(c, b)], mf), explain)


@skill("systems", "Systems of equations", "High School", "Algebra",
       "Solve two equations with two unknowns by elimination.")
def systems(rng):
    x, y = rng.randint(-6, 6), rng.randint(-6, 6)
    while True:
        a1, b1, a2, b2 = (rng.choice([n for n in range(-5, 6) if n]) for _ in range(4))
        if a1 * b2 - a2 * b1:
            break
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    k, r = a2 * b1 - a1 * b2, a2 * c1 - a1 * c2
    eq1, eq2 = f"{linear([(a1, 'x'), (b1, 'y')])} = {c1}", f"{linear([(a2, 'x'), (b2, 'y')])} = {c2}"
    eliminated = f"${linear([(k, 'y')])} = {r}$"
    substituted = f"${linear([(a1, 'x'), (b1 * y, '')])} = {c1}$"
    explain = L(
        f"Multiply the first equation by ${a2}$ and the second by ${a1}$ so the $x$ terms match, then subtract: "
        f"{eliminated}, so $y = {y}$. Put that into the first equation: {substituted}, so $x = {x}$.",
        f"Multiplie la première équation par ${a2}$ et la seconde par ${a1}$ pour avoir les mêmes termes en $x$, puis soustrais : "
        f"{eliminated}, donc $y = {y}$. Remplace dans la première équation : {substituted}, donc $x = {x}$.",
    )
    pair = lambda p: m(L(f"x = {p[0]},\\ y = {p[1]}", f"x = {p[0]} \\text{{ et }} y = {p[1]}"))
    wrong = [(y, x), (-x, -y), (x, -y), (-x, y), (x + 1, y - 1), (x - 1, y + 1), (x + 2, y), (x, y + 2)]
    cases = f"$\\begin{{cases}} {eq1} \\\\ {eq2} \\end{{cases}}$"
    prompt = L(f"Solve the system: {cases}", f"Résous le système : {cases}")
    return Question(prompt, *pick(rng, (x, y), wrong, pair), explain)


@skill("quadratics", "Quadratic equations", "High School", "Algebra",
       "Solve quadratics by factoring into two brackets.")
def quadratics(rng):
    r1, r2 = rng.sample(NONZERO, 2)
    k = rng.choice([1, 1, 1, 2, 3])
    b, c = -(r1 + r2), r1 * r2
    factor = lambda r: f"(x {'-' if r > 0 else '+'} {abs(r)})"
    either = L("or", "ou")

    def roots(p):
        low, high = sorted(p)
        return m(f"x = {low}") if low == high else m(f"x = {low} \\text{{ {either} }} x = {high}")

    reduced = f"${poly({2: 1, 1: b, 0: c})} = 0$"
    factored = f"${factor(r1)}{factor(r2)} = 0$"
    explain = L(
        (f"Divide every term by ${k}$: {reduced}. " if k > 1 else "")
        + f"Find two numbers that multiply to ${c}$ and add to ${b}$. They are ${-r1}$ and ${-r2}$, "
        f"so the equation factors as {factored}. That gives $x = {r1}$ or $x = {r2}$.",
        (f"Divise chaque terme par ${k}$ : {reduced}. " if k > 1 else "")
        + f"Cherche deux nombres dont le produit est ${c}$ et la somme ${b}$. Ce sont ${-r1}$ et ${-r2}$, "
        f"donc l'équation se factorise en {factored}. On obtient $x = {r1}$ ou $x = {r2}$.",
    )
    wrong = [(-r1, -r2), (r1, -r2), (-r1, r2), (r1 + 1, r2 - 1), (r1 - 1, r2 + 1)]
    equation = f"${poly({2: k, 1: k * b, 0: k * c})} = 0$"
    prompt = L(f"Solve {equation}", f"Résous {equation}")
    return Question(prompt, *pick(rng, (r1, r2), wrong, roots), explain)


@skill("exponents", "Exponent rules", "High School", "Exponents",
       "Multiply, divide and raise powers, including zero and negative exponents.")
def exponents(rng):
    kind = rng.randrange(5)
    v = rng.choice(["x", "a", "y", "n"])
    a, b = rng.randint(2, 9), rng.randint(2, 6)
    pw = lambda e: m(f"{v}^{{{e}}}")
    simplify = L("Simplify", "Simplifie")
    if kind == 0:
        work = f"${v}^{{{a} + {b}}} = {v}^{{{a + b}}}$"
        explain = L(f"Multiplying powers with the same base means adding the exponents: {work}.",
                    f"Multiplier des puissances de même base revient à additionner les exposants : {work}.")
        return Question(f"{simplify} ${v}^{{{a}}} \\cdot {v}^{{{b}}}$", *pick(rng, a + b, [a * b, abs(a - b), a + b + 1], pw), explain)
    if kind == 1:
        work = f"${v}^{{{a} \\times {b}}} = {v}^{{{a * b}}}$"
        explain = L(f"A power of a power means multiplying the exponents: {work}.",
                    f"Une puissance de puissance revient à multiplier les exposants : {work}.")
        return Question(f"{simplify} $({v}^{{{a}}})^{{{b}}}$", *pick(rng, a * b, [a + b, a * b + b, a * b - 1], pw), explain)
    if kind == 2:
        a = b + rng.randint(1, 6)
        work = f"${v}^{{{a} - {b}}} = {v}^{{{a - b}}}$"
        explain = L(f"Dividing powers with the same base means subtracting the exponents: {work}.",
                    f"Diviser des puissances de même base revient à soustraire les exposants : {work}.")
        prompt = f"{simplify} $\\frac{{{v}^{{{a}}}}}{{{v}^{{{b}}}}}$"
        return Question(prompt, *pick(rng, a - b, [a + b, b - a, a * b], pw), explain)

    base, n = rng.randint(2, 5), rng.randint(2, 4)
    if kind == 3:
        chain = " \\times ".join([str(base)] * n)
        explain = L(
            f"${base}^{n}$ means ${n}$ copies of ${base}$ multiplied together: ${chain} = {base ** n}$.",
            f"${base}^{n}$ signifie ${n}$ facteurs égaux à ${base}$ : ${chain} = {base ** n}$.",
        )
        prompt = L(f"What is ${base}^{n}$?", f"Combien vaut ${base}^{n}$ ?")
        return Question(prompt, *pick(rng, base ** n, [base * n, base ** (n - 1), base ** (n + 1)], m), explain)
    n = rng.randint(1, 3)
    work = f"${base}^{{-{n}}} = \\frac{{1}}{{{base}^{n}}} = \\frac{{1}}{{{base ** n}}}$"
    explain = L(f"A negative exponent means one over the positive power: {work}.",
                f"Un exposant négatif signifie l'inverse de la puissance positive : {work}.")
    wrong = [-(base ** n), Fraction(1, base * n), -base * n]
    prompt = L(f"What is ${base}^{{-{n}}}$?", f"Combien vaut ${base}^{{-{n}}}$ ?")
    return Question(prompt, *pick(rng, Fraction(1, base ** n), wrong, mf), explain)


@skill("pythagorean", "Pythagorean theorem", "High School", "Geometry",
       "Find the missing side of a right triangle.")
def pythagorean(rng):
    a, b, c = rng.choice(TRIPLES)
    k = rng.randint(1, 3) if c <= 17 else 1
    a, b, c = a * k, b * k, c * k
    if rng.random() < 0.5:
        a, b = b, a
    if rng.random() < 0.5:
        work = f"${a}^2 + {b}^2 = {a * a} + {b * b} = {c * c}$"
        root = f"$c = \\sqrt{{{c * c}}} = {c}$"
        explain = L(f"Use $a^2 + b^2 = c^2$: {work}. So {root}.", f"Utilise $a^2 + b^2 = c^2$ : {work}. Donc {root}.")
        prompt = L(f"A right triangle has legs of ${a}$ and ${b}$. How long is the hypotenuse?",
                   f"Un triangle rectangle a des côtés de l'angle droit de ${a}$ et ${b}$. Quelle est la longueur de l'hypoténuse ?")
        return Question(prompt, *pick(rng, c, [a + b, c + 1, c - 1, c * c], m), explain)
    work = f"${c}^2 - {a}^2 = {c * c} - {a * a} = {b * b}$"
    root = f"$b = \\sqrt{{{b * b}}} = {b}$"
    explain = L(f"Rearrange to $b^2 = c^2 - a^2$: {work}. So {root}.", f"Transforme en $b^2 = c^2 - a^2$ : {work}. Donc {root}.")
    prompt = L(f"A right triangle has a hypotenuse of ${c}$ and one leg of ${a}$. How long is the other leg?",
               f"Un triangle rectangle a une hypoténuse de ${c}$ et un côté de ${a}$. Quelle est la longueur de l'autre côté ?")
    return Question(prompt, *pick(rng, b, [c - a, round(sqrt(c * c + a * a)), b + 1, b + 2], m), explain)


EXACT = {
    ("sin", 0): "0", ("sin", 30): "\\frac{1}{2}", ("sin", 45): "\\frac{\\sqrt{2}}{2}",
    ("sin", 60): "\\frac{\\sqrt{3}}{2}", ("sin", 90): "1",
    ("cos", 0): "1", ("cos", 30): "\\frac{\\sqrt{3}}{2}", ("cos", 45): "\\frac{\\sqrt{2}}{2}",
    ("cos", 60): "\\frac{1}{2}", ("cos", 90): "0",
    ("tan", 0): "0", ("tan", 30): "\\frac{\\sqrt{3}}{3}", ("tan", 45): "1", ("tan", 60): "\\sqrt{3}",
}
THIRTY_SIXTY = (
    "Use the right triangle with angles $30^\\circ$ and $60^\\circ$ and sides $1$, $\\sqrt{3}$ and $2$.",
    "Utilise le triangle rectangle d'angles $30^\\circ$ et $60^\\circ$ et de côtés $1$, $\\sqrt{3}$ et $2$.",
)
ANGLE_HINTS = {
    0: ("On the unit circle the point at $0^\\circ$ is $(1, 0)$. Cosine is the $x$ value, sine is the $y$ value and tangent is $y$ over $x$.",
        "Sur le cercle trigonométrique, le point à $0^\\circ$ est $(1;0)$. Le cosinus est l'abscisse, le sinus est l'ordonnée et la tangente est $y$ sur $x$."),
    90: ("On the unit circle the point at $90^\\circ$ is $(0, 1)$. Cosine is the $x$ value and sine is the $y$ value.",
         "Sur le cercle trigonométrique, le point à $90^\\circ$ est $(0;1)$. Le cosinus est l'abscisse et le sinus est l'ordonnée."),
    45: ("Use the right triangle with sides $1$, $1$ and $\\sqrt{2}$.",
         "Utilise le triangle rectangle de côtés $1$, $1$ et $\\sqrt{2}$."),
    30: THIRTY_SIXTY,
    60: THIRTY_SIXTY,
}
RATIO_RULES = {
    "sin": ("opposite over hypotenuse", "le côté opposé sur l'hypoténuse"),
    "cos": ("adjacent over hypotenuse", "le côté adjacent sur l'hypoténuse"),
    "tan": ("opposite over adjacent", "le côté opposé sur le côté adjacent"),
}


@skill("trigonometry", "Trigonometry", "High School", "Trigonometry",
       "Exact values of special angles and SOH CAH TOA ratios.")
def trigonometry(rng):
    if rng.random() < 0.5:
        fn, angle = rng.choice(list(EXACT))
        value = EXACT[(fn, angle)]
        wrong = rng.sample(sorted(set(EXACT.values()) - {value}), 3)
        result = f"$\\{fn} {angle}^\\circ = {value}$"
        explain = L(f"{ANGLE_HINTS[angle][0]} So {result}.", f"{ANGLE_HINTS[angle][1]} Donc {result}.")
        prompt = L(f"What is the exact value of $\\{fn} {angle}^\\circ$?", f"Quelle est la valeur exacte de $\\{fn} {angle}^\\circ$ ?")
        return Question(prompt, *pick(rng, value, wrong, m), explain)

    a, b, c = rng.choice(TRIPLES[:3])
    k = rng.randint(1, 2)
    a, b, c = a * k, b * k, c * k
    fn = rng.choice(list(RATIO_RULES))
    sides = {"sin": (a, c), "cos": (b, c), "tan": (a, b)}[fn]
    value = Fraction(*sides)
    others = [Fraction(a, c), Fraction(b, c), Fraction(a, b), Fraction(b, a), Fraction(c, a), Fraction(c, b)]
    wrong = [w for w in others if w != value]
    reduced = f" = {frac(value)}" if value.denominator != sides[1] else ""
    ratio = f"$\\frac{{{sides[0]}}}{{{sides[1]}}}{reduced}$"
    explain = L(f"$\\{fn}\\theta$ is {RATIO_RULES[fn][0]}: {ratio}.", f"$\\{fn}\\theta$ est {RATIO_RULES[fn][1]} : {ratio}.")
    prompt = L(
        f"In a right triangle, the side opposite angle $\\theta$ is ${a}$, the side next to it is ${b}$ "
        f"and the hypotenuse is ${c}$. What is $\\{fn}\\theta$?",
        f"Dans un triangle rectangle, le côté opposé à l'angle $\\theta$ mesure ${a}$, le côté adjacent ${b}$ "
        f"et l'hypoténuse ${c}$. Combien vaut $\\{fn}\\theta$ ?",
    )
    return Question(prompt, *pick(rng, value, wrong, mf), explain)
