import requests
from pydantic.dataclasses import dataclass

from tools.api_exception_handler import handle_api_exceptions

SENSORS_URL = "https://api.gios.gov.pl/pjp-api/rest/station/sensors/{stationId}"


@dataclass
class ApiSensorParam:
    paramName: str
    paramFormula: str
    paramCode: str
    idParam: int


@dataclass
class ApiSensor:
    id: int
    stationId: int
    param: ApiSensorParam


@handle_api_exceptions
def get_sensors(id_station: int) -> list[ApiSensor] | None:
    response = requests.get(url=SENSORS_URL.format(stationId=id_station))
    response.raise_for_status()
    return [ApiSensor(**sensor) for sensor in response.json()]
