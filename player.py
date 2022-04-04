"""
Player class
"""


class Player:
    """
    Player object that contains all the information about a player
    """

    def __init__(self, name, team, kills, deaths, assists):
        self.name = name
        self.team = team
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.alive = True

    def __eq__(self, other):
        return self.name == other.name and self.team == other.team

    def __str__(self):
        return f"{self.name} ({self.team}): {self.kills} kills, {self.deaths} deaths, {self.assists} assists"
