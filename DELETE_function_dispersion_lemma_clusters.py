'''
Please be aware:
This function loops over any and all wds in a string. For it to measure what we want it to, we have to only run it over a string of lemmas in the dataset. Otherwise, the function will need to be adjusted to only pay respect to lemmas.
'''

'''
UNFINISHED. 
atm, it prints the number of lemmas that repeat (within 20 tokens of themselves) for each group of 100 words. We still need to calculate the average (add each of these numbers up and divide by number of 100-word groups)

This function takes string as input and gives average number of lemmas that repeat within 20 tokens of themselves per 100 tokens as output. 

So we want the number of lemmas that repeat, right? Not the number of clusters? Because a full number of clusters would mean counting the lemma again if it repeated in a different 20 token window within the same group of 100 tokens???
'''

# import packages
import re
from nltk.corpus import stopwords
from math import floor

def get_lemma_clusters(txt):
    # example text
    # txt = "I cat bit the dog and the dog jump on the cat and the dog barked."

    # find all the words in a string
    # take care of differences in case
    wds = re.findall(r"[-'a-z]+", txt.lower(), flags=re.IGNORECASE)

    # create dictionary to hold the words w/ their indexes
    wd_index = {}

    # get nltk stopwords
    stops = list(stopwords.words('english'))

    # Loop through all words in the input string
    for i in range(len(wds)):
        # Round word indexes in a way that groups them by 100s
        group = floor((i + 100) / 100) * 100
        # create dictionary for current 100s group
        if group not in wd_index:
            wd_index[group] = {}
        # get current word using its index
        cur_wd = wds[i]
        # ignore stopwords
        if cur_wd not in stops:
            # print(cur_wd)
            # if cur_wd doesn't exist, add it
            if cur_wd not in wd_index[group]:
                wd_index[group][cur_wd] = [i]
            # if cur_wd already exists, append current index
            else:
                wd_index[group][cur_wd].append(i)

    # create dictionary to hold # of repeated lemmas in each group of 100 words
    repeated_words = {}

    # loop over each group of 100 words
    for group_number, group in wd_index.items():
        # create counter for each group of 100 words
        repeated_words[group_number] = 0
        # loop over each word in current group of 100 words
        for word in group:
            # get index list from each lemma in the group
            index_list = group[word]
            # if list length is greater than 1
            if len(index_list) > 1:
                # loop over each index in the list
                for sub_i in range(len(index_list) - 1):
                    # check distance between indexes for the lemma
                    index_distance = abs(int(index_list[sub_i]) - int(index_list[sub_i + 1]))
                    # if distance between a lemma and its repetition is 20 or less, add it to the counter for current group
                    if index_distance <= 20:
                        repeated_words[group_number] += 1
                        # for lemmas that repeat within 20 tokens from themselves, no need to count the same lemma twice. We want the number of lemmas that repeat, not the number of clusters?
                        # move to next token in current group
                        break
        # Print the results
        print(f'For lemmas in {group_number - 99} - {group_number}, there are {repeated_words[group_number]} repeated lemmas')
