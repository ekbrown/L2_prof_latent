wds = ["apple", "banana", "orange", "mango", "kiwi", "apple", "asdf", "asdf", "asdf", "a", "b", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m", "apple"]
count = 0
n_wds = len(wds)
print(n_wds)
for i in range(len(wds)):
    cur_wd = wds[i]
    for j in range(1, 20):
        if i + j < n_wds:
            other_wd = wds[i+j]
            if cur_wd == other_wd:
                print(cur_wd, i, i+j)
                count += 1

print(count / n_wds * 100)