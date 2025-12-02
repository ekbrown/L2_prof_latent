import os
import spacy
import re
import json
from multiprocessing import Pool
from nltk import word_tokenize
from spellchecker import SpellChecker


# Load English tokenizer, tagger, parser and NER
nlp = spacy.load('en_core_web_trf')

def get_info(txt, regex):
    return re.search(f"<{regex}: ([^>]+)>", txt).group(1)

def has_alpha(in_str):
    return bool(re.search(r"[-'’a-zA-Z]", in_str))

def lemmaticize_txt(inpath):
    outfilename = re.sub(r"\.txt$", ".json", os.path.basename(inpath))
    outpath = os.path.join("/Users/ekb5/Corpora/ELC/writings_2018-2021_json", outfilename)
    with open(inpath) as infile, open(outpath, "w") as outfile:
        txt = infile.read()
        student_id = get_info(txt, "Student ID")
        year = get_info(txt, "Year")
        semester = get_info(txt, "Semester")
        test_type = get_info(txt, "Test type")
        time_control = get_info(txt, "Time control")
        response = re.sub(r"<[^>]+>", "", txt).strip().upper()
        
        tokens = word_tokenize(response)
        spell = SpellChecker()
        misspelled = spell.unknown(tokens)
        # print("---pre tokens---")
        # print(tokens)
        for i in range(len(tokens)):
            if tokens[i] in misspelled:
                tokens[i] = spell.correction(tokens[i])

        # print("---post tokens---")
        tokens = [item if item is not None else "" for item in tokens]

        # print(tokens)
        response_spell_checked = ' '.join(tokens)
        # print(response_spell_checked)

        # doc = nlp(response)
        # lemmas = ' '.join([(w.lemma_.upper() + "_" + w.pos_[0]) for w in doc if has_alpha(w.lemma_)])

        doc = nlp(response_spell_checked)
        lemmas = ' '.join([(w.lemma_.upper() + "_" + w.pos_) for w in doc if has_alpha(w.lemma_)])
        outdict = {'student_id': student_id, 'year': year, 'semester': semester, 'test_type': test_type, 'time_control': time_control, 'lemmas': lemmas}
        json.dump(outdict, outfile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    os.chdir("/Users/ekb5/Corpora/ELC/writings_2018-2021_txt")
    filenames = [f for f in os.listdir() if f.endswith("txt")]
    with Pool() as p:
        p.map(lemmaticize_txt, filenames)
