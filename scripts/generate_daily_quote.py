#!/usr/bin/env python3
"""
Generate a daily quote from a Google Sheet and save it to api/today.json.
Tracks history in .quote-history.json to avoid repeating recently shown quotes.
"""

from datetime import datetime, timezone, timedelta
import csv
import io
import json
import os
from pathlib import Path
import random
import sys
import urllib.request

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SPREADSHEET_ID = '19hESY6AbY2ZwBph_ndF3zrw9hG__2NLzsbZTMrTlcPk'
DEFAULT_QUOTE_INDEX = 1
DEFAULT_AUTHOR_INDEX = 2
DAYS_BEFORE_REUSE = 30

FALLBACK_QUOTES = [
    {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"quote": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
    {"quote": "It always seems impossible until it's done.", "author": "Nelson Mandela"},
    {"quote": "Keep your face always toward the sunshine - and shadows will fall behind you.", "author": "Walt Whitman"},
    {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"quote": "Start where you are. Use what you have. Do what you can.", "author": "Arthur Ashe"},
]


def load_history(history_path: Path) -> dict:
    if history_path.exists():
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: could not read history file ({e}), resetting", file=sys.stderr)
    return {'quotes': []}


def save_history(history_path: Path, history: dict) -> None:
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def prune_history(history: dict, days: int = DAYS_BEFORE_REUSE) -> dict:
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat().replace('+00:00', 'Z')
    valid = [entry for entry in history.get('quotes', []) if entry.get('selected_on', '') > cutoff]
    return {'quotes': valid}


def clean_text(text: str) -> str:
    cleaned = text.strip()
    if len(cleaned) >= 2 and cleaned[0] == '"' and cleaned[-1] == '"':
        cleaned = cleaned[1:-1].strip()
    return cleaned


def fetch_sheet_quotes(spreadsheet_id: str, quote_idx: int = DEFAULT_QUOTE_INDEX, author_idx: int = DEFAULT_AUTHOR_INDEX) -> list[dict]:
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"
    req = urllib.request.Request(url, headers={'User-Agent': 'TRMNL-Google-Sheet-Quote/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode('utf-8')

    reader = csv.reader(io.StringIO(content))
    rows = list(reader)
    if not rows:
        return []

    quotes = []
    for row in rows[1:]:
        if len(row) > quote_idx and row[quote_idx].strip():
            q = clean_text(row[quote_idx])
            a = clean_text(row[author_idx]) if len(row) > author_idx else ""
            if q:
                quotes.append({"quote": q, "author": a})
    return quotes


def select_quote(quotes: list[dict], history: dict) -> tuple[dict, dict]:
    pruned = prune_history(history, DAYS_BEFORE_REUSE)
    recent_texts = {entry['quote'] for entry in pruned['quotes']}

    available = [q for q in quotes if q['quote'] not in recent_texts]
    if not available:
        print("All quotes recently displayed or history full. Resetting history cycle.")
        pruned['quotes'] = []
        available = quotes

    selected = random.choice(available)
    now_iso = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    pruned['quotes'].append({
        'quote': selected['quote'],
        'author': selected['author'],
        'selected_on': now_iso,
    })
    return selected, pruned


def run(spreadsheet_id: str = None,
        quote_idx: int = None,
        author_idx: int = None,
        output_path: Path = None,
        history_path: Path = None) -> dict:
    sid = spreadsheet_id or os.environ.get('SPREADSHEET_ID', DEFAULT_SPREADSHEET_ID)
    q_idx = quote_idx if quote_idx is not None else int(os.environ.get('QUOTE_INDEX', DEFAULT_QUOTE_INDEX))
    a_idx = author_idx if author_idx is not None else int(os.environ.get('AUTHOR_INDEX', DEFAULT_AUTHOR_INDEX))
    out_file = output_path or (REPO_ROOT / os.environ.get('OUTPUT_FILE', 'api/today.json'))
    hist_file = history_path or (REPO_ROOT / os.environ.get('HISTORY_FILE', '.quote-history.json'))

    quotes = []
    try:
        quotes = fetch_sheet_quotes(sid, q_idx, a_idx)
        print(f"Fetched {len(quotes)} quotes from Google Sheet {sid}")
    except Exception as e:
        print(f"Warning: Failed to fetch from Google Sheet ({e}). Using fallback quotes.", file=sys.stderr)

    if not quotes:
        quotes = list(FALLBACK_QUOTES)

    history = load_history(hist_file)
    selected, updated_history = select_quote(quotes, history)
    save_history(hist_file, updated_history)

    now_iso = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    payload = {
        "quote": selected["quote"],
        "author": selected["author"],
        "updated_at": now_iso
    }

    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Saved daily quote to {out_file}:")
    print(f"  \"{payload['quote']}\" — {payload['author']}")
    return payload


if __name__ == '__main__':
    run()
