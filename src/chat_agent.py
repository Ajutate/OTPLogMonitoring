from log_parser.accrossa_parser import parse_accrossa_log
from log_parser.axiom_parser import parse_axiom_log
from log_parser.e2fa_parser import parse_e2fa_log
from vector_db.chroma_db import ChromaDB
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA

SYSTEM_PROMPT = (
    "You are an expert log monitoring assistant. "
    "When a user asks for the OTP journey of a specific ORN number, "
    "provide the complete journey of OTP generation using the following flow: "
    "1. Generate OTP: show success/fail status and time for generation request. "
    "2. OTP send: show success/fail status and time of OTP send. "
    "3. OTP verification: show success/fail status and time. "
    "Summarize the journey in this order and be concise."
)

class ChatAgent:
    def __init__(self, ollama_model, embedding_model, vector_db_path):
        self.llm = Ollama(model=ollama_model)
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.vector_db = ChromaDB(persist_directory=vector_db_path, embedding_model=embedding_model)
        # Remove as_retriever and LLM chain, since only deterministic method is used

    def get_response(self, query):
        # Extract ORN from anywhere in the query string (even in a sentence)
        import re
        match = re.search(r'(\d{12,})', str(query))
        print("Match found:", match)
        if match:
            orn = match.group(1)
            print("ORN found:", orn)
            return self.get_otp_journey_by_orn_formatted(orn)
        else:
            return "Please provide a valid ORN number in your query."

    def get_otp_journey_by_orn(self, orn: str):
        # Use metadata search for each log type
        accossa_chunks = self.vector_db.metadata_search(orn, log_type="accossa", k=10)
        axiom_chunks = self.vector_db.metadata_search(orn, log_type="axiom", k=10)
        e2fa_chunks = self.vector_db.metadata_search(orn, log_type="e2fa", k=10)
        return {
            "accossa": accossa_chunks,
            "axiom": axiom_chunks,
            "e2fa": e2fa_chunks
        }

    def format_otp_journey(self, orn: str):
        journey = self.get_otp_journey_by_orn(orn)
        def extract_status_and_time(chunks):
            if not chunks or not hasattr(chunks[0], 'page_content'):
                return ("Not found", "-")
            # Try to extract status and timestamp from the chunk content or metadata
            for doc in chunks:
                meta = getattr(doc, 'metadata', {})
                content = getattr(doc, 'page_content', '')
                status = meta.get('status') or ("Success" if "Success" in content else "Fail" if "Fail" in content else "Unknown")
                timestamp = meta.get('timestamp')
                if not timestamp:
                    # Try to extract timestamp from content
                    import re
                    match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', content)
                    timestamp = match.group(1) if match else "-"
                return (status, timestamp)
            return ("Not found", "-")
        gen_status, gen_time = extract_status_and_time(journey["accossa"])
        send_status, send_time = extract_status_and_time(journey["axiom"])
        ver_status, ver_time = extract_status_and_time(journey["e2fa"])
        return f"ORN -{orn}\nGeneration: {gen_status} {gen_time}\nSend: {send_status} {send_time}\nVerification: {ver_status} {ver_time}"

    def get_otp_journey_by_orn_formatted(self, orn: str):
        # Use metadata search for each log type
        accrossa_chunks = self.vector_db.metadata_search(orn, log_type="accossa", k=10)
        axiom_chunks = self.vector_db.metadata_search(orn, log_type="axiom", k=10)
        e2fa_chunks = self.vector_db.metadata_search(orn, log_type="e2fa", k=10)

        def extract_status_and_time(chunks, default_status="Not found", default_time="-"):
            if not chunks or not hasattr(chunks[0], 'page_content'):
                return (default_status, default_time)
            for doc in chunks:
                meta = getattr(doc, 'metadata', {})
                content = getattr(doc, 'page_content', '')
                # Try to extract status and timestamp from metadata or content
                status = meta.get('status') or ("Success" if "Success" in content else "Failed" if "Fail" in content else "Unknown")
                timestamp = meta.get('timestamp')
                if not timestamp:
                    import re
                    match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', content)
                    timestamp = match.group(1) if match else "-"
                return (status, timestamp)
            return (default_status, default_time)

        gen_status, gen_time = extract_status_and_time(accrossa_chunks, default_status="Failed")
        send_status, send_time = extract_status_and_time(axiom_chunks, default_status="Failed")
        ver_status, ver_time = extract_status_and_time(e2fa_chunks, default_status="Failed")
        
        print(f"ORN -{orn}\nGeneration: {gen_status} {gen_time}\nSend: {send_status} {send_time}\nVerification: {ver_status} {ver_time}")
        # If all are not found or failed, show generic message
        if (gen_status in ["Not found", "Failed"] and send_status in ["Not found", "Failed"] and ver_status in ["Not found", "Failed"]):
            return f"No OTP journey found for ORN {orn}. Please check the ORN and try again."
        return f"ORN -{orn}\nGeneration: {gen_status} {gen_time}\nSend: {send_status} {send_time}\nVerification: {ver_status} {ver_time}"