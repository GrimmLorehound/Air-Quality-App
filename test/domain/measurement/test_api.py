import pytest
import responses

from domain.measurement.api import get_measurement

EXAMPLE_API_RESPONSE = {
    "key": "PM10",
    "values": [
        {
            "date": "2017-03-28 11:00:00",
            "value": 30.3018
        },
        {
            "date": "2017-03-28 12:00:00",
            "value": 27.5946
        }
    ]
}

MEASUREMENTS_URL = "https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensorId}"


@responses.activate
def test_get_measurement():
    sensor_id = 92
    responses.add(
        responses.GET,
        MEASUREMENTS_URL.format(sensorId=sensor_id),
        json=EXAMPLE_API_RESPONSE,
        status=200
    )

    measurement = get_measurement(sensor_id)

    assert measurement is not None
    assert measurement.key == "PM10"
    assert len(measurement.values) == 2

    first_value, second_value = measurement.values

    assert first_value.date.strftime('%Y-%m-%d %H:%M:%S') == "2017-03-28 11:00:00"
    assert first_value.value == 30.3018

    assert second_value.date.strftime('%Y-%m-%d %H:%M:%S') == "2017-03-28 12:00:00"
    assert second_value.value == 27.5946
