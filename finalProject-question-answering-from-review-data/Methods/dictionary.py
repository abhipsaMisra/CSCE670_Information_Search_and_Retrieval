# To populate dictionary
rev = set()
ques = set()

def create_dict(question, review, question_file_name, review_file_name, ques_count, test_question):
    count, data = 0, dict()
    # taking care of questions from Amazon data
    count = make_ques(question, data, count, question_file_name, ques_count, test_question)
    # taking care of reviews from Amazon data
    make_review(review, question, data, count, review_file_name)

    unwanted = list()
    for item in question:
        if item not in review:
            unwanted.append(item)

    for item in unwanted:
        question.pop(item, 0)
        if item in test_question:
            test_question.pop(item, 0)

    return data, question, review, ques_count, test_question


# Handling Question/answers here
def make_ques(question, data, count, question_file_name, ques_count, test_question):
    c = 0.0
    # opening questions file from amazon data
    with open(question_file_name) as fp:
        for line in fp:

            words = line.split()
            if words[1] != "A":
                c += 1

            # Not taking open ended question for now, only taking YN(binary) questions
            if len(words) == 0 or words[2] == "O" or words[2] == "?":
                continue
            if words[3] in ques:
                continue

            ques.add(words[3])

            # product id and looking for questions
            if words[0] not in question and words[1] != "A":
                question[words[0]] = list()
            if words[0] not in test_question and words[1] != "A" and c > ques_count:
                test_question[words[0]] = list()
            # Handling anwers here
            # looking for answer value, default answer is stored as False, making it True
            if words[1] == "A" and words[2] == "Y":
                # In case there is no question corresponsing to answer
                if words[0] not in question:
                    continue
                # Storing answer as True for "Y" answers
                question[words[0]][-1]["A"] = True
                if c > ques_count and words[0] in test_question and len(test_question[words[0]]) !=0 :
                    test_question[words[0]][-1]["A"] = True
                continue
            # Handling questions here
            if words[1] == "Q" and words[2] == "YN":

                # for each question in an item
                freq = dict()
                q = list()
                # answer is False by default
                freq["A"] = False
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
                    if words[i] not in data:
                        data[words[i]] = count
                        count += 1
                    id = data[words[i]]
                    # Increasing frequency of each word, initial 1 when first appear for first time in question
                    if id not in freq["words"]:
                        freq["words"][id] = 1
                    else:
                        freq["words"][id] += 1
                    # for Rogue
                    freq["sentence"].append(id)
                # appending freq for each question corresponding to item
                question[words[0]].append(freq)
                if c > ques_count:
                    test_question[words[0]].append(freq)
    return count


'''
    for key in question:
        print key
        for i in question[key]:
            print i["A"]
            print i["sentence"]
            for v in i["words"]:
                print v, i["words"][v]
'''


# handling review part here
def make_review(review, question, data, count, review_file_name):
    # opening Review data file from amazon data
    with open(review_file_name) as fp:
        for line in fp:
            words = line.split()
            # if there is no questions for product, not considering reviews
            if len(words) == 0 or words[1] not in question:
                continue
            if words[0] in rev:
                continue

            rev.add(words[0])
            # If product Id is not present in review
            if words[1] not in review:
                review[words[1]] = list()
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
                if words[i] not in data:
                    data[words[i]] = count
                    count += 1
                id = data[words[i]]
                # storing freq of each word
                if id not in freq["words"]:
                    freq["words"][id] = 1
                else:
                    freq["words"][id] += 1
                # sentence will have id for each word
                freq["sentence"].append(id)
                freq["actual_sen"] += words[i] + " "
            # appending to the list of review per product
            review[words[1]].append(freq)


'''
    for key in review:
        print key
        for i in review[key]:
            print i["sentence"]
            for x in i["words"]:
                print x, i["words"][x]

'''