from models.location import Location


def get_locations_counties():
    locations = [loc.serialize() for loc in Location.get_all()]
    counties = list(set(loc['county'] for loc in locations))
    return locations, counties
