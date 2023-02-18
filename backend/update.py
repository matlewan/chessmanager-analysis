import bs4
import json
import os
import pandas as pd
import re
import requests

from data import *

def download_players(tournament_url : str) -> list[Result]:
    df = pd.read_html(f'{tournament_url}/players')[0]
    players = []
    for _,row in df.iterrows():
        _,_,title,name,club,rating,birthdate,_ = row
        b = 0 if pd.isna(birthdate) else int(birthdate)
        r = 1000 if pd.isna(rating) else int(rating)
        t = "" if pd.isna(title) else title
        c = "" if pd.isna(club) else club
        r = Player(norm_player(name), t, c, b, r)
        players.append(r)
    return players

def norm_player(player):
    try:
        p = player.replace(', ', ' ').replace(',', ' ')
        x = p.split()
        return f"{x[0]} {x[1]}"
    except:
        return player


def download_matches(tournament_url : str, tournament : str, rounds : int) -> list[Match]:
    matches = []
    for round in range(1,rounds+1):
        round_url = f"{tournament_url}/rounds/{round}"
        matches += download_round(round_url, tournament, round)
    return matches

def download_round(url : str, tournament : str, round : int) -> list[Match]:
    matches = []
    df = pd.read_html(url)[0]
    for _,row in df.iterrows():
        _, _, _, player1, _, _, result, _, _, player2, _, _, _ = row
        white = norm_player(player1)
        black = norm_player(player2)
        result = {'0':0.0, '1':1.0}.get(result.split()[0], 0.5)
        m = Match(tournament, round, white, black, result)
        matches.append(m)
    return matches

def download_results(tournament_url : str, tournament : str, rounds : int) -> list[Result]:
    df = pd.read_html(f'{tournament_url}/results/{rounds}')[0]
    results = []
    for _,row in df.iterrows():
        place, _, _, player, _, _, _, pts, bch1, bch, _, _, _, _, _ = row
        r = Result(tournament, norm_player(player), int(place), float(pts), float(bch1), float(bch))
        results.append(r)
    return results

def download_tournaments(filter_url : str, search_phrase : str) -> list[Tournament]:
    offset = 0
    tournaments = []
    while True:
        url = f"{filter_url}&offset={offset}"
        print(offset, end=' ')
        t = subdownload_tournaments(url, search_phrase)
        if t == []:
            break
        tournaments += t
        offset += 50
    print()
    return tournaments

def subdownload_tournaments(url : str, search_phrase : str) -> list[Tournament]:
    tournaments = []
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.content, "html.parser")

    for a in soup.find_all('a', 'tournament'):
        if search_phrase not in a.text:
            continue
        words = re.split(r'\s{2,}', a.text)
        id = a.attrs['href'].split('/')[-1]
        date = words[1]
        rounds = int(words[2].split('/')[0])
        tname = words[3].split()[-1]
        tname = tname if '.' in tname else ('#1.' + tname[-1])
        players = int(words[5].split()[0])
        t = Tournament(id, tname, date, players, rounds)
        tournaments.append(t)
    return tournaments

def load(filename : str) -> Data:
    with open(filename) as file:
        j = json.load(file)
        return Data(**j)

def save(filename : str, data : object):
    with open(filename, 'w') as file:
        jsonString = json.dumps(data, default=lambda o: o.__dict__, indent=2, ensure_ascii=False)
        file.write(jsonString)

def _update(filename:str, data : Data, url : str, search_phrase : str):
    names = { r['tournament'] for r in data.results }
    players = {p['name'] : p for p in data.players}
    data.tournaments = download_tournaments(url, search_phrase)
    for t in data.tournaments[::-1]:
        if t.name in names:
            continue
        print(t.name, end=" ")
        url = f"https://www.chessmanager.com/en/tournaments/{t.id}"
        try:
            data.results += download_results(url, t.name, t.rounds)
            print()
        except:
            print('fail') # case when tournament is not finished yet
            continue
        data.matches += download_matches(url, t.name, t.rounds)
        for p in download_players(url):
            players[p.name] = p
        data.players = list(players.values())
        save(filename, data)
    
# download_matches('https://www.chessmanager.com/en/tournaments/6008432340500480', '#13.3', 7)
# download_results('https://www.chessmanager.com/en/tournaments/6008432340500480', '#13.3', 7)
# download_players('https://www.chessmanager.com/en/tournaments/6008432340500480')
# download_tournaments('https://www.chessmanager.com/en/tournaments?name=Pomys%C5%82+GrandPrix', 'Pomysł GrandPrix')
# save('./data.json', data)
# data = load('./data.json')
# update(data, 'https://www.chessmanager.com/en/tournaments?name=Pomys%C5%82+GrandPrix', 'Pomysł GrandPrix')

def update(filename):
    url = 'https://www.chessmanager.com/en/tournaments?name=Pomys%C5%82+GrandPrix'
    search_phrase = 'Pomysł GrandPrix'

    data = load(filename) if os.path.isfile(filename) else Data([],[],[],[],[])
    _update(filename, data, url, search_phrase)

if __name__ == "__main__":
    update('data.json')
