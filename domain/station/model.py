from sqlalchemy import Column, Float, Integer, String

from infra.declarative_base import Base


class Commune(Base):
    __tablename__ = 'communes'
    id = Column(Integer, primary_key=True)
    communeName = Column(String)
    districtName = Column(String)
    provinceName = Column(String)


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    id_commune = Column(Integer)  # foreign key to commune table
    name = Column(String)


class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    id_city = Column(Integer)  # foreign key to city table
    station_name = Column(String)
    gegr_latitude = Column(Float)
    gegr_longitude = Column(Float)
    address_street = Column(String)

    def to_dict(self) -> dict:
        return {
            "Nazwa stacji": self.station_name,
            "Szerokość geograficzna": self.gegr_latitude,
            "Długość geograficzna": self.gegr_longitude,
            "Ulica": self.address_street,
        }
