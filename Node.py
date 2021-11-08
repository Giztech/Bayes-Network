class Node:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.parent = []
        self.originalParents = []
        self.prob = {}
        self.children = []
        self.state = ''
        self.domain_exists = True

    def updateState(self, state):
        self.state = state