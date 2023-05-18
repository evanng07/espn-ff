import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def get_draft_details(league_id, season_id, espn_cookies):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/0/leagues/{}?view=mDraftDetail&view=mSettings&view=mTeam&view=modular&view=mNav".format(season_id, league_id)
    r = requests.get(url,
                     headers=headers,
                     cookies=espn_cookies)
    espn_raw_data = r.json()
    espn_draft_detail = espn_raw_data
    draft_picks = espn_draft_detail['draftDetail']['picks']
    df = pd.DataFrame(draft_picks)

    draft_df = df[['overallPickNumber', 'playerId', 'teamId']].copy()
    return draft_df

def get_player_info(season_id, espn_cookies):
    custom_headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-fantasy-filter': '{"filterActive":null}',
        'x-fantasy-platform': 'kona-PROD-b72486ffb3d82002978cf0d1973c4dc783d0ac3d',
        'x-fantasy-source': 'kona'
    }
    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/{}/players?scoringPeriodId=0&view=players_wl".format(season_id)
    r = requests.get(url,
                     cookies=espn_cookies,
                     headers=custom_headers)
    player_data = r.json()
    df = pd.DataFrame(player_data)

    player_df = df[['defaultPositionId', 'fullName','id', 'proTeamId']].copy()

    player_df.rename(columns={'id': 'player_id'}, inplace=True)
    return player_df

def get_team_info(season_id):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/{}?view=proTeamSchedules_wl".format(season_id)
    r = requests.get(url,
                     headers=headers)
    team_data = r.json()
    team_names = team_data['settings']['proTeams']
    df = pd.DataFrame(team_names)

    team_df = df[['id', 'location', 'name']].copy()
    team_df['team name'] = team_df['location'].astype(str) +" "+ team_df['name']

    team_df.rename(columns={'id': 'team_id'}, inplace=True)
    return team_df