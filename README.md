Ocean Riders' Journal
===========

![CoverPage](https://raw.githubusercontent.com/kb0rg/hb_project/master/screengrabs/sg01_cover.png)

Ocean Rider’s Journal is a place for Northern and Central California surfers to record their time in the ocean. The journal collects swell and wind data based on time and location, and combines it with subjective user ratings to visually graph the best conditions for the user. develop a keener sense of what conditions work best for them at their favorite spots.

![JournalEntriesSummaryPageExample](https://raw.githubusercontent.com/kb0rg/hb_project/master/screengrabs/sg02_summary.png)

Ocean Rider’s Journal was made at Hackbright Academy as my final project for the Winter 2015 cohort. 

### Technology

Ocean Rider’s Journal uses a Python controller and a Flask web framework. The SQLite database collects information provided by users about their surf sessions, the boards they ride, and the wind and swell conditions at the time of each journal entry. Weather data is gathered from the magicseaweed.com API. 

Python, Flask, Jinja2, SQLite, SQLAlchemy, HTML5, CSS, highcharts.js, and Bootstrap. 
(Dependencies are listed in requirements.txt)


##### Screengrabs

Each user can an entry to their personal surf journal:
![JournalAddEntryExample](https://raw.githubusercontent.com/kb0rg/hb_project/master/screengrabs/sg04_add.png)
View a summary of all journal entries:
![JournalEntriesSummaryTableExample](https://raw.githubusercontent.com/kb0rg/hb_project/master/screengrabs/sg02b_summary.png)
Summary page inclused a chart correlating overall ratings with swell conditions:
![JournalEntriesSummaryChartExample](https://raw.githubusercontent.com/kb0rg/hb_project/master/screengrabs/sg02c_summaryChart.png)
![JournalEntryDetailsExample](https://raw.githubusercontent.com/kb0rg/hb_project/master/screengrabs/sg03_details.png)
![QuiverBoardListExample](https://raw.githubusercontent.com/kb0rg/hb_project/master/screengrabs/sg06_quiverList.png)
![QuiverAddBoardExample](https://raw.githubusercontent.com/kb0rg/hb_project/master/screengrabs/sg04_add.png)


##### Contact Me

Connect with the developer: www.linkedin.com/in/kborges

##### Acknowledgements

Many thanks to all the amazing Hackbright teachers and TAs (especially my advisor Katie LeFevre), and my very inspiring mentors.
I am also deeply indebted to my irreplaceable collection of friends and family, all of whom encouraged me to make the jump to Hackbright.  

##### To recreate this webapp

- Sign up for an API key at: http://magicseaweed.com/developer/sign-up.
- Store your API key as "MSW_API_KEY" along with an "APP_SECRET_KEY" in a local "secrets.sh" file.
- Install the required packages in the webapp directory's virtualenv.
- Source the env and your secrets file.
- Run the model.py file in interactive mode (python -i model.py) and follow the prompts to initialize your database.
- Run the db_seed.py in python (python db_seed.py) to seed the database (necessary to have access to beach locations in the add entry form).
- Start the webapp (python surfjournal.py), register as a user, and start exploring the journal!

