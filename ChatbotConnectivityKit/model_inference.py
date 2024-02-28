from load_models import get_models
import config
import sklearn
import numpy as np
import json
from keras.models import load_model
from load_models import get_models
import pandas as pd
import re


print("[model_inference.py] scikit-learn Version: ", sklearn.__version__)
import os

models_and_encoders = get_models(config.VERSION)


def extract_entities(doc):
    """Extrahiert Entities aus dem Dokument."""
    return {ent.label_: ent.text for ent in doc.ents}


def get_model_capabilities(version):
    with open("model_capabilities.json", "r") as file:
        model_capabilities = json.load(file)
    return model_capabilities.get(version, {}).get("features", {})


models_and_encoders = get_models(config.VERSION)


class ModelInference:
    def __init__(self, version):
        self.models_and_encoders = get_models(version)
        self.vectorizer = self.models_and_encoders.get("vectorizer")
        # Direkte Verwendung der geladenen Modelle basierend auf den Fähigkeiten
        self.model = self.models_and_encoders.get(
            "neural_network"
        ) or self.models_and_encoders.get("chain_model")
        self.encoders = {
            key: value
            for key, value in self.models_and_encoders.items()
            if key.endswith("_encoder")
        }

    def clean_text(self, text):
        # Überprüfen auf NaN-Werte
        if pd.isna(text):
            return text
        # Entfernen von Sonderzeichen und Ziffern, behalten von Leerzeichen und Buchstaben
        text = re.sub(r"[^A-Za-zäöüßÄÖÜ\s]", "", text)
        # Umwandlung in Kleinbuchstaben
        text = text.lower()
        # Ersetzen mehrfacher Leerzeichen durch ein einzelnes Leerzeichen
        text = re.sub(r"\s+", " ", text)
        # Entfernen von Leerzeichen am Anfang und Ende
        text = text.strip()
        return text

    def vectorize_text(self, text):
        if not self.vectorizer:
            print("Fehler: Vectorizer ist nicht geladen.")
            return None
        cleaned_text = self.clean_text(text)
        return self.vectorizer.transform([cleaned_text]).toarray()

    def predict(self, vectorized_text):
        if not self.model:
            print("Fehler: Kein Modell geladen.")
            return None
        # Verwenden von predict für neuronale Netzwerke und Classifier Chains
        return self.model.predict(vectorized_text)

    def decode_predictions(self, predictions):
        decoded = {}

        # Single-Label-Vorhersagen interpretieren
        decoded["method"] = self.encoders["method_encoder"].inverse_transform(
            np.argmax(predictions[0], axis=1).reshape(-1)
        )[0]
        decoded["endpoint"] = self.encoders["endpoint_encoder"].inverse_transform(
            np.argmax(predictions[1], axis=1).reshape(-1)
        )[0]
        decoded["presentation"] = self.encoders[
            "presentation_encoder"
        ].inverse_transform(np.argmax(predictions[2], axis=1).reshape(-1))[0]

        threshold = 0.5

        # Multi-Label-Vorhersagen interpretieren
        decoded["required"] = self.encoders["required_encoder"].inverse_transform(
            (predictions[3] > threshold).astype(int)
        )[0]
        decoded["select"] = self.encoders["select_encoder"].inverse_transform(
            (predictions[4] > threshold).astype(int)
        )[0]
        decoded["filter"] = self.encoders["filter_encoder"].inverse_transform(
            (predictions[5] > threshold).astype(int)
        )[0]
        decoded["expand"] = self.encoders["expand_encoder"].inverse_transform(
            (predictions[6] > threshold).astype(int)
        )[0]
        decoded["expand_select"] = self.encoders[
            "expand_select_encoder"
        ].inverse_transform((predictions[7] > threshold).astype(int))[0]

        print(["decoded parameters"], decoded)

        return decoded


def build_request(base_url, client, entity, decoded_prediction):
    # Initialisiere 'endpoint' und 'required_entity' sicher
    method = decoded_prediction.get("method", ["GET"])
    endpoint = decoded_prediction.get("endpoint", [""])
    required = decoded_prediction.get("required", [[]])

    if required and entity:
        key, value = next(iter(entity.items()), ("", ""))
        endpoint = f"{endpoint}('{value}')"
    else:
        print(
            f"[model_inference.py] required {required} oder entity {entity} wurde nicht erkannt."
        )

        exit

    full_url = f"{base_url}{endpoint}"
    # print("full_url", full_url)

    # Parameter für den Request aufbauen
    params = {"sap-client": client, "$format": "json"}

    # expand Parameter aufbauen, wenn vorhanden und nicht leer
    if decoded_prediction.get("expand"):
        expand_values = decoded_prediction["expand"]
        expand_param = ",".join(expand_values)
        params["$expand"] = expand_param if expand_param else None

    # select Parameter aufbauen, wenn vorhanden und nicht leer
    if decoded_prediction.get("select"):
        select_values = decoded_prediction["select"]
        select_param = ",".join(select_values)
        params["$select"] = select_param if select_param else None

    # filter Parameter aufbauen, wenn vorhanden und nicht leer
    if decoded_prediction.get("filter"):
        filter_values = decoded_prediction["filter"]
        filter_param = ",".join(filter_values)
        params["$filter"] = filter_param if filter_param else None

    # print(full_url, params, method)

    return full_url, params, method
