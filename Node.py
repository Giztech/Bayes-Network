class Node:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.parent = []
        self.prob = {}
        self.children = []
