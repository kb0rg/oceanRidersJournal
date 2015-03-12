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
    username|firstname|lastname|home region
    """
    
    with open("db_seed_data/seed_users") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            username, firstname, lastname, home_region = row
            
            u = model.User(username=username, email=None, password=None, firstname=firstname, lastname=lastname, home_region=home_region)
            session.add(u)
        
        ## based on func from ratings app, not sure about the use of try/ except
        # try:
        #     session.commit()
        # except sqlalchemy.exc.IntegrityError, e:
        #     session.rollback()
        
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
            loc_id, region, country, state_or_prov, county, beach_name, msw_id, msw_unique_id_exists, msw_beach_name, lat, long = row

            # convert string to Boolean:
            if msw_unique_id_exists == "T":
                msw_unique_id_exists = True
            else:
                msw_unique_id_exists = False

            m = model.Location(loc_id=loc_id, region=region, country=country, state_or_prov=state_or_prov,
                county=county, beach_name = beach_name, 
                msw_id=msw_id, msw_unique_id_exists=msw_unique_id_exists, msw_beach_name=msw_beach_name,
                lat=lat, long=long)
            session.add(m)
         
        ## based on func from ratings app, not sure about the use of try/ except
        # try:
        #     session.commit()
        # except:
        #     session.rollback()

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
            # print "user: ", type(user)
            # print "changing user to int..."
            # user = int(user)
            # print "user: ", type(user)

            # print "length_ft: ", length_ft, type(length_ft)
            # length_ft = int(length_ft)
            
            # print "length_ft: ", length_ft, type(length_ft)
            # length_in = int(length_in)

            m = model.Board(user_id=user_id, nickname=nickname, category=category,
                            length_ft=length_ft, length_in=length_in,
                            shaper=shaper, shape=shape, fins=fins)
            session.add(m)

        session.commit()
        print "boards table seeded."

 
def main(session):
    # call each of the load_* functions with the session as an argument
    print "Seeding the tables..."
    
    load_users(session)
    load_locations(session)
    # load_boards(session)

    print "Done!"
 
def load_entries(session):

    """
    populates entries table from seed file.
    seed file is using these fields:
    user_id|datetime start|loc_id|spot_name|swell1_ht|swell1_per|swell1_arrow_deg|
            swell1_dir_comp|wind_speed|wind_gusts|wind_arrow_deg|board_id|board_pref|board_notes

    (using msw api data collected for past dates, only rounded degress available. need to convert here)
    """
    
    with open("db_seed_data/seed_entries") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            user_id, datetime_start, loc_id, spot_name, swell1_ht, swell1_per, swell1_arrow_deg,
            swell1_dir_comp, wind_speed, wind_gusts, wind_arrow_deg, board_id, board_pref, board_notes = row
            
            u = model.Entry(username=username, email=None, password=None, firstname=firstname, lastname=lastname, home_region=home_region)
            session.add(u)
        
        ## based on func from ratings app, not sure about the use of try/ except
        # try:
        #     session.commit()
        # except sqlalchemy.exc.IntegrityError, e:
        #     session.rollback()
        
        session.commit()
        print "users table seeded." 
if __name__ == "__main__":
    session = model.session
    main(session)