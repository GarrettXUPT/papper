
from walsh_and_nonlinearity import walshCompute
from RSBF import initRSBF, finalOribit, TruthTableSelect
from truthTable import AlltruTable

def oneNumStaticGen(varsNum):
    oneNumStatic = {}
    for i in range(varsNum + 1):
        oneNumStatic[i] = 0
    return oneNumStatic

def xiao_messay(varsNum, TruthTable, allTruthTable):
    oneNumStatic = oneNumStaticGen(varsNum)
    for ele in allTruthTable:
        num = ele.count(1)
        oneNumStatic[num] =  oneNumStatic[num] + 1

    walshVec = walshCompute(varsNum, TruthTable)

    zeroVec = []
    len1 = len(walshVec)
    for i in range(len1):
        if walshVec[i] == 0:
            zeroVec.append(i)

    truthTableVec = []
    for ele in zeroVec:
        truthTableVec.append(allTruthTable[ele].count(1))
    # print(oneNumStatic)
    # print(truthTableVec)
    oneNumStatic.pop(0)
    autoDeg = 0
    item = oneNumStatic.items()
    for k, v in item:
        if truthTableVec.count(k) == v:
            autoDeg = k
        else:
            break
    return autoDeg


if __name__ == '__main__':
    varsNum = 8
    # # lst = [6, 7, 8, 9, 10, 14, 16, 17, 18, 19, 20, 22, 24, 25, 26, 32, 34]
    allTruthTable = AlltruTable(varsNum)

    RSST = [3.0, 10.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 21.0, 24.0, 25.0, 26.0, 27.0, 30.0, 34.0]
    # tmp = (sorted(RSST))
    # print(tmp)
    oribit = finalOribit(varsNum)
    dicIndexList = initRSBF(varsNum, RSST, oribit)
    truthTable = TruthTableSelect(varsNum, dicIndexList)
    print(truthTable)
    print(xiao_messay(varsNum, truthTable, allTruthTable))

