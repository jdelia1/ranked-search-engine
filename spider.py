# Evan Sobkowicz
# COMP 490 - Lab 1

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from socket import timeout
from bs4 import BeautifulSoup
import bs4
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import re

class Spider:

    def fetch(self, url):

        # Request the page, catch errors to prevent program from crashing by returning '-1' back to the main
        response = self.request(url)
        if response == -1:
            return -1

        # Read and parse the response using BeautifulSoup
        html = response.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html)
        [x.extract() for x in soup.findAll('script', 'iframe', 'style', 'link')] # Strip all unneeded tags

        # Get Title, with error handling for no head, and no title
        if (soup.html is not None) and (soup.html.head is not None) and (soup.html.head.title is not None):
            title = soup.html.head.title.get_text()
        else:
            title = ""

        # Get Body, with error handling for no body
        if (soup.html is not None) and (soup.html.body is not None):
            body = soup.html.body.get_text()
        else:
            body = ""

        # Process text: Tokenize, Unique Terms, Lowercase Terms, Stemmed Terms
        tokens = word_tokenize(body)
        terms = self.get_terms(tokens)
        lower_terms = self.get_terms(self.lower(terms))
        stem_terms = self.get_terms(self.stem(lower_terms))

        # Return data for main
        return title, response.info(), stem_terms, str(soup), self.doctype(response.info())

    # Get the page, or return '-1' on an error
    def request(self, url):
        req = Request(url, None, {'User-agent': 'Firefox/3.05'})
        try:
            return urlopen(req)
        except (HTTPError, URLError) as error:
            print('ERROR:  Could not retrieve', url, 'because', error)
            return -1
        except timeout:
            print('ERROR:  Socket timed out - URL: %s', url)
            return -1

    # Get the doctype from the headers
    def doctype(self, headers):
        match = re.search("content-type:\s*([\w/]+);", str(headers), re.IGNORECASE)
        try:
            return match.group(1)
        except:
            return None

    # Lowercase a list of tokens
    def lower(self, tokens):
        lower_tokens = list()
        for w in tokens:
            lower_tokens.append(w.lower())
        return lower_tokens

    # Stem a list of tokens
    def stem(self, tokens):
        stemmed_tokens = list()
        ps = PorterStemmer()
        for word in tokens:
            stemmed_tokens.append(ps.stem(word))
        return stemmed_tokens

    # Get unique tokens
    def get_terms(self, tokens):
        terms = list()
        for word in tokens:
            #if word not in terms:
            terms.append(word)
        #terms.sort()
        return terms