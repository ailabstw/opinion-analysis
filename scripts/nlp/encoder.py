import tensorflow_text
import tensorflow_hub as hub

from typing import List
from transformers import AutoModel, AutoTokenizer

USE_MODEL_PATH = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"


class USEEncoder:

    def __init__(self, model_path=USE_MODEL_PATH):
        self.embed = hub.load(model_path)

    def encode(self, texts: List[str]):
        embeddings = self.embed(texts).numpy()
        return embeddings
