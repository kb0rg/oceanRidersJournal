from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os
import requests
import json
from datetime import datetime

# more imports from ratings app seed script
# not sure if all are in use. clean up if not.
import csv
import sqlalchemy.exc
import re
 
def load_users(session):

    """
    populates users table from seed file.
    seed file is using these fields:
    id|username|email|password|firstname|lastname|home region
    """
    
    with open("db_seed_data/seed_users") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            id, username, email, password, firstname, lastname, home_region = row
            id = int(id)
            
            u = model.User(id=id,username=username, email=email, password=password, 
                            firstname=firstname, lastname=lastname, home_region=home_region)
            session.add(u)
        
        session.commit()
        print "users table seeded."

def load_locations(session):

    """
    populates locations table from seed file.
    seed file is using these fields:
    Region|Country|State or Province|County|Beach Name|MSW_ID used|msw id exists for this location?|
    Beach Name of closest MSW data|lat|lon|
    """

    with open("db_seed_data/seed_locations") as f:

        reader = csv.reader(f, delimiter="|")
        for row in reader:
            id, region, country, state_or_prov, county, beach_name, msw_id, msw_unique_id_exists, msw_beach_name, lat, long = row

            # convert string to Boolean:
            if msw_unique_id_exists == "T":
                msw_unique_id_exists = True
            else:
                msw_unique_id_exists = False

            m = model.Location(
                id=id, region=region, country=country, state_or_prov=state_or_prov,
                county=county, beach_name = beach_name, 
                msw_id=msw_id, msw_unique_id_exists=msw_unique_id_exists, msw_beach_name=msw_beach_name,
                lat=lat, long=long
                )
            session.add(m)

        session.commit()
        print "locations table seeded."



def load_boards(session):

    """
    populates boards table from seed file.
    seed file is using these fields:
    user|nickname|type|length_ft|length_in|shaper|shape(model)|fins
    """

    with open("db_seed_data/seed_boards") as f:

        reader = csv.reader(f, delimiter="|")
        for row in reader:
            print row

            user_id, nickname, category, length_ft, length_in, shaper, shape, fins = row

            m = model.Board(user_id=user_id, nickname=nickname, category=category,
                            length_ft=length_ft, length_in=length_in,
                            shaper=shaper, shape=shape, fins=fins)
            session.add(m)

        session.commit()
        print "boards table seeded."

def load_entries(session):

    """
    populates entries table from seed file.

    seed file is using these fields:

    user_id|datetime start|loc_id|spot_name|go_out|
    swell1_ht|swell1_per|swell1_dir_deg|swell1_arrow_deg|swell1_dir_comp|
    wind_speed|wind_gust|wind_arrow_deg|
    board_id|board_pref|board_notes|buddy|gen_notes
    rate_wave_challenge|rate_wave_fun|rate_crowd_den|rate_crowd_vibe|rate_overall_fun

    (using msw api data collected for past dates from another app, only rounded degress available)
    """
    
    with open("db_seed_data/seed_entries") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:

            print row

            (user_id, datetime_start, loc_id, spot_name, go_out,
            swell1_ht, swell1_per, swell1_dir_deg_global, swell1_arrow_deg, swell1_dir_comp, 
            wind_speed, wind_gust, wind_arrow_deg, 
            board_id, board_pref, board_notes, buddy_name, gen_notes,
            rate_wave_challenge, rate_wave_fun, rate_crowd_den, rate_crowd_vibe,
            rate_overall_fun) = row
            
            ## convert string to datetime
            date_time_start = datetime.strptime(datetime_start, "%Y-%m-%d %H:%M")
            ## temp using same start and end time. 
            date_time_end = date_time_start

            ## convert string to Boolean:
            if go_out == "T":
                go_out = True
            else:
                go_out = False

            swell1_dir_deg_global = float(swell1_dir_deg_global)
            ## convert from global deg back to deg as msw would provide
            swell1_dir_deg_msw = (swell1_dir_deg_global - 180)%360
            print "swell1_dir_deg_global: ", swell1_dir_deg_global
            print "swell1_dir_deg_msw: ", swell1_dir_deg_msw


            u = model.Entry(user_id=user_id, date_time_start=date_time_start, date_time_end=date_time_end, 
                            loc_id=loc_id, spot_name=spot_name, go_out=go_out,
                            swell1_ht=swell1_ht, swell1_per=swell1_per, swell1_dir_deg_global=swell1_dir_deg_global,
                            swell1_dir_deg_msw=swell1_dir_deg_msw, swell1_arrow_deg=swell1_arrow_deg, swell1_dir_comp=swell1_dir_comp,
                            wind_speed=wind_speed, wind_gust=wind_gust, wind_arrow_deg=wind_arrow_deg,
                            board_id=board_id, board_pref=board_pref, board_notes=board_notes,
                            buddy_name=buddy_name, gen_notes=gen_notes,
                            rate_wave_challenge=rate_wave_challenge, rate_wave_fun=rate_wave_fun,
                            rate_crowd_den=rate_crowd_den, rate_crowd_vibe=rate_crowd_vibe,
                            rate_overall_fun=rate_overall_fun)
            session.add(u)
        
        
        session.commit()
        print "entries table seeded." 


def main(session):
    # call each of the load_* functions with the session as an argument
    print "Seeding the tables..."
    
    load_users(session)
    load_locations(session)
    load_boards(session)
    load_entries(session)

    print "Done!"


if __name__ == "__main__":
    session = model.session
    main(session)
