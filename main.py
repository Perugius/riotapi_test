import requests

api_key = "RGAPI-84e9c9c4-5abe-409d-a544-a6ab786f2d20"
region_dict = {"euw": "euw1", "eune": "eun1", "na": "na1"}

# inputting summoner info to search up
summoner_name = input("Input summoner name:")
summoner_region = input("Input summoner region:")
summoner_region = region_dict[summoner_region]


# dictionary of champions and their attributes/ids
champion_dict = requests.get("http://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/champion.json").json()


def get_summoner_id(reg, name):
    summoner_info = requests.get("https://"+reg+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name+"/?api_key="+api_key).json()
    return summoner_info["id"]


# dictionary for association of id number of champion with champion name for better readability
champ_key2id = []
for key in champion_dict["data"]:
    champ_key2id.append([key, champion_dict["data"][key]["key"]])  # (key, ":", champion_dict["data"][key]["key"])


# replacing champion number ids to in-game name and returning final mastery list
# includes query when requesting output of first n champs, or all champs when query is 0
def account_mastery(reg, sid, api, query):
    acc_mastery_dict = requests.get("https://"+reg+".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"+sid+"/?api_key="+api).json()
    for i in acc_mastery_dict:
        for j in champ_key2id:
            if i["championId"] == int(j[1]):
                i["championId"] = j[0]
    if query:
        return acc_mastery_dict[:query]
    #else:
        #return acc_mastery_dict


# return all entries in queue for a given summoner ID, mainly extract rank (tier + division) and winrate
# have to first separate flex rank and soloq rank
def get_rank_info(reg, sid, api):
    # return champion mastery entries sorted by number of champion points descending
    response = requests.get("https://"+reg+".api.riotgames.com/lol/league/v4/entries/by-summoner/"+sid+"/?api_key="+api).json()

    if not response: # check if response list is empty, if yes then summoner is unranked
        rank = ["Unranked"]
    # check both queue types to find soloq rank
    elif response[0]["queueType"] == "RANKED_SOLO_5x5":
        rank = [response[0]["tier"], response[0]["rank"], str(response[0]["leaguePoints"])+"LP", str(round(100*(response[0]["wins"]/(response[0]["wins"]+response[0]["losses"])), 2))+"% wr"]
    else:
        rank = [response[1]["tier"], response[1]["rank"], str(response[1]["leaguePoints"])+"LP", str(round(100*(response[1]["wins"]/(response[1]["wins"]+response[1]["losses"])), 2))+"% wr"]
    return rank


summoner_id = get_summoner_id(summoner_region, summoner_name)

# testing functions
for i in account_mastery(summoner_region, summoner_id, api_key, 3):
    print(i["championId"], "Level: "+str(i["championLevel"]), "Points: "+str(i["championPoints"]))

print(summoner_name, ":", get_rank_info(summoner_region, summoner_id, api_key))
