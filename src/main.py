import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chat_agent import ChatAgent
from vector_db.chroma_db import ChromaDB
from log_parser.accrossa_parser import parse_accrossa_log
from log_parser.axiom_parser import parse_axiom_log
from log_parser.e2fa_parser import parse_e2fa_log

def main():
    # Initialize the vector database with embedding model
    vector_db = ChromaDB(persist_directory="../vector_db", embedding_model="nomic-embed-text")

    # Dynamically resolve log file paths relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    accossa_path = os.path.join(base_dir, '../logs/accossa.txt')
    axiom_path = os.path.join(base_dir, '../logs/Axiom.txt')
    e2fa_path = os.path.join(base_dir, '../logs/e2fa.txt')

    # Parse log files and store details in the vector database
    accossa_data = parse_accrossa_log(accossa_path)
    axiom_data = parse_axiom_log(axiom_path)
    e2fa_data = parse_e2fa_log(e2fa_path)

    # Ingest each log into the vector DB (chunked), passing status and timestamp as metadata
    for orn, details in accossa_data.items():
        status = details.get("status")
        timestamp = details.get("timestamp")
        vector_db.chunk_and_store_logs(orn, str(details), "accossa", status=status, timestamp=timestamp)
    for orn, details in axiom_data.items():
        status = details.get("status")
        timestamp = details.get("timestamp")
        vector_db.chunk_and_store_logs(orn, str(details), "axiom", status=status, timestamp=timestamp)
    for orn, details in e2fa_data.items():
        status = details.get("status")
        timestamp = details.get("timestamp")
        vector_db.chunk_and_store_logs(orn, str(details), "e2fa", status=status, timestamp=timestamp)

    print("Log data ingested into Chroma vector DB.")

if __name__ == "__main__":
    main()