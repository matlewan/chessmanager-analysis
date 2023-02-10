from dataclasses import dataclass
from typing import Optional

@dataclass
class Match:
    tournament : str
    round : int
    white : str
    black : str
    result : float

@dataclass
class Result:
    tournament : str
    player : str
    place : int
    points : float
    bch1 : float
    bch : float

@dataclass
class Player:
    name : str
    title : str
    club : str
    birthdate : int
    rating : float
    id : int = 0
    pomysl_rating : float = 0.0  # Rating calculated based on result in Pomysł GrandPrix
    score : float = 0.0
    M: int = 0
    W: int = 0
    D: int = 0
    L: int = 0

@dataclass
class Tournament:
    id : str
    name : str
    date : str
    players : int
    rounds : int

@dataclass
class Duel:
    player : str
    opponent : str
    W : int
    D : int
    L : int

@dataclass
class Data:
    tournaments : list[Tournament]
    matches : list[Match]
    results : list[Result]
    players : list[Player]
    duels : Optional[list[Duel]]
