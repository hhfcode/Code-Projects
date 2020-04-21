from flasksite.models import soughtgps, emailsos, db, bikeGps, Post, User, gps, streetandCity
import numpy as np
import matplotlib.pyplot as plt
from statistics import mode

#Finds how many SoS Email has been sent + Most Active Recipent
def SoSemailsent():
    totalemailslist = []
    totalmailsent = []
    emailid = emailsos.query.all()
    for ids in emailid:
        totalemailslist.append(ids.email)
        totalmailsent.append(ids.id)
    #Mode Takes the most occuring element and selects it to be put into our vararible
    mostcommonEmailAddress = mode(totalemailslist)
    return mostcommonEmailAddress, totalmailsent[-1]

def MostActiveUser():
    postalID = []
    Idposts = Post.query.filter_by(user_id = Post.user_id).all()
    for ints in Idposts:
        postalID.append(ints.user_id)
    mostActivePoster = mode(postalID)
    UserActive = User.query.filter_by(id=mostActivePoster).first()
    postmostactive = UserActive.username
    return postmostactive

def mostsoughtafterLocationForABike():
     list = []
     listtwo = []
     idstreetandcity = streetandCity.query.all()
     for each in idstreetandcity:
         list.append(each.street)
         listtwo.append(each.city)
     mcstreet = mode(list)
     mccity = mode(listtwo)
     return mcstreet, mccity




