import json
# 1 = our ball
# 0 = oppenent's ball

        #center     #left     #right    #leftleft  #rightright
silo = [['Red','Blue','Red'],    ['Red','Blue'],    ['Red','Blue'],    [],        ['Blue','Blue']]

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
        if (['Red','Blue'] in silo) or (['Blue','Red'] in silo):
            if (['Red','Blue'] in silo):
                pr1 = silo.index(['Red','Blue'])
            if (['Blue','Red'] in silo):
                pr2 = silo.index(['Red','Blue'])
            if pr1 < pr2:
                print(f"['Red','Blue'] : {pr1}")
                return pr1
            else:
                print(f"['Blue,'Red'] : {pr2}")
                return pr2
        elif (['Blue','Blue'] in silo):
            pr3 = silo.index(['Blue','Blue'])
            print(f"['Blue','Blue'] : {pr3}")
            return pr3
        else:
            self.shortest_path_state += 1
            return self.shortest_path_state - 1

what = Decision(silo)
what.silo_decision()
print(what.shortest_path_state)

