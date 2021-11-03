import numpy as np

class ExactInference:
    def __init__(self):
        pass

    def variableElimination(self, query, evidence, bn):
        if query in evidence.keys():
            print("NOPE")
            quit()
        factors = []
        # instead of reversed do we need a heuristic for ordering
        for v in reversed(bn.variables):
            factors = self.makeFactor(v, evidence, bn) + factors
            #if v is a hidden variable using query:
            #    factors = self.sumOut(v, factors)
        return np.linalg.norm(self.pointwiseProduct(factors))


    def makeFactor(self, v, e, bn):
        node = bn.getNode(v)
        var =
        pass
        #return factors

    def sumOut(self, v, factors):
        return factors

    def pointwiseProduct(self, factors):
        return factors