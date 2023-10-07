from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from infra.database import Database
from infra.declarative_base import Base
from services.end_user import ServiceEndUser
from services.persistence import ServicePersistence


def boot(filename: str) -> Session:
    engine = create_engine(f"sqlite:///{filename}.sqlite")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@dataclass
class App:
    end_user: ServiceEndUser
    persitence: ServicePersistence


def start_application() -> App:
    db = Database.init(session=boot("air_quality_db"))
    return App(end_user=ServiceEndUser(db=db), persitence=ServicePersistence(db=db))
