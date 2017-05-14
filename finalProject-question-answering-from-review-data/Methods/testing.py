# To populate dictionary
def create_dict_test(question, review, data, question_file_name, count, ques_count):
    #count, data = 0, dict()
    # taking care of questions from Amazon data
    count = make_ques(question, data, count, question_file_name, ques_count)

    unwanted = list()
    for item in question:
        if item not in review:
            unwanted.append(item)

    for item in unwanted:
        question.pop(item, 0)

    return data, question, review


# Handling Question/answers here
def make_ques(question, data, count, question_file_name, ques_count):
    c = 0.0
    # opening questions file from amazon data
    with open(question_file_name) as fp:
        for line in fp:
            if words[1] != "A":
                c += 1
            if c <= ques_count:
                continue

            words = line.split()
            # Not taking open ended question for now, only taking YN(binary) questions
            if len(words) == 0 or words[2] == "O" or words[2] == "?":
                continue
            # product id and looking for questions
            if words[0] not in question and words[1] != "A":
                question[words[0]] = list()
            # Handling anwers here
            # looking for answer value, default answer is stored as False, making it True
            if words[1] == "A" and words[2] == "Y":
                # In case there is no question corresponsing to answer
                if words[0] not in question:
                    continue
                # Storing answer as True for "Y" answers
                question[words[0]][-1]["A"] = True
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
    return count
