from BayesNet import BayesNet
from ExactInference import ExactInference

def main():
    bn = BayesNet('data/alarm.bif')
    bn.generateList()
    node = bn.getNode('CO')
    print(node.name)
    print(node.prob)
    print(node.children)
    print(node.parent)
    ei = ExactInference()
    ei.variableElimination('HYPOVOLEMIA', {'HRBP': 'HIGH', 'CO': 'LOW', 'BP': 'HIGH'}, bn)

if __name__ == '__main__':
    main()

