from datetime import datetime

import requests
from pydantic.dataclasses import dataclass

from tools.api_exception_handler import handle_api_exceptions

AQI_URL = "https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{stationId}"


@dataclass
class ApiAqIndexLevel:
    id: int
    indexLevelName: str


@dataclass
class ApiAqIndex:
    id: int
    stCalcDate: datetime | None
    stIndexLevel: ApiAqIndexLevel | None
    stSourceDataDate: datetime | None
    so2CalcDate: datetime | None
    so2IndexLevel: ApiAqIndexLevel | None
    so2SourceDataDate: datetime | None
    no2CalcDate: datetime | None
    no2IndexLevel: ApiAqIndexLevel | None
    no2SourceDataDate: datetime | None
    pm10CalcDate: datetime | None
    pm10IndexLevel: ApiAqIndexLevel | None
    pm10SourceDataDate: datetime | None
    pm25CalcDate: datetime | None
    pm25IndexLevel: ApiAqIndexLevel | None
    pm25SourceDataDate: datetime | None
    o3CalcDate: datetime | None
    o3IndexLevel: ApiAqIndexLevel | None
    o3SourceDataDate: datetime | None

    @staticmethod
    def from_response(response: dict) -> 'ApiAqIndex':
        return ApiAqIndex(
            id=response['id'],
            stCalcDate=(
                datetime.strptime(response['stCalcDate'], '%Y-%m-%d %H:%M:%S')
                if response['stCalcDate'] else None
            ),
            stIndexLevel=(
                ApiAqIndexLevel(**response['stIndexLevel'])
                if response['stIndexLevel'] else None
            ),
            stSourceDataDate=(
                datetime.strptime(response['stSourceDataDate'], '%Y-%m-%d %H:%M:%S')
                if response['stSourceDataDate'] else None
            ),
            so2CalcDate=(
                datetime.strptime(response['so2CalcDate'], '%Y-%m-%d %H:%M:%S')
                if response['so2CalcDate'] else None
            ),
            so2IndexLevel=(
                ApiAqIndexLevel(**response['so2IndexLevel'])
                if response['so2IndexLevel'] else None
            ),
            so2SourceDataDate=(
                datetime.strptime(response['so2SourceDataDate'], '%Y-%m-%d %H:%M:%S')
                if response['so2SourceDataDate'] else None
            ),
            no2CalcDate=(
                datetime.strptime(response['no2CalcDate'], '%Y-%m-%d %H:%M:%S')
                if response['no2CalcDate'] else None
            ),
            no2IndexLevel=(
                ApiAqIndexLevel(**response['no2IndexLevel'])
                if response['no2IndexLevel'] else None
            ),
            no2SourceDataDate=(
                datetime.strptime(response['no2SourceDataDate'], '%Y-%m-%d %H:%M:%S')
                if response['no2SourceDataDate'] else None
            ),
            pm10CalcDate=(
                datetime.strptime(response['pm10CalcDate'], '%Y-%m-%d %H:%M:%S')
                if response['pm10CalcDate'] else None
            ),
            pm10IndexLevel=(
                ApiAqIndexLevel(**response['pm10IndexLevel'])
                if response['pm10IndexLevel'] else None
            ),
            pm10SourceDataDate=(
                datetime.strptime(response['pm10SourceDataDate'], '%Y-%m-%d %H:%M:%S')
                if response['pm10SourceDataDate'] else None
            ),
            pm25CalcDate=(
                datetime.strptime(response['pm25CalcDate'], '%Y-%m-%d %H:%M:%S')
                if response['pm25CalcDate'] else None
            ),
            pm25IndexLevel=(
                ApiAqIndexLevel(**response['pm25IndexLevel'])
                if response['pm25IndexLevel'] else None
            ),
            pm25SourceDataDate=(
                datetime.strptime(response['pm25SourceDataDate'], '%Y-%m-%d %H:%M:%S')
                if response['pm25SourceDataDate'] else None
            ),
            o3CalcDate=(
                datetime.strptime(response['o3CalcDate'], '%Y-%m-%d %H:%M:%S')
                if response['o3CalcDate'] else None
            ),
            o3IndexLevel=(
                ApiAqIndexLevel(**response['o3IndexLevel'])
                if response['o3IndexLevel'] else None
            ),
            o3SourceDataDate=(
                datetime.strptime(response['o3SourceDataDate'], '%Y-%m-%d %H:%M:%S')
                if response['o3SourceDataDate'] else None
            )
        )


@handle_api_exceptions
def get_air_quality_index(station_id: int) -> ApiAqIndex:
    response = requests.get(url=AQI_URL.format(stationId=station_id))
    response.raise_for_status()
    return ApiAqIndex.from_response(response.json())
