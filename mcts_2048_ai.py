import base_2048_ai as base_ai
import TwentyFortyEight as TFE
import copy
import random
import math
import time

class TwentyFortyEight_mcts(base_ai.TwentyFortyEight_ai):
    def __init__(self, Cp = 0.707):
        base_ai.TwentyFortyEight_ai.__init__(self)
        self.tree_root_state = None   
        self.Cp = Cp     

    def get_move(self, game, max_traj=100000, max_time=1, min_traj = 5):
        actions = game.get_possible_moves()
        if len(actions) == 0: 
            print 'No more moves left'
            return None

        return self.mcts(game, max_traj, max_time, min_traj)    
        

    def mcts(self, game, max_traj, max_time, min_traj):
        end_time = time.time() + max_time
        root_state = self.get_root(game)        
        # print root_state.cnt
        
        for rollout_num in xrange(max_traj):
            if time.time() > end_time and rollout_num > min_traj: 
                break
            # print "Rollout: " , rollout_num
            selected_state, reward_collected1 = self.tree_policy(root_state)

            # print "Default..."
            final_state, reward_collected2 = self.default_policy(selected_state)
            # print final_state.game.cells
            
            #print selected_state
            # print final_state
            self.backup(final_state, reward_collected1+reward_collected2)
            # raw_input()

        return self.best_child(root_state, 0)

    def get_root(self, game):
        """
        Find partially constructed tree if there already is, using brute force
        """

        if self.tree_root_state == None:
            self.tree_root_state = StateNode(copy.deepcopy(game), None)
            return self.tree_root_state
        else:
            hashkey_needle = tuple([tuple(x) for x in game.cells])
            # Search for next state
            for action, action_node in self.tree_root_state.children.iteritems():
                for hashkey in action_node.children:
                    if hashkey == hashkey_needle:
                        self.tree_root_state = action_node.children[hashkey]
                        self.tree_root_state.parent = None
                        return self.tree_root_state
                        
        self.tree_root_state = StateNode(copy.deepcopy(game), None)
        return self.tree_root_state

    def tree_policy(self, init_state):
        reward_collected = 0
        cur_state = init_state
        while len(cur_state.possible_moves) > 0:
            if len(cur_state.children) < len(cur_state.possible_moves): # not all actions have been tried
                for action_expanded in cur_state.possible_moves: # find action which has not been taken before
                    if not action_expanded in cur_state.children: break
                cur_state.children[action_expanded] = ActionNode(action_expanded, cur_state.game, cur_state)
                next_state = cur_state.children[action_expanded].sample_state()
                return next_state, reward_collected + next_state.rwd
            else: # all actions have been tried, continue jacking down
                # action selection based on UCT
                action_selected = self.best_child(cur_state, self.Cp)                
                action_node_selected = cur_state.children[action_selected]
                cur_state = action_node_selected.sample_state()
                reward_collected += cur_state.rwd
        
        # Only reach here when tree policy gets stuck (no move to make)
        return cur_state, reward_collected       

    def default_policy(self, state):
        reward_collected = 0
        while True:
            actions = state.possible_moves
            if len(actions) == 0: break
            
            action_taken = random.choice(actions)
            state.children[action_taken] = ActionNode(action_taken, state.game, state)
            next_state = state.children[action_taken].sample_state()
            state = next_state
            reward_collected += state.rwd

        return state, reward_collected

    def backup(self, node, run_rwd):
        while not node == None:
            node.cnt += 1
            node.val += run_rwd
            node = node.parent

    def best_child(self, state, expl_factor):
        best_score = -float('inf')
        for action in state.possible_moves:
            score = float(state.children[action].val)/float(state.children[action].cnt) + expl_factor * math.sqrt((2.0 * math.log(state.cnt))/state.children[action].cnt)
            # print state.game.cells, score
            if score > best_score: 
                best_action = action
                best_score = score

        return best_action


    def eval(self, state):
        return 0

class StateNode:
    def __init__(self, game, parent, rwd = 0):
        self.game = game
        self.children = dict()
        self.possible_moves = self.game.get_possible_moves()
        self.parent = parent
        self.cnt = 0 # count from MCTS
        self.val = 0 # value form MCTS
        self.rwd = rwd # incremental reward at this node
        
class ActionNode:
    def __init__(self, action, game, parent):
        self.game = game
        self.action = action
        self.children = dict()
        self.parent = parent
        self.cnt = 0
        self.val = 0

    def sample_state(self):
        #newgame = copy.deepcopy(self.game)
        #rwd = newgame.move(self.action) 
        newgame, rwd = self.game.move_cpy(self.action)
        rwd = float(rwd)/2048.0
        # print newgame.cells
        
        hashkey = tuple([tuple(x) for x in newgame.cells])
        if hashkey in self.children: return self.children[hashkey]
        self.children[hashkey] = StateNode(newgame, self, rwd)

        return self.children[hashkey]
   
if __name__ == '__main__':
    base_ai.Play(TwentyFortyEight_mcts())
    base_ai.Evaluate(TwentyFortyEight_mcts(),5)
