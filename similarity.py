# similarity.py
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# BERT modelini yükle
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# BERT embedding'lerini al
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# Makaleler arasındaki benzerlikleri hesapla
def calculate_similarities(papers):
    embeddings = [get_bert_embedding(paper['Description']) for paper in papers]
    similarity_matrix = cosine_similarity(embeddings)

    # Benzerlik skorlarını çıkart ve sıralama
    similarities = [
        {
            "paper_id": paper['Id'],
            "other_paper_id": other_paper['Id'],
            "similarity_score": similarity_matrix[i][j]
        }
        for i, paper in enumerate(papers)
        for j, other_paper in enumerate(papers)
        if i != j
    ]
    return sorted(similarities, key=lambda x: x['similarity_score'], reverse=True)