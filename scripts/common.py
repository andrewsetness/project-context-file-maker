"""
Context File Maker — Shared CLI configuration and helpers.

Single source of truth for values used by more than one script:
  - OPTIONAL_FIELDS: fields the interviewer treats as skippable (not the same
    as the JSON schemas' `required` lists, which are the minimum fields needed
    to generate a file).
  - reconfigure_console(): best-effort UTF-8 output on Windows.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

#: Fields that are optional during the interview (may be skipped without
#: follow-up). Kept here so generate.py and checklist.py cannot drift apart.
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


def reconfigure_console():
    """Best-effort UTF-8 console output on Windows (CP1252 consoles mangle
    em-dashes and other non-ASCII characters in printed output)."""
    if sys.platform == 'win32':
        try:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except Exception:
            pass
