from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
import torch
import re
import emoji
import unicodedata
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

device = "cuda" if torch.cuda.is_available() else "cpu"
text_model = SentenceTransformer("intfloat/e5-base", device=device)


def preprocess_text(text):
    text = emoji.replace_emoji(text, replace='')
    text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C')
    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text)
    filtered = [w for w in words if w not in stop_words]

    return " ".join(filtered)


def get_text_embedding(text):
    clean_text = preprocess_text(text)
    emb = text_model.encode(clean_text, convert_to_numpy=True, normalize_embeddings=True)
    return emb.tolist()


class TextEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [get_text_embedding(text) for text in texts]

    def embed_query(self, text):
        return get_text_embedding(text)
