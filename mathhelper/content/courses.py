"""Thirteen short courses from elementary arithmetic to college linear algebra."""
from dataclasses import dataclass, field, replace

from flask import g, has_app_context
from sqlalchemy import select

from ..extensions import db
from ..i18n import language, polish
from ..models import SavedLesson
from .courses_fr import FR_COURSES


@dataclass
class Example:
    problem: str
    steps: list[str]
    answer: str


@dataclass
class Lesson:
    id: str
    title: str
    minutes: int
    intro: str
    points: list[str]
    example: Example
    mistake: str
    skill: str
    grade: str = ""


@dataclass
class Course:
    id: str
    title: str
    level: str
    tone: str
    glyph: str
    summary: str
    lessons: list[Lesson] = field(default_factory=list)


COURSES = [
    Course("whole-numbers", "Whole Numbers", "Elementary", "blue", "123",
           "Place value and the four operations that everything else is built on.", [
        Lesson("place-value", "Place value", 5,
               r"Every digit has a job that depends on where it sits. In $4{,}372$ the $3$ is not worth three, it is worth three hundred.",
               [r"Reading right to left, the places are ones, tens, hundreds, thousands and so on.",
                r"Each place is worth ten times the place to its right.",
                r"Expanded form shows what every digit is worth: $4{,}372 = 4000 + 300 + 70 + 2$.",
                r"To round, look at the digit one place to the right. Five or more rounds up."],
               Example(r"Round $6{,}748$ to the nearest hundred.",
                       [r"The hundreds digit is $7$, so the answer is $6{,}700$ or $6{,}800$.",
                        r"Look one place to the right, at the tens digit: $4$.",
                        r"$4$ is less than $5$, so round down."],
                       r"$6{,}700$"),
               r"Reading a digit as its own value. The $7$ in $6{,}748$ is worth $700$.",
               "add-subtract"),
        Lesson("add-subtract", "Adding and subtracting", 6,
               r"Adding combines amounts and subtracting finds the difference. Working one place at a time keeps big numbers easy.",
               [r"Line the numbers up by place value before you start.",
                r"Work from the ones place toward the left.",
                r"When a column adds up to $10$ or more, carry the extra ten to the next column.",
                r"When the top digit is too small to subtract, borrow ten from the next column."],
               Example(r"$503 - 267$",
                       [r"The ones need a borrow, but the tens digit is $0$, so borrow from the hundreds first. The $5$ becomes $4$ and the tens become $10$.",
                        r"Now borrow from the tens. They become $9$ and the ones become $13$, so $13 - 7 = 6$.",
                        r"Tens: $9 - 6 = 3$. Hundreds: $4 - 2 = 2$."],
                       r"$236$"),
               r"Taking the smaller digit from the larger in every column, which skips borrowing.",
               "add-subtract"),
        Lesson("multiply-divide", "Multiplying and dividing", 7,
               r"Multiplication is fast repeated addition, and division splits a total into equal groups. Each one undoes the other.",
               [r"$6 \times 4$ means six groups of four, which is $24$.",
                r"Order does not matter when multiplying: $6 \times 4 = 4 \times 6$.",
                r"Division asks how many groups: $24 \div 4 = 6$ because $6 \times 4 = 24$.",
                r"Split bigger numbers into tens and ones to multiply in your head."],
               Example(r"$37 \times 6$",
                       [r"Split $37$ into $30 + 7$.",
                        r"$30 \times 6 = 180$ and $7 \times 6 = 42$.",
                        r"Add the parts: $180 + 42 = 222$."],
                       r"$222$"),
               r"Multiplying only the ones, for example writing $37 \times 6 = 30 + 42$.",
               "multiply-divide"),
    ]),
    Course("fractions-decimals", "Fractions and Decimals", "Elementary", "green", "½",
           "Parts of a whole, written two ways, and how to move between them.", [
        Lesson("fraction-meaning", "What a fraction means", 5,
               r"A fraction describes part of a whole. The bottom number says how many equal pieces there are, and the top says how many you have.",
               [r"In $\frac{3}{8}$ the whole is cut into $8$ equal pieces and you have $3$ of them.",
                r"Multiplying top and bottom by the same number gives an equal fraction: $\frac{1}{2} = \frac{4}{8}$.",
                r"To simplify, divide top and bottom by their greatest common factor.",
                r"When the top is bigger than the bottom, the fraction is more than one whole."],
               Example(r"Simplify $\frac{18}{24}$.",
                       [r"The greatest common factor of $18$ and $24$ is $6$.",
                        r"$18 \div 6 = 3$ and $24 \div 6 = 4$."],
                       r"$\frac{3}{4}$"),
               r"Dividing only the top or only the bottom, which changes the value.",
               "fractions"),
        Lesson("fraction-add", "Adding and subtracting fractions", 7,
               r"You can only add pieces that are the same size. That is why fractions need a common denominator first.",
               [r"Find a common denominator, usually the least common multiple of the bottoms.",
                r"Rewrite each fraction with that denominator.",
                r"Add or subtract the tops and keep the bottom.",
                r"Simplify the answer if you can."],
               Example(r"$\frac{2}{3} + \frac{1}{4}$",
                       [r"The least common multiple of $3$ and $4$ is $12$.",
                        r"$\frac{2}{3} = \frac{8}{12}$ and $\frac{1}{4} = \frac{3}{12}$.",
                        r"$\frac{8}{12} + \frac{3}{12} = \frac{11}{12}$."],
                       r"$\frac{11}{12}$"),
               r"Adding the tops and the bottoms, as in $\frac{2}{3} + \frac{1}{4} = \frac{3}{7}$.",
               "fractions"),
        Lesson("decimals", "Decimals and conversions", 6,
               r"Decimals are fractions with bottoms of $10$, $100$, $1000$ and so on. After the point come tenths, then hundredths, then thousandths.",
               [r"$0.7 = \frac{7}{10}$ and $0.25 = \frac{25}{100} = \frac{1}{4}$.",
                r"To turn a fraction into a decimal, divide the top by the bottom.",
                r"When adding or subtracting decimals, line up the decimal points.",
                r"To turn a decimal into a percent, multiply by $100$: $0.35 = 35\%$."],
               Example(r"Write $\frac{5}{8}$ as a decimal.",
                       [r"A fraction bar means divide, so work out $5 \div 8$.",
                        r"$5.000 \div 8 = 0.625$."],
                       r"$0.625$"),
               r"Lining up the last digits instead of the decimal points, as in $3.4 + 1.25$.",
               "decimals"),
    ]),
    Course("integers-expressions", "Integers and Expressions", "Middle School", "violet", "±",
           "Negative numbers, the order of operations and your first taste of algebra.", [
        Lesson("negative-numbers", "Negative numbers", 6,
               r"Negative numbers sit to the left of zero on the number line. They describe things like temperatures below zero or money owed.",
               [r"Adding a negative moves left: $5 + (-8) = -3$.",
                r"Subtracting a negative is the same as adding: $4 - (-6) = 10$.",
                r"Multiplying or dividing two numbers with the same sign gives a positive answer.",
                r"Different signs give a negative answer: $-3 \times 7 = -21$."],
               Example(r"$-12 - (-5) + 3$",
                       [r"Turn subtracting $-5$ into adding $5$: $-12 + 5 + 3$.",
                        r"$-12 + 5 = -7$.",
                        r"$-7 + 3 = -4$."],
                       r"$-4$"),
               r"Thinking two negatives always make a positive. That rule is for multiplying and dividing, not adding.",
               "integers"),
        Lesson("order-of-operations", "Order of operations", 6,
               r"When an expression has several operations, everyone follows the same order so everyone gets the same answer.",
               [r"Brackets first.",
                r"Then exponents.",
                r"Then multiplication and division, from left to right.",
                r"Then addition and subtraction, from left to right."],
               Example(r"$3 + 4 \times (6 - 1)^2$",
                       [r"Brackets: $6 - 1 = 5$.",
                        r"Exponent: $5^2 = 25$.",
                        r"Multiply: $4 \times 25 = 100$.",
                        r"Add: $3 + 100 = 103$."],
                       r"$103$"),
               r"Always multiplying before dividing. They have equal rank, so go left to right: $12 \div 3 \times 2 = 8$, not $2$.",
               "order-of-operations"),
        Lesson("expressions", "Variables and expressions", 7,
               r"A variable is a letter that stands for a number. You can tidy up expressions by combining like terms.",
               [r"Like terms share the same variable part: $3x$ and $5x$ are like terms, $3x$ and $3x^2$ are not.",
                r"Combine like terms by adding their numbers: $3x + 5x = 8x$.",
                r"The distributive property opens brackets: $4(x + 2) = 4x + 8$.",
                r"To evaluate, swap the variable for its value and follow the order of operations."],
               Example(r"Simplify $2(3x - 4) + 5x + 1$.",
                       [r"Distribute: $6x - 8 + 5x + 1$.",
                        r"Combine the $x$ terms: $6x + 5x = 11x$.",
                        r"Combine the numbers: $-8 + 1 = -7$."],
                       r"$11x - 7$"),
               r"Multiplying only the first term in the bracket, as in $2(3x - 4) = 6x - 4$.",
               "linear-equations"),
    ]),
    Course("ratios-percents", "Ratios and Percents", "Middle School", "amber", "%",
           "Compare amounts, scale recipes and work out discounts with confidence.", [
        Lesson("ratios", "Ratios and rates", 6,
               r"A ratio compares two amounts. A rate is a ratio with different units, like kilometers per hour.",
               [r"The ratio $3:2$ means for every $3$ of one thing there are $2$ of another.",
                r"Ratios simplify like fractions: $12:8 = 3:2$.",
                r"A unit rate tells you the amount for one: $30$ dollars for $5$ tickets is $6$ dollars per ticket.",
                r"To share an amount in a ratio, find the size of one part first."],
               Example(r"Share $45$ in the ratio $4:5$.",
                       [r"There are $4 + 5 = 9$ parts.",
                        r"One part is $45 \div 9 = 5$.",
                        r"The shares are $4 \times 5 = 20$ and $5 \times 5 = 25$."],
                       r"$20$ and $25$"),
               r"Dividing the total by one side of the ratio instead of by the total number of parts.",
               "ratios"),
        Lesson("proportions", "Proportions", 6,
               r"A proportion says two ratios are equal. If you know three of the four numbers, you can always find the fourth.",
               [r"$\frac{a}{b} = \frac{c}{d}$ is a proportion.",
                r"Cross multiply to solve: $a \times d = b \times c$.",
                r"Or scale: see what one part was multiplied by, then do the same to the other part.",
                r"Check that your answer keeps the same relationship."],
               Example(r"Solve $\frac{3}{5} = \frac{x}{35}$.",
                       [r"The bottom went from $5$ to $35$, which is times $7$.",
                        r"Do the same to the top: $3 \times 7 = 21$."],
                       r"$x = 21$"),
               r"Adding instead of multiplying, as in thinking $\frac{3}{5} = \frac{33}{35}$ because $5 + 30 = 35$.",
               "ratios"),
        Lesson("percents", "Percents and percent change", 7,
               r"Percent means per hundred. It puts different amounts on the same scale so they are easy to compare.",
               [r"To find $p\%$ of a number, multiply by $\frac{p}{100}$.",
                r"To find what percent $a$ is of $b$, work out $\frac{a}{b} \times 100$.",
                r"Percent change is the change divided by the original amount, times $100$.",
                r"A $20\%$ rise followed by a $20\%$ drop does not bring you back to the start."],
               Example(r"A jacket drops from $80$ dollars to $60$ dollars. What is the percent decrease?",
                       [r"The change is $80 - 60 = 20$.",
                        r"Divide by the original price: $\frac{20}{80} = 0.25$.",
                        r"Multiply by $100$ to get $25\%$."],
                       r"A $25\%$ decrease"),
               r"Dividing by the new amount instead of the original one.",
               "percentages"),
    ]),
    Course("measurement", "Shapes and Measurement", "Middle School", "teal", "△",
           "Perimeter, area and circles, with the formulas explained rather than memorized.", [
        Lesson("perimeter", "Perimeter", 5,
               r"Perimeter is the total distance around the outside of a shape. Picture walking along every edge.",
               [r"Add up the lengths of all the sides.",
                r"Rectangle: $P = 2(l + w)$.",
                r"Square: $P = 4s$.",
                r"Perimeter is a length, so it uses units like cm or m."],
               Example(r"A rectangle is $9$ m long and $4$ m wide. Find its perimeter.",
                       [r"Use $P = 2(l + w)$.",
                        r"$2 \times (9 + 4) = 2 \times 13 = 26$."],
                       r"$26$ m"),
               r"Adding only two sides. A rectangle has four.",
               "area-perimeter"),
        Lesson("area", "Area", 6,
               r"Area measures the space inside a flat shape, counted in unit squares.",
               [r"Rectangle: $A = l \times w$.",
                r"Triangle: $A = \frac{1}{2} \times b \times h$, where $h$ is the height straight up from the base.",
                r"Parallelogram: $A = b \times h$.",
                r"Area uses square units like $\text{cm}^2$."],
               Example(r"Find the area of a triangle with base $10$ cm and height $7$ cm.",
                       [r"Use $A = \frac{1}{2} b h$.",
                        r"$\frac{1}{2} \times 10 \times 7 = 35$."],
                       r"$35 \text{ cm}^2$"),
               r"Using a slanted side as the height. The height must meet the base at a right angle.",
               "area-perimeter"),
        Lesson("circles", "Circles", 6,
               r"Every circle has a center, a radius from the center to the edge, and a diameter straight across that is twice the radius.",
               [r"$d = 2r$.",
                r"Circumference: $C = 2\pi r$.",
                r"Area: $A = \pi r^2$.",
                r"$\pi$ is about $3.14$. Leaving answers in terms of $\pi$ keeps them exact."],
               Example(r"Find the area of a circle with a diameter of $12$ cm.",
                       [r"The radius is half the diameter: $r = 6$.",
                        r"$A = \pi \times 6^2 = 36\pi$."],
                       r"$36\pi \text{ cm}^2 \approx 113.1 \text{ cm}^2$"),
               r"Putting the diameter into $\pi r^2$, which makes the area four times too big.",
               "area-perimeter"),
    ]),
    Course("data-probability", "Data and Probability", "Middle School", "pink", "P",
           "Describe a set of numbers and measure how likely things are.", [
        Lesson("averages", "Mean, median and mode", 6,
               r"An average is one number that describes a whole set of data. There are three common ways to choose it.",
               [r"Mean: add everything and divide by how many values there are.",
                r"Median: sort the values and take the middle one. With an even count, average the two middle values.",
                r"Mode: the value that appears most often.",
                r"Range: the largest value minus the smallest. It measures spread, not center."],
               Example(r"Find the mean and median of $4, 9, 2, 7, 8$.",
                       [r"Mean: $4 + 9 + 2 + 7 + 8 = 30$ and $30 \div 5 = 6$.",
                        r"Median: sorted, the values are $2, 4, 7, 8, 9$ and the middle one is $7$."],
                       r"Mean $6$, median $7$"),
               r"Picking the middle value before sorting the list.",
               "statistics"),
        Lesson("basic-probability", "Basic probability", 6,
               r"Probability measures how likely something is, from $0$ for impossible to $1$ for certain.",
               [r"$P(\text{event}) = \frac{\text{outcomes that count}}{\text{all equally likely outcomes}}$.",
                r"Probabilities can be written as fractions, decimals or percents.",
                r"The chance something does not happen is $1 - P(\text{event})$.",
                r"Listing every outcome in a table stops you from missing any."],
               Example(r"A bag has $3$ red and $5$ blue marbles. What is the chance of picking red?",
                       [r"There are $3 + 5 = 8$ marbles in total.",
                        r"$3$ of them are red."],
                       r"$\frac{3}{8}$"),
               r"Comparing red to blue instead of red to the total, which gives $\frac{3}{5}$.",
               "probability"),
        Lesson("combined-events", "Combining events", 7,
               r"When two things happen together, like rolling two dice, count the pairs of outcomes or multiply the chances.",
               [r"Two dice have $6 \times 6 = 36$ equally likely pairs.",
                r"For independent events, $P(A \text{ and } B) = P(A) \times P(B)$.",
                r"Flipping a coin $n$ times gives $2^n$ equally likely results.",
                r"Exactly $k$ heads in $n$ flips happens in $\binom{n}{k}$ ways."],
               Example(r"What is the probability of rolling a total of $8$ with two dice?",
                       [r"The pairs that make $8$ are $(2,6)$, $(3,5)$, $(4,4)$, $(5,3)$ and $(6,2)$.",
                        r"That is $5$ of the $36$ pairs."],
                       r"$\frac{5}{36}$"),
               r"Treating every total from $2$ to $12$ as equally likely. A total of $7$ is six times more likely than a total of $2$.",
               "probability"),
    ]),
    Course("algebra-1", "Algebra I", "High School", "blue", "x",
           "Solve equations, understand lines and handle two unknowns at once.", [
        Lesson("solving-equations", "Solving linear equations", 7,
               r"Solving an equation means finding the value that makes both sides equal. Whatever you do to one side, do to the other.",
               [r"Undo addition and subtraction first, then multiplication and division.",
                r"Clear brackets with the distributive property.",
                r"Gather the variable terms on one side and the numbers on the other.",
                r"Check by putting your answer back into the original equation."],
               Example(r"Solve $5x - 7 = 2x + 8$.",
                       [r"Subtract $2x$ from both sides: $3x - 7 = 8$.",
                        r"Add $7$ to both sides: $3x = 15$.",
                        r"Divide by $3$: $x = 5$.",
                        r"Check: $5(5) - 7 = 18$ and $2(5) + 8 = 18$."],
                       r"$x = 5$"),
               r"Changing a sign on only one side, for example turning $3x - 7 = 8$ into $3x = 1$.",
               "linear-equations"),
        Lesson("slope-lines", "Slope and lines", 7,
               r"A straight line is described by how steep it is and where it crosses the $y$ axis.",
               [r"Slope is rise over run: $m = \frac{y_2 - y_1}{x_2 - x_1}$.",
                r"A positive slope goes up to the right and a negative slope goes down.",
                r"Slope intercept form is $y = mx + b$, where $b$ is where the line crosses the $y$ axis.",
                r"Parallel lines have the same slope."],
               Example(r"Find the line through $(1, 3)$ and $(4, 9)$.",
                       [r"Slope: $\frac{9 - 3}{4 - 1} = \frac{6}{3} = 2$.",
                        r"Put $(1, 3)$ into $y = 2x + b$: $3 = 2 + b$, so $b = 1$."],
                       r"$y = 2x + 1$"),
               r"Putting the $x$ change on top. Slope is the $y$ change over the $x$ change.",
               "slope"),
        Lesson("systems", "Systems of equations", 8,
               r"A system is two equations that must both be true. Its solution is the point where the two lines cross.",
               [r"Substitution: solve one equation for a variable and put it into the other.",
                r"Elimination: add or subtract the equations so one variable cancels.",
                r"Parallel lines never cross, so that kind of system has no solution.",
                r"Always check your pair in both equations."],
               Example(r"Solve $x + y = 10$ and $x - y = 4$.",
                       [r"Add the equations: $2x = 14$, so $x = 7$.",
                        r"Put $x = 7$ into $x + y = 10$: $y = 3$.",
                        r"Check: $7 - 3 = 4$."],
                       r"$x = 7,\ y = 3$"),
               r"Finding one variable and stopping. The answer needs both $x$ and $y$.",
               "systems"),
    ]),
    Course("algebra-2", "Algebra II", "High School", "violet", "x²",
           "Exponent rules and every way to solve a quadratic.", [
        Lesson("exponent-rules", "Exponent rules", 6,
               r"Exponents are shorthand for repeated multiplication. A few rules let you simplify almost any power.",
               [r"Product rule: $x^a \cdot x^b = x^{a+b}$.",
                r"Quotient rule: $\frac{x^a}{x^b} = x^{a-b}$.",
                r"Power rule: $(x^a)^b = x^{ab}$.",
                r"Zero and negative exponents: $x^0 = 1$ and $x^{-n} = \frac{1}{x^n}$."],
               Example(r"Simplify $\frac{(x^3)^4}{x^5}$.",
                       [r"Power rule on the top: $(x^3)^4 = x^{12}$.",
                        r"Quotient rule: $x^{12 - 5} = x^7$."],
                       r"$x^7$"),
               r"Multiplying the exponents when you multiply powers. $x^2 \cdot x^3$ is $x^5$, not $x^6$.",
               "exponents"),
        Lesson("factoring", "Factoring quadratics", 8,
               r"Factoring rewrites a quadratic as two brackets multiplied together. Once it is factored, solving is quick.",
               [r"For $x^2 + bx + c$, find two numbers that multiply to $c$ and add to $b$.",
                r"Those numbers go in the brackets: $(x + p)(x + q)$.",
                r"Zero product rule: if $AB = 0$, then $A = 0$ or $B = 0$.",
                r"Take out a common factor first if every term shares one."],
               Example(r"Solve $x^2 - x - 12 = 0$.",
                       [r"Two numbers that multiply to $-12$ and add to $-1$ are $-4$ and $3$.",
                        r"Factor: $(x - 4)(x + 3) = 0$.",
                        r"Set each bracket to zero: $x = 4$ or $x = -3$."],
                       r"$x = 4$ or $x = -3$"),
               r"Keeping the sign from the bracket. $x - 4 = 0$ gives $x = 4$, not $x = -4$.",
               "quadratics"),
        Lesson("quadratic-formula", "The quadratic formula", 7,
               r"When a quadratic does not factor nicely, the quadratic formula always works.",
               [r"For $ax^2 + bx + c = 0$: $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.",
                r"The discriminant $b^2 - 4ac$ tells you how many real solutions there are.",
                r"Positive means two, zero means one, and negative means none that are real.",
                r"Put the equation in standard form before reading off $a$, $b$ and $c$."],
               Example(r"Solve $2x^2 + 3x - 2 = 0$.",
                       [r"Here $a = 2$, $b = 3$ and $c = -2$.",
                        r"Discriminant: $3^2 - 4(2)(-2) = 9 + 16 = 25$.",
                        r"$x = \frac{-3 \pm 5}{4}$, so $x = \frac{1}{2}$ or $x = -2$."],
                       r"$x = \frac{1}{2}$ or $x = -2$"),
               r"Dividing only the square root by $2a$ instead of the whole top.",
               "quadratics"),
    ]),
    Course("geometry-trig", "Geometry and Trigonometry", "High School", "teal", "θ",
           "Right triangles, the Pythagorean theorem and the trig ratios.", [
        Lesson("pythagorean", "The Pythagorean theorem", 6,
               r"In any right triangle, the square of the longest side equals the sum of the squares of the other two.",
               [r"$a^2 + b^2 = c^2$, where $c$ is the hypotenuse across from the right angle.",
                r"To find the hypotenuse, add the squares and take the square root.",
                r"To find a shorter side, subtract the squares instead.",
                r"Common whole number triples are $3, 4, 5$ and $5, 12, 13$."],
               Example(r"A $13$ m ladder reaches $12$ m up a wall. How far is its foot from the wall?",
                       [r"The ladder is the hypotenuse, so $c = 13$.",
                        r"$b^2 = 13^2 - 12^2 = 169 - 144 = 25$.",
                        r"$b = \sqrt{25} = 5$."],
                       r"$5$ m"),
               r"Adding the squares when the hypotenuse is already known.",
               "pythagorean"),
        Lesson("soh-cah-toa", "SOH CAH TOA", 7,
               r"Trigonometry links the angles of a right triangle to the ratios of its sides.",
               [r"$\sin\theta = \frac{\text{opposite}}{\text{hypotenuse}}$.",
                r"$\cos\theta = \frac{\text{adjacent}}{\text{hypotenuse}}$.",
                r"$\tan\theta = \frac{\text{opposite}}{\text{adjacent}}$.",
                r"Opposite and adjacent depend on which angle you are looking from."],
               Example(r"A ramp rises $3$ m along a $6$ m slope. What angle does it make with the ground?",
                       [r"Opposite is $3$ and the hypotenuse is $6$, so use sine.",
                        r"$\sin\theta = \frac{3}{6} = \frac{1}{2}$.",
                        r"$\theta = \sin^{-1}\left(\frac{1}{2}\right) = 30^\circ$."],
                       r"$30^\circ$"),
               r"Labeling the sides from the wrong angle. Always start from the angle you care about.",
               "trigonometry"),
        Lesson("special-angles", "Special angles", 6,
               r"A few angles show up so often that their exact trig values are worth knowing by heart.",
               [r"$\sin 30^\circ = \frac{1}{2}$ and $\cos 30^\circ = \frac{\sqrt{3}}{2}$.",
                r"$\sin 45^\circ = \cos 45^\circ = \frac{\sqrt{2}}{2}$.",
                r"$\sin 60^\circ = \frac{\sqrt{3}}{2}$ and $\cos 60^\circ = \frac{1}{2}$.",
                r"On the unit circle, cosine is the $x$ value and sine is the $y$ value."],
               Example(r"Find the exact value of $\tan 60^\circ$.",
                       [r"$\tan\theta = \frac{\sin\theta}{\cos\theta}$.",
                        r"$\frac{\sqrt{3}/2}{1/2} = \sqrt{3}$."],
                       r"$\sqrt{3}$"),
               r"Swapping sine and cosine for $30^\circ$ and $60^\circ$. Sine grows as the angle grows.",
               "trigonometry"),
    ]),
    Course("functions-logs", "Functions and Logarithms", "College", "amber", "log",
           "Function notation, exponential growth and the logarithms that undo it.", [
        Lesson("functions", "Functions", 6,
               r"A function takes an input and gives exactly one output. Writing $f(x)$ is just a name for that rule.",
               [r"$f(3)$ means put $3$ in for $x$.",
                r"The domain is every allowed input and the range is every possible output.",
                r"Composition feeds one function into another: $(f \circ g)(x) = f(g(x))$.",
                r"An inverse function undoes the original: $f^{-1}(f(x)) = x$."],
               Example(r"If $f(x) = 2x + 1$ and $g(x) = x^2$, find $f(g(3))$.",
                       [r"Inside first: $g(3) = 9$.",
                        r"Then $f(9) = 2(9) + 1 = 19$."],
                       r"$19$"),
               r"Working a composition from the outside in. Always evaluate the inner function first.",
               "slope"),
        Lesson("exponential", "Exponential growth", 6,
               r"Exponential change multiplies by the same factor every step, which is why it starts slow and then races ahead.",
               [r"The general form is $y = a \cdot b^x$, where $a$ is the start and $b$ is the growth factor.",
                r"$b > 1$ means growth and $0 < b < 1$ means decay.",
                r"A $5\%$ rise each year is a factor of $1.05$.",
                r"Doubling time is how long it takes to grow by a factor of $2$."],
               Example(r"A population of $200$ doubles every year. How big is it after $4$ years?",
                       [r"The start is $200$ and the factor is $2$.",
                        r"$200 \cdot 2^4 = 200 \cdot 16 = 3200$."],
                       r"$3200$"),
               r"Multiplying by the number of years, as in $200 \times 2 \times 4$.",
               "exponents"),
        Lesson("logarithms", "Logarithms", 8,
               r"A logarithm answers the question of which power you need. $\log_2 8 = 3$ because $2^3 = 8$.",
               [r"$\log_b x = y$ means $b^y = x$.",
                r"Product rule: $\log_b (MN) = \log_b M + \log_b N$.",
                r"Quotient rule: $\log_b \frac{M}{N} = \log_b M - \log_b N$.",
                r"Power rule: $\log_b M^k = k \log_b M$."],
               Example(r"Solve $3^{x} = 81$.",
                       [r"Write $81$ as a power of $3$: $81 = 3^4$.",
                        r"The bases match, so the exponents match: $x = 4$."],
                       r"$x = 4$"),
               r"Treating $\log(M + N)$ like $\log M + \log N$. The product rule only works for multiplication.",
               "logarithms"),
    ]),
    Course("calculus-1", "Calculus I", "College", "rose", "d/dx",
           "Limits, derivatives and what they tell you about change.", [
        Lesson("limits", "Limits", 7,
               r"A limit describes the value a function approaches as the input gets close to a number, even if it never arrives.",
               [r"For polynomials, just plug the number in.",
                r"If plugging in gives $\frac{0}{0}$, factor and cancel, then try again.",
                r"At infinity, compare the highest powers on the top and bottom.",
                r"A limit only exists when the left and right sides agree."],
               Example(r"Find $\lim_{x \to 3} \frac{x^2 - 9}{x - 3}$.",
                       [r"Plugging in gives $\frac{0}{0}$, so factor: $\frac{(x - 3)(x + 3)}{x - 3}$.",
                        r"Cancel $x - 3$ to leave $x + 3$.",
                        r"Plug in: $3 + 3 = 6$."],
                       r"$6$"),
               r"Stopping at $\frac{0}{0}$ and saying the limit does not exist.",
               "limits"),
        Lesson("derivative-rules", "Derivative rules", 8,
               r"The derivative measures how fast a function changes. On a graph it is the slope of the tangent line.",
               [r"Power rule: $\frac{d}{dx} x^n = n x^{n-1}$.",
                r"Constants disappear, and constant multiples stay in front.",
                r"$\frac{d}{dx} \sin x = \cos x$ and $\frac{d}{dx} \cos x = -\sin x$.",
                r"$\frac{d}{dx} e^x = e^x$ and $\frac{d}{dx} \ln x = \frac{1}{x}$."],
               Example(r"Differentiate $f(x) = 4x^3 - 5x + 2$.",
                       [r"$4x^3$ becomes $12x^2$.",
                        r"$-5x$ becomes $-5$.",
                        r"The constant $2$ disappears."],
                       r"$f'(x) = 12x^2 - 5$"),
               r"Lowering the power but forgetting to multiply by it.",
               "derivatives"),
        Lesson("chain-rule", "The chain rule", 8,
               r"The chain rule handles a function inside another function. It turns up almost everywhere in calculus.",
               [r"$\frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x)$.",
                r"Differentiate the outside, keep the inside, then multiply by the derivative of the inside.",
                r"Setting $f'(x) = 0$ finds possible peaks and valleys.",
                r"The tangent line at $x = a$ has slope $f'(a)$."],
               Example(r"Differentiate $(3x + 1)^5$.",
                       [r"Outside: $5(3x + 1)^4$.",
                        r"Derivative of the inside: $3$.",
                        r"Multiply: $15(3x + 1)^4$."],
                       r"$15(3x + 1)^4$"),
               r"Forgetting to multiply by the derivative of the inside.",
               "derivatives"),
    ]),
    Course("integration", "Integration", "College", "indigo", "∫",
           "Antiderivatives, areas under curves and substitution.", [
        Lesson("antiderivatives", "Antiderivatives", 7,
               r"Integration runs differentiation backwards. An antiderivative of $f$ is any function whose derivative is $f$.",
               [r"Power rule: $\int x^n \, dx = \frac{x^{n+1}}{n+1} + C$ when $n \neq -1$.",
                r"The $+ C$ is there because constants vanish when you differentiate.",
                r"$\int \frac{1}{x} \, dx = \ln|x| + C$.",
                r"Check any answer by differentiating it."],
               Example(r"Find $\int (6x^2 + 4x) \, dx$.",
                       [r"$6x^2$ becomes $\frac{6x^3}{3} = 2x^3$.",
                        r"$4x$ becomes $\frac{4x^2}{2} = 2x^2$.",
                        r"Add the constant $C$."],
                       r"$2x^3 + 2x^2 + C$"),
               r"Forgetting to divide by the new power.",
               "integrals"),
        Lesson("definite-integrals", "Definite integrals", 7,
               r"A definite integral adds up a quantity between two limits. For a positive function it is the area under the curve.",
               [r"Fundamental theorem: $\int_a^b f(x) \, dx = F(b) - F(a)$.",
                r"No $+ C$ is needed because it cancels out.",
                r"Area below the $x$ axis counts as negative.",
                r"Swapping the limits flips the sign."],
               Example(r"Evaluate $\int_0^2 3x^2 \, dx$.",
                       [r"An antiderivative is $F(x) = x^3$.",
                        r"$F(2) - F(0) = 8 - 0 = 8$."],
                       r"$8$"),
               r"Working out $F(a) - F(b)$ instead of $F(b) - F(a)$.",
               "integrals"),
        Lesson("substitution", "Substitution", 8,
               r"Substitution is the chain rule in reverse. It turns a messy integral into a simple one by renaming the inside part.",
               [r"Choose $u$ to be the inside function.",
                r"Find $du$ and swap it in.",
                r"Integrate in terms of $u$, then switch back to $x$.",
                r"It works when the derivative of the inside also appears in the integral."],
               Example(r"Find $\int 2x(x^2 + 1)^3 \, dx$.",
                       [r"Let $u = x^2 + 1$, so $du = 2x \, dx$.",
                        r"The integral becomes $\int u^3 \, du = \frac{u^4}{4} + C$.",
                        r"Switch back to $x$."],
                       r"$\frac{(x^2 + 1)^4}{4} + C$"),
               r"Switching to $u$ but leaving some $x$ terms behind.",
               "integrals"),
    ]),
    Course("linear-algebra", "Linear Algebra", "College", "cyan", "[ ]",
           "Vectors, matrix multiplication and determinants.", [
        Lesson("vectors", "Vectors", 6,
               r"A vector has both size and direction. In coordinates it is simply a list of numbers.",
               [r"Add vectors entry by entry: $(1, 2) + (3, 4) = (4, 6)$.",
                r"Multiplying by a number stretches a vector: $3(1, 2) = (3, 6)$.",
                r"Length: $\|(a, b)\| = \sqrt{a^2 + b^2}$.",
                r"Dot product: $(a, b) \cdot (c, d) = ac + bd$. It is zero when the vectors are perpendicular."],
               Example(r"Find the dot product of $(2, -1, 3)$ and $(4, 5, 1)$.",
                       [r"Multiply matching entries: $8$, $-5$ and $3$.",
                        r"Add them: $8 - 5 + 3 = 6$."],
                       r"$6$"),
               r"Multiplying the entries but forgetting to add them up.",
               "matrices"),
        Lesson("matrix-multiplication", "Matrix multiplication", 8,
               r"Multiplying matrices combines the rows of the first with the columns of the second.",
               [r"The entry in row $i$, column $j$ is row $i$ of $A$ dotted with column $j$ of $B$.",
                r"$AB$ only works when $A$ has as many columns as $B$ has rows.",
                r"Order matters: $AB$ is usually not equal to $BA$.",
                r"The identity matrix $I$ leaves any matrix unchanged."],
               Example(r"Multiply $\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}\begin{pmatrix} 5 \\ 6 \end{pmatrix}$.",
                       [r"Top: $1 \cdot 5 + 2 \cdot 6 = 17$.",
                        r"Bottom: $3 \cdot 5 + 4 \cdot 6 = 39$."],
                       r"$\begin{pmatrix} 17 \\ 39 \end{pmatrix}$"),
               r"Multiplying matching entries directly instead of rows by columns.",
               "matrices"),
        Lesson("determinants", "Determinants", 7,
               r"The determinant is a single number that tells you whether a square matrix can be undone.",
               [r"For $\begin{pmatrix} a & b \\ c & d \end{pmatrix}$ the determinant is $ad - bc$.",
                r"If the determinant is $0$, the matrix has no inverse.",
                r"Its size tells you how much the matrix stretches area.",
                r"A negative determinant means the matrix flips orientation."],
               Example(r"Find the determinant of $\begin{pmatrix} 3 & 5 \\ 2 & 4 \end{pmatrix}$.",
                       [r"$ad = 3 \cdot 4 = 12$.",
                        r"$bc = 5 \cdot 2 = 10$.",
                        r"$12 - 10 = 2$."],
                       r"$2$"),
               r"Adding the two diagonal products instead of subtracting them.",
               "matrices"),
    ]),
]

def _french(course):
    """Return a French copy of a course."""
    text = FR_COURSES[course.id]
    fix = lambda value: polish(value, "fr")
    lessons = []
    for item in course.lessons:
        fr = text["lessons"][item.id]
        example = Example(fix(fr["problem"]), [fix(step) for step in fr["steps"]], fix(fr["answer"]))
        lessons.append(replace(item, title=fr["title"], intro=fix(fr["intro"]), points=[fix(point) for point in fr["points"]],
                               example=example, mistake=fix(fr["mistake"])))
    return replace(course, title=text["title"], summary=text["summary"], lessons=lessons)


LOCALIZED = {"en": COURSES, "fr": [_french(course) for course in COURSES]}


TEXT_FIELDS = ("title", "intro", "problem", "answer", "mistake")
LIST_FIELDS = ("points", "steps")


def stored_lessons():
    """Return every lesson the admin wrote or changed, read once per request."""
    if not has_app_context():
        return []
    if "lesson_rows" not in g:
        g.lesson_rows = db.session.scalars(select(SavedLesson).order_by(SavedLesson.id)).all()
    return g.lesson_rows


def forget_lessons():
    """Drop the cached lessons after the admin changes one."""
    g.pop("lesson_rows", None)
    g.pop("course_cache", None)


def lesson_from_row(row, lang):
    """Build a lesson from a stored row, using English wherever the other language is empty."""
    english, local = row.content.get("en", {}), row.content.get(lang, {})
    text = {name: polish(local.get(name) or english.get(name) or "", lang) for name in TEXT_FIELDS}
    lists = {name: [polish(item, lang) for item in local.get(name) or english.get(name) or []] for name in LIST_FIELDS}
    example = Example(text["problem"], lists["steps"], text["answer"])
    return Lesson(row.slug, text["title"], row.minutes, text["intro"], lists["points"], example, text["mistake"], row.skill,
                  row.grade or "")


def _merge(base, rows, lang):
    """Lay the admin's lessons over the built in ones and drop courses left empty."""
    by_course = {}
    for row in rows:
        by_course.setdefault(row.course_id, {})[row.slug] = row
    merged = []
    for course in base:
        mine = dict(by_course.get(course.id, {}))
        lessons = []
        for item in course.lessons:
            row = mine.pop(item.id, None)
            if row is None:
                lessons.append(item)
            elif row.visible:
                lessons.append(lesson_from_row(row, lang))
        lessons += [lesson_from_row(row, lang) for row in mine.values() if row.visible]
        if lessons:
            merged.append(replace(course, lessons=lessons))
    return merged


def courses():
    """Return every course in the language of the current request, with the admin's changes applied."""
    lang = language()
    base = LOCALIZED.get(lang, COURSES)
    rows = stored_lessons()
    if not rows:
        return base
    cache = g.setdefault("course_cache", {})
    if lang not in cache:
        cache[lang] = _merge(base, rows, lang)
    return cache[lang]


def find_course(course_id):
    """Return the course with this id in the current language, or None."""
    return next((course for course in courses() if course.id == course_id), None)


def find_lesson(course, lesson_id):
    """Return the lesson and its position inside a course, or (None, -1)."""
    for index, lesson in enumerate(course.lessons):
        if lesson.id == lesson_id:
            return lesson, index
    return None, -1


def lesson_key(course, lesson):
    """Return the key used to store lesson progress."""
    return f"{course.id}/{lesson.id}"
