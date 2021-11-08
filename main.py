from BayesNet import BayesNet
from ExactInference import ExactInference

def main():
    bn = BayesNet('data/alarm.bif')
    bn.generateList()
    ei = ExactInference()
    ei.variableElimination('HYPOVOLEMIA', {}, bn)

if __name__ == '__main__':
    main()

