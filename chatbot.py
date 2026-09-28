import re
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from faq_data import FAQ_DATA

CONFIDENCE_THRESHOLD = 0.34
FALLBACK_RESPONSE = "I could not find a confident answer in the FAQ knowledge base. Please try rephrasing your question or ask about a supported admission topic."

def ensure_nltk():
    for path,pkg in [("corpora/stopwords","stopwords"),("corpora/wordnet","wordnet"),("corpora/omw-1.4","omw-1.4")]:
        try: nltk.data.find(path)
        except LookupError: nltk.download(pkg, quiet=True)
ensure_nltk()
LEMMA=WordNetLemmatizer(); STOP=set(stopwords.words("english"))

def clean_text(text):
    text=re.sub(r"[^a-z0-9\s]"," ",str(text).lower())
    return " ".join(LEMMA.lemmatize(w) for w in text.split() if w not in STOP and len(w)>1)

faq_df=pd.DataFrame(FAQ_DATA)
faq_df["clean_question"]=faq_df["question"].map(clean_text)
word_vectorizer=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True)
char_vectorizer=TfidfVectorizer(analyzer="char_wb",ngram_range=(3,5),sublinear_tf=True)
word_vectors=word_vectorizer.fit_transform(faq_df["clean_question"])
char_vectors=char_vectorizer.fit_transform(faq_df["clean_question"])

def get_bot_response(user_question):
    cleaned=clean_text(user_question)
    if not cleaned:
        return {"answer":"Please enter a meaningful question.","matched_question":None,"category":None,"confidence_score":0.0,"is_confident":False,"status":"Empty question"}
    ws=cosine_similarity(word_vectorizer.transform([cleaned]),word_vectors).flatten()
    cs=cosine_similarity(char_vectorizer.transform([str(user_question).lower()]),char_vectors).flatten()
    scores=0.70*ws+0.30*cs
    idx=int(scores.argmax()); score=float(scores[idx])
    if score<CONFIDENCE_THRESHOLD:
        return {"answer":FALLBACK_RESPONSE,"matched_question":None,"category":None,"confidence_score":round(score,3),"is_confident":False,"status":"No confident FAQ match found"}
    row=faq_df.iloc[idx]
    return {"answer":row["answer"],"matched_question":row["question"],"category":row["category"],"confidence_score":round(score,3),"is_confident":True,"status":"Confident answer"}
