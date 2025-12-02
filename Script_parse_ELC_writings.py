import sys
sys.path.append('/Users/ekb5/Documents/lex_div_operationalizations')
from lexical_diversity_modern import LexDivModern
from nltk import word_tokenize
import os, re
import pickle
from multiprocessing import Pool
import polars as pl
from collections import defaultdict

def get_info(txt, regex):
    return re.search(f"<{regex}: ([^>]+)>", txt).group(1)

def has_alpha(in_str):
    return bool(re.search(r"[-'’a-zA-Z]", in_str))

def process_one_file(pathway):
    with open(pathway) as infile:
        txt = infile.read()
        student_id = get_info(txt, "Student ID")
        year = get_info(txt, "Year")
        semester = get_info(txt, "Semester")
        test_type = get_info(txt, "Test type")
        time_control = get_info(txt, "Time control")
        response = re.sub(r"<[^>]+>", "", txt).strip().upper()
        tokens = word_tokenize(response)
        tokens = [t for t in tokens if has_alpha(t)]
        if len(tokens)<42:
            print(pathway)
            print("less than 42 tokens here")
            return 1
        doc_obj = LexDivModern(tokens)
        mattr = doc_obj.get_mattr()
        mtld_wrap = doc_obj.get_mtld_wrap_Jarvis()
        hdd = doc_obj.get_hdd()
        out_dict = {"filename": pathway, "student_id": student_id, "year": year, "semester": semester, "test_type": test_type, "time_control": time_control, "mattr": mattr, "mtld_wrap": mtld_wrap, "hdd": hdd}
        with open(f'/Users/ekb5/Downloads/temp/{pathway.replace("txt", "pkl")}', "wb") as outfile:
            pickle.dump(out_dict, outfile)
    return 0

def merge_dicts(pathway):
    os.chdir(pathway)
    pickles = [f for f in os.listdir() if f.endswith("pkl")]
    merged = defaultdict(list)
    for p in pickles:
        with open(p, "rb") as infile:
            cur_dict = pickle.load(infile)
            for k, v in cur_dict.items():
                merged[k].append(v)
    return merged

def expand_semester(in_str):
    semesters = {"W": "Winter", "S": "Summer", "F": "Fall"}
    return semesters[in_str]

def expand_year(in_str):
    years = {"18": "2018", "19": "2019", "20": "2020", "21": "2021"}
    return years[in_str]

def get_exam_type(in_str):
    return re.search(r"(LAT|Placement)", in_str).group(1)

def combine_excel_file(in_dir):
    all_excel = pl.DataFrame()
    for root, dirs, files in os.walk(in_dir):
        for file in files:
            if file.endswith(".xlsx"):
                semester = expand_semester(file[0])
                year = expand_year(file[1:3])
                exam =get_exam_type(file)
                # print(file)
                # print(exam)
                # raise Exception("asdf")
                # print(semester)
                # print(year)
                # raise Exception("asdf")
                pathway = os.path.join(root, file)
                cur_excel = pl.read_excel(pathway, has_header=False, columns = [0, 1, 3, 5, 6]).with_row_index()
                cur_excel = cur_excel.filter(pl.col("index") != 0)
                cur_excel = cur_excel.rename({"column_1": "ID", "column_2": "FairAverage", "column_3": "Age", "column_4": "L1", "column_5": "Sex"})
                cur_excel = cur_excel.drop("index")

                cur_excel = cur_excel.with_columns(
                    semester = pl.lit(semester), 
                    year = pl.lit(year),
                    exam = pl.lit(exam))
                # print(cur_excel)
                # raise Exception("asdf")
                all_excel = pl.concat([all_excel, cur_excel])
    return all_excel
                

if __name__ == "__main__":

    ### analyze the written response ###
    # os.chdir("/Users/ekb5/Corpora/ELC/writings_2018-2021")
    # filenames = [f for f in os.listdir() if f.endswith("txt")]
    # with Pool() as p:
    #     p.map(process_one_file, filenames)

    ### concatenate the pickled dictionaries ###
    pathway = "/Users/ekb5/Downloads/temp"
    all_dicts = merge_dicts(pathway)

    ### create Polars data frame ###
    df = pl.DataFrame(all_dicts)
    print(df) 
    # print(df.get_column("test_type"))
    # raise Exception("asdf")
    # df.write_csv("/Users/ekb5/Downloads/df1.csv", separator=",")

    sociodemo = combine_excel_file("/Users/ekb5/Corpora/ELC/Writing Rating/")
    print(sociodemo)
    # sociodemo.write_csv("/Users/ekb5/Downloads/sociodemo.csv", separator=",")
    
    df = df.join(sociodemo, how="left", left_on=["student_id", "year", "semester", "test_type"], right_on=["ID", "year", "semester", "exam"])
    df = df.filter(pl.col("FairAverage").is_not_null())
    print(df)
    df.write_csv("/Users/ekb5/Downloads/df2.csv", separator=",")
