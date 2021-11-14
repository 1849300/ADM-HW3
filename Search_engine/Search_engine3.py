import heapq
import pandas as pd
from nltk import RegexpTokenizer

def get_weights(section,query,word):
    '''It assigns a weight to a given word inside the anime document that is also inside the query.
        The weight depends on the section of the anime in which the word appears.'''
    if  word in query:
        if section=="animeTitle":
            return 10
        elif section=="animeCharacters":
            return 8
        elif section=="animeStaff":
            return 5
        elif section=="animeVoices":
            return 4
    return 0
    
def rank(s,query,k):
    '''It ranks each document using the custom weights and the popularity of each anime. '''
    li=[]
    #it creates the min heap
    heapq.heapify(li)
    # Tokenizing the query
    tokenizer = RegexpTokenizer(r'\w+')
    query=tokenizer.tokenize(query)
    for freq,doc in s:
        value=0
        with open("/content/drive/My Drive/ADM-HW3/HW3/preprocessed_files/"+str(doc)+".tsv") as f:
            dataframe=pd.read_csv(f,sep="\t",index_col=[0])
            for ind in dataframe:
                # It takes a specific field of the file
                data_field=dataframe[ind].to_string(index=False)
                # It tokenizes words in the following sections, else it just increments the value without tokenizing (e.g. date)
                if ind in ["animeTitle","animeType","animeDescription","animeRelated","animeCharacters","animeVoices","animeStaff"]:
                    token=tokenizer.tokenize(data_field)
                    for word in token:
                        t=get_weights(ind,query,word)
                        value+=t
                else:
                    t=get_weights(ind,query,word)
                    value+=t
        # It creates the k-values minheap
        if len(li)<k:
            heapq.heappush(li,(doc,value))
        elif li[0][0]<value:
            heapq.heappop(li)
            heapq.heappush(li,(doc,value))
    final=[]
    # It ensures a correct value for k
    if k>len(li):
        k=len(li)
    # It appends the results to the final list
    for i in range(k):
        doc,value=heapq.heappop(li)
        final.append((doc,value))
    # Ordering results
    final.sort(key=lambda x:(-x[1],x[0]))
    read_info(final)
    return final


def read_info(f_set):
    # It reads and prints all the important infos
    for id_doc, sim in f_set:
        with open("/content/drive/My Drive/ADM-HW3/HW3/tsvFiles/anime_"+str(id_doc)+".tsv") as f:
            dataframe=pd.read_csv(f,sep="\t")
            title=dataframe["animeTitle"].to_string(index=False).strip(" - MyAnimeList.net")
            description =dataframe["animeDescription"].to_string(index=False)
            url=dataframe["animeUrl"].to_string(index=False)
            # Print the results
            print("title, {}\ndescription, {}\nurl, {}\nSimilarity, {}\n".format(title,description,url,sim))
                    