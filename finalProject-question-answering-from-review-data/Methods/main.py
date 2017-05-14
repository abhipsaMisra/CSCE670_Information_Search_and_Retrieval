import Dictionary.Corpus
import Model.Mixture_of_experts



def main(question_file_name, review_file_name):
    
    corp = Dictionary.Corpus.corpus(question_file_name,review_file_name)
    corp.create_dict()
    print "Dictionary formation done"

    mod = Model.Mixture_of_experts.mixture_of_experts(corp)
    predicted_model = mod.get_relevance()
    print "training done"

    #testing
    modtest = Model.Mixture_of_experts.mixture_of_experts(corp)
    test_pairscore,test_bilinear_score= modtest.test_relevance()
    print "testing done"

    c, i = mod.get_voting(predicted_model,test_pairscore,test_bilinear_score,corp.test_question, corp.question, corp.review)
    print "voting done"

    accuracy =  float(c) / float(c + i)
    print ("accuracy: %s" %accuracy)

if __name__ == "__main__":
    question_file_name = 'questions_Appliances.txt'
    review_file_name = 'reviews_Appliances.txt'
    main(question_file_name, review_file_name)