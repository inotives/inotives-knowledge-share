#!/usr/bin/env python3
"""Jigsaw-puzzle SVG for 'the whole picture' slides: a grid of interlocking pieces.

Each piece has a stage number. Pieces of stage 1 are drawn immediately; later
stages are returned as <g class="fragment" data-fragment-index="N"> groups so a
click fills one stage at a time. Ghost versions of the later pieces sit under them.

Run `python3 jigsaw.py` for a demo that prints an SVG.
"""
import html, math

R_, W_, STEM = 14, 7, 4          # knob radius, half neck width, neck length

def _edge(p0, p1, n, t):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0); d = ((x1 - x0) / L, (y1 - y0) / L)
    pt = lambda a, b: (x0 + d[0] * a + n[0] * b, y0 + d[1] * a + n[1] * b)
    if t == 0: return f"L{x1:.1f},{y1:.1f} "
    a1, a2 = pt(L / 2 - W_, 0), pt(L / 2 - W_, t * STEM)
    b2, b1 = pt(L / 2 + W_, t * STEM), pt(L / 2 + W_, 0)
    cross = d[0] * (n[1] * t) - d[1] * (n[0] * t)
    sweep = 1 if cross < 0 else 0
    return (f"L{a1[0]:.1f},{a1[1]:.1f} L{a2[0]:.1f},{a2[1]:.1f} "
            f"A{R_},{R_} 0 1 {sweep} {b2[0]:.1f},{b2[1]:.1f} "
            f"L{b1[0]:.1f},{b1[1]:.1f} L{x1:.1f},{y1:.1f} ")

def piece_path(x, y, w, h, top, right, bottom, left):
    """Edge values: 0 flat, +1 knob outward, -1 notch."""
    d = f"M{x},{y} "
    d += _edge((x, y), (x + w, y), (0, -1), top)
    d += _edge((x + w, y), (x + w, y + h), (1, 0), right)
    d += _edge((x + w, y + h), (x, y + h), (0, 1), bottom)
    d += _edge((x, y + h), (x, y), (-1, 0), left)
    return d + "Z"

def _joint(r, c): return 1 if (r + c) % 2 == 0 else -1

def grid(pieces, cols, rows, stage_colors, cell=(288, 116), origin=(8, 8), ghost=True):
    """pieces: list of (name, subtitle, stage). Returns an <svg> string."""
    cw, ch = cell; x0, y0 = origin
    base, frags = [], {}
    for i, (name, sub, st) in enumerate(pieces):
        r, c = divmod(i, cols); x, y = x0 + c * cw, y0 + r * ch
        top = -_joint(r - 1, c) if r > 0 else 0
        bottom = _joint(r, c) if r < rows - 1 else 0
        left = -_joint(r, c - 1) if c > 0 else 0
        right = _joint(r, c) if c < cols - 1 else 0
        d = piece_path(x, y, cw, ch, top, right, bottom, left)
        tx = x + 36
        title = f"<title>{html.escape(name)}: {html.escape(sub)} (stage {st})</title>"
        label = lambda fg, sg: (f'<text x="{tx}" y="{y+52}" font-size="16" font-weight="700" fill="{fg}">{html.escape(name)}</text>'
                                f'<text x="{tx}" y="{y+73}" font-size="12.5" fill="{sg}">{html.escape(sub)}</text>')
        full = (f'<g>{title}<path d="{d}" fill="{stage_colors[st]}" stroke="#FBFCFC" stroke-width="3" '
                f'stroke-linejoin="round"/>{label("#fff", "#E6EDED")}</g>')
        if st == 1:
            base.append(full)
        else:
            if ghost:
                base.append(f'<g>{title}<path d="{d}" fill="#FBFCFC" stroke="#B8C6C8" stroke-width="2" '
                            f'stroke-dasharray="8 6" stroke-linejoin="round"/>{label("#8A9B9E", "#8A9B9E")}</g>')
            frags.setdefault(st, []).append(full)
    inner = "".join(base)
    for st in sorted(frags):
        inner += f'<g class="fragment" data-fragment-index="{st-1}">{"".join(frags[st])}</g>'
    W, H = cols * cw + 2 * x0, rows * ch + 2 * y0
    return f'<svg viewBox="0 0 {W} {H}" style="width:{W}px;height:{H}px" role="img">{inner}</svg>'

if __name__ == "__main__":
    demo = [(f"Piece {i+1}", "what it does", 1 + i // 3) for i in range(12)]
    print(grid(demo, 4, 3, {1: "#0E6E77", 2: "#3E8E96", 3: "#1D7FB8", 4: "#6B4FC4"}))
