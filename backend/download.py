import datetime
import bs4
import json
import os
from dacite import from_dict
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
        p = re.sub(r', ?', ' ', player)
        return re.sub(r' \(.*', '', p).strip()
    except:
        return player


def download_rounds(tournament_url : str, n_rounds : int) -> list[Match]:
    rounds = []
    for n_round in range(1,n_rounds+1):
        round = Round(n_round, [])
        df = pd.read_html(f"{tournament_url}/rounds/{n_round}")[0]
        for _,row in df.iterrows():
            _, _, _, player1, _, _, result, _, _, player2, _, _, _ = row
            white = norm_player(player1)
            black = norm_player(player2)
            result = {'0':0.0, '1':1.0}.get(result.split()[0], 0.5)
            m = Match(white, black, result)
            round.matches.append(m)
        rounds.append(round)
    return rounds

def download_results(tournament_url : str) -> list[Result]:
    df = pd.read_html(f'{tournament_url}/results')[0]
    results = []
    for _,row in df.iterrows():
        place, _, _, title, player, _, _, _, pts, bch1, bch, _, _, _, _, _ = row
        r = Result(norm_player(player), int(place), float(pts), float(bch1), float(bch))
        results.append(r)
    return results

def download_tournaments(filter_url : str) -> list[Tournament]:
    offset = 0
    tournaments = []
    while True:
        print(f"Offset: {offset}")
        t = download_tournaments_page(filter_url, offset)
        if t == []:
            break # no tournaments on page with given offset
        tournaments += t
        offset += 50
    print()
    return tournaments

def download_tournaments_page(url : str, offset: int) -> list[Tournament]:
    tournaments = []
    resp = requests.get(f"{url}&offset={offset}")
    soup = bs4.BeautifulSoup(resp.content, "html.parser")
    for a in soup.select('div.bottom a.tournament'):
        date, rounds, tname, time_control = [div.text.strip().split('\n')[0] for div in a.select('div.header')]
        id = a.attrs['href'].split('/')[-1]
        rounds_finished, rounds_total = map(int, rounds.split()[0].split('/')) # words[2] == 7/7 rund
        if rounds_finished < rounds_total:
            continue # avoid download when tournament is not completed yet
        tname = tname.split()[-1]
        tname = tname if '.' in tname else ('#1.' + tname[-1])
        t = Tournament(id, tname, date, time_control, rounds_total, None, None)
        tournaments.append(t)
    return tournaments

def load(filename: str) -> Data:
    with open(filename) as f:
        return from_dict(data_class=Data, data=json.load(f))

def save(filename: str, data: Data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, default=lambda o: o.__dict__))

def download(filename:str, url: str):
    data = load(filename) if os.path.isfile(filename) else Data([])
    tournaments = download_tournaments(url)
    for t in tournaments:
        if any(x.id==t.id for x in data.tournaments):
            continue
        print(t.name)
        url = f"https://www.chessmanager.com/en/tournaments/{t.id}"
        t.results = download_results(url)
        t.rounds = download_rounds(url, t.n_rounds)
        data.tournaments.append(t)
        data.tournaments.sort(key=lambda t: datetime.datetime.strptime(t.date, '%d.%m.%Y').date())
        save(filename, data)
    
if __name__ == "__main__":
    url = 'https://www.chessmanager.com/en/tournaments?name=Pomys%C5%82+GrandPrix'
    # url = 'https://www.chessmanager.com/en/tournaments?name=Pomys%C5%82+GrandPrix+%232'
    download('data.json', url)
