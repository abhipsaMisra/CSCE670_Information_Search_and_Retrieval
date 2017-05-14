# To populate dictionary
import itertools

class reviews:
    def __init__(self, filename, question, data, count):
        self.rev = set()
        self.review = dict()
        self.file = filename
        self.count = count
        self.data = data
        self.question = question
    
    # handling review part here
    def make_review(self):
        # opening Review data file from amazon data
        with open(self.file) as fp:
            for line in itertools.islice(fp, 1, 10000):
                words = line.split()
                # if there is no questions for product, not considering reviews
                if len(words) == 0 or words[1] not in self.question:
                    continue
                if words[0] in self.rev:
                    continue
    
                self.rev.add(words[0])
                # If product Id is not present in review
                if words[1] not in self.review:
                    self.review[words[1]] = list()
                # considering each review
                freq = dict()
                # words in review
                freq["words"] = dict()
                # Id correpsond to all words in sequence in a review for Rogue
                freq["sentence"] = list()
                freq["actual_sen"] = ""
                # Review id
                freq["ID"] = words[0]
                # traversing all the words in a review
                for i in range(5, 5 + int(words[4])):
                    if words[i] == ".":
                        continue
                    # Assigning id to each word in whole review
                    if words[i] not in self.data:
                        self.data[words[i]] = self.count
                        self.count += 1
                    id = self.data[words[i]]
                    # storing freq of each word
                    if id not in freq["words"]:
                        freq["words"][id] = 1
                    else:
                        freq["words"][id] += 1
                    # sentence will have id for each word
                    freq["sentence"].append(id)
                    freq["actual_sen"] += words[i] + " "
                # appending to the list of review per product
                self.review[words[1]].append(freq)
                
        return self.review, self.data