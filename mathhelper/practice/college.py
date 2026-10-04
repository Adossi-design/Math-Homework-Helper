"""College skills: logarithms, limits, derivatives, integrals and matrices."""
from fractions import Fraction

from .core import L, Question, frac, linear, m, mf, paren, pick, poly, skill

NONZERO = [n for n in range(-9, 10) if n]
LOG_RANGES = {2: (-3, 6), 3: (-2, 4), 5: (-2, 3), 10: (-2, 4)}


def signed(n):
    """Write a number with a spaced sign, like + 4 or - 4."""
    return f"+ {n}" if n >= 0 else f"- {-n}"


def math_or_text(value):
    """Format numbers as math and leave ready made LaTeX strings alone."""
    return m(value) if isinstance(value, str) else mf(value)


@skill("logarithms", "Logarithms", "College", "Logarithms",
       "Evaluate logs, combine them with log rules and solve exponential equations.")
def logarithms(rng):
    kind = rng.randrange(3)
    if kind == 0:
        b = rng.choice(list(LOG_RANGES))
        k = rng.randint(*LOG_RANGES[b])
        arg = Fraction(b) ** k
        explain = L(
            f"Ask which power of ${b}$ gives ${frac(arg)}$. Since ${b}^{{{k}}} = {frac(arg)}$, the answer is ${k}$.",
            f"Cherche quelle puissance de ${b}$ donne ${frac(arg)}$. Comme ${b}^{{{k}}} = {frac(arg)}$, la réponse est ${k}$.",
        )
        prompt = L(f"What is $\\log_{{{b}}} {frac(arg)}$?", f"Combien vaut $\\log_{{{b}}} {frac(arg)}$ ?")
        return Question(prompt, *pick(rng, k, [k + 1, -k, k - 1, arg / b], mf), explain)

    simplify = L("Simplify", "Simplifie")
    if kind == 1:
        if rng.random() < 0.5:
            b, k = rng.choice([2, 3, 5]), rng.randint(1, 3)
            y = rng.choice([n for n in range(2, 8) if n % b])
            x = y * b ** k
            work = f"$\\log_{{{b}}} \\frac{{{x}}}{{{y}}} = \\log_{{{b}}} {b ** k} = {k}$"
            explain = L(f"Subtracting logs with the same base means dividing inside: {work}.",
                        f"Soustraire des logarithmes de même base revient à diviser à l'intérieur : {work}.")
            prompt = f"{simplify} $\\log_{{{b}}} {x} - \\log_{{{b}}} {y}$"
            return Question(prompt, *pick(rng, k, [k + 1, x - y, b ** k], m), explain)
        b, k = rng.choice([2, 3, 6, 10]), rng.randint(2, 3)
        x = rng.choice([n for n in range(2, b ** k) if b ** k % n == 0])
        y = b ** k // x
        work = f"$\\log_{{{b}}} ({x} \\times {y}) = \\log_{{{b}}} {b ** k} = {k}$"
        explain = L(f"Adding logs with the same base means multiplying inside: {work}.",
                    f"Additionner des logarithmes de même base revient à multiplier à l'intérieur : {work}.")
        prompt = f"{simplify} $\\log_{{{b}}} {x} + \\log_{{{b}}} {y}$"
        return Question(prompt, *pick(rng, k, [k + 1, k - 1, x + y], m), explain)

    b = rng.choice([2, 3, 5])
    k, s = rng.randint(2, 4), rng.randint(-2, 3)
    exponent = linear([(1, "x"), (s, "")])
    explain = L(
        f"Write ${b ** k}$ as ${b}^{{{k}}}$. With the same base, the exponents must match: ${exponent} = {k}$, so $x = {k - s}$.",
        f"Écris ${b ** k}$ sous la forme ${b}^{{{k}}}$. Avec la même base, les exposants sont égaux : ${exponent} = {k}$, donc $x = {k - s}$.",
    )
    equation = f"${b}^{{{exponent}}} = {b ** k}$"
    prompt = L(f"Solve for $x$: {equation}", f"Trouve $x$ : {equation}")
    return Question(prompt, *pick(rng, k - s, [k, k + s, b ** k // b - s], m), explain)


@skill("limits", "Limits", "College", "Calculus",
       "Direct substitution, factoring away zero over zero and limits at infinity.")
def limits(rng):
    kind = rng.randrange(3)
    find = L("Find", "Calcule")
    if kind == 0:
        a = rng.choice([n for n in range(-6, 7) if n])
        k = rng.choice([n for n in range(-6, 7) if n])
        top, bottom = poly({2: 1, 1: k - a, 0: -a * k}), linear([(1, "x"), (-a, "")])
        factored = f"$({bottom})({linear([(1, 'x'), (k, '')])})$"
        result = f"${a} {signed(k)} = {a + k}$"
        explain = L(
            f"Plugging in $x = {a}$ gives $\\frac{{0}}{{0}}$, so factor the top as {factored}. "
            f"Cancel the shared factor, then plug in: {result}.",
            f"Remplacer par $x = {a}$ donne $\\frac{{0}}{{0}}$, donc factorise le numérateur en {factored}. "
            f"Simplifie le facteur commun, puis remplace : {result}.",
        )
        prompt = f"{find} $\\lim_{{x \\to {a}}} \\frac{{{top}}}{{{bottom}}}$"
        wrong = [0, L("\\text{does not exist}", "\\text{n'existe pas}"), a - k, k]
        return Question(prompt, *pick(rng, a + k, wrong, math_or_text), explain)

    if kind == 1:
        p, s = rng.sample(NONZERO, 2)
        q, r, t, u = (rng.randint(-9, 9) for _ in range(4))
        bottom = poly({2: s, 1: t, 0: u})
        if rng.random() < 0.6:
            answer = Fraction(p, s)
            top = poly({2: p, 1: q, 0: r})
            ratio = f"$\\frac{{{p}}}{{{s}}} = {frac(answer)}$"
            explain = L(
                f"Top and bottom share the same highest power, $x^2$, so the limit is the ratio of their leading numbers: {ratio}.",
                f"Le numérateur et le dénominateur ont la même plus grande puissance, $x^2$, donc la limite est le rapport de leurs coefficients : {ratio}.",
            )
            wrong = [Fraction(q, t) if t else Fraction(q + 1), Fraction(r, u) if u else Fraction(p), 0, "\\infty"]
        else:
            answer = Fraction(0)
            top = poly({1: p, 0: q})
            explain = L(
                "The bottom has the higher power, so it grows much faster than the top and the fraction shrinks toward $0$.",
                "Le dénominateur a la plus grande puissance, il grandit donc bien plus vite que le numérateur et la fraction tend vers $0$.",
            )
            wrong = [Fraction(p, s), "\\infty", Fraction(q, u) if u else Fraction(1), Fraction(p, t) if t else Fraction(-1)]
        prompt = f"{find} $\\lim_{{x \\to \\infty}} \\frac{{{top}}}{{{bottom}}}$"
        return Question(prompt, *pick(rng, answer, wrong, math_or_text), explain)

    a = rng.randint(-4, 4)
    b, c, d = rng.choice(NONZERO), rng.randint(-9, 9), rng.randint(-9, 9)
    value = b * a * a + c * a + d
    work = f"${b} \\cdot {paren(a)}^2 {signed(c)} \\cdot {paren(a)} {signed(d)} = {value}$"
    explain = L(f"A polynomial is continuous, so plug in $x = {a}$ directly: {work}.",
                f"Un polynôme est continu, il suffit donc de remplacer par $x = {a}$ : {work}.")
    prompt = f"{find} $\\lim_{{x \\to {a}}} \\left({poly({2: b, 1: c, 0: d})}\\right)$"
    return Question(prompt, *pick(rng, value, [b * a + c * a + d, 2 * b * a + c, value + b], m), explain)


SPECIAL_DERIVATIVES = {
    "sin": ("{n}\\sin x", "{n}\\cos x", ["-{n}\\cos x", "\\cos x", "-{n}\\sin x"],
            "The derivative of $\\sin x$ is $\\cos x$, and the constant ${n}$ stays in front.",
            "La dérivée de $\\sin x$ est $\\cos x$, et la constante ${n}$ reste devant."),
    "cos": ("{n}\\cos x", "-{n}\\sin x", ["{n}\\sin x", "-\\sin x", "-{n}\\cos x"],
            "The derivative of $\\cos x$ is $-\\sin x$, and the constant ${n}$ stays in front.",
            "La dérivée de $\\cos x$ est $-\\sin x$, et la constante ${n}$ reste devant."),
    "exp": ("e^{{{n}x}}", "{n}e^{{{n}x}}", ["e^{{{n}x}}", "{n}xe^{{{n}x - 1}}", "\\frac{{e^{{{n}x}}}}{{{n}}}"],
            "By the chain rule the derivative of $e^{{kx}}$ is $ke^{{kx}}$, so here $k = {n}$.",
            "La dérivée de $e^{{kx}}$ est $ke^{{kx}}$, donc ici $k = {n}$."),
    "ln": ("{n}\\ln x", "\\frac{{{n}}}{{x}}", ["\\frac{{1}}{{{n}x}}", "-\\frac{{{n}}}{{x^2}}", "{n}x"],
           "The derivative of $\\ln x$ is $\\frac{{1}}{{x}}$, and the constant ${n}$ stays in front.",
           "La dérivée de $\\ln x$ est $\\frac{{1}}{{x}}$, et la constante ${n}$ reste devant."),
}


@skill("derivatives", "Derivatives", "College", "Calculus",
       "The power rule, derivative values and derivatives of common functions.")
def derivatives(rng):
    kind = rng.randrange(3)
    if kind == 0:
        powers = [rng.randint(2, 5)] + rng.sample(range(0, 2), rng.randint(1, 2))
        coeffs = {p: rng.choice(NONZERO) for p in powers}
        d = {p - 1: c * p for p, c in coeffs.items() if p}
        wrong = [
            {p - 1: c for p, c in coeffs.items() if p},
            {p: c * p for p, c in coeffs.items() if p},
            {k: -v for k, v in d.items()},
        ]
        result = f"$f'(x) = {poly(d)}$"
        explain = L(
            f"Use the power rule on each term: multiply by the power, then lower the power by one. Constants disappear. So {result}.",
            f"Applique la règle des puissances à chaque terme : multiplie par l'exposant, puis baisse l'exposant de un. Les constantes disparaissent. Donc {result}.",
        )
        function = f"$f(x) = {poly(coeffs)}$"
        prompt = L(f"Find the derivative of {function}", f"Calcule la dérivée de {function}")
        return Question(prompt, *pick(rng, d, wrong, lambda cs: m(poly(cs))), explain)

    if kind == 1:
        a, b, c = rng.choice(NONZERO), rng.randint(-9, 9), rng.randint(-9, 9)
        k = rng.randint(-4, 4)
        value = 2 * a * k + b
        first = f"$f'(x) = {poly({1: 2 * a, 0: b})}$"
        second = f"$f'({k}) = {2 * a} \\cdot {paren(k)} {signed(b)} = {value}$"
        explain = L(f"First {first}. Then {second}.", f"D'abord {first}. Puis {second}.")
        function = f"$f(x) = {poly({2: a, 1: b, 0: c})}$"
        prompt = L(f"If {function}, what is $f'({k})$?", f"Si {function}, combien vaut $f'({k})$ ?")
        return Question(prompt, *pick(rng, value, [a * k * k + b * k + c, 2 * a + b, a * k + b], m), explain)

    name = rng.choice(list(SPECIAL_DERIVATIVES))
    n = rng.randint(2, 9)
    func, right, wrong, rule_en, rule_fr = (s.format(n=n) if isinstance(s, str) else [w.format(n=n) for w in s]
                                            for s in SPECIAL_DERIVATIVES[name])
    explain = L(f"{rule_en} So the answer is ${right}$.", f"{rule_fr} La réponse est donc ${right}$.")
    expression = f"$\\frac{{d}}{{dx}}\\left({func}\\right)$"
    return Question(f"{L('Find', 'Calcule')} {expression}", *pick(rng, right, wrong, m), explain)


@skill("integrals", "Integrals", "College", "Calculus",
       "Antiderivatives and definite integrals of polynomials.")
def integrals(rng):
    powers = sorted(rng.sample(range(0, 4), 2), reverse=True)
    coeffs = {p: (p + 1) * rng.choice([-3, -2, -1, 1, 2, 3]) for p in powers}
    anti = {p + 1: Fraction(c, p + 1) for p, c in coeffs.items()}
    body = poly(coeffs)

    def evaluate(cs, x):
        return sum(Fraction(c) * Fraction(x) ** p for p, c in cs.items())

    if rng.random() < 0.5:
        wrong = [
            {p + 1: c for p, c in coeffs.items()},
            {p: Fraction(c, p + 1) for p, c in coeffs.items()},
            {p - 1: c * p for p, c in coeffs.items() if p},
            {p: -c for p, c in anti.items()},
        ]
        result = f"${poly(anti)} + C$"
        explain = L(
            f"Raise each power by one, divide by the new power, then add the constant $C$: {result}.",
            f"Augmente chaque exposant de un, divise par le nouvel exposant, puis ajoute la constante $C$ : {result}.",
        )
        with_c = lambda cs: m(f"{poly(cs)} + C")
        prompt = f"{L('Find', 'Calcule')} $\\int \\left({body}\\right) dx$"
        return Question(prompt, *pick(rng, anti, wrong, with_c), explain)

    lo, hi = sorted(rng.sample(range(-1, 4), 2))
    top, bottom = evaluate(anti, hi), evaluate(anti, lo)
    value = top - bottom
    shown = f"\\left({frac(bottom)}\\right)" if bottom < 0 else frac(bottom)
    primitive = f"$F(x) = {poly(anti)}$"
    work = f"$F({hi}) - F({lo}) = {frac(top)} - {shown} = {frac(value)}$"
    explain = L(f"An antiderivative is {primitive}. Then {work}.", f"Une primitive est {primitive}. Alors {work}.")
    forgot = {p + 1: c for p, c in coeffs.items()}
    wrong = [top + bottom, evaluate(coeffs, hi) - evaluate(coeffs, lo), evaluate(forgot, hi) - evaluate(forgot, lo), -value]
    prompt = f"{L('Evaluate', 'Calcule')} $\\int_{{{lo}}}^{{{hi}}} \\left({body}\\right) dx$"
    return Question(prompt, *pick(rng, value, wrong, mf), explain)


def matrix(rows):
    """Write a small matrix in LaTeX."""
    body = " \\\\ ".join(" & ".join(str(v) for v in row) for row in rows)
    return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"


@skill("matrices", "Matrices", "College", "Linear Algebra",
       "Determinants, matrix times vector and entries of a matrix product.")
def matrices(rng):
    kind = rng.randrange(3)
    draw = lambda: rng.randint(-5, 6)
    a, b, c, d = draw(), draw(), draw(), draw()
    if kind == 0:
        det = a * d - b * c
        work = f"${paren(a)} \\cdot {paren(d)} - {paren(b)} \\cdot {paren(c)} = {a * d} - {paren(b * c)} = {det}$"
        explain = L(f"For a $2 \\times 2$ matrix the determinant is $ad - bc$: {work}.",
                    f"Pour une matrice $2 \\times 2$, le déterminant est $ad - bc$ : {work}.")
        shown = f"${matrix([[a, b], [c, d]])}$"
        prompt = L(f"What is the determinant of {shown}?", f"Quel est le déterminant de {shown} ?")
        return Question(prompt, *pick(rng, det, [a * d + b * c, b * c - a * d, a * b - c * d], m), explain)

    if kind == 1:
        x, y = draw(), draw()
        r0, r1 = a * x + b * y, c * x + d * y
        vector = lambda p: m(matrix([[p[0]], [p[1]]]))
        wrong = [(a * x + c * y, b * x + d * y), (a * x, d * y), (r1, r0), (r0 + 1, r1), (r0, r1 - 1), (r0 - 1, r1 + 1)]
        top = f"${paren(a)} \\cdot {paren(x)} + {paren(b)} \\cdot {paren(y)} = {r0}$"
        bottom = f"${paren(c)} \\cdot {paren(x)} + {paren(d)} \\cdot {paren(y)} = {r1}$"
        explain = L(f"Multiply each row by the vector and add. Top: {top}. Bottom: {bottom}.",
                    f"Multiplie chaque ligne par le vecteur et additionne. Haut : {top}. Bas : {bottom}.")
        product = f"${matrix([[a, b], [c, d]])}{matrix([[x], [y]])}$"
        prompt = L(f"What is {product}?", f"Combien vaut {product} ?")
        return Question(prompt, *pick(rng, (r0, r1), wrong, vector), explain)

    first = [[a, b], [c, d]]
    second = [[draw(), draw()], [draw(), draw()]]
    i, j = rng.randrange(2), rng.randrange(2)
    value = first[i][0] * second[0][j] + first[i][1] * second[1][j]
    work = f"${paren(first[i][0])} \\cdot {paren(second[0][j])} + {paren(first[i][1])} \\cdot {paren(second[1][j])} = {value}$"
    explain = L(
        f"Take row ${i + 1}$ of $A$ and column ${j + 1}$ of $B$, multiply matching entries and add: {work}.",
        f"Prends la ligne ${i + 1}$ de $A$ et la colonne ${j + 1}$ de $B$, multiplie les coefficients correspondants et additionne : {work}.",
    )
    wrong = [
        first[i][0] * second[j][0] + first[i][1] * second[j][1],
        first[i][j] * second[i][j],
        second[i][0] * first[0][j] + second[i][1] * first[1][j],
    ]
    prompt = L(
        f"Let $A = {matrix(first)}$ and $B = {matrix(second)}$. What is the entry in row ${i + 1}$, column ${j + 1}$ of $AB$?",
        f"Soit $A = {matrix(first)}$ et $B = {matrix(second)}$. Quel est le coefficient en ligne ${i + 1}$, colonne ${j + 1}$ de $AB$ ?",
    )
    return Question(prompt, *pick(rng, value, wrong, m), explain)
