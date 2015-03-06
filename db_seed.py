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
            region, country, state_or_prov, county, beach_name, msw_id, msw_unique_id_exists, msw_beach_name, lat, long = row

            # convert string to Boolean:
            if msw_unique_id_exists == "T":
                msw_unique_id_exists = True
            else:
                msw_unique_id_exists = False

            m = model.Location(region=region, country=country, state_or_prov=state_or_prov,
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


def load_boards(session):

    """
    populates boards table from seed file.
    seed file is using these fields:
    user|nickname|type|lenght_ft|lenght_in|shaper|model|fins
    """

    with open("db_seed_data/seed_boards") as f:

        reader = csv.reader(f, delimiter="|")
        for row in reader:
            print row

            user, nickname, type, length_ft, length_in, shaper, model, fins = row

            user = int(user)
            print "user type: " + type(user)

            length_ft = int(length_ft)
            print "length_ft type: " + type(length_ft)

            length_in = int(length_in)
            print "length_in type: " + type(length_in)


            m = model.Board(user=user, nickname=nickname, type=type, 
                            length_ft=length_ft, length_in=length_in,
                            shaper=shaper, model=model, fins=fins)
            session.add(m)
         
        ## based on func from ratings app, not sure about the use of try/ except
        # try:
        #     session.commit()
        # except:
        #     session.rollback()

        session.commit()

 

def main(session):
    # call each of the load_* functions with the session as an argument
    print "Seeding the tables..."
    load_users(session)
    load_locations(session)
    load_boards(session)

    print "Done!"
 
if __name__ == "__main__":
    s = model.session
    main(s)