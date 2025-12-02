def get_dispersion_Jarvis_2013(wds, span = 20):
    """Function to calculate the number of clusters of repeated words per 100 words of running text. Jarvis 2013 defines a cluster as a word that is preceded by itself within 20 words of running text.

    param wds: The tokenized words as a Python list of strings;
    param span: The number of running words that a word should be repeated within in order to count as a cluster;
    
    return: A float with the number of clusters per 100 words.

    See:
    Jarvis, Scott. 2013. Defining and measuring lexical diversity. Vocabulary Knowledge: Human ratings and automated measures (Studies in Bilingualism 47), 13–44. Amsterdam: John Benjamins Publishing Company. (https://doi.org/10.1075/sibil.47.03ch1)

    This function was written by Earl Kjar Brown ekbrown byu edu.
    """
    n_wds = len(wds)
    n_clusters = 0
    indexes = {}
    for i in range(n_wds):
        cur_wd = wds[i]
        if cur_wd not in indexes:
            indexes[cur_wd] = i
        else:
            if i - indexes[cur_wd] <= span:
                n_clusters += 1
            indexes[cur_wd] = i
    return n_clusters / n_wds * 100

if __name__ == "__main__":
    wds = "apple banana apple orange mango kiwi strawberry orange orange banana orange apple mango".split()
    span = 5
    result = get_dispersion_Jarvis_2013(wds, span)
    print(result)
