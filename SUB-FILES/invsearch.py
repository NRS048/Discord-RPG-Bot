import json

id = int(input("what id \n"))

def invList(discid):
    invContent = []
    invItem = []
    possibleItems = []
    with open("items.json", 'r') as invFile:
        invData = json.load(invFile)

    with open("playerdata.json", 'r') as playerFile:
        playerData = json.load(playerFile)
        
    for z in playerData["player_stats"]:
        if z["discid"] == discid:
            invContent = z["inventory"]
    
    for y in invData["items"]:
        possibleItems.append(y["name"])

    for x in invContent:
        invItem.append(possibleItems[x])
    
    return invItem

print(invList(id))