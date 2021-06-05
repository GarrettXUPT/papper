
from innerproduct import innerProductSelect
import copy
'''
    布尔函数walsh谱的计算
    :return walsh谱向量
'''
def walshCompute(varsNum, truthTable, innerProductRes):
    # print(truthTable)
    walshTmpResList = []
    tmpList = []
    walshResList = []
    len1 = len(innerProductRes)
    for i in range(len1):
        tmpList.append((truthTable[i % len(truthTable)] + innerProductRes[i]) % 2)
    # print(tmpList)
    len2 = len(tmpList)
    for i in range(len2):
            if tmpList[i] == 0:
               walshTmpResList.append(1)
            else:
                walshTmpResList.append(-1)

    len3 = len(truthTable)
    for i in range(len3):
        tmpRes = 0
        for j in range(len3):
            tmpRes = walshTmpResList[j + i * len(truthTable)] + tmpRes
        walshResList.append(tmpRes)

    return walshResList

'''
    布尔函数非线性度的计算
    :return 布尔函数非线性度的值
'''
def nonlinearityCompute(varsNum, truthTable, innerProduct):
    tmpList = []
    walsh = walshCompute(varsNum, truthTable, innerProduct)
    for ele in walsh:
        tmpList.append(abs(ele))
    # print(tmpList)
    return pow(2, varsNum - 1) - 0.5 * max(tmpList)



if __name__ == '__main__':
    pass

