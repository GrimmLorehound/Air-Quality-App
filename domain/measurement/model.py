from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from infra.declarative_base import Base


class MeasurementDataValue(Base):
    __tablename__ = 'measurement_data_values'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    value = Column(Float, nullable=True)
    measurement_id = Column(Integer, ForeignKey('measurements.id'))
    measurement = relationship("Measurement", back_populates="values")


class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=True)
    id_sensor = Column(Integer)
    values = relationship("MeasurementDataValue", back_populates="measurement")

    @property
    def formatted_values(self):
        return [{
            "Key": self.key,
            "Date": value.date,
            "Value": value.value
        } for value in self.values]
