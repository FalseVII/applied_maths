
import numpy as np


class DCT_Demo(object):
    def __init__(self, level,M_block):
        self.N = 8
        self.n = 8.0
        self.T = np.zeros((self.N, self.N), dtype='float_')
        self.Tt = np.zeros((self.N, self.N), dtype='float_')
        self.DCT = np.zeros((self.N, self.N), dtype='float_')
        self.TM = np.zeros((self.N, self.N), dtype='float_')
        self.R = np.zeros((self.N, self.N), dtype='float_')
        self.Q_Mat = np.zeros((self.N, self.N), dtype='int32')
        self.C = np.zeros((self.N, self.N), dtype='int32')
        self.fin = np.zeros((self.N, self.N), dtype='int32')
        self.Q50 = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                             [12, 12, 14, 19, 26, 58, 60, 55],
                             [14, 13, 16, 24, 40, 57, 69, 56],
                             [14, 17, 22, 29, 51, 87, 80, 62],
                             [18, 22, 37, 56, 68, 109, 103, 77],
                             [24, 35, 55, 64, 81, 104, 113, 92],
                             [49, 64, 78, 87, 103, 121, 120, 101],
                             [72, 92, 95, 98, 112, 100, 103, 99]])
        self.M = np.copy(M_block)

        self.Qlevel = level
        self.Generate_T()
        self.CalculateQ()

    def Calculate_FDCT(self):
        self.TM = np.dot(self.T, self.M)
        self.DCT = np.dot(self.TM, self.Tt)

    def Calculate_IDCT(self):
        self.TM = np.dot(self.Tt, self.R)
        self.fin = np.dot(self.TM, self.T)

    def CalculateQ(self):
        temp = 0
        if self.Qlevel == 50:
            self.Q_Mat = np.copy(self.Q50)
        elif self.Qlevel >= 1 and self.Qlevel < 50:
            for i in range(self.N):
                for j in range(self.N):
                    temp = int(self.Q50[i][j] * (50 / self.Qlevel))
                    if temp > 255:
                        self.Q_Mat[i][j] = 255
                    else:
                        self.Q_Mat[i][j] = temp
        elif self.Qlevel > 50 and self.Qlevel <= 100:
            for i in range(self.N):
                for j in range(self.N):
                    self.Q_Mat[i][j] = int(round(self.Q50[i][j] * ((100 - float(self.Qlevel)) / 50)))
        else:
            print("Invalid Argument")
        self.printMatrix(self.Q_Mat, 1)

    def Generate_T(self):
        for i in range(self.N):
            for j in range(self.N):
                if i == 0:
                    self.T[i][j] = 1 / np.sqrt(self.n)
                else:
                    self.T[i][j] = np.sqrt(2 / self.n) * np.cos(((2 * j + 1) * i * np.pi) / (2 * self.n))
                self.Tt[j][i] = self.T[i][j]

    def printMatrix(self, npArray, type):
        if type == 1:
            for i in range(self.N):
                for j in range(self.N):
                    print("{0}".format(npArray[i][j]), end=' ')
                print(" ")
        else:
            for i in range(self.N):
                for j in range(self.N):
                    print("{0:0.3f}".format(npArray[i][j]), end='')
                print()

    def QuantizationStepForward(self):
        self.C = np.divide(self.DCT, self.Q_Mat)

    def QuantizationStepInverse(self):
        self.R = np.multiply(self.C, self.Q_Mat)

    def Compare(self):
        dif = np.abs(np.subtract(self.M, self.fin))
        print("Difference between original and reconstructed matrix")
        self.printMatrix(dif, 1)
