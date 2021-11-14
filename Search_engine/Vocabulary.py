import pickle


class Vocabulary:
    # It contains all the words mapped to numbers
    def __init__(self):
        # Creation on the object
        self.name="vocabulary"
        self.dict={}
        self.number=0

    def add(self, word):
        # Adds element to the object self
        if word not in self.dict:
            self.dict[word]=self.number
            self.number+=1

    def myget(self,word):
        # It returns the number associated with the given word
        return self.dict[word]

    def write(self):
        # It writes the object self in a binary file
        with open("/content/drive/My Drive/ADM-HW3/HW3/"+self.name,"wb") as f:
            pickle.dump(self,f)

    def print(self):
        # It prints the dictionary inside the object self
        print(self.dict)

    def getKeys(self):
        # It returns the keys of the dictionary inside self
        return self.dict.keys()
    
    def getValues(self):
        # It returns the values of the dictionary inside self
        return self.dict.values()