"""
Game class
"""


import random


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
