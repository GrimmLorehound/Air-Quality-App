from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from infra.declarative_base import Base


class SensorParam(Base):
    __tablename__ = 'sensors_params'
    id = Column(Integer, primary_key=True)
    paramName = Column(String)
    paramFormula = Column(String)
    paramCode = Column(String)
    idParam = Column(Integer)
    sensor = relationship("Sensor", uselist=False, back_populates="sensor_param")


class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    id_station = Column(Integer)
    id_sensor_param = Column(Integer, ForeignKey('sensors_params.id'))
    sensor_param = relationship("SensorParam", back_populates="sensor")

    @property
    def information(self) -> str:
        return f"- Sensor ID: {self.id} - {self.sensor_param.paramName.title()} ({self.sensor_param.paramCode})"
