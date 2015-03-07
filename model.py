from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, Integer, Float, String, DateTime, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

# not sure if I need regex -- was used in one of the examples I may not be using
# import re

engine = create_engine("sqlite:///db_surfjournal.db", echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

### Class declarations go here
Base = declarative_base()

class User(Base):
    """
    makes a row in the users table.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String(64), nullable = False)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    firstname = Column(String(64), nullable = True)
    lastname = Column(String(64), nullable = True)
    """
    todo region: tie this to loc table?
    """
    home_region = Column(String(64), nullable = True)

    def __repr__(self):
        return "%d, %s, %s, %s, %s" % (self.id, self.username, self.firstname, self.lastname, self.home_region)

class Location(Base):
    """
    makes a row in the locations table.
    """
    __tablename__ = "locations"

    id = Column(Integer, primary_key = True)
    # general location name, ie Bolinas or Ocean Beach
    beach_name = Column(String(64), nullable = False)

    # human-readable location info:
    # (allowing for future expansion beyond CA)
    region = Column(String(64), nullable = False)
    country = Column(String(64), nullable = False)
    state_or_prov = Column(String(64), nullable = False)
    county = Column(String(64), nullable = False)

    # API-readable location info:
    msw_id = Column(Integer, nullable = True)
    msw_unique_id_exists = Column(Boolean, nullable = True)
    # which beach's MSW report is being displayed:
    msw_beach_name = Column(String(64), nullable = False)

    """
    todo latlong:
    should these be left as strings, or converted to another format?
    # USING STRING FOR NOW
    """
    # lat long for reloacting later (in case API changes)
    # (or in case I wanna do something fancy)
    lat = Column(String(64), nullable = False)
    long = Column(String(64), nullable = False)
    # lat = Column(Float, nullable = False)
    # long = Column(Float, nullable = False)

    def __repr__(self):
        return "<Location: %d, %s, MSW (or nearest) ID: %d >"%(self.id, self.beach_name, self.msw_id) 

class Board(Base):
    """
    makes a row in the boards table.
    """
    __tablename__ = "boards"

    id = Column(Integer, primary_key = True)

    """
    TODO boards general:
    --> ?? make field to note if board is borrowed/ whose it is?
    (for purposes of db, each board has only one user)
    """
    """
    todo board user: 
    -> need to get this from login info
    """
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User",
        backref=backref("boards", order_by=id))

    nickname = Column(String(64), nullable = False)
    # changed "type" to "category" -- reserved
    category = Column(String(64), nullable = False)
    length_ft = Column(Integer, nullable = True)
    length_in = Column(Integer, nullable = True)
    shaper = Column(String(64), nullable = True)
    # changed "model" to "shape" -- reserved
    shape = Column(String(64), nullable = True)
    fins = Column(String(64), nullable = True)

    def __repr__(self):
        return "<Board: %d, %s, %s %d\' %d\">"%(self.id, self.nickname, self.shaper, self.length_ft, self.length_in) 

class Entry(Base):
    """
    makes a row in the entries table.
    """
    __tablename__ = "entries"

    # automatically generated when instance is created
    id = Column(Integer, primary_key = True)

    """
    todo entry user: 
    -> should get this from login info
    """
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User",
        backref=backref("entries", order_by=id))

    """
    todo entry datetime:
    -> set up form to make inputs, not just use datetime.now 
    --> format in a way MSW can read, or do that conversion at API call?
    """
    date_time_start = Column(DateTime, nullable = False)
    date_time_end = Column(DateTime, nullable = False)

    """
    todo entry location:
    -> need to explicity link this to ID in loc table?
    -> make not nullable? or give warning in form that if not provided, 
    no weather info will be given?
    -> make dropdown in form that reads from loc table
    # todo LATER: add input field for more specific spot_name /nickname (ie Patch or Noriega)
    """
    ## for working with temp beach name input text field:
    # beach_name = Column(String(64), nullable = False)

    # beach from location ID (uses loc table's loc_id)
    loc_id = Column(Integer, ForeignKey('locations.id'))
    spot_name = Column(String(64), nullable = True)

    loc = relationship("Location",
        backref=backref("entries", order_by=id))

    """
    todo entry board:
    --> make ability to get board from quiver in form
    LATER:
    --> ?? (entry has only one board, or multiple?)
    --> ? make ability to add to quiver?
    """
    board_id = Column(Integer, ForeignKey('boards.id'))

    board_pref = Column(String(64), nullable = False)
    board_notes = Column(String(64), nullable = True)

    board = relationship("Board",
        backref=backref("entries", order_by=id))

    """
    todo API:
    ---> data model question:
    should I pull API specifics out of entry table, and make an API_info table with entry_id keys?
    -> add swell2 and swell3?
    -> add tide height and state
    -> add wind speed and direction
    -> add air and water temp
    -> remove dirComp if function converts to global degrees
    """
    ## pull swell1 data from apis and add to entry
    swell1_ht = Column(Float, nullable = True)
    swell1_per = Column(Integer, nullable = True)
    swell1_dir_deg = Column(Float, nullable = True)
    swell1_dir_comp = Column(String(4), nullable = True)

    ## pull wind data from apis and add to entry
    wind_speed = Column(Float, nullable = True)
    wind_dir_deg = Column(Float, nullable = True)
    wind_dir_comp = Column(String(4), nullable = True)
    wind_unit = Column(String(10), nullable = True)

    ## pull swell2 and 3, wind, and temp data from MSW api and add to entry
    ## tide data from .... api?  and add to entry

    ## pull water and air temp from API 
    temp_h2o = Column(Integer, nullable = True)
    temp_air = Column(Integer, nullable = True)

    def __repr__(self):
        return "%d, %d, %s, %s, %s" % (self.id, self.loc_id, self.spot_name, self.board.nickname, self.board_pref)


### End class declarations


def main():
    """In case we need this for something"""
    
    print "\nWelcome to your surfjournal's model.\n" + \
    "I suspect you are here to rebuild the database schema.\n" + \
    "AGAIN\n" + \
    "Here we go.\n"
    print "*" * 13, "\n"
    print "To proceed rebuilding the schema, run the following code:\n" + \
    "engine = create_engine(\"sqlite:///db_surfjournal.db\", echo=True)\n" + \
    "Base.metadata.create_all(engine)\n"
    print "*" * 13, "\n"
    print "Otherwise please exit now."


if __name__ == "__main__":
    main()


"""
NOTE!!!!
*****
when db needs to be deleted and rebuilt:

1) run model.py in interactive mode (while in venv):
python -i model.py
2) enter this in interactive python shell 
engine = create_engine("sqlite:///db_surfjournal.db", echo=True)
Base.metadata.create_all(engine)

"""