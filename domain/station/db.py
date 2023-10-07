from dataclasses import dataclass

from sqlalchemy.orm import Session

from domain.station.api import ApiCommune, ApiStation
from domain.station.model import City, Commune, Station


@dataclass
class DBStation:
    session: Session
    
    def get_all_polish_stations(self) -> list[Station]:
        """ Returns all saved stations from Polish REST Api """
        return self.session.query(Station).all()

    def get_all_stations_in_city(self, city_name: str) -> list[Station]:
        """ Returns all the stations in the given city """
        return (
            self.session.query(Station)
            .join(City, Station.id_city == City.id)
            .filter(City.name == city_name)
            .all()
        )

    def _load_station_from_db(self, station_id: int) -> Station | None:
        return self.session.query(Station).filter_by(id=station_id).first()

    def _load_city_from_db(self, city_id: int) -> City | None:
        return self.session.query(City).filter_by(id=city_id).first()

    def _find_commune_in_db(self, api_commune: ApiCommune) -> Commune | None:
        return self.session.query(Commune).filter_by(
            communeName=api_commune.communeName,
            districtName=api_commune.districtName,
            provinceName=api_commune.provinceName
        ).first()

    def save_station_to_db(self, station: ApiStation):
        if self._load_station_from_db(station.id) is not None:
            # print(f"Station with ID {station.id} already exists in the database.")
            return

        if (commune := self._find_commune_in_db(station.city.commune)) is None:
            commune = Commune(
                communeName=station.city.commune.communeName,
                districtName=station.city.commune.districtName,
                provinceName=station.city.commune.provinceName
            )
            self.session.add(commune)
            self.session.flush()

        if (city := self._load_city_from_db(station.city.id)) is None:
            city = City(
                id=station.city.id,
                id_commune=commune.id,
                name=station.city.name,
            )
            self.session.add(city)
            self.session.flush()

        self.session.add(Station(
            id=station.id,
            id_city=city.id,
            station_name=station.stationName,
            gegr_latitude=station.gegrLat,
            gegr_longitude=station.gegrLon,
            address_street=station.addressStreet,
        ))
        self.session.commit()
        # print(f"Station with ID {station.id} saved to the database.")
