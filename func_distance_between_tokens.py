import re

txt = "I cat bit the dog and the dog jump on the cat and the dog barked."

wds = re.findall(r"[-'a-z]+", txt.upper(), flags=re.IGNORECASE)

wd_index = {}
stopwords = ["THE", "AND"]
for i in range(len(wds)):
    cur_wd = wds[i]
    if cur_wd not in stopwords:
        # print(cur_wd)
        if cur_wd not in wd_index:
            wd_index[cur_wd] = [i]
        else:
            wd_index[cur_wd].append(i)

numerator = 0
num_of_diff = 0
for k, v in wd_index.items():
    if len(v)>1:
        for sub_i in range(len(v)):
            if sub_i > 0:
                numerator += (v[sub_i] - v[sub_i - 1])
                num_of_diff += 1
print("numerator = ", numerator)
print("number of numbers =", num_of_diff)
print("average distance: ", numerator / num_of_diff)