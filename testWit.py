from wit import Wit
access_token = 'ZYC3PPGBCNJY7KWUHVKBH6K4HZNTA3RE'
client = Wit(access_token)
msg = str(input('your question is ? \n'))
resp = client.message(msg)
print(resp)
keyWords = []
dict_entities = resp['entities']
for key in dict_entities.keys():
    for j in range(len(dict_entities[key])):
        keyWords.append(dict_entities[key][j]['value'])
print(keyWords)
