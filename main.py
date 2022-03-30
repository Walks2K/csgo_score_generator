"""
Python & OOP version of https://github.com/Walks2K/CSGO-Score-Generator

CSGO Score Generator - simulate CS:GO matches

CS matches are won either by first to 16 rounds (unless 15-15, in which case the first team to get 4 ahead wins)
"""


import copy
import random
import requests
from bs4 import BeautifulSoup


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

    def __str__(self):
        return f"{self.name} ({self.team}): {self.kills} kills, {self.deaths} deaths, {self.assists} assists"


class Team:
    """
    Team object that contains all the information about a team
    """

    def __init__(self, name, rounds_won, players):
        self.name = name
        self.rounds_won = rounds_won
        self.players = players

    def __str__(self):
        return f"{self.name}: {self.rounds_won}, {[player.name for player in self.players]}"


class Game:
    """
    Game object that contains all the information and logic
    """

    def __init__(self, teams):
        self.teams = teams

    def simulate(self):
        """
        Simulates a CS:GO match
        """
        # Initialize the game
        self.teams[0].rounds_won = 0
        self.teams[1].rounds_won = 0
        self.teams[0].players[0].kills = 0
        self.teams[0].players[0].deaths = 0
        self.teams[0].players[0].assists = 0
        self.teams[1].players[0].kills = 0
        self.teams[1].players[0].deaths = 0
        self.teams[1].players[0].assists = 0
        # Simulate the game
        while self.teams[0].rounds_won < 16 and self.teams[1].rounds_won < 16:
            self.simulate_round()
        # Determine the winner
        if self.teams[0].rounds_won > self.teams[1].rounds_won:
            winner = self.teams[0]
            loser = self.teams[1]
        else:
            winner = self.teams[1]
            loser = self.teams[0]
        # Print the results
        print(f"{winner.name} won the game!")
        print(
            f"{winner.name} won {winner.rounds_won} rounds, {loser.name} won {loser.rounds_won} rounds"
        )
        print(f"{winner.name}'s team: {[player.name for player in winner.players]}")
        print(f"{loser.name}'s team: {[player.name for player in loser.players]}")

    def simulate_round(self):
        """
        Simulates a single round of CS:GO
        """
        team1 = copy.deepcopy(self.teams[0])
        team2 = copy.deepcopy(self.teams[1])

        while len(team1.players) > 1 and len(team2.players) > 1:
            team1_player = random.choice(team1.players)
            team2_player = random.choice(team2.players)

            if random.random() < 0.5:  # team1 kills team2 player
                team1_player.kills += 1
                team2_player.deaths += 1
                team2.players.remove(team2_player)
            else:  # team2 kills team1 player
                team2_player.kills += 1
                team1_player.deaths += 1
                team1.players.remove(team1_player)

        if len(team1.players) > len(team2.players):
            self.teams[0].rounds_won += 1
        elif len(team2.players) > len(team1.players):
            self.teams[1].rounds_won += 1

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

    game.simulate()


if __name__ == "__main__":
    main()
