from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


class RLTDatabase:
    def __init__(self, database):
        self.base = automap_base()
        self.engine = create_engine(f"sqlite:///{database}")
        self.base.prepare(autoload_with=self.engine)

        self.drivers = self.base.classes.Drivers

    def getDrivers(self):
        ret = []

        with Session(self.engine) as session:
            for driver in session.query(self.drivers).all():
                retDriver = driver.__dict__
                if driver.nationalities:
                    retDriver['nationalities']=driver.nationalities.__dict__
                ret.append(retDriver)

        return ret
