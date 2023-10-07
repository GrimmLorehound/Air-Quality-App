from datetime import datetime

import requests
from pydantic.dataclasses import dataclass

from tools.api_exception_handler import handle_api_exceptions

MEASUREMENTS_URL = "https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensorId}"


@dataclass
class ApiMeasurementDataValue:
    date: datetime
    value: float | None

    @staticmethod
    def from_response(response: dict) -> 'ApiMeasurementDataValue':
        return ApiMeasurementDataValue(
            date=datetime.strptime(response['date'], '%Y-%m-%d %H:%M:%S'),
            value=response['value']
        )


@dataclass
class ApiMeasurement:
    key: str | None
    values: list[ApiMeasurementDataValue] | None

    @staticmethod
    def from_response(response: dict) -> 'ApiMeasurement':
        return ApiMeasurement(
            key=response.get('key'),
            values=(
                [ApiMeasurementDataValue.from_response(value_data) for value_data in response.get('values') if value_data]
                if response.get('values') else None
            )
        )



@handle_api_exceptions
def get_measurement(id_sensor: int) -> ApiMeasurement:
    response = requests.get(url=MEASUREMENTS_URL.format(sensorId=id_sensor))
    response.raise_for_status()
    return ApiMeasurement.from_response(response.json())
