import random as rand
from BayesNet import BayesNet

class ApproxInterface:
    def __init__(self):
        pass

    def normalize(self, node):
        return [x / sum(node) for x in data]

    def markov_blanket(self, X, e, bn):

        markov_list = []
        Node = BayesNet.getNode(bn, X)

        for child in Node.children:
            markov_list.append(child)
            for child_parent in Node.parent:
                markov_list.append(parent)

        for parent in Node.parent:
            markov_list.append(parent)

        print(markov_list)

        return markov_list



        #for child in Node.children:


        pass

    def gibbsSampling(self, X, e, bn, n=1000):

        count = []
        Z = [var for var in bn.nodes if var not in e]
        x = e


        pass
        """
      

        for Zi in Z:
            x[Zi] = rand.choice(bn.variables(Zi))
        for j in range(N):
            for Zi in Z:
                x[Zi] = markov_blanket(Zi, x, bn)
                count[x[X]] += 1
        """







