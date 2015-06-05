# Author: Joe Delia
# COMP 490 - Lab 03

import os, sys
from nltk import *
from webDB import *

class PositionalIndexDictionary:

    def __init__(self):
        self.path = 'data/clean/'
        self.dataArray = []
        self.positionalIndex = {}

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

        for dir in dirs:
            type = dir.strip('.txt')
            types.append(type)

        for type in types:
            terms = []
            docID = type
            path = "data/clean/" + type + ".txt"
            f = open(path, "r")
            count = 0
            try:
                for line in f:
                    cleanline = line.strip('\n')
                    terms.append(cleanline)
                    count = count + 1
            except UnicodeDecodeError:
                continue

            length = count

            # Create dictionary entry
            for i in range(length):
                currterm = terms[i]
                if currterm not in index:
                    index[currterm] = dict()
                if docID not in index[currterm]:
                    index[currterm][docID] = []
                index[currterm][docID].append(i+1)

        return index

def options():
        print("Command Options:")
        print("1) Token Query")
        print("2) AND Query")
        print("3) OR Query")
        print("4) Phrase Query")
        print("5) Near Query")
        print("6) Quit")

def main():
    index = PositionalIndexDictionary()
    positionalIndex = index.create_index()
    db = "data/cache.db"
    db_file = WebDB(db)
    end = False

    while end == False:
        options()
        c = input("Select option 1-6: ")
        if c == "1":
            token = input("Search Term: ")
            stemmer = PorterStemmer()
            token = stemmer.stem(token)

            try:
                print()
                """print("Token: " + str(positionalIndex[token]))
                print("Keys: " + str(positionalIndex[token].keys()))
                print("Values: " + str(positionalIndex[token].values()))
                print()"""

                count = 1
                for key in positionalIndex[token].keys():
                    urls = db_file.lookupCachedURL_byID(int(key))
                    print(str(count) + ". " + urls[2])
                    print("    " + urls[0])
                    print()

                    count = count + 1
                print()
            except KeyError:
                print("No Results")
                print()
                continue

        if c == "2":
            token1 = input("First Search Term: ")
            token2 = input("Second Search Term: ")
            stemmer = PorterStemmer()
            token1 = stemmer.stem(token1)
            token2 = stemmer.stem(token2)

            key_list = [] # docIDs which have both tokens

            try:
                for key in positionalIndex[token1].keys():
                    for key2 in positionalIndex[token2].keys():
                        if key == key2:
                            key_list.append(key)

                count = 1
                for key in key_list:
                    urls = db_file.lookupCachedURL_byID(int(key))
                    print(str(count) + ". " + urls[2])
                    print("    " + urls[0])
                    print()

                    count = count + 1

                print()
            except KeyError:
                print("No Results")
                continue
            print()

        if c == "3":
            token1 = input("First Search Term: ")
            token2 = input("Second Search Term: ")
            stemmer = PorterStemmer()
            token1 = stemmer.stem(token1)
            token2 = stemmer.stem(token2)

            key_list = [] # docIDs for documents with either token1 or token2

            try:
                for key in positionalIndex[token1].keys():
                    key_list.append(key)
                for key in positionalIndex[token2].keys():
                    key_list.append(key)

                count = 1
                for key in key_list:
                    urls = db_file.lookupCachedURL_byID(int(key))
                    print(str(count) + ". " + urls[2])
                    print("    " + urls[0])
                    print()

                    count = count + 1

                print()
            except KeyError:
                print("No Results")
                continue
            print()

        if c == "4":
            token = input("Enter a two-word search term: ")
            tokenCheck = token.split(" ")
            if len(tokenCheck) != 2:
                print("Query not formatted correctly.")
                print()
            else:
                stemmer = PorterStemmer()
                tokenCheck[0] = stemmer.stem(tokenCheck[0])
                tokenCheck[1] = stemmer.stem(tokenCheck[1])
                tok1keys = positionalIndex[tokenCheck[0]]
                tok1keys = tok1keys.keys()
                tok2keys = positionalIndex[tokenCheck[1]]
                tok2keys = tok2keys.keys()

                key_list = []

                try:
                    for key1 in tok1keys:
                        for key2 in tok2keys:
                            values1 = tok1keys.get(key1)
                            values2 = tok2keys.get(key2)
                            for val1 in values1:
                                for val2 in values2:
                                    if int(val1)+1 == int(val2):
                                        key_list.append(key1)
                    count = 1
                    for i in key_list:
                        urls = db_file.lookupCachedURL_byID(int(i))
                        print(str(count) + ". " + urls[2])
                        print("    " + urls[0])
                        print()

                        count = count + 1

                except KeyError:
                    print("No Results")
                    continue

            print()

        if c == "5":
            print("5")
            token = input("Enter a two-word search term, separated by the word 'NEAR': ")
            tokenCheck = token.split(" ")
            if len(tokenCheck) != 3:
                print("Query not formatted correctly.")
                print()
            else:
                stemmer = PorterStemmer()
                tokenCheck[0] = stemmer.stem(tokenCheck[0])
                tokenCheck[1] = stemmer.stem(tokenCheck[1])
                tokenCheck[2] = stemmer.stem(tokenCheck[2])
                tok1keys = positionalIndex[tokenCheck[0]]
                tok1keys = tok1keys.keys()
                tok2keys = positionalIndex[tokenCheck[2]]
                tok2keys = tok2keys.keys()
                if tokenCheck[1] != "NEAR":
                    print("Query not formatted correctly.")
                    print()
                else:
                    key_list = []

                    try:
                        for key1 in tok1keys:
                            for key2 in tok2keys:
                                values1 = tok1keys.get(key1)
                                values2 = tok2keys.get(key2)
                                for val1 in values1:
                                    for val2 in values2:
                                        if (int(val1) - int(val2)) >= -5 or (int(val1) - int(val2) <= 5):
                                            key_list.append(key1)
                        count = 1
                        for i in key_list:
                            urls = db_file.lookupCachedURL_byID(int(i))
                            print(str(count) + ". " + urls[2])
                            print("    " + urls[0])
                            print()

                            count = count + 1
                    except KeyError:
                        print("No Results")
                        continue

                print()
        if c == "6":
            print("Thank you, and have a nice day!")
            end = True

main()