"""
UTM Letter Designator Rewritten
"""
def utm_letter_designator(lat):
    """
    This routine determines the correct UTM letter designator for the given 
    latitude and returns 'Z' if latitude is outside the UTM limits of 84N to 80S

    Written by Chuck Gantz- chuck.gantz@globalstar.com

    :type lat: float
    :param lat: latitude to check for designation
    :rtype: str
    :return: letter designation for given `lat`
    """
    # Designation codes: (lat_max, lat_min]
    utm_designations = {
        "X": (84.001, 72),  # fudge factor to make logic work
        "W": (72, 64),
        "V": (64, 56),
        "U": (56, 48),
        "T": (48, 40),
        "S": (40, 32),
        "R": (32, 24),
        "Q": (24, 16),
        "P": (16, 8),
        "N": (8, 0),
        "M": (0, -8),
        "L": (-8, -16),
        "K": (-16, -24),
        "J": (-24, -32),
        "H": (-32, -40),
        "G": (-40, -48),
        "F": (-48, -56),
        "E": (-56, -64),
        "D": (-64, -72),
        "C": (-72, -80),
    }

    for designation, coords in utm_designations.items():
        lat_max, lat_min = coords
        if lat_min <= lat < lat_max:
            return designation
    else:
        return "Z"    
    

if __name__ == "__main__":
    latitudes = [85, 84, 64, 0, -1, -79.9999, 200]
    for latitude in latitudes:
        print(f"lat {latitude} = {utm_letter_designator(latitude)}")
