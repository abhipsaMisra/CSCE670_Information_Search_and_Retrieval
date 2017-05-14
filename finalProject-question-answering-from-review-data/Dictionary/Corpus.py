import Questions
import Review

class corpus:
   def __init__(self, quesfile, reviewfile):
        self.question = dict()
        self.review = dict()
        self.data = dict()
        self.count = 0
        self.test_question = dict()
        self.num_lines = 0
        self.reviewfile = 'C:\\MyData\\Coding\\Python\\CSCE670\\FinalProject\\CS670Project\\Data\\'+reviewfile
        self.quesfile = 'C:\\MyData\\Coding\\Python\\CSCE670\\FinalProject\\CS670Project\\Data\\'+quesfile

   def create_dict(self):
        num_lines = sum(1 for line in open(self.quesfile))
        q = Questions.questions(self.quesfile, (0.90*self.num_lines)/2, self.data)
        # taking care of questions from Amazon data
        self.count, self.data, self.question, self.test_question= q.make_ques()
        r = Review.reviews(self.reviewfile, self.question, self.data, self.count)
        # taking care of reviews from Amazon data
        self.review, self.data = r.make_review()

        unwanted = list()
        for item in self.question:
            if item not in self.review:
                unwanted.append(item)

        for item in unwanted:
            self.question.pop(item, 0)
            if item in self.test_question:
                self.test_question.pop(item, 0)
