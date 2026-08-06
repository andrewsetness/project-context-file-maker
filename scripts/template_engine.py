"""
Context File Maker — Template Engine

Fills Mustache-style templates with structured answer data from JSON.
Supports: {{field}}, {{#field}}...{{/field}} (conditional blocks).

Usage:
    from template_engine import fill_template
    result = fill_template(template_str, answers_dict)
"""

import re
from typing import Any, Dict


def fill_template(template: str, data: Dict[str, Any]) -> str:
    """
    Fill a Mustache-style template with data.

    Template syntax:
        {{field}}          — Replace with data['field'] (string or text)
        {{#field}}         — If data['field'] is truthy, include the block
        {{/field}}         — End of conditional block

    Empty/None fields in conditional blocks are omitted entirely.
    """
    result = _process_conditionals(template, data)
    result = _replace_simple_fields(result, data)
    result = _clean_extra_whitespace(result)
    return result


def _process_conditionals(template: str, data: Dict[str, Any]) -> str:
    """Process {{#field}}...{{/field}} conditional blocks."""
    pattern = re.compile(
        r'\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}',
        re.DOTALL
    )

    def replacer(match: re.Match) -> str:
        field = match.group(1)
        content = match.group(2)
        value = data.get(field)
        if value and str(value).strip():
            return content
        return ''

    return pattern.sub(replacer, template)


def _replace_simple_fields(template: str, data: Dict[str, Any]) -> str:
    """Replace {{field}} with data values."""
    pattern = re.compile(r'\{\{(\w+)\}\}')

    def replacer(match: re.Match) -> str:
        field = match.group(1)
        value = data.get(field, '')
        if value is None:
            return ''
        return str(value)

    return pattern.sub(replacer, template)


def _clean_extra_whitespace(template: str) -> str:
    """Remove triple+ blank lines left by removed conditionals."""
    return re.sub(r'\n{3,}', '\n\n', template).strip() + '\n'


def extract_placeholders(template: str) -> Dict[str, Any]:
    """
    Extract all placeholder names from a template.
    Returns {field_name: is_conditional (bool)}.
    """
    placeholders: Dict[str, bool] = {}

    # Simple fields: {{field}}
    for match in re.finditer(r'\{\{(\w+)\}\}', template):
        field = match.group(1)
        if field not in placeholders:
            placeholders[field] = False

    # Conditional fields: {{#field}}
    for match in re.finditer(r'\{\{#(\w+)\}\}', template):
        field = match.group(1)
        placeholders[field] = True

    return placeholders
