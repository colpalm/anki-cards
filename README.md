# anki-cards
Anki flashcards for technical learning - Python, ML, etc.

Cards are created/reviewed by Claude based on personal notes.

## Syncing to Anki

`anki_sync.py` pushes the markdown cards into Anki. Markdown is the source of truth — make edits here, not in Anki, or the next sync overwrites them.

**One-time setup:** install the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on (Tools → Add-ons → Get Add-ons, code `2055492159`) and restart Anki. Anki must be open when you sync.

```bash
uv run anki_sync.py           # dry run: report adds, updates, and text changes
uv run anki_sync.py --apply   # write to Anki
```

- The sync adds an `<!-- anki:<note id> -->` comment under each card's title, linking the card to its Anki note so it is updated in place and keeps its review history. Never copy or hand-edit these IDs.
- New card files need an entry in `FILE_TAGS` in `anki_sync.py` — the script refuses to run without one.
- Only Basic (Front/Back) cards sync. A `###` heading without `**Front:**` (e.g. a chapter divider) is skipped.
