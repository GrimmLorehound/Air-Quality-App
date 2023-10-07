from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from domain.measurement.api import ApiMeasurement
from domain.measurement.model import Measurement, MeasurementDataValue


@dataclass
class DBMeasurement:
    session: Session

    def get_historical_data(self, start_date: str, end_date: str, id_sensor: int) -> list[Measurement]:
        """
        Pobiera dane historyczne dla danego sensora w określonym zakresie dat.

        :param start_date: Data początkowa w formacie 'YYYY-MM-DD HH:MM:SS'.
        :param end_date: Data końcowa w formacie 'YYYY-MM-DD HH:MM:SS'.
        :param id_sensor: ID sensora.
        :return: Lista obiektów Measurement.
        """
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        return self.session.query(Measurement)\
            .join(MeasurementDataValue)\
            .filter(Measurement.id_sensor == id_sensor)\
            .filter(MeasurementDataValue.date.between(start_datetime, end_datetime))\
            .all()

    def get_measurement_for_sensor(self, id_sensor: int) -> list[Measurement]:
        """ Returns all the measurements for the given sensor """
        return self.session.query(Measurement).filter_by(id_sensor=id_sensor).all()

    def _load_measurement_data_value_from_db(self, date: str) -> MeasurementDataValue | None:
        return self.session.query(MeasurementDataValue).filter_by(date=date).first()

    def _find_data_value_in_db(self, date: str, value: float | None) -> MeasurementDataValue | None:
        return self.session.query(MeasurementDataValue).filter_by(date=date, value=value).first()

    def save_measurement_to_db(self, api_measurement: ApiMeasurement, id_sensor: int):
        if api_measurement.values is None:
            print(f"Measurement for sensor ID {id_sensor}, key {api_measurement.key} has no values.")
            return

        measurement = Measurement(
            key=api_measurement.key,
            id_sensor=id_sensor
        )
        self.session.add(measurement)
        self.session.flush()  # Flush to assign ID to measurement object before creating MeasurementDataValue objects

        for api_data_value in api_measurement.values:
            self.session.add(MeasurementDataValue(
                date=api_data_value.date,
                value=api_data_value.value,
                measurement_id=measurement.id
            ))

        self.session.commit()
