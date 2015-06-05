# Author: Joe Delia
# COMP 490 - Lab 04

import os, sys
from nltk import *
from webDB import *
import math
import time


class RankedSearchIndex:

    def __init__(self):
        self.path = 'data/clean/'
        self.dataArray = []  # First value will be weight
        self.positionalIndex = {}
        self.doc_nnnltc = self.get_doc_nnnltc()
        self.quer_nnnltc = self.get_quer_nnnltc()
        self.query = dict()
        self.ranked_search_index = dict()
        self.tot_df = 0  # Number of documents in corpus

    """def __init__(self, doc_nnnltc, quer_nnnltc):
        self.path = 'data/clean/'
        self.dataArray = []  # First value will be weight
        self.positionalIndex = {}
        self.doc_nnnltc = doc_nnnltc
        self.quer_nnnltc = quer_nnnltc
        self.query = dict()
        self.ranked_search_index = dict()
        self.tot_df = 0  # Number of documents in corpus"""

    def get_doc_nnnltc(self):
        doc_nnnltc = input("Please enter SMART variant for documents (nnn or ltc): ")
        while (doc_nnnltc != "nnn") and (doc_nnnltc != "ltc"):
            doc_nnnltc = input("Please enter SMART variant for documents (nnn or ltc): ")

        return doc_nnnltc

    def get_quer_nnnltc(self):
        quer_nnnltc = input("Please enter SMART variant for queries (nnn or ltc): ")
        while (quer_nnnltc != "nnn") and (quer_nnnltc != "ltc"):
            quer_nnnltc = input("Please enter SMART variant for queries (nnn or ltc): ")

        return quer_nnnltc

    def create_positional_index(self):
        for doc in self.get_docs():
            self.create_index()

    def get_docs(self):
        docs = list()
        path = "data/clean/"
        dirs = os.listdir(path)
        for dir in dirs:
            type = dir.strip('.txt')
            docs.append(type)
        print(docs)
        return docs

    def create_index(self):
        index = dict() # Dictionary
        types = [] # Doc IDs
        path = "data/clean/" # Directory Path
        dirs = os.listdir(path)
        sum_squares_list = []

        print("Loading Index (Weight = " + self.doc_nnnltc + ")")
        for dir in dirs:
            type = dir.strip('.txt')
            types.append(type)

        for type in types:
            terms = []
            docID = type
            #print(docID)
            path = "data/clean/" + type + ".txt"
            f = open(path, "r", errors='ignore')
            count = 0
            try:
                for line in f:
                    cleanline = line.strip('\n')
                    terms.append(cleanline)
                    count = count + 1
            except UnicodeDecodeError:
                continue

            length = count  # number of terms in document

            # Create dictionary entry

            for i in range(length):
                currterm = terms[i]
                if currterm not in index:
                    index[currterm] = dict()
                if docID not in index[currterm]:
                    index[currterm][docID] = [0]
                index[currterm][docID].append(i+1)

            # Determines tf
            for i in range(length):
                currterm = terms[i]
                tf = len(index[currterm][docID])-1
                index[currterm][docID][0] = tf
                # print(currterm + " - Term Frequency: " + str(tf))
                # print(currterm + " - Doc Frequency: " + str(len(index[currterm])))
                # print(index[currterm])
                # print(index[currterm][docID])
                # print()

        # Determines tf-idf
        self.tot_df = len(dirs)
        for i in range(len(dirs)+1):
            sum_squares_list.append(0)
        doc_num = len(dirs)
        print("Calculating TFIDF Values")
        for term in index.keys():
            for doc in index[term]:
                tf = index[term][doc][0]      # Sets the tf of term in doc
                df = len(index[term])         # Determines df
                # print(doc)
                # print(term + ": in document " + str(doc) + " - df=" + str(df) + " TF=" + str(tf))
                # print(index[term][doc])
                # print()
                if self.doc_nnnltc == "ltc":
                    idf = math.log10(doc_num/df)  # Determines idf
                    tfidf = tf * idf              # Determines tf-idf
                    # print(doc)
                    sum_squares_list[int(doc)] += (tfidf*tfidf)
                    index[term][doc][0] = tfidf   # Sets first list value to tf-idf

        self.ranked_search_index = index
        for i in range(len(sum_squares_list)):
            sum_squares_list[i] = math.sqrt(sum_squares_list[i])

        if self.doc_nnnltc == "ltc":
            print("Normalizing Index")
            for term in index.keys():
                for doc in index[term]:
                    index[term][doc][0] /= sum_squares_list[int(doc)]

        print("Query Weighting Scheme: " + self.quer_nnnltc + ")")
        return [index, sum_squares_list]

    def get_df(self):
        return self.tot_df

    def get_query(self):
        token = input("Enter Query (or 'QUIT' to end): ").lower()
        tokenCheck = token.split(" ")
        stemmer = PorterStemmer()
        ret_val = True
        q_dict = dict()

        if token == "quit":
            ret_val = False
        else:
            for tok in range(len(tokenCheck)):
                tokenCheck[tok] = stemmer.stem(tokenCheck[tok])
                if tokenCheck[tok] not in q_dict:
                    q_dict[tokenCheck[tok]] = 1
                else:
                    q_dict[tokenCheck[tok]] += 1
            self.query = q_dict

        sum_of_squares = 1
        if self.quer_nnnltc == "ltc":
            for key in q_dict:
                if key in self.ranked_search_index:
                    weight = 1 + math.log10(q_dict[key])
                    idf = math.log10(self.tot_df / len(self.ranked_search_index[key]))
                    weight *= idf
                    q_dict[key] = weight
                    sum_of_squares += (weight * weight)
                else:
                    q_dict[key] = 0

            for key in q_dict:
                if key in self.ranked_search_index:
                    q_dict[key] /= math.sqrt(sum_of_squares)

        return [ret_val, q_dict, tokenCheck]

    def get_query_input(self, query):
        token = query.lower()
        tokenCheck = token.split(" ")
        stemmer = PorterStemmer()
        ret_val = True
        q_dict = dict()

        if token == "quit":
            ret_val = False
        else:
            for tok in range(len(tokenCheck)):
                tokenCheck[tok] = stemmer.stem(tokenCheck[tok])
                if tokenCheck[tok] not in q_dict:
                    q_dict[tokenCheck[tok]] = 1
                else:
                    q_dict[tokenCheck[tok]] += 1
            self.query = q_dict

        sum_of_squares = 1
        if self.quer_nnnltc == "ltc":
            for key in q_dict:
                if key in self.ranked_search_index:
                    weight = 1 + math.log10(q_dict[key])
                    idf = math.log10(self.tot_df / len(self.ranked_search_index[key]))
                    weight *= idf
                    q_dict[key] = weight
                    sum_of_squares += (weight * weight)
                else:
                    q_dict[key] = 0

            for key in q_dict:
                if key in self.ranked_search_index:
                    q_dict[key] /= math.sqrt(sum_of_squares)

        return [ret_val, q_dict, tokenCheck]


def main():
    """x = 5
    doc_smart = ["nnn", "nnn", "ltc", "ltc"]
    quer_smart = ["nnn", "ltc", "nnn", "ltc"]
    for i in range(len(doc_smart)):
        time_tot = 0.0
        for j in range(x):
            print("Running: " + doc_smart[i] + "." + quer_smart[i] + " - Attempt: " + str(j))
            start_time = time.time()
            index = RankedSearchIndex(doc_smart[i], quer_smart[i])
            create_index_res = index.create_index()
            end_time = time.time()
            time_tot += end_time-start_time
        print("Average Time for " + doc_smart[i] + "." + quer_smart[i] + ": " + str(time_tot/x))
"""
    index = RankedSearchIndex()
    create_index_res = index.create_index()
    ranked_index = create_index_res[0]
    sum_of_squares = create_index_res[1]
    db = "data/cache.db"
    db_file = WebDB(db)

    query_tuple = index.get_query()

    check = False
    while query_tuple[0] != False:
    #while check != False:
        # print(query_tuple)
        q_dict = query_tuple[1]
        tokenCheck = query_tuple[2]
        query_check = []
        for token in tokenCheck:
            #print(ranked_index[token])
            if token not in query_check:
                query_check.append(token)

        key_list = []
        value_list = []

        oKey_list = []
        oVal_list = []

        #print(q_dict)
        for i in range(len(query_check)):
            #print("IN FOR")
            try:
                #print("IN FOR > TRY")
                #print(ranked_index[query_check[i]])
                #print(query_check[i])
                for key in ranked_index[query_check[i]].keys():
                    #print(ranked_index[query_check[i]])
                    #print("IN FOR > TRY > FOR")
                    key_list.append(key)
                    value = ranked_index[tokenCheck[i]][key][0]
                    #print("KEY: " + key)
                    #print("INIT VAL: " + str(value))
                    # WHY DOESN'T THIS ISH WORK?
                    #print("q_dict[query_check[i]] = " + str(q_dict[query_check[i]]))
                    value *= q_dict[query_check[i]]
                    #print("FINAL VAL: " + str(value))
                    # END OF NOT WORKING ISH
                    value_list.append(value)
                    #print(value_list)
            except KeyError:
                continue

        item_type_list = []
        term_type_list = []
        for doc_key in key_list:
            path1 = "data/item_type/" + str(doc_key) + ".txt"
            path2 = "data/term/" + str(doc_key) + ".txt"
            f = open(path1, "r")
            try:
                for line in f:
                    item_type_list.append(line)
            except UnicodeDecodeError:
                continue
            f = open(path2, "r")
            try:
                for line in f:
                    term_type_list.append(line)
            except UnicodeDecodeError:
                continue

        term_dict = dict()
        for term_type in term_type_list:
            if term_type not in term_dict:
                term_dict[term_type] = 0


        #print("VAL LIST: " + str(value_list))
        while(len(key_list) != 0):
            curr_max = max(value_list)
            for i in range(len(value_list)):
                if (value_list[i] == curr_max):
                    if key_list[i] not in oKey_list:
                        oKey_list.append(key_list[i])
                        oVal_list.append(value_list[i])
                    else:
                        for j in range(len(oKey_list)):
                            if oKey_list[j] == key_list[i]:
                                oVal_list[j] += value_list[i]
                                break

                    key_list.pop(i)
                    value_list.pop(i)
                    break

        for key in range(len(oKey_list)):
            path1 = "data/term/" + str(oKey_list[key]) + ".txt"
            f = open(path1, "r")
            try:
                for line in f:
                    term_dict[line] += oVal_list[key]
            except UnicodeDecodeError:
                continue

        print()
        for c in range(3):
            current_max = 0
            max_term = ""
            for term in term_dict:
                if term_dict[term] > current_max:
                    current_max = term_dict[term]
                    max_term = term
            print(str(c+1) + ". " + max_term + " (" + str(term_dict[max_term]) + ")")
            term_dict[max_term] = 0
        print()

        count = 1

        # print(oKey_list)
        if len(oKey_list) == 0:
            print("No Results")
            print()
        else:
            for key in range(len(oKey_list)):
                urls = db_file.lookupCachedURL_byID(int(oKey_list[key]))
                print(str(count) + ". " + urls[2] + " -- KEY: " + str(oKey_list[key]) + " -- VAL: " + str(oVal_list[key]))
                print("    " + urls[0])
                path1 = "data/item_type/" + str(oKey_list[key]) + ".txt"
                path2 = "data/term/" + str(oKey_list[key]) + ".txt"
                f = open(path1, "r")
                try:
                    for line in f:
                        iType = line
                except UnicodeDecodeError:
                    continue
                f = open(path2, "r")
                try:
                    for line in f:
                        sTerm = line
                        #print(items[0])
                except UnicodeDecodeError:
                    continue
                print("\t" + iType + " | " + sTerm)
                print()

                count = count + 1
                if count > 10:  # Prints only the top 10 results
                    break
        print()

        query_tuple = index.get_query()

    print("Thank you for using Joe's Search Engine")

main()