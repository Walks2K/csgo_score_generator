"""
Downloads top teams from HLTV.org and saves them in a ready to use format.
"""


import requests
from bs4 import BeautifulSoup
from team import Team
from player import Player


URL = "https://www.hltv.org/ranking/teams/2022/march/28"


def download_teams(url=URL):
    """
    Downloads top teams from HLTV.org and saves them in a ready to use format.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    teams = []
    for team in soup.find_all(class_="ranked-team standard-box"):
        team_name = team.find(class_="name").text
        players = []
        for player in team.find_all(class_="rankingNicknames"):
            players.append(
                Player(
                    player.text,
                    team_name,
                    0,
                    0,
                    0,
                )
            )
        teams.append(Team(team_name, 0, players))

    # save to txt file
    with open("teams.txt", "w", encoding="utf-8") as file:
        for team in teams:
            file.write(str(team) + "\n")
    return teams


if __name__ == "__main__":
    download_teams()