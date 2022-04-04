"""
Python & OOP version of https://github.com/Walks2K/CSGO-Score-Generator

CSGO Score Generator - simulate CS:GO matches

CS matches are won either by first to 16 rounds (unless 15-15, in which case the first team to get 4 ahead wins)
"""


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
        self.alive = True

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

    def alive_players(self):
        """
        Returns a list of alive players
        """
        return [player for player in self.players if player.alive]

    def alive_players_count(self):
        """
        Returns the number of alive players
        """
        return len(self.alive_players())

    def reset_round(self):
        """
        Resets team after a round has ended
        """
        for player in self.players:
            player.alive = True

    def print_team(self, sort=None):
        """
        Prints the team in a nice format
        """
        if sort == "kills":
            self.players.sort(key=lambda player: player.kills, reverse=True)
        elif sort == "deaths":
            self.players.sort(key=lambda player: player.deaths, reverse=True)
        elif sort == "assists":
            self.players.sort(key=lambda player: player.assists, reverse=True)
        elif sort == "alive":
            self.players.sort(key=lambda player: player.alive, reverse=True)
        else:
            self.players.sort(key=lambda player: player.name)

        print(f"{self.name} ({self.rounds_won}):")
        for player in self.players:
            print(f"\t{player}")


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
        winner.print_team("kills")
        loser.print_team("kills")

    def simulate_round(self):
        """
        Simulates a single round of CS:GO
        """
        while (self.teams[0].alive_players_count() > 0) and (self.teams[1].alive_players_count() > 0):
            # Pick a random player from each team
            team1_player = random.choice(self.teams[0].alive_players())
            team2_player = random.choice(self.teams[1].alive_players())

            # Roll a random chance for who will kill who
            if random.randint(0, 1) == 0:
                self.event_kill(team1_player, team2_player, None)
            else:
                self.event_kill(team2_player, team1_player, None)

        # End the round
        self.round_end()

    def event_kill(self, killer, victim, assist):
        """
        Handles a kill event

        Args:
            killer (Player): The player who killed
            victim (Player): The player who was killed
            assist (Player): The player who assisted in killing
        """
        killer.kills += 1
        victim.deaths += 1

        # Set victim as dead
        victim.alive = False

        # Roll a random chance for assist to count
        if random.randint(0, 1) == 0 and assist is not None:
            assist.assists += 1

    def round_end(self):
        """
        Resets the game after a round has ended and finds the winner
        """
        # Find team with more alive players
        if self.teams[0].alive_players_count() > self.teams[1].alive_players_count():
            winner = self.teams[0]
            loser = self.teams[1]
        else:
            winner = self.teams[1]
            loser = self.teams[0]

        # Add a round to the winner
        winner.rounds_won += 1

        # Reset the game
        for team in self.teams:
            team.reset_round()

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
        "https://www.hltv.org/matches/2354979/fnatic-vs-ence-esl-pro-league-season-15"
    )

    game.simulate()


if __name__ == "__main__":
    main()
