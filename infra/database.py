from dataclasses import dataclass

from sqlalchemy.orm import Session

from domain.air_quality.db import DBAirQuality
from domain.measurement.db import DBMeasurement
from domain.sensor.db import DBSensor
from domain.station.db import DBStation


@dataclass
class Database:
    station: DBStation
    sensor: DBSensor
    air_quality: DBAirQuality
    measurement: DBMeasurement

    @staticmethod
    def init(session: Session):
        return Database(
            station=DBStation(session),
            sensor=DBSensor(session),
            air_quality=DBAirQuality(session),
            measurement=DBMeasurement(session),
        )
