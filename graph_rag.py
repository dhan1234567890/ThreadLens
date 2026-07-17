import os
from langchain_community.graphs import Neo4jGraph
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CyberGraphRAG:
    def __init__(self):
        self.graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD
        )
        self.llm = ChatOpenAI(temperature=0, model="gpt-4o", openai_api_key=OPENAI_API_KEY)
        
        # We use GraphCypherQAChain which takes natural language, 
        # converts it to Cypher, queries Neo4j, and returns a natural language response.
        self.chain = GraphCypherQAChain.from_llm(
            cypher_llm=self.llm,
            qa_llm=self.llm,
            graph=self.graph,
            verbose=True,
            allow_dangerous_requests=True # Required for executing Cypher
        )

    def query(self, question: str) -> str:
        try:
            # Refresh schema so LLM knows about our nodes/relationships
            self.graph.refresh_schema()
            response = self.chain.invoke({"query": question})
            return response['result']
        except Exception as e:
            return f"Error executing query: {str(e)}"

if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("Please set OPENAI_API_KEY in your environment.")
    else:
        rag = CyberGraphRAG()
        print(rag.query("What IP addresses have triggered high severity alerts?"))
