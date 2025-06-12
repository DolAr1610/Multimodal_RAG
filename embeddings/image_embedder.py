from transformers import AutoProcessor, AutoModel
from PIL import Image
from io import BytesIO
import torch
import requests

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModel.from_pretrained("openai/clip-vit-large-patch14-336").to(device)
processor = AutoProcessor.from_pretrained("openai/clip-vit-large-patch14-336")


def get_image_embedding(image_url):
    try:
        response = requests.get(image_url, timeout=10)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        inputs = processor(images=img, return_tensors="pt").to(device)
        with torch.no_grad():
            emb = model.get_image_features(**inputs)
        emb = emb / emb.norm(p=2, dim=-1, keepdim=True)
        return emb[0].cpu().numpy().tolist()
    except Exception as e:
        print(f"Image loading failed: {e}")
        return None


def get_text_embedding_clip(text_query):
    inputs = processor(text=[text_query], return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        emb = model.get_text_features(**inputs)
    emb = emb / emb.norm(p=2, dim=-1, keepdim=True)
    return emb[0].cpu().numpy().tolist()
