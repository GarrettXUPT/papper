import numpy as np
from S_BOX_Transparency import shortTableToLong
import time
from innerproduct import innerProductSelect

'''
    十六进制转化为二进制列表
    return 转化结果
'''
def hexToBinary(hexList):
    ResList = []
    for ele in hexList:
        tmpEle = int(ele, base = 16)   # 将16进制转化为十进制
        binRes = str(bin(tmpEle))[2:]  # 将十进制转化为二进制
        binLen = len(binRes)  # 计算二进制表示的长度
        if binLen < 4:  # 若长度小于4，则补全
            binRes = '0' * (4 - binLen) + binRes
        tmpList = []
        for i in range(0, 4):
            tmpList.append(int(binRes[i]))
        ResList.append(tmpList)
    return ResList


'''
    AES S盒真值表
    :return f0-->f7的真值表组成的列表
'''
def S_BOX_TRUTHTABLE(varsNum, TRUTHTABLE):
    hexTableList =[]
    for ele in TRUTHTABLE:
        hexTableList.append(ele.split(" "))

    binaryListTmp = []
    for ele in hexTableList:
        binaryListTmp.append(hexToBinary(ele))

    binaryList = []
    for ele in binaryListTmp:
        tmpList = []
        for elem in ele:
            for elebinary in elem:
                tmpList.append(int(elebinary))
        binaryList.append(tmpList)
    # print(binaryList[0])

    fTruthTableList = []
    for i in range(varsNum):
        fTruthTableList.append([])

    binLen = len(binaryList)
    for i in range(binLen):
        for j in range(varsNum):
            fTruthTableList[j].append(binaryList[i][varsNum - j - 1])

    return fTruthTableList

'''
    八元乘积
    return:各个情况的乘积结果，共 2 ** (2 ** n) 个
'''
def S_BOX_EightVars_innerProduct(varsNum, resList):
    ResultList = []
    pos = pow(2, varsNum)
    for i in range(pos):
        ResultList.append(resList[0 + i * pow(2, varsNum): pow(2, varsNum) + i * pow(2, varsNum)])
    return ResultList

'''
    数值之间的相乘
    :return:乘积的结果
'''
def multiply(x, w):
    return x * w

'''
    向量间的相乘
    :return:相乘结果向量
'''
def vectorMutiply(vec1, vec2):
    npRes = np.multiply(np.array(vec1), np.array(vec2))
    return npRes.tolist()

'''
    向量间的加法
    :return:加法计算结果向量
'''
def vectorAdd(vec1, vec2):
    npRes = np.add(np.array(vec1), np.array(vec2))
    return npRes.tolist()


'''
    input:theta 由thetaGenerate产生的theta矩阵
    truthtableList 由AES转化而来的真值表矩阵
'''
def multiply_theta_truthTable(varsNum, theta, truthtableList):
    ResLst = []
    pos = pow(2, varsNum)
    for i in range(pos):
        tmpList = []
        for ele in truthtableList:
            tmpList.append(ele[i])
        ResLst.append(vectorMutiply(theta, tmpList))
        # print(ResLst)
    return ResLst

'''
    walsh谱指数部分计算 theta * F + X * W
    :return:返回计算结果
'''
def indexCompute(multiply_theta_truthtable, innerproductRes):
    resList = []
    for inner in innerproductRes:
        tmpList = vectorAdd(inner, multiply_theta_truthtable)
        resList.append(tmpList)
    return resList

'''
    S盒Walsh谱计算
    :return walsh谱向量
'''
def S_Box_Walsh(varsNum, truthTableList, innerRes, thetaList):
    Mul_theta_and_F_ResList = []
    for theta in thetaList:
        Mul_theta_and_F_ResList.append(multiply_theta_truthTable(varsNum,theta, truthTableList))
    # print(Mul_theta_and_F_ResList)

    resList = []
    for ele in Mul_theta_and_F_ResList:
        tmpList = []
        for elem in ele:
            tmpList.append(sum(elem) % 2)
        resList.append(tmpList)


    indexAddList = []
    for mutiply_theta_truthTable in resList:
        indexAddList.append(indexCompute(mutiply_theta_truthTable, innerRes))
    # print(indexAddList)
    WalshTmp = []
    for ele in indexAddList:
        for elem in ele:
            for element in elem:
                if element % 2 == 0:
                    WalshTmp.append(1)
                elif element % 2 == 1:
                    WalshTmp.append(-1)
                else:
                    print("Error")

    WalshTmpList = []
    for i in range(len(WalshTmp) // pow(2, varsNum)):
        WalshTmpList.append(abs(sum(WalshTmp[0 + i * pow(2, varsNum) : pow(2, varsNum) + i * pow(2, varsNum)])))

    WalshVectorList = []
    for i in range(len(WalshTmpList) // pow(2, varsNum)):
        WalshVectorList.append(WalshTmpList[0 + i * pow(2, varsNum) : pow(2, varsNum) + i * pow(2, varsNum)])
    # print(len(WalshVectorList))
    return  WalshVectorList

'''
    S盒非线性度的计算
    :print 打印S盒非线性度
'''
def S_BOX_nolinearityCompte(varsNum, WalshVectorList):
    WalshMaxValueList = []
    for ele in WalshVectorList:
        WalshMaxValueList.append(max(ele))
    WalshMax = max(WalshMaxValueList[1:])
    nolinearity = pow(2, varsNum - 1) - 0.5 * WalshMax
    # print("AES_S_BOX_Nolinearity = ", nolinearity)
    return nolinearity

'''
    非线性度计算主程序
'''
def nonlinearity(varsNum, S_BOX_LIST, AlltruthTable, innerList):
    innerList = S_BOX_EightVars_innerProduct(varsNum, innerList)
    truthTableList = S_BOX_TRUTHTABLE(varsNum, S_BOX_LIST)
    WalshVectorList = S_Box_Walsh(varsNum, truthTableList, innerList, AlltruthTable)
    return S_BOX_nolinearityCompte(varsNum, WalshVectorList)

def translateHex(table):
    if table == [0, 0, 0, 0]:
        return '0'
    elif table == [0,0,0,1]:
        return '1'
    elif table == [0,0,1,0]:
        return '2'
    elif table == [0,0,1,1]:
        return '3'
    elif table == [0,1,0,0]:
        return '4'
    elif table == [0,1,0,1]:
        return '5'
    elif table == [0,1,1,0]:
        return '6'
    elif table == [0,1,1,1]:
        return '7'
    elif table == [1,0,0,0]:
        return '8'
    elif table == [1,0,0,1]:
        return '9'
    elif table == [1,0,1,0]:
        return 'A'
    elif table == [1,0,1,1]:
        return 'B'
    elif table == [1,1,0,0]:
        return 'C'
    elif table == [1,1,0,1]:
        return 'D'
    elif table ==[1,1,1,0]:
        return 'E'
    elif table == [1,1,1,1]:
        return 'F'

def binartToHex(varsNum, SMatrix):
    binTmpList = []
    for i in range(len(SMatrix[0])):
        tmpList = []
        for ele in SMatrix:
            tmpList.append(ele[i])
        tmp1 = translateHex(tmpList[:4])
        tmp2 = translateHex(tmpList[4:])
        tmp = tmp1 + ' ' + tmp2
        binTmpList.append(tmp)
    return binTmpList




if __name__ == '__main__':
    start = time.time()
    table = [128, 199, 143, 172, 158, 42, 216, 26, 188, 12, 84, 68, 177, 16, 52, 114, 248, 65, 24,
            234, 41, 77, 9, 205, 226, 214, 32, 129, 104, 210, 101, 198, 241, 74, 3, 4, 48, 51, 213,
            212, 82, 108, 27, 185, 18, 229, 155, 88, 197, 72, 173, 144, 64, 151, 130, 153, 81, 236,
            165, 201, 75, 98, 141, 39, 227, 150, 21, 13, 6, 34, 8, 57, 96, 181, 102, 230, 171, 192,
            169, 163, 37, 2, 89, 170, 54, 220, 242, 44, 36, 136, 203, 204, 182, 228, 49, 83, 139,
            70, 17, 92, 218, 179, 160, 209, 1, 149, 174, 22, 132, 166, 178, 105, 35, 46, 217, 232,
            202, 11, 147, 116, 23, 180, 69, 58, 154, 29, 78, 0, 127, 73, 19, 47, 38, 110, 94, 30, 76,
            164, 93, 250, 61, 56, 60, 194, 25, 196, 200, 45, 59, 195, 245, 95, 122, 106, 112, 159,
            120, 115, 133, 193, 50, 91, 137, 14, 145, 240, 90, 124, 118, 156, 135, 221, 235, 246,
            63, 253, 117, 175, 85, 243, 97, 219, 190, 244, 113, 125, 103, 167, 138, 247, 131, 66,
            100, 87, 55, 15, 146, 189, 28, 161, 162, 86, 225, 111, 53, 207, 121, 224, 109, 7, 184,
            62, 142, 238, 187, 254, 215, 249, 237, 186, 126, 211, 251, 33, 107, 71, 222, 208, 43,
            119, 231, 176, 67, 31, 183, 191, 252, 157, 233, 80, 99, 168, 123, 152, 79, 223, 206,
            40, 148, 140, 239, 20, 134, 10, 5, 255]
    binartToHex(8, shortTableToLong(8, table))
    end = time.time()
    print(end - start)




