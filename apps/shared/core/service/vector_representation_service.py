from pathlib import Path
import numpy as np
import spacy
from gensim.models import KeyedVectors


DATA_DIR = Path(__file__).resolve().parent


class VectorRepresentationService:
    def __init__(self):
        self._text_analyzer = spacy.load("en_core_web_sm")
        self._w2v_model = KeyedVectors.load_word2vec_format(
            fname=f"{DATA_DIR}/data/GoogleNews-vectors-negative300.bin", binary=True
        )

    def get_representation(self, text: str):
        tokens = self._text_analyzer(text)
        lemmatized_words = [
            token.lemma_ for token in tokens if not token.is_stop and not token.is_punct
        ]
        return self._vectorize_words_list(lemmatized_words=lemmatized_words)

    def _vectorize_words_list(self, lemmatized_words: list[str]):
        word_vectors = [
            self._w2v_model[word]
            for word in lemmatized_words
            if word in self._w2v_model
        ]
        if not word_vectors:
            return np.zeros(self._w2v_model.vector_size)
        return np.mean(word_vectors, axis=0)


if __name__ == "__main__":
    documents = [
        "The cat is on the mat.",
        "Dogs are in the yard.",
        "Birds are flying in the sky.",
    ]
    service = VectorRepresentationService()
    result = []
    for document in documents:
        result.append(service.get_representation(document))

    print(result)
