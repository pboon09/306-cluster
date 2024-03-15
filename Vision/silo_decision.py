import json
# 1 = our ball
# 0 = oppenent's ball

        #center     #left     #right    #leftleft  #rightright
silo = [[1,0,1],    [1,0],    [1,0],    [],        [0,0]]

        #center     #left     #right    #leftleft  #rightright
silo = [[],    [],    [],    [],        []]

class Decision:
    def __init__(self, silo):

        self.shortest_path_state = 0 
        self.silo = silo

    def silo_decision(self):
        pr1 = 5
        pr2 = 5
        pr3 = 5
        if ([1,0] in silo) or ([0,1] in silo):
            if ([1,0] in silo):
                pr1 = silo.index([1,0])
            if ([0,1] in silo):
                pr2 = silo.index([1,0])
            if pr1 < pr2:
                print(f"[1,0] : {pr1}")
                return pr1
            else:
                print(f"[0,1] : {pr2}")
                return pr2
        elif ([0,0] in silo):
            pr3 = silo.index([0,0])
            print(f"[0,0] : {pr3}")
            return pr3
        else:
            self.shortest_path_state += 1
            return self.shortest_path_state - 1

what = Decision(silo)
what.silo_decision()
print(what.shortest_path_state)

