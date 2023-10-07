from dataclasses import dataclass

import pandas as pd
import streamlit as st

from app import App


@dataclass
class ShowMeasurements:
    app: App

    NAME = "Pokaż pomiary dla stacji"

    def process(self):
        if not (sensor_id := st.selectbox(
            label="Wybierz sensor:",
            options=self._get_sorted_unique_sensor_ids()
        )):
            return

        if not (measurements := self.app.end_user.get_measurements_for_sensor(sensor_id)):
            return

        try:
            start_date, end_date = self._get_date_range(measurements)
        except ValueError:
            st.write("Wybierz zakres dat (obecnie wybrano pojedynczą date)")
            return

        if (filtered_data_values := self._filter_data_values(measurements, start_date, end_date)):
            self._display_chart_and_stats(filtered_data_values)

    def _get_sorted_unique_sensor_ids(self):
        sensors = self.app.end_user.get_all_sensors()
        return sorted({sensor.id for sensor in sensors})

    def _get_date_range(self, measurements):
        min_date, max_date = self._get_min_and_max_possible_dates(measurements)
        return st.date_input(
            label="Wybierz zakres dat:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

    def _get_min_and_max_possible_dates(self, measurements):
        all_dates = [data_value.date for measurement in measurements for data_value in measurement.values]
        return min(all_dates), max(all_dates)

    def _filter_data_values(self, measurements, start_date, end_date):
        return [
            data_value for measurement in measurements for data_value in measurement.values
            if (start_date <= data_value.date.date() <= end_date) and (data_value.value is not None)
        ]

    def _display_chart_and_stats(self, filtered_data_values):
        values = [data_value.value for data_value in filtered_data_values]
        dates = [data_value.date for data_value in filtered_data_values]

        st.line_chart(data=pd.DataFrame(data={"Value": values}, index=dates))

        if values:
            stats = Statistics(values, dates)
            stats.display_stats()
            stats.display_trend()

    def _display_stats(self, min_value, min_date, max_value, max_date, avg_value):
        st.write(f"Najmniejsza wartość: {min_value} (Data: {min_date})")
        st.write(f"Największa wartość: {max_value} (Data: {max_date})")
        st.write(f"Średnia wartość: {avg_value:.2f}")

    def _display_trend(self, values):
        trend = "wzrasta" if values[0] < values[-1] else "maleje"
        st.write(f"Trend: {trend}")


@dataclass
class Statistics:
    values: list
    dates: list

    @property
    def min_value(self):
        return min(self.values)

    @property
    def min_date(self):
        return self.dates[self.values.index(self.min_value)]

    @property
    def max_value(self):
        return max(self.values)

    @property
    def max_date(self):
        return self.dates[self.values.index(self.max_value)]

    @property
    def avg_value(self):
        return sum(self.values) / len(self.values)

    @property
    def trend(self):
        return "wzrasta" if self.values[0] < self.values[-1] else "maleje"

    def display_stats(self):
        st.write(f"Najmniejsza wartość: {self.min_value} (Data: {self.min_date})")
        st.write(f"Największa wartość: {self.max_value} (Data: {self.max_date})")
        st.write(f"Średnia wartość: {self.avg_value:.2f}")

    def display_trend(self):
        st.write(f"Trend: {self.trend}")
