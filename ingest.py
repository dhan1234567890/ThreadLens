import os
import pandas as pd
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

class Neo4jIngestor:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_constraints(self):
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (i:IP) REQUIRE i.address IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:CVE) REQUIRE c.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Technique) REQUIRE t.id IS UNIQUE")

    def ingest_firewall_logs(self, df):
        query = """
        UNWIND $rows AS row
        MERGE (src:IP {address: row.source_ip})
        MERGE (dst:IP {address: row.destination_ip})
        CREATE (src)-[:COMMUNICATED_WITH {
            timestamp: row.timestamp, 
            port: row.port, 
            action: row.action
        }]->(dst)
        """
        with self.driver.session() as session:
            session.run(query, rows=df.to_dict('records'))

    def ingest_ids_alerts(self, df):
        records = df.to_dict('records')
        for row in records:
            for k, v in row.items():
                if pd.isna(v):
                    row[k] = None
        
        query = """
        UNWIND $rows AS row
        MERGE (src:IP {address: row.source_ip})
        MERGE (dst:IP {address: row.destination_ip})
        CREATE (alert:Alert {
            name: row.alert_name,
            timestamp: row.timestamp,
            severity: row.severity
        })
        CREATE (src)-[:TRIGGERED]->(alert)
        CREATE (alert)-[:TARGETED]->(dst)
        
        FOREACH (ignoreMe IN CASE WHEN row.cve IS NOT NULL THEN [1] ELSE [] END |
            MERGE (cve:CVE {id: row.cve})
            MERGE (alert)-[:RELATES_TO_VULNERABILITY]->(cve)
        )
        
        FOREACH (ignoreMe IN CASE WHEN row.mitre_technique IS NOT NULL THEN [1] ELSE [] END |
            MERGE (tech:Technique {id: row.mitre_technique})
            MERGE (alert)-[:USES_TECHNIQUE]->(tech)
        )
        """
        with self.driver.session() as session:
            session.run(query, rows=records)

if __name__ == "__main__":
    print("Connecting to Neo4j...")
    ingestor = Neo4jIngestor(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
    
    print("Creating constraints...")
    ingestor.create_constraints()
    
    if os.path.exists("firewall_logs.csv"):
        print("Ingesting firewall logs...")
        fw_df = pd.read_csv("firewall_logs.csv")
        ingestor.ingest_firewall_logs(fw_df)
        
    if os.path.exists("ids_alerts.csv"):
        print("Ingesting IDS alerts...")
        ids_df = pd.read_csv("ids_alerts.csv")
        ingestor.ingest_ids_alerts(ids_df)
        
    ingestor.close()
    print("Ingestion complete!")
