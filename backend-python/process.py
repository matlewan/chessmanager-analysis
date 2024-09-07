import json
import os
from data import *
from dacite import from_dict
from glicko2 import Glicko2
from datetime import datetime

def process(in_file, out_file):
    data = load(in_file)
    
    # Fix (normalize) tournament name for 1st edition of tournaments
    for t in data.tournaments:
        t.name = t.name.replace('Pomysł GrandPrix ', '')
        if t.name in ["#1", "#2", "#3", "#4", "#5"]:
            t.name = '#1.' + t.name[-1]

    # Fix (merge) player names where 'ł' was typed as 'l'
    all_names = [p.name for t in data.tournaments for p in t.players]
    names = {}
    for name in all_names:
        norm = normalize(name)
        if norm not in names or normalize_score(names[norm]) > normalize_score(name):
            names[norm] = name
    for t in data.tournaments:
        for p in t.players:
            p.name = names.get(normalize(p.name), p.name)
        for r in t.results:
            r.player = names.get(normalize(r.player), r.player)
        for r in t.rounds:
            for m in r.matches:
                m.white = names.get(normalize(m.white), m.white)
                m.black = names.get(normalize(m.black), m.black)
    
    # Initialize data
    tournaments = {t.name:t for t in data.tournaments}
    players = {p.name:p for t in data.tournaments for p in t.players}
    matches = [m for t in data.tournaments for r in t.rounds for m in r.matches]

    NO_OPPONENT = 'No Opponent'

    # Calculate M,W,D,L
    for m in matches:
        if m.black == NO_OPPONENT:
            continue
        w,b = players[m.white], players[m.black]
        w.M += 1
        b.M += 1
        if m.result == 1.0:
            w.W += 1
            b.L += 1
        if m.result == 0.5:
            w.D += 1
            b.D += 1
        if m.result == 0.0:
            w.L += 1
            b.W += 1
        
    # Calculate score and "Pomysł GrandPrix" rating
    glicko = Glicko2(tau=0.5)
    players = {k:v for k,v in players.items() if v.M > 0}
    for p in players.values():
        p.score = round((p.W + p.D/2) * 100 / p.M, 2)
        rd = 500 if p.rating in [1000,1200,1400,1600,1800] else 50
        p.pomysl_rating = glicko.create_rating(p.rating, rd)

    for m in matches:
        if m.black == NO_OPPONENT:
            continue
        w,b = players[m.white], players[m.black]
        if m.result == 1.0:
            w.pomysl_rating, b.pomysl_rating = glicko.rate_1vs1(w.pomysl_rating, b.pomysl_rating, drawn=False)
        if m.result == 0.5:
            w.pomysl_rating, b.pomysl_rating = glicko.rate_1vs1(w.pomysl_rating, b.pomysl_rating, drawn=True)
        if m.result == 0.0:
            b.pomysl_rating, w.pomysl_rating = glicko.rate_1vs1(b.pomysl_rating, w.pomysl_rating, drawn=False)

    for p in players.values():
        p.pomysl_rating = p.pomysl_rating.mu

    # Calculate duels
    duels = {}
    for m in matches:
        key = (m.white, m.black)
        duels[key] = duel = duels.get(key, Duel(m.white, m.black, 0,0,0))
        if m.result == 1.0: duel.W += 1
        if m.result == 0.5: duel.D += 1
        if m.result == 0.0: duel.L += 1        

        key = (m.black, m.white)
        duels[key] = duel = duels.get(key, Duel(m.black, m.white, 0,0,0))
        if m.result == 0.0: duel.W += 1
        if m.result == 0.5: duel.D += 1
        if m.result == 1.0: duel.L += 1        

    data.players = players
    data.duels = list(duels.values())
    data.tournaments = tournaments
    save(out_file, data)

def load(directory: str) -> Data:
    os.makedirs(directory, exist_ok=True)
    data = Data([])
    for filename in os.listdir(directory):
        with open(f"{directory}/{filename}") as f:
            tournament = from_dict(data_class=Tournament, data=json.load(f))
            data.tournaments.append(tournament)
    data.tournaments = sorted(data.tournaments, key=lambda t: datetime.strptime(t.date, '%d.%m.%Y'))[::-1]
    return data
    
def save(filename: str, data: Data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, default=lambda o: o.__dict__))

def normalize(word):
    d = str.maketrans('żółćęśąźń','zolcesazn')
    return word.lower().translate(d)

def normalize_score(word):
    return len([c for c in word if c in 'abcdefghijklmnopqrstuvwxyz' and c.islower()])

if __name__ == "__main__":
    process('data/pomysl-grand-prix/tournaments', '../frontend/public/out.json')
