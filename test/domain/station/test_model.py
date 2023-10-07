import pytest

from domain.station.model import Station

example_station = Station(
    id=1,
    id_city=1,
    station_name="Przykładowa stacja",
    gegr_latitude=52.2297,
    gegr_longitude=21.0122,
    address_street="Przykładowa ulica"
)


def test_station_to_dict():
    expected_dict = {
        "Nazwa stacji": "Przykładowa stacja",
        "Szerokość geograficzna": 52.2297,
        "Długość geograficzna": 21.0122,
        "Ulica": "Przykładowa ulica",
    }

    assert example_station.to_dict() == expected_dict
