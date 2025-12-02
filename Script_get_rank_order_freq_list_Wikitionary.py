import requests
from bs4 import BeautifulSoup as bs
import pickle

s = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

url = "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016)"
extensions = ["", "/10001-20000", "/20001-30000", "/30001-40000", "/40001-50000"]

freqs = {}
count = 0
for ex in extensions:
    cur_url = url + ex
    print(f"Working on {cur_url}...", end=" ")
    r = s.get(cur_url, headers=headers)
    soup = bs(r.content, "html.parser")
    wds = soup.select("p a")    
    for w in wds:
        count += 1
        # print(w.get_text(), i)
        freqs[w.get_text()] = count
    print("done.")
with open("/Users/ekb5/Documents/SLRF_2025/with_Alyssa_Nathaniel/freqs.pkl", mode="wb") as outfile:
    pickle.dump(freqs, outfile)
print("All done!")