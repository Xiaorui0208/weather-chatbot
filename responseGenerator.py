#from colorterm import colorterm
import dateconverter
emoji={"ciel couvert":"\U0001F325","nuage":"\U00002601","ciel clair":"\U00002600","pluie":"\U00002614","orage":"\U000026A1","brouillards":"\U0001F32B","neige":"\U00002744",
        "airtemperature":"\U0001F321","puce":"\U000025AB","humidite":"\U0001F4A7","vitesseDuVent":"\U0001F32C","rafaleVent":"\U0001F32A","temperatureRessentit":"\U0001F321 ",
    "directionVent":"\U000027A1","hauteurVague":"\U0001F30A","directionVague":"\U00002196","pression":"\U0001F37E"}#dictionnaire paramètre/emoji

emoji_param={"airtemperature":"airtemperature","precipitation":"pluie","humidity":"humidite","windspeed":"vitesseDuVent","gust":"rafaleVent","windchill":"temperatureRessentit",
    "winddirection":"directionVent","swellheight":"hauteurVague","wavedirection":"directionVague","mslpressure":"pression"} #dictionnaire paramètre/signification


units={"airtemperature":"°C","precipitation":"mm/h","humidity":"%","windspeed":"noeuds","gust":"noeuds","windchill":"°C",
    "winddirection":"°Nord","swellheight":"m","wavedirection":"°","mslpressure":"hPa"} #dictionnaire paramètre/unitées
def description_pluie(param):  #fonction qui retourne la description de la pluie
    if param ==0:
        return " il ne pleut pas"
    elif param <1:
        return "très faible"
    elif param<=3:
        return "faible modérée"
    elif param <= 7:
        return "moyenne"
    else :
        return "forte"
    
def generation(dico): # Pour chaque paramètre présent dans le fichier JSON extrait du serveur, la fonction va associé son nom aux données météo(avec les unités) et afficher les 2.
    msg=""
    tempo_dic = {}
    for dateX in dico: #Le premier paramètre (la première clé)renvoyé par le serveur météo est la date.
        tempo_dic = dico[dateX]
        liste = [i for i in tempo_dic]
        msg += dateconverter.convertdate(dateX) + " " + dico[dateX]["time"]["start"]+"h" + "-" + dico[dateX]["time"]["end"]+"h \n" # message qui retourne la date et l'heure demandé par l'utilisateur. On prend les valeurs associé au début et à la fin de l'intervalle de temps choisis.
        if "weather" in liste : #pour chaque paramètre dans le dictionnaire météo..
            ch = ""
            for keys in dico[dateX]["weather"]["forecast"]:
                ch += emoji[keys] +" "+ dico[dateX]["weather"]["forecast"][keys]+" " #..la fonction va retourner l'émoji correspondant, et les valeurs des données météo associé au paramètre.
            msg += "Météo "+" :"+ ch+"\n"
    
        if "airtemperature" in liste :
            msg += "Température "+emoji["airtemperature"]+" :" + str(dico[dateX]["airtemperature"]["min"]) + "°C à " + str(dico[dateX]["airtemperature"]["max"]) + "°C.\n"
            # if "precipitation" in liste :
            #     msg += "Les précipitations sont de "+ str(dico[dateX]["precipitation"]["value"])+"mm"+",c'est une "+str(dico[dateX]["precipitation"]["description"])+".\n"
        if "precipitation" in liste :
           
           msg += "Pluie "+emoji["pluie"]+" :"+ str(dico[dateX]["precipitation"])+"mm/h"+","+description_pluie(dico[dateX]["precipitation"])+".\n"
        if "humidity" in liste :
            msg += "Humidité "+emoji["humidite"]+" :"+str(dico[dateX]["humidity"])+"%.\n"
            # if "windspeed" in liste :
            #     msg += "La vitesse du vent est de "+str(dico[dateX]["windspeed"]["max"])+"-c'est un vent "+str(dico[dateX]["windspeed"]["description"])+".\n"
        if "windspeed" in liste :
            msg += "Vitesse du vent "+emoji["vitesseDuVent"]+" :"+str(dico[dateX]["windspeed"])+ " nds max.\n"
        if "gust" in liste :
            msg += "Rafales "+emoji["rafaleVent"]+" :"+str(dico[dateX]["gust"])+" nds max.\n"
        if "windchill" in liste :
            msg += "Température ressentie "+emoji["temperatureRessentit"]+" :"+str(dico[dateX]["windchill"])+"°C.\n"
        if "winddirection" in liste :
            msg += "Direction du vent "+emoji["directionVent"]+" :"+str(dico[dateX]["winddirection"])+"Degrés Nord.\n"
        if "swellheight" in liste :
            msg += "Hauteur de la houle "+emoji["hauteurVague"]+" :"+str(dico[dateX]["swellheight"])+"m.\n"
        if "wavedirection" in liste :
            msg += "Direction des vagues "+emoji["directionVague"]+" :"+str(dico[dateX]["wavedirection"])+"DegrésAngle.\n"
        if "mslpressure" in liste :
            msg += "Pression Atmosphérique "+emoji["pression"]+" :"+str(dico[dateX]["mslpressure"])+"hPa.\n"
    return msg


#dico ={'2018-06-27': {'weather': {'match': False, 'forecast': {'nuage': '100%'}}, 'time': {'start': '00', 'end': '01'}, 'precipitation': 0.0}}                                                              
#Bot: 	Voici la météo de Brest du 27  mai entre 07h et 22h.
#		Temps: ciel clair 33%, pluie 52%, nuageux 10%, orage 5%
#		Température: de 9° à 27°
#		Précipitation: jusqu'à 50mm
#		Humidité: jusqu'à 70%
#		Vitesse du vent: jusqu'à 12 noeuds(alerte bleue)
#print  (generation(dico))

def details(les_details): #les_details={datetime1: {....}, datetime2:{....}}
    msg=""
    output=[]
    for datetimeX in les_details:
        msg_horaireX="\n"+str(datetimeX.split('T')[1].split(':')[0])+"h: "
        msg_emoji=""
        for param in les_details[datetimeX]:
            if param=="weather":
                msg_horaireX+=les_details[datetimeX][param]+" "
            elif param in emoji_param and param in units:
                msg_emoji+= param + ": "+emoji[emoji_param[param]]+" "+str(les_details[datetimeX][param])+units[param]+" \n"
        output.append(msg_horaireX+msg_emoji)
    if len(output)==0:
        return {"message":"je suis désolé de ne pouvoir te donner plus de détails. \n Réessaie une autre fois peut être."}
    else:
        msg+="Les détails: \n"
        output.sort()
        print("voici output: \n \n ")
        print(output)
        for msg_horaireX in output:
            msg+=msg_horaireX
        return {"message":msg}



def generator(orion_data): #fonction qui assure l'extraction des données depuis le serveur météo 
    print("\n From ResponseGenerator: \n")
    if "details" in orion_data:
        return details(orion_data["details"])
    elif "synthese" in orion_data:
        return {"message":generation(orion_data["synthese"]), "details":""}
        
    return {message:"je n'arrive pas à synthétiser un réponse correcte avec les donnees d'Orion :-( "}


