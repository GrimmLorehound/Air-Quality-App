from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def mock_session():
    return create_autospec(Session, instance=True)
