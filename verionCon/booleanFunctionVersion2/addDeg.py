
from RSBF import finalOribit, TruthTableSelect, initRSBF
from truthTable import AlltruTable


def shortTableToLongTable(varsNum, RSTT):
    OribitList = finalOribit(varsNum)
    dicIndexList = initRSBF(varsNum, RSTT, OribitList)
    truthTable = TruthTableSelect(varsNum, dicIndexList, AlltruTable(varsNum))
    return truthTable

def bitBiger(lst1, lst2):
    j = 0
    len1 = len(lst1)
    for i in range(len1):
        if lst1[i] < lst2[j]:
            return False
        j += 1
    return True

def cAlpha(lst1, F2N, longTruthtable):
    ret = 0
    len1 = len(F2N)
    for i in range(len1):
        if bitBiger(lst1, F2N[i]) == True:
            ret = (ret +  longTruthtable[i]) % 2
    return ret

def getDegree(longTable, allInputTable):
    retLst = []
    len1 = len(allInputTable)
    for i in range(len1):
        retLst.append(cAlpha(allInputTable[i], allInputTable, longTable))

    maxdeg = 0
    len2 = len(retLst)
    for i in range(len2):
        if retLst[i] == 1:
           deg = allInputTable[i].count(1)
           if deg > maxdeg:
                maxdeg = deg
    return maxdeg


if __name__ == '__main__':
    varsNum = 8
    st = [3.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 21.0, 23.0, 24.0, 25.0, 26.0, 27.0, 30.0, 31.0, 32.0, 34.0]
    lt = shortTableToLongTable(varsNum, st)
    allTable = AlltruTable(varsNum)
    deg = getDegree(lt, allTable)
    print(deg)

