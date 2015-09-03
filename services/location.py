from models.location import Location


def get_locations_counties():
    locations = [location.serialize() for location in Location.get_all_locations()]
    counties = set(location['county'] for location in locations)
    return location, counties
