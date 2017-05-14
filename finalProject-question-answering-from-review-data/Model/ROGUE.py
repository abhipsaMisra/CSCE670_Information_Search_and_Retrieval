class roguel:

    def __init__(self, review, question):
        self.pairscore = dict()
        self.review = review
        self.question = question

    # Dynamic Programming implementation of LCS problem
    def lcs(self, X, Y):
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



    def rogueL(self):
        # r = dict()
        for item in self.question:
            # r[item] = list()
            for q in self.question[item]:
                # res = list()
                if item not in self.review:
                    continue
                if item not in self.pairscore:
                    self.pairscore[item] = dict()
                if q["ID"] not in self.pairscore[item]:
                    self.pairscore[item][q["ID"]] = dict()
                for val in self.review[item]:
                    if val["ID"] not in self.pairscore[item][q["ID"]]:
                        self.pairscore[item][q["ID"]][val["ID"]] = dict()
                    self.pairscore[item][q["ID"]][val["ID"]]["ROGUE"] = self.lcs(q["sentence"], val["sentence"])
                    #print "one review done"
                    # r[item].append(res)
        
        return self.pairscore


'''
    value = dict()
    for item in question:
        value[item] = list()
        for q in question[item]:
            res = list()
            for r in review[item]:
                res.append(LCS(["Aa", "B", "Da", "G", "Ha"], ["Aa", "E", "Da", "F", "Ha", "R"]))
            value[item].append(res)'''