# Clone of 2048 game for Principles of Computing Coursera class
# @jbutewicz

import random
import poc_2048_gui
import copy

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    res = [0] * len(line)
    searching = True # searching for first pair
    prev = -1
    cnt = 0
    score_inc = 0
    for k in xrange(len(line)):
        if line[k] == 0: continue
        if searching == True:
            searching = False
            prev = line[k]
        else:
            if line[k] == prev:
                searching = True
                res[cnt] = prev * 2
                score_inc += prev * 2
                prev = -1
                cnt += 1
            else: # diff number
                res[cnt] = prev
                prev = line[k]
                cnt += 1
    
    if prev >= 0:
        res[cnt] = prev     
           
    return res, score_inc     

class TwentyFortyEight:
    # Class to run the game logic.

    initial=dict()

    def __init__(self, grid_height, grid_width, cells=[]):
        # Initialize class
        self.grid_height = grid_height
        self.grid_width = grid_width
        if len(cells) > 0:
            self.cells = list(map(list, cells))
        else:
            self.reset()
        self.next_pos_cached = dict()        

        # singleton
        if not (grid_height, grid_width) in TwentyFortyEight.initial:
            TwentyFortyEight.initial[(grid_height, grid_width)]= {
                UP : [[0,element] for element in range(self.get_grid_width())],
                DOWN : [[self.get_grid_height() - 1, element] for element in range(self.get_grid_width())],
                LEFT : [[element, 0] for element in range(self.get_grid_height())],
                RIGHT : [[element, self.get_grid_width() - 1] for element in range (self.get_grid_height())]
            }


    def reset(self):
        # Reset the game so the grid is empty.
        self.cells = [[0 for col in range(self.get_grid_height())] for row in range(self.get_grid_width())]
        self.new_tile() 

    def __str__(self):
        # Print a string representation of the grid for debugging.
        for number in range(0, self.get_grid_height()):
            print self.cells[number]
    
    def get_grid_height(self):
        # Get the height of the board.
        return self.grid_height    
    def get_grid_width(self):
        # Get the width of the board.
        return self.grid_width
    def check_move(self, direction):
        # Check if moving in that direction is a valid move. True if valid
        # return True if valid

        if(direction == UP):
            return not self.next_pos(direction, self.get_grid_height()) == None
        elif(direction == DOWN):
            return not self.next_pos(direction, self.get_grid_height()) == None
        elif(direction == LEFT):
            return not self.next_pos(direction, self.get_grid_width()) == None
        elif(direction == RIGHT):
            return not self.next_pos(direction, self.get_grid_width()) == None
     
    def move(self, direction):
        # Move all tiles in the given direction and add
        # a new tile if any tiles moved.
        # print direction
        # @return None if invalid move, otherwise score change
        if(direction == UP):
            return self.move_helper(direction, self.get_grid_height())
        elif(direction == DOWN):
            return self.move_helper(direction, self.get_grid_height())
        elif(direction == LEFT):
            return self.move_helper(direction, self.get_grid_width())
        elif(direction == RIGHT):
            return self.move_helper(direction, self.get_grid_width())
    
    def move_cpy(self, direction):
        if(direction == UP):
            return self.move_helper_cpy(direction, self.get_grid_height())
        elif(direction == DOWN):
            return self.move_helper_cpy(direction, self.get_grid_height())
        elif(direction == LEFT):
            return self.move_helper_cpy(direction, self.get_grid_width())
        elif(direction == RIGHT):
            return self.move_helper_cpy(direction, self.get_grid_width())
        
    def get_possible_moves(self):
        return [x for x in [UP, DOWN, LEFT, RIGHT] if self.check_move(x)]

    def move_helper(self, direction, row_or_column):
        # Make a move and add a piece 
        move_outcome = self.next_pos(direction, row_or_column)
        if not move_outcome == None: # Move is an actual, valid move
            self.cells = move_outcome[0]
            self.new_tile()
            self.next_pos_cached = dict()
            return move_outcome[1]
        else: return None

    def move_helper_cpy(self, direction, row_or_column):
        # Makes a new board and a move on it
        move_outcome = self.next_pos(direction, row_or_column)
        if not move_outcome == None: # Move is an actual, valid move
            ret = TwentyFortyEight(self.grid_height, self.grid_width, move_outcome[0])
            ret.new_tile()
        else: return None
        return ret, move_outcome[1]

    def next_pos(self, direction, row_or_column):
        # Find the next position after making a move. Move all columns and merge
        # Does not include adding a piece
        # @return next_cells, reward
        # None if invalid move

        if direction in self.next_pos_cached: return self.next_pos_cached[direction]
        
        score_inc = 0
        mod_cells = list(map(list, self.cells))        
        before_move = str(mod_cells)
        
        if direction == LEFT:
            for k in xrange(self.grid_height):
                mod_cells[k], rwd = merge(mod_cells[k])
                score_inc += rwd
        elif direction == RIGHT:
            for k in xrange(self.grid_height):
                merged, rwd = merge(mod_cells[k][::-1])
                mod_cells[k] = list(reversed(merged))
                score_inc += rwd
        elif direction == UP:
            for k in xrange(self.grid_width):
                merged, rwd = merge([mod_cells[x][k] for x in xrange(self.grid_height)])
                score_inc += rwd
                for g in xrange(self.grid_height): mod_cells[g][k] = merged[g]
        elif direction == DOWN:
            for k in xrange(self.grid_width):
                merged, rwd = merge([mod_cells[x][k] for x in reversed(range(self.grid_height))])
                merged = list(reversed(merged))
                score_inc += rwd
                for g in xrange(self.grid_height): mod_cells[g][k] = merged[g]                
                
        after_move = str(mod_cells)
        null_move = before_move == after_move
        
        if null_move == True: 
            self.next_pos_cached[direction] = None
        else: 
            self.next_pos_cached[direction] = (mod_cells, score_inc)
        return self.next_pos_cached[direction]

    def new_tile(self):
        # Create a new tile in a randomly selected empty 
        # square.  The tile should be 2 90% of the time and
        # 4 10% of the time.
        available_positions = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.cells[row][col] == 0:
                    available_positions.append([row, col])
 
        if not available_positions:
            print "There are no available positions."
        else:
            random_tile = random.choice(available_positions)
 
            weighted_choices = [(2, 9), (4, 1)]
            population = [val for val, cnt in weighted_choices for i in range(cnt)]
            tile = random.choice(population)

            self.set_tile(random_tile[0],random_tile[1], tile)
        
    def set_tile(self, row, col, value):
        # Set the tile at position row, col to have the given value.
        self.cells[row][col] = value
            
    def get_tile(self, row, col):
        # Return the value of the tile at position row, col.
        return self.cells[row][col]
 
if __name__ == '__main__':   
    poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
