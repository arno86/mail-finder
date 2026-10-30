from pathlib import Path

import pytest

from mailfinder import Message, parse

SAMPLES = Path(__file__).parent / "samples"


@pytest.fixture
def activation() -> Message:
    return parse((SAMPLES / "activation.eml").read_bytes())


@pytest.fixture
def invitation() -> Message:
    return parse((SAMPLES / "site_invitation.eml").read_bytes())
