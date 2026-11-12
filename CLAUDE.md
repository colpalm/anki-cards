# CLAUDE.md

## Purpose

This repository contains Anki flashcards for building deep, lasting knowledge across technical domains. The goal is mastery - understanding concepts thoroughly enough to apply them fluently in real work, not just recalling facts for a test.

## Card Creation Guidelines

### Philosophy
- Focus on **conceptual understanding** over trivia
- Ask "would knowing this make someone better at the craft?"
- Lead with the concept, use concrete examples to illustrate
- Keep cards atomic - one idea per card
- Avoid overly specific examples that don't generalize
- Be concise and direct. Less is more
- Note: Feel free to recommend cards if you think it is important and related to a current topic even if it is not present in the notes.

### Format
Reference existing cards in the repo for format and style. General structure:

```markdown
### Descriptive Title

**Front:**
The question or prompt

**Back:**
The answer, with code examples if helpful

**Tags:**
topic::tags source::tag

---
```

When the answer is a fixed set meant to be recalled in full (steps, challenges, benefits), end the front with a count naming what's counted, e.g. `(3 challenges)`. Otherwise it's easy to recall part of the set and grade yourself as correct. Skip the count when the bullets only structure an explanation (the two sides of a tradeoff) or the front already names the items.

### Tags

Two orthogonal axes, space-separated. Anki tags are hierarchical via `::`.

- **Topic** — e.g. `ml::llm::inference`. Nest under the broadest domain so tags roll up; add a deeper level only when a topic outgrows a flat list (~20 cards).
- **Source** — one per file, matching the Sources section, e.g. `source::modular-handbook`.

Each file's default tags live in `FILE_TAGS` in `anki_sync.py`. A card's `**Tags:**` line is optional and *replaces* the file defaults for that card.

Skip difficulty and status tags — Anki's scheduler already tracks that.

### Card Types

**Basic (Front/Back)** - Default choice for most concepts
- Good for: definitions, syntax, comparisons, "how do you do X?"

**Cloze Deletion** - For memorizing specific syntax, formulas, or sequences
- Format: "The time complexity of binary search is {{c1::O(log n)}}"
- Good for: exact syntax you need to recall, step-by-step processes, formulas

**Image Occlusion** - For visual/spatial information
- Good for: diagrams, architecture charts, data structure visualizations, anatomical/spatial relationships

Use the simplest card type that works. Basic cards are usually sufficient.

### File Organization

Organize by topic area:
```
anki-cards/
├── programming-languages/
│   ├── python-fundamentals.md
│   └── java-fundamnetals.md
├── ml/
│   └── ml-fundamentals.md
└── ...
```

Each file should include a **Sources** section at the top listing books, courses, or documentation the cards were derived from.

### Syncing to Anki

See the README for how to sync cards to Anki. Read it before adding a card file or touching the `<!-- anki:... -->` ID comments.

- After adding or editing cards, run the dry run (`uv run anki_sync.py`) and show the user the report. Run `--apply` only after the user approves — reviewing the cards is their final read before they reach Anki.
- Only Basic (Front/Back) cards sync. Cloze or Image Occlusion cards have to be added in Anki by hand, so check with the user before writing one.

### What Makes a Good Card

✓ Tests understanding of a concept, not just recall of an example  
✓ Would be useful to someone working in the domain  
✓ Stands alone - doesn't require context from other cards  
✓ Has a clear, unambiguous answer  

✗ Too specific to one narrow example  
✗ Tests something easily looked up and rarely needed  
✗ Combines multiple concepts (split into separate cards)  
✗ Vague question that could have many valid answers