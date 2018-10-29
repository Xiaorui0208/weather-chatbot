from wit import Wit
import request_orion
import random
"""
    Cette fonction permet d'initialiser la connexion avec la plateforme wit.ai
    elle prend comme paramètre le message de l'utilisateur, et elle renvoie 
    un dictionnaire qui contient les entités et les intentions
"""
def get_Wit_resp(msg):
    client = Wit('VNL5SPPZRQGD7MLIP3MYONFEXJBQ7QAF')
    resp = client.message(msg)
    return resp

"""
{
	"date":{"start":"2018-06-21", "end": "2018-06-21" },
	"time":{ "start":"20","end": "20","details": False},
	"weather": { "match":"pleuvoir", "forecast": True},
	"precipitation": True, 	
	"airtemperature": False, 
	"swellheight": False, 	
	"windspeed": False, 		
	"humidity": False, 		
	"autre_parametre": False 	
}
c'est une exemple de dictionnaire qu'utilise pour extraire des données

"""
"""
   Cette fonction permet de résoudre le décalage d'une heure lorsqu'il s'agit
   d'un interval, le paramètre end représente la fin de l'interval
   elle retourne la borne concernée sans le problème de décalage
   exemple pluie entre 20h et 22h
   la plateforme retourne start: 20h et end 23h
"""
def solve_time_issue(end):
    end1 = ''   #une chaine de caractère vide qu'on va retourner à la fin
    time = end[11:13] #time correspond à l'heure demandé
    date = end[8:10]  #date correspond à la date du jour demand
    if time == '00':
        hour = 23
        time = str(time)
        date = str(int(mia)-1)
    else:
        time = str(int(mio)-1)
    end1  = end1 + end[0:8] + date + 'T' + time + end[13:]
    return end1


"""

   cette fonction retourne soit un JSON soit une chaine de caractère
   si c'est une chaine de caractère renvoyer directement à l'utilisateur
   sinon on continue le traitement

"""
def get_Keywords(msg):
    resp = get_Wit_resp(msg)
    print("la reponse de wit: \n")
    print(resp)
    keys =['datetime', 'weather','airtemperature','precipitation','gust','windchill','winddirection','swellheight','humidity' ,'wavedirection','windspeed','mslpressure',"details","activite_mer","insult"]
    dico = {} #the final dictionnary
    dico1 = resp['entities'] #dictionnaire qui contient tous les entités présentes dans le message
    #print(dico1)
    liste = [ i for i in dico1]
    #print(liste)
    if len(liste) == 0 or ('salutation' in dico1 and dico1['salutation'][0]['confidence'] < 0.6) or ('insult' in dico1 and dico1['insult'][0]['confidence'] < 0.5)  :
        return {"message":"Je suis un chatbot spécialiste dans la météo. Je ne comprends pas ta réponse"}
    elif len(liste)==1:
        if liste[0] == 'salutation' and dico1['salutation'][0]['confidence'] > 0.6:
            salutations=["Bonjour", "Salut", "Hola", "Hello", "Hi", "Ni hao"]
            greeting=salutations[random.randint(0,len(salutations)-1)]
            return {"message":greeting+" \U0001F44B"}
        elif liste[0] == 'insult' and dico1['insult'][0]['confidence'] > 0.9:
            return {"message":"J'ai pas ton temps \U0001F595"}
    if "datetime" in dico1:
        dico2 = dico1['datetime']
        dico['datetime']={}
        if dico2[0]['type'] == 'interval':
            dico['datetime']['start'] = dico2[0]['from']['value'].split(".")[0] + 'Z'
            dico['datetime']['end'] = dico2[0]['to']['value'].split(".")[0] + 'Z'
            dico['datetime']['end'] = solve_time_issue(dico['datetime']['end'])
        else :
            dico['datetime']['start'] = dico2[0]['value'].split(".")[0] + 'Z'
            dico['datetime']['end'] = dico2[0]['value'].split(".")[0] + 'Z'
        for key in dico1.keys():
            if key == "weather":
                dico["weather"]={}
                dico["weather"]["forecast"]=True
                dico['weather']['match'] = dico1[key][0]['value']
            elif key=="activite_mer":
                sea_params=["gust","winddirection","windspeed","wavedirection","swellheight"]
                for param in sea_params:
                    dico[param]=True

            elif key != 'datetime' and key!= 'insult' and key in keys:
                dico[key] = True

        print("From Wit:  \n \n",  dico, "\n")
    else:
        print("Wit demande de compléter: \n ", {"message":"pour quand ?","complement":""})

        return {"message":"pour quand ?","complement":""}
            
    return request_orion.sort_data(dico)
 
