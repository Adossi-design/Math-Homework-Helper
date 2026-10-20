"""School classes in the French system, what each one is taught, and which lessons belong to it."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Grade:
    id: str
    name: str
    short: str
    stage: str
    methods: str


STAGES = ["Primary school", "Middle school (collège)", "High school (lycée)", "University"]

GRADES = [
    Grade("cm1", "CM1 (Huitième)", "CM1", "Primary school",
          "Whole numbers up to millions, the four operations written in columns, simple fractions as parts of a whole "
          "(halves, thirds, quarters, tenths), decimals with tenths and hundredths, perimeter by adding sides, and "
          "measures (length, mass, time, money). No letters for unknowns, no negative numbers, no equations: solve with "
          "concrete reasoning, drawings, number lines and step by step calculations."),
    Grade("cm2", "CM2 (Septième)", "CM2", "Primary school",
          "Everything from CM1, plus long division, decimals in all four operations, fractions of a quantity, simple "
          "proportionality using tables and the unit value (règle de trois explained with words), area of rectangles "
          "and squares, and perimeter. No letters for unknowns, no negative numbers, no equations: find a missing "
          "number by reasoning or with the inverse operation."),
    Grade("6e", "Sixième", "6e", "Middle school (collège)",
          "Whole numbers and decimals, the order of operations, fractions as quotients, simple fractions of a quantity, "
          "proportionality with tables and the unit value, simple percentages, perimeters and areas of rectangles, "
          "triangles and circles, and angles. No negative numbers yet and no algebraic equations: a missing number is "
          "found with the inverse operation, like $? + 7 = 12$ so $? = 12 - 7$."),
    Grade("5e", "Cinquième", "5e", "Middle school (collège)",
          "Relative (negative) numbers with adding and subtracting, adding fractions with a common denominator, "
          "first literal expressions (replace a letter by a number, simple distributing like $k(a + b)$), "
          "proportionality, percentages, simple probability, and areas and volumes. Equations are only tested by "
          "substituting a value, not solved by moving terms across."),
    Grade("4e", "Quatrième", "4e", "Middle school (collège)",
          "Multiplying and dividing relative numbers and fractions, powers of ten and powers, literal calculation "
          "(distribute, collect like terms), solving first degree equations like $3x - 2 = x + 6$, the cross product "
          "(produit en croix) for proportions, the Pythagorean theorem and its converse, averages, and percentages. "
          "No square of a sum identity yet, no functions notation beyond simple tables."),
    Grade("3e", "Troisième", "3e", "Middle school (collège)",
          "Everything from 4e, plus remarkable identities and factoring with them, product equations like "
          "$(x - 2)(x + 3) = 0$, inequalities of the first degree, linear and affine functions $f(x) = ax + b$, "
          "Thales' theorem, trigonometry in a right triangle (cos, sin, tan), square roots, probability and statistics "
          "(median, range). No discriminant, no derivatives."),
    Grade("2nde", "Seconde", "2nde", "High school (lycée)",
          "Functions and their graphs, variation tables, affine functions and their signs, square and inverse "
          "functions, intervals, solving equations and inequalities with factoring and sign tables, systems of two "
          "linear equations, vectors and coordinates, and statistics. No discriminant formula and no derivatives: "
          "quadratics are handled by factoring or the canonical form."),
    Grade("1ere", "Première", "1ère", "High school (lycée)",
          "Second degree polynomials with the discriminant $\\Delta = b^2 - 4ac$, derivatives and the tangent line, "
          "using the derivative to study variations, arithmetic and geometric sequences, the exponential function, "
          "the trigonometric circle and radians, the dot product, and conditional probability. No limits at infinity "
          "techniques beyond intuition, no logarithm and no integrals."),
    Grade("tle", "Terminale", "Tle", "High school (lycée)",
          "Everything from Première, plus limits, continuity, composite functions and the chain rule, the natural "
          "logarithm, convexity, primitives and integrals, proof by induction, the binomial law, and vectors in space. "
          "Use the methods and vocabulary of the baccalauréat."),
    Grade("univ", "University", "Univ.", "University",
          "University level mathematics: any rigorous method is allowed, including linear algebra, multivariable "
          "calculus, series and formal proofs. Still prefer the clearest method."),
]
GRADE_IDS = [grade.id for grade in GRADES]
BY_ID = {grade.id: grade for grade in GRADES}

# Which class each built in lesson is written for, following the French programme.
LESSON_GRADES = {
    "whole-numbers/place-value": "cm1", "whole-numbers/add-subtract": "cm1", "whole-numbers/multiply-divide": "cm2",
    "fractions-decimals/fraction-meaning": "cm1", "fractions-decimals/fraction-add": "5e",
    "fractions-decimals/decimals": "cm2",
    "integers-expressions/negative-numbers": "5e", "integers-expressions/order-of-operations": "6e",
    "integers-expressions/expressions": "5e",
    "ratios-percents/ratios": "6e", "ratios-percents/proportions": "4e", "ratios-percents/percents": "4e",
    "measurement/perimeter": "cm2", "measurement/area": "6e", "measurement/circles": "6e",
    "data-probability/averages": "4e", "data-probability/basic-probability": "5e",
    "data-probability/combined-events": "3e",
    "algebra-1/solving-equations": "4e", "algebra-1/slope-lines": "3e", "algebra-1/systems": "2nde",
    "algebra-2/exponent-rules": "4e", "algebra-2/factoring": "2nde", "algebra-2/quadratic-formula": "1ere",
    "geometry-trig/pythagorean": "4e", "geometry-trig/soh-cah-toa": "3e", "geometry-trig/special-angles": "1ere",
    "functions-logs/functions": "2nde", "functions-logs/exponential": "1ere", "functions-logs/logarithms": "tle",
    "calculus-1/limits": "tle", "calculus-1/derivative-rules": "1ere", "calculus-1/chain-rule": "tle",
    "integration/antiderivatives": "tle", "integration/definite-integrals": "tle", "integration/substitution": "univ",
    "linear-algebra/vectors": "2nde", "linear-algebra/matrix-multiplication": "univ",
    "linear-algebra/determinants": "univ",
}

# A lesson the admin adds without choosing a class goes to the first class its course is taught in.
COURSE_GRADES = {
    "whole-numbers": "cm1", "fractions-decimals": "cm1", "integers-expressions": "6e", "ratios-percents": "6e",
    "measurement": "cm2", "data-probability": "5e", "algebra-1": "4e", "algebra-2": "4e", "geometry-trig": "4e",
    "functions-logs": "2nde", "calculus-1": "1ere", "integration": "tle", "linear-algebra": "univ",
}


def find_grade(grade_id):
    """Return the class with this id, or None."""
    return BY_ID.get(grade_id or "")


def rank(grade_id):
    """Return the position of a class from CM1 up, with unknown classes last."""
    return GRADE_IDS.index(grade_id) if grade_id in BY_ID else len(GRADES)


def by_stage():
    """Return the classes grouped by stage, in order."""
    return [(stage, [grade for grade in GRADES if grade.stage == stage]) for stage in STAGES]


def lesson_grade(course_id, lesson):
    """Return the class a lesson is written for."""
    return getattr(lesson, "grade", "") or LESSON_GRADES.get(f"{course_id}/{lesson.id}") or COURSE_GRADES.get(course_id, "univ")


def lessons_for(all_courses, grade_id):
    """Return (course, lessons) pairs holding the lessons written for one class, in course order."""
    groups = []
    for course in all_courses:
        lessons = [lesson for lesson in course.lessons if lesson_grade(course.id, lesson) == grade_id]
        if lessons:
            groups.append((course, lessons))
    return groups


def earlier_lessons(all_courses, grade_id):
    """Return (grade, groups) pairs for every class before this one, the closest first, for revision."""
    earlier = [grade for grade in GRADES if rank(grade.id) < rank(grade_id)]
    pairs = [(grade, lessons_for(all_courses, grade.id)) for grade in reversed(earlier)]
    return [(grade, groups) for grade, groups in pairs if groups]


def ai_guidance(grade_id, beyond):
    """Return the prompt text that keeps the AI at the student's class, or nothing when the class is unknown.

    beyond says how the AI should flag a problem that needs ideas from a later class.
    """
    grade = find_grade(grade_id)
    if grade is None:
        return ""
    return (
        f"\nThe student is in {grade.name}, {grade.stage.lower()}, in the French school system. "
        "Solve and explain only with the methods, notation and vocabulary a student in this class is taught. "
        f"What this class knows: {grade.methods}\n"
        "Never use a method from a later class when a method from this class works, even if it is shorter. "
        "If the problem truly needs ideas this class has not learned yet, still solve it as simply as you can, "
        f"explain any new idea in the plainest words, and {beyond}\n"
    )
