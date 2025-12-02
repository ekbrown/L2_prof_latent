# Script created by Earl Brown, with some post processing by Claude 3.7 and Nathaniel May
import re

def calculate_word_distances(text, stopwords=None):
    # Calculate the average distance between repeated words in a text.
    
    #Args:
        # text (str): The input text to analyze
        # stopwords (list, optional): List of words to ignore. Defaults to ["THE", "AND"]
    
   # Returns:
        # dict: A dictionary containing the numerator, number of differences, average distance,
        #       and the word index dictionary
    
    if stopwords is None:
        stopwords = ["THE", "AND"]
    # we can add in NLTK stopword elements here. I tried to mess with it on a different script and couldn't get it to work properly
    
    # Convert stopwords to uppercase for case-insensitive comparison
    stopwords = [word.upper() for word in stopwords]
    
    # Find all words
    wds = re.findall(r"[-'a-z]+", text.upper(), flags=re.IGNORECASE)
    
    # Create word index dictionary
    wd_index = {}
    for i in range(len(wds)):
        cur_wd = wds[i]
        if cur_wd not in stopwords:
            if cur_wd not in wd_index:
                wd_index[cur_wd] = [i]
            else:
                wd_index[cur_wd].append(i)
    
    # Calculate distances
    numerator = 0
    num_of_diff = 0
    for k, v in wd_index.items():
        if len(v) > 1:
            for sub_i in range(len(v)):
                if sub_i > 0:
                    numerator += (v[sub_i] - v[sub_i - 1])
                    num_of_diff += 1
    
    # Calculate average distance
    avg_distance = numerator / num_of_diff if num_of_diff > 0 else 0
    
    return {
        "numerator": numerator,
        "number_of_differences": num_of_diff,
        "average_distance": avg_distance,
        "word_index": wd_index
    }