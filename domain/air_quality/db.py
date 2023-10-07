
from dataclasses import dataclass

from sqlalchemy.orm import Session

from domain.air_quality.api import ApiAqIndex
from domain.air_quality.model import AirQuality


@dataclass
class DBAirQuality:
    session: Session

    def save_aqindex_to_db(self, aqindex: ApiAqIndex):
        aq = AirQuality(
            id=aqindex.id,
            st_calc_date=aqindex.stCalcDate,
            st_index_level=aqindex.stIndexLevel.id if aqindex.stIndexLevel else None,
            st_source_data_date=aqindex.stSourceDataDate,
            so2_calc_date=aqindex.so2CalcDate,
            so2_index_level=aqindex.so2IndexLevel.id if aqindex.so2IndexLevel else None,
            so2_source_data_date=aqindex.so2SourceDataDate,
            no2_calc_date=aqindex.no2CalcDate,
            no2_index_level=aqindex.no2IndexLevel.id if aqindex.no2IndexLevel else None,
            no2_source_data_date=aqindex.no2SourceDataDate,
            pm10_calc_date=aqindex.pm10CalcDate,
            pm10_index_level=aqindex.pm10IndexLevel.id if aqindex.pm10IndexLevel else None,
            pm10_source_data_date=aqindex.pm10SourceDataDate,
            pm25_calc_date=aqindex.pm25CalcDate,
            pm25_index_level=aqindex.pm25IndexLevel.id if aqindex.pm25IndexLevel else None,
            pm25_source_data_date=aqindex.pm25SourceDataDate,
            o3_calc_date=aqindex.o3CalcDate,
            o3_index_level=aqindex.o3IndexLevel.id if aqindex.o3IndexLevel else None,
            o3_source_data_date=aqindex.o3SourceDataDate
        )
        self.session.add(aq)
        self.session.commit()