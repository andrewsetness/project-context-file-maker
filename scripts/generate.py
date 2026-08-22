#!/usr/bin/env python3
"""
Context File Maker — CLI Generator

Generates context files from JSON answer payloads.

Usage:
    python scripts/generate.py about_me --answers data/about_me.json
    python scripts/generate.py ai_preferences --answers data/prefs.json
    python scripts/generate.py all --about data/about.json --prefs data/prefs.json
    python scripts/generate.py about_me --answers data/about.json --output my_about.md

Options:
    --validate          Accepted for compatibility; schema enforcement is always on
    --json              Emit machine-readable output instead of the rendered file
    --force             Overwrite existing output files without prompting
    -v, --verbose       Print diagnostic detail (unfilled fields, warnings)
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OPTIONAL_FIELDS, PROJECT_ROOT, reconfigure_console
from template_engine import fill_template

TEMPLATES = {
    'about_me': PROJECT_ROOT / 'templates' / 'free' / 'about_me.md',
    'ai_preferences': PROJECT_ROOT / 'templates' / 'free' / 'ai_preferences.md',
}

SCHEMAS = {
    'about_me': PROJECT_ROOT / 'schemas' / 'about_me_answers.schema.json',
    'ai_preferences': PROJECT_ROOT / 'schemas' / 'ai_preferences_answers.schema.json',
}

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_VALIDATION = 2


def load_json(path: Path) -> dict:
    """Load a JSON file, with helpful error on failure."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    if not isinstance(data, dict):
        print(f"Error: {path} must contain a JSON object of answers, "
              f"not {type(data).__name__}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    return data


def _contract_check(answers: dict, schema: dict) -> list:
    """Dependency-free required/type check from the schema JSON. Guarantees
    enforcement even when jsonschema is not installed."""
    problems = []
    props = schema.get('properties', {})
    for field in schema.get('required', []):
        if field not in answers:
            problems.append(f"missing required field '{field}'")
    for field, value in answers.items():
        spec = props.get(field)
        if isinstance(spec, dict) and spec.get('type') == 'string' \
                and not isinstance(value, str):
            problems.append(f"field '{field}' must be string")
    return problems


def validate_answers(template_name: str, answers: dict, verbose: bool = False):
    """Validate answers against the schema. Returns (valid, messages).

    Enforcement is unconditional (per docs/DATA-CONTRACT.md): required fields
    and basic types are always checked; jsonschema adds full validation when
    installed."""
    schema_path = SCHEMAS.get(template_name)
    if not schema_path or not schema_path.exists():
        if verbose:
            print(f"Warning: no schema for '{template_name}' — skipping validation",
                  file=sys.stderr)
        return True, []

    try:
        schema = json.loads(schema_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        # A broken schema is a repo bug — fail closed rather than skipping.
        return False, [f"Invalid schema JSON in {schema_path}: {e}"]

    messages = _contract_check(answers, schema)
    if messages:
        return False, messages

    try:
        import jsonschema
    except ImportError:
        print("Warning: jsonschema not installed — enforced required/type "
              "checks only", file=sys.stderr)
    else:
        try:
            jsonschema.validate(answers, schema)
        except jsonschema.ValidationError as e:
            # A single, readable message rather than a wall of schema internals.
            where = '.'.join(str(p) for p in e.path) or '(root)'
            return False, [f"Field '{where}': {e.message}"]

    # Warn about unknown keys (typos) rather than failing — future fields
    # should be forward-compatible. Independent of jsonschema availability.
    known = set(schema.get('properties', {}).keys())
    unknown = [key for key in answers if key not in known]
    if unknown and verbose:
        print(f"Note: unknown answer fields (possible typos): "
              f"{', '.join(sorted(unknown))}", file=sys.stderr)

    return True, []


def check_missing_optional(template_name: str, answers: dict) -> list:
    """Return a sorted list of optional fields the user did not fill in."""
    return sorted(
        field for field in OPTIONAL_FIELDS.get(template_name, ())
        if not answers.get(field)
    )


def generate(template_name: str, answers: dict, verbose: bool = False):
    """Generate a context file from a template and answers. Returns the result
    string; the caller decides how to present it."""
    if template_name not in TEMPLATES:
        print(f"Error: Unknown template '{template_name}'. "
              f"Available: {list(TEMPLATES.keys())}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    template_path = TEMPLATES[template_name]
    if not template_path.exists():
        print(f"Error: Template not found: {template_path}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    template_str = template_path.read_text(encoding='utf-8')
    result = fill_template(template_str, answers)

    if verbose:
        missing = check_missing_optional(template_name, answers)
        if missing:
            print(f"Note: optional fields not provided: {', '.join(missing)}",
                  file=sys.stderr)

    return result


def confirm_overwrite(path: Path, force: bool) -> bool:
    """Ask before overwriting an existing file unless --force is set."""
    if not path.exists() or force:
        return True
    try:
        answer = input(f"{path} exists. Overwrite? [y/N] ")
    except EOFError:
        return False
    return answer.strip().lower() in ('y', 'yes')


def write_output(path: Path, content: str, force: bool) -> bool:
    """Write content to path, prompting before overwrite. Returns success."""
    if not confirm_overwrite(path, force):
        print(f"Skipped: {path} (already exists)")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print(f"Generated: {path}")
    return True


def main():
    reconfigure_console()

    parser = argparse.ArgumentParser(
        description='Generate AI context files from JSON answer payloads',
        epilog=(
            'Examples:\n'
            '  python scripts/generate.py about_me --answers data/about.json\n'
            '  python scripts/generate.py ai_preferences --answers data/prefs.json \\\n'
            '      --validate -o my_prefs.md\n'
            '  python scripts/generate.py all --about data/about.json \\\n'
            '      --prefs data/prefs.json --outdir out --validate --force\n'
            '\n'
            'All subcommands accept --validate, --json, --force, --verbose.\n'
            'Diagnostics always go to stderr; rendered markdown to stdout.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
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

    for sub in (about_parser, prefs_parser, all_parser):
        sub.add_argument('--validate', action='store_true',
                         help='Accepted for compatibility; schema enforcement '
                              'is always on (docs/DATA-CONTRACT.md)')
        sub.add_argument('--json', action='store_true', dest='as_json',
                         help='Emit machine-readable JSON instead of the rendered file')
        sub.add_argument('--force', '-f', action='store_true',
                         help='Overwrite existing output files without prompting')
        sub.add_argument('--verbose', '-v', action='store_true',
                         help='Print diagnostic detail')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(EXIT_ERROR)

    if args.command == 'all':
        about_data = load_json(args.about)
        prefs_data = load_json(args.prefs)

        # Schema enforcement is unconditional (docs/DATA-CONTRACT.md);
        # --validate is accepted for compatibility and is a no-op.
        about_valid, about_msgs = validate_answers('about_me', about_data, args.verbose)
        prefs_valid, prefs_msgs = validate_answers('ai_preferences', prefs_data, args.verbose)
        if not (about_valid and prefs_valid):
            problems = ([(m, 'about_me') for m in about_msgs]
                        + [(m, 'ai_preferences') for m in prefs_msgs])
            for msg, which in problems:
                print(f"Validation error ({which}): {msg}", file=sys.stderr)
            sys.exit(EXIT_VALIDATION)

        about_out = args.outdir / 'about_me.md'
        prefs_out = args.outdir / 'ai_preferences.md'

        about_result = generate('about_me', about_data, verbose=args.verbose)
        prefs_result = generate('ai_preferences', prefs_data, verbose=args.verbose)

        if args.as_json:
            payload = {
                'files': {
                    'about_me': about_result,
                    'ai_preferences': prefs_result,
                }
            }
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            sys.exit(EXIT_OK)

        ok = write_output(about_out, about_result, args.force)
        ok = write_output(prefs_out, prefs_result, args.force) and ok
        sys.exit(EXIT_OK if ok else EXIT_ERROR)
    elif args.command in ('about_me', 'ai_preferences'):
        data = load_json(args.answers)

        # Schema enforcement is unconditional (docs/DATA-CONTRACT.md).
        valid, msgs = validate_answers(args.command, data, args.verbose)
        if not valid:
            for msg in msgs:
                print(f"Validation error: {msg}", file=sys.stderr)
            sys.exit(EXIT_VALIDATION)

        result = generate(args.command, data, verbose=args.verbose)

        if args.as_json:
            payload = {'file': result, 'name': f'{args.command}.md'}
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(
                    json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
                print(f"Generated: {args.output}")
            else:
                print(json.dumps(payload, indent=2, ensure_ascii=False))
            sys.exit(EXIT_OK)

        if args.output:
            ok = write_output(args.output, result, args.force)
            sys.exit(EXIT_OK if ok else EXIT_ERROR)
        else:
            print(result)
            sys.exit(EXIT_OK)
    else:
        parser.print_help()
        sys.exit(EXIT_ERROR)


if __name__ == '__main__':
    main()
