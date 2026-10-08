---
title: Interaction patterns
description: "How the interactive pitch deck skill makes slides respond to clicks and the arrow key: fragments, hidden trigger fragments, the bindSteps helper, tabs, a switch, a step explorer and a time-stamped feed."
---
# Interaction patterns

Every interactive control in these decks works three ways, so it is as good for a live presenter as for someone clicking around alone:

1. **Click** a button to jump to a state.
2. **Press the right arrow** to step to the next state.
3. **Opening state** is set on load, so the slide is never blank.

Reveal.js provides step-by-step reveals through *fragments*. The trick is to let a fragment drive a custom control.

## 1. Plain build: cards that appear one by one

Put `class="fragment fade-up"` on each element. Optionally set `data-fragment-index` to fix the order or to reveal several things on the same press (give them the same index).

```html
<div class="pcard fragment fade-up">...</div>
```

For SVG, wrap the shapes in `<g class="fragment" data-fragment-index="2">`.

## 2. Hidden trigger fragments: the arrow key drives a control

A tab bar or stepper is not a fragment, so the arrow key would skip it. Add **one invisible fragment per step after the first**. When the presenter presses the right arrow, Reveal marks the next trigger visible and an event handler moves the control.

```html
<span class="fragment ptrig" data-fragment-index="1" style="position:absolute;opacity:0;pointer-events:none"></span>
<span class="fragment ptrig" data-fragment-index="2" style="position:absolute;opacity:0;pointer-events:none"></span>
```

The number of visible triggers is the step: zero visible means step 0, two visible means step 2.

## 3. The `bindSteps` helper

One function wires all three behaviours. It is already in `assets/starter.html`.

```js
function bindSteps(buttons, trigClass, setFn) {
  buttons.forEach(function (b, i) { b.addEventListener('click', function () { setFn(i); b.blur(); }); });
  function sync(e) { if (e.fragment.classList.contains(trigClass)) setFn(document.querySelectorAll('.' + trigClass + '.visible').length); }
  Reveal.on('fragmentshown', sync); Reveal.on('fragmenthidden', sync);
}
```

Call `bindSteps(buttons, 'ptrig', setPhase); setPhase(0);`. Keep `setFn` idempotent (return early if the step is unchanged).

## 4. Tabs that dim a diagram

Give every diagram group a `data-ph="1 2 3"` listing the phases in which it is lit. `setPhase(i)` toggles a `.dim` class (opacity .22) on groups whose list does not include the phase, marks the active tab, and swaps the caption. One drawing then tells the whole "now, next, goal" story. A later phase can hold a **ghost** row that shows faintly in earlier phases and lights up when selected.

## 5. A switch that turns a picture on

A toggle button flips a class on an `<svg>` (`.on`). CSS shows the connecting lines and the hub only when `.on` is set, and hides the question marks. The caption text changes with it. Bind the `M` key to the same function. This is the strongest single interaction for a "before and after" claim.

## 6. Step explorer

A list of buttons on the left, a detail panel on the right. A `DATA` array holds the title, colour, text for each side and a code or path line for every step. `setStep(i)` writes them into the panel, sets the panel's CSS variable `--c` to the step colour, and fills the progress dots up to `i`. Use this for "how you will work with it".

## 7. Time-stamped feed with counters

Events live in the HTML with data attributes (`data-s` for the step, plus the counter increments they contribute). `setN(n)` shows every event with `data-s <= n`, sums the counters, highlights the time buttons up to `n`, and swaps a narration caption. The last state shows a summary line in colour. Use it for a week, a night or a request from start to finish.

## 8. Hover tooltips

Puzzle pieces and stage cells carry a `<title>` or a hidden `<em>` that shows on hover. They cost nothing and reward exploring.

## Rules

- **Idempotent setters.** Clicking the active step must not flicker.
- **Escape quotes in strings.** An apostrophe in a JS string literal that was generated from Python needs a backslash in front of it (`\'`) in the final HTML. See the gotchas page.
- **Do not depend on hover** for anything a presenter must say. Hover is a bonus.
- **Keep the arrow-key path complete.** Every state must be reachable by the right arrow alone.
- **Never put required information only in an animation.** The final state must contain everything.
- **Reduced motion.** The starter turns animation off for users who ask. Keep it.
