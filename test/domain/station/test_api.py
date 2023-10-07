import pytest
import responses

from domain.station.api import ApiStation, get_stations

# URL API do stacji
STATIONS_URL = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"

# Przykład odpowiedzi z API
EXAMPLE_API_RESPONSE = [
    {
        "id": 14,
        "stationName": "Działoszyn",
        "gegrLat": "50.972167",
        "gegrLon": "14.941319",
        "city": {
            "id": 192,
            "name": "Działoszyn",
            "commune": {
                "communeName": "Bogatynia",
                "districtName": "zgorzelecki",
                "provinceName": "DOLNOŚLĄSKIE"
            }
        },
        "addressStreet": None
    }
]


@responses.activate
def test_get_stations():
    responses.add(
        responses.GET,
        STATIONS_URL,
        json=EXAMPLE_API_RESPONSE,
        status=200
    )

    stations = get_stations()

    assert stations is not None
    assert len(stations) == 1
    
    station = stations[0]
    assert isinstance(station, ApiStation)
    assert station.id == 14
    assert station.stationName == "Działoszyn"
    assert station.gegrLat == 50.972167
    assert station.gegrLon == 14.941319
    assert station.city.id == 192
    assert station.city.name == "Działoszyn"
    assert station.city.commune.communeName == "Bogatynia"
    assert station.city.commune.districtName == "zgorzelecki"
    assert station.city.commune.provinceName == "DOLNOŚLĄSKIE"
    assert station.addressStreet is None
