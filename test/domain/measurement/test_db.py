from datetime import datetime
from unittest.mock import MagicMock

import pytest

from domain.measurement.db import DBMeasurement, Measurement


@pytest.fixture
def db_measurement(mocker):
    mock_session = mocker.Mock()
    mocker.patch.object(mock_session, 'query', return_value=mock_session.query)
    return DBMeasurement(session=mock_session)


def test_get_measurement_for_sensor(db_measurement: DBMeasurement):
    # given
    id_sensor = 1

    # when
    db_measurement.get_measurement_for_sensor(id_sensor)

    # then
    db_measurement.session.query.assert_called_once_with(Measurement)
    assert db_measurement.session.query().filter_by.called


def test_save_measurement_to_db(db_measurement: DBMeasurement):
    # given
    api_measurement = MagicMock()
    api_measurement.values = [MagicMock(date=datetime.now(), value=1.0)]
    api_measurement.key = 'PM10'
    id_sensor = 1

    # when
    db_measurement.save_measurement_to_db(api_measurement, id_sensor)

    # then
    assert db_measurement.session.add.called
    assert db_measurement.session.flush.called
    assert db_measurement.session.commit.called
