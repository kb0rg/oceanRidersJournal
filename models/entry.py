from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from models import Base

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
        return "%d, %d, %s, %s, %s" % (self.id, self.loc_id, self.spot_name,
            self.board.nickname, self.board_pref)
