import os
import pickle
import pandas as pd
from Search_engine.Vocabulary import Vocabulary
from Search_engine.inverted import inverted_index
from preprocessing import first,write_pre
pd.set_option('display.max_colwidth', None)
from nltk import RegexpTokenizer

def vocabulary(field):
    '''
    It creates the vocabulary that links each word to a number.
    If field == True then it maps all the words inside the animeDescription section else it maps all the words from the document
    '''
    voc=Vocabulary()
    tokenizer = RegexpTokenizer(r'\w+')
    for file in os.listdir("/content/drive/My Drive/ADM-HW3/HW3/preprocessed_files/"):
        # Reads the preprocessed file
        dataframe=pd.read_csv("/content/drive/My Drive/ADM-HW3/HW3/preprocessed_files/"+file,sep="\t", index_col = [0])
        if field:
            reviews=dataframe["animeDescription"].to_string(index=False)
            token=tokenizer.tokenize(reviews)
            # It maps each tokenized word in animeDescription in a number
            for word in token:
                voc.add(word)
        else:
            # It maps each tokenized word in each section of the document in a number
            for index in dataframe:
                data_field=dataframe[index].to_string(index=False)
                if index in ["animeTitle","animeType","animeDescription","animeRelated","animeCharacters","animeVoices","animeStaff"]:
                    token=tokenizer.tokenize(data_field)
                    for word in token:
                        voc.add(word)
                else:
                    voc.add(data_field)
    # It writes the vocabulary on the disk
    voc.write()
    return voc

# It preprocesses each document and save it
def preprocessing_files():
    columns=["animeUrl","animeNumEpisode","releaseDate","endDate","animeNumMembers",
    "animeScore","animeUsers","animeRank","animePopularity"]
    for file in os.listdir("/content/drive/My Drive/ADM-HW3/HW3/tsvFiles/"):
        id_file=file.split("_")[1].strip(".tsv")
        dataframe=pd.read_csv("/content/drive/My Drive/ADM-HW3/HW3/tsvFiles/"+file,sep="\t")
        for index in dataframe:
            # If the column associated with the considered string is in the columns list we don't process it
            if index not in columns:
                stringOb=dataframe[index].to_string(index=False)
                dataframe[index] = " ".join(first(stringOb))
        with open("/content/drive/My Drive/ADM-HW3/HW3/preprocessed_files/"+id_file+".tsv","w") as f:
            dataframe.to_csv(f,sep="\t")
    
        
            

def inverted(Voc,field):
    # It creates the inverted index
    voc=inverted_index()
    tokenizer = RegexpTokenizer(r'\w+')
    for file in os.listdir("/content/drive/My Drive/ADM-HW3/HW3/preprocessed_files/"):
        id_file=file.strip(".tsv")
        dataframe=pd.read_csv("/content/drive/My Drive/ADM-HW3/HW3/preprocessed_files/"+file,sep="\t", index_col = [0])
        # If field == True creates the inverted index using only the words in animeDescription
        if field:
            reviews=dataframe["animeDescription"].to_string(index=False)
            token=tokenizer.tokenize(reviews)
            for word in token:
                word=Voc.myget(word)
                voc.add(word,id_file)
        else:
            # If field == False creates the inverted index using all the words in the document
            for index in dataframe:
                data_field=dataframe[index].to_string(index=False)
                if index in ["animeTitle","animeType","animeDescription","animeRelated","animeCharacters","animeVoices","animeStaff"]:
                    token=tokenizer.tokenize(data_field)
                    for word in token:
                        word=Voc.myget(word)
                        voc.add(word,id_file)
                else:
                    word=Voc.myget(data_field)
                    voc.add(word,id_file)
    voc.write()
    return voc




def And_query(query,check,field):
    ''' It computes the and query '''
    
    # It checks if vocabulary is in the dir
    if "vocabulary" in os.listdir("/content/drive/My Drive/ADM-HW3/HW3/"):
        voc=readVoc()
    else:
        voc=vocabulary(field)
    # It checks if inverted_index is in the dir
    if "inverted_index" in os.listdir("/content/drive/My Drive/ADM-HW3/HW3/"):
        vocI=readInv()
    else:
        vocI=inverted(voc,field)
    
    # It preprocesses the query
    query=first(query)
    f_set=set()
    # It intersects the sets of documents that contain each word
    for word in query:
        word=voc.myget(word)
        if len(f_set)==0:
            f_set.update(vocI.get_res(word))
        else:
            f_set=f_set.intersection(vocI.get_res(word))
    # It sorts the document in ascending order of comparison
    f_list=sorted(map(int,list(f_set)))
    # If check == True it prints the result
    if check:
        read_info(f_list)
    else:
        return f_list
    

def read_info(f_set):
    # It reads all the important informations from the files
    for file in f_set:
        with open("/content/drive/My Drive/ADM-HW3/HW3/tsvFiles/anime_"+str(file)+".tsv") as f:
            dataframe=pd.read_csv(f,sep="\t")
            title=dataframe["animeTitle"].to_string(index=False).strip(" - MyAnimeList.net")
            description =dataframe["animeDescription"].to_string(index=False)
            url=dataframe["animeUrl"].to_string(index=False)
            # Printing results
            print("title, {}\ndescription, {}\nurl, {}\n".format(title,description,url))


def readVoc():
    # It reads the created vocabulary
    with open("/content/drive/My Drive/ADM-HW3/HW3/vocabulary","rb") as f:
        voc=pickle.load(f)
    return voc 
    
    

def readInv():
    # It reads the created inverted index  
    with open("/content/drive/My Drive/ADM-HW3/HW3/inverted_index","rb") as f:
        voc=pickle.load(f)
    return voc
