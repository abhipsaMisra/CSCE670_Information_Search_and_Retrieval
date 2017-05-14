PART 1:
Tokenize documents using whitespaces and punctuations as delimiters but do not remove stop words. Your parser needs to also provide the following two confgiuration options:
Case-folding
Stemming - use nltk Porter stemmer

Compile and Run:
Place the code and southpark_scripts folder in the same path and run 
Python tokenization.py

Output:
(int) - No of tokens generated

# 4 cases considered: 
Stemming + Casefolding
Stemming + No Casefolding
No Stemming + Casefolding
No Stemming + No Casefolding
---------

PART 2:
Build an inverted index to support Boolean retrieval. We only require your index to support AND queries. In other words, your index does not have to support OR, NOT, or parentheses. Also, we do not explicitly expect to see AND in queries, e.g., when we query great again, your search engine should treat it as great AND again.

Compile and Run:
Place the code and southpark_scripts folder in the same path and run 
Python indexing.py

Output:
prints a result set of document IDs containing the search term
---------

PART 3:
Support queries over an index that you build. This time you will use the vector space model plus cosine similarity to rank documents. We will  rank all the 277 documents but only need to output the top-5 documents (i.e. document ids) plus the cosine score of each of these documents.

Compile and Run:
Place the code and southpark_scripts folder in the same path and run 
Python ranking.py

Output: (format)
result1 - score1
result2 - score2
result3 - score3
result4 - score4
result5 - score5
