# LLM-Powered Network Threat Analysis Assistant 🛡️

This project is an AI-powered cybersecurity assistant that uses **Graph RAG (Retrieval-Augmented Generation)** to analyze network security data and explain potential cyber threats. 

Instead of traditional vector search, this system structures cybersecurity logs into a **Knowledge Graph**, allowing the Large Language Model (LLM) to understand complex relationships between IP addresses, vulnerabilities (CVEs), malware, and MITRE ATT&CK techniques.

## Current Features (Prototype)
- **Data Ingestion:** Parses mock Firewall and IDS/IPS logs into a graph structure.
- **Knowledge Graph:** Uses **Neo4j** to map relationships (e.g., `IP -> TRIGGERED -> Alert -> USES_TECHNIQUE -> MITRE`).
- **Graph RAG:** Uses **LangChain** to translate natural language questions into Cypher queries to retrieve contextual sub-graphs.
- **Backend API:** Exposes the Graph RAG logic via a **FastAPI** server.
- **Interactive UI:** Provides a chat interface built with **Streamlit** for security analysts to query the data.

## Technology Stack
* **Language:** Python 3
* **Database:** Neo4j (via Docker)
* **LLM Orchestration:** LangChain
* **LLM Provider:** OpenAI (GPT-4o)
* **Backend:** FastAPI & Uvicorn
* **Frontend:** Streamlit
* **Data Processing:** Pandas

---

## How to Run the Project Locally

### 1. Prerequisites
- [Docker & Docker Compose](https://docs.docker.com/get-docker/) installed.
- Python 3.10+ installed.
- An OpenAI API Key.

### 2. Setup Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_actual_api_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
```

### 3. Start the Neo4j Database
Start the database in the background using Docker:
```bash
docker-compose up -d
```
*(You can view the raw graph by visiting `http://localhost:7474` in your browser and logging in with `neo4j` / `password`).*

### 4. Install Dependencies & Ingest Data
Set up your Python virtual environment and run the data ingestion pipeline:
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Generate mock logs and ingest them into Neo4j
python mock_data_gen.py
python ingest.py
```

### 5. Start the Application
You will need two terminal windows/tabs (make sure the virtual environment is activated in both).

**Terminal 1 (Backend API):**
```bash
uvicorn main:app --reload
```

**Terminal 2 (Frontend UI):**
```bash
streamlit run app.py
```

The Streamlit UI will automatically open in your browser, and you can start asking questions about your network traffic!
