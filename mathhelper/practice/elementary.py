"""Elementary skills: whole numbers, fractions and decimals."""
from decimal import Decimal
from fractions import Fraction
from math import gcd, lcm

from .core import L, Question, frac, local_number, m, mf, pick, skill


def dec(value):
    """Write a Decimal without trailing zeros."""
    return local_number(format(value.normalize(), "f"))


def two_places(value):
    """Write a Decimal with exactly two decimal places."""
    return local_number(f"{value:.2f}")


@skill("add-subtract", "Adding and subtracting", "Elementary", "Arithmetic",
       "Three digit sums and differences with carrying and borrowing.")
def add_subtract(rng):
    a, b = rng.randint(120, 989), rng.randint(110, 899)
    if rng.random() < 0.5:
        c = a + b
        ha, ta, oa = a // 100 * 100, a // 10 % 10 * 10, a % 10
        hb, tb, ob = b // 100 * 100, b // 10 % 10 * 10, b % 10
        explain = L(
            f"Split each number by place value. Hundreds: ${ha} + {hb} = {ha + hb}$. "
            f"Tens: ${ta} + {tb} = {ta + tb}$. Ones: ${oa} + {ob} = {oa + ob}$. "
            f"Add the parts: ${ha + hb} + {ta + tb} + {oa + ob} = {c}$.",
            f"Décompose chaque nombre selon ses rangs. Centaines : ${ha} + {hb} = {ha + hb}$. "
            f"Dizaines : ${ta} + {tb} = {ta + tb}$. Unités : ${oa} + {ob} = {oa + ob}$. "
            f"Additionne le tout : ${ha + hb} + {ta + tb} + {oa + ob} = {c}$.",
        )
        prompt = L(f"What is ${a} + {b}$?", f"Combien font ${a} + {b}$ ?")
        return Question(prompt, *pick(rng, c, [c + 10, c - 10, c + 100, c - 1], m), explain)

    while abs(a - b) < 40:
        b = rng.randint(110, 899)
    a, b = max(a, b), min(a, b)
    c = a - b
    no_borrow = int("".join(str(abs(int(x) - int(y))) for x, y in zip(str(a), str(b))))
    explain = L(
        f"Subtract column by column, borrowing when the top digit is smaller. Check by adding back: ${c} + {b} = {a}$.",
        f"Soustrais colonne par colonne, en empruntant quand le chiffre du haut est plus petit. Vérifie en additionnant : ${c} + {b} = {a}$.",
    )
    prompt = L(f"What is ${a} - {b}$?", f"Combien font ${a} - {b}$ ?")
    return Question(prompt, *pick(rng, c, [no_borrow, c + 10, c - 10, c + 100], m), explain)


@skill("multiply-divide", "Multiplying and dividing", "Elementary", "Arithmetic",
       "Times tables, division facts and two digit multiplication.")
def multiply_divide(rng):
    kind = rng.choice(["times", "divide", "split"])
    if kind == "times":
        a, b = rng.randint(3, 12), rng.randint(3, 12)
        c = a * b
        explain = L(
            f"Start from a fact you know: ${a} \\times {b - 1} = {a * (b - 1)}$. Add one more ${a}$ to get ${c}$.",
            f"Pars d'un résultat que tu connais : ${a} \\times {b - 1} = {a * (b - 1)}$. Ajoute encore ${a}$ pour obtenir ${c}$.",
        )
        prompt = L(f"What is ${a} \\times {b}$?", f"Combien font ${a} \\times {b}$ ?")
        return Question(prompt, *pick(rng, c, [a * (b + 1), a * (b - 1), (a + 1) * b, a + b], m), explain)
    if kind == "divide":
        a, b = rng.randint(3, 12), rng.randint(3, 12)
        c = a * b
        explain = L(
            f"Ask which number times ${a}$ makes ${c}$. Since ${a} \\times {b} = {c}$, the answer is ${b}$.",
            f"Cherche quel nombre multiplié par ${a}$ donne ${c}$. Comme ${a} \\times {b} = {c}$, la réponse est ${b}$.",
        )
        prompt = L(f"What is ${c} \\div {a}$?", f"Combien font ${c} \\div {a}$ ?")
        return Question(prompt, *pick(rng, b, [b + 1, b - 1, b + 2, a], m), explain)
    a, b = rng.choice([n for n in range(12, 99) if n % 10]), rng.randint(3, 9)
    tens, ones, c = a // 10 * 10, a % 10, a * b
    explain = L(
        f"Break ${a}$ into ${tens} + {ones}$. Multiply each part: ${tens} \\times {b} = {tens * b}$ and "
        f"${ones} \\times {b} = {ones * b}$. Add them: ${tens * b} + {ones * b} = {c}$.",
        f"Décompose ${a}$ en ${tens} + {ones}$. Multiplie chaque partie : ${tens} \\times {b} = {tens * b}$ et "
        f"${ones} \\times {b} = {ones * b}$. Additionne : ${tens * b} + {ones * b} = {c}$.",
    )
    prompt = L(f"What is ${a} \\times {b}$?", f"Combien font ${a} \\times {b}$ ?")
    return Question(prompt, *pick(rng, c, [tens * b + ones, c + 10, c - b, c + b], m), explain)


@skill("fractions", "Adding and subtracting fractions", "Elementary", "Fractions",
       "Find a common denominator, combine, then simplify.")
def fractions(rng):
    while True:
        b, d = rng.sample(range(2, 10), 2)
        a, c = rng.randint(1, b - 1), rng.randint(1, d - 1)
        if gcd(a, b) == 1 and gcd(c, d) == 1:
            break
    x, y = Fraction(a, b), Fraction(c, d)
    op = rng.choice("+-")
    if op == "-" and x < y:
        x, y, a, b, c, d = y, x, c, d, a, b
    result = x + y if op == "+" else x - y
    big = lcm(b, d)
    top1, top2 = a * big // b, c * big // d
    top = top1 + top2 if op == "+" else top1 - top2
    work = f"$\\frac{{{top1} {op} {top2}}}{{{big}}} = \\frac{{{top}}}{{{big}}}$"
    reduces = Fraction(top, big).denominator != big
    explain = L(
        f"Use the common denominator ${big}$: ${frac(x)} = \\frac{{{top1}}}{{{big}}}$ and "
        f"${frac(y)} = \\frac{{{top2}}}{{{big}}}$. {'Add' if op == '+' else 'Subtract'} the tops: {work}"
        + (f", which simplifies to ${frac(result)}$" if reduces else "") + ".",
        f"Utilise le dénominateur commun ${big}$ : ${frac(x)} = \\frac{{{top1}}}{{{big}}}$ et "
        f"${frac(y)} = \\frac{{{top2}}}{{{big}}}$. {'Additionne' if op == '+' else 'Soustrais'} les numérateurs : {work}"
        + (f", qui se simplifie en ${frac(result)}$" if reduces else "") + ".",
    )
    wrong = [Fraction(a + c if op == "+" else a - c, b + d), Fraction(top, b * d), result + Fraction(1, big), result * 2]
    prompt = L(f"What is ${frac(x)} {op} {frac(y)}$?", f"Combien font ${frac(x)} {op} {frac(y)}$ ?")
    return Question(prompt, *pick(rng, result, wrong, mf), explain)


@skill("decimals", "Decimals", "Elementary", "Decimals",
       "Turn fractions into decimals and add decimals with the points lined up.")
def decimals(rng):
    if rng.random() < 0.5:
        den = rng.choice([2, 4, 5, 8, 10, 20, 25])
        num = rng.choice([n for n in range(1, den) if gcd(n, den) == 1])
        value = Decimal(num) / Decimal(den)
        wrong = [Decimal(f"0.{num}"), Decimal(f"0.{num}{den}"), value * 10, value / 10]
        explain = L(
            f"A fraction bar means divide. ${num} \\div {den} = {dec(value)}$.",
            f"Une barre de fraction signifie diviser. ${num} \\div {den} = {dec(value)}$.",
        )
        prompt = L(f"Write $\\frac{{{num}}}{{{den}}}$ as a decimal.", f"Écris $\\frac{{{num}}}{{{den}}}$ sous forme décimale.")
        return Question(prompt, *pick(rng, value, wrong, lambda v: m(dec(v))), explain)

    a = Decimal(rng.randint(101, 999)) / 100
    b = Decimal(rng.choice([n for n in range(11, 99) if n % 10])) / 10
    total = a + b
    explain = L(
        f"Line up the decimal points. Writing ${dec(b)}$ as ${two_places(b)}$ keeps the places matched: "
        f"${two_places(a)} + {two_places(b)} = {two_places(total)}$.",
        f"Aligne les virgules. Écrire ${dec(b)}$ sous la forme ${two_places(b)}$ garde les rangs alignés : "
        f"${two_places(a)} + {two_places(b)} = {two_places(total)}$.",
    )
    wrong = [a + b / 10, total + Decimal("0.1"), total - 1, total + 1]
    prompt = L(f"What is ${dec(a)} + {dec(b)}$?", f"Combien font ${dec(a)} + {dec(b)}$ ?")
    return Question(prompt, *pick(rng, total, wrong, lambda v: m(dec(v))), explain)
