from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from db_utils import get_latest_health_data

# Initialize model
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

# --- General advice embeddings ---
general_advice = [
    "Paracetamol is used for fever and pain.",
    "Normal heart rate is 60-100 bpm.",
    "Normal blood pressure is 90/60 to 120/80 mmHg.",
    "Older adults should stay hydrated.",
    "Regular walking improves cardiovascular health.",
]
advice_docs = [Document(page_content=txt) for txt in general_advice]
advice_store = FAISS.from_documents(advice_docs, embedding_model)
advice_store.save_local("faiss_advice")

# --- User-specific health data embeddings ---
user_id = "user_1"
data = get_latest_health_data(user_id)
if data:
    heart_rate, systolic, diastolic, timestamp = data
    user_text = f"User {user_id} has heart rate {heart_rate} bpm, systolic {systolic} mmHg, diastolic {diastolic} mmHg. Recorded on {timestamp}."
    user_store = FAISS.from_texts([user_text], embedding_model)
    user_store.save_local("faiss_user_data")
else:
    print(f"No data found for {user_id}")
