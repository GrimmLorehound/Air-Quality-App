from dataclasses import dataclass

import streamlit as st

from app import App
from ui.pages.all_polish_stations import AllPolishStations
from ui.pages.nearby_stations import NearbyStations
from ui.pages.page import Page
from ui.pages.show_measurements import ShowMeasurements

BOOT_INFORMATION = """
Aplikacja stara pobrać się całą dostępną historię z zewnętrznego
źródła, więc proces ten może potrwać parę minut (ETA 2-3 minuty).
Odśwież stronę po tym czasie i eksploruj! 🎉
"""

@dataclass
class UI:
    app: App
    all_polish_stations: AllPolishStations
    nearby_stations: NearbyStations
    show_measurements: ShowMeasurements

    TITLE = "Jakość powietrza w Polsce 🍃😷"
    SIDEBAR_TITLE = "Funkcjonalności"
    SIDEBAR_PAGE_CHOOSER = "Wybierz opcję:"

    def __post_init__(self):
        self.pages: dict[str, Page] = {
            AllPolishStations.NAME: self.all_polish_stations,
            NearbyStations.NAME: self.nearby_stations,
            ShowMeasurements.NAME: self.show_measurements,
        }

        st.title(self.TITLE)
        st.sidebar.title(self.SIDEBAR_TITLE)
        chosen_page = st.sidebar.radio(label=self.SIDEBAR_PAGE_CHOOSER, options=self.pages.keys())

        # Fetch all data button
        if st.sidebar.button('Odśwież dane z zewnętrznego źródła'):
            st.write(BOOT_INFORMATION)
            self.app.persitence.fetch_all_information_and_save_to_db()

        if page := self.pages.get(chosen_page or ""):
            page.process()


def start_user_interface(app: App) -> None:
    UI(
        app=app,
        all_polish_stations=AllPolishStations(app=app),
        nearby_stations=NearbyStations(app=app),
        show_measurements=ShowMeasurements(app=app),
    )
