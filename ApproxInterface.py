import random as rand

class ApproxInterface:
    def __init__(self):
        pass

    def normalize(self, node):
        return [x / sum(node) for x in data]

    def gibbsSampling(self, X, e, bn, n=1000):


        count = []
        Z = [var for var in bn.nodes if var not in e]
        x = e

        for Zi in Z:
            x[Zi] = rand.choice(bn.variables(Zi))
        for j in range(N):
            for Zi in Z:
                x[Zi] = markov_blanket(Zi, x, bn)
                count[x[X]] += 1


        return ProbDist(X, count)

    def markov_blanket(self, X, e, bn):

        #Dont Use

        Xnode = bn.val(X)
        Q = ProbDist(X)
        for xi in bn.val(X):
            ei = extend(e,X,xi)
            Q[xi] = Xnode.p(xi, e) * product(Yj.p(ei[Yj.variable], ei)for Yj in Xnode.children)

        return probability(Q.normalize()[True])

        #Dont use



