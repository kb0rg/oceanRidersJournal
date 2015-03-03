from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os
import requests
import json
from datetime import datetime

# more imports from ratings app seed script
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
	Region|Country|State or Province|County|Beach Name|MSW_ID of closest location|T or F msw id exists for this actual location|lat|lon|
	"""

	with open("db_seed_data/seed_locations") as f:

		reader = csv.reader(f, delimiter="|")
		for row in reader:
			region, country, state_or_prov, county, beach_name, msw_id, msw_unique_id_exists, lat, long = row

			if msw_unique_id_exists == "T":
				msw_unique_id_exists = True
			else:
				msw_unique_id_exists = False

			m = model.Location(region=region, country=country, state_or_prov=state_or_prov,
				county=county, beach_name = beach_name, 
				msw_id=msw_id, msw_unique_id_exists=msw_unique_id_exists,
				lat=lat, long=long)
			session.add(m)
		 
 		## based on func from ratings app, not sure about the use of try/ except
		# try:
		#     session.commit()
		# except:
		#     session.rollback()

		session.commit()

"""
unused stuff from ratings app, for ref if needed:

# ## based on func from ratings app, not sure about the use of try/ except
# def load_entries(session):
#     with open("db_seed_data/seed_entries") as f:
#         reader = csv.reader(f, delimiter="|")
#         for row in reader:
#             # username, firstname, lastname, home_region = row
#             # u = model.User(username=username, email=None, password=None, firstname=firstname, lastname=lastname, home_region=home_region)
#             # session.add(u)
#             ## this might be useful for entries table
#             # if not release_date:
#             #     continue
#             # release_date = datetime.datetime.strptime(release_date, "%d-%b-%Y")

#         # try:
#         #     session.commit()
#         # except sqlalchemy.exc.IntegrityError, e:
#         #     session.rollback()
		
#         session.commit()

## from ratings app, this function does NOT use try/ except
# def load_ratings(session):
#     with open("db_seed_data/u.data") as f:
#         reader = csv.reader(f, delimiter="\t")
#         for row in reader:
#             user_id = int(row[0])
#             movie_id = int(row[1])
#             rating = int(row[2])
			 
#             r = model.Rating(user_id=user_id, movie_id=movie_id, rating=rating)
#             session.add(r)
#         session.commit()
 
"""

def main(session):
	# call each of the load_* functions with the session as an argument
	load_users(session)
	load_locations(session)
 
if __name__ == "__main__":
	s = model.session
	main(s)