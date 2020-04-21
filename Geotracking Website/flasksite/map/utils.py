from flask import abort, flash, url_for
from flasksite.models import soughtgps, bikeGps, gps, streetandCity
from math import cos, asin, sqrt
from flasksite import mail
from flask_mail import Message
from datetime import datetime
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="flasksite")

def findNearest():
    userpoint = streetandCity.query.order_by(streetandCity.id.desc()).first()
    location = geolocator.geocode([userpoint.street, userpoint.city])
    if location == None:
        flash('WRONG ADDRESS/NON EXISTANT ADDRESS', 'danger')
        abort(501)
    v = { 'lat': location.latitude, 'lon': location.longitude}

    #Query the database for the most recent data for each bike ID
    bike1 = gps.query.order_by(gps.timestamp.desc()).first()
    bike2 = bikeGps.query.filter_by(bike_id=2).order_by(bikeGps.id.desc()).first()
    bike3 = bikeGps.query.filter_by(bike_id=3).order_by(bikeGps.id.desc()).first()
    bike4 = bikeGps.query.filter_by(bike_id=4).order_by(bikeGps.id.desc()).first()
    bike5 = bikeGps.query.filter_by(bike_id=5).order_by(bikeGps.id.desc()).first()

    #testing to see if bike is still in the safe zone
    bikeranaway(bike1.latitude,bike1.longitude)

    #Putting the GPS locations into a list so the data can be utilized.
    DataList = [{'lat': bike1.latitude, 'lon': bike1.longitude},
                    {'lat': bike2.Latitude, 'lon': bike2.Longtitude},
                    {'lat': bike3.Latitude, 'lon': bike3.Longtitude},
                    {'lat': bike4.Latitude, 'lon': bike4.Longtitude},
                    {'lat': bike5.Latitude, 'lon': bike5.Longtitude}]
    #Findest the closets points and all the distance from each bike.
    closet_point = closest(DataList, v)
    distlist = []
    Distone= round(distance( location.latitude, location.longitude ,bike1.latitude,bike1.longitude ),2)
    Disttwo = round(distance(location.latitude, location.longitude ,bike2.Latitude,bike2.Longtitude ),2)
    Distthree = round(distance(location.latitude,location.longitude ,bike3.Latitude,bike3.Longtitude ),2)
    Distfour = round(distance(location.latitude, location.longitude ,bike4.Latitude,bike4.Longtitude ),2)
    Distfive = round(distance(location.latitude,location.longitude ,bike5.Latitude,bike5.Longtitude ),2)
    distlist.append(Distone), distlist.append(Disttwo), distlist.append(Distthree),distlist.append(Distfour),distlist.append(Distfive)
    #Returning the data to be displayed
    return closet_point, distlist



#Finding the Distance with the Haversine formula
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

#Finding the closet location utilizing this Haversine Formula against a list of coordinates
#Data is the data we measured our point up against
def closest(data, ourpoint):
    return min(data, key=lambda p: distance(ourpoint['lat'],ourpoint['lon'],p['lat'],p['lon']))

def bikeranaway(latitude, longitude):
    if latitude >56.23790246985043 or latitude <  56.083563113:
        print(latitude)
        sendsos()
    if longitude > 10.320187398 or longitude < 10.071151042:
        print(longitude)
        sendsos()

def sendsos():
    mytime = datetime.now()
    msg = Message('SoS Message - Danger Danger',
                  sender='noreply@demo.com',
                  recipients=[bikewebnoreply@gmail.com])
    msg.body = f'''Warning: This is an Autonomous SOS Signal
    {url_for('map.displaymap', _external=True)}
    A Bike has left the Pass Zone - at {mytime} - Danger Danger Beware if this is not a test
    '''
    mail.send(msg)

