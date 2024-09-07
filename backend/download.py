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
        try:
            place, _, _, title, player, _, _, _, pts, bch1, bch, _, _, _, _, _ = row
        except:
            place, _, _, title, player, _, _, _, pts, _, _, _, _ = row
            bch1 = bch = 0
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
    for a in soup.select('a.red.card'):
        text = a.text
        id = a.attrs['href'].split('/')[-1]
        tname = re.findall(r'Pomysł GrandPrix \S+', text)[0]
        date = re.findall(r'\d\d.\d\d.\d\d\d\d', text)[0]
        # players = int(re.findall(r'\d+\s+players', text)[0].split()[0])
        rounds_str = re.findall(r'\d+/\d+\s+rounds', text)[0]
        rounds_total = int(rounds_str.split()[0].split('/')[1])
        time_control = re.findall(r'players\s+\S+', text)[0].split()[1]
        t = Tournament(id, tname, date, time_control, rounds_total, None, None, None)
        tournaments.append(t)
    return tournaments

def load(directory: str) -> Data:
    os.makedirs(directory, exist_ok=True)
    data = Data([])
    for filename in os.listdir(directory):
        with open(f"{directory}/{filename}") as f:
            tournament = from_dict(data_class=Tournament, data=json.load(f))
            data.tournaments.append(tournament)
    return data

def save(directory: str, data: Data):
    os.makedirs(directory, exist_ok=True)
    for tournament in data.tournaments:
        filename = f"{directory}/{tournament.name}.json"
        with open(filename, 'w') as f:
            f.write(json.dumps(tournament, default=lambda o: o.__dict__))

def download(directory:str, url: str):
    data = load(directory)
    tournaments = download_tournaments(url)
    for t in tournaments:
        if any(x.id==t.id for x in data.tournaments):
            continue
        print(t.name)
        url = f"https://www.chessmanager.com/en/tournaments/{t.id}"
        t.results = download_results(url)
        t.rounds = download_rounds(url, t.n_rounds)
        t.players = download_players(url)
        data.tournaments.append(t)
        data.tournaments.sort(key=lambda t: datetime.datetime.strptime(t.date, '%d.%m.%Y').date())
        save(directory, data)
    
if __name__ == "__main__":
    url = 'https://www.chessmanager.com/en/tournaments?name=Pomys%C5%82+GrandPrix'
    # url = 'https://www.chessmanager.com/en/tournaments?name=Pomys%C5%82+GrandPrix+%232'
    download('data/pomysl-grand-prix/tournaments', url)
