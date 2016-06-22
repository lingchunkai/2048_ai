import base_2048_ai as base_ai
import TwentyFortyEight as TFE
import copy

class TwentyFortyEight_greedy(base_ai.TwentyFortyEight_ai):
    """
    Picks the move which gives the most instantaneous reward
    """
    def __init__(self):
        base_ai.TwentyFortyEight_ai.__init__(self)

    def get_move(self, game):
        actions = game.get_possible_moves()
        if len(actions) == 0: 
            print 'No more moves left'
            return None
 
        best_change = 0
        for action in actions:   
            new_game = copy.deepcopy(game)
            score_change = new_game.move(action)
            if score_change >= best_change:
                best_change = score_change
                best_action = action
            
        return action

if __name__ == '__main__':
    base_ai.Play(TwentyFortyEight_greedy())
    base_ai.Evaluate(TwentyFortyEight_greedy())
