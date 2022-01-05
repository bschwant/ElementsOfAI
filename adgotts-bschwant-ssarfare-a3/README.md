# Assignment 3
Group: Andrew Gotts, Brian Schwantes, Satyajeet Arun Sarfare

IU Usernames: adgotts-bschwant-ssarfare

## Part 1: Part-of-speech tagging

Here we are suppose to train a 3 Models to predict Part of speech tag for a given sentence 

### Training
Initially, we are given a text file with POS labeled for a given sentence after every word. We have to make models using this data by computing emission, 
transition probablities which we are going to use to predict POS.

Here we calculate the following dictionaries:

|No| Dictionary                  | Description                                                                                         |
|:-:|:----------------------------:|:----------------------------------------------------------------------------------------------------:|
|1.| emission_count              |contains the  number of times a POS tag given to a specific word.                                    |
|2.| totaltag_count              | contains the total occurence of tag in the training data                                            |
|3.| emission_probability        |  here we calculate the probability of a tag given to a specific word P(W|S)                         |
|4.| totaltag_prob               |  this contains the probablity of a tag in training file. - P(S)                                     |
|5.| transition_count            |  contains the  number of times transition of POS tag to a different POS tag given to a specific word|
|6.|transition_probability       | this contains the probablity of a transition tag in training file. - P(Si|Si-1)                     |
|7.|tags                         | contains all unique POS tags encountered in the training file, which are 12 in total.               |
|8.|double_transition_count      |this contains the number of times a POS tag comes after 2 previous tags.                             |
|9.|double_transition_probability|this contains second level transition probability - P(Si|Si-1,Si-2)                                  |

Emission probablity and totaltag_prob  is used in Simple Naive Bayes. Emission probablity, Transition probability and tags is used in Viterbi to make viterbi table. 
The double transition probability is used in Gibbs Sampling.

### Solution

#### Approach 1: Simple Naive Bayes

Here we want to maximise the P(S|W) and allocate that tag to the word. 
						
						P(S|W) = maximise (P(W|S)*P(S) / P(W)) ===> P(S|W) = maximise[(P(W|S)*P(S)]

The divisior is neglected since its going to be constant when we try to maximise P(S|W). P(W|S) is stored in emission_probability and P(S) is stored in totaltag_prob.

#### Approach 2:  HMM Viterbi

Here we consider 2 probabilities for calculating. One is P(W|S), stored in emission_probability and the next is the P(Si|Si-1), stored in transition_probability.
These are used to calculate the veterbi table. They are calculated as follows:
	
			Veterbi Table(ith row,tag) = max{(Veterbi Table(ith row, previous tag)*transition_probability(tag|previous tag)*emission_probability(word, tag))}

So once we get the max probability, we also add the corrospending tag to the lookup table. This is used to backtrack so as to get final tags for the sentence. 

#### Approach 3:  Gibbs Sampling Complex

Even though I couldn't implement Gibbs, the basic idea is as follows. First we create sample and then randomly generate some samples form that initial sample by changing tags. The next step is to calculate probablitity for those data generated from tags and return the maximum probability tag. Here we dont consider the first few samples as those will have very less accuracy. 

So we can say that the accuracy of this will depend on number of samples (iterations) that we perform. It will converge when it reaches its peak.

### Result

From the table below, we can see that HMM is providing us maximum accuracy as compared to simple for both words and sentence. 

|	  |		           |  Words correct:     |Sentences correct:|
|:-:|:------------:|:-------------------:|:----------------:|
|0. | Ground truth |     100.00%         |           100.00%|
|1. | Simple       |      93.92%         |           47.45% |
|2. | HMM          |     95.04%          |           54.20% |
|3. | Complex      |     18.60%          |            0.00%	|

### Design Decisions

The most common problem faced was for missing values. At first we encountered key errors. For these missing keys, I added a significantly small value so that it's very less and does not affect the probabilities of other tags. 

The next decision was to assign all words which were not encountered before as noun. This was done because this increaased out overall accuracy.

### References

Piazza slide
In class veterbi solution
https://stackoverflow.com/questions/54623094/creating-multilevel-dictionary-pos-tagger-in-python
https://www.w3schools.com/python/python_dictionaries.asp
https://www.mygreatlearning.com/blog/pos-tagging/
https://www.youtube.com/watch?v=fv6Z3ZrAWuU&ab_channel=ritvikmath
https://towardsdatascience.com/implementing-part-of-speech-tagging-for-english-words-using-viterbi-algorithm-from-scratch-9ded56b29133




# Part 2
The goal of this assignment was to create code that can find the boundaries between air/ice and ice/rock from the image of a radar echogram.
For this part of the assignment we used 3 approaches to find these boundaries - Simple Bayes Net, Viterbi Encoding, and Viterbi with Human Feedback.

### Simple Bayes Net
When finding the two bondaries using a simple bayes net, we first found the ice/rock edge because we assume it is more prominent. For every column in the image, we select the row with the highest strength from the provided edge strength function this gives us the ice/rock boundary. To find the air/ice edge, we do the same thing but only look at values 10 pixels below the ice/rock bondary we found. We do this because we are assuing the air/ice rock edge will be 10 pixels below the ice/rock edge.

### Viterbi Encoding
When find the two boundaries using viterbi encoding, we have to calculate and use transition probabilites and emission probabilites.

#### Transition Probability
When computing transition probability, we used a distribution that encourages "smoothness". To do this, we first computed the absoulte value of the distance from the previous, and then subtracted the max distance from all of the values and took the absoulte value which resulted in row closer to the previous row having higher probabilty. We also increased probability for the rows within 5 pixels of previous row.

#### Emission Probability
To compute the emission probability we normalized each row in a given column.

Overall using viterbi encoding identified boundaries that were more accurate and smoother than were achieved with the simple Bayes Net.

### Viterbi Encoding w/ Human Feedback 
To improve the boundaries found by Viterbi Encoding, we included the ability for a human to given feedback. For this part, a person givens coordinates that lie on the air/ice edge and coordinates that lie on the ice/rock edge. This allows us to have a defined starting point where the probability of being an edge is 1.

Given the coordinates, we used the same viterbi function; however, we started at the column provided. We then find the boundary to the left and right of the starting column.

### Results Part 2
![Results Image 16](/result_images/result_16.png)
Above are the results for the Simple Bayes Net, Viterbi Encoding, and Viterbi Encoding w/ Human Feedback (yellow, blue, red) for image 16. For a simpler image such as this one,  all techniques found reasonable boundaires. The simple bayes net was not as smooth as the viterbi techniques. For this image, the boundaries found for both viterbi techniques are basically the same.

![Results Image 23](/result_images/result_23.png)
Above are the results for the Simple Bayes Net, Viterbi Encoding, and Viterbi Encoding w/ Human Feedback (yellow, blue, red) for image 23. Image 23 has a lot more possible edges in it and thus proved to be a challenge for all techniques. All 3 techniques correctly identified the air/ice boundary for the most part. The simple bayes net identified much of the ice/rock boundary but is not smooth and is very disconnected. Viterbi without human feedback correctly identifies half of the ice/rock boundary but then incorrectly identifies the second half. When human feedback is provided, the viterbi encoding does slightly better. We tested many inputs and struggle to get the code to identify the entire boundary.


## Part 3: Reading text

The goal of this assignment was to implement the simple bayesian network of part 1 and then HMM of part 1 to recognize noisy text from an image. 

### Simple Bayes
To recognize noisy images, we first implemented a simple bayes net with a naive bayesian classifier. Provided a list of characters from a training image, we count the amount of pixels that match between a "test", or noisy image, and the list of training characters. The probability of a noisy character matching a train character is then calculated by dividing the amount of matching pixels by the total amount of pixels for each letter (14x25). Given this data our program loops over each letter in the noisy test image, and chooses the corresponding training letter with the highest probability of matching it.

This outputs a text string with the deciphered text. This output is somewhat accurate, but fails to recognize images as they get more and more noisy, and often confuses similar characters such as "I" and "1".  

### HMM
Given the characters "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' ", we started off by first parsing an english text document passed in by the user. A 2D dictionary where each key represented a character from the above list, {A: {A: 1, B:3, C:4 .... }, B:{ } ..... }, was used to store the amount of times a character occurs after another character in the training file. From this dictionary we were able to calculate the transition probabilities for each entry in the dictionary. The emission probabilities were calculated the same as they were in the simple bayes net, by comparing the amount of pixels between the test and training characters. We constructed a table perform the viterbi decoding. Where each row was the maximum result of the product of the transition probability multiplied by the emission probability multiplied by each character from the previous row. The character with the highest probability in the last column of the table was then identified, and we then backtracked the result through the table to get the final deciphered string for the HMM. 

We unfortunately ran into problems calculating the probabilities for each row value in the table. The transition probabilities seemed to have too much of an effect on the result and were thus weighted down significantly. This allowed our HMM to be somewhat accurate, but it still performed worse than the Simple Bayes net. It is possible using a different set of training data would improve the accuracy of the HMM, as we used the training data from part 1.
