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
            print(v)
            factors[v] = [self.makeFactor(v, evidence, bn)]
            if v != query and v not in evidence.keys():    #is a hidden variable if hidden we sum over that var
                print('calling SumOut')
                factors = {v: self.sumOut(v, factors, bn)}
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
        looking_f = factors[v]    #list of dicts
        looking_f_keys = [v]
        for f in factors.keys():
            f_node = bn.getNode(f)
            if v in f_node.parent:  #if v is a child of f
                looking_f += factors[f]
                looking_f_keys.append(f_node.name)
                print(looking_f)
                print(looking_f_keys)
        ret_val = []
        for d in v_node.domain: #get var at all stages, make factors for each
            to_pp = []
            for i in range(len(looking_f)):
                out = {}
                if i == 0:
                    if len(bn.getNode(looking_f_keys[i]).parent) == 0:
                        out[v] = looking_f[i][d]
                    else:
                        for var, val in looking_f[i].items():
                            out[var] = {}
                            out[var][d] = val[d]
                else:
                    #now v is a part of outer vals
                    if len(bn.getNode(looking_f_keys[i]).parent) != 0:
                        par_vals = []
                        for par in bn.getNode(looking_f_keys[i]).parent:
                            if par == v:
                                par_vals.append([d])
                            else:
                                par_vals.append(bn.getNode(par).domain)
                        print(bn.getNode(looking_f_keys[i]).parent)
                        par_keys = list(itertools.product(*par_vals))
                        for p in par_keys:
                            key = ""
                            for val in p:
                                key += str(val) + ', '
                            key = key[:-2]
                            print('this', looking_f[i])
                            out[p] = looking_f[i][key]
                    else:
                        print('ERROR')
                        quit()
                to_pp.append(out)
            if len(ret_val) == 0:
                ret_val = self.pointwiseProduct(to_pp, looking_f_keys, bn)
            else:
                pp = self.pointwiseProduct(to_pp, looking_f_keys, bn)
                for i in range(len(ret_val)):
                    ret_val[i] += pp[i]
        #turn list back to dict
        for c in v_node.children:
            if c in factors.keys():
                c_node = bn.getNode(c)
                if len(c_node.originalParents) == 0:
                    c_node.originalParents = c_node.parent
                temp = c_node.originalParents.copy()
                temp.remove(v)
                v_node.parent += temp
                v_node.parent.append(c)
        par_val = []
        for par in v_node.parent:
            par_val.append(bn.getNode(par).domain)
        par_keys = list(itertools.product(*par_val))
        # print(par_keys)
        # print(v_node.parent)
        # print(looking_f_keys)
        # print('ret_val', ret_val)
        new_dict = {}
        for i in range(len(par_keys)):
            new_dict[par_keys[i]] = ret_val[i]
        return new_dict

    def pointwiseProduct(self, factors, keys, bn):  #return a matrix
        if len(factors) == 1:
            return self.dict_to_matrix(factors)   #get fixed
        else:
            out = []
            for i in range(len(factors)):
                if i == 0:
                    out = self.dict_to_matrix(factors[i])
                else:
                    mult = self.dict_to_matrix(factors[i])
                    temp = []
                    for o in out:
                        for m in mult:
                            temp.append(o*m)
                    out = temp
            return out

    def dict_to_matrix(self, dict):
        out = []
        for keys, vals in dict.items():
            try:
                for keys1, vals1 in vals.items():
                    out.append(vals1)
            except:
                out.append(vals)
        return out

