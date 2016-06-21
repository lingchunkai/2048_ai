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
    # Helper function that merges a single row or column in 2048
    # Move all non-zero values of list to the left
    # @return: (result after merging, increase in score)
    nonzeros_removed = []
    result = []
    merged = False
    for number in line:
        if number != 0:
            nonzeros_removed.append(number)

    while len(nonzeros_removed) != len(line):
        nonzeros_removed.append(0)
    
    score_inc = 0
    # Double sequental tiles if same value
    for number in range(0, len(nonzeros_removed) - 1):
        if nonzeros_removed[number] == nonzeros_removed[number + 1] and merged == False:
            result.append(nonzeros_removed[number] * 2)
            merged = True
            score_inc += nonzeros_removed[number] * 2
        elif nonzeros_removed[number] != nonzeros_removed[number + 1] and merged == False:
            result.append(nonzeros_removed[number])
        elif merged == True:
            merged = False
    
    if nonzeros_removed[-1] != 0 and merged == False:
        result.append(nonzeros_removed[-1])

    while len(result) != len(nonzeros_removed):
        result.append(0)

    return result, score_inc

class TwentyFortyEight:
    # Class to run the game logic.

    def __init__(self, grid_height, grid_width):
        # Initialize class
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.cells = []
        self.reset()

        # Compute inital row dictionary to make move code cleaner
        self.initial = {
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
    
    def get_alive(self):
        # Brute force method to check if any move is available
        nfilled = sum([sum([1 if x > 0 else 0 for x in y]) for y in self.cells])
        if nfiled < self.grid_width * self.grid_height: return True

        isDead = True
        for direction in [UP,DOWN,LEFT,RIGHT]:
            g = copy.deepcopy(self)
            
            if g.check_move(direction): 
                isDead = False
                continue

        return not isDead
            
    def check_move(self, direction):
        # Check if moving in that direction is a valid move. True if valid
        # return True if valid
        g = copy.deepcopy(self)

        if(direction == UP):
            return not g.next_pos(direction, self.get_grid_height()) == None
        elif(direction == DOWN):
            return not g.next_pos(direction, self.get_grid_height()) == None
        elif(direction == LEFT):
            return not g.next_pos(direction, self.get_grid_width()) == None
        elif(direction == RIGHT):
            return not g.next_pos(direction, self.get_grid_width()) == None
     
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
     
    def get_possible_moves(self):
        return [x for x in [UP, DOWN, LEFT, RIGHT] if self.check_move(x)]

    def move_helper(self, direction, row_or_column):
        # Make a move and add a piece 
        move_outcome = self.next_pos(direction, row_or_column)
        if not move_outcome == None: # Move is an actual, valid move
            self.new_tile()

        return move_outcome

    def next_pos(self, direction, row_or_column):
        # Find the next position after making a move. Move all columns and merge
        # Does not include adding a piece
        # @return - None if null move (nothing changed)
        # else, change in score 
        initial_list = self.initial[direction]
        temporary_list=[]
        
        before_move = str(self.cells)

        for element in initial_list:
            temporary_list.append(element)
            
            for index in range(1, row_or_column):
                temporary_list.append([x + y for x, y in zip(temporary_list[-1], OFFSETS[direction])])
            
            indices = []
            
            for index in temporary_list:
                indices.append(self.get_tile(index[0], index[1]))
            
            merged_list, score_inc = merge(indices)
            
            for index_x, index_y in zip(merged_list, temporary_list):
                self.set_tile(index_y[0], index_y[1], index_x)
        
            temporary_list = []
        
        after_move = str(self.cells)
        null_move = before_move == after_move
        
        if null_move == True: return None
        else: return score_inc

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
