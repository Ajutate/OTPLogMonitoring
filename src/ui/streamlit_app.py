import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from chat_agent import ChatAgent
from vector_db.chroma_db import ChromaDB


def main():
    st.title("Agentic RAG Log Monitoring Chat Agent")

    # Initialize chat agent with Ollama and LangChain only once per session
    if "chat_agent" not in st.session_state:
        st.session_state.chat_agent = ChatAgent(
            ollama_model="llama3",  # or any Ollama-supported model
            embedding_model="nomic-embed-text",  # Ollama embedding model
            vector_db_path="../vector_db"  # path to your ChromaDB or similar
        )

    # Add a sidebar for navigation
    page = st.sidebar.selectbox("Select Page", ["Chat", "Vector DB Viewer"])

    if page == "Chat":
        user_input = st.text_input("Ask about the OTP journey of a specific ORN number:")
        if st.button("Submit"):
            if user_input:
                # Use the get_response method for deterministic chat
                response = st.session_state.chat_agent.get_response(user_input)
                st.text_area("Response:", value=response, height=300)
            else:
                st.warning("Please enter an ORN number to query.")
    elif page == "Vector DB Viewer":
        st.header("Vector DB Data Viewer")
        vector_db = ChromaDB(persist_directory="../vector_db", embedding_model="nomic-embed-text")
        # Show all records using metadata search (no query, just get all)
        results = vector_db.get_all_by_metadata(k=1000)
        if results:
            import pandas as pd
            data = []
            for i, doc in enumerate(results):
                row = {"#": i+1, "Content": doc.page_content}
                if hasattr(doc, 'metadata') and isinstance(doc.metadata, dict):
                    row.update(doc.metadata)
                data.append(row)
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info("No records found in the vector DB.")

if __name__ == "__main__":
    main()
