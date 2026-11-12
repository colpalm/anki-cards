#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown-it-py", "pygments"]
# ///
"""Sync the markdown flashcards into Anki via AnkiConnect.

Markdown is the source of truth. Each card is linked to its Anki note by an
`<!-- anki:<note id> -->` comment under its title, so re-running updates notes
in place (keeping review history) rather than duplicating them. Cards without
an ID are matched to existing notes by their Front text, or added as new notes.

    uv run anki_sync.py           # dry run: report what would change
    uv run anki_sync.py --apply   # write to Anki and add IDs to the markdown
"""
import argparse
import difflib
import html
import json
import re
import sys
import urllib.request
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

ROOT = Path(__file__).parent
DECK = "Programming"
MODEL = "Basic"
# Default tags per card file. A card's own **Tags:** line replaces these.
FILE_TAGS = {
    "programming-languages/python-fundamentals.md": "python::fundamentals source::neetcode",
    "programming-languages/python-oop.md": "python::oop source::neetcode",
    "machine-learning/python-data-analysis.md": "python::data-analysis source::python-for-data-analysis",
    "machine-learning/handson-mlp.md": "ml source::handson-mlp",
    "machine-learning/modular-llm-inference-handbook.md": "ml::llm::inference source::modular-handbook",
    "system-design/system-design-interview.md": "system-design source::system-design-interview-xu",
}
ANKI_OWNED_TAGS = {"leech", "marked"}  # added by Anki itself; a sync never removes them
FUZZY_MATCH = 0.9
ID_COMMENT = re.compile(r"<!-- anki:(\d+) -->")
CSS_START, CSS_END = "/* anki-sync:start */", "/* anki-sync:end */"


@dataclass
class Card:
    path: str
    part: int  # index of the card's section when the file is split on "### "
    title: str
    front: str  # rendered HTML
    back: str
    tags: list[str]
    note_id: int | None
    new_id: bool = False  # linked or added this run; needs writing back to the markdown


# --- Rendering ---------------------------------------------------------------

def _highlight(code, lang, _attrs):
    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        return ""  # markdown-it falls back to a plain, escaped <pre><code>
    return f'<pre class="highlight"><code>{highlight(code, lexer, HtmlFormatter(nowrap=True))}</code></pre>'


MD = MarkdownIt("commonmark", {"highlight": _highlight}).enable("table")


def render(markdown: str) -> str:
    # The .md wrapper scopes our CSS to synced cards, leaving other Basic notes untouched.
    return f'<div class="md">{MD.render(markdown.strip()).strip()}</div>'


def css() -> str:
    light, dark = HtmlFormatter(style="default"), HtmlFormatter(style="github-dark")
    night = ".nightMode .md, .night_mode .md"
    return "\n".join([
        ".md { text-align: left; max-width: 42em; margin: 0 auto; }",
        ".md > :first-child { margin-top: 0; }",
        ".md code { font-family: Menlo, Consolas, monospace; }",
        ".md :not(pre) > code { font-size: .85em; padding: .1em .3em; border-radius: 4px; background: rgba(127,127,127,.15); }",
        f".md pre {{ padding: .6em .8em; border-radius: 6px; overflow-x: auto; font-size: .75em; line-height: 1.4; background: {light.style.background_color}; }}",
        f"{night.replace('.md', '.md pre')} {{ background: {dark.style.background_color}; color: #e6edf3; }}",
        *light.get_token_style_defs(".md .highlight"),
        *dark.get_token_style_defs([".nightMode .md .highlight", ".night_mode .md .highlight"]),
    ])


# --- Markdown ----------------------------------------------------------------

def parse_file(rel: str) -> list[Card]:
    parts = re.split(r"(?m)^### ", (ROOT / rel).read_text(encoding="utf-8"))
    cards = []
    for i, section in enumerate(parts[1:], 1):
        title = section.split("\n", 1)[0].strip()
        if "**Front:**" not in section:
            continue  # a divider heading (e.g. "### Chapter 1"), not a card
        card = re.split(r"(?m)^-{3,}\s*$", section)[0]  # anything after the "---" separator isn't the card
        m = re.search(r"\*\*Front:\*\*(.*?)\*\*Back:\*\*(.*?)(?:\*\*Tags:\*\*(.*))?\Z", card, re.S)
        if not m:
            sys.exit(f"{rel}: card '{title}' needs **Front:** and **Back:** sections")
        front, back, tags = m.group(1), m.group(2), (m.group(3) or "").split() or FILE_TAGS[rel].split()
        note_id = ID_COMMENT.search(section)
        cards.append(Card(rel, i, title, render(front), render(back), tags,
                          int(note_id.group(1)) if note_id else None))
    return cards


def write_ids(cards: list[Card]) -> None:
    for rel in sorted({c.path for c in cards if c.new_id}):
        parts = re.split(r"(?m)^### ", (ROOT / rel).read_text(encoding="utf-8"))
        for c in cards:
            if c.path == rel and c.new_id:
                title, _, rest = parts[c.part].partition("\n")
                parts[c.part] = f"{title}\n<!-- anki:{c.note_id} -->\n{rest}"
                c.new_id = False
        (ROOT / rel).write_text("### ".join(parts), encoding="utf-8")


# --- Anki --------------------------------------------------------------------

def anki(action: str, **params):
    request = json.dumps({"action": action, "version": 6, "params": params}).encode()
    try:
        response = json.load(urllib.request.urlopen("http://localhost:8765", request))
    except OSError as e:
        sys.exit(f"Can't reach AnkiConnect on localhost:8765 ({e}). Is Anki open?")
    if response["error"]:
        raise RuntimeError(f"AnkiConnect {action}: {response['error']}")
    return response["result"]


def plain(markup: str) -> str:
    """Text only, for comparing content while ignoring formatting."""
    return re.sub(r"[^a-z0-9]", "", html.unescape(re.sub(r"<[^>]+>", " ", markup)).lower())


def text(markup: str) -> str:
    """Readable text: inline tags vanish (so highlighted code stays intact), block tags become spaces."""
    markup = re.sub(r"</?(span|code|strong|em|b|i|a)\b[^>]*>", "", markup)
    return html.unescape(re.sub(r"<[^>]+>", " ", markup.replace("&nbsp;", " ")))


def word_diff(old: str, new: str) -> list[str]:
    a, b = text(old).split(), text(new).split()
    return [f"      - {' '.join(a[i1:i2])!r}\n      + {' '.join(b[j1:j2])!r}"
            for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes() if op != "equal"]


def link_existing(cards: list[Card], notes: dict[int, dict]) -> list[str]:
    """Match unlinked cards to unclaimed notes by Front text. Returns fuzzy-match notes."""
    claimed = {c.note_id for c in cards}
    unclaimed = {i: plain(n["fields"]["Front"]["value"]) for i, n in notes.items() if i not in claimed}
    fuzzy = []
    for c in (c for c in cards if c.note_id is None):
        key = plain(c.front)
        ratio, best = max(((difflib.SequenceMatcher(None, key, k).ratio(), i) for i, k in unclaimed.items()),
                          default=(0, None))
        if ratio >= FUZZY_MATCH:
            if ratio < 1:
                fuzzy.append(f"  {c.path} :: {c.title} ({ratio:.2f} match)")
            c.note_id, c.new_id = best, True
            del unclaimed[best]
    return fuzzy


def sync_styling(apply: bool) -> bool:
    current = anki("modelStyling", modelName=MODEL)["css"]
    block = f"{CSS_START}\n{css()}\n{CSS_END}"
    if CSS_START in current:
        new = re.sub(re.escape(CSS_START) + ".*?" + re.escape(CSS_END), lambda _: block, current, flags=re.S)
    else:
        new = f"{current.rstrip()}\n\n{block}"
    if apply and new != current:
        anki("updateModelStyling", model={"name": MODEL, "css": new})
    return new != current


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="write changes (default is a dry run)")
    apply = parser.parse_args().apply

    files = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob("*/*.md"))
    if missing := [f for f in files if f not in FILE_TAGS]:
        sys.exit(f"Add default tags to FILE_TAGS in {Path(__file__).name} for: {', '.join(missing)}")
    cards = [c for f in files for c in parse_file(f)]

    deck_ids = anki("findNotes", query=f'"deck:{DECK}" "note:{MODEL}"')
    linked_ids = [c.note_id for c in cards if c.note_id]
    notes = {n["noteId"]: n for n in anki("notesInfo", notes=list({*deck_ids, *linked_ids})) if n}
    if dangling := [c for c in cards if c.note_id and c.note_id not in notes]:
        sys.exit("Linked notes no longer exist in Anki (delete the ID comment to re-add):\n"
                 + "\n".join(f"  {c.path} :: {c.title} (anki:{c.note_id})" for c in dangling))
    fuzzy = link_existing(cards, notes)

    adds, updates, text_changes, tag_changes = [], [], [], Counter()
    for c in cards:
        if c.note_id is None:
            adds.append(c)
            continue
        note = notes[c.note_id]
        old_front, old_back = note["fields"]["Front"]["value"], note["fields"]["Back"]["value"]
        old_tags = note["tags"]
        c.tags = c.tags + [t for t in old_tags if t.lower() in ANKI_OWNED_TAGS]
        fields_changed = (old_front, old_back) != (c.front, c.back)
        tags_changed = {t.lower() for t in old_tags} != {t.lower() for t in c.tags}  # Anki tags ignore case
        if fields_changed or tags_changed:
            updates.append((c, fields_changed, tags_changed))
        if (plain(old_front), plain(old_back)) != (plain(c.front), plain(c.back)):
            text_changes.append(f"  {c.path} :: {c.title}\n"
                                + "\n".join(word_diff(old_front + " " + old_back, c.front + " " + c.back)))
        if tags_changed:
            tag_changes[f"{' '.join(sorted(old_tags)) or '(none)'}  ->  {' '.join(c.tags)}"] += 1
    linked_now = {c.note_id for c in cards}
    orphans = [n for i, n in notes.items() if i not in linked_now]

    print(f"{'APPLYING' if apply else 'DRY RUN'}: {len(cards)} cards, {len(notes)} notes in '{DECK}'\n")
    print(f"Link to existing notes: {sum(c.new_id for c in cards)}")
    if fuzzy:
        print("  Fuzzy Front matches (check these):", *fuzzy, sep="\n")
    print(f"Add new notes: {len(adds)}", *(f"  {c.path} :: {c.title}" for c in adds), sep="\n")
    print(f"Update notes: {len(updates)} "
          f"(fields {sum(u[1] for u in updates)}, tags {sum(u[2] for u in updates)})")
    if text_changes:
        print(f"  Text differs from Anki, not just formatting ({len(text_changes)}):", *text_changes, sep="\n")
    if tag_changes:
        print("  Tag changes:", *(f"    {n:>3}  {k}" for k, n in tag_changes.most_common()), sep="\n")
    if orphans:
        print(f"Anki notes with no markdown card (left alone): {len(orphans)}",
              *(f"  {plain(n['fields']['Front']['value'])[:80]}" for n in orphans), sep="\n")
    styling = sync_styling(apply)
    print(f"Note type styling: {'updated' if styling and apply else 'needs update' if styling else 'up to date'}")

    if not apply:
        print("\nDry run only. Re-run with --apply to write changes.")
        return
    try:
        for c in adds:
            c.note_id = anki("addNote", note={
                "deckName": DECK, "modelName": MODEL, "tags": c.tags,
                "fields": {"Front": c.front, "Back": c.back},
                "options": {"allowDuplicate": False, "duplicateScope": "deck"},
            })
            c.new_id = True
        for c, fields_changed, tags_changed in updates:
            if fields_changed:
                anki("updateNoteFields", note={"id": c.note_id, "fields": {"Front": c.front, "Back": c.back}})
            if tags_changed:
                anki("updateNoteTags", note=c.note_id, tags=c.tags)
    finally:
        write_ids(cards)  # keep links for whatever succeeded, even if a later call failed
    print("\nDone.")


if __name__ == "__main__":
    main()
