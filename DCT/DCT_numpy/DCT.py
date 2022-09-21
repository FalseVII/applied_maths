import random
import numpy as np

class DCT_Demo(object):
    def __init__(self, level):
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

        self.M = np.array([[16, 8, 23, 16, 5, 14, 7, 22],
                           [20, 14, 22, 7, 14, 22, 24, 6],
                           [15, 23, 24, 23, 9, 6, 6, 20],
                           [14, 8, 11, 14, 12, 12, 25, 10],
                           [10, 9, 11, 9, 13, 19, 5, 17],
                           [8, 22, 20, 15, 12, 8, 22, 17],
                           [24, 22, 17, 12, 18, 11, 23, 14],
                           [21, 25, 15, 16, 23, 14, 22, 22]])

        self.Qlevel = level
        self.Generate_T()
        self.CalculateQ()

    def Generate_T(self):
            for i in range(self.N):
                for j in range(self.N):
                    if i == 0:
                        self.T[i][j] = 1 / np.sqrt(self.n)
                    else:
                        self.T[i][j] = np.sqrt(2 / self.n) * np.cos(((2 * j + 1) * i * np.pi) / (2 * self.n))
                self.Tt[j][i] = self.T[i][j]


            self.Tt = self.T.transpose()
    def Calculate_FDCT(self):
            self.DCT = np.dot(np.dot(self.T, self.M), self.Tt)
    def Calculate_IDCT(self):
            self.fin = np.dot(np.dot(self.Tt, self.R), self.T)

    def CalculateQ(self):
        for i in range(self.N):
            for j in range(self.N):
                self.Q_Mat[i][j] = self.Q50[i][j] * self.Qlevel
    def printMatrix(self, npArray, type):
        if type == 1:
            for i in range(self.N):
                for j in range(self.N):
                    print("{0:4d}".format(npArray[i][j]), end='')
                print()
        else:
            for i in range(self.N):
                for j in range(self.N):
                    print("{0:4.2f}".format(npArray[i][j]), end='')
                print()
    def QuantizationStepForward(self):
        for i in range(self.N):
            for j in range(self.N):
                self.C[i][j] = round(self.DCT[i][j]/self.Q_Mat[i][j])
    def QuantizationStepInverse(self):
        for i in range(self.N):
            for j in range(self.N):
                self.fin[i][j] = self.C[i][j]*self.Q_Mat[i][j]
    def Compare(self):
        for i in range(self.N):
            for j in range(self.N):
                if self.fin[i][j] != self.R[i][j]:
                    print("Error")
                    return
        print("Success")