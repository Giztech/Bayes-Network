import numpy as np
import itertools

class ExactInference:
    def __init__(self):
        self.count = 0
        pass

    def variableElimination(self, query, evidence, bn):
        if query in evidence.keys():
            print(evidence[query])
            quit()
        factors = {}   #3d dict [v][string of parents][v.domain val]
        # instead of reversed do we need a heuristic for ordering
        for v in bn.variables:
            print(v)
            factors = {**self.makeFactor(v, evidence, bn), **factors}
            if v != query and v not in evidence.keys():    #is a hidden variable if hidden we sum over that var
                factors = self.sumOut(v, factors, bn)
            print(factors["['" + query + "']"])
        print([float(i)/sum(self.dict_to_matrix(factors["['"+query+"']"])) for i in self.dict_to_matrix(factors["['"+query+"']"])])
        print(self.count)
        print(factors["['"+query+"']"])
        return [float(i)/sum(self.dict_to_matrix(factors["['"+query+"']"])) for i in self.dict_to_matrix(factors["['"+query+"']"])]


    def makeFactor(self, v, e, bn):
        #get probs
        out = {}
        node = bn.getNode(v)
        for child in [v] + node.children:
            var = []
            par_val = []
            factors = {}
            c_node = bn.getNode(child)
            if c_node.prob == {}:
                continue
            for par in c_node.parent:
                if par not in e.keys():
                    var.append(par)
                    par_val.append(bn.getNode(par).domain)
                else:
                    bn.getNode(par).domain = [e[par]]
                    par_val.append([e[par]])
            if child in e.keys():
                c_node.domain = [e[child]]
                v_key = [e[child]]
            else:
                v_key = c_node.domain
            if len(par_val) == 0:
                if len(v_key) == 1:
                    factors = c_node.prob[v_key[0]]
                else:
                    factors = c_node.prob
            else:
                par_keys = list(itertools.product(*par_val))
                for pk in par_keys:
                    key = ""
                    for val in pk:
                        key += str(val) + ', '
                    key = key[:-2]
                    for vk in v_key:
                        factors[key + ", " + vk] = c_node.prob[key][vk]
            out[str(c_node.parent + [child])] = factors
        return out #dict of probs

    def sumOut(self, v, factors, bn):
        #iterate over domain v
        v_node = bn.getNode(v)
        for p in v_node.parent:
            p_node = bn.getNode(p)
            p_node.children.remove(v)
        for c in v_node.children:
            c_node = bn.getNode(c)
            c_node.parent.remove(v)
            c_node.prob = {}
        looking_f = []
        looking_f_keys = []
        out = {}
        for f in factors.keys():
            check = self.key_to_string(f)
            if v in check:
                looking_f += [factors[f]]
                looking_f_keys.append(check)
            else:
                out[f] = factors[f]
        pp = self.pointwiseProduct(looking_f, looking_f_keys, bn)

        mylist = {}
        gone = None
        for key, val in pp.items():
            check = self.key_to_string(key)
            for c in check:
                if c == v:
                    loc = check.index(c)
                    gone = loc

            for d in v_node.domain:
                for key1, value in val.items():
                    check1 = self.key_to_string(key1)
                    if d in check1[loc]:
                        temp = check1.copy()
                        del temp[loc]
                        if str(temp) not in mylist.keys():
                            mylist[str(temp)] = value
                        else:
                            mylist[str(temp)] += value

            del check[gone]
        print(str(check))
        out[str(check)] = mylist
        print('here', out)
        return out

    def pointwiseProduct(self, factors, keys, bn):
        print('new pp')
        out = {}
        out_keys = []
        for i in range(len(factors)):
            if i == 0:  #len(out) == 0:
                out = factors[i]
                out_keys = keys[i]
            else:
                overlap = []
                for k in keys[i]:
                    if k in out_keys:
                        overlap.append(k)
                loc1 = []
                loc = []
                domain_vals = []
                for o in overlap:
                    loc1.append(out_keys.index(o))
                    loc.append(keys[i].index(o))
                    domain_vals.append(bn.getNode(o).domain)
                dv = list(itertools.product(*domain_vals))
                temp_dict = {}
                for d in dv:
                    for key, val in factors[i].items():
                        check = self.key_to_string(key)
                        for key1, val1 in out.items():
                            check1 = self.key_to_string(key1)
                            count = 0
                            for x in range(len(loc1)):
                                if check[loc[x]] == d[x] and check1[loc1[x]] == d[x]:
                                    count += 1
                            #print('here', count, len(loc1))
                            if count == len(loc1):
                                temp1 = []
                                for l in range(len(check)):
                                    if l not in loc:
                                        temp1.append(check[l])
                                index = temp1 + check1
                                use = ""
                                for ind in index:
                                    use += str(ind) + ', '
                                use = use[:-2]
                                temp_dict[use] = val * val1
                                self.count += 1
                print(temp_dict)
                out = temp_dict
                temp = []
                for l in range(len(keys[i])):
                    if l not in loc:
                        temp.append(keys[i][l])
                out_keys = temp + out_keys
        print('out', out)
        return {str(out_keys): out}

    def dict_to_matrix(self, dict):
        out = []
        for keys, vals in dict.items():
            try:
                for keys1, vals1 in vals.items():
                    out.append(vals1)
            except:
                out.append(vals)
        return out

    def key_to_string(self, key):
        check = key.replace('[', "")
        check = check.replace(']', "")
        check = check.replace("'", "")
        check = check.replace(" ", "")
        check = check.split(',')
        return check

