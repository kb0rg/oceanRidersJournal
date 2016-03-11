# database model for surf journal
import os
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///db_surfjournal.db")

engine = create_engine(DATABASE_URL, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

## Class declarations:

Base = declarative_base()

class User(Base):
    """
    makes a row in the users table.
    """
    __tablename__ = "users"

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    ## ID is automatically generated when instance is created
    id = Column(Integer, primary_key = True)
    username = Column(String(64), nullable = False)
    email = Column(String(64), nullable = False)
    password = Column(String(64), nullable = False)

    ## optional, for possible future use
    firstname = Column(String(64), nullable = True)
    lastname = Column(String(64), nullable = True)
    home_region = Column(String(64), nullable = True)

    def __repr__(self):
        return "%d, %s, %s, %s, %s" % (self.id, self.username, self.firstname, self.lastname, self.home_region)


class Board(Base):
    """
    makes a row in the boards table.
    """
    __tablename__ = "boards"

    ## automatically generated when instance is created
    id = Column(Integer, primary_key = True)

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User",
        backref=backref("boards", order_by=id))

    ## required fields: 
    nickname = Column(String(64), nullable = False)
    ## type of board (long, short, fish, etc)
    ## used in add entry dropdown
    category = Column(String(64), nullable = False)

    ## optional fields:
    length_ft = Column(Integer, nullable = True)
    length_in = Column(Integer, nullable = True)
    shaper = Column(String(64), nullable = True)
    ## modelname or desciption of board
    shape = Column(String(64), nullable = True)
    fins = Column(String(64), nullable = True)

    def __repr__(self):
        return "<Board: %d, %s, %s %s>"%(self.id, self.nickname, self.shaper, self.shape) 

class Entry(Base):
    """
    makes a row in the entries table.
    """
    __tablename__ = "entries"

    ## automatically generated when instance is created
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))

    ## Entry/ Yser tables relationship
    user = relationship("User",
        backref=backref("entries", order_by=id))

    date_time_start = Column(DateTime, nullable = False)
    date_time_end = Column(DateTime, nullable = False)
    ## whether surfed or just observed (for future feature expansion)
    go_out = Column(String(1), nullable = False)

    ## loc_id grabbed from dropdown (uses loc table's loc_id)
    loc_id = Column(Integer, ForeignKey('locations.id'))
    ## more specific/ desciptive location from user input
    spot_name = Column(String(64), nullable = True)

    ## Entry/ Location tables relationship
    loc = relationship("Location",
        backref=backref("entries", order_by=id))

    ## board_id grabbed from dropdown (uses board table's id)
    board_id = Column(Integer, ForeignKey('boards.id'))
    board_pref = Column(String(64), nullable = False)
    board_notes = Column(String(64), nullable = True)

    ## Entry/ Board tables relationship
    board = relationship("Board",
        backref=backref("entries", order_by=id))

    ## pull swell1 data from apis and add to entry
    swell1_ht = Column(Float, nullable = True)
    swell1_per = Column(Integer, nullable = True)
    swell1_dir_deg_msw = Column(Float, nullable = True)
    swell1_dir_deg_global = Column(Float, nullable = True)
    swell1_dir_comp = Column(String(4), nullable = True)
    swell1_arrow_deg = Column(Integer, nullable = True)

    ## pull wind data from apis and add to entry
    wind_speed = Column(Float, nullable = True)
    wind_gust = Column(Float, nullable = True)
    wind_dir_deg = Column(Float, nullable = True)
    wind_dir_comp = Column(String(4), nullable = True)
    wind_unit = Column(String(10), nullable = True)
    wind_arrow_deg = Column(Integer, nullable = True)

    ## water and air pulled temp from API (for future feature expansion)
    temp_h2o = Column(Integer, nullable = True)
    temp_air = Column(Integer, nullable = True)

    ## subjective user ratings
    rate_wave_challenge = Column(Integer, nullable = True)
    rate_wave_fun = Column(Integer, nullable = True)
    rate_crowd_den = Column(Integer, nullable = True)
    rate_crowd_vibe = Column(Integer, nullable = True)
    rate_overall_fun = Column(Integer, nullable = True)

    ## additional user inputs
    buddy_name = Column(String(64), nullable = True)
    ## general notes about the session
    gen_notes = Column(String(140), nullable = True)


    def __repr__(self):
        return "%d, %d, %s, %s, %s" % (self.id, self.loc_id, self.spot_name, self.board.nickname, self.board_pref)


## End class declarations


def main():
    """
    directions for rebuilding db when model is called directly.
    """
    
    print "\nWelcome to kborg's surfjournal model.\n"
    print "*" * 13, "\n"
    print "To proceed rebuilding the schema, run the following code:\n" + \
    "engine = create_engine(\"sqlite:///db_surfjournal.db\", echo=True)\n" + \
    "Base.metadata.create_all(engine)\n"
    print "*" * 13
    print "When complete, exit python and run python db_seed.py in the terminal."
    print "*" * 13, "\n"
    print "Otherwise please exit now."


if __name__ == "__main__":
    main()

"""
NOTE!!!!
*****
when db needs to be deleted and rebuilt,
run model.py in interactive mode (while in virtual env):
python -i model.py
"""
