import logging

from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from models import base
from models.location import Location

from services import api_msw as msw

class Entry(base.Base):

    """
    makes a row in the entries table.
    """
    __tablename__ = "entries"

    ## automatically generated when instance is created
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))

    ## Entry/ Yser tables relationship
    user = relationship("User",
        backref = backref("entries", order_by = id))

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
        backref = backref("entries", order_by = id))

    ## board_id grabbed from dropdown (uses board table's id)
    board_id = Column(Integer, ForeignKey('boards.id'))
    board_pref = Column(String(64), nullable = False)
    board_notes = Column(String(64), nullable = True)

    ## Entry/ Board tables relationship
    board = relationship("Board",
        backref = backref("entries", order_by = id))

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

    @classmethod
    def get_all_for_user(cls, user):
        return base.session.query(cls).filter_by(user_id= user)

    @classmethod
    def get_by_id(cls, entry_id):
        return base.session.query(cls).filter_by(id = entry_id).one()

    @classmethod
    def from_form_data(cls, data_dict):

        user_id = data_dict.get("user_id")
        date_time_start = data_dict.get("date_time_start")
        date_time_end = data_dict.get("date_time_end")

        loc_id = data_dict.get("loc_id")
        spot_name = data_dict.get("spot_name")
        go_out = data_dict.get("go_out")
        buddy_name = data_dict.get("buddy_name")
        board_id = data_dict.get("board_id")
        board_pref = data_dict.get("board_pref")
        board_notes = data_dict.get("board_notes")
        rate_overall_fun = data_dict.get("rate_overall_fun")
        rate_wave_challenge = data_dict.get("rate_wave_challenge")
        rate_wave_fun = data_dict.get("rate_wave_fun")
        rate_crowd_den = data_dict.get("rate_crowd_den")
        rate_crowd_vibe = data_dict.get("rate_crowd_vibe")
        gen_notes = data_dict.get("gen_notes")

        # TODO: Abstract all MSW data processing to the api_msw module
        ## get msw_id from db for this loc
        msw_id = Location.get_by_id(loc_id).msw_id

        ## make API call for swell1 info using msw_id
        msw_swell1_json_obj = msw.get_swell_1(msw_id)

        swell1_ht = msw_swell1_json_obj['swell']['components']['primary']['height']
        swell1_per = msw_swell1_json_obj['swell']['components']['primary']['period']
        swell1_dir_deg_msw = msw_swell1_json_obj['swell']['components']['primary']['direction']
        swell1_dir_comp = msw_swell1_json_obj['swell']['components']['primary']['compassDirection']
        swell1_dir_deg_global = msw.get_global_degrees(swell1_dir_deg_msw)
        swell1_arrow_deg = msw.get_arrow_degrees(swell1_dir_deg_global)

        ## make API call for wind info using msw_id
        msw_wind_json_obj = msw.get_wind(msw_id)
        logging.debug('msw_wind_json_obj: {}'.format(msw_wind_json_obj))

        ## parse msw response object for wind info into desired attr
        wind_speed = msw_wind_json_obj['wind']['speed']
        wind_gust = msw_wind_json_obj['wind']['gusts']
        wind_dir_deg = msw_wind_json_obj['wind']['direction']
        wind_dir_comp = msw_wind_json_obj['wind']['compassDirection']
        wind_unit = msw_wind_json_obj['wind']['unit']
        wind_arrow_deg = msw.get_arrow_degrees(wind_dir_deg)

        new_entry = Entry(
            user_id = user_id,
            date_time_start = date_time_start,
            date_time_end=date_time_end,
            loc_id = loc_id,
            spot_name = spot_name,
            go_out = go_out,
            buddy_name = buddy_name,
            swell1_ht = swell1_ht,
            swell1_per = swell1_per,
            swell1_dir_deg_msw = swell1_dir_deg_msw,
            swell1_dir_comp = swell1_dir_comp,
            swell1_dir_deg_global = swell1_dir_deg_global,
            swell1_arrow_deg = swell1_arrow_deg,
            wind_speed = wind_speed,
            wind_gust= wind_gust,
            wind_dir_deg = wind_dir_deg,
            wind_dir_comp = wind_dir_comp,
            wind_unit = wind_unit,
            wind_arrow_deg = wind_arrow_deg,
            board_id = board_id,
            board_pref = board_pref,
            board_notes = board_notes,
            rate_overall_fun = rate_overall_fun,
            rate_wave_challenge = rate_wave_challenge,
            rate_wave_fun = rate_wave_fun,
            rate_crowd_den = rate_crowd_den,
            rate_crowd_vibe = rate_crowd_vibe,
            gen_notes = gen_notes,
            )

        return new_entry

