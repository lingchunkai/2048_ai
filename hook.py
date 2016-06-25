import threading
import poc_2048_gui
import base_2048_ai
import mcts_2048_ai
import TwentyFortyEight
import time
class GUI_AI(poc_2048_gui.GUI):
    def __init__(self, game):
        poc_2048_gui.GUI.__init__(self,game)
    
class AI_wrapper(threading.Thread):
    def __init__(self, game, ai):
        self.game = game
        self.AI = ai
        threading.Thread.__init__(self)

    def run(self):
        print 'START'
        total_score = 0
        while True:
            possible_moves = self.game.get_possible_moves()
            if len(possible_moves) == 0: break
            move = self.AI.get_move(self.game)
            assert move in possible_moves, 'invalid move'
            total_score += self.game.move(move)
            print move, total_score
        print 'Game over. Total score: ', total_score
        return total_score

if __name__ == '__main__':
    game = TwentyFortyEight.TwentyFortyEight(4,4)
    ai = mcts_2048_ai.TwentyFortyEight_mcts()
    Aix = AI_wrapper(game, ai)
    Aix.daemon = True
    Aix.start()
    gui = GUI_AI(game) # TODO: unprotected memory here, but only causes small problems with drawing occasionally
    
