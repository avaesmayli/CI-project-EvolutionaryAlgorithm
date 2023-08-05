import random
import game
import matplotlib.pyplot as plt
import os

class Game:
    def __init__(self, levels):
        # Get a list of strings as levels
        # Store level length to determine if a sequence of action passes all the steps

        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0

    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def get_score(self, actions, method):
    # Get an action sequence and determine the steps taken/score
    # Return a tuple, the first one indicates if these actions result in victory
    # and the second one shows the steps taken
        current_level = self.levels[self.current_level_index]

        def longest_route(level, actions):
            steps = 0
            longest_route_length = 0

            for i in range(len(actions)):
                if is_valid_action(level, actions, i):
                    steps += 1
                else:
                    longest_route_length = max(longest_route_length, steps)
                    steps = 1

            return max(longest_route_length, steps)

        def win(longest_route_score, level):
            if longest_route_score == len(level):
                if method == 1:
                    return 5
            return 0

        def score(level, actions):
            mashroom_score = 2
            score = 0
            for i in range(len(actions)):
                if i == 0 and level[0] == 'M':
                    score += mashroom_score
                elif level[i] == 'M' and actions[i - 1] != 1:
                    score += mashroom_score
            return score

        def springs(level, actions):
            spring_bonus = 0

            if actions[-1] == 1:
                spring_bonus += 1

            for i in range(len(actions)):
                if actions[i] == 1:
                    spring_bonus -= 0.5
                    if i < len(actions) - 2 and level[i + 2] == 'G':
                        spring_bonus += 2

            return spring_bonus

        total_score = longest_route(current_level, actions) + win(longest_route(current_level, actions), current_level) +\
             score(current_level, actions) + springs(current_level, actions)
        return total_score

    def is_solvable(self, level, actions):
        for i in range(len(actions)):
            if not is_valid_action(level, actions, i):
                return False
        return True

def is_valid_action(level, actions, position):
    if position > 0 and actions[position - 1] == 1 and (actions[position] == 1 or actions[position] == 2):
        return False
    if position > 0 and level[position] == 'G' and actions[position - 1] != 1 and (position < 2 or actions[position - 2] != 1):
        return False
    if position > 0 and level[position] == 'L' and actions[position - 1] != 2:
        return False
    return True
