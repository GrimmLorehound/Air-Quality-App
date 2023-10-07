import pytest

from domain.sensor.model import Sensor, SensorParam

example_sensor = Sensor(
    id=2,
    id_station=14,
    id_sensor_param=1,
    sensor_param=SensorParam(
        id=1,
        paramName="pył zawieszony PM10",
        paramFormula="PM10",
        paramCode="PM10",
        idParam=3
    )
)


def test_sensor_information():
    expected_information = "- Sensor ID: 1 - Pył Zawieszony Pm10 (PM10)"
    assert example_sensor.information == expected_information
