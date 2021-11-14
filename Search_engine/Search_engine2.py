import pandas as pd
from nltk import RegexpTokenizer
from preprocessing import first
import numpy as np
import heapq
from numpy.linalg import norm
import pickle
import os
np.set_printoptions(suppress=True)
import Search_engine as se

def index(f_list,voc,vocI, field):
    ''' It creates the index dictionary where the keys are the document ids and the values are the list composed by tuples (e.g. (id_term, tdfIf))
    '''
    llen=len(os.listdir("/content/drive/My Drive/ADM-HW3/HW3/preprocessed_files"))
    # It creates the index
    index={}
    tokenizer = RegexpTokenizer(r'\w+')
    # It iterates on each document in the list
    for id_doc in f_list:
        doc={}
        # It inserts all the words in the vocabulary
        for word_voc in voc.getKeys():
            doc[voc.myget(word_voc)]=0
        # It opens each file and creates the vector with all the words on each documents
        with open("/content/drive/My Drive/ADM-HW3/HW3/preprocessed_files/"+str(id_doc)+".tsv","r") as f:
            dataframe=pd.read_csv(f,sep="\t", index_col = [0])
            # If field == true takes only words in animeDescription
            if field:
                animeDescription=dataframe["animeDescription"].to_string(index=False)
                token=tokenizer.tokenize(animeDescription)
                for word in token:
                    word=voc.myget(word)
                    doc[word]=doc[word]+1
            else:
                # If field == false takes all the words from the document
                for ind in dataframe:
                    data_field=dataframe[ind].to_string(index=False)
                    if ind in ["animeTitle","animeType","animeDescription","animeRelated","animeCharacters","animeVoices","animeStaff"]:
                        token=tokenizer.tokenize(data_field)
                        for word in token:
                            word=voc.myget(word)
                            doc[word]=doc[word]+1
                    else:
                        word=voc.myget(data_field)
                        doc[word]=doc[word]+ 1
        # It sorts the vector
        vec=sorted(list(doc.items()),key=lambda x: x[0])
        for pos in range(len(vec)):
            #tf * idf(t)
            valuetf=vec[pos][1]/len(token)
            valueidf=llen/len(vocI.get_res(vec[pos][0]))
            vec[pos]=(vec[pos][0],valuetf*valueidf)
        # It inserts it in the index
        index[id_doc]=vec
    write_index(index)
    return index

# It writes the index
def write_index(index):
    with open("/content/drive/My Drive/ADM-HW3/HW3/freq_index","wb") as f:
        pickle.dump(index,f)
        
#it reads the index    
def readIndex():
    with open("/content/drive/My Drive/ADM-HW3/HW3/freq_index","rb") as f:
        voc=pickle.load(f)
    return voc 
    
def cosineVectors(query,index,voc,vocI,k):
    doc={}
    llen=len(os.listdir("/content/drive/My Drive/ADM-HW3/HW3/preprocessed_files"))
    #it creates an array of dimension k
    li=[]
    #it creates the min heap
    heapq.heapify(li)
    #it preprocess the query
    query=first(query)
    #it creates the vector that corrisponds to the query 
    for word_voc in voc.getKeys():
        doc[voc.myget(word_voc)]=0
    #it add the words in the vector
    for word in query:
        #it gets the id_term
        word=voc.myget(word)
        doc[word]=doc[word]+1
    #it sorts the array
    vec=sorted(np.asarray(list(doc.items())),key=lambda x: x[0])
    #it creates the frequency of each word in the query
    for pos in range(len(vec)):
            #tf * idf(t)
            valuetf=vec[pos][1]/len(query)
            valueidf=llen/len(vocI.get_res(vec[pos][0]))
            vec[pos]=(vec[pos][0],valuetf*valueidf)
    for index_doc in index.keys():
        # doc is the vectorized document (only values)
        doc = zip(*index[index_doc])
        doc= list(doc)[1]
        # query is the vectorized query
        query = zip(*vec)
        query= list(query)[1]
        distance=cosine(query,doc)
        if len(li)<k:
            heapq.heappush(li,(distance,index_doc))
        elif li[0][0]<distance:
            heapq.heappop(li)
            heapq.heappush(li,(distance,index_doc))
    
    # It gets the first k docs
    final=[]
    if len(list(index.keys()))<k:
        k=len(index.keys())
    for i in range(k):
        distance,index_doc=heapq.heappop(li)
        if distance!=0:
            final.append((distance,index_doc))
    final.sort(key=lambda x:x[0],reverse=True)
    return final

            
# It computes the cosine similarity between 2 vectors
def cosine(query,doc):
    cosine = np.dot(query, doc)/(norm(query)*norm(doc))
    return cosine
        
# It gets all the infos giving in input the query and the k
def Query_AndFreq(query,field, check, k):
    # It calls the And_query to get back the set of documents with the words we are looking for
    set = se.And_query(query,False, field)
    # It calls the needed dictionaries
    vocI=se.readInv()
    voc=se.readVoc()
    inverted_index=index(set,voc,vocI, field)
    final=cosineVectors(query,inverted_index,voc,vocI,k)
    if check:
        read_info(final)
    else:
        return final
        


# It reads all the important infos
def read_info(f_set):
    for sim,id_doc in f_set:
        with open("/content/drive/My Drive/ADM-HW3/HW3/tsvFiles/anime_"+str(id_doc)+".tsv") as f:
            dataframe=pd.read_csv(f,sep="\t")
            title=dataframe["animeTitle"].to_string(index=False).strip(" - MyAnimeList.net")
            description =dataframe["animeDescription"].to_string(index=False)
            url=dataframe["animeUrl"].to_string(index=False)
            # Print the results
            print("title, {}\ndescription, {}\nurl, {}\nSimilarity, {}\n".format(title,description,url,sim))


