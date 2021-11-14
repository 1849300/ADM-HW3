# ADM-HW3
Third homework of the ADM course

Group members:
- Boesso Simone
- Conti Andrea
- Napoli Mario
- Zeynalpour Sara

## Module description
Our repository contains main.ipynb that is our notebook with practical and algorithmic solutions.
The repository contains also the modules we used to accomplish the requested tasks,let's describe all of them more in details:
- Parse_Urls: we import it in order to download and save in a file all the links we have to use to download pages;
- FilesLoad: we use it to download and save all the html pages whose links were previously stored (each member of the group made this step in parallel with others);
- Html_Parse: we use this module to parse the html code of the pages in order to obtain tsv files;
- preprocessing: this module allows us to process all the strings we want (tokenizing, removing stopwords, stemming etc.);
- Search_engine: this module contains more than one file:
  - init.py: it contains all the functions to make the first conjunctive query and it also call the functions to build vocabulary and inverted index;
  - Vocabulary.py: create the object 'Vocabulary' (that contains the vocabulary) and defines all the operations we can do with this object;
  - inverted.py: create the object 'inverted' (that contains the inverted index) and defines all the operations we can do with this object;
  - Search_engine2.py: it defines all the stuff necessary to make the second query with cosine similarity;
  - Search_engine3.py: this module allows us to define our score function and to sort the resulting documents with our parameters.
  

For any problem, please, contact us to the emails related with this repository.
