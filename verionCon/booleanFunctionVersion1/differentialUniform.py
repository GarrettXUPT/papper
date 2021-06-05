
from truthTable import AlltruTable
from autocorrelation import boxMidOp
from S_BOX_Transparency import shortTableToLong

def uniform(varsNum, SMatix):
    SMatix = shortTableToLong(varsNum, SMatix)
    alltruthTable = AlltruTable(varsNum)
    midOpRes = boxMidOp(SMatix, alltruthTable)
    countList = []

    for element in alltruthTable:
        for ele in midOpRes:
            count = 0
            for i in range(len(ele[0])):
                tmpList = []
                for j in range(len(ele)):
                    tmpList.append(ele[j][i])
                if tmpList == element:
                        count += 1
            countList.append(count)
    return max(countList)


if __name__ == '__main__':
    table = [
        69, 82, 172, 84, 3, 4, 188, 93, 88, 52, 252, 246, 251, 135, 213, 152, 27, 169, 165,
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
    print(uniform(8, shortTableToLong(8, table)))