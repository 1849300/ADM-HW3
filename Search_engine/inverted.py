import pickle
from preprocessing import first

class inverted_index():
    # It contains all the id terms associated with the ids of the documents that contain that term
    def __init__(self):
        self.name="inverted_index"
        # the inverted index
        self.dict={}
        


    # It adds a document inside the postings
    def add(self,id_term,id_doc):
        if id_term not in self.dict:
            self.dict[id_term]=set()
            self.dict[id_term].add(id_doc)
        else:
            self.dict[id_term].add(id_doc)


    # It returns the posting given a id_term
    def get_res(self,id_term):
        return self.dict[id_term]

    # It prints the index
    def print(self):
        print(self.dict)

    # It writes the index
    def write(self):
        with open("/content/drive/My Drive/ADM-HW3/HW3/"+self.name,"wb") as f:
            pickle.dump(self,f)


