from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from models import Base, session

class Board(Base):
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
    def get_all_for_user(user):
        return session.query(models.Board).filter_by(user_id=user)

    @classmethod
    get get_all_categories():
        return set(session.query(models.Board.category).all())
