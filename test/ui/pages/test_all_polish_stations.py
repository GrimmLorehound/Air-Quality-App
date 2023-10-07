from unittest.mock import MagicMock

import pytest

from app import App, boot
from infra.database import Database
from services.end_user import ServiceEndUser
from services.persistence import ServicePersistence
from ui.pages.all_polish_stations import AllPolishStations


@pytest.fixture
def mock_st(mocker):
    return mocker.patch("ui.pages.all_polish_stations.st", autospec=True)


@pytest.fixture
def mock_app(mock_session):
    db = Database.init(session=boot("test_air_quality_db"))
    return App(end_user=ServiceEndUser(db=db), persitence=ServicePersistence(db=db))


def test_process_without_stations(mock_st, mock_app):
    # Given
    all_polish_stations = AllPolishStations(app=mock_app)
    all_polish_stations._stations = MagicMock(return_value=[])

    # When
    all_polish_stations.process()

    # Then
    mock_st.write.assert_called_once_with("Brak stacji do wyświetlenia.")
