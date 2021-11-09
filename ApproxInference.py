import random as rand


class ApproxInference:
    def __init__(self):
        pass

    def get_markov_blanket(self, X, bn):

        markov_list = []
        node = X

        # get the children and children's parents of selected node

        for child in node.children:
            markov_list.append(child)
            # for child_parent in node.parent:
            #     markov_list.append(child_parent)

        # get the parents of selected node

        # for parent in node.parent:
        #     markov_list.append(parent)

        list(set(markov_list))

        '''
        Test Statement
        
        for i in markov_list:
            node = bn.getNode(i)
            print(node.name)
        
        '''


        return markov_list
    '''
    sets the initial values of the bayesian network by starting at the top node
    and setting the state based on the probability provided
    the non-root nodes are set based on the states of it's parents 
    and the probabilities provided
    '''
    def forwardSampling(self, evidence, bn):
        # if the node is evidence, we want to set it first!
        for node in bn.nodes:
            for key, val in evidence.items():
                if key == node.name:
                    if val in node.domain:
                        node.state = val
                    else:
                        print(val)
                        print('loser')
        # after setting the evidence, go through and set the rest of the states
        for node in bn.nodes:
            if node.state == '':
                parents = node.parent

                if len(parents) == 0:
                    # if this node has no parents, then we can just set it based on the probability given
                    problist = []
                    keylist = []
                    for key, val in node.prob.items():
                        problist.append(float(val))
                        keylist.append(key)
                    bn = self.updateState(node, problist, keylist, bn)
                else:
                    problist, keylist = self.getProb(parents, node, bn)
                    bn = self.updateState(node, problist, keylist, bn)
        return bn

    '''
    called when the node's parents need to have their states set
    used only for forward sampling
    '''
    def setParent(self, m, bn):
        gms = m.parent
        if len(gms) == 0:
            # if this node has no parents, then we can just set it based on the probability given
            problist = []
            keylist = []
            for key, val in m.prob.items():
                problist.append(float(val))
                keylist.append(key)
            return self.updateState(m, problist, keylist, bn)
        problist, keylist = self.getProb(gms, m, bn)
        return self.updateState(m, problist, keylist, bn)

    '''
    generates a random number and based on the probability, sets the state of the node given 
    '''
    def updateState(self, node, problist, keylist, bn):
        value = rand.random()
        for y in range(len(problist)):
            if y == 0:
                # if the random value is less than the first probability num
                if value < problist[y]:
                    bn.updateState(node, keylist[y])
                    return bn
                else:
                    continue
            # the current value to be looking at should be the previous prbability plus the current probability
            problist[y] += problist[y - 1]
            if value < problist[y]:
                bn.updateState(node, keylist[y])
                return bn
    '''
    Gets the probability list and key list for the given node and it's parents
    used only for forward sampling
    '''
    def getProb(self, parents, node, bn):
        parList = ''
        for p in parents:
            parNode = bn.getNode(p)
            if parNode.state == '':
                bn = self.setParent(parNode, bn)
            parList += (parNode.state) + ', '
        parList = parList[:-2]
        problist = []
        keylist = []
        for key, val in node.prob.items():
            if parList == key:
                for key1, val1 in node.prob[key].items():
                    problist.append(float(val1))
                    keylist.append(key1)
        return problist, keylist

    '''
    samples the current node and sets the value based on the markov blanket
    '''
    def setValue(self, node, bn):
        mb = self.get_markov_blanket(node, bn)
        # print(mb)
        total_prob = []
        for d in node.domain:
            problist = []
            bn.updateState(node, d)
            # to get the probabilities of the current node
            parlist = ''
            # to deal with no parents
            if len(node.parent) == 0:
                problist.append(node.prob[d])
            # to ddeal with parents
            else:
                for par in node.parent:
                    parlist += bn.getNode(par).state + ', '
                parlist = parlist[:-2]

                for key, val in node.prob.items():
                    if parlist == key:
                        problist.append(val[d])

            # to get the probabilities of the markov blanket
            for name in mb:
                mbnode = bn.getNode(name)
                # print(name, mbnode.state)

                parlist = ''
                for par in mbnode.parent:
                    parlist += bn.getNode(par).state + ', '
                parlist = parlist[:-2]
                # print(parlist, 'aprlier')


                keylist = []
                for key,val in mbnode.prob.items():
                    if parlist == key:
                        for d1 in mbnode.domain:
                            if d1 == mbnode.state:
                                problist.append( val[d1])
                        # problist.append(val)
                        # keylist.append(key)
            # print('problist', problist)
            mult = 1
            for p in problist:
                mult *= p
            total_prob.append(mult)
            # print('\n\n New domain')
        calc_prob = []
        total = 0
        # print('total prob', total_prob)
        for m in total_prob:
            total += m
        if total == 0:
            print('total is 0', node.name)
        else:
            for m in total_prob:
                calc_prob.append(m / total)
        # print('calc_prob', calc_prob)
        bn = self.updateState(node, calc_prob, node.domain, bn)

        return bn


    def gibbsSampling(self, X, evidence, bn, N):

        count = {}
        for d in bn.getNode(X).domain:
            count[d] = 0
        Z = []
        # for every node not in evidence, add to Z
        for node in bn.nodes:
            add = True
            for key, val in evidence.items():
                if key == node.name:
                    add = False
                    break
            if add:
                Z.append(node)

        # forward sampling to set the initial values for bn
        x = self.forwardSampling(evidence, bn)
        # for node in x.nodes:
        #     # print(node.name)
        #     # print(node.domain)
        #     if node.state == '':
        #         print('aint no satte here')
        test_node = bn.getNode('HR')

        x.updateState(test_node, 'NORMAL')
        test_node = bn.getNode('HRSAT')
        x.updateState(test_node, 'NORMAL')
        test_node = bn.getNode('HREKG')
        x.updateState(test_node,'NORMAL')
        test_node = bn.getNode('ERRCAUTER')
        x.updateState(test_node, 'FALSE')
        for j in range(N):
            node = rand.choice(Z)
            # if j%100000 == 0 :
            #     print(j)
            # if node == bn.getNode(X):
            #     print('weredointit')
            # print('before', node.name, node.domain)
            # print(node.state)
            # print(node.name, 'here\t\t', node.state)
            x = self.setValue(node, x)
            # print('after', node.state, '\n\n\n\n')
            query = bn.getNode(X)
            count[query.state] += 1
        print(count)
        total = 0
        for key, val in count.items():
            total += val
        for key, val in count.items():
            count[key] = val/total
        print(count, 'normalized')

        pass
