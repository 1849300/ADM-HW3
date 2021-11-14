from nltk import RegexpTokenizer, SnowballStemmer
from nltk.corpus import stopwords


def first(t):
    # It tokenizes the string
    tokenizer = RegexpTokenizer(r'\w+')
    token=tokenizer.tokenize(t)
    words = []
    for  p in range(len(token)):
        # It checks if there are stopwords
        if token[p] not in stopwords.words('english') and  token[p] not in ["MyAnimeList","net"]:
            words.append(token[p])
    # It stemmes the words
    snowball = SnowballStemmer(language='english')
    res=[]
    for p in words:
        t = snowball.stem(p)
        res.append(t)
    return res



def write_pre(text,name):
    # It writes a dataframe (preprocessed text)
    id_doc=int(name.split("_")[1].strip(".tsv"))
    with open ("/content/drive/My Drive/ADM-HW3/HW3/preprocessed_files/"+str(id_doc)+".tsv","w") as f:
        text.to_csv(f,sep="\t")