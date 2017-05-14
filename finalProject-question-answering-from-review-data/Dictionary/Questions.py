
class questions:
    def __init__(self, filename, ques_count, data):
        self.ques = set()
        self.question = dict()
        self.test_question = dict()
        self.file = filename
        self.count = 0
        self.ques_count = ques_count
        self.data = data
    
        # Handling Question/answers here
    def make_ques(self):
        c = 0.0
        # opening questions file from amazon data
        with open(self.file) as fp:
            for line in fp:
    
                words = line.split()
                if words[1] != "A":
                    c += 1
    
                # Not taking open ended question for now, only taking YN(binary) questions
                if len(words) == 0 or words[2] == "O" or words[2] == "?":
                    continue
                if words[3] in self.ques:
                    continue
    
                self.ques.add(words[3])
    
                # product id and looking for questions
                if words[0] not in self.question and words[1] != "A":
                    self.question[words[0]] = list()
                if words[0] not in self.test_question and words[1] != "A" and c > self.ques_count:
                    self.test_question[words[0]] = list()
                # Handling anwers here
                # looking for answer value, default answer is stored as False, making it True
                if words[1] == "A" and words[2] == "?":
                    if words[0] not in self.question:
                        continue
                    self.question[words[0]].pop()
                    if c > self.ques_count and words[0] in self.test_question and len(self.test_question[words[0]]) !=0 :
                        self.test_question[words[0]].pop()
                    continue

                if words[1] == "A" and words[2] == "N":
                    # In case there is no question corresponsing to answer
                    if words[0] not in self.question:
                        continue
                    # Storing answer as True for "Y" answers
                    self.question[words[0]][-1]["A"] = False
                    if c > self.ques_count and words[0] in self.test_question and len(self.test_question[words[0]]) !=0 :
                        self.test_question[words[0]][-1]["A"] = False
                    continue
                # Handling questions here
                if words[1] == "Q" and words[2] == "YN":
    
                    # for each question in an item
                    freq = dict()
                    q = list()
                    # answer is False by default
                    freq["A"] = True
                    # Storing all words correpsonding to questions in a dictionary
                    freq["words"] = dict()
                    # To store sentence Id for Rogue implementation
                    freq["sentence"] = list()
                    # Question ID
                    freq["ID"] = words[3]
                    # traversing questions word by word
                    for i in range(5, 5 + int(words[4])):
                        if words[i] == ".":
                            continue
                        # Each word is represented by an ID
                        if words[i] not in self.data:
                            self.data[words[i]] = self.count
                            self.count += 1
                        id = self.data[words[i]]
                        # Increasing frequency of each word, initial 1 when first appear for first time in question
                        if id not in freq["words"]:
                            freq["words"][id] = 1
                        else:
                            freq["words"][id] += 1
                        # for Rogue
                        freq["sentence"].append(id)
                    # appending freq for each question corresponding to item
                    self.question[words[0]].append(freq)
                    if c > self.ques_count:
                        self.test_question[words[0]].append(freq)
        
        return self.count, self.data, self.question, self.test_question
        