import random as rand


class ApproxInference:
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

    def forwardSampling(self, X, evidence, bn):
        for node in bn.nodes:
            # print('node', node.name)
            if node.state == '':
                parents = node.parent
                for p in parents:
                    parNode = bn.getNode(p)
                    if parNode.state == '':
                        bn = self.setParent(parNode, bn)

        return bn

    def setParent(self, m, bn):
        gms = m.parent
        if len(gms) == 0:
            # if this parent has no parents, then we can just set it based on the probability given
            problist = []
            keylist = []
            for key, val in m.prob.items():
                problist.append(float(val))
                keylist.append(key)
            value = rand.random()

            for y in range(len(problist)):
                if y == 0:
                    # if the random value is less than the first probability num
                    if value < problist[y]:
                        bn.updateState(m, keylist[y])
                        return bn
                    else:
                        continue
                # the current value to be looking at should be the previous prbability plus the current probability
                problist[y] += problist[y-1]
                if value < problist[y]:
                    bn.updateState(m, keylist[y])
                    return bn

        for g in gms:
            gnode = bn.getNode(g)
            if gnode.state == '':
                bn = self.setParent(gnode, bn)
        #state = # do calculation to set the state
        # bn.updateState(m, state)
            # if the node's parents are set
            # self.setParent(gm, bn)
            # calculate probability of node m since it's parent is already set
        return bn
    def gibbsSampling(self, X, evidence, bn, N):

        count = []
        Z = [var for var in bn.nodes if var not in evidence]
        x = evidence

        # random choice each domain of a node then set it
        # forward sampling to set the initial values for bn
        bn = self.forwardSampling(X, evidence, bn)

        # for node in bn.nodes:
        #
        #         print(node.state)

        for j in range(N):
            for node in bn.nodes:
                pass



        pass
