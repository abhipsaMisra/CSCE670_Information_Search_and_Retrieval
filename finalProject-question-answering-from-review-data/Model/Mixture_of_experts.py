import ROGUE
import BM25
import sim_fact
import Bilinear
import Binary_Scorer
import Voting

class mixture_of_experts:
    
    def __init__(self, corpus):
        self.rel_sim = dict()
        self.rel_syn = dict()
        self.voting = dict()
        self.corpus = corpus
        
    def get_relevance(self):
        r = ROGUE.roguel(self.corpus.review, self.corpus.question)
        self.rel_sim = r.rogueL()
        b = BM25.bm25(self.corpus.review, self.corpus.question, self.rel_sim)
        self.rel_sim = b.okapi()
        
        s = sim_fact.similarity_fact(self.corpus.review, self.corpus.question)
        cosine,tf_idf_questions,tf_idf_reviews = s.evaluate_cosine_similarity()
        
        #cosine,tf_idf_questions,tf_idf_reviews = evaluate_cosine_similarity(data, question, review)
        #print("cosine done")
        bilinear_score = Bilinear.evaluate_bilinear(cosine,tf_idf_questions,tf_idf_reviews)
        #print("bilinear done")
        predicted_model = Binary_Scorer.evaluate_model(self.rel_sim,bilinear_score,self.corpus.question)

        return predicted_model

    def test_relevance(self):
        r = ROGUE.roguel(self.corpus.review, self.corpus.test_question)
        self.rel_sim = r.rogueL()
        b = BM25.bm25(self.corpus.review, self.corpus.test_question, self.rel_sim)
        self.rel_sim = b.okapi()
        
        s = sim_fact.similarity_fact(self.corpus.review, self.corpus.test_question)
        cosine,tf_idf_questions,tf_idf_reviews = s.evaluate_cosine_similarity()
                #cosine,tf_idf_questions,tf_idf_reviews = evaluate_cosine_similarity(data, question, review)
        #print("cosine done")
        bilinear_score = Bilinear.evaluate_bilinear(cosine,tf_idf_questions,tf_idf_reviews)
        return self.rel_sim, bilinear_score
        
    def get_voting(self, predicted_model,test_pairscore,test_bilinear_score,test_question, question, review):
        correct, incorrect = Voting.classification(predicted_model,test_pairscore,test_bilinear_score,test_question, question, review)
        return correct, incorrect

