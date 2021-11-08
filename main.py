from BayesNet import BayesNet
from ExactInference import ExactInference

def main():
    bn = BayesNet('data/alarm.bif')
    bn.generateList()
    ei = ExactInference()

    #Alarm

    #Little Evidence
    ei.variableElimination('HYPOVOLEMIA',{'HRBP': 'HIGH', 'CO': 'LOW', 'BP': 'HIGH' } , bn)
    ei.variableElimination('LVFAILURE', {'HRBP': 'HIGH', 'CO': 'LOW', 'BP': 'HIGH'}, bn)
    ei.variableElimination('ERRLOWOUTPUT', {'HRBP': 'HIGH', 'CO': 'LOW', 'BP': 'HIGH'}, bn)

    #Moderate Evidence
    ei.variableElimination('HYPOVOLEMIA', {'HRBP' : 'HIGH', 'CO' : 'LOW', 'BP' : 'HIGH', 'HRSAT' : 'LOW', 'HREKG' : 'LOW', 'HISTORY' :'TRUE'}, bn)
    ei.variableElimination('LVFAILURE', {'HRBP' : 'HIGH', 'CO' : 'LOW', 'BP' : 'HIGH', 'HRSAT' : 'LOW', 'HREKG' : 'LOW', 'HISTORY' :'TRUE'}, bn)
    ei.variableElimination('ERRLOWOUTPUT', {'HRBP' : 'HIGH', 'CO' : 'LOW', 'BP' : 'HIGH', 'HRSAT' : 'LOW', 'HREKG' : 'LOW', 'HISTORY' :'TRUE'}, bn)



    #Child

    bn = BayesNet('data/child.bif')
    bn.generateList()
    ei = ExactInference()

    #Little Evidence
    ei.variableElimination('Disease',{'LowerBodyO2' : '<5','RUQO2' : '>=12', 'CO2Report' : '>=7.5', 'XrayReport' : 'Asy/Patchy'},bn)

    #Moderate Evidence
    ei.variableElimination('Disease',{'LowerBodyO2': '<5', 'RUQO2': '>=12', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy', 'GruntingReport' : 'Yes', 'Age' : '11-30 Days'},bn)

    #Hailfinder

    bn = BayesNet('data/hailfinder.bif')
    bn.generateList()
    ei = ExactInference()

    #Little Evidence

    ei.variableElimination('SatContMoist', {'RSfest' : 'XNIL', 'N32StarFest' : 'XNIL', 'MountainFest' : 'XNIL', 'AreaMoDryAir' : 'VeryWet'}, bn)
    ei.variableElimination('LLIW', {'RSfest' : 'XNIL', 'N32StarFest' : 'XNIL', 'MountainFest' : 'XNIL', 'AreaMoDryAir' : 'VeryWet'}, bn)

    #Moderate Evidence

    ei.variableElimination('SatContMoist',{'RSfest': 'XNIL', 'N32StarFest': 'XNIL', 'MountainFest': 'XNIL', 'AreaMoDryAir': 'VeryWet', 'ComboVerMo' : 'Down', 'AreaMeso_ALS' : 'Down', 'CurPropConv' : 'Strong'},bn)
    ei.variableElimination('LLIW',{'RSfest': 'XNIL', 'N32StarFest': 'XNIL', 'MountainFest': 'XNIL', 'AreaMoDryAir': 'VeryWet','ComboVerMo': 'Down', 'AreaMeso_ALS': 'Down', 'CurPropConv': 'Strong'}, bn)

    #Insurance

    bn = BayesNet('data/insurance.bif')
    bn.generateList()
    ei = ExactInference()

    #Little Evidence

    ei.variableElimination('MedCost', {'Age' : 'Adolescent', 'GoodStudent' : 'False', 'SeniorTrain' : 'False', 'DrivQuality' : 'Poor'},bn)
    ei.variableElimination('ILiCost',{'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor'},bn)
    ei.variableElimination('PropCost',{'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor'},bn)

    #Moderate Evidence

    ei.variableElimination('MedCost',{'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor', 'MakeModel' : 'Luxury', 'CarValue' : 'FiftyThousand','DrivHistory': 'Zero'},bn)
    ei.variableElimination('MedCost',{'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor','MakeModel': 'Luxury', 'CarValue': 'FiftyThousand', 'DrivHistory': 'Zero'}, bn)
    ei.variableElimination('MedCost',{'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor','MakeModel': 'Luxury', 'CarValue': 'FiftyThousand', 'DrivHistory': 'Zero'}, bn)

    #Win95

    bn = BayesNet('data/win95pts.bif')
    bn.generateList()
    ei = ExactInference()



    #Evidence 1

    ei.variableElimination('Problem1', {'Problem1' : 'No_Output'}, bn)
    ei.variableElimination('Problem2', {'Problem1' : 'No_Output'}, bn)
    ei.variableElimination('Problem3', {'Problem1' : 'No_Output'}, bn)
    ei.variableElimination('Problem4', {'Problem1' : 'No_Output'}, bn)
    ei.variableElimination('Problem5', {'Problem1' : 'No_Output'}, bn)
    ei.variableElimination('Problem6', {'Problem1' : 'No_Output'}, bn)

    #Evidence 2

    ei.variableElimination('Problem1', {'Problem2' : 'Too_Long'}, bn)
    ei.variableElimination('Problem2', {'Problem2' : 'Too_Long'}, bn)
    ei.variableElimination('Problem3', {'Problem2' : 'Too_Long'}, bn)
    ei.variableElimination('Problem4', {'Problem2' : 'Too_Long'}, bn)
    ei.variableElimination('Problem5', {'Problem2' : 'Too_Long'}, bn)
    ei.variableElimination('Problem6', {'Problem2' : 'Too_Long'}, bn)

    #Evidence 3

    ei.variableElimination('Problem1', {'Problem3' : 'No'}, bn)
    ei.variableElimination('Problem2', {'Problem3' : 'No'}, bn)
    ei.variableElimination('Problem3', {'Problem3' : 'No'}, bn)
    ei.variableElimination('Problem4', {'Problem3' : 'No'}, bn)
    ei.variableElimination('Problem5', {'Problem3' : 'No'}, bn)
    ei.variableElimination('Problem6', {'Problem3' : 'No'}, bn)

    #Ecidence 4

    ei.variableElimination('Problem1', {'Problem4' : 'No'}, bn)
    ei.variableElimination('Problem2', {'Problem4' : 'No'}, bn)
    ei.variableElimination('Problem3', {'Problem4' : 'No'}, bn)
    ei.variableElimination('Problem4', {'Problem4' : 'No'}, bn)
    ei.variableElimination('Problem5', {'Problem4' : 'No'}, bn)
    ei.variableElimination('Problem6', {'Problem4' : 'No'}, bn)

    #Evidence 5

    ei.variableElimination('Problem1',{'Problem5' : 'No'},bn)
    ei.variableElimination('Problem2',{'Problem5' : 'No'},bn)
    ei.variableElimination('Problem3',{'Problem5' : 'No'},bn)
    ei.variableElimination('Problem4',{'Problem5' : 'No'},bn)
    ei.variableElimination('Problem5',{'Problem5' : 'No'},bn)
    ei.variableElimination('Problem6',{'Problem5' : 'No'},bn)

    #Evidence 6

    ei.variableElimination('Problem1',{'Problem6' : 'Yes'},bn)
    ei.variableElimination('Problem2',{'Problem6' : 'Yes'},bn)
    ei.variableElimination('Problem3',{'Problem6' : 'Yes'},bn)
    ei.variableElimination('Problem4',{'Problem6' : 'Yes'},bn)
    ei.variableElimination('Problem5',{'Problem6' : 'Yes'},bn)
    ei.variableElimination('Problem6',{'Problem6' : 'Yes'},bn)

if __name__ == '__main__':
    main()

