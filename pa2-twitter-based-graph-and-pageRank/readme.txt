PART 1:

In this assignment, we're going to adapt the classic PageRank approach to allow us to find not the most authoritative web pages, but rather to find significant Twitter users. So, instead of viewing the world as web pages with hyperlinks (where pages = nodes, hyperlinks = edges), we're going to construct a graph of Twitter users and their mentions of other Twitter users (so user = node, mention of another user = edge). Over this Twitter-user graph, we can apply the PageRank approach to order the users. The main idea is that a user who is mentioned by other users is more "impactful".

Here is a toy example. Suppose you are given the following four tweets:
userID: diane, text: "@bob Howdy!"
userID: charlie, text: "Welcome @bob and @alice!"
userID: bob, text: "Hi @charlie and @alice!"
userID: alice, text: "Howdy!"

There are four short tweets generated by four users. The @mentions between users form a directed graph with four nodes and five edges. E.g., the "diane" node has a directed edge to the "bob" node. Note that a retweet also contain the "@", so it should be counted as a mention as well.

You should build a graph by parsing the tweets in the file we provide called pagerank.json.

Notes:

* The edges are binary and directed. If Bob mentions Alice once, in 10 tweets, or 10 times in one tweet, there is an edge from Bob to Alice, but there is not an edge from Alice to Bob.
* If a user mentions herself, ignore it.
* Correctly parsing @mentions in a tweet is error-prone. Use the entities field.

Compile and Run:
Clone the src and data folders, navigate to src folder and run 
Python pageRank.py

Output:
The size of user graph, i.e. no of nodes and no of edges

-------------------------

PART 2:

Your program will return the top 10 users with highest PageRank scores. The output should be like:

user1 - score1
user2 - score2
...
user10 - score10

You should follow these rules:

* Assume all nodes start out with equal probability.
* The probability of the random surfer teleporting is 0.1 (that is, the damping factor is 0.9).
* If a user is never mentioned and does not mention anyone, their PageRank scores should be zero. Do not include the user in the calculation.

Compile and Run:
Clone the src and data folders, navigate to src folder and run 
Python pageRank.py

Output:
The top 10 mention list