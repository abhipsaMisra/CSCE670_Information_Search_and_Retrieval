import os
import json
from collections import defaultdict
import operator

class pageRank:

    def __init__(self):
        self.user_graph = defaultdict(list)
        self.edge_count = 0
        self.data_path = '../data/'
        self.page_rank = defaultdict(list)
        self.page_rank_prev = defaultdict(list)
        self.top_list = defaultdict(list)
        self.inlink_list = defaultdict(list)
        self.result_set = defaultdict(list)

    def generate_graph(self):
        for fname in os.listdir(self.data_path):
            if fname[0] == '.' or fname != 'pagerank.json':
                continue
            path = os.path.join(self.data_path, fname)
            f = open(path, 'r')
            for line in iter(f):
                data = json.loads(line)
                user_parent_id = data['user']['id']
                entities = data['entities']
                if entities is not None:
                    user_mentions = entities['user_mentions']
                    for each_mention in user_mentions:
                        mention_id = each_mention['id']
                        if mention_id != user_parent_id:
                            if user_parent_id not in self.user_graph or mention_id not in self.user_graph[user_parent_id]:
                                self.user_graph[user_parent_id].append(mention_id)
                                if user_parent_id not in self.inlink_list[mention_id]:
                                    self.inlink_list[mention_id].append(user_parent_id)
                            if mention_id not in self.user_graph:
                                self.user_graph[mention_id] = []

                else:
                    if user_parent_id not in self.user_graph:
                        self.user_graph[user_parent_id] = []

            for links in self.user_graph:
                for edges in self.user_graph[links]:
                    self.edge_count += 1

            print ("length user_graph: %s" %len(self.user_graph))
            print ("edge count: %s" %(self.edge_count))

    def generate_page_rank(self):
        count = 0
        d = 0.9
        inlink_list = {}
        flag = True
        count = 0
        while flag:
            for user in self.user_graph:
                if count == 0:
                    self.page_rank[user] = float(1/len(self.user_graph))
                else:
                    inlink_list = self.inlink_list[user]
                    if inlink_list is not None:
                        inlink_sum = 0
                        for each_incoming in inlink_list:
                            inlink_sum += self.page_rank_prev[each_incoming]/len(self.user_graph[each_incoming])
                        self.page_rank[user] = ((1-d)/len(self.user_graph)) + (d*(inlink_sum))
                    else:
                        self.page_rank[user] = ((1 - d) / len(self.user_graph))
                self.page_rank_prev[user] = self.page_rank[user]
            sorted_list = list(reversed(sorted(self.page_rank.items(), key=operator.itemgetter(1))))
            if count == 0 or self.top_list != sorted_list[:10]:
                self.top_list = sorted_list[:10]
            else:
                flag = False
            count += 1
        norm_factor = 0
        for page in self.page_rank:
            norm_factor += self.page_rank[page]
        print ("top 10 list: ")
        for page in self.top_list:
            self.result_set[page[0]] = page[1]/norm_factor
            print ("* %s - %s" %(page[0], self.result_set[page[0]]))
        print ("no of iterations: %s" %count)

p = pageRank()
p.generate_graph()
p.generate_page_rank()
