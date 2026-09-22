import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def find_patient():
    load_dotenv()
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    
    with engine.connect() as conn:
        query = text("""
            SELECT DISTINCT subject_id 
            FROM patient_encounters 
            WHERE subject_id IS NOT NULL AND clinical_embedding IS NOT NULL 
            LIMIT 5;
        """)
        result = conn.execute(query).fetchall()
        
        print("\n🎯 Mapped Patient IDs with Active Vector Embeddings:")
        print("-" * 50)
        if not result:
            print("❌ No patients found with generated embeddings.")
            print("👉 Run: python scripts/04_generate_embeddings.py first!")
        for row in result:
            print(f"  • Patient ID: {row[0]}")
        print("-" * 50)

if __name__ == "__main__":
    find_patient()
