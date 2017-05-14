PART 1:

In this part, you will implement a Naive Bayes classifier, which outputs the probabilities that a given review belongs to each class.
Use a mixture model that mixes the probability from the document with the general collection frequency of the word. You should use lambda = 0.7. Be careful about the decimal rounding since multiplying many probabilities can generate a tiny value. If the tie case happens, always go to the "Food-irrelevant" side.

Compile and Run:
Clone the src and data folders, navigate to src folder and then run:
Python naiveBayes.py

Output:
* For the entire testing dataset, report the overall accuracy.
* For the class "Food-relevant", report the precision and recall.
* For the class "Food-irrelevant", report the precision and recall.

-----------------------

PART 2:

In this part, your job is to implement a Rocchio classifier for "food-relevant vs. food-irrelevant". You need to aggregate all the reviews of each class, and find the center. Use the normalized raw term frequency.

Compile and Run:
Clone the src and data folders, navigate to src folder and then run:
Python rocchio.py

Output:
* For the entire testing dataset, report the overall accuracy.
* For the class "Food-relevant", report the precision and recall.
* For the class "Food-irrelevant", report the precision and recall.