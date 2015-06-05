"""
Lab 2: Web-Crawling for CS490: Search Engines and Recommender Systems - Spring 2015
http://jimi.ithaca.edu/CourseWiki/index.php/CS490_S15_Lab2

Spider Class Code for obtaining a website from a given URL
The HTML, Script, and other content is stripped (using BeautifulSoup4)
The raw content is tokenized (using NLTK)
The list of tokens is normalized by lowercasing and porter stemming (using NLTK)

Dependencies: you may need to download the nltk importer:
 import nltk
 nltk.download('all')

Code by Evan Sobkowicz (Commented by Doug Turnbull)
February 2015
"""

import os, sys

from webDB import *
from google import search
from spider import *
#from positional import *

# Get item types from file names in item directory
def get_item_types():
    """
    Get item types from file names in item directory
    :return list of time types a strings:
    """
    types = list()
    path = "data/item/"
    dirs = os.listdir(path)
    for dir in dirs:
        type = dir.strip('.txt')
        types.append(type)
    return types

def get_items_by_type(type):
    """
    Read items from text file into a list
    :param item type as a string (e.g., "book", "movie" :
    :return: list of strings
    """
    results = list()
    path = "data/item/" + type + ".txt"
    f = open(path, "r")
    lines = f.readlines()
    for line in lines:
        clean_line = line.strip('\n')
        results.append(clean_line)
    f.close()
    return results

def write_to_file(id, dir, contents):
    """
     Write 'contents' to a file named 'id' in the folder 'dir'
    :param id (int):
    :param dir (string):
    :param contents (string or list of strings:
    """

    file_path = "data/" + dir + "/" + str(id) + ".txt"
    f = open(file_path, "w", encoding='utf-8')
    output = ""
    if type(contents) == list:
        for item in contents:
            output += str(item)
            output += "\n"
    else:
        output = str(contents)
    try:
        f.write(str(output))
    except:
        print('ERROR: Could not write to', dir, 'file!')
    f.close()


def setup_directories():
    """
    Create subdirectories if they don't exist
    """
    directories = ["clean", "header", "item", "raw", "term", "item_type"]
    for dir in directories:
        dir_path = "data/" + dir
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

def main():
    """
    Google, Parse, Add to DB, and Cache
    :return:
    """

    # Initialize
    count = 0
    spider = Spider()
    google_results = 5

    # Setup the Cache File Structure
    setup_directories()

    # Setup Database
    db = WebDB("data/cache.db")

    # For each list of items (movies, books, music)
    for type in get_item_types():

        print(type)

        # For each item in the list
        for item in get_items_by_type(type):

            print("\n", item)

            # Add the item to the database
            item_id = db.insertItem(db._quote(item), type)
            numURLs = db.numURLToItem(item_id)
            if numURLs >= 8:
                print("Skipping: Already have "+str(numURLs) + "urls for item.\n")
                continue


            # Use Search Engine to find N=10 relevant URLs
            # For each URL
            results_counter = 0
            for url in search(str(item), stop=google_results, pause=0.5):

                print("\t " + url)

                # Check if url is already cached
                if db.lookupCachedURL_byURL(url):
                    print("\t\t Already Cached!")
                else:

                    # Download, Parse, & Cache Each Website
                    try:
                      response = spider.fetch(url)
                    except TimeoutError:
                      print ("Skipping URL: timeout error")
                      continue
                    except ConnectionResetError:
                      print ("Skipping URL: Connection Reset Error")
                      continue

                    # Process the Spider's response
                    if response == -1:
                        # Failure in the Spider's fetching
                        print('ERROR: Spider fetch failure!')
                    else:
                        if results_counter < 10:
                            # Successful Spider response
                            page_title = db._quote(response[0])
                            headers = "Title: " + page_title + "\n" + str(response[1])
                            terms = response[2] # These are stemmed!
                            html = response[3]
                            doc_type = response[4]

                            # Update information in database
                            url_id = db.insertCachedURL(url, doc_type, page_title)
                            url_to_item_id = db.insertURLToItem(url_id, item_id)

                            # Write cache files
                            write_to_file(url_id, "header", headers)
                            write_to_file(url_id, "raw", html)
                            write_to_file(url_id, "clean", terms)
                            write_to_file(url_id, "term", item)
                            write_to_file(url_id, "item_type", type)

                            # Status
                            print('\t\t Added Successfully!')
                            count += 1
                            results_counter += 1
                        else:
                            break


    # Print the number of processed URLs
    print("Processed " + str(count) + " URLs.")

main()