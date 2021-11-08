from BayesNet import BayesNet
from ExactInference import ExactInference

def main():
    bn = BayesNet('data/child.bif')
    bn.generateList()
    print(bn.getNode('ChestXray').parent)
    ei = ExactInference()
    ei.variableElimination('Disease', {"LowerBodyO2": "<5", "RUQO2": ">=12", "CO2Report": ">=7.5", "XrayReport": "Asy/Patchy", "GruntingReport": "Yes", "LVHReport": "Yes", "Age": "11-30_days"}, bn)

if __name__ == '__main__':
    main()

