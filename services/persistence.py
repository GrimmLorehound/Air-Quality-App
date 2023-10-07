from dataclasses import dataclass

# from domain.air_quality.api import get_air_quality_index
from domain.measurement.api import get_measurement
from domain.sensor.api import get_sensors
from domain.sensor.model import Sensor
from domain.station.api import get_stations
from domain.station.model import Station
from infra.database import Database


@dataclass
class ServicePersistence:
    db: Database

    def fetch_all_information_and_save_to_db(self):
        for station in get_stations():
            print(f"Saving information for station {station}...")
            station: Station
            self.db.station.save_station_to_db(station)

            # aqindex = get_air_quality_index(station.id)
            # self.db.air_quality.save_aqindex_to_db(aqindex)

            for sensor in get_sensors(id_station=station.id):
                sensor: Sensor
                self.db.sensor.save_sensor_to_db(sensor)

                measurement_data = get_measurement(id_sensor=sensor.id)
                self.db.measurement.save_measurement_to_db(measurement_data, sensor.id)
