from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph_rag import CyberGraphRAG
import uvicorn

app = FastAPI(title="Cybersecurity Assistant API", description="LLM-Powered Graph RAG API")

# Initialize our Graph RAG engine
try:
    rag_engine = CyberGraphRAG()
except Exception as e:
    print(f"Warning: Failed to initialize Graph RAG engine. Check Neo4j and OpenAI API key. Error: {e}")
    rag_engine = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"message": "Cybersecurity Graph RAG Assistant API is running."}

@app.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    if not rag_engine:
        raise HTTPException(status_code=500, detail="Graph RAG engine not initialized. Check server logs.")
    
    answer = rag_engine.query(request.query)
    return {"response": answer}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
