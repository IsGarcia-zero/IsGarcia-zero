"""Generates the animated SVGs of the profile README by running the real rules.

Nothing is hand-drawn: every frame comes from Conway's Game of Life (B3/S23) or from
elementary rule 30. GitHub does not run scripts in a README, but it does play CSS animations
inside SVG images, so each frame is a <path> that a stepped animation shows in turn.

Usage: python assets/automata.py   (writes banner.svg, rule30.svg and glider.svg next to it)
"""
import random
from pathlib import Path

OUT = Path(__file__).parent
BG, INK, INK_2, INK_3, ACCENT = "#0e0f12", "#f4f4f5", "#a1a1aa", "#8e8e98", "#67e8f9"
GEN_MS = 90          # same pace as the automaton in the CV sidebar
GAP = 0.18           # 1 px gap between 6 px cells, like the CV


# ── Game of Life on an unbounded plane or on a torus ──

def life_step(cells, torus=None):
    counts = {}
    for x, y in cells:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    n = (x + dx, y + dy)
                    if torus:
                        n = (n[0] % torus[0], n[1] % torus[1])
                    counts[n] = counts.get(n, 0) + 1
    return {c for c, n in counts.items() if n == 3 or (n == 2 and c in cells)}


def parse(art):
    return {(x, y) for y, row in enumerate(art.strip().splitlines()) for x, ch in enumerate(row.strip()) if ch == "O"}


def shift(cells, dx, dy):
    return {(x + dx, y + dy) for x, y in cells}


def phases(cells, period):
    out = [cells]
    for _ in range(period - 1):
        out.append(life_step(out[-1]))
    return out


# ── SVG pieces ──

def path(cells, cls, extra=""):
    size = 1 - GAP
    d = "".join(f"M{x} {y}h{size:g}v{size:g}h-{size:g}z" for x, y in sorted(cells))
    return f'<path class="{cls}" d="{d}"{extra}/>'


def frame_style(name, count):
    """Frame i of `count` is visible only during its own generation; each frame starts later."""
    cycle = count * GEN_MS
    rules = [f"@keyframes {name}{{0%{{visibility:visible}}{100 / count:.4f}%{{visibility:hidden}}100%{{visibility:hidden}}}}",
             f".{name}{{visibility:hidden;animation:{name} {cycle}ms steps(1) infinite}}",
             f".{name}.f0{{visibility:visible}}"]
    rules += [f".{name}.f{i}{{animation-delay:{i * GEN_MS}ms}}" for i in range(1, count)]
    return "".join(rules)


def frames(states, name, transform=""):
    paths = "".join(path(s, f"{name} f{i}") for i, s in enumerate(states))
    return f'<g transform="{transform}">{paths}</g>' if transform else paths


REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(width, height, cell, body, style, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img" aria-label="{label}"><style>{style}{REDUCED}</style>'
            f'<clipPath id="r"><rect width="{width}" height="{height}" rx="14"/></clipPath>'
            f'<rect width="{width}" height="{height}" rx="14" fill="{BG}"/>'
            f'<g clip-path="url(#r)"><g transform="scale({cell})" fill="{ACCENT}">{body}</g></g></svg>')


# ── Banner: two fleets of lightweight spaceships (c/2) around the name, and a pulsar ──

LWSS = parse("""
.O..O
O....
O...O
OOOO.
""")
PULSAR = parse("""
..OOO...OOO..
.............
O....O.O....O
O....O.O....O
O....O.O....O
..OOO...OOO..
.............
..OOO...OOO..
O....O.O....O
O....O.O....O
O....O.O....O
.............
..OOO...OOO..
""")


def fleet(name, lane_y, xs, width, leftward):
    """Ships in one lane. Each period of 4 generations the group jumps 2 cells, so after
    2·width generations it has crossed the whole banner and the loop closes without a seam."""
    ship = phases(LWSS, 4)
    moved = life_step(ship[-1])
    dx = min(x for x, _ in moved) - min(x for x, _ in ship[0])   # −2: the base pattern flies left
    if not leftward:
        ship = [{(-x, y) for x, y in s} for s in ship]
        dx = -dx
    steps = width // abs(dx)
    duration = steps * 4 * GEN_MS
    # A copy one banner-width to each side fills the gap the fleet leaves while it slides.
    per_phase = [set().union(*[shift(ship[k], x + offset, lane_y) for x in xs for offset in (0, -width, width)])
                 for k in range(4)]
    style = (frame_style(name, 4)
             + f"@keyframes {name}m{{to{{transform:translateX({dx * steps}px)}}}}"
             + f".{name}m{{animation:{name}m {duration}ms steps({steps}) infinite}}")
    return f'<g class="{name}m">{frames(per_phase, name)}</g>', style


def banner():
    cell, width, height = 6, 140, 40
    top, top_style = fleet("a", 2, [3, 22, 38, 61, 80, 97, 121], width, leftward=False)
    bottom, bottom_style = fleet("b", 34, [9, 27, 50, 68, 91, 110, 129], width, leftward=True)
    pulsar = frames(phases(shift(PULSAR, 117, 13), 3), "p")
    clip = f'<clipPath id="c"><rect width="{width}" height="{height}"/></clipPath>'
    body = f'{clip}<g clip-path="url(#c)">{top}{bottom}{pulsar}</g>'
    style = top_style + bottom_style + frame_style("p", 3)
    text = (f'<text x="34" y="120" font-family="Segoe UI, Inter, Helvetica, Arial, sans-serif" font-size="40" '
            f'font-weight="700" fill="{INK}">Eduardo Hernández <tspan fill="{ACCENT}">Vergara</tspan></text>'
            f'<text x="36" y="156" font-family="Consolas, Menlo, monospace" font-size="16" fill="{INK_2}">'
            f'cellular automata · emergence · slime molds · backend by day</text>'
            f'<text x="741" y="182" text-anchor="middle" font-family="Consolas, Menlo, monospace" font-size="11" '
            f'fill="{INK_3}">B3/S23 · pulsar</text>')
    out = svg(width * cell, height * cell, cell, body, style,
              "Eduardo Hernández Vergara — cellular automata, emergence, slime molds; Game of Life banner")
    return out.replace("</svg>", text + "</svg>")


# ── Rule 30 strip: rows wipe in and out, top to bottom ──

def rule30():
    cell, width, rows = 4, 210, 22
    rng = random.Random(30)
    row = [rng.random() < 0.5 for _ in range(width)]
    history = []
    for _ in range(rows):
        history.append({(x, len(history)) for x, alive in enumerate(row) if alive})
        row = [(30 >> (row[x - 1] << 2 | row[x] << 1 | row[(x + 1) % width])) & 1 for x in range(width)]
    step = 3 * GEN_MS
    cycle = 2 * rows * step
    style = (f"@keyframes w{{0%{{opacity:0}}2%{{opacity:1}}48%{{opacity:1}}52%{{opacity:0}}100%{{opacity:0}}}}"
             f".r{{animation:w {cycle}ms linear infinite backwards}}"
             + "".join(f".r{i}{{animation-delay:{i * step}ms}}" for i in range(rows)))
    body = "".join(path(cells, f"r r{i}") for i, cells in enumerate(history))
    return svg(width * cell, rows * cell + 8, cell, f'<g transform="translate(0 1)">{body}</g>', style,
               "Elementary cellular automaton, rule 30")


# ── Glider on a small torus: back where it started after 4·8 generations ──

def glider():
    cell, size = 6, 8
    state = shift(parse(".O.\n..O\nOOO"), 2, 2)
    states = [state]
    for _ in range(4 * size - 1):
        states.append(life_step(states[-1], torus=(size, size)))
    assert life_step(states[-1], torus=(size, size)) == states[0]
    return svg(size * cell, size * cell, cell, frames(states, "g"), frame_style("g", len(states)), "A glider")


if __name__ == "__main__":
    for name, make in (("banner", banner), ("rule30", rule30), ("glider", glider)):
        text = make()
        (OUT / f"{name}.svg").write_text(text, encoding="utf-8")
        print(f"{name}.svg  {len(text) / 1024:.1f} KB")
