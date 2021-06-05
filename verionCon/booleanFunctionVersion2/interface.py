'''
    Author: shiyu
    Created Time: 2021年4月27日17:35:33
    version：2.0
'''
import time, copy
from addDeg import getDegree
from truthTable import AlltruTable
from innerproduct import innerProductSelect
from xiao_massey import xiao_messay
from transparency import transparencyCompute
from autocorrelation import maxAbsolute
from differentialUniform import uniform
from S_Box_nonlinearity import nonlinearity, binartToHex
from S_BOX_Transparency import modifyMTO, shortTableToLong, revisedTO, boxDegree, vectorXOR
from nonAbsoluteIndicator import non_absolute_indicatorSelect
from RSBF import finalOribit, initRSBF, TruthTableSelect, nonlinearityCompute
from judge import longTableToTable, trans, isRotationSymmetric

class BooleanFunction:
    AlltruthTable = []
    OribitList = []
    innerList = []
    midProcess = []
    ToMid = []

    def __init__(self, varsNum, shortTable = None, longTable = None, S_BOX_Table = None,):
        self.varsNum = varsNum
        self.shortTable = shortTable
        self.longTable = longTable
        self.S_BOX_Table = S_BOX_Table
        self.setTruthTable()
        self.setInnerList()
        self.setOribit()
        if self.S_BOX_Table != None:
            self.setToMid()
        if shortTable != None or longTable != None:
            self.setMidProcess()

        if S_BOX_Table == None and longTable == None and shortTable == None:
            print("无真值表输入")


    def setMidProcess(self):
        self.midProcess = self.__midProcess()


    def setToMid(self):
        for ele in self.AlltruthTable:
            tmpList = []
            for elem in self.AlltruthTable:
                tmpList.append((vectorXOR(ele, elem)))
            self.ToMid.append(copy.deepcopy(tmpList))

    def setTruthTable(self):
        self.AlltruthTable = self.__alltruthTable()


    def setInnerList(self):
        self.innerList = self.__innerProduct()


    def setOribit(self):
        self.OribitList = self.__allOribit()


    def __alltruthTable(self):
        return AlltruTable(self.varsNum)


    def __innerProduct(self):
        return innerProductSelect(self.AlltruthTable)


    def __allOribit(self):
        return finalOribit(self.varsNum, self.AlltruthTable)


    def __midProcess(self):
        if self.longTable != None:
            truthTable = longTableToTable(self.longTable)
            dicIndexList = trans(self.varsNum, truthTable, self.AlltruthTable)
            return truthTable, dicIndexList
        else:
            dicIndexList = initRSBF(self.varsNum, self.shortTable, self.OribitList)
            truthTable = TruthTableSelect(self.varsNum, dicIndexList, self.AlltruthTable)
            return truthTable, dicIndexList


    def oribitCount(self):
        return len(self.__allOribit())


    def nonliearity(self):
        midRes = self.midProcess
        return nonlinearityCompute(self.varsNum, midRes[0], self.innerList)


    def transparency(self):
        midRes = self.midProcess
        return transparencyCompute(self.varsNum, midRes[0], midRes[1], self.AlltruthTable)


    def nonlinearityAndTransparency(self):
        midRes = self.midProcess
        return nonlinearityCompute(self.varsNum, midRes[0], self.innerList), \
               transparencyCompute(self.varsNum, midRes[0], midRes[1], self.AlltruthTable)


    def S_Box_Nonlinearity(self):
        return nonlinearity(self.varsNum, binartToHex(self.varsNum, shortTableToLong(self.varsNum, self.S_BOX_Table)), self.AlltruthTable, self.innerList)


    def S_BOX_MTO(self):
        return modifyMTO(self.varsNum, shortTableToLong(self.varsNum, self.S_BOX_Table))


    def S_BOX_RTO(self):
        return revisedTO(self.varsNum, shortTableToLong(self.varsNum, self.S_BOX_Table))


    def autoCorrelationMaxAbsolute(self):
        return maxAbsolute(self.varsNum, self.S_BOX_Table, self.AlltruthTable)


    def isRotationSymmetric(self):
        truthTable, indexList = self.midProcess
        return isRotationSymmetric(self.varsNum, truthTable, self.AlltruthTable, self.OribitList)

    def nonAbsoluteIndictor(self):
        truthTable, indexList = self.midProcess
        return non_absolute_indicatorSelect(self.varsNum, truthTable, indexList)


    def relisentCompute(self):
        if self.isBalanced():
            truthTable, indexList = self.midProcess
            return xiao_messay(self.varsNum, truthTable, self.AlltruthTable, self.innerList)
        else:
            print("this is a unBalanced function")


    def degree(self):
        truthTable, indexList = self.midProcess
        return getDegree(truthTable, self.AlltruthTable)


    def differentialUniformValue(self):
        return uniform(self.varsNum, self.S_BOX_Table, self.AlltruthTable)


    def sBoxDegree(self):
        return boxDegree(self.varsNum, self.S_BOX_Table, self.AlltruthTable)


    def isBalanced(self):
        if self.midProcess[0].count(1)  == pow(2, self.varsNum - 1):
            return "balanced function"
        else:
            return "unbalanced function"


if __name__ == '__main__':
    '''
        短表使用
    '''
    varsNum = 9
    shortTable = [3, 6, 7, 9, 16, 17, 18, 19, 22, 25, 26, 27, 29, 31, 32, 35, 38, 40, 41, 42, 46, 47, 49, 50, 51, 53, 55, 59, 60]
    bf = BooleanFunction(varsNum, shortTable=shortTable)
    print(bf.nonlinearityAndTransparency())
    print(bf.isRotationSymmetric())
    print(bf.isBalanced())
    print(bf.relisentCompute())
    print(bf.degree())
    print(bf.nonliearity())
    print(bf.transparency())


    '''
        长表使用
    '''
    varsNum = 10
    longTable = "FAD9A6878D2C806F81B609B185446CBBC1068F3D51C3DE53803674607CF08BDAA553107C95AE1EE26356B11FA3AD664EC0511B6D7A706D152EE1AE50849BE6D8CD23320B16153AA59237D9ED06E8EC1C3D4E72689E5713AA8D5BCCB7292C25ACB141674347DB28A67AC86F503DA7123259B9BD02C8BC7344D57086DAFC2CE280"
    bf = BooleanFunction(varsNum, longTable=longTable)
    print(bf.nonlinearityAndTransparency())
    print(bf.isRotationSymmetric())
    print(bf.isBalanced())
    print(bf.nonAbsoluteIndictor())
    print(bf.relisentCompute())
    print(bf.degree())


    '''
        S盒使用
    '''

    varsNum = 8
    table2 = [69, 82, 172, 84, 3, 4, 188, 93, 88, 52, 252, 246, 251, 135, 213, 152, 27, 169, 165,
                102, 67, 214, 244, 137, 231, 49, 161, 109, 139, 147, 32, 209, 125, 73, 205, 58, 106,
                30, 143, 41, 224, 163, 85, 189, 158, 193, 108, 220, 184, 215, 182, 111, 16, 64, 140,
                185, 6, 218, 35, 87, 39, 14, 241, 38, 116, 157, 240, 154, 174, 136, 104, 43, 40, 166,
                179, 197, 124, 103, 78, 155, 28, 181, 0, 21, 8, 113, 79, 92, 48, 47, 9, 44, 56, 10,
                226, 151, 129, 159, 225, 119, 76, 62, 230, 175, 126, 253, 138, 236, 162, 160, 53,
                107, 150, 149, 242, 101, 249, 191, 24, 5, 131, 73, 75, 60, 80, 207, 55, 11, 29, 248,
                238, 33, 228, 117, 74, 86, 105, 45, 216, 148, 66, 110, 36, 20, 250, 23, 180, 121,
                130, 194, 119, 99, 192, 171, 59, 232, 243, 208, 254, 127, 217, 210, 146, 202, 134,
                50, 176, 90, 91, 63, 211, 112, 67, 255, 97, 222, 223, 145, 94, 54, 239, 13, 128, 95,
                2, 144, 49, 19, 118, 96, 89, 64, 177, 234, 132, 122, 168, 25, 195, 227, 153, 77, 18,
              22, 12, 183, 221, 233, 170, 42, 247, 200, 178, 190, 187, 114, 206, 212, 164, 15, 17,
              229, 156, 1, 237, 201, 51, 100, 142, 245, 81, 203, 141, 34, 37, 173, 167, 46, 72,
              199, 219, 31, 87, 204, 61, 235, 120, 186, 198, 7, 196, 70, 123, 26, 133, 98
              ]

    # table2 = [255, 73, 146, 195, 5, 217, 148, 205, 74, 67, 194, 154, 9, 107, 27, 82, 148, 137, 132,
    #         233, 71, 213, 103, 3, 66, 245, 210, 234, 54, 147, 44, 249, 41, 104, 51, 159, 13, 36,
    #         219, 147, 142, 129, 251, 18, 107, 103, 2, 22, 53, 222, 225, 116, 173, 199, 213, 85,
    #         108, 156, 38, 178, 88, 60, 243, 112, 82, 116, 144, 218, 98, 125, 191, 204, 18, 10,
    #         144, 217, 167, 241, 39, 14, 29, 95, 128, 124, 247, 26, 4, 110, 214, 48, 206, 169,
    #         4, 184, 44, 188, 104, 95, 29, 93, 211, 64, 136, 70, 91, 59, 143, 39, 171, 128, 138,
    #         55, 216, 48, 121, 84, 220, 226, 100, 119, 184, 60, 112, 25, 231, 178, 224, 190, 166,
    #         160, 184, 198, 33, 109, 180, 41, 76, 244, 254, 129, 126, 116, 25, 252, 48, 207, 4,
    #         203, 32, 1, 179, 11, 79, 35, 98, 160, 94, 25, 28, 56, 58, 46, 191, 103, 133, 76, 250,
    #         39, 239, 62, 247, 39, 8, 95, 92, 90, 169, 172, 32, 35, 157, 242, 127, 155, 8, 42, 113,
    #         187, 88, 220, 105, 159, 146, 99, 246, 212, 123, 64, 170, 252, 229, 228, 129, 133,
    #         213, 113, 140, 28, 150, 49, 78, 195, 31, 171, 203, 47, 87, 145, 73, 197, 21, 253, 46,
    #         175, 177, 234, 96, 63, 242, 194, 234, 78, 157, 193, 205, 151, 160, 230, 238, 199,
    #         101, 156, 33, 7, 240, 10, 115, 251, 239, 129, 165, 245, 195, 158, 79, 16]

    print(len(set(table2)))
    bf = BooleanFunction(varsNum, S_BOX_Table=table2)
    start = time.time()
    print(bf.S_Box_Nonlinearity())
    end = time.time()
    print("the during time_nonlinearity is ", end - start)
    #
    start = time.time()
    print(bf.autoCorrelationMaxAbsolute())
    end = time.time()
    print("the during time_absolute_value is ", end - start)
    
    start = time.time()
    print(bf.differentialUniformValue())
    end = time.time()
    print("the during time_duf is ", end - start)
    
    start = time.time()
    print(bf.sBoxDegree())
    end = time.time()
    print("the during time_degree is ", end - start)


    # start = time.time()
    # print(bf.S_BOX_MTO())
    # end = time.time()
    # print("the during time_MTO is", end - start)
    #
    # start = time.time()
    # print(bf.S_BOX_RTO())
    # end = time.time()
    # print("the during time_rto is ", end - start)
    #
    # makeSence("matrix.txt")

#
