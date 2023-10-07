from dataclasses import dataclass

from sqlalchemy.orm import Session

from domain.sensor.api import ApiSensor
from domain.sensor.model import Sensor, SensorParam


@dataclass
class DBSensor:
    session: Session

    def get_sensor_for_station(self, station_id: int) -> list[Sensor]:
        """ Returns all the sensors in the given station """
        return self.session.query(Sensor).filter_by(id_station=station_id).all()

    def get_all_sensors(self) -> list[Sensor]:
        """ Returns all the sensors """
        return self.session.query(Sensor).all()

    def _load_sensor_from_db(self, id_sensor: int) -> Sensor | None:
        return self.session.query(Sensor).filter_by(id=id_sensor).first()

    def _load_param_from_db(self, param_id: int) -> SensorParam | None:
        return self.session.query(SensorParam).filter_by(idParam=param_id).first()

    def save_sensor_to_db(self, api_sensor: ApiSensor):
        if self._load_sensor_from_db(api_sensor.id) is not None:
            # print(f"Sensor with ID {api_sensor.id} already exists in the database.")
            return

        if (sensor_param := self._load_param_from_db(api_sensor.param.idParam)) is None:
            sensor_param = SensorParam(
                id=api_sensor.param.idParam,
                paramName=api_sensor.param.paramName,
                paramFormula=api_sensor.param.paramFormula,
                paramCode=api_sensor.param.paramCode,
                idParam=api_sensor.param.idParam
            )
            self.session.add(sensor_param)
            self.session.flush()

        self.session.add(Sensor(
            id=api_sensor.id,
            id_station=api_sensor.stationId,
            id_sensor_param=sensor_param.id
        ))
        self.session.commit()
        # print(f"Sensor with ID {api_sensor.id} saved to the database.")
