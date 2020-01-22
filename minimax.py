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
        self.create_children()


    def get_row_num(self):
        return self.list.pop(0)

    def get_col_num(self):
        return self.list.pop(0)

    def create_children(self):
        global node_created
        #Creating all the children of current node by checking 0 edges.
        for i in range (0, len(self.onlylineslist)):
            if(self.onlylineslist[i] == 0):
                child_lines = self.onlylineslist.copy()
                child_lines[i] = 1
                child_list = self.create_list(child_lines, self.player1_score, self.player2_score)
                #Checking the current value and potential child values
                if(self.get_total() < self.get_list_total(child_list)):
                    #Checking whose round
                    if(self.playerNum == 1):
                        self.children.append(Node(self.create_list(child_lines, (self.player1_score + 1), self.player2_score), self.depth+1, self.playerNum))
                        node_created+=1
                    if(self.playerNum == -1):
                        self.children.append(Node(self.create_list(child_lines, self.player1_score , (self.player2_score + 1)), self.depth+1, self.playerNum))
                        node_created+=1
                else: 
                    self.children.append(Node(child_list, self.depth+1, -self.playerNum))
                    node_created+=1
    
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

def MinMax(node):    

    if (len(node.children) == 0):
        return node.player1_score, node.player2_score

    ### Max is player1(RED) and Min is player2(BLUE)
    ### If player2 wants to have min value, this can be minimum score for player 1 or maximum score for player2
    ### I prefer chosing maximum for both. Yet, only checking player1 score to min and max can be used as well.

    best_val1 = maxsize * -1    
    best_val2 = maxsize * -1

    for i in range(len(node.children)): #Getting leaf's score values
        child = node.children[i]
        p1, p2 = MinMax(child)
        
        if(node.playerNum == 1): #Check for whose turn
            if(best_val1 < p1): 
                best_val1 = p1
                best_val2 = p2
        elif(node.playerNum == -1): #Check for whose turn
            if(best_val2 < p2):
                best_val1 = p1
                best_val2 = p2

    return best_val1, best_val2 #Returning best scores for player which have game round.
        


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

    p1_score, p2_score = MinMax(node)
    
    print("Red and Blue Score with Minimax Algorithm")
    print(p1_score)
    print(p2_score)

    #timestamp for algorithm's end
    stop = timeit.default_timer()

    print("Running time of algorithm: ", stop - start)

    print("Total node created: ", node_created, "(without root)")
