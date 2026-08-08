#!/usr/bin/env python3
"""
Context File Maker — Interview Checklist

Renders a compact, checkable interview checklist from the question banks, and
optionally verifies which fields are still missing given a partial answers
file. Designed to be used by the interviewer (agent or human) to track
progress without re-reading the full question bank.

Usage:
    python scripts/checklist.py                    # Full free-tier checklist
    python scripts/checklist.py about_me           # about_me checklist only
    python scripts/checklist.py ai_preferences     # ai_preferences only
    python scripts/checklist.py --answers data/partial.json   # show missing
"""

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _reconfigure_console():
    """Best-effort UTF-8 console output on Windows (CP1252 consoles mangle
    em-dashes and other non-ASCII characters in printed output)."""
    if sys.platform == 'win32':
        try:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except Exception:
            pass

QUESTION_BANKS = {
    'about_me': PROJECT_ROOT / 'docs' / 'questionnaires' / 'about_me_questions.md',
    'ai_preferences': PROJECT_ROOT / 'docs' / 'questionnaires' / 'ai_preferences_questions.md',
}

# Fields the agent treats as optional during the interview.
OPTIONAL_FIELDS = {
    'about_me': {
        'preferred_name', 'ai_pain_points', 'favorite_tools', 'tools_avoid',
        'hobbies', 'fun_fact',
    },
    'ai_preferences': {
        'stack_preferences', 'no_touch_files', 'pet_peeves',
        'past_frustrations', 'must_haves', 'never_do',
    },
}


def parse_question_bank(path: Path) -> list:
    """Parse a question bank markdown table into [(field, question, ...)]."""
    questions = []
    content = path.read_text(encoding='utf-8')
    for line in content.split('\n'):
        # | # | Field | Primary Question | ... |
        match = re.match(r'\|\s*\d+\s*\|\s*(\w+)\s*\|\s*([^|]+?)\s*\|', line)
        if match:
            questions.append((match.group(1), match.group(2)))
    return questions


def render_checklist(name: str, answers: dict = None) -> None:
    bank = QUESTION_BANKS.get(name)
    if not bank or not bank.exists():
        print(f"Error: question bank not found: {bank}", file=sys.stderr)
        sys.exit(1)

    questions = parse_question_bank(bank)
    if not questions:
        print(f"Error: no questions parsed from {bank}", file=sys.stderr)
        sys.exit(1)

    optional = OPTIONAL_FIELDS.get(name, set())
    print(f"\n{name} — interview checklist ({len(questions)} questions)\n")

    for i, (field, question) in enumerate(questions, 1):
        if answers is not None:
            has_value = answers.get(field)
            if has_value and str(has_value).strip():
                marker = '[x]'
            else:
                marker = '[ ]'
        else:
            marker = '[ ]'

        opt = ''
        if field in optional and '(optional)' not in question.lower():
            opt = ' (optional)'
        print(f"{marker} {i:>2}. {question}{opt}")

    if answers is not None:
        missing = [
            (f, q) for f, q in questions
            if f not in optional and not (answers.get(f) and str(answers.get(f)).strip())
        ]
        if missing:
            print(f"\nMissing required fields ({len(missing)}):")
            for field, question in missing:
                print(f"  - {field}: {question}")
        else:
            print("\nAll required fields covered.")

    print()


def main():
    _reconfigure_console()

    parser = argparse.ArgumentParser(description='Render an interview checklist')
    parser.add_argument('file', nargs='?', choices=['about_me', 'ai_preferences', 'all'],
                        default='all', help='Which checklist (default: all)')
    parser.add_argument('--answers', type=Path, default=None,
                        help='Partial answers JSON — check off and flag missing fields')
    args = parser.parse_args()

    answers = None
    if args.answers:
        try:
            answers = json.loads(args.answers.read_text(encoding='utf-8'))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    targets = ['about_me', 'ai_preferences'] if args.file == 'all' else [args.file]
    for name in targets:
        render_checklist(name, answers)


if __name__ == '__main__':
    main()
