from collections import Counter
# import lex_div_operationalizations
from statistics import mean
from spellchecker import SpellChecker
from statistics import stdev


class LexDivModern:
    """Pass in a list of already tokenized words"""
    def __init__(self, in_list):
        self.in_list = in_list

    def get_ttr(self, in_wds):
        return len(set(in_wds)) / len(in_wds)

    def get_mattr(self, window_span = 50):
        n_wds = len(self.in_list)
        if n_wds <= window_span:
            output = self.get_ttr(self.in_list)
        else:
            numerator = 0.0
            n_window = n_wds - window_span + 1
            for i in range(n_window):
                numerator += self.get_ttr(self.in_list[i : i+window_span])
            output = numerator / float(n_window)
        return output

    def get_mattr_rs(self):
        return lex_div_operationalizations.get_mattr_rs(self.in_list, 50)

    def get_mtld_wrap_Jarvis(self, target_ttr = 0.72):
        """
        Get MTLD_wrap with Python code written by Scott Jarvis
        Vidal, Karina & Jarvis, Scott. 2020. Effects of English-medium instruction on Spanish students’ proficiency and lexical diversity in English. Language Teaching Research. SAGE Publications 24(5). 568–587. (doi:10.1177/1362168818817945)
        """
        factor_lengths = []
        e = set()
        iterations = len(self.in_list)
        for n in range(0, iterations):
            tokens = 0
            end_reached = False
            for i in range(n, iterations):
                lemma = self.in_list[i]
                tokens += 1
                e.add(lemma)
                if tokens >= 10:
                    types = float(len(e))
                    ttr = float(types / tokens)
                    if ttr < target_ttr:
                        factor_lengths.append(tokens)
                        e.clear()
                        end_reached = True
                        break
            if end_reached == False:
                for i in range(0, iterations):
                    lemma = self.in_list[i]
                    tokens += 1
                    e.add(lemma)
                    if tokens >= 10:
                        types = float(len(e))
                        ttr = float(types / tokens)
                        if ttr < target_ttr:
                            factor_lengths.append(tokens)
                            break
                break
        sum_of_factors = sum(factor_lengths)
        number_of_factors = float(len(factor_lengths))
        mtld_wrap = float(sum_of_factors / number_of_factors)
        # return mtld_wrap
        return (mtld_wrap, number_of_factors, mean(factor_lengths))


    def get_mtld_wrap_Jarvis_debug(self, target_ttr = 0.72):
        """
        Get MTLD_wrap with Python code written by Scott Jarvis
        Vidal, Karina & Jarvis, Scott. 2020. Effects of English-medium instruction on Spanish students’ proficiency and lexical diversity in English. Language Teaching Research. SAGE Publications 24(5). 568–587. (doi:10.1177/1362168818817945)
        """
        factor_lengths = []
        e = set()
        iterations = len(self.in_list)
        with open("/Users/ekb5/Downloads/debug.csv", "w") as outfile:
          outfile.write("start_index,len_factor,ttr\n")
          for n in range(0, iterations):
              tokens = 0
              end_reached = False
              for i in range(n, iterations):
                  lemma = self.in_list[i]
                  tokens += 1
                  e.add(lemma)
                  if tokens >= 10:
                      types = float(len(e))
                      ttr = float(types / tokens)
                      if ttr < target_ttr:
                          factor_lengths.append(tokens)
                          outfile.write(f"{n},{tokens},{ttr}\n")
                          e.clear()
                          end_reached = True
                          break
              if end_reached == False:
                  for i in range(0, iterations):
                      lemma = self.in_list[i]
                      tokens += 1
                      e.add(lemma)
                      if tokens >= 10:
                          types = float(len(e))
                          ttr = float(types / tokens)
                          if ttr < target_ttr:
                              factor_lengths.append(tokens)
                              outfile.write(f"{n},{tokens},{ttr}\n")
                              break
                  break
          sum_of_factors = sum(factor_lengths)
          number_of_factors = float(len(factor_lengths))
          mtld_wrap = float(sum_of_factors / number_of_factors)
          # return mtld_wrap
        return (mtld_wrap, number_of_factors, mean(factor_lengths))


    def get_mtld_wrap_jarvis_rs(self):
        return lex_div_operationalizations.get_mtld_wrap_jarvis_rs(self.in_list)

    ### helper functions for HDD ###
    ### lifted from Kris Kyle's lexical_diversity Python module:
    ### https://github.com/kristopherkyle/lexical_diversity/
    ### many thanks are expressed to Kris for making his code public
    def choose(self, n, k): #calculate binomial
        """
		A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
		"""
        if 0 <= k <= n:
            ntok = 1
            ktok = 1
            for t in range(1, min(k, n - k) + 1): #this was changed to "range" from "xrange" for py3
                ntok *= n
                ktok *= t
                n -= 1
            output = ntok // ktok
        else:
            output = 0
        return output
    
    def hyper(self, successes, sample_size, population_size, freq): #calculate hypergeometric distribution
		#probability a word will occur at least once in a sample of a particular size
        try:
            prob_1 = 1.0 - (float((self.choose(freq, successes) * self.choose((population_size - freq),(sample_size - successes)))) / float(self.choose(population_size, sample_size)))
            prob_1 = prob_1 * (1/sample_size)
        except ZeroDivisionError:
            prob_1 = 0
        return prob_1

    def get_hdd(self, sample_size = 42):
        prob_sum = 0.0
        ntokens = len(self.in_list)
        types_list = list(set(self.in_list))
        frequency_dict = Counter(self.in_list)
        for items in types_list:
            prob = self.hyper(0, sample_size, ntokens, frequency_dict[items]) #random sample is 42 items in length
            prob_sum += prob
        return prob_sum 

    def check_spelling(self):
        self.in_list
        spell = SpellChecker()
        misspelled = spell.unknown(self.in_list)
        for i in range(len(self.in_list)):
            if self.in_list[i] in misspelled:
                self.in_list[i] = spell.correction(self.in_list[i])


    def get_evenness(self):
        word_counts = {}
        for word in self.in_list:
            word_counts[word] = word_counts.get(word, 0) + 1
        values = list(word_counts.values())
        std_dev = stdev(values)
        return std_dev


### end class definition ###
