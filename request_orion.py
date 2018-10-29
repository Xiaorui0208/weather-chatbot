import requests
import responseGenerator
#############################r json keys#############################

####################################### weather index matching ####################################
weather_matching={  0:"orage avec averse de neige",1:"orage avec averse de grêle",2:"orage avec averse de grésil",3:"orage et pluie", 4:"averses de grêle",5:"grésil",6:"averses de neige", 
                    7:"averses de pluie et de neige", 8:"averses de pluie",9:"pluie et neige fortes",10:"pluie et neiges modérées",11:"pluie et neige faibles", 12:"neige forte", 13:"neige modérée",
                    14:"neige faible",15:"pluie vergalaçante forte",16:"pluie vergalaçante modérée",17:"pluie vergalaçante faible",18:"pluie forte", 19:"pluie modérée", 20:"pluie faible", 21:"bruine forte",
                    22:"bruine modérée", 23:"bruine faible", 24:"brouillards",25:"brumes en blancs", 26:"brouillards de rayonnement",27:"voile de nuages élevés", 28:"ciel couvert",29:"très nuageux",
                    30:"nuageux",31:"peu nuageux",32:"ciel clair"}
# for x in weather_matching:
#         print(x, ": ", weather_matching[x], "\n")

###################################################################################################
#url = https://data2.weathernco.com/point?format=chatbot&variables=humidity,airtemperature,gust,wavedirection&lat=48.354513&lon=-4.56433&start=2018-06-12T00:00:00Z&end=2018-06-12T23:00:00Z

#'02' et '10'  par exmple pour 2h et 10h
def time_splitter(start_time, end_time): 
    start=int(start_time)
    end=int(end_time)
    if end<start:
        end,start=start,end
    if end-start<=3:
        pas=1
    elif end-start<=7:
        pas=2
    else:
        pas=round((end-start)/3)
    output=[start]
    while output[-1]+pas<=end:
        output.append(output[-1]+pas)
    if output[-1]!=end and pas>=3:
        output.append(end)
    return ["%02d"%(x) for x in output] # ['02','05','08','10']

# extraire  l'heure de début et l'heure de fin  du dico_wit et normaliser le format
def get_datetimes(dico_wit):
    try:
        start_datetime=dico_wit["datetime"]["start"][0:13]+":00:00Z"
    except Exception as e:
        error_message="start date undefined"
        print(error_message)
        #raise e
    try:
        end_datetime=dico_wit["datetime"]["end"][0:13]+":00:00Z"
    except Exception as e:
        raise e 
    if start_datetime==end_datetime:
        #print("je decale d'1h")
        #if
        end_time="%02d"%(int(end_datetime.split('T')[1].split(':')[0])+1)
        if end_time=='01':
            end_time="%02d"%(int(end_time) +19)
        else:
            end_time=str(end_time)
        end_datetime=start_datetime.split('T')[0]+"T"+end_time+":00:00Z"
    # print(end_datetime)
    # print(start_datetime)
    return start_datetime, end_datetime

# remplacer la description du météo et compter la pourcentage pour chaque status
def common_weather(sorted_data):
    common_params=["pluie","nuage","orage","neige","ciel clair","ciel couvert"]
    for dateX in sorted_data:
        forecast=sorted_data[dateX]["weather"]["forecast"] #list
        common_weatherX={}
        for weather in forecast :
            for params in common_params:
                if params in weather :
                    if params in common_weatherX:
                        common_weatherX[params]+=1
                    else:
                        common_weatherX[params]=1
        for params in common_weatherX:
            common_weatherX[params] = format(common_weatherX[params]/len(forecast), '0.0%')
        sorted_data[dateX]["weather"]["forecast"]=common_weatherX

# chercher les variables  de dico_wit
def getVariables(dico_wit):
    variables =['weather']
    allVariables = ['airtemperature','precipitation','gust','windchill','winddirection','swellheight','humidity' ,'wavedirection','windspeed','mslpressure']
    for variable in allVariables:
      if variable in dico_wit and dico_wit[variable]:
        variables.append(variable)
    return variables

# envoyer le request au serveur orion pour récupère les données météo
def get_data(dico_wit):
    start,end = get_datetimes(dico_wit)
    lat=48.354513
    lon=-4.56433
    variables=getVariables(dico_wit)
    payload = {'format':'chatbot', 'variables': variables, 'lat':lat, 'lon':lon, 'start':start, 'end':end}
    r = requests.get('https://data2.weathernco.com/point', params=payload)
    #r.status_code
    if r.status_code!=200:
        print("error ",r.status_code)
        return {"message":"données non disponible"}
    else:
        #print("donnees serveur directes: \n ",r.json())
        return r.json()
    

  #  traiter les données météo et formaliser le format adapté
def sort_data(dico_wit):
    dico_server = get_data(dico_wit)
    if "message" in dico_server:
        #print("Internal Server Error")
        return dico_server
    output={}
    sorted_data={} # dico_Virgile
    #faire un boucle de dico_serveur pour chercher les valeurs maximal des variables correspondant à chaque jour
    for datetime in dico_server:
        dateX=datetime.split('T')[0]  
        if dateX not in sorted_data:
            sorted_data[dateX]={'time':{"start":datetime.split('T')[1].split(':')[0],"end":datetime.split('T')[1].split(':')[0]},
                                "weather":{"forecast":[ weather_matching[dico_server[datetime]["weather"] ]] , "match":"" } }
            for params in dico_server[datetime]:
                if params not in ["weather","latitude", "longitude"]:
                    if dico_server[datetime][params]==None:
                        if params=="airtemperature":
                            sorted_data[dateX][params]={"max":0.0,"min":0.0}
                        else:
                            sorted_data[dateX][params]=0.0
                    else:
                        if params=="airtemperature":
                            sorted_data[dateX][params]={"max":dico_server[datetime]["airtemperature"],"min":dico_server[datetime]["airtemperature"]}
                        else:
                            sorted_data[dateX][params]=dico_server[datetime][params]
        else:
            new_time=datetime.split('T')[1].split(':')[0]
            start=sorted_data[dateX]["time"]["start"]
            start=(start>new_time)*new_time+(start<=new_time)*start
            end=sorted_data[dateX]["time"]["end"]
            end=(end<new_time)*new_time+(end>=new_time)*end
            sorted_data[dateX]["time"]={"start":start,"end":end}
            if dico_server[datetime]["weather"]:
                sorted_data[dateX]["weather"]["forecast"].append(weather_matching[ dico_server[datetime]["weather"] ])

            for params in dico_server[datetime]:
                if params not in ["weather","latitude", "longitude"]:
                    if dico_server[datetime][params]==None:
                        dico_server[datetime][params]=0

                    if params=="airtemperature":
                        new_temperature=dico_server[datetime]["airtemperature"]
                        max_temperature=sorted_data[dateX]["airtemperature"]["max"]
                        min_temperature=sorted_data[dateX]["airtemperature"]["min"]
                        sorted_data[dateX][params]={"max": (max_temperature<new_temperature)*new_temperature+(max_temperature>=new_temperature)*max_temperature,
                                                    "min":(min_temperature>new_temperature)*new_temperature+(min_temperature<=new_temperature)*min_temperature}
                    else:
                        max_params=sorted_data[dateX][params]
                        new_params=dico_server[datetime][params]
                        sorted_data[dateX][params]=(max_params<new_params)*new_params+(max_params>=new_params)*max_params
    #print("donnees Orion triees \n :", sorted_data)
    common_weather(sorted_data)
    if  "weather" in dico_wit and dico_wit["weather"]["match"]:
        for dateX in sorted_data:
            sorted_data[dateX]["weather"]["match"]=False
            for forecast in sorted_data[dateX]["weather"]["forecast"]:
                if dico_wit["weather"]["match"] in forecast:
                    sorted_data[dateX]["weather"]["match"]=True

    if len(sorted_data)!=0:
        output["synthese"]=sorted_data

    # si "details " dans le dico_wit,  on retourner  les données météo par heure de chaque jour
    if "details" in dico_wit and dico_wit["details"]:
        if len(sorted_data)==1: # one single date
            all_dates=[dateY for dateY in sorted_data]
            #print(all_dates)
            single_date=all_dates[0]
            output["details"]={}
            start,end=sorted_data[single_date]["time"]["start"],sorted_data[single_date]["time"]["end"]
            times=time_splitter(start,end)
            datetimes=[single_date+"T"+time+":00:00Z" for time in times]
            for datetime in datetimes:
                if datetime in dico_server:
                    output["details"][datetime]=dico_server[datetime]
                    if "weather" in dico_server[datetime]:
                        output["details"][datetime]["weather"]=weather_matching[dico_server[datetime]["weather"]]
                    del output["details"][datetime]["latitude"]
                    del output["details"][datetime]["longitude"]
            if len(output["details"])==0:
                del output["details"]

    print(" \n From Orion: \n",output, "\n ")
    #virgile_file.make_response(sorted_data)
    return responseGenerator.generator(output)




# get_data(dico_wit)








