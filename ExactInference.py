import numpy as np
import itertools

class ExactInference:
    def __init__(self):
        pass

    def variableElimination(self, query, evidence, bn):
        if query in evidence.keys():
            print("NOPE")
            quit()
        factors = {}    #3d dict [v][string of parents][v.domain val]
        # instead of reversed do we need a heuristic for ordering
        for v in reversed(bn.variables):
            factors[v] = [self.makeFactor(v, evidence, bn)]
            if v != query and v not in evidence.keys():    #is a hidden variable if hidden we sum over that var
                factors = self.sumOut(v, factors, bn)    #this might be wrong
        return np.linalg.norm(self.pointwiseProduct(factors))


    def makeFactor(self, v, e, bn):
        #get probs
        node = bn.getNode(v)
        var = []
        par_val = []
        factors = {}
        for par in node.parent:
            if par not in e.keys():
                var.append(par)
                par_val.append(bn.getNode(par).domain)
            else:
                bn.getNode(par).domain = [e[par]]
                par_val.append([e[par]])
        if v in e.keys():
            node.domain = [e[v]]
            v_key = [e[v]]
        else:
            v_key = node.domain
        if len(par_val) == 0:
            factors = node.prob
        else:
            par_keys = list(itertools.product(*par_val))
            for pk in par_keys:
                key = ""
                for val in pk:
                    key += str(val) + ', '
                key = key[:-2]
                factors[key] = {}
                for vk in v_key:
                    factors[key][vk] = node.prob[key][vk]
        return factors #dict of probs

    def sumOut(self, v, factors, bn):
        #iterate over domain v
        print('var', v)
        v_node = bn.getNode(v)
        looking_f = [factors[v]]     #list of dicts
        looking_f_keys = [v]
        for f in factors.keys():
            f_node = bn.getNode(f)
            # if v in f_node.children:  #if v is a parent of f
            #     looking_f.append(factors[f])
            #     looking_f_keys.append(f_node.name)
            if v in f_node.parent:  #if v is a child of f
                looking_f.append(factors[f])
                looking_f_keys.append(f_node.name)
        for d in v_node.domain: #get var at all stages, make factors for each
            to_pp = []
            for i in range(len(looking_f)):
                out = {}
                if i == 0:
                    if len(bn.getNode(looking_f_keys[i]).parent) == 0:
                        out = looking_f[i][0][d]
                    else:
                        for var, val in looking_f[i][0].items():
                            out[var] = {}
                            out[var][d] = val[d]
                else:
                    #now v is a part of outer vals
                    par_vals = []
                    print(par_vals)
                    print(bn.getNode(looking_f_keys[i]).parent)
                    for par in bn.getNode(looking_f_keys[i]).parent:
                        if par == v:
                            par_vals.append([d])
                            print('this')
                        else:
                            par_vals.append(bn.getNode(par).domain)
                        print(par_vals)
                    par_keys = list(itertools.product(*par_vals))
                    print(looking_f[i][0])
                    for p in par_keys:
                        key = ""
                        for val in p:
                            key += str(val) + ', '
                        key = key[:-2]
                        print(key)
                        out[p] = looking_f[i][0][key]
                to_pp.append(out)
            print(len(to_pp))
            #print(looking_f_keys)
            self.pointwiseProduct(to_pp, looking_f_keys, bn)
            # pp + pp + pp
            #need to return factors as dict of dicts
        quit()
        return factors

    def pointwiseProduct(self, factors, keys, bn):
        #checking if
        if len(factors) == 1:
            return {keys[0]: factors}
        else:
            for i in range(len(factors)):
                check = bn.getNode(keys[i]).parent
                check.append(keys[i])
                #print('this', check)
                if i == 0:
                    #inside
                    pass
                else:
                    #outside
                    pass
                print(bn.getNode(keys[i]).parent)
        #quit()
        return factors

    def dict_to_matrix(self, dict):
        pass
