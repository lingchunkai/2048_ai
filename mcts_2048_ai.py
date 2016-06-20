import base_2048_ai as base_ai
import TwentyFortyEight as TFE
import copy
import random

class TwentyFortyEight_mcts(base_ai.TwentyFortyEight_ai):
    def __init__(self):
        base_ai.TwentyFortyEight_ai.__init__(self)

    def get_move(self, game):
        actions = game.get_possible_moves()
        if len(actions) == 0: 
            print 'No more moves left'
            return None

        return random.choice(actions)
   
if __name__ == '__main__':
    base_ai.Play(TwentyFortyEight_mcts())
