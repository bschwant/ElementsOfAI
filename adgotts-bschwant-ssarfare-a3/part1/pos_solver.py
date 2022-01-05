###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names Satyajeet Sarfare and user ids: ssarfare
#
# (Based on skeleton code by D. Crandall)
#


import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
emission_count = {}
totaltag_count = {}
emission_probability={}
totaltag_prob = {}
transition_count = {'start':{}}
transition_probability = {}
tags = ['det','noun','adj','verb','adp','.','adv','conj','prt','pron','num','x']
double_transition_count={}
double_transition_probability = {}

class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            log_posterior = 0
            for data_index in range(0,len(label)):
                if sentence[data_index] in emission_probability and label[data_index] in emission_probability[sentence[data_index]]:
                    log_emission = math.log(emission_probability[sentence[data_index]][label[data_index]])
                else:
                    # we add a very less probability value so that 0 error for log don't happen.
                    log_emission = math.log(0.0000000001)
                log_label = math.log(totaltag_prob[label[data_index]])
                log_posterior += log_emission + log_label
            return log_posterior
        elif model == "HMM":
            log_posterior_hmm = 0
            for i in range (0,len(label)):
                if i == 0:
                    if label[i] not in transition_probability["start"]:
                        trans_pos_prob = math.log(0.0000000001)
                    else:
                        trans_pos_prob = math.log(transition_probability["start"][label[i]])
                else:
                    if label[i] not in transition_probability[label[i-1]]:
                        trans_pos_prob = math.log(0.0000000001)
                    else:
                        trans_pos_prob = math.log(transition_probability[label[i-1]][label[i]])
                if sentence[i] in emission_probability and label[i] in emission_probability[sentence[i]]:
                    emission_pos_prob = math.log(emission_probability[sentence[i]][label[i]])
                else:
                    # we add a very less probability value so that 0 error for log don't happen.
                    emission_pos_prob = math.log(0.0000000001)
                log_posterior_hmm +=  emission_pos_prob + trans_pos_prob
            return log_posterior_hmm
        elif model == "Complex":
            return -999
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):

        for sentence_tag in data:

            for i in range(0, len(sentence_tag[0])):
                # calculates emission count and stores count in dictionary global_emission_count.
                # sentence_tag[0][i] gives us words and sentence_tag[1][i] gives us tags(Part of Speech)
                if sentence_tag[0][i] in emission_count:
                    if sentence_tag[1][i] in emission_count[sentence_tag[0][i]]:
                        emission_count[sentence_tag[0][i]][sentence_tag[1][i]] += 1
                    else:
                        emission_count[sentence_tag[0][i]][sentence_tag[1][i]] = 1
                else:
                    emission_count[sentence_tag[0][i]] = {sentence_tag[1][i]: 1}

            # calculates Tag count and stores count in dictionary global_totaltag_count.
            # here we have a total of 12 tags - 'det','noun','adj','verb','adp','.','adv','conj','prt','pron','num','x'
            for i in range(0, len(sentence_tag[1])):
                if sentence_tag[1][i] in totaltag_count:
                    totaltag_count[sentence_tag[1][i]] += 1
                else:
                    totaltag_count[sentence_tag[1][i]] = 1

            # calculate transition count
            for i in range(0, len(sentence_tag[1])):
                #checks if its first tag, so as to add it to start
                if i == 0:
                    if sentence_tag[1][i] in transition_count['start']:
                        transition_count['start'][sentence_tag[1][i]] += 1
                    else:
                        transition_count['start'][sentence_tag[1][i]] = 1

                # sentence_tag[1][i - 1] is the previous tag and sentence_tag[1][i] gives us the current tag.
                elif sentence_tag[1][i - 1] in transition_count:
                    if sentence_tag[1][i] in transition_count[sentence_tag[1][i - 1]]:
                        transition_count[sentence_tag[1][i - 1]][sentence_tag[1][i]] += 1
                    else:
                        transition_count[sentence_tag[1][i - 1]][sentence_tag[1][i]] = 1
                else:
                    transition_count[sentence_tag[1][i - 1]] = {sentence_tag[1][i]: 1}

            # calculate double transition count
            for i in range(0, len(sentence_tag[1]) - 2):
                first_tag = sentence_tag[1][i]
                second_tag = sentence_tag[1][i + 1]
                third_tag = sentence_tag[1][i + 2]
                if first_tag in double_transition_count:
                    if second_tag in double_transition_count[first_tag]:
                        if third_tag in double_transition_count[first_tag][second_tag]:
                            double_transition_count[first_tag][second_tag][third_tag] += 1
                        else:
                            double_transition_count[first_tag][second_tag][third_tag] = 1
                    else:
                        double_transition_count[first_tag][second_tag] = {third_tag: 1}
                else:
                    double_transition_count[first_tag] = {second_tag: {third_tag: 1}}

        # This calculates the emission probability.
        for word in emission_count:
            emission_probability[word] = {}
            for tags in emission_count[word]:
                emission_probability[word][tags] = emission_count[word][tags] / totaltag_count[tags]
        # print(global_emission_probability)

        # This calculates the total count probability.
        total_tags = sum(totaltag_count.values())
        # print(total_tags)
        for tags in totaltag_count:
            totaltag_prob[tags] = totaltag_count[tags] / total_tags
        #print(global_totaltag_prob)

        # this is to calculate transition probability
        for previous_tags in transition_count:
            transition_probability[previous_tags] = {}
            transition_total = sum(transition_count[previous_tags].values())
            for tags in transition_count[previous_tags]:
                transition_probability[previous_tags][tags] = transition_count[previous_tags][tags] / transition_total

        # print(global_transition_probability)
        double_transition_probability = double_transition_count
        for first_tag in double_transition_probability:
            for second_tag in double_transition_probability[first_tag]:
                for third_tag in double_transition_probability[first_tag][second_tag]:
                    second_level_probability = double_transition_probability[first_tag][second_tag][third_tag] / sum(double_transition_probability[first_tag][second_tag].values())
                    double_transition_probability[first_tag][second_tag][third_tag] = second_level_probability


        #pass

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        tag_list = []
        for word in sentence:
            max_probability = 0
            #default if word not in training dataset
            if word not in emission_probability:
                tag_list.append("noun")
            else:
                for tag in emission_probability[word]:
                    if max_probability < emission_probability[word][tag] * totaltag_prob[tag]:
                        max_probability = emission_probability[word][tag] * totaltag_prob[tag]
                        new_tag = tag
                tag_list.append(new_tag)
        return (tag_list)


    def hmm_viterbi(self, sentence):
        veterbi_table = {}
        lookup_table = {}
        for tag in tags:
            veterbi_table[tag] = [0] * len(sentence)
            lookup_table[tag] = [0] * len(sentence)
            #lookup_table[tag][0] = tag
            if sentence[0] not in emission_probability or tag not in emission_probability[sentence[0]]:
                veterbi_table[tag][0] = 0.000000001
            else:
                veterbi_table[tag][0] = transition_probability['start'][tag] * \
                                        emission_probability[sentence[0]][tag]

        for i in range(1, len(sentence)):
            for tag in tags:
                max_prob = 0
                for prev_tag in tags:
                    if tag not in transition_probability[prev_tag]:
                        transition_prob = 0.000000001
                    else:
                        transition_prob = transition_probability[prev_tag][tag]

                    # Getting maximum value
                    prob = veterbi_table[prev_tag][i - 1] * transition_prob
                    if max_prob < prob:
                        max_prob = prob
                        max_tag = prev_tag
                        lookup_table[tag][i] = max_tag

                        if sentence[i] not in emission_probability or tag not in emission_probability[
                            sentence[i]]:
                            veterbi_table[tag][i] = max_prob * 0.000000001
                        else:
                            veterbi_table[tag][i] = max_prob * emission_probability[sentence[i]][tag]

        sentence_length = len(sentence)
        viterbi_tags = [""] * sentence_length
        #print(viterbi_tags)
        #print(sentence[len(sentence) - 1])

        if sentence[sentence_length - 1] not in emission_probability:
            viterbi_tags[sentence_length - 1] = "noun"
        else:
            max_tag_prob = 0
            for tag in veterbi_table:
                if max_tag_prob < veterbi_table[tag][sentence_length - 1]:
                    max_tag_prob = veterbi_table[tag][sentence_length - 1]
                    maximum_tag = tag
            viterbi_tags[sentence_length - 1] = maximum_tag

        for i in range(sentence_length - 2, -1, -1):
            viterbi_tags[i] = lookup_table[viterbi_tags[i + 1]][i + 1]

        #print(veterbi_table)
        #print(lookup_table)
        #print(lookup_table[tag])

        return viterbi_tags

    def complex_mcmc(self, sentence):
        return [ "noun" ] * len(sentence)



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")



