---
name: interactive-pitch-deck
title: Interactive pitch deck
description: "Build a self-contained, interactive reveal.js pitch deck (HTML) from a story outline: dark and bright hero slides, click-through steppers, phase tabs that dim a diagram, illustrative storyboards, jigsaw roadmaps, and a closing ask. Use when asked for a pitch, proposal or team deck that should be engaging to present, not a static slide list."
---
# Interactive pitch deck

Turns a story outline into one self-contained HTML file that presents well: every slide has a point, most slides **build on click**, and the interactive parts (tabs, steppers, a switch, a timeline) let the presenter and the audience explore instead of read.

This is an atomic skill. It builds a deck. It does not decide what the pitch should argue; bring the outline.

## When to use

- A manager pitch, a team briefing or a proposal that will be presented live.
- The user wants it "engaging", "interactive", "eye-catching" or less wordy.
- Not for a deck that will be read as a document. Use a plain report page instead.

## Inputs

1. **The story.** The problem, the idea, how it works, where it leads, the ask. A one-line headline for each slide is enough.
2. **The facts you may cite.** Every figure, name and claim must come from a source the user or the repository supplied. Collect these before building.
3. **The audience.** A manager wants the ask and the risks. A team wants "how do I work with this". The audience decides what to cut.

## Procedure

1. **Outline one point per slide.** If a slide needs two points, make two slides. Write the headline as a claim ("Agents forget, and what they know is not shared"), not a topic ("Background").
2. **Pick an archetype for each slide** from [slide archetypes](./references/slide-archetypes.md). Alternate dark and light slides so the deck has rhythm. Open with a gradient title and close with the ask.
3. **Copy [assets/starter.html](./assets/starter.html)** to the output path and replace every `REPLACE`. It already has the tokens, the layout, a dark hero slide, phase tabs, a step explorer and an ask slide, all wired.
4. **Make it interactive where it explains something.** Use the patterns in [interaction patterns](./references/interaction-patterns.md): hidden trigger fragments so the arrow key steps through a custom control, and one `bindSteps` helper for click, key and initial state.
5. **Write the copy short.** Aim for a sentence per card and a few words per label. If a slide reads like a paragraph, cut it or split it.
6. **Draw with SVG where a picture beats a sentence.** For a roadmap as a puzzle use [scripts/jigsaw.py](./scripts/jigsaw.py).
7. **Mark honesty on every slide** (see the rules below).
8. **Verify by rendering.** Run [scripts/render_slides.py](./scripts/render_slides.py) for every slide, in its opening state and its final state, and look at each image. See [verification and gotchas](./references/verification-and-gotchas.md).
9. **Save** as `generated_output/<subject>-<kind>-<YYYY-MM-DD>.html` in the knowledge base and open a pull request. Do not commit scratch renders.

## Rules that keep the deck honest

- **No invented numbers.** Use a figure only if a source supplies it. Where you have none, say "not estimated yet" or leave the number out. No cost, time-saved or date claims unless given.
- **Label illustrations.** Any example, story or picture that is made up carries an `illustrative` tag on the slide and says so in the footer. Names of real people may appear only if the user chose them.
- **Separate built from planned.** Show what exists with a solid style and what is a direction with a dashed or faded style. Say "proposal, not built" in the footer of a future slide.
- **Cite the source in every footer** (a file, a memo, a test run). If a claim has no source, cut it.
- **State the limits.** A pitch that names its weak points (an untested piece, a single approver) is more credible than one that does not.
- **Vendor and secondary sources are unverified.** Say so in the appendix or a footer.

## Design in one paragraph

Warm-neutral light ground with a teal accent; a serif for headlines, a sans for body, a mono for labels. Dark slides (`#101C1E`) for problems and asks, a teal gradient for the title, a navy gradient for the big picture, a green tint for safety, a sand tint for risks. A stage colour ramp (teal, blue, violet, indigo) shows progress. Full tokens and rules in [design system](./references/design-system.md).

## What good looks like

- One idea per slide and a headline that is a claim.
- Content starts right under the title, and nothing runs off the bottom.
- The presenter can click through every state with the arrow key alone.
- Every interactive state was rendered and looked at, not assumed.
- The last slide is a short ask, and the deck says what is **not** claimed.

## Files

- [references/design-system.md](./references/design-system.md): tokens, type, backgrounds and component styles.
- [references/slide-archetypes.md](./references/slide-archetypes.md): the slide types and when to use each.
- [references/interaction-patterns.md](./references/interaction-patterns.md): fragments, trigger spans, tabs, steppers, a switch, a timeline.
- [references/verification-and-gotchas.md](./references/verification-and-gotchas.md): the render loop and the mistakes to avoid.
- [assets/starter.html](./assets/starter.html): the working skeleton.
- [scripts/render_slides.py](./scripts/render_slides.py): headless render of any slide in any state.
- [scripts/jigsaw.py](./scripts/jigsaw.py): interlocking-puzzle SVG for roadmap slides.
