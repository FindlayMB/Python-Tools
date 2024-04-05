import math
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import sys


def laplaceTest(data):
    n = data["FC"]
    k = data["FC"].shape[0]

    u = {}
    cumSum = {1: n[0]}
    cumSum2 = {1: 0}
    for i in range(2, k + 1, 1):
        cumSum[i] = cumSum[i - 1] + n[i - 1]
        cumSum2[i] = cumSum2[i - 1] + (i - 1) * n[i - 1]

    for i in range(1, k + 1, 1):
        u[i] = cumSum2[i] - ((i - 1) / 2) * cumSum[i]
        u[i] = u[i] / math.sqrt((pow(i, 2) - 1) * cumSum[i] / 12)
    u[1] = 0

    plt.plot(u.values())
    plt.ylabel("u(k)")
    plt.xlabel("k")
    plt.title("Failure Count Laplace Trend test")
    plt.grid(visible=True)
    pprint(u)
    plt.show()


def main():
    try:
        filePath = sys.argv[1]
    except:
        print("Must include file path!")
        print("python laplaceTrendTest.py <file path>")
        exit(1)
    if filePath == "":
        print("Filepath is empty, must include file path! ")
        print("Run with:")
        print("python laplaceTrendTest.py <file path>")
        return

    data = np.genfromtxt(
        filePath,
        delimiter=",",
        dtype=np.float32,
        names=True,
        missing_values="Missing",
        filling_values=np.nan,
    )
    if data.dtype.names != ("T", "FC"):
        print("Invalid file format!")
        print(data.dtype.names)
        print("Expected 2 columns named T and FC")
        print("Please reformat data!")
        return

    checkResult = checkForInvalidData(data)
    if checkResult != 0:
        print("Invalid data types")
        print("Both columns T and FC need to be floats")
        match checkResult:
            case 1:
                print("Column T is not of type np.int32")
                print(data["T"].dtype)
            case 2:
                print("Column FC is not of type np.float32")
                print(data["FC"].dtype)
            case 3:
                print("Column T has a missing value")
            case 4:
                print("Column FC has a missing value")
        return
    laplaceTest(data)


def checkForInvalidData(data):
    if data["T"].dtype != np.float32:
        return 1

    if data["FC"].dtype != np.float32:
        return 2

    if np.isnan(data["T"]).any():
        return 3

    if np.isnan(data["FC"]).any():
        return 4

    return 0


if __name__ == "__main__":
    main()
