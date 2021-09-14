# imports
import sys
import copy

################ global variables ################
end_pos = (10, 0)
visited_pos = []
moves = []

################ node class ################
class Node:
    def __init__(self, board, parent, operator, steps):
        self.board = board
        self.parent = parent
        self.operator = operator
        self.steps = steps

def create_node(board, parent, operator, steps):
    return Node(board, parent, operator, steps)

################ utility functions ################
def printBoard(board, board_size) :
    for i in range(board_size) :
        for j in range(board_size) :
            print (board[i][j], end = ' ')
        print()

def getAgentPosition(board) :
    for r_index, row in enumerate(board) :
        for c_index, col in enumerate(row) :
            if 'A' in col :
                return r_index, c_index

################ expansion ################
def expand_node(node, board_size):
    expanded_nodes = []

    up_board = move_up(node.board, board_size)
    left_board = move_left(node.board, board_size)
    right_board = move_right(node.board, board_size)
    down_board = move_down(node.board, board_size)

    if (up_board is not None) :
        up_node = create_node(up_board, node, "up", node.steps + 1)
        expanded_nodes.append(up_node)

    if (left_board is not None) :
        left_node = create_node(left_board, node, "left", node.steps + 1)
        expanded_nodes.append(left_node)

    if (right_board is not None) :
        right_node = create_node(right_board, node, "right", node.steps + 1)
        expanded_nodes.append(right_node)

    if (down_board is not None) :
        down_node = create_node(down_board, node, "down", node.steps + 1)
        expanded_nodes.append(down_node)    

    return expanded_nodes

################ movement functions ################
def move_left(board, board_size):
    move_board = copy.deepcopy(board)
    x, y = getAgentPosition(board)

    if (y > 0 and board[x][y - 1] == '1') :
        move_board[x][y], move_board[x][y - 1] = move_board[x][y - 1], move_board[x][y]
        return move_board
    
    return None

def move_right(board, board_size):
    move_board = copy.deepcopy(board)
    x, y = getAgentPosition(board)

    if (y < board_size-1 and board[x][y + 1] == '1') :
        move_board[x][y], move_board[x][y + 1] = move_board[x][y + 1], move_board[x][y]
        return move_board
    
    return None


def move_up(board, board_size):
    move_board = copy.deepcopy(board)
    x, y = getAgentPosition(board)

    if (x > 0 and board[x - 1][y] == '1') :
        move_board[x][y], move_board[x - 1][y] = move_board[x - 1][y], move_board[x][y]
        return move_board
    
    return None


def move_down(board, board_size):
    move_board = copy.deepcopy(board)
    x, y = getAgentPosition(board)

    if (x < board_size-1 and board[x + 1][y] == '1') :
        move_board[x][y], move_board[x + 1][y] = move_board[x + 1][y], move_board[x][y]
        return move_board
    
    return None

################ bfs code ################
def bfs(start, board_size):

    # get agent index
    agent_pos = getAgentPosition(start)

    if (agent_pos == end_pos):
        return [None]
        
    else:
        # count number of iterations
        iter = 0

        start_node = create_node(start, None, None, 0)

        # queue for nodes
        for_expansion = []
        for_expansion.append(start_node)
    
        while (True):
            temp_nodes = []

            size = len(for_expansion)

            for i in range(size) :

                agent_pos = getAgentPosition(for_expansion[i].board)

                # visited nodes not expanded
                if (agent_pos in visited_pos) : 
                    continue;

                expanded_nodes = expand_node(for_expansion[i], board_size)
                number_of_nodes = len(expanded_nodes)
                
                # examining all expanded nodes
                for j in range(number_of_nodes):
                    iter += 1

                    pos = getAgentPosition(expanded_nodes[j].board)

                    #print("\tAgent position at current node: ", pos)

                    if (pos == end_pos):
                        moves.append(iter)
                        return expanded_nodes[j]

                    # mark for further expansion   
                    else :
                        temp_nodes.append(expanded_nodes[j]) 
                        visited_pos.append(agent_pos)

            # remove expanded nodes and copy over the new nodes
            for_expansion.clear()  
            for_expansion = temp_nodes.copy()  
            temp_nodes.clear()
    
    return None

################ dfs code ################
def dfs(start, board_size):

    # get agent index
    agent_pos = getAgentPosition(start)

    if (agent_pos == end_pos):
        return [None]
        
    else:
        # count number of iterations
        iter = 0

        start_node = create_node(start, None, None, 0)

        # stack for nodes
        node_stack = []
        node_stack.append(start_node)
    
        while (True):
            iter += 1

            # getting the last node in the stack
            top_node = node_stack.pop()

            agent_pos = getAgentPosition(top_node.board)
            #print("\tAgent position at current node: ", agent_pos)

            if (agent_pos == end_pos) :
                moves.append(iter)
                return top_node

            else :
                # recording all previous states
                visited_pos.append(agent_pos)

                # children will be added to stack
                expanded_nodes = expand_node(top_node, board_size)

                for node in expanded_nodes :
                    pos = getAgentPosition(node.board)

                    # make sure previous states are not being visited again
                    if (pos not in visited_pos) :
                        node_stack.append(node)
    
    return None

################ driver code ################
def main():    

    board_size = 12
    
    if (len(sys.argv) > 0) :
        board_size = int(sys.argv[1])
    
    print("\nBoard size: ", board_size)

    board = [
        ['0','0','0','0','0','0','0','0','0','0','0','0'],  # 0
        ['0','1','1','1','0','1','1','1','1','1','1','0'],  # 1
        ['0','1','0','1','0','1','0','0','0','0','1','0'],  # 2
        ['0','0','0','1','0','1','1','1','1','0','1','0'],  # 3
        ['0','1','1','1','1','0','0','0','1','0','1','A'],  # 4
        ['0','0','0','0','1','0','1','0','1','0','1','0'],  # 5
        ['0','1','1','0','1','0','1','0','1','0','1','0'],  # 6
        ['0','0','1','0','1','0','1','0','1','0','1','0'],  # 7
        ['0','1','1','1','1','1','1','1','1','0','1','0'],  # 8
        ['0','0','0','0','0','0','1','0','0','0','1','0'],  # 9
        ['1','1','1','1','1','1','1','1','1','1','1','0'],  # 10
        ['0','0','0','0','0','0','0','0','0','0','0','0']   # 11
    ]

    print("\n_________  Start State    _________\n")
    printBoard(board, board_size)

    ################ bfs execution ################

    print("\n________________________________________ BFS ________________________________________________\n")

    print("\nSearching nodes...")
    bfs_result = bfs(board, board_size)

    if bfs_result == None:
        print("No solution found")

    elif bfs_result == [None]:
        print  ("Agent is already at the end of the maze!")

    else:
        print("\n_________   BFS End State    _________\n")
        printBoard(bfs_result.board, board_size)
        print("\nAlgorithm used: BFS :")
        print("\tTotal number of moves needed: ", bfs_result.steps)
        print("\tTotal number of states examined: ", moves[0]) 

        opt = input("\nPress 1 to view moves from start to end, or any other key to continue to DFS: ")
        if (opt == '1') :
            node_seq = []
            node_seq.append(bfs_result)
            current_node = bfs_result

            while (current_node.parent is not None) :
                parent_node = current_node.parent
                prev_node = parent_node

                node_seq.append(prev_node)
                current_node = parent_node

            node_seq.reverse()

            print("\nSequence from start -> goal:\n\tAgent initially at index (4, 11)")

            for node in node_seq :
                if (node.operator is not None) :
                    pos = getAgentPosition(node.board)
                    print("\tAgent moves " + node.operator + " to index " + str(pos))

    moves.clear()
    visited_pos.clear()

    ################ dfs execution ################

    print("\n________________________________________ DFS ________________________________________________\n")

    print("\n Searching nodes...")
    dfs_result = dfs(board, board_size)

    if dfs_result == None:
        print("No solution found")

    elif dfs_result == [None]:
        print  ("Agent is already at the end of the maze!")

    else:
        print("\n_________   DFS End State    _________\n")
        printBoard(dfs_result.board, board_size)
        print("\nAlgorithm used: DFS :")
        print("\tTotal number of moves needed: ", bfs_result.steps)
        print("\tTotal number of states examined: ", moves[0]) 

        opt = input("\nPress 1 to view moves from start to end, or any other key to exit: ")
        if (opt == '1') :
            node_seq = []
            node_seq.append(dfs_result)
            current_node = dfs_result

            while (current_node.parent is not None) :
                parent_node = current_node.parent
                prev_node = parent_node

                node_seq.append(prev_node)
                current_node = parent_node

            node_seq.reverse()

            print("\nSequence from start -> goal:\n\tAgent initially at index (4, 11)")

            for node in node_seq :
                if (node.operator is not None) :
                    pos = getAgentPosition(node.board)
                    print("\tAgent moves " + node.operator + " to index " + str(pos))

    print("_____________________________________________________")

if __name__ == "__main__":
    main()