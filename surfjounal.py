from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import jinja2
import os
import requests
import json
from datetime import datetime
import model
import api_msw as msw


"""
TODO: general:
review post/ get methods and see if/ where post should be used
"""

"""
TODO:
app.secret.key = do I need to change this, or hide it in a secrets file?
"""
app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    
    """
    This is the 'cover' page of kborg's surf journal site.
    It will contain some kind of awesome background image.
    And a logo. And maybe some inspirational text. 
    But first kborg has to build the rest of the damn site.
    """

    return render_template("index.html")

@app.route("/about")
def list_entriesInfo():

    """
    temp page while building -- or turn into intro/ about page.
    currently a list of all of the potential info that can be collected
    """

    return render_template("about.html")

@app.route("/addEntryForm")
def go_to_addEntry():

    """
    goes to the form to add an entry to the surf journal.
    gets info from the db to send to/ populate the form.
    """

    """
    TODO: add entry form:
    flesh out the locations dropdown with regions.
    flesh out the boards dropdown with categories.
    """

    # get all locations from db and pass to template for dropdown
    loc_list = model.session.query(model.Location).all()
    board_list = model.session.query(model.Board).all()
    # print loc_list

    return render_template("surf_entry_add.html", locations = loc_list, boards = board_list)

@app.route("/addEntryToDB")
def add_entry():
    """receive input from add_entry form, commit to db, then redirect to page 
    that lists existing entries."""

    """
    TODO:
    get user_id from session once log-in enabled
    """
    # temp hardwire user id to kborg
    user_id = 1

    """
    TODO:
    rewire start and end time functionality
    - decide whether endtime triggers another 
    query to get changes in conditions, or 
    if it's just for personal record of duration
    - if no cron:
        - keep start as datetime now 
    - if cron:
        - find closest report time to start time
        and plug THAT into db query
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
    loc_id = request.args.get("loc_id")
    spot_name = request.args.get("spot_name")
    board_id = request.args.get("board_id")
    board_pref = request.args.get("board_pref")
    board_notes = request.args.get("board_notes")

    # look up loc from loc table: from loc_id get msw_id
    loc_obj = model.session.query(model.Location).get(loc_id)
    # assign db's msw_id to this function's msw_id var
    msw_id = loc_obj.msw_id

    """
    TODO: should I make just one API call, get everything?
    """
    # make API call for swell1 info using msw_id
    msw_swell1_json_obj = msw.getSwell1(msw_id)

    # parse msw response object for swell1 info into desired attr
    swell1_ht = msw_swell1_json_obj['swell']['components']['primary']['height']
    swell1_per = msw_swell1_json_obj['swell']['components']['primary']['period']
    swell1_dir_deg = msw_swell1_json_obj['swell']['components']['primary']['direction']
    swell1_dir_comp = msw_swell1_json_obj['swell']['components']['primary']['compassDirection']

    """
    TODO: response is showing way more than wind.
    """
    # make API call for wind info using msw_id
    msw_wind_json_obj = msw.getWind(msw_id)

    print "msw_wind_json_obj: ", msw_wind_json_obj
    # parse msw response object for wind info into desired attr
    wind_speed = msw_wind_json_obj['wind']['']
    wind_dir_deg = msw_wind_json_obj['wind']['direction']
    wind_dir_comp = msw_wind_json_obj['wind']['compassDirection']
    wind_unit = msw_wind_json_obj['wind']['unit']
    # add gusts to model?
    # wind_gusts = msw_wind_json_obj['wind']['gusts']

    # add info from user and api to this instance of model.Entry
    new_entry = model.Entry(user_id = user_id,
                            date_time_start = date_time_start, date_time_end=date_time_end,
                            loc_id = loc_id, spot_name = spot_name,
                            swell1_ht = swell1_ht, swell1_per = swell1_per, 
                            swell1_dir_deg = swell1_dir_deg, swell1_dir_comp = swell1_dir_comp,
                            wind_speed = wind_speed, wind_dir_deg = wind_dir_deg,
                            wind_dir_comp = wind_dir_comp, wind_unit = wind_unit,
                            board_id=board_id, board_pref = board_pref, board_notes = board_notes)

    model.session.add(new_entry)
    model.session.commit()

    return redirect("/entries")


@app.route("/entries")
def list_entries():
    """displays all of the surf entries logged so far"""

    entry_list = model.session.query(model.Entry).all()

    # TODO -- want to filter entries by date. sort here or on display/ template side?

    return render_template("surf_entries_summary.html", entries = entry_list)

"""
TODO:
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

@app.route("/addBoardToDB")
def add_board():
    """receive input from board_quiver form, commit to db, then redirect to quiver list page."""

    """
    TODO:
    get user_id from session once log-in enabled
    """
    # temp hardwire user_id to kborg
    user_id = 1

    # queries from user
    nickname = request.args.get("nickname")
    category = request.args.get("category")
    length_ft = request.args.get("length_ft")
    length_in = request.args.get("length_in")
    shaper = request.args.get("shaper")
    shape = request.args.get("shape")
    fins = request.args.get("fins")
     # = request.args.get("")

    new_entry = model.Board(user_id = user_id,
                            nickname = nickname, category = category,
                            length_ft = length_ft, length_in = length_in,
                            shaper = shaper, shape = shape, fins = fins)

    model.session.add(new_entry)
    model.session.commit()

    return redirect("/board_quiver")

@app.route("/board_quiver")
def edit_quiver():
    """display and edit existing quiver of boards"""

    """
    TODO quiver:
    """

    # get all boards from db and pass to template for display
    board_list = model.session.query(model.Board).all()
    # print board_list
    return render_template("board_quiver.html", boards = board_list)

"""
TODO: log-in. reference code from ratings below.
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
