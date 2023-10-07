from dataclasses import dataclass

import streamlit as st

from app import App
from domain.station.model import Station


@dataclass
class AllPolishStations:
    app: App

    NAME = "Stacje pomiarowe w Polsce"

    def process(self):
        if (stations := self._stations()):
            st.table([station.to_dict() for station in stations])
        else:
            st.write("Brak stacji do wyświetlenia.")

    def _stations(self) -> list[Station]:
        if city := st.text_input("Podaj nazwę miasta, aby wyświetlić stację w miejscowości:"):
            st.subheader(f"Stacje w: {city}")
            return self.app.end_user.show_all_stations_in_city(city)

        st.subheader("Wszystkie")
        return self.app.end_user.show_all_polish_stations()
