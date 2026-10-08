---
title: Pitch deck design system
description: Colour tokens, type, backgrounds and component styles used by the interactive pitch deck skill.
---
# Pitch deck design system

These are the choices behind the decks this skill produces. The starter template already contains all of them as CSS.

## Canvas

A fixed **1280 by 720** slide (`Reveal.initialize({ width: 1280, height: 720, margin: 0 })`). Every slide wraps its content in `.slide-wrap`, which is the full canvas with `44px 56px 26px` padding and a column flex layout. Reveal scales it to the screen, so design at that size.

## Colour tokens

| Token | Value | Use |
| --- | --- | --- |
| `--ground` | `#FBFCFC` | Slide background |
| `--surface`, `--surface-2` | `#FFFFFF`, `#EFF4F4` | Cards, code chips, table headers |
| `--ink`, `--ink-2`, `--ink-3` | `#0F1B1D`, `#3D4F52`, `#6A7C7F` | Headings, body, secondary text |
| `--accent` / `--accent-soft` | `#0E6E77` / `#D9ECEE` | Primary teal and its tint |
| `--good` / `--good-bg` | `#1F7A4D` / `#DDF0E6` | Built, human gate, success |
| `--warn` / `--warn-bg` | `#9A6B12` / `#F6EBD3` | Not yet, caution, illustrative tag |
| `--risk` / `--risk-bg` | `#A33B2E` / `#F6DEDA` | Risk, private, blocked |
| `--s1` to `--s5` | `#0E6E77`, `#3E8E96`, `#1D7FB8`, `#6B4FC4`, `#3B2B80` | The stage ramp: first stage is teal, the last is indigo |

A sixth hue, amber `#B5791A`, marks agents or anything "in motion" when a deck needs a second family next to the teal ramp.

**Rule:** colour carries meaning. Green means done or a person decides, amber means pending or illustrative, red means risk or private, and the ramp means sequence. Do not use a colour for decoration only.

## Type

| Role | Face | Size |
| --- | --- | --- |
| Headline | Source Serif 4, 700 | 40 to 48px, `text-wrap` natural, sentence case |
| Lead sentence | Source Serif 4 | 28px, `--ink-2` |
| Body and cards | IBM Plex Sans | 19 to 22px |
| Labels, eyebrows, code | IBM Plex Mono | 11 to 13px, uppercase, `.14em` letter-spacing for eyebrows |

Body text on a slide should be at least 17px. Footnotes may drop to 13px.

## Backgrounds that give the deck rhythm

| Background | Use |
| --- | --- |
| Teal gradient `135deg #0A4A51, #0E6E77, #1D7FB8` | Title slide |
| Near-black `#101C1E` | The problem, the ask |
| Navy gradient `#0B2540, #12456E, #1D7FB8` | The big picture or destination |
| Bright teal `#0E6E77` | The idea |
| Light green tint `#E4F2EA` or dark green `#0D2B26` | Safety and guardrails |
| Sand `#FBF4E6` | Risks, as friendly stories |
| Pale blue-grey `#EAF3F4` | The pilot or a plan |

Set it per slide with `data-background-color` or `data-background-gradient` on the `<section>`. On a dark slide add the class `dark` (or `bright`) to `.slide-wrap` so headings and the footer turn light. The starter recolours the navigation arrows and progress bar for dark backgrounds.

## Components

- **Eyebrow:** a numbered mono label above the title (`2 · The picture`). The number is the slide's place in the story.
- **Card:** white, 1px border, 14px radius. Variants `.risk`, `.warn`, `.accent` tint the card.
- **Chip and pill:** rounded labels for status. Use sparingly.
- **`.ex-tag`:** an amber "illustrative" or "proposal" tag placed after a title.
- **Footer:** left side is the source and caveat, right side is the slide number.
- **Legend:** a row of colour swatches under a diagram that uses the ramp.

## Motion

- Fragments fade and rise (`fade-up`) over 0.45s.
- Slides use `transition: 'slide'` and backgrounds `fade`.
- A pulsing outline marks "you are here". A gentle float animates a decorative cluster.
- `prefers-reduced-motion` switches all of it off.

## Layout habits

- Content starts directly under the title (`.body { justify-content: flex-start }`). Do not centre vertically, which leaves a gap under the title.
- If a slide is sparse, make the cards bigger and the type larger instead of centring.
- Keep the whole slide inside 720px. The footer sits at the bottom with `margin-top:auto`.
- Tables are for gates and plans, not for decoration. Use a tinted first column to carry colour.
