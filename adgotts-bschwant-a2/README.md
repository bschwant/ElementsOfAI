# a2

# Part 1: Raichu

Description: The program raichu.py uses the minimax algorithm in our best attempt to optimally play the game of raichu. Given the size of the board, the color you are playing in the game, the current state of the board, and a time limit, our program outputs a board that gives us the user the best chance of winning. Each piece on the board ( pichus, pikachu’s, and raichu’s ) had to have all possible movement patterns for it to be calculated and stored. This calculation is done in each piece's perspective class. The succeeding outputs from these classes are aggregated, and looped over in the recursive minimax algorithm to a depth of 5. We chose to implement alpha-beta pruning with our minimax algorithm to reduce the time and the memory needed to make this computation. Each state at the depth of 5 is given a score based off of our evaluation function, which tallies up the difference in the total amount of pichus, pikachus, and raichus left on the board for each player with weights 1,3,and 10 respectively. We chose these weights through experimentation. 

Problems: While developing this we ran into a few problems. It was originally a struggle to generate all the possible successors for each piece in the game, but through trial,error, and lots of debugging we got it done. 


# Part 2: The Game of Quintris 
### Assignment Description:
The objective for this part of the assignment was to write a computer player that was capable of achieving the highest score possible in the game of Quintris.

### Program Description
I struggled with this part of the assignment and was not able to implement a fully working computer player. While working on this part of the assignment, I did create functions too compute possible configurations of the pieces. I also created functions to weight the possible configurations. However, the program does not work effectively.

### Problems, Assumptions and Simplifications
I struggled with how to affectively determine all possible states/configurations a piece could be moved to. Because of this I could not accurately test the cost functions I created to be used when determining the best configuration a piece should be moved to

# Part 3: Truth be Told
### Assignment Description: 
The objective for this part of the assignment was to use a Naive Bayes model to classify hotel reviews as either 'truthful' or 'deceptive'. The weights or the probability that a given word would exist in each type of review was found by finding the frequency they occur in each type of review. The probabilites are computed using the provided training set of data. After these probabilities were found, the model was used to classify reviews that are unlabled containted in the test set. Our model was able to classify reviews in the test data set with an accuracy of 82.5%.

### Program Description: 
Our program works by first determining the number of times individual words appear in each type of review, truthful and deceptive. In order to improve accuracy, we ignore words that occur fewer times than a threshold level, discussed below. After these word frequencys are found, we compute the probability of each word occuring based on the type of review by dividing the number of occurances by the total number of words seen in the type of review. When classifying reviews, each word is mulltiplied by the probability it exists in truthful reviews and also deceptive reviews. After doing this for each word in the review, the review is classified depening on which probability is greater.

### Problems, Assumptions and Simplifications:
In order to improve accuracy of our model, the first simplification we did was ignoring words that occured less than a threshold level. After experimenting with various different thrshold levels, we determined removing words seen less than 12 times provided the best accuracy. We also ignored stop words such as "i", "me", "and", etc that occur alot if reviews but don't really reveal much when comparing real or fake reviews. Finally, we used a probability value of .01 for words unseen during training to achieve the highest accuracy after testing various values. 
