import pytest
import responses

from domain.sensor.api import get_sensors

EXAMPLE_API_RESPONSE = [
    {
        "id": 92,
        "stationId": 14,
        "param": {
            "paramName": "pył zawieszony PM10",
            "paramFormula": "PM10",
            "paramCode": "PM10",
            "idParam": 3
        }
    },
    {
        "id": 88,
        "stationId": 14,
        "param": {
            "paramName": "dwutlenek azotu",
            "paramFormula": "NO2",
            "paramCode": "NO2",
            "idParam": 6
        }
    }
]

SENSORS_URL = "https://api.gios.gov.pl/pjp-api/rest/station/sensors/{stationId}"


@responses.activate
def test_get_sensors():
    station_id = 14
    responses.add(
        responses.GET,
        SENSORS_URL.format(stationId=station_id),
        json=EXAMPLE_API_RESPONSE,
        status=200
    )

    # Wywołanie funkcji get_sensors
    sensors = get_sensors(station_id)

    # Sprawdzenie, czy funkcja zwróciła poprawne dane
    assert sensors is not None
    assert len(sensors) == 2
    first_sensor, second_sensor = sensors

    # Sprawdzanie wartości dla pierwszego sensora
    assert first_sensor.id == 92
    assert first_sensor.stationId == 14
    assert first_sensor.param.paramName == "pył zawieszony PM10"
    assert first_sensor.param.paramFormula == "PM10"
    assert first_sensor.param.paramCode == "PM10"
    assert first_sensor.param.idParam == 3

    # Sprawdzanie wartości dla drugiego sensora
    assert second_sensor.id == 88
    assert second_sensor.stationId == 14
    assert second_sensor.param.paramName == "dwutlenek azotu"
    assert second_sensor.param.paramFormula == "NO2"
    assert second_sensor.param.paramCode == "NO2"
    assert second_sensor.param.idParam == 6
