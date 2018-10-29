########################################################################################################################
########################################################################################################################
############Ce que je reçois de Driss. Ca reste globalement simple. Si besoin on va complexifier davantage##############
########################################################################################################################
########################################################################################################################
#############################r json keys#############################

weather="weather[unit=\"Index [0-32]\"]"
latitude="latitude[unit=\"degrees_north\"]"
longitude="longitude[unit=\"degrees_east\"]"
temperature="airtemperature[unit=\"°C\"]"
precipitation="precipitation[unit=\"mm/h\"]"
gust="gust[unit=\"Kts\"]" #vitesse rafale
windchill="windchill[unit=\"°C\"]" # refroidissement eolien
winddirection="winddirection[unit=\"Degree (N=0)\"]" 
swellheight="swellheight[unit=\"m\"]"#hauteur houle
humidite="humidity[unit=\"%\"]"
wavedirection="wavedirection[unit=\"Degree true\"]"
windspeed="windspeed[unit=\"Kts\"]"
mslpressure="mslpressure[unit=\"hPa\"]"


dico_Driss={
	"date":{ 	# les dates de début et de fin sont identiques si la question porte sur une seule journée          		
			"start":"yyyy-mm-dd",	#date début (si intervalle de jours). Mind the format!
			"end": "yyyy-mm-dd" 	#date de fin
	}

	"time":{ 	#les heures de début et de fin sont identiques si la question porte sur une heure précise. Elles sont 09h et 10h si la question porte sur 09:mm par exemple
		"start":"hh",
		"end": "hh",
		"details": "true, if details wanted within the time interval. false otherwise"

	}

	"weather": { #la météo annoncée
		"match":"neige ou \" ciel clair\"", #si la question est de vérifier un temps particulier
											#(c'est le cas en général des questions qui commencent par "Est-ce que...?")
											#est ce qu'il fera beau cet après midi? Est ce qu'il y aura du soleil demain? --> "match"= "ciel clair"
											#est ce qu'il va neiger dans les trois prochains jours? -->"match"="neige"
											#est ce qu'il y aura un orage demain? --> "match"="orage"
											#Est-ce qu’il va pleuvoir demain matin à 8h? -->"match"="pluie"

		"forecast":"true or false"			#"true" si la météo, le temps météo, les conditions météo... sont demandées. Très souvent ce sera true. 
											# il permet d'avoir au moins une réponse générale (faute de mieux) à une question imprévue
	},


	"precipitation": "true or false", 	#pour demander la valeur des précipitations 
	"airtemperature": "true or false", 	#pour demander la valeur de la température ambiante
	"swellheight": "true or false", 	#pour demander la hauteur max des vagues 
	"windspeed": "true or false", 		#pour demander la vitesse du vent
	"humidity": "true or false", 		#pour demander le pourcentage de l'humidité du vent
	"autre_parametre" : "true or false" 	#pour demander la valeur de autre_parametre
}

###############################################################################################################
###############################################################################################################
############################### Ce que je donne à Virgile #####################################################
###############################################################################################################
###############################################################################################################

#############################################################################################################################################################################
# si demande météo (du jour) 									# je fournis la météo du JOUR (temps météo: pluie, orage, neige, brouillard...etc) + température min et max #
#																# dans la journée																							#
#############################################################################################################################################################################
# si demande les détails sur la météo du jour 					# je donne température max et min dans la journée, l'humidité max et min dans la journée le pic de 			#
#																# précipitations et le vent																					#
#############################################################################################################################################################################
# si demande la météo sur les x prochaines HEURES 				# je donne (temps météo et température) par heure sur les x heures indiquées								#
#############################################################################################################################################################################
# si demande la météo sur les x prochains JOURS 				# je donne temps, température max et min (pas d'autres détails)													#
#############################################################################################################################################################################

dico_Virgile={
	"date1": { #le format reste le même "yyyy-mm-dd"
		"time":{ #time interval within a day
			"start":"hh",
			"end" : "hh"
			},

		"weather": {
			"forecast": ["nuage épais", "averses de pluie", "pluie", "peu nuageux"],
			"match": true or false or "je prévois un temps sec pour cet apres midi" or "",
			},
		"precipitation": {
			"value":"max value of precipitation",
			"description": "forte" or "faible" or "moyenne"
			},
		"airtemperature":{
			"max": "max value of air temperature",
			"min":"min value of air temperature"
			},
		"swellheight":{
			"value": "max height in the time interval",
			"description": "haute" or "basse"
			},
		"windspeed":{
			"value": "max value in the time interval",
			"description": "alerte orange, vert, bleu noir..."
			},
		"humidity": "max value in the time interval",

		"autre_parametre" : "max value in the time interval",

		"details":{
			"datetime1":{#yyyy-mm-dd-hh
				"weather": "nuage épais", "airtemperature": "value at this datetime", "autre_parametre": "value at this date"},
			"datetime2":{#yyyy-mm-dd-hh
				"weather": "nuage épais", "airtemperature": "value at this datetime", "autre_parametre": "value at this date"},
			"datetime3":{#yyyy-mm-dd-hh
				"weather": "nuage épais", "airtemperature": "value at this datetime", "autre_parametre": "value at this date"},
			"datetime4":{#yyyy-mm-dd-hh
				"weather": "nuage épais", "airtemperature": "value at this datetime", "autre_parametre": "value at this date"},
			"datetime5":{#yyyy-mm-dd-hh
				"weather": "nuage épais", "airtemperature": "value at this datetime", "autre_parametre": "value at this date"}

			}

		},

	"date2": { #le format reste le même "yyyy-mm-dd"
		"time":{ #time interval within a day
			"start":"hh",
			"end" : "hh"
			},

		"weather": {
			"forecast": ["nuage épais", "averses de pluie", "pluie", "peu nuageux"],
			"match": true or false or "je prévois un temps sec pour cet apres midi" or "",
			},	
	       precipitation: {
			"value":"max value of precipitation",
			"description": "forte" or "faible" or "moyenne"
			},
		"airtemperature":{
			"max": "max value of air temperature",
			"min":"min value of air temperature"
			},
		"swellheight":{
			"value": "max height in the time interval",
			"description": "haute" or "basse"
			},
		"windspeed":{
			"value": "max value in the time interval",
			"description": "alerte orange, vert, bleu noir..."
			},
		"humidity": "max value in the time interval",

		"autre_parametre": "max value in the time interval",

		"details":{
			"datetime1":{#yyyy-mm-dd-hh
				"weather": "nuage épais", "airtemperature": "value at this datetime", "autre_parametre": "value at this date"},
			"datetime2":{#yyyy-mm-dd-hh
				"weather": "nuage épais", "airtemperature": "value at this datetime", "autre_parametre": "value at this date"},
			"datetime3":{#yyyy-mm-dd-hh
				"weather": "nuage épais", "airtemperature": "value at this datetime", "autre_parametre": "value at this date"},
			"datetime4":{#yyyy-mm-dd-hh
				"weather": "nuage épais", "airtemperature": "value at this datetime", "autre_parametre": "value at this date"},
			"datetime5":{#yyyy-mm-dd-hh
				"weather": "nuage épais", "airtemperature": "value at this datetime", "autre_parametre": "value at this date"}

			}

		},
		"datex":{
				{{

					}


					}
			}

	}


#################################################################################################################################################################
#################################################################################################################################################################
##################################################### Exemples ##################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################

#User: Quel temps fait-il ce soir?
dico_Driss={
	"date":{
		"start":"2018-05-27",
		"end":"2018-05-27"
	},
	"time":{
		"start":"18",
		"end":"22",
		"details": false,
	},
	"weather":{
		"match": "",
		"forecast": true
	}, 
	"temperature": true
}

dico_Virgile={
	"2018-05-27":{
		"time":{
			"start":"18",
			"end":"22"
		},
		"weather":{
			"match":"",
			"forecast":["ciel clair","ciel clair","ciel clair","nuageux", "pluie"]  #pour 18h, 19h, 20h, 21h, 22h
		},
		"airtemperature":{#en degré celcius
			"max":24,
			"min":13
		}
	}
}
#Bot: 	Voici la météo de Brest du 27  mai entre 18h et 22h.
#		Temps: ciel clair en général avec nuage et pluie en fin de soirée
#		Temperature: de 13 à 24


#User: détails météo aujourd'hui

dico_Driss={
	"date":{
		"start":"2018-05-27",
		"end":"2018-05-27"
	},
	"time":{
		"start":"07",
		"end":"22",
		"details": false,  #l'intervalle de temps est trop large, on fournit plus de paramètres météo et  ne pas les détailler par heure
	},
	"weather":{
		"match": "",
		"forecast": true
	}, 
	"airtemperature": true,
	"precipitation": true,
	"humidity": true,
	"windspeed": true
}

dico_Virgile={
	"2018-05-27":{
		"time":{
			"start":"07",
			"end":"22"
		},
		"weather":{
			"match":"",
			"forecast":["ciel clair","ciel clair","ciel clair","nuageux", "pluie", "pluie", "....", "ciel couvert"]  #pour 07h, 08h, ..., 20h, 21h, 22h
		},
		"airtemperature":{#en degré celcius entre 07h et 22h
			"max":27,
			"min":9
		},
		"precipitation": {
			"value":"50mm",
			"description": "pluie forte"
		},
		"humidity": "70%",
		"windspeed": {
			"value": "12 noeuds",
			"description":"alerte bleue"  # du n'importe quoi :-D
		},

	}
}

#Bot: 	Voici la météo de Brest du 27  mai entre 07h et 22h.
#		Temps: ciel clair 33%, pluie 52%, nuageux 10%, orage 5%
#		Temperature: de 9 à 27
#		precipitation: jusqu'à 50mm
#		humidité: jusqu'à 70%
#		vitesse du vent: jusqu'à 12 noeuds( alerte bleu)
