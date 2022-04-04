"""
Python & OOP version of https://github.com/Walks2K/CSGO-Score-Generator

CSGO Score Generator - simulate CS:GO matches
"""


import requests
from bs4 import BeautifulSoup

from game import Game
from player import Player
from team import Team


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
        "https://www.hltv.org/matches/2354979/fnatic-vs-ence-esl-pro-league-season-15"
    )

    game.simulate()


if __name__ == "__main__":
    main()
