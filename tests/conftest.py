"""
Test configuration for the Context File Maker test suite.
"""

import json
import sys
from pathlib import Path

import pytest

# Add scripts directory to path so tests can import template_engine
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def project_root():
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def fixtures_dir():
    return Path(__file__).resolve().parent / 'fixtures'


@pytest.fixture
def load_fixture(fixtures_dir):
    def _load(name: str) -> dict:
        path = fixtures_dir / name
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return _load


@pytest.fixture
def about_me_answers(load_fixture):
    return load_fixture('about_me_answers.json')


@pytest.fixture
def ai_preferences_answers(load_fixture):
    return load_fixture('ai_preferences_answers.json')


@pytest.fixture
def about_me_minimal(load_fixture):
    return load_fixture('about_me_minimal.json')


@pytest.fixture
def ai_preferences_minimal(load_fixture):
    return load_fixture('ai_preferences_minimal.json')


@pytest.fixture
def about_me_template(project_root):
    path = project_root / 'templates' / 'free' / 'about_me.md'
    return path.read_text(encoding='utf-8')


@pytest.fixture
def ai_preferences_template(project_root):
    path = project_root / 'templates' / 'free' / 'ai_preferences.md'
    return path.read_text(encoding='utf-8')
