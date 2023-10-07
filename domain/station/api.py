import requests
from pydantic.dataclasses import dataclass

from tools.api_exception_handler import handle_api_exceptions

STATIONS_URL = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"


@dataclass
class ApiCommune:
    communeName: str
    districtName: str
    provinceName: str


@dataclass
class ApiCity:
    id: int
    name: str
    commune: ApiCommune


@dataclass
class ApiStation:
    id: int
    stationName: str
    gegrLat: float
    gegrLon: float
    city: ApiCity
    addressStreet: str | None


@handle_api_exceptions
def get_stations() -> list[ApiStation] | None:
    response = requests.get(STATIONS_URL)
    response.raise_for_status()
    return [ApiStation(**resp) for resp in response.json()]
