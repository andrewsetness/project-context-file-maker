"""
Context File Maker — Template Engine

Fills Mustache-style templates with structured answer data from JSON.

Supported syntax:
    {{field}}                  — Replace with data['field'] (string or text)
    {{~field}}                 — Replace with data['field'], or '[not provided]'
                                 if the value is empty/missing
    {{#field}}...{{/field}}    — If data['field'] is truthy, include the block;
                                 otherwise omit it entirely
    {{#any:f1,f2}}...{{/any}}  — Include the block if ANY of the listed fields
                                 has a value; otherwise omit it entirely.

Block tags that sit alone on their own line are removed cleanly so a removed
block never leaves a stray blank line (which would break markdown lists).
Inline (same-line) {{#field}} and {{#any:...}} blocks are also supported.

Known limitations:
    - Nesting two blocks of the SAME name inline (e.g. {{#a}}{{#a}}...{{/a}}
      ...{{/a}}) is not supported; same-name nesting only works when the outer
      block is line-isolated. Different names nest fine.
    - List/tuple values are rendered as comma-separated text.

Usage:
    from template_engine import fill_template
    result = fill_template(template_str, answers_dict)
"""

import re
from typing import Any, Dict, List

# {{#any:f1,f2}} ... {{/any}} — block kept if any listed field has a value.
# Anchored to its own line(s): the open tag starts a line and the close tag
# ends a line, so a removed section leaves no blank line behind.
_ANY_LINE_RE = re.compile(
    r'(?m)^[ \t]*\{\{#any:([\w,]+)\}\}(.*?)\{\{/any\}\}[ \t]*(?:\r?\n|$)',
    re.DOTALL,
)

# {{#field}} ... {{/field}} — block kept if the field has a value.
# Same line-isolated handling for the common case where the block sits on its
# own line(s).
_SECTION_LINE_RE = re.compile(
    r'(?m)^[ \t]*\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}[ \t]*(?:\r?\n|$)',
    re.DOTALL,
)

# Inline conditional blocks ({{#x}}...{{/x}} inside a line).
_SECTION_INLINE_RE = re.compile(r'\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}', re.DOTALL)

# Inline any-sections ({{#any:f1,f2}}...{{/any}} inside a line). The
# line-isolated form is matched first; this catches whatever remains.
_ANY_INLINE_RE = re.compile(r'\{\{#any:([\w,]+)\}\}(.*?)\{\{/any\}\}', re.DOTALL)

_SIMPLE_RE = re.compile(r'\{\{(\w+)\}\}')
_MISSING_RE = re.compile(r'\{\{~(\w+)\}\}')
_ANY_OPEN_RE = re.compile(r'\{\{#any:([\w,]+)\}\}')
_ANY_CLOSE_RE = re.compile(r'\{\{/any\}\}')

NOT_PROVIDED = '[not provided]'


def fill_template(template: str, data: Dict[str, Any]) -> str:
    """
    Fill a Mustache-style template with data.

    Empty/None fields in conditional blocks are omitted entirely.
    Simple fields with empty values render as '' (or '[not provided]'
    when using the {{~field}} form).
    """
    result = _process_any_sections(template, data)
    result = _process_conditionals(result, data)
    result = _replace_missing_fields(result, data)
    result = _replace_simple_fields(result, data)
    result = _clean_whitespace(result)
    return result


def _field_has_value(data: Dict[str, Any], field: str) -> bool:
    """Return True if the field exists, is not None, and is non-empty."""
    value = data.get(field)
    if value is None:
        return False
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) > 0
    return str(value).strip() != ''


def _render_value(value: Any) -> str:
    """Render a data value as text. Lists/tuples become comma-separated
    strings instead of Python repr; None becomes ''."""
    if value is None:
        return ''
    if isinstance(value, (list, tuple)):
        return ', '.join(str(item) for item in value)
    return str(value)


def _strip_one_leading_newline(content: str) -> str:
    """Remove the newline that immediately follows an open block tag when the
    tag sits alone on its line."""
    if content.startswith('\r\n'):
        return content[2:]
    if content.startswith('\n'):
        return content[1:]
    return content


def _process_any_sections(template: str, data: Dict[str, Any]) -> str:
    """Process {{#any:f1,f2}}...{{/any}} blocks (outermost sections)."""

    def replacer(match: re.Match) -> str:
        fields = [f for f in match.group(1).split(',') if f]
        content = match.group(2)

        if any(_field_has_value(data, field) for field in fields):
            return _strip_one_leading_newline(content)
        return ''

    result = _ANY_LINE_RE.sub(replacer, template)
    return _ANY_INLINE_RE.sub(replacer, result)


def _process_conditionals(template: str, data: Dict[str, Any]) -> str:
    """Process {{#field}}...{{/field}} blocks (line-isolated, then inline)."""

    def replacer(match: re.Match) -> str:
        field = match.group(1)
        content = match.group(2)

        if _field_has_value(data, field):
            return _strip_one_leading_newline(content)
        return ''

    result = _SECTION_LINE_RE.sub(replacer, template)
    result = _SECTION_INLINE_RE.sub(replacer, result)
    return result


def _replace_missing_fields(template: str, data: Dict[str, Any]) -> str:
    """Replace {{~field}} with '[not provided]' when the value is empty."""
    def replacer(match: re.Match) -> str:
        field = match.group(1)
        if _field_has_value(data, field):
            return _render_value(data[field])
        return NOT_PROVIDED

    return _MISSING_RE.sub(replacer, template)


def _replace_simple_fields(template: str, data: Dict[str, Any]) -> str:
    """Replace {{field}} with data values."""
    def replacer(match: re.Match) -> str:
        return _render_value(data.get(match.group(1)))

    return _SIMPLE_RE.sub(replacer, template)


def _clean_whitespace(template: str) -> str:
    """Collapse runs of blank lines and trim the result."""
    result = re.sub(r'\n{3,}', '\n\n', template)
    return result.strip() + '\n'


def extract_placeholders(template: str) -> Dict[str, Any]:
    """
    Extract all placeholder names from a template.
    Returns {field_name: is_conditional (bool)}.
    """
    placeholders: Dict[str, bool] = {}

    def _note_conditional(field: str) -> None:
        placeholders[field] = True

    def _note_simple(field: str) -> None:
        if field not in placeholders:
            placeholders[field] = False

    # Simple fields: {{field}}
    for match in _SIMPLE_RE.finditer(template):
        _note_simple(match.group(1))

    # Missing-fields: {{~field}}
    for match in _MISSING_RE.finditer(template):
        _note_simple(match.group(1))

    # any-sections
    for match in _ANY_OPEN_RE.finditer(template):
        for field in match.group(1).split(','):
            _note_conditional(field)

    # Conditional fields: {{#field}}
    for match in _SECTION_LINE_RE.finditer(template):
        _note_conditional(match.group(1))
    for match in _SECTION_INLINE_RE.finditer(template):
        _note_conditional(match.group(1))

    return placeholders


def list_any_sections(template: str) -> List[Dict[str, Any]]:
    """Return any-section field lists for diagnostics, e.g.
    [{'fields': ['hobbies', 'fun_fact'], 'body': '...'}]."""
    result = []
    for match in _ANY_LINE_RE.finditer(template):
        result.append({
            'fields': [f for f in match.group(1).split(',') if f],
            'body': match.group(2),
        })
    return result
