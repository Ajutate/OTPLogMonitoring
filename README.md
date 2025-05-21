# Agentic RAG Log Monitor

## Overview
The Agentic RAG Log Monitor is a chat-based application designed to monitor logs related to the OTP (One-Time Password) journey for specific ORN (Order Reference Number) entries. The application parses log files from various sources, stores relevant information in a vector database, and allows users to query the OTP journey through an interactive chat interface.

## Project Structure
```
agentic-rag-log-monitor
├── src
│   ├── main.py               # Entry point for the application
│   ├── chat_agent.py         # Implementation of the chat agent
│   ├── log_parser            # Module for parsing log files
│   │   ├── __init__.py
│   │   ├── accrossa_parser.py # Parser for Accrossa log files
│   │   ├── axiom_parser.py    # Parser for Axiom log files
│   │   └── e2fa_parser.py     # Parser for e2fa log files
│   ├── vector_db             # Module for vector database interaction
│   │   ├── __init__.py
│   │   └── chroma_db.py      # Functions for Chroma DB interaction
│   ├── ui                    # User interface components
│   │   └── streamlit_app.py   # Streamlit app for user interaction
│   └── types                 # Type definitions for the application
│       └── index.py
├── logs                      # Directory for log files
│   ├── accrossa.log
│   ├── axiom.log
│   └── e2fa.log
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd agentic-rag-log-monitor
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure that the log files are present in the `logs` directory.

## Usage
4. to store data in vector store:
```
python src/main.py
```

5. To launch the Streamlit UI, run:
   ```
   streamlit run src/ui/streamlit_app.py
   ```



Once the application is running, open your web browser and navigate to the provided URL to access the chat interface.

## Features
- **Log Parsing**: The application parses logs from Accrossa, Axiom, and e2fa files to extract relevant information regarding OTP generation, sending, and verification.
- **Chat Interface**: Users can interact with the application through a chat window, querying specific ORN numbers to retrieve detailed OTP journey information.
- **Vector Database**: The application stores parsed log details in a vector database for efficient retrieval and querying.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.