"""
Python & OOP version of https://github.com/Walks2K/CSGO-Score-Generator

CSGO Score Generator - simulate CS:GO matches and generates a score

Classes:
    Player:
        Player object that contains all the information about a player (name, team, kills, deaths, etc.)
    Team:
        Team object that contains all the information about a team (name, score, etc)
    Game:
        Game object that contains all the information about a game (teams, score, etc)

    Functions:
        parse_team_page:
            Parse a team page from HLTV.org and return a Team object
        parse_match_page:
            Parse a match page from HLTV.org and return a Game object
"""


import requests
from bs4 import BeautifulSoup


class Player:
    """
    Player object that contains all the information about a player (name, team, kills, deaths, etc.)
    """

    def __init__(self, name, team, kills, deaths, assists):
        self.name = name
        self.team = team
        self.kills = kills
        self.deaths = deaths
        self.assists = assists

    def __str__(self):
        return f"{self.name} ({self.team}): {self.kills} kills, {self.deaths} deaths, {self.assists} assists"


class Team:
    """
    Team object that contains all the information about a team (name, score, etc)
    """

    def __init__(self, name, score, players):
        self.name = name
        self.score = score
        self.players = players

    def __str__(self):
        return f"{self.name}: {self.score}, {[player.name for player in self.players]}"


class Game:
    """
    Game object that contains all the information about a game (teams, score, etc)
    """

    def __init__(self, teams):
        self.teams = teams

    def __str__(self):
        return f"Team 1: {self.teams[0]}, Team 2: {self.teams[1]}"


def parse_team_page(url):
    """
    Parse a team page from HLTV.org and return a Team object
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    team_name = soup.find(class_="profile-team-name text-ellipsis").text
    players = []
    team_grid = soup.find(class_="bodyshot-team g-grid")
    for player in team_grid.find_all(class_="col-custom"):
        players.append(Player(player.get("title"), team_name, 0, 0, 0))

    return Team(team_name, 0, players)


def parse_match_page(url):
    """
    Parse a match page from HLTV.org and return a Game object

    Create Team objects from div class="lineup standard-box", players are in class="player"
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    teams = []
    lineups = soup.find(class_="lineups")
    for team in lineups.find_all(class_="lineup standard-box"):
        team_name = team.find(class_="logo").get("title")
        players = []
        for player in team.find_all(class_="player"):
            if player.find(class_="text-ellipsis"):
                players.append(
                    Player(player.find(class_="text-ellipsis").text, team_name, 0, 0, 0)
                )
        teams.append(Team(team_name, 0, players))

    return Game(teams)


def main():
    """
    Main function
    """
    game = parse_match_page(
        "https://www.hltv.org/matches/2354538/g2-vs-nip-esl-pro-league-season-15"
    )

    print(game)


if __name__ == "__main__":
    main()
