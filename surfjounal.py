# controller file for surf journal webapp
from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import jinja2
import os
import requests
import json
from datetime import datetime
import model
import api_msw as msw

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
app.jinja_env.undefined = jinja2.StrictUndefined

@app.before_request
def load_user_id():
    g.user_id = session.get('user_id')

@app.route("/")
def index():
    
    """
    This is the 'cover' page of kborg's surf journal site.
    It will contain some kind of awesome background image.
    And a logo. And maybe some inspirational text. 
    """

    return render_template("index.html")

@app.route("/about")
def list_entriesInfo():

    """
    temp page while building -- turn into intro/ about page.
    currently a list of all of the potential info that can be collected
    """

    return render_template("about.html")

@app.route("/addEntryForm")
def go_to_addEntry():

    """
    goes to the form to add an entry to the surf journal.
    gets info from the db to send to/ populate the form.
    """

    if not g.user_id:
        flash("Please log in", "warning")
        return redirect(url_for("index"))

    """
    TODO: add entry form:
    flesh out the boards dropdown with categories.
    """

    # get all locations from db and pass to template for dropdown
    # and set of counties for organizing locations dropdown
    loc_list = model.session.query(model.Location).all()
    loc_county_list = set(model.session.query(model.Location.county).all())

    # get all boards for user from db and pass to template for dropdown
    # and set of board categorys for organizing boards dropdown
    board_list = model.session.query(model.Board).filter_by(user_id=g.user_id)
    board_cat_list = set(model.session.query(model.Board.category).all())

    # print "*" * 30
    # print loc_county_list
    # print board_cat_list

    return render_template("surf_entry_add.html", locations = loc_list, counties=loc_county_list,
                                                    boards = board_list, categories = board_cat_list)

@app.route("/addEntryToDB", methods=["POST"])
def add_entry():
    """receive input from add_entry form, commit to db, then redirect to page 
    that lists existing entries."""

    user_id = g.user_id

    # entry_date = request.form.get("entry_date")
    # start_time = request.form.get("start_time")
    # end_time = request.form.get("end_time")
    # date_time_start = datetime.strptime((entry_date + " " + start_time), "%Y-%m-%d %H:%M")
    # date_time_end = datetime.strptime((entry_date + " " + end_time), "%Y-%m-%d %H:%M")

    ## temporarily rewire start and end times to datetime.now()
    date_time_start = datetime.now()
    date_time_end = datetime.now()
    # print "\n" * 3, "date_time_start: ", date_time_start, "date_time_end: ", date_time_end

    """
    TODO:
    rewire start and end time functionality
    - decide whether endtime triggers another 
    query to get changes in conditions, or 
    if it's just for personal record of duration
    - if cron job created to store API data:
        - find closest report time to start time
        and plug THAT into db query
    """

    # queries from user
    loc_id = request.form.get("loc_id")
    spot_name = request.form.get("spot_name")
    buddy_name = request.form.get("buddy_name")
    board_id = request.form.get("board_id")
    board_pref = request.form.get("board_pref")
    board_notes = request.form.get("board_notes")
    rate_overall_fun = request.form.get("rate_overall_fun")
    rate_wave_challenge = request.form.get("rate_wave_challenge")
    rate_wave_fun = request.form.get("rate_wave_fun")
    rate_crowd_den = request.form.get("rate_crowd_den")
    rate_crowd_vibe = request.form.get("rate_crowd_vibe")
    gen_notes = request.form.get("gen_notes")

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
    swell1_dir_deg_msw = msw_swell1_json_obj['swell']['components']['primary']['direction']
    swell1_dir_comp = msw_swell1_json_obj['swell']['components']['primary']['compassDirection']
    swell1_dir_deg_global = msw.getGlobalDegrees(swell1_dir_deg_msw)
    swell1_arrow_deg = msw.getArrowDegrees(swell1_dir_deg_global)


    ## make API call for wind info using msw_id
    msw_wind_json_obj = msw.getWind(msw_id)
    """
    TODO: response is showing way more than wind.
    clean up query? combine with swell call?
    """
    print "msw_wind_json_obj: ", msw_wind_json_obj
    ## parse msw response object for wind info into desired attr
    wind_speed = msw_wind_json_obj['wind']['speed']
    wind_gust = msw_wind_json_obj['wind']['gusts']
    wind_dir_deg = msw_wind_json_obj['wind']['direction']
    wind_dir_comp = msw_wind_json_obj['wind']['compassDirection']
    wind_unit = msw_wind_json_obj['wind']['unit']
    wind_arrow_deg = msw.getArrowDegrees(wind_dir_deg)

    # add info from user and api to this instance of model.Entry
    new_entry = model.Entry(user_id = user_id,
                            date_time_start = date_time_start, date_time_end=date_time_end,
                            loc_id = loc_id, spot_name = spot_name, buddy_name = buddy_name,
                            swell1_ht = swell1_ht, swell1_per = swell1_per, swell1_dir_deg_msw = swell1_dir_deg_msw,
                            swell1_dir_comp = swell1_dir_comp, swell1_dir_deg_global =swell1_dir_deg_global, 
                            swell1_arrow_deg = swell1_arrow_deg,
                            wind_speed = wind_speed, wind_gust= wind_gust, wind_dir_deg = wind_dir_deg,
                            wind_dir_comp = wind_dir_comp, wind_unit = wind_unit, wind_arrow_deg = wind_arrow_deg,
                            board_id = board_id, board_pref = board_pref, board_notes = board_notes,
                            rate_overall_fun = rate_overall_fun, rate_wave_challenge = rate_wave_challenge,
                            rate_wave_fun = rate_wave_fun, rate_crowd_den = rate_crowd_den,
                            rate_crowd_vibe = rate_crowd_vibe, gen_notes = gen_notes)

    model.session.add(new_entry)
    model.session.commit()

    return redirect("/entries")

@app.route("/entries")
def list_entries():
    """displays all of the surf entries logged so far"""

    if not g.user_id:
        flash("Please log in", "warning")
        return redirect(url_for("index"))

    print "g.user_id: ", g.user_id
    entry_list = model.session.query(model.Entry).filter_by(user_id=g.user_id)
    username = model.session.query(model.User).filter_by(id=g.user_id).one().username

    print "*" * 30
    # print entry_list
    print username

    return render_template("surf_entries_summary.html", entries = entry_list, username = username)

@app.route("/entryDetails/<int:id>")
def list_entry_details(id):
    """displays full details of the selected surf entry"""

    if not g.user_id:
        flash("Please log in", "warning")
        return redirect(url_for("index"))

    entry = model.session.query(model.Entry).filter_by(id = id).one()
    print entry

    return render_template("surf_entry_details.html", entry = entry)

@app.route("/board_quiver")
def edit_quiver():
    """display and edit existing quiver of boards"""

    if not g.user_id:
        flash("Please log in", "warning")
        return redirect(url_for("index"))

    # get all boards from db and pass to template for display
    board_list = model.session.query(model.Board).filter_by(user_id=g.user_id)
    # print board_list
    return render_template("board_quiver.html", boards = board_list)

@app.route("/addBoardToDB", methods=["POST"])
def add_board():
    """receive input from board_quiver form, commit to db, then redirect to quiver list page."""

    user_id = g.user_id

    # queries from user
    nickname = request.form.get("nickname")
    category = request.form.get("category")
    length_ft = request.form.get("length_ft")
    length_in = request.form.get("length_in")
    shaper = request.form.get("shaper")
    shape = request.form.get("shape")
    fins = request.form.get("fins")

    new_entry = model.Board(user_id = user_id,
                            nickname = nickname, category = category,
                            length_ft = length_ft, length_in = length_in,
                            shaper = shaper, shape = shape, fins = fins)

    model.session.add(new_entry)
    model.session.commit()

    flash("%s added!" % nickname)

    return redirect("/board_quiver")

@app.route("/login", methods=["GET"])
def show_login():

    """
    TODO: 
    - hide button/ page while logged in.
    """

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    ## include a redirect if user is logged in and goes back to login page?
    # if g.user_id:
    #     return redirect("")

    email = request.form['email']
    password = request.form['password']

    try:
        user = model.session.query(model.User).filter_by(email=email, password=password).one()
    except:
        flash("Invalid username or password", "error")
        return redirect(url_for("index"))

    session['user_id'] = user.id
    return redirect("/entries")

@app.route("/register", methods=["POST"])
def register():

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    existing_email = model.session.query(model.User).filter_by(email=email).first()
    existing_username = model.session.query(model.User).filter_by(username=username).first()

    if existing_email or existing_username:
        flash("Email or username already in use: try again.", "error")
        return redirect(url_for("login"))

    u = model.User(username=username, email=email, password=password)
    model.session.add(u)
    model.session.commit()
    model.session.refresh(u)
    session['user_id'] = u.id 
    return redirect("/about")

@app.route("/logout")
def logout():

    """
    TODO:    
    - fix bug if button hit while not logged in.
    - hide button/ page while not logged in.
    """

    del session['user_id']
    return redirect(url_for("index"))

@app.route("/temp_bootstrap")
def bootstrap():

    return render_template("temp_bootstrap.html")

"""
TODO before deploying:
- turn off app.run debug 
- hash/ salt passwords.
- fix logout bug.
super stretch goal:
- give different permissions to different users:
ie, kborg = admin, can access pages that add locations, edit db...
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
