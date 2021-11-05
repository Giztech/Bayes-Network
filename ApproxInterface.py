import random as rand


class ApproxInterface:
    def __init__(self):
        pass

    def get_markov_blanket(self, X, bn):

        markov_list = []
        node = bn.getNode(X)

        # get the children and children's parents of selected node

        for child in node.children:
            markov_list.append(child)
            for child_parent in node.parent:
                markov_list.append(child_parent)

        # get the parents of selected node

        for parent in node.parent:
            markov_list.append(parent)

        list(set(markov_list))

        '''
        Test Statement
        
        for i in markov_list:
            node = bn.getNode(i)
            print(node.name)
        
        '''


        return markov_list

    def gibbsSampling(self, X, evidence, bn, N=1000):

        count = []
        Z = [var for var in bn.nodes if var not in evidence]
        x = evidence

        # random choice each domain of a node then set it

        for node in bn.nodes:
                node.domain = rand.choice(node.domain)
                print(node.name)
                print(node.domain)

        for j in range(N):
            for node in bn.nodes:
                pass



        pass
