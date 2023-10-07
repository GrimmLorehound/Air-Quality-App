import threading
from time import sleep

import schedule
import streamlit as st
from sqlalchemy.exc import IntegrityError

from app import App, start_application
from ui.ui import start_user_interface


def fetch_and_save(app: App):
    app.persitence.fetch_all_information_and_save_to_db()


def run_schedule(app: App):
    schedule.every(4).hours.do(fetch_and_save, app=app)

    while True:
        schedule.run_pending()
        sleep(60)


def main():
    try:
        app: App = start_application()

        fetch_thread = threading.Thread(target=run_schedule, args=(app,))
        fetch_thread.start()

        start_user_interface(app)
    except IntegrityError:
        st.warning(
            body="Nie udało się połączyć z bazą danych. Spróbuj ponownie później.",
            icon="🤖"
        )


if __name__ == "__main__":
    main()
