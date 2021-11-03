from BayesNet import BayesNet

def main():
    bn = BayesNet('data/alarm.bif')
    bn.generateList()

if __name__ == '__main__':
    main()

