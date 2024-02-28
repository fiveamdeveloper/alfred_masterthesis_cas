# config.py
from dotenv import load_dotenv
import os

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Laden der neuen Modellversionen und LLM-Modellkonfiguration
# Version aus Umgebungsvariablen abrufen
VERSION = "5g2"  # os.getenv("MODEL_VERSION")
NER_VERSION = os.getenv("NER_VERSION")
LLM_MODEL = os.getenv("LLM_MODEL")

# SAP-Konfiguration
SAP_HOST = os.getenv("SAP_HOST")
SAP_PORT = os.getenv("SAP_PORT")
SAP_CLIENT = os.getenv("SAP_CLIENT")
SAP_SERVICE_URL = os.getenv("SAP_SERVICE_URL")
BASE_URL = f"{SAP_HOST}:{SAP_PORT}{SAP_SERVICE_URL}/"

# SAP-Zugangsdaten
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# LLM-Konfiguration
REMOTE_LLM = True
LLM_REMOTE_HOST = os.getenv("LLM_REMOTE_HOST")
LLM_REMOTE_TOKEN = os.getenv("LLM_REMOTE_TOKEN")
LLM_HOST = os.getenv("LLM_HOST")
LLM_PORT = os.getenv("LLM_PORT")
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT")

print(f"[config.py] VERSION: {VERSION}, NER_VERSION: {NER_VERSION}")
