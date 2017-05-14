'''import py_common_subseq

def LCS(seq1, seq2):
    l1, l2 = list(), list()
    for i in seq1:
        l1.append(str(i))
    for i in seq2:
        l2.append(str(i))
    len = 0
    val = list(py_common_subseq.find_common_subsequences(l1, l2, sep=' '))

    for i in val:
        if i == '':
            continue
        l = 0
        for w in i.split():
            l += 1
        if len < l:
            len = l
    return len

   '''


# Dynamic Programming implementation of LCS problem

def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None] * (n + 1) for i in xrange(m + 1)]

    """Following steps build L[m+1][n+1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]


# end of function lcs



def rogueL(review, question, pairscore):
    # r = dict()
    for item in question:
        # r[item] = list()
        for q in question[item]:
            # res = list()
            if item not in review:
                continue
            if item not in pairscore:
                pairscore[item] = dict()
            if q["ID"] not in pairscore[item]:
                pairscore[item][q["ID"]] = dict()
            for val in review[item]:
                if val["ID"] not in pairscore[item][q["ID"]]:
                    pairscore[item][q["ID"]][val["ID"]] = dict()
                pairscore[item][q["ID"]][val["ID"]]["ROGUE"] = lcs(q["sentence"], val["sentence"])
                #print "one review done"
                # r[item].append(res)
    return pairscore


'''
    value = dict()
    for item in question:
        value[item] = list()
        for q in question[item]:
            res = list()
            for r in review[item]:
                res.append(LCS(["Aa", "B", "Da", "G", "Ha"], ["Aa", "E", "Da", "F", "Ha", "R"]))
            value[item].append(res)'''
# updateReviewID(review)