import pytest
from sqlalchemy.orm import Session

from domain.sensor.db import DBSensor, Sensor


@pytest.fixture
def db_sensor(mock_session: Session):
    return DBSensor(session=mock_session)


def test_get_sensor_for_station(db_sensor, mock_session):
    # given
    station_id = 1
    mock_session.query.return_value.filter_by.return_value.all.return_value = [Sensor(id=1, id_station=1)]

    # when
    result = db_sensor.get_sensor_for_station(station_id)

    # then
    mock_session.query.assert_called_once_with(Sensor)
    mock_session.query.return_value.filter_by.assert_called_once_with(id_station=station_id)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].id_station == 1


def test_get_all_sensors(db_sensor, mock_session):
    # given
    mock_session.query.return_value.all.return_value = [Sensor(id=1), Sensor(id=2)]

    # when
    result = db_sensor.get_all_sensors()

    # then
    mock_session.query.assert_called_once_with(Sensor)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
