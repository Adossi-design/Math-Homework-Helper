"""Small SVG figures for geometry lessons, built only from constants written in the chapter files, so the result is safe to show as it is."""
import math
from html import escape

FAR = 2000


class Figure:
    """A drawing made of named points, lines, rays, segments, circles and marks, in a fixed canvas."""

    def __init__(self, width=340, height=210):
        self.width, self.height = width, height
        self.points = {}
        self.under = []
        self.over = []

    def point(self, name, x, y, dx=9, dy=-9):
        """Add a labelled point at pixel coordinates, with its label shifted by (dx, dy)."""
        self.points[name] = (x, y)
        self.over.append(f'<circle class="fig-pt" cx="{x}" cy="{y}" r="3.8"/><text class="fig-label" x="{x + dx}" y="{y + dy}">{escape(name)}</text>')
        return self

    def _ends(self, a, b):
        (x1, y1), (x2, y2) = self.points[a], self.points[b]
        return x1, y1, x2, y2

    def _unit(self, a, b):
        x1, y1, x2, y2 = self._ends(a, b)
        length = math.hypot(x2 - x1, y2 - y1) or 1
        return (x2 - x1) / length, (y2 - y1) / length

    def segment(self, a, b, cls="fig-seg"):
        """Draw the segment between two points."""
        x1, y1, x2, y2 = self._ends(a, b)
        self.under.append(f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
        return self

    def line(self, a, b, cls="fig-line"):
        """Draw the whole line through two points, running off the canvas on both sides."""
        x1, y1 = self.points[a]
        ux, uy = self._unit(a, b)
        self.under.append(f'<line class="{cls}" x1="{x1 - FAR * ux:.1f}" y1="{y1 - FAR * uy:.1f}" x2="{x1 + FAR * ux:.1f}" y2="{y1 + FAR * uy:.1f}"/>')
        return self

    def ray(self, a, b, cls="fig-line"):
        """Draw the half-line that starts at the first point and goes through the second."""
        x1, y1 = self.points[a]
        ux, uy = self._unit(a, b)
        self.under.append(f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x1 + FAR * ux:.1f}" y2="{y1 + FAR * uy:.1f}"/>')
        return self

    def circle(self, center, radius, cls="fig-circle"):
        """Draw a circle around a named point, with the radius in pixels."""
        x, y = self.points[center]
        self.under.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{radius}"/>')
        return self

    def right_angle(self, vertex, a, b, size=12):
        """Mark a right angle at a vertex between the directions of two points."""
        x, y = self.points[vertex]
        ux, uy = self._unit(vertex, a)
        vx, vy = self._unit(vertex, b)
        p1 = (x + size * ux, y + size * uy)
        p2 = (x + size * (ux + vx), y + size * (uy + vy))
        p3 = (x + size * vx, y + size * vy)
        self.under.append(f'<polyline class="fig-mark" points="{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}"/>')
        return self

    def tick(self, a, b, count=1):
        """Mark a segment with small strokes at its middle: equal segments get the same number of strokes."""
        x1, y1, x2, y2 = self._ends(a, b)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ux, uy = self._unit(a, b)
        nx, ny = -uy, ux
        for index in range(count):
            shift = (index - (count - 1) / 2) * 5
            cx, cy = mx + shift * ux, my + shift * uy
            self.under.append(f'<line class="fig-mark" x1="{cx - 5 * nx:.1f}" y1="{cy - 5 * ny:.1f}" x2="{cx + 5 * nx:.1f}" y2="{cy + 5 * ny:.1f}"/>')
        return self

    def arrow_mark(self, a, b, count=1, at=0.5):
        """Mark a line with chevrons pointing along it: parallel lines get the same number of chevrons."""
        x1, y1, x2, y2 = self._ends(a, b)
        mx, my = x1 + (x2 - x1) * at, y1 + (y2 - y1) * at
        ux, uy = self._unit(a, b)
        nx, ny = -uy, ux
        for index in range(count):
            shift = (index - (count - 1) / 2) * 8
            cx, cy = mx + shift * ux, my + shift * uy
            tip = (cx + 4 * ux, cy + 4 * uy)
            left = (cx - 4 * ux + 5 * nx, cy - 4 * uy + 5 * ny)
            right = (cx - 4 * ux - 5 * nx, cy - 4 * uy - 5 * ny)
            self.under.append(f'<polyline class="fig-mark" points="{left[0]:.1f},{left[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} {right[0]:.1f},{right[1]:.1f}"/>')
        return self

    def arc(self, vertex, a, b, radius=28, cls="fig-arc"):
        """Draw the small arc that marks the angle between the directions of two points, around a vertex."""
        x, y = self.points[vertex]
        ux, uy = self._unit(vertex, a)
        vx, vy = self._unit(vertex, b)
        start = (x + radius * ux, y + radius * uy)
        end = (x + radius * vx, y + radius * vy)
        sweep = 1 if ux * vy - uy * vx > 0 else 0
        self.under.append(f'<path class="{cls}" d="M {start[0]:.1f} {start[1]:.1f} A {radius} {radius} 0 0 {sweep} {end[0]:.1f} {end[1]:.1f}"/>')
        return self

    def text(self, x, y, content):
        """Write a short note such as a length on the drawing."""
        self.over.append(f'<text class="fig-note" x="{x}" y="{y}" text-anchor="middle">{escape(content)}</text>')
        return self

    def svg(self):
        """Return the drawing as an inline SVG element, hidden from screen readers because the block carries a text description."""
        body = "".join(self.under + self.over)
        return (f'<svg class="fig" viewBox="0 0 {self.width} {self.height}" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">'
                f'<rect class="fig-bg" x="0" y="0" width="{self.width}" height="{self.height}" rx="12"/>{body}</svg>')


def figure(fig, alt, caption):
    """Return a lesson block that shows a drawing with a text description and a caption."""
    return {"type": "figure", "svg": fig.svg(), "alt": alt, "caption": caption}


class Graph:
    """A graph with two axes, a grid, points and lines, for lessons on proportionality and statistics. It shares the svg() method of Figure."""

    LEFT, RIGHT, TOP, BOTTOM = 46, 16, 14, 40

    def __init__(self, xmax, ymax, xstep, ystep, xlabel="", ylabel="", width=340, height=240):
        self.xmax, self.ymax, self.xstep, self.ystep = xmax, ymax, xstep, ystep
        self.xlabel, self.ylabel = xlabel, ylabel
        self.width, self.height = width, height
        self.under = []
        self.over = []

    def px(self, x):
        """Return the pixel position of an abscissa."""
        return round(self.LEFT + x / self.xmax * (self.width - self.LEFT - self.RIGHT), 1)

    def py(self, y):
        """Return the pixel position of an ordinate."""
        return round(self.height - self.BOTTOM - y / self.ymax * (self.height - self.BOTTOM - self.TOP), 1)

    def line(self, x1, y1, x2, y2, cls="fig-line"):
        """Draw a line segment between two points given in graph units."""
        self.under.append(f'<line class="{cls}" x1="{self.px(x1)}" y1="{self.py(y1)}" x2="{self.px(x2)}" y2="{self.py(y2)}"/>')
        return self

    def point(self, x, y, label=""):
        """Add a point given in graph units, with an optional label."""
        self.over.append(f'<circle class="fig-pt" cx="{self.px(x)}" cy="{self.py(y)}" r="4"/>')
        if label:
            self.over.append(f'<text class="fig-label" x="{self.px(x) + 7}" y="{self.py(y) - 7}">{escape(label)}</text>')
        return self

    def bars(self, values, labels=()):
        """Draw one vertical bar per value, evenly spread along the x axis, for a bar chart."""
        count = len(values)
        slot = (self.width - self.LEFT - self.RIGHT) / count
        for index, value in enumerate(values):
            x = self.LEFT + index * slot + slot * 0.2
            top = self.py(value)
            self.under.append(f'<rect class="fig-bar" x="{x:.1f}" y="{top}" width="{slot * 0.6:.1f}" height="{self.py(0) - top:.1f}" rx="3"/>')
            if labels:
                self.over.append(f'<text class="fig-note" x="{x + slot * 0.3:.1f}" y="{self.height - self.BOTTOM + 16}" text-anchor="middle">{escape(str(labels[index]))}</text>')
        return self

    def sticks(self, values, labels=()):
        """Draw one thin vertical stick per value, evenly spread along the x axis, for a stick diagram."""
        count = len(values)
        slot = (self.width - self.LEFT - self.RIGHT) / count
        for index, value in enumerate(values):
            x = self.LEFT + index * slot + slot / 2
            self.under.append(f'<line class="fig-stick" x1="{x:.1f}" y1="{self.py(0)}" x2="{x:.1f}" y2="{self.py(value)}"/>')
            self.over.append(f'<circle class="fig-pt" cx="{x:.1f}" cy="{self.py(value)}" r="3.5"/>')
            if labels:
                self.over.append(f'<text class="fig-note" x="{x:.1f}" y="{self.height - self.BOTTOM + 16}" text-anchor="middle">{escape(str(labels[index]))}</text>')
        return self

    def svg(self):
        """Return the graph as an inline SVG element, hidden from screen readers because the block carries a text description."""
        frame = []
        categorical = any(("fig-bar" in part or "fig-stick" in part) for part in self.under)
        x = 0
        while not categorical and x <= self.xmax + 1e-9:
            frame.append(f'<line class="fig-grid" x1="{self.px(x)}" y1="{self.py(0)}" x2="{self.px(x)}" y2="{self.py(self.ymax)}"/>')
            frame.append(f'<text class="fig-note" x="{self.px(x)}" y="{self.height - self.BOTTOM + 16}" text-anchor="middle">{x:g}</text>')
            x += self.xstep
        y = 0
        while y <= self.ymax + 1e-9:
            frame.append(f'<line class="fig-grid" x1="{self.px(0)}" y1="{self.py(y)}" x2="{self.px(self.xmax)}" y2="{self.py(y)}"/>')
            frame.append(f'<text class="fig-note" x="{self.LEFT - 6}" y="{self.py(y) + 4}" text-anchor="end">{y:g}</text>')
            y += self.ystep
        frame.append(f'<line class="fig-axis" x1="{self.px(0)}" y1="{self.py(0)}" x2="{self.px(self.xmax)}" y2="{self.py(0)}"/>')
        frame.append(f'<line class="fig-axis" x1="{self.px(0)}" y1="{self.py(0)}" x2="{self.px(0)}" y2="{self.py(self.ymax)}"/>')
        if self.xlabel:
            frame.append(f'<text class="fig-note" x="{(self.px(0) + self.px(self.xmax)) / 2}" y="{self.height - 6}" text-anchor="middle">{escape(self.xlabel)}</text>')
        if self.ylabel:
            frame.append(f'<text class="fig-note" x="12" y="{(self.py(0) + self.py(self.ymax)) / 2}" text-anchor="middle" transform="rotate(-90 12 {(self.py(0) + self.py(self.ymax)) / 2})">{escape(self.ylabel)}</text>')
        body = "".join(frame + self.under + self.over)
        return (f'<svg class="fig" viewBox="0 0 {self.width} {self.height}" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">'
                f'<rect class="fig-bg" x="0" y="0" width="{self.width}" height="{self.height}" rx="12"/>{body}</svg>')
