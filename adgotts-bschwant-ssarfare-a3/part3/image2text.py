#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: adgotts
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25

def simple_bayes(train_letters, test_letters):
    ''' Find the most likely string given only the emission probabilities'''

    final_str = ""

    # Compute final string
    for letter in test_letters: # loop through letters from image
        max_prob = 0
        best_letter = ""
        for key in train_letters: # loop through letters from training image
            chprob = emission_probs(train_letters[key], letter) # return probability of match between chars
            if(chprob > max_prob): # ensure the letter we output has the highest probability
                best_letter = key
                max_prob = chprob
        final_str += best_letter
    
    return final_str

def emission_probs(train_letter_key, test_letter):
    ''' Given the training and test letters find the emmision probabilities'''

    # Find number of pixels that match
    match = 0
    for x, y in zip(train_letter_key, test_letter):
        for i, char in enumerate(x):
            if (char == y[i]):
                match += 1

    # Calculate accuracy
    total_pixels = CHARACTER_HEIGHT*CHARACTER_WIDTH
    accuracy = match/total_pixels

    return accuracy

def transition_probs(train_txt_fname):
    ''' Given the location of a text file for training the model, count the occurences of each letter following another letter, 
        return a 2d dictionary with the transition probabilities for each character'''

    # Create a 2D dictionary to keep track of characters following character occurances
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    ch_dict_temp = {TRAIN_LETTERS[i]: 0 for i in range(0, len(TRAIN_LETTERS))}
    ch_dict = {TRAIN_LETTERS[i]: ch_dict_temp.copy() for i in range(0, len(TRAIN_LETTERS))}

    # Count how many time a character follows another character
    with open(train_txt_fname) as f: 
        for line in f:
            line = line.strip() # Remove newlines
            for i, ch in enumerate(line): # Loop through every character in each line
                try:
                    if(i+1 < len(line)):
                        ch_dict[ch][line[i+1]] += 1
                except (KeyError): # Character is not in list of TRAIN_LETTERS
                    pass
    
    # Given the final counts in the training data, calculate the probabilities of a letter occuring after another letter     
    for key in ch_dict:
        key_sum = sum(ch_dict[key].values())
        if key_sum != 0: # Save time by not looping through empty ones
            for innerkey in ch_dict[key]:
                val = ch_dict[key][innerkey]
                if val > 0:
                    ch_dict[key][innerkey] = (val/key_sum)
                
        else:
            #print(F"Keys not present in training data: {key}")
            pass
    

    return ch_dict

def HMM(train_letters, test_letters, train_txt_fname):
    ''' HMM''' 

    # Initialize Transition Probabilities 
    tran_probs = transition_probs(train_txt_fname)

    # Viterbi decoding data structure. List of collumn dictionaries
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    coll_dict = {TRAIN_LETTERS[i]: 0 for i in range(0, len(TRAIN_LETTERS))}
    hmmt = []

    # Letters for backtracking
    letter_track = {TRAIN_LETTERS[i]: "" for i in range(0, len(TRAIN_LETTERS))}
    
    for i, letter in enumerate(test_letters):
        coll_i = coll_dict.copy()

        # loop through rows
        for train_key in train_letters:
            chprob = emission_probs(train_letters[train_key], letter) # emmision probablity for this state/row
            if (i>0): # 2nd column and on
                # Initialize previous columns and values 
                prev_coll = hmmt[i-1]   
                max_prob = 0
                key = ""

                # Loop through the rows of the previous column, find the maximum probability, add max prob to associated row in new column
                for prev_key in prev_coll:
                    tp = tran_probs[prev_key][train_key] # transition probability
                    prob = (.49*prev_coll[prev_key]+.49*chprob+.02*tp)
                    if(prob > max_prob):
                        max_prob = prob
                        key = prev_key

                letter_track[train_key] += key # create a string showing the letters from the prev column that maximized each row entry
                coll_i[train_key] = max_prob
            
            else: # First column 
                coll_i[train_key] = chprob
        
        hmmt.append(coll_i)
    
        
    length = len(hmmt)-1
    vals = max(hmmt[length], key=hmmt[length].get)
    final_str = letter_track[vals] + vals
    return final_str

def load_letters(fname):
    '''  Converts an image into a 2D list structure that represents each letter in the image as 
    a 2-d grid of black and white dots'''
    
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    # print(im.size)
    # print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    ''' Returns a dictionary where each letter from the images dot representation is pre-pended with the letter it represents, 
    so ... {A: [dot list]. B: [ dot list] } '''

    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

# Check for correct args
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

# Generate lists from args
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname) # dictionary
test_letters = load_letters(test_img_fname) # 2D list

simple_result = simple_bayes(train_letters,test_letters)
hmm_result = HMM(train_letters,test_letters, train_txt_fname)

# The final two lines of your output should look something like this:
print("Simple: " + simple_result)
print("   HMM: " + hmm_result) 


