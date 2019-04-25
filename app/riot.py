import requests
from app import api

api_url = api.app.config['RIOT_API_URL']
api_key = api.app.config['RIOT_API_KEY']

def get_basic_summoner_info(summoner_name):
    summoner = _get_summoner(summoner_name)
    summoner = _get_rank(summoner)
    return summoner
    
def get_champions(summoner_id):
    request_url = api_url + '/lol/champion-mastery/v3/champion-masteries/by-summoner/' + str(summoner_id)
    payload = {'api_key':api_key}
    resp = requests.get(request_url, params=payload)
    api.app.logger.debug(resp.url)
    riot_response = resp.json()
    if (len(riot_response) != 0):
        summoner['champions'] = {}
        for champ in riot_response:
            summoner['champions'][str(champ['championId'])] = champ
    return summoner

def get_matches(account_id, matchCount):
    matches_url = api_url + '/lol/match/v3/matchlists/by-account/' + str(account_id)
    
    payload = {
        'api_key': api_key,
        'endIndex': matchCount
    }
    resp = requests.get(matches_url, params=payload)
    api.app.logger.debug(resp.url) 
    riot_response = resp.json()
    matches = riot_response['matches']
    api.app.logger.debug("matches found: %s" % len(matches))
    result = {}
    for match in matches:
        timeline_url =  api_url + '/lol/match/v3/timelines/by-match/' + str(match['gameId'])
        match_info_url = api_url + '/lol/match/v3/matches/%s' % str(match['gameId'])
        payload = {'api_key': api_key}
        timeline_resp = requests.get(timeline_url, params=payload)
        match_resp = requests.get(match_info_url, params=payload)
        api.app.logger.debug(match_resp.url)
        api.app.logger.debug(timeline_resp)
        result[str(match['gameId'])] = {}
        result[str(match['gameId'])]['match_info'] = match_resp.json()
        result[str(match['gameId'])]['timeline'] = timeline_resp.json()

    return result

def _get_summoner(name):
    summoner = {}
    request_url = api_url + '/lol/summoner/v3/summoners/by-name/' + name 
    payload = {'api_key':api_key}
    resp = requests.get(request_url, params=payload)
    api.app.logger.debug(resp.url)
    if resp.status_code == 200:
        api.app.logger.debug("good")
        riot_summoner = resp.json() 
        summoner['name'] = riot_summoner['name']
        summoner['account_id'] = riot_summoner['accountId']
        summoner['summoner_id'] = riot_summoner['id']
        summoner['level'] = riot_summoner['summonerLevel']
        return summoner
    else:
        app.logger.error(resp.text)
        return resp.json()

def _get_rank(summoner):
    request_url = api_url + '/lol/league/v3/positions/by-summoner/' + str(summoner['summoner_id'])
    payload = {'api_key':api_key}
    resp = requests.get(request_url, params=payload)
    api.app.logger.debug(resp.url)
    riot_response = resp.json()
    if (len(riot_response) != 0):
        summoner['rank'] = riot_response[0]['tier'] + ' ' + riot_response[0]['rank']
        if (riot_response[0]['leaguePoints']):
            summoner['lp'] = riot_response[0]['leaguePoints']
    return summoner 