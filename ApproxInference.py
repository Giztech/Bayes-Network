import random as rand


class ApproxInference:
    def __init__(self):
        pass

    def get_markov_blanket(self, X, bn):

        markov_list = []
        node = X

        # get the children of the selected node
        # since we look for the children's parents and the node's parents while looking at their
        # probabilities, we don't need to add them to the blanket initially

        for child in node.children:
            markov_list.append(child)
        return markov_list

    '''
    sets the initial values of the bayesian network by starting at the top node
    and setting the state based on the probability provided
    the non-root nodes are set based on the states of it's parents 
    and the probabilities provided
    '''
    def forwardSampling(self, evidence, bn):
        # print('forward sampling')
        # if the node is evidence, we want to set it first!
        for node in bn.nodes:
            for key, val in evidence.items():
                if key == node.name:
                    if val in node.domain:
                        node.state = val
                        # print('evidence', node.name, node.state)
                    else:
                        # if the val is not in node domain, the evidence was typed in wrong
                        print(val)
                        print('evidence is not in the correct format. please try again')
        # after setting the evidence, go through and set the rest of the states with forward elimination
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
                    # if the node has parents, we have to
                    problist, keylist = self.getProb(parents, node, bn)
                    bn = self.updateState(node, problist, keylist, bn)
        # print('end of forward sampling\n\n')
        return bn

    '''
    called when the node's parents need to have their states set
    used only for forward sampling
    '''
    def setParent(self, m, bn):
        # print('parent', m.name)
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
        # print('update state', node.name)
        value = rand.random()
        for y in range(len(problist)):
            if y == 0:
                # if the random value is less than the first probability num
                if value < problist[y]:
                    bn.updateState(node, keylist[y])
                    return bn
                else:
                    continue
            # the current value to be looking at should be the previous probability plus the current probability
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
                # print('set parent of', node.name)
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
        # print('set value')
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
            # to deal with parents (who are in the markov blanket)
            else:
                for par in node.parent:
                    parlist += bn.getNode(par).state + ', '
                    # print(par)
                parlist = parlist[:-2]

                for key, val in node.prob.items():
                    if parlist == key:
                        problist.append(val[d])

            # to get the probabilities of the children of the markov blanket
            for name in mb:
                mbnode = bn.getNode(name)
                # print(name)

                parlist = ''
                for par in mbnode.parent:
                    parlist += bn.getNode(par).state + ', '
                parlist = parlist[:-2]


                keylist = []
                for key,val in mbnode.prob.items():
                    if parlist == key:
                        for d1 in mbnode.domain:
                            if d1 == mbnode.state:
                                problist.append(val[d1])
                        # problist.append(val)
                        # keylist.append(key)
            mult = 1.0000000000
            for p in problist:
                mult *= p
            total_prob.append(mult)

        calc_prob = []
        total = 0

        # normalizing
        for m in total_prob:
            total += m
        if total == 0:
            # print('total is 0 normalizing', node.name)
            for m in total_prob:
                # if the probablility of all the domains equate to 0, set the probabilities of each state to be equal
                calc_prob.append(1/len(total_prob))
        else:
            for m in total_prob:
                calc_prob.append(m / total)
        # print(calc_prob)
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


        for j in range(N):
            node = rand.choice(Z)
            # print('node chosen', node.name, 'node state', node.state)
            x = self.setValue(node, x)
            # print('new state', node.state, '\n\n')
            # print('after', node.state, '\n\n\n\n')
            query = bn.getNode(X)
            count[query.state] += 1
        #
        # print(count)
        # # to normalize count
        total = 0
        for key, val in count.items():
            total += val
        for key, val in count.items():
            count[key] = val/total
        print(count, 'normalized')

        pass
