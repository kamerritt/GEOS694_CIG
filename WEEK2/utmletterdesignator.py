def _UTMLetterDesignator(Lat):
    # This routine determines the correct UTM letter designator
    # for the given latitude
    # returns 'Z' if latitude is outside the UTM limits of 84N to 80S
    # Written by Chuck Gantz- chuck.gantz@globalstar.com

    if 84 >= Lat >= 72:
        return 'X'
    elif 72 > Lat >= 64:
        return 'W'
    elif 64 > Lat >= 56:
        return 'V'
    elif 56 > Lat >= 48:
        return 'U'
    elif 48 > Lat >= 40:
        return 'T'
    elif 40 > Lat >= 32:
        return 'S'
    elif 32 > Lat >= 24:
        return 'R'
    elif 24 > Lat >= 16:
        return 'Q'
    elif 16 > Lat >= 8:
        return 'P'
    elif 8 > Lat >= 0:
        return 'N'
    elif 0 > Lat >= -8:
        return 'M'
    elif -8 > Lat >= -16:
        return 'L'
    elif -16 > Lat >= -24:
        return 'K'
    elif -24 > Lat >= -32:
        return 'J'
    elif -32 > Lat >= -40:
        return 'H'
    elif -40 > Lat >= -48:
        return 'G'
    elif -48 > Lat >= -56:
        return 'F'
    elif -56 > Lat >= -64:
        return 'E'
    elif -64 > Lat >= -72:
        return 'D'
    elif -72 > Lat >= -80:
        return 'C'
    else:
        return 'Z'  # if the Latitude is outside the UTM limits
    
def NEW_UTMLetterDesignator(Lat):
     maxlat = [84, 72, 64, 56, 48, 40, 32, 24, 16, 8, 0, -8, -16, -24, -32, -40, -48, -56, -64, -72]
     minlat = [72, 64, 56, 48, 40, 32, 24, 16, 8, 0, -8, -16, -24, -32, -40, -48, -56, -64, -72, -80]
     letter = ['X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'N', 'M', 'L', 'K', 'J', 'H', 'G', 'F', 'E', 'D', 'C']
    
     if not (-72 < Lat < 84):
         return 'Z'
     
     for maxlat, minlat, letter in zip(maxlat, minlat, letter):
        if maxlat > Lat >= minlat:
            return letter
          

#example for elvey building
utm_letter = _UTMLetterDesignator(64.8594)
print(utm_letter)

new_utm_letter = NEW_UTMLetterDesignator(64.8594)
print(new_utm_letter)
  
#example for Lat = 8
utm_letter = _UTMLetterDesignator(8)
print(utm_letter)

new_utm_letter = NEW_UTMLetterDesignator(8)
print(new_utm_letter)
