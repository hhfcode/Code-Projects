from flask import render_template, request, Blueprint, flash, url_for, redirect
from flask_login import login_required
from flasksite.Webstatistics.utils import SoSemailsent, MostActiveUser, mostsoughtafterLocationForABike
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="flasksite")

Webstatistics = Blueprint('Webstatistics', __name__)


@Webstatistics.route('/Webstatistics', methods=['GET'])
@login_required
def mainstatistics():
    MCemailadd, totalmailint = SoSemailsent()
    ActiveUser = MostActiveUser()
    mostsoughtstreet, mostsoughtcity = mostsoughtafterLocationForABike()
    mostSoughtStreetName = geolocator.geocode([mostsoughtstreet, mostsoughtcity])
    return render_template('statistics.html', totalmailsent = totalmailint, Mostactive = ActiveUser,
                         streetname = mostSoughtStreetName, streetnr = mostsoughtstreet)
