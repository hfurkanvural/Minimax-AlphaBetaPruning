from sys import maxsize
import sys
import timeit

node_created = 0

class Node (object):
    def __init__ (self, list, depth, playerNum):
        self.playerNum = playerNum
        self.depth = depth
        self.list = list
        self.rows = self.get_row_num()
        self.cols = self.get_col_num()
        self.horizontal_edge_num = self.get_h_nums()
        self.vertical_edge_num = self.get_v_nums()
        self.horizontal_edges = self.get_h_edges()
        self.vertical_edges = self.get_v_edges()
        self.player1_score = self.get_p1_score()
        self.player2_score = self.get_p2_score()
        self.onlylineslist = self.horizontal_edges + self.vertical_edges
        self.children = []

    def get_row_num(self):
        return self.list.pop(0)

    def get_col_num(self):
        return self.list.pop(0)

    #Getting total square number
    def get_total(self): 
        total = 0
        for i in range(0, self.horizontal_edge_num - (self.cols) ):
            total += self.check_is_square(i)
        return total
    
    #Checking the horizontal edge if it is a square or not
    def check_is_square(self,i):
        if (self.horizontal_edges[i] == 1):
            if(self.horizontal_edges[i + self.cols] == 1): #i + cols + 1 gives bottom horizontal line of the current line 
                # (i/(self.cols+1)) gives row number of the line and (self.rows+1) gives total vertical num
                #(i%(self.cols+1) gives the current line number on horizontally.
                j = (int(i/(self.cols)) * (self.rows+1)) + (i%self.cols)
                #j is the bottom left edge of current horizontal edge
                if(self.vertical_edges[j] == 1 ):
                    if(self.vertical_edges[j+1] == 1):
                        return 1
        return 0

    #Getting total square number for list.
    def get_list_total(self, list):
        total = 0
        for i in range(0, self.horizontal_edge_num - (self.cols) ):
            total += self.list_check_is_square(i,list)
        return total

    #Checking the edge in a list
    def list_check_is_square(self,i, list):
        h_edges = list[2:(2+self.horizontal_edge_num)]
        v_edges = list[(2+self.horizontal_edge_num):-2]
        if (h_edges[i] == 1):
            if(h_edges[i + self.cols] == 1): #i + cols + 1 gives bottom horizontal line of the current line 
                # (i/(self.cols+1)) gives row number of the line and (self.rows+1) gives total vertical num
                #(i%(self.cols+1) gives the current line number on horizontally.
                j = (int(i/(self.cols)) * (self.rows+1)) + (i%self.cols) 
                if(v_edges[j] == 1 ):
                    if(v_edges[j+1] == 1):
                        return 1
        return 0
    
    def get_h_nums(self):
        return self.cols * (self.rows + 1) 

    def get_v_nums(self):
        return self.rows * (self.cols + 1) 

    def get_h_edges(self):
        horizontal_edges = []
        for i in range(self.horizontal_edge_num):
            horizontal_edges.append(self.list.pop(0))
        return horizontal_edges

    def get_v_edges(self):
        vertical_edges = []
        for i in range(self.vertical_edge_num):
            vertical_edges.append(self.list.pop(0))
        return vertical_edges
    
    def get_p1_score(self):
        return self.list.pop(0)

    def get_p2_score(self):
        return self.list.pop(0)

    #Creating input format list
    def create_list(self, newlist, p1, p2): 
        return [self.rows] + [self.cols] + newlist + [p1] + [p2]

    #Getting max potential score
    def get_max_score(self):
        current_score = self.get_total()
        current_list = self.onlylineslist.copy()
        maxscore = 0

        for i in range (0, len(current_list)):
            if(current_list[i] == 0):
                current_list[i] = 1
                new_list = self.create_list(current_list, self.player1_score, self.player2_score)
                new_score = self.get_list_total(new_list)
                if(current_score < new_score):
                    maxscore +=1
                    current_score = new_score
        
        return maxscore

def alphabeta(node, a, b):
    global node_created
    ### Max is player1(RED) and Min is player2(BLUE)
    ### If player1 wants max and player2 wants min, we can assume that only checking for player1 could be enough
    ### or we can design a race condition for both to be max. I prefer chosing max-min value check on player1 score.

    #Checking if the node is leaf
    if(node.onlylineslist.count(0)==0):
        return node.player1_score
    #Check for if player turn is Red
    if(node.playerNum == 1):
        #loop for every edge
        for i in range (0, len(node.onlylineslist)):
            #Control for empty edge
            if(node.onlylineslist[i] == 0):
                child_lines = node.onlylineslist.copy()
                child_lines[i] = 1
                child_list = node.create_list(child_lines, node.player1_score, node.player2_score)
                #Check if there is a score
                if(node.get_total() < node.get_list_total(child_list)):
                    if(node.playerNum == 1):
                        node.children.append(Node(node.create_list(child_lines, (node.player1_score + 1), node.player2_score), node.depth+1, node.playerNum))
                        node_created+=1
                    if(node.playerNum == -1):
                        node.children.append(Node(node.create_list(child_lines, (node.player1_score), (node.player2_score + 1)), node.depth+1, node.playerNum))
                        node_created+=1
                else: 
                    node.children.append(Node(child_list, node.depth+1, -node.playerNum))
                    node_created+=1

                #Getting last appended child of node and getting highest possible child values
                a = max(a, alphabeta(node.children[-1], a, b))
                #pruning
                if(a >= b):
                    break
        return a
    #Check for if player turn is Blue
    if(node.playerNum == -1):
        for i in range (0, len(node.onlylineslist)):
            if(node.onlylineslist[i] == 0):
                child_lines = node.onlylineslist.copy()
                child_lines[i] = 1
                child_list = node.create_list(child_lines, node.player1_score, node.player2_score)
                if(node.get_total() < node.get_list_total(child_list)):
                    if(node.playerNum == 1):
                        node.children.append(Node(node.create_list(child_lines, (node.player1_score + 1), node.player2_score), node.depth+1, node.playerNum))
                        node_created+=1
                    if(node.playerNum == -1):
                        node.children.append(Node(node.create_list(child_lines, (node.player1_score), (node.player2_score + 1)), node.depth+1, node.playerNum))
                        node_created+=1
                else:
                    node.children.append(Node(child_list, node.depth+1, -node.playerNum))
                    node_created+=1
                #Getting last appended child of node and getting lowest possible child value
                b = min(b, alphabeta(node.children[-1], a, b))
                #pruning
                if(a >= b):
                    break
        return b

if __name__ == "__main__":

    if (len(sys.argv)<2):
        filename="input_11.txt"
    else:
        filename= str(sys.argv[1])

    lineList = list()
    with open(filename) as f:
        for line in f:
            lineList.append(int(line))

    #timestamp for algorithm starting by first node's creation
    start = timeit.default_timer()

    #playerNum defines the turn (1=Red, -1=Blue)
    node = Node(lineList, 0, 1)

    #Since I only get Red's score, I need to have total scores to compute Blue's score.
    total_score =node.get_max_score()
    p1_score = alphabeta(node,(-1 * maxsize),maxsize)
    p2_score = total_score - p1_score

    print("Red and Blue Score with Alpha Beta Pruning")
    print(p1_score)
    print(p2_score)

    #timestamp for algorithm's end
    stop = timeit.default_timer()

    print("Running time of algorithm: ", stop - start)

    print("Total node created: ", node_created, "(without root)")
