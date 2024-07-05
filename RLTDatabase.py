from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


class RLTDatabase:
    def __init__(self, database):
        self.base = automap_base()
        self.engine = create_engine(f"sqlite:///{database}")
        self.base.prepare(autoload_with=self.engine)

        self.drivers = self.base.classes.Drivers
        self.nationalities = self.base.classes.Nationalities

    def getNationalities(self):
        ret = []

        with Session(self.engine) as session:
            for nationality in session.query(self.nationalities).all():
                ret.append(nationality.__dict__)

        return ret

    def getDrivers(self):
        ret = []

        with Session(self.engine) as session:
            for driver in session.query(self.drivers).all():
                ret.append(driver.__dict__)

        return ret
