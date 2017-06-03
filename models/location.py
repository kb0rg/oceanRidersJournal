from sqlalchemy import Boolean, Column, Integer, String

from models import base

class Location(base.Base):
    """
    makes a row in the locations table.
    """
    __tablename__ = 'locations'

    ## automatically generated when instance is created
    id = Column(Integer, primary_key = True)

    ## general location name, ie Bolinas or Ocean Beach
    beach_name = Column(String(64), nullable = False)
    ## human-readable location info:
    ## (allowing for future expansion beyond CA)
    region = Column(String(64), nullable = False)
    country = Column(String(64), nullable = False)
    state_or_prov = Column(String(64), nullable = False)
    county = Column(String(64), nullable = False)

    ## API-readable location info:
    msw_id = Column(Integer, nullable = True)
    msw_unique_id_exists = Column(Boolean, nullable = True)
    ## which beach's MSW report is being displayed:
    msw_beach_name = Column(String(64), nullable = False)

    ## lat long for possible future use
    ## (in case API changes or adding ability to find nearest from current loc)
    ## storing as string until use-case determines necessary format
    lat = Column(String(64), nullable = False)
    long = Column(String(64), nullable = False)

    def __repr__(self):
        return '<Location: %d, %s, MSW (or nearest) ID: %d >'.format(
            self.id, self.beach_name, self.msw_id)

    @classmethod
    def get_all(cls):
        return base.session.query(cls).all()

    @classmethod
    def get_by_id(cls, loc_id):
        return base.session.query(cls).get(loc_id)

    def serialize(self):
        return {
            'id': self.id,
            'beach_name': self.beach_name,
            'region': self.region,
            'country': self.country,
            'state_or_prov': self.state_or_prov,
            'county': self.county,
            }
