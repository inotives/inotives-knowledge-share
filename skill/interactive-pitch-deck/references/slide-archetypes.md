---
title: Slide archetypes
description: The slide types the interactive pitch deck skill uses, what each one is for, and how it behaves on click.
---
# Slide archetypes

Pick one per slide. A good deck uses six to eight of these, not all.

| Archetype | Use it for | Behaviour | Starter has it |
| --- | --- | --- | --- |
| **Gradient title** | Opening slide: promise in one line, a draft tag | Static. Optionally a floating decorative cluster | Yes |
| **Dark problem cards** | The problem, the pain | Cards rise in one by one. Add a small illustration per card for impact, and a single punchline last | Yes |
| **Bright idea hub** | The idea: many people or agents around one shared thing | A hub appears, then the spokes in two groups, then a check badge, then the benefit pills | Pattern only |
| **Flow with human gates** | A process with steps and people at the ends | Boxes build left to right; gate labels in green; a branch for the refusal or exception | Pattern only |
| **Storyboard of mini screens** | A worked example: what a person would see at each step | Five cards, each a small drawn screen (chat, file tree, pull request, checks, approval). Arrows connect them | Pattern only |
| **Phase tabs over a diagram** | Where we are, what is next, the goal | Tabs dim the parts of one diagram that do not belong to the phase. A caption and a "your part" box change | Yes |
| **Step explorer** | "How you will work with it" | A list on the left, detail on the right: you, the agent, a code box, a why line, progress dots | Yes |
| **Time-stamped story** | One request or one week, start to finish | A feed of events appears one at a time. Counters tick up. A row of time buttons jumps to a moment. A caption narrates | Pattern only |
| **Jigsaw roadmap** | The whole picture in stages | Opens showing what is built. Each click fills one stage with colour. Hover shows a tooltip | `scripts/jigsaw.py` |
| **Stage table** | The roadmap as gates | Rows appear one at a time. A tinted first column carries the stage colour | Pattern only |
| **Story-style risks** | Risks that a manager can picture | Six cards, each: title, "what if" scenario, "so we" answer. Red for people and data, amber for platform and process | Pattern only |
| **Safety layers** | Guardrails | Stacked layers with the human gates highlighted, then the principles as pills | Pattern only |
| **Ask and next steps** | The close | One or two big asks, a "later" note, a four-step timeline, a tagline | Yes (ask) |

## Choosing the order

A deck that holds attention usually runs: **title, problem, idea, how it works, one worked example, guardrails, where it leads, the whole picture, roadmap, pilot, risks, ask.** Cut from the middle first. A manager deck can drop the worked examples. A team deck drops the roadmap detail and keeps the stepper.

## Making a sparse slide stronger

1. Replace a bullet list with cards that reveal one at a time.
2. Replace a paragraph with a drawn picture and a one-line caption.
3. Add a counter or a tag that changes as the presenter clicks (for example "10 lessons learned, 4 twice, 0 shared").
4. End with a single bold line that states the point.

## Making a crowded slide lighter

1. Split it into two slides, or turn the second half into a tab.
2. Move qualifications to the footer.
3. Cut every adjective you cannot defend with a source.
