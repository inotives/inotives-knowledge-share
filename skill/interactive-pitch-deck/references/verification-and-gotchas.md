---
title: Verification and gotchas
description: How to check an interactive pitch deck by rendering every slide in its states, and the mistakes that cost time when building one.
---
# Verification and gotchas

## The render loop

A deck is not done until every slide has been rendered and looked at **in its opening state and its final state**. Interactive decks fail in ways that code review will not show: text off the bottom, a label touching an arrow, a state that never appears.

`scripts/render_slides.py` makes a temporary copy of the deck, switches transitions off so fragments render in their final state, and screenshots chosen slides with headless Chrome.

```
python3 scripts/render_slides.py deck.html /tmp/renders \
  open=n:2,f:-1  full=n:2  tab3=n:3,c:.tab@2  step2=n:4,c:.stp@1
```

| Spec | Meaning |
| --- | --- |
| `n:3` | Slide 3 with every fragment shown (the final state) |
| `f:-1` | No fragments shown (the opening state) |
| `f:2` | Fragments up to index 2 |
| `c:.tab@2` | Then click the third element matching `.tab` |
| `c:.tab@2;.stp@0` | Several clicks, separated by `;` |

Look at each image. Do not tick a slide as fine until you have seen it.

## What to check on every render

1. Nothing runs off the bottom or the right edge. Footer and slide number visible.
2. No text overlaps a shape, an arrow or another label.
3. Contrast is readable on dark slides, including labels at 12 to 13px.
4. The opening state is not empty. It should say something even before the first click.
5. The final state contains the whole message.
6. Titles do not leave one orphan word on a line.
7. Counters and captions in an interactive slide match the state the buttons show.

## Gotchas

**Generated JavaScript and apostrophes.** When a deck is built from a Python script, a possessive such as `manager's` inside a JavaScript string breaks the whole script and every slide goes blank. Check with `node -e "new Function(script)"` on each `<script>` block, or put a backslash in front of the quote in the final HTML.

**Do not run a patch script twice.** Insert-after patches duplicate slides if re-run. Keep a clean backup of the template, restore it, and run the patch once. After patching, count `<section>` tags and list the eyebrows to confirm.

**Renumbering.** After adding or removing slides, renumber the eyebrows and the footer numbers together. A regex that expects a particular tag shape can silently skip later slides. List them afterwards.

**Transitions hide fragments in screenshots.** A fragment mid-transition is half transparent. The render script disables transitions for that reason. If you take your own screenshot, add `*{transition:none !important}`.

**Marker ids in SVG.** Two arrowheads with the same `id` in one page share one definition. Give each diagram its own marker id.

**Text in SVG does not wrap.** Break lines by hand, keep labels short, and give a box more width than the text needs. Check long labels in the render.

**Puzzle pieces need room for the tabs.** Keep the text inset from the knobs. If a label clips, shift it, not the piece.

**A box looks wider on screen than in the markup.** Reveal scales the slide. Judge only the render.

**Fixed height.** The slide is 720px. If you add a row, remove something else or shrink the diagram. Scaling an SVG with `style="width"` is cleaner than shrinking text below 13px.

**Dark slides need class `dark`.** Without it the headline is dark on a dark background.

**Headless Chrome path.** The script uses the macOS default. Set `CHROME` for another install.

## Before you share

- Every illustrative slide has an `illustrative` tag and says so in the footer.
- Every footer names its source.
- No figure appears that a source does not supply.
- The "not claimed" line is on the last slide: no dates, costs or savings unless given.
- The title in `<title>` is two to four words.
- The file is named `<subject>-<kind>-<YYYY-MM-DD>.html` and sits in `generated_output/`.
- Scratch renders and temp copies are deleted.
