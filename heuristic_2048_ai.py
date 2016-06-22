import base_2048_ai as base_ai
import TwentyFortyEight as TFE

class TwentyFortyEight_heuristic(base_ai.TwentyFortyEight_ai):
    """
    AI which alternates between left and down. moves one of the other 2 if left and down are not possible
    """
    def __init__(self):
        base_ai.TwentyFortyEight_ai.__init__(self)
        self.prev_move = TFE.DOWN

    def get_move(self, game):
        actions = game.get_possible_moves()
        if len(actions) == 0: 
            print 'No more moves left'
            return None
    
        if self.prev_move == TFE.DOWN:
            priority = [TFE.LEFT, TFE.DOWN, TFE.RIGHT, TFE.UP]
            self.prev_move = TFE.LEFT
        else:
            priority = [TFE.DOWN, TFE.LEFT, TFE.RIGHT, TFE.UP]
            self.prev_move = TFE.DOWN

        for action in priority:
            if action in actions: break 

        return action

if __name__ == '__main__':
    base_ai.Play(TwentyFortyEight_heuristic())
    base_ai.Evaluate(TwentyFortyEight_heuristic())
