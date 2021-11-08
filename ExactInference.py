import numpy as np
import itertools

class ExactInference:
    def __init__(self):
        pass

    def variableElimination(self, query, evidence, bn):
        if query in evidence.keys():
            print("NOPE")
            quit()
        factors = {}   #3d dict [v][string of parents][v.domain val]
        # instead of reversed do we need a heuristic for ordering
        for v in reversed(bn.variables):
            print(v)
            factors = {**self.makeFactor(v, evidence, bn), **factors}
            if v != query and v not in evidence.keys():    #is a hidden variable if hidden we sum over that var
                print('calling SumOut')
                factors = self.sumOut(v, factors, bn)
                print(factors)
                quit()
        print('ENDING')
        return np.linalg.norm(self.pointwiseProduct(factors))


    def makeFactor(self, v, e, bn):
        #get probs
        out = {}
        node = bn.getNode(v)
        for child in [v] + node.children:
            var = []
            par_val = []
            factors = {}
            c_node = bn.getNode(child)
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
        print('var', v)
        v_node = bn.getNode(v)
        for p in v_node.parent:
            p_node = bn.getNode(p)
            p_node.children.remove(v)
        for c in v_node.children:
            c_node = bn.getNode(c)
            c_node.parent.remove(v)

        looking_f = []
        looking_f_keys = []
        for f in factors.keys():
            check = f.replace('[', "")
            check = check.replace(']', "")
            check = check.replace("'", "")
            check = check.replace(" ", "")
            check = check.split(',')
            print(check)
            if v in check:
                looking_f += [factors[f]]
                print(factors[f])
                looking_f_keys.append(check)
        print('this', looking_f_keys)
        # pp = self.pointwiseProduct(looking_f, looking_f_keys, bn, v)
        mylist = {}
        for key, val in factors.items():
            k = key
            check = k.replace('[', "")
            check = check.replace(']', "")
            check = check.replace("'", "")
            check = check.replace(" ", "")
            check = check.split(',')
            for c in check:
                if c == v:
                    loc = check.index(c)
                    # print(loc)
            del check[loc]
            newkey = str(check)
            for d in v_node.domain:
                for key1, value in val.items():
                    print('heres valeu', value)
                    check = key1.replace('[', "")
                    check = check.replace(']', "")
                    check = check.replace("'", "")
                    check = check.replace(" ", "")
                    check = check.split(',')
                    if d in check[loc]:
                        print('before', check)

                        del check[loc]
                        if str(check) not in mylist.keys():
                            mylist[str(check)] = value
                        else:
                            mylist[str(check)] += value
                        print('check after', check)



        print(mylist)
        return {newkey: mylist}

    def pointwiseProduct(self, factors, keys, bn, v):
        print('pp\n\n\n')
        out = {}
        out_keys = []
        print(len(factors))
        print(len(keys))
        for i in range(len(factors)):
            print(factors[i])
            if len(out) == 0:
                out[str(keys[i])] = factors[i]
                print('out', out)
                out_keys += keys[i]
            else:
                overlap = []
                for k in keys[i]:
                    if k in out_keys:
                        overlap.append(k)
                print("O", overlap)
                loc1 = []
                loc2 = []
                #DEAL WITH MULTIPLE OVERLAPSSSSS
                #for o in overlap:
                loc1 = out_keys.index(overlap[0])
                loc2 = keys[i].index(overlap[0])
                print('look here')
                print(len(out_keys))
                print(len(keys[i]))
                print(factors[i].keys())
                print(out.keys())
                out_keys = (keys[i] + out_keys)
                out_keys.remove(overlap[0])
                for d in bn.getNode(overlap[0]).domain:
                    for key, val in factors[i].items():
                        check = key.replace('[', "")
                        check = check.replace(']', "")
                        check = check.replace("'", "")
                        check = check.replace(" ", "")
                        check = check.split(',')
                        for key1, val1 in out.items():
                            print('hereke', key1, 'KDFJDK')
                            for vit in val1.keys():
                                check1 = vit.replace('[', "")
                                check1 = check1.replace(']', "")
                                check1 = check1.replace("'", "")
                                check1 = check1.replace(" ", "")
                                check1 = check1.split(',')
                                # print('lalal', check,check1)
                                # if check[loc2] == d and check1[loc1] == d:
                                #     out[(check + check1).remove(overlap[0])] = val * val1
        print(out)
        return out
    # def pointwiseProduct(self, factors, keys, bn, v):  #return a matrix
    #     # if len(factors) == 1:
    #     #     return factors[0]
    #     # else:
    #     count = {}
    #     print(factors)
    #     print(keys)
    #     for key in keys:
    #         if key in count:
    #             count[key] += 1
    #         else:
    #             count[key] = 1
    #         check = bn.getNode(key)
    #         for c in check.parent:
    #             if c in count:
    #                 count[c] += 1
    #             else:
    #                 count[c] = 1
    #     notable_var = []
    #     for key, val in count.items():
    #         if val > 1:
    #             notable_var.append(key)
    #     # notable_var.remove(v)
    #     v_node = bn.getNode(v)
    #     for i in range(len(factors)):
    #         if len(notable_var) == 0 or keys[i] not in notable_var:
    #             v_node.parent
    #             out = factors[i]
    #             #simple multiply
    #         # else:


        # ret_val = []
        # for d in v_node.domain: #get var at all stages, make factors for each
        #     to_pp = []
        #     for i in range(len(looking_f)):
        #         out = {}
        #         if i == 0:
        #             if len(bn.getNode(looking_f_keys[i]).parent) == 0:
        #                 out[v] = looking_f[i][d]
        #             else:
        #                 for var, val in looking_f[i].items():
        #                     out[var] = {}
        #                     out[var][d] = val[d]
        #         else:
        #             #now v is a part of outer vals
        #             if len(bn.getNode(looking_f_keys[i]).parent) != 0:
        #                 par_vals = []
        #                 for par in bn.getNode(looking_f_keys[i]).parent:
        #                     if par == v:
        #                         par_vals.append([d])
        #                     else:
        #                         if bn.getNode(par).domain_exists == True:
        #                             par_vals.append(bn.getNode(par).domain)
        #                 par_keys = list(itertools.product(*par_vals))
        #                 for p in par_keys:
        #                     key = ""
        #                     for val in p:
        #                         key += str(val) + ', '
        #                     key = key[:-2]
        #                     out[key] = looking_f[i][key]
        #             else:
        #                 print('ERROR')
        #                 quit()
        #         to_pp.append(out)
        #     if len(ret_val) == 0:
        #         ret_val = self.pointwiseProduct(to_pp, looking_f_keys, bn, v)
        #     else:
        #         pp = self.pointwiseProduct(to_pp, looking_f_keys, bn, v)
        #         for i in range(len(ret_val)):
        #             ret_val[i] += pp[i]
        #
        # # turn list back to dict
        # for c in v_node.children:
        #     if c in factors.keys():
        #         c_node = bn.getNode(c)
        #         if len(c_node.originalParents) == 0:
        #             c_node.originalParents = c_node.parent
        #         temp = c_node.originalParents.copy()
        #         temp.remove(v)
        #         v_node.parent += temp
        #         v_node.parent.append(c)
        # v_node.domain_exists = False
        # par_val = []
        # for par in v_node.parent:
        #     if bn.getNode(par).domain_exists == True:
        #         par_val.append(bn.getNode(par).domain)
        # par_keys = list(itertools.product(*par_val))
        # # print(par_keys)
        # # print(v_node.parent)
        # # print(looking_f_keys)
        # # print('ret_val', ret_val)
        # new_dict = {}
        # for i in range(len(par_keys)):
        #     key = ""
        #     for val in par_keys[i]:
        #         key += str(val) + ', '
        #     key = key[:-2]
        #     new_dict[key] = ret_val[i]
        # print(new_dict)
        # return [new_dict]


    #
    #
    #
    #
    #
    #
    #         if len(notable_var) == 0:
    #             for i in range(len(factors)):
    #                 if i == 0:
    #                     out = self.dict_to_matrix(factors[i])
    #                 else:
    #                     mult = self.dict_to_matrix(factors[i])
    #                     temp = []
    #                     for o in out:
    #                         for m in mult:
    #                             temp.append(o*m)
    #                     out = temp
    #         else:
    #             print(notable_var)
    #             for n in notable_var:
    #                 for d in bn.getNode(n).domain:
    #                     for i in range(len(factors)):
    #                         if i == 0:
    #                             out = self.dict_to_matrix(factors[i])
    #                             if bn.getNode(keys[i]).name == n:
    #                                 pass
    #                             elif n in
    #                         else:
    #                             mult = self.dict_to_matrix(factors[i])
    #                             print(bn.getNode(keys[i]))
    #                             temp = []
    #                             for o in out:
    #                                 for m in mult:
    #                                     temp.append(o*m)
    #                             out = temp
    #             quit()
    #         return out
    #
    # def dict_to_matrix(self, dict):
    #     out = []
    #     for keys, vals in dict.items():
    #         try:
    #             for keys1, vals1 in vals.items():
    #                 out.append(vals1)
    #         except:
    #             out.append(vals)
    #     return out
    #
    # def matrix_to_dict(self):
    #     # turn list back to dict
    #     for c in v_node.children:
    #         if c in factors.keys():
    #             c_node = bn.getNode(c)
    #             if len(c_node.originalParents) == 0:
    #                 c_node.originalParents = c_node.parent
    #             temp = c_node.originalParents.copy()
    #             temp.remove(v)
    #             v_node.parent += temp
    #             v_node.parent.append(c)
    #     v_node.domain_exists = False
    #     par_val = []
    #     for par in v_node.parent:
    #         if bn.getNode(par).domain_exists == True:
    #             par_val.append(bn.getNode(par).domain)
    #     par_keys = list(itertools.product(*par_val))
    #     # print(par_keys)
    #     # print(v_node.parent)
    #     # print(looking_f_keys)
    #     # print('ret_val', ret_val)
    #     new_dict = {}
    #     for i in range(len(par_keys)):
    #         key = ""
    #         for val in par_keys[i]:
    #             key += str(val) + ', '
    #         key = key[:-2]
    #         new_dict[key] = ret_val[i]
    #     print(new_dict)

