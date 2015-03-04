from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os
import requests
import json
from datetime import datetime


"""
todo:
app.secret.key = do I need to change this, or hide it in a secrets file?
"""
app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

"""
remember to source keys .sh file to set tokens as env variables for each terminal session.
"""

def msw_query(spot_id):

    """
    make call to MSW API to get info for journal entry.
    """

    MSW_API_KEY = os.environ['MSW_ACCESS_TOKEN']
    # base URL for MSW API requests
    MSW_API_URL = "http://magicseaweed.com/api/"+MSW_API_KEY+"/forecast/?spot_id=" +str(spot_id)+"&units=us"

    """
    api call todo:
    -> spot_id hardwired for now, 
    but need to make this read from "add_entry" form
    -> filter out FIRST index of response, for now
    -> pass the api resp to entries table (model Entry arg)
    -> edit display template to include swell info
    -> get arrows from MSW?!

    REFACTOR QUESTION:
    break this into separate functions?
    build query, make query, parse query???
    add arg for which attr querying, loop queries?
    """

    ## generic query gets all forecast for given spot_id
    # msw_resp = requests.get(MSW_API_URL)
    # msw_json_list = msw_resp.json()
    # msw_json_obj = msw_json[0]

    # request all attr of primary swell
    MSW_API_URL_SWELL1 = MSW_API_URL+"swell.components.primary.*"
    msw_swell1_resp = requests.get(MSW_API_URL_SWELL1)
    msw_swell1_json_list = msw_swell1_resp.json()
    msw_swell1_json_obj = msw_swell1_json_list[0]
    return msw_swell1_json_obj


@app.route("/")
def index():
    """This is the 'cover' page of kborg's surf journal site.
    It will contain some kind of awesome background image.
    And a logo. And maybe some inspirational text. 
    But first kborg has to build the rest of the damn site."""
    return render_template("index.html")

@app.route("/about")
def list_entriesInfo():
    """temp page while building -- or turn into intro/ about page.
    currently a list of all of the potential info that can be collected"""

    return render_template("about.html")

@app.route("/addEntryForm")
def go_to_addEntry():
    """go to the form to add an entry to the surf journal.
    """

    """
    todo add entry page:
    flesh out the locations dropdown.
    unclear on how to query db from jinja inside html?
    or do I somehow do it here, and pass that back to the template?
    # need jinja loop that reads loc table. 
    # query db for all locations 
    # grab all locations as objects, pass those as array to template
    # will have ALL attributes of each loc, can pick and choose 
    #  on the html side
    """

    return render_template("surf_entry_add.html")

@app.route("/addEntryToDB")
def add_entry():
    """receive input from add_entry form, commit to db, then list all existing entries."""

    """
    TODO -- ask about this!
    ## this breaks now that I switched model to scoped sessions.
    # session = model.connect()
    ## session = model.session works! 
    but... should I put the session somewhere else, like in main? 
    or is it appropriate to make session calls inside particular routes?
    """
    session = model.session

    """
    todo:
    rewire start and end time functionality
    """
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
    spot_name = request.args.get("spot_name")
    board_name = request.args.get("board_name")
    board_pref = request.args.get("board_pref")

    """
    todo entry location:
    # get location id from locations dropdown value
    # query loc table to get msw_id using loc_id
    # pass msw_id to msw_query()
    # parse API json, grab pieces that I want and bind to var     
    """

    # base URL for MSW API requests REQUIRES spot id
    # using bolinas jetty as test/ default.
    msw_id = 4215
    # make API call using msw_id
    msw_swell1_json_obj = msw_query(msw_id)

    # parse msw response object into desired attr
    swell1_ht = msw_swell1_json_obj["swell"]['components']['primary']['height']
    swell1_per = msw_swell1_json_obj["swell"]['components']['primary']['period']
    swell1_dirDeg = msw_swell1_json_obj["swell"]['components']['primary']['direction']
    swell1_dirComp = msw_swell1_json_obj["swell"]['components']['primary']['compassDirection']

    # add piece from api to this instance of model.Entry
    new_entry = model.Entry(date_time_start = date_time_start, date_time_end=date_time_end,
                            beach_name = beach_name, spot_name = spot_name,
                            swell1_ht = swell1_ht, swell1_per = swell1_per, 
                            swell1_dirDeg = swell1_dirDeg, swell1_dirComp = swell1_dirComp,
                            board_name=board_name, board_pref = board_pref)
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

"""
todo:
entries details:
add ability to display details of a given journal entry.
"""

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

    """
    todo quiver:
    implement this. 


    follow locations for dropdown functionality.
    """

    # melons = model.get_melons()
    # return render_template("surf_entries.html",
    #                        session_list = entries)
    

    return render_template("board_quiver.html")    


"""
todo: log-in. reference code from ratings below.
additional goals:
hash/ salt passwords.
give different permissions to different users:
ie, kborg = admin, can access pages that add locations, edit db...
"""

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    return "Oops! This needs to be implemented"

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
