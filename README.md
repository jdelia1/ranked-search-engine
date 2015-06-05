# Summary
Project completed for the first half of the Spring 2015 semester in Ithaca College's COMP-490: Search Engines and Recommender Systems course. Scrapes Google search results, and created a TF-IDF weighted ranked retrieval search engine.

# How To Use
<ul>
<li><b>To scrape Google results:</b> Run main.py</li>
<li><b>To produce and use Ranked Retrieval Search Engine:</b> Run tfidf.py</li>
  <ul>
  <li>You will be prompted to enter a SMART weighting for the documents and queries. 'nnn' will produce raw weights for each term in the document or query, 'ltc' will produce TF-IDF weights for each term in the document or query.</li>
  </ul>
</ul>

If you want to scale up the search engine, add new terms to the text documents in the './data/item/' directory. 
