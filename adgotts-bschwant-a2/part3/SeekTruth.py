# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
from typing import DefaultDict
import math

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # Get number of reviews for each label
    num_truth, num_decep = num_words_by_label(train_data)
   
    # Get word frequency 
    word_freq_dict = word_count(train_data)

    # Remove words that dont impact classifcation
    word_freq_dict_removed = remove_words(word_freq_dict)
   
    # Threshold number of times word must occur to not be removed

    ## 15 is BEST SO FAr
    occurance_threshold = 12 #25
    new_word_freq_dict = remove_minimal_occuring(word_freq_dict_removed, occurance_threshold)
    

    # Compute probability that word occurs based on whether or not review is truth or lie
    word_prob = compute_probability(new_word_freq_dict, threshold=0.0) #.08
    
    label_probs = {}
    label_probs["truthful"] = float(num_truth / (num_truth+num_decep))
    label_probs["deceptive"] = float(num_decep / (num_truth+num_decep))
   
    # Classify test review data
    new_word_freq_dict["truthful"]
    predictions = classify_reviews(test_data, word_prob, label_probs)

    return predictions
    # This is just dummy code -- put yours here!
    #return [test_data["classes"][0]] * len(test_data["objects"])

'''
    Compute the number of reviews exist for truth and lie reviews
'''
def num_words_by_label(train_data):
    truth = 0
    lie = 0
    for label in train_data["labels"]:
        if label == "truthful":
            truth +=1
        elif label == "deceptive":
            lie +=1
    return (truth, lie)

'''
    Function to compute the number of times words appear in the reviews
    Return: A dictionary with keys 'truthful' and 'deceptive' that have a value 
        that is a dictionary of the word occurances 
'''
def word_count(train_data):
    word_freq = {}
    for type in train_data["classes"]:
        word_freq[type] = {}
        word_freq[type] = DefaultDict(lambda:0,word_freq[type]) 

    num_reviews = len(train_data["objects"])

    for curr_index in range(num_reviews):
       
        temp_review = train_data["objects"][curr_index]
        temp_label = train_data["labels"][curr_index]
        temp_review = temp_review.split(" ")
        if(temp_label == "truthful"):
            for word_index in range(len(temp_review)):
                curr_word = temp_review[word_index]
                curr_word = ''.join(filter(str.isalnum,curr_word))
                curr_word = ''.join([i for i in curr_word if not i.isdigit()])
                curr_word = curr_word.lower()
                num_occur = word_freq[temp_label][curr_word] + 1
                word_freq[temp_label][curr_word] = num_occur

        elif(temp_label == "deceptive"):
            for word_index in range(len(temp_review)):
                curr_word = temp_review[word_index]
                curr_word = ''.join(filter(str.isalnum,curr_word))
                curr_word = ''.join([i for i in curr_word if not i.isdigit()])
                curr_word = curr_word.lower()
                num_occur = word_freq[temp_label][curr_word] + 1
                word_freq[temp_label][curr_word] = num_occur

    return word_freq

'''
    Function to remove words that dont impact classification
'''
def remove_words(word_list):

    # Stop word list below from: https://gist.github.com/sebleier/554280
    remove_2 = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", 
            "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", 
            "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", 
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing",
            "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", 
            "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", 
            "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there",
            "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no",
            "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should",
            "now"}

    for label in word_list:
        word_to_remove = []
      
        for word in word_list[label]:
            if word in remove_2:
                    word_to_remove.append(word)
            elif len(word)<0:
                    word_to_remove.append(word)
        for i in range (len(word_to_remove)):
            word_list[label].pop(word_to_remove[i])
       
        word_to_change = []
        #for word in word_list[label]:    
        #    try:
        #        if(word[-1]=='s'):
        #            print()
        #            #word_to_change.append(word) 
                    
        #    except:
        #        print("Failed on word:", word)
            
        for i in range (len(word_to_change)):
            word = word_to_change[i]
            num_occur = word_list[label][word]
            word_change = word[:-1]
            word_list[label].pop(word_to_change[i])
            word_list[label][word_change] += num_occur

    return word_list


'''
    Function to remove words that appear fewer times than a threshold level passed as input
    Return: The modified word frequency dict
'''
def remove_minimal_occuring(word_freq, threshold):
    remove_true = []
    remove_lie = []
    for word in word_freq["truthful"]:
        num_occur = word_freq["truthful"][word]
        if (num_occur <= threshold):
            remove_true.append(word)
    for word in word_freq["deceptive"]:
        num_occur = word_freq["deceptive"][word]
        if (num_occur <= threshold):
            remove_lie.append(word)

    for i in range(len(remove_true)):
        word_freq["truthful"].pop(remove_true[i])
    for i in range(len(remove_lie)):
        word_freq["deceptive"].pop(remove_lie[i])

    return word_freq

'''
    Computes the probability of each word existing based on label 'truthful' or 'deceptive'
    ADDED THRESHOLD TO REMOVE PROBS
    Return: Dict of probability for each word for each label
'''
def compute_probability(word_freq, threshold):
    probability = {}
    for label in word_freq:
        probability[label] = {}
        words_for_label = float(len(word_freq[label]))

        for word in word_freq[label]:
            temp_prob = float(word_freq[label][word]) / words_for_label
            if temp_prob < threshold:
                continue
            else:
                probability[label][word] = float(word_freq[label][word]) / words_for_label

    return probability

'''
    Classify reviews as truthful or deceptive
    Return: Classification of test data as array
'''
def classify_reviews(test_data, word_prob, label_probs):

     # Stop word list below from: https://gist.github.com/sebleier/554280

    remove_2 = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
            "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they",
            "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing",
            "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with",
            "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from",
            "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there",
            "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no",
            "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should",
            "now"}

    predictions = []
    temp_probs = {}

    for review in test_data["objects"]:

        temp_probs["truthful"] = 0
        temp_probs["deceptive"] = 0

        # Parse the review to analyze
        temp_str = review.split(" ")

        # P(truthful)
        p_truth = float(label_probs["truthful"])

        # P(deceptive)
        p_decep = float(label_probs["deceptive"])
        # print(review)
        for i in range (len(temp_str)):
            # print("word:", curr_word)
            curr_word = temp_str[i]
            # print("word:", curr_word)
            # Remove all symboles, number and make all letters lowercase
            curr_word = ''.join(filter(str.isalnum,curr_word))
            curr_word = ''.join([i for i in curr_word if not i.isdigit()])
            curr_word = curr_word.lower()
            curr_word = curr_word.replace(" ", "")

            # Check if curr_word is equal to None
            if not curr_word:
                continue

            # Remove 's' at end of words to match training data!
            #try:
            #    if(curr_word[-1] == 's'):
            #        print()
            #        # curr_word = curr_word[:-1]
            #except:
            #    print("XXXXXXXXXXXX Failed on word classify:", curr_word)

            # If word is in the stop list, it is skipped
            if curr_word in remove_2:
                continue

            # Ignore 2 letter words like training
            if len(curr_word)<= 0:
                continue

            # print("word:", curr_word)

            # Set probability for unseen words
            unseen_word_prob = .01
            p_word_truth = word_prob["truthful"].get(curr_word, unseen_word_prob)
            p_word_decep = word_prob["deceptive"].get(curr_word,unseen_word_prob)

            if(temp_probs["truthful"] == 0):
                temp_probs["truthful"]= p_word_truth
            else:
                temp_probs["truthful"]+= math.log(p_word_truth)
            if(temp_probs["deceptive"] == 0):
                temp_probs["deceptive"] = p_word_decep
            else:
                temp_probs["deceptive"] += math.log(p_word_decep)

        max_prob = max(temp_probs, key=temp_probs.get)
        predictions.append(max_prob)

    return predictions


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
