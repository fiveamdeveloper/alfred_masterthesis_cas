from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from requests.auth import HTTPBasicAuth
import json
import model_inference
from model_inference import ModelInference
from load_models import load_spacy_model
import config
import urllib.parse

app = Flask(__name__)
CORS(app)

# Version aus Umgebungsvariablen abrufen
from config import VERSION, NER_VERSION

nlp = load_spacy_model(NER_VERSION)
model_inference_instance = ModelInference(VERSION)


# API Version 5
@app.route("/api/v1/predict", methods=["POST"])
def predict_v5():
    data = request.json
    text = data["content"]
    print("[alfred_api]:" + "Prompt:", text)
    entity = {}

    # Verwenden von Spacy für die Textverarbeitung
    doc = nlp(text)

    print("[alfred_api]: Prompt:", text)
    entity = model_inference.extract_entities(doc)
    print("[spaCy] Erkannte Entität:", entity)

    prompt_vector = model_inference_instance.vectorize_text(text)
    # Vorhersagen machen
    predictions = model_inference_instance.predict(prompt_vector)
    decoded_predictions = model_inference_instance.decode_predictions(predictions)

    # Request-Details aufbauen
    url, params, method = model_inference.build_request(
        config.BASE_URL, config.SAP_CLIENT, entity, decoded_predictions
    )

    # Request durchführen
    response = requests.get(
        url,
        params=urllib.parse.urlencode(params),
        auth=HTTPBasicAuth(config.username, config.password),
    )
    print("URL", response.url, response.status_code)

    if response.status_code == 200:
        data = response.json()
        print(data)
        print("[SAP API Response]:", data)
        print("decoded_prediction", decoded_predictions)

        def remove_metadata(obj):
            if isinstance(obj, dict):
                obj.pop("__metadata", None)  # Entfernt __metadata, falls vorhanden
                for key, value in obj.items():
                    remove_metadata(
                        value
                    )  # Rekursiver Aufruf für Werte, die selbst Dictionaries oder Listen sind
            elif isinstance(obj, list):
                for item in obj:
                    remove_metadata(
                        item
                    )  # Rekursiver Aufruf für jedes Element in der Liste

        if response.status_code == 200 and data:
            print(
                "[alfred-llm-connector]: Aufbereitung für Chatbot in LLM gestartet..."
            )

            headers = {
                "Authorization": f"Bearer {config.LLM_REMOTE_TOKEN}",
                "Content-Type": "application/json",
            }

            if config.REMOTE_LLM == True:
                llm_url = config.LLM_REMOTE_HOST
            else:
                llm_url = f"{config.LLM_HOST}:{config.LLM_PORT}/{config.LLM_ENDPOINT}"
            print("llm_url", llm_url)

            # remove_metadata(data["d"])
            sap_data = data.get("d")

            print("Data nach metadata removal", sap_data)
            generation_prompt = f"Using the provided data, generate a summary that is natural, clear, and easily understandable for non-technical users. The summary focuses on the essential details of the order without using technical jargon and answers this question/phrase: {text}. Do not repeat the question/phase, directly answer. Here is the data to summarize: {sap_data}."

            # generation_prompt = f"You are quesitoned: {text}. In response you received this data from an API Please generate a summary from the following exact ERP system data without altering any values. The summary should be in clear, plain language, understandable for non-technical users. It should focus on conveying the essential details of the order accurately, while avoiding technical jargon. ERP Data: {sap_data}. Emphasize clarity and accuracy in your summary. Answer in german."

            # generation_prompt = f"You are being asked for: '{text}'. In response you received the following data: {sap_data}. Please answer the questions you were asked for with the given data, without altering the values. The summary should be in clear, plain language, understandable for non-technical users. It should focus on conveying the essential details accurately, while avoiding technical jargon. Emphasize clarity and accuracy in your summary."

            # Wenn das Ergebnis in einer Tabelle auszugeben ist, dann soll die LLM eine Markdown Tabelle erstellen
            if decoded_predictions["presentation"] == "table":
                generation_prompt = f"You are being asked for: '{text}'. In response you received the following data: {sap_data}. Please answer the questions you were asked for with the given data, without altering the values. Prepare based von the given data a markdown table, without explaining what you did. Use the given keys in the JSON as header in the tables."

            print("generation_prompt", generation_prompt)

            if config.REMOTE_LLM == True:  # Remote LLM
                llm_data = json.dumps(
                    {
                        "inputs": generation_prompt,
                        "stream": False,
                    }
                )
            else:
                llm_data = json.dumps(  # Local LLM
                    {
                        "model": config.LLM_MODEL,
                        "prompt": generation_prompt,
                        "stream": False,
                    }
                )

            try:
                response = requests.post(
                    llm_url,
                    data=llm_data,
                    headers=headers,
                )

                if response.status_code == 200:
                    print("Erfolgreich:", response.text)
                    llm_response = response.json()

                    if config.REMOTE_LLM:
                        llm_response_el = llm_response[0].get("generated_text", "")
                        llm_response_mdl = "remote"
                    else:
                        llm_response_el = llm_response.get("response", "")
                        llm_response_mdl = llm_response.get("model", "")
                        print("LLM response:", llm_response.get("response", ""))

                    return jsonify(
                        {
                            "role": "assistant",
                            "content": llm_response_el,
                            "usedModels": {
                                "textGenModel": llm_response_mdl,
                                "alfredModel": f"v{config.VERSION}",
                            },
                            "sapApiData": data.get("d"),
                        }
                    )
                else:
                    return (
                        jsonify(
                            {
                                "error": "Ein Fehler beim Verbinden mit dem LLM-Connector ist aufgetreten .",
                                "details": f"Statuscode: {response.status_code}. Bitte versuchen Sie es später erneut oder kontaktieren Sie den Support.",
                                "role": "assistant",
                                "type": "danger",
                            }
                        ),
                        response.status_code,
                    )
            except requests.exceptions.RequestException as e:
                error_message = str(e).split(" for url:")[
                    0
                ]  # Behält nur den Fehlerstatus bei
                return (
                    jsonify(
                        {
                            "error": "Ein Fehler ist aufgetreten bei der Anfrage.",
                            "details": error_message,
                        }
                    ),
                    500,
                )
        else:
            return (
                jsonify(
                    {
                        "role": "assistant",
                        "content": f"Das hat leider nicht geklappt. Bitte versuche es erneut. {str(response)}",
                        "type": "danger",
                    }
                ),
                404,
            )
    else:
        return (
            jsonify(
                {
                    "role": "assistant",
                    "content": f"Das hat leider nicht geklappt. Bitte starte das LLM.",
                    "type": "danger",
                }
            ),
            404,
        )


if __name__ == "__main__":
    app.run(debug=True, port=3005)
