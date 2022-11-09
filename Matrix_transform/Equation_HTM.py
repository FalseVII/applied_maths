import numpy as np
def printMatrix(data, N):
    for r in range(N):
        print(" "),
        for c in range(N):
            print("{0:0.3f}\t".format(data[r][c]), end=' ')

def printData(data):
    for i in range(data.size):
        print("{0:0.3f}\t".format(data[i]), end=' ')

def  make_kpqTable(N):
    print("k\tp\tq\n0\t0\t0")
    for i in range(1, N):
        p = int(np.fix(np.log2(i)))
        q = int(np.fix((i) - (2 ** p) + 1))
        print("{0}\t{1}\t{2}".format(i, p, q))

def generateMatrix(N):
    make_kpqTable(N)
    print("Generating Matrix for N={0}".format(N))
    haarMatrix = np.zeros((N, N), dtype='float')
    haarMatrix[0, :] = 1 / np.sqrt(N)
    for r in range(1, N):
        p = int(np.fix(np.log2(r)))
        q = (r) - (2 ** p) + 1
        for c in range(0, N):
            z = (c / N)
            if (z >= (q - 1) / (2 ** p)) and (z < (q - 1 / 2) / (2 ** p)):
                haarMatrix[r][c] = (1 / (np.sqrt(N))) * (2 ** (p / 2))
            elif (z >= (q - 1 / 2) / (2 ** p)) and (z < q / (2 ** p)):
                haarMatrix[r][c] = (1 / np.sqrt(N) * (-2 ** (p / 2)))
            else:
                haarMatrix[r][c] = 0.0
    printMatrix(haarMatrix, N)
    return haarMatrix

def RunExample(N, haar):
    print("\n\nGenerating Data")
    data = np.random.randint(1, 100, size=(N))
    printData(data)
    print("\nHaar Decomposition: ")
    decomp = np.matmul(data, haar)
    printData(decomp)
    print("\nHaar Recomposition: ")
    recomp = np.matmul(haar, decomp)
    printData(recomp)

def main(N):
    haar = generateMatrix(N)
    RunExample(N, haar)

if __name__=="__main__":
    print("Haar Test Generate Matrix Transform")
    n = int(input("Enter a integer value for n where n will be used as 2ⁿ: "))
    print("Size of data will be 2^{0} = {1}".format(n, (2 ** n)))
    if (n < 2 or n > 5):
        print("Value for n is incorrect, should be 2\u2265n\u22645")
    else:
        N = 2 ** n
        main(N)
