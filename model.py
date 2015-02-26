from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None 

"""
using ratings webapp for reference here. see "deployed" branch on HB github
https://github.com/hackbrightacademy/ratings/blob/deployed/judgemental.py
"""
### Class declarations go here
Base = declarative_base()

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key = True)

    date_time_start = Column(DateTime, nullable = False)
    date_time_end = Column(DateTime, nullable = False)

    beach_name = Column(String(64), nullable = False)
    board_name = Column(String(64), nullable = True)
    board_pref = Column(String(64), nullable = True)

    # user_name = Column(String(64), nullable = False)
    # location = Column(String(64), nullable = False)
    # # date = (DateTime, nullable = False)

    # board = Column(String(64), nullable = True)

    # # relate user_name to users table: get via id of currently logged-in user
    # # relate location to locations table: get from and/or add to?
    # # pull swell, wind, and tide data from apis and add to entry
    # # relate board to bords table: get from and/or add to quiver?

    def __repr__(self):
        return "%d, %s, %s" % (self.id, self.beach_name, self.board_pref)


class Location(Base):
    """docstring will go here."""

    __tablename__ = "locations"

    id = Column(Integer, primary_key = True)
    # general location name, ie Bolinas or Ocean Beach
    beach_name = Column(String(64), nullable = False) 
    # specific location name or nickname, ie Patch or Noriega
    spot_name = Column(String(64), nullable = True)
    lat = Column(Float, nullable = False)
    long = Column(Float, nullable = False)

    def __repr__(self):
        return "<Location: %d, %s, %s>"%(self.id, self.beach_name, self.spot_name) 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = False)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)

    def __repr__(self):
        return "%d, %s, %s" % (self.id, self.email, self.password)


### End class declarations

def connect():
    global ENGINE
    global Session
    ENGINE = create_engine("sqlite:///surf_journal.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()



"""
NOTE!!!! DO NOT FORGET THIS!!!!
*****
in the event that db needs to be deleted and rebuilt:

remember to do this in interactive python shell - -while in venv
(python -i model.py)

engine = create_engine("sqlite:///surf_journal.db", echo=True)
Base.metadata.create_all(engine)

"""