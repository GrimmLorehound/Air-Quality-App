from sqlalchemy import Column, DateTime, Integer

from infra.declarative_base import Base


class AirQuality(Base):
    __tablename__ = 'air_quality'
    id = Column(Integer, primary_key=True)
    st_calc_date = Column(DateTime, nullable=True)
    st_index_level = Column(Integer, nullable=True)
    st_source_data_date = Column(DateTime, nullable=True)

    so2_calc_date = Column(DateTime, nullable=True)
    so2_index_level = Column(Integer, nullable=True)
    so2_source_data_date = Column(DateTime, nullable=True)

    no2_calc_date = Column(DateTime, nullable=True)
    no2_index_level = Column(Integer, nullable=True)
    no2_source_data_date = Column(DateTime, nullable=True)

    pm10_calc_date = Column(DateTime, nullable=True)
    pm10_index_level = Column(Integer, nullable=True)
    pm10_source_data_date = Column(DateTime, nullable=True)

    pm25_calc_date = Column(DateTime, nullable=True)
    pm25_index_level = Column(Integer, nullable=True)
    pm25_source_data_date = Column(DateTime, nullable=True)

    o3_calc_date = Column(DateTime, nullable=True)
    o3_index_level = Column(Integer, nullable=True)
    o3_source_data_date = Column(DateTime, nullable=True)
