import os
import spacy
import json
from dotenv import load_dotenv
import pickle

# import tensorflow as tf
from keras.models import load_model

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Version aus Umgebungsvariablen abrufen
from config import VERSION


# Laden der Modellfähigkeiten
def load_model_capabilities():
    with open("model_capabilities.json") as f:
        return json.load(f)


model_capabilities = load_model_capabilities()


def load_spacy_model(NER_VERSION):
    try:
        nlp = spacy.load(f"./output/v{NER_VERSION}/model-best")
        print(f"[load_models.py]: Spacy model version {NER_VERSION} loaded")
        return nlp
    except Exception as e:
        print(f"[load_models.py]: Error loading Spacy model: {e}")
        return None


def get_models(version):
    base_directory = "./"

    # Pfad und Fähigkeiten basierend auf der Konfiguration laden
    capabilities_path = os.path.join(base_directory, "model_capabilities.json")
    with open(capabilities_path, "r") as f:
        capabilities = json.load(f).get("model-" + version, {})

    if not capabilities:
        raise ValueError(f"Keine Fähigkeiten für Modellversion {version} definiert.")

    # Entscheiden, welcher Modelltyp basierend auf den Fähigkeiten geladen wird
    if capabilities.get("is_chain_model"):
        model_directory = os.path.join(base_directory, "clf_model", version)
    elif capabilities.get("is_neural_network_model"):
        model_directory = os.path.join(base_directory, "nn_model", version)
    else:
        raise ValueError("Unbekannter Modelltyp in den Fähigkeiten definiert.")

    models_and_encoders = {}

    # TfidfVectorizer laden
    vectorizer_path = os.path.join(model_directory, f"tfidf_vectorizer-v{version}.pkl")
    with open(vectorizer_path, "rb") as file:
        models_and_encoders["vectorizer"] = pickle.load(file)

    # Entscheidung basierend auf capabilities
    if capabilities.get("is_chain_model"):
        # Laden der Classifier Chain
        chain_model_path = os.path.join(
            model_directory, f"classifier_chain-v{version}.pkl"
        )
        with open(chain_model_path, "rb") as file:
            models_and_encoders["chain_model"] = pickle.load(file)
    elif capabilities.get("is_neural_network_model"):
        # Laden des neuronalen Netzwerks
        # Pfad zum gespeicherten Modell und den Komponenten
        model_directory = f"./nn_model/{VERSION}"

        # Modell laden
        model_filename = (
            f"{base_directory}nn_model/{VERSION}/neural_network-v{VERSION}.h5"
        )
        models_and_encoders["neural_network"] = load_model(model_filename)
        # models_and_encoders["neural_network"] = tf.keras.models.load_model(
        #    f"{model_directory}/neural_network-v{version}.keras"
        # )

    # Encoder basierend auf den Fähigkeiten laden
    encoder_features = [
        "select",
        "required",
        "filter",
        "expand",
        "expand_select",
        "method",
        "endpoint",
        "presentation",
    ]
    for feature in encoder_features:
        if capabilities.get(
            feature
        ):  # Überprüfen, ob das Feature in den Fähigkeiten enthalten ist
            encoder_name = f"{feature}_encoder"
            encoder_path = os.path.join(
                model_directory, f"{encoder_name}-v{version}.pkl"
            )
            try:
                with open(encoder_path, "rb") as file:
                    models_and_encoders[encoder_name] = pickle.load(file)
            except FileNotFoundError:
                print(f"Encoder {encoder_name} für Version {version} nicht gefunden.")

    return models_and_encoders
