
import datetime



jours = { 'Monday': "lundi", 'Tuesday': "mardi", 'Wednesday': "Mercredi", 'Thursday': "jeudi", 'Friday': "vendredi", 'Saturday': "samedi", 'Sunday': "dimanche"}

mois = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

moisfr = ["janvier", "février", "mars", "avril","mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"] 


def convertdate(date):
    amj = date.split("-")
    moischiffre = int(amj[1])
    moislettre = mois[moischiffre - 1]
    jouren =  datetime.datetime.strptime(moislettre + " " + amj[2] + ", " + amj[0], '%B %d, %Y').strftime('%A')
    jourfr = jours[jouren]
    date_finale =  " " + jourfr + " " + amj[2] + " " + moisfr[moischiffre - 1]
    return date_finale


