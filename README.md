## INTRODUCTION

	Search engine project is one of the most widely used application of the Information Retrieval application.

	Given the corpus or the collection of the documents or website, and a user query in the form of the string, the task of the Search Engine is to provide the ranked documents which are relevant to the query.

This project has Four main components which are:

1. Web Crawler:
Components that will crawl over the web pages and it will provide the collection of documents on which we can do the query processing. Crawling will start from the https://www.cs.uic.edu and visit the pages in the Breadth First Search Fashion and it will retrieve the pages that are under the uic domain.

2. Inverted Index:
Data Structure used to map the words information and documents and frequency.
Which will be used in the vector space model while querying the data.

3. Retrieve component:
This is the component that takes the user query and ranks the document      present in the collection according to the query and using the vector space model or the page rank algorithm. 

4. Graphical User Interface:
User interface where the user can enter their query and retrieve component will retrieve the top ten ranked documents and it will display it to the user in the UI elements. 
