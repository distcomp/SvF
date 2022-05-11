def testYield():
    yield "one"
    yield  "two"
    yield  "tree"


if __name__ == "__main__":
    # print(str(testYield()))
    # print(str(testYield()))
    l = testYield()
    for s in testYield():
        print(s)