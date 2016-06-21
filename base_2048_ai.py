import TwentyFortyEight as TFE
import copy
import random

class TwentyFortyEight_ai:
    def __init__(self):
        self.all_actions = [TFE.UP,TFE.DOWN,TFE.LEFT,TFE.RIGHT]

    def get_move(self, game):
        actions = game.get_possible_moves()
        if len(actions) == 0: 
            print 'No more moves left'
            return None

        return random.choice(actions)
   
def Play(ai):
    game = TFE.TwentyFortyEight(4,4)
    total_score = 0
    while True:
        possible_moves = game.get_possible_moves()
        if len(possible_moves) == 0: break
        move = ai.get_move(game)
        assert move in possible_moves, 'invalid move'
        total_score += game.move(move)
        print move, total_score
    print 'Game over. Total score: ', total_score
    return total_score


if __name__ == '__main__':
    Play(TwentyFortyEight_ai())
