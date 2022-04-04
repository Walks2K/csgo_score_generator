"""
Team class
"""


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
