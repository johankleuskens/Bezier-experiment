import utm

def utm_to_latlon(coords, zone_number, zone_letter):
    easting = coords[0]
    northing = coords[1]
    return utm.to_latlon(easting, northing, zone_number, zone_letter)

def latlon_to_utm(lattitude, longitude):
    return utm.from_latlon(lattitude, longitude)
