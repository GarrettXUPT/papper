
import time, copy
from addDeg import getDegree
from truthTable import AlltruTable

def XOR(ele1, ele2):
    return (ele1 + ele2) % 2


def vectorXOR(vec1, vec2):
    resLst = []
    len1 = len(vec1)
    for i in range(len1):
        resLst.append(XOR(vec1[i], vec2[i]))
    return resLst

def vectorXORes(vec1, vec2):
    res = 0
    len1 = len(vec1)
    for i in range(len1):
        tmp = XOR(vec1[i], vec2[i])
        if tmp == 0:
            res += 1
        elif tmp == 1:
            res -= 1
        else:
            print("value error")
    return res


def firstTerm(truthTable1):
    return truthTable1


def truthTableDicGen(truthTable, alltruthTable):
    truthTableDic = {}
    len1 = len(alltruthTable)
    for i in range(len1):
        truthTableDic[str(alltruthTable[i])] = truthTable[i]
    return truthTableDic


def secondTerm(truthTable2, alltruthTable, truthTableXOR):
    truthTableDic = truthTableDicGen(truthTable2, alltruthTable)
    putLst = []
    len1 = len(alltruthTable)
    for i in range(len1):
        putLst.append(truthTableDic[str(truthTableXOR[i])])
    return putLst


def correlation(truthTable1, truthTable2, alltruthTable, truthTableXOR):
    first = firstTerm(truthTable1)
    second = secondTerm(truthTable2, alltruthTable, truthTableXOR)
    res = vectorXORes(first, second)
    return res


def betaOp(beta):
    resLst = []
    for ele in beta:
        for elem in beta:
            if XOR(ele, elem) == 1:
                resLst.append(-1)
            elif XOR(ele, elem) == 0:
                resLst.append(1)
    return resLst



def sumTermRTO(beta, SMatrix, alltruthTable, truthTableXOR):
    sumRes = 0
    len1 = len(SMatrix)
    for i in range(len1):
        for j in range(len1):
            sumRes += (correlation(SMatrix[i], SMatrix[j], alltruthTable, truthTableXOR) * beta[i * len(SMatrix) + j])
    return abs(sumRes)


def sumTermMTO(beta, SMatrix, alltruthTable, truthTableXOR):
    sumRes = 0
    len1 = len(SMatrix)
    for i in range(len1):
        sumTerm = 0
        for j in range(len1):
            sumTerm += (correlation(SMatrix[i], SMatrix[j], alltruthTable, truthTableXOR) * beta[i * len(SMatrix) + j])
        sumRes += abs((sumTerm))
    return sumRes


def revisedTO(varsNum, SMatrix):
    truthTableXOR = []
    allTruthtable = AlltruTable(varsNum)

    for ele in allTruthtable[1:]:
        tmpList = []
        for elem in allTruthtable:
            tmpList.append((vectorXOR(ele, elem)))
        truthTableXOR.append((tmpList))

    betaList = []
    for ele in allTruthtable:
        betaList.append(betaOp(ele))

    maxValue = 0
    len1 = len(allTruthtable)
    len2 = len(allTruthtable[1:])
    for j in (range(len1)):
        sumTerm = 0
        for i in range(len2):
            sumTerm += (sumTermRTO(betaList[j], SMatrix, allTruthtable, truthTableXOR[i]))
        tmpValue = (varsNum - ((1 / ((pow(2, 2 * varsNum) - pow(2, varsNum)))) * sumTerm))
        if  tmpValue > maxValue:
            maxValue = tmpValue

    return maxValue



def modifyMTO(varsNum, SMatrix):
    truthTableXOR = []
    allTruthtable = AlltruTable(varsNum)

    for ele in allTruthtable[1:]:
        tmpList = []
        for elem in allTruthtable:
            tmpList.append((vectorXOR(ele, elem)))
        truthTableXOR.append((tmpList))

    betaList = []
    for ele in allTruthtable:
        betaList.append(betaOp(ele))
    len1 = len(allTruthtable)
    len2 = len(allTruthtable[1:])
    maxValue = 0
    for j in (range(len1)):
        sumTerm = 0
        for i in range(len2):
            sumTerm += sumTermMTO(betaList[j], SMatrix, allTruthtable, truthTableXOR[i])
        tmpValue = (varsNum - ((1 / ((pow(2, 2 * varsNum) - pow(2, varsNum)))) * sumTerm))
        if tmpValue > maxValue:
            maxValue = tmpValue

    return maxValue



def shortTableToLong(varsNum, shortTable):
    '''
        数字转字符串
    '''
    shortTableStr = []
    for ele in shortTable:
        shortTableStr.append(str(ele))

    '''
        短表转二进制
    '''
    binLst = []
    for ele in shortTableStr:
        tmp = bin(int(ele))[2 : ]
        if len(tmp) != varsNum:
            tmpLen = varsNum - len(tmp)
            for i in range(tmpLen):
                tmp = '0' + tmp
        binLst.append(tmp)

    truthTableLst = []
    for i in range(varsNum):
        tmpLst = []
        for ele in binLst:
            tmpLst.append(int(ele[i]))
        truthTableLst.append(tmpLst)

    return truthTableLst


def boxDegree(varsNum, SMatrix):
    SMatrix = shortTableToLong(varsNum, SMatrix)
    alltruthTable = AlltruTable(varsNum)
    degMin = varsNum
    for ele in SMatrix:
        deg = getDegree(ele, alltruthTable)
        if deg < degMin:
            degMin = deg
    return degMin

if __name__ == '__main__':
    # table = [0, 1, 2, 35, 4, 26, 38, 34, 8, 22, 21, 3, 44, 12, 36, 54, 16, 49, 13, 33, 11, 17, 6, 43, 56,
    #     48, 24, 53, 40, 58, 45, 32, 63, 42, 52, 62, 41, 28, 61, 60, 50, 7, 25, 18, 59, 10, 57, 29,
    #     37, 47, 14, 46, 19, 9, 5, 30, 55, 39, 20, 15, 51, 23, 27, 31]
    table = [
        0, 10, 20, 56, 40, 31, 49, 3, 17, 27, 62, 23, 35, 1, 6, 57, 34, 55, 54, 16, 61, 21, 46, 52, 7, 58, 2, 9, 12, 19,
        51, 25, 5, 28, 47, 33, 45, 43, 32, 60, 59, 8, 42, 26, 29, 36, 41, 44, 14, 48, 53, 30, 4, 13, 18, 22, 24, 15, 38,
        11, 39, 37, 50, 63
             ]
    # table = [13, 7, 3, 2, 9, 10, 12, 1, 15, 4, 5, 14, 6, 0, 11, 8]
    varsNum = 6
    boxDegree(varsNum, table)
    SMatrix = shortTableToLong((varsNum), table)

    start = time.time()
    print(revisedTO(varsNum, SMatrix))
    end = time.time()
    print("the during time is ", end - start)

    start1 = time.time()
    print(modifyMTO(varsNum, SMatrix))
    end1 = time.time()
    print("the during time is", end1 - start1)




