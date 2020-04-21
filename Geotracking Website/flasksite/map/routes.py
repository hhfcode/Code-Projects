from flask import render_template, request, Blueprint, flash, url_for, redirect
from flask_login import login_required
from flasksite.map.forms import inputGPS
from flasksite.models import soughtgps, gps, streetandCity, bikeGps
from flasksite import db
from flasksite.map.utils import findNearest
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="flasksite")



map = Blueprint('map', __name__)

@map.route('/displaymap')
@login_required
def displaymap():
    currentbikeLoc = gps.query.order_by(gps.timestamp.desc()).first() #Get last updated coordinates
    lon,lat, ts = currentbikeLoc.longitude, currentbikeLoc.latitude, currentbikeLoc.timestamp #Put them into variables
    newts = (ts[0:10] + " " + ts[11:19]) #String Manipulation
    return render_template('displaymap.html', title='Displayed Map', longitude=lon, latitude=lat, timestamp = newts) #put into our map


@map.route('/nearest_bike', methods=['GET', 'POST'])
@login_required
def nearest_bike():
    form = inputGPS()
    if form.validate_on_submit():
        address = streetandCity(street=form.street.data , city= form.city.data )
        db.session.add(address)
        db.session.commit()
        flash('Your Coords Has Been Uploaded - Thank You', 'info')
        return redirect(url_for('map.displaymapandclosets'))
    return render_template('nearest_bike.html', form=form)

@map.route('/displaymapandclosets')
@login_required
def displaymapandclosets():
    closestpoint, distlist = findNearest()
    lon = closestpoint.pop('lon')
    lat = closestpoint.pop('lat')
    location = geolocator.reverse([lat,lon])
    address = location.address
    distlist.sort()
    currentbikeLoc = gps.query.order_by(gps.timestamp.desc()).first() #Get last updated coordinates
    lon,lat, ts = currentbikeLoc.longitude, currentbikeLoc.latitude, currentbikeLoc.timestamp #Put them into variables
    newts = (ts[0:10] + " " + ts[11:19]) #String Manipulation
    staticloc2 = bikeGps.query.filter_by(bike_id=2).order_by(bikeGps.id.desc()).first()
    staticloc3 = bikeGps.query.filter_by(bike_id=3).order_by(bikeGps.id.desc()).first()
    staticloc4 = bikeGps.query.filter_by(bike_id=4).order_by(bikeGps.id.desc()).first()
    staticloc5 = bikeGps.query.filter_by(bike_id=5).order_by(bikeGps.id.desc()).first()
    return render_template('distanceshow.html', closestpoint=address, distlistzero = distlist[0], distlistone = distlist[1],
                           distlisttwo = distlist[2], distlistthree = distlist[3], distlistfour = distlist[4],
    longitude = lon, latitude = lat, timestamp = newts,
    statlat2 = staticloc2.Latitude, statlon2 = staticloc2.Longtitude, statlat3 = staticloc3.Latitude,
      statlon3 = staticloc3.Longtitude, statlat4 = staticloc4.Latitude, statlon4 = staticloc4.Longtitude,
            statlat5 = staticloc5.Latitude, statlon5 = staticloc5.Longtitude
    )

@map.route('/staticmap')
@login_required
def staticmap():
    currentbikeLoc = gps.query.order_by(gps.timestamp.desc()).first() #Get last updated coordinates
    lon,lat, ts = currentbikeLoc.longitude, currentbikeLoc.latitude, currentbikeLoc.timestamp #Put them into variables
    newts = (ts[0:10] + " " + ts[11:19]) #String Manipulation
    staticloc2 = bikeGps.query.filter_by(bike_id=2).order_by(bikeGps.id.desc()).first()
    staticloc3 = bikeGps.query.filter_by(bike_id=3).order_by(bikeGps.id.desc()).first()
    staticloc4 = bikeGps.query.filter_by(bike_id=4).order_by(bikeGps.id.desc()).first()
    staticloc5 = bikeGps.query.filter_by(bike_id=5).order_by(bikeGps.id.desc()).first()
    return render_template('staticlandmarks.html', title='Displayed Map', longitude=lon, latitude=lat, timestamp = newts,
                           statlat2 = staticloc2.Latitude, statlon2 = staticloc2.Longtitude, statlat3 = staticloc3.Latitude,
                           statlon3=staticloc3.Longtitude, statlat4=staticloc4.Latitude, statlon4=staticloc4.Longtitude,
                           statlat5=staticloc5.Latitude, statlon5=staticloc5.Longtitude) #put into our map




