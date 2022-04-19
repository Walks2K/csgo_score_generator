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
        self.winner = None
        self.loser = None

    def simulate(self):
        """
        Simulates a CS:GO match
        """
        # Simulate the game
        while self.winner is None:
            self.simulate_round()
            self.check_winner()

        # Print the result
        self.print_result()

    def check_winner(self):
        """
        Checks if there is a winner
        """
        # Check for winner in regular rounds
        if self.teams[0].rounds_won == 16 and self.teams[1].rounds_won < 15:
            self.winner = self.teams[0]
            self.loser = self.teams[1]
        elif self.teams[1].rounds_won == 16 and self.teams[0].rounds_won < 15:
            self.winner = self.teams[1]
            self.loser = self.teams[0]
        # Check for winner in overtime
        elif self.teams[0].rounds_won >= 15 and self.teams[1].rounds_won >= 15:
            if (
                self.teams[0].rounds_won % 3 == 1
                and self.teams[0].rounds_won > self.teams[1].rounds_won + 1
            ):
                self.winner = self.teams[0]
                self.loser = self.teams[1]
            elif (
                self.teams[1].rounds_won % 3 == 1
                and self.teams[1].rounds_won > self.teams[0].rounds_won + 1
            ):
                self.winner = self.teams[1]
                self.loser = self.teams[0]

    def print_result(self):
        """
        Prints the result of the game
        """
        print(f"{self.winner.name} won the game!")
        print(
            f"{self.winner.name} won {self.winner.rounds_won} rounds, {self.loser.name} won {self.loser.rounds_won} rounds"
        )
        self.winner.print_team("kills")
        self.loser.print_team("kills")

    def simulate_round(self):
        """
        Simulates a single round of CS:GO
        """
        while (self.teams[0].alive_players_count() > 0) and (
            self.teams[1].alive_players_count() > 0
        ):
            # If a team has 2+ player advantage, roll chance for round to end in their favour
            if (
                self.teams[0].alive_players_count() - 2
                >= self.teams[1].alive_players_count()
                and random.randint(0, 1) == 1
            ):
                self.round_end()
                return
            elif (
                self.teams[1].alive_players_count() - 2
                >= self.teams[0].alive_players_count()
                and random.randint(0, 1) == 1
            ):
                self.round_end()
                return

            # Pick a random player from each team
            team1_player = random.choice(self.teams[0].alive_players())
            team2_player = random.choice(self.teams[1].alive_players())
            assist = None

            # Roll a random chance for who will kill who
            if random.randint(0, 1) == 0:
                # choose a unique random player from team1 to assist
                while (assist is team1_player or assist is None) and len(
                    self.teams[0].alive_players()
                ) > 1:
                    assist = random.choice(self.teams[0].alive_players())
                self.event_kill(team1_player, team2_player, assist)
            else:
                # choose a unique random player from team2 to assist
                while (assist is team2_player or assist is None) and len(
                    self.teams[1].alive_players()
                ) > 1:
                    assist = random.choice(self.teams[1].alive_players())
                self.event_kill(team2_player, team1_player, assist)

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
