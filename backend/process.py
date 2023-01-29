import json
from data import *
from dacite import from_dict
from glicko2 import Glicko2

def process(in_file, out_file):

    with open(in_file) as f:
        data : Data = from_dict(data_class=Data, data=json.load(f))
        
    tournaments = {t.name:t for t in data.tournaments}
    players = {p.name:p for p in data.players}
    matches = data.matches
    results = {}
    for r in data.results:
        results[r.tournament] = results.get(r.tournament, [])
        results[r.tournament].append(r)

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
    for p in players.values():
        p.score = round((p.W + p.D/2) * 7 / p.M, 2)
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
        duels[key] = duel = duels.get(key, Duel(m.white, m.black, 0.0, 0.0))
        duel.W += m.result
        duel.L += 1.0-m.result

        key = (m.black, m.white)
        duels[key] = duel = duels.get(key, Duel(m.black, m.white, 0.0, 0.0))
        duel.W += 1.0-m.result
        duel.L += m.result

    data.players = players
    data.matches = matches
    data.duels = list(duels.values())
    data.tournaments = tournaments
    data.results = results
    with open(out_file, 'w') as f:
        f.write(json.dumps(data, default=lambda o: o.__dict__))

if __name__ == "__main__":
    process('backend/data.json', 'frontend/pomysl-grandprix/public/out.json')
