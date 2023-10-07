from unittest.mock import MagicMock

import pytest

from domain.station.db import DBStation, Station


@pytest.fixture
def db_station(mock_session):
    return DBStation(session=mock_session)


def test_get_all_polish_stations(db_station, mock_session):
    mock_session.query.return_value.all.return_value = [Station(id=1), Station(id=2)]

    result = db_station.get_all_polish_stations()

    mock_session.query.assert_called_once_with(Station)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


def test_get_all_stations_in_city(db_station, mock_session):
    city_name = 'TestCity'
    mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [Station(id=1, id_city=1)]

    result = db_station.get_all_stations_in_city(city_name)

    mock_session.query.assert_called_once_with(Station)
    mock_session.query.return_value.join.assert_called_once()
    mock_session.query.return_value.join.return_value.filter.assert_called_once()
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].id_city == 1
