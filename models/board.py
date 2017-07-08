from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from models import base

BOARD_CATEGORIES = [
    "longboard",
    "shortboard",
    "fish",
    "gun",
    "SUP",
    "other",
    ]

class Board(base.Base):
    """
    makes a row in the boards table.
    """
    __tablename__ = "boards"

    ## automatically generated when instance is created
    id = Column(Integer, primary_key = True)

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User",
        backref = backref("boards", order_by=id))

    ## required fields:
    nickname = Column(String(64), nullable = False)
    ## type of board (long, short, fish, etc)
    ## used in add entry dropdown
    category = Column(String(64), nullable = False)

    ## optional fields:
    length_ft = Column(Integer, nullable = True)
    length_in = Column(Integer, nullable = True)
    shaper = Column(String(64), nullable = True)
    ## modelname or desciption of board
    shape = Column(String(64), nullable = True)
    fins = Column(String(64), nullable = True)

    def __repr__(self):
        return "<Board: %d, %s, %s %s>"%(self.id, self.nickname, self.shaper,
            self.shape)

    @classmethod
    def get_all_for_user(cls, user):
        return base.session.query(cls).filter_by(user_id=user)

    @classmethod
    def get_categories_for_user(cls):
        return set(base.session.query(cls.category).all())
