#!/usr/bin/env python3
"""
Context File Maker — CLI Generator

Generates context files from JSON answer payloads.

Usage:
    python scripts/generate.py about_me --answers data/about_me.json
    python scripts/generate.py ai_preferences --answers data/prefs.json
    python scripts/generate.py all --about data/about.json --prefs data/prefs.json
    python scripts/generate.py about_me --answers data/about.json --output my_about.md
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from template_engine import fill_template


PROJECT_ROOT = Path(__file__).resolve().parent.parent

TEMPLATES = {
    'about_me': PROJECT_ROOT / 'templates' / 'free' / 'about_me.md',
    'ai_preferences': PROJECT_ROOT / 'templates' / 'free' / 'ai_preferences.md',
}


def load_json(path: Path) -> dict:
    """Load a JSON file, with helpful error on failure."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {path}: {e}")
        sys.exit(1)


def generate(template_name: str, answers: dict, output_path: Path = None):
    """Generate a context file from a template and answers."""
    if template_name not in TEMPLATES:
        print(f"Error: Unknown template '{template_name}'. Available: {list(TEMPLATES.keys())}")
        sys.exit(1)

    template_path = TEMPLATES[template_name]
    if not template_path.exists():
        print(f"Error: Template not found: {template_path}")
        sys.exit(1)

    template_str = template_path.read_text(encoding='utf-8')
    result = fill_template(template_str, answers)

    if output_path:
        output_path.write_text(result, encoding='utf-8')
        print(f"Generated: {output_path}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(
        description='Generate AI context files from JSON answer payloads'
    )
    subparsers = parser.add_subparsers(dest='command', help='What to generate')

    # about_me command
    about_parser = subparsers.add_parser('about_me', help='Generate about_me.md')
    about_parser.add_argument('--answers', required=True, type=Path,
                              help='JSON file with about_me answers')
    about_parser.add_argument('--output', '-o', type=Path,
                              help='Output file path (default: stdout)')

    # ai_preferences command
    prefs_parser = subparsers.add_parser('ai_preferences', help='Generate ai_preferences.md')
    prefs_parser.add_argument('--answers', required=True, type=Path,
                              help='JSON file with ai_preferences answers')
    prefs_parser.add_argument('--output', '-o', type=Path,
                              help='Output file path (default: stdout)')

    # all command
    all_parser = subparsers.add_parser('all', help='Generate both files')
    all_parser.add_argument('--about', required=True, type=Path,
                            help='JSON file with about_me answers')
    all_parser.add_argument('--prefs', required=True, type=Path,
                            help='JSON file with ai_preferences answers')
    all_parser.add_argument('--outdir', '-d', type=Path, default=Path('.'),
                            help='Output directory (default: current dir)')

    args = parser.parse_args()

    if args.command == 'all':
        about_data = load_json(args.about)
        prefs_data = load_json(args.prefs)

        about_out = args.outdir / 'about_me.md'
        prefs_out = args.outdir / 'ai_preferences.md'

        generate('about_me', about_data, about_out)
        generate('ai_preferences', prefs_data, prefs_out)
    elif args.command == 'about_me':
        data = load_json(args.answers)
        generate('about_me', data, args.output)
    elif args.command == 'ai_preferences':
        data = load_json(args.answers)
        generate('ai_preferences', data, args.output)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
