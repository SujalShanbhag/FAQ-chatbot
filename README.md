# FAQ Chatbot — Enhanced Black & Blue Theme

Enhanced from the uploaded FAQ chatbot. The original Streamlit architecture and NLP approach are retained, while the interface uses a black + blue dashboard style and the FAQ knowledge base is expanded substantially.

## Included
- Black + blue gradient dashboard
- Clearly separated cards and visible borders
- 200+ university admission FAQ questions
- Multiple categories and sample questions
- NLTK preprocessing: cleanup, stopword removal, lemmatization
- Word-level TF-IDF + character n-gram TF-IDF
- Cosine similarity and confidence threshold
- Chat history and clear history
- No paid AI API

## Run
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

## Customize
Edit `faq_data.py` to add, remove or update questions. Restart Streamlit after changes. The dataset is intentionally kept separate from the matching logic.
