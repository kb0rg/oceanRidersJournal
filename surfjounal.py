from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os
import requests
import json

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the surf journal site"""
    
    return render_template("index.html")

@app.route("/entriesSummary")
def list_entriesInfo():
    """temp page while building? or turn into intro/ about page?
    currently a list of all of the potential info that can be collected"""

    return render_template("surf_entries_summary.html")

@app.route("/entries")
def list_entries():
    """diplay all of the surf entries logged so far"""

    return render_template("surf_entries_list.html")

@app.route("/addEntry")
def add_entry():
    """put everything from this form into the db"""


    # noaa_url = "http://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20130101%2010:00&end_date=20130101%2010:24&station=8454000&product=water_level&datum=mllw&units=metric&time_zone=gmt&application=web_services&format=json"
    # r = requests.get(noaa_url)
    # spitcast_tide_url = "http://api.spitcast.com/api/county/tide/san-francisco/"
    # r = requests.get(spitcast_tide_url)
    # return json.dumps(r.json())

    # # json.load vs json.loads, json.dumps, Flask.jsonify
    # s = model.Session(date, time,)
    # model.session.add
    return render_template("surf_entry_add.html")


@app.route("/board_quiver")
def edit_quiver():
    """display and edit existing quiver of boards"""
    # melons = model.get_melons()
    # return render_template("surf_entries.html",
    #                        session_list = entries)
    return render_template("board_quiver.html")    

# @app.route("/melon/<int:id>")
# def show_melon(id):
#     """This page shows the details of a given melon, as well as giving an
#     option to buy the melon."""
#     melon = model.get_melon_by_id(id)
#     print melon
#     return render_template("melon_details.html",
#                   display_melon = melon)

# @app.route("/cart")
# def shopping_cart():
#     """TODO: Display the contents of the shopping cart. The shopping cart is a
#     list held in the session that contains all the melons to be added. Check
#     accompanying screenshots for details."""
#     return render_template("cart.html")

# @app.route("/add_to_cart/<int:id>")
# def add_to_cart(id):
#     """TODO: Finish shopping cart functionality using session variables to hold
#     cart list.

#     Intended behavior: when a melon is added to a cart, redirect them to the
#     shopping cart page, while displaying the message
#     "Successfully added to cart" """

#     return "Oops! This needs to be implemented!"


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    return "Oops! This needs to be implemented"


# @app.route("/checkout")
# def checkout():
#     """TODO: Implement a payment system. For now, just return them to the main
#     melon listing page."""
#     flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
#     return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
