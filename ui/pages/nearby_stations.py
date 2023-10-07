from dataclasses import dataclass

import pandas as pd
import streamlit as st

from app import App
from domain.station.model import Station


@dataclass
class NearbyStations:
    app: App

    NAME = "Znajdź najbliższą stację"

    def process(self):
        localization = st.text_input("Podaj lokalizację:", value="Poznań")
        radius = st.slider("Podaj promień (km):", min_value=1, max_value=100, value=50)
        if not (localization and radius):
            return

        if (nearest_stations := self.app.end_user.get_nearest_stations(localization, radius)):
            st.map(data=pd.DataFrame({
                'lat': [station.gegr_latitude for station in nearest_stations],
                'lon': [station.gegr_longitude for station in nearest_stations]
            }))

            selected_station = st.selectbox(
                "Wybierz stację, aby zobaczyć dostępne sensory:",
                options=[station.station_name for station in nearest_stations],
                format_func=lambda x: x
            )

            if (station_id := self._find_station(nearest_stations, selected_station)) is not None:
                st.write("Dostępne czujniki:")
                sensors = self.app.end_user.get_sensors_for_station(station_id)
                for sensor in sensors:
                    st.write(sensor.information)

                if (selected_sensor := st.selectbox(
                    "Wybierz czujnik, aby zobaczyć pomiary:",
                    options=[sensor.id for sensor in sensors],
                    format_func=lambda x: f"Sensor ID: {x}"
                )) is not None:
                    measurements = self.app.end_user.get_measurements_for_sensor(selected_sensor)
                    measurement_data = [data for measurement in measurements for data in measurement.formatted_values]

                    if measurement_data:
                        st.dataframe(pd.DataFrame(measurement_data))

        else:
            st.write("Brak stacji w podanym promieniu.")

    def _find_station(self, nearest_stations: list[Station], selected_station: Station):
        return next((station.id for station in nearest_stations if station.station_name == selected_station), None)
