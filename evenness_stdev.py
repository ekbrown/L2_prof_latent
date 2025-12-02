import re
from statistics import stdev

def evenness_std_dev(text):
  words_list = re.findall(r"[-'’a-z]+", text.lower(), flags=re.IGNORECASE)
  word_counts = {}
  for word in words_list:
    if word in word_counts:
      word_counts[word] += 1
    else:
      word_counts[word] = 1
  
  # TEST STATEMENT - designed to print the words and their counts for testing purposes
  # for word, count in word_counts.items():
  #   print(f"word: {word} > count: {count}")

  values = list(word_counts.values())

  std_dev = stdev(values)

  return std_dev