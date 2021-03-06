import jinja2
import json
import logging
import os
import requests
from datetime import datetime

from flask import (Flask, request, session, render_template, g, redirect,
    url_for, flash, jsonify)

from models import base as db
from models.board import Board, BOARD_CATEGORIES
from models.entry import Entry
from models.location import Location
from models.user import User
from services import api_msw as msw
from services import entries
from services import location

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
app.jinja_env.undefined = jinja2.StrictUndefined

@app.before_request
def load_user_id():
    g.user_id = session.get('user_id')

@app.route('/')
def index():
    """
    The cover page of kborg's surf journal site.
    """

    return render_template('index.html')

@app.route('/about')
def list_entriesInfo():
    """
    intro/ about page.
    """

    return render_template('about.html')

@app.route('/addEntryForm')
def go_to_addEntry():
    """
    renders form, using info from the db, to add an entry to the surf journal.
    """

    ## make page available only if logged in
    if not g.user_id:
        flash('You must be logged in to add to your journal.', 'warning')
        return redirect('/about')

    loc_list, loc_county_list = location.get_locations_counties()

    return render_template('surf_entry_add.html',
        locations = loc_list,
        counties = loc_county_list,
        boards = Board.get_all_for_user(g.user_id),
        categories = Board.get_categories_for_user(),
        )

@app.route('/addEntryToDB', methods = ['POST'])
def add_entry():
    """
    receive input from add_entry form, commit to db, goto summary display page.
    """

    data_dict = {}

    data_dict['user_id'] = g.user_id

    ## wire start and end times to datetime.now for MVP
    data_dict['date_time_start'] = datetime.now()
    data_dict['date_time_end'] = datetime.now()

    ## get info from user input
    form_input = request.values
    data_dict.update(form_input.to_dict())

    new_entry = Entry.from_form_data(data_dict)

    db.session.add(new_entry)
    db.session.commit()

    return redirect('/entries')

@app.route('/entries')
def list_entries():
    """
    render summary page, chart plus all surf entries logged for current user.
    """

    if not g.user_id:
        flash('You must be logged in to view your journal entries.', 'warning')
        return redirect('/about')

    ## get all entries and username for current user from db and pass to template for display
    entry_list = Entry.get_all_for_user(g.user_id)
    username = User.get_username(g.user_id)

    return render_template(
        'surf_entries_summary.html', entries = entry_list, username = username)

@app.route('/entries_data')
def list_entries_data():
    """
    sends json to the entry_details route to render bubble chart.
    """

    entry_list = Entry.get_all_for_user(g.user_id)

    ## process entries data into form required by chart
    results = {}
    for entry in entry_list:
        if entry.loc_id not in results:
            results[entry.loc_id] = {
                'data': [],
                'name': entry.loc.beach_name}

        disp = entries.format_for_chart(entry)
        logging.debug('Data for display: {}'.format(disp))

        results[entry.loc_id]['data'].append(disp)

    ## get values from results dict: chart expects a list of dictionaries
    results_list = results.values()
    logging.debug('All results to display: {}'.format(results_list))

    ## send to chart as json object
    return jsonify(results=results_list)

@app.route('/entryDetails/<int:id>')
def list_entry_details(id):
    """
    displays full details of the selected surf entry.
    """

    ## make page available only if logged in
    if not g.user_id:
        flash('Please log in', 'warning')
        # return redirect(url_for('index'))

    ## get all fields from db for entry selected and pass to template for display
    entry = Entry.get_by_id(id)
    opts = entries.ENTRY_DETAIL_OPTS

    return render_template(
        'surf_entry_details.html',
        entry = entry,
        wave_challenge = opts.get('wave_challenge'),
        wave_fun = opts.get('wave_fun'),
        crowd_vibe = opts.get('crowd_vibe'),
        crowd_den = opts.get('crowd_den'),
        overall_fun = opts.get('overall_fun'),
        )

@app.route('/board_quiver')
def edit_quiver():
    """
    display and edit existing quiver of boards.
    """

    ## make page available only if logged in
    if not g.user_id:
        flash('You must be logged in to add or view your boards.', 'warning')
        return redirect('/about')

    return render_template(
        'board_quiver.html',
        boards = Board.get_all_for_user(g.user_id),
        username = User.get_username(g.user_id),
        categories = BOARD_CATEGORIES,
        )

@app.route('/addBoardToDB', methods=['POST'])
def add_board():

    """
    adds board to quiver.

    receives input from board_quiver form,
    commits to db, then redirects to quiver list page
    and flashes message confirming board was added.
    """

    ## get user id from session
    user_id = g.user_id

    ## get info from user input
    nickname = request.form.get('nickname')
    category = request.form.get('category')
    length_ft = request.form.get('length_ft')
    length_in = request.form.get('length_in')
    shaper = request.form.get('shaper')
    shape = request.form.get('shape')
    fins = request.form.get('fins')

    ## add info from user to this instance of Board
    new_entry = Board(
        user_id = user_id,
        nickname = nickname,
        category = category,
        length_ft = length_ft,
        length_in = length_in,
        shaper = shaper,
        shape = shape,
        fins = fins,
        )

    db.session.add(new_entry)
    db.session.commit()

    flash('%s added to your quiver!' % nickname)

    return redirect('/board_quiver')

@app.route('/login', methods = ['GET'])
def show_login():
    """
    displays log-in/ register form.
    """
    ## flash message and stay on same page if user is logged in and tries to go back to login page
    if g.user_id:
        username = User.get_username(g.user_id)
        flash('Hey %s! You\'re already logged in!' % username, 'error')
        return redirect(redirect_url())
    else:
        return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    """
    validates input from log-in form and starts user session,
    redirects to user's entries summary page.
    """
    ## get info from user input
    email = request.form['email']
    password = request.form['password']
    user = None
    ## make sure log-in info is valid
    try:
        user = User.get_by_login_creds(email, password)
    except:
        flash('Invalid username or password', 'error')
        # return redirect(url_for('index'))

    if not user:
        flash('NOPE', 'error')
        return redirect(url_for('index'))

    ## start session for user and redirect to user's journal summary
    session['user_id'] = user.id
    return redirect('/entries')

@app.route('/register', methods = ['POST'])
def register():

    """
    validates input from registration form and starts user session,
    redirects to add entry page.
    """

    ## get info from user input
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if User.email_exists(email):
        flash('This email is already registered: please log in!', 'error')
        return redirect(url_for('login'))

    if User.username_exists(username):
        flash('This username is already in use: pick another one.', 'error')
        return redirect(url_for('login'))

    u = User(
        username = username,
        email = email,
        password = password,
        )

    db.session.add(u)
    db.session.commit()
    db.session.refresh(u)
    session['user_id'] = u.id
    return redirect('/addEntryForm')

@app.route('/logout')
def logout():
    """
    log out user or redirect to log-in page.
    """

    if g.user_id:
        username = User.get_username(g.user_id)
        flash('See you again soon, %s. Now go get in the water.' % username, 'error')
        del session['user_id']
        return redirect(url_for('index'))
    else:
        flash('You can\'t log out, you\'re not logged in! Please log in to use the journal.', 'error')
        return render_template('login.html')


def redirect_url(default = 'index'):
    """
    flask helper function to redirect back to same page.

    used in unnecessary click of 'log in" button.'
    """

    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

"""
TODO before deploying:
- hash/ salt passwords.
"""

if __name__ == '__main__':

    """
    run app after getting env var for debug and port: allows for different
    settings for dev vs deployment.
    """

    ## for deploy on heroku: 'heroku config: Set NO_DUBUG = 1'
    DEBUG = 'NO_DEBUG' not in os.environ
    ## heroku will set port as env var
    PORT = int(os.environ.get('PORT', 5000))

    app.run(debug = DEBUG, host = '0.0.0.0', port=PORT)
