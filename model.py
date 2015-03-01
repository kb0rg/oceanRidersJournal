from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

import re

"""
using ratings webapp for reference here. see "deployed" branch on HB github
https://github.com/hackbrightacademy/ratings/blob/deployed/judgemental.py
"""

engine = create_engine("sqlite:///surf_journal.db", echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

### Class declarations go here
Base = declarative_base()

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key = True)

    date_time_start = Column(DateTime, nullable = False)
    date_time_end = Column(DateTime, nullable = False)

    ## link this to ID in loc table?
    beach_name = Column(String(64), nullable = False) # relate to 

    # todo LATER: add input field for more specific location name or nickname (ie Patch or Noriega)
    # spot_name = Column(String(64), nullable = True)

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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String(64), nullable = False)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    firstname = Column(String(64), nullable = True)
    lastname = Column(String(64), nullable = True)
    home_region = Column(String(64), nullable = True)

    def __repr__(self):
        return "%d, %s, %s, %s, %s" % (self.id, self.username, self.firstname, self.lastname, self.home_region)

class Location(Base):
    """
    for temp reference: seed file is using these fields:
    Region|Country|State or Province|County|Beach Name|MSW_ID of closest location|T or F msw id exists for this actual location|lat|lon|
    """

    __tablename__ = "locations"

    id = Column(Integer, primary_key = True)
    # general location name, ie Bolinas or Ocean Beach
    beach_name = Column(String(64), nullable = False)

    # human-readable location
    region = Column(String(64), nullable = False)
    country = Column(String(64), nullable = False)
    state_or_prov = Column(String(64), nullable = False)
    county = Column(String(64), nullable = False)

    # API - readable location
    msw_id = Column(Integer, nullable = True)
    msw_unique_id_exists = Column(Boolean, nullable = True)

    # lat long for reloacting later (in case API changes)
    # should these be left as strings, or converted to another format?
    # STRING FOR NOW
    lat = Column(String(64), nullable = False)
    long = Column(String(64), nullable = False)
    # lat = Column(Float, nullable = False)
    # long = Column(Float, nullable = False)

    def __repr__(self):
        return "<Location: %d, %s, MSW (or nearest) ID: %d >"%(self.id, self.beach_name, self.msw_id) 

### End class declarations

"""
deprecated this function in favor of scoped session (threadsafe)
(see top of file)
# def connect():
#     global ENGINE
#     global Session
#     ENGINE = create_engine("sqlite:///surf_journal.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()
"""

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