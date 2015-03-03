from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os
import requests
import json
from datetime import datetime


# todo: set python variables (AS CONSTANTS?) to access variables in keys.sh, EX:
#NAME_CONSUMER_KEY=os.environ["NAME_CONSUMER_KEY"]
# remember to source key.sh to set tokens as env variables for that session.

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of kborg's surf journal site.
    It will contain some kind of awesome background image.
    And a logo. And maybe some inspirational text. 
    But first I have to build the rest of the damn site."""
    return render_template("index.html")

@app.route("/about")
def list_entriesInfo():
    """temp page while building? or turn into intro/ about page?
    currently a list of all of the potential info that can be collected"""

    return render_template("about.html")

@app.route("/addEntryForm")
def go_to_addEntry():
    """put everything from this form into the db"""


    # need jinja loop that reads loc table. 
    # query db for all locations 
    # grab all locations as objects, pass those as array to template
    # will have ALL attributes of each loc, can pick and choose 
    #  on the html side


    return render_template("surf_entry_add.html")


    ### clean this up -- api notes in wrong place
    # noaa_url = "http://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20130101%2010:00&end_date=20130101%2010:24&station=8454000&product=water_level&datum=mllw&units=metric&time_zone=gmt&application=web_services&format=json"
    # r = requests.get(noaa_url)
    # spitcast_tide_url = "http://api.spitcast.com/api/county/tide/san-francisco/"
    # r = requests.get(spitcast_tide_url)
    # return json.dumps(r.json())

    # # json.load vs json.loads, json.dumps, Flask.jsonify
    # s = model.Session(date, time,)
    # model.session.add

@app.route("/addEntry")
def add_entry():
    """receive input from add_entry form, commit to db, then list all existing entries."""

    ### TODO -- ask about this!
    ## this breaks now that I switched model to scoped sessions.
    # session = model.connect()
    ## try this?
    session = model.session
    ## this works! but should I put the session somewhere else, like in main?


    ## remove date and time inputs for now. 
    # entry_date = request.args.get("entry_date")
    # start_time = request.args.get("start_time")
    # end_time = request.args.get("end_time")
    # date_time_start = datetime.strptime((entry_date + " " + start_time), "%Y-%m-%d %H:%M")
    # date_time_end = datetime.strptime((entry_date + " " + end_time), "%Y-%m-%d %H:%M")

    ## temporarily rewire start and end times to datetime.now()
    date_time_start = datetime.now()
    date_time_end = datetime.now()

    print "\n" * 3, "date_time_start: ", date_time_start, "date_time_end: ", date_time_end

    # queries from user
    beach_name = request.args.get("beach_name")
    board_name = request.args.get("board_name")
    board_pref = request.args.get("board_pref")
    # add location
    # get location id from locations table
    # make API call using location id
    # parse API json, grab and bind to var the piece that I want
    
    # add piece from api to this instance of model.Entry
    new_entry = model.Entry(date_time_start = date_time_start, date_time_end=date_time_end, beach_name = beach_name, board_name=board_name, board_pref = board_pref)
    session.add(new_entry)
    session.commit()
    # entry_list = session.query(model.Entry).all()
    # TODO -- want to filer entries by date. filter_by seems to want specific entry data. is there a sort?
    # look below at show_melon( get_melon_by_id())?
    return redirect("/entries")



@app.route("/entries")
def list_entries():
    """displays all of the surf entries logged so far"""

    session = model.session
    entry_list = session.query(model.Entry).all()

    return render_template("surf_entries_summary.html", entries = entry_list)

### use this as ref for making "entry details" happen?
# @app.route("/melon/<int:id>")
# def show_melon(id):
#     """This page shows the details of a given melon, as well as giving an
#     option to buy the melon."""
#     melon = model.get_melon_by_id(id)
#     print melon
#     return render_template("melon_details.html",
#                   display_melon = melon)

@app.route("/board_quiver")
def edit_quiver():
    """display and edit existing quiver of boards"""
    # melons = model.get_melons()
    # return render_template("surf_entries.html",
    #                        session_list = entries)
    return render_template("board_quiver.html")    


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    return "Oops! This needs to be implemented"

"""
todo: log-in. reference code from ratings below. need to get user table set up before proceeding?
"""

# @app.route("/login", methods=["POST"])
# def login():
#     email = request.form['email']
#     password = request.form['password']

#     try:
#         user = db_session.query(User).filter_by(email=email, password=password).one()
#     except:
#         flash("Invalid username or password", "error")
#         return redirect(url_for("index"))

#     session['user_id'] = user.id
#     return redirect(url_for("display_search"))

# @app.route("/register", methods=["POST"])
# def register():
#     email = request.form['email']
#     password = request.form['password']
#     existing = db_session.query(User).filter_by(email=email).first()
#     if existing:
#         flash("Email already in use", "error")
#         return redirect(url_for("index"))

#     u = User(email=email, password=password)
#     db_session.add(u)
#     db_session.commit()
#     db_session.refresh(u)
#     session['user_id'] = u.id 
#     return redirect(url_for("display_search"))

# @app.route("/logout")
# def logout():
#     del session['user_id']
#     return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
