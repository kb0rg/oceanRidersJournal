# database model for surf journal
import os
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///db_surfjournal.db")

engine = create_engine(DATABASE_URL, echo = False)
session = scoped_session(sessionmaker(bind = engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()

def main():
    """
    directions for rebuilding db when model is called directly.
    """

    print "\nWelcome to kborg's surfjournal model.\n"
    print "*" * 13, "\n"
    print "To proceed rebuilding the schema, run the following code:\n" + \
    "engine = create_engine(\"sqlite:///db_surfjournal.db\", echo=True)\n" + \
    "Base.metadata.create_all(engine)\n"
    print "*" * 13
    print "When complete, exit python and run python db_seed.py in the terminal."
    print "*" * 13, "\n"
    print "Otherwise please exit now."


if __name__ == "__main__":
    main()

"""
NOTE!!!!
*****
when db needs to be deleted and rebuilt,
run base.py in interactive mode (while in virtual env):
python -i models/base.py
"""
