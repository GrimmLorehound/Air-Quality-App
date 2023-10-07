from dataclasses import dataclass

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.location import Location

from domain.measurement.model import Measurement
from domain.sensor.model import Sensor
from domain.station.model import Station
from infra.database import Database


@dataclass
class ServiceEndUser:
    db: Database

    def show_all_polish_stations(self) -> list[Station]:
        return self.db.station.get_all_polish_stations()

    def show_all_stations_in_city(self, city_name: str) -> list[Station]:
        return self.db.station.get_all_stations_in_city(city_name)

    def get_nearest_stations(self, localization: str, radius: float) -> list[Station]:
        user_location: Location | None = Nominatim(user_agent="Ameliasapp").geocode(localization)
        if user_location is None:
            raise ValueError(f"No coordinates found for localization: {localization}")

        return [
            station
            for station in self.db.station.get_all_polish_stations()
            if geodesic(
                (station.gegr_latitude, station.gegr_longitude),
                (user_location.latitude, user_location.longitude),
            ).kilometers
            <= radius
        ]

    def get_sensors_for_station(self, station_id: int) -> list[Sensor]:
        return self.db.sensor.get_sensor_for_station(station_id)

    def get_all_sensors(self) -> list[Sensor]:
        return self.db.sensor.get_all_sensors()

    def get_measurements_for_sensor(self, id_sensor: int) -> list[Measurement]:
        return self.db.measurement.get_measurement_for_sensor(id_sensor=id_sensor)
